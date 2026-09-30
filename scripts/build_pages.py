#!/usr/bin/env python3
"""
Genera las landing pages SEO por video (/v/<slug>/), sitemap.xml y llms.txt.

  python scripts/fetch_channel_data.py   # actualiza content/videos.json
  python scripts/build_pages.py          # genera paginas + sitemap + llms.txt

Entradas:
  - content/videos.json  archivo acumulativo (descripcion, duracion, vistas)
  - index.html           solo para la CSP (scripts/csp_hashes.py)

Salidas:
  - v/<slug>/index.html  una ficha por video: H1 con keyword, descripcion
                         limpia, facade de reproduccion (youtube-nocookie),
                         JSON-LD VideoObject, enlaces internos y CTA con UTM
  - sitemap.xml          home + todas las fichas
  - llms.txt             resumen + fichas recientes

No hay scripts inline en las fichas: la CSP se aplica tal cual (mismo policy
string que index.html). Ninguna URL se repite: el slug es estable.
"""
import html
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import csp_hashes  # noqa: E402
from fetch_channel_data import CHANNELS  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "content" / "videos.json"
SITEMAP = ROOT / "sitemap.xml"
LLMS = ROOT / "llms.txt"
VDIR = ROOT / "v"
BASE = "https://senalabierta.pages.dev"

TAG_CLASS = {"club": "vtag-club", "ia60": "vtag-ia"}
MESES = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN",
         "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]


def clean_description(desc: str) -> str:
    """Quita capitulos tipo '00:09 ...', hashtags sueltos y lineas solo-URL."""
    if not desc:
        return ""
    out = []
    for line in desc.splitlines():
        s = line.strip()
        if re.match(r"^\d{1,3}:\d{2}(\s|$)", s):
            continue
        if re.fullmatch(r"(#[\w\u00c0-\u024f]+[\s#]*)+", s):
            continue
        if re.fullmatch(r"https?://\S+", s):
            continue
        out.append(s)
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(text) > 1800:
        cut = text[:1800]
        text = cut[:cut.rfind(" ") if " " in cut else 1800].rstrip() + "…"
    return text


def meta_description(text: str, title: str) -> str:
    base = " ".join(text.split()) if text else title
    if len(base) > 155:
        base = base[:155]
        base = base[:base.rfind(" ")].rstrip() + "…"
    return base or title


def fmt_date(iso: str) -> str:
    try:
        d = datetime.strptime(iso, "%Y-%m-%d")
        return f"{d.day} {MESES[d.month - 1]} {d.year}"
    except ValueError:
        return iso


def fmt_dur(sec) -> str:
    if not isinstance(sec, int) or sec <= 0:
        return ""
    h, m, s = sec // 3600, (sec % 3600) // 60, sec % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def iso_dur(sec) -> str:
    if not isinstance(sec, int) or sec <= 0:
        return None
    h, m, s = sec // 3600, (sec % 3600) // 60, sec % 60
    parts = (f"{h}H" if h else "") + (f"{m}M" if m else "") + (f"{s}S" if s else "")
    return f"PT{parts}"


def fmt_views(n) -> str:
    if not isinstance(n, int) or n <= 0:
        return None
    return f"{n:,}".replace(",", ".")


def esc(s) -> str:
    return html.escape(str(s), quote=True)


def ld_json(obj) -> str:
    # evita cierre accidental del bloque si el texto contiene '</'
    return json.dumps(obj, ensure_ascii=False, indent=2).replace("</", "<\\/")


