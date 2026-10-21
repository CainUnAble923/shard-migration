# CC task P284: fix-up for P236 (satchel and guild bag icons): its branch did not merge into main

Iron, 2026-10-21.

## Headlines

- **P236 now merges with main.** All seven ShatteredLegacy conflicts are resolved with both sides kept. Every one came
  from Bronze's P237 (New Haven community art, F-21), which merged first and wrote into the same art files, the same
  `ShatteredLegacyArt.Apply`, the same package test and the same changelog version. Nothing contradicted: P237's IDs
  are 15496-15529 (0x3C88-0x3CA9), P236's 13184-13189 (0x3380-0x3385). P236 chose its range to stay clear of P237.
- shard-migration merged on its own, with no conflicts: P236's notes, its `cc-P236-art\` files and Codex's review.
  Codex found nothing in P236 (`notes\cc-P236-satchel-icons-ship-codex-review.md`).
- **Green:** `docker/uo/build.sh -t sl-modernuo:cc-P284` built the image (`fd00e42075c6`) with all 129 patches applied.
  1,961 tests: 1,957 passed, 0 failed, 4 skipped. P236's 44 `SatchelIconsVerification` cases and P237's
  community-art tests are both in that run.
- Package facts, `validate-art.py` and `find-free-art.py --check-registry` are green on the merged tree.
- **Not committed.** The merge is staged in both work copies (`MERGE_HEAD` set) for the Golem to commit.

## How it was merged

The hand-off put both work copies on `golem/Iron/P284` and said not to switch branches. `golem/Iron/P284` was exactly
`main` (`2ab20d7` in ShatteredLegacy). So instead of checking out P236 and merging main into it, I ran
`git merge --no-commit --no-ff golem/Iron/P236` on P284, as P272 and P278 did. The tree comes out the same, and P236
and main are both its parents.

## Conflicts resolved (ShatteredLegacy)

| File | Main's side | P236's side | Resolution |
|---|---|---|---|
| `VERSION` | `2026.10.21.7` | `2026.10.21.6` | the higher, `2026.10.21.7` |
| `CHANGELOG.md` | `## 2026.10.21.7` (P159: one Staff line) and `## 2026.10.21.6` (P237: three Added lines, one Staff line) | `## 2026.10.21.6`: two Changed lines, one Staff line | Both sides' lines under the newer heading, as the prompt says: P236's two Changed lines become a `### Changed` list under `2026.10.21.7`, and its Staff line follows P159's. Main's `.6` section is unchanged. So players see the satchel news as part of the newest version |
| `registry.csv` | 34 rows, 15496-15529 (P237) | 6 rows, 13184-13189 | both: P237's rows, then P236's. No ID appears twice |
| `records.json` | the `about` text with P237's sentence; P237's 18 tiledata records | the `about` text with P236's sentence; P236's 6 records | `about` is main's text plus P236's sentence; P237's records, then P236's (53 tiledata records, valid JSON) |
| `SOURCE.txt` | the community art section (P237) | the satchel icons section (P236) | both sections, P237's first |
| `server/customizations/ShatteredRunestone.cs` | `ClusterFCommunityArtRecords.Apply()` | `Items.SatchelArt.Apply()` | both calls in `ShatteredLegacyArt.Apply`, P237's first (they write different IDs) |
| `player-package/tests/Build-UoOverrides.Tests.ps1` | the "besides the stones" filter leaves out 15496-15529; counts 174 rows, 5 gumps, 144 art | leaves out 13184-13189; counts 146, 5, 116 | the filter leaves out both ranges; counts **180** rows (174 + 6), 5 gumps, **150** art (144 + 6) |

## Tests

| What | Result |
|---|---|
| `player-package\tests\Build-UoOverrides.Tests.ps1` (after `scripts\build-equip-anims.py`) | **12 of 14 pass**: P236's `TheSatchelIconRecordsAreTheServersTableAndEachIsOursWithItsPng`, P237's `TheCommunityArtRecordsAreTheServersTableAndEveryRowIdIsRegisteredWithItsPng`, and the row-count fact with the merged counts. The 2 that fail, `PlayStarts...`, need the test shard up ("Cannot reach TEST SHARD"), as the file's header says and as in P236's notes |
| `scripts\validate-art.py --data D:\UO\UltimaOnlineVanilla check-registry` | "0 of 180 rows have problems" |
| `scripts\find-free-art.py --check-registry` | "0 of 180 registered IDs are no longer free" |
| PNG count against registry art rows | 150 = 150 |
| `docker/uo/build.sh -t sl-modernuo:cc-P284` (a full build, under the `docker-build` lock) | attempt 1 failed in the patch step: `BaseArmor-exceptional-material.patch` (P228's) was logged "Applied", then the accounted-for check called it "never applied". **Attempt 2, the same tree: image built, 129 patches applied, 1,961 tests: 1,957 passed, 0 failed, 4 skipped** |

## Notes for Chase

- **A flaky check in `docker/uo/apply-patches.sh` (not changed here).**
  - The cause: the "every patch file is accounted for" loop runs `printf '%s' "$HANDLED_PATCHES" | grep -Fxq "$name"`
    under `set -euo pipefail` (`:9`). `grep -q` exits at its first match and can close the pipe while `printf` is
    still writing. `printf` then dies of SIGPIPE, and pipefail turns a found name into a failure.
  - That is what failed attempt 1: the log shows the patch `Applied`, then `never applied`. The same tree passed
    at once.
  - The fix is one line: `grep -Fxq "$name" <<< "$HANDLED_PATCHES"`, a here-string with no pipe. It checks
    exactly the same thing. Left for its own prompt, because this fix-up's scope is the merge.

- **P236's decisions still stand**, unchanged by the merge (its notes, "Deviations and decisions for Chase"): the
  lumber tier hues are blue and purple, not green (a proposal is there); the Smith bag now tints only its metal; and
  the hunter's tier hues look unlike their comments.
- My P239 branch (creature levels) took `2026.10.21.8` for its own changelog section, on top of `.7`. This fix-up does
  not touch `.8`.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P284 -NoRefresh`
(the hand-off's work copies in place of the real folders). It commits nothing; neither repo is BLOCKED:

```
Repo Result
---- ------
code dry run
docs dry run
```

- **code: 20 files**: P236's files, with the conflicts resolved as above. `VERSION` is not pending: it now equals main's
  `2026.10.21.7`.
- **docs: 7 files**: P236's notes, its art folder, its Codex review, and this note.

No file is over 5 MB.

P284 DONE
