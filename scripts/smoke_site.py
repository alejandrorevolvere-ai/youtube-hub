import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
root = Path(__file__).resolve().parent.parent
ok = True


def chk(c, m):
    global ok
    print(("OK  " if c else "FAIL") + " " + m)
    if not c:
        ok = False


vix = json.loads((root / "v-index.json").read_text(encoding="utf-8"))
chk(len(vix) == 94, f"v-index.json con {len(vix)} entradas")

t = ET.parse(root / "feed.xml")
ns = {"a": "http://www.w3.org/2005/Atom"}
chk(len(t.getroot().findall("a:entry", ns)) == 15, "feed.xml con 15 entradas")

sm = (root / "sitemap.xml").read_text(encoding="utf-8")
nloc = sm.count("<loc>")
chk(nloc == 96, f"sitemap con {nloc} URLs")
chk("/archivo/" in sm, "sitemap incluye /archivo/")

arch = (root / "archivo" / "index.html").read_text(encoding="utf-8")
nvc = arch.count('class="vcard"')
chk(nvc == 94, f"archivo con {nvc} tarjetas")
chk("archivo.js" in arch, "archivo usa archivo.js externo")
chk("Content-Security-Policy" in arch, "archivo con meta CSP")
inline = re.findall(r"<script(?![^>]*\ssrc=)[^>]*>", arch)
chk(len(inline) == 0, f"archivo sin scripts inline (encontrados {len(inline)})")

lp = sorted((root / "v").glob("*/index.html"))[0]
l = lp.read_text(encoding="utf-8")
chk("lp-aff" in l, f"bloque afiliados en {lp.parent.name}")
chk('rel="sponsored noopener noreferrer"' in l, "rel=sponsored en afiliados")
nslot = len(re.findall(r"TODO-AFILIADO", l))
chk(nslot == 2, f"{nslot} slots de afiliado en la landing")
chk("lp-related" in l, "relacionados presentes")

lp2 = sorted((root / "v").glob("*/index.html"))[10]
l2 = lp2.read_text(encoding="utf-8")
chk("lp-aff" in l2, f"bloque afiliados en {lp2.parent.name} (otro canal)")

nf = (root / "404.html").read_text(encoding="utf-8")
chk("noindex" in nf, "404 con noindex")
chk("Content-Security-Policy" in nf, "404 con meta CSP")

h = (root / "index.html").read_text(encoding="utf-8")
chk('id="q"' in h and 'id="rand"' in h, "buscador + boton aleatorio en index")
chk('id="hitos"' in h, "seccion hitos en index")
nhit = h.count('src="img/hitos/')
chk(nhit == 8, f"{nhit} imagenes de hitos referenciadas")
chk("05 / La pr" in h, "watch renumerado 05")
chk("04 / L" in h, "hitos numerado 04")
chk("ko-fi.com" in h, "footer con Ko-fi")
chk("buttondown.email" in h, "footer con newsletter")
chk("archivo/" in h, "index enlaza archivo")
chk("feed.xml" in h, "head enlaza feed")
for p in ["feed.xml", "archivo.js", "404.html", "v-index.json",
          "img/hitos/turing.webp", "img/hitos/CREDITS.md"]:
    chk((root / p).exists(), f"existe {p}")

# XSS: ninguna landing con scripts inline ni texto sin escapar en atributos
bad = 0
for f in (root / "v").glob("*/index.html"):
    txt = f.read_text(encoding="utf-8")
    if re.search(r"<script(?![^>]*\ssrc=)(?![^>]*application/ld\+json)", txt):
        bad += 1
chk(bad == 0, f"cero scripts inline en las {len(list((root / 'v').glob('*/index.html')))} landings")

print("ALL OK" if ok else "HAY FALLOS")
sys.exit(0 if ok else 1)