def video_page(v: dict, ch_key: str, ch_meta: dict, related: list, csp: str) -> str:
    vid, slug = v["id"], v["slug"]
    title = v.get("title", "")
    ch_name = ch_meta["name"]
    url = f"{BASE}/v/{slug}/"
    thumb = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
    body_text = clean_description(v.get("description", ""))
    desc = meta_description(body_text, title)
    dur = fmt_dur(v.get("duration"))
    views = fmt_views(v.get("views"))
    published = v.get("published", "")
    ch_url = ch_meta["url"] + "?utm_source=youtube_hub&utm_medium=link&utm_campaign=senal_abierta&utm_content=landing_ch"
    yt_url = (f"https://www.youtube.com/watch?v={vid}"
              "&utm_source=youtube_hub&utm_medium=link&utm_campaign=senal_abierta&utm_content=landing")

    ld_video = {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": title,
        "description": desc,
        "thumbnailUrl": [thumb],
        "uploadDate": published,
        "contentUrl": f"https://www.youtube.com/watch?v={vid}",
        "embedUrl": f"https://www.youtube-nocookie.com/embed/{vid}",
        "inLanguage": "es",
        "publisher": {"@type": "Organization", "name": "Señal Abierta",
                      "url": BASE + "/"},
    }
    if iso_dur(v.get("duration")):
        ld_video["duration"] = iso_dur(v["duration"])
    if isinstance(v.get("views"), int) and v["views"] > 0:
        ld_video["interactionStatistic"] = {
            "@type": "InteractionCounter",
            "interactionType": "https://schema.org/WatchAction",
            "userInteractionCount": v["views"],
        }

    ld_bread = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "BreadcrumbListItem", "position": 1, "name": "Inicio",
             "item": BASE + "/"},
            {"@type": "BreadcrumbListItem", "position": 2, "name": ch_name,
             "item": BASE + "/#canales"},
            {"@type": "BreadcrumbListItem", "position": 3, "name": title,
             "item": url},
        ],
    }

    paras = "".join(f"<p>{esc(p)}</p>" for p in body_text.split("\n\n") if p.strip())
    tags_line = ""
    tags = v.get("tags")
    if tags:
        tags_line = ('<p class="lp-tags">' +
                     esc(" · ".join(tags[:8])) + "</p>")

    meta_bits = [f'<time datetime="{esc(published)}">{fmt_date(published)}</time>']
    if dur:
        meta_bits.append(dur)
    if views:
        meta_bits.append(f"{views} reproducciones")

    rel_cards = []
    for r in related:
        r_id, r_slug = r["id"], r["slug"]
        r_title = esc(r.get("title", ""))
        rel_cards.append(f"""\
        <a class="vcard" href="../{esc(r_slug)}/">
          <span class="vthumb"><img src="https://i.ytimg.com/vi/{esc(r_id)}/hqdefault.jpg" alt="{r_title}" loading="lazy" /><span class="vtag {TAG_CLASS.get(ch_key, 'vtag-club')}">{esc(ch_name)}</span><span class="vplay">▶</span></span>
          <span class="vcard-body"><span class="vtitle">{r_title}</span><span class="vmeta"><span>{fmt_date(r.get('published', ''))}</span><span>Ver ficha →</span></span></span>
        </a>""")

    related_html = ""
    if rel_cards:
        related_html = f"""\
      <section class="lp-related">
        <div class="section-head"><div><p class="eyebrow">Sigue la señal</p><h2>Más de<br /><em>{esc(ch_name)}.</em></h2></div></div>
        <div class="vgrid lp-grid">
{chr(10).join(rel_cards)}
        </div>
      </section>"""

    return f"""\
<!doctype html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{esc(desc)}" />
  <meta name="theme-color" content="#11110f" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:type" content="video.other" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{thumb}" />
  <meta property="og:site_name" content="Señal Abierta" />
  <meta property="og:locale" content="es_ES" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{esc(title)}" />
  <meta name="twitter:description" content="{esc(desc)}" />
  <meta name="twitter:image" content="{thumb}" />
  <link rel="canonical" href="{url}" />
  <title>{esc(title)} · Señal Abierta</title>
  <link rel="icon" href="../../favicon.svg" type="image/svg+xml" />
  <meta name="referrer" content="strict-origin-when-cross-origin" />
  <meta http-equiv="Content-Security-Policy" content="{csp}" />
  <link rel="stylesheet" href="../../styles.css" />
  <script type="application/ld+json">
{ld_json(ld_video)}
  </script>
  <script type="application/ld+json">
{ld_json(ld_bread)}
  </script>
</head>
<body class="lp">
  <div class="grain" aria-hidden="true"></div>
  <header class="nav shell">
    <a class="brand" href="../../" aria-label="Señal Abierta, inicio"><span class="brand-mark">↗</span><span>SEÑAL<br /><b>ABIERTA</b></span></a>
    <nav aria-label="Navegación principal"><a href="../../#canales">Canales</a><a href="../../#senal">Últimas señales</a><a class="nav-cta" href="{yt_url}" target="_blank" rel="noopener noreferrer">YouTube <span>↗</span></a></nav>
  </header>

  <main class="lp-main shell">
    <nav class="lp-crumbs" aria-label="Migas de pan"><a href="../../">Inicio</a><b>✳</b><a href="../../#canales">{esc(ch_name)}</a><b>✳</b><span aria-current="page">{esc(title[:50])}{'…' if len(title) > 50 else ''}</span></nav>
    <article class="lp-article">
      <header class="lp-head">
        <p class="eyebrow">{esc(ch_name)}</p>
        <h1>{esc(title)}</h1>
        <p class="lp-meta">{'<b>✳</b>'.join(meta_bits)}</p>
      </header>

      <div class="lp-player" data-yt="{esc(vid)}" role="button" tabindex="0" aria-label="Reproducir: {esc(title)}">
        <img src="{thumb}" alt="{esc(title)}" />
        <span class="lp-play" aria-hidden="true">▶</span>
      </div>

      <div class="lp-cta">
        <a class="button button-accent" href="{yt_url}" target="_blank" rel="noopener noreferrer">Ver en YouTube <span>↗</span></a>
        <a class="text-link" href="{esc(ch_url)}" target="_blank" rel="noopener noreferrer">Abrir canal <span>↗</span></a>
        <a class="text-link" href="../../#senal">Más señales <span>↑</span></a>
      </div>

      {f'<section class="lp-body">{paras}</section>' if paras else ''}
      {tags_line}

      {related_html}
    </article>
  </main>
  <footer class="footer shell"><span>© 2026 SEÑAL ABIERTA</span><span>Ficha de vídeo <b>✳</b> datos de YouTube</span><span><a href="../../">Volver al hub ↑</a></span></footer>
  <script src="../../landing.js"></script>
</body>
</html>
"""


