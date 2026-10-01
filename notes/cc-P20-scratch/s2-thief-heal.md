# s2: thief and healer skills at 120 / 300 / 500 / 1000 (cc-P20)

Skills: Hiding, Stealth, Detect Hidden, Snooping, Stealing, Lockpicking, Remove Trap, Poisoning, Healing, Veterinary, Begging, Forensic Evaluation.

Paths are relative to D:\UO\ModernUO-pinned\Projects unless marked SL: (D:\ShatteredLegacy\server).
Expansion is Endless Journey, so the AOS/SE/ML/SA branches apply.

## Shard overrides checked

- I grepped SL:customizations and SL:patches for SkillName.X, Skills.X and Skills[SkillName.X] for all 12 skills. None of the shard files replaces or patches the handler for any of these skills (Hiding.cs, Stealth.cs, DetectHidden.cs, Snooping.cs, Stealing.cs, LockPick.cs, RemoveTrap.cs, Poisoning.cs, Bandage.cs, Begging.cs, ForensicEval.cs).
- SL:patches\Bandage-pet-mimic-targeting.patch only adds a PetMimic feed branch. It has no effect on the formulas.
- SL:patches\StealableArtifacts-servuo-entries.patch only adds stealable-artifact entries. It has no effect on the formulas.
- The shard reads these skills in these places:
  - Starter kits: SL:customizations\CharacterCreation.cs:1018-1339.
  - Guild starter paths: SL:customizations\ClusterFGuildStarterPath.cs:48-59.
  - Guild join gates: Healing 50 and Stealing 20 in SL:customizations\ClusterFGuildSystem.cs:151,171.
  - NPC SetSkill values and NPC AI calls to UseSkill(DetectHidden/Stealth) (OrcScout, GreenGoblinScout, KepetchAmbusher, TrapdoorSpider). These only use the skill as a threshold or a cosmetic.
- Item skill bonuses that raise Skill.Value:
  - Stealth +30 on each Assassin set piece and +40 on each Hunter set piece (SetSkillBonuses).
  - CloakOfSilence Stealth +10, RoyalGuardInvestigatorCloak Stealth +20.
  - MarkOfTravesty: Healing/Stealth/Stealing +10.
  - Whether the per-piece set bonuses stack, for example Hunter 4 x 40 = +160 Stealth, is unverified.
- Related shard change: SL:customizations\ClusterFStatCaps.cs:10 sets the individual stat cap to 500 (default; it is applied through SL:patches\PlayerMobile-individual-stat-cap.patch). Dex can therefore reach 500. Bandage delay is driven by Dex (see Healing).

## Gain ceilings (summary)

| Skill | Gain ceiling | Where |
|---|---|---|
| Hiding | 100 (0 inside a house where you are a friend) | Skills/Hiding.cs:73 |
| Stealth | 60 + 2*AR. That is 60 unarmored and at most 142 (AR 41) | Skills/Stealth.cs:96-100 |
| Detect Hidden | 100 | Skills/DetectHidden.cs:159,183,228 |
| Snooping | 100 | Skills/Snooping.cs:84 |
| Stealing | 127.5 (10-stone item, iw=100) | Skills/Stealing.cs:309 |
| Lockpicking | 140 (TMap L5, Paragon L5, ToT chest) | Items/Containers/TreasureMapChest.cs:190 |
| Remove Trap | TrapPower+30. About 180 on world chests; on tinker-made traps it is 0.9*Tinkering+30, so unbounded (930 at Tinkering 1000) | Skills/RemoveTrap.cs:61 |
| Poisoning | 100 (Deadly, Darkglow and Parasitic potions use 95-100) | Skills/Poisoning.cs:124 |
| Healing | 120 | Items/Skill Items/Misc/Bandage.cs:444-445 |
| Veterinary | 120 | Items/Skill Items/Misc/Bandage.cs:444-445 |
| Begging | 100 | Skills/Begging.cs:111 |
| Forensics | 100 | Skills/ForensicEval.cs:36,54 |

