#!/usr/bin/env python3
"""
IndexNow: notifica a los buscadores las URLs del sitemap tras cada deploy.

  python scripts/indexnow_ping.py            # todas las URLs de sitemap.xml
  python scripts/indexnow_ping.py <url> ...  # solo URLs concretas

La clave vive en un fichero <key>.txt de la raiz (publico por diseno:
https://senalabierta.pages.dev/<key>.txt). Este script SOLO la lee, nunca la
regenera. deploy.ps1 lo ejecuta siempre al final, ya con el deploy en vivo.
"""
import json
import sys
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
HOST = "senalabierta.pages.dev"
BASE = f"https://{HOST}"
ENDPOINT = "https://api.indexnow.org/indexnow"
RESERVED = {"robots.txt", "llms.txt"}
MAX_URLS = 10000


def key_file():
    cands = [p for p in ROOT.glob("*.txt") if p.name not in RESERVED]
    if len(cands) != 1:
        print(f"ERROR: se esperaba 1 fichero de clave (<key>.txt) en la raiz, "
              f"hay {len(cands)}: " + ", ".join(p.name for p in cands))
        return None, None
    p = cands[0]
    key = p.read_text(encoding="ascii").strip()
    if len(key) != 32 or any(c not in "0123456789abcdef" for c in key):
        print(f"ERROR: la clave de {p.name} no parece valida (32 hex)")
        return None, None
    return key, p


def sitemap_urls():
    tree = ET.parse(ROOT / "sitemap.xml")
    return [el.text for el in tree.getroot().iter()
            if el.tag.endswith("loc") and el.text]


def main() -> int:
    key, kf = key_file()
    if not key:
        return 1
    urls = (sys.argv[1:] or sitemap_urls())[:MAX_URLS]
    if not urls:
        print("ERROR: sin URLs que notificar")
        return 1
    payload = {
        "host": HOST,
        "key": key,
        "keyLocation": f"{BASE}/{kf.name}",
        "urlList": urls,
    }
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8",
                 "User-Agent": "senalabierta-deploy/1.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            code = r.status
    except urllib.error.HTTPError as e:
        print(f"IndexNow rechazo la peticion: HTTP {e.code} {e.reason}")
        print(e.read().decode("utf-8", "replace")[:500])
        return 1
    except urllib.error.URLError as e:
        print(f"IndexNow sin conexion: {e.reason}")
        return 1
    if code in (200, 202):
        print(f"IndexNow OK (HTTP {code}): {len(urls)} URLs notificadas")
        return 0
    print(f"IndexNow: respuesta inesperada HTTP {code}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
