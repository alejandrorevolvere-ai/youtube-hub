#!/usr/bin/env python3
"""
Regenera data.json con datos reales de los dos canales de YouTube.

  python scripts/fetch_channel_data.py

Fuentes (sin gastar cuota si no hay token):
  - RSS  https://www.youtube.com/feeds/videos.xml?channel_id=...  -> últimos 6 vídeos
  - YouTube Data API v3 (si YT_TOKEN_PICKLE apunta a un token OAuth válido)
    -> subs/vídeos/views. El token se lee SOLO de esa variable de entorno;
    no viaja al repo ni a data.json.

Este script es la única fuente de verdad de las cifras que se muestran en la
web. No editar los números a mano en index.html: ahí van los mismos que ya
genera este script (JS los refresca desde data.json al cargar).
"""
import json
import os
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data.json"

# Guardado respecto a data.json que ya existe
STALE_STAT_DAYS = 30

CHANNELS = {
    "club": {
        "id": "UCKBRqrOcPPfwc_jxWesEItA",
        "name": "El Club del Negocio",
        "url": "https://www.youtube.com/channel/UCKBRqrOcPPfwc_jxWesEItA",
        "accent": "coral",
        "tags": ["negocios", "dinero", "historias"],
    },
    "ia60": {
        "id": "UC670GGGsL5Bl9bd5DCdTKAg",
        "name": 'IA en 60"',
        "url": "https://www.youtube.com/channel/UC670GGGsL5Bl9bd5DCdTKAg",
        "accent": "acid",
        "tags": ["ia", "herramientas", "ahorro-de-tiempo"],
    },
}

# Ruta del token OAuth de YouTube: SOLO por variable de entorno.
# Ejemplo (PowerShell):  $env:YT_TOKEN_PICKLE="<ruta local a tu token OAuth de YouTube>"
# Sin ella, las stats se conservan del data.json anterior (stats_source=cached).
# El token nunca se copia a este repo ni a data.json.
TOKEN = Path(os.environ["YT_TOKEN_PICKLE"]) if os.environ.get("YT_TOKEN_PICKLE") else None

NS = {
    "a": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


def fetch_rss(channel_id: str, limit: int = 6) -> list:
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    last_err = None
    for attempt in range(3):
        try:
            data = urllib.request.urlopen(url, timeout=25).read()
            root = ET.fromstring(data)
            videos = []
            for e in root.findall("a:entry", NS)[:limit]:
                vid = e.find("yt:videoId", NS).text
                title = e.find("a:title", NS).text
                published = e.find("a:published", NS).text
                videos.append({
                    "id": vid,
                    "title": title,
                    "published": published[:10],
                    "url": f"https://www.youtube.com/watch?v={vid}",
                    "thumb": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
                })
            return videos
        except Exception as e:  # YouTube devuelve 500 intermitente
            last_err = e
            time.sleep(2)
    print(f"  RSS fallo ({channel_id}): {last_err}")
    return []


def fetch_stats(channel_id: str) -> dict | None:
    """subs/videos/views via YouTube Data API v3 con el token local."""
    if TOKEN is None or not TOKEN.exists():
        return None
    try:
        import pickle
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        creds = pickle.load(open(TOKEN, "rb"))
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
            pickle.dump(creds, open(TOKEN, "wb"))
        yt = build("youtube", "v3", credentials=creds, cache_discovery=False)
        r = yt.channels().list(part="statistics", id=channel_id).execute()
        s = r["items"][0]["statistics"]
        return {
            "subscribers": int(s.get("subscriberCount", 0)),
            "videos": int(s.get("videoCount", 0)),
            "views": int(s.get("viewCount", 0)),
        }
    except Exception as e:
        print(f"  API stats fallo ({channel_id}): {e}")
        return None


def main() -> int:
    prev = {}
    if OUT.exists():
        try:
            prev = json.loads(OUT.read_text(encoding="utf-8"))
        except Exception:
            prev = {}

    prev_stats = prev.get("channels", {})
    data = {"generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "channels": {}}

    for key, meta in CHANNELS.items():
        print(f"[{key}] {meta['name']}")
        videos = fetch_rss(meta["id"])
        if not videos and prev_stats.get(key):
            videos = prev_stats[key].get("latest", [])
            print("  RSS vacio: mantengo los videos previos")
        print(f"  videos: {len(videos)}")

        old = prev_stats.get(key, {})
        stats = fetch_stats(meta["id"])
        source = "api"
        if stats is None:
            stats = {k: old.get(k, 0) for k in ("subscribers", "videos", "views")}
            source = "cached"  # sin token valido: se conservan los ultimos reales
        print(f"  subs={stats.get('subscribers')} videos={stats.get('videos')} "
              f"views={stats.get('views')} ({source})")

        data["channels"][key] = {
            **meta,
            **stats,
            "stats_source": source,
            "latest": videos,
        }

    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
