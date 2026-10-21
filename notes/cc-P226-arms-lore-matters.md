# cc-P226: Arms Lore matters more and trains to 200 (F-26 parts 1 to 4 and 6)

Written 2026-10-20 by the Copper Golem (Opus), on branch golem/Copper/P226 of both repos. Pinned paths are relative to
`Projects/UOContent` at d4531cd94 (the pinned clone is not on this PC; I read the pristine commit with `git archive HEAD`
out of `sl-uo-builder:latest`, and the fully patched tree from the same image). "Ours" is `D:\ShatteredLegacy\server`.

## Headlines

1. **Crafting, rescaled to 200 (part 1).** Exceptional weapon damage increase is 35 + 15 x (Arms Lore / 200): 35 at 0,
   42 at 100, 50 at 200 (pinned 35 + Arms Lore / 20: 35, 40, 45). Exceptional armor's extra resist points stay
   Arms Lore / 20 but stop at **10 a piece** (pinned uncapped: 240 Arms Lore gave 12). The cap of 50 is still pinned's.
2. **Gear lasts longer (part 2).** The wielder's or wearer's Arms Lore saves Arms Lore / 400 of the wear: 25% at 100,
   50% at 200, linear. One call per item kind: weapon, body armor, shield. Self Repair is rolled first and unchanged.
3. **Field maintenance (part 3).** Arms Lore on your own damaged weapon or armor (pack or worn), when the inspect
   succeeds, restores **2 + Arms Lore / 10** durability (12 at 100, 22 at 200), never past the maximum, after a
   **(200 - Arms Lore) / 400** chance to lose 1 maximum (50% at 0, 25% at 100, 0 at 200). Once per **10 seconds**.
   A smith's repair still restores the item to full.
4. **Better smith repairs (part 4).** A player's tool repair of a weapon or armor takes **Arms Lore / 10** points off
   pinned's weaken chance (`Engines/Craft/Core/Repair.cs:41-42`, rolled at `:287` weapons and `:357` armor). A repair
   deed and clothing stay pinned's. Blacksmithy 100, 1 point missing: 31% at Arms Lore 0 (measured 30.9% in the red
   run), 21% at 100 and 11% at 200 by the formula; the fact asserts 17-25% and 7-15% over 3,000 real repairs each.
