import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // pozwala na dostęp spoza localhost
    allowedHosts: [
      'quiztokfront.byst.re' // ⬅️ twoja domena
    ],
  },
});