Every skill except Remove Trap stops gaining from use somewhere between 100 and 142. Points above that have to come from some other source. Remove Trap is the only skill whose gain ceiling grows with another skill (Tinkering).

---

## Hiding

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Hide success | Skills/Hiding.cs:73 | CheckSkill(0-bonus, 100-bonus); bonus 100 in a friend's house | clamps at 100 (always succeeds) | clamps | clamps | clamps | 100 |
| "Hide in combat" range | Skills/Hiding.cs:53-71 | range = min((int)((100-H)/2)+8, 18). Blocked if your combatant is in range and LOS, or if a mobile in range targets you | BREAKS: range = -2 | BREAKS: -92 | BREAKS: -192 | BREAKS: -442 | n/a |
| Stealth gate | Skills/Stealth.cs:77 | Hiding.Base >= 30 (ML) | clamps | clamps | clamps | clamps | - |
| Detect Hidden contest (active and passive) | Skills/DetectHidden.cs:124-127, 205-208 | reveal if DH+U(-10,10) >= H+U(-10,10) | see Detect Hidden | | | | - |
| Creature AI detect | Mobiles/AI/BaseAI/BaseAI.cs:942-955 | chance = max(DH/10, DH/1.2 - min(H/2.9, S/1.8))/100 | scales | clamps at the DH/10 floor | clamps | clamps | - |
| Reveal spell / Tracking difficulty | Spells/Sixth/Reveal.cs:63-82; Skills/Tracking/Tracking.cs:311-345 | 50*(Magery+DH)/(H+S) and 50*(2*Track+DH)/(H+S), all in Fixed units | scales (ratio) | scales | scales | scales | - |
| Snoop-fail reveal | Skills/Snooping.cs:97 | Hiding/2 < rand*100 | scales | clamps at 200 (never revealed) | clamps | clamps | - |
| Death Strike scalar | Spells/Ninjitsu/DeathStrike.cs:128 | min(1, (H+S)/220) | clamps at H+S=220 | clamps | clamps | clamps | - |
| SmokeBomb/EggBomb | Items/Skill Items/Ninjitsu/SmokeBomb.cs:40, EggBomb.cs:46 | call the same Hiding.OnUse | same as above | | | | |

**Hide-in-combat details**
- At Hiding 116-117 the range is 0. At 118 and above it is negative.
- `IEntity.InRange` with a negative range is always false (Server/IEntity.cs:100-104), so your combatant can never block the hide.
- `GetMobilesInRange` clamps the range to 0 (Server/Maps/Map.MobileEnumerator.cs:74). Only a mobile standing on your own tile can block it.
- Result: from about 118 skill (including item bonuses) you can hide in melee against anyone who is attacking you.
- There is a 10 s skill delay but no other limit.

recommendation: clamp the range at its pinned 100-skill value (8 tiles) and floor it at 1, for example `Math.Clamp(..., 8, 18)`. After that, give Hiding new effects past 100 instead of letting it shrink the combat range. Options: reduced reveal chance from damage, or a longer stealth step budget.

## Stealth

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Stealth success | Skills/Stealth.cs:96-100 | CheckSkill(-20+2AR, 60+2AR); AR >= 42 blocks it outright (Stealth.cs:91) | clamps (always succeeds at 60+2AR, at most 142) | clamps | clamps | clamps | 60 unarmored / 142 max |
| Steps | Skills/Stealth.cs:102 | max((int)(S/5), 1) | scales: 24 steps | scales: 60 | scales: 100 | BREAKS (mild): 200 steps | - |
| Running while stealthed | Mobiles/PlayerMobile.cs:3523-3536 | running costs 2 steps and reveals at 0; walking at 0 re-runs Stealth.OnUse | 12 running tiles | 30 | 50 | 100 running tiles hidden | - |
| Creature AI detect | Mobiles/AI/BaseAI/BaseAI.cs:947 | see Hiding (S/1.8 term) | scales | clamps | clamps | clamps | - |
| Reveal / Tracking | see Hiding | ratio | scales | scales | scales | scales | - |
| ShadowStrike gate | Items/Weapons/Abilities/ShadowStrike.cs:26-28 | Stealth >= 80 | clamps | clamps | clamps | clamps | - |
| Death Strike | Spells/Ninjitsu/DeathStrike.cs:128 | (H+S)/220 capped at 1 | clamps | clamps | clamps | clamps | - |

