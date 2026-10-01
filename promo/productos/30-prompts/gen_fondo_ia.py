# -*- coding: utf-8 -*-
"""Genera fondo-ia.png con modelo de imagen.

- GPU libre  -> Z-Image-Turbo local (GGUF, 8 pasos, ~2s)
- GPU ocupada -> NVIDIA NIM flux.1-dev (nube, gratis, 0 VRAM)
"""
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent
OUT = HERE / "fondo-ia.png"

PROMPT = (
    "Premium dark navy background for a digital product cover, abstract AI "
    "theme: glowing amber and gold neural network nodes, thin luminous circuit "
    "lines and soft bokeh particles flowing from the right side, subtle dark "
    "grid texture, deep slate blue gradient, cinematic rim light, minimalist "
    "tech aesthetic, high detail, the left two thirds is empty dark negative "
    "space for text overlay, no text, no letters, no words, no logo, no watermark"
)


def gpu_busy() -> bool:
    try:
        r = subprocess.run(
            ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=10,
        )
        return r.returncode == 0 and int(r.stdout.strip()) > 4000
    except Exception:
        return True


def gen_local(img, w=1152, h=896, steps=9, seed=20261002):
    sys.path.insert(0, r"D:\WSL\youtube-automation")
    from module.generate_thumbnail_gguf import generate_background
    return generate_background(PROMPT, width=w, height=h, steps=steps, seed=seed)


def gen_nim(w=1152, h=896, seed=20261002):
    import os
    os.environ["NVIDIA_NIM_IMAGE_MODEL"] = "black-forest-labs/flux.1-dev"
    sys.path.insert(0, r"D:\WSL\youtube-automation")
    from io import BytesIO
    from module.nvidia_nim_client import generate_image_nim
    from PIL import Image
    for model in ("dev", "klein"):
        data = generate_image_nim(PROMPT, seed=seed, width=w, height=h,
                                  steps=28, model=model, use_cache=False)
        if data:
            img = Image.open(BytesIO(data)).convert("RGB")
            meta = {"model": f"nim:{model}", "seed": seed,
                    "width": img.size[0], "height": img.size[1]}
            return img, meta
    raise RuntimeError("NIM dev y klein fallaron")


def main():
    if gpu_busy():
        print("GPU ocupada -> NIM flux (nube)")
        img, meta = gen_nim()
    else:
        print("GPU libre -> Z-Image local")
        img, meta = gen_local()
    img.save(OUT, "PNG")
    print(f"PNG: {OUT} ({img.size[0]}x{img.size[1]})")
    print(meta)


if __name__ == "__main__":
    main()
