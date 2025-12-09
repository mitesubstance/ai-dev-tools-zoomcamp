/**
 * API service for session management
 * Uses relative paths - Vite proxy handles routing in development
 */

/**
 * Create a new coding session
 * @param {string} language - Programming language (default: 'python')
 * @returns {Promise<Object>} Session data
 */
export async function createSession(language = 'python') {
  const response = await fetch('/api/sessions', {
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
  const response = await fetch(`/api/sessions/${sessionId}`);

  if (!response.ok) {
    throw new Error('Session not found');
  }

  return response.json();
}
