# Docker Deployment Guide

## Quick Start

### Prerequisites
- Docker 20.10+ installed
- Docker Compose 1.29+ installed (optional)

### Option 1: Using Docker Compose (Recommended)

```bash
# Build and start the container
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

### Option 2: Using Docker CLI

```bash
# Build the image
docker build -t coding-interview-platform .

# Run the container
docker run -d -p 8000:8000 --name coding-interview-platform coding-interview-platform

# View logs
docker logs -f coding-interview-platform

# Stop the container
docker stop coding-interview-platform
docker rm coding-interview-platform
```

## Access the Application

Once running:
- **Application**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## Architecture

### Multi-Stage Build

The Dockerfile uses a two-stage build process:

**Stage 1: Frontend Builder (Node.js Alpine)**
- Installs npm dependencies
- Builds React application for production
- Optimizes assets for production

**Stage 2: Production (Python 3.11 Slim)**
- Installs uv for Python package management
- Installs backend dependencies
- Copies built frontend from Stage 1
- Serves both frontend and backend on port 8000

### How It Works

1. **Frontend Build**: Vite builds the React app into static files (HTML, JS, CSS)
2. **Backend Serves Frontend**: FastAPI serves the built frontend files at root path `/`
3. **API Endpoints**: Backend also handles API routes (`/api/*`) and WebSocket (`/ws/*`)
4. **Single Port**: Everything runs on port 8000 in production

## File Overview

### Dockerfile
- Multi-stage build configuration
- Builds frontend in first stage
- Copies frontend to backend in second stage
- Installs Python dependencies with uv
- Exposes port 8000
- Includes health check

### .dockerignore
- Excludes unnecessary files from build context
- Reduces build time and image size
- Excludes: node_modules, tests, documentation, IDE configs

### docker-compose.yml
- Simplified container orchestration
- Environment variable configuration
- Port mapping (8000:8000)
- Health check configuration
- Auto-restart policy

### backend/main.py
- Updated to serve frontend static files when `frontend/dist` exists
- Catches all non-API routes and serves index.html (SPA routing)
- Maintains API routes at `/api/*` and WebSocket at `/ws/*`

## Testing the Build

### Verify Build Success

```bash
# Check if image was created
docker images | grep coding-interview-platform

# Should show something like:
# coding-interview-platform   latest   abc123def456   2 minutes ago   XXX MB
```

### Test the Application

```bash
# Start the container
docker-compose up -d

# Wait a few seconds for startup
sleep 5

# Test health endpoint
curl http://localhost:8000/api/health

# Expected output:
# {"status":"ok","timestamp":"2025-12-09T...","service":"coding-interview-backend"}

# Test frontend (should return HTML)
curl http://localhost:8000

# Should return HTML starting with <!DOCTYPE html>
```

### Debugging

```bash
# View container logs
docker-compose logs -f

# Execute commands inside running container
docker exec -it coding-interview-platform bash

# Check if frontend files exist
docker exec -it coding-interview-platform ls -la /app/frontend/dist

# Check Python dependencies
docker exec -it coding-interview-platform uv pip list
```

## Production Considerations

### Environment Variables

You can customize the deployment with environment variables:

```yaml
# docker-compose.yml
environment:
  - BACKEND_PORT=8000
  - PYTHONUNBUFFERED=1
  # Add more as needed
```

### Resource Limits

For production, consider adding resource limits:

```yaml
# docker-compose.yml
services:
  app:
    # ... other config ...
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

### Volumes (Optional)

If you need persistent storage for sessions (future enhancement):

```yaml
# docker-compose.yml
services:
  app:
    # ... other config ...
    volumes:
      - session-data:/app/data

volumes:
  session-data:
```

## Troubleshooting

### Build Fails

**Problem**: Frontend build fails in Stage 1
```
Solution: Check if package.json and package-lock.json are present
Verify: npm install works locally in frontend/
```

**Problem**: Backend dependencies fail to install
```
Solution: Check pyproject.toml and uv.lock are present
Verify: uv sync works locally in backend/
```

### Container Won't Start

**Problem**: Port 8000 already in use
```bash
# Find and kill process using port 8000
lsof -ti:8000 | xargs kill -9
```

**Problem**: Health check failing
```bash
# Check container logs
docker-compose logs

# Verify backend is running
docker exec -it coding-interview-platform ps aux | grep uvicorn
```

### Frontend Not Loading

**Problem**: Frontend returns 404 or API response
```bash
# Check if frontend files exist
docker exec -it coding-interview-platform ls -la /app/frontend/dist

# Should show: index.html, assets/, etc.
```

**Problem**: Assets not loading (JS/CSS)
```bash
# Verify assets directory is mounted correctly
docker exec -it coding-interview-platform ls -la /app/frontend/dist/assets
```

## Security Notes

### For Production Deployment

1. **Use HTTPS**: Add reverse proxy (nginx/traefik) with SSL certificates
2. **Remove CORS wildcard**: Update CORS settings in main.py
3. **Add rate limiting**: Implement rate limiting for session creation
4. **Enable authentication**: Add user authentication for sessions
5. **Scan images**: Use `docker scan coding-interview-platform`
6. **Update regularly**: Keep base images and dependencies updated

### Environment Hardening

```bash
# Run container as non-root user (add to Dockerfile)
RUN useradd -m -u 1000 appuser
USER appuser

# Use read-only filesystem where possible
docker run --read-only -p 8000:8000 coding-interview-platform
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Build and Push Docker Image

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build Docker image
        run: docker build -t coding-interview-platform .
      
      - name: Test image
        run: |
          docker run -d -p 8000:8000 --name test-container coding-interview-platform
          sleep 10
          curl -f http://localhost:8000/api/health || exit 1
          docker stop test-container
```

## Next Steps

1. ✅ Build and test locally
2. ✅ Verify all endpoints work
3. ✅ Check frontend loads correctly
4. ⚠️ Add production-grade security (HTTPS, auth)
5. ⚠️ Set up monitoring and logging
6. ⚠️ Deploy to cloud platform (AWS, GCP, Azure)

---

**Created**: 2025-12-09  
**Version**: 1.0
