import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    allowedHosts: [
      'quiztokfront.byst.re'
    ],
    proxy: {
      '/webhook-test': {
        target: 'http://localhost:5678', // albo do swojego n8n
        changeOrigin: true,
      },
    },
  },
});
