# AI Agent Operating Instructions

## 1. Identity & Purpose
You are an expert AI Coding Agent acting as a Senior Software Engineer. You value clean code, test-driven development (TDD), and architectural consistency.

## 2. The "Context-First" Workflow
Before writing code, you must:
1.  **Read `IMPLEMENTATION_PLAN.md`**: Understand the current phase.
2.  **Read `PRODUCT_SPECS.md`**: Understand the specific requirements for the current task.
3.  **Read `DECISIONS.md`**: Ensure your solution does not violate past architectural decisions.
4.  **Update `SESSION_LOG.md`**: Write down your plan for this specific session.
    - **NOTE**: `SESSION_LOG.md` is ephemeral working memory and is **NOT version controlled** (excluded in `.gitignore`)
    - It prevents commit noise and merge conflicts between different environments
    - Archive important session notes to `docs/archive/` if needed for future reference

## 3. Coding Standards

### Backend (Python)
- **Language**: Python 3.11+
- **Style**: Black (line length: 88), Ruff for linting
- **Type Hints**: Mandatory for all function signatures
- **Testing**: Pytest with pytest-asyncio for async tests
- **Comments**: Explain *why*, not *what*
- **Imports**: Use absolute imports, group by standard library → third-party → local

### Frontend (JavaScript/TypeScript)
- **Language**: JavaScript (ES6+) / TypeScript preferred
- **Style**: ESLint + Prettier (semi: true, singleQuote: true)
- **Testing**: Vitest for unit tests, Playwright for E2E
- **Components**: Functional components with hooks
- **Comments**: JSDoc for public APIs

### General
- **Git Commits**: Conventional Commits format (feat:, fix:, docs:, test:, refactor:)
- **Branch Names**: `feature/REQ-XXX-description`, `fix/issue-description`
- **PR Reviews**: All code must pass CI/CD checks before merge

## 4. Documentation Rules
- **ADRs**: If you make a significant architectural choice, propose an entry for `DECISIONS.md` with:
  - ADR number
  - Date
  - Status (Proposed, Accepted, Deprecated)
  - Context
  - Decision
  - Consequences
- **Roadmap**: When a task is complete, mark the checkbox `[x]` in `IMPLEMENTATION_PLAN.md`
- **Scratchpad**: Use `SESSION_LOG.md` to store error logs, brainstorming, or temporary steps. Clear it or archive it when the session goal is achieved.
- **API Changes**: Update `specs/openapi.yaml` when adding/modifying endpoints

## 5. Constraints
- **NO** placeholder code (e.g., `pass` or `// TODO`) in final commits
- **NO** breaking changes to the `ARCHITECTURE.md` design without explicit approval
- **ALWAYS** reference the specific Requirement ID from `PRODUCT_SPECS.md` in commit messages
- **NO** hardcoded secrets or API keys (use environment variables)
- **NO** console.log or print statements in production code (use proper logging)

## 6. Testing Requirements
- **Unit Tests**: Minimum 80% code coverage
- **Integration Tests**: Test all API endpoints
- **E2E Tests**: Test critical user flows (create session, collaborate, execute code)
- **Test Naming**: `test_<function>_<scenario>_<expected_result>`
- **Fixtures**: Use fixtures for common test data
- **Mocking**: Mock external dependencies (Pyodide, WebSocket connections)

## 7. Technology Stack Reference

### Core Technologies (See DECISIONS.md for rationale)
- **Frontend Framework**: React 18+ with Vite 5+
- **Backend Framework**: FastAPI 0.109+
- **Code Editor**: CodeMirror 6 with @codemirror/collab
- **Python WASM**: Pyodide 0.25+
- **Real-time**: Native WebSockets (FastAPI + Browser WebSocket API)
- **Data Layer**: Repository Pattern (in-memory → SQLAlchemy migration path)
- **Deployment**: Render (Docker container)

### Key Dependencies
**Backend:**
```
fastapi[all]>=0.109.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
httpx>=0.26.0
```

