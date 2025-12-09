# Architecture Decision Records (ADRs)

## Overview
This document tracks significant architectural decisions made during the project. Each decision is recorded with context, rationale, and consequences.

---

## ADR Template

```markdown
## ADR-XXX: [Title]

**Date**: YYYY-MM-DD
**Status**: [Proposed | Accepted | Deprecated | Superseded]
**Context**: What is the issue we're seeing that is motivating this decision?
**Decision**: What is the change we're proposing and/or doing?
**Consequences**: What becomes easier or harder as a result of this change?
```

---

## Active Decisions

### ADR-001: Adopt Vendor-Agnostic File-Based Context System

**Date**: 2025-12-09  
**Status**: Accepted  
**Context**: We need a way for any AI agent (current or future) to understand the project state, rules, and architecture immediately without relying on conversation history or external databases.

**Decision**: Implement a file-based context system with:
- `AGENTS.md` for agent operating instructions
- `ARCHITECTURE.md` for system design
- `DECISIONS.md` for this ADR log
- `PRODUCT_SPECS.md` for functional requirements
- `IMPLEMENTATION_PLAN.md` for roadmap tracking
- `SESSION_LOG.md` for short-term scratchpad

**Consequences**:
- ✅ Any AI agent can immediately understand project context
- ✅ Documentation is version-controlled alongside code
- ✅ Clear separation of concerns across documentation files
- ⚠️ Requires discipline to keep documentation updated
- ⚠️ Initial overhead in creating and maintaining structure

---

### ADR-002: SESSION_LOG.md Should Not Be Version Controlled

**Date**: 2025-12-09  
**Status**: Accepted  
**Context**: SESSION_LOG.md is a scratchpad for immediate work, debugging, and temporary notes. This file is agent-specific and session-specific, containing ephemeral information that doesn't need to be shared across the team or preserved in git history.

**Decision**: Add SESSION_LOG.md to .gitignore along with other AI-specific local files (.cursor/scratchpad.md, .windsurfrules). This file should remain local to each developer/agent's workspace.

**Consequences**:
- ✅ Prevents clutter in git history with temporary debugging notes
- ✅ Each agent/developer maintains their own scratchpad independently
- ✅ No merge conflicts from concurrent session logs
- ⚠️ Session context is not shared between agents/developers (must rely on formal documentation in other files)
- ⚠️ Important decisions logged in SESSION_LOG.md must be migrated to DECISIONS.md before being cleared

---

### ADR-003: Use FastAPI for Backend Framework

**Date**: 2025-12-09  
**Status**: Accepted  
**Context**: We need a Python backend framework that supports WebSockets for real-time collaboration, provides async capabilities for handling multiple concurrent connections, and has a good developer experience with minimal boilerplate.

**Decision**: Adopt FastAPI as the backend framework for the following reasons:
- Native WebSocket support with async/await patterns
- Excellent performance (built on Starlette/Uvicorn)
- Automatic API documentation (OpenAPI/Swagger)
- Type hints and Pydantic validation
- Minimal boilerplate for rapid development
- Large community and active development

**Consequences**:
- ✅ Modern async Python with excellent WebSocket support
- ✅ Fast development with automatic API docs
- ✅ Type safety with Pydantic models
- ✅ High performance for concurrent connections
- ⚠️ Requires Python 3.11+ for best performance
- ⚠️ Team needs familiarity with async/await patterns

---

### ADR-004: Use React + Vite for Frontend

**Date**: 2025-12-09  
**Status**: Accepted  
**Context**: We need a modern frontend framework with fast development experience, good ecosystem support for code editors (CodeMirror 6), and ability to integrate WebAssembly (Pyodide).

**Decision**: Adopt React 18+ with Vite as the build tool:
- React provides component-based architecture and large ecosystem
- Vite offers fast HMR (Hot Module Replacement) and quick builds
- Excellent support for modern JavaScript features
- Easy integration with CodeMirror 6, WebSockets, and Pyodide
- Strong community and extensive documentation

**Consequences**:
- ✅ Fast development experience with instant HMR
- ✅ Large ecosystem of libraries and components
- ✅ Excellent developer tools and debugging
- ✅ Modern build output with tree-shaking
- ⚠️ Requires Node.js 18+ for development
- ⚠️ Bundle size needs monitoring (React + CodeMirror + Pyodide)

---

### ADR-005: Client-Side Code Execution with Pyodide

**Date**: 2025-12-09  
**Status**: Accepted  
**Context**: We need to execute Python code safely without server-side security risks, reduce server load, and provide instant feedback. Traditional server-side execution poses security risks (arbitrary code execution) and scaling challenges.

**Decision**: Execute Python code entirely in the browser using Pyodide (Python compiled to WebAssembly):
- No server-side code execution eliminates major security vulnerability
- Execution happens on user's machine (scales infinitely)
- Instant results without network latency
- Access to standard Python library
- Run in Web Worker to avoid blocking UI

