# S2 - Combat skills audit (cc-P20)

Skills: Swords, Macing, Fencing, Archery, Throwing, Wrestling, Tactics, Anatomy, Parry, Bushido, Focus, Arms Lore (+ Lumberjacking combat bonus, mentioned).
Paths: pinned = relative to D:\UO\ModernUO-pinned\Projects. Shard = D:\ShatteredLegacy\server\...
Expansion: AOS/SE/ML/SA/HS/TOL all on, so AOS/ML branches only. Pre-AOS branches (Fists stun/disarm, BaseAxe/BaseBashing/BaseSpear/BasePoleArm anatomy procs, BaseShield.OnHit pre-AOS, ScaleDamageOld, MageAI/ThiefAI wrestle moves) are dead code here and are ignored.

## Shard overrides relevant to this group

- customizations\RegenRates.cs REPLACES UOContent/Misc/RegenRates.cs. Diff vs pinned: only the Meditation armor branch (customizations\RegenRates.cs:158-164). Focus code (stam :95-97, mana :152-154, CheckBonusSkill :28-41) is byte-identical to pinned UOContent/Misc/RegenRates.cs:95-97, :152-154.
- customizations\CraftItem.cs REPLACES pinned; it still calls craftable.OnCraft(..., from, ...) (customizations\CraftItem.cs:1194), so Arms Lore exceptional bonuses in BaseWeapon/BaseArmor.OnCraft still apply.
- customizations\ClusterFSkillGain.cs wraps the four SkillCheck handlers (:37-45) with extra attempts/multiplier but passes min/max/chance through unchanged, so every gain ceiling below still holds.
- customizations\ClusterFSkillCaps.cs sets per-skill cap (default 300, :10). Tactics/Anatomy combat gain uses Skills.X.Cap so they follow it.
- patches\BaseWeapon-talisman-durability.patch, patches\AOS-*.patch, patches\Mobile-set-item-resistance-hook.patch: no skill reads. Not relevant to scaling.
- Shard gargoyle weapons (customizations\Items\Equipment\Weapons\Gargish*.cs, Shortblade.cs) use DefSkill Swords/Fencing, not Throwing. GargishBattleAxe.cs:151-153 anatomy proc is the !Core.AOS copy (dead).
- customizations\PetMimicWeapon.cs:113-119 sets DefSkill by mimic category; it reads the wielder's skill only through the generic weapon path.
- No shard file reads Parry, Bushido, Focus, Tactics, Anatomy or Arms Lore values for gameplay other than CharacterCreation (start skills), ClusterFGuildSystem.cs:181/201/231/262 (guild join thresholds 30-50, clamps) and ClusterFGuildStarterPath.cs:46-56 (lists).

## Shared formulas used below

Hit chance (AOS), pinned UOContent/Items/Weapons/BaseWeapon.cs:1233-1365:
  ourValue = (atk + 20) * (100 + HCI), HCI capped 45 (:1294)
  theirValue = (def + 20) * (100 + DCI), DCI capped 45 (:1343)
  chance = ourValue / (2 * theirValue), floor 0.02 (:1358-1362); CheckSkill(weapon skill, chance) (:1365)
  atk = Skills[GetUsedSkill].Value (:1178-1229); def = defender weapon skill (Fists: max(Wrestling, min((Anat+Eval+20)/2, 120)), Fists.cs:44-58).
  Gain ceiling: chance >= 1.0 at atk = 2*(def+20)*(100+DCI)/(100+HCI) - 20. Versus a 100-skill monster with no mods: 220. Versus 120: 260. With 45 HCI vs 100: 145.5.

Weapon damage (AOS), BaseWeapon.cs:2533-2603, GetBonus :2501-2511 (value*scalar, +offset at >=100):
  Str: 0.30*Str + 5 ; Anatomy: 0.50*v + 5 ; Tactics: 0.625*v + 6.25 ; Lumberjacking (axes only): 0.20*v + 10   (percent)
  "These are the bonuses given by the physical characteristics of the mobile. No caps apply." (comment :2552-2555)
  Only the item/spell part (WeaponDamage etc.) is capped at 100 (:2594-2597). The later percentageBonus cap of 300 (:1874) covers specials/moves/slayers, NOT tactics/anatomy.

