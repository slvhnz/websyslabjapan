import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Production configuration for Vercel deployment
export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist',
    sourcemap: false,
    minify: 'terser',
  },
  define: {
    'process.env.VITE_API_URL': JSON.stringify(process.env.VITE_API_URL || 'https://your-api.vercel.app'),
  }
})
