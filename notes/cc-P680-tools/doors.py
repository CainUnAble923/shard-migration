"""cc-P680: is a door hanging in a doorway? The rule the fact uses (tools/tests/test_s5_decoration.py).

A door (a cfg header whose type is a door or gate: its name holds "Door" or "Gate") at x, y, z is in a doorway when:
  - along one axis, both neighbours (x-1 and x+1, or y-1 and y+1) hold a wall: a static that is a wall, a window or
    impassable (a fence, a palisade, a pillar), from 5 below the door to 15 above it, or another door (double doors,
    side by side). The statics are the map's and the cfg's own Static entries on that facet: many stock doorways are
    built from cfg walls (New Haven's plaza), which the SoS author then baked into his map;
  - and the door's own tile holds nothing impassable in that band but walls, and no wall piece at the door's own
    height (within 2 Z) other than an arch or door art: a door there would be inside a wall.
The facing is left out on purpose: the cfg's facings do not follow one rule for which side the hinge is on.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import maps  # noqa: E402

WALLISH = maps.WALL | maps.WINDOW | maps.IMP


def is_door(header):
    t = header.split(' ')[0]
    return 'Door' in t or 'Gate' in t


def walled(M, x, y, z, doors, extra):
    if (x, y) in doors:
        return True
    return any(M.flags(t) & WALLISH and -5 <= sz - z <= 15 for sz, t in M.statics(x, y) + extra.get((x, y), []))


def in_doorway(M, x, y, z, doors=frozenset(), extra=None):
    """(True, '') or (False, why). doors: the door tiles on this facet; extra: {(x, y): [(z, id)]}, the cfg's statics."""
    extra = extra or {}
    for sz, t in M.statics(x, y) + extra.get((x, y), []):
        f = M.flags(t)
        name = (M.name(t) or 'static').lower()
        if f & maps.IMP and not f & maps.DOOR and not f & maps.SURF and -5 <= sz - z <= 15 and not f & maps.WALL:
            return False, 'something impassable on its own tile: %s 0x%04X z%d' % (name, t, sz)
        if f & maps.WALL and abs(sz - z) <= 2 and 'arch' not in name and 'door' not in name:
            return False, 'inside a wall: %s 0x%04X z%d on its own tile' % (name, t, sz)
    ew = walled(M, x - 1, y, z, doors, extra) and walled(M, x + 1, y, z, doors, extra)
    ns = walled(M, x, y - 1, z, doors, extra) and walled(M, x, y + 1, z, doors, extra)
    if ew or ns:
        return True, ''
    return False, 'no wall on both sides along either axis'


def facet_layout(entries, facet, placed):
    """(door tiles, {(x, y): [(z, id)]} of cfg statics) for one facet. entries: (folder, header, x, y, z) as placed."""
    folders = ('Britannia', facet)
    doors, extra = set(), {}
    for folder, header, x, y, z in entries:
        if folder not in folders:
            continue
        if is_door(header):
            doors.add((x, y))
        elif header.split(' ')[0] in ('Static', 'LocalizedStatic'):
            m = header.split(' ')[1].split('(')[0] if ' ' in header else ''
            try:
                extra.setdefault((x, y), []).append((z, int(m, 0)))
            except ValueError:
                pass
    return doors, extra
