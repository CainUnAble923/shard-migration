"""cc-P686 (SoS swap S13): Felucca's regions on the Siege of Sosaria land, redrawn from S3's Trammel work (cc-P676).

Felucca reads Trammel's files since P675, so both facets stand on the same land and their towns must match. Writes the
whole Felucca part of the server's regions as ModernUO JSON; the server loads it in place of pinned's Felucca regions
(server/patches/RegionJsonSerializer-shard-maps.patch takes every Data/ShatteredLegacy/regions-<map>.json).

    python -P gen_felucca.py <SoS map folder> <code copy> [--check-only]

Inputs, all read only: pinned regions.json (Felucca's 107 regions, 272 rects; Trammel's 145), S3's output
<code copy>/server/data/regions-trammel.json and its decision log notes/cc-P676-tools/out-decisions.csv, and the
SoS land (the SoS base with this branch's trammel.mapops) for Felucca's own change share (measure_felucca.py).

The rules (notes/cc-P686-*.md says why):
  1. Felucca's own fields stay: type, priority, guards (Buccaneer's Den's GuardsDisabled), music, rune name, logout.
  2. A Felucca region whose rects are pinned Trammel's same region's (100 of 107) takes S3's decision for it: kept,
     clipped, redrawn from the author (its rects, go location and entrance as S3 wrote them, the guard zone peeled to
     the town as on Trammel), kept by name, or dropped. Children of a dropped region are dropped.
  3. Ocllo, Felucca's name for the pre-UOML Haven town the author rebuilt, takes pinned Trammel "Haven"'s rects: the
     ones Trammel's New Haven is registered over at every start (P678, HavenTownRegions.cs). The towns match. Its inn
     child (no logout delay) is the inn building Trammel's New Haven Inn is registered over (HavenTownRegions.InnArea).
  4. Every other Felucca region (Felucca's own geography: the T2A Arena, Khaldun, and the inn children of Britain,
     Nujel'm and Moonglow, whose rects differ from Trammel's) takes S3's rule on Felucca's own change share:
     under 25 percent kept; else only its rects each under 25 percent changed; else dropped, unless our code looks it
     up by name.
  5. The author's regions S3 added (his towns, keeps, dungeons, wild areas, docks, isles, S14's unfinished land) are
     added to Felucca the same, with Felucca's rules: his towns guarded, as every stock Felucca town but Buccaneer's
     Den is. A name Felucca already has (Khaldun: the same rect) keeps Felucca's.
"""
import collections, copy, csv, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
NOTES = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import measure_felucca as M  # noqa: E402

PINNED = M.PINNED
DECISIONS = M.DECISIONS
TRAMMEL_REL = os.path.join('server', 'data', 'regions-trammel.json')
OUT_REL = os.path.join('server', 'data', 'regions-felucca.json')
REDRAW = 25.0
KEEPS = {'kept', 'kept for S7', 'redrawn from the author', 'clipped', 'kept by name'}


def parent_name(r):
    p = r.get('Parent')
    return p['Name'] if isinstance(p, dict) else None


def looked_up(code, names):
    """Felucca names our shipped code names on a line that looks a region up (P676's code_lookups rule)."""
    out = {}
    top = os.path.join(code, 'server', 'customizations')
    for dp, dn, fn in os.walk(top):
        for f in fn:
            if f.endswith('.cs'):
                p = os.path.join(dp, f)
                for line in open(p, encoding='utf-8', errors='replace'):
                    if re.search(r'Region|IsPartOf|Find\(|\.Name', line):
                        for n in names:
                            if '"%s"' % n in line:
                                out.setdefault(n, os.path.relpath(p, code).replace(os.sep, '/'))
    return out


