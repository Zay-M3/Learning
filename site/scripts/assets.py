#!/usr/bin/env python3
"""
Procesa todos los assets de las sesiones del repo Learning:
- Notebooks .ipynb → HTML estático self-contained (con outputs ejecutados)
- Archivos de código → HTML con syntax highlighting (Pygments)
- Archivos no-código (.txt, .json, .csv, etc.) → HTML con highlighting o texto plano
- Binarios (imágenes, etc.) → copia tal cual

Output por sesión en public/<session>/<asset-type>/<slug>/index.html
Output combinado: public/<session>/_index.json con metadata de todos los assets

Uso:
    python3 scripts/assets.py
    LEARNING_REPO_ROOT=/repo-sessions python3 scripts/assets.py   (en Docker)
"""
import json
import os
import re
import shutil
import sys
import urllib.request
from pathlib import Path

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor


HERE = Path(__file__).resolve().parent
SITE_DIR = HERE.parent

# Raíz del repo: puede venir por env (Docker) o se infiere desde SITE_DIR
REPO_ROOT = Path(os.environ.get("LEARNING_REPO_ROOT") or SITE_DIR.parent)
PUBLIC_DIR = SITE_DIR / "public"


# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

ASSET_EXTENSIONS: dict[str, str] = {
    # Código con highlighting por nombre de lexer
    ".py": "python",
    ".js": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "typescript",
    ".jsx": "jsx",
    ".tsx": "tsx",
    ".rs": "rust",
    ".go": "go",
    ".java": "java",
    ".c": "c",
    ".h": "c",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".hpp": "cpp",
    ".rb": "ruby",
    ".php": "php",
    ".sh": "bash",
    ".bash": "bash",
    ".zsh": "bash",
    ".sql": "sql",
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    ".scss": "scss",
    ".sass": "sass",
    ".less": "less",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".xml": "xml",
    ".md": "markdown",
    ".txt": "text",
    ".csv": "csv",
    ".tsv": "tsv",
    ".ini": "ini",
    ".conf": "ini",
    ".cfg": "ini",
    ".env": "bash",
    ".dockerfile": "dockerfile",
    ".lua": "lua",
    ".pl": "perl",
    ".kt": "kotlin",
    ".swift": "swift",
    ".dart": "dart",
    ".r": "r",
    ".scala": "scala",
    ".vue": "vue",
    ".svelte": "svelte",
}

BINARY_EXTENSIONS: set[str] = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".ico",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".bz2",
    ".xz",
    ".7z",
    ".rar",
    ".mp4",
    ".mp3",
    ".wav",
    ".mov",
    ".webm",
}

# Estructura jerárquica (debe reflejar src/utils/posts.ts).
# - LEAF_SESSIONS: sesiones planas en el repo root (carpeta directa).
# - NAMESPACES: cada namespace tiene `children` con su propio `slug`; los
#   assets viven en `<repo>/<ns>/<child>/`. El "session field" para el
#   _index.json es el slug del child (se usa como clave en la home).
LEAF_SESSIONS: list[str] = [
    "arquitectura-software",
    "agentes-ia",
    "algoritmia",
    "ingenieria-de-requisitos",
    "ingenieria-de-software",
]

NAMESPACES: list[dict] = [
    {
        "slug": "Dominios",
        "children": [
            {"slug": "ordenes-de-compra"},
        ],
    },
]


def iter_session_paths() -> list[tuple[str, Path]]:
    """Devuelve (url_path, repo_dir) para cada sesión activa.
    Para leaf: url_path = leaf slug, repo_dir = <root>/<leaf>.
    Para namespace-child: url_path = <ns_slug>/<child_slug>, repo_dir = <root>/<ns>/<child>.
    """
    out: list[tuple[str, Path]] = []
    for leaf in LEAF_SESSIONS:
        out.append((leaf, REPO_ROOT / leaf))
    for ns in NAMESPACES:
        for ch in ns["children"]:
            url_path = f"{ns['slug']}/{ch['slug']}"
            out.append((url_path, REPO_ROOT / ns["slug"] / ch["slug"]))
    return out


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------


def slugify(name: str) -> str:
    """Convierte 'quicshort.py' → 'quicshort'."""
    base = name.rsplit(".", 1)[0] if "." in name else name
    return base.replace("_", "-").replace(" ", "-").lower()


def titleize(name: str) -> str:
    """Convierte 'quicshort.py' → 'Quicshort' para mostrar al usuario."""
    base = slugify(name)
    return base.replace("-", " ").title()


