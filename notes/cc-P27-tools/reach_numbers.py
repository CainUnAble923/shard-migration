# cc-P27 Part C: the numbers the reach repair moves, computed the same way for any copy of the tool and any export.
# Read only. Usage:
#   python reach_numbers.py <path to a content_index.py> <export root holding server/ and docker/uo/apply-patches.sh>
# The 340 and the 219 are the audit's own lists (notes/reachability-audit.md Appendix A: 340 files, 219 of them
# without a "(not in the 219" mark, plus the 32 costumes listed after them); gate 9 and gate 14 are its groups.
import importlib.util, os, re, sys

tool, root = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location('ci_under_test', tool)
ci = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ci)

audit = open(os.path.join(os.path.dirname(__file__), '..', 'reachability-audit.md'), encoding='utf-8').read()
appx = audit[audit.index('## Appendix A.'):]
groups, cur = {}, None
for line in appx.split('\n'):
    m = re.match(r'\*\*(.+?)\*\* \((\d+)\)', line)
    if m:
        cur = m.group(1)
        groups[cur] = []
        continue
    m = re.match(r'- `([^`]+)`(.*)', line)
    if m and cur:
        groups[cur].append((m.group(1), 'not in the 219' in m.group(2)))
all340 = [(f, n) for k, v in groups.items() for f, n in v]
assert len(all340) == 340, len(all340)
the219 = [f for f, n in all340 if not n]
assert len(the219) == 219, len(the219)
gate9 = [f for f, _ in groups[next(k for k in groups if k.startswith('Pinned TODO drops'))]]
gate14 = [f for f, _ in groups[next(k for k in groups if k.startswith('Underworld generator'))]]

r = ci.Reach(os.path.join(root, 'server', 'customizations'))
rows = r.report()
files = ci.reach_files(r, rows)
ported = {f: s for f, (s, _) in files.items() if '/' in f}
costume = lambda f: f.startswith('Items/Equipment/Suits/')
count = lambda pred: sum(1 for f, s in ported.items() if pred(f, s))
print(f'export {root}')
print(f'ported content files {len(ported)}: ' + ', '.join(
    f'{k} {count(lambda f, s, k=k: s == k)}' for k in ('reached', 'partial', 'unreached', 'staff-only')))
print(f'  not reached (unreached, partial or staff-only), costumes excluded: '
      f'{count(lambda f, s: s != "reached" and not costume(f))}; strictly unreached, costumes excluded: '
      f'{count(lambda f, s: s == "unreached" and not costume(f))}')
nr = lambda fs: [f for f in fs if ported.get(f, 'gone') not in ('reached',)]
print(f'audit Appendix A: {len(nr([f for f, _ in all340]))} of its 340 still not reached; '
      f'{len(nr(the219))} of the 219')
print(f'gate 9 (7 files): reached {sum(ported.get(f) == "reached" for f in gate9)}: '
      + ', '.join(f'{os.path.basename(f)}={ported.get(f, "gone")}' for f in gate9))
print(f'gate 14 (3 files): reached {sum(ported.get(f) == "reached" for f in gate14)}: '
      + ', '.join(f'{os.path.basename(f)}={ported.get(f, "gone")}' for f in gate14))
for n in ('MyrmidonGloves', 'GreymistChest', 'FountainOfFortune', 'GemologistsSatchel'):
    e = r.reached.get(n)
    print(f'  {n}: ' + (f'reached by {e[1]} in {e[3]} ({e[4]}:{e[5]})' if e else 'not reached'))
src = ci.servuo_sources(r, ['CrystalShards'])['CrystalShards']
print(f'ServUO sources of CrystalShards ({len(src)}): '
      + '; '.join(f'{k} at {site} by {ctx} {p}:{ln}' for k, site, ctx, st, p, ln in src))
