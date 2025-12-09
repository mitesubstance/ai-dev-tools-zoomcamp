# Product Specifications

## Overview
A real-time collaborative coding interview platform that allows multiple users to share a coding session, edit code simultaneously, and execute Python code safely in the browser.

---

## Requirement Template (Full-Stack TDD)

```markdown
### REQ-XXX: [Feature Name]

**Priority**: [Critical | High | Medium | Low]
**Status**: [Draft | Approved | In Progress | Completed | Deferred]
**Dependencies**: [List any REQ-IDs this depends on]

**Description**:
[Detailed description of the requirement]

**User Story**:
As a [user type], I want [goal] so that [benefit].

**Acceptance Criteria**:
- [ ] Criterion 1
- [ ] Criterion 2

**Backend Verification** (Tests MUST pass before feature is "Done"):
- [ ] Test: `tests/backend/test_[feature].py` - Verify API endpoint returns status 200
- [ ] Test: `tests/backend/test_[feature].py` - Verify response JSON payload structure
- [ ] Test: `tests/backend/test_[feature].py` - Verify business logic correctness
- [ ] Test: `tests/backend/test_[feature].py` - Verify error handling (4xx/5xx scenarios)

**Frontend Verification** (Tests MUST pass before feature is "Done" - using Vitest + React Testing Library):
- [ ] Test: `frontend/src/__tests__/[Component].test.jsx` - Verify component renders without errors
- [ ] Test: `frontend/src/__tests__/[Component].test.jsx` - Verify user interaction (click/input) triggers correct behavior
- [ ] Test: `frontend/src/__tests__/[Component].test.jsx` - Verify state management and updates
- [ ] Test: `frontend/src/__tests__/[Component].test.jsx` - Verify error states and edge cases

**Integration Verification** (Optional but recommended):
- [ ] Test: End-to-end test verifying complete user flow

**Technical Notes**:
[Any technical considerations or constraints]

**Test-First Implementation Order**:
1. Write failing backend tests
2. Implement backend code to pass tests
3. Write failing frontend tests
4. Implement frontend code to pass tests
5. Refactor if needed
6. Run full test suite (backend + frontend)
```

---

## Functional Requirements

### REQ-001: Session Management

**Priority**: Critical  
**Status**: Approved  
**Dependencies**: None

**Description**:
Users must be able to create unique coding interview sessions and share them via links. Each session should have a unique identifier and allow multiple users to join.

**User Story**:
As an interviewer, I want to create a coding session and share a link with candidates so that we can conduct remote coding interviews together.

**Acceptance Criteria**:
- [ ] User can create a new coding session
- [ ] Each session has a unique, shareable URL/link
- [ ] Multiple users can join the same session using the link
- [ ] Session persists while at least one user is connected
- [ ] Session state is maintained across user connections/disconnections

**Technical Notes**:
- Use UUIDs for session identifiers
- Backend manages session state
- WebSocket connections track active users per session

**Backend Verification** (Tests MUST pass before feature is "Done"):
- [x] Test: `tests/backend/test_sessions.py` - POST /api/sessions returns 201 and unique session_id ✅
- [x] Test: `tests/backend/test_sessions.py` - GET /api/sessions/{id} returns 200 with session data ✅
- [x] Test: `tests/backend/test_sessions.py` - Session ID is valid UUID v4 format ✅
- [x] Test: `tests/backend/test_sessions.py` - GET non-existent session returns 404 ✅
- [x] Test: `tests/backend/test_sessions.py` - Multiple concurrent session creation works correctly ✅

**Frontend Verification** (Tests MUST pass before feature is "Done"):
- [x] Test: `frontend/src/__tests__/App.test.jsx` - CreateSession button renders ✅
- [x] Test: `frontend/src/__tests__/App.test.jsx` - Clicking create button calls API ✅
- [x] Test: `frontend/src/__tests__/App.test.jsx` - Session link is displayed after creation ✅
- [x] Test: `frontend/src/__tests__/App.test.jsx` - Session link is copyable to clipboard ✅
- [x] Test: `frontend/src/__tests__/App.test.jsx` - Error handling for failed creation ✅

