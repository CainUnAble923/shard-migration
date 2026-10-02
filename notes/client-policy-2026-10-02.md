# Player client and file policy: Chase, 2026-10-02, 16:34

Recorded by the overseer.

- **Decision:** "change our outlook on sending files and custom clients. I am pro custom client so we can have
  upgraded art." The package may ship client data files, not only our own records, so the shard can have upgraded
  and new art.
- **What this replaces:** the P26 premise that the package ships nothing of EA's
  (`player-package\Build-PlayerPackage.ps1`, the gate around `:19`; P26 built the art pipeline by patching copies of the
  player's own `tiledata.mul` and `animdata.mul` on their machine). It agrees with dungeon decision 2b
  (`dungeon-decisions-2026-10-01.md`: the package ships EA's Trammel files and `tiledata.mul`), and settles the conflict
  the 2026-10-02 overseer pass-down flagged between the two.
- **Answered (Chase, 16:42):**
  1. **"Custom client" means both:** our own client data (art, map, tiledata, gumps) **and our own build of TazUO**.
  2. **Ship patches from us, not EA's files.** The package carries only our changes and applies them to EA's files on
     the player's machine (the P26 route, extended from tiledata/animdata to whatever we change: map, statics, art,
     gumps). Our download server never hosts EA's files.
  3. **The package gets what it needs and installs as easily as possible for the player.** If EA's client is missing,
     the package should fetch it (from EA's own official source, to be researched) and then apply our patches, with as
     few player steps as possible.
- **Consequence for dungeon decision 2b:** it said the package ships EA's Trammel files and `tiledata.mul`. Under this
  policy the dungeon's map and statics edits ship as **our patches**, applied locally, not as EA's files. Tell the
  dungeon chat; P36 has not run.
- **Affects:** P36 (dungeon build 1, map edits and the client floor), F-8's pipeline (P26), F-21 to F-23 (art), P35 (the
  clean-machine package test), and `Build-PlayerPackage.ps1`'s gate. Update the package policy line in `docs\` once the
  open questions are answered.