**Consequences**:
- ✅ Eliminates server-side code execution security risks
- ✅ Infinite scalability (execution on client machines)
- ✅ No network latency for code execution
- ✅ Reduced server infrastructure costs
- ⚠️ Initial Pyodide load time (~6-10MB download)
- ⚠️ Limited to Python standard library (no arbitrary pip packages)
- ⚠️ Requires modern browser with WebAssembly support
- ⚠️ Performance depends on user's device

---

### ADR-006: Use CodeMirror 6 for Code Editor

**Date**: 2025-12-09  
**Status**: Accepted  
**Context**: We need a powerful, extensible code editor that supports syntax highlighting for multiple languages, real-time collaborative editing, and provides excellent developer experience.

**Decision**: Adopt CodeMirror 6 as the code editor component:
- Modern architecture built on functional programming principles
- Excellent performance with large documents
- Extensible language system (easy to add Python, JavaScript, etc.)
- Built-in support for collaborative editing patterns
- Active development and strong community
- Better than Monaco Editor for our use case (lighter, more extensible)

**Consequences**:
- ✅ High-performance code editing experience
- ✅ Easy to add syntax highlighting for new languages
- ✅ Excellent extension system for future features
- ✅ Good documentation and examples
- ⚠️ Steeper learning curve than simpler textarea solutions
- ⚠️ Requires understanding of CM6's state management

---

### ADR-007: In-Memory Session Storage for v1

**Date**: 2025-12-09  
**Status**: Accepted  
**Context**: We need to store session state (code, active connections) during development and MVP phase. We need to decide between in-memory storage, Redis, or a database.

**Decision**: Use in-memory Python dictionaries for session storage in v1:
- Simplest implementation for MVP
- No external dependencies (Redis, database)
- Sufficient for development and small-scale testing
- Easy to migrate to Redis/database later
- Sessions are ephemeral (exist only while server runs)

**Consequences**:
- ✅ Zero setup overhead for development
- ✅ Fast access times (in-process memory)
- ✅ Simple implementation and debugging
- ⚠️ Sessions lost on server restart
- ⚠️ Cannot scale horizontally (single server only)
- ⚠️ Memory usage grows with active sessions
- ⚠️ Not suitable for production at scale
- 📝 Migration path: Later move to Redis for distributed sessions

---

### ADR-008: Use concurrently for Development Workflow

**Date**: 2025-12-09  
**Status**: Accepted  
**Context**: We need to run both frontend (Vite) and backend (FastAPI) servers during development. Developers should be able to start both with a single command.

**Decision**: Use `concurrently` npm package to run both servers:
- Single `npm run dev` command starts both services
- Colored output distinguishes frontend/backend logs
- Handles process management and cleanup
- Common pattern in full-stack development
- Platform-independent

**Consequences**:
- ✅ Simple developer experience (one command)
- ✅ Both servers start simultaneously
- ✅ Clear log separation with colors
- ✅ Easy to stop all processes with Ctrl+C
- ⚠️ Requires Node.js even for Python developers
- ⚠️ Both services must be configured properly

---

### ADR-009: Enforce Full-Stack Test-Driven Development (TDD)

**Date**: 2025-12-09  
**Status**: Accepted  
**Context**: We need to ensure code quality, reliability, and maintainability across both frontend and backend. Without strict testing requirements, features may be considered "done" without proper validation, leading to bugs and technical debt. Traditional approaches often test only one layer (backend OR frontend), missing integration issues.

**Decision**: Enforce Full-Stack TDD with the following mandatory requirements:
- **No feature is considered "Complete" unless BOTH backend and frontend tests pass**
- **Test-First Workflow**: Write failing tests before implementation (Red-Green-Refactor)
- **Backend Testing**: Pytest for unit tests covering API endpoints, business logic, and error handling
- **Frontend Testing**: Jest/React Testing Library (or Vitest) for component tests covering rendering, interactions, state management, and edge cases
- **Integration Testing**: Optional but recommended for critical user flows
- **Definition of Done**: Feature checkbox in IMPLEMENTATION_PLAN.md can only be marked `[x]` when:
  1. Backend tests pass
  2. Frontend tests pass
  3. Code is committed with tests
  4. PRODUCT_SPECS.md verification checkboxes are marked complete

**Consequences**:
- ✅ Higher code quality and confidence in changes
- ✅ Catches bugs early in both layers
- ✅ Better documentation through tests (tests as specifications)
- ✅ Easier refactoring with safety net
- ✅ Reduced production bugs
- ⚠️ Initial development may feel slower (but faster long-term)
- ⚠️ Requires discipline to write tests first
- ⚠️ Learning curve for team members unfamiliar with TDD
- ⚠️ Test maintenance overhead

---

### ADR-010: Use Vitest for Frontend Testing

