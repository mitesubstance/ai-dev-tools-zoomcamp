# Architecture Decision Records (ADRs)

This document records all significant architectural decisions made for the Collaborative Coding Interview Platform.

## Format
Each ADR follows this structure:
- **ADR Number**: Unique identifier
- **Date**: When the decision was made
- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Context**: The issue or situation motivating the decision
- **Decision**: What we decided to do
- **Consequences**: Positive and negative outcomes of the decision

---

## ADR-001: React + Vite for Frontend

**Date**: 2025-12-08  
**Status**: ✅ Accepted  

### Context
Need a modern frontend framework for building a real-time collaborative code editor. Requirements:
- Fast development experience with HMR
- Component-based architecture
- Good ecosystem for real-time features
- Recommended by homework assignment

### Decision
Use **React 18+** with **Vite 5+** as the build tool.

### Alternatives Considered
- **Next.js**: Full-stack framework, but overkill for this project's scope
- **Vue.js**: Good alternative, but React has larger ecosystem for editor libraries
- **Svelte**: Modern and fast, but smaller community

### Consequences
**Positive:**
- ✅ Fast HMR (<50ms) for excellent DX
- ✅ Huge ecosystem (CodeMirror React wrappers available)
- ✅ Easy to integrate WebSocket hooks
- ✅ Modern build tool (ES modules, tree-shaking)
- ✅ Well-documented and widely used

**Negative:**
- ⚠️ React's bundle size larger than Svelte
- ⚠️ Requires understanding of hooks and lifecycle

---

## ADR-002: FastAPI for Backend

**Date**: 2025-12-08  
**Status**: ✅ Accepted  

### Context
Need a Python backend framework that:
- Supports WebSocket for real-time collaboration
- Has async/await for high concurrency
- Auto-generates API documentation
- Is modern and actively maintained

### Decision
Use **FastAPI 0.109+** with **Uvicorn** as the ASGI server.

### Alternatives Considered
- **Express.js (Node.js)**: Homework recommendation, but user preferred Python backend
- **Flask + Flask-SocketIO**: Simpler but lacks native async and auto-docs
- **Django + Channels**: Feature-rich but heavyweight for this use case

### Consequences
**Positive:**
- ✅ Native async/await (perfect for WebSocket)
- ✅ Auto-generates OpenAPI/Swagger docs
- ✅ Type hints with Pydantic (better AI code generation)
- ✅ High performance (comparable to Node.js)
- ✅ Growing ecosystem and community
- ✅ Built-in WebSocket support

**Negative:**
- ⚠️ Python GIL (not relevant for I/O-bound WebSocket app)
- ⚠️ Smaller deployment ecosystem compared to Node.js

---

## ADR-003: Repository Pattern for Data Layer

**Date**: 2025-12-08  
**Status**: ✅ Accepted  

### Context
Need to store session data, but:
- Homework doesn't require persistent database
- Want to keep initial implementation simple
- Need flexibility to add database later without major refactoring

### Decision
Implement **Repository Pattern** with:
- Abstract `SessionRepository` interface
- `InMemorySessionRepository` for Phase 1
- Easy migration path to `SQLAlchemyRepository` later

### Alternatives Considered
- **Direct SQLAlchemy from start**: Over-engineering for homework
- **Plain dictionaries everywhere**: Hard to refactor later
- **No abstraction**: Tight coupling to storage mechanism

### Consequences
**Positive:**
- ✅ Simple initial implementation (dict-based)
- ✅ Zero infrastructure dependencies for development
- ✅ Easy to swap implementations later
- ✅ Testable (can inject mock repositories)
- ✅ Clean separation of concerns

**Negative:**
- ⚠️ In-memory data lost on server restart
- ⚠️ Doesn't scale beyond single server (need Redis for multi-server)

**Future Migration Path:**
```python
# Phase 1: InMemorySessionRepository
# Phase 2: SQLAlchemySessionRepository (PostgreSQL)
# Phase 3: RedisSessionRepository (production scale)
```

---

## ADR-004: CodeMirror 6 for Code Editor

**Date**: 2025-12-08  
**Status**: ✅ Accepted  

### Context
Need a code editor with:
- Syntax highlighting (JavaScript, Python)
- Real-time collaborative editing support
- Good performance
- Active development

### Decision
Use **CodeMirror 6** with `@codemirror/collab` extension.

