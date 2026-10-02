# Sweep A: melee / items stat formulas vs stats above 125

Authority: pinned ModernUO D:\UO\ModernUO-pinned, commit 7c9215d97 (verified with rev-parse).
All paths below are relative to D:\UO\ModernUO-pinned\Projects. Expansion EJ: AOS, SE, ML, SA all live.
Value tables computed by sweepA_calc.py in this folder (rerunnable).

## 0. The single most important structural fact

Every LIVE player-felt formula in this domain reads the EFFECTIVE stat (`.Str/.Dex/.Int`, which
PlayerMobile clamps at CAP: UOContent/Mobiles/PlayerMobile.cs:594, :609, :624, `Math.Min(base.X, 150)`)
or the current stamina pool (`.Stam`, bounded by StamMax = effective Dex + BonusStam,
Server/Mobiles/Mobile.cs:2096 and UOContent/Mobiles/PlayerMobile.cs:581, setter clamp Mobile.cs:2067).
No live formula in this domain reads RawStr/RawDex/RawInt. The only Raw reads are the pre-AOS
Concussion Blow (BaseAxe.cs:129, BasePoleArm.cs:79), which is not live.

Consequence:
- With CAP = 150 (pinned), raising the raw ceiling to 200 changes NOTHING in melee/items except that
  players reach 150 effective with fewer item bonuses. All values below at "effective 150" are the
  OSI-balanced ceiling.
- With CAP = 500 (our shard today), every runaway below is ALREADY reachable by stacking item
  bonuses and potions on raw 125 (items sum with no total cap: UOContent/Misc/AOS.cs:506-585 GetValue,
  AOS.cs:590-613 AddStatBonuses; Greater Agility/Strength +20 scaled by Enhance Potions up to
  EP 50 + Alchemy120/3.3 = +86 percent -> about +37, Items/Skill Items/Magical/Potions/BasePotion.cs:207-218, :242).
- BonusStam (PlayerMobile.cs:581) is summed with no cap, so current Stam can exceed effective Dex.

Column convention for tables: "125..200" = stat value the formula sees (raw with no item bonus,
assuming CAP >= value); "150 / 225 / 500" = value at an effective clamp of that size.

## 1. BaseWeapon.cs

### 1a. Swing delay (ML branch) - RUNAWAY (bounded by 1.25 s floor)
- UOContent/Items/Weapons/BaseWeapon.cs:1428 `var stamTicks = m.Stam / 30;`
- :1430-1431 `ticks = speed * 4; ticks = Math.Floor((ticks - stamTicks) * (100.0 / (100 + bonus)));`
- Reads CURRENT Stam (pool). Bonus = SSI, capped at 60 (:1419-1422).
- Own clamp: ticks floor 5 = 1.25 s (:1446-1449). No clamp on Stam.
- Not live: :1442 (SE non-ML), :1455 (AOS pre-SE), :1490 (pre-AOS).

Swing delay seconds, Stam = column value (full stamina, BonusStam 0):

| speed / SSI | 125 | 140 | 155 | 170 | 185 | 200 | eff150 | eff225 | eff500 |
|---|---|---|---|---|---|---|---|---|---|
| 2.00 any SSI | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 |
| 2.50 SSI0 | 1.50 | 1.50 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 |
| 3.00 SSI0 | 2.00 | 2.00 | 1.75 | 1.75 | 1.50 | 1.50 | 1.75 | 1.25 | 1.25 |
| 3.00 SSI30 | 1.50 | 1.50 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 |
| 3.50 SSI0 | 2.50 | 2.50 | 2.25 | 2.25 | 2.00 | 2.00 | 2.25 | 1.75 | 1.25 |
| 3.50 SSI30 | 1.75 | 1.75 | 1.50 | 1.50 | 1.50 | 1.50 | 1.50 | 1.25 | 1.25 |
| 3.50 SSI60 | 1.50 | 1.50 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 | 1.25 |
| 4.25 SSI0 (bow, halberd) | 3.25 | 3.25 | 3.00 | 3.00 | 2.75 | 2.75 | 3.00 | 2.50 | 1.25 |
| 4.25 SSI30 | 2.50 | 2.50 | 2.25 | 2.25 | 2.00 | 2.00 | 2.25 | 1.75 | 1.25 |
| 4.25 SSI60 | 2.00 | 2.00 | 1.75 | 1.75 | 1.50 | 1.50 | 1.75 | 1.50 | 1.25 |
| 5.00 SSI0 (heavy xbow) | 4.00 | 4.00 | 3.75 | 3.75 | 3.50 | 3.50 | 3.75 | 3.25 | 1.25 |
| 5.00 SSI60 | 2.50 | 2.50 | 2.25 | 2.25 | 2.00 | 2.00 | 2.25 | 2.00 | 1.25 |

