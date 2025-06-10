import subprocess
import sys



def run_sample(sample, deps=None):
    cmd = [sys.executable, 'run_code.py', sample]
    if deps:
        cmd += ['--deps'] + deps
    result = subprocess.run(cmd, text=True, capture_output=True)
    return result.stdout.strip(), result.returncode


def test_python_sample():
    out, rc = run_sample('samples/hello.py')
    assert rc == 0
    assert out == 'Hello from Python'



def run_node(lang, code, deps=''):
    import json
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



def test_python_with_dep():
    out, rc = run_sample('samples/use_local.py', ['libs/localpkg'])
    assert rc == 0
    assert out == '42'


def test_node_with_dep():
    out, rc = run_node('javascript', "const rev=require('stringer');console.log(rev('abc'));", 'libs/stringer')
    assert rc == 0
    assert 'cba' in out


def test_wsgi_python():
    from app import run_code as wsgi_run
    out = wsgi_run('python', "print('WSGI')")
    assert 'WSGI' in out

