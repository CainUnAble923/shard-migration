# P541: patch notes for October 24

## In plain words

- Wrote [the October 24 player draft](cc-P541-patch-notes-2026-10-24.md), grouped under Launcher and Lumberjacking, following P513's separate draft and evidence-note format.
- Covered the launcher progress display, preparation during updates, background rebuild fallback, default test-shard connection, corrected stump height, client tree hiding, and polearm message.
- Kept the known startup-delay and floating-leaf limits visible. Did not promise that every launch completes within a minute or that every tree disappears completely.
- Reviewed the day's documentation merges as well. Research, reviews, test plans, unused-art catalogs, and unpublished guide drafts are not new gameplay or published wiki pages.

## Scope and release boundary

Read AGENTS.md in both work copies first, then the migration direction decision and task list, P513's player draft and work record, and P406's work record and review. Both work copies began clean. No skill was needed for the explicitly requested Markdown files.

The code snapshot is `372bf893a90040c1e3066806460b5ad9776cd446`, version `2026.10.24.3`. The notes snapshot is `7f9f3b1adcec4685f90a3b45eef083596fc6d050`. The cutoff is the October 24 work present in these local snapshots, using America/Chicago dates and first-parent merge commit times. This is not a package-to-package comparison or a claim to cover merges arriving after those snapshots.

Enumerated four code merges and 29 notes merges with local Git history, from `2026-10-24T00:00:00-05:00` through `2026-10-24T23:59:59-05:00`. Each appears below. Read each merge's change list against its first parent. Notes changes outside notes/ consist only of generated project reporting and testing records; they do not publish the new guides or implement the proposed systems.

The player draft is explicitly pending the next package and server update. Deployment, published package contents, current shared test-world behavior, and client appearance were not verified. No remote request, fetch, or Haven connection was made.

## Code merge inventory

| October 24 merge | Work | Treatment |
| --- | --- | --- |
| `f2853e8`, P370 | Golem build retries, prompt completion, scheduling and question handling | Omitted staff tooling. Repository changes are CHANGELOG.md and VERSION only. |
| `70df7c5`, P373 | Codex Golem operation and console routing | Omitted staff tooling and console changes. |
| `0de0d9e`, P411 | Launcher progress, background rebuilding and default test-shard routing | Included player changes with startup limits. |
| `372bf89`, P412 | Stump height, exhausted-tree client visuals and polearm refusal | Included with updated-client dependency and floating-leaf limit. |

## Notes merge inventory

These are the actual merges on October 24, even when the underlying research began October 23. A review finding or fix-up draft is not a merged implementation fix.

| October 24 merge | Work | Treatment |
| --- | --- | --- |
| `51acde6`, P514 | Feature queue audit | Omitted research. |
| `d1e3232`, P516 | Guild hall design comparison | Omitted research; no new hall placement. |
| `668b31b`, P515 | League design comparison | Omitted research; no new League feature. |
| `53381f7`, P517 | F-12 progression numbers | Omitted research; no new progression system. |
| `493ce64`, P518 | Skill gain paths | Omitted research; no gain changes. |
| `06cbb96`, P370 | Golem fix documentation | Omitted staff tooling; paired with code merge above. |
| `984d8a3`, P519 | Herbalism comparison | Omitted research; Herbalism remains unbuilt. |
| `7100f98`, P521 | Reward mount and evo-stage review | Omitted review findings; mount implementation merged October 23. |
| `fbac49a`, P522 | Quest marker review disposition | Omitted; review skipped because the implementation was absent from its main snapshot. No quest markers announced. |
| `5b8a7c2`, P523 | Tutorial trades review | Omitted review findings; no tutorial fixes merged here. |
| `f85a525`, P524 | Golem fixes review | Omitted staff review. |
| `c170846`, P525 | New player tutorial guide draft | Omitted unpublished notes/wiki-drafts guide. |
| `99f2562`, P526 | Mounts guide draft | Omitted unpublished notes/wiki-drafts guide. |
| `8512bdb`, P528 | Achievements and loot design comparison | Omitted research; no new rewards. |
| `8a5ee4c`, P529 | New Haven dungeon comparison | Omitted research; no dungeon opening. |
| `b36347c`, P530 | Clean Up Britannia comparison | Omitted research; no shop or points changes. |
| `42d9618`, P373 | Codex Golem documentation | Omitted staff tooling; paired with code merge above. |
| `ec0c5e3`, P534 | Levelable gear comparison | Omitted research; no new Seal acquisition route. |
| `bdc3eee`, P533 | Findings and proposed fix-up prompts | Omitted drafts; no fixes implemented here. |
| `7bb45b1`, P527 | Companions and evo pets comparison | Omitted research; no new hiring or pet progression. |
| `0d55bac`, P531 | Play-test plans | Omitted plans; no new validation pass implied. |
| `f1ba96a`, P532 | Open questions sweep | Omitted recommendations and pending decisions. |
| `629b79e`, P542/P409 | Town Houses design handoff | Omitted design; no rentals or leaseholds implemented. |
| `3c52d24`, P536 | High Seas and fishing comparison | Omitted research; no new fishing or naval access. |
| `7d14365`, P535 | Skills comparison | Omitted research; no skill changes. |
| `bcc8013`, P412 | Chopped-tree implementation evidence and review | Used as evidence for the included code merge, with its limitations retained. |
| `bbb9693`, P543/P411 | Restored P411 notes and review | Used as launcher evidence. Documentation handoff only; not an additional launcher fix. |
| `1513dcf`, P538 | Unused-art inventory | Omitted catalog; no new art imported or activated. |
| `7f9f3b1`, P539 | Wiki draft cross-check | Omitted review report; no player draft or published wiki page changed. |

