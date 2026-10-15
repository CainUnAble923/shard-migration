# cc-P121: Pet Training part 1, the ability core

2026-10-15. Prompt: `D:\UO\cc-prompts\cc-P121-pet-ability-core.md` (handed by the Golem). Both repos were clean at the
start apart from `notes/cc-P120-port-pet-training.md`, P120's own stopped-run note, which the Golem does not commit on
STOPPED; it goes in with this commit. Built on Chase's answers to P120: 1a (one ability set), 2a (side table), split.

## Headlines

- **Ported: the whole ability core.** ServUO's 29 special abilities, 7 area effects, the MagicalAbility schools, the
  AbilityProfile and the profile half of PetTrainingHelper, in `server/customizations/Services/Pet Training/` (7 files,
  3,396 lines), plus `SpiderWebbing` (Webbing's web). Creatures can call `SetSpecialAbility`, `SetAreaEffect` and
  `SetMagicalAbility` exactly as their ServUO source does (a `partial class BaseCreature`, no patch). **P129 can run.**
- **The brief's "30 special abilities" is 29.** ServUO's table is `new SpecialAbility[29]` (`SpecialAbility.cs:236-268`),
  counted; P120's survey carried the 30. The area effects are 7, as stated.
- **Decision 1a, built.** Seven abilities run through pinned's classes: DragonBreath (FireBreath, with ServUO's per-type
  breath table carried onto it), GraspingClaw, TailSwipe, RuneCorruption, ColossalBlow, LifeLeech (DrainLifeAttack),
  AuraDamage (HasAura/AuraDamage). **An eighth found: Heal**, whose ServUO body calls `CheckHeal`, pinned's
  `CanHeal`/`HealStart`; same rule, same treatment. A stock creature's profile lists its natural twins (a Dragon shows
  Magery and DragonBreath, once); the profile never dispatches a natural twin, so pinned's pipeline is the only one that
  fires it. Natural abilities are computed from the creature, never stored.
- **Decision 2a, built.** Profiles live in `AbilityProfileStore`, a `GenericPersistence` side table (`Saves/PetAbility
  Profiles/PetAbilityProfiles.bin`), keyed by creature, removed on `CreatureDeletedEvent`. BaseCreature's save format is
  untouched. A natural-only profile is never written.
- **Five upstream patches**, each one or two calls into `PetTrainingHooks.cs`: BaseCreature (4 hunks), AOS (3),
  SpellHelper (2), Bandage (1), MageAI (1). 42 lines added, 5 removed in all. Plus our `RegenRates.cs` replacement.
- **One player-visible change today:** a tamed poisoner now poisons by its Poisoning skill (ServUO/OSI pet rules), and
  poison hits show TOL's green flash. Everything else waits for creatures that use it (P129) or training (P130).
- **Gates:** 62 new facts, every one seen failing under deliberate breaks (three break sets, below); the gated build
  green at 1,234 shard facts; the full server suite green; the test world booted, saved the new file and read it back.
- **Found in passing, not mine:** the test host never registers poisons, so `Poison.Lethal` etc. are null there and
  several existing facts that compare poisons pass vacuously. Now fixable with `ShardTestHost.EnsurePoisons()` (added).

## What was ported

| ServUO file | Ours | Lines (ServUO -> ours) | Notes |
|---|---|---|---|
| `Services/Pet Training/SpecialAbility.cs` | same path | 2,688 -> 1,662 | 22 abilities line for line; 7 twins as adapters |
| `Services/Pet Training/AreaEffects.cs` | same path | 596 -> 425 | 6 line for line; AuraDamage twin; AuraDefinition table not ported (below) |
| `Services/Pet Training/AbilityProfile.cs` | same path | 759 -> 831 | natural abilities added; save by name |
| `Services/Pet Training/PetTrainingHelper.cs` | same path | 1,778 -> 121 | MagicalAbility enum, Enabled, GetAbilityProfile, MagicalAbilities, RuleBreakers only |
| `Items/Functional/SpiderWebbing.cs` | same path | forced leaf dependency of Webbing | |
| (ServUO BaseCreature.cs:577-678) | `Pet Training/BaseCreature.PetTraining.cs` | 37 | partial class: AbilityProfile, Set*/Remove*/HasAbility |
| (new) | `Pet Training/AbilityProfileStore.cs` | 124 | decision 2a |
| (new) | `Pet Training/PetTrainingHooks.cs` | 196 | everything the patches call |