Special-move mana, pinned UOContent/Items/Weapons/Abilities/WeaponAbility.cs:177-218:
  skillTotal = Swords+Macing+Fencing+Archery+Parry+Lumberjacking+Stealth+Poisoning+Bushido+Ninjitsu (:182-191). >=300 -> -10 mana, >=200 -> -5. Lowest BaseMana is 15 (InfusedStrike/MovingShot/WhirlwindAttack), so it never goes negative. Clamps at total 300 (one skill at 300 alone qualifies). Throwing is NOT in the list.
  Required weapon skill: Base >= 70 primary / 90 secondary (:122-138); Tactics Base >= 70/90 (:160-176, :235); secondary Bushido/Ninjitsu >= 50 (:145). All clamp.

Swing speed: no skill reads. SE/ML GetDelay (BaseWeapon.cs:1366-1460) reads Stam, SSI (capped 60 at :1419), HonorableExecution swing bonus (Bushido, folded into the 60 cap). Focus only matters indirectly via stamina.

---

## Swords / Macing / Fencing / Archery / Throwing / Wrestling (weapon skills)

All six are read through the same generic path; only differences are noted.

| Use | file:line | formula (short) | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Attack hit chance vs 100-skill monster (no HCI/DCI) | BaseWeapon.cs:1299,1358 | (a+20)/(2*120) | scales: 58% | clamps: 133% -> always hits (100% reached at 220) | clamps (217%) | clamps (425%) | 220 vs 100-skill target, 260 vs 120, 145.5 with 45 HCI. To keep training at 300+ you need defenders with ~140+ skill; 1000 needs ~490-skill defenders |
| Defense: 100-skill monster hitting you (its chance) | BaseWeapon.cs:1348,1358 | 120/(2*(D+20)), /1.45 with 45 DCI, floor 2% | 43% (30% w/ DCI) | 19% (13%) | 11.5% (8.0%) | breaks: 5.9% (4.1%); near-immunity vs all normal monsters | (defense never gains) |
| PvP, equal skills | same | (a+20)/(2*(a+20)) | 50% | 50% | 50% | 50% | n/a - scales neutrally. Mismatch: 1000 vs 300 = 159% -> always hits; 300 vs 1000 = 15.7% |
| GetUsedSkill / UseBestSkill picks highest of Swords/Fencing/Macing | BaseWeapon.cs:1178-1229 | max | scales | scales | scales | scales | - |
| Weapon ability weapon-skill requirement | WeaponAbility.cs:122-138, 260-275 | Base >= 70/90 | clamps at 90 | clamps | clamps | clamps | - |
| Special-move mana discount (not Throwing, not Wrestling) | WeaponAbility.cs:182-200 | total>=300 -> -10 | -5 if total>=200 | clamps at 300 | clamps | clamps | - |
| Evasion cast / spell-evasion weapon gate | Spells/Bushido/Evasion.cs:56, :95 | Base >= 50 | clamps | clamps | clamps | clamps | - |
| Archery: Serpent Arrow poison level | Abilities/SerpentArrow.cs:25-31 | Archery+Poisoning > 199.8 -> Deadly (3) | scales | clamps at sum 199.8 | clamps | clamps | - |
| Throwing: DefSkill on BaseThrown (Boomerang, Cyclone, SoulGlaive) | Weapons/Throwing/BaseThrown.cs:38 | generic hit chance only | as above | as above | as above | as above | same as above |
| Wrestling: Fists defend value | Weapons/Fists.cs:44-58 | max(Wres, min((Anat+Eval+20)/2,120)) | scales | Anat/Eval part clamps at 120 | clamps (that part) | clamps | - |
| Wrestling: AOS Disarm / Paralyzing Blow on fists | Fists.cs:19-20; Abilities/Disarm.cs:18; ParalyzingBlow.cs:22 | Wrestling Base >= 70/90, no tactics needed | clamps | clamps | clamps | clamps | - |

