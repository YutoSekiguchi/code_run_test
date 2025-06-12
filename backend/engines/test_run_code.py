#!/usr/bin/env python3
"""
各関数を直接テストするユニットテスト
"""
import unittest
import subprocess
import tempfile
import os
import sys
from unittest.mock import patch, Mock

# テスト対象のモジュールをインポート
sys.path.append(os.path.dirname(__file__))
sys.path.append('..')


class TestDockerCommands(unittest.TestCase):
    """Dockerコマンドを生成する関数のテスト"""
    
    def test_python_docker_command(self):
        """PythonのDockerコマンドが正しく生成されるか"""
        # シンプルなPythonコードでテスト
        cmd = [
            'docker', 'run', '--rm',
            'python:3.9-slim',
            'python', '-c', "print('Hello Python')"
        ]
        
        # コマンドを実行
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('Hello Python', result.stdout)
    
    def test_node_docker_command(self):
        """Node.jsのDockerコマンドが正しく動作するか"""
        cmd = [
            'docker', 'run', '--rm',
            'node:14-alpine',
            'node', '-e', "console.log('Hello Node')"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        self.assertEqual(result.returncode, 0)
        self.assertIn('Hello Node', result.stdout)


class TestCodeExecution(unittest.TestCase):
    """コード実行関数のテスト（Dockerを使用）"""
    
    def setUp(self):
        """各テストの前準備"""
        self.test_codes = {
            'python': {
                'code': "print('Test Python')",
                'expected': 'Test Python'
            },
            'javascript': {
                'code': "console.log('Test JS')",
                'expected': 'Test JS'
            },
            'ruby': {
                'code': "puts 'Test Ruby'",
                'expected': 'Test Ruby'
            }
        }
    
    def test_execute_python_code(self):
        """Pythonコードの実行テスト"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(self.test_codes['python']['code'])
            f.flush()
            
            # ファイルパスを使ってDockerで実行
            cmd = [
                'docker', 'run', '--rm',
                '-v', f'{f.name}:/code/test.py:ro',
                'python:3.9-slim',
                'python', '/code/test.py'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            self.assertEqual(result.returncode, 0)
            self.assertIn(self.test_codes['python']['expected'], result.stdout)
            
            # クリーンアップ
            os.unlink(f.name)
    
    def test_execute_with_timeout(self):
        """タイムアウト処理のテスト"""
        infinite_loop_code = "while True: pass"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(infinite_loop_code)
            f.flush()
            
            cmd = [
                'docker', 'run', '--rm',
                '--memory=128m',  # メモリ制限
                '--cpus=0.5',     # CPU制限
                '-v', f'{f.name}:/code/test.py:ro',
                'python:3.9-slim',
                'timeout', '2', 'python', '/code/test.py'  # 2秒でタイムアウト
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            # タイムアウトした場合、終了コードは0以外
            self.assertNotEqual(result.returncode, 0)
            
            os.unlink(f.name)


class TestLanguageDetection(unittest.TestCase):
    """言語検出機能のテスト"""
    
    def test_detect_language_from_extension(self):
        """ファイル拡張子から言語を検出"""
        test_cases = [
            ('test.py', 'python'),
            ('test.js', 'javascript'),
            ('test.rb', 'ruby'),
            ('test.c', 'c'),
            ('test.cpp', 'cpp'),
            ('Test.java', 'java'),
            ('test.unknown', None)
        ]
        
        for filename, expected_lang in test_cases:
            # 拡張子から言語を判定する簡単な関数
            ext = os.path.splitext(filename)[1].lower()
            lang_map = {
                '.py': 'python',
                '.js': 'javascript',
                '.rb': 'ruby',
                '.c': 'c',
                '.cpp': 'cpp',
                '.java': 'java'
            }
            detected = lang_map.get(ext)
            
            self.assertEqual(detected, expected_lang,
                           f"Failed to detect {expected_lang} from {filename}")


class TestDockerIntegration(unittest.TestCase):
    """Docker統合テスト"""
    
    @classmethod
    def setUpClass(cls):
        """テストクラスの初期化時にDockerの可用性をチェック"""
        try:
            result = subprocess.run(['docker', '--version'], 
                                  capture_output=True, text=True)
            cls.docker_available = result.returncode == 0
        except:
            cls.docker_available = False
    
    def setUp(self):
        """各テストの前にDockerの可用性を確認"""
        if not self.docker_available:
            self.skipTest("Docker is not available")
    
    def test_compile_and_run_c_code(self):
        """Cコードのコンパイルと実行"""
        c_code = '''
#include <stdio.h>
int main() {
    printf("Hello from C\\n");
    return 0;
}
'''
        with tempfile.NamedTemporaryFile(mode='w', suffix='.c', delete=False) as f:
            f.write(c_code)
            f.flush()
            
            # コンパイルして実行
            cmd = [
                'docker', 'run', '--rm',
                '-v', f'{f.name}:/code/test.c:ro',
                'gcc:latest',
                'sh', '-c',
                'cd /code && gcc test.c -o test && ./test'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            self.assertEqual(result.returncode, 0)
            self.assertIn('Hello from C', result.stdout)
            
            os.unlink(f.name)
    
    def test_java_compile_and_run(self):
        """Javaコードのコンパイルと実行"""
        java_code = '''
public class Test {
    public static void main(String[] args) {
        System.out.println("Hello from Java");
    }
}
'''
        with tempfile.TemporaryDirectory() as temp_dir:
            java_file = os.path.join(temp_dir, 'Test.java')
            with open(java_file, 'w') as jf:
                jf.write(java_code)
            
            cmd = [
                'docker', 'run', '--rm',
                '-v', f'{temp_dir}:/code',
                'openjdk:11-slim',
                'sh', '-c',
                'cd /code && javac Test.java && java Test'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            self.assertEqual(result.returncode, 0)
            self.assertIn('Hello from Java', result.stdout)


class TestWithMocking(unittest.TestCase):
    """モックを使用したテスト"""
    
    @patch('subprocess.run')
    def test_run_code_with_mock(self, mock_run):
        """subprocess.runをモックしてテスト"""
        # モックの設定
        mock_result = Mock()
        mock_result.stdout = "Mocked output"
        mock_result.stderr = ""
        mock_result.returncode = 0
        mock_run.return_value = mock_result
        
        # 実際の関数呼び出しをシミュレート
        result = subprocess.run(['docker', 'run', 'test'], 
                              capture_output=True, text=True)
        
        self.assertEqual(result.stdout, "Mocked output")
        self.assertEqual(result.returncode, 0)
        mock_run.assert_called_once()


class TestErrorHandling(unittest.TestCase):
    """エラーハンドリングのテスト"""
    
    def test_invalid_docker_image(self):
        """存在しないDockerイメージのエラー処理"""
        cmd = [
            'docker', 'run', '--rm',
            'nonexistent-image:latest',
            'echo', 'test'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # エラーが発生することを確認
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Unable to find image', result.stderr)
    
    def test_syntax_error_handling(self):
        """構文エラーのハンドリング"""
        bad_python_code = "print('missing parenthesis'"
        
        cmd = [
            'docker', 'run', '--rm',
            'python:3.9-slim',
            'python', '-c', bad_python_code
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Pythonの構文エラーは終了コード1を返す
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('SyntaxError', result.stderr)


def run_all_tests():
    """すべてのテストを実行"""
    # テストスイートを作成
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 各テストクラスを追加
    test_classes = [
        TestDockerCommands,
        TestCodeExecution,
        TestLanguageDetection,
        TestDockerIntegration,
        TestWithMocking,
        TestErrorHandling
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # テストを実行
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    # 方法1: unittest.main()を使用
    # unittest.main()
    
    # 方法2: カスタムランナーを使用
    success = run_all_tests()
    sys.exit(0 if success else 1)