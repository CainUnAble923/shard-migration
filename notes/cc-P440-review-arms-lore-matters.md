# P440: review of P226 Arms Lore changes

Reviewed 2026-10-22. Notes only. No code or tests changed.

Read `notes/cc-P226-arms-lore-matters.md` first. No separate P226 Codex review was found beside it or elsewhere under `notes/`; the findings below do not repeat the implementation note's already recorded limitations.

## Findings

1. **bug | `server/patches/BaseArmor-arms-lore.patch:17`**: The crafted gain roll runs before pinned `Items/Armor/BaseArmor.cs:611` applies runic attributes, so an otherwise plain exceptional Valorite armor craft is evaluated at difficulty 124 instead of its finished magic difficulty of 149; at Arms Lore 180, crafting cannot gain even though inspecting that finished item can. Move the single crafted roll after runic attributes are applied, preserve its exceptional non-shield gate, and add a real runic armor crafting test above the premature window's 174 ceiling.

2. **bug | `server/customizations/ClusterFArmsLore.cs:175`**: The damage-increase exclusion also applies to nonexceptional weapons, so a normal-quality Valorite weapon whose only magic property is damage increase gets difficulty 99 instead of 124 and stops teaching at 149 instead of 174. Pass weapon quality into the magic check, count nonzero damage increase on nonexceptional weapons, and add a damage-only case alongside the existing exceptional weapon case that must stay nonmagic.

3. **risk | `server/tests/Skills/ArmsLoreMattersVerification.cs:319`**: The ownership test creates `other` but never puts gear on that player or in that player's backpack; it only rejects a ground item, so removing the equipped-item ownership restriction could leave this test green. Exercise targeting another player's worn gear and packed gear, assert both current and maximum durability stay unchanged, and retain a positive case for gear nested in the user's own backpack.

4. **risk | `server/tests/Skills/ArmsLoreMattersVerification.cs:209`**: Wear tests refill current durability after every hit, maintenance tests use large maxima, and only the armor crafting test adds an over-cap skill bonus, leaving exhausted durability, maximum 1, Self Repair stacking, and the remaining 200-skill clamps unprotected. Add deterministic cases for exhausted weapon/armor/shield wear, maintenance at 0/1 and 1/2 durability, Self Repair succeeding before wear reduction, and a +40 Arms Lore bonus that cannot improve weapon crafting, wear savings, maintenance, or repair beyond their 200-skill results.

5. **risk | `server/tests/Skills/ArmsLoreMattersVerification.cs:432`**: Smith weakening coverage repairs only katanas with a tool, so the armor call site and the promised repair-deed and clothing exclusions can regress without failing these tests. Add a tool repair of armor plus paired deed and clothing repairs at Arms Lore 0 and 200, checking that only tool repairs of weapons and armor receive the reduction.

## Checks with no finding

- No Arms Lore bonus stacking past its stated cap was found: `ClusterFArmsLore.cs:47` clamps skill to 0 through 200, and the weapon patch retains pinned's damage-increase cap of 50. The armor helper limits its extra allocation to 10 points per piece.
- No new path from valid durability values to negative current or maximum durability, or negative combat damage, was found. Maintenance only reduces a maximum above 1 and clamps restoration to that maximum; wear reduction keeps a subset of the incoming wear points, and the upstream wear branches handle exhausted items.
- No field-maintenance or tool-repair mutation of another player's gear was found. Maintenance checks backpack ancestry or a direct mobile parent at `ClusterFArmsLore.cs:105`; pinned repair checks equivalent ownership before the patched weaken calls. Inspecting someone else's gear can still train Arms Lore, but does not maintain that gear.
- `RepairWeakenChance` does not clamp its returned percentage, but a nonpositive result cannot weaken an item because the caller compares it with a random integer from 0 through 99. This is not a negative-durability finding.

## Evidence and verification limits

Reviewed canonical files:

- `server/customizations/ClusterFArmsLore.cs` and the Arms Lore row, crafted roll, and shared gain flow in `ClusterFSkillGain.cs`.
- `server/patches/ArmsLore-field-maintenance.patch`, `BaseWeapon-arms-lore.patch`, `BaseArmor-arms-lore.patch`, `BaseShield-arms-lore-wear.patch`, and `Repair-arms-lore-weaken.patch`.
- `server/tests/Skills/ArmsLoreMattersVerification.cs` and `SkillGainRowKeysVerification.cs`.
- Supporting `ClusterFCraftGain.cs`, `ClusterFMetalTiers.cs`, `ClusterFWoodTiers.cs`, `ClusterFRareSelfRepair.cs`, `BaseArmor-set-self-repair.patch`, `BaseWeapon-talisman-durability.patch`, and patch ordering in `docker/uo/apply-patches.sh`. Checked the later wood and exceptional-material patches for changes to the reviewed call sites.

Verified the read-only `D:/UO/ModernUO-pinned` checkout is at `d4531cd94b739613155225c234900de9f47d2c88`. Read its `Items/Weapons/BaseWeapon.cs`, `Items/Armor/BaseArmor.cs`, `Items/Shields/BaseShield.cs`, `Skills/ArmsLore.cs`, `Engines/Craft/Core/Repair.cs`, and relevant `Skills/SkillCheck.cs` and `Items/Skill Items/Tools/BaseRunicTool.cs` code. Weapon damage increase is a real random magic property in `BaseRunicTool.cs:398`; the ownership ancestry implementation is in `Projects/Server/Items/Item.cs:4193`.

The two bug findings follow from source and patch placement. Runtime reproduction, a fresh build, and client behavior are unverified in P440; no tests were added or run, as this task requests review notes only and specifies no lane tests. The P226 build results remain that task's historical evidence, not a fresh result from this review.

Ran `tools/progress.py --dry-run` successfully with both work-copy paths set. The reporter still rewrites `tools/progress.json` in dry-run mode; restored that generated change to its initially clean state to preserve this task's notes-only scope. No Haven connection, deployment, commit, merge, push, or branch switch was made.

P440 DONE
