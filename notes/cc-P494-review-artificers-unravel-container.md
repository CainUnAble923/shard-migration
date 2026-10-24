# P494: review of the Artificers' Unravel Container (P176)

Reviewed on 2026-10-23 in the Verite work copies. Notes only; no code changes.

## Findings

1. **bug** - `server/customizations/ArtificersImbueGump.cs:2042`: Confirmation counts the bag's contents when the page opens, but approval snapshots its contents again, so adding a magic item while the page remains open destroys it despite the smaller displayed count. Save the eligible item list with the confirmation, recheck eligibility and direct parent before destroying each saved item, and test adding and swapping items between preview and approval.

2. **bug** - `server/customizations/ArtificersImbueGump.cs:1961`: The shared guard checks `LootType.Blessed` and `Newbied` but ignores `Item.BlessedFor`, so otherwise eligible magic gear with a personal blessing can be destroyed by bulk unravel or Full Disenchant. Also refuse `BlessedFor != null`, preserving the intentional single-item insurance policy, and add container and single-item regression cases with regular loot type and `BlessedFor` set.

3. **risk** - `server/customizations/ArtificersImbueGump.cs:1978`: Recovery ignores property magnitude: under the defaults, a mastered player's Basic Hit Life Leech 17 costs 2 shards and 1,020 gold to imbue, then pays 3 shards when unraveled, allowing repeatable shard creation at the cost of gold and replacement weapons. Scale recovery to the actual positive property value, cap it below the corresponding imbue cost, and test the Basic-tier purchase and recovery together; this imbalance predates P176's bulk path.

4. **risk** - `server/customizations/ArtificersImbueGump.cs:2031`: Only the selected container's lock is checked, so targeting an inner bag, locking its outer chest, and then approving still destroys the inner bag's magic items inside the locked chest. Check for locked ancestors up to the backpack at approval, using the existing `ILockable` protection pattern in `GuildResources.IsClosedToGuild`, and add a regression case for locking the ancestor after preview.

5. **risk** - `server/tests/Misc/UnravelContainerVerification.cs:133`: The mixed-bag test accepts any positive shard increase and checks the summary against that same increase, so excessive payouts pass, while its helper immediately approves and leaves confirmation-time changes untested. Assert the independent expected total of 8 shards for this fixture, force both essence-roll outcomes and verify exact deliveries, and add approval-time ownership, lock, protection-change, repeated-response, and full-destination cases.

## Supporting evidence

- Finding 1: `DrawUnravelContainerConfirm` at `ArtificersImbueGump.cs:1438` stores only counts in the rendered page; the gump retains the container reference. ServUO pub57's `Scripts/Services/LootGeneration/Imbuing/Gumps/ImbuingGump.cs:311` saves the list when constructing its confirmation and iterates that list at `:349`. Our execution-time snapshot differs from that source; a same-count item swap also escapes a count-only fix.
- Finding 2: pinned ModernUO's `Projects/Server/Items/Item.cs:4428` recognizes `BlessedFor` in `CheckBlessed`, and our `GuildResources.cs:89` also treats a non-null `BlessedFor` as blessed. The P176 test at `UnravelContainerVerification.cs:149` and its single-item test at `:185` cover only `LootType.Blessed`. ServUO's eligibility check also omits personal blessing, so this is an inherited protection gap to address in our shared guard. Whether any currently saved eligible gear has a personal blessing is unverified.
- Finding 3: the Hit Life Leech row at `ArtificersImbueGump.cs:308` has Full 50, ShardBase 7 and GoldBase 3,000; `ImbuingTable.cs:99` sets BasicFraction to 0.333; `ClusterFImbueKnowledge.cs:412` rounds Basic to 17. The scaling at `ArtificersImbueGump.cs:100` and `:114` truncates costs to 2 shards and 1,020 gold. Basic is a selectable tier (`:1209`, `:1242`, `:1721`), mastery removes the essence cost (`:1825`), successful imbuing spends those costs (`:1880`), and recovery pays integer half of 7 regardless of value (`:1979`). This is an economic risk, not a claim of free gold, weapon duplication, or a new P176 formula change.
- Finding 4: `CanUnravel` at `ArtificersImbueGump.cs:1960` tests backpack ancestry but no ancestor locks; `ContainerRefusal` checks only the selected bag. Pinned `Projects/UOContent/Items/Misc/Key.cs:186` can toggle the outer chest's lock while the confirmation remains open; our normal response handler does not repeat the targeting checks or walk ancestors.
- Finding 5: the fixture is two Hit Life Leech swords at 3 shards each and one Luck ring at 2, with plain items paying zero (`UnravelContainerVerification.cs:114`, `ArtificersImbueGump.cs:259`, `:308`, `:1979`). The bot's P176-1 check in `tools/playtest-bot/uobot/checks_p224_imbuing.py:600` likewise accepts any positive yield agreeing with the journal and does not change the bag between preview and approval. `UnravelSatchelVerification.cs:203` covers a forced successful single-item essence roll, and `:293` covers full-satchel fallback with backpack space; neither covers a full backpack during bulk unravel.

