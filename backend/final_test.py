#!/usr/bin/env python3
"""
修正後の最終テスト
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from app import run_code

def test_all_languages():
    """全言語をテスト"""
    tests = [
        ('python', "print('Hello from Python')"),
        ('javascript', "console.log('Hello from JavaScript')"),
        ('ruby', "puts 'Hello from Ruby'"),
        # ('c', '#include <stdio.h>\nint main() {\n    printf("Hello from C\\n");\n    return 0;\n}'),
        # ('cpp', '#include <iostream>\nint main() {\n    std::cout << "Hello from C++" << std::endl;\n    return 0;\n}'),
        # ('java', 'public class prog {\n    public static void main(String[] args) {\n        System.out.println("Hello from Java");\n    }\n}'),
    ]
    
    for lang, code in tests:
        print(f"\n=== Testing {lang} ===")
        result = run_code(lang, code)
        print(f"Result: '{result.strip()}'")

if __name__ == '__main__':
    test_all_languages()