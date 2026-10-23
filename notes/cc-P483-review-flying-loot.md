# P483: flying loot review

Reviewed 2026-10-23 against ShatteredLegacy `d58c75e` and shard-migration `387c68f`. Notes only. No code changes.

Read `cc-P366-cont-fixup-cont-loot-box-flying-loot.md` and the related P379 merge review first. P242 and P360 original notes are absent from this work copy. P379's merge and art-ID findings are not repeated here; P378's proposed playtests were also consulted.

## Findings

1. **risk**: `server/customizations/LootBoxes/ClusterFFlyingLoot.cs:148`: tier 4 and higher boxes send the opener's position and reward animation to every nearby client, including viewers behind walls or unable to see a hidden opener, because pinned `Projects/Server/Effects.cs:465` broadcasts without visibility or line-of-sight checks; this exposes a cosmetic effect, not an item transfer. Filter public recipients with `CanSee(pm)` and `InLOS(pm)` while preserving the opener's effect, and verify hidden and obstructed cases before changing the existing fanfare-style audience policy.

2. **risk**: `server/tests/Misc/LootBoxFlyingLootVerification.cs:144` and `:280`: the audience assertions inspect only `ClusterFFlyingLoot.Sent` and its `Major` flag, so the test would still pass if a private effect were broadcast or a major effect reached nobody. Capture actual effect packets for the opener, a nearby observer, a distant observer, and an observer on another map, and assert recipients, coordinates, art ID, speed, and duration for each tier boundary and suppression case.

3. **risk**: `server/tests/Misc/LootBoxFlyingLootVerification.cs:280` and `server/tests/Misc/LootBoxFanfareVerification.cs:187`: neither delivery test forces backpack rejection, leaving the bank fallback and preservation of rewards under item or weight limits untested. Add full-pack cases with known gold, stackable quantities, an insured weapon, and a blessed cosmetic, including an already-full bank, and check exact ownership, quantities, insurance and blessing after the box deletes itself with flying loot both enabled and disabled.

## Checks with no defect found

- **Wrong player:** `LootBoxItems.cs:192` checks the account and `:198` requires the box in the opener's backpack before the player-facing open path; `:253` delivers each reward to that same player. The private animation uses that player's `NetState` at `ClusterFFlyingLoot.cs:150`.
- **Full pack:** `ClusterFGuildPromotion.cs:236` tries the backpack, then `:242` calls `pm.BankBox.DropItem`. Pinned `Projects/Server/Mobiles/Mobile.cs:1614` supplies the player's bank, creating one if necessary, and `Projects/Server/Items/Container.cs:464` inserts directly without a capacity refusal. I found no full-pack item-loss path by source inspection, including a full bank.
- **Insured or blessed items:** the effect only classifies the box's fixed rewards and sends an art ID. It does not search corpses or other players' inventories, strip insurance, change `LootType`, or move items; the blessed box cosmetic at `LootBoxItems.cs:341` is a legitimate reward to animate.

## Scope and limits

Reviewed canonical `server/customizations/LootBoxes/ClusterFFlyingLoot.cs`, `LootBoxItems.cs`, `ClusterFLootBoxes.cs`, `LootBoxRoller.cs`, `ClusterFFanfare.cs`, and the delivery helper in `server/customizations/ClusterFGuildPromotion.cs`; read `server/tests/Misc/LootBoxFlyingLootVerification.cs` and `LootBoxFanfareVerification.cs`.

Also inspected the flying-loot entries in `player-package/vendor/shattered-legacy-art/registry.csv`, `records.json`, and `SOURCE.txt`, the related merge checks and flying-loot fact in `player-package/tests/Build-UoOverrides.Tests.ps1:640`, and the relevant `CHANGELOG.md` entry and `VERSION`. Upstream behavior was checked in the read-only ModernUO source at `d4531cd94b739613155225c234900de9f47d2c88`.

This was a source review. No tests were added or run, and no build or client was launched. Actual client rendering through walls, animation timing, packet delivery, and save/reload behavior remain unverified. The full package test script includes a remote shard probe, so it was not executed. The progress reporter was not run because its `--dry-run` path still writes `tools/progress.json`, outside this task's notes-only deliverable.

P483 DONE
