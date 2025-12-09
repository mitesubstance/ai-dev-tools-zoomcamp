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

### ADR-003: [Next Decision]

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

---
*Last Updated: 2025-12-09*
