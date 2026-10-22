# P446: Review of creature levels and Appraisal (P239)

Reviewed October 22, 2026. Review notes only. No code or tests changed.

## Findings

1. **bug** - `server/customizations/ClusterFCreatureLevels.cs:471`: The card prints the raw `DamageMin` and `DamageMax`, so an NPC such as a Banker, which leaves both at their default, is described as dealing `Damage -1--1` even though combat resolves a usable weapon or fists range. Resolve the base range through the equipped `BaseWeapon.GetBaseDamageRange`, label it as base damage, and add a card assertion for an NPC without `SetDamage`.

2. **bug** - `server/customizations/ClusterFCreatureLevels.cs:479` and `:497`: A Skeletal Dragon is described as "Breathes fire" even though its breath deals cold damage, and a HellSteed gets the same description for chaos breath, because the Bard helper recognizes every `FireBreath` subclass and the later ability loop suppresses their actual names. Describe the resolved breath ability and its damage types, with card tests for cold and chaos breath alongside the existing Dragon case.

3. **bug** - `server/customizations/ClusterFCreatureLevels.cs:484` and `:489`: A paragon GiantSpider's card reports Regular hit poison and Regular immunity, while its actual melee and immunity checks increase both to Greater poison. Apply the same paragon adjustment used by combat when describing poison, and test an ordinary spider and its paragon with poisons initialized.

4. **bug** - `server/customizations/ClusterFCreatureLevels.cs:494` and `:503`: The Special line shows "Monster Ability Group" for a Betrayer instead of its Colossal Blow and Poison Gas Area Attack, while a FleshRenderer shows only one randomly sampled weapon ability instead of its Dismount and Paralyzing Blow options. Use a read-only ability inventory that expands groups and lists possible weapon abilities, and add these creatures to the card tests so the description identifies their actual options consistently.

5. **risk** - `server/customizations/ClusterFCreatureLevels.cs:550`: Every card row is a single cropped label only 424 pixels wide, and even the ordinary five-resistance row with values of 30 measures 447 pixels in the local client font, so the last details can be cut off; `server/tests/Mobiles/CreatureLevelsVerification.cs:411` checks the stored strings rather than what fits on the card. Wrap or split long rows and size the card accordingly, then verify a complete resistance row and a long Special line in TazUO.

6. **risk** - `server/tests/Mobiles/CreatureLevelsVerification.cs:204`: The level tests construct fresh creatures and change an override in memory, but none saves and reloads a creature, leaving the requested restart behavior without regression coverage. Add a save/load test that compares level and con for an ordinary creature and a paragon with fixed stats, skills, and poison, without introducing a separately stored level.

## Evidence

Paths in the findings are relative to the code work copy. Pinned paths below are relative to `D:\UO\ModernUO-pinned\Projects\UOContent`; its HEAD was verified as `d4531cd94b739613155225c234900de9f47d2c88`.