- Walking stealth is already effectively unlimited at the pinned cap: when the steps run out, OnUse runs again and always succeeds above 60+2AR.
- The step count only matters in three places:
  - Running.
  - Backstab, SurpriseAttack and KiAttack, which need steps > 0 (Spells/Ninjitsu/Backstab.cs:25, SurpriseAttack.cs:20, KiAttack.cs:31).
  - Tracking/Reveal ratios.
- At 1000 a player can run 100 tiles while hidden.

recommendation: soft-cap the steps, for example `steps = 20 + 20*ln(1 + S/100)` (about 34 at 100, about 48 at 300, about 68 at 1000), or cap running steps separately. Otherwise let it scale.

## Detect Hidden

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Area scan range | Skills/DetectHidden.cs:153, 183-186, 198, 223 | range = (int)(DH/10); halved on a failed check (no failures at 100+). Scans mobiles and items in a (2r+1)^2 square around the target point | scales: 12 | BREAKS: 30 tiles (beyond the 18-tile view) | BREAKS: 50 | BREAKS: 100 tiles (201x201 scan) | 100 |
| Contest vs hider | Skills/DetectHidden.cs:205-208 | reveal if DH+U(-10,10) >= H+U(-10,10) | scales (relative) | scales vs players; BREAKS vs fixed-skill NPC hiders/detectors (see below) | same | same | - |
| Passive detect (Felucca PvP, within 4 tiles) | Skills/DetectHidden.cs:69-136; Mobiles/PlayerMobile.cs:3552-3564 | same +/-10 contest, 3 s debounce | scales (relative) | scales | scales | scales | - |
| Trapped container | Skills/DetectHidden.cs:158-159 | in range DH/10 and CheckSkill(0,100) | clamps at 100 (always) | clamps | clamps | clamps | 100 |
| Dungeon traps | Skills/DetectHidden.cs:245 | HS: DH >= 75 | clamps | clamps | clamps | clamps | - |
| Faction traps | Skills/DetectHidden.cs:228; Engines/Factions/Items/Traps/BaseFactionTrap.cs:173 | CheckTargetSkill(80,100); passive (DH-80)/20 | clamps at 100 | clamps | clamps | clamps | 100 |
| Reveal spell / Tracking | Spells/Sixth/Reveal.cs:71; Skills/Tracking/Tracking.cs:312 | ratio with H+S | scales | scales | scales | scales | - |
| Remove Trap gate | Skills/RemoveTrap.cs:21 | DH >= 50 | clamps | clamps | clamps | clamps | - |

**Area range**
- At 300 the scan reaches hidden players and traps up to 30 tiles away, which is off screen.
- At 1000 the radius is 100 tiles. That reveals everyone hidden across a whole town or dungeon level.
- Each use also runs a 201x201 GetMobilesInRange plus GetItemsInRange scan (a performance cost).

**Contest**
- When the hider's skill exceeds the detector's by more than 20, reveal is impossible.
- When it is lower by 20 or more, reveal is certain.
- Between players this is a fair relative contest. Against fixed-skill NPCs it becomes immunity:
  - Archer and Warrior guards have DH 100 (Mobiles/Guards/ArcherGuard.cs:64,159; WarriorGuard.cs:81,170).
  - They can never reveal a hider at 121 or higher. At Hiding 120 the chance is about 0.2 percent.
  - The shard boss SlasherOfVeils (DH 127.1) is likewise blind to Hiding 148 and higher.
- Creature AI (BaseAI) uses a different formula with a DH/10 floor, so monsters keep at least a 10 percent chance (for DH 100).