### Alternatives Considered
- **Monaco Editor**: Most actively developed (Microsoft-backed), but 2MB+ bundle size
- **Ace Editor**: Mature and stable, but older architecture
- **Prism.js**: Lightweight but highlighting-only (no editing)

### Consequences
**Positive:**
- ✅ Built-in **Operational Transformation (OT)** for collaboration
- ✅ Tree-shakable modules (smaller bundle)
- ✅ No third-party collaboration library needed
- ✅ Dedicated language packages (`@codemirror/lang-python`)
- ✅ Modern architecture designed for real-time editing
- ✅ Extensible plugin system

**Negative:**
- ⚠️ Steeper learning curve than Monaco
- ⚠️ Fewer features than Monaco (no IntelliSense out-of-box)

**Key Technical Detail:**
CodeMirror's `@codemirror/collab` provides OT-based conflict resolution, eliminating need for libraries like Y.js or ShareDB.

---

## ADR-005: Pyodide for Python WASM Execution

**Date**: 2025-12-08  
**Status**: ✅ Accepted  

### Context
Homework requires safe Python code execution in browser (Question 5). Requirements:
- Execute Python without server-side security risks
- Support standard library
- Modern and maintained

### Decision
Use **Pyodide 0.25+** (CPython compiled to WebAssembly).

### Alternatives Considered
- **Skulpt**: Lighter (~1MB) but limited stdlib, educational focus
- **Brython**: Python-to-JS transpiler, good for DOM but not general Python
- **Server-side execution**: Security nightmare for untrusted code

### Consequences
**Positive:**
- ✅ Full CPython 3.11 compatibility
- ✅ No server-side execution (secure by design)
- ✅ Supports NumPy, Pandas (if needed later)
- ✅ Mozilla-backed (reliable maintenance)
- ✅ Can install pip packages in browser
- ✅ Perfect for coding interviews

**Negative:**
- ⚠️ Large initial download (~15MB)
- ⚠️ Loading time (3-5 seconds on first load)
- ⚠️ Performance slower than native Python

**Mitigation:**
- Lazy load Pyodide (only when user clicks "Run")
- Cache via Service Worker for subsequent visits
- Show loading indicator during initialization

---

## ADR-006: Native WebSockets for Real-time Communication

**Date**: 2025-12-08  
**Status**: ✅ Accepted  

### Context
Need real-time bidirectional communication for collaborative editing. Requirements:
- Works with CodeMirror's OT protocol
- Simple to implement
- Low latency

### Decision
Use **FastAPI's built-in WebSocket** support on backend and **native browser WebSocket API** on frontend.

### Alternatives Considered
- **Socket.IO (python-socketio)**: More features (rooms, auto-reconnect) but adds complexity
- **websockets library**: Lower-level, more control but more code
- **SSE (Server-Sent Events)**: Unidirectional only

### Consequences
**Positive:**
- ✅ No extra backend dependencies (built into FastAPI)
- ✅ Native async/await support
- ✅ Simple WebSocket protocol (no Socket.IO overhead)
- ✅ Works seamlessly with CodeMirror collab
- ✅ Easier to debug (standard protocol)

**Negative:**
- ⚠️ No auto-reconnection (must implement ourselves)
- ⚠️ No rooms abstraction (implement manually)
- ⚠️ No fallback transport (WebSocket or nothing)

**Implementation Note:**
Frontend will implement reconnection logic with exponential backoff.

---

## ADR-007: Render for Deployment

**Date**: 2025-12-08  
**Status**: ✅ Accepted  

### Context
Need to deploy containerized application (Homework Question 7). Requirements:
- Docker support
- WebSocket support
- Free tier or low cost
- Simple setup

### Decision
Use **Render** with Docker deployment.

### Alternatives Considered
- **Railway**: Easier Docker deploy but limited free tier
- **Fly.io**: Edge deployment, excellent WebSocket, slightly more complex
- **Vercel**: Great for frontend but poor WebSocket support
- **Google Cloud Run**: Production-grade but more config required
- **AWS ECS/App Runner**: Most complex, enterprise-grade

### Consequences
**Positive:**
- ✅ Good free tier (enough for homework demo)
- ✅ Native Docker container support
- ✅ WebSocket support out-of-box
- ✅ Auto-deploy from GitHub
- ✅ Environment variable management
- ✅ Good documentation

