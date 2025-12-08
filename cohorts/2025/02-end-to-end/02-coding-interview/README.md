# Collaborative Coding Interview Platform

A real-time collaborative coding interview platform built with AI assistance for the AI Dev Tools Zoomcamp (Week 2 Homework).

## 🎯 Project Overview

This application allows multiple users to:
- Create and share coding session links
- Edit code collaboratively in real-time
- View live updates across all connected users
- Execute Python code safely in the browser
- Syntax highlighting for JavaScript and Python

## 🛠️ Tech Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Frontend** | React + Vite | Fast HMR, modern build tool |
| **Backend** | FastAPI (Python) | Async-first, auto OpenAPI docs |
| **Code Editor** | CodeMirror 6 | Built-in OT for collaboration |
| **Python Execution** | Pyodide (WASM) | Secure browser-based execution |
| **Real-time** | WebSockets | Native FastAPI + Browser API |
| **Deployment** | Render | Free tier, Docker support |

## 🚀 Quick Start

### Development
```bash
# Install dependencies
npm install
pip install -r requirements.txt

# Run development servers (both client and server)
npm run dev

# Run tests
npm test
```

### Production
```bash
# Build Docker image
docker build -t coding-interview-platform .

# Run container
docker run -p 8000:8000 coding-interview-platform
```

## 📁 Project Structure

```
02-coding-interview/
├── README.md                    # This file
├── AGENTS.md                    # AI agent instructions
├── ARCHITECTURE.md              # System design
├── DECISIONS.md                 # Architecture Decision Records
├── PRODUCT_SPECS.md             # Functional requirements
├── IMPLEMENTATION_PLAN.md       # Development roadmap
├── SESSION_LOG.md               # Scratchpad for current work
├── specs/
│   └── openapi.yaml            # API specification
├── backend/                     # FastAPI backend
├── frontend/                    # React frontend
└── Dockerfile                   # Container configuration
```

## 🤖 AI Context & Documentation

If you are an AI assistant helping with this project, please review the following context files before making changes:

* **[AGENTS.md](./AGENTS.md)**: **READ THIS FIRST.** Your operating instructions and rules.
* **[ARCHITECTURE.md](./ARCHITECTURE.md)**: System design and topology.
* **[DECISIONS.md](./DECISIONS.md)**: ADRs - Do not violate agreed-upon architectural decisions.
* **[PRODUCT_SPECS.md](./PRODUCT_SPECS.md)**: Functional requirements and acceptance criteria.
* **[IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md)**: Global roadmap - Update this when phases are complete.
* **[SESSION_LOG.md](./SESSION_LOG.md)**: Your scratchpad. Use this to track immediate progress and errors.

## 📚 Homework Questions

This project addresses the following homework requirements:

1. **Q1**: Initial Implementation (Frontend + Backend)
2. **Q2**: Integration Tests
3. **Q3**: Concurrent Development (concurrently)
4. **Q4**: Syntax Highlighting (CodeMirror 6)
5. **Q5**: Code Execution (Pyodide WASM)
6. **Q6**: Containerization (Docker)
7. **Q7**: Deployment (Render)

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test

# Integration tests
npm run test:integration
```

## 📦 Deployment

See [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) Phase 8 for deployment instructions.

## 📄 License

MIT License - Created for educational purposes as part of AI Dev Tools Zoomcamp.

## 🙏 Acknowledgments

- [DataTalks.Club](https://datatalks.club/) for the AI Dev Tools Zoomcamp
- Course materials: https://github.com/DataTalksClub/ai-dev-tools-zoomcamp
