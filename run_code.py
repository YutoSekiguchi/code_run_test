import os
import sys
import subprocess
import tempfile
import argparse

LANG_RUNNERS = {
    '.py': ['python3'],
    '.js': ['node'],
    '.rb': ['ruby'],
    '.php': ['php'],
    '.pl': ['perl'],
}

COMPILED_LANGUAGES = {
    '.c': {
        'compile': ['gcc', '{src}', '-o', '{out}', '-lm'],
        'run': ['{out}']
    },
    '.cpp': {
        'compile': ['g++', '{src}', '-o', '{out}', '-lm'],
        'run': ['{out}']
    },
    '.java': {
        'compile': ['javac', '-d', '{outdir}', '{src}'],
        'run': ['java', '-cp', '{outdir}', '{classname}']
    }
}


def run_command(cmd, env=None, cwd=None):
    result = subprocess.run(cmd, text=True, capture_output=True, env=env, cwd=cwd)
    print(result.stdout, end='')
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode


def install_dependencies(ext, deps, depdir):
    env = {}
    if not deps:
        return env
    if ext == '.py':
        local_paths = []
        install_deps = []
        for d in deps:
            if os.path.exists(d):
                local_paths.append(os.path.abspath(d))
            else:
                install_deps.append(d)
        if install_deps:
            run_command(['pip', 'install', '--target', depdir] + install_deps)
            local_paths.append(depdir)
        env['PYTHONPATH'] = os.pathsep.join(local_paths)
    elif ext == '.js':
        run_command(['npm', 'init', '-y'], cwd=depdir)
        dep_args = []
        for d in deps:
            if os.path.exists(d):
                dep_args.append(os.path.abspath(d))
            else:
                dep_args.append(d)
        run_command(['npm', 'install', '--prefix', depdir] + dep_args)
        env['NODE_PATH'] = os.path.join(depdir, 'node_modules')
    return env


def run_script(path, deps=None):
    deps = deps or []
    ext = os.path.splitext(path)[1]
    with tempfile.TemporaryDirectory() as depdir:
        env = os.environ.copy()

        if ext == '.py':
            stub = os.path.join(os.path.dirname(__file__), 'libs', 'pandas_stub')
            env['PYTHONPATH'] = os.pathsep.join(filter(None, [stub, env.get('PYTHONPATH', '')]))

        env.update(install_dependencies(ext, deps, depdir))

        if ext in LANG_RUNNERS:
            cmd = LANG_RUNNERS[ext] + [path]
            return run_command(cmd, env=env)
        elif ext in COMPILED_LANGUAGES:
            config = COMPILED_LANGUAGES[ext]
            with tempfile.TemporaryDirectory() as tmpdir:
                out = os.path.join(tmpdir, 'prog')
                classname = os.path.splitext(os.path.basename(path))[0]
                compile_cmd = [arg.format(src=path, out=out, outdir=tmpdir, classname=classname) for arg in config['compile']]
                rc = run_command(compile_cmd, env=env)
                if rc != 0:
                    return rc
                run_cmd = [arg.format(src=path, out=out, outdir=tmpdir, classname=classname) for arg in config['run']]
                return run_command(run_cmd, env=env)
        else:
            raise ValueError(f"Unsupported file extension: {ext}")


def main():
    parser = argparse.ArgumentParser(description="Run code in various languages")
    parser.add_argument('source', help='Source file to execute')
    parser.add_argument('--deps', nargs='*', default=[], help='Dependencies to install')
    args = parser.parse_args()

    if not os.path.exists(args.source):
        print(f"File not found: {args.source}")
        sys.exit(1)

    try:
        rc = run_script(args.source, args.deps)

        sys.exit(rc)
    except ValueError as exc:
        print(exc)
        sys.exit(1)


if __name__ == '__main__':
    main()
