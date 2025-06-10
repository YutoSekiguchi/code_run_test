import os
import tempfile
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

LANGUAGE_EXT = {
    'python': '.py',
    'javascript': '.js',
    'ruby': '.rb',
    'php': '.php',
    'perl': '.pl',
    'c': '.c',
    'cpp': '.cpp',
    'java': '.java'
}


def run_code(lang, code, deps=''):
    ext = LANGUAGE_EXT.get(lang)
    if not ext:
        return f'Unsupported language: {lang}'
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, 'prog' + ext)
        with open(path, 'w') as f:
            f.write(code)
        run_code_path = os.path.join(os.path.dirname(__file__), 'run_code.py')
        args = ['/usr/bin/python3', run_code_path, path]
        dep_list = deps.strip().split()
        if dep_list:
            args += ['--deps'] + dep_list
        
        print(f"DEBUG run_code: args={args}")
        print(f"DEBUG run_code: file contents={code}")
        print(f"DEBUG run_code: run_code_path exists={os.path.exists(run_code_path)}")
        
        result = subprocess.run(args, text=True, capture_output=True)
        
        print(f"DEBUG run_code: returncode={result.returncode}")
        print(f"DEBUG run_code: stdout={result.stdout}")
        print(f"DEBUG run_code: stderr={result.stderr}")
        
        return result.stdout + result.stderr


class CodeRunnerHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/plain')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(b'Code Runner API - Use POST to run code')

    def do_POST(self):
        if self.path == '/' or self.path == '/run':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            params = parse_qs(post_data)
            
            lang = params.get('language', [''])[0]
            code = params.get('code', [''])[0]
            deps = params.get('deps', [''])[0]
            
            # デバッグ出力
            print(f"DEBUG: Received POST data: {post_data}")
            print(f"DEBUG: Parsed params: {params}")
            print(f"DEBUG: lang={lang}, code={code[:50]}...")
            
            output = run_code(lang, code, deps)
            
            # デバッグ出力
            print(f"DEBUG: output={output[:100]}...")
            
            self.send_response(200)
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(output.encode())
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', '8000'))
    server = HTTPServer(('', port), CodeRunnerHandler)
    print(f'Server running on port {port}')
    server.serve_forever()