Stam needed to hit the 1.25 s floor (SSI 0 / 30 / 60): speed 2.0: 90/30/0; 2.5: 150/90/30;
3.0: 210/150/90; 3.5: 270/210/150; 4.25: 360/300/240; 5.0: 450/390/330.
Weapon speeds surveyed from MlSpeed overrides (2.00 to 5.00; 4.25 = Bow, Halberd; 5.00 = HeavyCrossbow).

Verdict: runaway. Each +30 Stam removes one quarter-second tick before SSI scaling, forever, until the
1.25 s floor. At Stam 200 vs 125: slow weapons swing 0.5 s faster (bow SSI60 2.00 -> 1.50 s = +33 percent
DPS; heavy xbow 2.50 -> 2.00 = +25 percent). At CAP 500 with Stam ~450 every weapon swings at 1.25 s, so
weapon speed stops mattering and the slowest, hardest-hitting weapons dominate. Fast weapons
(2.0-2.5) already sit on the floor at 125-150 and gain nothing.

### 1b. Strength damage bonus (AOS) - RUNAWAY (mild to 200, severe at 500)
- BaseWeapon.cs:2556 `var strengthBonus = GetBonus(attacker.Str, 0.300, 100.0, 5.00);`
  GetBonus :2502-2512 = (Str*0.3 + 5 if Str>=100)/100. Reads EFFECTIVE Str.
- Own clamp: none. The comment at :2552-2555 says "No caps apply". The 100 percent cap at :2594-2597
  is only on Damage Increase; the 300 percent cap at :1874 is only on percentageBonus (specials,
  slayers etc.), not on strength.
- Combined at :2599-2602 with Anatomy (:2557), Tactics (:2558), Lumberjacking for axes (:2559-2561).

Fixed: Tactics 120, Anatomy 120, DI 100 (cap), non-axe; axe row adds Lumberjacking 100.

| | 125 | 140 | 155 | 170 | 185 | 200 | eff150 | eff225 | eff500 |
|---|---|---|---|---|---|---|---|---|---|
| Str bonus % | 42.5 | 47.0 | 51.5 | 56.0 | 60.5 | 65.0 | 50.0 | 72.5 | 155.0 |
| total multiplier | 3.888 | 3.933 | 3.978 | 4.022 | 4.067 | 4.112 | 3.962 | 4.188 | 5.012 |
| vs Str 125 | +0.0 | +1.2 | +2.3 | +3.5 | +4.6 | +5.8 | +1.9 | +7.7 | +28.9 |
| axe LJ100 mult | 4.188 | 4.232 | 4.277 | 4.322 | 4.367 | 4.412 | 4.262 | 4.487 | 5.312 |

Verdict: runaway. Linear 0.3 percent per point with no cap. Str 200 vs OSI max 150: +3.8 percent melee
damage (small). Effective 500: +26.5 percent over OSI max on every melee hit, before the 300 percent
special cap. Pre-AOS ScaleDamageOld :2635 (`attacker.Str / 5.0 / 100.0`) is not live.

### 1c. Weapon hit-spell damage Int bonus - RUNAWAY (mild)
- BaseWeapon.cs:2265 `damageBonus += attacker.Int / 10;` inside GetAosDamage :2248-2286, players only.
  Reads EFFECTIVE Int. Used by HitMagicArrow :3582, HitHarm :3599, HitFireball :3625, HitLightning :3642.
- Own clamp: none. Note SDI (:2268) is also not capped here.
- HitLightning (23 + 1d4, avg 25.5), Inscribe 0, SDI 0:

| | 125 | 140 | 155 | 170 | 185 | 200 | eff150 | eff225 | eff500 |
|---|---|---|---|---|---|---|---|---|---|
| Int bonus % | 12 | 14 | 15 | 17 | 18 | 20 | 15 | 22 | 50 |
| avg Lightning dmg | 28.6 | 29.1 | 29.3 | 29.8 | 30.1 | 30.6 | 29.3 | 31.1 | 38.2 |

Verdict: runaway (mild). +5 points over OSI at 200; +35 points at 500 (hit spells +30 percent vs eff150).

