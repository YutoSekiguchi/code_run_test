# Code Run Test Project

## Project Structure
This is a code execution platform with a React frontend and Python FastAPI backend.

### Frontend (`/frontend`)
- React + TypeScript + Vite application
- Tailwind CSS for styling
- ESLint configuration

### Backend (`/backend`)
- FastAPI server (`app.py`)
- Code execution engine (`engines/run_code.py`)
- Multi-language support with sample files
- Local package libraries for testing

## Current Branch
- Base branch: `main`

## Modified Files
All files have been modified as part of the recent refactoring:
- Backend restructuring with FastAPI
- Frontend creation with React
- Package organization and samples

## Key Components
- **Code Execution**: `backend/engines/run_code.py` - Handles multi-language code execution
- **API Server**: `backend/app.py` - FastAPI endpoints
- **Template Files**: `backend/templates/` - Code templates for learning and testing
  - `backend/templates/solution/` - Basic Hello World templates
  - `backend/templates/fibonacci/` - Advanced Fibonacci implementations
- **Docker Images**: `backend/dockerfiles/` - Language-specific containers

## Languages Supported
- Python (`.py`) - Python 3.11 with pip
- JavaScript (`.js`) - Node.js with npm
- Java (`.java`) - OpenJDK with javac/java
- C (`.c`) - GCC compiler
- C++ (`.cpp`) - G++ compiler
- Ruby (`.rb`) - Ruby interpreter
- PHP (`.php`) - PHP 8.2 CLI
- C# (`.cs`) - Mono compiler and runtime

## Docker Images
Each language has its own optimized Docker image:
- `code-runner-python-base` - Python 3.11 slim
- `code-runner-js-base` - Node.js 18 Alpine
- `code-runner-java-base` - OpenJDK 11 Alpine
- `code-runner-c-base` - GCC on Alpine
- `code-runner-cpp-base` - G++ on Alpine
- `code-runner-ruby-base` - Ruby 3.1 Alpine
- `code-runner-php-base` - PHP 8.2 CLI Alpine
- `code-runner-csharp-base` - Mono latest

## Development Philosophy

### Test-Driven Development (TDD)
- Proceed with Test-Driven Development (TDD) as a principle
- Create tests first based on expected inputs and outputs
- Do not write implementation code, only prepare tests
- Run tests and confirm failures
- Commit once you have confirmed that the tests are correct
- Then proceed with implementation to make the tests pass
- Do not modify tests during implementation, keep modifying the code
- Repeat until all tests pass

## Current Features Status
- ✅ Multi-language execution (Python, JavaScript, Ruby, PHP, C, C++, Java, C#)
- ✅ Docker-based security isolation
- ✅ Template system with Hello World examples
- ✅ Advanced Fibonacci implementations for all languages
- ✅ Frontend with language selection and code execution
- ✅ Dependency installation support (pip for Python, npm for JavaScript)
- ✅ API endpoints for code execution and template retrieval
