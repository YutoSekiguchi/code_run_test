import subprocess
import sys



def run_sample(sample, deps=None):
    cmd = [sys.executable, '../engines/run_code_docker.py', sample]
    if deps:
        cmd += ['--deps'] + deps
    result = subprocess.run(cmd, text=True, capture_output=True)
    return result.stdout.strip(), result.returncode


def test_web_python():
    out, rc = run_node('python', "print('OK')")
    assert rc == 0
    assert 'OK' in out


def run_node(lang, code, deps=''):
    import json
    script = (
        f"const r=require('./server.js');"
        f"process.stdout.write(r.runCode({json.dumps(lang)},{json.dumps(code)},{json.dumps(deps)}));"
    )
    result = subprocess.run(['node', '-e', script], text=True, capture_output=True)
    return result.stdout.strip(), result.returncode


def test_wsgi_python():
    import sys
    sys.path.append('..')
    from app import run_code as wsgi_run
    out = wsgi_run('python', "print('WSGI')")
    assert 'WSGI' in out

