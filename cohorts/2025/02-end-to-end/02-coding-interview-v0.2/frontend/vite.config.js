import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { copyFileSync, mkdirSync } from 'fs'
import { join } from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    // Plugin to copy Pyodide files to assets directory
    {
      name: 'copy-pyodide-files',
      writeBundle() {
        const pyodidePath = 'node_modules/pyodide';
        const outDir = 'dist/assets';
        
        // Create assets directory if it doesn't exist
        mkdirSync(outDir, { recursive: true });
        
        // List of Pyodide files to copy
        const filesToCopy = [
          'pyodide.asm.js',
          'pyodide.asm.wasm',
          'pyodide-lock.json',
          'python_stdlib.zip',
          'pyodide.asm.data'
        ];
        
        // Copy each file
        filesToCopy.forEach(file => {
          try {
            const src = join(pyodidePath, file);
            const dest = join(outDir, file);
            copyFileSync(src, dest);
            console.log(`Copied ${file} to ${outDir}`);
          } catch (err) {
            // Some files might not exist in all Pyodide versions
            console.warn(`Could not copy ${file}:`, err.message);
          }
        });
      }
    }
  ],
  optimizeDeps: {
    exclude: ['pyodide']
  },
  server: {
    proxy: {
      // Proxy API requests to backend
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      // Proxy WebSocket connections to backend
      '/ws': {
        target: 'ws://localhost:8000',
        ws: true,
        changeOrigin: true,
      }
    }
  }
})
