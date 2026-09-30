#!/usr/bin/env python3
"""Borrador semanal de la newsletter (Buttondown).

  python scripts/newsletter_draft.py            # escribe promo/digest-AAAA-WW.md
  python scripts/newsletter_draft.py --apply    # crea el borrador en Buttondown

Recoge los estrenos de los ultimos 7 dias (v-index.json), el libro de la
semana (data/libros.json) y arma el digest en Markdown.

API key: variable de entorno BUTTONDOWN_API_KEY o archivo .env en la raiz
(esta en .gitignore; nunca se commitea).
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VINDEX = ROOT / "v-index.json"
LIBROS = ROOT / "data" / "libros.json"
PROMO = ROOT / "promo"

BASE = "https://senalabierta.pages.dev"
HUB_U = (f"{BASE}/?utm_source=newsletter&utm_medium=newsletter"
         "&utm_campaign=senal_abierta")
LAND_U = (f"{BASE}/v/{{slug}}/?utm_source=newsletter&utm_medium=newsletter"
          "&utm_campaign=senal_abierta")
KOFI_U = ("https://ko-fi.com/alejandrorevolvere?utm_source=newsletter"
          "&utm_medium=kofi&utm_campaign=senal_abierta")
AMZ_U = ("https://www.amazon.es/dp/{asin}?tag=senalabierta-21"
         "&utm_source=newsletter&utm_medium=affiliate&utm_campaign=libros")
AMZ_DISC = ("Como Afiliado de Amazon, percibo dinero con las compras "
            "que cumplen los requisitos.")
CH = {"club": "El Club del Negocio", "ia60": "IA en 60 segundos"}
API = "https://api.buttondown.com/v1/emails"


def load_env() -> None:
    p = ROOT / ".env"
    if not p.exists():
        return
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, _, v = line.partition("=")
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def pick_book(books, vids_this_week):
    if not books:
        return None
    week_ids = {v["id"] for v in vids_this_week}
    for b in books:
        if set(b.get("videos", [])) & week_ids:
            return b
    # deterministico por semana ISO: mismo libro en toda la semana
    return books[date.today().isocalendar()[1] % len(books)]


def render(videos, books, hoy):
    desde = hoy - timedelta(days=7)
    nuevos = [v for v in videos if v.get("pub", "") >= desde.isoformat()]
    nuevos.sort(key=lambda v: v["pub"], reverse=True)
    if nuevos:
        intro = (f"Estrenos del {desde.strftime('%d/%m')} al "
                 f"{hoy.strftime('%d/%m')}:")
        subject = (f"Señal Abierta · {len(nuevos)} estrenos esta semana "
                   f"({hoy.strftime('%d/%m')})")
    else:
        nuevos = sorted(videos, key=lambda v: v["pub"], reverse=True)[:3]
        intro = "Sin estrenos esta semana; te dejo lo más reciente del archivo:"
        subject = f"Señal Abierta · lo más reciente ({hoy.strftime('%d/%m')})"

    lines = [f"# Señal Abierta — {intro}", ""]
    for v in nuevos:
        url = LAND_U.format(slug=v["slug"])
        lines.append(f"- **[{v['title']}]({url})** — {CH.get(v['ch'], v['ch'])}"
                     f" · {v['pub']}")
    lines += ["", "## Libro de la semana", ""]
    b = pick_book(books, [v for v in nuevos])
    if b:
        lines += [f"[**{b['title']}**]({AMZ_U.format(asin=b['asin'])}) — "
                  f"la historia de {b['empresa']} que aparece en el hub.",
                  "", AMZ_DISC]
    else:
        lines += ["(esta semana sin libro destacado)"]
    lines += ["", "## El hub", "",
              f"- [Archivo completo (94 vídeos y contando)]({HUB_U})",
              f"- [Apóyanos con un café ☕]({KOFI_U})",
              "", "---",
              "", "[Ver en el navegador](%s)" % HUB_U]
    return subject, "\n".join(lines)


def post_draft(subject: str, body: str) -> int:
    key = os.environ.get("BUTTONDOWN_API_KEY")
    if not key:
        print("Falta BUTTONDOWN_API_KEY (entorno o .env en la raiz)")
        return 1
    req = urllib.request.Request(
        API,
        data=json.dumps({"subject": subject, "body": body,
                         "status": "draft"}).encode("utf-8"),
        headers={"Authorization": f"Token {key}",
                 "Content-Type": "application/json",
                 "X-API-Version": "2026-04-01"},
        method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:500]}")
        return 1
    except urllib.error.URLError as e:
        print(f"Error de red: {e.reason}")
        return 1
    print(f"OK borrador creado: {data.get('url') or data.get('id')} "
          f"(status={data.get('status')})")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="crea el borrador en Buttondown")
    args = ap.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    videos = json.loads(VINDEX.read_text(encoding="utf-8"))
    books = json.loads(LIBROS.read_text(encoding="utf-8")).get("books", [])
    hoy = date.today()

    subject, body = render(videos, books, hoy)

    if not args.apply:
        PROMO.mkdir(exist_ok=True)
        iso = hoy.isocalendar()
        out = PROMO / f"digest-{iso.year}-W{iso.week:02d}.md"
        out.write_text(f"Asunto: {subject}\n\n{body}\n", encoding="utf-8")
        print(f"DRY: {out}")
        print(f"Asunto: {subject}")
        print(f"Cuerpo: {len(body)} chars, "
              f"{body.count(chr(10) + '- **[')} videos listados")
        print("Siguiente: BUTTONDOWN_API_KEY en .env y --apply")
        return 0

    load_env()
    return post_draft(subject, body)


if __name__ == "__main__":
    sys.exit(main())