### 1d. Parry low-Dex penalty - FINE (by design flat above 80)
- BaseWeapon.cs:1535-1538 (shield) and :1574-1577 (weapon): `if (defender.Dex < 80) chance = chance * (20 + defender.Dex) / 100;`
  Reads EFFECTIVE Dex of defender. Factor 1.00 at every value >= 80; stats above 125 do nothing.

### 1e. Hit chance and defense chance - FINE (no stat input)
- BaseWeapon.cs:1235-1366: only skills, HCI/DCI (capped 45 at :1294, :1343), effects. No Str/Dex/Int read.

### 1f. Equip requirements and equipped stat bonuses - FINE
- BaseWeapon.cs:1049, :1055 (`AOS.Scale(StrRequirement, 100 - GetLowerStatReq())`), :1061: thresholds on
  EFFECTIVE stats; more stat only makes them easier. OnEquip/OnAdded stat mods :1072-1093, :4023-4033.
- Same pattern: BaseArmor.cs ComputeStatReq :826-836, ComputeStatBonus :838-846, CanEquip :1128-1148,
  stat mods :1046-1066, :1172-1193; BaseClothing.cs :484-490, :496-505, :513-536; BaseJewel.cs :211-231,
  :420-440; AOS.cs AddStatBonuses :590-613; PlayerMobile.cs:1406 (armor recheck).
- No item requirement approaches 150, so a higher CAP never blocks or unblocks anything.
- Note: item stat bonuses are summed without any total cap; the PlayerMobile CAP is the only limiter
  of the effective stat. That is the lever for everything in this sweep.

### 1g. Leech, Confidence - FINE
- Leech :2057, :2062, :2067 scale with damage dealt, not stats; target pools are clamped by setters.
- Confidence on parry :1622-1623 uses Bushido skill.

### 1h. Creature only
- BaseWeapon.cs:2457-2458 `min = max = c.Str / 28` creature unarmed damage (BaseCreature with no
  DamageMin, non-human body). Creature only; player pets use their own Str, not the player CAP.

## 2. Weapon subclasses and abilities

### 2a. Thrown weapon range - RUNAWAY (fine at CAP 150)
- UOContent/Items/Weapons/Throwing/BaseThrown.cs:24
  `baseRange - 3 + (attacker.Str - AosStrengthReq) / ((140 - AosStrengthReq) / 3)`. EFFECTIVE Str.
- Designed so range = MaxThrowRange exactly at Str 140. Own clamp: none. Consumer:
  Server/Mobiles/Mobile.cs:790 `InRange(combatant, weapon.MaxRange)`, plus MysticArc.cs:31. CanSee
  (Mobile.cs:7156-7168) has no distance limit; only LOS (Mobile.cs:793) and the client view range bound it.
- Params: Boomerang MinThrowRange 4, StrReq 25 (Boomerang.cs:12,16); Cyclone 6/40 (Cyclone.cs:12,16);
  SoulGlaive 8/60 (SoulGlaive.cs:12,16).

| range (tiles) | 125 | 140 | 155 | 170 | 185 | 200 | eff150 | eff225 | eff500 |
|---|---|---|---|---|---|---|---|---|---|
| Boomerang (design max 7) | 6 | 7 | 7 | 7 | 8 | 8 | 7 | 9 | 16 |
| Cyclone (design max 9) | 8 | 9 | 9 | 9 | 10 | 10 | 9 | 11 | 19 |
| SoulGlaive (design max 11) | 10 | 11 | 11 | 12 | 12 | 13 | 11 | 14 | 24 |

Exceeds design max from Str 164 (SoulGlaive), 172 (Cyclone), 177 (Boomerang). At CAP 150 it is exactly
OSI. At Str 200: +1/+1/+2 tiles beyond OSI. At 500: 16-24 tiles, at or past Core.GlobalUpdateRange 18
(Server/Main.cs:150): a gargoyle thrower can hit from the edge of the screen while melee/most
ranged opponents cannot respond. Verdict: runaway.

### 2b. Force of Nature (SA) - PLATEAU at Str 150
- UOContent/Items/Weapons/Abilities/ForceOfNature.cs:106 `var bonus = Math.Min(100, Math.Max(50, from.Str - 50));`
  EFFECTIVE Str. Scalar (100+bonus)/100: 125 -> 1.75, 140 -> 1.90, 150 and above -> 2.00.
