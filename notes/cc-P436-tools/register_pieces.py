"""cc-P436 step 2: register look B's nine gumps (23200-23208) in registry.csv and credit them in SOURCE.txt. Refuses
to add a row for an ID the registry already has, so running it twice changes nothing."""
import csv
import io
import os

ART = r"D:\UO\golems\Iron\ShatteredLegacy\player-package\vendor\shattered-legacy-art"
REG = os.path.join(ART, "registry.csv")
SRC = os.path.join(ART, "SOURCE.txt")
FIRST = 23200
NAMES = ["top-left corner", "top edge", "top-right corner", "left edge", "centre (basalt)", "right edge",
         "bottom-left corner", "bottom edge", "bottom-right corner"]
SOURCE = ("Erachiro: erads-custom-content\\Erad's Custom UO Content\\Client\\UO Gump Basalt Edition\\"
          "Character Status Basalt .bmp; cut out (the braided bronze border, mirrored for the other sides; the centre "
          "is the title strip's plain basalt stacked mirror-wise), notes\\cc-P436-tools\\make_pieces.py")
LICENSE = ("Erachiro: \"\"Everything you see in this pack is free to use.\"\" Credit Erachiro in the shard credits, ship "
           "only inside the player package or the private repo, do not repost "
           "(D:\\UO\\third-party\\erads-custom-content\\SOURCE.txt); new IDs, no stock ID changed")

text = open(REG, encoding="utf-8").read()
have = {line.split(",", 1)[0] for line in text.splitlines() if line and not line.startswith("#")}
rows = []
for i, name in enumerate(NAMES):
    gid = FIRST + i
    if str(gid) in have:
        continue
    buf = io.StringIO()
    csv.writer(buf, lineterminator="\n").writerow(
        [gid, "0x%04X" % gid, "Guild and League gump frame, stone and bronze (cc-P436): %s" % name,
         SOURCE, LICENSE.replace('""', '"'), "gump"])
    rows.append(buf.getvalue())
if rows:
    if not text.endswith("\n"):
        text += "\n"
    open(REG, "w", encoding="utf-8", newline="").write(text + "".join(rows))
print("registry rows added:", len(rows))

section = """
Guild and League gump frame, stone and bronze, gumps 23200-23208 (0x5AA0-0x5AA8) (cc-P436)
--------------------------------------------------------------------------------------------
Chase's pick (2026-10-25, look B of three): the frame of our guild and League menus, drawn by the server's GuildStyle
(server\\customizations\\GuildStyle.cs) with AddBackground(23200), only for our own client; every other client keeps
the stock frame 9270.
Source:      Erachiro, "Erad's Custom UO Content" (D:\\UO\\third-party\\erads-custom-content), Client\\UO Gump Basalt
             Edition\\Character Status Basalt .bmp. Cut from it: the braided bronze border's top-left corner, a top and a
             left run (the other corners and edges are those mirrored), and the title strip's plain basalt stacked
             mirror-wise for the centre. Nothing recoloured or redrawn.
License:     Erachiro: "Everything you see in this pack is free to use." Credit Erachiro in the shard credits; ship only
             inside the player package or the private repo; do not repost.
Made by:     notes\\cc-P436-tools\\make_pieces.py in shard-migration (the same cut as the step 1 previews; --check
             compares the shipped PNGs with a fresh cut).
"""
src = open(SRC, encoding="utf-8").read()
if "gumps 23200-23208" not in src:
    open(SRC, "w", encoding="utf-8", newline="").write(src.rstrip("\n") + "\n" + section)
    print("SOURCE.txt section added")
