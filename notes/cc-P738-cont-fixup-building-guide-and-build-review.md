# cc-P738: P734 (the building and decorating guide, [PlaceBuild) brought onto main

Iron Golem, 2026-10-30. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P738`. Not committed, nothing deployed, Haven not touched.

## In plain words

- **P734's work is ready to merge again.** It covers the building and decorating guide, the six practice builds and
  the `[PlaceBuild` command that puts one down. It clashed only with P736, which had already added two sections to
  the same guide on main. The merged guide keeps P734's text and P736's additions, word for word.
- **No new shard build was run, as you chose.** The PC was too short of memory and you picked "Skip the build".
  The server files are exactly the ones P734 built and tested green (2,821 shard tests), and main has changed
  nothing under `server/` since P734 started.
- Nothing for you to do.

## What was done

`golem/Iron/P738` starts from main `5a3127c` (P689 merged). The prompt says to check out `golem/Iron/P734` and merge
main into it, but the hand-off forbids switching branches. So, as P730 did, I brought P734 into this branch instead:
`git merge --squash golem/Iron/P734` in both work copies. The result is the same tree, staged for the Golem's commit,
with no merge in progress.

- **Code copy:** merged with no conflicts. P734's files: `server/customizations/Builds/PlaceBuild.cs`, six
  `server/data/Decoration/Builds/practice-*.cfg`, `server/tests/Misc/PlaceBuildVerification.cs`. Main has none of
  them.
- **Docs copy:** one conflict, the one the integrator hit. Everything else merged cleanly: `notes/cc-P734-review/`,
  `notes/cc-P734-tools/`, and the two-line skip in `tools/tests/test_sos_fences.py`.

## The conflict, and why it took main's side

`notes/guides/building-and-decorating.md`, add/add. Both branches created the file. P736 was written before P734
merged, so it started from P734's guide (`git show e5b1dcf:...`, its notes say so) and added two sections. P736 then
merged first.

- **Checked:** `diff` of P734's guide against main's shows additions only: lines 382-400 and 504-642, which are P736's
  two sections. No line of P734's is missing or changed (0 lines removed).
- **So the file takes main's version.** That keeps both sides, and the staged file is byte-identical to main's.

No CHANGELOG.md or VERSION conflict: P734 changed neither.

## Tests

- `tools/tests/test_sos_fences.py` (the one docs test P734 touched): 4 skipped, 0 failed. Its facts need
  `SL_SOS_BASE`, a pristine SoS copy with `map1LegacyMUL.uop`. I found none on this PC: the
  `D:\UO\third-party\sos-trammel-map` folder holds only an unfinished `Statics1.mul`. P734's change there is a
  two-line skip of the `Decoration/Builds` folder.
- `tools/tests/test_s5_decoration.py`: 3 ran, 2 skipped, OK. `tools/tests/test_sos_dungeon_decoration.py`: 3 of 3 OK.
  That test rewrites `notes/cc-P683-tools/out/check.txt` and `ends.csv` with line-ending changes only. I restored
  both.
- **Gated build (`docker/uo/build.sh -t sl-modernuo:cc-P738`): not run.** It is needed because `server/` changed
  (P734's PlaceBuild.cs, the six cfgs and the new test). I took the docker-build lock at 05:32. Windows had 1,166 MB
  free. Dropping the Docker VM's page cache freed nothing on the Windows side: the VM's cache was already small
  (737 MB). A 20-minute wait (05:33 to 05:54) never got above 1,100 MB available, with commit charge at 89.6 of 95.6
  GB. I released the lock and asked Chase (Iron-P738-20261030-055531-e616).
  For reference, P734's own gated build on its branch was green: 2,821 shard tests (`notes/cc-P734-tools/green-gated-build.txt`).

## Chase's answer, and the finish

Chase answered Iron-P738-20261030-055531-e616 on the console at 07:34: **Skip the build**. Before finishing I checked
the code copy: the diff of `server/` from the merge-base of P734 and main to HEAD is empty. Main has had no server
change since P734 branched, so the staged tree under `server/` is P734's tree. That tree built and passed green in
P734's gate (`notes/cc-P734-tools/green-gated-build.txt`). This session ran no Docker build, took no lock and made no
image `sl-modernuo:cc-P738`. Both work copies stay staged for the Golem's commit.

P738 DONE
