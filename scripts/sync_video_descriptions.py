"""Sincroniza el bloque CTA en las descripciones de los videos de YouTube.

El bloque (idempotente) anade al final de cada descripcion:
  - libro de la historia (solo canal club, si data/libros.json lo mapea)
  - enlace al hub con UTM medium=description
  - newsletter (Buttondown) y Ko-fi con UTM

Uso:
  python scripts/sync_video_descriptions.py                 # dry-run
  python scripts/sync_video_descriptions.py --apply         # aplica (lote por defecto 30)
  python scripts/sync_video_descriptions.py --apply --limit 0   # sin limite
  python scripts/scripts.py --apply --channel club          # solo un canal

La cuota de YouTube Data API: 50 unidades por videos.update y 1 por
videos.list (50 ids). Un lote de 30 = ~1.500 de 10.000 diarias.
"""

import argparse
import json
import pickle
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VINDEX = ROOT / "v-index.json"
LIBROS = ROOT / "data" / "libros.json"
TOKENS = {
    "club": Path(r"D:\WSL\youtube-automation\config\youtube_token.pickle"),
    "ia60": Path(r"D:\WSL\youtube-automation\config\youtube_token_ia.pickle"),
}
MARKERS = ("buttondown.com/revolvere", "utm_medium=description")
MAX_LEN = 5000
HUB = "https://senalabierta.pages.dev/v/{slug}/?utm_source=youtube&utm_medium=description&utm_campaign=senal_abierta"
NEWSLETTER = "https://buttondown.com/revolvere?utm_source=senalabierta&utm_medium=newsletter&utm_campaign=youtube"
KOFI = "https://ko-fi.com/alejandrorevolvere?utm_source=senalabierta&utm_medium=kofi&utm_campaign=youtube"
AMZ_DISCLOSURE = ("Como Afiliado de Amazon, percibo dinero con las compras "
                  "que cumplen los requisitos.")


def build_cta(ch: str, slug: str, book_url: str | None) -> str:
    lines = ["", "---", ""]
    if book_url:
        lines.append(f"Libro de esta historia: {book_url}")
        lines.append(AMZ_DISCLOSURE)
    lines.append(f"Todo el archivo (94 videos): {HUB.format(slug=slug)}")
    lines.append(f"Newsletter semanal: {NEWSLETTER}")
    lines.append(f"Invitame a un cafe: {KOFI}")
    return "\n".join(lines)


def load_creds(path: Path):
    with open(path, "rb") as f:
        creds = pickle.load(f)
    if getattr(creds, "expired", False) and getattr(creds, "refresh_token", None):
        from google.auth.transport.requests import Request
        creds.refresh(Request())
    return creds


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true", help="ejecuta los updates")
    ap.add_argument("--limit", type=int, default=None,
                    help="maximo de updates en este lote (defecto 30 con --apply, 0=todo)")
    ap.add_argument("--channel", choices=["club", "ia60"], default=None)
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    import googleapiclient.discovery

    idx = json.loads(VINDEX.read_text(encoding="utf-8"))
    if args.channel:
        idx = [v for v in idx if v["ch"] == args.channel]
    idx.sort(key=lambda v: v.get("pub", ""), reverse=True)

    books = {}
    if LIBROS.exists():
        books = json.loads(LIBROS.read_text(encoding="utf-8"))

    limit = args.limit if args.limit is not None else (30 if args.apply else 0)

    creds_by_ch = {ch: load_creds(p) for ch, p in TOKENS.items()
                   if any(v["ch"] == ch for v in idx)}
    yts = {ch: googleapiclient.discovery.build(
        "youtube", "v3", credentials=c, cache_discovery=False)
        for ch, c in creds_by_ch.items()}

    # 1) fetch de descripciones actuales (en lotes de 50 ids)
    current: dict[str, dict] = {}
    list_units = 0
    for ch in yts:
        ids = [v["id"] for v in idx if v["ch"] == ch]
        for i in range(0, len(ids), 50):
            batch = ids[i:i + 50]
            r = yts[ch].videos().list(part="snippet", id=",".join(batch)).execute()
            list_units += 1
            for item in r.get("items", []):
                current[item["id"]] = item["snippet"]

    n_update = n_skip = n_missing = n_toolong = 0
    update_units = 0
    for v in idx:
        vid, ch, slug = v["id"], v["ch"], v["slug"]
        snip = current.get(vid)
        if not snip:
            print(f"MISS {vid} ({ch}) no devuelto por la API")
            n_missing += 1
            continue
        desc = snip.get("description", "")
        if any(m in desc for m in MARKERS):
            n_skip += 1
            continue
        book = books.get(vid)
        book_url = None
        if book and ch == "club":
            book_url = book if isinstance(book, str) else book.get("url")
        new_desc = desc.rstrip() + "\n" + build_cta(ch, slug, book_url)
        if len(new_desc) > MAX_LEN:
            print(f"TOO-LONG {vid} ({len(new_desc)} chars), se omite")
            n_toolong += 1
            continue
        if not args.apply:
            print(f"DRY  {vid} ({ch}) {desc.strip()[:45]!r} -> +{len(new_desc)-len(desc)} chars")
            n_update += 1
            continue
        body = {
            "id": vid,
            "snippet": {
                "title": snip["title"],
                "description": new_desc,
                "categoryId": snip["categoryId"],
            },
        }
        for k in ("tags", "defaultLanguage", "defaultAudioLanguage"):
            if k in snip:
                body["snippet"][k] = snip[k]
        try:
            yts[ch].videos().update(part="snippet", body=body).execute()
        except Exception as e:
            print(f"ERR  {vid} ({ch}) {e}")
            continue
        update_units += 50
        n_update += 1
        print(f"OK   {vid} ({ch}) desc {len(desc)} -> {len(new_desc)} chars")
        time.sleep(0.15)
        if limit and n_update >= limit:
            print(f"(lote completo: {n_update} updates, --limit {limit})")
            break

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"\n[{mode}] updates={n_update} ya-con-CTA={n_skip} "
          f"missing={n_missing} demasiado-larga={n_toolong}")
    print(f"cuota estimada: list={list_units} update={update_units} "
          f"(total {list_units + update_units} / 10000 diarias)")
    if not args.apply and n_update:
        print("Siguiente: --apply --limit 30")
    return 0


if __name__ == "__main__":
    sys.exit(main())