recommendation: cap the scan radius at 18, for example `Math.Min(DH/10, 18)`, or scale it as `10 + 8*(1-e^(-(DH-100)/200))`. Scale guard and NPC DH with the expected player cap, or give guards a floor chance as BaseAI already does. Above 100, new effects would fit better than a bigger radius, for example revealing stealth steps or longer trap visibility.

## Snooping

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Peek success | Skills/Snooping.cs:84 | CheckTargetSkill(0,100) | clamps at 100 | clamps | clamps | clamps | 100 |
| "You notice X peeking" | Skills/Snooping.cs:62-63 | only if snoop < 100 and snoop < rand*100 | clamps (never noticed at 100+) | clamps | clamps | clamps | - |

recommendation: let it scale (it is harmless). Possible new effect past 100: reduced trap trigger on snoop, or seeing the victim's bank or containers nested deeper.

## Stealing

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Single item steal | Skills/Stealing.cs:309 | CheckTargetSkill(iw-22.5, iw+27.5), iw = ceil(weight)*10 <= 100 | clamps at 127.5 (every item up to 10 st is certain) | clamps | clamps | clamps | 127.5 |
| Max item weight | Skills/Stealing.cs:24,33,254-256 | config stealing.maxWeightToSteal = 10 (unit weight + contents) | clamps | clamps | clamps | clamps | - |
| Stack amount | Skills/Stealing.cs:264-300 | amount = RandomMinMax(1, clamp(S/10/unitWeight)); check (pile*10-22.5, pile*10+27.5), so stolen pile weight is up to S/10 stones | scales: 12 st | BREAKS: 30 st | BREAKS: 50 st | BREAKS: 100 st | - |
| Gold (ML gold weight 0.02/3) | Items/Misc/Gold.cs:22 | max = S*15 gold per attempt | 1800 | 4500 | 7500 | 15000 | - |
| Caught | Skills/Stealing.cs:330 | caught = S < Random(150) | scales: 19.3 percent | BREAKS: 0 percent | BREAKS: 0 | BREAKS: 0 | - |
| Stealable artifacts | Skills/Stealing.cs:228 | S >= 100 | clamps | clamps | clamps | clamps | - |
| Faction sigil | Skills/Stealing.cs:182 | CheckTargetSkill(80,80) = gate at 80 | clamps | clamps | clamps | clamps | 80 |
| Pickpocket dips | Items/Addons/PickpocketDips.cs:61,85 | training dummy MinSkill/MaxSkill | clamps (exact max unverified) | | | | dip MaxSkill |

**Caught**
- At 150 or above (strictly > 149) a thief is never caught.
- That means no "You notice X trying to steal" broadcast and no CriminalAction from being caught.
- PermaFlags against innocent player victims still apply (Stealing.cs:406-411).

**Stacks**
- The configured 10-stone limit applies to the unit weight, not to the pile.
- Pinned skill (100) gives at most a 10-stone pile, so the two limits agreed. Above 100 the stack path bypasses the configured limit.
- Example at 300: a thief takes up to 300 iron ingots (30 stones) or 4500 gold per attempt.
- Example at 1000: up to 100 stones or 15000 gold, with at least a 45 percent success chance for any amount rolled. The skill is always at least pile-22.5, so the chance is >= 22.5/50.

recommendation:
- Cap the caught roll, for example `caught = Random(100) >= min(S, 100)*0.9`, or keep a floor like 5 percent.
- Cap the stack amount at maxWeightToSteal/unitWeight.
- Past 100, scale with diminishing returns: for example, a lower caught chance that approaches a 5 percent floor, or new effects such as stealing from equipped containers.

