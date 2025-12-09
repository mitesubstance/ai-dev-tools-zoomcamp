# Implementation Plan

This document outlines the step-by-step implementation roadmap for the Collaborative Coding Interview Platform.

**Status Legend:**
- `[ ]` Not started
- `[x]` Completed
- `[~]` In progress
- `[!]` Blocked

---

## Phase 0: Planning & Documentation ✅

- [x] Define project requirements (PRODUCT_SPECS.md)
- [x] Make technology stack decisions (DECISIONS.md)
- [x] Design system architecture (ARCHITECTURE.md)
- [x] Create AI agent instructions (AGENTS.md)
- [x] Set up vendor-agnostic documentation system
- [x] Create OpenAPI specification (specs/openapi.yaml)

**Completion Date**: 2025-12-08

---

## Phase 1: Project Setup ✅

**Goal**: Initialize project structure and dependencies.

### Backend Setup
- [x] Create `backend/` directory structure
- [x] Initialize Python project
  - [x] Create `requirements.txt` with dependencies:
    - `fastapi[all]>=0.109.0`
    - `uvicorn[standard]>=0.27.0`
    - `pydantic>=2.5.0`
    - `pytest>=8.0.0`
    - `pytest-asyncio>=0.23.0`
    - `httpx>=0.26.0`
- [x] Set up FastAPI app skeleton (`app/main.py`)
- [x] Configure CORS middleware
- [x] Create health check endpoint (`GET /health`)
- [x] Verify backend runs: `uvicorn app.main:app --reload`

### Frontend Setup
- [x] Create `frontend/` directory
- [x] Initialize Vite + React project: `npm create vite@latest`
- [x] Install dependencies:
  - Core: `react`, `react-dom`
  - Editor: `@codemirror/state`, `@codemirror/view`, `@codemirror/collab`
  - Languages: `@codemirror/lang-javascript`, `@codemirror/lang-python`
  - Execution: `pyodide`
- [x] Create basic App component
- [x] Verify frontend runs: `npm run dev`

### Root Setup
- [x] Create root `package.json` with scripts:
  ```json
  {
    "scripts": {
      "dev": "concurrently \"npm run dev:client\" \"npm run dev:server\"",
      "dev:client": "cd frontend && npm run dev",
      "dev:server": "cd backend && uvicorn app.main:app --reload",
      "test": "npm run test:client && cd backend && pytest",
      "test:client": "cd frontend && npm test",
      "test:integration": "npm run test:integration:run"
    }
  }
  ```
- [x] Install `concurrently`: `npm install -D concurrently`
- [x] Create `.gitignore` (Python + Node.js)
- [x] Create `.env.example` template

**Acceptance Criteria:**
- ✅ `npm run dev` can start both client and server
- ✅ Health check returns: `{"status": "ok"}`
- ✅ Frontend displays "Hello World" (Vite default)

**Completion Date**: 2025-12-08
**Actual Time**: ~1.5 hours

---

## Phase 2: Initial Implementation (Q1)

**Goal**: Implement basic session management and collaborative editing.  
**Homework Question**: Q1 - Initial Implementation

### Backend - Session Management
- [ ] Create Pydantic models (`app/models/session.py`):
  - `Session` model (id, language, created_at, users, document)
  - `User` model (id, name, color)
  - `Message` model (WebSocket message schemas)
- [ ] Implement Repository Pattern:
  - [ ] Create `app/repositories/base.py` (abstract SessionRepository)
  - [ ] Create `app/repositories/memory.py` (InMemorySessionRepository)
- [ ] Implement REST endpoints (`app/routes/sessions.py`):
  - [ ] `POST /sessions` - Create new session
  - [ ] `GET /sessions/{id}` - Get session details
  - [ ] `DELETE /sessions/{id}` - Delete session
- [ ] Test endpoints with curl/Postman

### Backend - WebSocket
- [ ] Create WebSocket endpoint (`app/routes/websocket.py`):
  - [ ] `GET /ws/{session_id}` - WebSocket connection
  - [ ] Accept connection with query params: `userId`, `userName`
- [ ] Implement connection manager:
  - [ ] Add user to session on connect
  - [ ] Remove user on disconnect
  - [ ] Broadcast messages to all users in session
