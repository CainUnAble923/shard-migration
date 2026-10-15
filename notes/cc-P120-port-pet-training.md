# cc-P120: Port list, Pet Training (OSI animal training), in full

2026-10-15. Prompt: `D:\UO\cc-prompts\cc-P120-port-pet-training.md`. Both repos were clean at the start (P119 committed
as 537993b). **Stopped after the survey, before porting anything:** three facts change what the 2026-10-13 "port it
fully" decision was weighing, and two architecture choices fix the save format for P120 and P121. Nothing was ported
and no repo file was changed except this note.

## Headlines

- **The patch surface is about twice the figure the earlier decisions used.** `docs/subsystem-policy.md` (2026-09-07)
  and `docs/patch-backlog.md` row P6 say "six or seven upstream patches". A full port touches **about 13 upstream
  files**:
  - `BaseCreature.cs`: about 10 separate hunks;
  - `AOS.cs`, which already carries 4 shard patches;
  - AnimalTaming, AnimalLore, SkillCheck, MageAI, Discordance, BaseInstrument;
  - SpecialMove and six weapon abilities;
  - SamuraiSpell, PlayerMobile and AnimalTrainer.

  The full list is below.
- **Pinned already has a monster-ability system, and it collides with ServUO's on tameable stock creatures.**
  - Pinned's `Mobiles/Abilities/` (`MonsterAbilities`, about 30 files) gives breath, claws and the like to 57 stock
    creature files. 18 of them are tameable: Dragon, Drake, GreaterDragon, Nightmare, FireSteed, HellCat,
    PredatorHellCat, HellHound, LavaLizard, Reptalon, Hiryu, LesserHiryu, Slith, StoneSlith, BakeKitsune, RuneBeetle,
    and others.
  - ServUO expresses the same abilities through Pet Training's `SpecialAbility` and `AreaEffect`, so a straight port
    gives a tamed stock Dragon **no** natural abilities in its profile.
  - Training could then add `DragonBreath` on top of pinned's `FireBreath`: two breaths.
  - Seven ServUO abilities have a pinned twin: DragonBreath to FireBreath, GraspingClaw, TailSwipe, RuneCorruption,
    ColossalBlow, LifeLeech to DrainLifeAttack, and AuraDamage to HasAura.
- **It does not fit one prompt.**
  - ServUO's `Services/Pet Training/` is 11 files and 8,664 lines, counted. 1,918 of those are gumps, which need
    rewriting for pinned's gump API.
  - On top of that come the ~13 upstream patches and a save-format decision.
  - The training half also needs OSI's variable control slots (`ControlSlotsMin/Max`, `CanLowerSlot`), which pinned
    has none of.
- **What it unblocks, counted** (ServUO `Mobiles`, `Services` and `Quests`, excluding Pet Training itself and
  BaseCreature): **161 files** call `SetSpecialAbility` (109), `SetAreaEffect` (29), `SetMagicalAbility` (23) or
  `PetTrainingHelper` (17). Files overlap, so the per-method counts sum past 161.

## The decisions needed

**1. The two ability systems.**
- **(a) Recommended: one ability set, pinned's where it has one.**
  - The seven abilities that have a pinned twin run through the pinned class.
  - The rest are ported from ServUO.
  - A creature's profile also reads its stock `GetMonsterAbilities()`, so a tamed Dragon shows its breath once and
    trains with it counted.
  - This is the AGENTS.md "equivalents hide under different names" rule, and how D-55/D-56/D-62/D-68 were resolved.
  - **Cost:** about 7 small adapters. A pinned bump that changes a monster ability changes the pet's too.
- **(b) Faithful in structure: port ServUO's system whole, beside pinned's.**
  - Simpler to port.
  - Stock creatures show no natural abilities in Animal Lore and can stack a trained breath on a built-in one. A
    player reading UOGuide would see the difference.

**2. Where a creature's profile is saved.**
- **(a) Recommended: a side table we own**, keyed by creature serial, in its own save file through ModernUO's generic
  persistence.
  - Zero change to `BaseCreature`'s save format; no migration.
  - A pinned bump cannot conflict with it.
  - Entries are removed when the creature is deleted. Stabling and transfer keep the serial, so the profile follows.
  - **Cost:** the profile lives beside the creature, not in it, so a world restored without our save file loses
    profiles (wild abilities are re-set by constructors only for new spawns).
- **(b) In the creature:** patch `BaseCreature`'s generated serialization from version 24 to 25, adding the two
  profiles and `ControlSlotsMin/Max`.
  - This is ServUO's shape, and every creature in every save takes the bump.
  - If upstream bumps `BaseCreature` to 25 for its own reasons, the patch fails at the next pinned bump and has to be
    reconciled by hand. The build gate catches it.

**3. Split into two prompts** (recommended):
- **P120a, the ability core:**
  - profiles, `SpecialAbility`, `AreaEffect`, `MagicalAbility` and weapon-ability masteries;
  - the `Set*Ability` hooks creatures call;
  - the combat, think and approach triggers, regen and poisoning;
  - MageAI spell choice, and storage per decision 2.
  - **This alone unblocks P121.**
- **P120b, training itself:**
  - training points and progress, planning, the training gumps and the Animal Lore additions;
  - the AnimalTrainer NPC, `ControlSlotsMin/Max` with slot lowering, and the Ethologist title deed;
  - the pet training gate.

Either order works; P121 needs only P120a.

