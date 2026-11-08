r"""cc-P817: the isle bank's two map-static changes, in the shipped patch and in the isle driver's data, together.

    python -P bank_statics.py <trammel.mapops> <isle-sets.json> [--check]

  - the strongbox 0x09A8 (2472) moves from 6766,3974 (by the east wall, apart from the other chests) to 6762,3973, on
    the back wall under the north torch, behind Merrin, between the practice bank box (6761,3973, a server prop) and the
    north window's floor tile (6764,3973) is left clear;
  - the potted plant 0x11CA (4554) inside, at 6766,3978, is removed: it crowded the south-east corner beside the standing
    candelabra 0x0B26 (6766,3979); the plant by the door outside (6760,3981) stays.

The patch keeps one line per static, sorted by x, y, z within each block (block 845,496 holds both chests' rows); the
block fingerprints are EA's base, not our lines, so moving our S+ lines leaves them right. isle-sets.json is the
driver's source (notes/cc-P662-tools/build_isle.py), so a rebuild of the isle lays the same."""
import json
import sys

ops_path, sets_path = sys.argv[1], sys.argv[2]
check = '--check' in sys.argv

STRONGBOX_OLD = 'S+ 6766 3974 0 2472 0'
STRONGBOX_NEW = 'S+ 6762 3973 0 2472 0'
PLANT = 'S+ 6766 3978 0 4554 0'
AFTER = 'S+ 6762 3973 0 1302 0'   # the floor tile at 6762,3973: the strongbox line goes right after it

raw = open(ops_path, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in raw else '\n'
lines = raw.split(nl)
have = set(lines)
if check:
    ok = STRONGBOX_NEW in have and STRONGBOX_OLD not in have and PLANT not in have
    print('mapops:', 'done' if ok else 'NOT done')
else:
    for need in (STRONGBOX_OLD, PLANT, AFTER):
        if lines.count(need) != 1:
            raise SystemExit('trammel.mapops: %r is there %d times, not once' % (need, lines.count(need)))
    lines.remove(STRONGBOX_OLD)
    lines.remove(PLANT)
    lines.insert(lines.index(AFTER) + 1, STRONGBOX_NEW)
    open(ops_path, 'w', encoding='utf-8', newline='').write(nl.join(lines))
    print('mapops: strongbox moved, inside plant removed')

# isle-sets.json keeps one line per section, so it is edited as text (a re-dump would re-lay the whole file).
BOX_OLD = '["0x09A8", 6766, 3974, 0, "strongbox"]'
BOX_NEW = '["0x09A8", 6762, 3973, 0, "strongbox, back wall under the north torch (cc-P817)"]'
PLANT_ROW = '["0x11CA", 6766, 3978, 0, "potted plant"], '
text = open(sets_path, encoding='utf-8', newline='').read()
if check:
    print('isle-sets:', 'done' if BOX_NEW in text and BOX_OLD not in text and PLANT_ROW not in text else 'NOT done')
else:
    if text.count(BOX_OLD) != 1 or text.count(PLANT_ROW) != 1:
        raise SystemExit('isle-sets.json: the bank strongbox or the inside plant is not where P720 put them')
    text = text.replace(BOX_OLD, BOX_NEW).replace(PLANT_ROW, '')
    sets = json.loads(text)
    bank = sets['interiors']['bank']['pieces']
    assert any(p[0] == '0x09A8' and p[1:3] == [6762, 3973] for p in bank)
    assert not any(p[0] == '0x11CA' and p[1:3] == [6766, 3978] for p in bank)
    open(sets_path, 'w', encoding='utf-8', newline='').write(text)
    print('isle-sets: strongbox moved, inside plant removed')
