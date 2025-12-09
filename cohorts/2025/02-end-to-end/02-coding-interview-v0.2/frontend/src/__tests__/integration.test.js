/**
 * Integration tests for client-server interaction
 * These tests verify end-to-end communication between frontend and backend
 * 
 * NOTE: These tests require a running backend server at http://localhost:8000
 * Run with: npm run dev (in backend directory) before running these tests
 * 
 * @vitest-environment node
 */
import { describe, it, expect, beforeAll } from 'vitest';

const API_URL = 'http://localhost:8000';
const WS_URL = 'ws://localhost:8000';

// Helper to check if backend is running
async function isBackendRunning() {
  try {
    const response = await fetch(`${API_URL}/api/health`, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });
    return response.ok;
  } catch {
    return false;
  }
}

describe('Integration Tests - Client-Server Communication', () => {
  let backendAvailable = false;

  beforeAll(async () => {
    backendAvailable = await isBackendRunning();
    if (!backendAvailable) {
      console.warn('\n⚠️  Backend server not running at http://localhost:8000');
      console.warn('   Integration tests will be skipped.');
      console.warn('   Start backend with: cd backend && uvicorn main:app --reload\n');
    } else {
      console.log('✅ Backend is running - integration tests will execute');
    }
  });

  describe('HTTP API Integration', () => {
    it('should connect to health check endpoint', async function() {
      if (!backendAvailable) this.skip();
      
      const response = await fetch(`${API_URL}/api/health`);
      const data = await response.json();

      expect(response.status).toBe(200);
      expect(data.status).toBe('ok');
      expect(data).toHaveProperty('timestamp');
    });

    it('should create a new session', async function() {
      if (!backendAvailable) this.skip();
      
      const response = await fetch(`${API_URL}/api/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language: 'python' }),
      });

      const data = await response.json();

      expect(response.status).toBe(201);
      expect(data).toHaveProperty('session_id');
      expect(data.session_id).toMatch(/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/);
      expect(data.language).toBe('python');
    });

    it('should retrieve session information', async function() {
      if (!backendAvailable) this.skip();
      
      // First create a session
      const createResponse = await fetch(`${API_URL}/api/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language: 'python' }),
      });
      const { session_id } = await createResponse.json();

      // Then retrieve it
      const getResponse = await fetch(`${API_URL}/api/sessions/${session_id}`);
      const data = await getResponse.json();

      expect(getResponse.status).toBe(200);
      expect(data.session_id).toBe(session_id);
      expect(data.language).toBe('python');
      expect(data).toHaveProperty('active_users');
    });

    it('should return 404 for non-existent session', async function() {
      if (!backendAvailable) this.skip();
      
      const fakeSessionId = '00000000-0000-0000-0000-000000000000';
      const response = await fetch(`${API_URL}/api/sessions/${fakeSessionId}`);

      expect(response.status).toBe(404);
    });
  });

  describe('WebSocket Integration', () => {
    it('should establish WebSocket connection to valid session', async function() {
      if (!backendAvailable) this.skip();
      
      // Create a session first
      const createResponse = await fetch(`${API_URL}/api/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language: 'python' }),
      });
      const { session_id } = await createResponse.json();

      // Connect via WebSocket
      return new Promise((resolve, reject) => {
        const ws = new WebSocket(`${WS_URL}/ws/${session_id}`);
        const timeout = setTimeout(() => {
          ws.close();
          reject(new Error('WebSocket connection timeout'));
        }, 5000);

        ws.onopen = () => {
          clearTimeout(timeout);
          expect(ws.readyState).toBe(WebSocket.OPEN);
          ws.close();
        };

        ws.onmessage = (event) => {
          const message = JSON.parse(event.data);
          // Should receive session_state on connect
          if (message.type === 'session_state') {
            expect(message.data).toHaveProperty('code');
            expect(message.data).toHaveProperty('language');
            expect(message.data).toHaveProperty('active_users');
            ws.close();
            resolve();
          }
        };

        ws.onerror = (error) => {
          clearTimeout(timeout);
          reject(error);
        };
      });
    }, 10000);

    it('should broadcast messages to multiple clients', async function() {
      if (!backendAvailable) this.skip();
      
      // Create a session
      const createResponse = await fetch(`${API_URL}/api/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language: 'python' }),
      });
      const { session_id } = await createResponse.json();

      return new Promise((resolve, reject) => {
        const ws1 = new WebSocket(`${WS_URL}/ws/${session_id}`);
        const ws2 = new WebSocket(`${WS_URL}/ws/${session_id}`);
        
        let ws1Connected = false;
        let ws2Connected = false;
        let ws2ReceivedUpdate = false;

        const timeout = setTimeout(() => {
          ws1.close();
          ws2.close();
          reject(new Error('Test timeout'));
        }, 10000);

        ws1.onopen = () => {
          ws1Connected = true;
        };

        ws2.onopen = () => {
          ws2Connected = true;
        };

        ws2.onmessage = (event) => {
          const message = JSON.parse(event.data);
          
          // Wait for code_update from ws1
          if (message.type === 'code_update' && message.data.code === 'print("test")') {
            ws2ReceivedUpdate = true;
            clearTimeout(timeout);
            
            expect(ws2ReceivedUpdate).toBe(true);
            
            ws1.close();
            ws2.close();
            resolve();
          }
        };

        // Wait a bit for both to connect, then send from ws1
        setTimeout(() => {
          if (ws1Connected && ws2Connected) {
            ws1.send(JSON.stringify({
              type: 'code_update',
              data: {
                code: 'print("test")',
                timestamp: Date.now(),
              },
            }));
          }
        }, 1000);

        ws1.onerror = ws2.onerror = (error) => {
          clearTimeout(timeout);
          reject(error);
        };
      });
    }, 15000);

    it('should track user count correctly', async function() {
      if (!backendAvailable) this.skip();
      
      // Create a session
      const createResponse = await fetch(`${API_URL}/api/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language: 'python' }),
      });
      const { session_id } = await createResponse.json();

      return new Promise((resolve, reject) => {
        const ws1 = new WebSocket(`${WS_URL}/ws/${session_id}`);

        const timeout = setTimeout(() => {
          ws1.close();
          reject(new Error('Test timeout'));
        }, 10000);

        ws1.onmessage = (event) => {
          const message = JSON.parse(event.data);
          
          if (message.type === 'session_state') {
            // First connection
            expect(message.data.active_users).toBeGreaterThanOrEqual(1);
          }
          
          if (message.type === 'user_joined') {
            expect(message.data.user_count).toBeGreaterThan(1);
            
            clearTimeout(timeout);
            ws1.close();
            ws2.close();
            resolve();
          }
        };

        // Connect second client after a delay
        let ws2;
        setTimeout(() => {
          ws2 = new WebSocket(`${WS_URL}/ws/${session_id}`);
        }, 1000);

        ws1.onerror = (error) => {
          clearTimeout(timeout);
          reject(error);
        };
      });
    }, 15000);
  });

  describe('Full User Flow Integration', () => {
    it('should complete full collaborative session flow', async function() {
      if (!backendAvailable) this.skip();
      
      // 1. Create session
      const createResponse = await fetch(`${API_URL}/api/sessions`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ language: 'python' }),
      });
      expect(createResponse.status).toBe(201);
      const { session_id } = await createResponse.json();

      // 2. Verify session exists
      const getResponse = await fetch(`${API_URL}/api/sessions/${session_id}`);
      expect(getResponse.status).toBe(200);

      // 3. Connect via WebSocket and send/receive code
      return new Promise((resolve, reject) => {
        const ws = new WebSocket(`${WS_URL}/ws/${session_id}`);
        let receivedState = false;

        const timeout = setTimeout(() => {
          ws.close();
          reject(new Error('Test timeout'));
        }, 10000);

        ws.onmessage = (event) => {
          const message = JSON.parse(event.data);
          
          if (message.type === 'session_state') {
            receivedState = true;
            expect(message.data).toHaveProperty('code');
            expect(message.data).toHaveProperty('language', 'python');
            
            // Send a code update
            ws.send(JSON.stringify({
              type: 'code_update',
              data: {
                code: 'print("integration test")',
                timestamp: Date.now(),
              },
            }));
          }
          
          if (message.type === 'code_update' && receivedState) {
            // Successfully completed the flow
            clearTimeout(timeout);
            expect(message.data.code).toBe('print("integration test")');
            ws.close();
            resolve();
          }
        };

        ws.onerror = (error) => {
          clearTimeout(timeout);
          reject(error);
        };
      });
    }, 15000);
  });
});
