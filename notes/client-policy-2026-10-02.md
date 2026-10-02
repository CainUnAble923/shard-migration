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
- **Open, for Chase:** see the overseer's questions in the chat (what "custom client" covers: our own data files, our
  own TazUO build, or both; whether players still need an EA install; full files or patches).
- **Affects:** P36 (dungeon build 1, map edits and the client floor), F-8's pipeline (P26), F-21 to F-23 (art), P35 (the
  clean-machine package test), and `Build-PlayerPackage.ps1`'s gate. Update the package policy line in `docs\` once the
  open questions are answered.