Minor/cosmetic: tooltip "skill required" switch has no Throwing case (BaseWeapon.cs:3306-3328); BaseHire.cs:133-142 hireling pay (NPC only); AOS.cs:1095-1104 skill-name strings; BaseThrown inherits AccuracySkill => Archery from BaseRanged.cs:41, so old-style accuracy-level skill mods on a thrown weapon buff Archery not Throwing (minor bug, only legacy accuracy items).
Gaps (not breaks): Throwing is missing from the special-move mana skill total (WeaponAbility.cs:182-191) so a pure thrower never gets the -5/-10 mana discount that a pure archer gets. Wrestling is also missing.

Recommendation: soft-cap the hit-chance input past 120 (for example effective = 120 + 40*ln(1 + (v-120)/100)) or cap final hit chance at about 95% and floor defender-side at about 10% per attacker tier; otherwise defense past 500 makes normal monsters near-harmless. Re-think gain: weapon skills effectively stop gaining at 220-260 against normal content, so use a separate gain rule above 120 (e.g. gain on hit with a fixed small chance) or give gains vs high-tier creatures.

## Tactics

| Use | file:line | formula (short) | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| AOS damage bonus | BaseWeapon.cs:2558, total :2599-2602 | 0.625*v + 6.25 % (uncapped) | scales: +81.3% | scales: +193.8% | breaks: +318.8% | breaks: +631.3% | none: CheckSkill(Tactics, 0, Skills.Tactics.Cap) BaseWeapon.cs:2540 - follows the cap (300 now, 1000 later) |
| Weapon-ability tactics requirement | WeaponAbility.cs:235 | Base >= 70/90 | clamps | clamps | clamps | clamps | - |
| Evasion bonus gate (with Anatomy, Bushido>100) | Evasion.cs:167, :199 | >= 100 | clamps | clamps | clamps | clamps | - |

Combined example (Tactics = Anatomy = v, Str 125, 100% DI, non-axe): multiplier 3.89x at 120, 5.91x at 300, 8.16x at 500, 14.79x at 1000 (1.5x / 2.1x / 3.8x the 120 baseline). A weapon averaging 12 base damage: 47 / 71 / 98 / 178 per hit before resists; vs 70 physical resist: 14 / 21 / 29 / 53. Nothing caps this: the 100% DI cap and the 300% percentageBonus cap do not include it.
Recommendation: soft-cap with diminishing returns: keep 0.625*v up to 120, then add e.g. 25 * ln(1 + (v-120)/50) percent, or move tactics past 120 into a separate pool that counts toward the 100% DI cap.
Minor: BaseCreature.cs:2420 FightMode.Strongest target selection; AnimalLore gump display.

## Anatomy

| Use | file:line | formula (short) | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| AOS damage bonus | BaseWeapon.cs:2557 | 0.5*v + 5 % (uncapped) | scales: +65% | scales: +155% | breaks: +255% (see Tactics combined) | breaks: +505% | none: CheckSkill(Anatomy, 0, Cap) BaseWeapon.cs:2543 |
| Bandage heal (AOS, secondary skill) | Items/Skill Items/Misc/Bandage.cs:387-388 | min += v/8, max += v/6 | scales: 15-20 | scales: 37.5-50 | scales: 62.5-83 | scales: 125-167 (anatomy part only; Healing part covered by Healing audit) | Bandage.cs:444 CheckSkill(Anatomy, 0, 120) -> 120 |
| Bandage cure/res gates | Bandage.cs:240, :322 | >= 80 / >= 60 | clamps | clamps | clamps | clamps | - |
| Anatomy active use | Skills/Anatomy.cs:59, :97, :106 | margin = max(0, 25 - v/4); target check 0-100 | clamps at 100 | clamps | clamps | clamps | 100 |
| Fists defend value | Fists.cs:54-56 | min((Anat+Eval+20)/2,120) | clamps at Anat+Eval = 220 | clamps | clamps | clamps | - |
| Evasion bonus gate | Evasion.cs:167, :199 | >= 100 | clamps | clamps | clamps | clamps | - |
| BaseCreature self-heal (NPC only) | Mobiles/BaseCreature.cs:5367-5409 | v/10..v/8 | n/a players | | | | 100 |

Overall Anatomy gain ceiling: none (combat path uses Cap).
Recommendation: soft-cap the damage term like Tactics; let the bandage term scale (or give it a separate soft cap together with Healing).

