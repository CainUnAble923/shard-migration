"""cc-P679 (SoS swap S4): every public moongate and every Trammel and Felucca teleporter end stands on the SoS land.

    SL_SHARD_REPO=<code copy> SL_SOS_MAP=<overlay> [SL_STOCK_TRAMMEL=<EA Trammel folder>] python -P tools/tests/test_s4_gates.py

SL_SOS_MAP holds the server's map overlay (map1LegacyMUL.uop, statics1.mul, staidx1.mul: the SoS base with the code
copy's trammel.mapops; docker/uo/Build-MapOverlay.ps1 writes it). Trammel and Felucca both read it (SosMaps.cs).
SL_STOCK_TRAMMEL is EA's own Trammel (default P167's scratch client), for stock's quirks. Skipped without the overlay.
MAPBUILD_CLIENT names the client folder whose tiledata.mul is read. The spot rule is P677's (notes/cc-P677-tools/spots.py:
a standing surface, nothing impassable or solid in the 16 Z above).

  1. Every PMList gate on Trammel and Felucca (pinned's PublicMoongate.cs with the code copy's
     PublicMoongate-sos-gates.patch, if it has one; New Haven's from HavenSpots.cs) stands exactly on a floor: its Z is
     one of the tile's open standing Zs (Magincia's is pinned's GetAverageZ, read off the map as the server does).
  2. Every Trammel or Felucca end of the teleporters the server makes ([TelGen: the code copy's
     server/data/teleporters-sos.json in place of pinned's Trammel and Felucca entries, or pinned's own when there is no
     such file) stands on the SoS land, and every source end fires (pinned Mobile.Move: an item 1 high is entered from
     a floor at or up to 14 below it; notes/cc-P679-tools/tele.py). An end that fails passes only as stock's own
     quirk: it fails the same way on EA's Trammel, SoS left its 3 x 3 alone, and pinned has that very end on Trammel.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

DOCS = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TOOLS = os.path.join(DOCS, 'notes', 'cc-P679-tools')
sys.path.insert(0, TOOLS)
SHARD = os.environ.get('SL_SHARD_REPO', r'D:\ShatteredLegacy')
SOS = os.environ.get('SL_SOS_MAP', '')
STOCK = os.environ.get('SL_STOCK_TRAMMEL', r'D:\UO\cc-p167-work\scratch-client')
PINNED = r'D:\UO\ModernUO-pinned'
READY = bool(SOS) and os.path.exists(os.path.join(SOS, 'staidx1.mul'))
GATE_FILE = 'Projects/UOContent/Items/Misc/PublicMoongate.cs'
SOS_MAPS = ('Trammel', 'Felucca')


def gates_source():
    """PublicMoongate.cs as the code copy builds it."""
    src = os.path.join(PINNED, *GATE_FILE.split('/'))
    patch = os.path.join(SHARD, 'server', 'patches', 'PublicMoongate-sos-gates.patch')
    if not os.path.exists(patch):
        return open(src, encoding='utf-8').read()
    tmp = tempfile.mkdtemp()
    try:
        dst = os.path.join(tmp, *GATE_FILE.split('/'))
        os.makedirs(os.path.dirname(dst))
        shutil.copy(src, dst)
        with open(patch, 'rb') as f:
            subprocess.run(['patch', '-p1', '--fuzz=0', '--batch', '--forward'], cwd=tmp, stdin=f, check=True,
                           stdout=subprocess.DEVNULL)
        return open(dst, encoding='utf-8').read()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def haven_gate():
    text = open(os.path.join(SHARD, 'server', 'customizations', 'Tutorial', 'HavenSpots.cs'), encoding='utf-8').read()
    m = re.search(r'Point3D PublicMoongate = new\((\d+), (\d+), (-?\d+)\)', text)
    return tuple(int(v) for v in m.groups())


def gates():
    """{facet: [(number, x, y, z or 'avg')]} for Trammel and Felucca."""
    text = gates_source()
    out = {}
    for facet in SOS_MAPS:
        block = re.search(r'public static readonly PMList %s =(.*?)\);' % facet, text, re.S).group(1)
        rows = []
        for m in re.finditer(r'new PMEntry\((.*?), (\d{7})\)', block):
            loc, number = m.group(1), int(m.group(2))
            p = re.match(r'new Point3D\((\d+), (\d+), (-?\d+)\)$', loc)
            a = re.match(r'new Point3D\((\d+), (\d+), Map\.\w+\.GetAverageZ\(\1, \2\)\)$', loc)
            if p:
                rows.append((number,) + tuple(int(v) for v in p.groups()))
            elif a:
                rows.append((number, int(a.group(1)), int(a.group(2)), 'avg'))
            elif loc.endswith('HavenSpots.PublicMoongate'):
                rows.append((number,) + haven_gate())
            else:
                raise AssertionError('unread PMEntry: ' + m.group(0))
        out[facet] = rows
    return out


def teleporters():
    """The entries [TelGen makes with an end on Trammel or Felucca."""
    pinned = json.load(open(os.path.join(PINNED, 'Distribution', 'Data', 'teleporters.json'), encoding='utf-8'))
    on = [e for e in pinned if e['src']['map'] in SOS_MAPS or e['dst']['map'] in SOS_MAPS]
    ours = os.path.join(SHARD, 'server', 'data', 'teleporters-sos.json')
    return pinned, (json.load(open(ours, encoding='utf-8')) if os.path.exists(ours) else on)


@unittest.skipUnless(READY, 'SL_SOS_MAP (the server map overlay) not set')
class OnSos(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import changed
        import tele
        cls.tele = tele
        cls.both = changed.Both(SOS, STOCK)
        cls.S, cls.K = cls.both.sos, cls.both.stock

    def verdict(self, L, which, x, y, z):
        v = L.check(x, y, z)
        if v == 'ok' and which == 'src' and not self.tele.fires(L, x, y, z):
            v = 'never fires'
        return v

    def test_1_every_gate_stands_on_a_floor(self):
        bad = []
        for facet, rows in gates().items():
            self.assertEqual(9, len(rows), facet)
            for number, x, y, z in rows:
                if z == 'avg':
                    z = self.S.avgz(x, y)
                tops = self.S.open_tops(x, y)
                if z not in tops:
                    bad.append('%s %d at %d,%d,%d: floors %s' % (facet, number, x, y, z, tops))
        self.assertEqual([], bad)

    def test_2_every_teleporter_end_stands_and_every_source_fires(self):
        pinned, entries = teleporters()
        tram = {(w, *e[w]['loc']) for e in pinned for w in ('src', 'dst') if e[w]['map'] == 'Trammel'}
        bad, quirks, ends = [], 0, 0
        for e in entries:
            for which in ('src', 'dst'):
                w = e[which]
                if w['map'] not in SOS_MAPS:
                    continue
                ends += 1
                x, y, z = w['loc']
                v = self.verdict(self.S, which, x, y, z)
                if v == 'ok':
                    continue
                if (which, x, y, z) in tram and v == self.verdict(self.K, which, x, y, z) and not self.both.changed(x, y):
                    quirks += 1
                    continue
                bad.append('%s %s %d,%d,%d: %s' % (w['map'], which, x, y, z, v))
        print('\n  ends', ends, 'as stock', quirks, 'failing', len(bad))
        for b in bad:
            print('   ', b)
        self.assertEqual([], bad)


if __name__ == '__main__':
    unittest.main(verbosity=2)