- [ ] Handle message types:
  - [ ] `join` - User joins session
  - [ ] `edit` - Code change from user
  - [ ] `cursor` - Cursor position update

### Frontend - Session Management
- [ ] Create API service (`src/services/api.js`):
  - [ ] `createSession()` - POST /sessions
  - [ ] `getSession(id)` - GET /sessions/{id}
- [ ] Create components:
  - [ ] `SessionControls.jsx` - Create/Join session UI
  - [ ] `HomePage.jsx` - Landing page with "Create Session" button
  - [ ] `SessionPage.jsx` - Main session view
- [ ] Implement routing (React Router or similar)
- [ ] Add copy-to-clipboard for session link

### Frontend - Code Editor
- [ ] Create `CodeEditor.jsx` component
- [ ] Initialize CodeMirror with basic config:
  - [ ] Python language support
  - [ ] Basic theme
  - [ ] Read-only mode for testing
- [ ] Wire up editor to React state

### Frontend - WebSocket
- [ ] Create WebSocket hook (`src/hooks/useWebSocket.js`):
  - [ ] Connect to `/ws/{session_id}`
  - [ ] Handle connection states (connecting, connected, disconnected)
  - [ ] Send messages
  - [ ] Receive messages
- [ ] Implement message handlers:
  - [ ] `sync` - Initialize document state
  - [ ] `user_joined` - Update user list
  - [ ] `user_left` - Update user list
  - [ ] `update` - Apply code changes

### Integration
- [ ] Connect CodeEditor to WebSocket
- [ ] Test with two browser windows:
  - [ ] Create session in window 1
  - [ ] Join same session in window 2
  - [ ] Type in window 1, verify appears in window 2

**Acceptance Criteria:**
- User can create a session and get a shareable link
- User can join session via link
- Multiple users see each other typing in real-time
- Document state stays consistent

**Estimated Time**: 6-8 hours

---

## Phase 3: Integration Tests (Q2)

**Goal**: Write tests for client-server interaction.  
**Homework Question**: Q2 - Integration Tests

### Backend Tests
- [ ] Set up pytest configuration (`backend/conftest.py`)
- [ ] Create test fixtures:
  - [ ] `test_client` - FastAPI TestClient
  - [ ] `mock_session` - Sample session data
- [ ] Write tests (`backend/tests/test_routes.py`):
  - [ ] Test `POST /sessions` - Returns 201 with session ID
  - [ ] Test `GET /sessions/{id}` - Returns session data
  - [ ] Test `GET /sessions/invalid` - Returns 404
  - [ ] Test `DELETE /sessions/{id}` - Returns 204
- [ ] Write WebSocket tests (`backend/tests/test_websocket.py`):
  - [ ] Test connection succeeds
  - [ ] Test message broadcast to multiple clients
  - [ ] Test user join/leave events
- [ ] Verify: `cd backend && pytest`

### Frontend Tests
- [ ] Set up Vitest configuration (`frontend/vitest.config.js`)
- [ ] Write component tests:
  - [ ] Test `SessionControls` renders correctly
  - [ ] Test "Create Session" button click
  - [ ] Test session link copy functionality
- [ ] Write service tests:
  - [ ] Mock API calls with `vi.mock()`
  - [ ] Test `createSession()` calls correct endpoint
  - [ ] Test error handling
- [ ] Verify: `cd frontend && npm test`

### Integration Tests
- [ ] Create `tests/integration/` directory
- [ ] Write E2E test with Playwright:
  - [ ] Test: Create session
  - [ ] Test: Join session in second browser context
  - [ ] Test: Type in one browser, verify in other
  - [ ] Test: Verify both users see same content
- [ ] Create `npm run test:integration` script

### Documentation
- [ ] Update README.md with test commands:
  ```bash
  # Backend tests
  cd backend && pytest
  
  # Frontend tests
  cd frontend && npm test
  
  # Integration tests
  npm run test:integration
  ```
- [ ] Document test coverage expectations (80%)

**Acceptance Criteria:**
- All backend tests pass
- All frontend tests pass
- Integration test demonstrates collaborative editing
- Test commands documented in README

**Answer to Q2**: `npm test` (runs both frontend and backend tests)

**Estimated Time**: 4-6 hours

---

## Phase 4: Development Environment (Q3)

**Goal**: Set up concurrent development workflow.  
**Homework Question**: Q3 - Running Both Client and Server