## Lumberjacking (combat part only, mentioned)

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Axe damage bonus | BaseWeapon.cs:2559-2561 | 0.2*v + 10 % | scales: +34% | scales: +70% | scales: +110% | breaks-ish: +210% on top of Tactics/Anatomy | combat gain CheckSkill(Lumberjacking, 0, 100) BaseWeapon.cs:2548 -> 100 (harvest gain is the gathering auditor's; shard ClusterFLumberjackingExtension reads Lumberjacking to 300) |
| Special-move mana total | WeaponAbility.cs:188 | counts | clamps at total 300 | | | | |

Recommendation: same soft-cap shape as Tactics.

## Parry

| Use | file:line | formula (short) | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Block chance WITH shield (Bushido 0, Dex >= 80, no Evasion) | BaseWeapon.cs:1520-1540 | max((Parry - BushidoNonRacial)/400, 0) + 0.05 if Parry or Bushido >= 100 | scales: 35% | scales: 80% | breaks: 130% -> every weapon hit (melee AND ranged) blocked, damage set to 0 (:1599-1603) | breaks: 255% -> immune | direct chance: reaches 1.0 at Parry 380 (+BushidoNonRacial). Note Bushido SUBTRACTS here: Parry 300/Bushido 300 with shield = 5% |
| Block chance, 1H weapon no shield, Bushido = Parry | BaseWeapon.cs:1550-1585 | P*B/48000 (2H /41140) +0.05; Evasion scalar; Dex<80 penalty | scales: 35% (40% 2H) | breaks (live today): 1.875+0.05 -> 100% block | breaks | breaks | gain only if bushido-chance > aosChance; stops at P*B >= 45600 (1H) / 39083 (2H), e.g. 213.5/213.5 |
| Block chance, weapon, Parry only (Bushido 0) | BaseWeapon.cs:1554-1585 | Parry/800 + 0.05 | 20% | 42.5% | 67.5% | breaks: 130% -> immune (100% at Parry 760) | NO gain on this path (Utility roll, not CheckSkill :1585) |
| Evasion spell dodge (uses CheckParry) | Spells/Bushido/Evasion.cs:80-110; Spell.cs:320; FireBreath.cs:147 | while evading, CheckParry also blocks single-target spells and fire breath | scales | breaks when block chance >= 100%: immune to single-target spells while Evasion is up | breaks | breaks | - |
| Shield ArmorRating | Items/Shields/BaseShield.cs:24 | Parry*AR/200 + 1 | heater (23): 14.8 | 35.5 | 58.5 | 116 | - |
| Shield wear per block vs Bashing (AOS) | BaseShield.cs:30-45, 78-112 | rand(AR/2..AR)/2 durability | 3-7 | 8-17 | breaks (self-harm): 14-29 | breaks: 29-58 per block; heater has 50-65 HP so it hits 0 HP in about 2 mace blocks, then MaxHitPoints is eaten and the shield is deleted (:100-110) | - |
| Special-move mana total | WeaponAbility.cs:187 | counts | clamps at 300 | | | | |
| Counter Attack / Confidence triggers | BaseWeapon.cs:1593-1625 | fire on every successful block | see Bushido | | | | |

Recommendation: hard-cap final block chance (e.g. 50-60% shield, 40% weapon) and put a soft-capped curve on Parry past 120 (e.g. +0.05 per 100 points); decouple shield ArmorRating from Parry (use min(Parry,120)) so high Parry does not shred shields; fix the shield path subtracting Bushido.

## Bushido

| Use | file:line | formula (short) | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| No-shield parry multiplier | BaseWeapon.cs:1552 | P*B/48000 | see Parry | breaks (with Parry 300) | breaks | breaks | - |
| Shield parry penalty | BaseWeapon.cs:1520 | (P - B_nonracial)/400 | reduces shield block | at B=P shield block = 5% | same | same | - (bad interaction, not abusable) |
| Evasion duration (s) | Evasion.cs:159-172 | (int)(3 + (B-60)/20) +1 w/ Anat&Tac>=100 | 6 (7) | 15 (16) | 25 (26) | 50 (51) | Evasion gain req+-: 47.5-97.5 |
| Evasion uptime vs 20 s cooldown | Evasion.cs:135-136 | duration >= 20 s at B >= 400 (380 with bonus) | scales | scales | breaks: permanent Evasion | breaks: permanent | - |
| Evasion parry scalar | Evasion.cs:175-204 | 1 + 0.16 + (B-60)*0.004 (+0.10) | 1.40 (1.50) | 2.12 (2.22) | 2.92 (3.02) | 4.92 (5.02) | - |
| Confidence regen (4 ticks, stops on damage) | Spells/Bushido/Confidence.cs:131-133, PlayerMobile.cs:2377 | per tick (15 + B^2/576)/4 | scales: 10/s, 40 total | scales: 42/s, 168 total | breaks: 112/s, 448 total, 10 mana | breaks: 437/s, 1748 total (full heal in 1 tick) | Confidence req 25 -> 62.5 |
| Confidence heal on block | BaseWeapon.cs:1615-1624 | Hits += 1..B/12, Stam += 1..B/5 | 1-10 hp, 1-24 stam | 1-25 hp, 1-60 stam | 1-41, 1-100 | breaks: 1-83 hp per block, with 100% block every enemy swing heals | - |
| Counter Attack | Spells/Bushido/CounterAttack.cs | free swing on block; no skill scaling | clamps | clamps (but fires on every block once block = 100%) | | | 40 -> 77.5 |
| Lightning Strike armor-ignore chance | Spells/Bushido/LightningStrike.cs:28-33 | B^2/72000 | 20% | clamps: 100% at 268.3 | clamps | clamps | 50 -> 87.5. PvP armor-ignore capped 35 dmg (Misc/AOS.cs:155-159) |
| Honorable Execution damage scalar | Spells/Bushido/HonorableExecution.cs:18-20 | 1 + B*0.002 | +24% | +60% | +100% | +200% (inside the 300% percentageBonus cap, BaseWeapon.cs:1874) - clamps there | 25 -> 62.5 |
| HE heal on kill | HonorableExecution.cs:38-41 | 20 + B^2/480 | 50 | scales: 207 (~full player HP) | breaks: 540 full heal per kill | breaks: 2103 | - |
| HE swing-speed bonus | HonorableExecution.cs:43; BaseWeapon.cs:1419 | max(1, B^2/720) % SSI | 20 | clamps (125 -> SSI cap 60, reached at B 208) | clamps | clamps | - |
| Momentum Strike damage | Spells/Bushido/MomentumStrike.cs:46-60 | damageBonus B/100 -> +(B-100)% | +20% | +200% | clamps at B 400 (300% cap) | clamps | MomentumStrike.cs:65-67 CheckSkill(Bushido, 70, 120) -> 120 |
| Honor Perfection ramp | Engines/Virtues/HonorContext.cs:117-129 | +B/10 per hit, cap 100 | 12/hit | 30/hit | 50/hit | clamps (100 in one hit) | - |
| Feint (max Bushido/Ninjitsu) | Weapons/Abilities/Feint.cs:35-41; applied BaseWeapon.cs:1994-1998 and Spells/Base/SpellHelper.cs:1029-1033 | reduction = (int)(20 + 3*(S-50)/7) % | 50% | breaks (live today): 127% -> damage <= 0, AOS.Damage returns 0 (Misc/AOS.cs:52-55): full immunity to that target's weapon AND spell damage for 6 s, repeatable | breaks: 212% | breaks: 427% | reaches 100% at S 236.7 |
| Defense Mastery phys resist | Abilities/DefenseMastery.cs:30-39 | 50 + 30*(S-50)/70 | 80 | 157 | 242 | 457 -> all clamp to player resist cap 70 (Server/Mobiles/Mobile.cs:431, :3251) at S 96.7 | - |
| Block (DCI) | Abilities/Block.cs:29-34 | 10*((S-50)/70 + 5) | 60 | 85 | 114 | 185 -> DCI cap 45 (BaseWeapon.cs:1343) - clamps from the start | - |
| Nerve Strike damage / paralyze | Abilities/NerveStrike.cs:54-71 | 15*(B-50)/70 + 0..9 armor-ignoring; para (150/7 + 4B/7)% | 15-24, 90% | 53-62, clamps 100% at 137.5 | 96-105 | 203-212 vs monsters (scales hard); PvP capped 35 | - |
| Riding Swipe damage | Abilities/RidingSwipe.cs:42, :60 | 10 + (int)(10*(B-50)/70 + 5) | 25 | 50 | 79 | 150 - scales | - |
| Frenzied Whirlwind total per target / 3 s | Abilities/FrenziedWhirlwind.cs:34-38 | 10*((S-50)/70 + 5) | 60 | 85 | 114 | 185 - scales | - |
| Whirlwind Attack bonus | Abilities/WhirlwindAttack.cs:58-64 | 1 + (n*B/60)^2/100, max 2.0 | scales | clamps (2.0 at n*B = 600) | clamps | clamps | - |
| Bladeweave pool | Abilities/Bladeweave.cs:44-46 | >= 50 | clamps | clamps | clamps | clamps | - |
| Samurai spell / move gating | Spells/Bushido/SamuraiSpell.cs:46,67; SamuraiMove.cs:9 | value >= req (25-70) | clamps | clamps | clamps | clamps | spells/moves gain in [req-12.5, req+37.5]; max is Momentum Strike 120 |
| Special-move mana total | WeaponAbility.cs:191 | counts | clamps at 300 | | | | |

Bushido GAIN CEILING: 120 (Momentum Strike). No other use gains Bushido above 107.5. Values above 120 can only come from scrolls/admin/bonuses.
Recommendation: give Bushido new effects past 120 rather than scaling these: hard-cap Feint at 50%, cap Evasion duration at 8 s (or below the cooldown), cap Confidence/HE heals (e.g. clamp B at 120 inside them), and keep the no-shield parry product P*B using min(P,120)*min(B,120).

## Focus

| Use | file:line | formula (short) | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Stamina regen points (uncapped part) | customizations\RegenRates.cs:97 (= pinned Misc/RegenRates.cs:97) | (int)(F*0.1); interval 1/(0.1*(2+pts)) s | 12 -> 0.71 s/stam (1.4/s) | 30 -> 0.31 s (3.2/s) | 50 -> 0.19 s (5.2/s) | breaks: 100 -> 0.098 s (10.2 stam/s), stamina drain/leech effects become irrelevant | CheckBonusSkill chance = cur/max*(1-v)+v, v = sqrt(F*0.005) (:28-41): v = 1 at F 200 -> chance >= 1, no gain. Ceiling 200 |
| Mana regen points (uncapped part) | customizations\RegenRates.cs:154 (= pinned :154) | F*0.05 added to totalPoints; ML floors | 6 -> 1.25 s/mana (0.8/s) | 15 -> 0.59 s (1.7/s) | 25 -> 0.37 s (2.7/s) | breaks: 50 -> 0.19 s (5.2 mana/s from Focus alone, stacks with Meditation which is also uncapped) | same 200 |
| Item caps that do NOT apply to Focus | RegenRates.cs:118-121 (stam 24), :187-190 (mana 18) | caps only item/spell regen | - | - | - | - | - |

Note: pinned 18/24 player caps only touch cappedPoints, the skill points are added outside them. Our replacement file did not change this. Regen timers have no minimum interval (Server/Mobiles/Mobile.cs:8020, :8931-8940).
Recommendation: soft-cap with diminishing returns: points = 12 + 8*ln(1 + (F-120)/60) past 120 (about 20 at 300, 26 at 1000 for stamina; half that for mana), and fix the gain ceiling (chance hits 1.0 at Focus 200) by clamping v to 0.95.

## Arms Lore

| Use | file:line | formula (short) | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Exceptional crafted weapon DI | Items/Weapons/BaseWeapon.cs:698-712 | 35 + (int)(AL/20), cap 50 | 41 | clamps: 50 (cap reached exactly at 300) | clamps | clamps | CheckSkill(ArmsLore, 0, 100) -> 100 |
| Exceptional crafted armor random resist points (not shields) | Items/Armor/BaseArmor.cs:595-632 | +(int)(AL/20) random points on top of 15 distributed; uncapped per item | +6 | +15 (30 bonus points per piece) | breaks: +25 (40 per piece) | breaks: +50 (65 per piece; 6 pieces = 390 bonus points, more than the 350 needed for 70 in all five) | CheckSkill(ArmsLore, 0, 100) -> 100 |
| Arms Lore active use | Skills/ArmsLore.cs:33, :89, :107 | target check 0-100; outputs clamp (Math.Min(..,30/35)) | clamps | clamps | clamps | clamps | 100 |
| Repair | Engines/Craft/Core/Repair.cs | does not read Arms Lore (grep) | - | - | - | - | - |
| Pre-AOS wrestling disarm, ThiefAI | Fists.cs:116, :216; ThiefAI.cs:58 | dead under AOS | - | | | | |

The per-player resist cap of 70 (Mobile.cs:431) limits the harm to players, but items become far above normal loot/imbue budget and tradeable.
Arms Lore GAIN CEILING: 100 (every use is 0-100).
Recommendation: cap the armor bonus like the weapon one (e.g. min(AL,300)/20 with a hard cap of +15 per piece) or give it new effects past 120 (durability, lower requirements). Fix gain ceiling if Arms Lore is meant to reach 300+.

---

## Gain ceiling summary

| Skill | ceiling | from |
|---|---|---|
| Swords/Macing/Fencing/Archery/Throwing/Wrestling | ~220 vs 100-skill targets (260 vs 120; 145 with 45 HCI) | BaseWeapon.cs:1358-1365 direct chance |
| Tactics | none (follows Cap) | BaseWeapon.cs:2540 |
| Anatomy | none (follows Cap); bandage 120, active use 100 | BaseWeapon.cs:2543 |
| Lumberjacking (combat) | 100 | BaseWeapon.cs:2548 |
| Parry | 380 with shield (+Bushido non-racial); weapon path when P*B >= 45600 | BaseWeapon.cs:1540, :1581 |
| Bushido | 120 | MomentumStrike.cs:67 |
| Focus | 200 | RegenRates.cs:28-41 |
| Arms Lore | 100 | BaseWeapon.cs:711, BaseArmor.cs:631, ArmsLore.cs |

## BREAKS list

1. Feint (Bushido or Ninjitsu >= 236.7): damage reduction >= 100% -> zero damage from the feinted target (weapons and spells) for 6 s. Already reachable at the live 300 cap (127%). Feint.cs:41, BaseWeapon.cs:1997, SpellHelper.cs:1032, AOS.cs:52.
2. Parry + Bushido without shield: P*B/48000 + 0.05 -> 100% block once P*B >= 45600; live at 300/300 (187%). Blocks every melee and ranged weapon hit. BaseWeapon.cs:1552.
3. Parry with shield >= 380, or Parry alone (weapon) >= 760: 100% block. BaseWeapon.cs:1520, :1554.
4. Evasion + 100% block: also evades every single-target spell and fire breath; Evasion duration >= its 20 s cooldown at Bushido >= 400 -> permanent. Evasion.cs:106, :136, :163.
5. Tactics + Anatomy damage uncapped: x5.9 at 300, x8.2 at 500, x14.8 at 1000 vs x3.9 at 120 (with 100 DI, 125 Str). BaseWeapon.cs:2557-2602.
6. Confidence: regen 112 hp/s at 500, 437 hp/s at 1000 (quadratic); heal on block up to B/12 hp and B/5 stam per block, which fires on every enemy swing once block = 100%. Confidence.cs:131; BaseWeapon.cs:1622-1623.
7. Honorable Execution heal on kill: 540 at 500, 2103 at 1000 (quadratic). HonorableExecution.cs:41.
8. Defender hit chance: at 1000 weapon skill, 100-skill monsters hit 5.9% (4.1% with 45 DCI). BaseWeapon.cs:1358.
9. Focus regen at 1000: 10.2 stam/s and 5.2 mana/s from Focus alone, outside the 18/24 item caps. customizations\RegenRates.cs:97, :154.
10. Arms Lore exceptional armor: +25 (500) / +50 (1000) resist points per piece uncapped; 70-cap trivial with any armor. BaseArmor.cs:597.
11. Shield durability: wear per block vs bashing scales with Parry (29-58 at 1000, shield gone in ~2 blocks). BaseShield.cs:24, :40-43.

Unverified: exact Katana/base damage values used in the damage example (illustrative 12 average); whether any client/other system clamps regen intervals (none found in Server Mobile.cs).
