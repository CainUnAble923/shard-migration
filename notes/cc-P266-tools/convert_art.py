# cc-P266 WRITES player-package/vendor/shattered-legacy-art/art/<id>.png for this set's 47 IDs, through
# scripts/anchor-art-frames.py --keep-geometry --black-transparent (every source is a 24-bit BMP whose black means
# transparent): format and black only, and the tool re-reads each PNG and checks it pixel for pixel. Also WRITES
# gumps/22469.png, the advent calendar gump: the 400 x 400 BMP re-encoded as an opaque PNG (it has no pure black
# pixel, and a gump is a solid picture). art_src.py is the table.
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import art_src as S
SL = 'D:/UO/golems/Bronze/ShatteredLegacy'
OUT = SL + '/player-package/vendor/shattered-legacy-art/art'
GUMPS = SL + '/player-package/vendor/shattered-legacy-art/gumps'
TOOL = SL + '/scripts/anchor-art-frames.py'
if __name__ == '__main__':
    for first, key, what, pack, files, how in S.GROUPS:
        extra = ['--black-transparent'] if how == 'bt' else []
        r = subprocess.run([sys.executable, '-P', TOOL, '--files'] + files + ['--first-id', str(first), '--out', OUT,
                            '--keep-geometry'] + extra + sys.argv[1:], capture_output=True, text=True)
        print(key, (r.stdout.strip() or r.stderr.strip()).replace('\n', ' | ')[:200])
        if r.returncode: sys.exit(r.returncode)
    import numpy as np
    from PIL import Image
    src = Image.open(S.GUMP_SRC).convert('RGB')
    a = np.array(src)
    assert a.shape == (400, 400, 3), a.shape
    assert int(((a == 0).all(axis=2)).sum()) == 0, 'the gump has pure black pixels; decide whether they mean transparent'
    out = np.dstack([a, np.full(a.shape[:2], 255, np.uint8)])
    p = os.path.join(GUMPS, '%d.png' % S.GUMP_ID)
    Image.fromarray(out).save(p, optimize=True)
    back = np.array(Image.open(p).convert('RGBA'))
    assert (back[..., :3] == a).all() and (back[..., 3] == 255).all()
    print('gump', S.GUMP_ID, 'written and re-read:', p, back.shape)
