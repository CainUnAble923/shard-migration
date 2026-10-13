# cc-P36: candidate hues for the four starter resources, read from EA's hues.mul (the 117 copy).
# Prints, per target colour, the nearest hues by their mid-ramp colour, skipping any hue already used by a
# resource in server/customizations/ResourceInfo.cs (and its +-2 neighbours). ASCII only.
import struct, re, sys
HUES = r"D:\ShatteredLegacy\client-data\classic-client-7.0.117.0\hues.mul"
RI = r"D:\ShatteredLegacy\server\customizations\ResourceInfo.cs"
data = open(HUES, "rb").read()
def entry(h):  # h is the 0-based hue index in the file; a hue number N maps to index N-1
    blk, e = divmod(h, 8)
    off = blk * 708 + 4 + e * 88
    cols = struct.unpack_from("<32H", data, off)
    name = data[off + 68: off + 88].split(b"\0")[0].decode("ascii", "replace")
    return cols, name
def rgb(c): return ((c >> 10) & 31) * 255 // 31, ((c >> 5) & 31) * 255 // 31, (c & 31) * 255 // 31
n = len(data) // 708 * 8
s = open(RI, encoding="utf-8").read()
used = {int(x, 16) for x in re.findall(r"new\(\s*(0x[0-9A-Fa-f]+)\s*,", s[s.index("class CraftResources"):])}
blocked = {u + d for u in used for d in range(-2, 3)}
targets = {"Dawnstone (pale rose-gold dawn)": (232, 176, 150), "Burrowhide (earthy grey-brown)": (120, 100, 80),
           "Rootwood (dark red-brown root)": (110, 60, 40), "Gloomsilk (dusky violet-grey)": (90, 75, 110)}
for t, (r, g, b) in targets.items():
    cands = []
    for h in range(1, min(n, 3000)):
        if h in blocked: continue
        cols, name = entry(h - 1)
        mr, mg, mb = rgb(cols[20])
        d = ((mr - r) ** 2 + (mg - g) ** 2 + (mb - b) ** 2) ** 0.5
        cands.append((d, h, name, (mr, mg, mb)))
    cands.sort()
    print(t)
    for d, h, name, c in cands[:6]:
        print(f"  0x{h:04X} ({h})  mid-ramp rgb{c}  dist {d:.0f}  '{name}'")
print("used resource hues:", ", ".join(f"0x{u:04X}" for u in sorted(used)))