- Damage: `Mobiles/BaseCreature.cs:572` and `:582` initialize the damage fields to -1. `Mobiles/Townfolk/Banker.cs:19` uses the vendor constructor, and `Mobiles/Vendors/BaseVendor.cs:615` sets stats without setting damage. `Items/Weapons/BaseWeapon.cs:2428` resolves a creature's explicit damage, nonhuman fists fallback, or the weapon's own range.
- Breath: `Items/Skill Items/Musical Instruments/BaseInstrument.cs:243` checks the common ability type. `Mobiles/Monsters/Reptile/Magic/SkeletalDragon.cs:60` supplies ColdBreath, and `Mobiles/Animals/Mounts/HellSteed.cs:20` supplies ChaosBreath. Their implementations in `Mobiles/Abilities/Fire Breath/ColdBreath.cs:5` and `ChaosBreath.cs:5` set cold or chaos to 100 and fire to zero.
- Poison: `Mobiles/Monsters/Arachnid/Melee/GiantSpider.cs:51` and `:52` return Regular immunity and hit poison. `Mobiles/BaseCreature.cs:1931` and `:2687` apply the paragon increase before checking immunity or poisoning a melee target. The Appraisal card reads the original properties directly.
- Ability inventory: `Mobiles/Monsters/Humanoid/Magic/Betrayer.cs:101` groups the two abilities, and `Mobiles/Abilities/MonsterAbilityGroup.cs:6` is the wrapper the card names. `Mobiles/Monsters/AOS/FleshRenderer.cs:57` randomly chooses between its two weapon abilities on each call.
- Card width: the server sets `W = 460` and passes `W - 36` to `AddLabelCropped`. In the local client source, `D:\UO\tazuo-sl-build\src\src\ClassicUO.Client\Game\UI\Controls\CroppedText.cs:15` sets `FontStyle.Cropped` and uses font 1; `ClassicUO.Assets\FontsLoader.cs:1230` sums each glyph's horizontal offset, width, and one pixel, with an eight-pixel fallback for space. A read-only calculation using `D:\UO\UltimaOnlineVanilla\unifont1.mul` measured `Resists: Physical 30%  Fire 30%  Cold 30%  Poison 30%  Energy 30%` at 447 pixels and `Special: Casts spells (Magery 100), Breathes fire, Immune to Lethal poison` at 446 pixels. These are font measurements, not a client screenshot or a completed client play test.

## What matched

I found no level-driven damage or loot scaling. The production callers of `ClusterFCreatureLevels.Level` use it for display, the diagnostic report, or the documented Appraisal gain window in `ClusterFSkillGain.cs:420`; the level calculation reads creature state and does not change damage, stats, loot, or Bard difficulty.

I found no stored creature level that would be lost on restart. `ClusterFCreatureLevels.cs:169` recomputes it, while pinned `Mobiles/BaseCreature.cs:539`, `:549`, `:559`, and `:927` declare serialization for maximum-stat seeds and paragon state. Actual save/load equality remains unverified, as finding 6 records.

I found no additional hidden-stat disclosure through the player skill target: the source gates numeric stats at 60 and the card at 90 as P239 specifies, and pinned `Projects/Server/Targeting/Target.cs:180` checks map, range, visibility, and line of sight before the patched target runs. The existing tests exercise 0, 30, 60, and 90; hidden-target rejection was checked in source, not exercised in a running shard.

## Sources and limits

Read both work-copy `AGENTS.md` files, `docs/direction-decision.md`, `docs/tasks.md`, and `notes/cc-P239-creature-levels-appraisal.md`, and checked the relevant creature rows in its companion `notes/cc-P239-files/bard-difficulty-spread.txt`. There is no separate P239 Codex review in the tracked notes, so there were no prior P239 review findings to repeat. P239 already records randomized poison levels, provisional player strength, uncapped Bard difficulty, and detail being shown even when the skill roll fails; those deliberate behaviors are not new findings here.

Reviewed the canonical implementation and its callers, both P239 patches, their registration in `docker/uo/apply-patches.sh`, `server/customizations/ClusterFSkillGain.cs`, and all of `server/tests/Mobiles/CreatureLevelsVerification.cs`. Also read the skill-renaming implementation in `player-package/payload/app/Build-UoOverrides.ps1` and the two corresponding facts at `player-package/tests/Build-UoOverrides.Tests.ps1:920` and `:937`; I found no additional rename defect in those paths.

No lane tests were requested, added, or run. The findings follow the current source and the read-only font measurement; runtime reproduction, client appearance, a fresh build, and a save/load round trip remain unverified. No Haven connection, deployment, container operation, or branch operation was made.

Ran `tools/progress.py --dry-run` with the work-copy path overrides and its filesystem write suppressed in memory, since `build()` otherwise writes `tools/progress.json` even in dry-run mode. It completed successfully without changing progress files.

P446 DONE
