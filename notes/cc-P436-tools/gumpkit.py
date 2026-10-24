"""cc-P436: draw guild and League gump previews from gump art, as the client lays a gump out.

Reads stock gumps from the client's gumpartLegacyMUL.uop (find-free-art.py's Uop reader) and PNG art from disk.
A "look" maps the stock IDs our gumps use (frame 9270, panel 2624, rule 9304, the buttons) to images.
    python -P gumpkit.py            (writes previews\\*.png beside this file)
"""
import importlib.util
import os
import struct
import zlib

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FFA = r"D:\UO\golems\Iron\ShatteredLegacy\scripts\find-free-art.py"
CLIENT = r"D:\UO\UltimaOnlineVanilla"

_spec = importlib.util.spec_from_file_location("ffa", FFA)
ffa = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ffa)
_uop = ffa.Uop(os.path.join(CLIENT, "gumpartLegacyMUL.uop"))

# EA's 7.0.117 gumpart entries are flag 3: zlib, then the BWT pass cliloc.py ports from pinned's BwtDecompress.
_spec2 = importlib.util.spec_from_file_location("cliloc", os.path.join(HERE, "..", "cc-P29-tools", "cliloc.py"))
_bwt = importlib.util.module_from_spec(_spec2)
_spec2.loader.exec_module(_bwt)


def _entry(gid):
    v = _uop.e.get(ffa.uop_hash("build/gumpartlegacymul/%08d.tga" % gid))
    if not v:
        return None
    _uop.f.seek(v[0])
    d = _uop.f.read(v[1])
    if v[3] in (1, 3):
        d = zlib.decompress(d)
    if v[3] == 3:
        d = bytes(_bwt._internal(_bwt._mtf(d[4:])))
    return d


def stock(gid):
    """A stock gump as RGBA (colour 0 transparent), or None."""
    d = _entry(gid)
    if d is None:
        return None
    w, h = struct.unpack("<ii", d[:8])
    body = d[8:]
    table = struct.unpack("<%di" % h, body[: 4 * h])
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = img.load()
    for y in range(h):
        start = table[y] * 4
        end = table[y + 1] * 4 if y + 1 < h else len(body)
        x = 0
        for i in range(start, end, 4):
            colour, run = struct.unpack("<HH", body[i : i + 4])
            if colour:
                r = ((colour >> 10) & 0x1F) * 255 // 31
                g = ((colour >> 5) & 0x1F) * 255 // 31
                b = (colour & 0x1F) * 255 // 31
                for k in range(run):
                    if x + k < w:
                        px[x + k, y] = (r, g, b, 255)
            x += run
    return img


def png(path, black_transparent=True):
    img = Image.open(path).convert("RGBA")
    if black_transparent:
        data = [(0, 0, 0, 0) if p[:3] == (0, 0, 0) else p for p in img.getdata()]
        img.putdata(data)
    return img


# -- Drawing primitives as the client does them -------------------------------------------------------------------


def tile(canvas, img, x, y, w, h):
    if img is None or w <= 0 or h <= 0:
        return
    iw, ih = img.size
    for yy in range(y, y + h, ih):
        for xx in range(x, x + w, iw):
            piece = img.crop((0, 0, min(iw, x + w - xx), min(ih, y + h - yy)))
            canvas.alpha_composite(piece, (xx, yy))


def background(canvas, parts, x, y, w, h):
    """A resizable background: nine images (top-left, top, top-right, left, centre, right, bottom-left, bottom,
    bottom-right), as AddBackground draws gump IDs id..id+8."""
    tl, t, tr, l, c, r, bl, b, br = parts
    tile(canvas, c, x + l.width, y + t.height, w - l.width - r.width, h - t.height - b.height)
    tile(canvas, t, x + tl.width, y, w - tl.width - tr.width, t.height)
    tile(canvas, b, x + bl.width, y + h - b.height, w - bl.width - br.width, b.height)
    tile(canvas, l, x, y + tl.height, l.width, h - tl.height - bl.height)
    tile(canvas, r, x + w - r.width, y + tr.height, r.width, h - tr.height - br.height)
    canvas.alpha_composite(tl, (x, y))
    canvas.alpha_composite(tr, (x + w - tr.width, y))
    canvas.alpha_composite(bl, (x, y + h - bl.height))
    canvas.alpha_composite(br, (x + w - br.width, y + h - br.height))


def nine(get, base):
    return [get(base + i) for i in range(9)]


_FONT = None


def font():
    global _FONT
    if _FONT is None:
        for f in (r"C:\Windows\Fonts\tahomabd.ttf", r"C:\Windows\Fonts\tahoma.ttf", r"C:\Windows\Fonts\arial.ttf"):
            if os.path.exists(f):
                _FONT = ImageFont.truetype(f, 12)
                break
        else:
            _FONT = ImageFont.load_default()
    return _FONT


def label(canvas, x, y, colour, text):
    ImageDraw.Draw(canvas).text((x, y + 1), text, fill=colour, font=font())
