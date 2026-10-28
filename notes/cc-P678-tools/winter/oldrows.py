r"""cc-P678: WRITES old-rows.json, the 109 rows of ClusterFWinterDecorLayout.cs as the code copy's HEAD has them
(git show, so a regenerated working file does not change it), with P266's modes and reasons from placement.json."""
import json, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
src = subprocess.run(['git', '-C', 'D:/UO/golems/Iron/ShatteredLegacy', 'show', 'HEAD:server/customizations/ClusterFWinterDecorLayout.cs'],
                     capture_output=True, text=True, check=True).stdout
pl = {r['key']: r for r in json.load(open(os.path.join(HERE, '..', '..', 'cc-P266-tools', 'placement.json')))}
rows = []
for m in re.finditer(r'new\("([^"]+)", "([^"]+)", (\d+), (\d+), (-?\d+), 0x([0-9A-F]+), "([^"]*)", 0x([0-9A-F]+), "([^"]+)", "([^"]+)"\)', src):
    k = m.group(1)
    rows.append(dict(key=k, area=m.group(2), x=int(m.group(3)), y=int(m.group(4)), z=int(m.group(5)), itemId=int(m.group(6), 16),
                     name=m.group(7), hue=int(m.group(8), 16), facing=m.group(9), layer=m.group(10), mode=pl[k]['mode'], why=pl[k]['why']))
json.dump(rows, open(os.path.join(HERE, 'old-rows.json'), 'w', encoding='ascii'), indent=1)
print(len(rows), 'rows')
