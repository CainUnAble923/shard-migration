# cc-P281: edits one field of a hall in halls.json in place (keeps the file's one-hall-per-block layout by rewriting it).
#   python -P setpick.py <key> <section> k=v [k=v ...]     e.g. setpick.py warriors npc x=1362 y=3716
import json, sys
P = 'D:/UO/golems/Iron/ShatteredLegacy/design/guild-halls/halls.json'
d = json.load(open(P))
key, sec = sys.argv[1], sys.argv[2]
h = next(x for x in d['halls'] if x['key'] == key)
tgt = h if sec == 'hall' else (h[sec] if not sec.startswith('decor') else h['decor'][int(sec[5:] or 0)])
for kv in sys.argv[3:]:
    k, v = kv.split('=', 1)
    try: v = json.loads(v)
    except ValueError: pass
    tgt[k] = v
def dump(d):
    out = ['{', '  "about": ' + json.dumps(d['about']) + ',', '  "halls": [']
    hs = []
    for h in d['halls']:
        head = {k: h[k] for k in h if k not in ('npc', 'sign', 'travel', 'decor', 'building')}
        parts = ['    ' + json.dumps(head)[:-1] + ',']
        for k in ('building', 'npc', 'sign', 'travel', 'decor'):
            if k in h:
                parts.append('     "%s": %s,' % (k, json.dumps(h[k])))
        parts[-1] = parts[-1][:-1] + '}'
        hs.append('\n'.join(parts))
    out.append(',\n'.join(hs))
    out.append('  ],')
    out.append('  "waiting": [')
    out.append(',\n'.join('    ' + json.dumps(w) for w in d['waiting']))
    out.append('  ]')
    out.append('}')
    return '\n'.join(out) + '\n'
open(P, 'w').write(dump(d))
