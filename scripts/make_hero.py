#!/usr/bin/env python3
"""Prepare the Welcome page photograph: brighten it, mark the card, compress it.

Not part of the build. The photograph changes about as often as the brand does,
so this exists to record what was done to it rather than to run on a schedule:
a gamma lift, because the room reads as murk on a white page otherwise, and the
hexagon laid over the graphics card at low opacity and sheared to sit on its
face rather than floating in front of it.

    python3 scripts/make_hero.py assets/hero-source.png

The source photograph lives in `assets/`, which the build does not stage, so the
published tree carries only the finished JPEG.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageEnhance

REPO = Path(__file__).resolve().parent.parent
SYMBOL = Path.home() / "Edgible/www.edgible.com/website/static/edgible-symbol-white-on-transperant.png"
DEST = REPO / "static" / "images" / "self-hosted-machine.jpg"

# Where the card face sits in the photograph, as fractions of width and height,
# so the numbers survive a change of source resolution but not a change of
# photograph. Re-measure if the picture changes.
CARD_CENTRE = (0.498, 0.600)
CARD_HEIGHT = 0.26
SHEAR = 0.10  # the card face recedes to the right, so the mark leans with it


def brighten(im: Image.Image, gamma: float, brightness: float) -> Image.Image:
    lut = [min(255, round(255 * ((i / 255) ** gamma))) for i in range(256)]
    out = im.point(lut * 3)
    out = ImageEnhance.Brightness(out).enhance(brightness)
    return ImageEnhance.Color(out).enhance(1.03)


def watermark(im: Image.Image, alpha: float) -> Image.Image:
    mark = Image.open(SYMBOL).convert("RGBA")
    # The file is padded, and the glyph is much wider than it is tall, so crop
    # to the ink and scale by height or the hexagon comes out stretched.
    mark = mark.crop(mark.getchannel("A").getbbox())
    side = round(im.height * CARD_HEIGHT)
    mark = mark.resize((round(side * mark.width / mark.height), side), Image.LANCZOS)

    # Lean the mark with the face it sits on. The affine matrix is inverse, so a
    # negative shear on x tips the top of the hexagon to the right.
    pad = round(mark.height * SHEAR)
    mark = mark.transform(
        (mark.width + pad, mark.height),
        Image.AFFINE,
        (1, SHEAR, -pad * 0.5, 0, 1, 0),
        resample=Image.BICUBIC,
    )

    shape = mark.getchannel("A")
    x = round(im.width * CARD_CENTRE[0] - mark.width / 2)
    y = round(im.height * CARD_CENTRE[1] - mark.height / 2)
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))

    # The card face is bright metal and its fans are nearly black, so a single
    # white mark disappears against one or the other. Laying a dark copy down
    # first, offset by a few pixels, reads as an etch on both.
    for colour, dx, dy, strength in (
        ((0, 0, 26), 4, 4, 0.85),
        ((255, 255, 255), 0, 0, 1.0),
    ):
        ink = Image.new("RGBA", mark.size, colour + (0,))
        ink.putalpha(shape.point(lambda a: round(a * alpha * strength)))
        layer.paste(ink, (x + dx, y + dy), ink)

    return Image.alpha_composite(im.convert("RGBA"), layer).convert("RGB")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("--alpha", type=float, default=0.55)
    ap.add_argument("--gamma", type=float, default=0.72)
    ap.add_argument("--brightness", type=float, default=1.08)
    ap.add_argument("--width", type=int, default=1400)
    ap.add_argument("--out", type=Path, default=DEST)
    args = ap.parse_args()

    im = Image.open(args.source).convert("RGB")
    im.thumbnail((args.width, args.width), Image.LANCZOS)
    im = brighten(im, args.gamma, args.brightness)
    im = watermark(im, args.alpha)
    im.save(args.out, "JPEG", quality=82, optimize=True, progressive=True)
    print(f"wrote {args.out} at {im.size[0]}x{im.size[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
