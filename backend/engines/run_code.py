import os
import sys
import tempfile
import argparse
import shutil
import docker
from pathlib import Path

# Language to Dockerfile mapping
LANGUAGE_DOCKERFILES = {
    '.py': 'Dockerfile.python',
    '.js': 'Dockerfile.javascript', 
    '.java': 'Dockerfile.java',
    '.cpp': 'Dockerfile.cpp',
    '.c': 'Dockerfile.c',
    '.rb': 'Dockerfile.ruby',
}

# Language to main file name mapping
MAIN_FILE_NAMES = {
    '.py': 'main.py',
    '.js': 'main.js',
    '.java': 'Main.java',
    '.cpp': 'main.cpp',
    '.c': 'main.c',
    '.rb': 'main.rb',
}


def run_script(source_path, deps=None):
    """Run code in Docker container"""
    deps = deps or []
    ext = os.path.splitext(source_path)[1]
    
    if ext not in LANGUAGE_DOCKERFILES:
        raise ValueError(f"Unsupported file extension: {ext}")
    
    client = docker.from_env()
    dockerfile_path = os.path.join(os.path.dirname(__file__), 'dockerfiles', LANGUAGE_DOCKERFILES[ext])
    
    if not os.path.exists(dockerfile_path):
        raise FileNotFoundError(f"Dockerfile not found: {dockerfile_path}")
    
    # Create temporary directory for build context
    with tempfile.TemporaryDirectory() as build_context:
        # Copy source file to main file name
        main_file = MAIN_FILE_NAMES[ext]
        shutil.copy2(source_path, os.path.join(build_context, main_file))
        
        # Copy dockerfile to build context
        shutil.copy2(dockerfile_path, os.path.join(build_context, 'Dockerfile'))
        
        # Handle dependencies
        if deps and ext == '.py':
            # Handle local libraries
            local_deps = []
            pip_deps = []
            for dep in deps:
                if os.path.exists(dep):
                    local_deps.append(dep)
                else:
                    pip_deps.append(dep)
            
            # Copy local libraries
            for local_dep in local_deps:
                if os.path.isdir(local_dep):
                    shutil.copytree(local_dep, os.path.join(build_context, os.path.basename(local_dep)))
                else:
                    shutil.copy2(local_dep, build_context)
            
            # Create requirements.txt for pip dependencies
            if pip_deps:
                with open(os.path.join(build_context, 'requirements.txt'), 'w') as f:
                    for dep in pip_deps:
                        f.write(f"{dep}\n")
                
                # Update Dockerfile to install requirements
                with open(os.path.join(build_context, 'Dockerfile'), 'a') as f:
                    f.write("\nCOPY requirements.txt .\n")
                    f.write("RUN pip install -r requirements.txt\n")
            
            # Add pandas stub support
            stub_path = os.path.join(os.path.dirname(__file__), 'libs', 'pandas_stub')
            if os.path.exists(stub_path):
                shutil.copytree(stub_path, os.path.join(build_context, 'pandas_stub'))
                with open(os.path.join(build_context, 'Dockerfile'), 'a') as f:
                    f.write("\nENV PYTHONPATH=/app/pandas_stub:$PYTHONPATH\n")
        
        elif deps and ext == '.js':
            # Handle local and npm dependencies
            local_deps = []
            npm_deps = []
            for dep in deps:
                if os.path.exists(dep):
                    local_deps.append(dep)
                else:
                    npm_deps.append(dep)
            
            # Copy local dependencies
            for local_dep in local_deps:
                if os.path.isdir(local_dep):
                    shutil.copytree(local_dep, os.path.join(build_context, os.path.basename(local_dep)))
                else:
                    shutil.copy2(local_dep, build_context)
            
            # Create package.json for npm dependencies
            if npm_deps:
                package_json = {
                    "name": "code-runner",
                    "version": "1.0.0",
                    "dependencies": {}
                }
                for dep in npm_deps:
                    package_json["dependencies"][dep] = "latest"
                
                import json
                with open(os.path.join(build_context, 'package.json'), 'w') as f:
                    json.dump(package_json, f, indent=2)
                
                # Update Dockerfile to install packages
                with open(os.path.join(build_context, 'Dockerfile'), 'a') as f:
                    f.write("\nCOPY package.json .\n")
                    f.write("RUN npm install\n")
        
        try:
            # Build image
            image_tag = f"code-runner-{ext[1:]}-{os.getpid()}"
            image, build_logs = client.images.build(
                path=build_context,
                tag=image_tag,
                rm=True,
                forcerm=True
            )
            
            # Run container
            container = client.containers.run(
                image_tag,
                remove=True,
                stdout=True,
                stderr=True,
                timeout=30,  # 30 second timeout
                mem_limit="128m",  # Memory limit
                network_disabled=True  # Disable network access
            )
            
            # Print output
            output = container.decode('utf-8')
            print(output, end='')
            
            return 0
            
        except docker.errors.ContainerError as e:
            print(f"{e.stderr.decode('utf-8')}", file=sys.stderr, end='')
            return e.exit_status
        except docker.errors.ImageNotFound:
            print("Docker image not found", file=sys.stderr)
            return 1
        except docker.errors.APIError as e:
            print(f"Docker API error: {e}", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1
        finally:
            # Clean up image
            try:
                client.images.remove(image_tag, force=True)
            except:
                pass


def main():
    parser = argparse.ArgumentParser(description="Run code in various languages")
    parser.add_argument('source', help='Source file to execute')
    parser.add_argument('--deps', nargs='*', default=[], help='Dependencies to install')
    args = parser.parse_args()

    if not os.path.exists(args.source):
        print(f"File not found: {args.source}")
        sys.exit(1)

    try:
        rc = run_script(args.source, args.deps)

        sys.exit(rc)
    except ValueError as exc:
        print(exc)
        sys.exit(1)


if __name__ == '__main__':
    main()
