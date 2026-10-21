# cc-P237: the one table of which source file becomes which art ID (registry.csv repeats it per row). Read by
# convert_art.py, registry_rows.py, the renders and validate.py. IDs from 0x3C88 (15496), 8-aligned after the mimic
# (0x3C81), inside find-free-art.py --placeholder's run 0x3C82-0x3D11.
#   (first id, key, what, pack, [source files], how)
#   how: 'bt' = 24-bit BMP, black means transparent (--black-transparent --keep-geometry)
#        'a'  = the source has its own alpha (PNG, TIFF, 32-bit BMP): --keep-geometry only, black stays black
TP = 'D:/UO/third-party'
FC = TP + '/farm-carts/FarmCartGraphics'
OL = TP + '/oil-lantern'
MR = TP + '/marble-railings/marblerailings'
BB = TP + '/bridge-support-beam'
OE = TP + '/orc-encampment/Orc encampment/BMP'
PO = TP + '/paintings-odin/Paintings'
P2 = TP + '/paintings-odin-2'
FIRST = 0x3C88

_GROUPS = [
    # farm carts (Moonrose): made for OSI slots 6784/6785 and 6807/6808, taken here as new IDs
    ('cart-fruit-a', 'fruit cart (facing A, made for slot 6784)', 'farm-carts', [FC + '/Item_06784.tiff'], 'a'),
    ('cart-fruit-b', 'fruit cart (facing B, made for slot 6785)', 'farm-carts', [FC + '/Item_06785.tiff'], 'a'),
    ('cart-veg-a', 'vegetable cart (facing A, made for slot 6807)', 'farm-carts', [FC + '/Item_06807.tiff'], 'a'),
    ('cart-veg-b', 'vegetable cart (facing B, made for slot 6808)', 'farm-carts', [FC + '/Item_06808.tiff'], 'a'),
    # oil lantern (Ems): the three lit frames ("lantern 4.png" is the unlit lantern, not used)
    ('lantern', 'oil lantern (animated, 3 lit frames)', 'oil-lantern', [OL + '/lantern 1.bmp', OL + '/lantern 2.bmp', OL + '/lantern 3.bmp'], 'a'),
    # marble railings (OUTLANDSOwyn), named for IDs 70290 and up in his pack
    ('rail-y', 'marble railing, straight, along the tile\'s west edge (his 70321)', 'marble-railings', [MR + '/Item-70321.png'], 'a'),
    ('rail-y-post', 'marble railing with its end post, west edge (his 70324)', 'marble-railings', [MR + '/Item-70324.png'], 'a'),
    # bridge support beam (gollin)
    ('beam-ew-left', 'bridge support beam, east-west, left support', 'bridge-support-beam', [BB + '/EW_Left_Support_beam.bmp'], 'bt'),
    ('beam-ew-right', 'bridge support beam, east-west, right support', 'bridge-support-beam', [BB + '/EW_Right_Support_beam.bmp'], 'bt'),
    ('beam-ns-left', 'bridge support beam, north-south, left support', 'bridge-support-beam', [BB + '/NS_Left_Support_beam.bmp'], 'bt'),
    ('beam-ns-right', 'bridge support beam, north-south, right support', 'bridge-support-beam', [BB + '/NS_Right_Support_beam.bmp'], 'bt'),
    # orc encampment (Vrark): his finished BMPs, named for the IDs he built them for (Item 0xB2xx)
    ('orc-cage', 'orcish cage (facing 1, his 0xB2B3)', 'orc-encampment', [OE + '/Item 0xB2B3.bmp'], 'bt'),
    ('orc-fire', 'orcish campfire (facing 2, his 0xB2B8)', 'orc-encampment', [OE + '/Item 0xB2B8.bmp'], 'bt'),
    ('orc-meat', 'orcish meat hang (facing 1, his 0xB2BB)', 'orc-encampment', [OE + '/Item 0xB2BB.bmp'], 'bt'),
    ('orc-palisade-1', 'orcish palisade (facing 1, his 0xB2BF)', 'orc-encampment', [OE + '/Item 0xB2BF.bmp'], 'bt'),
    ('orc-palisade-2', 'orcish palisade (facing 2, his 0xB2C0)', 'orc-encampment', [OE + '/Item 0xB2C0.bmp'], 'bt'),
    ('orc-rug', 'orcish rug (facing 1, his 0xB2C3)', 'orc-encampment', [OE + '/Item 0xB2C3.bmp'], 'bt'),
    ('orc-tent-1', 'orcish tent, long (tent 001 facing 1, his 0xB2C7)', 'orc-encampment', [OE + '/Item 0xB2C7.bmp'], 'bt'),
    ('orc-tent-2', 'orcish tent, square (tent 002 facing 1, his 0xB2CB)', 'orc-encampment', [OE + '/Item 0xB2CB.bmp'], 'bt'),
    ('orc-tent-3', 'orcish tent, round (tent 003 facing 1, his 0xB2CF)', 'orc-encampment', [OE + '/Item 0xB2CF.bmp'], 'bt'),
    # paintings (Odin): public-domain paintings, drawn for a north wall (they face south)
    ('ptg-beata', 'painting: Beata Beatrix', 'paintings-odin', [PO + '/Beata Beatrix.bmp'], 'bt'),
    ('ptg-morgan', 'painting: Morgan le Fay', 'paintings-odin', [PO + '/Morgan le Fay.bmp'], 'bt'),
    ('ptg-ophelia', 'painting: Ophelia', 'paintings-odin', [PO + '/Ophelia.bmp'], 'bt'),
    ('ptg-galahad', 'painting: Sir Galahad at the Ruined Chapel', 'paintings-odin', [PO + '/Sir Galahad at the ruined Chapel.bmp'], 'bt'),
    ('ptg-feller', "painting: The Fairy Feller's Master-Stroke", 'paintings-odin', [PO + "/The Fairy Feller's Master-Stroke.bmp"], 'bt'),
    ('ptg-hesperides', 'painting: The Garden of the Hesperides', 'paintings-odin', [PO + '/The Garden of the Hesperides.bmp'], 'bt'),
    ('ptg-shalott', 'painting: The Lady of Shalott', 'paintings-odin', [PO + '/The Lady of Shalott.bmp'], 'bt'),
    ('ptg-lovesong', 'painting: The Love Song', 'paintings-odin', [PO + '/The Love Song.bmp'], 'bt'),
    ('ptg-towers', 'painting: The Tune of the Seven Towers', 'paintings-odin', [PO + '/The Tune of the Seven Towers.bmp'], 'bt'),
    ('ptg-roses', 'painting: Wars of the Roses', 'paintings-odin', [PO + '/Wars of the Roses.bmp'], 'bt'),
    ('ptg-nightmare', 'painting: The Nightmare', 'paintings-odin-2', [P2 + '/Nightmare.bmp'], 'bt'),
    ('ptg-circle', 'painting: The Magic Circle', 'paintings-odin-2', [P2 + '/The_Magic_Circle.bmp'], 'bt'),
]

# key -> (first id, what, pack, files, how); ids run on in table order, an animation's frames after its first id
GROUPS = []
ID = {}
_n = FIRST
for key, what, pack, files, how in _GROUPS:
    GROUPS.append((_n, key, what, pack, files, how))
    ID[key] = _n
    _n += len(files)
LAST = _n - 1


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
    """{id: RGBA image} for every ID (each frame its own ID)."""
    out = {}
    for first, key, what, pack, files, how in GROUPS:
        for k, f in enumerate(files):
            out[first + k] = load(f, how)
    return out


if __name__ == '__main__':
    for first, key, what, pack, files, how in GROUPS:
        print('%d-%d 0x%04X %-16s %s' % (first, first + len(files) - 1, first, key, what))
    print('IDs %d-%d (0x%04X-0x%04X), %d' % (FIRST, LAST, FIRST, LAST, LAST - FIRST + 1))