**4. Evo pets and companions** (no choice needed unless Chase disagrees). EvoPet (`C/Mobiles/Evo/EvoPet.cs`, cc-P65) is
its own BaseCreature with its own XP and an empty abilities slot. Training would be **off for it**: no training
definition for its type, so it gains no points, shows no training pages, and its control slots stay 1. That keeps P65
exactly as now. Companions and squires (P41) are the same: excluded by type.
- **Stable slots** past OSI's top are the shard's `ClusterFSkillClamps` (`StableSlotsPerSkillAt200`). OSI training
  does not touch stable slots, so there is no meeting point.
- **Animal Lore to 200:** OSI training gives Animal Lore nothing above 120 directly. Its "can train this pet" gate is
  Animal Taming and Animal Lore skill against the pet's level, capped at OSI values. It adds **no** high-level
  tameables. So Chase's 2026-10-06 gap (needs high-level tameables or a quest) stays open after either half; P120b
  would only add one more use of the skill.

**To answer:** decision 1 (a or b), decision 2 (a or b), and "split" or "one prompt". The overseer can then queue P120a
and P120b.

## The surface, counted

**ServUO `Scripts/Services/Pet Training/`**, line counts from `wc -l`:

| File | Lines | Goes to |
|---|---|---|
| SpecialAbility.cs | 2,688 | P120a (30 abilities) |
| Gumps.cs | 1,918 | P120b |
| PetTrainingHelper.cs | 1,778 | both: per-type definitions and costs (b); profile access (a) |
| AbilityProfile.cs | 759 | P120a |
| AreaEffects.cs | 596 | P120a (7 effects) |
| TrainingProfile.cs | 442 | P120b |
| PetTrainingGate.cs | 185 | P120b |
| PlanningProfile.cs | 161 | P120b |
| TrainingPoint.cs | 55 | P120b |
| TrainingDefinition.cs | 51 | P120b |
| EthologistTitleDeed.cs | 31 | P120b |
| **total** | **8,664** | |

**ServUO's ability enums**, from the source:
- SpecialAbility: 30;
- AreaEffect: 7, namely AuraOfEnergy, AuraOfNausea, EssenceOfDisease, EssenceOfEarth, ExplosiveGoo, AuraDamage and
  PoisonBreath;
- MagicalAbility: a flags enum of 16 single-bit abilities (Piercing through Magery, `PetTrainingHelper.cs:67-84`),
  plus composite masks per creature family (Tokuno, Dragon1, Wolf and others, `:86-100` onward).

**Upstream files a full port patches.** Training references were counted in each ServUO file; the right-hand column is
the pinned file and whether the shard already patches it:

| ServUO file | refs | What it hooks | Pinned file / shard patches |
|---|---|---|---|
| Mobiles/Normal/BaseCreature.cs | 92 | profiles and their save, Set*Ability, regen x3, AI-type magic, taming slots, poisoning, approach and think triggers, ColossalBlow, discordance, stat loss | `Mobiles/BaseCreature.cs` / 1 (auto-stable) |
| Misc/AOS.cs | 13 | damage-time ability triggers and modifiers | `Misc/AOS.cs` / **4** |
| Mobiles/PlayerMobile.cs | 6 | pet-related player hooks | `Mobiles/PlayerMobile.cs` / 5 |
| Skills/AnimalTaming.cs | 5 | slots and profiles on tame | `Skills/AnimalTaming.cs` / 0 |
| Spells/Base/SpecialMove.cs | 4 | pet weapon masteries | yes / 0 |
| Skills/Discordance.cs | 4 | pet discordance | yes / 0 |
| Mobiles/NPCs/AnimalTrainer.cs | 4 | training at the trainer | `Mobiles/Vendors/NPC/AnimalTrainer.cs` / 0 |
| Skills/AnimalLore.cs, Misc/SkillCheck.cs, MageAI.cs, BaseInstrument.cs, SamuraiSpell.cs | 2 each | Lore gump entry, gains, spell choice, pet bard, pet Bushido | each exists / 0 |
| Abilities/NerveStrike, TalonStrike, Block, Feint, Bladeweave, FrenziedWhirlwind | 1 each | mastery checks | each exists / 0 |

**Hook points pinned lacks entirely:** `ControlSlotsMin`, `ControlSlotsMax`, `CanLowerSlot` and an `OnAfterTame` hook
(grep of pinned UOContent: no hits). `AnimalTraining`'s slot lowering needs all four.

## What was ported

Nothing. The survey above is the whole of this run.

## Port-list numbers

Unchanged: Pet Training 0 of 11 (`tools/port-list.json`). The Creatures row is 109 of 193 after P119.

## Deviations and decisions for Chase

1. Decisions 1 to 3 above, plus a nod on 4.
2. **The 2026-09-07 "wait" decision in `docs/subsystem-policy.md` should be marked superseded** by Chase's 2026-10-13
   call, by whoever edits `docs/`. Its stated trigger has happened: pinned `BaseCreature` is on the SerializationGenerator
   (`[SerializationGenerator(24, false)]`, `Mobiles/BaseCreature.cs:137`). Its patch count (six or seven) should be
   corrected to about 13, as measured here.
3. **P121 (creatures part 2) depends on this.** If P120 waits, P121 should wait too; the Golem would otherwise hand it
   over next.

## For Chase

Nothing to try in game yet. Answer decisions 1 to 3 (I recommend 1a, 2a, split) and the port can be queued as P120a
and P120b. P121 can run after P120a.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo Result
---- ------
code clean
docs dry run
```

code: nothing pending. docs: this note only.

P120 STOPPED: needs Chase