**Integration Verification**:
- [ ] Test: End-to-end test - Create session, copy link, join from new browser tab

**Test Scenarios**:
1. Create a new session and verify unique ID is generated
2. Share session link and verify multiple users can join
3. Verify session state persists when users reconnect

---

### REQ-002: Real-Time Collaborative Code Editing

**Priority**: Critical  
**Status**: Approved  
**Dependencies**: REQ-001

**Description**:
Multiple users in the same session must be able to edit code simultaneously with real-time synchronization. Changes made by any user should be instantly visible to all other users in the session.

**User Story**:
As a coding interview participant, I want to see code changes in real-time so that I can collaborate effectively with other participants.

**Acceptance Criteria**:
- [ ] Code editor supports multiple concurrent users
- [ ] Changes are synchronized in real-time via WebSockets
- [ ] Low latency updates (< 200ms typical)
- [ ] No conflicts when multiple users edit simultaneously
- [ ] Cursor positions visible for all users (optional for v1)

**Technical Notes**:
- Use WebSockets for real-time communication
- CodeMirror 6 as the code editor component
- Broadcast all editor changes to connected clients
- Consider operational transformation or CRDT for conflict resolution (simplified approach for v1)

**Backend Verification** (Tests MUST pass before feature is "Done"):
- [x] Test: `tests/backend/test_websocket.py` - WebSocket connection accepted ✅
- [x] Test: `tests/backend/test_websocket.py` - code_update message broadcast to all clients in session ✅
- [x] Test: `tests/backend/test_websocket.py` - New client receives current session state on connect ✅
- [x] Test: `tests/backend/test_websocket.py` - user_joined event broadcast correctly ✅
- [x] Test: `tests/backend/test_websocket.py` - user_left event broadcast on disconnect ✅

**Frontend Verification** (Tests MUST pass before feature is "Done"):
- [ ] Test: `frontend/src/__tests__/CodeEditor.test.jsx` - CodeMirror editor renders
- [ ] Test: `frontend/src/__tests__/CodeEditor.test.jsx` - Local edits trigger WebSocket message send
- [ ] Test: `frontend/src/__tests__/CodeEditor.test.jsx` - Received updates applied to editor
- [ ] Test: `frontend/src/__tests__/useWebSocket.test.js` - WebSocket connection management
- [ ] Test: `frontend/src/__tests__/useWebSocket.test.js` - Reconnection logic works correctly

**Integration Verification**:
- [ ] Test: Two browser windows editing same session synchronize changes

**Test Scenarios**:
1. Two users edit different parts of code simultaneously
2. Two users edit the same line and verify proper synchronization
3. User joins mid-session and receives current code state
4. Verify changes persist across disconnections

---

### REQ-003: Python Code Execution (Client-Side)

**Priority**: High  
**Status**: Approved  
**Dependencies**: REQ-001

**Description**:
Users must be able to execute Python code directly in the browser without server-side execution. This ensures safety, scalability, and reduces server load.

**User Story**:
As a candidate, I want to run my Python code and see the output immediately so that I can test my solution during the interview.

**Acceptance Criteria**:
- [ ] Execute Python code in the browser using Pyodide (WASM)
- [ ] Display code execution output (stdout)
- [ ] Display error messages if code fails
- [ ] Execution happens client-side (no server processing)
- [ ] Support standard Python library functions
- [ ] Execution timeout to prevent infinite loops

**Technical Notes**:
- Use Pyodide for Python execution in browser
- Load Pyodide on-demand to optimize initial page load
- Capture stdout and stderr
- Run in Web Worker to avoid blocking UI
- Implement timeout mechanism

**Backend Verification** (Tests MUST pass before feature is "Done"):
- [ ] Note: No backend tests required (client-side only feature)

