# Product Specifications

This document defines the functional requirements for the Collaborative Coding Interview Platform.

## Project Overview

**Name**: Collaborative Coding Interview Platform  
**Purpose**: Real-time collaborative code editor for conducting technical interviews  
**Target Users**: Interviewers and candidates conducting remote coding interviews  
**Homework Assignment**: AI Dev Tools Zoomcamp - Week 2 (End-to-End Application Development)

---

## Core Requirements (Homework Assignment)

The application must satisfy these requirements from `cohorts/2025/02-end-to-end/homework.md`:

1. ✅ Create a link and share it with candidates
2. ✅ Allow everyone who connects to edit code in the code panel
3. ✅ Show real-time updates to all connected users
4. ✅ Support syntax highlighting for multiple languages (JavaScript, Python)
5. ✅ Execute code safely in the browser

---

## Functional Requirements

### REQ-001: Session Management

**Priority**: Critical  
**Status**: Required for Q1  

#### User Story
As an **interviewer**, I want to **create a new coding session** so that I can **share a unique link with the candidate**.

#### Acceptance Criteria
- [ ] User can create a new session with a single click
- [ ] System generates a unique session ID (UUID)
- [ ] System returns a shareable URL (e.g., `/session/{id}`)
- [ ] Session link is copyable to clipboard
- [ ] Session persists for the duration of the interview
- [ ] Multiple users can join the same session using the link

#### Technical Notes
- Session ID must be a UUID (not sequential for security)
- Initial implementation: in-memory storage (lost on server restart)
- Future: persistent storage with SQLAlchemy

#### API Endpoints
```
POST /sessions
Response: {id: "uuid", createdAt: "ISO8601"}
```

---

### REQ-002: Join Session

**Priority**: Critical  
**Status**: Required for Q1  

#### User Story
As a **candidate**, I want to **join a session using a shared link** so that I can **participate in the coding interview**.

#### Acceptance Criteria
- [ ] User can access session via `/session/{id}` URL
- [ ] System validates session exists
- [ ] System prompts for user name (optional but recommended)
- [ ] User is automatically connected to the session
- [ ] Other participants see when a new user joins
- [ ] User sees current document state upon joining

#### Technical Notes
- WebSocket connection established on page load
- Server sends `sync` message with current document state
- Broadcast `user_joined` event to all participants

#### API Endpoints
```
GET /sessions/{id}
WebSocket /ws/{session_id}?userId={uuid}&userName={name}
```

---

### REQ-003: Collaborative Code Editing

**Priority**: Critical  
**Status**: Required for Q1  

#### User Story
As a **session participant**, I want to **edit code in real-time with others** so that we can **collaborate during the interview**.

#### Acceptance Criteria
- [ ] Multiple users can type simultaneously
- [ ] Changes appear instantly for all users (<100ms latency)
- [ ] Conflicts are resolved automatically (OT)
- [ ] Each user has a unique cursor color
- [ ] User can see other users' cursor positions
- [ ] Document state remains consistent across all clients
- [ ] No data loss even with concurrent edits

#### Technical Notes
- Use CodeMirror 6 with `@codemirror/collab`
- WebSocket messages: `{type: "edit", changes: [...]}`
- Operational Transformation handles conflict resolution
- Version number tracks document state

#### WebSocket Messages
```javascript
// Outgoing (client → server)
{type: "edit", sessionId, userId, changes: [...], version: 0}

// Incoming (server → client)
{type: "update", userId, changes: [...], version: 1}
```

---

### REQ-004: Syntax Highlighting (JavaScript)

**Priority**: High  
**Status**: Required for Q4  

#### User Story
As a **session participant**, I want **JavaScript syntax highlighting** so that I can **write and read code more easily**.

#### Acceptance Criteria
- [ ] JavaScript keywords are highlighted (const, let, function, etc.)
- [ ] Strings, numbers, comments are color-coded
- [ ] Syntax errors are not highlighted (no linting, just highlighting)
- [ ] Highlighting updates in real-time as user types
- [ ] Works in collaborative mode

#### Technical Notes
- Use `@codemirror/lang-javascript` package
- Theme: default CodeMirror light/dark theme

---

### REQ-005: Syntax Highlighting (Python)

**Priority**: High  
**Status**: Required for Q4  

#### User Story
As a **session participant**, I want **Python syntax highlighting** so that I can **write and read Python code more easily**.

#### Acceptance Criteria
- [ ] Python keywords are highlighted (def, class, import, etc.)
- [ ] Strings, numbers, comments are color-coded
- [ ] Indentation is preserved (critical for Python)
- [ ] Highlighting updates in real-time
- [ ] Works in collaborative mode

#### Technical Notes
- Use `@codemirror/lang-python` package
- Consider adding auto-indent support

---

### REQ-006: Code Execution (Python)

**Priority**: High  
**Status**: Required for Q5  

