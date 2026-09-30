#!/usr/bin/env python3
"""
Regenera el hash CSP de los <script> inline de index.html.

  python scripts/csp_hashes.py

Si editas un bloque inline (el classList('js') o cualquier JSON-LD),
vuelve a ejecutar este script y pega la meta http-equiv CSP actualizada
en el <head> de index.html. Los hashes sha256 son sobre el contenido
EXACTO entre las etiquetas <script>...</script>.

Seguridad: solo calcula hashes; no lee ni escribe credenciales.
"""
import base64
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"


def main() -> int:
    h = HTML.read_text(encoding="utf-8")
    blocks = re.findall(r"<script(?![^>]*\ssrc=)[^>]*>(.*?)</script>", h, re.S)
    if not blocks:
        print("No hay scripts inline en index.html")
        return 1
    script_src = ["'self'"]
    for i, body in enumerate(blocks):
        dig = base64.b64encode(hashlib.sha256(body.encode("utf-8")).digest()).decode()
        preview = " ".join(body.strip().split())[:55]
        print(f"[{i}] 'sha256-{dig}'  <- {preview}")
        script_src.append(f"'sha256-{dig}'")
    print("\nscript-src (pega esto en la meta CSP):")
    print("script-src " + " ".join(script_src) + ";")
    return 0


if __name__ == "__main__":
    sys.exit(main())
