#!/usr/bin/env python3
"""
Convierte notebooks .ipynb a HTML estático self-contained y los deja
en site/public/algoritmia/notebooks/<nombre>/index.html

Cada notebook queda accesible en /algoritmia/notebooks/<nombre>/

Uso:
    python3 scripts/nbconvert.py
    LEARNING_REPO_ROOT=/repo-sessions python3 scripts/nbconvert.py   (en Docker)
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor


HERE = Path(__file__).resolve().parent
SITE_DIR = HERE.parent

# Raíz del repo: puede venir por env (Docker) o se infiere desde SITE_DIR
REPO_ROOT = Path(os.environ.get("LEARNING_REPO_ROOT") or SITE_DIR.parent)
NOTEBOOKS_SRC = REPO_ROOT / "algoritmia"
OUTPUT_DIR = SITE_DIR / "public" / "algoritmia" / "notebooks"


def find_assets() -> dict[str, list[Path]]:
    """Busca notebooks y scripts .py en algoritmia/."""
    if not NOTEBOOKS_SRC.exists():
        print(f"⚠️  {NOTEBOOKS_SRC} no existe")
        return {"notebooks": [], "scripts": []}
    return {
        "notebooks": sorted(NOTEBOOKS_SRC.glob("*.ipynb")),
        "scripts": sorted(NOTEBOOKS_SRC.glob("*.py")),
    }


def slugify(name: str) -> str:
    return name.replace(".ipynb", "").replace("_", "-").lower()


def convert_one(nb_path: Path) -> Path | None:
    """Convierte un notebook a HTML self-contained."""
    slug = slugify(nb_path.name)
    out_dir = OUTPUT_DIR / slug
    out_file = out_dir / "index.html"

    out_dir.mkdir(parents=True, exist_ok=True)

    # Leer notebook
    with open(nb_path, encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    # Intentar ejecutar el notebook (para que los outputs estén actualizados).
    # Si falla (ej: dependencias faltantes), seguimos con los outputs que ya estén guardados.
    try:
        ep = ExecutePreprocessor(timeout=60, kernel_name="python3")
        ep.preprocess(nb, {"metadata": {"path": str(nb_path.parent)}})
        print(f"  ✓ Ejecutado: {nb_path.name}")
    except Exception as e:
        print(f"  ⚠️  No se pudo ejecutar {nb_path.name}: {e}")
        print(f"     → usando outputs embebidos")

    # Exportar a HTML con template clásico (self-contained)
    exporter = HTMLExporter(
        template_name="classic",
        exclude_input_prompt=False,
        exclude_output_prompt=False,
        exclude_input=False,
        exclude_output=False,
    )
    body, resources = exporter.from_notebook_node(nb)

    # Self-contained: inline CSS/JS/images (sin CDN)
    # El exporter "classic" embebe recursos locales automáticamente si
    # el notebook los tiene. Para CDN externos (cdnjs) los descargamos.
    body = embed_external_resources(body)

    # Escribir
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(body)

    size_kb = out_file.stat().st_size / 1024
    print(f"  ✓ {nb_path.name} → {out_file.relative_to(SITE_DIR)} ({size_kb:.1f} KB)")
    return out_file


def embed_external_resources(html: str) -> str:
    """
    Descarga CSS/JS de CDN y los embebe inline para que el HTML sea
    realmente self-contained (sin dependencias de red).
    """
    import re
    import urllib.request

    # Buscar <link href="..."> y <script src="...">
    def fetch_and_replace(match):
        kind = match.group(1)  # "link" o "script"
        attr = match.group(2)
        url = match.group(3)

        if not url.startswith(("http://", "https://")):
            return match.group(0)

        try:
            print(f"    ↳ embebiendo {url[:80]}")
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as resp:
                content = resp.read().decode("utf-8", errors="replace")
        except Exception as e:
            print(f"    ⚠️  no se pudo descargar {url}: {e}")
            return match.group(0)

        # Determinar tipo de recurso
        if kind == "link":
            # Si es CSS
            if "css" in url.lower() or url.endswith(".css"):
                return f"<style>{content}</style>"
            # Si es otro tipo de link, lo dejamos como está
            return match.group(0)
        else:  # script
            return f"<script>{content}</script>"

    # Reemplazar links CSS
    html = re.sub(
        r'<link([^>]*?)href=["\'](https?://[^"\']+)["\']',
        lambda m: fetch_and_replace(
            type("M", (), {"group": lambda self, i: ["link", "href", m.group(2)][i - 1]})()
        ) if "stylesheet" in m.group(0) else m.group(0),
        html,
    )

    # Reemplazar scripts src
    def script_replace(match):
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

    html = re.sub(r'<script[^>]*?src=["\'](https?://[^"\']+)["\']', script_replace, html)
    # Limpiar tags de cierre asociados
    html = re.sub(r'</script>\s*</script>', '</script>', html)

    return html


def main():
    print(f"📓 Procesando assets en {NOTEBOOKS_SRC}")
    assets = find_assets()
    notebooks = assets["notebooks"]
    scripts = assets["scripts"]

    if not notebooks and not scripts:
        print("  (ninguno encontrado)")
        return 0

    # 1. Convertir notebooks a HTML self-contained
    converted = []
    for nb in notebooks:
        out = convert_one(nb)
        if out:
            converted.append(out)

    # 2. Copiar scripts .py como archivos descargables
    scripts_dir = OUTPUT_DIR / "scripts"
    scripts_dir.mkdir(parents=True, exist_ok=True)
    script_meta = []
    for py in scripts:
        dst = scripts_dir / py.name
        shutil.copy2(py, dst)
        size_kb = dst.stat().st_size / 1024
        print(f"  ✓ {py.name} → {dst.relative_to(SITE_DIR)} ({size_kb:.1f} KB)")
        script_meta.append({
            "filename": py.name,
            "url": f"/algoritmia/notebooks/scripts/{py.name}",
            "size_kb": round(size_kb, 1),
        })

    # 3. Crear índice JSON combinado
    import json
    meta = []
    for nb_path in notebooks:
        slug = slugify(nb_path.name)
        with open(nb_path, encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)

        description = ""
        for cell in nb.cells:
            if cell.cell_type == "markdown":
                description = "".join(cell.source)[:200].strip()
                break

        meta.append({
            "type": "notebook",
            "slug": slug,
            "title": slug.replace("-", " ").title(),
            "filename": nb_path.name,
            "description": description,
            "url": f"/algoritmia/notebooks/{slug}/",
            "cells": len(nb.cells),
        })

    for s in script_meta:
        meta.append({
            "type": "script",
            "title": s["filename"],
            "filename": s["filename"],
            "url": s["url"],
            "size_kb": s["size_kb"],
        })

    meta_file = OUTPUT_DIR / "_index.json"
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"\n✅ {len(converted)} notebooks + {len(script_meta)} scripts → {OUTPUT_DIR}")
    print(f"   Índice: {meta_file.relative_to(SITE_DIR)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())