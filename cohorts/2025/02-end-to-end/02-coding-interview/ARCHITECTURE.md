# System Architecture

## 1. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Browser (Client)                             │
│                                                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │   React App      │  │  CodeMirror 6    │  │  Pyodide WASM    │  │
│  │  (UI/State)      │  │  (Code Editor)   │  │  (Python Runtime)│  │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘  │
│           │                     │                      │             │
│           └─────────────────────┴──────────────────────┘             │
│                                 │                                    │
└─────────────────────────────────┼────────────────────────────────────┘
                                  │
                    WebSocket Connection (wss://)
                    HTTP/REST API (https://)
                                  │
┌─────────────────────────────────┼────────────────────────────────────┐
│                         FastAPI Server                                │
│                                                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐  │
│  │   API Routes     │  │  WebSocket       │  │  Session Manager │  │
│  │   /sessions      │  │  /ws/{session}   │  │  (Repository)    │  │
│  └────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘  │
│           │                     │                      │             │
│           └─────────────────────┴──────────────────────┘             │
│                                 │                                    │
│                    ┌────────────┴──────────────┐                    │
│                    │  In-Memory Session Store  │                    │
│                    │  (Dict / Future: Redis)   │                    │
│                    └───────────────────────────┘                    │
└───────────────────────────────────────────────────────────────────────┘
```

## 2. Component Breakdown

### 2.1 Frontend (React + Vite)

**Directory Structure:**
```
frontend/
├── src/
│   ├── components/
│   │   ├── CodeEditor.jsx          # CodeMirror wrapper with collab
│   │   ├── SessionControls.jsx     # Create/Join session UI
│   │   ├── ExecutionPanel.jsx      # Python execution + output
│   │   └── CollaboratorList.jsx    # Active users display
│   ├── hooks/
│   │   ├── useWebSocket.js         # WebSocket connection management
│   │   ├── useCodeMirror.js        # Editor initialization
│   │   └── usePyodide.js           # WASM runtime loader
│   ├── services/
│   │   ├── api.js                  # REST API client (axios/fetch)
│   │   ├── collaboration.js        # OT message handling
│   │   └── execution.js            # Pyodide code execution
│   ├── utils/
│   │   ├── sessionId.js            # UUID generation
│   │   └── constants.js            # Config (WS_URL, API_URL)
│   ├── App.jsx                     # Main app component
│   └── main.jsx                    # Entry point
├── public/
├── package.json
└── vite.config.js
```

**Key Responsibilities:**
- Render collaborative code editor
- Manage WebSocket connection for real-time updates
- Load and execute Python code via Pyodide
- Handle UI state (session creation, user list, output)

### 2.2 Backend (FastAPI + Python)

**Directory Structure:**
```
backend/
├── app/
│   ├── main.py                     # FastAPI app initialization
│   ├── models/
│   │   ├── session.py              # Pydantic models (Session, User)
│   │   └── message.py              # WebSocket message schemas
│   ├── repositories/
│   │   ├── base.py                 # Abstract SessionRepository
│   │   ├── memory.py               # InMemorySessionRepository
│   │   └── sqlalchemy.py           # Future: SQLAlchemyRepository
│   ├── routes/
│   │   ├── sessions.py             # REST endpoints (CRUD sessions)
│   │   └── websocket.py            # WebSocket endpoint
│   ├── services/
│   │   ├── session_manager.py      # Business logic for sessions
│   │   └── collaboration.py        # OT message routing
│   └── config.py                   # Environment configuration
├── tests/
│   ├── test_routes.py
│   ├── test_websocket.py
│   └── conftest.py                 # Pytest fixtures
├── requirements.txt
└── Dockerfile
```

**Key Responsibilities:**
- Manage session lifecycle (create, get, delete)
- Route WebSocket messages between connected clients
- Validate and sanitize all inputs
- Provide OpenAPI documentation

### 2.3 Collaboration Layer (CodeMirror Collab + WebSocket)

**Message Types:**
```typescript
// Client → Server
{
  type: "join",
  sessionId: "uuid",
  userId: "uuid",
  userName: "string"
}

{
  type: "edit",
  sessionId: "uuid",
  userId: "uuid",
  changes: [...],  // CodeMirror ChangeSet
  version: number
}

{
  type: "cursor",
  sessionId: "uuid",
  userId: "uuid",
  position: number
}

// Server → Client
{
  type: "user_joined",
  userId: "uuid",
  userName: "string"
}

{
  type: "user_left",
  userId: "uuid"
}

{
  type: "update",
  userId: "uuid",
  changes: [...],
  version: number
}

{
  type: "sync",
  version: number,
  content: "string"
}
```

## 3. Data Flow

### 3.1 Session Creation Flow

```
User → React → POST /sessions → FastAPI → SessionRepository
                                              ↓
                                    Create Session (UUID)
                                              ↓
User ← React ← 201 Created + sessionId ← FastAPI
        ↓
  Navigate to /session/{id}
```

### 3.2 Collaborative Editing Flow

```
User Types → CodeEditor → Local Update (instant)
                              ↓
                    Generate ChangeSet
                              ↓
                 WebSocket.send({type: "edit", ...})
                              ↓
                         FastAPI Server
                              ↓
            Broadcast to all other clients in session
                              ↓
            Other Clients' WebSocket.onmessage
                              ↓
                Apply changes to CodeMirror
                              ↓
                    UI Updates (instant)
```

### 3.3 Code Execution Flow

```
User → Click "Run" → ExecutionPanel
                           ↓
                   Get code from editor
                           ↓
                   await pyodide.runPython(code)
                           ↓
                   Capture stdout/stderr
                           ↓
              Display output in UI (browser only)
```

**Note:** Code execution happens **entirely in the browser** via Pyodide WASM. No code is sent to the server for execution (security by design).

## 4. API Endpoints

### REST API

| Method | Endpoint | Description | Request | Response |
|--------|----------|-------------|---------|----------|
| POST | `/sessions` | Create new session | `{language: "python"}` | `{id: "uuid", createdAt: "ISO8601"}` |
| GET | `/sessions/{id}` | Get session details | - | `{id: "uuid", language: "python", users: [...]}` |
| DELETE | `/sessions/{id}` | Delete session | - | `204 No Content` |
| GET | `/health` | Health check | - | `{status: "ok"}` |
| GET | `/docs` | OpenAPI docs (auto) | - | Swagger UI |

### WebSocket API

| Endpoint | Protocol | Description |
|----------|----------|-------------|
| `/ws/{session_id}` | WebSocket | Real-time collaboration channel |

**Connection Flow:**
1. Client connects: `ws://server/ws/{session_id}?userId={uuid}&userName={name}`
2. Server broadcasts `user_joined` to all clients
3. Server sends `sync` message with current document state
4. Clients exchange `edit` and `cursor` messages
5. On disconnect, server broadcasts `user_left`

## 5. State Management

### Frontend State (React)
```javascript
// Global state (via Context or Zustand)
{
  session: {
    id: "uuid",
    language: "python",
    users: [{id, name, color}]
  },
  editor: {
    content: "string",
    version: number,
    selections: Map<userId, position>
  },
  execution: {
    isRunning: boolean,
    output: "string",
    error: "string | null"
  },
  connection: {
    status: "connected" | "disconnected" | "reconnecting",
    ws: WebSocket
  }
}
```

### Backend State (Python)
```python
# In-memory storage (SessionRepository)
{
  "session_id": {
    "id": "uuid",
    "language": "python",
    "created_at": datetime,
    "users": {
      "user_id": {
        "id": "uuid",
        "name": "string",
        "connection": WebSocket
      }
    },
    "document": {
      "content": "string",
      "version": 0
    }
  }
}
```

## 6. Technology Integration Points

### 6.1 CodeMirror 6 Integration
```javascript
import { EditorState } from '@codemirror/state';
import { EditorView } from '@codemirror/view';
import { python } from '@codemirror/lang-python';
import { javascript } from '@codemirror/lang-javascript';
import { collab, receiveUpdates, sendableUpdates } from '@codemirror/collab';

// Create collaborative editor
const state = EditorState.create({
  doc: initialContent,
  extensions: [
    python(),
    collab({
      startVersion: 0,
      clientID: userId
    }),
    EditorView.updateListener.of(update => {
      if (update.docChanged) {
        const updates = sendableUpdates(update.state);
        ws.send(JSON.stringify({type: "edit", updates}));
      }
    })
  ]
});
```

### 6.2 Pyodide Integration
```javascript
import { loadPyodide } from 'pyodide';

// Load Pyodide (once, on component mount)
const pyodide = await loadPyodide({
  indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.0/full/'
});

// Execute Python code
try {
  pyodide.runPython('import sys; import io');
  pyodide.runPython('sys.stdout = io.StringIO()');
  pyodide.runPython(userCode);
  const output = pyodide.runPython('sys.stdout.getvalue()');
  setOutput(output);
} catch (err) {
  setError(err.message);
}
```

### 6.3 FastAPI WebSocket
```python
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    await session_manager.add_user(session_id, websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            await session_manager.broadcast(session_id, data)
    except WebSocketDisconnect:
        await session_manager.remove_user(session_id, websocket)
```

## 7. Security Considerations

### 7.1 Code Execution Security
- ✅ Pyodide runs in browser WASM sandbox (no server execution)
- ✅ Limited to browser's memory and CPU
- ✅ No file system access (virtual FS only)
- ✅ No network access from Python code

### 7.2 WebSocket Security
- ✅ Validate all incoming messages
- ✅ Rate limiting per connection (e.g., 100 msg/sec)
- ✅ Session IDs are UUIDs (not guessable)
- ✅ CORS configured for production domain
- ⚠️ Future: Add authentication/authorization

### 7.3 Input Validation
- ✅ Pydantic models for all API inputs
- ✅ WebSocket message schema validation
- ✅ Sanitize user names (no XSS)

## 8. Scalability Considerations

### Current (Homework) Architecture
- In-memory session storage (single server)
- WebSocket connections on same server
- Suitable for: Demo, low traffic (< 100 concurrent sessions)

### Future Production Architecture
- **Session Storage**: Redis (centralized state)
- **WebSocket**: Sticky sessions or Redis Pub/Sub for multi-server
- **Database**: PostgreSQL + SQLAlchemy (session history)
- **CDN**: Cloudflare for static assets and Pyodide
- **Monitoring**: Prometheus + Grafana for metrics

## 9. Performance Optimizations

### Frontend
- Lazy load Pyodide (only when user clicks "Run")
- Code-split routes (`React.lazy` + `Suspense`)
- Debounce WebSocket sends (batch rapid edits)
- Virtual scrolling for large outputs

### Backend
- Connection pooling for future DB
- Message compression (WebSocket permessage-deflate)
- Horizontal scaling with Redis
- Health checks for container orchestration

## 10. Deployment Architecture (Render)

```
┌────────────────────────────────────────────────────────────┐
│                        Render                               │
│                                                             │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Docker Container                              │  │
│  │                                                       │  │
│  │  ┌──────────────┐         ┌──────────────┐          │  │
│  │  │   Nginx      │────────▶│   FastAPI    │          │  │
│  │  │  (Static     │         │   (Uvicorn)  │          │  │
│  │  │   Assets)    │         │   :8000      │          │  │
│  │  └──────────────┘         └──────────────┘          │  │
│  │                                                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                             │
│  Environment Variables:                                    │
│  - FRONTEND_URL                                            │
│  - CORS_ORIGINS                                            │
│  - LOG_LEVEL                                               │
└────────────────────────────────────────────────────────────┘
```

## 11. Error Handling

### Frontend
- WebSocket reconnection logic (exponential backoff)
- Pyodide loading failure → show error + retry
- Network errors → display user-friendly message
- Code execution timeout (prevent infinite loops)

### Backend
- WebSocket disconnect → cleanup session
- Invalid JSON → log + send error response
- Session not found → 404 with message
- Rate limit exceeded → close connection

## 12. Monitoring & Observability

### Metrics to Track
- Active sessions count
- Active WebSocket connections
- Messages per second
- Average message latency
- Code execution count (frontend analytics)
- Error rates

### Logging
- Structured JSON logs
- Log levels: DEBUG, INFO, WARNING, ERROR
- Correlation IDs for request tracing
- WebSocket event logging

---

**Last Updated**: 2025-12-08  
**Status**: ✅ Approved  
**Version**: 1.0