#### User Story
As a **session participant**, I want to **execute Python code in the browser** so that I can **test my solutions during the interview**.

#### Acceptance Criteria
- [ ] User can click "Run" button to execute code
- [ ] Code executes in browser (not on server)
- [ ] Standard output (print statements) is displayed
- [ ] Errors are caught and displayed
- [ ] Execution timeout prevents infinite loops (e.g., 10 seconds)
- [ ] Loading indicator shown while Pyodide initializes
- [ ] Works offline after initial Pyodide load

#### Technical Notes
- Use Pyodide 0.25+ for WASM execution
- Lazy load Pyodide (only when user first clicks "Run")
- Capture stdout: `sys.stdout = io.StringIO()`
- Security: No server-side execution

#### UI Elements
```
[Run Code] button
Loading: "Initializing Python..." (first run only)
Output panel:
  > print("Hello, world!")
  Hello, world!
```

---

### REQ-007: User Presence Awareness

**Priority**: Medium  
**Status**: Nice-to-have for Q1  

#### User Story
As a **session participant**, I want to **see who else is in the session** so that I **know who I'm collaborating with**.

#### Acceptance Criteria
- [ ] List of active users displayed (names + colors)
- [ ] User count shown (e.g., "3 users online")
- [ ] List updates when users join/leave
- [ ] Each user has a unique avatar color
- [ ] Current user is highlighted in the list

#### Technical Notes
- WebSocket events: `user_joined`, `user_left`
- Store user list in React state
- Assign colors from predefined palette

---

### REQ-008: Session Cleanup

**Priority**: Medium  
**Status**: Nice-to-have  

#### User Story
As the **system**, I want to **clean up inactive sessions** so that **memory doesn't grow unbounded**.

#### Acceptance Criteria
- [ ] Sessions with no active users for 1 hour are deleted
- [ ] Session cleanup runs every 15 minutes
- [ ] Users are notified if they try to rejoin a deleted session

#### Technical Notes
- Background task in FastAPI
- Check `last_activity` timestamp
- Future: persist sessions to database before deletion

---

### REQ-009: Error Handling

**Priority**: High  
**Status**: Required  

#### User Story
As a **user**, I want **clear error messages** when something goes wrong so that I **know what to do**.

#### Acceptance Criteria
- [ ] Session not found → "Session does not exist or has expired"
- [ ] WebSocket disconnect → "Connection lost. Reconnecting..."
- [ ] Pyodide load failure → "Failed to load Python. Please refresh."
- [ ] Code execution timeout → "Execution timed out after 10 seconds"
- [ ] Network errors display user-friendly messages

---

### REQ-010: Responsive Design

**Priority**: Medium  
**Status**: Nice-to-have  

#### User Story
As a **mobile user**, I want the **interface to work on smaller screens** so that I can **participate from any device**.

#### Acceptance Criteria
- [ ] Layout adapts to screen size (responsive CSS)
- [ ] Editor is usable on tablets (768px+)
- [ ] Desktop-optimized (1024px+)
- [ ] Mobile support is best-effort (may have limitations)

---

## Homework-Specific Requirements

### Q1: Initial Implementation

**Requirement**: Implement frontend and backend with AI assistance.

**Deliverable**: 
- Frontend: React + Vite with CodeMirror
- Backend: FastAPI with WebSocket support
- Basic session management (create, join)

**Success Criteria**:
- [ ] REQ-001: Session Management implemented
- [ ] REQ-002: Join Session implemented
- [ ] REQ-003: Collaborative editing works

---

### Q2: Integration Tests

**Requirement**: Write tests that verify client-server interaction.

**Deliverable**:
- Integration tests using Vitest (frontend) and Pytest (backend)
- README.md with test commands

**Success Criteria**:
- [ ] Test: Create session via API
- [ ] Test: Join session via WebSocket
- [ ] Test: Send/receive collaborative edit messages
- [ ] Test: Multiple clients can edit simultaneously
- [ ] Test command documented in README

**Expected Command**: `npm test` or `npm run test:integration`

---

### Q3: Concurrent Development

**Requirement**: Run both client and server with a single command using `concurrently`.

**Deliverable**:
- Root `package.json` with `dev` script

**Success Criteria**:
- [ ] `npm run dev` starts both frontend and backend
- [ ] Output shows logs from both processes
- [ ] Color-coded output (blue for client, green for server)

**Expected Command**: `npm run dev`

---

### Q4: Syntax Highlighting

**Requirement**: Add syntax highlighting for JavaScript and Python.

**Deliverable**:
- CodeMirror with language support

**Success Criteria**:
- [ ] REQ-004: JavaScript highlighting implemented
- [ ] REQ-005: Python highlighting implemented
- [ ] User can switch languages (or separate sessions)

**Library Used**: CodeMirror 6 (`@codemirror/lang-javascript`, `@codemirror/lang-python`)

