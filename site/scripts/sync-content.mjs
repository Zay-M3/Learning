#!/usr/bin/env node
// Sincroniza los markdowns de las sesiones del repo (raíz) hacia src/content/
// y se asegura de inyectar el frontmatter `session` y `title` en cada archivo.
import fs from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const SITE_DIR = path.resolve(__dirname, '..');
// REPO_ROOT: raíz del repo donde viven las carpetas de sesiones.
// - En local: se infiere desde SITE_DIR/.. (sitio vive en site/ del repo)
// - En Docker (Dokploy): viene de env var LEARNING_REPO_ROOT (montado en /repo-sessions)
const REPO_ROOT = process.env.LEARNING_REPO_ROOT
  ? process.env.LEARNING_REPO_ROOT
  : path.resolve(SITE_DIR, '..');
const CONTENT_DIR = path.join(SITE_DIR, 'src', 'content');

const SESSIONS = [
  'arquitectura-software',
  'agentes-ia',
  'algoritmia',
  'ingenieria-de-requisitos',
  'ingenieria-de-software',
];

async function main() {
  // Limpiar y recrear el directorio de contenido
  await fs.rm(CONTENT_DIR, { recursive: true, force: true });
  await fs.mkdir(CONTENT_DIR, { recursive: true });

  let totalFiles = 0;

  for (const session of SESSIONS) {
    const srcDir = path.join(REPO_ROOT, session);
    const dstDir = path.join(CONTENT_DIR, session);
    try {
      await fs.cp(srcDir, dstDir, {
        recursive: true,
        filter: (f) => f.endsWith('.md') || !f.includes('.'),
      });
    } catch (e) {
      console.warn(`⚠️  Sesión "${session}" no encontrada en repo root:`, e.message);
      continue;
    }

    // Inyectar frontmatter `session` y `title` si faltan
    const files = await walkMd(dstDir);
    for (const file of files) {
      await ensureFrontmatter(file, session);
    }
    totalFiles += files.length;
    console.log(`  • ${session}: ${files.length} markdowns`);
  }

  console.log(
    `✅ Sincronizadas ${SESSIONS.length} sesiones (${totalFiles} posts) → ${CONTENT_DIR}`,
  );
}

async function walkMd(dir) {
  const out = [];
  const entries = await fs.readdir(dir, { withFileTypes: true });
  for (const e of entries) {
    const full = path.join(dir, e.name);
    if (e.isDirectory()) out.push(...(await walkMd(full)));
    else if (e.name.endsWith('.md')) out.push(full);
  }
  return out;
}

/**
 * Devuelve el slug legible del filename, sin extensión y separado por guiones.
 * Ej: "estilos-arquitectura.md" → "estilos-arquitectura"
 */
function filenameSlug(filepath) {
  return path.basename(filepath, '.md');
}

/**
 * Extrae el título del primer encabezado H1 del markdown (sin #).
 * Devuelve null si no encuentra.
 */
function extractH1Title(raw) {
  // Busca la primera línea que sea un H1 (# … ######), la primera heading puede estar
  // antes o después del frontmatter; como el caller le pasa el contenido post-FM,
  // basta con buscar al principio.
  const lines = raw.split(/\r?\n/);
  for (const line of lines) {
    const m = line.match(/^#\s+(.+?)\s*#*\s*$/);
    if (m) return m[1].trim();
  }
  return null;
}

/**
 * Asegura que el archivo tenga frontmatter `session` y `title`.
 * - session: siempre se inyecta (obligatorio por schema).
 * - title: si no existe, intenta sacarlo del primer H1; si no, usa el slug del filename.
 */
async function ensureFrontmatter(file, session) {
  const raw = await fs.readFile(file, 'utf8');
  let fm = '';
  let body = raw;

  // Detectar frontmatter existente
  if (/^---\n/.test(raw)) {
    const closeIdx = raw.indexOf('\n---\n', 4);
    if (closeIdx !== -1) {
      fm = raw.slice(0, closeIdx + 5);
      body = raw.slice(closeIdx + 5);
    }
  }

  const fmText = fm.replace(/^---\n/, '').replace(/\n---\n?$/, '');
  const hasSession = /^session:\s/m.test(fmText);
  const hasTitle = /^title:\s/m.test(fmText);

  if (hasSession && hasTitle) return;

  // Construir líneas a inyectar
  const additions = [];
  if (!hasSession) additions.push(`session: ${session}`);

  if (!hasTitle) {
    // 1) intentar H1 del cuerpo (post-frontmatter)
    let title = extractH1Title(body);
    // 2) fallback: filename legible
    if (!title) {
      const slug = filenameSlug(file);
      title = slug
        .replace(/^index-/, '')
        .replace(/-/g, ' ')
        .replace(/\b\w/g, (c) => c.toUpperCase());
      if (!title) title = slug;
    }
    // Escapar comillas dobles para YAML
    const safe = title.replace(/"/g, '\\"');
    additions.push(`title: "${safe}"`);
  }

  if (fm) {
    // Insertar antes de la línea de cierre `---`
    const closeIdx = raw.indexOf('\n---\n', 4);
    const before = raw.slice(0, closeIdx + 1); // incluye "\n"
    const after = raw.slice(closeIdx + 1);     // empieza con "---\n..."
    const newFm = `---\n${fmText.trim()}\n${additions.join('\n')}\n---\n`;
    await fs.writeFile(file, newFm + after);
  } else {
    // Sin frontmatter — agregar uno nuevo al principio
    const newFm = `---\n${additions.join('\n')}\n---\n\n`;
    await fs.writeFile(file, newFm + raw);
  }
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
