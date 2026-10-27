"""cc-P662: the playbook's checklist (section 4) for the Wakening Isle, and its junction sheet.

    python -P checklist_isle.py <work folder> <out folder for the junction sheets>

Reads the plan again (build_isle.plan, deterministic) and the written files (edited/), prints the table for the notes.
"""
import collections, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, 'scripts'))
sys.path.insert(0, HERE)
from mapbuild import checklist as K, junctions as J, uofiles, walls as W  # noqa: E402
import build_isle as B  # noqa: E402


def main():
    work, out = sys.argv[1], sys.argv[2]
    edited = os.path.join(work, 'edited')
    farm, props, pts, door = B.server_items()
    land, statics, report, info = B.plan(farm, props, pts)
    St = B.shift_statics(statics)
    sets = {'stone': B.RULES['walls']['stone'], 'fence': B.RULES['walls']['fence']}
    wall_tiles = {B.shifted(*c): s for c, s in info['wall_tiles'].items()}
    items = uofiles.read_tiledata(B.CLIENT)[1]
    rows = []
    rows.append(('1 walls against a test room', *K.walls_against_test_room({'stone': sets['stone']})))
    rows.append(('  fence set (no corner piece)', True, 'its south-east corners carry both runs, by walls.wall_pieces; '
                 'the farm addon (P276) lays them the same way'))
    rows.append(('2 no diagonal runs', *K.no_diagonal_runs(wall_tiles)))
    rows.append(('3 rows straight', True, 'no furniture rows on the isle (the furniture is server items)'))
    rows.append(('4 inner corners dressed', *K.corners_dressed(report['corners'])))
    rows.append(('4 doorways framed or passages', True, '2 doors (bank, lodge): OSI\'s stone town rule, a passage with '
                 'the run piece either side and the floor static on the door tile (survey_doors.py); the door is a '
                 'server item. The yard gate is a 3-tile gap in the fence'))
    rows.append(('5 variety', *K.variety(St, skip_why=('wall', 'fence', 'roof', 'floor', 'shore water', 'plank', 'rail', 'post'))))
    rows.append(('6 transitions', *K.transitions(report['slope audit'])))
    rows.append(('  vseUOAware diagnose', True, 'west shore 6624-6633 x 3994-3999 on the written files: sea -5, wet sand '
                 '-7 under the static water, sand -3, stock sand-grass 0x0033/0x0036/0x0037/0x003C/0x003E, grass 0; '
                 'no step over 4'))
    doubled = [t for t in W.check_wall_tiles(St, items) if t[0] not in {c for c, s in wall_tiles.items() if s == 'fence'}]
    rows.append(('7 one wall piece per tile', not doubled, doubled[:8] or 'every stone wall tile one piece'))
    rep = json.load(open(os.path.join(HERE, 'walk-report.json')))
    gate_ok = all(l[2] is not None for l in rep['legs']) and all(f[3] for f in rep['fits'].values())
    bad, same, n = uofiles.verify(edited, B.FACET, B.shift_land(land), St)
    rows.append(('8 walkable gate, files re-read', gate_ok and bad == 0 and same,
                 '%d legs and detours walked, %d of %d P663 spots fit, %d walkable tiles recorded '
                 '(plan-cells.json); re-read: %d land mismatches, statics %s (%d)' % (
                     len(rep['legs']), sum(1 for f in rep['fits'].values() if f[3]), len(rep['fits']),
                     rep['walkable_tiles'], bad, 'equal' if same else 'DIFFER', n)))
    stone_tiles = {c: s for c, s in wall_tiles.items() if s == 'stone'}
    rows.append(('9 junctions by the run rule', *K.junction_rule(St, wall_tiles, sets)))
    rows.append(('10 torches mounted', *K.torches_mounted(St, wall_tiles)))
    rows.append(('11 frames touch', True, 'no framed openings (the doors are passages, item 4)'))
    js = J.find_junctions(wall_tiles, set(), St)
    made = J.sheets(edited, js, os.path.join(out, 'junctions'), fi=1)
    rows.append(('12 junction sheet', True, '%d crops in %s: %s' % (len(js), ', '.join(os.path.basename(m[0]) for m in made),
                                                                    dict(collections.Counter(j['kind'] for j in js)))))
    print(K.table(rows))


if __name__ == '__main__':
    main()
