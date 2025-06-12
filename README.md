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
- PHP (`.php`)
- C (`.c`)
- C++ (`.cpp`)
- Java (`.java`)
- C# (`.cs`)

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

### Docker-based Execution (Secure)
```bash
cd backend
python engines/run_code.py <path to source file>
```

Examples:
```bash
python engines/run_code.py templates/solution/solution.py
python engines/run_code.py templates/fibonacci/fibonacci.js
```

### Installing dependencies

Use the `--deps` option to specify packages to install before running:

```bash
python engines/run_code.py templates/solution/solution.py --deps pandas
python engines/run_code.py templates/fibonacci/fibonacci.js --deps lodash
```

The runner installs Python packages with `pip` and JavaScript packages with `npm`. Docker mode provides additional security isolation.

### Built-in packages

The runner exposes a stub of the `pandas` library without needing to install it. Programs can `import pandas as pd` straight away. C programs are compiled with the math library (`-lm`) linked by default.

## API Endpoints

- `GET /` - API status
- `POST /` - Execute code (form-data: language, code, deps)
- `POST /run` - Alternative endpoint for code execution
- `GET /template/{language}` - Get template code for a language

## Features

- ✅ Multi-language support (Python, JavaScript, Ruby, PHP, C, C++, Java, C#)
- ✅ React frontend with modern UI
- ✅ FastAPI backend with CORS support
- ✅ Docker-based secure code execution
- ✅ Docker Compose orchestration
- ✅ Dependency installation (pip, npm) 
- ✅ Built-in pandas stub
- ✅ Real-time code execution
- ✅ Error handling and output display
- ✅ Memory and network isolation in Docker mode
- ✅ Template files for quick start and learning
- ✅ Comprehensive Fibonacci implementations in all languages

## Templates and Examples

The project includes comprehensive template files for learning and experimentation:

### Basic Templates (`backend/templates/solution/`)
- `solution.py` - Python Hello World
- `solution.js` - JavaScript Hello World
- `solution.rb` - Ruby Hello World
- `solution.php` - PHP Hello World
- `solution.c` - C Hello World
- `solution.cpp` - C++ Hello World
- `solution.cs` - C# Hello World
- `Solution.java` - Java Hello World

### Advanced Examples (`backend/templates/fibonacci/`)
Each language includes multiple implementations of the Fibonacci sequence:
- **Recursive** with memoization
- **Iterative** approaches
- **Matrix exponentiation** for fast calculation
- **Golden ratio** approximation
- **Language-specific** features (generators, LINQ, etc.)

These examples demonstrate:
- Algorithm optimization techniques
- Language-specific idioms and features
- Performance comparison between approaches
- Mathematical properties of the Fibonacci sequence

## Architecture

- **Frontend**: React + TypeScript + Vite + Tailwind CSS
- **Backend**: FastAPI + Python + Docker
- **Execution**: Isolated Docker containers for security
- **Languages**: Multiple runtime environments via Docker images