### Tasks
- [x] Install `concurrently` package (done in Phase 1)
- [x] Create `npm run dev` script (done in Phase 1)
- [ ] Test concurrent execution:
  - [ ] Verify both processes start
  - [ ] Verify colored output (client in blue, server in green)
  - [ ] Verify hot reload works for both
- [ ] Add `npm run dev:client` (frontend only)
- [ ] Add `npm run dev:server` (backend only)
- [ ] Update README.md with usage instructions

### Configuration
```json
{
  "scripts": {
    "dev": "concurrently -c \"blue,green\" \"npm run dev:client\" \"npm run dev:server\"",
    "dev:client": "cd frontend && npm run dev -- --port 5173",
    "dev:server": "cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
  }
}
```

**Acceptance Criteria:**
- Single command starts both services
- Changes to frontend auto-reload
- Changes to backend auto-reload
- Different colors for log output

**Answer to Q3**: `npm run dev` or:
```json
"dev": "concurrently \"npm run dev:client\" \"npm run dev:server\""
```

**Estimated Time**: 1 hour

---

## Phase 5: Syntax Highlighting (Q4)

**Goal**: Add JavaScript and Python syntax highlighting.  
**Homework Question**: Q4 - Syntax Highlighting

### Tasks
- [ ] Install language packages (if not done in Phase 1):
  - [ ] `@codemirror/lang-javascript`
  - [ ] `@codemirror/lang-python`
- [ ] Update `CodeEditor.jsx`:
  - [ ] Import language extensions
  - [ ] Add language selection dropdown (or default to Python)
  - [ ] Apply appropriate language extension based on selection
- [ ] Test syntax highlighting:
  - [ ] Python: keywords, strings, comments colored
  - [ ] JavaScript: keywords, strings, comments colored
- [ ] Ensure highlighting works in collaborative mode

### Code Example
```javascript
import { python } from '@codemirror/lang-python';
import { javascript } from '@codemirror/lang-javascript';

const extensions = [
  language === 'python' ? python() : javascript(),
  // ... other extensions
];
```

**Acceptance Criteria:**
- Python keywords (def, class, import) are highlighted
- JavaScript keywords (const, let, function) are highlighted
- Strings and comments are colored
- Highlighting updates in real-time
- Multiple users see correct highlighting

**Answer to Q4**: CodeMirror 6 (specifically `@codemirror/lang-javascript` and `@codemirror/lang-python`)

**Estimated Time**: 2 hours

---

## Phase 6: Code Execution (Q5)

**Goal**: Execute Python code safely in the browser using WASM.  
**Homework Question**: Q5 - Code Execution

### Tasks
- [ ] Install Pyodide: `npm install pyodide`
- [ ] Create `usePyodide` hook (`src/hooks/usePyodide.js`):
  - [ ] Lazy load Pyodide on first use
  - [ ] Handle loading state
  - [ ] Execute code function
  - [ ] Capture stdout/stderr
  - [ ] Handle errors
- [ ] Create `ExecutionPanel.jsx` component:
  - [ ] "Run Code" button
  - [ ] Loading indicator ("Initializing Python...")
  - [ ] Output display area
  - [ ] Error display (red text)
- [ ] Implement code execution:
  - [ ] Get code from CodeMirror editor
  - [ ] Pass to Pyodide
  - [ ] Redirect stdout to capture output
  - [ ] Display output in panel
- [ ] Add timeout to prevent infinite loops (10 seconds)
- [ ] Test with sample Python code:
  ```python
  print("Hello, world!")
  for i in range(5):
      print(i)
  ```

### Security Verification
- [ ] Verify in Network tab: No API calls during execution
- [ ] Verify code runs entirely in browser
- [ ] Test that server is never contacted for execution

**Acceptance Criteria:**
- User can click "Run Code" button
- Python code executes in browser
- Output (print statements) displayed correctly
- Errors caught and displayed
- No server-side execution (verified via Network tab)
- Works offline after initial Pyodide load

**Answer to Q5**: Pyodide (CPython compiled to WebAssembly)

**Estimated Time**: 4 hours

---

## Phase 7: Containerization (Q6)

**Goal**: Create a Dockerfile with both frontend and backend.  
**Homework Question**: Q6 - Containerization