**Frontend:**
```json
{
  "@codemirror/state": "^6.4.0",
  "@codemirror/view": "^6.24.0",
  "@codemirror/lang-javascript": "^6.2.1",
  "@codemirror/lang-python": "^6.1.4",
  "@codemirror/collab": "^6.1.0",
  "pyodide": "^0.25.0",
  "react": "^18.2.0",
  "vite": "^5.0.0"
}
```

## 8. Development Workflow

### Starting a New Feature
1. Read `IMPLEMENTATION_PLAN.md` to identify current phase
2. Read relevant requirements from `PRODUCT_SPECS.md`
3. Update `SESSION_LOG.md` with your plan
4. Create feature branch: `git checkout -b feature/REQ-XXX-description`
5. Write tests first (TDD)
6. Implement feature
7. Run tests: `npm test` and `pytest`
8. Update documentation if needed
9. Mark task complete in `IMPLEMENTATION_PLAN.md`
10. **Ask user for approval before committing**
11. After approval, commit with reference: `git commit -m "feat: implement REQ-XXX description"`

### Debugging
1. Document error in `SESSION_LOG.md`
2. Check relevant logs (browser console, FastAPI logs)
3. Write failing test to reproduce bug
4. Fix bug
5. Verify test passes
6. Document fix in `SESSION_LOG.md`

### Adding New Dependencies
1. Document rationale in `DECISIONS.md`
2. Add to `package.json` or `requirements.txt`
3. Update `README.md` if it affects setup
4. Commit: `chore: add <package> for <reason>`

## 9. Security Guidelines
- **Code Execution**: All Python code runs in Pyodide (WASM sandbox) in browser only
- **WebSocket**: Validate all incoming messages, implement rate limiting
- **CORS**: Configure appropriately for production domain
- **Environment Variables**: Use `.env` files (never commit `.env`)
- **Input Validation**: Validate all user input with Pydantic models
- **Session IDs**: Use UUIDs, not sequential IDs

## 10. Performance Guidelines
- **Frontend**: Code-split routes, lazy load Pyodide (~15MB)
- **Backend**: Use async/await for all I/O operations
- **WebSocket**: Implement message throttling for high-frequency updates
- **Caching**: Consider Redis for session storage in production
- **Monitoring**: Log WebSocket connection counts, message rates

## 11. AI-Specific Instructions

### When You Encounter Ambiguity
1. Check `PRODUCT_SPECS.md` for requirements
2. Check `DECISIONS.md` for architectural guidance
3. If still unclear, ask the user before implementing

### When You Encounter Errors
1. Log error details in `SESSION_LOG.md`
2. Attempt to fix based on error message
3. If error persists after 2 attempts, ask the user for guidance

### When Proposing Architecture Changes
1. Document in `SESSION_LOG.md` first
2. Explain why current approach is insufficient
3. Propose alternative with pros/cons
4. Wait for user approval before implementing

## 12. File Modification Rules
- **Never delete** `AGENTS.md`, `ARCHITECTURE.md`, `DECISIONS.md`, `PRODUCT_SPECS.md`, or `IMPLEMENTATION_PLAN.md` without explicit approval
- **Always update** `IMPLEMENTATION_PLAN.md` checkboxes when completing tasks
- **Archive** `SESSION_LOG.md` entries when session goals are complete (move to a dated section at bottom)
- **Version** `specs/openapi.yaml` when making breaking API changes

## 13. Quick Reference Commands

```bash
# Setup
npm install && pip install -r requirements.txt

# Development
npm run dev              # Run both client and server
npm run dev:client       # Frontend only
npm run dev:server       # Backend only

# Testing
npm test                 # Frontend tests
pytest                   # Backend tests
npm run test:integration # Integration tests
npm run test:e2e         # End-to-end tests

# Linting
npm run lint             # Frontend
black backend/ && ruff backend/  # Backend

# Build
npm run build            # Production build
docker build -t app .    # Container image

# Deployment
git push render main     # Auto-deploy to Render
```

---

**Remember**: This file is your source of truth. When in doubt, refer back to these instructions and the other context files.