- Feeds percentageBonus (BaseWeapon.cs:1797), which is capped at 300 (:1874).

### 2c. Concussion Blow (SA) - FINE
- Abilities/ConcussionBlow.cs:47-58: 10 + min(|hits% - mana%| / 4, 20) on the DEFENDER's current/max
  pools. Percent based and clamped at 20; stat size irrelevant.

### 2d. Bleed, Talon Strike, mace/staff stamina drain - FINE (no stat input)
- BleedAttack.cs:74 `Utility.RandomMinMax(level, level * 2)`; TalonStrike.cs:86 damage from hit.
- BaseBashing.cs:24, BaseStaff.cs:23: flat 3-5 Stam drain. Note only: a flat drain is relatively
  weaker against larger stamina pools (no formula issue).

### 2e. Weapon ability mana - FINE
- WeaponAbility.cs:307, :324 `from.Mana < mana`, mana cost from skills/LMC; pool check only.

### 2f. Not live (pre-AOS)
- BaseAxe.cs:127-129 and BasePoleArm.cs:77-79: Concussion `-(defender.RawInt / 2)` gated `!Core.AOS`
  (BaseAxe.cs:115, BasePoleArm.cs:65). Not live.
- Fists.cs:77, :83, :123, :148, :158: pre-AOS stun/disarm Stam cost, gated `!Core.AOS` at :167. Not live.

### 2g. ThrowingDagger - BROKEN (degenerate), low impact
- UOContent/Items/Weapons/Knives/ThrowingDagger.cs:57 `if (Utility.RandomDouble() >= Math.Sqrt(m.Dex / 100.0) * 0.8)`
  hit chance = 1 - 0.8*sqrt(targetDex/100), target EFFECTIVE Dex. :61 damage `Utility.Random(5, from.Str / 10)`
  = 5 .. 4+Str/10 (Utility.Random(from,count), Server/Random/BuiltInRng.cs:34).
- Hit%: 125 -> 10.6, 140 -> 5.3, 150 -> 2.0, 155 -> 0.4, 157+ -> 0. Damage max: 125 -> 16, 200 -> 24, 500 -> 54.
- Verdict: broken for target Dex >= 157 (immune). Low impact: plain Item, only [Constructible],
  no other references in UOContent (GM-spawn only).

## 3. Spells/Base/SpecialMove.cs, Bushido, Ninjitsu - FINE (pool checks only)
- SpecialMove.cs:103, :117 mana check/consume; SamuraiSpell.cs:53, :74, :86; NinjaSpell.cs:52, :73, :85;
  AnimalForm.cs:133-157, :453-473 mana; AnimalForm.cs:535-541 Cu Sidhe regen flat 20-50.
- Confidence.cs:133, HonorableExecution.cs:41: Bushido-skill based heals.
- No Str/Dex/Int formula in any Bushido or Ninjitsu file (grep of both folders).

## 4. Healing and consumables

### 4a. Self bandage delay - BROKEN (worst finding)
- UOContent/Items/Skill Items/Misc/Bandage.cs:484 `var dex = healer.Dex;` (EFFECTIVE Dex)
- :493 `seconds = 5.0 + 0.5 * ((double)(120 - dex) / 10);` (AOS, onSelf; "TODO: Verify algorithm")
- :531 `seconds *= 1000;` :533 `new BandageContext(..., TimeSpan.FromMilliseconds(seconds))`, :535 Start.
- Own clamp: NONE. No floor.

| | 125 | 140 | 155 | 170 | 185 | 200 | eff150 | eff225 | eff500 |
|---|---|---|---|---|---|---|---|---|---|
| self delay s | 4.75 | 4.00 | 3.25 | 2.50 | 1.75 | 1.00 | 3.50 | -0.25 | -14.00 |

- Reaches 0 at Dex 220 and goes negative above it.
- Negative delay reaches the timer wheel: Server/Timer/Timer.cs:115 `AddTimer(this, (long)Delay.TotalMilliseconds)`;
  Server/Timer/Timer.TimerWheel.cs:185-235 computes `slot = (delay >> 3) + ringIndex + ...` with no
  negative guard. Reading the code: when ringIndex is smaller than |delay|/8 the slot is negative and
  `_rings[i][slot]` throws IndexOutOfRangeException inside Bandage.BeginHeal; otherwise the timer lands
  in a slot behind the current index and fires only after the 4096-slot ring wraps (up to about 32 s at
  8 ms per slot, TimerWheel.cs:30-34, Turn() :68-90). Either outcome is a bug. (Code reading only; not
  run.)
