# s2-magic: per-skill scaling audit (cc-P20)

Skills: Magery, Evaluating Intelligence, Resisting Spells, Meditation, Inscription, Necromancy, Spirit Speak,
Chivalry, Spellweaving, Mysticism, Imbuing, Ninjitsu.

Paths for pinned code are relative to D:\UO\ModernUO-pinned\Projects. Shard files are under
D:\ShatteredLegacy\server\customizations (written "shard:"). Expansion = EJ (AOS/SE/ML/SA/HS/TOL all on).
Columns 120/300/500/1000 are the skill value (Skill.Value, includes item bonuses).

## Common facts used below

- Gain wrapper: shard ClusterFSkillGain.cs:97-150 re-runs the pinned handler up to 3 times and multiplies the
  gain amount by 5, but calls the pinned handler with the SAME min/max, so every gain ceiling below is unchanged by it.
- Spell.CheckFizzle (UOContent/Spells/Base/Spell.cs:614-629): if DamageSkill != CastSkill it also calls
  CheckSkill(DamageSkill, 0, DamageSkill.Cap) (:623-626). So the damage skill of every spell school gains up to its own cap.
  Magery -> EvalInt, Necromancy -> Spirit Speak, Mysticism -> EvalInt (see Mysticism: quirk).
- AOS spell damage, Spell.GetNewAosDamage (Spell.cs:218-258):
  dmg = dice * (100 + inscBonus + Int/10 + SDI [+ReaperForm]) % * (30 + 0.09*evalFixed) % * scalar.
  - inscBonus = (inscFixed + 1000*(inscFixed/1000))/200 (:222-223). Integer division makes the intended one-time
    "+5 at GM" repeat every 100 points: 120 -> 11, 300 -> 30, 500 -> 50, 1000 -> 100. (BaseWeapon.GetAosDamage
    Items/Weapons/BaseWeapon.cs:2253-2258 uses the correct insc/200 + 5 once.)
  - evalScale = 30 + 9*evalFixed/100 (:250-251): 120 -> 138 %, 300 -> 300 %, 500 -> 480 %, 1000 -> 930 %.
  - No final cap on spell damage anywhere in pinned. Only caps: SDI 15 in PvP (:232-236), Mind Blast 60
    (Fifth/MindBlast.cs:43), Wither has its cap commented out (Necromancy/Wither.cs:123-125).
  - Combined multiplier (Int 125, SDI 0, Eval = Insc = X): 120 -> 1.70x, 300 -> 4.26x, 500 -> 7.78x, 1000 -> 19.7x.
  - In AOS no damage spell rolls CheckResisted (the resist branches are all !Core.AOS), so Resisting Spells never
    reduces spell damage; only elemental resists (cap 70) do.
- Melee percentage damage bonus (move scalars, slayers etc) is capped at +300 % (BaseWeapon.cs:1874).
- Player resists: Mobile.MaxPlayerResistance = 70 (Server/Mobiles/Mobile.cs:431). Resist > 100 on a creature makes
  AOS.Damage go to the floor of 1 (UOContent/Misc/AOS.cs:144); damage <= 0 is ignored entirely (AOS.cs:52).
- Any damage clears Paralyzed (Server/Mobiles/Mobile.cs:5932), so long paralyzes break on the first hit.
- Negative timer delays are rounded up to one tick (Server/Timer/Timer.TimerWheel.cs:176-179), so negative
  durations below just mean "instant expiry" (harmless immunity).
- Reference numbers: player HP about 150, a typical 8th-circle cast cycle is about 3 s.

---

## Magery

