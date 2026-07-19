import { getCollection, type CollectionEntry } from 'astro:content';
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';

export type Post = CollectionEntry<'posts'>;

// Sesiones "leaf": tienen markdowns directamente bajo su carpeta en el repo.
// Renderizan como `/<slug>/` (lista) y `/<slug>/<post-id>/` (post).
export const LEAF_SESSIONS = [
  'arquitectura-software',
  'agentes-ia',
  'algoritmia',
  'ingenieria-de-requisitos',
  'ingenieria-de-software',
] as const;
export type LeafSession = (typeof LEAF_SESSIONS)[number];

// Namespaces: NO tienen markdowns propios. Agrupan sub-dominios (children).
// Renderizan como `/<ns>/` (lista de children) y `/<ns>/<child>/` (lista de markdowns del child).
// `sessionField` es el valor que va en el frontmatter `session` de los markdowns del child.
export type NamespaceChild = {
  slug: string;
  label: string;
  description: string;
  sessionField: string;
};

export type Namespace = {
  slug: string;
  label: string;
  description: string;
  children: readonly NamespaceChild[];
};

export const NAMESPACES: readonly Namespace[] = [
  {
    slug: 'Dominios',
    label: 'Dominios',
    description: 'Investigación de dominios previa a implementación.',
    children: [
      {
        slug: 'ordenes-de-compra',
        label: 'Órdenes de Compra',
        description:
          'Purchase-to-Pay (P2P): ciclo completo de compras y sincronización de stock.',
        sessionField: 'ordenes-de-compra',
      },
    ],
  },
] as const;

// Etiquetas amigables para mostrar en la UI
export const LEAF_SESSION_LABELS: Record<LeafSession, string> = {
  'arquitectura-software': 'Arquitectura de Software',
  'agentes-ia': 'Agentes de IA',
  algoritmia: 'Algoritmia',
  'ingenieria-de-requisitos': 'Ingeniería de Requisitos',
  'ingenieria-de-software': 'Ingeniería de Software',
};

