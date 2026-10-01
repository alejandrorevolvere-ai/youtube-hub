# -*- coding: utf-8 -*-
"""Genera portada-kofi.png (imagen del producto para el Ko-fi Shop).

Diseño minimalista: héroe IA (fondo-ia.png) + mensaje corto.
Tipografía: Bahnschrift (variable, estilo DIN) + Segoe UI Light.
"""
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
OUT = HERE / "portada-kofi.png"
FONDO_IA = HERE / "fondo-ia.png"

W, H = 1200, 900
INK = (15, 23, 42)
AMBER = (245, 158, 11)
WHITE = (255, 255, 255)
GRAY = (148, 163, 184)
SOFT = (226, 232, 240)

F = "C:/Windows/Fonts/"


def font(name, size, bold=False):
    f = ImageFont.truetype(F + name, size)
    if bold:
        f.set_variation_by_name("Bold")
    return f


def tracked(d, x, y, text, f, fill, tracking=0):
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + tracking
    return x


def base_layer():
    """Fondo: imagen IA (fondo-ia.png) con scrim, o color plano."""
    if FONDO_IA.exists():
        src = Image.open(FONDO_IA).convert("RGB")
        scale = max(W / src.width, H / src.height)
        src = src.resize((round(src.width * scale), round(src.height * scale)),
                         Image.LANCZOS)
        left = (src.width - W) // 2
        top = (src.height - H) // 2
        fondo = src.crop((left, top, left + W, top + H))
        scrim = Image.new("RGB", (W, H), INK)
        mask = Image.new("L", (W, H), 0)
        md = ImageDraw.Draw(mask)
        for x in range(W):
            t = x / W
            if t < 0.55:
                a = int(150 * (1 - t / 0.55) + 55)
            else:
                a = int(55 * (1 - (t - 0.55) / 0.45))
            md.line([(x, 0), (x, H)], fill=a)
        return Image.composite(scrim, fondo, mask)
    return Image.new("RGB", (W, H), INK)


def main():
    img = base_layer()
    d = ImageDraw.Draw(img)

    f_brand = font("bahnschrift.ttf", 30, bold=True)
    f_url = font("segoeuil.ttf", 24)
    f_h1 = font("bahnschrift.ttf", 96, bold=True)
    f_h2 = font("bahnschrift.ttf", 54)

    d.rectangle([0, 0, W, 8], fill=AMBER)

    tracked(d, 60, 50, "SEÑAL ABIERTA", f_brand, AMBER, tracking=5)
    url = "senalabierta.pages.dev"
    uw = d.textlength(url, font=f_url)
    d.text((W - 60 - uw, 52), url, font=f_url, fill=GRAY)

    d.text((60, 296), "30 prompts de IA", font=f_h1, fill=WHITE)
    d.text((60, 432), "para trabajar el doble", font=f_h2, fill=AMBER)
    d.text((60, 500), "en la mitad de tiempo", font=f_h2, fill=SOFT)

    d.rectangle([60, 596, 180, 600], fill=AMBER)

    img.save(OUT, "PNG")
    w1 = d.textlength("30 prompts de IA", font=f_h1)
    print(f"PNG: {OUT} ({W}x{H}) h1_width={w1:.0f}")


if __name__ == "__main__":
    main()
