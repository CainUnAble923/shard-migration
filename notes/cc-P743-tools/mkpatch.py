"""cc-P714: makes a server/patches/*.patch from one exact replacement in a file of the patched build tree
(sl-uo-builder's /build/modernuo, copied out to <tree>), with diff -u and 3 lines of context, and checks it with
patch --dry-run --fuzz=0 (memory: hand-built hunks failed the gate).

    python -P mkpatch.py <tree> <Projects/... path> <old text file> <new text file> <out .patch>
"""
import os
import shutil
import subprocess
import sys
import tempfile

tree, rel, old_f, new_f, out = sys.argv[1:6]
old = open(old_f, encoding='utf-8').read()
new = open(new_f, encoding='utf-8').read()
src = os.path.join(tree, rel)
raw = open(src, 'rb').read()
crlf = b'\r\n' in raw
text = raw.decode('utf-8-sig' if raw.startswith(b'\xef\xbb\xbf') else 'utf-8')
bom = raw.startswith(b'\xef\xbb\xbf')
norm = text.replace('\r\n', '\n')
if norm.count(old) != 1:
    sys.exit('old text found %d times in %s' % (norm.count(old), rel))
changed = norm.replace(old, new)

STAMP = chr(9) + "2026-10-31 00:00:00.000000000 -0500"  # a tab ends a name with spaces
work = tempfile.mkdtemp()
a = os.path.join(work, 'a', rel)
b = os.path.join(work, 'b', rel)
os.makedirs(os.path.dirname(a))
os.makedirs(os.path.dirname(b))
shutil.copyfile(src, a)
data = changed.replace('\n', '\r\n') if crlf else changed
open(b, 'wb').write((b'\xef\xbb\xbf' if bom else b'') + data.encode('utf-8'))
r = subprocess.run(['diff', '-u', '--label', 'a/' + rel + STAMP, '--label', 'b/' + rel + STAMP, 'a/' + rel, 'b/' + rel],
                   cwd=work, capture_output=True)
if r.returncode != 1:
    sys.exit('diff gave %d: %s' % (r.returncode, r.stderr))
open(out, 'wb').write(r.stdout)
chk = os.path.join(work, 'chk')
os.makedirs(os.path.dirname(os.path.join(chk, rel)))
shutil.copyfile(src, os.path.join(chk, rel))
r2 = subprocess.run(['patch', '-p1', '--dry-run', '--fuzz=0', '-i', os.path.abspath(out)], cwd=chk, capture_output=True, text=True)
print(r2.stdout.strip(), r2.stderr.strip(), 'exit', r2.returncode)
shutil.rmtree(work)
sys.exit(r2.returncode)