Gain ceiling: 120.0 (8th circle from a book: min 80, max 120; scrolls max 92). Nothing else gains Magery.

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Cast success | Spells/Base/MagerySpell.cs:15-17, :41-42 | ML table min = -18/-4/10/24/38/52/66/80 per circle (book), max = min+40 | 100 % all circles | clamps (100 % from 120) | clamps | clamps | 120 (8th circle) |
| Resist% vs target (caster side) | MagerySpell.cs:88-97 | second% = R - ((Mag-20)/5 + 5(c+1)); n = max(R/5, second)/2 | scales | scales: lowers target resist toward floor R/10 | clamps at floor R/10 | clamps (floor R/10 can't be beaten) | n/a |
| Earthquake radius | Spells/Eighth/Earthquake.cs:41, :56-65 | radius 1 + Mag/15; dmg = target Hits/2 (+0..15), NPC clamp 15-100 | 9 tiles | 21 tiles (past the 18-tile client view) | 34 tiles | BREAKS: 67-tile radius, halves the current HP of every player/creature in LOS, mostly off-screen | 120 |
| Reveal radius | Spells/Sixth/Reveal.cs:32 | 1 + Mag/20 | 7 | 16 | 26 | BREAKS (minor): 51-tile radius reveal, far past view range | 120 |
| Heal (1st) | Spells/First/Heal.cs:50-56 | Mag/12 + 1..4, x1.5 on others | 11-14 (16-21) | 26-29 (39-44) | 42-45 (63-68) | BREAKS: 84-87 self, 126-131 on others for 4 mana, 0.5 s cast | 120 |
| Greater Heal | Spells/Fourth/GreaterHeal.cs:51-52 | 0.4*Mag + 1..10 | 49-58 | 121-130 (near full HP) | BREAKS: 201-210, every cast is a full heal | BREAKS: 401-410 | 120 |
| Cure / Arch Cure | Spells/Second/Cure.cs:33-34, Fourth/ArchCure.cs:74 | (10000 + 75*Mag - (L+1)*3100..3300)/100 % | lethal 90 % | clamps 100 % (lethal at >= 206.7) | clamps | clamps | 120 |
| Poison spell level | Spells/Third/Poison.cs:75-81 | Mag+Poisoning > 200 -> level 3 (10 % lethal at <=2 tiles, SA) | level 2-3 | clamps (max level 3/4 at Mag+Pois 200) | clamps | clamps | 120 |
| Mind Blast (AOS) | Fifth/MindBlast.cs:43 | min((Mag+Int)/5, 60) | 49 | clamps 60 (at Mag+Int 300) | clamps | clamps | 120 |
| Fire Field duration | Fourth/FireField.cs:47-51 | 4 + 0.5*Mag s | 64 s | 154 s | 254 s | 504 s (scales, griefing) | 120 |
| Poison Field duration | Fifth/PoisonField.cs:44-48 | 3 + 0.4*Mag s; level by Mag+Pois (:124) | 51 s | 123 s | 203 s | 403 s (scales) | 120 |
| Energy Field duration | Seventh/EnergyField.cs:44-46 | (15 + 2*Mag)/7 s | 36 s | 88 s | 145 s | BREAKS: 288 s impassable wall, recastable; doorway/bank/spawn blocking for ~5 min | 120 |
| Paralyze Field duration | Sixth/ParalyzeField.cs:44-48 | 3 + Mag/3 s (each touch: see EvalInt) | 43 s | 103 s | 170 s | BREAKS: 336 s field, combined with 1000 EI touch = 90 s (player) / 270 s (NPC) paralyze per touch | 120 |
| Summon durations (elementals, daemon, Summon Creature) | Eighth/AirElemental.cs:49 etc, Fifth/SummonCreature.cs:77 | 4*Mag s | 8 min | 20 min | 33 min | 67 min (scales; summon stats NOT scaled: every call passes scaleStats=false, Base/SpellHelper.cs:520-537 unused) | 120 |
| Invisibility duration | Sixth/Invisibility.cs:55 | 1.2*Mag s | 144 s | 360 s | 600 s | 1200 s (scales; ends on action) | 120 |
| Incognito | Fifth/Incognito.cs:113 | min(1.2*Mag, 144) s | clamps 144 | clamps | clamps | clamps | 120 |
| Dispel / Mass Dispel | Sixth/Dispel.cs:35-36, Seventh/MassDispel.cs:47 | (50 + 100*(Mag-DD)/(2*DF))/100 | scales | clamps 100 % vs every summon | clamps | clamps | 120 |
| Crafted spellbook props | Items/Skill Items/Magical/Spellbook.cs:168-210 | Magery BaseFixed tiers, top tier at 120 | clamps at 120 | clamps | clamps | clamps | n/a |
| Chivalry FC cap | Spells/Base/Spell.cs:704-708 | Magery >= 70 -> FC cap 2 | gate | gate | gate | gate | n/a |
| Polymorph | Seventh/Polymorph.cs:170-177 | ML: no timer | n/a | n/a | n/a | n/a | n/a |

recommendation: soft-cap the radius/duration/heal reads with diminishing returns: e.g. effectiveMag = 120 + 60*ln(1 + (Mag-120)/60) for Earthquake/Reveal radius, field durations and heals (300 -> ~200, 1000 -> ~260), and hard-cap Earthquake/Reveal radius at 18. Past 120 give new effects instead (e.g. reduced reagent use, FC/FCR breakpoints, extra field tiles) because cast success already clamps at 120 and Magery cannot be gained past 120 by casting.

## Evaluating Intelligence

Gain ceiling: Cap (CheckFizzle gains it up to its cap on every Magery cast, Spell.cs:623-626). Other gain uses: EvalInt skill use 120 (Skills/EvalInt.cs:75), stat buffs/curses 120 (Base/SpellHelper.cs:323, :370). So the effective ceiling is the skill cap (300 today, 1000 by design).

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| AOS spell damage | Spell.cs:250-253 | evalScale 30 + 0.09*fixed % | 138 % | 300 % | 480 % | 930 % | Cap |
| Energy Bolt (40+1d5) with Insc = Eval, Int 125 | Sixth/EnergyBolt.cs:38 + above | 43 * combined mult | 73 | 183 (55 vs 70 resist) | 334 (100 vs 70 resist) | BREAKS: 848, 254 after 70 resist = one-shot any player | Cap |
| Flame Strike (48+1d5) | Seventh/FlameStrike.cs:36 | 51 * mult | 87 | 217 (65) | 397 (119) | BREAKS: 1005 (301 after 70 resist) | Cap |
| Chain Lightning / Meteor / Hail Storm (51+1d5) | Seventh/ChainLightning.cs:59-71, MeteorSwarm.cs:62-75 | 54 * mult, x2/count if >2 targets | 92 | 230 | 420 | BREAKS: 1064 per target (1-2 targets), AoE | Cap |
| Stat buff % (Bless/Str/Agi/Cunning) | Base/SpellHelper.cs:382-391, :393-407 | 1 + EI/10 % of raw stat | 13 % | 31 % | 51 % | 101 % (doubles all 3 raw stats of any target incl. pets; scales but strong) | 120 |
| Stat curse % (Weaken/Clumsy/Feeble/Curse/Mass Curse) | SpellHelper.cs:384-385 | 8 + (EI - targetResist)/10 %, floor 0, NO cap | 8 % vs 120 R | 26 % vs 120 R | 46 % vs 120 R | BREAKS: 96 % vs 120 R: Str 125 -> 5 (HitsMax drops, overweight), Int -> 5 (no mana, cannot cast); Mass Curse does it in an area. Against a 0-resist NPC 108 % (stat clamps at 1, Server/Mobiles/Mobile.cs:1868) | 120 |
| Buff/curse duration | SpellHelper.cs:378-380 | 1.2*EI s | 144 s | 360 s | 600 s | 1200 s (scales) | 120 |
| Paralyze duration | Fifth/Paralyze.cs:42-55 | EI/10 - R/10 s, x3 vs NPC, floor 0 | 0 s vs 120 R | 18 s vs 120 R (60 s NPC R100) | 38 s (120 s NPC) | 88 s player / 270 s NPC (scales; broken by any damage, Mobile.cs:5932) | Cap |
| Paralyze Field per touch | Sixth/ParalyzeField.cs:149-160 | 2 + int(EI/10) - int(R/10), x3 NPC | 2 s | 20 s | 40 s | 90 s / 276 s (scales, see Magery field duration) | Cap |
| Mana Drain (AOS) | Fourth/ManaDrain.cs:41 | clamp(40 + EI - R, 0, mana), returned after 5 s | 40 | 220 (full pool) | clamps (full pool) | clamps | Cap |
| Mana Vampire (AOS) | Seventh/ManaVampire.cs:41-46 | EI - R (NPC /2), capped at target mana, permanent | 0 vs 120 R | 180 (full pool of a 120-R player) | clamps | clamps (relative to target resist; bounded by target mana) | Cap |
| Wrestling defense (Fists) | Items/Weapons/Fists.cs:54-56 | min((Anat+EI+20)/2, 120) | clamps 120 | clamps | clamps | clamps | n/a |
| EvalInt skill use | Skills/EvalInt.cs:55 | margin of error 20 - EI/5, floor 0 | clamps at 100 | clamps | clamps | clamps | 120 |

recommendation: soft-cap EvalInt's damage term: evalScale = 138 + 100*ln(1 + (EI-120)/100) (300 -> ~240 %, 1000 -> ~360 %) and cap the stat curse at about 25 % (OSI-like); keep stat buff linear but cap at 30-40 %. New effects past 120 (e.g. small spell penetration of resist, longer curse duration) are safer than raw damage.

## Resisting Spells (MagicResist)

Gain ceiling: 130 (Magery CheckResisted only gains while R < (1+c)*10 + (1+c/6)*25, 8th circle = 130, MagerySpell.cs:77-83; Mystic same :116-122; GetResistSkill gate 121, MagerySpell.cs:51-56; curses/necro use fixed 120: SpellHelper.cs:371, Necromancy/PainSpike.cs:59, MindRot.cs:58, CorpseSkin.cs:70, BloodOathSpell.cs:85). Above 130 Resist cannot be gained from spells.

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| AOS resist floor (all 5 elemental resists) | Mobiles/PlayerMobile.cs:1203-1222 | fixed>=1000: 40 + (fixed-1000)/50, clamp to MaxPlayerResistance 70 | 44 | clamps at 70 (reached at 250.0) | clamps | clamps | 130 |
| side effect of the floor | Server/Mobiles/Mobile.cs:3228-3246 + PlayerMobile.cs:1221, :1133-1136 | if max < min then max = min; floor clamps to the static 70, not the cursed max | n/a | at 250+: every resist is 70 with no gear; Curse (-10 max), Corpse Skin, Magic Reflect/Reactive Armor/Protection maluses and other resist debuffs become no-ops | same | same | |
| Resist chance vs Magery spells (AOS: Poison spell; also Mystic Bombard) | MagerySpell.cs:61-97, Third/Poison.cs:35 | n = max(R/5, R - ((CasterSkill-20)/5 + 5(c+1)))/2; n >= 1 -> always resisted | 42 % vs equal 120 caster (3rd) | BREAKS: equal 300 caster -> 114 % (8th circle: 102 %), i.e. immune at equal skill | BREAKS | BREAKS: floor R/10 = 100 % -> immune to every Magery/Mystic CheckResisted regardless of caster skill | 130 |
| Stat curse reduction | SpellHelper.cs:384-388 | 8 + (EI-R)/10 % floor 0 | 8 % vs 120 EI | 0 % (immune) vs EI < 220 | immune vs EI < 420 | immune vs EI < 920 (relative only) | 120 |
| Paralyze / Paralyze Field / Bombard paralyze | Fifth/Paralyze.cs:42, ParalyzeField.cs:152, Mysticism/BombardSpell.cs:70 | EI/10 - R/10 (Bombard: Imb-or-Focus/10 - R/10) | relative | immune vs casters below 300 | relative | relative | 130 |
| Spell Plague explosion chance | Mysticism/SpellPlagueSpell.cs:148-155 | 90 - 30*n - ((Rfixed-700)/100)*3 | 75 % first | 21 % first | BREAKS: 0 % (immune from R 370) | BREAKS: immune | 130 |
| Nether Cyclone drain reduction | Mysticism/NetherCycloneSpell.cs:81 | drain - R/800 | -15 % | -37.5 % | -62.5 % | -125 % (once the result is negative the victim GAINS stam/mana, see note) | 130 |
| Necro: Pain Spike | Necromancy/PainSpike.cs:58 | max((SS-R)/10 + 18 player/30 NPC, 1) | relative | relative | relative | floor 1 dmg vs SS 120 | 120 |
| Necro: Mind Rot / Corpse Skin / Blood Oath durations | MindRot.cs:57, CorpseSkin.cs:72, BloodOathSpell.cs:84 | (SS-R)/5+20, (SS-R)/2.5+40, (SS-R)/80+8 s | relative | negative durations vs SS 120 (instant expiry, harmless immunity) | same | same | 120 |
| Evil Omen | EvilOmen.cs:57 | halves Resist via skill mod | scales | scales | scales | scales | |
| Protection malus | Second/Protection.cs:139 | -35 + caster Insc/20 resist skill | see Inscription | | | | |
| Revenant/AnimatedWeapon get resist = caster skill | Mobiles/Monsters/AOS/Revenant.cs:19-27, AnimatedWeapon.cs:65 | see Spirit Speak / Mysticism | | | | | |

Note on Nether Cyclone at very high target Resist: resistedReduction = reduction - R/800 can go negative; m.Stam -= (int)(StamMax * negative) ADDS stamina/mana to the victim (NetherCycloneSpell.cs:81-84). With caster 120/120 vs R 300: 0.2 - 0.375 = -0.175 -> victim gains 17 % stam and mana per cast. BREAKS (sign flip) at R >= ~200 vs a 120/120 mystic; this is the Resist side of the same formula.

recommendation: replace the floor R/10 term and the second% term with a curve that never reaches 100 %, e.g. resist% = 50 * (R - casterSkill/2) / (R + 100), cap 75 %; give the resist floor a lower slope (e.g. 40 + (R-100)/10, still clamped 70, reaching cap at 400) and do NOT let the floor override curse/debuff maxima (clamp min to the current max, not the static 70). Clamp Nether Cyclone resistedReduction at 0. Past 130 Resist needs a gain source (none exists).

## Meditation (shard: Meditation.cs and RegenRates.cs replace pinned Skills/Meditation.cs and Misc/RegenRates.cs)

Diffs from pinned: Meditation.cs:46-59, :85-87, :92 (active gain max raised from 100 to the skill cap; armored meditation allowed above 200); RegenRates.cs:156-165 (armored medPoints kept at max(0.1, 1 - 0.02*armorOffset) when meditating above 200). Everything else in RegenRates is identical to pinned.

Gain ceiling: active use = skill Cap (shard Meditation.cs:92, chance = value/cap, true-no-gain at cap). Passive regen check = 200.0: CheckBonusSkill v = sqrt(S*0.005) (shard RegenRates.cs:35-41) reaches 1.0 at S = 200, so n >= 1 and the direct check returns true with no gain for every mana state. Same 200 ceiling for Focus (stam and mana regen checks).

Mana regen (shard RegenRates.cs:146-202), AOS: medPoints = (Int + 3*Med) * (Med < 100 ? 0.025 : 0.0275); meditating adds min(medPoints, 13); Focus adds 0.05*Focus; RegenMana items capped 18 (ML); floor(total); mana/s = 0.1*(2 + total).
Numbers below: Int 125, Focus 0, no items, unarmored.

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Passive mana regen | shard RegenRates.cs:148-150, :167, :202 | see above | 13 pts -> 1.5 mana/s (2.8 meditating) | 28 -> 3.0/s (4.3 med) | 44 -> 4.6/s (5.9 med) | BREAKS: 85 -> 8.7/s (10.0 med); with Focus 1000 and MR 18: 166 -> 16.8 mana/s, enough to chain-cast 8th circle with no mana limit (8th = 50 mana per ~3 s) and infinite Energy Bolts with LMC 40 even without meditating | 200 (passive), Cap (active) |
| Active meditate chance | shard Meditation.cs:83 | (50 + (Med - missingMana)*2)/100 | 90 % at 100 missing | clamps 100 % unless >275 mana missing | clamps | clamps | Cap |
| Armored meditation (shard) | shard Meditation.cs:50-59, :86-87; RegenRates.cs:161-164 | allowed only at Med > 200; chance and medPoints x max(0.1, 1 - 0.02*armorOffset) | blocked | allowed, penalised | allowed | allowed (medPoints 85.9 x penalty: with offset 25 -> x0.5 -> still 43 pts = 4.5 mana/s in plate) | n/a |
| Focus stam regen (not in my list, same file) | shard RegenRates.cs:95-128 | points = 0.1*Focus + capped 24 | 12 -> 1.4 stam/s | 30 -> 3.2/s | 50 -> 5.2/s | 100 -> 10.2/s (12.6 with items) | 200 |
| Focus mana regen | RegenRates.cs:152-154 | +0.05*Focus pts | +0.6/s | +1.5/s | +2.5/s | +5.0/s | 200 |

recommendation: soft-cap with diminishing returns: medPoints = 13.3 * (1 + ln(1 + (Med-120)/120)) above 120 (300 -> ~25, 1000 -> ~40 pts, i.e. 4.2 mana/s), and keep the meditating bonus capped at 13. Note the passive gain ceiling of 200 is below the shard's 300 cap: points 200-300 come only from active use.

## Inscription

Gain ceiling: 150.0 (Mystic Spellbook craft 50-150, Engines/Craft/DefInscription.cs:457; Spellbook 50-126 :439; 8th-circle scrolls 75-125 :173-174; Mystic 7th-circle scrolls 60.7-110.7; necro scrolls min..min+1). Crafting runs through the shard's CraftItem.cs (replaces pinned): shard CraftItem.cs:855-913 keeps CheckSkill(min, max) per craft skill, so the ceilings are unchanged; success chance > 1 above max is harmless.

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Spell damage bonus | Spell.cs:222-224 | (fixed + 1000*(fixed/1000))/200 % (bug: +5 per 100 skill) | +11 % | +30 % | +50 % | +100 % (scales; multiplies with Eval, see EvalInt BREAKS) | 150 |
| Weapon hit-spell damage bonus | Items/Weapons/BaseWeapon.cs:2247-2283 | fixed/200 + 5 (once) | +11 % | +20 % | +30 % | +55 % (scales) | 150 |
| Reactive Armor (AOS) | Spells/First/ReactiveArmor.cs:192-195 | phys +15 + Insc/20, elem -5 | +21 | +30 | +40 | +65 (clamps at player cap 70) | 150 |
| Magic Reflect (AOS) | Spells/Fifth/MagicReflect.cs:86-87 | phys -25 + Insc/20, elem +10 | -19 | -10 | 0 | BREAKS: +25 phys AND +10 all elem; the intended drawback inverts into a pure buff (limited by the 70 cap) | 150 |
| Protection (AOS) | Spells/Second/Protection.cs:138-145 | phys -15 + Insc/20; Resist skill -35 + Insc/20; disrupt immunity 100 % | -9 / -29 | 0 / -20 | BREAKS: +10 phys / -10 | BREAKS: +35 phys and +15 Resisting Spells, plus no spell disruption; only cost left is -2 FC | 150 |
| Runebook charges | Items/Skill Items/Magical/Runebook.cs:104 | min(5 + quality + Insc/30, 10) | clamps 10 | clamps | clamps | clamps | n/a |
| Slayer spellbook | Spellbook.cs:168-210; Spell.cs:328-373 | slayer from crafted props (reads Magery, not Inscription); x2 damage | n/a | n/a | n/a | n/a | n/a |
| Scroll crafting success | shard CraftItem.cs:898-905 | (Insc - min)/(max - min) | 100 % all magery scrolls | clamps | clamps | clamps | 150 |

recommendation: fix the inscBonus integer bug (use fixed/200 + (fixed >= 1000 ? 5 : 0)) and soft-cap it (e.g. 10 + 10*ln(1 + (Insc-100)/100)); clamp the Magic Reflect and Protection maluses at 0 (they should never turn into bonuses). New effects past 150: scroll quality tiers or reduced mana on scribed scrolls.

## Necromancy

Gain ceiling: 120.0 (Exorcism / Vengeful Spirit RequiredSkill 80 + 40, NecromancerSpell.cs:37-41; Vampiric Embrace override 80-120, VampiricEmbrace.cs:32-42). Necromancy itself only gates spells; spell power is Spirit Speak (DamageSkill, NecromancerSpell.cs:15).

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Cast success | NecromancerSpell.cs:37-41 | min = req, max = req+40 | 100 % all | clamps | clamps | clamps | 120 |
| Animate Dead ability | Necromancy/AnimateDeadSpell.cs:313-317 | (30*Necro + 70*SS)/10*18, clamp to corpse Fame | ~21600 | clamps at corpse fame | clamps | clamps | 120 |
| Summon Familiar gates | SummonFamiliar.cs:140-148 | Necro/SS thresholds | clamps | clamps | clamps | clamps | n/a |
| Dispel Evil drain (target side) | Chivalry/DispelEvil.cs:105 | 0.5*Chiv/max(Necro,1) | relative | relative | relative | relative | n/a |
| Forms (Lich, Wraith, Vampiric, Horrific Beast) | LichForm.cs, VampiricEmbrace.cs, HorrificBeast.cs | fixed offsets; only Wraith reads SS (see Spirit Speak) | n/a | n/a | n/a | n/a | |
| Karma loss per cast | NecromancerSpell.cs:22-35 | fixed by cast time | n/a | | | | |

recommendation: Necromancy itself clamps at 120 harmlessly; give it new effects past 120 (e.g. extra Animate Dead slot, form bonuses scaling with (Necro-120)) rather than scaling, because Spirit Speak is where the runaway is.

## Spirit Speak

Gain ceiling: Cap (necro casting gains it via CheckFizzle, Spell.cs:623-626). Other uses: ghost listening 100 (Skills/SpiritSpeak.cs:32), self-heal 120 (:159).

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Spirit Speak heal | Skills/SpiritSpeak.cs:137-138, :159-176 | 1 + 0.25*SS .. +4 hits, 10 mana or free with a corpse, ~1 s cast | 31-35 | 76-80 (strong) | BREAKS: 126-130 (full heal) | BREAKS: 251-255 per ~1-2 s, free near corpses | 120 |
| Pain Spike | Necromancy/PainSpike.cs:58, :78-80, :105-113 | (SS-R)/10 + 18 (player) / 30 (NPC), raw damage ignoring resists, restored after 10 s, leeches | 18 vs R120 | 36 | 56 | BREAKS: 106 unresistable vs R120 player, 120 vs NPC R100, for 5 mana and a 1 s cast | Cap |
| Poison Strike | PoisonStrike.cs:61 | 32-40 * (300 + 9*SS)/1000 * SDI | ~50 | ~108 | ~173 | BREAKS: ~335 pre-resist (100 after 70 poison resist) | Cap |
| Wither (AoE cold) | Wither.cs:106-118 | 30-35 * (300 + Karma/100 + 10*SS)/1000, cap commented out | ~44 (vs -15000 karma) | ~102 | ~167 | BREAKS: ~330 AoE pre-resist | Cap |
| Strangle | Strangle.cs:86-95, :139-147, :186-200 | ticks = max(4, SS/10)-1; per tick (SS/10 -2..+1) * (3 - 2*stam%), x1.75 NPC; duration 3*SS/10 + 5 s; poison type | 11 ticks x 11.5 = ~127 over 41 s | ~856 over 95 s (7x baseline, quadratic) | BREAKS: ~2400 over 155 s, 50-150/tick | BREAKS: ~9850 over 305 s, 100-300 per tick (x1.75 NPC) | Cap |
| Mind Rot duration | MindRot.cs:57 | ((SS-R)/5 + 20) s, x2 NPC | 20 s | 56 s | 96 s | 196 s player / 392 s NPC (scales) | Cap |
| Blood Oath duration | BloodOathSpell.cs:84 | (SS-R)/80 + 8 s | 8 s | 10 s | 13 s | 19 s (scales) | Cap |
| Corpse Skin duration | CorpseSkin.cs:72 | (SS-R)/2.5 + 40 s | 40 s | 112 s | 192 s | 392 s (scales; resist mods nullified by the Resist floor on 250+ R players) | Cap |
| Evil Omen duration | EvilOmen.cs:62 | SS/12 + 1 s | 11 s | 26 s | 43 s | 84 s (scales) | Cap |
| Curse Weapon duration | CurseWeapon.cs:51 | SS/3.4 + 1 s (50 % life leech) | 36 s | 89 s | 148 s | 295 s (scales) | Cap |
| Wraith Form mana leech | WraithForm.cs:37-38 | 5 + 15*SS/100 % of melee damage dealt, capped by target mana | 23 % | 50 % | 80 % | BREAKS: 155 %, leeches more mana than damage dealt | Cap |
| Vengeful Spirit (Revenant) | VengefulSpirit.cs:49; Mobiles/Monsters/AOS/Revenant.cs:19-45 | duration SS*2/3 + 10 s; Resist/Swords = SS; resists 40+20*(SS/120)..50+... | 76 s, 60-70 resists | 210 s, phys/cold/energy 90-100 | BREAKS: 343 s, phys/cold/energy 123-133 % -> only 1 damage per hit (AOS.cs:144), Swords 500 | BREAKS: 677 s, resists 206-216 %, Swords/Resist 1000; effectively unkillable hunter | Cap |
| Ghost listening duration | SpiritSpeak.cs:37-39 | Base/50*90 s | 216 s | 540 s | 900 s | 1800 s (harmless) | 100 |
| Exorcism gate | Exorcism.cs:74 | SS >= 100 | gate | gate | gate | gate | |

recommendation: soft-cap Spirit Speak as a power stat: effSS = 120 + 80*ln(1 + (SS-120)/80) (300 -> ~200, 1000 -> ~290) for all damage/heal/leech formulas; hard-cap Wraith leech at 30-40 %, Pain Spike at about 40, Strangle tick count at 12 and per-tick power at 15, Revenant resists at 70 and skill at 120.

## Chivalry

Gain ceiling: 115.0 (RequiredSkill + 50, Noble Sacrifice req 65, PaladinSpell.cs:126-130; DamageSkill == CastSkill so no extra gain). Note the HS Divine Fury upgrade needs Chivalry >= 120 (DivineFury.cs:46), which cannot be reached by casting.

Power value = sqrt(Karma + 20000 + 100*Chiv) (PaladinSpell.cs:136-146). With Karma 15000: 120 -> 216, 300 -> 254, 500 -> 291, 1000 -> 367 (sqrt growth, already soft).

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Cast success | PaladinSpell.cs:126-130 | min = req, max = req+50 | 100 % | clamps | clamps | clamps | 115 |
| Close Wounds | CloseWounds.cs:65 | clamp(power/6 + 0..2, 7, 39) | 36-38 | clamps 39 (at ~143-198) | clamps | clamps | 115 |
| Consecrate Weapon duration | ConsecrateWeapon.cs:91 | clamp(power/20, 3, 11) s | 10 s | clamps 11 (at ~134) | clamps | clamps | 115 |
| Divine Fury duration | DivineFury.cs:44-48 | clamp(power/10, 7, 24) s; HS boost at Chiv>=120 and Karma>=10000 (15/20/15/10 vs 10/10/10/20) | 21 s, boost | clamps 24 (at ~226) | clamps | clamps | 115 |
| Enemy of One duration | EnemyOfOne.cs:42 | clamp(power/60, 1.5, 3.5) min | clamps 3.5 | clamps | clamps | clamps | 115 |
| Holy Light | HolyLight.cs:74 | clamp(power/10 + 0..2, 8, 24) | 21-23 | clamps 24 | clamps | clamps | 115 |
| Noble Sacrifice heal | NobleSacrifice.cs:102 | clamp(power/10 + 0..2, 8, 24) | 21-23 | clamps 24 | clamps | clamps | 115 |
| Cleanse by Fire cure / self-damage | CleanseByFire.cs:51, :97 | (10000 + 75*Chiv - (L+1)*2000)/100 %; self dmg clamp(50 - power/4, 13, 55) | lethal 90 %; 13 dmg | clamps 100 % (lethal at 133.3) | clamps | clamps | 115 |
| Dispel Evil: dispel summons | DispelEvil.cs:45, :65-66 | (50 + 100*(Chiv-DD)/(2*DF))/100 * power/200 | partial | clamps 100 % vs every summon in 8 tiles | clamps | clamps | 115 |
| Dispel Evil: flee | DispelEvil.cs:90-91 | (100 - sqrt(Fame/2)) * Chiv * power/2 / 1e6 | 17 % (fame 15000) | 51 % | 97 % | clamps 100 % | 115 |
| Dispel Evil: drain transformed necros | DispelEvil.cs:105-110 | 0.5*Chiv/Necro; drain 5*power/2/100 | relative | relative | relative | relative | 115 |

recommendation: Chivalry already clamps almost everywhere by 120-230 (harmless; points past ~230 are wasted). Let it scale nowhere new; give new effects past 120 instead (e.g. tithing cost reduction, extra Close Wounds cap, Consecrate damage bonus), and make 120 reachable by casting (raise the gain max) if the HS Divine Fury tier should be earnable.

## Spellweaving

Gain ceiling: 117.5 (Word of Death req 80 + 37.5, ArcanistSpell.cs:85-89). DamageSkill == CastSkill. Wildfire is NOT implemented in pinned (no WildfireSpell; only a ConPVP option name, Engines/ConPVP/RulesetLayout.cs:255) - unverified on the shard side, nothing in customizations.

Focus level (Arcane Focus strength) comes from the number of arcanists in the circle, not from skill (ArcaneCircle.cs:55-56). Arcane Circle only accepts arcanists within 20 skill of the caster (ArcaneCircle.cs:113-117): a 300+ weaver can no longer circle with 120 players (side effect).

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Cast success | ArcanistSpell.cs:85-89 | min = req-12.5, max = req+37.5 | 100 % | clamps | clamps | clamps | 117.5 |
| Resist check | ArcanistSpell.cs:127-139 | (50 + 2*(R - SW))/100 | 50 % at equal | relative (0 % vs R <= SW-25) | relative | relative | |
| Arcane Circle focus duration | ArcaneCircle.cs:50-53 | max(1, SW/24) hours | 5 h | 12 h | 20 h | 41 h (harmless) | 117.5 |
| Arcane Summon duration | ArcaneSummon.cs:35-36 | SW/24 + 2F min | 5 min | 12 min | 20 min | 41 min (scales) | 117.5 |
| Attune Weapon absorb | AttuneWeapon.cs:53-58 | 18 + 3*(SW-10)/10 + 6F melee damage absorbed, 60+12F s, recast after expiry | 51 | 105 | 165 (more than a player's HP) | BREAKS: 315-351 absorb pool (2x player HP) every ~60 s | 117.5 |
| Essence of Wind duration | EssenceOfWind.cs:34 | SW/24 + F s (damage fixed 25+F) | 5 s | 12 s | 20 s | 41 s (scales) | 117.5 |
| Ethereal Voyage | EtherealVoyage.cs:69 | 12 + SW/24 + 2F s | 17 s | 24 s | 32 s | 53 s (scales; 5 min cooldown) | 117.5 |
| Gift of Life hits on res | GiftOfLife.cs:30, :64; Gumps/ResurrectGump.cs:268-270 | (SW/2.4 + F)% of HitsMax; duration (SW/24)*2 + F min | 50 % | clamps 100 % (at 240) | clamps | clamps; duration 82 min | 117.5 |
| Gift of Renewal | GiftOfRenewal.cs:53-54 | 5 + SW/24 + F hits per 2 s for 30+10F s, 60 s cooldown | 10/2 s (150 total) | 17/2 s (255) | 25/2 s (375) | BREAKS: 46/2 s = 23 HP/s, 690 HP per cast (52/tick for 90 s at F6 = 2340) | 117.5 |
| Immolating Weapon | ImmolatingWeapon.cs:52-53 | dmg 5 + SW/24 + F fire per hit, 10 + SW/24 + F s | 10 dmg / 15 s | 17 / 22 s | 25 / 30 s | 46 fire per hit / 51 s (scales; 14 after 70 resist) | 117.5 |
| Nature's Fury duration | NatureFury.cs:46 | SW/24 + 25 + 2F s | 30 s | 37 s | 45 s | 66 s (scales) | 117.5 |
| Thunderstorm | Thunderstorm.cs:36 | max(11, 10 + SW/24) + F energy AoE | 15 | 22 | 30 | 51 (scales) | 117.5 |
| Word of Death | WordOfDeath.cs:46-66 | SW/5..SW/3 chaos (+SDI, 15 PvP); 300 flat if NPC below 5F % HP | 24-40 | 60-100 | 100-166 | 200-333 (scales, 60-100 vs 70-resist player) | 117.5 |
| Reaper Form | ReaperForm.cs:24-30 | focus only | n/a | | | | |

recommendation: soft-cap the SW/24 terms (e.g. 5 + 5*ln(1 + (SW-120)/120) beyond 120) and hard-cap Attune Weapon absorb at about 60 and Gift of Renewal per-tick at about 15. Widen or remove the +-20 skill window on Arcane Circle so high-skill weavers can still form circles.

## Mysticism

Implemented in pinned: Animated Weapon, Bombard, Cleansing Winds, Eagle Strike, Hail Storm, Nether Cyclone, Spell Plague, Stone Form (Spells/Mysticism). NOT implemented: Nether Bolt, Healing Stone, Purge Magic, Enchant (Mystic Weapon), Sleep, Mass Sleep, Spell Trigger, Rising Colossus (only scroll items exist, e.g. Items/Skill Items/Magical/Scrolls/Mysticism/MassSleepScroll.cs). So "Sleep" and "Mystic weapon" have no formulas to audit (unverified on the shard: nothing in customizations).

Gain ceiling: 120.5 (8th circle req 83 + 37.5, MysticSpell.cs:9, :46-54).
Quirk: MysticSpell overrides GetDamageSkill/GetDamageFixed to max(Imbuing, Focus) (MysticSpell.cs:42-44) but not the DamageSkill property, which stays EvalInt (Spell.cs:52). CheckFizzle therefore gains EvalInt, not Imbuing/Focus, on every Mystic cast (Spell.cs:623-626). Damage scales with Imbuing/Focus through GetNewAosDamage.
Below, M = Mysticism, I = max(Imbuing, Focus), shown as M = I = X.

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Cast success | MysticSpell.cs:46-54 | min = req-12.5, max = req+37.5 | 100 % | clamps | clamps | clamps | 120.5 |
| Spell damage (Hail Storm / Nether Cyclone 51+1d5, Bombard 40+1d5, Spell Plague, Eagle Strike) | HailStormSpell.cs:62, NetherCycloneSpell.cs:72, BombardSpell.cs:58, SpellPlagueSpell.cs:57/161, EagleStrikeSpell.cs:68 | GetNewAosDamage with I as eval | Hail 92 | 230 | 420 | BREAKS: Hail/Cyclone ~1064 AoE, Bombard ~848 | n/a (casting gains EvalInt, not I) |
| Resist% vs target (caster side) | MysticSpell.cs:127-136 | as Magery with M | | | | | |
| Bombard paralyze | BombardSpell.cs:67-75 | I/10 - R/10 s (no NPC x3) | relative | 18 s vs R120 | 38 s | 88 s (scales, breaks on damage) | |
| Bombard knockback | BombardSpell.cs:78-82 | (M + I - R)/20 used as a probability | already >= 1 at 120 (pinned bug: comment says 12 %) | always | always | always | |
| Nether Cyclone stam/mana drain | NetherCycloneSpell.cs:73-84 | (M+I)/1200 - R/800 of max stam and mana | 5 % vs R120 | 35 % | 68 % | BREAKS: 152 % -> wipes all stamina and mana of every target in the AoE (stam 0 = cannot move); negative values ADD stam/mana (see Resist) | 120.5 |
| Cleansing Winds heal | CleansingWindsSpell.cs:46-69 | ((M+I)/4 +-3)/targets, also cures/removes curses | 60 | 150 (full heal, single target) | BREAKS: 250 single / 62 each on 4 | BREAKS: 500 single / 125 each on 4 | 120.5 |
| Stone Form resist bonus | StoneFormSpell.cs:98-110 | +(M+I)/24 all resists | +10 | +25 | +41 | +83 (clamps at 70 cap); damageBonus and resistCap (:119-120) are only shown in the buff, never applied | 120.5 |
| Animated Weapon | AnimatedWeaponSpell.cs:43-45; Mobiles/Monsters/Misc/Melee/AnimatedWeapon.cs:14-66 | level (M+I)/2: Str/Dex 10+level, Hits 20+1.5*level, Wrestling and Resist = level, duration 10+level s; damage caps at 14-18 (level 120) | 200 HP, 130 s | 470 HP, 310 s | 770 HP, wrestling 500 | BREAKS: 1520 HP, Wrestling/Resist 1000 (attackers hit it ~10 % of the time), 17 min | 120.5 |
| Spell Plague | SpellPlagueSpell.cs:148-161 | damage via GetNewAosDamage | scales | scales | scales | as damage row | |

recommendation: same damage soft-cap as EvalInt applied to I; clamp Nether Cyclone drain to [0, 0.5]; cap Cleansing Winds heal (e.g. 60 + 20*ln(1+(X-120)/60)); cap Animated Weapon level at 120 and give extra weapons (count) instead. Fix DamageSkill so Imbuing/Focus gain from Mystic casting (or document that EvalInt gains instead).

## Imbuing (shard system; pinned ModernUO has no Imbuing crafting: SkillName.Imbuing is read only by MysticSpell.cs:42-44 and UI/tables)

Gain ceiling: 140.0 (imbue check CheckSkill(diff-20, diff+20) with diff max 120 at intensity cap 200 %, shard ArtificersImbueGump.cs:85-92, :1406; disenchant/craft essence 20-80, :1478, :1533).

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Imbue success | shard ArtificersImbueGump.cs:1406, :1661-1665 | (I - (diff-20))/40, diff = 40 + (maxDiff-40)*fraction, maxDiff 100..120 | 100 % up to diff 100 (max standing: 80 %) | clamps 100 % (from 140) | clamps | clamps | 140 |
| Intensity limits / property slots | shard ArtificersImbueGump.cs:53-60, :1667-1683 | by guild standing only (100-200 %, 5-8 slots) | n/a (not skill based) | n/a | n/a | n/a | |
| Mysticism damage skill | MysticSpell.cs:42-44 | see Mysticism | 138 % | 300 % | 480 % | BREAKS via Mysticism damage (930 % eval-equivalent) | |
| Failure item damage | shard ArtificersImbueGump.cs:1411-1412 | -10 durability | | | | | |

recommendation: imbuing success clamps harmlessly at 140; points past 140 only feed Mysticism damage. Either soft-cap the Mysticism read (see Mysticism) or give Imbuing new effects past 140 (e.g. cheaper shards, small intensity bonus within guild caps). Raise the imbue gain max if 300 should be reachable by imbuing.

## Ninjitsu

Gain ceiling: 137.5 (Animal Form Kirin/Unicorn req 100 + 37.5, Spells/Ninjitsu/AnimalForm.cs:49-50, :186). Death Strike 122.5 (NinjaMove.cs:9 with req 85). Mirror Image/ShadowJump lower.

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Animal Form Dog/Cat hits regen (shard RegenRates.cs is a copy of pinned here) | shard RegenRates.cs:80-85; pinned Misc/RegenRates.cs:82 | +N/3 regen points, added AFTER the ML cap of 18; HP/s = (1+points)/10 | +40 -> 4.1 HP/s | +100 -> 10.1 HP/s | BREAKS: +166 -> 16.7 HP/s | BREAKS: +333 -> 33.4 HP/s (full heal of 150 HP in 4.5 s) | 137.5 |
| Animal Form success | AnimalForm.cs:186-204 | req..req+37.5 | 100 % all forms | clamps | clamps | clamps | 137.5 |
| Death Strike hit chance | DeathStrike.cs:35-39 | 63 + 1.1*(N-100) % | 85 % | clamps 100 % (at 133.6) | clamps | clamps | 122.5 |
| Death Strike damage (ML) | DeathStrike.cs:128-137, :56 | min(60, N/3*(0.3+0.7*hide/stealth)) direct; repeat bonus N/15 unused in ML | 40 | clamps 60 (at 180) | clamps | clamps | 122.5 |
| Focus Attack damage | FocusAttack.cs:35-38; BaseWeapon.cs:1794, :1874 | +N^2/43636 (x100 %), total bonus cap +300 % | +33 % | +206 % | clamps +300 % (at 362) | clamps | 137.5 |
| Focus Attack property bonus | FocusAttack.cs:42-49; BaseWeapon.cs:2023-2046 | 1 + 3*N^2/43636 multiplies hit-leech/hit-effect chance | x2.0 | x7.2 (any leech -> 100 %) | clamps | clamps | 137.5 |
| Backstab | Backstab.cs:16-21 | +N/360 (+stalking), inside +300 % cap | +33 % | +83 % | +139 % | +278 % (scales up to the 300 cap) | 137.5 |
| Surprise Attack defense malus | SurpriseAttack.cs:57-59; BaseWeapon.cs:1327-1362 | malus = fixed/60 DCI on target for 8 s; their = (defSkill+20)*(100 + DCI - malus) | -20 | -50 | -83 (auto-hit) | BREAKS: -166: their value goes NEGATIVE so hit chance floors at 2 % for EVERY attacker (sign inversion); at exactly DCI-malus = -100 it divides by zero (infinite chance, auto-hit). Threshold: N >= ~600 + 0.6*DCI | 137.5 |
| Mirror Image absorb / duration | BaseWeapon.cs:1747; MirrorImage.cs:171 | N/150 absorb chance; 30 + N/4 s | 80 % / 60 s | clamps 100 % (at 150) / 105 s | clamps / 155 s | clamps / 280 s | 137.5 |
| Dual Wield SSI (weapon ability, Ninjitsu secondary) | Items/Weapons/Abilities/DualWield.cs:36-39; BaseWeapon.cs:1394-1421 | 20 + 3*(N-50)/7 %, SSI cap 60 | 50 % | clamps 60 (at 143) | clamps | clamps | n/a |
| Feint (max of Ninjitsu/Bushido) | Feint.cs:35-41; BaseWeapon.cs:1994-1997; Misc/AOS.cs:52 | damage reduction 20 + 3*(S-50)/7 % for 6 s | 50 % | BREAKS: 127 % -> damage <= 0 -> AOS.Damage ignores it: total melee immunity from the feinted target (from S 236.7) | BREAKS | BREAKS: 427 % | n/a |
| Block DCI bonus (max Bushido/Ninjitsu) | Block.cs:30-34; BaseWeapon.cs:1343 | 10*((S-50)/70 + 5) (= 50 + 10*(S-50)/70), DCI cap 45 | clamps 45 | clamps | clamps | clamps | n/a |
| Defense Mastery phys | DefenseMastery.cs:30-37 | 50 + 30*(S-50)/70 phys resist mod | 80 -> clamps 70 | clamps | clamps | clamps | n/a |
| Talon Strike DoT | TalonStrike.cs:36 | 10*(N-50)/70 + 5 | 15 | 40 | 69 | 140 (scales) | n/a |
| Frenzied Whirlwind DoT per adjacent target | FrenziedWhirlwind.cs:35-39 | 10*((S-50)/70 + 5) (comment says 5-15, code gives 50-60 at 50-120) | 60 | 85 | 114 | 185 (scales; AoE) | n/a |
| Shadowjump / Ki Attack | ShadowJump.cs, KiAttack.cs:93-103 | gate only / distance only | n/a | | | | |
| Animal form gump gate | AnimalForm.cs:389-394 | compares Ninjitsu Fixed (x10) to ReqSkill: always passes (display bug, harmless; real gate at :178) | | | | | |

recommendation: clamp Surprise Attack malus to (100 + DCI - 1) or a flat 40, clamp Feint reduction at about 50-60 %, cap the Dog/Cat regen term (e.g. min(N/3, 40) or include it under the 18 cap). Focus Attack and Death Strike already clamp; give new effects past ~140 (e.g. extra mirror image, shorter Shadowjump stealth requirement) instead.

---

## BREAKS summary

1. EvalInt (and Inscription bonus) spell damage: no cap, x19.7 at 1000/1000; Energy Bolt 848, Flame Strike 1005, Chain Lightning/Meteor ~1064 pre-resist: one-shot through 70 resists (Spell.cs:218-258). Same path breaks Mysticism via Imbuing/Focus.
2. EvalInt stat curse: 8 + (EI-R)/10 % with no cap: 96 % at EI 1000 vs R 120 (Str/Int to ~5, Mass Curse AoE) (SpellHelper.cs:384-385).
3. Resisting Spells: equal-skill 300 vs 300 = always resisted (immunity) for Poison spell/8th-circle checks; R 1000 = immune to every Magery/Mystic CheckResisted regardless of caster (MagerySpell.cs:88-97).
4. Resisting Spells: Spell Plague immunity from R 370 (SpellPlagueSpell.cs:150-155); Nether Cyclone drain turns into a stam/mana GAIN when R/800 > caster term (NetherCycloneSpell.cs:81-84).
5. Magery: Earthquake radius 1 + Mag/15 = 67 tiles at 1000 (halves HP of everything in LOS); Reveal 51 tiles; Energy Field 288 s walls; Paralyze Field 336 s.
6. Magery heals: Greater Heal 201-210 at 500 and 401-410 at 1000 (full heal every cast); Heal 126-131 on others at 1000.
7. Meditation (shard RegenRates.cs): 8.7 mana/s at 1000 (16.8 with Focus 1000 and items) = mana no longer limits casting.
8. Inscription: Magic Reflect phys malus inverts to +25 at 1000; Protection inverts to +10 phys at 500 and +35 phys / +15 Resist at 1000 (MagicReflect.cs:86, Protection.cs:138-139).
9. Spirit Speak: SS heal 126-130 (500) / 251-255 (1000); Pain Spike 106 unresistable at 1000; Poison Strike and Wither ~335 pre-resist; Strangle quadratic (~2400 at 500, ~9850 at 1000); Wraith leech 155 %; Revenant resists > 100 % (immune) from SS 500.
10. Spellweaving: Attune Weapon absorb 315+ at 1000; Gift of Renewal 23 HP/s at 1000.
11. Mysticism: Nether Cyclone 152 % full stam/mana wipe at 1000/1000; Cleansing Winds 250/500 heal; Animated Weapon 1520 HP with Wrestling 1000.
12. Ninjitsu: Dog/Cat regen bypasses the 18 cap: 16.7 HP/s (500), 33 HP/s (1000); Surprise Attack malus > 100 + DCI inverts hit chance to 2 % (and divides by zero at exactly -100); Feint (Ninjitsu or Bushido) >= 236.7 = 100 %+ melee immunity.

Gain ceilings: Magery 120, EvalInt Cap, Resist 130, Meditation Cap active / 200 passive, Inscription 150, Necromancy 120, Spirit Speak Cap, Chivalry 115, Spellweaving 117.5, Mysticism 120.5, Imbuing 140 (shard), Ninjitsu 137.5. Points above these come only from other skills' casts, bonuses or admin edits.
