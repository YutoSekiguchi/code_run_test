import os
import sys
import tempfile
import argparse
import shutil
import docker
from pathlib import Path

# Language configurations with base image tags
LANGUAGE_CONFIGS = {
    '.py': {
        'base_image': 'code-runner-python-base',
        'main_file': 'main.py',
        'dockerfile': 'Dockerfile.python'
    },
    '.js': {
        'base_image': 'code-runner-js-base',
        'main_file': 'main.js', 
        'dockerfile': 'Dockerfile.javascript'
    },
    '.rb': {
        'base_image': 'code-runner-ruby-base',
        'main_file': 'main.rb',
        'dockerfile': 'Dockerfile.ruby'
    },
    '.java': {
        'base_image': 'code-runner-java-base',
        'main_file': 'Solution.java',
        'dockerfile': 'Dockerfile.java'
    },
    '.c': {
        'base_image': 'code-runner-c-base',
        'main_file': 'main.c',
        'dockerfile': 'Dockerfile.c'
    },
    '.cpp': {
        'base_image': 'code-runner-cpp-base',
        'main_file': 'main.cpp',
        'dockerfile': 'Dockerfile.cpp'
    }
}


def ensure_base_image_exists(client, ext):
    """Ensure the base image for the language exists, build if necessary."""
    config = LANGUAGE_CONFIGS[ext]
    base_image = config['base_image']
    
    try:
        # Check if base image exists
        client.images.get(base_image)
        return True
    except docker.errors.ImageNotFound:
        
        # Build base image
        script_dir = Path(__file__).parent.parent
        dockerfiles_dir = script_dir / 'dockerfiles'
        dockerfile_path = dockerfiles_dir / config['dockerfile']
        
        if not dockerfile_path.exists():
            raise FileNotFoundError(f"Dockerfile not found: {dockerfile_path}")
        
        try:
            client.images.build(
                path=str(dockerfiles_dir),
                dockerfile=config['dockerfile'],
                tag=base_image,
                rm=True,
                forcerm=True
            )
            return True
        except Exception as e:
            print(f"Failed to build base image: {e}")
            return False


def run_code_in_docker(source_path, deps=None):
    """Run code in Docker container using pre-built base images."""
    deps = deps or []
    ext = os.path.splitext(source_path)[1]
    
    if ext not in LANGUAGE_CONFIGS:
        raise ValueError(f"Unsupported file extension: {ext}")
    
    client = docker.from_env()
    config = LANGUAGE_CONFIGS[ext]
    
    # Ensure base image exists
    if not ensure_base_image_exists(client, ext):
        raise RuntimeError(f"Failed to ensure base image for {ext}")
    
    # Create temporary directory for code execution
    with tempfile.TemporaryDirectory() as temp_dir:
        # Copy source file to temp directory with expected name
        main_file = config['main_file']
        temp_code_path = os.path.join(temp_dir, main_file)
        shutil.copy2(source_path, temp_code_path)
        
        
        # Handle dependencies if provided
        if deps and ext == '.py':
            # Create requirements.txt for Python dependencies
            requirements_path = os.path.join(temp_dir, 'requirements.txt')
            with open(requirements_path, 'w') as f:
                for dep in deps:
                    if not os.path.exists(dep):  # Only add non-local dependencies
                        f.write(f"{dep}\n")
            
            # Install dependencies in container before running code
            if os.path.getsize(requirements_path) > 0:
                try:
                    # Run pip install in temporary container
                    client.containers.run(
                        config['base_image'],
                        f"pip install -r /app/requirements.txt",
                        volumes={temp_dir: {'bind': '/app', 'mode': 'rw'}},
                        working_dir='/app',
                        remove=True
                    )
                except Exception as e:
                    print(f"Warning: Failed to install dependencies: {e}")
        
        elif deps and ext == '.js':
            # Handle Node.js dependencies
            package_json = {
                "name": "code-runner",
                "version": "1.0.0",
                "dependencies": {}
            }
            for dep in deps:
                if not os.path.exists(dep):  # Only add non-local dependencies 
                    package_json["dependencies"][dep] = "latest"
            
            if package_json["dependencies"]:
                import json
                package_path = os.path.join(temp_dir, 'package.json')
                with open(package_path, 'w') as f:
                    json.dump(package_json, f, indent=2)
                
                try:
                    # Run npm install in temporary container
                    client.containers.run(
                        config['base_image'],
                        "npm install",
                        volumes={temp_dir: {'bind': '/app', 'mode': 'rw'}},
                        working_dir='/app',
                        remove=True
                    )
                except Exception as e:
                    print(f"Warning: Failed to install dependencies: {e}")
        
        try:
            # Determine the command to run based on language
            if ext == '.py':
                cmd = f"python {main_file}"
            elif ext == '.js':
                cmd = f"node {main_file}"
            elif ext == '.rb':
                cmd = f"ruby {main_file}"
            elif ext == '.java':
                cmd = f"sh -c 'javac {main_file} && java Solution'"
            elif ext == '.c':
                cmd = f"sh -c 'gcc -o main {main_file} -lm && ./main'"
            elif ext == '.cpp':
                cmd = f"sh -c 'g++ -o main {main_file} && ./main'"
            else:
                cmd = f"echo 'Unsupported language: {ext}'"
            
            # Run container with volume mount
            # Use read-write for compiled languages, read-only for interpreted
            volume_mode = 'rw' if ext in ['.java', '.c', '.cpp'] else 'ro'
            container = client.containers.run(
                config['base_image'],
                cmd,
                volumes={temp_dir: {'bind': '/app', 'mode': volume_mode}},
                working_dir='/app',
                remove=True,
                stdout=True,
                stderr=True,
                mem_limit="128m",
                network_disabled=True
            )
            
            # Print output
            output = container.decode('utf-8')
            print(output, end='')
            
            return 0
            
        except docker.errors.ContainerError as e:
            print(f"Container error: {e.stderr.decode('utf-8')}", file=sys.stderr)
            return e.exit_status
        except docker.errors.ImageNotFound:
            print("Docker image not found", file=sys.stderr)
            return 1
        except docker.errors.APIError as e:
            print(f"Docker API error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Unexpected error: {e}", file=sys.stderr)
            return 1


def main():
    parser = argparse.ArgumentParser(description="Run code in Docker containers")
    parser.add_argument('source', help='Source file to execute')
    parser.add_argument('--deps', nargs='*', default=[], help='Dependencies to install')
    args = parser.parse_args()
    
    if not os.path.exists(args.source):
        print(f"File not found: {args.source}")
        sys.exit(1)
    
    try:
        rc = run_code_in_docker(args.source, args.deps)
        sys.exit(rc)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()