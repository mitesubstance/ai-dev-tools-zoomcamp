/**
 * API service for session management
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Create a new coding session
 * @param {string} language - Programming language (default: 'python')
 * @returns {Promise<Object>} Session data
 */
export async function createSession(language = 'python') {
  const response = await fetch(`${API_URL}/api/sessions`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ language }),
  });

  if (!response.ok) {
    throw new Error('Failed to create session');
  }

  return response.json();
}

/**
 * Get session information
 * @param {string} sessionId - Session ID
 * @returns {Promise<Object>} Session data
 */
export async function getSession(sessionId) {
  const response = await fetch(`${API_URL}/api/sessions/${sessionId}`);

  if (!response.ok) {
    throw new Error('Session not found');
  }

  return response.json();
}
