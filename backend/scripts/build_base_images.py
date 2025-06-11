#!/usr/bin/env python3
"""
Build base Docker images for all supported languages.
This script builds images once and they can be reused for code execution.
"""

import os
import docker
import sys
from pathlib import Path

# Language configurations
LANGUAGE_CONFIGS = {
    'python': {
        'dockerfile': 'Dockerfile.python',
        'image_tag': 'code-runner-python-base',
        'main_file': 'main.py'
    },
    'javascript': {
        'dockerfile': 'Dockerfile.javascript', 
        'image_tag': 'code-runner-js-base',
        'main_file': 'main.js'
    },
    'ruby': {
        'dockerfile': 'Dockerfile.ruby',
        'image_tag': 'code-runner-ruby-base', 
        'main_file': 'main.rb'
    },
    'java': {
        'dockerfile': 'Dockerfile.java',
        'image_tag': 'code-runner-java-base',
        'main_file': 'Main.java'
    },
    'c': {
        'dockerfile': 'Dockerfile.c',
        'image_tag': 'code-runner-c-base',
        'main_file': 'main.c'
    },
    'cpp': {
        'dockerfile': 'Dockerfile.cpp',
        'image_tag': 'code-runner-cpp-base',
        'main_file': 'main.cpp'
    }
}


def build_base_images():
    """Build all base Docker images for supported languages."""
    client = docker.from_env()
    script_dir = Path(__file__).parent
    dockerfiles_dir = script_dir.parent / 'dockerfiles'
    
    if not dockerfiles_dir.exists():
        print(f"Error: Dockerfiles directory not found: {dockerfiles_dir}")
        return False
    
    success_count = 0
    total_count = len(LANGUAGE_CONFIGS)
    
    for lang, config in LANGUAGE_CONFIGS.items():
        dockerfile_path = dockerfiles_dir / config['dockerfile']
        
        if not dockerfile_path.exists():
            print(f"Warning: Dockerfile not found for {lang}: {dockerfile_path}")
            continue
            
        try:
            print(f"Building base image for {lang}...")
            
            # Check if image already exists
            try:
                existing_image = client.images.get(config['image_tag'])
                print(f"  Image {config['image_tag']} already exists, skipping...")
                success_count += 1
                continue
            except docker.errors.ImageNotFound:
                pass  # Image doesn't exist, continue with build
            
            # Build the image
            image, build_logs = client.images.build(
                path=str(dockerfiles_dir),
                dockerfile=config['dockerfile'],
                tag=config['image_tag'],
                rm=True,
                forcerm=True,
                quiet=False
            )
            
            print(f"  ✓ Successfully built {config['image_tag']}")
            success_count += 1
            
        except Exception as e:
            print(f"  ✗ Failed to build {lang} image: {e}")
    
    print(f"\nBuild summary: {success_count}/{total_count} images built successfully")
    return success_count == total_count


def list_images():
    """List all code-runner base images."""
    client = docker.from_env()
    
    print("Code Runner Base Images:")
    print("-" * 40)
    
    for lang, config in LANGUAGE_CONFIGS.items():
        try:
            image = client.images.get(config['image_tag'])
            created = image.attrs['Created'][:19].replace('T', ' ')
            size_mb = round(image.attrs['Size'] / (1024 * 1024), 1)
            print(f"{lang:<12} {config['image_tag']:<25} {created} {size_mb:>6}MB")
        except docker.errors.ImageNotFound:
            print(f"{lang:<12} {config['image_tag']:<25} NOT BUILT")


def clean_images():
    """Remove all code-runner base images."""
    client = docker.from_env()
    
    removed_count = 0
    for lang, config in LANGUAGE_CONFIGS.items():
        try:
            client.images.remove(config['image_tag'], force=True)
            print(f"✓ Removed {config['image_tag']}")
            removed_count += 1
        except docker.errors.ImageNotFound:
            print(f"- {config['image_tag']} not found")
        except Exception as e:
            print(f"✗ Failed to remove {config['image_tag']}: {e}")
    
    print(f"\nRemoved {removed_count} images")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "build":
            build_base_images()
        elif command == "list":
            list_images()
        elif command == "clean":
            clean_images()
        else:
            print("Usage: python build_base_images.py [build|list|clean]")
    else:
        build_base_images()