# cc-P54: builds the notes file from notes_template.md plus the two model outputs. Deterministic.
# Run from this folder: python xp_ladder.py > xp_ladder_out.md; python reclimb.py > reclimb_out.md; python assemble.py
import re

def sections(path):
    out, cur, buf = {}, None, []
    for line in open(path, encoding="ascii"):
        if line.startswith("### "):
            if cur: out[cur] = buf
            cur, buf = line[4:].strip(), []
        elif cur:
            buf.append(line)
    if cur: out[cur] = buf
    return out

GEN = {}
GEN.update(sections("xp_ladder_out.md"))
GEN.update(sections("reclimb_out.md"))

def expand(m):
    key = m.group(1)
    hits = [k for k in GEN if k.startswith(key)]
    assert len(hits) == 1, f"marker {key!r} matched {hits}"
    k = hits[0]
    return "#### " + k + " (generated)\n" + "".join(GEN[k]).rstrip() + "\n"

text = open("notes_template.md", encoding="ascii").read()
text = re.sub(r"^\{\{GEN:(.+?)\}\}$", expand, text, flags=re.M)
assert all(ord(c) < 128 for c in text), "non-ASCII in notes"
open("../cc-P54-f12-xp-and-gain-paths.md", "w", encoding="ascii", newline="\n").write(text)
print("written", len(text), "chars")
