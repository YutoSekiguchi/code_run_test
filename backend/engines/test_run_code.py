#!/usr/bin/env python3
import subprocess
import sys
import os
import json

sys.path.append(os.path.dirname(__file__))
sys.path.append('..')

from app import run_code


def run_sample(sample, deps=None):
    cmd = [sys.executable, 'run_code_docker.py', sample]
    if deps:
        cmd += ['--deps'] + deps
    result = subprocess.run(cmd, text=True, capture_output=True)
    return result.stdout.strip(), result.returncode


def run_node(lang, code, deps=''):
    script = (
        f"const r=require('./server.js');"
        f"process.stdout.write(r.runCode({json.dumps(lang)},{json.dumps(code)},{json.dumps(deps)}));"
    )
    result = subprocess.run(['node', '-e', script], text=True, capture_output=True)
    return result.stdout.strip(), result.returncode


def test_web_python():
    out, rc = run_node('python', "print('OK')")
    assert rc == 0
    assert 'OK' in out


def test_wsgi_python():
    out = run_code('python', "print('WSGI')")
    assert 'WSGI' in out


def test_all_languages():
    """全言語をテスト（FastAPI run_code経由）"""
    tests = [
        ('python', "print('Hello from Python')"),
        ('javascript', "console.log('Hello from JavaScript')"),
        ('ruby', "puts 'Hello from Ruby'"),
        ('c', '#include <stdio.h>\nint main() {\n    printf("Hello from C\\n");\n    return 0;\n}'),
        ('cpp', '#include <iostream>\nint main() {\n    std::cout << "Hello from C++" << std::endl;\n    return 0;\n}'),
        ('java', 'public class Solution {\n    public static void main(String[] args) {\n        System.out.println("Hello from Java");\n    }\n}'),
    ]
    
    for lang, code in tests:
        print(f"\n=== Testing {lang} ===")
        try:
            result = run_code(lang, code)
            print(f"Result: '{result.strip()}'")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == '__main__':
    test_all_languages()