**Frontend Verification** (Tests MUST pass before feature is "Done"):
- [ ] Test: `frontend/src/__tests__/PyodideRunner.test.js` - Pyodide loads successfully
- [ ] Test: `frontend/src/__tests__/PyodideRunner.test.js` - Execute simple Python code and capture stdout
- [ ] Test: `frontend/src/__tests__/PyodideRunner.test.js` - Execute code with syntax errors and capture error
- [ ] Test: `frontend/src/__tests__/PyodideRunner.test.js` - Execute code with runtime errors
- [ ] Test: `frontend/src/__tests__/PyodideRunner.test.js` - Timeout mechanism prevents infinite loops
- [ ] Test: `frontend/src/__tests__/OutputPanel.test.jsx` - Output panel displays results
- [ ] Test: `frontend/src/__tests__/OutputPanel.test.jsx` - Error messages displayed in red/distinct style

**Integration Verification**:
- [ ] Test: Run button executes code and displays output in same browser session

**Test Scenarios**:
1. Execute simple Python code (print statements)
2. Execute code with errors and verify error messages
3. Execute code with loops and verify output
4. Test timeout for infinite loops

---

### REQ-004: Multi-Language Syntax Highlighting Support (Architecture)

**Priority**: Medium  
**Status**: Completed  
**Dependencies**: REQ-002

**Description**:
The code editor architecture must support adding syntax highlighting for multiple programming languages in the future. Initial implementation will focus on Python, but the system should be extensible.

**User Story**:
As a platform maintainer, I want the ability to easily add support for new programming languages so that the platform can grow to support more interview scenarios.

**Acceptance Criteria**:
- [x] CodeMirror 6 configured with language extension system
- [x] Python syntax highlighting implemented
- [x] JavaScript syntax highlighting implemented
- [x] Architecture allows adding new languages via language packs
- [x] Language selection mechanism prepared (prop-based for v1)
- [x] Documentation on how to add new languages (ADR-012)
- [x] Centralized language configuration in `/frontend/src/utils/languages.js`

**Technical Notes**:
- CodeMirror 6 has excellent language extension support
- @codemirror/lang-python for Python support ✅
- @codemirror/lang-javascript for JavaScript support ✅
- Future languages: @codemirror/lang-java, @codemirror/lang-cpp, etc.
- Language state managed via component props (defaults to 'python')
- Helper functions: `getLanguageExtension()`, `getDefaultPlaceholder()`

**Frontend Verification** (Tests MUST pass before feature is "Done"):
- [x] Test: `frontend/src/components/__tests__/CodeEditor.test.jsx` - Python syntax support ✅
- [x] Test: `frontend/src/components/__tests__/CodeEditor.test.jsx` - JavaScript syntax support ✅
- [x] Test: `frontend/src/components/__tests__/CodeEditor.test.jsx` - Language switching works ✅
- [x] Test: `frontend/src/components/__tests__/CodeEditor.test.jsx` - Unsupported language handling ✅

**Test Scenarios**:
1. ✅ Verify Python syntax highlighting works correctly (18 tests passing)
2. ✅ Verify architecture allows importing new language packs (JavaScript added successfully)
3. ✅ Test switching between languages (dynamic language switching implemented and tested)

**Implementation Summary**:
- Added @codemirror/lang-javascript package
- Enhanced CodeEditor component with `language` prop
- Created helper functions for language extensions and placeholders
- Centralized language configuration in utilities file
- 18 comprehensive tests passing (including 3 new test suites for JavaScript and language switching)
- Documented in ADR-012

---

### REQ-005: WebSocket Real-Time Communication

**Priority**: Critical  
**Status**: Approved  
**Dependencies**: REQ-001

**Description**:
Establish reliable WebSocket connections between clients and server for real-time bidirectional communication. This is the foundation for collaborative editing.

**User Story**:
As a system, I need reliable real-time communication so that all users see updates immediately without polling or page refreshes.

