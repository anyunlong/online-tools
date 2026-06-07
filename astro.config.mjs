import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
export default defineConfig({
  site: 'https://online-tools.vercel.app',
  vite: { plugins: [tailwindcss()] }
});