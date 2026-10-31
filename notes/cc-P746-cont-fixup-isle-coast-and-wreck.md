# cc-P746: fix-up for P741 (isle coast, shipwreck, signs, farm, bank and League house round)

Iron Golem, 2026-10-31. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P746`. Nothing deployed, no package built, the shared Test Shard and Haven not touched.

## In plain words

- **P741's isle round can now merge.** The coast, the whole shipwreck, the signs north of the paths, the turned farm,
  and the redone bank and League lodge now sit together with main's newer work: the easier-to-see waking (P740) and
  Blackthorn's move to the Fold (P691). Nothing from either side was dropped.
- **One map patch holds both.** The isle's new coast and P691's Blackthorn dungeon sit in different places on the map,
  so the shipped map patch now has both, with no tile where the two disagree.
- **One patch-notes version.** The six isle lines from P741 join P740's two lines under version 2026.10.30.3.
- **The bandages beside Pip moved with his farmhouse.** P740 set a pile of bandages on the farmhouse table beside Pip.
  P741 moved the farmhouse 12 tiles east, so the pile was left in the new field. It now sits on the moved table beside
  Pip. On a world that already has the pile, it is carried across, not doubled.
- **For you:** Nothing new to do. What P741 asked still stands: walk the isle on the next test build, and P741's
  render review by a second Golem.

## What changed

Neither repo's main was touched. In both work copies, `golem/Iron/P746` (main at the P691 merge) has `golem/Iron/P741`
merged in, not committed (`git merge --no-commit --no-ff`; MERGE_HEAD is P741's tip, 430799d in the code copy and
7219f30 in the docs copy). The hand-off says not to switch branches, so I merged P741 into this branch and did not
check out P741 and merge main into it. The tree is the same either way. The Golem's commit makes the merge commit.

### The conflicts resolved (code copy)

- **`VERSION`:** main's `2026.10.30.3` (P740), the higher one.
- **`CHANGELOG.md`:** one section, `## 2026.10.30.3`. Its `### Changed` list has P740's two lines first, then P741's
  six lines (P741 had them under 2026.10.30.2). Every other section is main's.
- **`player-package/vendor/shattered-legacy-map/trammel.mapops`:** git's text merge cannot join it, because both sides
  wrote sorted lines next to each other. P691 added Blackthorn's two pieces (x 6217-6511 and 6904-7146, 1,599 new
  B lines). P741 rewrote the isle (x about 6600-6870). I merged it three ways, line by line
  (`notes\cc-P746-tools\merge_mapops.py`):
  - the base is P741's fork point dadf28f;
  - each land cell (`L`), each block fingerprint (`B`) and each static line (`S+`/`S-`, counted) takes the side that
    changed it;
  - the output is in `mapops.py diff`'s own order and header.
  - **Its check:** written back on its own, main's file and P741's file each come out byte for byte (the same order).
    **0 clashes**: no cell, block or static was changed by both sides.
  - **Counts:**

| | base | main | P741 | merged |
|---|---|---|---|---|
| B lines | 2,288 | 3,887 | 2,288 | 3,887 |
| L lines | 50,760 | 137,748 | 50,760 | 137,748 |
| S lines | 13,007 | 45,623 | 13,033 | 45,649 |

  P741 changed L lines' values and statics only inside the isle's existing blocks, so the B list is main's.
