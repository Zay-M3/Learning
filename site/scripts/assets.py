#!/usr/bin/env python3
"""
Procesa todos los assets de las sesiones del repo Learning:
- Notebooks .ipynb → HTML estático self-contained (con outputs ejecutados)
- Archivos de código → HTML con syntax highlighting (Pygments)
- Archivos no-código (.txt, .json, .csv, etc.) → HTML con highlighting o texto plano
- Binarios (imágenes, etc.) → copia tal cual

Output por sesión en public/<session>/<asset-type>/<slug>/index.html
Output combinado: public/<session>/_index.json con metadata de todos los assets

Dependencias Python: nbformat, nbconvert, jupyter-client, ipykernel, pygments

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

# ──────────────────────────────────────────────────────────────────────────────
# Configuración: extensiones y sesiones
# ──────────────────────────────────────────────────────────────────────────────

# Código con highlighting especial (mapea extensión → lexer de Pygments)
ASSET_EXTENSIONS: dict[str, str] = {
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
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".h": "c",
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
    ".jsonc": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".toml": "toml",
    ".xml": "xml",
    # .md intencionalmente NO incluido: lo gestiona sync-content.mjs
    ".txt": "text",
    ".csv": "csv",
    ".tsv": "csv",
    ".ini": "ini",
    ".cfg": "ini",
    ".conf": "ini",
    ".lua": "lua",
    ".pl": "perl",
    ".swift": "swift",
    ".kt": "kotlin",
    ".r": "r",
    ".dart": "dart",
}

# Binarios que se copian tal cual para descarga
BINARY_EXTENSIONS: set[str] = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".ico",
    ".bmp",
    ".pdf",
    ".zip",
    ".tar",
    ".gz",
    ".tgz",
    ".rar",
    ".7z",
    ".mp3",
    ".mp4",
    ".wav",
    ".mov",
    ".avi",
    ".woff",
    ".woff2",
    ".ttf",
    ".eot",
}

SESSIONS = [
    "arquitectura-software",
    "agentes-ia",
    "algoritmia",
    "ingenieria-de-requisitos",
    "ingenieria-de-software",
]


# ──────────────────────────────────────────────────────────────────────────────
# Utilidades
# ──────────────────────────────────────────────────────────────────────────────


def slugify(name: str) -> str:
    """Convierte un nombre de archivo en un slug URL-safe.

    Ej: "ordenamiento.ipynb" → "ordenamiento"
        "quicshort.py" → "quickshort"  (corrige typo si lo hay, ver archivo)
        "mi_archivo.test.js" → "mi-archivo-test"
    """
    base = name.rsplit(".", 1)[0] if "." in name else name
    slug = base.replace("_", "-").replace(" ", "-").lower()
    # Colapsa guiones repetidos
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug or "asset"


def file_icon(ext: str) -> str:
    """Devuelve un emoji representativo según la extensión."""
    ext = ext.lower()
    icons = {
        ".py": "🐍",
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
        ".sql": "🗃️",
        ".html": "🌐",
        ".css": "🎨",
        ".json": "📋",
        ".yaml": "📋",
        ".yml": "📋",
        ".toml": "📋",
        ".xml": "📋",
        ".md": "📝",
        ".txt": "📄",
        ".csv": "📊",
        ".png": "🖼️",
        ".jpg": "🖼️",
        ".jpeg": "🖼️",
        ".gif": "🖼️",
        ".svg": "🖼️",
        ".webp": "🖼️",
        ".pdf": "📕",
        ".zip": "🗜️",
        ".tar": "🗜️",
        ".gz": "🗜️",
        ".ipynb": "📓",
    }
    return icons.get(ext, "📄")


def language_label(ext: str) -> str:
    """Etiqueta legible del lenguaje para mostrar en la UI."""
    ext = ext.lower()
    labels = {
        ".py": "Python",
        ".js": "JavaScript",
        ".mjs": "JavaScript",
        ".ts": "TypeScript",
        ".jsx": "JSX",
        ".tsx": "TSX",
        ".rs": "Rust",
        ".go": "Go",
        ".java": "Java",
        ".c": "C",
        ".cpp": "C++",
        ".rb": "Ruby",
        ".php": "PHP",
        ".sh": "Bash",
        ".bash": "Bash",
        ".sql": "SQL",
        ".html": "HTML",
        ".css": "CSS",
        ".scss": "SCSS",
        ".json": "JSON",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".toml": "TOML",
        ".xml": "XML",
        ".md": "Markdown",
        ".txt": "Texto",
        ".csv": "CSV",
    }
    return labels.get(ext, ext.lstrip(".").upper() or "Texto")


# ──────────────────────────────────────────────────────────────────────────────
# Descubrimiento de assets
# ──────────────────────────────────────────────────────────────────────────────


def find_assets(session_dir: Path) -> dict[str, list[Path]]:
    """Busca notebooks, archivos de código y binarios en una sesión.

    Ignora archivos dentro de directorios ocultos (``.git``, ``.venv``, etc.)
    y cualquier archivo ``.md`` (ya gestionados por sync-content.mjs).
    """
    assets: dict[str, list[Path]] = {"notebooks": [], "code": [], "binary": []}

    if not session_dir.exists():
        return assets

    for f in sorted(session_dir.rglob("*")):
        if not f.is_file():
            continue
        # Ignorar rutas ocultas o comunes a saltar
        parts = f.relative_to(session_dir).parts
        if any(p.startswith(".") for p in parts):
            continue
        if any(p in {"node_modules", "__pycache__", ".venv", "venv", "dist", "build"} for p in parts):
            continue

        suffix = f.suffix.lower()
        if suffix == ".ipynb":
            assets["notebooks"].append(f)
        elif suffix in BINARY_EXTENSIONS:
            assets["binary"].append(f)
        elif suffix in ASSET_EXTENSIONS:
            assets["code"].append(f)
        # .md y resto → ignorados (los gestiona sync-content)

    return assets


# ──────────────────────────────────────────────────────────────────────────────
# Renderizado de código con Pygments
# ──────────────────────────────────────────────────────────────────────────────


def render_code_to_html(filepath: Path, language: str) -> tuple[str, str]:
    """Renderiza un archivo de código a HTML con syntax highlighting (Pygments).

    Devuelve ``(lexer_name, html_completo)``.
    """
    from pygments import highlight
    from pygments.formatters import HtmlFormatter
    from pygments.lexers import get_lexer_by_name, guess_lexer
    from pygments.util import ClassNotFound

    try:
        code = filepath.read_text(encoding="utf-8", errors="replace")
    except Exception as e:
        print(f"  ⚠️  no se pudo leer {filepath}: {e}")
        code = ""

    # Intentar lexer por nombre → fallback a guess → fallback a texto plano
    lexer = None
    lexer_name = language
    try:
        lexer = get_lexer_by_name(language)
    except ClassNotFound:
        try:
            lexer = guess_lexer(code)
            lexer_name = lexer.name
        except ClassNotFound:
            lexer = get_lexer_by_name("text")
            lexer_name = lexer.name

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
    icon = file_icon(filepath.suffix)
    label_lang = language_label(filepath.suffix)

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
    h1 {{ font-size: 1.5rem; margin: 0 0 0.5rem; color: #18181b; word-break: break-all; }}
    .meta {{ color: #71717a; font-size: 0.875rem; margin-bottom: 1.5rem; }}
    .meta code {{ background: #f4f4f5; padding: 0.125rem 0.375rem; border-radius: 0.25rem; font-size: 0.8125rem; }}
    .icon {{ font-size: 1.5rem; vertical-align: middle; margin-right: 0.5rem; }}
  </style>
</head>
<body>
  <a href="../" class="back">← Volver</a>
  <h1><span class="icon">{icon}</span>{filepath.name}</h1>
  <p class="meta">
    Lenguaje: <code>{lexer_name}</code>
    · Tamaño: <code>{size_kb:.1f} KB</code>
    · Solo lectura
  </p>
  {body}
</body>
</html>"""
    return lexer_name, page


