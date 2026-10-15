"""Generate the PWA icons from the planner's own palette.

    python tools/build-icons.py        # -> icons/

Edit this file, never the PNGs it writes. The mark is a stylised week: three
columns of blocks, two of them in the accent orange, on the app's dark ground.
"""

import os
from PIL import Image, ImageDraw

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons")

BG = "#151515"
ORANGE = "#FF6B00"
GREY_D = "#5A5A57"
GREY_M = "#8C8C88"
GREY_L = "#C9C9C4"

# (column, top, bottom, colour) in normalised content-box coordinates
BLOCKS = [
    (0, 0.00, 0.45, GREY_M),
    (0, 0.55, 1.00, ORANGE),
    (1, 0.18, 0.82, GREY_D),
    (2, 0.00, 0.30, GREY_L),
    (2, 0.40, 1.00, ORANGE),
]
COLS, GAP = 3, 0.10


def render(size, inset):
    """inset is the fraction of the canvas left empty on each side."""
    # 4x supersampling, then downscale: PIL has no antialiased rounded_rectangle
    s = size * 4
    im = Image.new("RGB", (s, s), BG)
    d = ImageDraw.Draw(im)

    box = s * (1 - 2 * inset)
    off = s * inset
    cw = box * (1 - GAP * (COLS - 1)) / COLS
    radius = cw * 0.22

    for col, top, bot, colour in BLOCKS:
        x0 = off + col * (cw + box * GAP)
        d.rounded_rectangle(
            [x0, off + top * box, x0 + cw, off + bot * box],
            radius=radius, fill=colour,
        )
    return im.resize((size, size), Image.LANCZOS)


def main():
    os.makedirs(OUT, exist_ok=True)
    jobs = [
        ("icon-192.png", 192, 0.14),
        ("icon-512.png", 512, 0.14),
        # maskable: platforms crop to a circle of 80% diameter, so keep the
        # mark well inside that safe zone and let the background bleed out
        ("icon-maskable-512.png", 512, 0.26),
    ]
    for name, size, inset in jobs:
        p = os.path.join(OUT, name)
        render(size, inset).save(p, optimize=True)
        print("%-26s %4dpx  %5.1f KB" % (name, size, os.path.getsize(p) / 1024))


if __name__ == "__main__":
    main()