def main():
    folder, code = sys.argv[1], sys.argv[2]
    pinned = json.load(open(PINNED, encoding='utf-8'))
    fel = [r for r in pinned if r['Map'] == 'Felucca']
    tram = [r for r in pinned if r['Map'] == 'Trammel']
    tout = json.load(open(os.path.join(code, TRAMMEL_REL), encoding='utf-8'))
    dec = list(csv.DictReader(open(DECISIONS, newline='')))
    stock_dec = dec[:len(tram)]
    assert all(d['region'] == (t.get('Name') or '(unnamed)') for d, t in zip(stock_dec, tram)), 'decision order'
    # S3's output holds the stock regions it kept, in pinned order, then the ones it added
    kept_j = [j for j, d in enumerate(stock_dec) if d['decision'] in KEEPS]
    t_of = dict(zip(kept_j, tout))
    for j, r in t_of.items():
        assert (r.get('Name') or None) == (tram[j].get('Name') or None), ('S3 output order', j)
    added = tout[len(kept_j):]
    assert all(d['decision'] == 'added' for d in dec[len(tram):] if d['region'] in {a.get('Name') for a in added})

    m = M.changed_blocks(folder)
    lookups = looked_up(code, {r.get('Name') for r in fel if r.get('Name')})
    haven = next(t for t in tram if t.get('Name') == 'Haven')
    hv = open(os.path.join(code, 'server', 'customizations', 'Regions', 'HavenTownRegions.cs'), encoding='utf-8').read()
    inn = tuple(int(v) for v in re.search(
        r'InnArea = new\(new Point3D\((\d+), (\d+), -?\d+\), new Point3D\((\d+), (\d+), ', hv).groups())
    out, log, dropped = [], [], set()
    for i, f in enumerate(fel):
        name = f.get('Name') or '(unnamed)'
        r = copy.deepcopy(f)
        pn = parent_name(f)
        pct = M.share(m, M.rects_of(f))[2]
        if pn in dropped:
            dropped.add(name); log.append(('dropped', name, pct, 'its parent was dropped')); continue
        if f.get('Name'):
            js = [j for j, t in enumerate(tram) if t.get('Name') == f['Name']]
        else:
            js = [j for j, t in enumerate(tram) if not t.get('Name') and M.rects_of(t) == M.rects_of(f)
                  and parent_name(t) == pn]
        if js and M.rects_of(tram[js[0]]) == M.rects_of(f):
            j = js[0]
            d = stock_dec[j]['decision']
            if d == 'dropped' and name not in lookups:
                dropped.add(name); log.append(('dropped', name, pct, 'as on Trammel (S3): ' + stock_dec[j]['why'])); continue
            if d == 'dropped':
                out.append(r); log.append(('kept by name', name, pct, 'S3 dropped it; our code looks it up (%s)' % lookups[name])); continue
            t = t_of[j]
            r['Area'] = copy.deepcopy(t['Area'])
            for k in ('GoLocation', 'Entrance'):
                if k in t:
                    r[k] = copy.deepcopy(t[k])
            out.append(r)
            log.append((d if d != 'kept for S7' else 'kept', name, pct, 'as on Trammel (S3): ' + stock_dec[j]['why']))
            continue
        if f.get('Name') == 'Ocllo':
            r['Area'] = copy.deepcopy(haven['Area'])
            out.append(r)
            log.append(('redrawn to the town', name, pct, 'pinned Trammel Haven\'s rects, the pre-UOML Haven the author '
                        'rebuilt; Trammel\'s New Haven is registered over the same (P678)'))
            continue
        if pn == 'Ocllo':
            r['Area'] = [{'x1': inn[0], 'y1': inn[1], 'x2': inn[2], 'y2': inn[3]}]
            out.append(r)
            log.append(('redrawn to the town', name, pct, 'Ocllo\'s inn: the inn building Trammel\'s New Haven Inn is '
                        'registered over (P678, HavenTownRegions.InnArea %d,%d to %d,%d)' % inn))
            continue
        if pct < REDRAW:
            out.append(r); log.append(('kept', name, pct, 'Felucca\'s own; under 25 percent changed'))
            continue
        keep = [q for q in M.rects_of(f) if M.share(m, [q])[2] < REDRAW]
        if keep:
            r['Area'] = [{'x1': a, 'y1': b, 'x2': c, 'y2': e} for (a, b, c, e) in keep]
            go = r.get('GoLocation')
            if go and not any(x1 <= go['x'] < x2 and y1 <= go['y'] < y2 for (x1, y1, x2, y2) in keep):
                big = max(keep, key=lambda q: (q[2] - q[0]) * (q[3] - q[1]))
                r['GoLocation'] = {'x': (big[0] + big[2]) // 2, 'y': (big[1] + big[3]) // 2, 'z': go.get('z', 0)}
            out.append(r)
            log.append(('clipped', name, pct, 'Felucca\'s own; %d of %d rects kept (each under 25 percent changed)'
                        % (len(keep), len(M.rects_of(f)))))
        elif name in lookups:
            out.append(r); log.append(('kept by name', name, pct, 'our code looks it up (%s)' % lookups[name]))
        else:
            dropped.add(name)
            log.append(('dropped', name, pct, 'Felucca\'s own; the land under it changed'))

    # 5. the author's regions S3 added, on Felucca
    taken = {r.get('Name') for r in out if r.get('Name')}
    for a in added:
        name = a.get('Name')
        if name in taken:
            log.append(('not added', name, '', 'Felucca has its own %s (rects %s)' % (
                name, 'equal' if next(r for r in out if r.get('Name') == name)['Area'] == a['Area'] else 'different')))
            continue
        e = copy.deepcopy(a)
        e['Map'] = 'Felucca'
        if isinstance(e.get('Parent'), dict):
            assert e['Parent']['Name'] in taken, ('parent missing on Felucca', name)
            e['Parent']['Map'] = 'Felucca'
        out.append(e); taken.add(name)
        log.append(('added', name, '', 'as on Trammel (S3): ' + next(d['why'] for d in dec[len(tram):] if d['region'] == name)))

    names = [r.get('Name') for r in out]
    for i, r in enumerate(out):
        pn = parent_name(r)
        assert not pn or pn in names[:i], ('parent after child', r.get('Name'), pn)
        assert r['Map'] == 'Felucca' and (not pn or r['Parent']['Map'] == 'Felucca')
    named = collections.Counter(n for n in names if n)
    assert all(v == 1 for v in named.values()), [k for k, v in named.items() if v > 1]
    path = os.path.join(code, OUT_REL)
    if '--check-only' not in sys.argv:
        text = '[\n' + ',\n'.join('  ' + json.dumps(r, ensure_ascii=True) for r in out) + '\n]\n'
        open(path, 'w', encoding='ascii', newline='\n').write(text)
    with open(os.path.join(HERE, 'out-decisions.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['decision', 'region', 'percentChangedOnFelucca', 'why'])
        w.writerows(log)
    print(collections.Counter(l[0] for l in log))
    print('regions', len(out), 'rects', sum(len(r['Area']) for r in out), 'written to', path)
    print('looked up by name (Felucca names):', lookups)


if __name__ == '__main__':
    main()
