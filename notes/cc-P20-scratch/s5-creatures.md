# S5: creature difficulty vs a 300-skill character

Read-only research. Authority: pinned ModernUO (`D:\UO\ModernUO-pinned\Projects`, paths below are relative
to it). Shard creatures from `D:\ShatteredLegacy\server\customizations`. Era: EJ (expansion Id 11 per
AGENTS.md), so Core.LBR, Core.AOS, Core.SE, Core.ML are all true. Shard caps: 300.0 per skill
(customizations\ClusterFSkillCaps.cs:10), 500 per stat / 1500 total (ClusterFStatCaps.cs:10-11). No shard
patch touches the bard skills, BaseInstrument, CheckHit or ScaleDamageAOS (checked patches\ and a grep of
customizations).

Files in this folder:
- `s5_bard_difficulty.py` - the parser/calculator (re-runnable, read-only on sources).
- `s5-creature-difficulty.csv` - 694 rows, one per computed creature, sorted by uncapped difficulty.
- `s5-parse-failures.txt` - 215 classes not computed, with the reason.
- `s5-run-output.txt` - console summary of the last run.

## 1. The formula, exactly (UOContent/Items/Skill Items/Musical Instruments/BaseInstrument.cs:250-306)

```
val  = HitsMax * (Core.LBR ? 1.6 : 0.625) + StamMax + ManaMax        (:260)
val += SkillsTotal / 10.0                                              (:262)
if val > 700: val = 700 + (int)((val - 700) * 3/11)                    (:264-267, soft cap)
+100 if IsMageryCreature:  AI == AI_Mage && Skills.Magery.Base > 5.0   (:242, :271)
+100 if IsFireBreathingCreature: GetAbility(MonsterAbilityType.FireBreath) != null   (:244, :276)
+100 if PoisonImmune != null                                           (:246, :281)
+100 if VampireBat or VampireBatFamiliar                               (:286)
+ (HitPoison.Level + 1) * 20   (no HitPoison -> 0)                     (:248, :291)
val /= 10                                                              (:293)
+40 if IsParagon                                                       (:295-298)
cap 160 if Core.SE                                                     (:300-303)
```

Inputs, as pinned computes them:
- `HitsMax` (Mobiles/BaseCreature.cs:579-580): `HitsMaxSeed <= 0 ? Str : HitsMaxSeed + StatOffset(Str)`.
  `SetHits` writes HitsMaxSeed (BaseCreature.cs:4599-4620); the pre-AOS x100/60 rescale (:4601, :4612) is
  off in EJ. With no SetHits, a creature's HitsMax is its Str (not 50 + Str/2, which is Mobile.cs:2051 and
  is overridden).
- `StamMax` / `ManaMax` (BaseCreature.cs:586-594): seed from SetStam/SetMana, else Dex / Int.
- `SkillsTotal` (Server/Mobiles/Mobile.cs:477) = `Skills.Total`, the sum of BaseFixedPoint (Server/Skills.cs:513,
  :836), i.e. tenths; `/10.0` makes it skill points. So a creature with 600.0 total skill adds 600.
