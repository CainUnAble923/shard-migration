# cc-P20 skill audit, slice s2: animal + bard + misc skills

Skills: Animal Taming, Animal Lore, Herding, Musicianship, Peacemaking, Provocation, Discordance,
Tracking, Item Identification, Taste Identification, Camping, Cartography.

Paths are relative to D:\UO\ModernUO-pinned\Projects unless prefixed "shard:" (= D:\ShatteredLegacy\server).
Expansion assumed Endless Journey (AOS/SE/ML/SA/HS/TOL true). Values are Skill.Value (includes mods).
Gain rules: SkillCheck.cs:53-61 / :161-169 (value >= maxSkill -> true, no gain roll), :84-87 / :190-193
(direct chance >= 1.0 -> true, no gain).

Shard overrides touching these skills (grep of shard:customizations and shard:patches):
- None of the shard files replaces AnimalTaming.cs, AnimalLore.cs, BaseInstrument.cs, Peacemaking.cs,
  Provocation.cs, Discordance.cs, Tracking.cs, ItemIdentification.cs, TasteID.cs, Kindling.cs, TreasureMap.cs,
  BaseCreature.GetControlChance, AnimalTrainer.GetMaxStabled or Bandage heal math. Pinned behavior applies.
- shard:customizations/OutridersCrook.cs:82-85 adds +5/+10/+15 Taming, +5/+10/+15 Peacemaking, +10 Lore as
  DefaultSkillMod (relative). SkillMod._obeyCap defaults false (Server/Mobiles/Mods/SkillMod.cs:25,57), so these
  go past the skill cap. Raises effective Value; does not change any formula.
- shard:customizations/ClusterFRangersSystem.cs:53 HasPeacefulTaming() says it is "called from the AnimalTaming
  patch", but no AnimalTaming patch exists in shard:patches and nothing calls it (grep). Subdue bypass is
  unwired (unverified whether a build-time hook exists elsewhere).
- shard:customizations/Mobiles/Normal/Raptor.cs:50 MinTameSkill 107.1 (highest tame difficulty on the shard;
  pinned max is 106.0). Dimetrosaur/Najasaurus/Saurosaurus 102.0.
- shard:customizations/ClusterFWorkOrderSystem.cs:151,183 work-order gates (Taming/Lore/Tracking >= minSkill).
  ClusterFGuildSystem.cs:161 Musicianship 30 gate. Pure gates: clamp, harmless.
- Item bonuses: MarkOfTravesty (+10 bard/tamer), CollectionsBritLibraryTalismans (+5), LegendaryMapmakersGlasses
  (+1..5 Cartography). Only raise Value.
- Cartography crafting goes through shard:customizations/CraftItem.cs (replaces pinned) GetSuccessChance
  (CraftItem.cs:877-895): generic min/max craft check; not re-audited here.

---------------------------------------------------------------------------------------------------------------

## Animal Taming

Taming rule (UOContent/Skills/AnimalTaming.cs):
- Hard gate ("too difficult" / "You have no chance"): Value < MinTameSkill -> refused (:185). Not owner-adjusted.
- Final roll (:397-407): minSkill = MTS + 6*Owners + 24.9; CheckTargetSkill(Taming, min-25, min+25)
  => range [MTS + 6*Owners - 0.1, MTS + 6*Owners + 49.9]; chance = (V - MTS - 6*Owners + 0.1) / 50.
  Owners < MaxOwners=5 (BaseCreature.cs:159), so a new tamer faces up to +24.
