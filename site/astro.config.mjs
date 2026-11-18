import { defineConfig } from 'astro/config';

// Plain static output: every page is pre-rendered HTML. No server, no adapter.
export default defineConfig({
  trailingSlash: 'ignore',
  build: { format: 'directory' },
});
