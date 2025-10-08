import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'node:path'
export default defineConfig({ plugins: [react()], envDir: resolve(__dirname, '..'), server: { port: 5173 }, build: { outDir: 'dist' } })