- CanAngerOnTame creatures: 95% anger roll before taming (:209), independent of skill.

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Tame gate | AnimalTaming.cs:185 | V >= MTS | clamps (all tamable at 107.1) | clamps | clamps | clamps | n/a |
| Tame roll | AnimalTaming.cs:397-407 | (V-MTS-6*Own+0.1)/50 | scales: MTS 106 fresh = 28.2%; MTS 95.1 = 50% | clamps: 100% vs everything (needs V >= 157.0 fresh / 181.0 with 4 prior owners on Raptor) | clamps 100% | clamps 100% | 157.0 (Raptor 107.1, fresh); 181.0 (Raptor, 4 owners); pinned 155.9/179.9 |
| Control chance | Mobiles/BaseCreature.cs:1408-1474 | ML: bonus = 3*(T10+L10-2*MTS10) (tenths), chance = clamp(700+bonus,220,990) - (MaxLoyalty-Loyalty)*10, /1000 | clamps: 99% once T+L >= 2*MTS+9.7 (MTS 106: T+L >= 221.7) | clamps 99% | clamps 99% | clamps 99% | n/a (no skill check) |
| Bonding req | BaseCreature.cs:4304-4306 | Value >= MTS | clamps | clamps | clamps | clamps | n/a |
| Stable slots | Mobiles/Vendors/NPC/AnimalTrainer.cs:58-97 | 2..5 by T+L+V sum, + (int)((S-90)/10) per skill >=100 | scales: all three 120 -> 14 | 68 | 128 | 278 | n/a |
| Passive AnimalLore gain during taming | AnimalTaming.cs:373,394 | Lore 0-120 | see Lore | | | | |

Notes:
- 100% taming at ~157+ is the normal "overskilled tamer" state; no exploit beyond the fact that Taming can no
  longer gain past 157 (181 using 4-owner creatures). Control is clamped at 99%, never 100% (harmless).
- Stable slots grow without bound: 278 stabled pets per character at 1000/1000/1000 (91 extra per skill).
  BREAKS (low severity): storage/hoarding and save-size abuse. 300 live already gives 68.
- recommendation: let tame/control clamp as is; cap stable slots (e.g. bonus counts only skill up to 120,
  or flat max ~ 20); if desired give Taming >157 new effects (e.g. +control slots, faster bonding, pet stat
  retention on tame instead of 0.90 ScaleSkills).

## Animal Lore

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Lore gump on wild tamable | Skills/AnimalLore.cs:49 | V >= 100 | clamps at 100 | clamps | clamps | clamps | |
| Lore gump on wild non-tamable | AnimalLore.cs:54 | V >= 110 | clamps at 110 | clamps | clamps | clamps | |
| Lore use check | AnimalLore.cs:59 | CheckTargetSkill 0-120 -> V/120 | clamps 100% at 120 | clamps | clamps | clamps | 120 |
| Control chance (half weight) | BaseCreature.cs:1426-1453 | see Taming | clamps 99% | clamps | clamps | clamps | n/a |
| Stable slots | AnimalTrainer.cs:61,90 | +(int)((L-90)/10) | +3 | +21 | +41 | +91 | n/a |
| Vet bandage heal (Lore = secondary) | Items/Skill Items/Misc/Bandage.cs:185-189, 375-393 | AOS: min = L/8 + Vet/5 + 4, max = L/6 + Vet/2.5 + 4 (+HitsMax/100 for animals), every 2.0 s (:500-502) | scales: L+Vet 120: 23-28 lore part 15-20, total 43-72 | L+Vet 300: 101.5-174 | L+Vet 500: 166.5-287.3 | L+Vet 1000: 329-570.7 | 120 (Bandage.cs:444 CheckSkill 0-120) |
| Vet resurrect gate | Bandage.cs:237-240 | Lore >= 80 | clamps | clamps | clamps | clamps | |
| Passive gain while taming | AnimalTaming.cs:373,394 | 0-120 | | | | | 120 |

- Lore's share of bandage healing at 1000 is 125-167 HP per bandage, every 2 s, uncapped. With Vet at the
  same value a pet heals 329-571 per 2 s: BREAKS (runaway healing, pets effectively unkillable) at 500+, already
  strong at 300 (101-174/2s). Overlaps the Veterinary auditor; Lore is half the formula.
- recommendation: Lore can clamp at 120 for gump/control; soft-cap its bandage contribution
  (e.g. L_eff = 120 + 30*ln(1 + (L-120)/30)) or move >120 into new effects (pet-info detail, small pet
  resist/regen aura, stable bonus capped).

## Herding

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Shepherd's crook command | Items/Weapons/Staves/ShepherdsCrook.cs:133-146 | CheckTargetSkill(MTS-30, MTS+30+rand(10)) | scales: 100% vs MTS<=81 | clamps 100% vs all | clamps | clamps | 145.0 pinned (MTS 106 + 39); 146.1 shard Raptor |

