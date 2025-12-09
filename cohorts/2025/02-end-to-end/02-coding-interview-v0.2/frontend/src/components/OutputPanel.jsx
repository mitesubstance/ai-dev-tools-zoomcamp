/**
 * OutputPanel Component
 * REQ-003: Python Code Execution (Client-Side)
 * 
 * Displays code execution output and errors
 */
import { useState } from 'react';
import { executePython } from '../services/pyodide';
import './OutputPanel.css';

export function OutputPanel({ code }) {
  const [output, setOutput] = useState('');
  const [error, setError] = useState(null);
  const [isRunning, setIsRunning] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const handleRunCode = async () => {
    if (!code || !code.trim()) {
      setError('No code to execute');
      setOutput('');
      return;
    }

    setIsRunning(true);
    setIsLoading(true);
    setError(null);
    setOutput('');

    try {
      const result = await executePython(code);
      
      if (result.success) {
        setOutput(result.output || '(No output)');
        setError(null);
      } else {
        setError(result.error);
        setOutput('');
      }
    } catch (err) {
      setError(`Execution error: ${err.message}`);
      setOutput('');
    } finally {
      setIsRunning(false);
      setIsLoading(false);
    }
  };

  const handleClearOutput = () => {
    setOutput('');
    setError(null);
  };

  return (
    <div className="output-panel">
      <div className="output-header">
        <h3>Output</h3>
        <div className="output-actions">
          <button 
            onClick={handleRunCode} 
            disabled={isRunning || isLoading}
            className="run-button"
          >
            {isLoading ? '⏳ Loading Python...' : isRunning ? '⏳ Running...' : '▶️ Run Code'}
          </button>
          <button 
            onClick={handleClearOutput}
            className="clear-button"
            disabled={!output && !error}
          >
            🗑️ Clear
          </button>
        </div>
      </div>

      <div className="output-content">
        {isLoading && (
          <div className="loading-message">
            Loading Python runtime (first time only)...
          </div>
        )}
        
        {error && (
          <div className="output-error">
            <strong>Error:</strong>
            <pre>{error}</pre>
          </div>
        )}
        
        {output && (
          <div className="output-success">
            <pre>{output}</pre>
          </div>
        )}
        
        {!isLoading && !error && !output && (
          <div className="output-empty">
            Click "Run Code" to execute your Python code
          </div>
        )}
      </div>
    </div>
  );
}
