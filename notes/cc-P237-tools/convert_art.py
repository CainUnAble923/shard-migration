# cc-P237 WRITES player-package/vendor/shattered-legacy-art/art/<id>.png for this set's IDs, through
# scripts/anchor-art-frames.py --keep-geometry (and --black-transparent for the 24-bit BMPs whose black means
# transparent). Format and black only; the tool re-reads each PNG and checks it pixel for pixel. art_src.py is the table.
import subprocess, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import art_src as S
SL = 'D:/UO/golems/Bronze/ShatteredLegacy'
OUT = SL + '/player-package/vendor/shattered-legacy-art/art'
TOOL = SL + '/scripts/anchor-art-frames.py'
if __name__ == '__main__':
    for first, key, what, pack, files, how in S.GROUPS:
        extra = ['--black-transparent'] if how == 'bt' else []
        r = subprocess.run([sys.executable, '-P', TOOL, '--files'] + files + ['--first-id', str(first), '--out', OUT,
                            '--keep-geometry'] + extra + sys.argv[1:], capture_output=True, text=True)
        print(key, (r.stdout.strip() or r.stderr.strip()).replace('\n', ' | ')[:200])
        if r.returncode: sys.exit(r.returncode)
