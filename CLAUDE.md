# Code Run Test Project

## Project Structure
This is a code execution platform with a React frontend and Python FastAPI backend.

### Frontend (`/frontend`)
- React + TypeScript + Vite application
- Tailwind CSS for styling
- ESLint configuration

### Backend (`/backend`)
- FastAPI server (`app.py`)
- Code execution engine (`run_code.py`)
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

## Recent Changes
- UI design improvements
- FastAPI server implementation
- ASGI interface removal
- Frontend/backend separation
- Directory restructuring