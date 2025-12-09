# Question 2: Integration Tests

## Answer

The terminal command to execute tests is:

```bash
npm test
```

## What This Runs

This command runs the backend integration tests using pytest:
- Executes `cd backend && pytest -v`
- 13 integration tests covering client-server interaction
- Tests health endpoint, root endpoint, CORS, API documentation, and error handling

## Test Results

```
============================================================================== 13 passed in 0.03s ==============================================================================
```

## Test Coverage

### Health Endpoint (3 tests)
- ✅ Returns 200 OK status
- ✅ Returns correct JSON structure (`{"status": "ok"}`)
- ✅ Returns JSON content type

### Root Endpoint (3 tests)
- ✅ Returns 200 OK status
- ✅ Returns API information (name, version, docs, health)
- ✅ Returns JSON content type

### CORS Configuration (2 tests)
- ✅ Allows localhost:5173 origin
- ✅ Allows localhost:3000 origin

### API Documentation (3 tests)
- ✅ OpenAPI JSON schema accessible
- ✅ Swagger UI docs accessible
- ✅ ReDoc docs accessible

### Error Handling (2 tests)
- ✅ Returns 404 for nonexistent routes
- ✅ Returns 405 for wrong HTTP methods

## Alternative Test Commands

```bash
# Run backend tests directly
cd backend && pytest -v

# Run backend tests with coverage
cd backend && pytest --cov=app --cov-report=html

# Run specific test file
cd backend && pytest tests/test_api.py -v

# Run specific test class
cd backend && pytest tests/test_api.py::TestHealthEndpoint -v
```

## Test Files Created

- `backend/conftest.py` - Pytest configuration and fixtures
- `backend/tests/__init__.py` - Test package marker
- `backend/tests/test_api.py` - Integration tests for API endpoints
