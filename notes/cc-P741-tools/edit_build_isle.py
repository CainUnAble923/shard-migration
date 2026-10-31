"""cc-P741: edits build_isle.py in place (run once): the OSI shore rule (surf on the first sand, sand at the sea's
height) and the coast smoothing (no one-tile notch or spur)."""
import os, re
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cc-P662-tools', 'build_isle.py')
s = open(p, encoding='utf-8').read()

old1 = "    water = {c for c, v in d.items() if v > 0}\n"
new1 = '''    water = {c for c, v in d.items() if v > 0}
    # cc-P741 (Chase 10-30: "shoreline is not fluid, it's choppy"): no one-tile notch or spur. A sea cell with land
    # on 3 or 4 of its sides becomes land, a land cell with sea on 3 or 4 sides becomes sea, until none is left; and
    # the coast's stairs are evened (smooth_coast), so the shore runs in whole runs, not single-tile teeth
    if RULES.get('coastSmooth'):
        water = smooth_coast(water, set(d), RULES['coastSmooth'])
'''
assert old1 in s
s = s.replace(old1, new1, 1)

i = s.index("    shore_rule = json.load(open(os.path.join(HERE, 'shore-rule.json')))")
j = s.index("    report['shore'] = dict(shore_log)")
old_block = s[i:j]
indented = ''.join(('    ' + l if l.strip() else l) for l in old_block.splitlines(True))
new_block = '''    if RULES.get('shoreRule') == 'osi-land':
        shore_log = osi_land_shore(cls, land, put, stream('shore'), deck_set | landing | dock_dry, L['seaZ'])
    else:
''' + indented
s = s[:i] + new_block + s[j:]

helpers = '''

# ------------------------------------------------------------------------------------------------ cc-P741: the coast

NB8 = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
N4 = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def smooth_coast(water, area, R):
    """No one-tile notch or spur: flip a cell that has the other kind on 3 or 4 of its 4 sides, and (R['stairs'])
    fill the inside corner of a one-tile stair step, so a diagonal coast takes OSI's look of short runs, until stable.
    The cells R['keepLand'] (the buildings' margins are forced land in shape()) are never made sea."""
    water = set(water)
    for _ in range(50):
        flip_land, flip_sea = set(), set()
        for c in area:
            k = sum((c[0] + a, c[1] + b) in water or (c[0] + a, c[1] + b) not in area for a, b in N4)
            if c in water and k <= 1:
                flip_land.add(c)
            elif c not in water and k >= 3:
                flip_sea.add(c)
        if not flip_land and not flip_sea:
            break
        water -= flip_land
        water |= flip_sea
    return water


def osi_shore_table():
    """notes/cc-P741-tools/shore-survey741.json: OSI's gentle sandy coasts on stock Trammel (survey_shore741.py)."""
    t = json.load(open(os.path.join(REPO, 'notes', 'cc-P741-tools', 'shore-survey741.json')))
    return t['land'], t['sea']


def osi_land_shore(cls, land, put, rng, no_shore, sea_z):
    """cc-P741: the shore as OSI lays its gentle sandy coasts (survey_shore741.py, 704 sand cells on stock
    Trammel): the first sand tiles beside the sea stand at the sea's height (land Z -5, beachZ '1') and carry the surf
    piece for their edge, chosen by the cell's 8-neighbour sea pattern: sea to the west 0x179D/0x179E, sea to the
    south 0x179F/0x17A0, the inside corner (sea south and west) 0x17A9, sea only on the south-west diagonal 0x17A5,
    and so on; sea to the north or east only gets nothing, as on OSI's coasts (the sand meets the water). The sea's
    cells keep their water land and take OSI's plain water static where OSI lays one. A pattern OSI shows fewer than
    5 times falls back to the piece for its sea side. Returns the log."""
    land_t, sea_t = osi_shore_table()
    log = collections.Counter()
    sea = lambda c: cls.get(c, 'w') == 'w'
    pattern = lambda c: ''.join('S' if sea((c[0] + a, c[1] + b)) else '.' for a, b in NB8)

    def pick(options, total):
        top = options[0][1]
        keep = [(comp, n) for comp, n in options if n * 4 >= top]
        r = rng.uniform(0, sum(n for _, n in keep))
        for comp, n in keep:
            r -= n
            if r <= 0:
                return comp
        return keep[-1][0]

    fallback = {'W': ['179D', '179E'], 'S': ['179F', '17A0'], 'SW': ['17A9'], 'dSW': ['17A5']}
    for c in sorted(cls):
        if c in no_shore:
            continue
        pat = pattern(c)
        if 'S' not in pat or pat == 'SSSSSSSS':
            continue
        if sea(c):
            opts = sea_t.get(pat)
            if opts and sum(n for _, n in opts) >= 5:
                comp = pick(opts, None)
                for p in [q for q in comp.split('+') if q][:1]:
                    tid, dz = p.split('@')
                    put(c[0], c[1], sea_z + int(dz) - (-5), int(tid, 16), 'shore water sea ' + pat)
                    log['sea ' + ('static' if comp else 'none')] += 1
            continue
        if cls[c] != 's':
            continue
        opts = land_t.get(pat)
        if opts and sum(n for _, n in opts) >= 5:
            comp = pick(opts, None)
            src = 'osi'
        else:
            w = pat[6] == 'S' or (pat[5] == 'S' and pat[7] == 'S')
            s_ = pat[4] == 'S' or (pat[3] == 'S' and pat[5] == 'S')
            side = 'SW' if (w and s_) else 'W' if w else 'S' if s_ else 'dSW' if pat[5] == 'S' else None
            comp = (rng.choice(fallback[side]) + '@-5') if side else ''
            src = 'fallback'
        for p in [q for q in comp.split('+') if q]:
            tid, dz = p.split('@')
            put(c[0], c[1], sea_z + int(dz) - (-5), int(tid, 16), 'shore water land ' + pat)
        log['land %s %s' % (src, 'piece' if comp else 'none')] += 1
    return log
'''
k = s.index('# ------------------------------------------------------------------------------------------------ the plan')
s = s[:k] + helpers.lstrip('\n') + '\n\n' + s[k:]
open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('edited')
