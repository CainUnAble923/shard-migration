# cc-P675: the map patch's SOURCE.txt says what the patch applies to now (the SoS map) and what left it.
p = r'D:\UO\golems\Iron\ShatteredLegacy\player-package\vendor\shattered-legacy-map\SOURCE.txt'
s = open(p, newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
old = 'rocks and debris on the rim (0x1771-0x177C, 0x0C2E-0x0C30, all passable): 49 S+ lines added, the' + nl + \
      "                 hole's one S+ line gone, one more B line." + nl
assert s.count(old) == 1
add = [
    "                 cc-P662, 2026-10-26: the Wakening Isle (x 6594-6865, y 3905-4049, site A of cc-P673).",
    "                 cc-P675, 2026-10-28 (SoS swap S2): RE-BASED onto the Siege of Sosaria map by Zigholtul",
    "                 (player-package/vendor/sos-trammel-map; pristine hashes in shard-migration",
    "                 notes/cc-P675-tools/sos-base/ORIGINAL-SHA256.txt). The Burrows' 210 blocks and the isle's 665",
    "                 apply as they were (both sit on void in his map; no block drifted). Dropped: the way in from Old",
    "                 Haven (its 2 blocks; that bank is the author's Second Bank of Haven now, and cc-P678's cellar",
    "                 hatch is a server item) and cc-P276's four farm removals (the farm is on the isle; the old spot",
    "                 is his forest). Every B line now fingerprints his blocks, not EA's.",
]
s = s.replace(old, old + nl.join(add) + nl)
s = s.replace('python -P scripts/mapbuild/mapops.py diff <the shard\'s client-data copy> <the scratch build> 1 trammel.mapops',
              'python -P scripts/mapbuild/mapops.py diff <a pristine SoS copy> <the scratch build> 1 trammel.mapops')
open(p, 'w', newline='').write(s)
print('ok')