# ──────────────────────────────────────────────────────────────────────────────
# Conversión de notebooks
# ──────────────────────────────────────────────────────────────────────────────


def get_cell_count(nb_path: Path) -> int:
    """Cuenta el número de celdas de un notebook sin ejecutarlo."""
    try:
        with open(nb_path, encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
        return len(nb.cells)
    except Exception:
        return 0


def get_notebook_description(nb_path: Path) -> str:
    """Extrae la primera celda markdown como descripción corta."""
    try:
        with open(nb_path, encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
        for cell in nb.cells:
            if cell.cell_type == "markdown":
                return "".join(cell.source)[:200].strip()
    except Exception:
        pass
    return ""


def embed_external_resources(html: str) -> str:
    """Descarga CSS/JS de CDN y los embebe inline para HTML self-contained."""

    def fetch(url: str) -> str | None:
        try:
            print(f"    ↳ embebiendo {url[:80]}")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            print(f"    ⚠️  no se pudo descargar {url}: {e}")
            return None

    # Reemplazar <link href="..."> stylesheet
    def link_replace(match: re.Match) -> str:
        url = match.group(2)
        if not url.startswith(("http://", "https://")):
            return match.group(0)
        if "stylesheet" not in match.group(0):
            return match.group(0)
        content = fetch(url)
        if content is None:
            return match.group(0)
        if "css" in url.lower() or url.endswith(".css"):
            return f"<style>{content}</style>"
        return match.group(0)

    html = re.sub(
        r'<link([^>]*?)href=["\'](https?://[^"\']+)["\']',
        link_replace,
        html,
    )

    # Reemplazar <script src="...">
    def script_replace(match: re.Match) -> str:
        url = match.group(1)
        if not url.startswith(("http://", "https://")):
            return match.group(0)
        content = fetch(url)
        if content is None:
            return match.group(0)
        return f"<script>{content}</script>"

    html = re.sub(r'<script[^>]*?src=["\'](https?://[^"\']+)["\']', script_replace, html)
    html = re.sub(r"</script>\s*</script>", "</script>", html)
    return html


def convert_notebook(nb_path: Path, out_dir: Path) -> Path | None:
    """Convierte un .ipynb a HTML self-contained y lo escribe en ``out_dir/index.html``."""
    out_file = out_dir / "index.html"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Leer notebook
    try:
        with open(nb_path, encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
    except Exception as e:
        print(f"  ⚠️  no se pudo leer {nb_path}: {e}")
        return None

    # Intentar ejecutar para refrescar outputs; si falla, usar los embebidos
    try:
        ep = ExecutePreprocessor(timeout=60, kernel_name="python3")
        ep.preprocess(nb, {"metadata": {"path": str(nb_path.parent)}})
        print(f"  ✓ Ejecutado: {nb_path.name}")
    except Exception as e:
        print(f"  ⚠️  No se pudo ejecutar {nb_path.name}: {e}")
        print(f"     → usando outputs embebidos")

    # Exportar a HTML clásico self-contained
    try:
        exporter = HTMLExporter(
            template_name="classic",
            exclude_input_prompt=False,
            exclude_output_prompt=False,
            exclude_input=False,
            exclude_output=False,
        )
        body, _resources = exporter.from_notebook_node(nb)
        body = embed_external_resources(body)
    except Exception as e:
        print(f"  ⚠️  Error exportando {nb_path}: {e}")
        return None

    out_file.write_text(body, encoding="utf-8")
    size_kb = out_file.stat().st_size / 1024
    print(f"  ✓ {nb_path.name} → {out_file.relative_to(SITE_DIR)} ({size_kb:.1f} KB)")
    return out_file


# ──────────────────────────────────────────────────────────────────────────────
# Procesamiento principal
# ──────────────────────────────────────────────────────────────────────────────


def process_session(session: str) -> list[dict]:
    """Procesa todos los assets de una sesión. Devuelve la lista de metadatos."""
    session_dir = REPO_ROOT / session
    if not session_dir.exists():
        print(f"⏭️  {session}: directorio no existe ({session_dir})")
        return []

    print(f"\n📂 Procesando {session}/")
    assets = find_assets(session_dir)
    session_meta: list[dict] = []

    # 1) Notebooks
    for nb in assets["notebooks"]:
        slug = slugify(nb.name)
        out_dir = PUBLIC_DIR / session / "notebooks" / slug
        out_file = convert_notebook(nb, out_dir)
        if out_file:
            session_meta.append({
                "type": "notebook",
                "slug": slug,
                "title": nb.stem.replace("-", " ").replace("_", " ").title(),
                "filename": nb.name,
                "description": get_notebook_description(nb),
                "url": f"/{session}/notebooks/{slug}/",
                "cells": get_cell_count(nb),
                "size_kb": round(out_file.stat().st_size / 1024, 1),
                "language": "jupyter",
            })

    # 2) Archivos de código (cualquier extensión soportada)
    for f in assets["code"]:
        slug = slugify(f.name)
        language = ASSET_EXTENSIONS.get(f.suffix.lower(), "text")
        out_dir = PUBLIC_DIR / session / "files" / slug
        out_file = out_dir / "index.html"
        out_dir.mkdir(parents=True, exist_ok=True)
        lexer_name, page = render_code_to_html(f, language)
        out_file.write_text(page, encoding="utf-8")
        size_kb = f.stat().st_size / 1024
        print(f"  ✓ {f.name} → {out_file.relative_to(SITE_DIR)} ({size_kb:.1f} KB)")
        session_meta.append({
            "type": "file",
            "slug": slug,
            "title": f.stem.replace("-", " ").replace("_", " ").title(),
            "filename": f.name,
            "language": language_label(f.suffix),
            "lexer": lexer_name,
            "url": f"/{session}/files/{slug}/",
            "size_kb": round(size_kb, 1),
            "extension": f.suffix.lower(),
        })

    # 3) Binarios (copia tal cual)
    for f in assets["binary"]:
        slug = slugify(f.name)
        out_dir = PUBLIC_DIR / session / "binaries"
        out_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, out_dir / f.name)
        size_kb = f.stat().st_size / 1024
        print(f"  📦 {f.name} → {out_dir.relative_to(SITE_DIR)}/ ({size_kb:.1f} KB)")
        session_meta.append({
            "type": "binary",
            "slug": slug,
            "title": f.stem.replace("-", " ").replace("_", " ").title(),
            "filename": f.name,
            "url": f"/{session}/binaries/{f.name}",
            "size_kb": round(size_kb, 1),
            "extension": f.suffix.lower(),
        })

    return session_meta


def main() -> int:
    print(f"🚀 Procesando assets en {REPO_ROOT}")
    total_meta: dict[str, list[dict]] = {}

    for session in SESSIONS:
        meta = process_session(session)
        total_meta[session] = meta

        if meta:
            meta_file = PUBLIC_DIR / session / "_index.json"
            meta_file.write_text(
                json.dumps(meta, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
            counts = {
                t: sum(1 for m in meta if m["type"] == t)
                for t in ("notebook", "file", "binary")
            }
            print(
                f"✅ {session}: {counts['notebook']} notebooks + "
                f"{counts['file']} archivos + {counts['binary']} binarios "
                f"→ {meta_file.relative_to(SITE_DIR)}"
            )
        else:
            print("   (sin assets)")

    # Resumen global
    total_assets = sum(len(v) for v in total_meta.values())
    print(f"\n🏁 Total: {total_assets} assets procesados en {len(SESSIONS)} sesiones")
    return 0


if __name__ == "__main__":
    sys.exit(main())
