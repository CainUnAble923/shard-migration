# cc-P872: one-off edit of placed872.py (adds the "What cc-P872 changed" section and the part count from the design).
p = r"D:\UO\golems\Iron\shard-migration\notes\cc-P872-tools\placed872.py"
s = open(p, encoding="utf-8").read()
anchor = 'w("- Origin **%d,%d,%d** Trammel'
section = (
    'w("### What cc-P872 changed (the build review P868)\\n\\n"\n'
    '  "Nothing on the roof (building guide 1.1, 2.3, 2.6). Out of the design: the rune glyphs 0x4862 at 3649,2630,52,\\n"\n'
    '  "0x4856 at 3649,2635,50, 0x4856 at 3647,2631,56 and 0x4844 at 3647,2635,56 (the author\'s hidden window lights,\\n"\n'
    '  "drawn as green symbols on the shingles), and the vent sculpture 0x2419 at 3648,2633,53 on the ridge. Moved: the\\n"\n'
    '  "black cat 0x4689 from the roof\'s corner at 3650,2629,47 down onto the driver\'s bench 0x0B2D at the wagon\'s north\\n"\n'
    '  "end, at **3648,2627,22** (the bench is 1 high at z 21), its line kept. The wagon keeps its light from the porch\\n"\n'
    '  "lantern 0x0A22, the lamp stand 0x4C53 inside and the stained glass window 0xA5F8. Every other part is as P858\\n"\n'
    '  "had it.\\n\\n")\n'
)
assert anchor in s
s = s.replace(anchor, section + anchor, 1)
old = 'w("### Every part (212), one line each'
assert old in s
s = s.replace(old, 'w("### Every part (%d), one line each' , 1)
s = s.replace('|---|---|---|---|---|---|---|\\n")', '|---|---|---|---|---|---|---|\\n" % len(rows))', 1)
open(p, "w", encoding="utf-8", newline="\n").write(s)
print("ok")
