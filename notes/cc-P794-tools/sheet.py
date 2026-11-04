# cc-P794: one sheet of the seven rides, cropped round the character, for looking at them side by side. python -P sheet.py
from PIL import Image, ImageDraw

d = "D:/UO/golems/Iron/shard-migration/notes/cc-P794-shots/"
names = ["windrunner", "lasher", "tiger", "light-tiger", "hellhound", "boura", "peacock"]
W, H = 300, 270
sheet = Image.new("RGB", (W * 4, H * 4), "black")
for i, n in enumerate(names):
    for j, part in enumerate(("1-ridden", "2-walked")):
        im = Image.open(d + "%s-%s.jpg" % (n, part)).convert("RGB")
        c = im.crop((262, 215, 262 + W, 215 + H))
        ImageDraw.Draw(c).text((6, 4), "%s %s" % (n, part), fill="yellow")
        col, row = i % 4, (i // 4) * 2 + j
        sheet.paste(c, (col * W, row * H))
sheet.save(d + "sheet-all-seven.jpg", quality=88)
