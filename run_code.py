import os
import sys
import subprocess
import tempfile

LANG_RUNNERS = {
    '.py': ['python3'],
    '.js': ['node'],
    '.rb': ['ruby'],
    '.php': ['php'],
    '.pl': ['perl'],
}

COMPILED_LANGUAGES = {
    '.c': {
        'compile': ['gcc', '{src}', '-o', '{out}'],
        'run': ['{out}']
    },
    '.cpp': {
        'compile': ['g++', '{src}', '-o', '{out}'],
        'run': ['{out}']
    },
    '.java': {
        'compile': ['javac', '-d', '{outdir}', '{src}'],
        'run': ['java', '-cp', '{outdir}', '{classname}']
    }
}

def run_command(cmd):
    result = subprocess.run(cmd, text=True, capture_output=True)
    print(result.stdout, end='')
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode

def run_script(path):
    ext = os.path.splitext(path)[1]
    if ext in LANG_RUNNERS:
        cmd = LANG_RUNNERS[ext] + [path]
        return run_command(cmd)
    elif ext in COMPILED_LANGUAGES:
        config = COMPILED_LANGUAGES[ext]
        with tempfile.TemporaryDirectory() as tmpdir:
            out = os.path.join(tmpdir, 'prog')
            classname = os.path.splitext(os.path.basename(path))[0]
            compile_cmd = [arg.format(src=path, out=out, outdir=tmpdir, classname=classname) for arg in config['compile']]
            rc = run_command(compile_cmd)
            if rc != 0:
                return rc
            run_cmd = [arg.format(src=path, out=out, outdir=tmpdir, classname=classname) for arg in config['run']]
            return run_command(run_cmd)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python run_code.py <source_file>")
        sys.exit(1)
    source = sys.argv[1]
    if not os.path.exists(source):
        print(f"File not found: {source}")
        sys.exit(1)
    try:
        rc = run_script(source)
        sys.exit(rc)
    except ValueError as exc:
        print(exc)
        sys.exit(1)


if __name__ == '__main__':
    main()
