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
- **Code Execution**: `backend/run_code.py` - Handles multi-language code execution
- **API Server**: `backend/app.py` - FastAPI endpoints
- **Sample Code**: `backend/samples/` - Test files for various languages
- **Local Libraries**: `backend/libs/` - Custom packages for testing

## Languages Supported
- Python
- JavaScript/Node.js
- Java
- C/C++
- Ruby

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
