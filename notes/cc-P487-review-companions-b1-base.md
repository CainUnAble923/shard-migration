# P487: companions batch 1 and its base, code review

Reviewed 2026-10-23. Notes only. No code, tests, settings, saves, or services were changed.

## Scope and evidence

- Code work copy: `d58c75e164cb580446a24338f2999e64b487d5c0`. Docs work copy before this note: `9c414ae4637a98f2a8bcbd4d3b7cbb72a515c75c`.
- Read both work-copy `AGENTS.md` files and the direction and task documents. Read `notes/cc-P369-cont-fixup-companions-b1-base-and-record.md`; recovered the absent `notes/cc-P264-companions-b1-base-and-record.md` with `git show 5d6f168:notes/cc-P264-companions-b1-base-and-record.md`.
- Checked the existing P379 merge review, P389 guide review, P41 design review, and P45 probes. No separate P264 or P369 review file was found in the available notes or their local history. The findings below do not repeat their known personality conflict, owner-loop/rank decisions, Owners-list gap, or deferred AI and parity work.
- Reviewed canonical `server/customizations/Companions/BaseCompanion.cs`, `CompanionLineage.cs`, `CompanionParty.cs`, and `CompanionSettings.cs`; the companion changes in `server/customizations/ClusterFSkillCaps.cs` and `ClusterFSkillGain.cs`; and `server/tests/Mobiles/Companions/CompanionBaseVerification.cs`.
- Also read P369's changed tests: `server/tests/Services/Revamped Dungeons/DespiseRevamped/WispOrbPossessionVerification.cs` and `server/tests/Mobiles/Normal/CC6Batch1CreatureVerification.cs`. No new finding in those flake fixes.
- Traced the inherited paths in the read-only `D:/UO/ModernUO-pinned`, verified at `d4531cd94b739613155225c234900de9f47d2c88` with a clean Git status, and checked the shard's auto-stable and pet-training slot patches. Did not read `server/uo/`.

All findings are from source inspection. Runtime reproduction, a real world restart, and live-shard behavior are **unverified**. No tests were added or run, consistent with this notes-only task and its lane-test setting of none. In the engine citations below, `pinned/` means `D:/UO/ModernUO-pinned/Projects/`.

## Findings

1. **bug** - `server/customizations/Companions/BaseCompanion.cs:313`: A full reload resets an equipped elemental weapon's damage split to physical because `AfterCompanionLoad` runs while item shells still lack their loaded layer and parent, and item deserialization does not call `OnItemAdded` to correct it later. Recompute after all items load, or read the equipped weapon when calculating damage, and add a cold-load test with an elemental weapon.

2. **bug** - `server/customizations/Companions/CompanionParty.cs:108`: The bond is established only through `Join`, but an inherited pet transfer bypasses `Join` and explicitly clears `IsBonded`, so a transferred companion can die permanently instead of becoming a ghost. Block ordinary pet transfers until a companion transfer path exists, or preserve the bond in that path and test death after transfer.

3. **bug** - `server/customizations/Companions/CompanionParty.cs:61`: The companion count limit is checked only by `CanTake` callers, so stock pet transfers let a loop-0 owner receive a third one-slot companion while still below the five-slot follower cap. Enforce the companion count limit when issuing and accepting transfers, with a regression case where slots fit but the party is full.

4. **bug** - `server/customizations/Companions/CompanionParty.cs:108`: Bonding does not exempt a living companion from the hourly pet loyalty sweep, so an idle companion can lose all loyalty over ten hourly checks without food or command gains and be released despite the design's promise that companions never go wild. Exempt controlled companions from involuntary loyalty release through a hook that recognizes companions and add a timed regression that also checks ordinary pets keep their existing behavior.

5. **bug** - `server/customizations/Companions/CompanionParty.cs:141`: Disabling `clusterf.companions.enabled` after an owner logs out makes the next login skip recovery, leaving the saved companion on `Map.Internal`, stabled and still consuming follower slots with no player recovery path. Recover already-away companions independently of the enable flag, or provide a safe disable transition, and test enabled logout followed by disabled login.

