import os
import tempfile
import subprocess
import logging
import base64
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, JSONResponse

logging.basicConfig(level=logging.DEBUG)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LANGUAGE_EXT = {
    'python': '.py',
    'javascript': '.js',
    'ruby': '.rb',
    'php': '.php',
    'c': '.c',
    'cpp': '.cpp',
    'java': '.java',
    'csharp': '.cs',
    'wasm': '.wasm'
}

MAIN_FILE_NAMES = {
    '.py': 'main.py',
    '.js': 'main.js',
    '.rb': 'main.rb',
    '.php': 'main.php',
    '.java': 'Main.java',
    '.c': 'main.c',
    '.cpp': 'main.cpp',
    '.cs': 'Program.cs',
    '.wasm': 'main.cpp'
}

TEMPLATE_FILES = {
    'python': 'solution.py',
    'javascript': 'solution.js',
    'ruby': 'solution.rb',
    'php': 'solution.php',
    'java': 'Solution.java',
    'c': 'solution.c',
    'cpp': 'solution.cpp',
    'csharp': 'solution.cs',
    'wasm': 'solution_wasm.cpp'
}


def run_code(lang, code, deps=''):
    ext = LANGUAGE_EXT.get(lang)
    if not ext:
        return f'Unsupported language: {lang}'
    
    # Handle WebAssembly compilation differently
    if lang == 'wasm':
        return run_wasm(code, deps)
    
    with tempfile.TemporaryDirectory() as tmpdir:
        main_file = MAIN_FILE_NAMES.get(ext, 'prog' + ext)
        path = os.path.join(tmpdir, main_file)
        with open(path, 'w') as f:
            f.write(code)
        run_code_path = os.path.join(os.path.dirname(__file__), 'engines', 'run_code.py')
        import sys
        args = [sys.executable, run_code_path, path]
        dep_list = deps.strip().split()
        if dep_list:
            args += ['--deps'] + dep_list
        
        logging.debug(f"args={args}")
        logging.debug(f"code={code}")
        result = subprocess.run(args, text=True, capture_output=True)
        logging.debug(f"returncode={result.returncode}")
        logging.debug(f"stdout={result.stdout}")
        logging.debug(f"stderr={result.stderr}")
        return result.stdout + result.stderr


def run_wasm(code, deps=''):
    """Handle WebAssembly compilation and return compiled files."""
    from engines.run_code import run_wasm_code
    
    with tempfile.TemporaryDirectory() as tmpdir:
        path = os.path.join(tmpdir, 'main.cpp')
        with open(path, 'w') as f:
            f.write(code)
        
        try:
            result = run_wasm_code(path, deps.strip().split() if deps else [])
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'output': ''
            }


@app.get("/")
async def root():
    return PlainTextResponse("Code Runner API - Use POST to run code")


@app.post("/")
async def run_code_endpoint(
    language: str = Form(...),
    code: str = Form(...),
    deps: str = Form(default="")
):
    output = run_code(language, code, deps)
    return PlainTextResponse(output)


@app.post("/run")
async def run_code_endpoint_alt(
    language: str = Form(...),
    code: str = Form(...),
    deps: str = Form(default="")
):
    output = run_code(language, code, deps)
    if language == 'wasm' and isinstance(output, dict):
        if output['success']:
            # Return WASM compilation result as JSON
            return JSONResponse({
                'success': True,
                'html': output['html'],
                'js': output['js'],
                'wasm': base64.b64encode(output['wasm']).decode('utf-8'),
                'output': output['output']
            })
        else:
            return JSONResponse({
                'success': False,
                'error': output['error'],
                'output': output['output']
            })
    return PlainTextResponse(output)


@app.get("/template/{language}")
async def get_template(language: str):
    template_file = TEMPLATE_FILES.get(language)
    if not template_file:
        return PlainTextResponse(f"Template not found for language: {language}", status_code=404)
    
    template_path = os.path.join(os.path.dirname(__file__), 'templates', 'solution', template_file)
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return PlainTextResponse(content)
    except FileNotFoundError:
        return PlainTextResponse(f"Template file not found: {template_file}", status_code=404)
    except Exception as e:
        return PlainTextResponse(f"Error reading template: {str(e)}", status_code=500)


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get('PORT', '8000'))
    uvicorn.run(app, host="0.0.0.0", port=port)