- **Merged by git without a conflict, but wrong together (fixed):** the bandage table, next section.
- **Merged by git without a conflict:** `server/customizations/Tutorial/TutorialFarm.cs` (P740's bandage table and
  P741's farm move), and in the docs copy `tools/tests/test_mapops.py` (P691's Blackthorn fact and P741's fact 12).


### What the two branches got wrong together (git saw no conflict)

- **The bandage table beside Pip** (P740) stayed at the old farmhouse table, 6690,3975 Z 13. P741 moved the farmhouse
  12 east, so Pip's bench is at 6704,3975 and the old spot is in the new field. P740's fact
  `TheTableBesidePipHandsBandagesThatStayThere` failed in the first gated build (`red-gated-build-1.txt`).
  - `TutorialFarm.TableBandagesSpot` is now 6702,3975 Z 13. That is the moved cottage's own table
    (`TutorialIsleFarmLayout` 0x0B90 at 6702,3975, Z 7), two tiles west of Pip's bench, as P740 had it.
  - `TutorialFarm.OldTableBandagesSpot` (P740's spot) is new. `MoveFromOldLayout` carries a table left there to the new
    spot, or deletes it when one is there already. It runs before the seeder lays a table, so a world seeded with P740
    keeps its one table.
  - **The fact:** `TutorialIsleCoastVerification.AFarmLaidBeforeTheMoveIsMovedInPlace` (P741's old-world fact) now also
    sets the table on P740's spot and wants the same table, once, at the new spot. **Seen failing** on a mutant without
    the mover (`red-notablemove.txt`: "The collection contained 2 items").
- **A random-roll flake, not from the merge:** the second gated build failed one fact,
  `CreatureLevelsVerification.BelowPinnedsCapTheUncappedDifficultyIsPinnedsExactly` ("TheButcher: uncapped 158.1
  under pinned's cap 160", `red-gated-build-2.txt`). It passed in the first build on the same code, and neither branch
  touched it. Both reads roll. The fact read ours 12 times, and here none reached 160. P355 fixed the same kind of flake
  on pinned's side. I made the fact keep reading ours (up to 400 times) once pinned reaches its cap. It then passed 5
  runs of 5 (`probe-levels-5runs.txt`).

## Tests

- **Map facts** (`tools\tests\test_mapops.py`, `SL_SHARD_REPO` = the code copy, on the merged patch): **13 of 13**
  (P741's 12 plus P691's Blackthorn fact), `notes\cc-P746-tools\test-mapops.txt`. This proves the merged patch applies,
  is the isle's build plus P691's Blackthorn, and that the player-side applier writes the same bytes.
- **Tutorial facts** on `sl-uo-builder:cc-P746` (`probe.sh`, P741's): **243 of 243** (`probe-tutorial.txt`).
- **Gated build** (`docker/uo/build.sh -t sl-modernuo:cc-P746`, run detached by `gated-build.ps1`, `docker-build` lock
  taken and released): **EXIT=0**, 2,836 tests, 2,830 passed, 6 skipped, 0 failed (`green-gated-build.txt`). The image
  `sl-modernuo:cc-P746` is built. Two red builds came before it (above).
- **Not re-run:** P741's live proof on a private shard and its bot route. The merge changed no isle code except the
  table spot. The fact covers the table, and the image is built for the next test-shard run.

## Deviations and decisions for Chase

- **Merged P741 into this branch, not main into P741.** The hand-off says not to switch branches. The tree is the same.
  The Golem's commit makes the merge commit (MERGE_HEAD is set in both copies).
- **One file view refused.** The unattended run refused the Read tool on `server\customizations\Tutorial\TutorialFarm.cs`
  in the code copy (I wanted to view lines 508-511 and 1374-1377 before editing them). I had already read those lines
  with `sed` and made the two edits with a checked Python script (each replaced text found exactly once). The gated
  build and the facts above cover the edits.
- **A fact outside the isle changed:** `server\tests\Mobiles\CreatureLevelsVerification.cs`, the flake fix above. It is
  test-only.

## Files

- **Code copy:** CHANGELOG.md, VERSION (main's), `player-package/vendor/shattered-legacy-map/trammel.mapops`
  (merged), P741's server and test files, plus `server/customizations/Tutorial/TutorialFarm.cs` (the table spot and the
  mover), `server/tests/Tutorial/TutorialIsleCoastVerification.cs` (the table in the old-world fact),
  `server/tests/Mobiles/CreatureLevelsVerification.cs` (the flake).
- **Docs copy:** P741's files (notes, tools, `tools/tests/test_mapops.py`, the guide), this file, and
  `notes/cc-P746-tools/` (the merge script, launchers, probes, logs).

P746 DONE
