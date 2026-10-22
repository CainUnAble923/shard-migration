# P400: review of P359 and P380 chopped tree stumps

Reviewed October 22, 2026. Notes only. No code changes, new tests, builds, live connections, deployment, commits, or branch changes.

The documented marker lifecycle is consistent with the source, apart from the already reported map-tree elevation bug. There is also a smaller tool-message bug. I found no new stump-state leak or two-player race in the normal server execution path. Exhaustion and stumps deliberately do not survive a restart.

## Review basis

Read both work copies' AGENTS.md, the direction decision and task list, and these predecessor notes:

- `notes/cc-P359-chopped-tree-stumps.md`
- `notes/cc-P359-chopped-tree-stumps-codex-review.md`
- `notes/cc-P380-cont-fixup-chopped-tree-stumps.md`

`git log main` identifies code commit `43c4cc3` for P359, P380 merge commit `044af6c`, and its main merge `1ecd9f3`. The corresponding notes commits are `5a0f128`, `e0e8533`, and main merge `2b7def6`. The reviewed production file, patch, and test file match code main in this work copy.

Reviewed `server/customizations/ClusterFLumberStumps.cs`, `server/patches/HarvestBank-lumber-stumps.patch`, `server/tests/Engines/Harvest/ChoppedTreeStumpsVerification.cs`, and their registration in `docker/uo/apply-patches.sh:870`. The prompt's `server-patches/` means the actual `server/patches/` directory here. Also checked the lumber extension, Burrows harvest override, harvest-system patch, and test clock/tile helpers for interactions.

Upstream citations below are relative to the clean, read-only `D:/UO/ModernUO-pinned` tree, verified at `d4531cd94b739613155225c234900de9f47d2c88`. Shard citations are relative to the code work copy.

## Findings

1. **bug | `server/customizations/ClusterFLumberStumps.cs:23` | Map trees place the stump above their base.** `StaticTarget` adds the tile's calculated height to Z (`Projects/Server/Targeting/StaticTarget.cs:11` and `:18`), and `GetHarvestDetails` returns that elevated position unchanged (`Projects/UOContent/Engines/Harvest/Core/HarvestSystem.cs:499`), so a tree with nonzero height gets a floating marker. Subtract `TileData.ItemTable[staticTarget.ItemID].CalcHeight` only for `StaticTarget` targets, preserve dynamic `Static` locations, and add a real seeded tree-row test through harvest completion; this confirms the existing P359/P380 finding, without a new client observation.

2. **bug | `server/customizations/ClusterFLumberStumps.cs:121` | Valid lumber tools can get the wrong refusal.** An equipped polearm can chop wood (`Projects/UOContent/Items/Weapons/PoleArms/BasePoleArm.cs:32`), and its harvest target dispatches to `IChoppable`, but this check only accepts `BaseAxe`, so targeting or double-clicking the stump tells that player to equip an axe instead of reporting exhausted wood. Accept equipped tools whose harvest system is Lumberjacking, including polearms, and cover both stump interaction routes with message assertions.

3. **risk | `server/tests/Engines/Harvest/ChoppedTreeStumpsVerification.cs:81` | Duplicate-hook coverage does not exercise two players.** The duplicate case calls `OnHarvestFinished` again after manually consuming the bank, so it cannot catch a later change that lets two in-flight harvests both consume the last batch or create extra markers. Add a shared-bank case with one harvestable batch left and two equipped players starting before depletion, complete both through the real timer path, and assert the total logs consumed, one stump, and no extension of the first-consumption deadline.

4. **risk | `server/tests/Engines/Harvest/ChoppedTreeStumpsVerification.cs:154` | Restart coverage stops at forced item deserialization.** The case checks `SkipSerialization` and the defensive delete callback, but does not exercise normal world-save exclusion or a fresh server's bank state. Add a scratch save/reload integration case that proves the marker is absent from the restored world and the fresh bank is full, with no carried-over expiry timer.

