# cc-P237 read only: every image file in the seven packs (bytes, size, mode, bbox of non-black pixels) and one contact
# sheet per pack (sheet-<pack>.png here, git-ignored) so the art can be looked at. Writes only the sheets.
import os, sys, glob
from PIL import Image, ImageDraw
TP = 'D:/UO/third-party'
PACKS = ['farm-carts', 'oil-lantern', 'marble-railings', 'bridge-support-beam', 'orc-encampment', 'paintings-odin',
         'paintings-odin-2']
HERE = os.path.dirname(os.path.abspath(__file__))
EXT = ('.png', '.bmp', '.tif', '.tiff')
for p in PACKS:
    files = sorted(f for f in glob.glob(os.path.join(TP, p, '**', '*'), recursive=True)
                   if f.lower().endswith(EXT) and '_zips' not in f and os.path.basename(f) not in ('sheet.png', 'existing-slots.png'))
    print('=== %s: %d files' % (p, len(files)))
    thumbs = []
    for f in files:
        im = Image.open(f)
        rgb = im.convert('RGBA')
        px = rgb.load()
        # bbox of pixels that are neither pure black nor fully transparent
        mask = Image.new('L', rgb.size, 0); mp = mask.load()
        for y in range(rgb.size[1]):
            for x in range(rgb.size[0]):
                r, g, b, a = px[x, y]
                if a and (r, g, b) != (0, 0, 0): mp[x, y] = 255
        bb = mask.getbbox()
        print('  %-60s %8d B  %4dx%-4d %-5s bits=%s content=%s' % (os.path.relpath(f, os.path.join(TP, p)), os.path.getsize(f),
              im.size[0], im.size[1], im.mode, im.info.get('compression', ''), bb))
        thumbs.append((os.path.basename(f), rgb))
    if not thumbs: continue
    cw = max(t.size[0] for _, t in thumbs) + 8; ch = max(t.size[1] for _, t in thumbs) + 20
    cols = min(8, len(thumbs)); rows = (len(thumbs) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * cw, rows * ch), (90, 110, 90))
    d = ImageDraw.Draw(sheet)
    for i, (n, t) in enumerate(thumbs):
        x, y = (i % cols) * cw, (i // cols) * ch
        sheet.paste(t, (x + 4, y + 16), t)
        d.text((x + 2, y + 2), n[:24], fill=(255, 255, 255))
    sheet.save(os.path.join(HERE, 'sheet-' + p + '.png'))
