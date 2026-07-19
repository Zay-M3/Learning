import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

// Esquema de la colección de posts (markdowns sincronizados desde las sesiones del repo)
const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content' }),
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
      'Dominios',
    ]),
    tags: z.array(z.string()).default([]),
    date: z.date().optional(),
    draft: z.boolean().default(false),
  }),
});

export const collections = { posts };
