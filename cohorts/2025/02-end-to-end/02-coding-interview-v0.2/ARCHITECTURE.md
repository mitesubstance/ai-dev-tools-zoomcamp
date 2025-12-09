# System Architecture

## Overview
This document describes the system design, component topology, data flow, and technical architecture for the Real-Time Collaborative Coding Interview Platform.

## System Components

### Frontend
- **Technology**: React 18+ with Vite
- **Responsibility**: User interface, code editing, WebSocket client, client-side Python execution
- **Key Components**:
  - **CodeEditor Component**: CodeMirror 6 integration for collaborative editing
  - **SessionManager**: Handles session creation and joining
  - **WebSocketClient**: Manages real-time communication with backend
  - **PyodideRunner**: Executes Python code in browser using WASM
  - **OutputDisplay**: Shows code execution results and errors
  - **ConnectionStatus**: Displays real-time connection state

### Backend
- **Technology**: FastAPI (Python 3.11+)
- **Responsibility**: WebSocket server, session management, message broadcasting
- **Key Components**:
  - **SessionStore**: In-memory storage for active sessions
  - **WebSocketManager**: Handles WebSocket connections and broadcasting
  - **SessionRouter**: API endpoints for session operations
  - **ConnectionManager**: Tracks active connections per session

### Data Storage
- **Technology**: In-memory (Python dictionaries) for v1
- **Schema**: 
  ```python
  {
    "session_id": {
      "code": str,  # Current code content
      "language": str,  # Programming language (default: "python")
      "connections": Set[WebSocket],  # Active WebSocket connections
      "created_at": datetime,
      "last_activity": datetime
    }
  }
  ```