- Before breaking: Dex 200 gives a 1.0 s self-bandage vs 4.75 s at 125 and 3.5 s at OSI 150. With
  Healing/Anatomy 120 (heal 43-72, :387-388) that is roughly 57 HP per second of self-healing at Dex 200
  vs about 12 at 125 and 16 at 150: a near-unkillable melee character. At Dex 219 the delay is 0.05 s.
- Reachability: at raw 125 needs +96 Dex from items/potions (hard but possible today under CAP 500);
  at raw 200 needs +21 (trivial: one Greater Agility potion).

### 4b. Bandage on others - PLATEAU at Dex 204 (own clamp 0.70 s)
- Bandage.cs:506-513 `if (dex < 204) seconds = 3.2 - Math.Sin(dex / 130) * 2.5 + resDelay; else 0.7 + resDelay`.
  sin peaks at dex = 130*pi/2 = 204.2, so the branch is a deliberate floor.
- 125 -> 1.15, 140 -> 1.00, 150 -> 0.91, 155 -> 0.88, 170 -> 0.79, 185 -> 0.73, 200 -> 0.70, 225/500 -> 0.70.
- Still a 1.3x faster healer vs OSI 150 at Dex 200, but bounded.
- Vet target :502 flat 2.0 s. Pre-AOS :497, :515-525 not live.
- Heal amount :387-388 uses skills only. :400 `Patient.HitsMax / 100.0` only for monster/animal bodies
  (pets; creature HitsMax).

### 4c. Potions - FINE
- Refresh: Refresh Potions/BaseRefreshPotion.cs:32 `Stam += Scale(from, (int)(Refresh * from.StamMax))`:
  proportional to the pool (25 / 100 percent), scales sanely.
- Heal: Heal Potions/BaseHealPotion.cs:32 full-HP check; heal amount fixed min/max scaled by EP.
- Agility / Strength: BaseAgilityPotion.cs:25, BaseStrengthPotion.cs:25 flat +10/+20 (x EP, about +37 max)
  via SpellHelper.AddStatOffset (Spells/Base/SpellHelper.cs:288-291). Flat; they feed the runaways above.

### 4d. Food, Magic fish, Rose of Trinsic, Clarity, Rejuvenation ankh - FINE
- Food.cs:94-96 flat Stam gain if below StamMax. MagicFish.cs:19 flat stat offset, 1 minute.
- RoseOfTrinsic.cs:180 flat +5 Str 5 minutes.
- ClarityPotion.cs:36-42: removes Concussion mod (pre-AOS only, so a no-op live) and adds flat Int.
- RejuvinationAnkhs.cs:23-49 refill pools to max: scales with pool, fine.

### 4e. Poison - FINE (victim side, clamped)
- UOContent/Misc/Poison.cs:120-121 `damage = 1 + (int)(_mobile.Hits * _poison._scalar); Math.Clamp(damage, min, max)`.
  Reads victim CURRENT Hits; AOS tables Misc/PoisonKinds.cs:79-83 clamp max at 16/18/20/30/50. A player
  HitsMax of 137 (Str 125) already hits the clamp for Deadly/Lethal; larger HP pools make poison
  relatively weaker, not stronger.

### 4f. Ninjitsu bombs - FINE
- EggBomb.cs:37, SmokeBomb.cs:31 flat `Mana < 10` check.

## 5. Virtues, crafting, PvP, misc - FINE / nothing player-felt
- Honor.cs:134 target must be at full HP (creature target; ML forbids players at :128). Creature only.
- Sacrifice.cs:108 target hits percent >= 90. Creature only.
- Repair.cs:171 golem HitsMax - Hits. Creature only.
- CraftItem.cs:287-299 pool >= recipe cost checks. Fine.
- Corpse.cs:265 looting rights from creature HitsMax. Creature only.
- DuelContext.cs:742-744, :1879-1881 refill pools to max. Fine.
- KingOfTheHill.cs:93 `Stam >= StamMax` check. Fine.
- StormsEye.cs:103-110 `damage = mob.Hits * 6 / 10` clamped at 75 (victim side). Fine.
- PlantItem.cs:95 plant system hits, not a mobile. Nothing.
- Server/Items/Item.cs:2097 is an XML doc comment only. Nothing.
- Fatigue on damage (outside listed files, melee-felt): UOContent/Misc/StaminaSystem.cs:287
  `damage * (100.0 / m.Hits) * (Stam / 100) - 5` called from PlayerMobile.cs:2379. Proportional to
  Stam/Hits, so it scales with the pool. Fine.