### Tasks
- [ ] Create `Dockerfile` with multi-stage build:
  
  **Stage 1: Build Frontend**
  ```dockerfile
  FROM node:20-alpine AS frontend-build
  WORKDIR /app/frontend
  COPY frontend/package*.json ./
  RUN npm ci
  COPY frontend/ ./
  RUN npm run build
  ```
  
  **Stage 2: Final Image**
  ```dockerfile
  FROM python:3.11-slim
  
  # Install Nginx
  RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*
  
  # Copy backend
  WORKDIR /app/backend
  COPY backend/requirements.txt ./
  RUN pip install --no-cache-dir -r requirements.txt
  COPY backend/ ./
  
  # Copy frontend build
  COPY --from=frontend-build /app/frontend/dist /var/www/html
  
  # Configure Nginx
  COPY nginx.conf /etc/nginx/nginx.conf
  
  # Expose port
  EXPOSE 8000
  
  # Start script
  COPY start.sh /start.sh
  RUN chmod +x /start.sh
  CMD ["/start.sh"]
  ```

- [ ] Create `nginx.conf`:
  - [ ] Serve frontend static files
  - [ ] Proxy `/api/*` to FastAPI
  - [ ] Proxy `/ws/*` to FastAPI WebSocket
  
- [ ] Create `start.sh`:
  ```bash
  #!/bin/bash
  nginx &
  cd /app/backend && uvicorn app.main:app --host 0.0.0.0 --port 8000
  ```

- [ ] Create `.dockerignore`:
  ```
  node_modules/
  __pycache__/
  *.pyc
  .env
  .git/
  ```

- [ ] Test Docker build:
  - [ ] `docker build -t coding-interview-platform .`
  - [ ] `docker run -p 8000:8000 coding-interview-platform`
  - [ ] Access at `http://localhost:8000`
  - [ ] Verify frontend loads
  - [ ] Verify backend API works
  - [ ] Verify WebSocket connections work

**Acceptance Criteria:**
- Dockerfile builds successfully
- Single container runs both frontend and backend
- Health check endpoint accessible
- WebSocket connections work through Nginx
- Frontend and backend communicate correctly

**Answer to Q6**: `python:3.11-slim` (or `node:20-alpine` if Node-based approach)

**Estimated Time**: 3-4 hours

---

## Phase 8: Deployment (Q7)

**Goal**: Deploy to Render.  
**Homework Question**: Q7 - Deployment

### Render Setup
- [ ] Create account on Render.com
- [ ] Create new "Web Service"
- [ ] Configure service:
  - [ ] Repository: Link to GitHub repo
  - [ ] Branch: `main`
  - [ ] Build Command: (none, using Dockerfile)
  - [ ] Docker: Enable
  - [ ] Port: 8000
  - [ ] Environment: Production

### Environment Variables
- [ ] Set environment variables in Render:
  - `FRONTEND_URL` = Your render URL
  - `CORS_ORIGINS` = Your render URL
  - `LOG_LEVEL` = `info`
  - `PYTHONUNBUFFERED` = `1`

### Configuration Files
- [ ] Create `render.yaml`:
  ```yaml
  services:
    - type: web
      name: coding-interview-platform
      env: docker
      region: oregon
      plan: free
      dockerfilePath: ./Dockerfile
      envVars:
        - key: FRONTEND_URL
          value: https://your-app.onrender.com
  ```

### Deployment
- [ ] Push code to GitHub
- [ ] Trigger deployment on Render
- [ ] Monitor build logs
- [ ] Wait for deployment to complete (~5-10 minutes)

### Verification
- [ ] Access deployed URL
- [ ] Test session creation
- [ ] Test joining session (open in two browsers/incognito)
- [ ] Test collaborative editing
- [ ] Test code execution
- [ ] Test WebSocket stays connected

### Documentation
- [ ] Add deployment URL to README.md
- [ ] Document environment variables needed
- [ ] Add troubleshooting section for common deployment issues

**Acceptance Criteria:**
- Application deployed and accessible via public URL
- Multiple users can collaborate in real-time
- Code execution works
- WebSocket connections stable
- No CORS errors

**Answer to Q7**: Render

**Estimated Time**: 2-3 hours

---

## Phase 9: Final Polish & Documentation

**Goal**: Complete documentation and prepare for submission.

