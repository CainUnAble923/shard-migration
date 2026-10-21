# cc-P266: the one table of which source file becomes which art ID for the second winter set (registry.csv repeats
# it per row). Read by convert_art.py, registry_rows.py, records.py, the renders and validate.py.
# IDs from 0x3388 (13192), 8-aligned inside find-free-art.py --placeholder's run 0x3386-0x3420 (155 IDs, the longest
# left; the 0x3C00 block P34, P50, P237, P243 and P265 used has no run of 40 free IDs any more). The satchel icons
# (cc-P236) end at 0x3385, just before.
#   (first id, key, what, pack, [source files], how)
#   how: 'bt' = 24-bit BMP, black means transparent (anchor-art-frames.py --black-transparent --keep-geometry)
# An animation's frames take the IDs after its first (the client's animdata counts from the base ID).
TP = 'D:/UO/third-party'
MC = TP + '/mrriots-christmas'
CAL = TP + '/mrriots-christmas-calendar'
FIRST = 0x3388


def _frames(folder, names):
    return [MC + '/' + folder + '/' + n for n in names]


_TREE = ['xmastree %02d.bmp' % k for k in range(2, 13)]   # 11 frames, 02..12 as the author numbered them

_GROUPS = [
    # the two animated Christmas trees (MrRiots, "Thanks Vorspire" for the animation)
    ('tree-large', 'decorated Christmas tree, large, animated (11 frames)', 'mrriots-christmas', _frames('Christmas Tree', _TREE), 'bt'),
    ('tree-small', 'decorated Christmas tree, small, animated (11 frames)', 'mrriots-christmas', _frames('ChristmasTreeSmall', _TREE), 'bt'),
    # ribbon garlands: the art's top edge falls to the right in ChristmasRibbon.bmp (a north wall, faces south) and to
    # the left in ChristmasRibbon1.bmp (a west wall, faces east): P34's rule, measured in facts.py
    ('ribbon-n', 'ribbon garland (on a north wall, faces south)', 'mrriots-christmas', [MC + '/ChristmasRibbon.bmp'], 'bt'),
    ('ribbon-w', 'ribbon garland (on a west wall, faces east)', 'mrriots-christmas', [MC + '/ChristmasRibbon1.bmp'], 'bt'),
    # lights: the tall candle stand (4 lit frames; "Off.bmp" not used), the short candle (4 lit frames; "off.bmp" not
    # used), the antler candelabra (4 frames), the Swedish advent candles (4 frames, the "n.bmp" facing; "n-n.bmp" is the
    # other facing and "Off" the unlit one, not used)
    ('candle-tall', 'tall candle stand, lit, animated (4 frames)', 'mrriots-christmas', _frames('TallCandle', ['1.bmp', '2.bmp', '3.bmp', '4.bmp']), 'bt'),
    ('candle-short', 'short candle, lit, animated (4 frames)', 'mrriots-christmas', _frames('ShortCandle', ['1.bmp', '2.bmp', '3.bmp', '4.bmp']), 'bt'),
    ('antler', 'antler candelabra, lit, animated (4 frames)', 'mrriots-christmas', _frames('Antlier', ['Antlier.bmp', 'Antlier1.bmp', 'Antlier2.bmp', 'Antlier3.bmp']), 'bt'),
    ('advent', 'advent candles, lit, animated (4 frames)', 'mrriots-christmas', _frames('AdventCandles', ['1.bmp', '2.bmp', '3.bmp', '4.bmp']), 'bt'),
    # small pieces
    ('poinsettia', 'poinsettia', 'mrriots-christmas', [MC + '/Pointsetta.bmp'], 'bt'),
    ('potted', 'potted holiday tree', 'mrriots-christmas', [MC + '/PottedSomething.bmp'], 'bt'),
    ('gnome', 'holiday gnome', 'mrriots-christmas', [MC + '/Gnome.bmp'], 'bt'),
    ('soldier', 'toy soldier', 'mrriots-christmas', [MC + '/ToySoldier.bmp'], 'bt'),
    ('plush-dragon', 'dragon plushie', 'mrriots-christmas', [MC + '/DragonPlush.bmp'], 'bt'),
    # the advent calendar (the item; its gump is 22469, gumps\22469.png): 1.bmp's top edge falls to the left (a west
    # wall), 2.bmp's to the right (a north wall)
    ('calendar-w', 'advent calendar (on a west wall, faces east)', 'mrriots-christmas-calendar', [CAL + '/1.bmp'], 'bt'),
    ('calendar-n', 'advent calendar (on a north wall, faces south)', 'mrriots-christmas-calendar', [CAL + '/2.bmp'], 'bt'),
]

GUMP_ID = 22469
GUMP_SRC = CAL + '/AdventCalendar.bmp'   # 400 x 400, no pure black pixel: shipped opaque

# key -> (first id, what, pack, files, how); ids run on in table order, an animation's frames after its first id
GROUPS = []
ID = {}
_n = FIRST
for key, what, pack, files, how in _GROUPS:
    GROUPS.append((_n, key, what, pack, files, how))
    ID[key] = _n
    _n += len(files)
LAST = _n - 1

# P34's first set (0x3C40-0x3C6E, 15424-15470): already shipped PNGs, read back from the package for the renders
P34_FIRST, P34_LAST = 0x3C40, 0x3C6E
ART_DIR = 'D:/UO/golems/Bronze/ShatteredLegacy/player-package/vendor/shattered-legacy-art/art'


def load(path, how):
    """The converted frame as RGBA, as anchor-art-frames.py writes it (format and black only)."""
    import numpy as np
    from PIL import Image
    img = Image.open(path)
    if how == 'a':
        return Image.fromarray(np.array(img.convert('RGBA')))
    rgb = np.array(img.convert('RGB'))
    alpha = np.where((rgb == 0).all(axis=2), 0, 255).astype(np.uint8)
    out = np.dstack([rgb, alpha]); out[alpha == 0, :3] = 0
    return Image.fromarray(out)


def images():
    """{id: RGBA image} for every winter ID: this set converted from its sources, P34's set from its shipped PNGs."""
    import os
    from PIL import Image
    out = {}
    for first, key, what, pack, files, how in GROUPS:
        for k, f in enumerate(files):
            out[first + k] = load(f, how)
    for i in range(P34_FIRST, P34_LAST + 1):
        p = os.path.join(ART_DIR, '%d.png' % i)
        if os.path.exists(p):
            out[i] = Image.open(p).convert('RGBA')
    return out


if __name__ == '__main__':
    for first, key, what, pack, files, how in GROUPS:
        print('%d-%d 0x%04X %-14s %s' % (first, first + len(files) - 1, first, key, what))
    print('IDs %d-%d (0x%04X-0x%04X), %d; gump %d' % (FIRST, LAST, FIRST, LAST, LAST - FIRST + 1, GUMP_ID))
