import subprocess
import sys


def run_sample(sample):
    result = subprocess.run([sys.executable, 'run_code.py', sample], text=True, capture_output=True)
    return result.stdout.strip(), result.returncode


def test_python_sample():
    out, rc = run_sample('samples/hello.py')
    assert rc == 0
    assert out == 'Hello from Python'


def run_node(lang, code):
    script = f"const r=require('./server.js');process.stdout.write(r.runCode('{lang}',`{code}`));"
    result = subprocess.run(['node', '-e', script], text=True, capture_output=True)
    return result.stdout.strip(), result.returncode


def test_web_python():
    out, rc = run_node('python', "print('OK')")
    assert rc == 0
    assert 'OK' in out