### Code Quality
- [ ] Run linters:
  - [ ] Backend: `black backend/` and `ruff backend/`
  - [ ] Frontend: `npm run lint -- --fix`
- [ ] Ensure all tests pass:
  - [ ] `cd backend && pytest`
  - [ ] `cd frontend && npm test`
- [ ] Check test coverage (aim for 80%+)
- [ ] Remove console.log statements
- [ ] Remove commented-out code

### Documentation
- [ ] Complete README.md:
  - [ ] Project description
  - [ ] Tech stack
  - [ ] Setup instructions
  - [ ] Usage instructions
  - [ ] Test commands
  - [ ] Deployment instructions
  - [ ] Link to deployed app
- [ ] Ensure all context files are up to date:
  - [ ] AGENTS.md
  - [ ] ARCHITECTURE.md
  - [ ] DECISIONS.md
  - [ ] PRODUCT_SPECS.md
  - [ ] IMPLEMENTATION_PLAN.md (this file!)
- [ ] Create HOMEWORK_ANSWERS.md with answers to Q1-Q7

### Git Hygiene
- [ ] Review commit history
- [ ] Ensure meaningful commit messages
- [ ] Commits reference REQ-XXX where applicable
- [ ] Tag final version: `git tag v1.0.0`

### Optional: Demo Video
- [ ] Record 60-90 second demo showing:
  - [ ] Creating a session
  - [ ] Joining from another browser
  - [ ] Real-time collaborative editing
  - [ ] Code execution
- [ ] Upload to YouTube/LinkedIn
- [ ] Add link to README.md

**Estimated Time**: 2-3 hours

---

## Phase 10: Homework Submission

### Deliverables Checklist
- [ ] GitHub repository with all code
- [ ] README.md with setup/usage instructions
- [ ] All 7 homework questions answered
- [ ] Application deployed and accessible
- [ ] Demo video (optional but recommended)

### Homework Answers Summary

| Question | Answer |
|----------|--------|
| Q1 | [Your initial AI prompt] |
| Q2 | `npm test` |
| Q3 | `"dev": "concurrently \"npm run dev:client\" \"npm run dev:server\""` |
| Q4 | CodeMirror 6 |
| Q5 | Pyodide |
| Q6 | `python:3.11-slim` |
| Q7 | Render |

### Submission
- [ ] Submit GitHub repo link to: https://courses.datatalks.club/ai-dev-tools-2025/homework/hw2
- [ ] Ensure repo is public
- [ ] Share on LinkedIn/Twitter with #AIDevToolsZoomcamp (optional)

---

## Timeline Estimate

| Phase | Estimated Time | Status |
|-------|---------------|--------|
| Phase 0: Planning | 3-4 hours | ✅ Complete |
| Phase 1: Setup | 2 hours | [ ] Not Started |
| Phase 2: Implementation | 6-8 hours | [ ] Not Started |
| Phase 3: Tests | 4-6 hours | [ ] Not Started |
| Phase 4: Dev Environment | 1 hour | [ ] Not Started |
| Phase 5: Syntax Highlighting | 2 hours | [ ] Not Started |
| Phase 6: Code Execution | 4 hours | [ ] Not Started |
| Phase 7: Containerization | 3-4 hours | [ ] Not Started |
| Phase 8: Deployment | 2-3 hours | [ ] Not Started |
| Phase 9: Polish | 2-3 hours | [ ] Not Started |
| Phase 10: Submission | 1 hour | [ ] Not Started |
| **Total** | **30-40 hours** | **3% Complete** |

---

## Notes & Lessons Learned

### Important Notes
- `SESSION_LOG.md` is ephemeral working memory and NOT version controlled (excluded in `.gitignore`)
- Session logs should NOT be archived here to prevent commit noise
- Use `docs/archive/` if you need to permanently save specific session notes

### Lessons Learned

**2025-12-08 - Phase 0 & 1**: 
- Initial planning completed with comprehensive documentation system
- All context files created with specifications
- Project setup completed with frontend (React+Vite), backend (FastAPI), and dev tooling (concurrently)
- Decided to keep SESSION_LOG.md out of version control to prevent merge conflicts and commit noise

---

**Last Updated**: 2025-12-08  
**Current Phase**: Phase 0 (Complete) → Ready for Phase 1  
**Next Action**: Begin Phase 1 - Project Setup