def emoji_for_extension(ext: str) -> str:
    """Emoji representativo según la extensión del archivo."""
    mapping = {
        ".py": "🐍",
        ".ipynb": "📓",
        ".js": "🟨",
        ".ts": "🔷",
        ".jsx": "⚛️",
        ".tsx": "⚛️",
        ".rs": "🦀",
        ".go": "🐹",
        ".java": "☕",
        ".c": "©️",
        ".cpp": "➕",
        ".rb": "💎",
        ".php": "🐘",
        ".sh": "🐚",
        ".sql": "🗄️",
        ".html": "🌐",
        ".css": "🎨",
        ".json": "📋",
        ".yaml": "⚙️",
        ".yml": "⚙️",
        ".toml": "⚙️",
        ".md": "📝",
        ".txt": "📄",
        ".csv": "📊",
        ".png": "🖼️",
        ".jpg": "🖼️",
        ".jpeg": "🖼️",
        ".gif": "🖼️",
        ".svg": "🖼️",
        ".pdf": "📕",
        ".zip": "🗜️",
    }
    return mapping.get(ext.lower(), "📄")


def get_cell_count(nb_path: Path) -> int:
    """Cuenta las celdas de un notebook .ipynb."""
    try:
        with open(nb_path, encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
        return len(nb.cells)
    except Exception:
        return 0


def get_notebook_description(nb_path: Path) -> str:
    """Extrae la primera celda markdown del notebook (para descripción)."""
    try:
        with open(nb_path, encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
        for cell in nb.cells:
            if cell.cell_type == "markdown":
                return "".join(cell.source).strip()
    except Exception:
        pass
    return ""


# ---------------------------------------------------------------------------
# Búsqueda de assets
# ---------------------------------------------------------------------------


def find_assets(session_dir: Path) -> dict[str, list[Path]]:
    """Busca notebooks, archivos de código y binarios en una sesión."""
    assets: dict[str, list[Path]] = {"notebooks": [], "code": [], "binary": []}
    if not session_dir.exists():
        return assets
    for f in sorted(session_dir.rglob("*")):
        if not f.is_file():
            continue
        suffix = f.suffix.lower()
        if suffix == ".ipynb":
            assets["notebooks"].append(f)
        elif suffix in BINARY_EXTENSIONS:
            assets["binary"].append(f)
        elif suffix in ASSET_EXTENSIONS:
            assets["code"].append(f)
        # Ignorar .md (ya se manejan en sync-content.mjs)
    return assets


# ---------------------------------------------------------------------------
# Renderer de notebooks
# ---------------------------------------------------------------------------


def embed_external_resources(html: str) -> str:
    """
    Descarga CSS/JS de CDN y los embebe inline para que el HTML sea
    realmente self-contained (sin dependencias de red).
    """

    # Reemplazar links CSS
    def link_replace(match: re.Match) -> str:
        attrs = match.group(1)
        url = match.group(2)
        if not url.startswith(("http://", "https://")) or "stylesheet" not in attrs:
            return match.group(0)
        try:
            print(f"    ↳ embebiendo CSS {url[:80]}")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read().decode("utf-8", errors="replace")
            return f"<style>{content}</style>"
        except Exception as e:
            print(f"    ⚠️  no se pudo descargar {url}: {e}")
            return match.group(0)

    html = re.sub(
        r"<link([^>]*?)href=[\"'](https?://[^\"']+)[\"']",
        link_replace,
        html,
    )

    # Reemplazar scripts src
    def script_replace(match: re.Match) -> str:
        url = match.group(1)
        try:
            print(f"    ↳ embebiendo script {url[:80]}")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read().decode("utf-8", errors="replace")
            return f"<script>{content}</script>"
        except Exception as e:
            print(f"    ⚠️  no se pudo descargar {url}: {e}")
            return match.group(0)

    html = re.sub(
        r"<script[^>]*?src=[\"'](https?://[^\"']+)[\"']",
        script_replace,
        html,
    )
    html = re.sub(r"</script>\s*</script>", "</script>", html)
    return html


def convert_notebook(nb_path: Path, session: str) -> tuple[Path, str]:
    """
    Convierte un .ipynb a HTML self-contained.
    Devuelve (path_salida, slug).
    """
    slug = slugify(nb_path.name)
    out_dir = PUBLIC_DIR / session / "notebooks" / slug
    out_file = out_dir / "index.html"
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(nb_path, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    # Intentar ejecutar el notebook. Si falla, usamos los outputs embebidos.
    try:
        ep = ExecutePreprocessor(timeout=60, kernel_name="python3")
        ep.preprocess(nb, {"metadata": {"path": str(nb_path.parent)}})
        print(f"  ✓ Ejecutado: {nb_path.name}")
    except Exception as e:
        print(f"  ⚠️  No se pudo ejecutar {nb_path.name}: {e}")
        print("     → usando outputs embebidos")

    exporter = HTMLExporter(
        template_name="classic",
        exclude_input_prompt=False,
        exclude_output_prompt=False,
        exclude_input=False,
        exclude_output=False,
    )
    body, _resources = exporter.from_notebook_node(nb)
    body = embed_external_resources(body)

    # Inyectar botón "Volver" justo después del <body>
    back_href = f"/{session}/" if session else "/"
    back_button = (
        f'<div style="position:fixed;top:0;left:0;right:0;z-index:9999;'
        f'background:#fafafa;border-bottom:1px solid #e4e4e7;padding:0.75rem 1.5rem;'
        f'font-family:system-ui,-apple-system,sans-serif;font-size:0.875rem">'
        f'<a href="{back_href}" style="color:#2563eb;text-decoration:none;font-weight:500">'
        f'← Volver a {session or "inicio"}</a>'
        f'</div>'
        f'<div style="height:3rem"></div>'  # Spacer para que el contenido no quede tapado
    )
    body = re.sub(r"(<body[^>]*>)", r"\1" + back_button, body, count=1)

    with open(out_file, "w", encoding="utf-8") as f:
        f.write(body)

    size_kb = out_file.stat().st_size / 1024
    print(f"  ✓ {nb_path.name} → {out_file.relative_to(SITE_DIR)} ({size_kb:.1f} KB)")
    return out_file, slug


# ---------------------------------------------------------------------------
# Renderer universal de código (Pygments)
# ---------------------------------------------------------------------------


def render_code_to_html(filepath: Path, language: str, session: str = "") -> tuple[str, str]:
    """
    Renderiza un archivo de código a HTML con Pygments.
    Devuelve (body_html, page_completa).
    `session` se usa para construir el link "Volver" a la página de sesión.
    """
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.util import ClassNotFound

    code = filepath.read_text(encoding="utf-8", errors="replace")

    # Intentar lexer por nombre, si no por guess, fallback a texto plano
    try:
        lexer = get_lexer_by_name(language)
    except ClassNotFound:
        try:
            lexer = guess_lexer(code)
        except ClassNotFound:
            lexer = get_lexer_by_name("text")

    formatter = HtmlFormatter(
        style="monokai",
        full=True,
        linenos="table",
        lineanchors="line",
        anchorlinenos=True,
        cssclass="highlight",
    )
    body = highlight(code, lexer, formatter)

    size_kb = filepath.stat().st_size / 1024
    # Link "Volver" apunta a la página de sesión, no al directorio padre
    back_href = f"/{session}/" if session else "/"
    page = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{filepath.name} - Learning</title>
  <style>
    body {{ font-family: system-ui, -apple-system, sans-serif; max-width: 1000px; margin: 0 auto; padding: 2rem; background: #fafafa; color: #18181b; }}
    pre, code {{ font-family: 'Fira Mono', 'Cascadia Code', 'Courier New', monospace; font-size: 0.875rem; line-height: 1.5; }}
    .linenos {{ color: #888; user-select: none; }}
    a.back {{ display: inline-block; margin-bottom: 1.5rem; color: #2563eb; text-decoration: none; font-size: 0.875rem; }}
    a.back:hover {{ text-decoration: underline; }}
    h1 {{ font-size: 1.5rem; margin: 0 0 0.5rem; color: #18181b; }}
    .meta {{ color: #71717a; font-size: 0.875rem; margin-bottom: 1.5rem; }}
    .meta code {{ background: #f4f4f5; padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-size: 0.8125rem; }}
  </style>
</head>
<body>
  <a href="{back_href}" class="back">← Volver a {session or 'inicio'}</a>
  <h1>{filepath.name}</h1>
  <p class="meta">
    Lenguaje: <code>{lexer.name}</code>
    · Tamaño: <code>{size_kb:.1f} KB</code>
    · Solo lectura
  </p>
  {body}
</body>
</html>"""
    return body, page


# ---------------------------------------------------------------------------
# Pipeline principal
# ---------------------------------------------------------------------------


def process_session(session_dir: Path, session_path: str) -> list[dict]:
    """Procesa todos los assets de una sesión. Devuelve la metadata.
    `session_dir` es la carpeta en el repo; `session_path` es el prefijo URL
    donde se publican los assets. Para namespace-children se pasa
    p.ej. ("<root>/Dominios/ordenes-de-compra", "Dominios/ordenes-de-compra").
    """
    if not session_dir.exists():
        print(f"⏭️  {session_path}: carpeta inexistente")
        return []

    print(f"\n📂 {session_path} → {session_dir}")
    assets = find_assets(session_dir)
    nb_count = len(assets["notebooks"])
    code_count = len(assets["code"])
    bin_count = len(assets["binary"])
    print(f"   {nb_count} notebooks · {code_count} código · {bin_count} binarios")

    session_meta: list[dict] = []

    # 1. Notebooks
    for nb in assets["notebooks"]:
        out_file, slug = convert_notebook(nb, session_path)
        size_kb = round(out_file.stat().st_size / 1024, 1)
        description = get_notebook_description(nb)
        session_meta.append(
            {
                "type": "notebook",
                "slug": slug,
                "title": titleize(nb.name),
                "filename": nb.name,
                "description": description,
                "url": f"/{session_path}/notebooks/{slug}/",
                "cells": get_cell_count(nb),
                "size_kb": size_kb,
                "language": "jupyter",
            }
        )

    # 2. Archivos de código (renderer universal con Pygments)
    for f in assets["code"]:
        ext = f.suffix.lower()
        slug = slugify(f.name)
        language = ASSET_EXTENSIONS.get(ext, "text")
        out_dir = PUBLIC_DIR / session_path / "files" / slug
        out_file = out_dir / "index.html"
        out_dir.mkdir(parents=True, exist_ok=True)

        _body, page = render_code_to_html(f, language, session_path)
        out_file.write_text(page, encoding="utf-8")

        size_kb = round(f.stat().st_size / 1024, 1)
        print(f"  ✓ {f.name} → {out_file.relative_to(SITE_DIR)} ({size_kb:.1f} KB)")
        session_meta.append(
            {
                "type": "file",
                "slug": slug,
                "title": titleize(f.name),
                "filename": f.name,
                "language": language,
                "lexer": language,
                "url": f"/{session_path}/files/{slug}/",
                "size_kb": size_kb,
                "extension": ext,
            }
        )

    # 3. Binarios (copia tal cual para descarga)
    for f in assets["binary"]:
        ext = f.suffix.lower()
        slug = slugify(f.name)
        out_dir = PUBLIC_DIR / session_path / "binaries"
        out_dir.mkdir(parents=True, exist_ok=True)
        dst = out_dir / f.name
        shutil.copy2(f, dst)
        size_kb = round(dst.stat().st_size / 1024, 1)
        print(f"  ✓ {f.name} → {dst.relative_to(SITE_DIR)} ({size_kb:.1f} KB)")
        session_meta.append(
            {
                "type": "binary",
                "slug": slug,
                "title": titleize(f.name),
                "filename": f.name,
                "url": f"/{session_path}/binaries/{f.name}",
                "size_kb": size_kb,
                "extension": ext,
            }
        )

    return session_meta


def main() -> int:
    print(f"🔧 Procesando assets del repo Learning")
    print(f"   REPO_ROOT = {REPO_ROOT}")
    print(f"   PUBLIC_DIR = {PUBLIC_DIR}")

    if not REPO_ROOT.exists():
        print(f"❌ REPO_ROOT no existe: {REPO_ROOT}")
        return 1

    total_assets = 0
    for session_path, repo_dir in iter_session_paths():
        session_meta = process_session(repo_dir, session_path)
        if session_meta:
            meta_file = PUBLIC_DIR / session_path / "_index.json"
            meta_file.parent.mkdir(parents=True, exist_ok=True)
            meta_file.write_text(
                json.dumps(session_meta, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            print(
                f"✅ {session_path}: {len(session_meta)} assets → {meta_file.relative_to(SITE_DIR)}"
            )
            total_assets += len(session_meta)
        else:
            print(f"ℹ️  {session_path}: sin assets")

    print(f"\n🎉 Total: {total_assets} assets procesados")
    return 0


if __name__ == "__main__":
    sys.exit(main())