5. **Gain path to 200 (part 6).** Followed cc-P66's hook G, the pattern every other skill uses past its stock top: a
   new Arms Lore row (inspect and field maintenance share the use's (0, 100) check) and an `ArmsLoreCrafted` roll after
   the crafting check, like Detect Hidden's found-something roll. Past 100 the window is the item's tier,
   **Difficulty +/- 50**, Difficulty = the material's craft requirement + 25 exceptional + 25 magic. A Valorite
   exceptional magic weapon is 149 (window 99 to 199), a Celestial exceptional magic one 250; plain iron is 0, so it
   teaches nothing past 50. Below 100 nothing differs from pinned. All gain is pinned's own roll (F-12: no free points).
6. **Facts, each red first:** 17 in `ArmsLoreMattersVerification` plus 7 new keys in `SkillGainRowKeysVerification`.
   Built as `sl-modernuo:cc-P226` (9e9309c0345f): **1,663 passed, 4 skipped (pinned's), 0 failed.**

## 1. What I read, and what pinned does today (re-verified on d4531cd94)

Read: `docs\feature-queue.md` F-26 and F-27, `notes\cc-P20-skill-scaling-research.md` (Arms Lore rows, section 2.1),
`notes\cc-P191-cont-earned-skill-gain.md`, `docs\fidelity-principle.md` (register format), ours
`ClusterFRareSelfRepair.cs`, `ClusterFSkillGain.cs`, `ClusterFCraftGain.cs`, `ClusterFMetalTiers.cs`,
`ClusterFWoodTiers.cs`, `patches\BaseWeapon-talisman-durability.patch`, `patches\BaseArmor-set-self-repair.patch`.

The entry's lines were as of 7c9215d97; on d4531cd94 they moved:

| What | Entry said | Today (pristine d4531cd94) |
|---|---|---|
| Exceptional weapon DI, 35 + AL / 20, cap 50 | `BaseWeapon.cs:700-711` | `Items/Weapons/BaseWeapon.cs:671-686` (`:677` the bonus, `:684` the check) |
| Exceptional armor + AL / 20 points, uncapped | `BaseArmor.cs:595-631` | `Items/Armor/BaseArmor.cs:569-606` (`:571` the bonus, `:605` the check) |
| Inspect checks (0, 100) | `ArmsLore.cs:33, :89, :107` | unchanged: `Skills/ArmsLore.cs:33` weapon, `:89` armor, `:107` barding |
| Weapon wear in combat | | `BaseWeapon.cs:2064-2098`: acid monsters always, else 1 in 25 hits; Self Repair `:2076`, the point `:2080-2097` |
| Armor wear | | `BaseArmor.cs:727-780` (`OnHit`): 25% of hits, Self Repair `:737`, wear `:743` (bashing: absorbed / 2, else 0 or 1) |
| Shield wear | | `Items/Shields/BaseShield.cs:31-76` (`OnHit`), Self Repair `:35`, wear in `TryLowerDurability` `:78-112` |
| Smith repair loss | | `Repair.cs:41-42` `GetWeakenChance` = 40 + missing - skill / 10, `:44-45` `CheckWeaken`, rolled `:287` (weapon), `:357` (armor), `:428` (clothing) |

The patched build tree (every shard patch applied, from the builder image) differs from pristine near none of these
lines: BaseWeapon's other hunks are at 873, 1528, 1569, 1639, 1871, 2207, 2542; BaseArmor's at 726 and 737 (Self Repair's
`EffectiveSelfRepair`); BaseShield, ArmsLore and Repair are untouched by any other patch.

## 2. What changed

All numbers are in one new file; the pinned files only call in. Five small patches, applied last
(`docker/uo/apply-patches.sh`, after the void-pool patch, with a comment block):

| File | Lines (patched tree) | What |
|---|---|---|
| `customizations/ClusterFArmsLore.cs` (new) | `:52` `ExceptionalDamageBonus`, `:56` `ExceptionalResistBonus`, `:62` `WearSaved`, `:65` `ReduceWear`, `:88` `SavesWeaponWear`, `:93` `MaintenanceRestore`, `:96` `MaintenanceMaxLossChance`, `:103` `FieldMaintenance`, `:147` `RepairWeakenChance`, `:159` `Difficulty`, `:178` `MaterialTier`, `:204` `Window` | every number and rule |
| `patches/BaseWeapon-arms-lore.patch` | `BaseWeapon.cs:678` bonus, `:686` crafted roll, `:2092` wear point | 3 hunks, 1 to 4 lines each |
| `patches/BaseArmor-arms-lore.patch` | `BaseArmor.cs:572` capped bonus, `:607` crafted roll, `:752` wear | 3 hunks |
| `patches/BaseShield-arms-lore-wear.patch` | `BaseShield.cs:81` | top of `TryLowerDurability`, so both its callers (AOS hit, pre-AOS parry) |
| `patches/ArmsLore-field-maintenance.patch` | `ArmsLore.cs:82` weapon, `:102` armor | after the successful inspect's messages |
| `patches/Repair-arms-lore-weaken.patch` | `Repair.cs:44` | `GetWeakenChance` and `CheckWeaken` take `gear = false`; the weapon and armor calls pass `true` |
| `customizations/ClusterFSkillGain.cs` | `:406` the Arms Lore row in `TryRow`; `:491` `ArmsLoreCrafted`, `:501` `ArmsLoreCraftedChance`; header comment | hook G |
| `docker/uo/apply-patches.sh` | the five `apply_patch` lines and their comment | |
| `tests/Skills/ArmsLoreMattersVerification.cs` (new), `tests/Skills/SkillGainRowKeysVerification.cs` | | section 3 |
| `CHANGELOG.md`, `VERSION` | `2026.10.20.17` | Added, Changed, Staff |

Why patches and not hooks: the bonus and the wear are locals inside `OnCraft`, `OnHit` and a private shield method;
`GetWeakenChance` is private in a private nested target; the inspect target is private. No event or virtual reaches any
of them. Each hunk is one call; the logic is all in `ClusterFArmsLore`.

**Clash note (P228).** My BaseWeapon hunks are at the exceptional bonus lines (`:677`, `:684`) and the wear point
(`:2086-2093`); BaseArmor at `:571`, `:605` and `:743`. If P228 edits the exceptional block of either `OnCraft`, the
second to merge regenerates its patch against the other's; both are one-line hunks.

### Design details and the choices I made

- **Which Arms Lore.** `Skills.ArmsLore.Value` everywhere, as pinned's crafting bonus already reads it: worn bonuses
  count, and so does the stat offset below Base 100 and the Human racial floor of 20. So a Human with Base 0 saves 5%
  of wear and restores 4 per maintenance. Clamped to 200 in every formula, so a bonus above the cap buys nothing extra.
- **Wear, per item kind.** Weapon: an extra `else if` after Self Repair's roll skips the one point with chance
  WearSaved. Armor and shield: each point of the wear amount is kept with chance 1 - WearSaved (a bashing hit's 3
  points can become 0 to 3), so the expected wear is exactly scaled. Creatures count too (the rule says "the wielder"),
  which only matters for gear a creature wears.
- **Self Repair (F-27, `ClusterFRareSelfRepair.cs`).** Untouched. Its roll comes first in all three places
  (`BaseWeapon.cs:2076`, `BaseArmor.cs:737` through `BaseArmor-set-self-repair.patch`'s `EffectiveSelfRepair`,
  `BaseShield.cs:35`); when it fires the item gains 2 and Arms Lore never rolls. Arms Lore only thins the wear that gets
  past it, so the two stack: Self Repair 1 at Arms Lore 200 wears 0.9 x 0.5 = 45% as fast and repairs 10% of the time.
- **`BaseWeapon-talisman-durability.patch`.** That hunk passes the hit to an `IWearableDurability` talisman (the Pet
  Mimic) from `AbsorbDamage`; it is not a `BaseWeapon` or `BaseArmor` and keeps its own wear. Arms Lore does not reach it
  (it is not gear Arms Lore works on), and nothing there changed.
- **Field maintenance, the numbers.** Restore 2 + AL / 10 against a smith's full repair: typical weapons have 30 to 255
  maximum, so a smith is always at least as good per use and better on anything missing more than 22. Max loss
  (200 - AL) / 400 is milder than a smith's 31% at GM from 25% down at 100 and ends at 0, as the entry asked. Only on
  success of the inspect's own check, so it gives no extra skill roll; the check at 0 skill effectively never succeeds.
  An item with maximum 1 never loses it. The 10 s wait is `BeginAction(typeof(ClusterFArmsLore))` with a timer; the
  inspect still works during it, with "You must wait a moment before tending your gear again." Messages are plain
  `SendMessage` text (no cliloc exists for them).
- **Smith repairs.** Only `m_Deed == null` and only weapons and armor. Clothing (a tailor's repair) is not Arms Lore's
  business, and a deed's level is the deed's, not the player's.
- **Tier difficulty.** Material: `ClusterFMetalTiers.RequiredSkill` (stock metals 65 to 99, post-Valorite 112.5 to 200,
  Dawnstone 45), `ClusterFWoodTiers.RequiredSkill` then pinned's OSI woods (`DefCarpentry.cs:602-607`: 65, 80, 95, 100),
  leathers from `DefTailoring.cs:663-665` (65, 80, 99; Burrowhide 45), scales 0. Exceptional +25. Magic +25: any
  weapon or armor attribute, skill bonus or weapon/armor attribute, **except the damage increase every exceptional
  weapon carries** (`BaseWeapon.cs:673`): the first red run showed an exceptional craft counting as magic without it
  (tier 149 for a non-runic Valorite katana). It is now 124.
- **Gain, past 100.** The row returns `(Difficulty - 50, Difficulty + 50)`; hook G then rolls pinned's `CheckSkill` on it
  with the worn bonus added to the top, only when the use's stock window says "no challenge". Valorite exceptional
  magic at 150: chance (150 - 99) / 100 = 0.51. To train past 150 you need about Valorite exceptional with magic, or a
  post-Valorite exceptional; past 175, post-Valorite. The barding check (`ArmsLore.cs:107`) is not a row.

## 3. Tests

`server\tests\Skills\ArmsLoreMattersVerification.cs`, every fact through a real pinned call site:

| Fact | What it drives | Pinned (red run) | Now |
|---|---|---|---|
| A1 `ExceptionalWeaponDamageIncreaseRescaledTo200` (0, 100, 200) | `Katana.OnCraft`, exceptional, iron | 35, **40**, **45** | 35, 42, 50 |
| A2 `ExceptionalArmorResistBonusIsCappedAtTen` | `PlateChest.OnCraft` at Arms Lore 240 (200 + a +40 mod) | **27** points (15 + 12) | 25 (15 + 10) |
| B1 `ArmsLoreSavesAQuarterOfTheWearAt100AndHalfAt200` (weapon, armor, shield) | 6,000 hits: `Katana.OnHit` on a blessed Slime (acid wears every hit), `PlateChest.OnHit` and `HeaterShield.OnHit` from a mace | weapon and shield **100%** at 100 and 200; armor 98% and 96% (seed noise) | in 70-80% at 100 and 45-55% at 200 |
| C1 `FieldMaintenanceRestoresDurabilityUpToTheMaximum` (100/30, 200/30, 200/5) | `ArmsLore.OnUse`, then the target on the katana in the pack | nothing restored | +12, +22, +5 to full |
| C1 `FieldMaintenanceIsOwnGearOnlyAndWaitsTenSeconds` | a katana on the ground, worn plate, a second use at once, a use after 11 s (test clock) | nothing | ground none; worn 50 to 62; refused; 74 |
| C2 `FieldMaintenanceNeverCostsMaximumAt200AndAQuarterOfTheTimeAt100` | 2,000 seeded maintenances each | **0%** at 100 (no maintenance) | 0 at 200; 21-29% at 100 |
| C3 `SmithRepairStillRestoresMoreThanFieldMaintenance` | 60 missing at Arms Lore 200: maintenance vs a real repair at an anvil and forge | maintenance 40 | 62 vs 100 |
| D1 `SmithRepairLosesMaximumLessOftenWithArmsLore` | 3,000 real repairs each, Blacksmithy 100, 1 point missing | 30.9%, **31.9%**, **30.4%** | 27-35% at 0, 17-25% at 100, 7-15% at 200 |
| E1 `InspectAt150GainsOnlyOnGearOfAHighEnoughTier` (true, false) | the Arms Lore target at Base 150, gain rolls held | 150 -> **150** on Valorite exceptional magic | gains on it (tier 149); plain iron stays 150 |
| E2 `CraftingAnExceptionalValoriteWeaponAt150Gains` | `Katana.OnCraft` from Valorite ingots at 150 | **150** | gains (tier 124) |

`SkillGainRowKeysVerification` gains seven keys (the two inspect checks, the two field-maintenance calls, the two crafting
checks and the two crafted rolls; each counted in its file and in all of UOContent), so an upstream change to any keyed
line stops the build.

The test player is an Elf (no Human +20 floor), and the facts at Arms Lore 0 zero the player's stats after equipping,
because below Base 100 a skill's Value carries a stat offset; each asserts Value equals the intended Arms Lore.

Runs, all through `docker/uo/build.sh -t sl-modernuo:cc-P226` with the docker-build lock held:

| Run | Tree | Result |
|---|---|---|
| red 1 (`--tests-only`) | the five patches skipped by name (`SKIPPED_PATCHES`) and the Arms Lore row disabled, both temporarily | 18 failed: 15 of the new facts for the stock reason, 3 row keys (the hooks absent). The three wear facts failed on my own `EquipItem` assert, not on wear: fixed (`AddItem`) |
| red 2 (`--tests-only`) | same, wear facts fixed, magic tier fixed | **all 17 new facts and the 3 call-site keys failed, each for the stock reason** (values above); 1,645 others passed |
| green 1 (full) | real tree | 1,662 passed, 1 failed: `WispOrbPossessionVerification` Sagittarri vs Phantom, the known flaky fact (D56; P50, P52, P82, P142, P193 saw it), green in both red runs; all 17 Arms Lore facts passed |
| green 2 (full, unchanged) | real tree | **1,663 passed, 4 skipped, 0 failed; image `sl-modernuo:cc-P226` built (9e9309c0345f)** |

The image predates the changelog edit (the CHANGELOG and VERSION change was made after the build), so a shard on it
shows `2026.10.20.16`'s notes; the code is the same.

## 4. Deviations and decisions for Chase

All are **Ours** (F-26, approved 2026-10-02). Wording for `docs\fidelity-principle.md`'s numbered register, for the
overseer to number:

| What changed | What a player notices | Status | Note |
|---|---|---|---|
| Exceptional weapon damage increase 35 + 15 x (Arms Lore / 200), not 35 + Arms Lore / 20 (cap 50 kept) | 42% at GM Arms Lore, 50% at 200, where OSI gives 40% and 45% | `visible` | `cc-P226` |
| Exceptional armor's Arms Lore resist bonus capped at 10 points a piece | nothing below 200 Arms Lore; above it (worn bonuses) no more than 10 | `visible` | `cc-P226` |
| The wielder's or wearer's Arms Lore saves Arms Lore / 400 of weapon, armor and shield wear | gear wears a quarter slower at 100, half at 200 | `visible` | `cc-P226` |
| Field maintenance: Arms Lore on your own damaged weapon or armor restores 2 + Arms Lore / 10, with a (200 - Arms Lore) / 400 chance to lose 1 maximum, once per 10 s | a new use of Arms Lore; no forge needed | `visible` | `cc-P226` |
| A player's tool repair of a weapon or armor: weaken chance lowered by Arms Lore / 10 | smiths with Arms Lore lose maximum durability less often | `visible` | `cc-P226` |
| Arms Lore gains past 100 (hook G row and crafted roll) on the item's tier: material requirement + 25 exceptional + 25 magic, +/- 50 | Arms Lore trains to 200 on fine gear; OSI stops it at 100 | `visible` | `cc-P226` |

Decisions I made that Chase may want to change (each a one-number edit in `ClusterFArmsLore.cs`):

1. **Field maintenance restore 2 + Arms Lore / 10 and max loss (200 - AL) / 400, 10 s wait.** The prompt asked me to
   propose these. The restore keeps a smith better on anything missing more than 22 points.
2. **Value, not Base**, for every Arms Lore read (pinned's choice in OnCraft). Worn Arms Lore bonuses count, capped at
   200 in each formula.
3. **Creatures' Arms Lore also saves wear** on what they wear ("the wielder's"). It only matters for monster-worn loot.
4. **Tier: +25 exceptional, +25 magic, +/- 50 window.** Plain iron teaches nothing past 50; Valorite exceptional
   magic (149) to 199; a Celestial exceptional to 250, past the cap. If 100 to 150 should be reachable on cheaper gear,
   widen the window (`TierHalfWidth`).
5. **Not covered:** the Pet Mimic talisman's wear (not gear), Ilhenir's acid splash (`Mobiles/Monsters/ML/Special/
   Ilhenir.cs:351`, an `IDurability` hit of its own), clothing and jewellery wear, and repair deeds.

## 5. For Chase (what to check in the client, on the test shard with this image)

1. As a smith with Arms Lore 100, craft exceptional iron weapons until one is exceptional: the damage increase reads
   42%. At 200 Arms Lore, 50%.
2. Craft exceptional plate at 200 Arms Lore (or with an Arms Lore bonus item on): total resists are 15 + 10 points above
   the plate's base, never more.
3. Damage a weapon (fight a slime), then Arms Lore it from your pack: the inspect lines, then "You tend to the wear,
   restoring 12 durability." at 100. Again at once: "You must wait a moment...". After 10 s it works again.
4. With Arms Lore 150 locked up, Arms Lore a Valorite exceptional weapon with any magic property: the skill rises.
   A plain iron one does not.
5. Repair at an anvil with Arms Lore 0 and then 200: the "severely damaged" maximum loss shows up far less at 200.

## 6. Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, before this notes file was
written (it adds one more pending file in docs):

```
=== code  (D:\ShatteredLegacy) ===
  12 file(s) pending:
    CHANGELOG.md
    VERSION
    docker/uo/apply-patches.sh
    server/customizations/ClusterFSkillGain.cs
    server/tests/Skills/SkillGainRowKeysVerification.cs
    server/customizations/ClusterFArmsLore.cs
    server/patches/ArmsLore-field-maintenance.patch
    server/patches/BaseArmor-arms-lore.patch
    server/patches/BaseShield-arms-lore-wear.patch
    server/patches/BaseWeapon-arms-lore.patch
    server/patches/Repair-arms-lore-weaken.patch
    server/tests/Skills/ArmsLoreMattersVerification.cs
  dry run: would add, commit and push

=== docs  (D:\UO\shard-migration) ===
  4 file(s) pending:
    testing/bot-runs/2026-10-20-2027/email-before.txt
    testing/bot-runs/2026-10-20-2027/real-shards-before.json
    testing/bot-runs/2026-10-20-2028/email-before.txt
    testing/bot-runs/2026-10-20-2028/real-shards-before.json
  dry run: would add, commit and push

Repo Result
---- ------
code dry run
docs dry run
```

Neither repo BLOCKED. Repo size: the largest new file is `ArmsLoreMattersVerification.cs` (about 20 KB); nothing near
5 MB, and all scratch (the pinned export, patched copies, build logs) is in the session scratchpad outside both repos.

P226 DONE
