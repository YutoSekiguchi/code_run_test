import os
import tempfile
import subprocess
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

HTML_FORM = """<!doctype html>
<title>Code Runner</title>
<form method='post'>
<select name='language'>
{}\n</select><br>
<textarea name='code' rows='10' cols='40'></textarea><br>
<input type='text' name='deps' placeholder='Dependencies (space separated)'><br>
<input type='submit' value='Run'>
</form>"""


def run_code(lang, code, deps=''):
    ext = LANGUAGE_EXT.get(lang)
    if not ext:
        return f'Unsupported language: {lang}'
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, 'prog' + ext)
        with open(path, 'w') as f:
            f.write(code)
        args = ['python3', 'run_code.py', path]
        dep_list = deps.strip().split()
        if dep_list:
            args += ['--deps'] + dep_list
        result = subprocess.run(args, text=True, capture_output=True)
        return result.stdout + result.stderr


def application(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        size = int(environ.get('CONTENT_LENGTH', 0) or 0)
        data = environ['wsgi.input'].read(size)
        params = parse_qs(data.decode())
        lang = params.get('language', [''])[0]
        code = params.get('code', [''])[0]
        deps = params.get('deps', [''])[0]
        output = run_code(lang, code, deps)
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [output.encode()]
    else:
        options = '\n'.join(f"<option value='{l}'>{l}</option>" for l in LANGUAGE_EXT)
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [HTML_FORM.format(options).encode()]


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    port = int(os.environ.get('PORT', '8000'))
    with make_server('', port, application) as httpd:
        print(f'Server running on port {port}')
        httpd.serve_forever()
