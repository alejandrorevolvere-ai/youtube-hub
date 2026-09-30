#!/usr/bin/env python3
"""
Regenera data.json (estadisticas + ultimos videos) y content/videos.json
(archivo acumulativo con descripcion/duracion/vistas por video).

  python scripts/fetch_channel_data.py

Fuentes:
  - RSS  https://www.youtube.com/feeds/videos.xml?channel_id=...  -> ultimos 6
  - YouTube Data API v3 (si YT_TOKEN_PICKLE apunta a un token OAuth valido):
      * estadisticas del canal (subs/videos/views)
      * hasta 50 videos del feed "uploads" con descripcion, tags, duracion y
        vistas -> backfill del archivo para las landing pages SEO

content/videos.json es el archivo historico: nunca se borran videos; el slug de
cada video se calcula una sola vez (estabilidad de URL). data.json solo lleva
los ultimos videos (con su slug) para el hub.

El token se lee SOLO de la variable de entorno YT_TOKEN_PICKLE; no viaja al
repo ni a data.json.
"""
import json
import os
import re
import sys
import time
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data.json"
ARCHIVE = ROOT / "content" / "videos.json"

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
TOKEN = Path(os.environ["YT_TOKEN_PICKLE"]) if os.environ.get("YT_TOKEN_PICKLE") else None

NS = {
    "a": "http://www.w3.org/2005/Atom",
    "yt": "http://www.youtube.com/xml/schemas/2015",
    "media": "http://search.yahoo.com/mrss/",
}


def slugify(title: str, vid: str, used: dict) -> str:
    """Slug estable a partir del titulo. Si choca con otro video, sufijo corto."""
    txt = unicodedata.normalize("NFKD", title or "")
    txt = txt.encode("ascii", "ignore").decode("ascii").lower()
    base = re.sub(r"[^a-z0-9]+", "-", txt).strip("-")[:70].rstrip("-")
    if not base:
        base = re.sub(r"[^a-z0-9]+", "", vid.lower()) or "video"
    slug = base
    owner = used.get(slug)
    if owner is not None and owner != vid:
        suffix = re.sub(r"[^a-z0-9]+", "", vid.lower())[:8]
        slug = f"{base}-{suffix}"
    used[slug] = vid
    return slug


def iso8601_to_seconds(value: str) -> int | None:
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", value or "")
    if not m:
        return None
    d, h, mn, s = (int(x) if x else 0 for x in m.groups())
    return ((d * 24 + h) * 60 + mn) * 60 + s


def yt_client():
    """Cliente de YouTube desde el token OAuth local (None si no hay token)."""
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
        return build("youtube", "v3", credentials=creds, cache_discovery=False)
    except Exception as e:
        print(f"  cliente YouTube fallo: {e}")
        return None


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
                desc_el = e.find("media:group/media:description", NS)
                stats_el = e.find("media:group/media:community/media:statistics", NS)
                videos.append({
                    "id": vid,
                    "title": title,
                    "published": published[:10],
                    "url": f"https://www.youtube.com/watch?v={vid}",
                    "thumb": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
                    "description": desc_el.text if desc_el is not None else None,
                    "views": int(stats_el.attrib["views"]) if stats_el is not None else None,
                })
            return videos
        except Exception as e:  # YouTube devuelve 500 intermitente
            last_err = e
            time.sleep(2)
    print(f"  RSS fallo ({channel_id}): {last_err}")
    return []


def fetch_uploads(yt, channel_id: str, limit: int = 50) -> list:
    """Backfill desde el feed uploads (descripcion, tags, duracion, vistas)."""
    try:
        uploads = "UU" + channel_id[2:]
        items, page = [], None
        while len(items) < limit:
            r = yt.playlistItems().list(
                part="contentDetails", playlistId=uploads,
                maxResults=min(50, limit - len(items)),
                pageToken=page or None,
            ).execute()
            items.extend(r.get("items", []))
            page = r.get("nextPageToken")
            if not page:
                break
        ids = [i["contentDetails"]["videoId"] for i in items]
        videos = []
        for i in range(0, len(ids), 50):
            batch = ids[i:i + 50]
            r = yt.videos().list(
                part="snippet,contentDetails,statistics", id=",".join(batch),
                maxResults=50,
            ).execute()
            for it in r.get("items", []):
                sn, cd, st = it["snippet"], it["contentDetails"], it.get("statistics", {})
                vid = it["id"]
                videos.append({
                    "id": vid,
                    "title": sn["title"],
                    "published": sn["publishedAt"][:10],
                    "url": f"https://www.youtube.com/watch?v={vid}",
                    "thumb": f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg",
                    "description": sn.get("description") or None,
                    "tags": sn.get("tags") or None,
                    "duration": iso8601_to_seconds(cd.get("duration", "")),
                    "views": int(st.get("viewCount", 0)) or None,
                })
        return videos
    except Exception as e:
        print(f"  uploads fallo ({channel_id}): {e}")
        return []


def fetch_stats(yt, channel_id: str) -> dict | None:
    """subs/videos/views via YouTube Data API v3 con el token local."""
    if yt is None:
        return None
    try:
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


def load_archive() -> dict:
    if ARCHIVE.exists():
        try:
            data = json.loads(ARCHIVE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
        except Exception:
            pass
    return {"generated_at": None, "videos": {}}


def save_archive(archive: dict) -> None:
    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    archive["generated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    ARCHIVE.write_text(
        json.dumps(archive, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def upsert_videos(archive_videos: dict, entries: list, ch_key: str) -> dict:
    """Inserta/actualiza en el archivo; el slug se conserva del primer alta."""
    used = {v.get("slug"): vid for vid, v in archive_videos.items() if v.get("slug")}
    for e in entries:
        vid = e["id"]
        prev = archive_videos.get(vid, {})
        slug = prev.get("slug") or slugify(e.get("title", ""), vid, used)
        merged = {**prev}
        for k, v in e.items():
            if v is not None:
                merged[k] = v
        merged["slug"] = slug
        merged["channel"] = ch_key
        merged.setdefault("url", f"https://www.youtube.com/watch?v={vid}")
        archive_videos[vid] = merged
    return archive_videos


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

    yt = yt_client()
    archive = load_archive()
    a_videos = archive.get("videos", {})

    for key, meta in CHANNELS.items():
        print(f"[{key}] {meta['name']}")

        # Feed completo (API) + RSS como fallback inmediato de "latest"
        uploads = fetch_uploads(yt, meta["id"]) if yt else []
        rss = fetch_rss(meta["id"])
        if not rss and not uploads and prev_stats.get(key):
            rss = prev_stats[key].get("latest", [])
            print("  sin feed: mantengo los videos previos")

        feed = uploads or rss
        # latest = ordenado por fecha, tope 6 (como el RSS)
        latest_src = sorted(feed, key=lambda v: v.get("published", ""), reverse=True)[:6]
        # latest en data.json siempre con slug del archivo
        a_videos = upsert_videos(a_videos, feed, key)
        latest = []
        for v in latest_src:
            item = {k: v[k] for k in ("id", "title", "published", "url", "thumb")
                    if k in v}
            item["slug"] = a_videos[v["id"]]["slug"]
            latest.append(item)

        print(f"  videos: {len(feed)} (latest {len(latest)})")

        old = prev_stats.get(key, {})
        stats = fetch_stats(yt, meta["id"])
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
            "latest": latest,
        }

    archive["videos"] = dict(
        sorted(a_videos.items(), key=lambda kv: kv[1].get("published", ""), reverse=True)
    )
    save_archive(archive)
    print(f"archivo: {len(archive['videos'])} videos -> {ARCHIVE}")

    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