Only reader. recommendation: let it clamp (harmless); optional new effect: herd multiple animals / longer range.

## Musicianship

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| CheckMusicianship (all bard skills) | Items/Skill Items/Musical Instruments/BaseInstrument.cs:527-532 | gain CheckSkill 0-120 (result discarded); success = Mus/100 > rand | clamps: 100% at 100 | clamps | clamps | clamps | 120 |
| Bard difficulty reduction (peace target, provo, discord) | Peacemaking.cs:163-169, Provocation.cs:131-138, Discordance.cs:154-160 | diff -= (Mus-100)*0.5 if Mus>100 | -10 | -100 | -200 | -450 | n/a |
| Fire Horn success | Items/Skill Items/Misc/FireHorn.cs:72-77 | direct chance 0.5 + (Mus-77.5)*0.02 | clamps 100% at 102.5 | clamps | clamps | clamps | 102.5 |
| Fire Horn damage | FireHorn.cs:115-160 | see Provocation section | | | | | |
| Carpentry instrument recipes | Engines/Craft/DefCarpentry.cs:405-426 (shard dup CarpentryCraftRegistrations.cs:61) | secondary 45-50 | clamps | clamps | clamps | clamps | 50 |

- The diff reduction is unbounded; combined with the bard difficulty cap (160) it makes every bard check
  unfailable (see the table below). BREAKS (via the bard skills).
- recommendation: soft-cap the Musicianship reduction (e.g. -(Mus-100)*0.5 up to Mus 120, then
  -10 - 10*ln(1+(Mus-120)/50)), and keep CheckMusicianship clamped.

## Bard difficulty (BaseInstrument.cs:250-306, GetDifficultyFor :308-350)

D = (HitsMax*1.6 + StamMax + ManaMax + SkillsTotal/10, compressed above 700 by 3/11, +100 each magery /
fire breath / poison immune / vampire bat, +20*poison level) / 10, +40 paragon, then capped at 160.0 (Core.SE,
:298-301). Instrument: exceptional -5, each slayer slot -10 if it slays, +10 if target is the opposing super-slayer
group. So D in practice: max 160 natural, max 180 with a double opposing-slayer instrument; D = 200 cannot occur
in pinned content (computed anyway as asked).

Range for all three skills: GetBardRange = 8 + (int)(V/15) (BaseInstrument.cs:213):
120 -> 16, 300 -> 28, 500 -> 41, 1000 -> 74 tiles.

### Success chance table (formula used)

Overall success = P(Mus) * P(skill).
- P(Mus) = min(1, Mus/100) (BaseInstrument.cs:531).
- Peacemaking (target mode) and Discordance: diff = D - 10 - max(0,(Mus-100)/2); P = (S - (diff-25)) / 50,
  0 if S < diff-25 (too difficult), 1 if S >= diff+25 (Peacemaking.cs:163-171, Discordance.cs:154-168).
- Provocation: diff = (D1+D2)/2 - 5 - max(0,(Mus-100)/2); same 50-wide window (Provocation.cs:131-154).
  Table uses D1 = D2 = D.
- Peacemaking area mode: CheckSkill(Peacemaking, 0, 120) -> S/120 (Peacemaking.cs:83).
Assumption: the bard has Musicianship equal to the listed skill.

| bard skill (=Mus) | D=100 peace/discord | D=160 peace/discord | D=200 peace/discord | D=100 provo | D=160 provo | D=200 provo | area peace |
|---|---|---|---|---|---|---|---|
| 120 | 100% (130%, no gain) | 10% | 0% (too difficult) | 100% (120%) | 0% (S == min) | 0% (too difficult) | 100% |
| 300 | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| 500 | 100% | 100% | 100% | 100% | 100% | 100% | 100% |
| 1000 | 100% | 100% | 100% | 100% | 100% | 100% | 100% |

Thresholds for guaranteed success (S = Mus = X): peace/discord X >= (D+65)/1.5 -> D160: 150.0, D180: 163.3;
provo X >= (D+70)/1.5 -> D160: 153.3, D180: 166.7. Even with Musicianship at only 100, bard skill >= D+15
(peace/discord) or D+20 (provo) is guaranteed: 175/180 for D160.

