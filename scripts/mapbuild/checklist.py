"""The pre-render checklist (notes/map-building-playbook.md section 4): the checks a builder runs before showing anyone
a picture. Each function returns (ok, detail). The driver for a build (for the Burrows,
notes/cc-P167-tools/checklist.py) calls them with that build's sets and prints the table."""
import collections

from mapbuild import walls as W


def walls_against_test_room(wall_sets):
    """Build a 5 x 5 room in every wall set and check the four corners: NW post, NE east-west piece, SW north-south
    piece, SE corner piece, and that every run tile carries exactly one piece of the right kind."""
    bad = []
    for name, ws in wall_sets.items():
        fl = {(x, y) for x in range(1, 6) for y in range(1, 6)}
        statics, ring = W.walls_for(fl, set(), ws)
        by = collections.defaultdict(list)
        for (x, y, z, tid, role) in statics:
            by[(x, y)].append(role)
        want = {(0, 0): ['post'], (6, 0): ['ew'], (0, 6): ['ns'], (6, 6): ['corner']}
        for c, roles in want.items():
            if by.get(c) != roles:
                bad.append((name, c, by.get(c), roles))
        for x in range(1, 6):
            if by.get((x, 0)) != ['ew'] or by.get((x, 6)) != ['ew']:
                bad.append((name, 'row', x, by.get((x, 0)), by.get((x, 6))))
            if by.get((0, x)) != ['ns'] or by.get((6, x)) != ['ns']:
                bad.append((name, 'column', x, by.get((0, x)), by.get((6, x))))
    return not bad, bad or '%d wall sets, 5 x 5 rooms: corners post / ew / ns / corner, runs single pieces' % len(wall_sets)


def no_diagonal_runs(wall_tiles):
    """A wall tile with no orthogonal wall neighbour but a diagonal one is a stair-step (OSI never steps a wall
    diagonally). Returns the offenders."""
    ws = set(wall_tiles)
    bad = []
    for (x, y) in ws:
        orth = any((x + a, y + b) in ws for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        diag = any((x + a, y + b) in ws for a, b in ((1, 1), (-1, 1), (1, -1), (-1, -1)))
        if diag and not orth:
            bad.append((x, y))
    return not bad, bad or '%d wall tiles, none joined only diagonally' % len(ws)


def rows_straight(statics, rows, facing_groups):
    """Every furniture row (a 1-tile-thick obstacle rect) must be contiguous, on one Z, and drawn from one facing
    group. rows: [(name, (x1, y1, x2, y2))]; facing_groups: {groupName: set(ids)}; statics: [(x, y, z, id, why)]."""
    by = collections.defaultdict(list)
    for s in statics:
        by[(s[0], s[1])].append((s[2], s[3]))
    bad = []
    for name, (x1, y1, x2, y2) in rows:
        cells = [(x, y) for x in range(x1, x2 + 1) for y in range(y1, y2 + 1)]
        zs = set()
        groups = collections.Counter()
        for c in cells:
            if not by.get(c):
                bad.append((name, 'empty tile', c))
                continue
            for z, tid in by[c]:
                zs.add(z)
                for g, ids in facing_groups.items():
                    if tid in ids:
                        groups[g] += 1
        if len(zs) > 1:
            bad.append((name, 'mixed Z', sorted(zs)))
        if len(groups) > 1:
            bad.append((name, 'mixed facings', dict(groups)))
    return not bad, bad or '%d rows contiguous, one Z, one facing each' % len(rows)


def corners_dressed(corner_report):
    """corner_report: {zone: Counter(concave=.., 'concave dressed'=..)}; every concave corner must be dressed."""
    bad = {z: (c['concave'], c.get('concave dressed', 0)) for z, c in corner_report.items() if c.get('concave dressed', 0) < c['concave']}
    total = sum(c['concave'] for c in corner_report.values())
    return not bad, bad or '%d inner corners, every one dressed' % total


def variety(statics, skip_why=('wall',)):
    """Distinct ids by category, and orthogonally adjacent identical pieces among the decor (the never-two-alike rule;
    walls excluded). Returns (ok, detail) with ok when no adjacent identical decor pieces."""
    by = {}
    cats = collections.defaultdict(set)
    for (x, y, z, tid, why) in statics:
        if any(w in why for w in skip_why):
            continue
        by[(x, y, tid)] = why
        cats[why.split(':')[0].split(' corner')[0]].add(tid)
    dup = []
    for (x, y, tid), why in by.items():
        for a, b in ((1, 0), (0, 1)):
            if (x + a, y + b, tid) in by:
                dup.append((x, y, '0x%04X' % tid, why))
    distinct = len({k[2] for k in by})
    return not dup, dict(distinct_decor_ids=distinct, categories=len(cats), adjacent_identical=dup[:12], adjacent_identical_count=len(dup))


def transitions(slope_flags):
    return not slope_flags, slope_flags[:10] or 'no tile over the slope limit'


def gate(same):
    return bool(same), 'walkable floor, openings and wall tiles equal the previous build' if same else 'the walkable set changed'


def frames_all(frame_report, openings_groups):
    framed = len(frame_report)
    return framed == openings_groups, '%d opening groups, %d framed or passages' % (openings_groups, framed)


def table(results):
    """results: [(name, ok, detail)] -> text table."""
    lines = ['| Check | Result | Detail |', '|---|---|---|']
    for name, ok, detail in results:
        d = str(detail)
        if len(d) > 160:
            d = d[:157] + '...'
        lines.append('| %s | %s | %s |' % (name, 'PASS' if ok else 'FAIL', d.replace('|', '/')))
    return '\n'.join(lines)
