r"""cc-P678: a top-down picture of SoS Haven in radar colours, with a 10-tile grid and marked spots.
    python -P towntop.py x1 y1 x2 y2 scale out.png [label=x,y ...]
Read only, SoS 3.0 through P481's loaders (islands.build: radar colours of land and the top static).
"""
import os
import sys

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "cc-P481-tools"))
import islands  # noqa: E402


def main():
    x1, y1, x2, y2, s = (int(v) for v in sys.argv[1:6])
    out = sys.argv[6]
    marks = []
    for a in sys.argv[7:]:
        name, xy = a.split("=")
        x, y = (int(v) for v in xy.split(","))
        marks.append((name, x, y))
    col, _, _, _, _, _ = islands.build("sos")
    sub = col[x1:x2 + 1, y1:y2 + 1].transpose(1, 0, 2).copy()
    im = Image.fromarray(sub).resize(((x2 - x1 + 1) * s, (y2 - y1 + 1) * s), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for x in range(x1, x2 + 1):
        if x % 10 == 0:
            d.line([((x - x1) * s, 0), ((x - x1) * s, im.height)], fill=(255, 255, 255), width=1)
            d.text(((x - x1) * s + 2, 2), str(x), fill=(255, 255, 0))
    for y in range(y1, y2 + 1):
        if y % 10 == 0:
            d.line([(0, (y - y1) * s), (im.width, (y - y1) * s)], fill=(255, 255, 255), width=1)
            d.text((2, (y - y1) * s + 2), str(y), fill=(255, 255, 0))
    for name, x, y in marks:
        cx, cy = (x - x1) * s + s // 2, (y - y1) * s + s // 2
        d.ellipse([cx - s, cy - s, cx + s, cy + s], outline=(255, 0, 255), width=2)
        d.text((cx + s + 2, cy - 6), name, fill=(255, 0, 255))
    im.save(out)
    print(out, im.size)


if __name__ == "__main__":
    main()
