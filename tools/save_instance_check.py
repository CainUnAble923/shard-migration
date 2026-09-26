"""Read-only: does any save artefact on this machine hold an instance of the named types?

Type tables (SerializedTypes.db) are parsed for Server.* names; Backups/Automatic snapshots and the
Archives tarballs are searched the same way (tar.zst stream-decompressed, members matching
SerializedTypes.db read). A positive control (Server.Items.Dagger) must appear in each, or the read
is not trusted.
"""
import os, re, sys, tarfile, io

ROOT = r'D:\ShatteredLegacy\server\lib\uo\modernuo'
WANT = sys.argv[1:] or ['SpiritualityHelm', 'ValorGauntlets', 'BestialKilt', 'VirtuososKilt']
CONTROL = 'Server.Items.Dagger'
NAME = re.compile(rb'Server\.[A-Za-z0-9_.]+')


def report(label, data):
    names = {x.decode() for x in NAME.findall(data)}
    ctl = CONTROL in names
    hits = sorted(n for n in names if n.split('.')[-1] in WANT)
    print(f'{label}: {len(names)} names, control {"present" if ctl else "ABSENT"}, hits {hits or "none"}')


for sub in ('Saves', 'Saves-test'):
    p = os.path.join(ROOT, sub, 'SerializedTypes.db')
    if os.path.exists(p):
        report(sub, open(p, 'rb').read())

auto = os.path.join(ROOT, 'Backups', 'Automatic')
for d in sorted(os.listdir(auto)):
    p = os.path.join(auto, d, 'SerializedTypes.db')
    if os.path.exists(p):
        report('Backups/Automatic/' + d, open(p, 'rb').read())
    else:
        print('Backups/Automatic/' + d, ': no SerializedTypes.db;', os.listdir(os.path.join(auto, d)))

try:
    import zstandard
except ImportError:
    zstandard = None
arch = os.path.join(ROOT, 'Archives')
for kind in sorted(k for k in os.listdir(arch) if os.path.isdir(os.path.join(arch, k))):
    files = sorted(f for f in os.listdir(os.path.join(arch, kind)) if f.endswith('.tar.zst'))
    for f in files[-2:]:
        p = os.path.join(arch, kind, f)
        if zstandard is None:
            print(f'Archives/{kind}/{f}: zstandard not installed, not read')
            continue
        with open(p, 'rb') as fh:
            r = zstandard.ZstdDecompressor().stream_reader(fh)
            with tarfile.open(fileobj=r, mode='r|') as tf:
                found = False
                for m in tf:
                    if m.name.endswith('SerializedTypes.db'):
                        report(f'Archives/{kind}/{f}:{m.name}', tf.extractfile(m).read())
                        found = True
                if not found:
                    print(f'Archives/{kind}/{f}: no SerializedTypes.db member')
