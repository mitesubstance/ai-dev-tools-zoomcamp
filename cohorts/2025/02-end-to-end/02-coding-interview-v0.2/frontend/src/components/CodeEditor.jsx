/**
 * CodeEditor component with CodeMirror 6
 * Supports real-time collaborative editing and multi-language syntax highlighting
 */
import { useEffect, useRef } from 'react';
import { EditorView } from '@codemirror/view';
import { EditorState } from '@codemirror/state';
import { syntaxHighlighting, defaultHighlightStyle } from '@codemirror/language';
import { python } from '@codemirror/lang-python';
import { javascript } from '@codemirror/lang-javascript';
import { oneDark } from '@codemirror/theme-one-dark';

/**
 * Get language extension based on language name
 * @param {string} language - Language name ('python' or 'javascript')
 * @returns {Extension} CodeMirror language extension
 */
function getLanguageExtension(language) {
  switch (language) {
    case 'javascript':
      return javascript();
    case 'python':
    default:
      return python();
  }
}

/**
 * Get default placeholder text based on language
 * @param {string} language - Language name
 * @returns {string} Placeholder text
 */
function getDefaultPlaceholder(language) {
  switch (language) {
    case 'javascript':
      return '// Write your JavaScript code here\n';
    case 'python':
    default:
      return '# Write your Python code here\n';
  }
}

/**
 * CodeEditor component
 * @param {Object} props
 * @param {string} props.code - Initial code content
 * @param {Function} props.onChange - Callback when code changes
 * @param {boolean} props.readOnly - Whether editor is read-only
 * @param {string} props.language - Programming language ('python' or 'javascript', defaults to 'python')
 */
export function CodeEditor({ code, onChange, readOnly = false, language = 'python' }) {
  const editorRef = useRef(null);
  const viewRef = useRef(null);
  const isRemoteChange = useRef(false);

  // Initialize CodeMirror
  useEffect(() => {
    if (!editorRef.current) return;

    const startState = EditorState.create({
      doc: code || getDefaultPlaceholder(language),
      extensions: [
        getLanguageExtension(language), // Language parser
        syntaxHighlighting(defaultHighlightStyle), // Apply highlighting styles
        oneDark, // Dark theme
        EditorView.editable.of(!readOnly),
        EditorView.updateListener.of((update) => {
          if (update.docChanged && !isRemoteChange.current) {
            const newCode = update.state.doc.toString();
            if (onChange) {
              onChange(newCode);
            }
          }
        }),
        EditorView.lineWrapping,
      ],
    });

    const view = new EditorView({
      state: startState,
      parent: editorRef.current,
    });

    viewRef.current = view;

    return () => {
      view.destroy();
    };
  }, [readOnly, language]); // Recreate on readOnly or language change

  // Update editor when code changes externally
  useEffect(() => {
    if (!viewRef.current || !code) return;

    const currentCode = viewRef.current.state.doc.toString();
    if (currentCode !== code) {
      isRemoteChange.current = true;
      
      viewRef.current.dispatch({
        changes: {
          from: 0,
          to: currentCode.length,
          insert: code,
        },
      });
      
      // Reset flag after a short delay
      setTimeout(() => {
        isRemoteChange.current = false;
      }, 50);
    }
  }, [code]);

  return (
    <div 
      ref={editorRef} 
      style={{ 
        height: '100%', 
        fontSize: '14px',
        overflow: 'auto'
      }} 
    />
  );
}
