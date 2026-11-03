import re, sys, json, glob, os
A = sys.argv[1]
out = []
for path in sorted(glob.glob(os.path.join(A, "*.cs"))):
    src = open(path, encoding="utf-8-sig").read()
    starts = [m.start() for m in re.finditer(r"(\[Flip\w*Attribute\([^\]]*\)\]\s*)?public class\s+\w+ : \w+", src)]
    starts.append(len(src))
    for i in range(len(starts) - 1):
        chunk = src[starts[i]:starts[i + 1]]
        m = re.search(r"public class\s+(\w+) : (\w+)", chunk)
        cls, base = m.group(1), m.group(2)
        flipattr = re.search(r"Flip\w*Attribute\(\s*(\d+)\s*,\s*(\d+)\s*\)", chunk)
        name = re.search(r'DefaultName\s*\{\s*get\s*\{\s*return\s*"([^"]*)"', chunk) or re.search(r'Name\s*=\s*"([^"]*)"', chunk)
        bid = int(re.search(r":\s*base\(\s*(\d+)\s*\)", chunk).group(1))
        light = re.search(r"Light\s*=\s*LightType\.(\w+)", chunk)
        simple_lit = re.search(r"LitItemID\s*\{\s*get\s*\{\s*return\s*(\d+)", chunk)
        simple_unlit = re.search(r"UnlitItemID\s*\{\s*get\s*\{\s*return\s*(\d+)", chunk)
        cases = [(int(a), int(b)) for a, b in re.findall(r"case\s+(\d+):\s*this\.ItemID\s*=\s*(\d+)", chunk)]
        rec = dict(file=os.path.basename(path), cls=cls, base=base, id=bid, name=name.group(1) if name else None,
                   light=light.group(1) if light else None)
        if base == "BaseLight" and cases:
            # lantern: unlit S -> unlit E flip, lit S -> lit E; lit/unlit pairs from the getters
            flip = dict(cases)
            unlitS = bid; unlitE = flip[unlitS]
            litS = [a for a, b in cases if a not in (unlitS, unlitE)][0]; litE = flip[litS]
            rec.update(kind="lantern", unlit=[unlitS, unlitE], lit=[litS, litE])
        elif base == "BaseLight":
            rec.update(kind="sculpture", unlit=[int(simple_unlit.group(1))], lit=[int(simple_lit.group(1))])
        else:
            a, b = int(flipattr.group(1)), int(flipattr.group(2))
            rec.update(kind="pillow" if "Pillow" in path else "tapestry", flip=[a, b])
        out.append(rec)
json.dump(out, open(sys.argv[2], "w"), indent=1)
from collections import Counter
print(len(out), "classes", Counter(o["kind"] for o in out))
for o in out:
    ids = o.get("unlit", []) + o.get("lit", []) + o.get("flip", [])
    print(o["kind"], o["cls"], repr(o["name"]), o["id"], ids, o["light"])
