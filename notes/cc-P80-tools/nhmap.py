import sys, struct, re, glob, importlib.util
spec=importlib.util.spec_from_file_location('uor', r'D:/ShatteredLegacy/design/mine-camp-tents/uorender.py')
src=open(r'D:/ShatteredLegacy/design/mine-camp-tents/uorender.py').read().replace("os.path.expanduser('~/mnt/ShatteredLegacy/client-data/classic-client')","r'D:/ShatteredLegacy/client-data/classic-client'")
src=src.split('def persp_coeffs')[0]
ns={}; exec(compile(src.replace('from PIL import Image, ImageDraw, ImageFont',''),'uor','exec'),ns)
M=ns['Map'](1); T=ns['Tiles']()
def cliloc():
    d=open(r'D:/ShatteredLegacy/client-data/classic-client/Cliloc.enu','rb').read(); o=6; c={}
    while o<len(d):
        n,fl,ln=struct.unpack_from('<iBH',d,o); o+=7; c[n]=d[o:o+ln].decode('utf8','replace'); o+=ln
    return c
if __name__=='__main__':
    C=cliloc()
    # sign art id -> shop labels used elsewhere in pinned decoration
    lab={}
    for f in glob.glob(r'D:/UO/ModernUO-pinned/Distribution/Data/Decoration/**/*.cfg',recursive=True):
        for m in re.finditer(r'LocalizedSign (0x[0-9A-Fa-f]+) \(LabelNumber=(\d+)\)',open(f,errors='replace').read()):
            lab.setdefault(int(m.group(1),16),set()).add(C.get(int(m.group(2)),'?'))
    X0,X1,Y0,Y1=3400,3560,2400,2760
    for bx in range(X0>>3,(X1>>3)+1):
        for by in range(Y0>>3,(Y1>>3)+1):
            for (sid,sx,sy,sz,hue) in M.statics(bx,by):
                if 'sign' in T.sname[sid].lower() and sid in lab:
                    print(f'{bx*8+sx},{by*8+sy},{sz} 0x{sid:X} {sorted(lab[sid])[:4]}')
