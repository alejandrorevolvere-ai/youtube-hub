# -*- coding: utf-8 -*-
"""Genera variantes de fondo IA (flux.1-dev, 50 pasos) con prompt del tema."""
import os
import sys
from io import BytesIO
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
os.environ["NVIDIA_NIM_IMAGE_MODEL"] = "black-forest-labs/flux.1-dev"
sys.path.insert(0, r"D:\WSL\youtube-automation")

from PIL import Image  # noqa: E402
from module.nvidia_nim_client import generate_image_nim  # noqa: E402

HERE = Path(__file__).resolve().parent

PROMPT = (
    "Premium editorial background for the cover of a digital PDF pack of AI "
    "prompts about productivity and time leverage. Deep slate navy studio "
    "backdrop, subtle volumetric light. On the right side: a floating stack "
    "of three glowing holographic chat-prompt cards in slight perspective, "
    "blank interfaces without any writing, connected to an abstract neural "
    "network of thin luminous golden lines and small sparkles; behind them a "
    "large minimalist hourglass made of light particles symbolizing time "
    "multiplied, faint elegant speed streaks. Warm amber and gold rim "
    "lighting, cinematic soft glow, shallow depth of field, ultra detailed "
    "8k product render, the left two thirds is clean empty dark negative "
    "space for a headline. No text, no letters, no words, no numbers, no "
    "logos, no watermark, no people"
)

SEEDS = [11, 77, 2026]
W, H, STEPS = 1216, 832, 50


def main():
    for i, seed in enumerate(SEEDS, 1):
        out = HERE / f"fondo-ia-v{i}.png"
        data = generate_image_nim(PROMPT, seed=seed, width=W, height=H,
                                  steps=STEPS, model="dev", use_cache=False)
        if not data:
            print(f"v{i}: FALLÓ")
            continue
        img = Image.open(BytesIO(data)).convert("RGB")
        img.save(out, "PNG")
        print(f"v{i}: {out} ({img.size[0]}x{img.size[1]}, seed={seed})")


if __name__ == "__main__":
    main()