- Fire breath: any ability whose AbilityType is FireBreath, which includes FireBreath, ChaosBreath,
  ColdBreath and every subclass (Mobiles/Abilities/Fire Breath/*.cs, e.g. Leviathan's nested breath, the
  shard's CrystalHydraBreath). There is no `HasBreath` property anywhere in pinned or customizations.
- Poison levels (Misc/PoisonKinds.cs:80-92): Lesser 0, Regular 1, Greater 2, Deadly 3, Lethal 4, so Lethal
  HitPoison adds 100 raw (10 final).
- Not in the formula (the TODO at :252-255 admits it): aura damage, summoning, life drain, stun, AoE
  specials, weapon abilities, damage output, resistances, attack skill.

Hand check, Dragon: hits 486.5*1.6 + 95.5 + 455.5 + 359.75 skill = 1689 raw -> 700 + int(989*3/11) = 969
-> +100 mage +100 breath = 1169 -> 116.9. Matches the CSV.

## 2. Method and approximations

Static parse, no build. The script strips comments/strings from every .cs in pinned UOContent (whole tree,
not just Mobiles, so Engines/ quest and champion creatures are included; the `category` column says where
each lives) and in customizations, finds every class, resolves inheritance to BaseCreature, drops abstract
classes, then for each concrete class walks the chain root-first, applying each class's chosen constructor.

Approximations:
1. Every `SetX(min, max)` uses the midpoint; `SetSkill` midpoint in fixed point (same as RandomMinMax of
   fixed values).
2. Constructor choice: the `[Constructible]` one, else the one with most Set calls; `: this(...)` chains are
   followed inside the class. If a Set call appears more than once (if/else branches) the last one wins
   (7 rows; flagged in `notes`).
3. `Core.X ? a : b` takes `a` (all era flags true). Golem's `scalar` parameter defaults to 1.0.
4. Stat offsets, equipment and buffs ignored (GetStatOffset = 0).
5. AI type: the literal `AIType.AI_x` in the base(...) call or an `AI = ` assignment; classes that pass AI
   as a parameter inherit it, and `ForcedAI` overrides are ignored (8 rows show `param`).
6. Breath/PoisonImmune/HitPoison are textual matches on the class body, inherited down the chain. A
   random HitPoison (`RandomBool() ? Lesser : Regular`) uses the average level.
7. Paragon is not applied to the main value; the `paragon` column is value + 40, capped at 160.
8. The `uncapped` column is the formula without the final 160 cap (so the top end can be ranked); `diff`
   is the in-game value.
9. Combat columns (sec. 6) use the creature's best of Wrestling/Swords/Macing/Fencing/Archery, SetDamage
   midpoint, and Str/Tactics/Anatomy bonuses from ScaleDamageAOS.

Parse failures: 215 classes. 175 are vendors, townsfolk, quest NPCs, talisman summons and the shard's
33 gargoyle vendors, whose stats are set in a base-class virtual (BaseVendor.InitBody etc.), not in the
constructor. About 40 are combat-relevant and were not computed: the 16 Despise power-scaled creatures
and DespiseBoss base (stats come from virtual StrStart/HitsStart properties scaled by power level), MedusaClone,
ShameGuardian, the 6 Meer "Enraged" animals (SetHits(50, Str)), Revenant (skills copied from the target),
4 war horses, Golem-derived summons, Parrot/SeaHorse/HellSteed/SilverSteed/GrizzledMare (stats in a shared
base), Clone (Mirror Image). Full list with reasons: `s5-parse-failures.txt`.

## 3. Results

Computed: 694 creatures (559 pinned, 135 custom). Categories: monster 279, other (Engines/quests/etc) 167,
custom 135, animal 70, npc 24, special (champions, Harrower etc) 14, familiar 5.

In-game difficulty (capped at 160):

| set | n | min | Q1 | median | Q3 | max | at cap 160 |
|---|---|---|---|---|---|---|---|
| all computed | 694 | 3.9 | 42.5 | 76.7 | 103.8 | 160 | 70 |
| combat set (monsters+animals+special+custom) | 498 | 3.9 | 58.4 | 85.0 | 120.0 | 160 | 68 |
| custom only | 135 | 26.0 | 74.8 | 103.6 | 160 | 160 | 34 |

Histogram, combat set (498), buckets of 10 on the in-game value:

```
  0- 9  14  ##############
 10-19  14  ##############
 20-29  26  ##########################
 30-39  22  ######################
 40-49  28  ############################
 50-59  25  #########################
 60-69  39  #######################################
 70-79  50  ##################################################
 80-89  58  ##########################################################
 90-99  40  ########################################
100-109 37  #####################################
110-119 21  #####################
120-129 18  ##################
130-139  8  ########
140-149 19  ###################
150-159 11  ###########
  =160  68  ####################################################################
```

Uncapped spread of the same set in buckets of 20: 0-19: 28, 20-39: 48, 40-59: 53, 60-79: 89, 80-99: 98,
100-119: 58, 120-139: 26, 140-159: 30, 160-179: 14, 180-199: 8, 200+: 46. The pile at 160 is real: 68
creatures (34 of them the shard's own) are indistinguishable to the bard formula. With the paragon +40,
112 of the combat set reach 160.

Top 20 (uncapped; every one is 160 in game):

| # | creature | src | uncapped | HitsMax | notes |
|---|---|---|---|---|---|
| 1 | AdrianTheGloriousLord | custom | 3317.6 | 60000 | mage |
| 2 | AndrosTheDreadLord | custom | 3317.6 | 60000 | mage |
| 3 | SlasherOfVeils | custom | 2876.2 | 57500 | mage |
| 4 | Medusa | custom | 2740.2 | 60000 | mage, poison immune, Deadly-or-Lethal HitPoison, BardImmune |
| 5 | RakktaviRenowned | custom | 2257.5 | 50000 | |
| 6 | TikitaviRenowned | custom | 2249.2 | 50000 | |
| 7 | VitaviRenowned | custom | 2160.1 | 47500 | mage |
| 8 | DemonKnight | pinned | 1546.6 | 30000 | mage, poison immune |
| 9 | NavreyNightEyes | custom | 1530.4 | 32500 | mage, poison immune, Lethal HitPoison |
| 10 | MinionOfScelestus | custom | 1420.4 | 30000 | mage, poison immune, Lethal HitPoison |
| 11 | StygianDragon | custom | 1400.0 | 30000 | breath |
| 12 | ChaosVortex | custom | 1257.0 | 27000 | poison immune |
| 13 | UnboundEnergyVortex | custom | 951.5 | 20000 | poison immune |
| 14 | Allosaurus | custom | 859.5 | 18000 | |
| 15 | Niporailem | custom | 580.9 | 10250 | |
| 16 | PixieRenowned | custom | 512.6 | 9150 | mage |
| 17 | Ilhenir | pinned | 502.6 | 9000 | mage, poison immune |
| 18 | Serado | pinned | 488.4 | 9000 | poison immune, Lethal HitPoison |
| 19 | EternalGazer | custom | 481.7 | 7425 | mage |
| 20 | Twaulo | pinned | 434.8 | 7500 | poison immune |

The ranking above the cap is almost purely HitsMax: past raw 700 every point counts 3/11, and the 1.6x hits
term dominates, so this is a "how big is the HP bar" list, not a danger list.

Sanity check (in-game values): Rat 6.2 < GiantRat 23.1 < Orc 43.5 < Troll 46.9 < Ogre 49.0 < OrcishLord 65.6
< Daemon 105.1 < Dragon 116.9 < Balron 126.6 < AncientWyrm 152.7 < AncientLich 155.6 < GreaterDragon /
Harrower / Semidar / Leviathan 160. The asked order rat < orc < troll < dragon < ancient wyrm holds. Oddities
the formula produces: Troll is barely above Orc (Orc's dex/skills offset the Troll's hits); WhiteWyrm 107.9 is
below Dragon; GreaterDragon (172.7 uncapped) outranks AncientWyrm.

## 4. Danger the formula misses

- Only four ability flags count. Not counted: DrainLife / mass drain (4+1 users), ColossalBlow stun (3),
  PoisonGas / mass poison, DeathExplosion, summon counters (Pixies, Skeletons, Lesser Undead), DestroyEquipment,
  BloodBath, GraspingClaw / RuneCorruption / FanningFire resist debuffs, ReflectPhysicalDamage, MagicalBarrier,
  weapon special moves, auras.
- Scripted boss mechanics in custom code: StygianDragon's crimson meteor (fire), stygian fireball (120-150
  chaos, StygianDragon.cs:438-442), fire column; Medusa (stone gaze, clones; BardImmune); Navrey; Slasher of
  Veils; the Despise bosses; Shame revamped guardians. All score 160 the same as a GreaterDragon.
- Damage output is absent: FierceDragon (Engines/Quests/Haochi's Trials/Mobiles/FierceDragon.cs:15-19, Str
  6000, damage 50-80) scores 160 like the rest but hits for roughly 1290 before resists, about 390 through 70
  resists, more than a 300-skill character's maximum HP. It is a quest creature meant to be fled from.
- Necro or other caster AIs get no mage bonus (only AI_Mage counts, :242), and the paragon bonus is a flat
  +40 although paragons get far more HP and damage.
- Health-pool sponges (the 47500-60000 HP bosses) score the same as a 160 creature with 1/50th the HP.

## 5. Bard success for a 300 bard

Peacemaking (Skills/Peacemaking.cs:163-170) and Discordance (Skills/Discordance.cs:154-170):
`diff = GetDifficultyFor - 10 - (Musicianship - 100) * 0.5`, success = CheckTargetSkill(diff - 25, diff + 25),
which is an automatic success once skill >= diff + 25 (Skills/SkillCheck.cs:166-169). Provocation
(Skills/Provocation.cs:131-138, :154): diff = mean of the two targets' difficulties - 5 - the same
musicianship term. The musicianship gate (BaseInstrument.cs:527-532) is `Musicianship / 100 > random`, so it
always passes at 100+.

| bard skill (all bard skills equal) | Peace/Discord vs 160 | Provoke 160 vs 160 |
|---|---|---|
| 100 | diff 150, window 125-175: 0% | 0% |
| 120 | diff 140, window 115-165: 10% | 0% (diff 145, window 120-170) |
| 150 | diff 125, window 100-150: 100% | 90% (diff 130) |
| 154 | 100% | 100% |
| 300 | diff 50, window 25-75: 100% | 100% (diff 55) |

So every creature that is not flagged is a guaranteed peace / provoke / discord from about skill 150-154 up.
At 300 the diff for the hardest target is 50, so even an exceptional-bonus, slayer-penalised instrument
changes nothing. What still blocks a bard: `BardImmune` (38 computed classes, e.g. Medusa, Meraktus,
WyvernRenowned, Revenant, KhaldunRevenant, faction NPCs), explicit `Unprovokable` / `Uncalmable` (15 / 3), and
paragons scoring >= 160, which cannot be provoked (Provocation.cs:66, BaseCreature.cs:3746) and take half
discord (Discordance.cs:190-193).

Discordance magnitude is uncapped above 100 (Discordance.cs:181-193): `effect = -20 + (skill-100)/-2.5`.
At 300 that is -100 to every resist, -100% to every skill (skill mod = Value * -1.0, :239) and, via
ScaleDamageAOS (Items/Weapons/BaseWeapon.cs:2586-2592), -200% damage bonus; halved for 160 targets (-50
resist). Creature resists have no floor (Server/Mobiles/Mobile.cs:3249 GetMinResistance = int.MinValue), so
a discorded dragon at 60 physical sits at -40 and takes 1.4x raw damage instead of 0.4x (3.5x more).
Odd detail worth a look: CheckHit subtracts the attacker's discord effect from the defender's
defense-chance bonus (BaseWeapon.cs:1334-1340, comment says the defender should be the one affected). At
300 discord this drives (100 + DCI - 100) to DCI, so a discorded creature swinging at a 0-DCI defender
gets theirValue 0 and an infinite hit chance. At OSI magnitudes (max 28) this was minor.

## 6. Can anything threaten a 300 / 500-stat character?

Player side, from pinned:
- HP: PlayerMobile.HitsMax = Str/2 + 50 + min(BonusHits, 25) (Mobiles/PlayerMobile.cs:548-576): 500 Str ->
  300, 325 with items. HP does not grow with skill.
- Resists capped at 70 (Server/Mobiles/Mobile.cs:431); AOS.Damage takes (100 - resist)% per type
  (Misc/AOS.cs:126-132), so at least 30% of every resisted hit lands.
- Hit chance (AOS, BaseWeapon.cs:1299, :1348, :1358-1363): `chance = (atk+20)(100+HCI) / (2 (def+20)(100+DCI))`,
  floor 2%. Defense skill 300 -> def term 320.
- Player damage (ScaleDamageAOS, BaseWeapon.cs:2556-2602, "No caps apply"): Str 500 +1.55, Anatomy 300 +1.55,
  Tactics 300 +1.94, plus capped DI 100% -> about 7.0x weapon base. Player vs a 120-wrestling creature:
  320/280 > 1, a guaranteed hit.

Creature side (computed for all 694; columns atkskill, dmghit, dmg70, hit_vs300, hit_vs300dci45):
- Highest attack skill is KhaldunRevenant at 145 -> 25.8% to hit a 300 defender (17.8% with 45 DCI). The
  median creature (80) hits 15.6%. Only 4 creatures reach 25%.
- Highest melee per landed hit through 70 resists: StygianDragon 59, WyvernRenowned 57, Navrey 55, Rend 54,
  Putrefier 53. Seven creatures exceed 50; none reaches 100 except the quest FierceDragon (~390).
- Expected melee per swing (hit chance x damage): top is Rend 14, StygianDragon 12.4, Putrefier 11.7,
  Medusa 10.8, GreaterDragon 10.8. Against 325 HP that is about 25+ swings to kill, with no healing.
- Fire breath is capped at 200 (Mobiles/Abilities/Fire Breath/FireBreath.cs:207-216), 30-45 s cooldown:
  about 60 through 70 fire resist.
- Spells: AOS spell damage = dice x (1 + Int/10 % + inscription) x (30 + 9 x EvalInt/100)%
  (Spells/Base/Spell.cs:218-257); MagicResist skill does not reduce AOS damage. A 100-EvalInt, 700-Int
  creature's Flamestrike is about 51 x 1.7 x 1.2 = 104, about 31 after 70 fire resist. Harrower (Int 1100)
  about 38.

Verdict: with a 300 template nothing in pinned or the shard's content threatens the character one on one,
and nothing resists the bard. What can still hurt:
1. Scripted boss specials in custom code that stack with melee and spells (StygianDragon meteor/fireball,
   Medusa, Navrey, Slasher of Veils, Despise bosses, Shame guardians), especially if several fire at once.
2. Numbers: several 150+ creatures, or a champion spawn wave, at 10-14 expected damage per swing each.
3. Lethal HitPoison carriers (Navrey, MinionOfScelestus, Serado, DarknightCreeper) if the player cannot cure.
4. Non-resisted damage paths (direct damage, `target.Damage` without AOS types) and anything that removes
   the 70 cap, e.g. resist debuffs (GraspingClaw, RuneCorruption, FanningFire).
5. FierceDragon, by design.
6. BardImmune bosses, which the bard simply cannot touch (Medusa, Meraktus, WyvernRenowned).
The big custom bosses are HP sponges: their threat is time, not danger.

## 7. What would have to scale for 500-1000 to matter

Formula by formula, what more skill buys a player and what a creature would need to keep pace:

| lever | player 300 -> 1000 | creature needed to keep pace |
|---|---|---|
| Hit chance vs player (ratio of atk+20 to def+20) | defense 320 -> 1020 | attack skill ~ the player's (1000) to keep ~50%; at 120 it sits at the 2% floor at 1000 |
| Player hit chance | already 100% | creature defense skill near the player's |
| Player melee damage (uncapped Str/Tactics/Anatomy) | x7.0 -> x14.9 | HP x2 again over today's |
| Player spell damage (EvalScale 30+9E/100) | x3.0 -> x9.3 eval term | HP / resists x3 |
| Bard success | saturated from ~150 | the 160 cap and the -(M-100)/2 term make it unwinnable; needs formula change |
| Discordance | -100 resist at 300, -380 at 1000 | no creature value survives; needs a clamp |
| Player HP / resists | fixed (Str-bound, 70 cap) | creature damage does not need to scale for the player to die faster; it needs to land |

To keep 500-1000 "meaningful" by scaling content, every creature's attack skill, defense skill, HP and
damage would need to rise roughly in proportion to the player's skill (attack skill alone x3-8), the bard
difficulty cap and formula would need replacing, and discord would need a clamp. That is a rewrite of about
700 creature definitions plus the bard skills, and it would make all existing content dead for anyone
under 300.

Recommendation: treat the upper range as prestige, and do it on purpose rather than by accident:
- Clamp the effective skill used by a few formulas that run away, not the displayed skill: Discordance
  effect (hold it at the OSI -28% or a modest extension), the Peacemaking/Provocation/Discord musicianship
  term, ScaleDamageAOS Tactics/Anatomy bonuses, and EvalInt scaling. A soft curve (full value to 120,
  then diminishing, e.g. 120 + sqrt(skill - 120) x k) keeps 300-1000 visible and slightly better without
  breaking the creature table.
- Let skills above ~150 pay out in non-combat or sideways ways (titles, cosmetic, crafting quality tiers,
  gathering yield, access to prestige content), not raw power.
- If endgame danger is wanted, build a small tier of new encounters whose threat is mechanics (unresisted
  or resist-piercing specials, adds, timed AoEs, BardImmune) plus attack skills of 300+, rather than more
  HP. The current 47k-60k HP bosses show that HP alone only adds time.
- Before any of this, decide whether the CheckHit discord sign quirk (BaseWeapon.cs:1337) is meant to be
  attacker or defender. It changes outcomes once discord exceeds about 45.
