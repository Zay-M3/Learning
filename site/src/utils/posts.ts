import { getCollection, type CollectionEntry } from 'astro:content';
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';

export type Post = CollectionEntry<'posts'>;

export const SESSIONS = [
  'arquitectura-software',
  'agentes-ia',
  'algoritmia',
  'ingenieria-de-requisitos',
  'ingenieria-de-software',
] as const;

export type Session = (typeof SESSIONS)[number];

// Etiquetas amigables para mostrar en la UI
export const SESSION_LABELS: Record<Session, string> = {
  'arquitectura-software': 'Arquitectura de Software',
  'agentes-ia': 'Agentes de IA',
  algoritmia: 'Algoritmia',
  'ingenieria-de-requisitos': 'Ingeniería de Requisitos',
  'ingenieria-de-software': 'Ingeniería de Software',
};

// Descripciones cortas de cada sesión
export const SESSION_DESCRIPTIONS: Record<Session, string> = {
  'arquitectura-software':
    'Patrones, estilos y decisiones de diseño de sistemas a gran escala.',
  'agentes-ia': 'Patrones y técnicas para construir agentes conversacionales.',
  algoritmia: 'Algoritmos clásicos y análisis de complejidad.',
  'ingenieria-de-requisitos':
    'Elicitación, análisis y gestión de requisitos de software.',
  'ingenieria-de-software':
    'Fundamentos, procesos y prácticas de ingeniería de software.',
};

/**
 * Devuelve el título de un post. Si el frontmatter no lo trae, lo deriva del
 * filename: "estilos-arquitectura" → "Estilos Arquitectura".
 */
export function getTitle(post: Post): string {
  if (post.data.title && post.data.title.trim()) return post.data.title;
  const filename = post.id.split('/').pop() ?? post.id;
  return filename
    .replace(/^index-/, '')
    .replace(/-/g, ' ')
    .replace(/\b\w/g, (c) => c.toUpperCase())
    .trim() || filename;
}

/**
 * Devuelve todos los posts publicados (no draft), ordenados por fecha descendente.
 */
export async function getAllPosts(): Promise<Post[]> {
  const posts = await getCollection('posts', ({ data }) => !data.draft);
  return posts.sort((a, b) => {
    const da = a.data.date?.getTime() ?? 0;
    const db = b.data.date?.getTime() ?? 0;
    return db - da;
  });
}

/**
 * Devuelve los posts filtrados por sesión.
 */
export async function getPostsBySession(session: Session): Promise<Post[]> {
  const posts = await getAllPosts();
  return posts.filter((p) => p.data.session === session);
}

/**
 * Devuelve los posts que tengan la etiqueta indicada (case-insensitive).
 */
export async function getPostsByTag(tag: string): Promise<Post[]> {
  const posts = await getAllPosts();
  const needle = tag.toLowerCase();
  return posts.filter((p) =>
    p.data.tags.some((t) => t.toLowerCase() === needle),
  );
}

/**
 * Devuelve el mapa tag -> cantidad de posts.
 */
export async function getAllTags(): Promise<Map<string, number>> {
  const posts = await getAllPosts();
  const counts = new Map<string, number>();
  for (const post of posts) {
    for (const tag of post.data.tags) {
      counts.set(tag, (counts.get(tag) ?? 0) + 1);
    }
  }
  return counts;
}

/**
 * Devuelve todas las sesiones que tienen al menos un post.
 */
export async function getAllSessions(): Promise<Session[]> {
  const posts = await getAllPosts();
  const present = new Set(posts.map((p) => p.data.session));
  return SESSIONS.filter((s) => present.has(s));
}

/**
 * Cuenta cuántos posts (markdowns) hay por sesión.
 */
export async function getSessionPostCounts(): Promise<Record<Session, number>> {
  const posts = await getAllPosts();
  const counts = Object.fromEntries(
    SESSIONS.map((s) => [s, 0]),
  ) as Record<Session, number>;
  for (const post of posts) {
    counts[post.data.session]++;
  }
  return counts;
}

/**
 * Cuenta cuántos assets (notebooks + archivos de código) hay por sesión,
 * leyendo los `_index.json` que genera `scripts/assets.py` durante el build.
 */
export async function getSessionAssetCounts(): Promise<Record<Session, number>> {
  const counts = Object.fromEntries(
    SESSIONS.map((s) => [s, 0]),
  ) as Record<Session, number>;

  // `process.cwd()` durante el build es la raíz del proyecto Astro
  // (donde están `astro.config.mjs`, `package.json`, `public/`).
  const projectRoot = process.cwd();

  await Promise.all(
    SESSIONS.map(async (s) => {
      try {
        const path = resolve(projectRoot, 'public', s, '_index.json');
        const raw = await readFile(path, 'utf8');
        const data = JSON.parse(raw);
        if (Array.isArray(data)) counts[s] = data.length;
      } catch {
        // No _index.json → 0 assets (sesión sin notebooks/files)
      }
    }),
  );

  return counts;
}

/**
 * Cuenta el total combinado (posts + assets) por sesión.
 * Es lo que se muestra en la home: "X notas" donde X incluye tanto
 * markdowns como notebooks/archivos de código.
 */
export async function getSessionCounts(): Promise<Record<Session, number>> {
  const [posts, assets] = await Promise.all([
    getSessionPostCounts(),
    getSessionAssetCounts(),
  ]);
  const total = Object.fromEntries(
    SESSIONS.map((s) => [s, 0]),
  ) as Record<Session, number>;
  for (const s of SESSIONS) {
    total[s] = posts[s] + assets[s];
  }
  return total;
}

/**
 * Convierte un slug de entrada a la ruta URL del sitio.
 * Ej: id "arquitectura-software/monolito" → "/arquitectura-software/monolito"
 */
export function postUrl(post: Post): string {
  return `/${post.id}`;
}

/**
 * Etiqueta legible de una sesión (con fallback al slug).
 */
export function sessionLabel(session: Session | string): string {
  return SESSION_LABELS[session as Session] ?? session;
}