---

### Q5: Code Execution

**Requirement**: Execute code safely in the browser using WASM.

**Deliverable**:
- Pyodide integration for Python execution

**Success Criteria**:
- [ ] REQ-006: Python code execution implemented
- [ ] Code runs in browser (verify in Network tab: no execution API calls)
- [ ] Output displayed correctly
- [ ] Errors handled gracefully

**Library Used**: Pyodide 0.25+

---

### Q6: Containerization

**Requirement**: Create a Dockerfile with both frontend and backend.

**Deliverable**:
- Dockerfile with multi-stage build
- Both apps in single container

**Success Criteria**:
- [ ] Dockerfile builds successfully
- [ ] Container runs both frontend and backend
- [ ] Health check endpoint works (`/health`)
- [ ] Frontend served via Nginx
- [ ] Backend accessible at `/api/*`

**Base Image**: TBD (likely `python:3.11-slim` or `node:20-alpine`)

---

### Q7: Deployment

**Requirement**: Deploy the containerized application.

**Deliverable**:
- Deployed application on Render

**Success Criteria**:
- [ ] Application accessible via public URL
- [ ] WebSocket connections work
- [ ] Multiple users can collaborate
- [ ] Code execution works

**Service Used**: Render

---

## Non-Functional Requirements

### NFR-001: Performance

- WebSocket latency: <100ms for local edits
- Pyodide load time: <5 seconds (first time)
- Page load time: <2 seconds (without Pyodide)
- Support 10+ concurrent users per session

### NFR-002: Security

- No server-side code execution
- UUID session IDs (not guessable)
- Input validation for all API calls
- CORS configured for production domain
- Rate limiting on WebSocket (100 msg/sec per client)

### NFR-003: Reliability

- WebSocket auto-reconnect (exponential backoff)
- Document state recovery after reconnect
- Graceful degradation if Pyodide fails
- Error logging for debugging

### NFR-004: Usability

- Intuitive UI (no user manual needed)
- Clear error messages
- Loading indicators for async operations
- Keyboard shortcuts (Ctrl+Enter to run code)

---

## Out of Scope (for Homework)

The following features are **not** required for this homework:

- ❌ User authentication/authorization
- ❌ Persistent session history (database)
- ❌ Video/audio conferencing
- ❌ Code saving/exporting
- ❌ Multiple files per session
- ❌ Linting or autocomplete
- ❌ Code formatting (Prettier integration)
- ❌ Session recording/playback
- ❌ Admin dashboard

---

## Success Metrics

The project is successful if:

1. ✅ All 7 homework questions are answered with working implementation
2. ✅ Multiple users can collaborate in real-time
3. ✅ Python code executes in browser
4. ✅ Application is deployed and accessible
5. ✅ Code is committed to GitHub with clear commit history

---

## User Flows

### Flow 1: Interviewer Creates Session
```
1. Interviewer visits homepage
2. Clicks "Create New Session"
3. System generates unique link
4. Interviewer copies link
5. Interviewer shares link with candidate (email, chat, etc.)
6. Interviewer opens session in browser
7. Editor loads with empty document
```

### Flow 2: Candidate Joins Session
```
1. Candidate receives session link
2. Candidate opens link in browser
3. System prompts for name (optional)
4. Candidate enters name and clicks "Join"
5. WebSocket connects
6. Editor loads with current document state
7. Interviewer sees "Candidate joined" notification
```

### Flow 3: Collaborative Editing
```
1. Interviewer types: "def fibonacci(n):"
2. Candidate sees update instantly
3. Candidate types: "    if n <= 1:"
4. Both see syntax highlighting
5. Interviewer sees candidate's cursor position
6. No conflicts, smooth collaboration
```

### Flow 4: Code Execution
```
1. User types Python code in editor
2. User clicks "Run Code" button
3. (First time) Pyodide loads (3-5 seconds)
4. Code executes in browser
5. Output appears in panel below editor
6. If error, stack trace is shown
7. User can edit and run again
```

---

## UI Mockup (Text-based)

```
┌─────────────────────────────────────────────────────────────┐
│  Collaborative Coding Interview                             │
│  Session: abc-123-def   [Copy Link]  👤 2 users online     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  def fibonacci(n):                                          │
│      if n <= 1:                                             │
│          return n                                           │
│      return fibonacci(n-1) + fibonacci(n-2)    👤Interviewer│
│                                                             │
│  print(fibonacci(10))                          👤Candidate  │
│                                                             │
│                                                             │
│                                          [Run Code ▶]       │
├─────────────────────────────────────────────────────────────┤
│  Output:                                                    │
│  55                                                         │
└─────────────────────────────────────────────────────────────┘
```

---

**Last Updated**: 2025-12-08  
**Status**: ✅ Approved  
**Version**: 1.0
