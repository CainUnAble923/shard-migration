r"""cc-P678: the notes' build results and the closing line.
    python -P edit_notes_final.py
"""
P = "D:/UO/golems/Iron/shard-migration/notes/cc-P678-new-haven-moves.md"
s = open(P, encoding="utf-8").read()

REPS = [
    ("""| not run red separately: the classes are new | see the gated build below |""",
     """| not run red separately: the classes are new | 4 of 4 in the gated build |"""),
    ("""**The gated build:** see the end of this file.""",
     """**The gated build** (`docker\\uo\\build.sh -t sl-modernuo:cc-P678`, detached through `gated-build.ps1`, docker-build
lock taken and released; free memory read 2.5 GB in Windows, 13 GB in the Docker VM):

- **Run 1, red** (`red\\red-build-1-summary.txt`): it compiled, and the test gate ran 2,688 facts with 8 failing.
  Each was a value that moved on purpose, or a fact this move invalidated:
  - the tour fact stepped 200 tiles east of the new centre, which is off the island, so the island gate held the
    trainee; it now steps 200 south;
  - the ruin count was 10, not 8: the two edge wildlife spawners;
  - the winter facts' community art floor (now 36), and the west-road arch one tile outside the town box (entrance
    arches may sit 3 outside);
  - the Thieves' Den lookout's post and the hall names in three guild and recipe facts.
- **Run 2, green** (`green-build-2-summary.txt`): **EXIT=0, 2,688 facts, 2,683 passed, 5 skipped, 0 failed**. The 5
  skipped are the real-map-file facts that skip in every build. All 169 facts in the files this prompt touched
  passed, and `sl-modernuo:cc-P678` was built."""),
    ("""- Code copy: 52 files changed (see `git status`), new""",
     """- Code copy: 56 entries in `git status` (the first build added the guild-hall, lookout, recipe and tour facts' fixes), new"""),
]
for a, b in REPS:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
s = s.rstrip() + """
- No file over 5 MB; the build logs are git-ignored (`*.log`) and summarised beside them. `docs\\` untouched.

P678 DONE
"""
open(P, "w", encoding="utf-8", newline="").write(s)
print("ok")
