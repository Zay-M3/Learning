# Learning-site — Local dev

Esta carpeta contiene el sitio Astro. Los markdowns viven en las carpetas
de la raíz del repo (`../arquitectura-software/`, `../agentes-ia/`, etc.) y
se sincronizan automáticamente con `scripts/sync-content.mjs`.

## Requisitos

- Node 22 (`nvm use`)

## Pasos

```bash
cd site
npm install
npm run dev      # http://localhost:4321
```

## Build de producción

```bash
npm run build    # sync + astro build + pagefind --site dist
```

Output en `dist/`, índice de búsqueda en `dist/pagefind/`.

## Estructura

- `src/pages/` — Rutas (index, search, tags, [...slug], [session])
- `src/components/` — ThemeToggle, SessionSidebar, SearchBox, MarkdownCard, TagChip
- `src/layouts/BaseLayout.astro` — Layout con sidebar, header y dark/light toggle
- `src/utils/posts.ts` — Helpers sobre la collection `posts`
- `src/content.config.ts` — Schema Zod de la collection
- `scripts/sync-content.mjs` — Copia los `.md` de la raíz a `src/content/`
- `Dockerfile` + `nginx.conf` — Build multi-stage para producción
