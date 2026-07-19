import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Esquema de la colección de posts (markdowns sincronizados desde las sesiones del repo).
// `generateId` preserva el case del path (Astro por defecto usa github-slugger que
// lowercase, lo cual rompe namespaces con mayúsculas como "Dominios/").
const posts = defineCollection({
  loader: glob({
    pattern: '**/*.md',
    base: './src/content',
    generateId: ({ entry }) =>
      entry
        .replace(/^.*?src\/content\//, '')
        .replace(/\.md$/, ''),
  }),
  schema: z.object({
    // Title es opcional: si falta, se deriva del nombre de archivo.
    title: z.string().optional(),
    description: z.string().optional(),
    session: z.enum([
      'arquitectura-software',
      'agentes-ia',
      'algoritmia',
      'ingenieria-de-requisitos',
      'ingenieria-de-software',
      'ordenes-de-compra',
    ]),
    tags: z.array(z.string()).default([]),
    date: z.date().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { posts };