// Descripciones cortas de cada sesión leaf
export const LEAF_SESSION_DESCRIPTIONS: Record<LeafSession, string> = {
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
 * Resuelve el path URL de un leaf o un namespace+child.
 * - leaf: 'agentes-ia'
 * - namespace child: 'Dominios/ordenes-de-compra'
 */
export function resolveSessionPath(
  session: LeafSession | string,
  child?: string,
): string {
  return child ? `${session}/${child}` : session;
}

/**
 * Devuelve el label legible de una sesión.
 * - leaf-session: lookup en LEAF_SESSION_LABELS
 * - namespace child: lookup del child.label
 * - namespace: lookup del ns.label
 * - sessionField (cuando se pasa directamente, p.ej. desde el frontmatter): busca el child
 *   cuyo sessionField coincide y devuelve su label
 */
export function sessionLabel(
  session: string,
  child?: string,
): string {
  if (child) {
    const ns = NAMESPACES.find((n) => n.slug === session);
    const ch = ns?.children.find((c) => c.slug === child);
    if (ch) return ch.label;
  }
  if ((LEAF_SESSIONS as readonly string[]).includes(session)) {
    return LEAF_SESSION_LABELS[session as LeafSession] ?? session;
  }
  // Lookup por sessionField (frontmatter `session` directo de un post)
  for (const ns of NAMESPACES) {
    const ch = ns.children.find((c) => c.sessionField === session);
    if (ch) return ch.label;
  }
  const ns = NAMESPACES.find((n) => n.slug === session);
  return ns?.label ?? session;
}

/**
 * Devuelve la descripción legible (leaf-session, namespace-child, namespace).
 * Si se pasa directamente un sessionField (frontmatter), busca el child correspondiente.
 */
export function sessionDescription(
  session: string,
  child?: string,
): string {
  if (child) {
    const ns = NAMESPACES.find((n) => n.slug === session);
    const ch = ns?.children.find((c) => c.slug === child);
    return ch?.description ?? '';
  }
  if ((LEAF_SESSIONS as readonly string[]).includes(session)) {
    return LEAF_SESSION_DESCRIPTIONS[session as LeafSession] ?? '';
  }
  for (const ns of NAMESPACES) {
    const ch = ns.children.find((c) => c.sessionField === session);
    if (ch) return ch.description;
  }
  const ns = NAMESPACES.find((n) => n.slug === session);
  return ns?.description ?? '';
}

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
 * Devuelve los posts filtrados por session field del frontmatter.
 * Funciona tanto para leaf como para namespace-child (el sessionField del child
 * es lo que va en el frontmatter `session`).
 */
export async function getPostsBySessionField(sessionField: string): Promise<Post[]> {
  const posts = await getAllPosts();
  return posts.filter((p) => p.data.session === sessionField);
}

/**
 * Devuelve los posts filtrados por tag (case-insensitive).
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
 * Devuelve todos los "sessionField" activos en el repo (presente en al menos un post).
 * Útil para que la home muestre solo sesiones con contenido.
 */
export async function getActiveSessionFields(): Promise<Set<string>> {
  const posts = await getAllPosts();
  return new Set(posts.map((p) => p.data.session));
}

/**
 * Cuenta cuántos posts (markdowns) hay por sessionField.
 */
export async function getSessionPostCounts(): Promise<Record<string, number>> {
  const posts = await getAllPosts();
  const counts: Record<string, number> = {};
  for (const leaf of LEAF_SESSIONS) counts[leaf] = 0;
  for (const ns of NAMESPACES) {
    for (const ch of ns.children) counts[ch.sessionField] = 0;
  }
  for (const post of posts) {
    counts[post.data.session] = (counts[post.data.session] ?? 0) + 1;
  }
  return counts;
}

/**
 * Cuenta cuántos assets (notebooks + archivos de código) hay por sessionField,
 * leyendo los `_index.json` que genera `scripts/assets.py` durante el build.
 *
 * - Para leaf-session: se busca en `public/<leaf>/_index.json`.
 * - Para namespace-child: se busca en `public/<ns>/<child>/_index.json`.
 */
export async function getSessionAssetCounts(): Promise<Record<string, number>> {
  const counts: Record<string, number> = {};
  for (const leaf of LEAF_SESSIONS) counts[leaf] = 0;
  for (const ns of NAMESPACES) {
    for (const ch of ns.children) counts[ch.sessionField] = 0;
  }

  const projectRoot = process.cwd();

  const lookupPaths: Array<{ key: string; path: string }> = [];
  for (const leaf of LEAF_SESSIONS) {
    lookupPaths.push({ key: leaf, path: resolve(projectRoot, 'public', leaf, '_index.json') });
  }
  for (const ns of NAMESPACES) {
    for (const ch of ns.children) {
      lookupPaths.push({
        key: ch.sessionField,
        path: resolve(projectRoot, 'public', ns.slug, ch.slug, '_index.json'),
      });
    }
  }

  await Promise.all(
    lookupPaths.map(async ({ key, path }) => {
      try {
        const raw = await readFile(path, 'utf8');
        const data = JSON.parse(raw);
        if (Array.isArray(data)) counts[key] = data.length;
      } catch {
        // No _index.json → 0 assets
      }
    }),
  );

  return counts;
}

/**
 * Cuenta el total combinado (posts + assets) por sessionField.
 * Es lo que se muestra en la home: "X notas".
 */
export async function getSessionCounts(): Promise<Record<string, number>> {
  const [posts, assets] = await Promise.all([
    getSessionPostCounts(),
    getSessionAssetCounts(),
  ]);
  const total: Record<string, number> = {};
  for (const leaf of LEAF_SESSIONS) total[leaf] = posts[leaf] + assets[leaf];
  for (const ns of NAMESPACES) {
    for (const ch of ns.children) {
      total[ch.sessionField] = posts[ch.sessionField] + assets[ch.sessionField];
    }
  }
  return total;
}

/**
 * Convierte un slug de entrada a la ruta URL del sitio.
 * Ej: id "arquitectura-software/monolito" → "/arquitectura-software/monolito"
 *     id "Dominios/ordenes-de-compra/01-foo" → "/Dominios/ordenes-de-compra/01-foo"
 */
export function postUrl(post: Post): string {
  return `/${post.id}`;
}
