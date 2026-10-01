#!/usr/bin/env python3
"""
Fuente unica de la Content-Security-Policy del sitio.

  python scripts/csp_hashes.py

Que hace:
  1. Calcula los hashes sha256 de los <script> inline de index.html
     (el classList('js') y los bloques JSON-LD).
  2. Parchea la meta http-equiv="Content-Security-Policy" de index.html.
  3. Escribe _headers (Cloudflare Pages) con la MISMA CSP como header HTTP
     + cabeceras de seguridad (X-Frame-Options, nosniff, HSTS...).

Las landing pages (v/<slug>/index.html) importan policy() desde este modulo,
asi toda la web comparte la politica exacta. Tras tocar un script inline de
index.html vuelve a ejecutar este script.

Seguridad: solo calcula hashes; no lee ni escribe credenciales.
"""
import base64
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = ROOT / "index.html"
HEADERS = ROOT / "_headers"

# Origen del beacon de Cloudflare Web Analytics (sin cookies, privacy-friendly)
BEACON = "https://static.cloudflareanalytics.com"
# Reproductor embebido de las landing pages (facade click-to-play)
FRAME_SRC = "https://www.youtube-nocookie.com"

HEADERS_EXTRA = """\
  X-Frame-Options: DENY
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
  Strict-Transport-Security: max-age=31536000; includeSubDomains
  Cross-Origin-Opener-Policy: same-origin
  Cross-Origin-Resource-Policy: same-origin
"""


def inline_hashes(html_text: str) -> list:
    """Hashes sha256 (base64) de cada <script> inline sin src."""
    blocks = re.findall(r"<script(?![^>]*\ssrc=)[^>]*>(.*?)</script>", html_text, re.S)
    out = []
    for body in blocks:
        dig = base64.b64encode(hashlib.sha256(body.encode("utf-8")).digest()).decode()
        out.append("'sha256-" + dig + "'")
    return out


def policy(hashes: list) -> str:
    script_src = " ".join(["'self'"] + hashes + [BEACON])
    return (
        "default-src 'none'; "
        "base-uri 'none'; "
        "form-action 'none'; "
        "frame-ancestors 'none'; "
        "object-src 'none'; "
        f"script-src {script_src}; "
        "style-src 'self'; "
        "img-src 'self' data: https://i.ytimg.com; "
        "font-src 'self'; "
        f"connect-src 'self' {BEACON}; "
        f"frame-src {FRAME_SRC}; "
        "media-src 'none'; "
        "worker-src 'none'; "
        "manifest-src 'none'; "
        "upgrade-insecure-requests"
    )


def current_policy() -> str:
    """CSP vigente calculada desde index.html (para build_pages.py)."""
    return policy(inline_hashes(HTML.read_text(encoding="utf-8")))


def main() -> int:
    h = HTML.read_text(encoding="utf-8")
    hashes = inline_hashes(h)
    if not hashes:
        print("No hay scripts inline en index.html")
        return 1
    for i, hh in enumerate(hashes):
        print(f"[{i}] {hh}")

    pol = policy(hashes)

    # 1. Parchea la meta CSP de index.html
    meta_re = re.compile(
        r'(<meta http-equiv="Content-Security-Policy" content=")([^"]*)(")'
    )
    if not meta_re.search(h):
        print("ERROR: no se encontro la meta CSP en index.html")
        return 1
    new_h = meta_re.sub(lambda m: m.group(1) + pol + m.group(3), h, count=1)
    if new_h != h:
        HTML.write_text(new_h, encoding="utf-8")
        print("meta CSP actualizada en index.html")

    # 2. Escribe _headers (Cloudflare Pages)
    HEADERS.write_text(f"/*\n{HEADERS_EXTRA}  Content-Security-Policy: {pol}\n",
                       encoding="utf-8")
    print(f"_headers escrito ({HEADERS})")
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