=> At 300 (live today) and above, NO creature can resist any bard skill: every Peacemaking, Provocation and
Discordance attempt succeeds against every creature that is not flagged Uncalmable / Unprovokable /
BardImmune (and Provocation's paragon-with-D>=160 refusal, Provocation.cs:66). BREAKS.

## Peacemaking

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Area peace success | Peacemaking.cs:83 | S/120 | clamps 100% | 100% | 100% | 100% | 120 |
| Area peace range | Peacemaking.cs:99, BaseInstrument.cs:213 | 8 + S/15 | 16 | 28 | 41 | 74 | n/a |
| Area peace effect | Peacemaking.cs:103-123 | every harmful-able mobile in range: Combatant=null, Warmode off; creatures pacified 1 s; repeat every 5 s | scales | breaks | breaks | breaks | |
| Target peace success | Peacemaking.cs:163-171 | see table | scales (10% vs D160) | breaks: 100% vs all | breaks | breaks | D+15 with Mus<=100 (175 for D160, 195 for D180); 150-163 when Mus = S |
| Target peace duration | Peacemaking.cs:190-201 | 100 - diff/1.5 clamped 10..120 s | D160: 10 s; D100: 46.7 s | D160: 66.7 s; D100: 106.7 s | 120 s cap | 120 s cap | |

- Area peace at 300: guaranteed, 28 tiles (beyond the 18-tile client view), every 5 s. At 1000: 74 tiles.
  Resets combatants of every creature and every attackable player in range, including fights of other players
  out of the bard's sight. BREAKS (griefing / spawn-wide aggro reset; also hits players in PvP areas).
- Target peace: guaranteed 66.7-120 s pacify of any calmable creature (bosses included) from 300. BREAKS.
- recommendation: cap range at e.g. 8 + min(S,120)/15 (=16) plus small log growth; keep area success at
  S/120 but add a per-target resist roll vs D; soft-cap the diff reduction from Musicianship; new effects past
  120 could be longer duration or reduced re-aggro rather than certainty.

## Provocation

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Provoke success | Provocation.cs:131-154 | see table | scales (0% vs D160 pair) | breaks: 100% vs all | breaks | breaks | avgD+20 with Mus<=100 (180 for D160, 200 for D180); 153-167 when Mus = S |
| Target/pair range | Provocation.cs:93,122 | 8 + S/15 | 16 | 28 | 41 | 74 | n/a |
| Provoke duration | Mobiles/BaseCreature.cs:3742 | fixed 30 s | n/a | | | | |
| Fire Horn damage (Prov x3, Disc x3, Peace x1, Mus x1) | Items/Skill Items/Misc/FireHorn.cs:115-145 | per skill fixed f: scaled = f + max(0,f-900)*2; weightAvg = (M + 3P + 3D + Pe)/80; avg = weightAvg/2 PvM, /3 PvP; min = 0.9 avg, max = avg*10/9; split *2/n if n>1 targets; radius 2, every 6 s, 100% fire | all four at 120: PvM 81-100, PvP 54-66 | PvM 324-400, PvP 216-266 | PvM 594-733, PvP 396-488 | PvM 1269-1566, PvP 846-1044 | Mus 102.5 (only Musicianship gains here) |

- Fire Horn is the biggest numeric break in this slice: all-equal X gives weightAvg = 3X - 180. At 300 a single
  horn blast does 216-266 fire to a player (65-80 after a 70 fire resist cap) and 324-400 to a monster; at 1000,
  846-1044 PvP (254-313 after 70 resist) = one-shot every 6 s, costs 4 sulfurous ash. The f>900 tripling was a
  "GM bonus" that now multiplies everything above 90. BREAKS (runaway damage) from 300.
- Guaranteed provocation of any provokable creature (bosses with D 160 included, unless paragon) at 300+. BREAKS.
- recommendation: Fire Horn: clamp each skill input at 120 (or log soft-cap) before scaling; Provocation:
  soft-cap Musicianship reduction and keep a minimum fail chance (e.g. 5%) vs D>=160.

## Discordance

Effect (AOS branch, Discordance.cs:177-201):
effect = (int)(S/-5) for S<=100, else -20 + (int)((S-100)/-2.5); halved if base D >= 160 (:190-193).
Applied as: all 5 resists +effect (ResistanceMod), every skill of target += Value * effect/100 (:234-241), and the
abs value is exposed via GetEffect to BaseWeapon (hit chance :1334-1340, swing speed :1405-1411 and :1464-1470,
damage :2586-2592) and NinjaWeapons.cs:255.

| S | effect (normal) | effect (D>=160) | skill scalar | target skills become |
|---|---|---|---|---|
| 120 | -28 | -14 | -0.28 / -0.14 | 72% / 86% |
| 300 | -100 | -50 | -1.00 / -0.50 | 0% / 50% |
| 500 | -180 | -90 | -1.80 / -0.90 | -80% (negative) / 10% |
| 1000 | -380 | -190 | -3.80 / -1.90 | -280% (negative) / -90% (negative) |

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Discord success | Discordance.cs:154-168 | see table | scales (10% vs D160) | breaks: 100% vs all | breaks | breaks | same as target peace: 175 (Mus<=100, D160), 195 (D180) |
| Resist reduction | Discordance.cs:197-201; Misc/AOS.cs:80-86; Mobile.GetMinResistance = int.MinValue (Server/Mobiles/Mobile.cs:3249) | creature resist R + effect, damage x (100-R')/100 | R60: 32 -> dmg x0.68 | R60 -> -40 -> dmg x1.40 (boss: 10 -> x0.90) | -120 -> x2.20 (boss -30 -> x1.30) | -320 -> x4.20 (boss -130 -> x2.30) | |
| Skill reduction | Discordance.cs:234-241, Server/Skills.cs:286-327 (no floor) | Value*scalar | -28% | all skills 0 (boss -50%) | skills negative | skills strongly negative | |
| Melee damage of discorded mob | BaseWeapon.cs:2586-2592, AOS.cs:52 (damage<=0 -> nothing) | damageBonus -= 2*effect (only capped above at +100) | -56% | -200% -> 0 damage (boss -100% -> ~0) | 0 | 0 | |
| Hit chance of discorded mob | BaseWeapon.cs:1334-1348, 1358-1363 | defender bonus = DCI - effect, theirValue = (def+20)*(100+bonus); chance = our/(their*2), min 0.02 | defender loses 28 DCI (mob hits MORE) | effect 100 vs 0-DCI defender: theirValue = 0 -> chance = +Infinity -> always hits | theirValue < 0 -> chance < 0 -> 2% floor | 2% | |
| Swing speed of discorded mob (SE/ML branch) | BaseWeapon.cs:1405-1450, 1496 | bonus = SSI - effect (no floor); ticks = floor((speed*4 - stam/30) * 100/(100+bonus)); min 5 ticks | x1.39 slower | 100/(100-100) = +Infinity -> TimeSpan.FromSeconds(+Inf) throws OverflowException | factor negative -> ticks < 5 -> clamped to 5 = 1.25 s, FASTEST swing | 1.25 s fastest | |
| Maintain range | Discordance.cs:60-66 | 8 + S/15 | 16 | 28 | 41 | 74 | |
| Target range | Discordance.cs:123-127 | 8 + S/15 | 16 | 28 | 41 | 74 | |

- At 300 (live): any non-boss creature is discorded with certainty to 0 skills, -100 all resists, 0 melee
  damage. Worse, effect exactly 100 hits two division-by-zero points: swing-delay ticks become +Infinity and
  TimeSpan.FromSeconds(+Inf) throws (crash/exception risk in the combat timer; unverified whether caught), and
  hit chance vs a 0-DCI defender becomes +Infinity (auto-hit). Players reach exactly 300.0 today.
- Above 300 the signs flip: discorded mobs swing at the 1.25 s cap and their hit chance drops to the 2% floor;
  their skills go negative; incoming damage is multiplied up to x4.2 (no min resist on creatures).
- Also note the hit-chance read uses GetEffect(attacker) to reduce the DEFENDER's DCI (BaseWeapon.cs:1336-1340),
  i.e. a discorded attacker hits more often at low skill (inherited RunUO behavior; looks like a bug).
- BREAKS at 300 / 500 / 1000 (immunity, negative values, divide by zero, runaway damage taken).
- recommendation: hard-cap |effect| at 28 (OSI value at 120) or soft-cap e.g. 28 + 10*ln(1+(S-120)/60) with an
  absolute max ~40; clamp scalar so skills never go below 0; floor (100+bonus) at e.g. 10 in swing speed and
  hit chance; give >120 new effects (longer maintain time after leaving range, or small extra effects) instead.

## Tracking

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Track success | Skills/Tracking/Tracking.cs:129 | CheckSkill 0-21.1 | clamps 100% at 21.1 | clamps | clamps | clamps | 21.1 |
| Passive gain | Tracking.cs:163 | CheckSkill 21.1-100 | clamps (no effect) | | | | 100.0 |
| Search range | Tracking.cs:166-168 | 10 + ((int)V/10)*10 | 130 | 310 | 510 | 1010 | n/a |
| Arrow range | Tracking.cs:374 | range*2 | 260 | 620 | 1020 | 2020 | n/a |
| Track players (AOS) | Tracking.cs:304-354 | chance% = 50*(2*T + DH)/(Hid + Stl) (fixed), elf halves T | scales | scales (75% at equal T=DH=Hid=Stl) | scales | scales; vs 120/120 hider: 625% -> always | n/a |
| Stalking bonus (ML) | Tracking.cs:58-71 | min(distance target moved, 10 + T/10) | 22 | 40 | 60 | 110 | |
| -> Backstab | Spells/Ninjitsu/Backstab.cs:20 | x(1 + Nin/360 + stalk/100) | +22% | +40% | +60% | +110% | |
| -> Surprise Attack malus | Spells/Ninjitsu/SurpriseAttack.cs:59 | Nin.Fixed/60 + stalk (no cap) -> defender DCI | ok | Nin300+T300: 90 | Nin500+T500: 143 -> theirValue < 0 -> attacker 2% hit | 277 -> 2% hit | |
| -> Death Strike | Spells/Ninjitsu/DeathStrike.cs:124-133 | capped 60/30 | clamps | clamps | clamps | clamps | |

- Tracking gains only up to 100.0 by use (the 0-21.1 roll is always true past 21.1); everything above 100 must
  come from scrolls/other sources.
- Search range 1010 at 1000: GetMobilesInRangeByDistance over a 2021x2021 area (about half of Felucca's width)
  every 10 s per player: server-cost and near map-wide player location. BREAKS (perf + information) from ~500;
  310 at live 300 is already 2-3 screens.
- Stalking bonus pushes Surprise Attack malus past 100 + DCI: at exactly 100 + DCI the defender value is 0
  (division by zero -> +Infinity -> auto-hit); above it the attacker's own hit chance inverts to 2%. BREAKS at
  500/1000 combined with Ninjitsu (shared with the Ninjitsu auditor).
- recommendation: soft-cap search range (e.g. 10 + min(V,120) + 20*ln(1+(V-120)/100), max ~200); cap stalking
  bonus at 22 (120 value); give >100 new effects (show target direction/health, reveal tracks of hidden).

## Item Identification

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Identify IIdentifiable | Skills/ItemIdentification.cs:44 | CheckTargetSkill 0-100 -> V/100 | clamps 100% at 100 | clamps | clamps | clamps | 100 |
Cosmetic/gate reads: AnimalFormRestrictedSkills (PlayerMobile.cs:261), ClusterFGuildSystem.cs:221,251 (dummy 0.0 gate).
recommendation: let it clamp; optional new effect past 100 (e.g. reveal hidden item properties/durability).

## Taste Identification

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Detect poison on food | Skills/TasteID.cs:37 | CheckTargetSkill 0-100 | clamps 100% at 100 | clamps | clamps | clamps | 100 |
No other gameplay reader in pinned (potion enhance uses Alchemy). recommendation: let it clamp; optional new effect
(detect poison strength / trapped containers).

## Camping

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Light kindling | Items/Skill Items/Camping/Kindling.cs:38 | CheckSkill 0-100 | clamps 100% at 100 | clamps | clamps | clamps | 100 |
Campfire secure (Campfire.cs:18,122) and bedroll logout are not skill based. WanderingHealer teach list cosmetic.
recommendation: let it clamp; new effects possible (faster secure camp, campfire regen buff).

## Cartography

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Treasure map decode | Items/Maps/TreasureMap.cs:371-417 | min by level: L1 -3, L2 41, L3 51, L4 61, L5/L6 70; CheckSkill(min, min+60) | scales: L5/6 83.3%; L1-L3 100% | clamps 100% all levels | clamps | clamps | 130 (L5/L6) |
| Dig/use gate | TreasureMap.cs:311,385,442,562 | V >= min | clamps at 70 | clamps | clamps | clamps | |
| Craft maps | Engines/Craft/DefCartography.cs:85-88 via shard CraftItem.cs:877-895 | min..max 10-70, 25-85, 35-95, 39.5-99.5 | clamps | clamps | clamps | clamps | 99.5 |
| Local map extent | Items/Maps/LocalMap.cs:18-21 | dist = 64 + 2V | 304 | 664 | 1064 | 2064 | |
| City map extent | Items/Maps/CityMap.cs:19-22 | dist = max(64+4V,200), size clamp 200-400 | 544 | 1264 | 2064 | 4064 | |
| Sea chart extent | Items/Maps/SeaChart.cs:19-22 | dist = max(64+10V,200) | 1264 | 3064 | 5064 | 10064 | |
| World map extent | Items/Maps/WorldMap.cs:21-25 | x20 = 20V, bounds 1344-x20 .. 1472+x20 | 2400 | 6000 | 10000 | 20000 | |

- Map extents grow without bound; display bounds go negative and past the facet edge (world map covers the whole
  facet at V ~182; at 1000 it is 41,000 tiles wide so the facet is ~12% of the image). Cosmetic BREAK (negative
  coords, maps become useless), no gameplay exploit (unverified how the client renders negative bounds).
- Treasure map levels 1-6 only; no level reads Cartography above 130.
- recommendation: clamp map dist at the 100-skill value; give >130 new effects (e.g. decode higher-tier maps,
  chance for bonus chest level, show dig radius).

---------------------------------------------------------------------------------------------------------------

## BREAKS summary

1. Bard success (Peacemaking target, Provocation, Discordance): bard difficulty caps at 160 (180 with opposing
   slayer instrument); with skill = Musicianship >= 150-167 (or skill >= D+15/D+20 with Mus 100) success is 100%
   vs every creature. Live 300 already guarantees it. No creature is resistible except flag-immune ones and
   Provocation's paragon D>=160 refusal.
2. Area Peacemaking: 100% from 120, range 8+S/15 = 28 tiles at 300, 74 at 1000, every 5 s; resets all
   combatants (players included where harmful allowed).
3. Discordance effect uncapped: at 300 normal creatures get 0 skills, -100 resists, 0 melee damage; effect = 100
   divides by zero in swing speed (+Infinity -> TimeSpan overflow exception) and hit chance (+Infinity);
   above 300 skills go negative, resists to -320 (x4.2 damage taken), swing speed inverts to fastest, hit chance
   inverts to 2%.
4. Fire Horn damage: weightAvg = 3X - 180 for all-equal bard skills; 216-266 PvP / 324-400 PvM at 300,
   846-1044 PvP / 1269-1566 PvM at 1000, AoE every 6 s.
5. Musicianship diff reduction (Mus-100)/2 unbounded: root cause of (1).
6. Animal Lore (with Vet) pet bandage healing 101-174 per 2 s at 300, 329-571 at 1000.
7. Stable slots unbounded: 68 at 300, 278 at 1000.
8. Tracking search range 10 + V rounded: 310 at 300, 1010 at 1000 (server cost, map-wide player tracking);
   stalking bonus 10+T/10 drives Surprise Attack malus past 100 (div-by-zero / 2% inversion) with Ninjitsu.
9. Cartography map extents unbounded (cosmetic, negative bounds).

Gain ceilings: Taming 157.0 (181.0 with 4-owner creatures), Lore 120, Herding 146.1, Musicianship 120,
Peacemaking 120 area / up to 175-195 target (falls as Musicianship rises), Provocation up to 180-200,
Discordance up to 175-195, Tracking 100, ItemID 100, TasteID 100, Camping 100, Cartography 130.
