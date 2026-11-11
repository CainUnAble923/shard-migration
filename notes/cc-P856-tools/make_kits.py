"""cc-P856: one-off. The proof kits from P849's: kit\\ (main: P849's main\\ scripts) and kit-isle\\ (release: P849's own),
each pointed at its own folder, its code copy and its shard name; stage856.py from P849's stage849.py."""
import os
import shutil

NOTES = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(NOTES, "cc-P849-tools")
OUT = os.path.join(NOTES, "cc-P856-tools")
B = "\\"

for kit, src, repo in (("kit", os.path.join(SRC, "main"), None), ("kit-isle", SRC, "D:" + B + "UO" + B + "golems" + B + "Iron" + B + "p856-isle")):
    dst = os.path.join(OUT, kit)
    os.makedirs(dst, exist_ok=True)
    for f in ("make_create_bin.py", "proof-shard.ps1", "run-tazuo.ps1", "tazuo-walk.ps1", "ui.ps1"):
        s = open(os.path.join(src, f), encoding="utf-8-sig").read()
        s = s.replace("cc-P849-tools" + B + "main", "cc-P856-tools" + B + kit)
        s = s.replace("cc-P849-tools'", "cc-P856-tools" + B + kit + "'")
        s = s.replace("Shattered Legacy P799 stock town proof", "Shattered Legacy P856 winter set proof")
        if repo:
            s = s.replace("D:" + B + "UO" + B + "golems" + B + "Iron" + B + "p803-isle", repo)
        open(os.path.join(dst, f), "w", encoding="utf-8", newline="\r\n" if f.endswith(".ps1") else "\n").write(s)
    print(kit, "written")

s = open(os.path.join(SRC, "stage849.py"), encoding="utf-8").read()
old = """    elif w[0] == "end":"""
assert old in s
s = s.replace(old, """    elif w[0] == "winter":  # cc-P856: the winter decor, all of it: winter place | winter clear
        r = c.command("[ClusterFWinterDecor %s" % w[1], 4)
        print("winter", [m.get("text") for m in r][:6], flush=True)
    elif w[0] == "end":""")
s = s.replace('ap.add_argument("--name", default="Iron Stock")', 'ap.add_argument("--name", default="Iron Winter")')
s = '"""cc-P856: P849\'s stage849.py plus "winter place|clear" ([ClusterFWinterDecor)."""\n' + s
open(os.path.join(OUT, "kit", "stage856.py"), "w", encoding="utf-8", newline="\n").write(s)
print("stage856.py written")
