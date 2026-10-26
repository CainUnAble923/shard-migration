# P635: fix-up for P628 (guards that patrol and see, pilot town): its branch did not merge into main

Written 2026-10-26 by the Iron Golem (Claude Code). The integrator could not merge `golem/Iron/P628` into main: `CHANGELOG.md` and `docker/uo/apply-patches.sh` conflicted with P627 (item identification), which merged first. Both conflicts were two independent additions in the same spot. Both now stay.

## In plain words

- P628's guard witness recorder (the Cove pilot) can now merge into main. Nothing in it changed; only two shared files needed both their new lines kept.
- Players notice nothing. As in P628, the recorder is off until staff switch it on with `[GuardWitness on` on the test shard.
- The patch notes for version 2026.10.25.14 now list both staff lines, item identification and the guard witness pilot.
- Nothing for you to do.

## Status

Done. The Iron Golem (Opus), branch `golem/Iron/P635` of both repos, not committed (the Golem commits). Gated build: see "Tests and build". No shard, package or Haven was touched.

## How

The hand-off says not to switch branches or merge. So I did not check out `golem/Iron/P628` and merge main into it. `golem/Iron/P635` starts at main, level with `origin/main` after `git fetch origin` (code `a113b35`, docs `5303c61`). I ran `git cherry-pick --no-commit` of P628's single commit in each repo (code `dff2f5c`, docs `4cc4de2`). That gives the same tree the merge would, as in P542 and P587.

- Docs repo: no conflict. P628's two notes (`cc-P628-build-guard-patrols-pilot.md` and its Codex review) were added, byte-identical to P628.
- Code repo: two conflicts, both resolved by keeping both sides (below). Checked afterwards: P628's three files (`ClusterFGuardWitness.cs`, `GuardedRegion-witness-observe.patch`, `GuardWitnessVerification.cs`) are byte-identical to P628's tip. The staged tree differs from P628's tip only by P627's work, which is main.

## The conflicts resolved

| File | Main (P627) | P628 | Resolution |
|---|---|---|---|
| `CHANGELOG.md` | `## 2026.10.25.14`, Staff: the item identification line | the same heading `## 2026.10.25.14`, Staff: the guard witness pilot line | One `## 2026.10.25.14` heading with both Staff lines, P627's first. |
| `docker/uo/apply-patches.sh` | the cc-P627 block (comment and four `apply_patch` lines: Item-property-list-policy, LootPack-unidentified-magic, ItemIdentification-item-knowledge, ArmsLore-item-knowledge) | the cc-P628 block (comment and `apply_patch GuardedRegion-witness-observe.patch`) | Both blocks, P627's then P628's, with a blank line between them as elsewhere in the file. The patches touch different pinned files (`Item.cs`, `LootPack.cs`, `ItemIdentification.cs`, `ArmsLore.cs` against `GuardedRegion.cs`), so their order does not matter. |
| `VERSION` | `2026.10.25.14` | `2026.10.25.14` | No conflict: both sides say `2026.10.25.14`, the higher (and only) value. |

The prompt says to keep both sets of lines under the newer version heading. Both branches had picked the same number, so the two lines share `2026.10.25.14`. Neither line is for players (both are Staff), so nobody misses a login bulletin because of the shared number.

For the integrator: P629 (League warrants, stage 1), not yet in main, adds its own `## 2026.10.26` section and sets `VERSION` to `2026.10.26`. It sits above `2026.10.25.14` and does not overlap these lines, but both branches edit the top of `CHANGELOG.md`. If git cannot place them, keep both sections, newest first, and take `2026.10.26`.

## Tests and build

`docker\uo\build.sh -t sl-modernuo:cc-P635`, under the Golem's `docker-build` lock (taken, then released). First I dropped the Docker VM's page cache: Windows showed 5.5 GB free before the drop and 5.8 GB after, with 13.8 GB available inside the VM. I then started the build detached. First run: **green**, exit 0. The build ended with "Built sl-modernuo:cc-P635 with patches applied and 2530 shard test(s) passing" (image `6fc7e9f7151a`).

- Patches gate: all five patches from the two blocks applied in order: `Item-property-list-policy`, `LootPack-unidentified-magic`, `ItemIdentification-item-knowledge`, `ArmsLore-item-knowledge`, then `GuardedRegion-witness-observe`.
- Test gate: 2,534 tests: 2,530 passed, 4 skipped (the real-map facts, which need client files), 0 failed.
- P628's own facts (`GuardWitnessVerification`): all 4 passed. `SightNeedsRangeLineOfSightAndAVisibleActor`, `ACrimeIsRecordedAtTheEventWithExactlyItsWitnesses`, `AJurisdictionIsNamedRegionsOnOneFacet`, `ACallReportsOnlyWhatTheCallerSawAndIsHeardInSpeechRange`.
- P627's facts beside them (`ItemKnowledgeVerification`): all 8 passed. Nothing in the two features interacts.

Nothing was red, so nothing needed fixing. No new tests: this prompt adds no behaviour, and P628's facts were seen red-then-green in P628.

P635 DONE
