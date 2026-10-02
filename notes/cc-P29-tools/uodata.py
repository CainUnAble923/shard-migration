# cc-P29: load the client map / statics / tiledata from either the server's client data (7.0.114.40) or EA's
# current install (7.0.117.0), through uorender.py's readers (the same ones P15 and P27 used). Read only.
import struct
SERVER = r'D:/ShatteredLegacy/client-data/classic-client'
EA = r'D:/UO/UltimaOnlineVanilla'
_SRC = open(r'D:/ShatteredLegacy/design/mine-camp-tents/uorender.py').read().split('def persp_coeffs')[0]
_SRC = _SRC.replace('from PIL import Image, ImageDraw, ImageFont', '')

def load(cd):
    ns = {}
    exec(compile(_SRC.replace("os.path.expanduser('~/mnt/ShatteredLegacy/client-data/classic-client')", repr(cd)), 'uor', 'exec'), ns)
    return ns

IMP, WET, SURF, BRIDGE, WALL, BG, FOLIAGE = 0x40, 0x80, 0x200, 0x400, 0x10, 0x1, 0x20000

def flagnames(f):
    names = {0x1:'Background',0x2:'Weapon',0x4:'Transparent',0x8:'Translucent',0x10:'Wall',0x20:'Damaging',
             0x40:'Impassable',0x80:'Wet',0x200:'Surface',0x400:'Bridge',0x800:'Generic',0x1000:'Window',
             0x2000:'NoShoot',0x4000:'ArticleA',0x8000:'ArticleAn',0x10000:'Internal',0x20000:'Foliage',
             0x40000:'PartialHue',0x100000:'Map',0x200000:'Container',0x400000:'Wearable',0x800000:'LightSource',
             0x1000000:'Animation',0x2000000:'HoverOver',0x8000000:'Armor',0x10000000:'Roof',0x20000000:'Door',
             0x40000000:'StairBack',0x80000000:'StairRight'}
    return '|'.join(n for b, n in names.items() if f & b) or '0'
