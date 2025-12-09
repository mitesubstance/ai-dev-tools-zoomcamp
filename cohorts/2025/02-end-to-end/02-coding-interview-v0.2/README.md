# Coding Interview Project v0.2

## Overview
A real-time collaborative coding interview platform that allows multiple users to share a coding session, edit code simultaneously, and execute Python code safely in the browser.

## Features
- 🔗 Create and share session links
- 👥 Multiple users can edit code simultaneously with real-time updates
- 🎨 Syntax highlighting for Python (extensible to other languages)
- ▶️ Execute Python code safely in the browser using WASM (Pyodide)
- ⚡ Real-time communication via WebSockets
- 🚀 Fast development experience with hot module reloading

## Tech Stack

### Frontend
- **Framework**: React 18+
- **Build Tool**: Vite (with Rolldown)
- **Code Editor**: CodeMirror 6
- **Python Execution**: Pyodide (WebAssembly)

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **WebSocket**: Native FastAPI WebSocket support
- **Session Storage**: In-memory (for v1)

### Development Tools
- **Concurrently**: Run frontend and backend simultaneously

## Project Structure
```
02-coding-interview-v0.2/
├── README.md                   # This file
├── AGENTS.md                   # AI Agent operating instructions
├── ARCHITECTURE.md             # System design and topology
├── DECISIONS.md                # Architecture Decision Records (ADRs)
├── PRODUCT_SPECS.md           # Functional requirements and acceptance criteria
├── IMPLEMENTATION_PLAN.md     # Global roadmap with checkboxes
├── SESSION_LOG.md             # Scratchpad for immediate work (local only)
├── package.json               # Root package.json for concurrently
├── backend/                   # Python-based backend
│   ├── main.py               # FastAPI application entry point
│   ├── requirements.txt      # Python dependencies
│   └── app/                  # Application modules (to be created)
└── frontend/                 # React-based frontend
    ├── package.json
    ├── vite.config.js
    ├── index.html
    └── src/                  # React application source
```

## Getting Started

### Prerequisites
- **Node.js**: 18+ (for npm and Vite)
- **Python**: 3.11+ (for FastAPI)
- **npm**: 9+ (for frontend dependencies)
- **pip**: Latest (for backend dependencies)

### Installation

#### 1. Install Backend Dependencies
```bash
cd backend
uv sync
cd ..
```

#### 2. Install Frontend Dependencies
```bash
cd frontend
npm install
cd ..
```

#### 3. Install Root Dependencies (concurrently)
```bash
npm install
```

Or use the convenience script:
```bash
npm run install:all
```

### Running the Application

#### Option 1: Run Both Services (Recommended)
```bash
npm run dev
```

This will start both the backend (port 8000) and frontend (port 5173) simultaneously.

#### Option 2: Run Services Separately

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Accessing the Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (automatic Swagger UI)
- **Health Check**: http://localhost:8000/api/health

## Development

### Backend Development
- **Package Manager**: uv (fast Python package manager)
- **Framework**: FastAPI with async/await patterns
- **Language**: Python 3.11+
- **Style**: PEP 8 (consider using Black formatter)
- **Testing**: Pytest with uv

### Frontend Development
- **Framework**: React with Vite
- **Language**: JavaScript/JSX
- **Style**: ESLint configuration included
- **Testing**: Jest/Vitest (to be set up)

### Code Editor Integration
The platform uses CodeMirror 6 for code editing. Future enhancements will add:
- Syntax highlighting for multiple languages
- Code autocompletion
- Collaborative cursors
- Custom themes

### Python Execution
Python code runs entirely in the browser using Pyodide (WebAssembly):
- No server-side execution (security benefit)
- Instant feedback without network latency
- Access to Python standard library
- Isolated execution environment

## Testing

### Backend Tests
```bash
cd backend
uv run pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm test
# (To be implemented)
```

## 🤖 AI Context & Documentation

If you are an AI assistant helping with this project, please review the following context files before making changes:
* **[AGENTS.md](./AGENTS.md)**: **READ THIS FIRST.** Your operating instructions and rules.
* **[ARCHITECTURE.md](./ARCHITECTURE.md)**: System design and topology.
* **[DECISIONS.md](./DECISIONS.md)**: ADRs - Do not violate agreed-upon architectural decisions.
* **[PRODUCT_SPECS.md](./PRODUCT_SPECS.md)**: Functional requirements and acceptance criteria.
* **[IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md)**: Global roadmap - Update this when phases are complete.
* **[SESSION_LOG.md](./SESSION_LOG.md)**: Your scratchpad. Use this to track immediate progress and errors.

## API Endpoints

### HTTP Endpoints

#### Root
- **GET** `/` - API information and status

#### Health Check
- **GET** `/api/health` - Server health status

#### Sessions (To be implemented)
- **POST** `/api/sessions` - Create a new coding session
- **GET** `/api/sessions/{session_id}` - Get session information

### WebSocket (To be implemented)
- **WS** `/ws/{session_id}` - Real-time collaborative editing

## Environment Variables

Create a `.env` file in the backend directory (optional):
```env
BACKEND_PORT=8000
```

Create a `.env` file in the frontend directory (optional):
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000
```

## Troubleshooting

### Backend won't start
- Ensure Python 3.11+ is installed: `python --version`
- Check if dependencies are installed: `pip list | grep fastapi`
- Try reinstalling dependencies: `pip install -r requirements.txt`

### Frontend won't start
- Ensure Node.js 18+ is installed: `node --version`
- Check if dependencies are installed: `npm list`
- Try reinstalling dependencies: `rm -rf node_modules package-lock.json && npm install`

### Port already in use
- Backend (8000): `lsof -ti:8000 | xargs kill -9`
- Frontend (5173): `lsof -ti:5173 | xargs kill -9`

## Contributing

### Development Workflow
1. Read the context files (AGENTS.md, ARCHITECTURE.md, DECISIONS.md, PRODUCT_SPECS.md)
2. Update SESSION_LOG.md with your plan
3. Make changes following the architectural decisions
4. Update IMPLEMENTATION_PLAN.md when tasks are complete
5. Document any new architectural decisions in DECISIONS.md

### Commit Message Format
Reference the requirement ID from PRODUCT_SPECS.md:
```
feat(REQ-001): Implement session creation endpoint
fix(REQ-002): Fix WebSocket connection handling
docs: Update API documentation
```

## Roadmap

See [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) for the detailed project roadmap and current progress.

**Current Phase**: Phase 0 (Project Setup & Documentation) - 80% complete

**Next Steps**:
1. Complete coding standards definition
2. Set up testing frameworks
3. Implement session management (REQ-001)
4. Implement real-time collaborative editing (REQ-002)
5. Integrate Pyodide for Python execution (REQ-003)

## License
[To be specified]

---
*Version: 0.2*  
*Last Updated: 2025-12-09*