**Negative:**
- ⚠️ Cold starts on free tier (slower first load)
- ⚠️ Limited to single region on free tier
- ⚠️ Less flexibility than AWS/GCP

**Deployment Configuration:**
- Single Docker container with both frontend (Nginx) and backend (FastAPI)
- Environment variables for CORS configuration
- Health check endpoint for container orchestration

---

## ADR-008: Hybrid OpenAPI Approach

**Date**: 2025-12-08  
**Status**: ✅ Accepted  

### Context
Homework mentions optional 3-step approach including OpenAPI specs. Need to balance:
- Design-first (write spec before code)
- Code-first (auto-generate from FastAPI)

### Decision
Use **Hybrid Approach**:
1. Hand-write initial `specs/openapi.yaml` as API contract
2. Reference during implementation
3. FastAPI auto-generates runtime docs at `/docs`
4. Periodically sync hand-written spec with implementation

### Consequences
**Positive:**
- ✅ Clear API contract upfront
- ✅ Guides AI during implementation
- ✅ Version-controlled spec file
- ✅ FastAPI auto-docs for testing

**Negative:**
- ⚠️ Manual sync required (spec can drift from code)
- ⚠️ Extra maintenance overhead

**Note:** For this homework, the hand-written spec serves primarily as documentation and design guide. The auto-generated FastAPI docs are the source of truth at runtime.

---

## ADR-009: Concurrently for Development

**Date**: 2025-12-08  
**Status**: ✅ Accepted  

### Context
Homework Question 3 requires running both client and server simultaneously during development.

### Decision
Use **`concurrently`** npm package in root `package.json`.

```json
{
  "scripts": {
    "dev": "concurrently \"npm run dev:client\" \"npm run dev:server\"",
    "dev:client": "cd frontend && npm run dev",
    "dev:server": "cd backend && uvicorn app.main:app --reload"
  }
}
```

### Alternatives Considered
- **Shell script**: Platform-dependent (bash vs PowerShell)
- **Makefile**: Less familiar to JavaScript developers
- **Docker Compose**: Overkill for development

### Consequences
**Positive:**
- ✅ Cross-platform (works on Windows, Mac, Linux)
- ✅ Single command: `npm run dev`
- ✅ Colored output for each process
- ✅ Standard in JavaScript ecosystem

**Negative:**
- ⚠️ Requires Node.js even for Python backend management

---

## ADR-010: Vitest for Frontend Testing

**Date**: 2025-12-08  
**Status**: ✅ Accepted  

### Context
Homework Question 2 requires integration tests. Need fast test runner compatible with Vite.

### Decision
Use **Vitest** for frontend unit/integration tests, **Playwright** for E2E tests.

### Alternatives Considered
- **Jest**: Industry standard but slower with Vite
- **Mocha + Chai**: Traditional but more configuration

### Consequences
**Positive:**
- ✅ Native Vite integration (uses same config)
- ✅ Fast (leverages Vite's transform pipeline)
- ✅ Jest-compatible API (easy migration)
- ✅ Built-in coverage support

**Negative:**
- ⚠️ Younger ecosystem than Jest

---

## Summary Table

| ADR | Decision | Status | Date |
|-----|----------|--------|------|
| ADR-001 | React + Vite | ✅ Accepted | 2025-12-08 |
| ADR-002 | FastAPI Backend | ✅ Accepted | 2025-12-08 |
| ADR-003 | Repository Pattern | ✅ Accepted | 2025-12-08 |
| ADR-004 | CodeMirror 6 | ✅ Accepted | 2025-12-08 |
| ADR-005 | Pyodide WASM | ✅ Accepted | 2025-12-08 |
| ADR-006 | Native WebSockets | ✅ Accepted | 2025-12-08 |
| ADR-007 | Render Deployment | ✅ Accepted | 2025-12-08 |
| ADR-008 | Hybrid OpenAPI | ✅ Accepted | 2025-12-08 |
| ADR-009 | Concurrently | ✅ Accepted | 2025-12-08 |
| ADR-010 | Vitest Testing | ✅ Accepted | 2025-12-08 |

---

**Note for Future AI Agents:**
These decisions should not be changed without explicit user approval. If you identify a need to revisit a decision, document it in `SESSION_LOG.md` and consult the user.
