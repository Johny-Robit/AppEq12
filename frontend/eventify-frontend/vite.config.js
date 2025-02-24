import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  base: '/AppEq12/', // Doit correspondre au nom du dépôt
  plugins: [vue()],
  server: {
    open: true,
  },
})
