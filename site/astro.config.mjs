import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
  site: 'https://learning.technoova.es',
  integrations: [mdx()],
  vite: {
    plugins: [tailwindcss()],
    // Pagefind sólo existe tras el build en `dist/pagefind/`. Lo marcamos como
    // externo para que Rollup no intente resolverlo durante la compilación.
    build: {
      rollupOptions: {
        external: [/^\/pagefind\//],
      },
    },
    // Ignorar el módulo en SSR/dev también, evitando errores si no existe.
    ssr: {
      noExternal: [],
    },
  },
});