- **Future**: Consider Redis for distributed sessions or database for persistence

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        Browser Client                       │
│  ┌────────────────────────────────────────────────────┐    │
│  │            React Application (Vite)                │    │
│  │                                                     │    │
│  │  ┌─────────────┐  ┌──────────────┐  ┌──────────┐ │    │
│  │  │  CodeMirror │  │  WebSocket   │  │ Pyodide  │ │    │
│  │  │  Editor (6) │  │   Client     │  │  WASM    │ │    │
│  │  └─────────────┘  └──────────────┘  └──────────┘ │    │
│  │         │                 │                │       │    │
│  │         └────────┬────────┘                │       │    │
│  │                  │                         │       │    │
│  └──────────────────│─────────────────────────│───────┘    │
│                     │                         │            │
└─────────────────────│─────────────────────────│────────────┘
                      │                         │
                      │ WebSocket               │ In-Browser
                      │ (wss://)                │ Execution
                      │                         │ (No Server)
                      ▼                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Backend                          │
│  ┌────────────────────────────────────────────────────┐    │
│  │         WebSocket Manager & Session Store          │    │
│  │                                                     │    │
│  │  ┌──────────────┐  ┌─────────────┐  ┌──────────┐ │    │
│  │  │  Connection  │  │   Session   │  │   HTTP   │ │    │
│  │  │   Manager    │  │    Store    │  │  Router  │ │    │
│  │  │              │  │  (In-Mem)   │  │          │ │    │
│  │  └──────────────┘  └─────────────┘  └──────────┘ │    │
│  │                                                     │    │
│  └────────────────────────────────────────────────────┘    │
│                                                             │
└─────────────────────────────────────────────────────────────┘

Key Characteristics:
- Client-side Python execution (no code sent to server for execution)
- WebSocket for real-time collaborative editing
- Stateless backend (sessions in-memory, ephemeral)
```

## Data Flow

### Session Creation Flow
1. User clicks "Create Session" in Frontend
2. Frontend sends POST request to `/api/sessions`
3. Backend generates UUID for session
4. Backend creates session in SessionStore
5. Backend returns session ID to Frontend
6. Frontend redirects to `/session/{session_id}`

### Session Join Flow
1. User navigates to `/session/{session_id}`
2. Frontend establishes WebSocket connection to `/ws/{session_id}`
3. Backend validates session exists
4. Backend adds connection to session's connection set
5. Backend sends current session state (code, language) to new user
6. Backend broadcasts "user_joined" event to all session participants

### Collaborative Editing Flow
1. User types in CodeMirror editor
2. Editor triggers onChange event with changes
3. Frontend sends `code_update` message via WebSocket
4. Backend receives message and updates session code
5. Backend broadcasts `code_update` to all other connections in session
6. Other clients receive update and apply to their editors

### Code Execution Flow (Client-Side Only)
1. User clicks "Run Code" button
2. Frontend loads Pyodide (if not already loaded)
3. Pyodide executes code in Web Worker
4. Execution output/errors captured
5. Results displayed in output panel
6. **No server interaction** - purely client-side

## API Design

### HTTP Endpoints

#### Create Session
- **Method**: `POST /api/sessions`
- **Description**: Creates a new coding session
- **Request Body**: `{ "language": "python" }` (optional)
- **Response**: `{ "session_id": "uuid", "created_at": "timestamp" }`

#### Get Session Info
- **Method**: `GET /api/sessions/{session_id}`
- **Description**: Retrieves session metadata
- **Response**: `{ "session_id": "uuid", "language": "python", "active_users": 2 }`

#### Health Check
- **Method**: `GET /api/health`
- **Description**: Backend health status
- **Response**: `{ "status": "ok" }`

### WebSocket Protocol

#### Connection
- **Endpoint**: `ws://localhost:8000/ws/{session_id}`
- **On Connect**: Server sends current session state

#### Message Types

```typescript
// Client -> Server
{
  "type": "code_update",
  "data": {
    "code": string,
    "timestamp": number
  }
}

// Server -> Client
{
  "type": "code_update",
  "data": {
    "code": string,
    "user_id": string,  // Future enhancement
    "timestamp": number
  }
}

{
  "type": "session_state",
  "data": {
    "code": string,
    "language": string,
    "active_users": number
  }
}

{
  "type": "user_joined",
  "data": {
    "user_count": number
  }
}

{
  "type": "user_left",
  "data": {
    "user_count": number
  }
}

{
  "type": "error",
  "data": {
    "message": string
  }
}
```

## Security Considerations
- **Session IDs**: UUID v4 (cryptographically random)
- **Code Execution**: Client-side only (Pyodide), no server-side execution risk
- **Input Validation**: Session ID format validation
- **CORS**: Configured for development (localhost), restrict in production
- **Rate Limiting**: Not implemented in v1, recommended for production
- **WebSocket Authentication**: Not implemented in v1 (sessions are public via link)
- **XSS Protection**: React's built-in escaping, CodeMirror handles user input safely

## Scalability & Performance

### Current Architecture (v1)
- **Horizontal Scaling**: Limited - in-memory session store
- **Vertical Scaling**: Good - async FastAPI handles many concurrent connections
- **Session Limit**: ~10-50 concurrent sessions per instance
- **Users per Session**: 2-5 recommended, up to 10 possible

### Future Improvements
- **Redis**: Shared session store for horizontal scaling
- **Load Balancer**: Distribute WebSocket connections across instances
- **Sticky Sessions**: Required if using multiple backend instances without shared store
- **Database**: PostgreSQL for session persistence
- **CDN**: Serve static React app from CDN
- **Monitoring**: Add metrics for session count, connection duration, message rate

## Technology Stack Summary

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Frontend Framework | React | 18+ | UI component library |
| Frontend Build | Vite | 5+ | Fast dev server and build tool |
| Code Editor | CodeMirror | 6 | Rich code editing experience |
| Python Execution | Pyodide | Latest | WASM Python runtime |
| Backend Framework | FastAPI | 0.100+ | Async API server with WebSocket support |
| WebSocket | Native WebSocket API | - | Real-time bidirectional communication |
| Package Manager (FE) | npm | 9+ | JavaScript dependencies |
| Package Manager (BE) | pip/uv | - | Python dependencies |
| Development | concurrently | Latest | Run frontend + backend simultaneously |
| Testing (Future) | Pytest, Jest | - | Unit and integration tests |

## Development Environment

### Prerequisites
- **Node.js**: 18+ (for npm and Vite)
- **Python**: 3.11+ (for FastAPI)
- **npm**: 9+ (for frontend dependencies)
- **pip or uv**: Latest (for backend dependencies)

### Directory Structure
```
02-coding-interview-v0.2/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── requirements.txt        # Python dependencies
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routers/
│   │   │   ├── sessions.py     # Session HTTP endpoints
│   │   │   └── websocket.py    # WebSocket endpoints
│   │   ├── models/
│   │   │   └── session.py      # Session data models
│   │   └── services/
│   │       ├── session_store.py
│   │       └── connection_manager.py
│   └── tests/                  # Backend tests (future)
│
├── frontend/
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   ├── src/
│   │   ├── main.jsx            # React entry point
│   │   ├── App.jsx             # Root component
│   │   ├── components/
│   │   │   ├── CodeEditor.jsx  # CodeMirror wrapper
│   │   │   ├── SessionManager.jsx
│   │   │   ├── OutputPanel.jsx
│   │   │   └── ConnectionStatus.jsx
│   │   ├── services/
│   │   │   ├── websocket.js    # WebSocket client
│   │   │   ├── pyodide.js      # Pyodide wrapper
│   │   │   └── api.js          # HTTP API client
│   │   └── hooks/
│   │       └── useWebSocket.js
│   └── tests/                  # Frontend tests (future)
│
├── package.json                # Root package.json for concurrently
└── README.md
```

### Running Locally
```bash
# Install dependencies
cd backend && pip install -r requirements.txt
cd ../frontend && npm install

# Run both services (from root)
npm run dev

# Or run separately:
# Terminal 1: cd backend && uvicorn main:app --reload --port 8000
# Terminal 2: cd frontend && npm run dev
```

### Environment Variables
- `BACKEND_PORT`: Backend server port (default: 8000)
- `FRONTEND_PORT`: Frontend dev server port (default: 5173)
- `VITE_API_URL`: Backend API URL (default: http://localhost:8000)
- `VITE_WS_URL`: WebSocket URL (default: ws://localhost:8000)

## Future Architecture Considerations

### Phase 2 Enhancements
- User authentication (sessions with ownership)
- Session persistence (save/load sessions)
- Multiple language execution support (JavaScript via browser, others TBD)
- Collaborative cursors (show where others are typing)
- Chat functionality within sessions
- Session expiration and cleanup

### Phase 3 Enhancements
- Video/audio integration (WebRTC)
- Recording and playback
- Code review and commenting
- Template library (starter code for common problems)
- Admin dashboard
- Analytics and metrics

---
*Last Updated: 2025-12-09*
*Version: 0.2*
