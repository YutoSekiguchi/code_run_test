# code_run_test

A multi-language code execution platform with a React frontend and FastAPI backend. Execute code in multiple programming languages through a modern web interface.

## Project Structure

- `backend/` - FastAPI server and code execution engine
- `frontend/` - React + Vite frontend application

## Supported languages

- Python (`.py`)
- JavaScript (`.js`)
- Ruby (`.rb`)
- PHP (`.php`)
- Perl (`.pl`)
- C (`.c`)
- C++ (`.cpp`)
- Java (`.java`)

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the FastAPI server:
```bash
python app.py
```
or
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

The API server will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Command Line Usage

You can also run code directly from the command line:

```bash
cd backend
python run_code.py <path to source file>
```

Example:
```bash
python run_code.py samples/hello.py
```

### Installing dependencies

Use the `--deps` option to specify packages to install before running:

```bash
python run_code.py samples/use_local.py --deps libs/localpkg
```

The runner installs Python packages with `pip` and JavaScript packages with `npm` into a temporary directory and adjusts environment variables so the executed program can import them.

### Built-in packages

The runner exposes a very small stub of the `pandas` library without needing to install it. Programs can `import pandas as pd` straight away. C programs are compiled with the math library (`-lm`) linked by default.

## API Endpoints

- `GET /` - API status
- `POST /` - Execute code (form-data: language, code, deps)
- `POST /run` - Alternative endpoint for code execution

## Features

- ✅ Multi-language support
- ✅ React frontend with syntax highlighting
- ✅ FastAPI backend with CORS support
- ✅ Dependency installation (pip, npm)
- ✅ Built-in pandas stub
- ✅ Real-time code execution
- ✅ Error handling and output display