**Date**: 2025-12-09  
**Status**: Accepted  
**Context**: We need a frontend testing framework that integrates well with Vite, supports React component testing, and provides a modern testing experience. The main options are Jest (traditional choice) and Vitest (Vite-native).

**Decision**: Adopt Vitest as the frontend testing framework:
- **Native Vite Integration**: Same configuration, transformers, and plugins as build process
- **Fast Execution**: Uses Vite's transformation pipeline, instant test reruns with HMR-like experience
- **Jest-Compatible API**: Minimal migration effort if moving from Jest, familiar syntax
- **ESM Support**: First-class support for ES modules (no complex configuration)
- **React Testing Library Integration**: Works seamlessly with @testing-library/react
- **TypeScript Support**: Out-of-the-box TypeScript support
- **Active Development**: Maintained by Vite team, future-proof choice

**Consequences**:
- ✅ Consistent tooling with Vite (same config, transformers)
- ✅ Fast test execution and watch mode
- ✅ No complex Jest configuration for ESM/Vite features
- ✅ Modern testing experience aligned with project stack
- ✅ Growing community and ecosystem
- ⚠️ Slightly smaller ecosystem compared to Jest (but growing)
- ⚠️ Team needs to learn Vitest-specific features (though API is Jest-compatible)

---

### ADR-011: Migrate from pip to uv for Python Package Management

**Date**: 2025-12-09  
**Status**: Accepted  
**Context**: We need a faster, more reliable Python package manager for development. Traditional pip is slow for dependency resolution and lacks modern features like lockfiles and virtual environment management. The team requested migration to uv, a next-generation Python package manager written in Rust.

**Decision**: Adopt uv for all Python package management:
- **Replace pip/requirements.txt** with uv/pyproject.toml
- **Use pyproject.toml** for dependency declarations (PEP 621 standard)
- **Automatic virtual environment** management with `.venv/`
- **Lockfile generation** via `uv.lock` (deterministic installs)
- **All commands prefixed** with `uv run` for isolated execution

**Key Benefits**:
- **10-100x faster** than pip for installs and resolves
- **Built-in virtual environment** management
- **Lockfile support** for reproducible builds
- **Modern Python packaging** (follows PEP 621 pyproject.toml standard)
- **Drop-in pip replacement** with familiar commands
- **Better dependency resolution** algorithm

**Migration Steps Completed**:
1. Created `pyproject.toml` with dependencies
2. Ran `uv sync` to create `.venv/` and install packages
3. Updated `.gitignore` to exclude `.venv/`
4. Removed old `requirements.txt`
5. Updated README.md with uv commands
6. All tests passing with `uv run pytest`

**Consequences**:
- ✅ Significantly faster dependency installation (< 1 second typical)
- ✅ Automatic virtual environment management
- ✅ Deterministic builds with lockfiles
- ✅ Modern tooling aligned with Python packaging standards
- ✅ Better developer experience
- ⚠️ Requires uv to be installed globally (`pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- ⚠️ Team must learn uv commands (though similar to pip)
- ⚠️ CI/CD pipelines need updating to use uv

**Command Comparisons**:
| pip | uv |
|-----|-----|
| `pip install -r requirements.txt` | `uv sync` |
| `pip install package` | `uv add package` |
| `pip install --upgrade package` | `uv add package --upgrade` |
| `python script.py` | `uv run python script.py` |
| `pytest` | `uv run pytest` |

---

### ADR-012: [Next Decision]

**Date**: [TBD]  
**Status**: [TBD]  
**Context**: [TBD]  
**Decision**: [TBD]  
**Consequences**: [TBD]

---

## Superseded Decisions

*None yet*

---

## Decision Log Summary

| ADR | Title | Date | Status |
|-----|-------|------|--------|
| 001 | Vendor-Agnostic File-Based Context System | 2025-12-09 | Accepted |
| 002 | SESSION_LOG.md Should Not Be Version Controlled | 2025-12-09 | Accepted |
| 003 | Use FastAPI for Backend Framework | 2025-12-09 | Accepted |
| 004 | Use React + Vite for Frontend | 2025-12-09 | Accepted |
| 005 | Client-Side Code Execution with Pyodide | 2025-12-09 | Accepted |
| 006 | Use CodeMirror 6 for Code Editor | 2025-12-09 | Accepted |
| 007 | In-Memory Session Storage for v1 | 2025-12-09 | Accepted |
| 008 | Use concurrently for Development Workflow | 2025-12-09 | Accepted |
| 009 | Enforce Full-Stack Test-Driven Development (TDD) | 2025-12-09 | Accepted |
| 010 | Use Vitest for Frontend Testing | 2025-12-09 | Accepted |
| 011 | Migrate from pip to uv for Python Package Management | 2025-12-09 | Accepted |

---
*Last Updated: 2025-12-09*