**Left, with the reason:**
- **The training half (P130):** TrainingProfile, PlanningProfile, TrainingPoint/Definition, Gumps, PetTrainingGate,
  EthologistTitleDeed, the per-family ability tables and `Class`, AnimalTrainer, AnimalTaming (OnTame, slots), the
  Animal Lore additions, ControlSlotsMin/Max. In AbilityProfile, `OnAddAbility`'s TrainingPoint requirements are a
  marked seam for P130.
- **SetWeaponAbility** is deliberately not added: pinned's combat reads `GetWeaponAbility()`, so a profile-only
  SetWeaponAbility would compile and do nothing. Ports keep the recipe's `GetWeaponAbility` override. Trained weapon
  abilities need that read point: P130.
- **Skill masteries** (the five weapon-mastery schools' casting, `BaseCreature.Mastery`/`CheckCastMastery`): pinned has
  no skill-mastery system at all (no `MasteryInfo`, no `SkillMasteryMove`). The schools are stored and the mastery skill
  kept on the profile, inert.
- **AI types:** Bushido, Ninjitsu, Mysticism, Spellweaving, Chivalry, Necromage and Necromancy switch a tame to AI
  pinned lacks (AIType.cs has 10 values). Those schools leave the AI as is; Bushido and Ninjitsu still add their
  weapon ability to the profile, as ServUO does.
- **Pet discordance, pet Bushido/Ninjitsu skill gains** (Discordance.cs, BaseInstrument, SamuraiSpell, the six weapon
  abilities' `OnWeaponAbilityUsed`): all gated on training; P130 or later.
- **ServUO's AuraDefinition table** (Cora, fire and cold auras): in pinned each such creature states its aura through
  the Aura* virtuals, as batch 3's FireDaemon does, so a table would duplicate it.
- **Stock pinned creatures that ServUO gives an ability pinned dropped** (not twins: e.g. a stock creature ServUO
  constructs with Webbing) are not restored: decision 1a says a profile reads *stock* abilities. Restoring them is a
  per-type table; unmeasured, a follow-up.

## Upstream files patched

Applied after `Imbue-custom-property-hooks.patch`, in this order, each with its own line and comment in
`docker/uo/apply-patches.sh`. Generated against the fully patched builder tree of `sl-uo-builder:cc-p119`, so they
meet the existing patches as they stand; all applied at `--fuzz=0`.

| Patch | Pinned file | Hunks | What | Meets |
|---|---|---|---|---|
| `BaseCreature-pet-ability-hooks.patch` | Mobiles/BaseCreature.cs | 4 | OnThink: think triggers first; OnMovement: approach trigger; OnGaveMeleeAttack: trained hit poison (ServUO GetHitPoison/TryHitPoison, the poisoning gain gate, TOL's flash) and Colossal Rage's blow | the CanAutoStable patch, far from these lines |
| `AOS-pet-ability-triggers.patch` | Misc/AOS.cs | 3 | AOS.Damage: take the damage type on entry; the combat trigger just before `if (totalDamage <= 0)`, after our damage-eater hook (ServUO's own order); GetValue: the debuff penalties before `return value` | the 4 existing AOS patches: after damage-eater's block, after pet-mimic's `PetMimic` branch; set-attribute and stat-bonus touch other lines |
| `SpellHelper-pet-ability-hooks.patch` | Spells/Base/SpellHelper.cs | 2 | mark the pair before the AOS spell path's AOS.Damage; Searing Wounds in Heal | after Imbue's Spell Leech line, which it sits beside |
| `Bandage-searing-wounds.patch` | Items/Skill Items/Misc/Bandage.cs | 1 | Searing Wounds halves a bandage heal | after Bandage-heal-scaled-200 and pet-mimic-targeting |
| `MageAI-pet-magery-mastery.patch` | Mobiles/AI/MageAI.cs | 1 | SmartAI also for the Magery Mastery school | none |

**Alternatives argued (AGENTS.md: before patching an upstream file):**
- *The combat trigger through pinned's own `TriggerAbility`/`AlterMeleeDamage` virtuals instead of AOS.Damage.* Rejected:
  those see pre-resist damage, and Repel (half back, hit cancelled) and StealLife use the damage after resists, which only
  AOS.Damage has. ServUO puts it in AOS.Damage; so do we.
- *A damage-type parameter on AOS.Damage.* Rejected: it changes a signature with dozens of callers. ServUO's callers leave
  it at Melee except SpellHelper; so SpellHelper marks the (from, to) pair in a thread-static and AOS.Damage takes the
  mark on entry, before any early return, so it cannot outlive its call.
- *Marking spell damage in BaseCreature.AlterSpellDamageTo/From.* Rejected: creatures that override them without calling
  base would silently lose the mark.
- *Overriding OnThink/OnMovement from customizations.* Impossible: they are BaseCreature's own methods; a partial class
  cannot override its own type.
- *Regeneration through a patch.* Not needed: `RegenRates.cs` is already our replacement.
- *Profiles in BaseCreature's save (decision 2b).* Chase chose 2a.

## What changed, file:line

- `customizations/Services/Pet Training/SpecialAbility.cs`: `CheckCombatTrigger` :74-129 (with the precedence fix and the
  depth guard), `CheckThinkTrigger` :131, `CheckApproachTrigger` :166; the table :245-278; the twins from :331
  (`PinnedTwinAbility`, `DragonBreathDefinitions` with ServUO's per-type breaths, `HealTwin`); the 22 ports after.
- `AreaEffects.cs`: base and dispatch, then the six, then `AuraDamageTwin` at the end.
- `AbilityProfile.cs`: natural abilities (`GetNaturalMagicalAbility`, `EnumerateNatural*`, `HasMagicalAbility`), the
  ServUO members, `IsEmpty`, `Serialize`/`Deserialize` (by name; an unknown name is dropped, not fatal).
- `AbilityProfileStore.cs`, `PetTrainingHooks.cs`, `BaseCreature.PetTraining.cs`, `Items/Functional/SpiderWebbing.cs`: new.
- `customizations/RegenRates.cs`: the profile's RegenHits/Stam/Mana, beside the paragon bonus in each handler.
- `docker/uo/apply-patches.sh`: five apply lines with their comment, after Imbue's.
- `server/tests/Route/ShardTestHost.cs`: `EnsurePoisons()`.

## Tests

`server/tests/Services/PetTraining/PetAbilityCoreVerification.cs`, **62 facts**:
- the tables (29 and 7, ServUO's order, the twins);
- **one fact per special ability (29) and per area effect (7)**, each asserting its effect on a sample creature;
- each trigger the patches add: a hit given (AOS.Damage), a melee ability in cooldown not picked (the fix), spell damage
  told apart from melee (Mana Drain never fires on 300 spells, then does on melee), Repel cancelling a spell, a think
  firing an area effect and Heal, an approach firing True Fear (and not a move inside range), a tamed spider's
  skill-scaled Lethal poison through OnGaveMeleeAttack, MageAI SmartAI from Magery Mastery, the regeneration bonus
  through `RegenRates` (by reflection, so the host's regeneration is not changed for other facts);
- the twins: seven stock creatures (Dragon, Hiryu, StoneSlith, RuneBeetle, Juggernaut, Kappa, CuSidhe) list their twin
  once and never dispatch it, setting it again stores nothing; a tamed Dragon has one breath, through pinned only; Pyre's
  aura is the natural AuraDamage; a Dragon's profile reads Magery, DragonBreath and a GiantSpider's Poisoning;
- storage: save and load, stabling (as AnimalTrainer does it) and transfer with saves between, a deleted creature's entry
  gone, a natural-only profile not written, a save folder without the file loading nothing (through the real file path);
- evo pets and pack mules: no stored profile through fights and thinks; looking makes an empty one.

**Seen failing first**, three deliberate break sets on a copy of the build tree (`breaks.py`, scratchpad), each a
fast run of the class in the builder image:
- **A, every hook removed** (combat, think, approach, poison, MageAI, GetValue, spell heal, RegenRates), the twin rule
  off, the store writing nothing and ignoring deletes, two table entries swapped: **27 of 62 failed**, every fact aimed
  at those, including the regen fact (`2s -> 2s`) and the poisoner (`with Regular`).
- **B**, the spell mark removed, ServUO's precedence restored, IsEmpty never true, a load that clears the table, and
  OnThink making profiles: **12 failed**, all five targeted facts among them (the twins theory too, through IsEmpty).
- **C, every ability's effect emptied:** **39 failed**: all 29 special-ability facts, all 7 area-effect facts, and the
  three dispatch facts that need an effect.

Two real defects in my own facts, found on the way: the first origin (x 1400) was off Ter Mur's 1280 width, so every
range search found nothing; and the host's players are Young and its poisons null (above). Both fixed in the facts.

**Gated builds** (`docker/uo/build.sh -t sl-modernuo:cc-p121`, all three gates), four in all:
1. **Green, 1,234 of 1,234** (P119's 1,172 + 62), image built. Re-run twice in the builder: 1,234/1,234 both times.
2. **Red, 2 of 1,234 failed**, after I made `BaseCreature.AbilityProfile` create a profile (so `[props` shows a stock
   creature's natural abilities): my evo-pet fact (the evo pet died during its 50-hit loop, was deleted, and a deleted
   creature has no profile; it is now kept alive) and `WispOrbPossessionVerification`'s Silenii-vs-Naba case. **The Wisp
   Orb case is a flake on the base, not this change:** P119's own builder failed it 2 times in 8 full-suite runs here
   (ForestNymph and Silenii, both against Naba), and `LootBoxFanfareVerification.ContentsAreRolledAtEarn...` once in
   the same 8. This tree failed it 1 time in 5. Neither touched; both for the overseer's bug list.
3. **Green, 1,234 of 1,234**, image built. Then I found my changelog edit had swallowed P119's `## 2026.10.15.5` header,
   which would have merged its notes into this version's in the login bulletin. Restored.
4. **Final: green, 1,234 of 1,234, image `sl-modernuo:cc-p121` built** from exactly this tree.

**Full server suite, unfiltered**, in the same builder (`dotnet test ModernUO.slnx`, seccomp unconfined, no network):
- `Server.Tests.dll`: 910 total, **893 passed, 0 failed**, 17 skipped;
- `UOContent.Tests.dll`: 2,421 total, **2,330 passed, 0 failed**, 91 skipped (P119: 2,268 of 2,359; +62).

**Not mine, recorded:** P119's own builder, re-run here, failed 1 of 1,172 shard facts once and passed 1,172 the next
time; I did not catch which fact. A flake on the base, unidentified. And the 109-110 "Corpse ... amount of 0" log lines
in every suite run are on P119's build too (109), not from these facts (0 in this class alone).

**The test shard boots clean.** `sl-modernuo:cc-p121` (first build) on a copy of the test world's newest automatic
backup (`Backups/Automatic/2026-10-15-16-50-00`, a world saved before this change, with no PetAbilityProfiles file):
- boot 1: `Loading world done (207033 items, 35052 mobiles) (3.14 seconds)`, listening; stopped (SaveOnShutdown):
  `Saving world done`, and `PetAbilityProfiles/PetAbilityProfiles.bin` written, 2 bytes (version 0, no entries: no
  creature in the world has a stored profile yet);
- boot 2 on that save: `Loading world done (207892 items, 35119 mobiles)`, no error, saved again on stop;
- boot 3, the final image (build 4) on the same scratch world: `[ShardVersion] Shattered Legacy 2026.10.15.6 (58
  version(s) in the changelog)`, `Loading world done (210014 items, 35273 mobiles)`, no error, saved on stop.
- The one ERR line in both is my scratch config listening on 2593 with Test Center on (the live-port guard). Not code.
- **Unverified:** a non-empty profile file through the real save path. The facts round-trip entries through the same
  Serialize/Deserialize with pinned's BufferWriter/BufferReader; the first real entries arrive with P129's creatures.
  The shard's console did not take piped `save` here; `docker stop` (SaveOnShutdown, D36) did the save.

## Port-list numbers

`tools/progress.py --dry-run`, before (HEAD, after P119) and after (this tree):

| | before | after |
|---|---|---|
| Pet Training row | 0 / 11 | **4 / 11** (stem proxy: SpecialAbility, AreaEffects, AbilityProfile, PetTrainingHelper; the last is only its profile half) |
| Port list, counted | 313 / 983 | **318 / 983 (32.3%)** (the fifth is SpiderWebbing, in an Items row) |
| Creatures row | 109 / 193 | 109 / 193 |

## Play-test items added

Through the For Chase list below, with Who and steps added by hand to `testing/bot-triage.md` (P121 group) and
`testing/playtest-steps.json`: P121-1 EYES (read the ability lists), P121-2 BOT-PARTIAL (a tamed spider's Lethal
poison), P121-3 CC (done here: the two boots).

## Deviations and decisions for Chase

1. **ServUO's cooldown slip, fixed (D-4 rule).** ServUO writes `(melee && doMelee) || (spell && doSpell) &&
   !IsInCooldown` (`SpecialAbility.cs:48-50`, and :73-75): `&&` binds first, so a melee-triggered ability never checks its
   cooldown, and `Trigger` does not either. Its 30 s cooldown is computed, tracked and ignored; only mana limits it.
   Parenthesised here. **Effect:** a melee special fires at most once per cooldown, not every lucky hit while mana lasts.
   Reverting is one pair of parentheses (`AMeleeAbilityInCooldownIsNotPicked` pins it). Say if you want ServUO's way.
2. **Twins use pinned's numbers, by your decision 1a.** A twin keeps pinned's chance, cooldown and effect, not ServUO's
   mana cost and 30 s. Two visible: pinned TailSwipe stuns 90% / confuses 10% (ServUO 50/50, pinned's comment cites
   Stratics); pinned AuraDamage's default is 5 fire every 5 s (ServUO's default 5 direct). Recorded, not new decisions.
3. **Heal is an eighth twin** (above). Same rule as the seven; tell me if you want it treated as a plain port instead.
4. **Small fixes to ServUO, each D-4 (broken, not missing):** ViciousBite sends cliloc 1234567, which does not exist; it
   sends the text of ServUO's own comment instead. LifeDrain loops over its targets but drains and messages the defender
   each time; it acts on each target. Copied as they are: FlurryForce's "energy" expiry line, VenomousBite's effects on
   the defender, ExplosiveGoo's shared busy flag.
5. **Tamed poisoners now follow ServUO's pet rules** (in scope: "regen and poisoning"). Poison strength rises with
   Poisoning skill (Lethal at 100) and the chance is skill/300 per hit instead of the creature's HitPoisonChance.
   Measured: every tameable hit-poisoner on the shard has Poisoning skill (6 stock: CorrosiveSlime, GiantSpider,
   RuneBeetle, Scorpion, Slime, Snake; 3 ours: CoralSnake, Najasaurus, WolfSpider), so none loses its poison. It is in
   the changelog as a Changed line.
6. **Companions and squires (decision 4):** none exist on the shard (P41 was research only), so their exclusion is
   vacuous today. Evo pets and pack mules are pinned by a fact.
7. **D-numbers this can now reverse, for P129 or a small prompt** (each was "Pet Training, declined B3"): D-32 (Phantom,
   Silenii Discordance; the school is stored but pet bard is P130), D-51/D-52/D-53 (bouras' ColossalBlow, TailSwipe),
   D-54 (Kepetch ViciousBite), D-58 (Rotworm BloodDisease), D-63 (BloodWorm Anemia), D-65 (FireAnt ExplosiveGoo), D-66
   (MaddeningHorror ManaDrain), D-82 (Medusa VenomousBite, Navrey Webbing, SlasherOfVeils AngryFire/ManaDrain/TrueFear),
   Saurosaurus (TailSwipe, LifeLeech), D-S5-1 (MinionOfScelestus DragonBreath). These creatures are already ported; restoring each is one line. I did not touch
   them: the prompt says no creatures here.
8. **The test host's null poisons** (found, not fixed outside my facts): `CC6Batch8Verification` (Medusa's poison set)
   and `CC6Batch2CreatureVerification` (Lich/fiend PoisonImmune) compare null to null unless something registered
   poisons first. `ShardTestHost.EnsurePoisons()` now exists; a bug-list entry for the overseer to number.
9. **`docs/subsystem-policy.md`'s 2026-09-07 "wait"** should be marked superseded (P120's item 2), by whoever edits docs.

## For Chase

Nothing new spawns yet: the creatures that use these abilities come with Creatures part 2 (P129), and training
(Animal Lore's ability pages, points, the trainer) with Pet Training part 2 (P130). Animal Lore does not show abilities
until P130; staff can see them now with `[props`.

**Rebuild the test shard** (console, Test shard, Rebuild) before trying these.

In game on the test shard:

1. **Ability lists:** `[add Dragon`, `[props` it and open AbilityProfile: AbilityNames reads Magery, DragonBreath. A `[add CuSidhe` reads Heal and a `[add GiantSpider` reads Poisoning.
2. **A trained poisoner (the bot can read the poison):** make a `[add GiantSpider` your pet, set its Poisoning to 100 in `[props`, and set it on a player character: within a few bites the player has lethal poison, with a green flash on each poisoning hit.
3. **The world saves the new file:** done by CC on a copy of the test world (two boots, no error).

## Repo size rule

No pending file in either repo is over 5 MB; the largest new one is `SpecialAbility.cs`, 1,662 lines. Build logs,
the scratch world, the patch generator and the break scripts stayed in my session scratchpad, outside both repos.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the notes were written:

```
Repo Result
---- ------
code dry run
docs dry run
```

code: the port (7 files under `Services/Pet Training/`, SpiderWebbing), five patches, `apply-patches.sh`, `RegenRates.cs`,
the test file, `ShardTestHost.cs`, CHANGELOG and VERSION. docs: this note, P120's stopped-run note (uncommitted since
P120), the triage and steps files, and progress.py's output (README, dashboard, progress.json, expansion-coverage.json).

P121 DONE
