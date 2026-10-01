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
chk(len(vix) == 98, f"v-index.json con {len(vix)} entradas")

t = ET.parse(root / "feed.xml")
ns = {"a": "http://www.w3.org/2005/Atom"}
chk(len(t.getroot().findall("a:entry", ns)) == 15, "feed.xml con 15 entradas")

sm = (root / "sitemap.xml").read_text(encoding="utf-8")
nloc = sm.count("<loc>")
chk(nloc == 102, f"sitemap con {nloc} URLs")
chk("/archivo/" in sm, "sitemap incluye /archivo/")
chk("/libros/" in sm, "sitemap incluye /libros/")
chk("/legal/" in sm, "sitemap incluye /legal/")

arch = (root / "archivo" / "index.html").read_text(encoding="utf-8")
nvc = arch.count('class="vcard"')
chk(nvc == 98, f"archivo con {nvc} tarjetas")
chk("archivo.js" in arch, "archivo usa archivo.js externo")
chk("Content-Security-Policy" in arch, "archivo con meta CSP")
inline = re.findall(r"<script(?![^>]*\ssrc=)[^>]*>", arch)
chk(len(inline) == 0, f"archivo sin scripts inline (encontrados {len(inline)})")

lp = sorted((root / "v").glob("*/index.html"))[0]
l = lp.read_text(encoding="utf-8")
chk("lp-aff" in l, f"bloque afiliados en {lp.parent.name}")
chk('rel="sponsored noopener noreferrer"' in l, "rel=sponsored en afiliados")
chk("lp-related" in l, "relacionados presentes")

# libro especifico por video (mapeo de data/libros.json)
net = (root / "v" / "netflix-el-error-que-lo-hizo-millonario" /
       "index.html").read_text(encoding="utf-8")
chk("1984881884" in net and "tag=senalabierta-21" in net,
    "landing Netflix enlaza su libro (ASIN + tag)")
chk("Libro de este v" in net, "blurb del libro en la landing")
nin = (root / "v" / "nintendo-de-cartas-de-poker-a-50-mil-millones" /
       "index.html").read_text(encoding="utf-8")
chk("amazon.es/s?k=" in nin, "landing sin libro mantiene la busqueda generica")

# tag de Amazon en todas las landings de negocio; slots IA siguen pendientes
files = [(f, f.read_text(encoding="utf-8"))
         for f in (root / "v").glob("*/index.html")]
n_amz = sum(1 for _, t in files if "senalabierta-21" in t)
n_quipu = sum(1 for _, t in files if "TODO-AFILIADO:quipu" in t)
n_ia = sum(1 for _, t in files if "TODO-AFILIADO:elevenlabs" in t)
chk(n_amz == n_quipu and n_amz > 0,
    f"Amazon tag (senalabierta-21) en {n_amz} landings club == quipu {n_quipu}")
chk(n_ia > 0, f"{n_ia} landings IA con slots de afiliado pendientes")

# divulgacion de Amazon obligatoria en toda landing con enlace de Amazon
disc = sum(1 for _, t in files if "Afiliado de Amazon" in t)
chk(disc == n_amz,
    f"divulgacion de Amazon en {disc} landings == {n_amz} con enlace Amazon")

# beacon del contador propio (/api/stats) en todas las paginas con JS
n_beacon = sum(1 for _, t in files if "count.js" in t)
chk(n_beacon == len(files),
    f"count.js en {n_beacon}/{len(files)} landings")

# tienda Ko-fi visible en todas las landings
n_shop = sum(1 for _, t in files if "ko-fi.com/s/c7fd921388" in t)
chk(n_shop == len(files),
    f"tienda Ko-fi en {n_shop}/{len(files)} landings")
chk("ko-fi.com/s/c7fd921388" in arch, "archivo enlaza tienda Ko-fi")

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
chk("ko-fi.com/alejandrorevolvere" in h, "footer con Ko-fi")
chk("ko-fi.com/s/c7fd921388" in h, "footer del hub enlaza tienda")
chk("buttondown.com/revolvere" in h, "footer con newsletter")
chk("archivo/" in h, "index enlaza archivo")
chk("libros/" in h, "index enlaza libros")
chk("legal/" in h, "index enlaza /legal/")
chk("feed.xml" in h, "head enlaza feed")
lib = (root / "libros" / "index.html").read_text(encoding="utf-8")
chk(lib.count('class="book"') == 11, "libros con 11 fichas")
chk("tag=senalabierta-21" in lib and "1984881884" in lib,
    "libros con links ASIN + tag")
chk("Afiliado de Amazon" in lib, "divulgacion de Amazon en libros")
for p in ["feed.xml", "archivo.js", "404.html", "v-index.json",
          "libros/index.html", "img/hitos/turing.webp",
          "img/hitos/CREDITS.md", "legal/index.html", "deploy.ps1",
          "scripts/indexnow_ping.py", "count.js",
          "functions/api/stats.js", "wrangler.jsonc"]:
    chk((root / p).exists(), f"existe {p}")

# beacon del contador en el hub, archivo y libros
chk('src="count.js"' in h, "index usa count.js")
chk("count.js" in arch, "archivo usa count.js")
chk("count.js" in lib, "libros usa count.js")

# pagina legal (LSSI) y clave IndexNow
lg = (root / "legal" / "index.html").read_text(encoding="utf-8")
chk("Content-Security-Policy" in lg, "legal con meta CSP")
chk("LSSI" in lg, "legal cita la LSSI-CE")
chk("Afiliado de Amazon" in lg, "divulgacion de Amazon en /legal/")
chk("[PENDIENTE" in lg, "legal con placeholders del titular marcados")
chk("count.js" in lg, "legal usa count.js")
chk("legal/" in arch, "archivo enlaza /legal/")
kfs = [p.name for p in root.glob("*.txt")
       if p.name not in ("robots.txt", "llms.txt")]
chk(len(kfs) == 1,
    f"clave IndexNow en la raiz ({kfs[0] if kfs else 'AUSENTE'})")
if kfs:
    chk((root / kfs[0]).read_text(encoding="ascii").strip() ==
        kfs[0][:-4], "fichero de clave IndexNow contiene su clave")

# XSS: ninguna landing con scripts inline ni texto sin escapar en atributos
bad = 0
no_news = 0
for f in (root / "v").glob("*/index.html"):
    txt = f.read_text(encoding="utf-8")
    if re.search(r"<script(?![^>]*\ssrc=)(?![^>]*application/ld\+json)", txt):
        bad += 1
    if "buttondown.com/revolvere" not in txt:
        no_news += 1
chk(bad == 0, f"cero scripts inline en las {len(list((root / 'v').glob('*/index.html')))} landings")
chk(no_news == 0, "newsletter en el pie de las 98 landings")
chk("Suscribirme a la newsletter" in h, "CTA newsletter en el hub")

print("ALL OK" if ok else "HAY FALLOS")
sys.exit(0 if ok else 1)
