#!/usr/bin/env python3
"""
Empaqueta el sitio publico en dist/ (lo unico que sube Cloudflare Pages).

  python scripts/package_site.py
  npx wrangler pages deploy dist --project-name senalabierta --branch=main

wrangler pages deploy NO respeta .cfignore/.assetsignore, asi que el filtro
se hace aqui: solo se copian los archivos que deben ser publicos.
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

FILES = [
    "index.html",
    "styles.css",
    "app.js",
    "landing.js",
    "data.json",
    "favicon.svg",
    "og.png",
    "sitemap.xml",
    "robots.txt",
    "llms.txt",
    "_headers",
]
DIRS = ["fonts", "v"]


def main() -> int:
    if DIST.exists():
        shutil.rmtree(DIST)
    DIST.mkdir()

    missing = []
    for name in FILES:
        src = ROOT / name
        if not src.exists():
            missing.append(name)
            continue
        shutil.copy2(src, DIST / name)
    for name in DIRS:
        src = ROOT / name
        if not src.is_dir():
            missing.append(name + "/")
            continue
        shutil.copytree(src, DIST / name)

    if missing:
        print("FALTAN (no copiados):", ", ".join(missing))
        return 1

    n = sum(1 for _ in DIST.rglob("*") if _.is_file())
    print(f"OK: dist/ con {n} archivos listos para desplegar")
    return 0


if __name__ == "__main__":
    sys.exit(main())