5. **risk | `server/tests/Engines/Harvest/ChoppedTreeStumpsVerification.cs:128` | Cleanup tests do not prove the bank can be marked again.** Expiry and refill cases assert that the world item vanished, while fixture teardown deletes remaining stumps, so a stale private registry entry that blocks the next depletion could escape these assertions. Add two-cycle coverage for the same bank after expiry, refill, and manual deletion, checking that exactly one new marker appears and that the old timer cannot delete it.

## Behavior checked against source

- **Appearance and regrowth:** `ClusterFLumberStumps.cs:19` validates the target's actual bank, and `:53` marks it only below the normal ten-log harvest threshold. One stock-art stump is added at the last targeted tree; the original map tree and foliage remain, and neighboring trees sharing the 4 by 3 bank stay unmarked. This matches P359's stated scope, with the elevation defect above; it is not a literal tree replacement, and visibility under foliage remains unverified in a client.
- **Timing:** The marker uses the actual first-consumption refill deadline at `ClusterFLumberStumps.cs:99`, including the elf discount in upstream `HarvestBank.cs:82`. Idle expiry deletes the visual without eagerly refilling the bank; the next bank access performs the stock lazy refill. `HarvestBank-lumber-stumps.patch:17` deletes the marker immediately on a real refill. I found no extra timer or deadline-reset bug.
- **Restart:** `ClusterFLumberStumps.cs:104` excludes markers from ordinary saves, and `:140` deletes a forced or legacy loaded marker. Upstream `Projects/Server/Serialization/GenericEntityPersistence.cs:256` and `:289` omit skip-save entities from save output. Banks are ordinary in-memory objects created full by `HarvestDefinition.GetBank` and the `HarvestBank` constructor, so restart clears depletion and creates no leftover stump. This matches the notes' explicit no-persistence design; a restart does not resume the old countdown.
- **State growth:** The registry is keyed by bank, not by swing or tree, and `ClusterFLumberStumps.cs:55` prevents duplicates. Refill removes its entry at `:69`; item deletion stops the timer and forgets the entry at `:133`. I found no accumulating stump history. Upstream `HarvestDefinition.cs:87` and `:104` already retain every distinct touched bank until restart, without eviction; that existing cache can grow as players explore but repeated chops do not add entries for the same bank. The stump dictionary can retain its peak allocated capacity after entries are removed, which is ordinary dictionary behavior.
- **Two players:** The normal path executes harvest completion and marker expiry on the server event loop (`Projects/Server/Main.cs:725`, `HarvestSoundTimer.cs:33`). `HarvestSystem.cs:104` rechecks resources before consumption at `:197`, then calls the marker hook at `:250`, without an asynchronous gap. The first completion consumes and marks; the later completion sees the new balance and cannot consume an unavailable batch. I found no race requiring a concurrent dictionary or a new lock, subject to the missing regression test above.

## Verification limits

The only stump test file is `server/tests/Engines/Harvest/ChoppedTreeStumpsVerification.cs`: nine `[Fact]` methods and five inline theory cases, for 14 cases. It covers successful harvest completion on a dynamic tree, target-bank identity, duplicate hooks, an unharvestable remainder, lazy refill, idle expiry, disabling, forced serialization cleanup, fixed and automatic art, mining exclusion, and mismatched banks. It has no map-static target with nonzero tile height and no stump interaction/message assertions. The test host's empty tile data would hide the height bug without a `TestTileRows.Seed` scope.

P380 reports a successful `docker/uo/build.sh -t sl-modernuo:cc-P380` run with all 2155 shard cases passing, including these stump cases. That is predecessor-reported evidence, not a P400 rerun. This review ran no lane tests, authored no tests, and makes no new red/green, world-restart, packet, or client-visual claim. Findings are source-based; the proposed fixes remain unverified at runtime.

Ran `tools/progress.py --dry-run` with both work-copy path overrides; it exited 0, but the helper still rewrote `tools/progress.json` inside `build()` before the dry-run return. Restored that generated file to its previously clean HEAD contents, keeping this task limited to the requested review note. Final whitespace, file-size, and change-scope checks passed; the note contains no em dashes. Windows PowerShell was verified as 5.1.

P400 DONE