def build_sitemap(videos: list) -> None:
    today = datetime.now(timezone.utc).date().isoformat()
    rows = [f"""  <url>
    <loc>{BASE}/</loc>
    <lastmod>{today}</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>"""]
    for v in videos:
        rows.append(f"""  <url>
    <loc>{BASE}/v/{v['slug']}/</loc>
    <lastmod>{v.get('published') or today}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>""")
    SITEMAP.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows) + "\n</urlset>\n",
        encoding="utf-8",
    )


def build_llms(videos: list, channels: dict) -> None:
    lines = [
        "# Señal Abierta",
        "",
        "> Hub editorial que reúne dos canales de YouTube: negocio/dinero e",
        "> inteligencia artificial en vídeos breves.",
        "",
        "Señal Abierta es el sitio de presentación de dos canales operados por",
        "el mismo creador. Cada vídeo tiene ficha propia (resumen + enlace).",
        "",
        "## Canales",
        "",
    ]
    for key, ch in channels.items():
        lines.append(f"- {ch['name']}: {ch['url']} — {ch['videos']} vídeos, "
                     f"{ch['views']:,} reproducciones.".replace(",", "."))
    lines += [
        "",
        "## Sitio",
        "",
        f"- Inicio: {BASE}/",
        f"- Fichas de vídeo: {BASE}/v/<slug>/",
        f"- Datos en JSON: {BASE}/data.json",
        f"- Sitemap: {BASE}/sitemap.xml",
        "- Idioma: español",
        "",
        "## Vídeos recientes",
        "",
    ]
    for v in videos[:15]:
        ch = channels.get(v.get("channel"), {})
        name = ch.get("name", "")
        lines.append(f"- [{v['title']}]({BASE}/v/{v['slug']}/) — {name}, "
                     f"{v.get('published', '')}")
    LLMS.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if not ARCHIVE.exists():
        print("Falta content/videos.json: ejecuta fetch_channel_data.py")
        return 1
    archive = json.loads(ARCHIVE.read_text(encoding="utf-8"))
    videos = [v for v in archive.get("videos", {}).values()
              if v.get("slug") and v.get("id")]
    videos.sort(key=lambda v: v.get("published", ""), reverse=True)
    if not videos:
        print("Archivo vacio, nada que generar")
        return 1

    slugs = [v["slug"] for v in videos]
    if len(set(slugs)) != len(slugs):
        print("ERROR: slugs duplicados en el archivo")
        return 1

    csp = csp_hashes.current_policy()

    # Indice por canal (los relacionados salen del mismo canal)
    by_channel = {}
    for v in videos:
        by_channel.setdefault(v.get("channel"), []).append(v)

    written = 0
    for v in videos:
        ch_key = v.get("channel")
        ch_meta = CHANNELS.get(ch_key)
        if not ch_meta:
            continue
        related = [r for r in by_channel.get(ch_key, []) if r["id"] != v["id"]][:3]
        page = video_page(v, ch_key, ch_meta, related, csp)
        out_dir = VDIR / v["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(page, encoding="utf-8")
        written += 1

    # Limpia fichas de videos que ya no esten en el archivo
    known = set(slugs)
    removed = 0
    if VDIR.exists():
        for d in VDIR.iterdir():
            if d.is_dir() and d.name not in known:
                shutil.rmtree(d, ignore_errors=True)
                removed += 1

    data = json.loads((ROOT / "data.json").read_text(encoding="utf-8")) \
        if (ROOT / "data.json").exists() else {"channels": {}}
    build_sitemap(videos)
    build_llms(videos, data.get("channels", {}))

    print(f"OK: {written} fichas en v/, {removed} retiradas, "
          f"sitemap con {len(videos) + 1} URLs, llms.txt actualizado")
    return 0


if __name__ == "__main__":
    sys.exit(main())
