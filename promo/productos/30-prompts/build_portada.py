# -*- coding: utf-8 -*-
"""Genera portada-kofi.png (imagen del producto para el Ko-fi Shop)."""
from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
OUT = HERE / "portada-kofi.png"

W, H = 1200, 900
INK = (15, 23, 42)
INK2 = (30, 41, 59)
AMBER = (245, 158, 11)
AMBER_DARK = (217, 119, 6)
WHITE = (255, 255, 255)
GRAY = (148, 163, 184)
LIGHT = (241, 245, 249)
DARKTXT = (30, 41, 59)

F = "C:/Windows/Fonts/"


def font(name, size):
    return ImageFont.truetype(F + name, size)


f_brand = font("segoeuib.ttf", 30)
f_url = font("segoeui.ttf", 24)
f_h1 = font("segoeuib.ttf", 96)
f_h2 = font("segoeuib.ttf", 74)
f_badge = font("segoeuib.ttf", 26)
f_mono = font("consola.ttf", 22)
f_mono_sm = font("consola.ttf", 19)
f_foot = font("segoeui.ttf", 24)


def main():
    img = Image.new("RGB", (W, H), INK)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 14], fill=AMBER)
    d.rectangle([0, H - 60, W, H], fill=INK2)

    d.text((60, 54), "SEÑAL ABIERTA", font=f_brand, fill=AMBER)
    url = "senalabierta.pages.dev"
    uw = d.textlength(url, font=f_url)
    d.text((W - 60 - uw, 60), url, font=f_url, fill=GRAY)

    d.text((60, 130), "30 prompts de IA", font=f_h1, fill=WHITE)
    d.text((60, 240), "para trabajar el doble", font=f_h2, fill=AMBER)
    d.text((60, 332), "en la mitad de tiempo", font=f_h2, fill=WHITE)

    card = [60, 470, 760, 760]
    d.rounded_rectangle(card, radius=18, fill=LIGHT)
    d.rectangle([60, 470, 70, 760], fill=AMBER_DARK)
    d.text((96, 494), "PROMPT 01 · CHATGPT", font=f_mono_sm, fill=(100, 116, 139))
    lines = [
        "Actúa como mi chief of staff.",
        "Metas: [METAS]. Disponibilidad:",
        "[HORAS LIBRES]. Plan día por día",
        "en bloques de 90 min.",
    ]
    y = 540
    for ln in lines:
        d.text((96, y), ln, font=f_mono, fill=DARKTXT)
        y += 42
    d.text((96, y + 10), "→ tabla | día | bloque | tarea |", font=f_mono, fill=(217, 119, 6))

    badges = ["30 prompts", "9 bloques", "3 recetas bonus", "+ PDF 14 pág."]
    x, by = 810, 480
    for b in badges:
        bw = d.textlength(b, font=f_badge) + 44
        d.rounded_rectangle([x, by, x + bw, by + 54], radius=27,
                            outline=AMBER, width=3)
        d.text((x + 22, by + 11), b, font=f_badge, fill=AMBER)
        by += 76
        if x + bw > W - 100:
            x, by = 810, by

    d.text((810, by + 18), "ChatGPT · Notion IA · Perplexity", font=f_foot, fill=GRAY)
    d.text((810, by + 54), "Midjourney · Ideogram · Gamma", font=f_foot, fill=GRAY)

    d.text((60, H - 46), "Cada prompt enlaza a su vídeo original  ·  Edición 1 · 2026",
           font=f_foot, fill=GRAY)

    img.save(OUT, "PNG")
    print(f"PNG: {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
