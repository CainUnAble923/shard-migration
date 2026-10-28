# cc-P678 read only: checks every row of placement.json on SoS Haven (rules.check: the P266 rules by mode, on the
# SoS files, plus the walk), then the walk with every blocking row in place, and writes validate.out.txt (the notes
# table, old place and new). Exit 1 if any row fails or the decor cuts any tile off from the start.
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rules as R, protected as PR


def main():
    rows = json.load(open(os.path.join(HERE, 'placement.json')))
    keys, taken, bad = set(), {}, 0
    out = ['| key | area | old x,y,z | new x,y,z | item | layer | mode | why | check |', '|---|---|---|---|---|---|---|---|---|']
    for r in rows:
        errs = R.check(r, taken)
        if r['key'] in keys: errs.append('duplicate key')
        keys.add(r['key']); taken[(r['x'], r['y'])] = r['key']
        bad += bool(errs)
        out.append('| %s | %s | %d,%d,%d | %d,%d,%d | 0x%04X %s | %s | %s | %s | %s |' % (
            r['key'], r['area'], r['oldx'], r['oldy'], r['oldz'], r['x'], r['y'], r['z'], r['itemId'], r['name'], r['layer'],
            r['mode'], r['why'], 'ok' if not errs else 'FAIL: ' + ' / '.join(errs)))
    cut = R.walk_cut(rows)
    out.append('')
    out.append('%d rows, %d failing. Walk from the start %d,%d: %d tiles reached before the decor; %s.' % (
        len(rows), bad, R.START[0], R.START[1], len(R.REACH),
        'none cut off with every blocking row in place (%d blocking rows)' % sum(1 for r in rows if r['itemId'] in R.BLOCKING and r['mode'] not in ('wall', 'wallout', 'post', 'table'))
        if not cut else 'CUT OFF by the blocking rows: %s' % cut[:40]))
    out.append('Protected tiles: %d (seeded literals read now from the code copy\'s customizations, incl. ClusterFCommunityArtLayout.cs and ClusterFHalloweenDecorLayout.cs).' % len(PR.P))
    text = '\n'.join(out)
    print(text)
    open(os.path.join(HERE, 'validate.out.txt'), 'w', encoding='ascii', newline='\n').write(text + '\n')
    return 1 if bad or cut else 0


if __name__ == '__main__':
    sys.exit(main())