## Checks with no additional finding

No double unravel or duplicate payout was found on the normal player response path. The container loop snapshots direct children and calls `CanUnravel` before each payout, including its deleted-item guard (`ArtificersImbueGump.cs:1959`, `:2042`). Pinned `Projects/UOContent/Gumps/Base/GumpSystem.IncomingPackets.cs:63` validates that a submitted button exists, and `:157` removes the registered gump before dispatch, preventing ordinary replay of that same response. These conclusions come from source review, not a concurrency or packet-replay test.

No bulk destruction of items already marked `LootType.Blessed`, `Newbied`, insured, quest, or faction was found through the guarded path. Those flags and backpack ancestry are rechecked for each item at execution. The selected container's deletion, ownership and own lock are also rechecked at approval. Nested bags are skipped. The documented single-item insurance exception is intentional and is not a new finding.

No container eating items because a satchel or backpack rejects a reward was found. `ArtificersSatchel.Deliver` at `ArtificersSatchel.cs:96` tries the satchel and then `AddToBackpack`; pinned `Projects/Server/Mobiles/Mobile.cs:7587` places the reward in the world if the backpack rejects it. Full destinations can therefore leave essences at the player's feet, which is documented behavior. The skill check in `UnravelOne` is a gain opportunity, not a success gate: its false result still pays the rewards before deleting the source item. No arbitrary exception or crash recovery claim was verified.

## Scope and validation

Read both work copies' AGENTS.md, `docs/direction-decision.md`, `docs/tasks.md`, and `notes/cc-P176-cont-artificers-unravel-container.md`. No separate P176 review was found among tracked notes. Also checked related P137 and P383 notes and the P383 guide review. Their documented insurance policy, ungated unravel behavior, and custom reward model are not repeated as findings.

P176 commit `c50973108092d12490902fc4e82e021fbaab027f` is in local `main` history. Code HEAD and main were both `579ad58f8f478280b03b8cf80f1ee9a5b3001a27`; the read-only ModernUO source is at `d4531cd94b739613155225c234900de9f47d2c88`.

Reviewed the relevant paths in `ArtificersImbueGump.cs`, `ArtificersSatchel.cs`, `GuildResources.cs`, `Imbuing/ClusterFImbueKnowledge.cs`, and `Imbuing/ImbuingTable.cs`; the P176 CHANGELOG entry and VERSION; `UnravelContainerVerification.cs` and `UnravelSatchelVerification.cs`; related coverage in `ImbuingReworkVerification.cs`, `ImbueSelfRepairGateVerification.cs`, `ImbueAllSlayersVerification.cs`, `ImbueEssenceSourcesVerification.cs`, and `ImbueExtractDurabilityVerification.cs`; and the P176 portions of the bot implementation, `testing/bot-triage.md`, and `testing/playtest-steps.json`. Pinned and ServUO evidence paths are cited above. Did not read `server/uo/`.

This was source review. No tests were added or run, no build or live-shard reproduction was performed, and no red/green result is claimed. Current saved-item state, active imbuing configuration overrides, and client behavior remain unverified. No service, remote machine, account, branch, or commit was changed.

`tools/progress.py --dry-run` completed with exit 0 against these work copies. Its `tools/progress.json` side effect was restored byte for byte from the pre-run contents. Only this review note is changed. The note is below 5 MB and contains no em dashes.

The review paused once at the Golem's budget stop request and resumed after authorization; all remaining review work listed at that checkpoint is now complete.

P494 DONE
