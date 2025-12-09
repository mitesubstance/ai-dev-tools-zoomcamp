# Coding Interview Project v0.2

## Overview
A real-time collaborative coding interview platform that allows multiple users to share a coding session, edit code simultaneously, and execute Python code safely in the browser.

## Features
- 🔗 Create and share session links
- 👥 Multiple users can edit code simultaneously with real-time updates
- 🎨 Syntax highlighting for Python and JavaScript (extensible to other languages)
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

#### Option 1: Docker (Recommended for Production)
- **Docker**: 20.10+ (for containerized deployment)
- **Docker Compose**: 1.29+ (optional, for easier management)

#### Option 2: Local Development
- **Node.js**: 18+ (for npm and Vite)
- **Python**: 3.11+ (for FastAPI)
- **npm**: 9+ (for frontend dependencies)
- **uv**: Latest (for backend dependencies)

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
- **Frontend**: http://localhost:5173 (development) or http://localhost:8000 (Docker)
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs (automatic Swagger UI)
- **Health Check**: http://localhost:8000/api/health

---

## Docker Deployment

### Building and Running with Docker

#### Using Docker Compose (Recommended)

**Build and start the container:**
```bash
docker-compose up --build
```

**Run in detached mode (background):**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Stop the container:**
```bash
docker-compose down
```

#### Using Docker CLI

**Build the image:**
```bash
docker build -t coding-interview-platform .
```

**Run the container:**
```bash
docker run -d -p 8000:8000 --name coding-interview-platform coding-interview-platform
```

**View logs:**
```bash
docker logs -f coding-interview-platform
```

**Stop and remove the container:**
```bash
docker stop coding-interview-platform
docker rm coding-interview-platform
```

### Docker Architecture

The Dockerfile uses a **multi-stage build** approach:

1. **Stage 1 (Frontend Builder)**: 
   - Uses Node.js Alpine image
   - Installs frontend dependencies
   - Builds React application for production (creates optimized static files)

2. **Stage 2 (Production)**:
   - Uses Python 3.11 slim image
   - Installs uv for Python package management
   - Installs backend dependencies
   - Copies built frontend from Stage 1
   - Serves both frontend (static files) and backend (API + WebSockets) on port 8000

**Benefits:**
- ✅ Single container for both frontend and backend
- ✅ Optimized image size (multi-stage build)
- ✅ Production-ready static asset serving
- ✅ Built-in health checks
- ✅ No external dependencies at runtime

### Accessing the Dockerized Application

Once the container is running:
- **Application**: http://localhost:8000 (serves both frontend and API)
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

**Note**: In Docker mode, the FastAPI backend serves both the API endpoints and the frontend static files. No need to run a separate frontend dev server.

---

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
The platform uses CodeMirror 6 for code editing with the following features:

**Currently Supported:**
- ✅ Python syntax highlighting
- ✅ JavaScript syntax highlighting
- ✅ Dynamic language switching
- ✅ Language-specific placeholders
- ✅ Dark theme (OneDark)

**Future Enhancements:**
- Code autocompletion
- Collaborative cursors
- Additional languages (Java, C++, Go, etc.)
- Custom themes
- Line numbers and code folding

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

### Backend Configuration

The backend uses the `APP_ENV` environment variable to control its behavior:

**Development Mode** (default):
- API-only mode (no frontend serving)
- CORS enabled for local development (localhost:5173, localhost:3000)
- Frontend should run separately (`npm run dev`)

**Production Mode**:
- Serves frontend static files from `frontend/dist`
- CORS enabled as safety net (protects against accidental absolute URL usage)
- Single container/process for both frontend and backend

Create a `.env` file in the backend directory (see `backend/.env.example`):
```env
# Set to 'production' when deploying
APP_ENV=development
```

**For Render/Cloud Deployment**:
Add environment variable in your platform's dashboard:
- Key: `APP_ENV`
- Value: `production`

### Frontend Configuration

The frontend uses **relative paths** for all API calls (e.g., `/api/sessions`, `/ws/{sessionId}`):
- **Development**: Vite proxy routes these to `localhost:8000` (configured in `vite.config.js`)
- **Production**: Same-origin requests (frontend and API served from same domain)

**No environment variables needed** - the frontend automatically adapts to its environment.

Legacy `.env` variables (no longer used):
```env
# ❌ NOT NEEDED - Frontend uses relative paths
# VITE_API_URL=http://localhost:8000
# VITE_WS_URL=ws://localhost:8000
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
