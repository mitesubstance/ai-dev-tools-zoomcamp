/**
 * Pyodide Service Wrapper
 * REQ-003: Python Code Execution (Client-Side)
 * 
 * Handles loading and executing Python code using Pyodide (WebAssembly)
 * All code execution happens in the browser, not on the server.
 */

import { loadPyodide as loadPyodideLib } from 'pyodide';

export class PyodideRunner {
  constructor() {
    this.pyodide = null;
    this.loading = false;
  }

  /**
   * Check if Pyodide is loaded
   * @returns {boolean}
   */
  isLoaded() {
    return this.pyodide !== null;
  }

  /**
   * Load Pyodide library (lazy loading)
   * This is idempotent - calling multiple times won't reload
   * @returns {Promise<void>}
   */
  async loadPyodide() {
    // If already loaded, return immediately
    if (this.pyodide) {
      return;
    }

    // If currently loading, wait for it
    if (this.loading) {
      while (this.loading) {
        await new Promise((resolve) => setTimeout(resolve, 100));
      }
      return;
    }

    try {
      this.loading = true;
      console.log('Loading Pyodide...');
      
      // Load Pyodide from the npm package (already installed locally)
      this.pyodide = await loadPyodideLib();
      
      console.log('Pyodide loaded successfully');
    } catch (error) {
      console.error('Failed to load Pyodide:', error);
      throw new Error('Failed to load Python runtime');
    } finally {
      this.loading = false;
    }
  }

  /**
   * Execute Python code and capture output
   * @param {string} code - Python code to execute
   * @param {object} options - Execution options
   * @param {number} options.timeout - Timeout in milliseconds (default: 10000)
   * @returns {Promise<{success: boolean, output: string, error: string|null}>}
   */
  async runCode(code, options = {}) {
    if (!this.pyodide) {
      throw new Error('Pyodide not loaded. Call loadPyodide() first.');
    }

    const timeout = options.timeout || 10000; // Default 10 second timeout
    let output = '';
    let error = null;
    let success = true;

    try {
      // Set up stdout/stderr capture
      this.pyodide.setStdout({
        batched: (text) => {
          output += text + '\n';
        },
      });

      this.pyodide.setStderr({
        batched: (text) => {
          output += text + '\n';
        },
      });

      // Execute with timeout
      const result = await Promise.race([
        this.executeCode(code),
        this.createTimeout(timeout),
      ]);

      if (result === 'TIMEOUT') {
        success = false;
        error = `Execution timeout: Code took longer than ${timeout}ms to execute. Possible infinite loop.`;
      }
    } catch (err) {
      success = false;
      error = this.formatError(err);
    }

    // Clean up output (remove trailing newline)
    output = output.trim();

    return {
      success,
      output,
      error,
    };
  }

  /**
   * Execute Python code
   * @private
   */
  async executeCode(code) {
    await this.pyodide.runPythonAsync(code);
    return 'SUCCESS';
  }

  /**
   * Create a timeout promise
   * @private
   */
  createTimeout(ms) {
    return new Promise((resolve) => {
      setTimeout(() => resolve('TIMEOUT'), ms);
    });
  }

  /**
   * Format error message from Pyodide
   * @private
   */
  formatError(err) {
    // Pyodide errors come with stack traces
    // Extract the relevant error message
    const errorString = err.toString();
    
    // Try to extract just the Python error
    const lines = errorString.split('\n');
    const relevantLines = [];
    
    for (const line of lines) {
      // Skip internal Pyodide frames
      if (line.includes('pyodide') && line.includes('.js')) {
        continue;
      }
      relevantLines.push(line);
    }

    return relevantLines.join('\n').trim() || errorString;
  }
}

// Singleton instance for easy use
let globalRunner = null;

/**
 * Get or create the global Pyodide runner instance
 * @returns {PyodideRunner}
 */
export function getPyodideRunner() {
  if (!globalRunner) {
    globalRunner = new PyodideRunner();
  }
  return globalRunner;
}

/**
 * Execute Python code using the global runner
 * Convenience function that automatically loads Pyodide if needed
 * @param {string} code - Python code to execute
 * @param {object} options - Execution options
 * @returns {Promise<{success: boolean, output: string, error: string|null}>}
 */
export async function executePython(code, options = {}) {
  const runner = getPyodideRunner();
  
  if (!runner.isLoaded()) {
    await runner.loadPyodide();
  }
  
  return runner.runCode(code, options);
}
