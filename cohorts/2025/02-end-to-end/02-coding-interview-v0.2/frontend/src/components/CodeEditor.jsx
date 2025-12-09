/**
 * CodeEditor component with CodeMirror 6
 * Supports real-time collaborative editing
 */
import { useEffect, useRef } from 'react';
import { EditorView } from '@codemirror/view';
import { EditorState } from '@codemirror/state';
import { python } from '@codemirror/lang-python';
import { oneDark } from '@codemirror/theme-one-dark';

/**
 * CodeEditor component
 * @param {Object} props
 * @param {string} props.code - Initial code content
 * @param {Function} props.onChange - Callback when code changes
 * @param {boolean} props.readOnly - Whether editor is read-only
 */
export function CodeEditor({ code, onChange, readOnly = false }) {
  const editorRef = useRef(null);
  const viewRef = useRef(null);
  const isRemoteChange = useRef(false);

  // Initialize CodeMirror
  useEffect(() => {
    if (!editorRef.current) return;

    const startState = EditorState.create({
      doc: code || '# Write your Python code here\n',
      extensions: [
        python(),
        oneDark,
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
  }, [readOnly]); // Only recreate on readOnly change

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