**Acceptance Criteria**:
- [ ] WebSocket connection established on session join
- [ ] Handle connection drops and automatic reconnection
- [ ] Message types defined (code_update, user_join, user_leave, etc.)
- [ ] Broadcast messages to all users in a session
- [ ] Connection state visible to users

**Technical Notes**:
- FastAPI WebSocket support
- Client-side WebSocket connection management
- Heartbeat/ping-pong to detect dead connections
- Exponential backoff for reconnection attempts
- Message queue for offline messages (optional)

**Backend Verification** (Tests MUST pass before feature is "Done"):
- [x] Test: `tests/backend/test_websocket.py` - WebSocket endpoint exists at /ws/{session_id} ✅
- [x] Test: `tests/backend/test_websocket.py` - Connection accepted for valid session ✅
- [x] Test: `tests/backend/test_websocket.py` - Connection rejected for invalid session (404) ✅
- [x] Test: `tests/backend/test_websocket.py` - Heartbeat/ping-pong keeps connection alive ✅
- [x] Test: `tests/backend/test_websocket.py` - Graceful disconnect cleanup ✅

**Frontend Verification** (Tests MUST pass before feature is "Done"):
- [ ] Test: `frontend/src/__tests__/useWebSocket.test.js` - WebSocket connects on mount
- [ ] Test: `frontend/src/__tests__/useWebSocket.test.js` - Auto-reconnect on connection drop
- [ ] Test: `frontend/src/__tests__/useWebSocket.test.js` - Exponential backoff for reconnection
- [ ] Test: `frontend/src/__tests__/useWebSocket.test.js` - Connection state updated correctly
- [ ] Test: `frontend/src/__tests__/ConnectionStatus.test.jsx` - Connection status indicator shows current state

**Integration Verification**:
- [ ] Test: WebSocket connection persists through network interruption and reconnects

**Test Scenarios**:
1. Establish WebSocket connection successfully
2. Send and receive messages
3. Handle network disconnection and reconnection
4. Verify message delivery to all session participants

---

## Non-Functional Requirements

### Performance
- WebSocket message latency: < 200ms for typical networks
- Page load time: < 3 seconds
- Pyodide initialization: < 2 seconds after first use
- Support at least 10 concurrent sessions
- Support 2-5 users per session

### Security
- Session IDs must be cryptographically random (UUID v4)
- No server-side code execution (mitigates code injection risks)
- Input sanitization for session IDs
- CORS configuration for API endpoints
- Rate limiting on session creation (future)

### Usability
- Clean, intuitive interface
- Clear visual feedback for connection status
- Error messages are user-friendly
- Responsive design (works on desktop, laptop)
- Keyboard shortcuts for common actions

### Accessibility
- Keyboard navigation support
- Screen reader compatible (WCAG 2.1 Level AA goal)
- High contrast mode support
- Focus indicators visible

---

## Out of Scope

*Document what this project explicitly will NOT include in v1*

- Video/audio communication (use external tools like Zoom)
- User authentication and accounts
- Session persistence beyond active connections (sessions are ephemeral)
- Code execution for languages other than Python
- File upload/download (copy-paste only)
- Code history/version control
- Chat functionality (focus on code collaboration)
- Whiteboard or drawing features
- Admin dashboard or analytics
- Payment/subscription system

---

## Requirements Summary

| ID | Title | Priority | Status | Dependencies |
|----|-------|----------|--------|--------------|
| REQ-001 | Session Management | Critical | Approved | None |
| REQ-002 | Real-Time Collaborative Code Editing | Critical | Approved | REQ-001 |
| REQ-003 | Python Code Execution (Client-Side) | High | Approved | REQ-001 |
| REQ-004 | Multi-Language Syntax Highlighting Support | Medium | Approved | REQ-002 |
| REQ-005 | WebSocket Real-Time Communication | Critical | Approved | REQ-001 |

---
*Last Updated: 2025-12-09*
*Version: 0.2*