6. **risk** - `server/customizations/Companions/CompanionParty.cs:28`: A save taken while the owner is online records the companion in the world with `AwayWithOwner == false`, but after a restart the engine internalizes the player without firing Logout, startup auto-stabling skips the companion, and its login handler ignores that false flag. Reconcile unroomed companions with offline owners after world load and test a restart from an online-owner save, including a ghost companion that would otherwise face the abandonment sweep.

7. **risk** - `server/tests/Mobiles/Companions/CompanionBaseVerification.cs:61`: `RoundTrip` deserializes a copy using the still-live original's serial, so equipment and owner references can resolve to existing objects and mask the cold-load problem above; the lifecycle fact also calls helpers directly and never kills or releases a companion. Add isolated load coverage with freshly loaded owners and equipment, plus real-event cases proving death stays ghosted through logout/login and release or deletion frees slots once without bringing the companion back.

## Supporting source paths

| Finding | Source trace |
|---|---|
| 1 | `pinned/Server/Serialization/Persistence.cs:58` creates entity shells before loading payloads; `pinned/Server/World/World.cs:661` and `:684` put items after mobiles; `pinned/Server/Mobiles/Mobile.cs:6475` loads item references and `:7535` looks up weapons by layer; `pinned/Server/Items/Item.cs:2912` restores the parent directly. Our `BaseCompanion.cs:280` requires the loaded weapon parent and `:285` overwrites the saved split. `pinned/UOContent/Items/Weapons/BaseWeapon.cs:2345` reads that split for creatures. |
| 2 | `pinned/UOContent/Mobiles/AI/BaseAI/OnSpeech.cs:420` permits the inherited transfer command; `pinned/UOContent/Mobiles/AI/BaseAI/TransferItem.cs:149` calls `SetControlMaster` directly and `:163` clears the bond. `pinned/UOContent/Mobiles/BaseCreature.cs:3482` gates ghost death on that bond. `Tamable = false` in our `BaseCompanion.cs:135` does not block transfer. |
| 3 | `pinned/UOContent/Mobiles/AI/BaseAI/TransferItem.cs:77` validates only follower slots; `pinned/UOContent/Mobiles/BaseCreature.cs:3770` repeats the slot check. Neither reaches `CompanionParty.CanTake`. |
| 4 | `pinned/UOContent/Mobiles/BaseCreature.cs:6008` includes controlled, commandable living companions; `:6014` subtracts ten loyalty and `:6046` releases them. `pinned/UOContent/Mobiles/AI/BaseAI/PetOrders.cs:490` removes the name, `:498` clears the bond, and `:503` drops the master. `docs/companions/companions-squire-evo-research.md:537` states the no-going-wild intent. |
| 5 | `CompanionParty.cs:132` sets the saved away flag; `BaseCompanion.cs:308` restores `IsStabled` on load even while disabled; `CompanionParty.cs:141` returns before clearing either flag. `BaseCompanion.cs:234` also excludes it from the ordinary auto-stable route. |
| 6 | `pinned/Server/Mobiles/Mobile.cs:6510` moves loaded players to Internal without invoking Logout; `pinned/UOContent/Mobiles/PlayerMobile.cs:1064` handles startup pets only through auto-stabling, which our patch skips for companions. `CompanionParty.cs:150` only restores already-away companions; `pinned/UOContent/Mobiles/BaseCreature.cs:5987` removes unprotected abandoned ghosts. |
| 7 | `CompanionBaseVerification.cs:54` leaves the original registered; `:167` and `:185` invoke the logout/login helpers directly; `:178` tests only an unowned away copy. The existing equipped-weapon assertions at `:325` never deserialize equipment. |

## Checks with no new finding

No additional follower-count drift was found in `ApplySlotCost`: it subtracts the old slots, changes the cost, then adds the new slots. A bonded death keeps the creature and its slots; stock release clears control and frees those slots, and a released ghost is deleted. There is no unconditional resurrection in the companion login code, and no new cannot-dismiss path was found.

No auto-loot implementation exists in this batch, so no new wrong-corpse looting finding applies. Companion combat targeting remains the explicitly deferred AI work already covered by P41/P45 and P264, rather than a new finding here. No new saved-field ordering or lineage-counter defect was found under the normal intact-save path.

Only this review note is intended to change. Progress regeneration was omitted because it writes unrelated status artifacts, including `progress.json` even in its current `--dry-run` implementation.

P487 DONE
