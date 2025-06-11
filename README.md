# code_run_test

A multi-language code execution platform with a React frontend and FastAPI backend. Execute code in multiple programming languages through a modern web interface with Docker-based security.

## Project Structure

- `backend/` - FastAPI server and code execution engine
- `frontend/` - React + Vite frontend application
- `docker-compose.yml` - Docker orchestration

## Supported languages

- Python (`.py`)
- JavaScript (`.js`)
- Ruby (`.rb`)
- C (`.c`)
- C++ (`.cpp`)
- Java (`.java`)

## Getting Started

### Docker Setup (Recommended)

1. Start all services with Docker Compose:
```bash
docker-compose up -d
```

This will start:
- Backend API server at `http://localhost:8000`
- Frontend application at `http://localhost:3000`

2. Stop services:
```bash
docker-compose down
```

### Manual Setup (Development)

#### Backend Setup

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
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

#### Frontend Setup

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

## Command Line Usage

You can run code directly from the command line using two execution modes:

### Standard Execution
```bash
cd backend
python run_code.py <path to source file>
```

### Docker-based Execution (Secure)
```bash
cd backend
python run_code_docker.py <path to source file>
```

Examples:
```bash
python run_code.py samples/hello.py
python run_code_docker.py samples/hello.rb
```

### Installing dependencies

Use the `--deps` option to specify packages to install before running:

```bash
python run_code.py samples/use_local.py --deps libs/localpkg
python run_code_docker.py samples/use_pandas.py --deps pandas
```

The runner installs Python packages with `pip` and JavaScript packages with `npm`. Docker mode provides additional security isolation.

### Built-in packages

The runner exposes a stub of the `pandas` library without needing to install it. Programs can `import pandas as pd` straight away. C programs are compiled with the math library (`-lm`) linked by default.

## API Endpoints

- `GET /` - API status
- `POST /` - Execute code (form-data: language, code, deps)
- `POST /run` - Alternative endpoint for code execution

## Features

- ✅ Multi-language support (Python, JavaScript, Ruby, C, C++, Java)
- ✅ React frontend with modern UI
- ✅ FastAPI backend with CORS support
- ✅ Docker-based secure code execution
- ✅ Docker Compose orchestration
- ✅ Dependency installation (pip, npm) 
- ✅ Built-in pandas stub
- ✅ Real-time code execution
- ✅ Error handling and output display
- ✅ Memory and network isolation in Docker mode

## Architecture

- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **Backend**: FastAPI + Python + Docker
- **Execution**: Isolated Docker containers for security
- **Languages**: Multiple runtime environments via Docker images

