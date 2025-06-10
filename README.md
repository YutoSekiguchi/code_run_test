# code_run_test

This repository contains a simple Python script that can execute source files written in multiple programming languages. The script detects the language by the file extension and invokes the appropriate interpreter or compiler.

## Supported languages

- Python (`.py`)
- JavaScript (`.js`)
- Ruby (`.rb`)
- PHP (`.php`)
- Perl (`.pl`)
- C (`.c`)
- C++ (`.cpp`)
- Java (`.java`)

## Command line usage

```
python run_code.py <path to source file>
```

Example:

```
python run_code.py samples/hello.py
```

The repository includes a `samples` directory with small example programs for each supported language.

### Installing dependencies

Use the `--deps` option to specify packages to install before running the program:

```
python run_code.py samples/use_local.py --deps libs/localpkg
```

The runner installs Python packages with `pip` and JavaScript packages with `npm` into a temporary directory and adjusts environment variables so the executed program can import them.

## Web interface

The `server.js` script offers a tiny web UI using Node's built-in `http` module. Start it with:

```
node server.js
```

Then open `http://localhost:8000` in your browser, choose a language, paste your code, and click **Run** to execute it.
You can also list dependencies in the **Dependencies** field (space separated) before running.
