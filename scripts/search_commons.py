#!/usr/bin/env python3
"""Busca candidatas en Wikimedia Commons e imprime licencia (uso puntual)."""
import json
import sys
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
API = "https://commons.wikimedia.org/w/api.php"


def search(q, limit=8):
    params = {
        "action": "query", "format": "json", "generator": "search",
        "gsrsearch": q, "gsrnamespace": "6", "gsrlimit": str(limit),
        "prop": "imageinfo", "iiprop": "url|extmetadata|size",
        "iiurlwidth": "1400",
    }
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "senalabierta-build/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    pages = (data.get("query") or {}).get("pages") or {}
    out = []
    for p in pages.values():
        ii = (p.get("imageinfo") or [{}])[0]
        meta = ii.get("extmetadata") or {}
        lic = (meta.get("LicenseShortName") or {}).get("value", "?")
        out.append({
            "title": p.get("title"),
            "license": lic,
            "w": ii.get("width"), "h": ii.get("height"),
            "thumb": ii.get("thumburl"),
            "desc": ((meta.get("ImageDescription") or {}).get("value") or "")[:140],
        })
    return out


QUERIES = sys.argv[1:] or [
    "Ford assembly line 1913", "Wall Street Crash 1929 crowd",
    "ENIAC computer", "Alan Turing portrait",
    "Nixon gold window 1971", "Jeff Bezos 2003",
]
for q in QUERIES:
    print("=" * 20, q)
    try:
        for r in search(q):
            print(f"  {r['license']:<22} {r['w']}x{r['h']}  {r['title']}")
            if r["desc"]:
                print(f"      {r['desc']}")
    except Exception as e:
        print("  ERROR", e)