## Lockpicking

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Pick lock | Items/Skill Items/Thief/LockPick.cs:121,128 | gate LP >= RequiredSkill; CheckTargetSkill(LockLevel, MaxLockLevel) | scales (TMap L5 90..140: 60 percent) | clamps at 140 (always) | clamps | clamps | 140 |
| Lock data | Items/Containers/TreasureMapChest.cs:178-190 (Req 36-100, Lock Req-10, Max Req+40); Items/Containers/ParagonChest.cs:100-111 (same); Engines/Treasures of Tokuno/LesserArtifacts.cs:465-466 (95..140); Items/Containers/BaseTreasureChest.cs:88-97 (LockLevel up to 120, Max 100 so min >= max: gate 120 then certain); Items/Containers/LockableContainer.cs:31-38 (tinker-made <= 95); Multis/Camps/*.cs (Max 116) | | | | | | |
| Power generator | Items/Misc/PowerGenerator.cs:389,427-436 | 40 + rand*80 < LP | clamps at 120 | clamps | clamps | clamps | - |
| Puzzle chest hints | Engines/Khaldun/PuzzleChest.cs:589,618-647 | Base thresholds 60-100 | clamps | clamps | clamps | clamps | - |
| Remove Trap gate | Skills/RemoveTrap.cs:17 | LP >= 50 | clamps | clamps | clamps | clamps | - |

recommendation: let it scale (it clamps harmlessly at 140). Possible new effects past 140: faster picks, no lockpick breakage, or new higher-tier locks such as higher treasure-map levels.

## Remove Trap

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Disarm container trap | Skills/RemoveTrap.cs:61 | CheckTargetSkill(TrapPower, TrapPower+30) | scales | scales | scales | scales | TrapPower+30 |
| World TrapPower | TreasureMapChest.cs:176 (level*25), ParagonChest.cs:96 (level*25), LesserArtifacts.cs:471 (100), FillableContainer.cs:163 (level*10..30), Camps (30-40), TreasureChestLevel1-4 (up to 100), MagicTrap spell (10-50) | | certain on all of these at about 180 (TMap level 6 = 150+30; the maximum map level is unverified) | clamps | clamps | clamps | about 180 |
| Tinker-made traps | Engines/Craft/DefTinkering.cs:663-666 | TrapPower = (int)(Tinkering/10)*9 | vs Tinker 120: 108..138 | vs Tinker 300: 270..300 | 450..480 | 900..930 | 0.9*Tinkering+30 |
| Faction traps | Skills/RemoveTrap.cs:96-97 | CheckTargetSkill(80,100) and Tinkering(80,100), or ML owner | clamps at 100 | clamps | clamps | clamps | 100 |

- Remove Trap stays meaningful only as the counter to player tinker traps. There it scales one-to-one with the trapper's Tinkering.
- Cross-skill note for the Tinkering auditor (not a Remove Trap formula): tinker trap damage scales with TrapLevel = Tinkering/10 (Items/Containers/TrappableContainer.ExecuteTrap.cs:65,107).
  - Explosion trap: (10..30)*level, which is 300..900 fire damage at Tinkering 300 and 1000..3000 at 1000.
  - Dart trap: (5..15)*level.
  - Poison trap level is capped at 4 (ExecuteTrap.cs:128).
  - That is a BREAK in Tinkering.

recommendation: let it scale. Optionally add new effects past world-chest power (about 180), such as salvaging the trap or reduced damage when a disarm fails.

## Poisoning

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Apply poison | Skills/Poisoning.cs:124; potions: Lesser 0-60, Regular 30-70, Greater 60-100, Deadly/Darkglow/Parasitic 95-100 | CheckTargetSkill(min,max) | clamps at 100 (always) | clamps | clamps | clamps | 100 |
| Charges | Skills/Poisoning.cs:133 | 18 - 2*level (no skill term) | - | - | - | - | - |
| Self-poison on fail | Skills/Poisoning.cs:159 | Base < 80 and 5 percent | clamps | clamps | clamps | clamps | - |
| Infectious Strike max level | Items/Weapons/Abilities/InfectiousStrike.cs:55-64 | Darkglow min(P/33.3, 3); Parasitic min(P/25, 4); standard P/20 (Lethal = 4 at 80) | clamps at 100 | clamps | clamps | clamps | - |
| Infectious Strike +1 level | Items/Weapons/Abilities/InfectiousStrike.cs:67-68 | chance P/100 to apply Poison.IncreaseLevel | clamps at 100 (always) and BREAKS: see the bug below | BREAKS | BREAKS | BREAKS | - |
| Serpent Arrow | Items/Weapons/Abilities/SerpentArrow.cs:25 | Archery+P > 199.8 gives level 3 | clamps at sum 200 | clamps | clamps | clamps | - |
| Poison Field | Spells/Fifth/PoisonField.cs:124 | Magery+P > 199.8 gives level 3 | clamps | clamps | clamps | clamps | - |
| Poison spell | Spells/Third/Poison.cs:48-89 | Magery+P (SA: minus 31 per tile beyond 2; AOS: level 0 at dist >= 3); > 200 at dist <= 2 gives level 3, with 10 percent for 4 | clamps at sum 200 | clamps | clamps | clamps | - |
| Pet poison gain | Mobiles/BaseCreature.cs:2354 | CheckSkill(0, cap) | - | - | - | - | pet cap |

**IncreaseLevel bug (pre-existing, made certain by skill)**
- The code is `Poison.IncreaseLevel(p) = Poisons[p.Index + 1]` (Server/Poison.cs:51-52).
- `Index` is the registration id (0-4, 10-13, 20-24 in UOContent/Misc/PoisonKinds.cs:80-106). It is used as if it were a list position. With AOS and ML, the list is Lesser..Lethal (0-4), LesserDG..DeadlyDG (5-8), LesserPara..LethalPara (9-13).
- Results:
  - Lethal (4) becomes LesserDarkglow (list position 5): a downgrade from level 4 to level 0.
  - LesserDarkglow (10) becomes GreaterParasitic.
  - RegularDarkglow (11) becomes DeadlyParasitic.
  - GreaterDarkglow (12) becomes LethalParasitic: a family jump to level 4 that heals the attacker.
  - DeadlyDarkglow and all Parasitic poisons do not change.
- At Poisoning 100 and above this happens on every Infectious Strike. For Lethal weapons it is a guaranteed downgrade. For Darkglow weapons it is a guaranteed jump to Parasitic.
- The same IncreaseLevel call makes Paragon HitPoison wrong (Mobiles/BaseCreature.cs:2345).

recommendation:
- Fix IncreaseLevel so it looks up the same family at level+1, which the existing GetPoisonByFamilyAndLevel in PoisonKinds.cs:59 can do.
- Otherwise Poisoning clamps at 100 everywhere.
- Possible new effects past 100: more charges per dose, for example `18-2L + (P-100)/50`, or a chance to not consume a charge. Do not raise the poison level: it is hard-capped at 4 by the families.

## Healing (Bandage, Healing+Anatomy; Veterinary+AnimalLore on pets)

Numbers assume Anatomy equals Healing. With Anatomy at 120 and only Healing raised, see the parenthesized values.

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Heal success | Items/Skill Items/Misc/Bandage.cs:377 | (H+10)/100 - 0.02*slips | clamps (100 percent at 90) | clamps | clamps | clamps | 120 |
| Heal amount (AOS) | Bandage.cs:387-396 | min = A/8 + H/5 + 4; max = A/6 + H/2.5 + 4; minus 35 percent per slip | 43..72 (avg 58) | BREAKS: 102..174 (avg 138) (A120: 79..144) | BREAKS: 167..287 (avg 227) (A120: 119..224) | BREAKS: 329..571 (avg 450) (A120: 219..424) | 120 |
| Cure | Bandage.cs:321-322 | (H-30)/50 - 0.1*poisonLevel - 0.02*slips; needs H, A >= 60 | clamps (Lethal certain at 100; at 120 slip-proof to 20 slips) | clamps | clamps | clamps | 120 |
| Resurrect | Bandage.cs:239-240 | (H-68)/50 - 0.02*slips; needs H, A >= 80 | clamps (certain at 118) | clamps | clamps | clamps | 120 |
| Delay, self (AOS) | Bandage.cs:493 | 5 + 0.05*(120-Dex), Dex only | Dex 150: 3.5 s | Dex 220: 0 s | Dex 500: -14 s | - | - |
| Delay, others (AOS) | Bandage.cs:506-512 | Dex < 204: 3.2 - sin(Dex/130)*2.5; otherwise 0.7 s | | | | | |
| Delay, pet (Vet) | Bandage.cs:500-502 | 2.0 s fixed | | | | | |
| Gain | Bandage.cs:442-445 | CheckSkill(primary, 0, 120), CheckSkill(secondary, 0, 120) | | | | | 120 |
| Creature self-heal (NPC/pet skill) | Mobiles/BaseCreature.cs:5366-5408 | min = A/10 + H/6 + 4; max = A/8 + H/3 + 4 (+10 on self) times HealScalar; gain 90 / 60+10*level | scales (pet skill caps limit it) | | | | 90 |
| Hireling cost | Mobiles/Hireables/BaseHire.cs:140 | sum/35 | cosmetic | | | | |
| Faction guard heal gate | Engines/Factions/Mobiles/Guards/GuardAI.cs:572 | Base > 20 | cosmetic | | | | |

**Runaway healing.** Healing has no cap other than HitsMax.
- Healing on another player:
  - The healer can reach Dex 204 because the shard individual stat cap is 500, which gives a 0.7 s delay.
  - At 300/300 that is about 138 HP per 0.7 s, roughly 197 HP/s.
  - At 1000/1000 it is about 640 HP/s.
- Self-healing:
  - At Dex 220 the delay reaches 0 s, and at higher Dex it goes negative (Dex 500 gives -14 s).
  - A Timer with a negative delay should fire on the next tick (unverified), so self-bandages become about as fast as the player can click and target. There is no other rate limit in Bandage.cs.
  - The delay is a Dex issue, not a Healing issue, but it multiplies the Healing break.
- For scale: a full AOS player (Str 150, +25 HP) has about 150 HitsMax (unverified for the shard's 500 Str cap). At 300 Healing, one bandage refills most of a bar.

recommendation:
- Soft-cap the heal amount with diminishing returns past 120, for example `bonus = 120-value + 60*ln(1 + (H-120)/120)`, which gives about 1.6x the 120 amount at 300 and about 2.5x at 1000.
- Or cap it as a percent of HitsMax per bandage.
- Clamp the self-bandage delay to at least 2 s and the other-target delay to at least 0.7 s, regardless of Dex.
- Possible new effects past 120: heal-over-time, removing debuffs (Mortal Strike), or area bandaging.

## Veterinary

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Pet heal amount | Bandage.cs:387-401 | same as Healing with Vet/AnimalLore, + HitsMax/100 | 43..72 + HitsMax/100 | 102..174 (about 69 HP/s at 2 s) | BREAKS: 167..287 (about 113 HP/s) | BREAKS: 329..571 (about 225 HP/s) | 120 |
| Pet cure / resurrect / success | Bandage.cs:239-240, 321-322, 377 | same as Healing | clamps | clamps | clamps | clamps | 120 |
| Delay | Bandage.cs:500-502 | 2.0 s fixed | | | | | |
| Stable slots | Mobiles/Vendors/NPC/AnimalTrainer.cs:58-97 | +(int)((V-90)/10) when V >= 100 (Taming and Lore give the same) | +3 | +21 | +41 | +91 (about 278 total with Taming and Lore at 1000) | - |

- Pet healing has a fixed 2 s delay and no Dex term.
- At 500 and above, one tamer keeps a high-HitsMax pet (dragon class) effectively unkillable outside burst damage.
- Stable slots scale linearly. That is a save/storage concern, not an exploit.

recommendation: use the same diminishing-returns heal curve as Healing. Optionally cap stable slots, for example a total of 15-20. Possible new effects past 120: pet buffs, or faster pet resurrection without skill loss (Bandage.cs:272-275 currently costs the pet 0.1 in every skill).

## Begging

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Beg success | Skills/Begging.cs:111 | CheckTargetSkill(0,100) | clamps at 100 | clamps | clamps | clamps | 100 |
| Gold amount | Skills/Begging.cs:113-118 | min(theirGold/10, clamp(10 + Fame/2500, 10, 14)); no skill term | clamps | clamps | clamps | clamps | - |
| Trick or Treat | Holiday Stuff/Halloween/2006/Engines/TrickOrTreat.cs:203 | Begging >= 100 gate, 1 percent | clamps | clamps | clamps | clamps | - |

recommendation: let it scale (it has no effect past 100). If the skill should matter, give it new effects past 100, for example a better gold cap or NPC vendor discounts.

## Forensic Evaluation

| Use | file:line | formula | 120 | 300 | 500 | 1000 | gain ceiling |
|---|---|---|---|---|---|---|---|
| Identify thief | Skills/ForensicEval.cs:36 | CheckTargetSkill(40,100) | clamps at 100 | clamps | clamps | clamps | 100 |
| Corpse info (killer, looters) | Skills/ForensicEval.cs:54 | CheckTargetSkill(0,100) | clamps | clamps | clamps | clamps | 100 |
| Other reads | Misc/AOS.cs:1082 (name only); healer NPC teach lists | cosmetic | | | | | |

recommendation: let it scale (it is harmless and stops having any effect past 100). Possible new effects: detecting hidden thieves nearby, or extra corpse data such as the time of death.

---

## BREAKS list

1. **Hiding, hide in combat.** The range goes to 0 at 116 and negative from 118: (int)((100-H)/2)+8 gives -2, -92, -192 and -442 at 120, 300, 500 and 1000. From 118 on, combatants never block the hide, so you can hide while being hit. Skills/Hiding.cs:53-71.
2. **Detect Hidden scan radius.** The radius is DH/10 tiles: 30, 50 and 100 at 300, 500 and 1000. It reveals hiders and traps far off screen, and at 1000 runs a 201x201 mobile and item scan. Skills/DetectHidden.cs:153,198,223.
3. **Detect Hidden vs Hiding contest (+/-10).** It gives total immunity once Hiding is more than DH+20. Guards (DH 100) can never reveal Hiding 121 or higher. SlasherOfVeils (127.1) can never reveal Hiding 148 or higher. Skills/DetectHidden.cs:205-208. BaseAI keeps a DH/10 floor, so monsters are fine.
4. **Stealing, never caught.** The rule is caught = S < Random(150), so from 150 on the thief is never caught: no broadcast and no criminal flag from being caught. Skills/Stealing.cs:330.
5. **Stealing, stack size.** The cap is S/10/unitWeight. That bypasses stealing.maxWeightToSteal=10, allowing 30, 50 and 100 stones per theft and up to 4500, 7500 and 15000 gold per attempt at 300, 500 and 1000. Skills/Stealing.cs:264-300.
6. **Healing amount.** The heal amount has no cap. Average heal is 138, 227 and 450 HP per bandage at 300, 500 and 1000 (Healing=Anatomy). With the shard's Dex cap of 500, the other-heal delay is 0.7 s (about 197 to 640 HP/s). The self-heal delay reaches 0 s at Dex 220 and goes negative above that (Dex-driven; timer behavior unverified). Bandage.cs:387-396, 493, 506-512.
7. **Veterinary.** The pet bandage delay is a fixed 2 s, giving about 113 and 225 HP/s at 500 and 1000. Bandage.cs:387-401, 500-502.
8. **Poisoning, Infectious Strike.** The level-up fires at chance P/100, so it is certain at 100 and above. Poison.IncreaseLevel uses Index+1 as a list position, so Lethal turns into LesserDarkglow and GreaterDarkglow turns into LethalParasitic. This is a pre-existing bug that skill makes deterministic. Items/Weapons/Abilities/InfectiousStrike.cs:67; Server/Poison.cs:51-52.
9. **Stealth steps (mild).** At 1000 there are 200 steps, which allows 100 running tiles while hidden. Skills/Stealth.cs:102; Mobiles/PlayerMobile.cs:3527-3531.

Cross-skill, for the Tinkering audit: tinker trap damage is (10..30)*(Tinkering/10), which is 1000..3000 at Tinkering 1000 (Items/Containers/TrappableContainer.ExecuteTrap.cs:65). Remove Trap is the only counter.
