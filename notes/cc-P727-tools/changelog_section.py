"""cc-P727: move P721's five CHANGELOG lines (P723's merge put them into P718's section) into their own newest section,
2026.10.28.6, and set VERSION to it."""
import os

BS = chr(92)
REPO = BS.join(['D:', 'UO', 'golems', 'Iron', 'ShatteredLegacy'])
p = os.path.join(REPO, 'CHANGELOG.md')
s = open(p, encoding='utf-8', newline='').read()
nl = '\r\n' if '\r\n' in s else '\n'
lines = s.split(nl)
starts = {
    'Added': ("- Test shard: a new character's first moments on the Wakening Isle",
              "- Test shard: dying on the Wakening Isle tells you what to do",
              "- Test shard: at the farm, before the pests, Wren gives you a pitchfork"),
    'Changed': ("- Test shard: the farm's bandage lesson has a patient who stays hurt",
                "- Test shard: the loop vision at the standing stones is lit from the start"),
}
moved = {k: [] for k in starts}
keep = []
for ln in lines:
    hit = next((k for k, pre in starts.items() if any(ln.startswith(x) for x in pre)), None)
    if hit:
        moved[hit].append(ln)
    else:
        keep.append(ln)
assert len(moved['Added']) == 3 and len(moved['Changed']) == 2, moved
top = next(i for i, ln in enumerate(keep) if ln.startswith('## 2026.10.28.5'))
assert not any(ln.startswith('## 2026.10.28.6') for ln in keep)
section = ['## 2026.10.28.6', '', '### Added'] + moved['Added'] + ['', '### Changed'] + moved['Changed'] + ['', '']
keep[top:top] = section
open(p, 'w', encoding='utf-8', newline='').write(nl.join(keep))
v = os.path.join(REPO, 'VERSION')
vs = open(v, encoding='utf-8', newline='').read()
assert vs.strip() == '2026.10.28.5', vs
open(v, 'w', encoding='utf-8', newline='').write(vs.replace('2026.10.28.5', '2026.10.28.6'))
print('ok')
