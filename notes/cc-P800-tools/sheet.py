# cc-P800: one sheet of the worn sash at each step, the paperdoll cropped. python -P sheet.py
from PIL import Image, ImageDraw

d = "D:/UO/golems/Iron/shard-migration/notes/cc-P800-shots/final/"
names = ["step0-4-worn"] + ["step%d-2-worn" % s for s in range(1, 7)]
W, H = 260, 300
sheet = Image.new("RGB", (W * 4, H * 2), "black")
for i, n in enumerate(names):
    c = Image.open(d + n + ".jpg").convert("RGB").crop((110, 140, 110 + W, 140 + H))
    ImageDraw.Draw(c).text((6, 4), n, fill="yellow")
    sheet.paste(c, ((i % 4) * W, (i // 4) * H))
sheet.save("D:/UO/golems/Iron/shard-migration/notes/cc-P800-shots/sheet-worn-steps.jpg", quality=90)