## Source checks and editorial choices

Paths in this section are relative to the code work copy unless linked to a notes file.

- `player-package/payload/app/Overrides-Launch.ps1:100`: checked the real invocation flow. Lines 122-151 implement the progress display, background child, bounded wait and previous-art fallback. Lines 158-170 handle failed or completed rebuilding. This supports the draft's limited fallback description.
- `player-package/payload/app/Update.ps1`: checked the final preparation block and subsequent call to Play.ps1. The updater prepares known installs before launching. It can then wait again in Play, so the draft gives no one-minute total guarantee or universal fast-start promise.
- `player-package/payload/app/Launch-Settings.ps1:34` and `player-package/payload/app/Play.ps1:78`: the default target is the test shard; Play also forces the test switch for its updater. The top-level Play shortcut calls that script. No remote-connectivity promise or claim that a new live world has opened is included.
- [P411 implementation notes](cc-P411-launcher-always-starts.md) and [review](cc-P411-launcher-always-starts-codex-review.md): the review reports an unbounded freshness check, missing active-step diagnostics, swap recovery risk, and a possible second timeout during update handoff. Source still calls CheckOnly synchronously at `Overrides-Launch.ps1:116`, before its timer starts at line 123. The draft therefore does not repeat the task title's absolute always-start claim. No claim is made that the last good art is preserved through every failure.
- [P543 handoff](cc-P543-cont-fixup-launcher-always-starts.md): this restores P411's documentation and reports rerun package gates. It does not repair the review findings. Those reported passes are not tests run by P541.
- `server/customizations/ClusterFLumberStumps.cs:80`: map-tree stumps use the resolved static base elevation. `ResolveTree` at line 96 reads actual statics and handles foliage targeting. This replaces the old elevated harvest target location.
- `server/customizations/ClusterFLumberStumps.cs:160`: a stump and client notification are created only for an exhausted bank, with only the final targeted tree marked. The default setting is enabled at line 69. Login resends the active entries at line 323.
- `client/patches/0006-exhausted-trees.patch:31`: the new render hook hides listed tree statics. The corresponding selection hook is at line 44. The manager expires the hidden entry at its deadline at line 149. This requires the updated shard client as well as the server change; other clients still show the standing tree beside its stump.
- `server/customizations/ClusterFLumberStumps.cs:135` and [P412 review](cc-P412-chopped-tree-visuals-codex-review.md): only statics at or above the trunk base enter the hide list. The review identifies a real map tree whose foliage is lower than its trunk. That source restriction remains in this snapshot, so the player draft explicitly allows floating leaves. The specific map example was not independently rechecked in client data during this documentation task.
- `server/customizations/ClusterFLumberStumps.cs:396`: an equipped lumberjacking axe or polearm gets the no-wood message. The draft describes targeting the exhausted stump rather than promising a changed response for every standing map tree.
- [P412 implementation notes](cc-P412-chopped-tree-visuals.md) report a private-world stump-position and packet check, but explicitly say the patched client was not visually driven. The note's Player-facing subsection still names version .2; actual CHANGELOG.md and VERSION put P412 at `2026.10.24.3`. Used the committed version files as authority.
- Read the documentation merge summaries and changed-file lists, including P525/P526's guide drafts and P539's cross-check. The guides remain notes/wiki-drafts files. They are not treated like P478's wiki-seed update in P513, and no new wiki release is promised.

October 23's late container skins and reward mounts are outside this calendar-day boundary, even though they merged after P513's earlier cutoff. October 22's Halloween release is also outside it. The draft does not backfill those releases or treat their later reviews as fresh content.

## Limits and validation

Docs-only task; lane tests are none. No tests or gates were added, so a red-first cycle does not apply. Existing implementation tests were read or cited as prior evidence, not rerun or claimed as this task's results.

- Ran `tools/progress.py --dry-run` with SL_SHARD and SL_MIGRATE pointing to these work copies: exit 0, reporting version `2026.10.24.3`. Its broader status text cannot establish the running shard image or published package and was not used as release evidence.
- The progress tool still writes tools/progress.json before checking dry-run. Preserved its initial bytes in memory, restored them afterward, and verified byte equality and clean status before drafting. No generated reporting changes remain.
- Commands run under Windows PowerShell `5.1.26100.9711`; no PowerShell 7 script or test ran.
- No code, CHANGELOG.md, VERSION, docs/ file, service, account, save, or installed tool was changed. No build, deployment, Haven connection, commit, merge, push, or branch switch occurred.
- Final document review passed: plain American English, no em dashes, short player lines grouped by area, no staff commands, no spoilers, and explicit update and known-defect limits.
- Compared the inventory tables with Git output: all four code merges and all 29 notes merges appear exactly once. Local Markdown links resolve, neither file has trailing whitespace, and both are below 5 MB.
- `git diff --check` passed in both work copies. New-file checks with `git diff --no-index --check` against NUL produced no whitespace diagnostics; their exit 1 indicates that the new files differ from NUL.
- Final scope is only the two requested new notes. The code work copy remains clean, and no generated reporting changes remain.
- Checked the stop-request path between research, drafting, and validation steps; it was absent. No work remains for P541.

P541 DONE
