# P62 server red run: break KitsuneEarsTail.cs three ways at once, run build.sh --tests-only, restore (SHA-256 checked).
#   s1 the female check never refuses       -> fact 2 (a man puts it on)
#   s2 the item goes on Helm, not Earrings -> facts 1 and 2
#   s3 the server record names Animation 4784 -> fact 3
import hashlib, os, shutil, subprocess

K = r'D:\ShatteredLegacy\server\customizations\KitsuneEarsTail.cs'
MUT = [('if (!from.Female)', 'if (!from.Female && false)'),
       ('        Layer = WornLayer;', '        Layer = Server.Layer.Helm;'),
       ('TileName, TileFlags, TileWeight, (int)WornLayer, AnimationId, 0, 0, TileHeight',
        'TileName, TileFlags, TileWeight, (int)WornLayer, AnimationId + 1, 0, 0, TileHeight')]
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
h0 = sha(K)
text = open(K, 'rb').read().decode('ascii')
for old, new in MUT:
    assert text.count(old) == 1, old
    text = text.replace(old, new)
shutil.copyfile(K, K + '.p62bak')
try:
    open(K, 'wb').write(text.encode('ascii'))
    with open(r'D:\UO\cc-p62-work\build-red.log', 'w') as log:
        r = subprocess.run([r'C:\Program Files\Git\bin\bash.exe', 'docker/uo/build.sh', '--tests-only',
                            '--builder-tag', 'sl-uo-builder:cc-p62-red'],
                           cwd=r'D:\ShatteredLegacy', stdout=log, stderr=subprocess.STDOUT)
    print('build.sh exit', r.returncode)
finally:
    shutil.copyfile(K + '.p62bak', K)
    os.remove(K + '.p62bak')
    assert sha(K) == h0, 'NOT RESTORED'
    print('restored', h0[:12])
for line in open(r'D:\UO\cc-p62-work\build-red.log', encoding='utf-8', errors='replace'):
    if ('KitsuneEarsTail' in line and ('Failed ' in line or 'Passed ' in line)) or 'Expected:' in line or \
            'Actual:' in line or line.strip().startswith(('Passed:', 'Failed:', 'Total tests')):
        print(line.rstrip())
