# cc-P520: fix-up for P363 (quest markers, keys, coloured moongates) so it merges into main

## In plain words

- **P363's work is now on a branch that sits on today's main, with its five merge conflicts resolved.** That work is the
  "!" and "?" quest markers, the keys and the four coloured moongates. The integrator can merge it like any other
  branch.
- **Nothing was lost:**
  - main's container and scroll skins (P362) and P363's art sit side by side in the art registry: 792 rows.
  - Both sets of patch notes are under version 2026.10.23.8.
- **Every test passed on the first full build:** 2,246 shard tests, and all three package test files.
- **For you:** nothing to do. When this merges, the next package build carries P363's art. P363's own "For Chase"
  steps still apply.

2026-10-23, the Iron Golem (Opus), branch golem/Iron/P520 of both repos. Prompt:
`cc-P520-cont-fixup-quest-markers-keys-gates.md`. Not committed (the Golem commits after DONE). Nothing was run against
any world, nothing was deployed, and the package was not built or published.

## Headlines

- golem/Iron/P520 started at main's tip (d418308, "Merge golem/Iron/P362"). It now carries all of P363 (commit
  98261ce), with the five conflicts resolved so that both sides survive.
- **Gate:** `sl-modernuo:cc-P520`, green on the first cycle: **2,246 tests, 2,242 passed, 4 skipped, 0 failed**.
  - P363's three facts (`QuestMarkersKeysGatesVerification`) pass.
  - Image fa815b558a4d carries VERSION 2026.10.23.8 and both changelog sets (read back from the container).
- **Package:**
  - `Build-UoOverrides` 23 of 23;
  - `Cliloc-Overrides` 10 of 10;
  - `Ui-Skins` (P362's) 4 of 4;
  - `validate-art.py check-registry` 0 of 792 rows with problems;
  - `find-free-art.py --check-registry` 0 of 792 no longer free;
  - `scripts\tests` OK.

## How, and one deviation from the prompt's step 1

The prompt says to check out `golem/Iron/P363` and merge main into it. The Golem's hand-off for this session says to
stay on `golem/Iron/P520`, never switch branches, and never run merge. Both ask for the same tree: main plus P363,
resolved. So:
- P520 is main's tip.
- I applied P363's own diff (`git diff <merge base bd95351> golem/Iron/P363`, binary included) onto it with
  `git apply --3way`.

This hits exactly the integrator's five conflicts and nothing else. Every other file of P363 applied cleanly:
- the 72 PNGs;
- records.json;
- the four new server files and the new test;
- ClusterFSmithBODSystem, ClusterFLootBoxes, EodonGeneration, ShatteredRunestone;
- Cliloc-Overrides.Tests.ps1.

**The result is ordinary staged changes on P520.** The Golem's commit makes it one commit on top of main, and the
integrator merges P520 as usual. `golem/Iron/P363` itself is left as it was. It need not be merged once P520 is in.

**Checked after resolving:**
- `git diff --cached golem/Iron/P363` shows only main's P362 files (client patch, Ui-Skins test, skins.json, its gumps
  and art, README) and the resolved lines.
- `git diff --cached HEAD` shows only P363's files.

**The docs repo.** P363's notes and tool (`notes/cc-P363-quest-markers-keys-gates.md`, `notes/cc-P363-tools/p363_art.py`)
were not on docs main either. The integrator aborts both repos together. They are brought onto P520 the same way: new
files, no conflict.

## The conflicts and how each was resolved

| File | main (ours) | P363 (theirs) | Resolution |
|---|---|---|---|
| `VERSION` | 2026.10.23.8 | 2026.10.23.7 | **2026.10.23.8**, the higher (the prompt's rule), so VERSION is unchanged from main |
| `CHANGELOG.md` | `## 2026.10.23.8`: 1 Added line (P362's skins) | `## 2026.10.23.7`: 3 Added, 4 Staff | **One `## 2026.10.23.8` section**: Added has main's line then P363's three; Staff has P363's four. 8 lines, counted against both sides; no `2026.10.23.7` heading left |
| `registry.csv` | P362's 93 rows appended (gumps 23052-23080, art 13049-13112) | P363's 72 rows (art 46592-46663) | **Both, main's first.** 792 rows (720 + 72), every ID unique; no shared IDs between the sides |
| `SOURCE.txt` | P362's "UI skins" section appended | P363's section appended | **Both sections**, main's first, with one blank line between |
| `Build-UoOverrides.Tests.ps1` (the ledger) | 720 rows, 40 bodies, 45 gumps, 634 art; P362 in the comment | 699 rows, 40 bodies, 16 gumps, 642 art; P363 in the comment | **792 rows, 40 bodies, 45 gumps, 706 art** (634 + 72); both comments kept, with "cc-P363: + 72 art" appended |

The rest of P363's edits to that test file merged by themselves:
- the new fact `TheMarkerGateTokenAndKeyRecordsAreTheServersTableAndNoStockIdIsOverwritten`;
- the carve-out 46592-46663;
- the synthetic fixtures grown to 1,460 groups and 46,720 animdata entries.

## Other notes

- **anim7.** The work copy's git-ignored `build\sl-anim7.bin` was left from the previous prompt's tree, so I re-encoded
  it for this tree: `build-equip-anims.py`, then `--check`, "anim7 matches", 51,891,270 bytes. P363 adds no bodies, so
  this is main's anim7.
- **Memory.** Free memory was 1.9 GB when the build started. The Docker VM held 12.9 GB of page cache; I dropped it
  (alpine `drop_caches`), which left the VM 13 GB free. Windows had 9.4 GB free when the build ended. The build was not
  killed.
- **For the integrator: P365 will conflict next.** P365 (golem/Iron/P365, reward mounts) was built on this same main
  without P363. Once P520 merges, P365 will conflict in the same five files:
  - its registry rows after P363's;
  - its ledger: 772 + 72 = **844 rows, 74 bodies, 45 gumps, 724 art** (652 + 72);
  - its SOURCE.txt section;
  - its CHANGELOG `2026.10.23.9` section, which stays separate as the higher version;
  - VERSION, which takes .9.
  - P365's fixture growth in both test files is identical to P363's, so it merges as one hunk.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive
-CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P520`

| Repo | Pending | What | Blocked |
|---|---|---|---|
| Code | 87 files | 77 added: 72 PNGs, 4 server files, 1 test; 10 changed | no |
| Docs | 3 | this note, P363's notes and P363's tool | no |

VERSION is not among the changed files: it stays main's 2026.10.23.8. No file is over 5 MB, and nothing under `docs\`
was edited.

```
Repo Result
---- ------
code dry run
docs dry run
```

P520 DONE