## 6. Files checked with nothing player-felt beyond the above
Items/Weapons/Abilities: ArmorIgnore, ArmorPierce, Bladeweave, Block, CrushingBlow, DefenseMastery,
Disarm, Dismount, DoubleShot, DoubleStrike, DualWield, Feint, ForceArrow, FrenziedWhirlwind,
InfectiousStrike, InfusedThrow, LightningArrow, MortalStrike, MovingShot, MysticArc (range only, see 2a),
NerveStrike, ParalyzingBlow, PsychicAttack, RidingSwipe, SerpentArrow, ShadowStrike, WhirlwindAttack,
WeaponAbilityPackets: no Str/Dex/Int/Stam/Hits/Mana formula (folder grep). All other Bushido and
Ninjitsu move files: none. BaseRanged: no stat reads.

## (a) Ranked runaways / brokens, worst first
1. BROKEN: self bandage delay, Bandage.cs:493. No floor; 1.0 s at Dex 200, 0 at 220, negative (timer-wheel
   exception or ~32 s stall) above 220. Live today if anyone reaches effective Dex > 220 under CAP 500.
2. RUNAWAY: ML swing speed, BaseWeapon.cs:1428-1431. Stam/30 uncapped until the 1.25 s floor; slow
   weapons +25-33 percent DPS at Stam 200, all weapons 1.25 s at Stam ~330-450 (CAP 500 + BonusStam).
3. RUNAWAY: thrown range, BaseThrown.cs:24. Past design max from Str 164-177; 16-24 tiles at 500.
4. RUNAWAY: Str melee damage bonus, BaseWeapon.cs:2556. +3.8 percent over OSI at 200, +26.5 percent at 500.
5. RUNAWAY (mild): hit-spell Int bonus, BaseWeapon.cs:2265. +5 points at 200, +35 at 500.
6. BROKEN (low impact, GM item): ThrowingDagger.cs:57 target immune at Dex >= 157.
Plateaus (safe): ForceOfNature.cs:106 (Str 150), Bandage.cs:506-513 other-heal (Dex 204).

## (b) Where a builder would put a soft cap
- Global lever (fixes everything here at once): UOContent/Mobiles/PlayerMobile.cs:588-630 (CAP in the
  Str :594, Int :609, Dex :624 getters). Keeping it at 150 makes every formula in this sweep OSI-identical
  regardless of raw 200. StamMax also inherits it via Mobile.cs:2096 (BonusStam at PlayerMobile.cs:581
  remains additive).
- If CAP is raised, per-formula caps:
  - UOContent/Items/Skill Items/Misc/Bandage.cs:484 (clamp `dex`) or :493 (floor `seconds`). MANDATORY
    for any CAP above 219.
  - UOContent/Items/Weapons/BaseWeapon.cs:1428 (clamp `m.Stam` before `/ 30`).
  - UOContent/Items/Weapons/BaseWeapon.cs:2556 (clamp `attacker.Str` passed to GetBonus).
  - UOContent/Items/Weapons/BaseWeapon.cs:2265 (clamp `attacker.Int / 10`).
  - UOContent/Items/Weapons/Throwing/BaseThrown.cs:24 (clamp Str at 140 or result at MaxThrowRange).
  - UOContent/Items/Weapons/Knives/ThrowingDagger.cs:57 (clamp target Dex or floor the hit chance).
- Defensive (independent of stats): Server/Timer/Timer.cs:115 / Timer.TimerWheel.cs:185 accept a
  negative delay without a guard; any caller passing a negative TimeSpan hits the same failure.

## (c) Not verified
- Runtime outcome of a negative bandage delay (exception vs stall) is from reading
  Timer.TimerWheel.cs:185-235 and :68-90 only; not executed. Whether the exception would crash the
  server or be caught by the target/packet handler was not traced.
- Whether our shard patch (CAP 500) changes any of these call sites: I read pinned only, per the rules.
- Practical reachable effective stats under CAP 500 depend on the shard's loot intensity tables
  (not in this sweep); the "+96 Dex" and "+21 Dex" reachability figures are arithmetic, not tested.
- Client-side targeting limits for thrown range beyond 18 tiles were not checked (server does not limit).
