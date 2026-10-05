# cc-P54 B - Combat group: can each skill still gain to 200?

Skills: Swords, Macing, Fencing, Archery, Throwing, Wrestling, Tactics, Anatomy, Parry, Bushido, Focus, Arms Lore (12).
Engine: pinned ModernUO d4531cd94b739613155225c234900de9f47d2c88 (verified with `git rev-parse HEAD`). Pinned paths are
relative to `D:\UO\ModernUO-pinned\Projects`. C\ = `D:\ShatteredLegacy\server\customizations`, P\ = `...\server\patches`.
Expansion is AOS/ML on, so pre-AOS branches are dead and ignored (BaseShield.OnHit pre-AOS Parry check
`UOContent/Items/Shields/BaseShield.cs:63` sits after the AOS branch at :33 that returns 0, dead).

## How I searched

- Every `Check*Skill*` method name in pinned (grep -o): CheckSkill 73, CheckTargetSkill 34, CheckSkills 14,
  CheckBonusSkill 4, CheckWeaponSkill 2, CheckTeachSkills 2, plus one test name. Every call site was read; the ones
  that name a combat skill, or pass a computed skill that can be one of ours, are in the table. CheckSkills /
  CheckWeaponSkill (WeaponAbility.cs:224, :294; SpecialMove.cs:63) only test requirements and never roll a gain.
  CheckTeachSkills is NPC teaching (sets Base directly, not a gain roll, and capped by the NPC's own skill).
- C\ and P\: grep for `CheckSkill`, `CheckTargetSkill`, `CheckBonusSkill`, `ModifyHitChance`, `CheckHit`,
  `GetDefendSkillValue`, the four SkillCheck handlers. The only combat-skill gain call in our code is the Focus call in
  our replacement `C\RegenRates.cs` (identical to pinned except the Meditation armor branch, diffed). `C\ClusterFSkillGain.cs`
  wraps the four handlers (:37-45) and passes min/max/chance through unchanged (:62-96), boost only while
  `skill.Base < skill.Cap` (:128-134). `P\BaseWeapon-talisman-durability.patch` adds a talisman OnHit hook only (hunk at
  :1649), no skill read.
- Gain gates (pinned SkillCheck.cs, re-verified): value < min -> no gain (:59-62); value >= max -> "No challenge", no
  roll (:64-67 and :184-189); direct chance >= 1.0 -> no roll (:97-100 and :215-220); Gain needs `skill.Base <
  skill.Cap` (:248). All the "value" tests use `Skill.Value`, which includes item bonuses. Since cc-P53 Part C
  (C\ClusterFSkillBonusAboveCap.cs, P\PlayerMobile-skill-bonus-above-cap.patch) item "+Skill" bonuses sit above the
  cap, so every "follows Cap" use below stalls at Base = 200 minus the player's worn bonus in that skill. Pinned had the
  same stall (ObeyCap clamped Value at Cap, so Value hit Cap at the same Base). Taking the jewelry off removes it.

## Shared formula: weapon hit chance (Swords, Macing, Fencing, Archery, Throwing, Wrestling)

`UOContent/Items/Weapons/BaseWeapon.cs:1208-1340`. Gain goes to the weapon's own skill (`atkSkill`, :1213), the value is
`GetUsedSkill` (:1152, UseBestSkill / MageWeapon). AOS:
ourValue = (a + 20)(100 + HCI), HCI capped 45 (:1267); theirValue = (d + 20)(100 + DCI), DCI capped 45 (:1316);
chance = ourValue / (2 theirValue) (:1331); `ModifyHitChance` hook (:1333); floor 0.02 (:1335); `CheckSkill(skill,
chance)` direct (:1340). Gain rolls while chance < 1, i.e. a < 2(d+20)(100+DCI)/(100+HCI) - 20.
- No HCI, no DCI: a < 2d + 20. To roll at a = 199.9 the defender needs d > 89.95.
- 45 HCI: a < 1.379(d + 20) - 20. To roll at 199.9 the defender needs d > 139.4.
- d for a creature with Fists = max(Wrestling, min((Anat + Eval + 20)/2, 120)) (`Fists.cs:45-58`); a creature with a
  weapon uses that weapon's skill, or Wrestling if higher and not human (:1188-1195).
- Strongest existing defenders (counted by grep of `SetSkill(SkillName.Wrestling, ...)`, max of range): pinned Rend
  136.3-150.3 (`Mobiles/Monsters/ML/Labyrinth/Rend.cs:34`), GreaterDragon 115-145, Abscess 132.3-143.8, RedDeath
  121.4-143.7, Coil 124.5-141.3, Swoop 120-140; ours Allosaurus 120-150 (`C\Mobiles\Normal\Allosaurus.cs:34`), Shame
  Revamped creatures 120-140 (`C\Services\Revamped Dungeons\Shame Revamped\Mobiles\Creatures.cs:911, :1117, :1257,
  :1360`). Max pinned creature Swords 150, Macing 125, Fencing 120, Archery 120. Many common creatures sit at 90-100
  (dragons, balrons). Paragons (Ilshenar only, `Mobiles/Special/Paragon.cs:11-14`) multiply Base by 1.2 (:76); I did not
  enumerate every Ilshenar paragon candidate (unverified whether any exceeds Rend). A 200-skill player sparring partner
  gives d = 200 (ceiling 420).
- So the ceiling vs the strongest creature (Rend 150.3, no HCI) is 320.6; with 45 HCI it is 214.9.
- Throwing only (`UOContent/Items/Weapons/Throwing/BaseThrown.cs:56-89`, new since P20's commit): -12% under min range,
  up to -12% in melee (mitigated by Throwing + RawDex), and with a shield `chance *= 1 - min(90, 1200/Parry)/100`. These
  only lower the chance, so they raise the ceiling; a thrower with a shield and low Parry has chance near 0.1x and
  rolls gains against anything (degenerate, but real).
- Dummies and buttes: `TrainingDummies.cs:67` and `ArcheryButteAddon.cs:185` use weapon skill with min/max -25/+25
  (defaults :23-24 and :18-19), ceiling 25 unless a GM edits them.

## (i) Per-skill table

| Skill | Gain calls (file:line, pinned/ours, min/max or chance) | Ceiling now | P20 ceiling (confirmed/corrected) | Reaches 200? |
|---|---|---|---|---|
| Swords | BaseWeapon.cs:1340 pinned, direct chance (formula above); TrainingDummies.cs:67 pinned, -25/25 | 2d+20 per target; 320.6 vs Rend (no HCI); 214.9 vs Rend with 45 HCI; 25 on dummy | ~220 vs 100-skill target: CONFIRMED as stated; refined: max over existing targets is ~320 | YES: hit attempts vs any defender with d > 90 (no HCI) or d > 139.4 (45 HCI) |
| Macing | same two calls | same | same, confirmed | YES, same condition |
| Fencing | same two calls | same | same, confirmed | YES, same condition |
| Archery | BaseWeapon.cs:1340 via BaseRanged.cs:78, direct chance; ArcheryButteAddon.cs:185 pinned, -25/25 | same as Swords; 25 on butte | confirmed | YES, same condition |
| Throwing | BaseWeapon.cs:1340 via BaseRanged.cs:78 with BaseThrown.cs:56-89 penalties | at least the Swords ceiling; unbounded in practice with shield + low Parry | CORRECTED upward (penalties did not exist at 7c9215d97 in this form) | YES, same condition (easier) |
| Wrestling | BaseWeapon.cs:1340 (Fists, Skill = Wrestling); TrainingDummies.cs:67 | same as Swords | confirmed | YES, same condition |
| Tactics | BaseWeapon.cs:2524 pinned, CheckSkill(Tactics, 0, Tactics.Cap) on every AOS damage roll (ComputeDamageAOS :2589-2590, called :2683) | Cap (200), less worn +Tactics | "none, follows cap": CONFIRMED | YES: any weapon hit, with no +Tactics worn |
| Anatomy | BaseWeapon.cs:2527 pinned, 0..Anatomy.Cap; Bandage.cs:444 pinned, 0-120 (secondary skill on a human patient, :185-193); Anatomy.cs:97 pinned, target 0-100; BaseCreature.cs:5774, :5806 creature self-heal (NPC only, n/a) | Cap (200) via combat; 120 bandage; 100 active | CONFIRMED | YES: any weapon hit, with no +Anatomy worn |
| Parry | BaseWeapon.cs:1528 pinned, shield: chance = max((P - Bushido nonracial)/400, 0) + 0.05 (P or B >= 100), x Evasion scalar, x (20+Dex)/100 if Dex < 80; BaseWeapon.cs:1569 pinned, no shield, P*B/48000 (1H) or /41140 (2H) + 0.05, gains only if above P/800 + 0.05 (:1542, :1567-1573); called from :1582 on every incoming weapon hit and Evasion.cs:106 | shield: 380 + Bushido nonracial (lower under Evasion); weapon path: P*B < 45600 (1H) / 39083 (2H) | 380: CONFIRMED | YES: blocking with a shield (chance 0.55 at Parry 200, Bushido 0, Dex >= 80) |
| Bushido | MomentumStrike.cs:67 pinned, CheckSkill(Bushido, 70, 120) (runs only when a second target is hit, :62); SamuraiMove.cs:9 pinned, [req-12.5, req+37.5]: HonorableExecution (req 25) 12.5-62.5, LightningStrike (50) 37.5-87.5; SamuraiSpell.cs (GetCastSkills) via Spell.cs:628, same window: Confidence 25 -> 62.5, CounterAttack 40 -> 77.5, Evasion 60 -> 97.5. Spell.cs:625 DamageSkill path skipped (DamageSkill == CastSkill, SamuraiSpell.cs:17-18) | 120 | 120: CONFIRMED | NO: STALLED at 120 |
| Focus | C\RegenRates.cs:41 OURS (replaces pinned Misc/RegenRates.cs), CheckBonusSkill chance n = cur/max x (1 - v) + v, v = sqrt(Focus x 0.005) (:35-39); stam :95, mana :152; called each regen timer tick (Server/Mobiles/Mobile.cs:9018, :9052) | v < 1 iff Value < 200, and n < 1 only while stam or mana is below max: rolls at 199.9, so Base can reach 200.0 | 200: CONFIRMED (equals the new cap exactly) | YES, just: stam or mana not full, no +Focus worn |
| Arms Lore | BaseWeapon.cs:684 pinned, 0-100 (ML exceptional craft); BaseArmor.cs:605 pinned, 0-100 (exceptional craft); ArmsLore.cs:33, :89, :107 pinned, target 0-100 | 100 | 100: CONFIRMED | NO: STALLED at 100. F-26 designs this |

Count: 10 reach 200 already, 2 stalled (Bushido 120, Arms Lore 100). Of the stalled, only Bushido needs a proposal
here; Arms Lore belongs to F-26.

Not counted here: BaseWeapon.cs:2532 Lumberjacking 0-100 on axe hits (another group's skill), NinjaWeapons.cs:274 (gains
Ninjitsu, not a weapon skill).

## (ii) Proposal for the stalled skill

### Bushido (stalled at 120) - option (a)

Change: in `MomentumStrike.CheckGain` keep pinned's `CheckSkill(Bushido, 70, 120)` while Bushido Value < 120, and use
`CheckSkill(Bushido, 70, Skills.Bushido.Cap)` from 120 up. Momentum Strike's gain is a fixed skill window, not a target
difficulty, and it already rolls on every successful second-target transfer (MomentumStrike.cs:13-62; no gain when no second target, :33), so the window
means the same at 170 as at 110; this is the Meditation pattern. At Cap 200 the chance at 120 is (120-70)/130 = 0.38,
at 180 it is 0.85, so gains slow down toward 200 as they do for Meditation. Under a lower loop cap (F-12 50/100/105...)
the same line follows that cap; at caps up to 120 it is identical to pinned.

Why not cheaper or other options: (a) is the cheapest. (b) does not apply: no Bushido gain depends on a target or
material, every window is fixed by RequiredSkill. (c) is not needed.

Files: `P\MomentumStrike-bushido-gain-above-120.patch` (NEW patch on pinned `UOContent/Spells/Bushido/MomentumStrike.cs`,
one hunk at :65-68) and one `apply_patch` line in `D:\ShatteredLegacy\docker\uo\apply-patches.sh` (ours, the list near
:255-270). A full replacement is not needed. A customization-only route (re-registering a subclass in SpellRegistry) is
possible but larger and riskier than a 3-line patch.

Fidelity: below 120 nothing changes (pinned window kept). OSI's Bushido cap is 120, so every gain above it is ours.
A player on OSI would notice nothing below 100 or 120. One visible seam: just under 120 the pinned chance is near 1
(slow gain), at 120 it drops to 0.38 (faster gain). Acceptable, but say so in the deviation entry.

Exploit check, rank-4 list (Hiding 118, Stealing 150, bard 150, guards 121, Tinkering traps 120, D42 salvage): none
relevant, Bushido feeds none of them.

New breaks opened between 120 and 200 (all these effects already scale with Bushido; today they top out at 120):
1. Parry + Bushido 100% block. No shield, two-handed weapon: P*B/41140 + 0.05 >= 1 at P*B >= 39083, so Parry 200 with
   Bushido >= 195.4 blocks every weapon hit (BaseWeapon.cs:1540, :1567-1569). One-handed needs P*B >= 45600, not
   reachable at 200/200 (0.883). With Evasion up (GetParryScalar, Evasion.cs:175-204, 1H, Parry 200, Anat and Tactics
   >= 100): 100% from Bushido about 140 (0.633 x 1.58 = 1.00); without the Anat/Tac bonus about 147. While Evasion is up,
   a 100% block also evades every single-target spell and fire breath (Evasion.cs:106). Evasion lasts
   (int)(3 + (B-60)/20) + 1 s, 8 s at 140 and 11 s at 200 (cooldown 20 s), so this is a timed window, not permanent.
   This is the P20 Parry+Bushido break moving from "300" to "about 140 with Evasion, 195 with a two-hander".
2. Nerve Strike paralyze chance (150/7 + 4B/7)% reaches 100% at Bushido 137.5 (`Items/Weapons/Abilities/NerveStrike.cs:66`);
   the ParalyzingBlow immunity window (:70) still limits it to once per immunity cycle.
3. Feint (`Weapons/Abilities/Feint.cs`, per P20): (int)(20 + 3(B-50)/7)% = 84% damage reduction at 200 (50% at 120).
   Not a break (P20's 100% point is 236.7), but large in PvP.
4. Magnitudes that grow but stay inside caps at 200: Momentum Strike damage bonus Bushido/100 (2.0x at 200, x1.5 on a
   kill, MomentumStrike.cs:46-51); Honorable Execution heal 20 + B^2/480 = 103; Confidence regen (15 + B^2/576)/4 = 21 per
   tick; Lightning Strike armor ignore B^2/72000 = 56%; HE swing bonus B^2/720 = 55.6 (SSI cap 60).
Recommendation to the overseer: ship the gain fix together with, or after, a cap on final block chance (P20's
recommendation), or at least clamp the no-shield P*B product at min(P,120) x min(B,120) and the Nerve Strike chance at
OSI's 90%. Without that, opening Bushido to 200 turns item 1 into a reachable 100% block.

### Arms Lore (stalled at 100)

Calls and ceiling are in the table (all five are 0-100). F-26 designs this (feature-queue.md:2030, item 6 "gain path to
200" already approved 2026-10-02). Note for F-26: cc-P20's lines moved (BaseWeapon.cs:711 -> :684, BaseArmor.cs:631 ->
:605); ArmsLore.cs :33/:89/:107 did not.

## (iii) Moved lines vs cc-P20 (7c9215d97 -> d4531cd94)

| P20 citation | Now | What |
|---|---|---|
| BaseWeapon.cs:1178-1229 | :1152-1200 | GetUsedSkill |
| BaseWeapon.cs:1294 | :1267 | HCI cap 45 |
| BaseWeapon.cs:1343 | :1316 | DCI cap 45 |
| BaseWeapon.cs:1358-1362 | :1331 (chance), :1335-1338 (floor) | hit chance |
| BaseWeapon.cs:1365 | :1340 | weapon-skill CheckSkill (new ModifyHitChance hook at :1333, :1348) |
| BaseWeapon.cs:1520 | :1508 | shield block formula |
| BaseWeapon.cs:1540 | :1528 | Parry CheckSkill, shield |
| BaseWeapon.cs:1550-1585 / :1552 / :1554 | :1534-1573 / :1540 / :1542 | no-shield block |
| BaseWeapon.cs:1581 | :1569 | Parry CheckSkill, no shield |
| BaseWeapon.cs:1585 | :1573 | aosChance roll (no gain) |
| BaseWeapon.cs:2540 | :2524 | Tactics CheckSkill (AOS) |
| BaseWeapon.cs:2543 | :2527 | Anatomy CheckSkill (AOS) |
| BaseWeapon.cs:2548 | :2532 | Lumberjacking CheckSkill (axes) |
| BaseWeapon.cs:698-712 / :711 | :670-684 / :684 | Arms Lore, exceptional weapon |
| BaseArmor.cs:631 | :605 | Arms Lore, exceptional armor |
| Fists.cs:44-58 | :45-58 | defend value |
| BaseThrown.cs:38 (DefSkill) | :49 | also new: AccuracySkill => Throwing at :50, so P20's "accuracy mods buff Archery" bug is fixed upstream; ModifyHitChance :56-89 is new |

Unchanged (verified): MomentumStrike.cs:65-67; SamuraiMove.cs:9; Spell.cs:625, :628 (P20 did not cite); Anatomy.cs:97;
ArmsLore.cs:33, :89, :107; Bandage.cs:444; Evasion.cs:106 and :175-204; C\RegenRates.cs:28-41, :95, :152.
SkillCheck.cs :62, :67, :100, :189, :220, :248 as stated in the brief: confirmed. Brief correction: our Meditation gain
call is `C\Meditation.cs:115`, not about :92.

## (iv) Batch sizing

Builder batch for the combat group: **S**.
- `P\MomentumStrike-bushido-gain-above-120.patch` (new patch on pinned MomentumStrike.cs :65-68).
- `D:\ShatteredLegacy\docker\uo\apply-patches.sh` (ours): one `apply_patch` line.
- A test file under `D:\ShatteredLegacy\server\tests\...` (ours), e.g. `tests\Misc\` next to the cc-P53 facts.
- Deviation register entry (gain above OSI's 120).
- If the overseer takes the recommendation in (ii), the block-chance cap is a separate M item touching pinned
  BaseWeapon.cs CheckParry (:1491-1574); BaseWeapon.cs already carries P\BaseWeapon-talisman-durability.patch (hunk at
  :1649, no overlap, but the two patches must apply in order).

Facts a builder would write (spy on `Mobile.SkillCheckLocationHandler` to capture min/max, as cc-P53's tests read caps):
1. Bushido Value 119.9: a Momentum Strike second-target hit calls CheckSkill(Bushido, 70, 120) exactly as pinned.
2. Bushido Value 150, cap 200: the call is (70, 200), and with forced rolls Base rises.
3. Bushido Base 200 = Cap: no gain.
4. Cap set to 120: every value behaves as pinned (no difference anywhere).
Regression facts that lock in the "already reaches 200" verdicts (no code change, cheap to add):
5. Tactics and Anatomy at 199.9, cap 200, no items: a weapon hit rolls a gain (min 0, max Cap).
6. Same with a +5 Tactics item worn: no roll at Base 195 (documents the D-113 stall).
7. Parry 199.9 with a shield, Dex 100, Bushido 0: CheckParry passes chance 0.5498 (< 1).
8. Focus 199.9, stamina below max: CheckBonusSkill passes chance < 1; at full stamina chance = 1 (no roll).
9. Swords 199.9 vs a defender with Wrestling 100, no HCI/DCI: chance 0.916 (< 1); vs Wrestling 89.9: chance >= 1.

File overlap: none of these files is touched by cc-P53 (its list: ClusterFSkillCaps, ClusterFMiningExtension, smith
commissions/BOD/salvage, LargeSmithBOD, SmallSmithBOD patch, Meditation, RegenRates :161, TestCenterKit). RegenRates is
shared with cc-P53, but this batch does not touch it. F-26 will touch BaseWeapon.cs (:670-684) and BaseArmor.cs (:595-605)
and ArmsLore.cs; this batch does not.

## Notes and surprises

- cc-P53's note says "by the F-12 counts only the six weapon skills, Focus, Parry and Mining can gain past about 160";
  Tactics and Anatomy also gain to the cap (pinned uses 0..Cap), so that list is short by two.
- Focus reaches 200 only because its no-gain point (v = 1) is exactly 200; any cap above 200 would stall it at 200.
- Weapon skills reach 200 only without heavy HCI or against strong targets: with 45 HCI only about a dozen creature
  types (d > 139.4) still train past ~200.
- Every follow-the-cap use stalls at 200 minus worn +skill (Value, not Base, is tested).
- Unverified: the full list of Ilshenar paragon candidates and their buffed skills.
