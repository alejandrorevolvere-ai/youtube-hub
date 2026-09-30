#!/usr/bin/env python3
"""
Descarga las imágenes de la sección Hitos desde Wikimedia Commons,
verifica que la licencia sea dominio publico o CC0 y las convierte a
duotone (ink/paper) en img/hitos/*.webp.

  python scripts/fetch_hitos.py

Tambien escribe img/hitos/CREDITS.md con la fuente y licencia de cada
archivo. No se hotlinkea contenido externo: todo queda self-hosted para
cumplir img-src 'self' de la CSP.
"""
import io
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageEnhance

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "img" / "hitos"
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "senalabierta-build/1.0 (pagina de hitos)"}

INK = (0x11, 0x11, 0x0F)
PAPER = (0xE9, 0xE6, 0xDC)
ASPECT = 14 / 9
OUT_W = 760

# name: nombre de salida (sin .webp)
# file: titulo exacto del archivo en Commons
# focal: "top" para retratos (recorta desde arriba), "center" para apaisadas
# alt: texto alternativo descriptivo de la IMAGEN (no del hito)
MANIFEST = [
    {
        "name": "ford-linea-montaje",
        "file": "File:Ford assembly line - 1913 (restored).jpg",
        "focal": "center",
        "alt": "Obreros trabajando en la línea de montaje de Ford, 1913",
        "milestone": "1913 - Ford y la línea de montaje",
    },
    {
        "name": "crac-1929",
        "file": "File:Crowds gathering outside New York Stock Exchange.jpg",
        "focal": "center",
        "alt": "Multitud frente a la Bolsa de Nueva York en octubre de 1929",
        "milestone": "1929 - El crac del 29",
    },
    {
        "name": "eniac",
        "file": ("File:Glen Beck and Betty Snyder program the ENIAC in "
                 "building 328 at the Ballistic Research Laboratory.jpg"),
        "focal": "top",
        "alt": "Glen Beck y Betty Snyder programan la computadora ENIAC",
        "milestone": "1946 - ENIAC, la primera computadora",
    },
    {
        "name": "turing",
        "file": "File:Alan Turing (1951).jpg",
        "focal": "top",
        "alt": "Retrato fotográfico de Alan Turing, 1951",
        "milestone": "1950 - La prueba de Turing",
    },
    {
        "name": "patron-oro",
        "file": ("File:United States one-hundred-thousand-dollar bill on "
                 "display at the Smithsonian National Museum of American "
                 "History, 7 February 2024.jpg"),
        "focal": "center",
        "alt": "Certificado de oro de 100.000 dólares expuesto en el Smithsonian",
        "milestone": "1971 - El fin del patrón oro",
    },
    {
        "name": "bezos-amazon",
        "file": "File:Jeff Bezos talking.jpg",
        "focal": "top",
        "alt": "Jeff Bezos, fundador de Amazon, en una visita militar",
        "milestone": "1994 - Amazon vende su primer libro",
    },
    {
        "name": "deep-learning",
        "file": "File:GPU workstation lid off.webp",
        "focal": "center",
        "alt": "Estación de trabajo con tarjeta gráfica (GPU) y disipadores",
        "milestone": "2012 - El deep learning despega",
    },
    {
        "name": "chatgpt",
        "file": "File:Laptop Programmcode.jpg",
        "focal": "center",
        "alt": "Portátil mostrando código de programación en pantalla",
        "milestone": "2022 - ChatGPT lleva la IA a todos",
    },
]

OK_LICENSES = ("public domain", "cc0", "cc-zero", "pd-", "pdm")


def commons_info(filename: str) -> dict:
    params = {
        "action": "query", "format": "json", "titles": filename,
        "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": "1600",
    }
    req = urllib.request.Request(
        API + "?" + urllib.parse.urlencode(params), headers=UA)
    with urllib.request.urlopen(req, timeout=40) as r:
        data = json.load(r)
    pages = (data.get("query") or {}).get("pages") or {}
    page = next(iter(pages.values()))
    if int(page.get("missing", 0) or 0) == 1 or "imageinfo" not in page:
        raise RuntimeError(f"no existe en Commons: {filename}")
    ii = page["imageinfo"][0]
    meta = ii.get("extmetadata") or {}
    lic = ((meta.get("LicenseShortName") or {}).get("value") or "?").strip()
    artist = ((meta.get("Artist") or {}).get("value") or "").strip()
    return {"license": lic, "artist": artist,
            "thumb": ii.get("thumburl") or ii.get("url"),
            "descurl": ii.get("descriptionurl", "")}


def download(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def crop_to_aspect(img: Image.Image, focal: str) -> Image.Image:
    w, h = img.size
    target = ASPECT
    if w / h > target:  # demasiado ancha: recorta los lados
        new_w = int(h * target)
        x = (w - new_w) // 2
        box = (x, 0, x + new_w, h)
    else:  # demasiado alta: recorta desde arriba (focal top) o centrado
        new_h = int(w / target)
        if h > new_h:
            y = 0 if focal == "top" else int((h - new_h) / 2)
            box = (0, y, w, y + new_h)
        else:
            box = (0, 0, w, h)
    return img.crop(box)


def duotone(img: Image.Image) -> Image.Image:
    gray = img.convert("L")
    gray = ImageEnhance.Contrast(gray).enhance(1.12)
    r = gray.point(lambda i: int(INK[0] + (PAPER[0] - INK[0]) * i / 255))
    g = gray.point(lambda i: int(INK[1] + (PAPER[1] - INK[1]) * i / 255))
    b = gray.point(lambda i: int(INK[2] + (PAPER[2] - INK[2]) * i / 255))
    return Image.merge("RGB", (r, g, b))


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Créditos de las imágenes de la sección Hitos",
        "",
        "Descargadas con `python scripts/fetch_hitos.py` y reprocesadas en",
        "duotone con la paleta de Señal Abierta (ink #11110f / paper #e9e6dc).",
        "Todas son dominio público o CC0: no exigen atribución, pero se",
        "documentan aquí por trazabilidad.",
        "",
    ]
    ok = 0
    for item in MANIFEST:
        info = commons_info(item["file"])
        lic = info["license"].lower()
        if not any(k in lic for k in OK_LICENSES):
            print(f"NO-CUMPLE {item['name']}: licencia '{info['license']}'")
            return 1
        raw = download(info["thumb"])
        src = Image.open(io.BytesIO(raw)).convert("RGB")
        cropped = crop_to_aspect(src, item["focal"])
        out = duotone(cropped).resize((OUT_W, int(OUT_W / ASPECT)),
                                      Image.LANCZOS)
        dest = OUT / f"{item['name']}.webp"
        out.save(dest, "WEBP", quality=84, method=6)
        lines.append(f"- **{item['milestone']}** — {item['alt']}. "
                     f"Fuente: [{item['file'].removeprefix('File:')}]"
                     f"({info['descurl']}) — {info['license']}.")
        print(f"OK {item['name']:<22} {info['license']:<16} "
              f"{src.size} -> {out.size} -> {dest.name}")
        ok += 1

    lines.append("")
    (OUT / "CREDITS.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"OK: {ok}/{len(MANIFEST)} imágenes en img/hitos/ + CREDITS.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
