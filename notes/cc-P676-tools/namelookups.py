"""cc-P676: which stock Trammel region names our code names in a string (customizations, patches, tests), counted.
python -I namelookups.py <code copy> <pinned regions.json>"""
import json, os, re, sys
code, rj = sys.argv[1], sys.argv[2]
names = sorted({r['Name'] for r in json.load(open(rj)) if r['Map'] == 'Trammel' and r.get('Name')}, key=len, reverse=True)
hits = {}
for top in ('server/customizations', 'server/patches', 'server/tests'):
    for dp, dn, fn in os.walk(os.path.join(code, top)):
        for f in fn:
            if not f.endswith(('.cs', '.patch')):
                continue
            p = os.path.join(dp, f)
            text = open(p, encoding='utf-8', errors='replace').read()
            for n in names:
                if '"%s"' % n in text:
                    for i, line in enumerate(text.splitlines(), 1):
                        if '"%s"' % n in line and re.search(r'Region|IsPartOf|Find\(|\.Name', line):
                            hits.setdefault(n, []).append('%s:%d' % (os.path.relpath(p, code).replace(os.sep, '/'), i))
files = sorted({h.split(':')[0] for v in hits.values() for h in v})
for n, v in sorted(hits.items()):
    print('%-28s %s' % (n, '; '.join(v)))
print('names', len(hits), 'files', len(files))
for f in files: print('  ', f)
