# Sweep B - MAGIC domain: stat -> player-felt number, behavior above 125

Authority: pinned ModernUO at D:\UO\ModernUO-pinned (7c9215d97). All paths below are relative to
D:\UO\ModernUO-pinned\Projects unless prefixed "ours:" (= D:\ShatteredLegacy\server\...).
Values computed by notes/cc-P25-scratch/sweepB/calc.py (throwaway; integer math mirrors the C#).

Stat semantics used (verified):
- Mobile.Int = Clamp(m_Int + GetStatOffset, 0, 65000) (Server/Mobiles/Mobile.cs:1984). Offsets (items, Bless, Curse) are applied BEFORE the player clamp.
- PlayerMobile.Int/Str/Dex = Math.Min(base.X, CAP) under ML for players (UOContent/Mobiles/PlayerMobile.cs:588-630; pinned CAP 150). Ours: PlayerMobile-individual-stat-cap.patch swaps 150 for ClusterFStatCaps.IndividualStatCap, which is 500 when enabled, 150 when disabled (ours: customizations/ClusterFStatCaps.cs:10, :103).
- ManaMax = Int (Server/Mobiles/Mobile.cs:2151) + BonusMana (+20 elf) (UOContent/Mobiles/PlayerMobile.cs:584-585). Uncapped BonusMana in pinned.
- HitsMax (player, AOS) = Str/2 + 50 + min(BonusHits,25) (PlayerMobile.cs:555-576). StamMax = Dex + BonusStam (PlayerMobile.cs:581, Mobile.cs:2096).

Live-file determination for regen/meditation:
- ours: docker/uo/apply-patches.sh:193-201 excludes Meditation.cs and RegenRates.cs from the additive copy; :243-244 replace_file customizations/Meditation.cs -> Projects/UOContent/Skills/Meditation.cs; :250 replace_file customizations/RegenRates.cs -> Projects/UOContent/Misc/RegenRates.cs. replace_file (:39-51) is a plain cp. So OURS IS LIVE for both.
- diff vs pinned: RegenRates only changes the armor branch (ours RegenRates.cs:158-165: if meditating and Meditation > 200, armored medPoints *= max(0.1, 1 - armorPenalty*0.02) instead of 0). Meditation.cs adds "armored expert" (skill > 200) path, an armor penalty on chance, and gain cap = skill Cap (ours Meditation.cs:50-59, 85-92). The stat-reading formulas are byte-identical to pinned.

Fixed inputs for multi-input formulas (stated per row): Magery 120, EvalInt 120, Inscription 120, Meditation 120, Focus 120, Magic Resist of target 120 (or 0 where noted), SDI PvP-capped 15, PvM SDI 35 (pinned has NO PvM SDI cap), Mana Regen items 18 (= ML player cap).
Columns: raw 125/140/155/170/185/200 assume no item offsets (effective = raw); last three are effective 150 (pinned clamp), 225, 500 (ours today).

---------------------------------------------------------------------------------------------

## 1. Spell damage Int bonus (GetNewAosDamage) - RUNAWAY (bounded only by the effective clamp)

UOContent/Spells/Base/Spell.cs:226-227
  var intBonus = Caster.Int / 10;  damageBonus += intBonus;
- Reads Caster.Int = EFFECTIVE Int (player: clamped at CAP; creature: uncapped).
- Own clamp: none. No cap on intBonus, nor on the summed damageBonus. The only cap in the function is the PvP item-SDI cap of 15 (Spell.cs:229-237), which does NOT apply to intBonus.
- Full chain (Spell.cs:219-257): dmg = dice*100; inscribeBonus = (insc + 1000*(insc/1000))/200 (=11 at Inscribe 120); dmg = Scale(dmg, 100 + inscribeBonus + Int/10 + SDI [+Reaper]); dmg = Scale(dmg, 30 + 9*EvalFixed/100) (=138% at Eval 120); dmg = Scale(dmg, scalar*100); /100.
- Callers (all live under AOS): MagicArrow.cs:46, Harm.cs:36, Fireball.cs:37, Lightning.cs:36, EnergyBolt.cs:38, Explosion.cs:82, FlameStrike.cs:36, ChainLightning.cs:60, MeteorSwarm.cs:63, Mysticism BombardSpell.cs:58, EagleStrikeSpell.cs:68, HailStormSpell.cs:62, NetherCycloneSpell.cs:72, SpellPlagueSpell.cs:57, :161 (all under Spells/). Necro/Chivalry/Spellweaving damage spells do NOT go through this (no Int term found in those folders).

Values (Inscribe 120, Eval 120; FlameStrike avg dice 51; EnergyBolt avg 43):

| stat | 125 | 140 | 155 | 170 | 185 | 200 | eff150 | eff225 | eff500 |
|---|---|---|---|---|---|---|---|---|---|
| Int/10 | 12 | 14 | 15 | 17 | 18 | 20 | 15 | 22 | 50 |
| damageBonus PvP (11+Int/10+15) | 38 | 40 | 41 | 43 | 44 | 46 | 41 | 48 | 76 |
| FlameStrike PvP avg | 97 | 98 | 99 | 100 | 101 | 102 | 99 | 104 | 123 |
| FlameStrike PvM (SDI 35) avg | 111 | 112 | 113 | 114 | 115 | 116 | 113 | 118 | 137 |
| EnergyBolt PvP avg | 81 | 83 | 83 | 84 | 85 | 86 | 83 | 87 | 104 |

- Verdict: runaway. Linear, never plateaus. At raw 200 with CAP 225 it is mild (+3% over OSI max of Int 150). At the current CAP 500 an Int-stacked mage gets +50 damage points, more than 3x the PvP SDI cap, and it is not subject to that cap.
- At 200 vs 125: +8 damage points, about +5% damage on every Magery/Mysticism nuke. With effective 500 (raw 200 + ~300 from items/buffs is possible only if item Int is uncapped, see section 9): +27% PvP damage over a 125 mage; a FlameStrike averages 123 instead of 97, EBolt 104 vs 81. In PvP that turns a standard 3-spell combo into a likely kill on a 150-HP target with no additional SDI. Biggest magic risk.

## 2. Mana pool - RUNAWAY (linear; listed here because it is the magic budget; HP/Stam pools belong to another sweep)

Server/Mobiles/Mobile.cs:2151 ManaMax => Int; UOContent/Mobiles/PlayerMobile.cs:584-585 adds BonusMana and +20 elf.
- Reads effective Int (clamped at CAP). Own clamp: none (BonusMana uncapped too).
- Values (no BonusMana): 125, 140, 155, 170, 185, 200 | eff 150 | 225 | 500.
- Verdict: runaway at CAP 500 (3.3x OSI's 150 pool); proportional and tolerable at CAP 225.
- In play: a 200-Int mage carries 200 mana vs 150 (~4 more FlameStrikes before LMC); at 500 effective, ~11 extra FlameStrikes (40 mana base cost) per pool. Regen does not keep pace (see 3), so the pool mostly matters for burst/sustained spam in a single fight.

## 3. Mana regeneration (AOS/ML branch) - FINE

Live file: ours customizations/RegenRates.cs (identical formula to pinned UOContent/Misc/RegenRates.cs:146-202).
ours RegenRates.cs:148  medPoints = from.Int + Meditation*3;
ours RegenRates.cs:150  medPoints *= Meditation < 100 ? 0.025 : 0.0275;
ours RegenRates.cs:154  focusPoints = Focus*0.05;
ours RegenRates.cs:167  totalPoints = focus + medPoints + (Meditating ? min(medPoints,13) : 0);
ours RegenRates.cs:174-190 cappedPoints = RegenMana items (+3 VampEmbrace / +13 Lich), capped 18 for ML players
ours RegenRates.cs:199 Floor; :202 rate = 1/(0.1*(2+total)) seconds per +1 mana (Server/Mobiles/Mobile.cs:8899-8905 ticks +1 mana).
- Reads from.Int = effective Int (clamped at CAP). No stat clamp of its own; the meditating bonus is capped at 13 points; item MR capped 18.
- Pre-AOS branch (ours :204-224, (Int+Med)*0.5 table) is not live.
- Armor branch (ours :158-165) is shard-specific and Meditation-skill-gated (>200), not stat-gated.

Mana per second (Med 120, Focus 120, MR 18):

| stat | 125 | 140 | 155 | 170 | 185 | 200 | eff150 | eff225 | eff500 |
|---|---|---|---|---|---|---|---|---|---|
| medPoints | 13.34 | 13.75 | 14.16 | 14.57 | 14.99 | 15.40 | 14.03 | 16.09 | 23.65 |
| mana/s idle | 3.9 | 3.9 | 4.0 | 4.0 | 4.0 | 4.1 | 4.0 | 4.2 | 4.9 |
| mana/s meditating | 5.2 | 5.2 | 5.3 | 5.3 | 5.3 | 5.4 | 5.3 | 5.5 | 6.2 |
| seconds to refill Int-sized pool from 0, idle | 32 | 36 | 39 | 43 | 46 | 49 | 38 | 54 | 102 |

- Verdict: fine. Int coefficient is 0.0275 points/Int = 0.00275 mana/s per Int; 125->200 adds 0.2 mana/s. Regen lags pool growth, so it acts as a natural brake.
- Note (out of stat scope): the Meditation-skill term (Med*3*0.0275) dominates and ours lets Meditation exceed 120 (gain cap = skill Cap, ours Meditation.cs:92). That, not Int, is the regen lever on this shard.
- HP regen (pinned Misc/RegenRates.cs:44-87, same in ours) and Stam regen (:89-128) read no stat; only item points capped 18/24 and Focus. Covered by another sweep.

## 4. Active Meditation success chance - BROKEN (degenerate absolute-deficit term; no overflow)

Live file: ours customizations/Meditation.cs:83 (pinned UOContent/Skills/Meditation.cs:76 identical)
  chance = (50.0 + (skillVal - (m.ManaMax - m.Mana)) * 2) / 100;
- Reads ManaMax (pool, from effective Int + BonusMana) and current Mana. No clamp; negative chance simply fails.
- The formula uses the ABSOLUTE mana deficit. Chance > 0 needs deficit < Meditation + 25. Pool growth from stats therefore makes active meditation impossible from low mana.

Minimum current mana needed for any chance (Mana from 0; BonusMana 0):

| ManaMax | 125 | 140 | 155 | 170 | 185 | 200 | 150 | 225 | 500 |
|---|---|---|---|---|---|---|---|---|---|
| Med 120: chance at 0 mana | 0.40 | 0.10 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Med 120: min mana for >0 | 0 | 0 | 10 | 25 | 40 | 55 | 5 | 80 | 355 |
| Med 200: min mana for >0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 275 |

- Verdict: broken (none of the given categories fit exactly; it is an inverted cliff: more Int = worse). It is already slightly present at OSI (150 pool), but at effective 500 a 120-Med mage cannot start meditating until 71% full, i.e. active meditation becomes useless. Shard's Meditation > 120 partially offsets it.
- Fix shape: make the deficit term relative, e.g. (ManaMax - Mana) * 125 / ManaMax.

## 5. Magery stat buffs and curses (Bless, Strength, Agility, Cunning, Curse, Weaken, Clumsy, Feeblemind, Mass Curse) - FINE (proportional), with clamp interactions

UOContent/Spells/Base/SpellHelper.cs:380-391 GetOffsetScalar: curse% = 8 + (Eval_caster - Resist_target)/10; buff% = 1 + Eval/10; floored at 0.
UOContent/Spells/Base/SpellHelper.cs:393-408 GetOffset (AOS): (int)(target.RawStr|RawDex|RawInt * percent). Pre-AOS (:395-398, 1 + Magery/10) not live.
- Reads TARGET RAW stat (not effective). Applied via StatMod (SpellHelper.cs:303-328 AddStatBonus, :349-375 AddStatCurse), so the result is added to raw+items and then clamped by the player CAP.
- Callers: Bless.cs:32-34, Strength.cs:32, Agility.cs:32, Cunning.cs:32, Curse.cs:44-64, Weaken.cs:33, Clumsy.cs:33, Feeblemind.cs:35, MassCurse.cs:46-48 (all under Spells/). Duration = 6*Eval/5 s (SpellHelper.cs:377-379), stat-independent.
- Own clamp: none on magnitude.

| target raw | 125 | 140 | 155 | 170 | 185 | 200 | 150 | 225 | 500 |
|---|---|---|---|---|---|---|---|---|---|
| Bless/Str/Agi/Cun +13% (Eval 120) | 16 | 18 | 20 | 22 | 24 | 26 | 19 | 29 | 65 |
| Curse 8% (Eval 120 vs Resist 120) | 10 | 11 | 12 | 13 | 14 | 16 | 12 | 18 | 40 |
| Curse 20% (vs Resist 0) | 25 | 28 | 31 | 34 | 37 | 40 | 30 | 45 | 100 |

(eff 150/225/500 columns read as raw values for the formula; the formula only reads raw, max raw is 200 under F-12.)
- Verdict: fine. Keeps OSI's percentage design; grows only with raw (max 200), not with items.
- Clamp interactions builders must know:
  a. Bless absorbed by a tight CAP: raw 200 + Bless 26 = 226 > 225. With CAP 225 Bless gives a 200-raw player at most +25 and nothing at all once items reach the cap.
  b. Curse absorbed by headroom: the clamp is applied after the negative mod (Mobile.cs:1984 then PlayerMobile.cs:604-611), so if raw + item bonus - curse >= CAP the curse has zero felt effect. OSI has the same quirk at 150; a lower F-12 CAP (225) relative to raw 200 widens it.

## 6. Mind Blast (AOS) - PLATEAU

UOContent/Spells/Fifth/MindBlast.cs:43
  var damage = Math.Min((int)((Caster.Skills.Magery.Value + Caster.Int) / 5), 60);  then RandomMinMax(d, d+4) at :119.
- Reads caster EFFECTIVE Int. Own clamp: 60. Not routed through GetNewAosDamage (no SDI, no Int/10 double-dip); slayer scalar forced to 1.0 (:128).
- Magery 120: 125->49, 140->52, 155->55, 170->58, 185->60, 200->60; eff 150->54, 225->60, 500->60.
- Verdict: plateau at effective Int 180 (Magery 120). Above 180 Int no gain. Mild power gain 125->180 (+11 dmg) that OSI could reach only at Int 180, i.e. never (OSI clamp 150 gives 54).
- Pre-AOS branch (:62-107, target highest-lowest stat, each clamped at 150, damage capped 45) is not live.

## 7. Evaluate Intelligence readout - PLATEAU (cosmetic)

UOContent/Skills/EvalInt.cs:55-61
  intel = targ.Int +/- margin; intMod = Math.Clamp(intel / 10, 0, 10); mnMod = Clamp(mana% /10, 0, 10)
- Reads target effective Int; mana as % of ManaMax. Clamp 10 -> all Int >= 100 shows the top message. Verdict: plateau at Int 100 (pure message text). Harmless.

## 8. Bard difficulty vs a player target (Peacemaking single-target) - FINE

UOContent/Items/Skill Items/Musical Instruments/BaseInstrument.cs:260
  val = targ.HitsMax * 1.6 + targ.StamMax + targ.ManaMax + SkillsTotal/10; >700 compressed by 3/11 (:264-267); /10 (:291); SE cap 160 (:298-301).
- Reads pools (HitsMax/StamMax/ManaMax from effective stats). Used by Peacemaking.cs:163 (players CAN be targeted; the duration branch :196-207 only applies to creatures, players just get combatant cleared). Discordance.cs:151 excludes players. Provocation is creature-only.
- All stats = s, BonusHits 25, skills 720: 125->83.3, 140->84.5, 155->85.6, 170->86.8, 185->87.9, 200->89.0; eff 150->85.2, 225->90.9, 500->112.0.
- Verdict: fine (monotone, own cap 160). High-stat players get modestly harder to peace.
- Discordance stat malus (Discordance.cs:206-231, RawStr/RawInt/RawDex * scalar) is in the pre-AOS else-branch: not live. AOS Discordance (:173-201) is skill-only.

## 9. Item stat bonuses (BonusInt/Str/Dex) - no formula, but uncapped feed into effective stats

UOContent/Items/Skill Items/Magical/Spellbook.cs:565-585 (OnAdded) and :855-880 (re-apply), UOContent/Misc/AOS.cs:590-616 (AddStatBonuses for talismans/quivers), clothing BaseClothing.cs:506. Pinned has no aggregate cap on item stat bonuses; the PlayerMobile CAP is the only limit. This is what lets effective Int exceed raw 200 and reach 500. Not a formula; listed because every Int-scaling row above is "raw 200 + items" in practice.

## 10. Pool-ratio and pool-sized effects (fine, proportional)

- Nether Cyclone drain: UOContent/Spells/Mysticism/NetherCycloneSpell.cs:83-84 m.Stam -= (int)(m.StamMax * r); m.Mana -= (int)(m.ManaMax * r), r = (Mysticism+Focus/Imbue)/1200 - Resist/800. Target pool max, percentage based: fine (bigger pools lose more in absolute, same fraction).
- Strangle: Spells/Necromancy/Strangle.cs:188 damage *= 3 - Stam/StamMax*2. Ratio of target pool: fine.
- Divine Fury: Spells/Chivalry/DivineFury.cs:40 Caster.Stam = Caster.StamMax. Full refill scales with Dex pool: fine (linear; stamina pool covered by another sweep).
- Earthquake AOS: Spells/Eighth/Earthquake.cs:58 damage = m.Hits/2 (+0..15), no cap for players: proportional to target current HP: fine.
- Close Wounds / Noble Sacrifice / Gift of Renewal / AnimalForm: HitsMax only as "is damaged" guards (CloseWounds.cs:48, :67-69; NobleSacrifice.cs:100; GiftOfRenewal.cs:134; Ninjitsu/AnimalForm.cs:535). Heal amounts are Karma/skill based (CloseWounds.cs:64 clamp 7..39; NobleSacrifice.cs:102 clamp 8..24). Fine.
- Word of Death: Spells/Spellweaving/WordOfDeath.cs:50 !m.Player guard: creature only.
- Mana Drain / Mana Vampire (Fourth/ManaDrain.cs:41, Seventh/ManaVampire.cs:41-58), Wraith Form leech (Necromancy/WraithForm.cs:37-38), Spirit Speak heal (Skills/SpiritSpeak.cs:137-183): skill/damage based, clamped by target current mana; no stat read. Fine.

## 11. Creature only

- Summon stat scaling by caster Magery: Spells/Base/SpellHelper.cs:520-537 (creature.RawStr/RawDex/RawInt *= 1 + (Magery-100)/200).
- Animate Dead scaling: Spells/Necromancy/AnimateDeadSpell.cs:384-396.
- Magical Barrier: Mobiles/Abilities/MagicalBarrier.cs:22 (creature HitsMax ratio).
- Creature casters' Spell.cs:226 Int bonus is uncapped (creature Int not clamped): existing behavior.
- Familiars: DarkWolf.cs:59 (++caster.Stam), ShadowWisp.cs:92 (mana from Karma): no stat read.

## Files checked with nothing player-felt from stats

Spells/Base/MagerySpell.cs (resist chance is skill-only, :61-99), Spells/Base/Spell.cs (cast delay, recovery, mana cost :520-760: no stat), Spells/Chivalry/PaladinSpell.cs, Spells/Chivalry/RemoveCurse.cs (removes curses only), Spells/Mysticism/MysticSpell.cs, Spells/Mysticism/CleansingWindsSpell.cs, Spells/Spellweaving/ArcanistSpell.cs, Spells/Necromancy/LichForm.cs (--Hits flat), Spells/Bushido/*, Spells/Ninjitsu/* (other than guard above), Spells/Gargoyle/*, Spells/Fourth/ManaDrain.cs, Spells/Seventh/ManaVampire.cs, Skills/SpiritSpeak.cs, Skills/Discordance.cs (AOS live path), Mobiles/Familiars/*, Misc/AOS.cs (only the PvP SDI context; no Int/SDI cap here; GetValue :496-585 sums items with no cap; ours patches AOS-set-attribute-aggregation / AOS-pet-mimic-attribute-aggregation add more summed sources, no caps). Regex sweep over Spells/ for .Str/.Dex/.Int/Raw*/HitsMax/StamMax/ManaMax returned only the files listed above.

---------------------------------------------------------------------------------------------

## (a) Ranked runaways / brokens in MAGIC, worst first

1. Spell.cs:226 Int/10 spell damage bonus - runaway, uncapped except by the effective CAP, bypasses the PvP SDI 15 cap. At CAP 500: +27% PvP nuke damage over a 125 mage. At CAP 225: about +5%.
2. ManaMax = Int (+BonusMana) - runaway pool at CAP 500 (500+ mana vs ~150 at OSI). Mild at CAP 225.
3. ours Meditation.cs:83 absolute mana-deficit chance - broken/degenerate: large pools cannot start active meditation from low mana (Med 120 needs 355 mana of 500 to have any chance).
4. (watch) Bless/Curse vs CAP interaction: proportional formula is fine, but CAP 225 with raw 200 makes Bless near-worthless and curses absorbable.
Plateaus (no action needed): Mind Blast at Int 180; EvalInt message at 100.

## (b) Where a builder would put a soft cap

- UOContent/Spells/Base/Spell.cs:226 (PINNED; needs a new patch): e.g. intBonus = Math.Min(Caster.Int, 150) / 10 for players, or a soft curve. Single choke point for all 15 GetNewAosDamage callers.
- UOContent/Spells/Fifth/MindBlast.cs:43 (PINNED): already capped at 60; only touch if a lower ceiling is wanted.
- UOContent/Spells/Base/SpellHelper.cs:402-407 GetOffset (PINNED): Math.Min(target.RawX, 125) if buff/curse size should not scale past OSI.
- UOContent/Mobiles/PlayerMobile.cs:584-585 ManaMax (PINNED file, already carried by ours patches/PlayerMobile-individual-stat-cap.patch which edits :591/:606/:621 of the same file): cap or soften the Int contribution to mana.
- Global lever: ours customizations/ClusterFStatCaps.cs:10 (DefaultIndividualStatCap = 500) / :103, consumed by the PlayerMobile patch. Lowering this to 225 caps every row above at the eff225 column.
- ours customizations/Meditation.cs:83 (OURS): change deficit to a ratio.
- ours customizations/RegenRates.cs:148-150 (OURS): Int term if regen should be soft-capped (not needed today).

## (c) Could not verify

- Mismatched StatMod keys for talisman/quiver stat bonuses: AOS.cs:598 names mods with GetHashCode() but RemoveStatBonuses (AOS.cs:618-624) removes by Owner.Serial. No GetHashCode override found in AOS.cs (BaseAttributes is a partial class with source-generated members at AOS.cs:1347-1352, which I did not inspect). If no override exists, BonusInt/Str/Dex from talismans (Items/Talismans/BaseTalisman.cs:356, :379) and quivers (Items/Quivers/BaseQuiver.cs:206, :214) persist after unequip, an effective-stat inflation path that would feed every Int row above. Recommend a runtime test.
- Real endgame skill levels on this shard: Eval, Inscription, Meditation can apparently exceed 120 (ours Meditation.cs:92 gains to skill Cap). Eval scales GetNewAosDamage (Spell.cs:250-252) and buff/curse size (SpellHelper.cs:383-385) harder than Int does; outside stat scope but larger than any Int effect.
- Runtime value of ClusterFStatCaps (_enabled / configured cap) on the live server; I used 500 per the brief.
- Whether any shard customization item grants SpellDamage beyond normal ranges (PvM SDI is uncapped in pinned, Spell.cs:229-237).
