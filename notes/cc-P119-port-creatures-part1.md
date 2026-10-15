# cc-P119: Port list, Creatures part 1 (the ones that do not call Pet Training)

2026-10-15. Prompt: `D:\UO\cc-prompts\cc-P119-port-creatures-part1.md`. Both repos were clean at the start except
`notes/cc-P118-port-bulk-orders.md`, P118's own note from its STOPPED run (CC output, not Chase's), which the Golem's
next commit picks up with this one.

## Headlines

- **29 creatures ported, plus 3 leaf items they drop.** 26 had no missing dependency; 3 needed one leaf item each
  (TigerClawKey, AnimalPheromone, TreefellowWood). The Creatures row goes **80 to 109 of 193**.
- **The brief's "19 spawn orphans first" is 18 today, and only 2 of them are creatures. Neither could be ported here.**
  `tools/spawn_orphans.py` re-run: 18 names (Niporailem was ported by CC9 since). 16 are NPCs: Underworld quest givers,
  High Seas vendors, the Heartwood elf, a guard. Those are ride-along content, ported with their systems, not
  creatures. The 2 creatures are `IronBeetle`, which calls Pet Training (left for P121), and `sphynx`. The Sphynx's
  reading needs `SphynxFortune` hooks in two upstream files, `AOS.cs` attribute bonuses and `PlayerMobile.GetResistance`,
  which makes it a subsystem. So no orphan closed, and the count stays 18.
- **The gate caught a duplicate before it shipped.** I ported ServUO's `ToxicElemental`, and `TypeIdentityVerification` went
  red. Pinned's `AcidElemental` carries `[TypeAlias("Server.Mobiles.ToxicElemental")]` (`AcidElemental.cs:5`), so the
  name already loads the stock creature. Withdrawn, with a fact that pins the alias. My name check had looked at
  declared types only, not alias strings. All 32 names are now checked against all 142 alias strings, and
  ToxicElemental was the only hit.
- **One deviation, proposed and unnumbered:** the Wight cannot use Cold Wind. Pinned has no Cold Wind weapon
  ability; the effect exists only inside stock `LadyOfTheSnow`. So the Wight always uses Mortal Strike.
- **One decision for Chase:** ServUO's `Drelgor` (Old Haven) is not ported, because the shard already has its own
  `DrelgorTheImpaler` with the same name and a different design.
- **The test found a turkey with no body.** Pinned refuses body 95 (`Mobile.SafeBody`), which ServUO unlocked in its
  core for exactly this creature. Fixed on the Turkey alone with a `SafeBody` override; it is ServUO's behaviour, not a
  deviation.
- Nothing is on a spawner. None of the 29 is named by pinned's spawn data, so the world does not change until someone
  places them. The 6 that ServUO's own XML spawns place are listed under For Chase.

## Sorting the candidates (re-derived, not taken from the brief)

The brief's "113 remaining" is right. Re-derived with `tools/progress.py`'s method (scratch script, same rules):
193 candidates in the row, 80 done, 113 remaining. Then each was sorted by:
- a Pet Training scan of the live code (calls inside `Deserialize` ignored, port recipe);
- a dependency scan: every `new X(`, `typeof(X)` and base class against declared types in pinned plus the shard;
- a duplicate scan: each class name against pinned's declarations and alias strings.

| Group | n | Files | What happens |
|---|---|---|---|
| Clean, ported | 26 | the table below | ported |
| One leaf item away, ported | 3 | TigersClawMaster, FireRabbit, TreefellowGuardian | ported with the item |
| **Calls Pet Training** | 25 | ChiefParoxysmus, CrimsonDragon, LadyMelisande, MonstrousInterredGrizzle, Navrey, BloodFox, ColdDrake, CrimsonDrake, DragonWolf, FrostDragon, FrostMite, GiantTurkey, IronBeetle, Lion, OsseinRam, PlatinumDrake, SabertoothedTiger, ShadowDweller, Slith, StoneSlith, StygianDrake, ToxicSlith, Triceratops, Viscera, WildTiger | P121. Slith, StoneSlith and ToxicSlith are already in pinned under those names, so they are not real candidates either |
| Already ported, stem proxy miss | 8 | ClanCA, ClanCT, ClanRC, ClanRS, ClanSH, ClanSS, ClanSSW, DragonsFlameGrandMage | CC6 batch 7 ported these under the spawn-data names (Q-056). The stem proxy cannot see them, so the row will never reach 193 |
| Already in pinned | 8 | Raptor, Spellbinder, `InterredGrizzle ` (sic, the space is in both trees' file names), ThirdDawnParrot (`class Parrot`), ToxicElemental (alias), NecroAI and NecromageAI (stock MageAI casts Necromancy from skill, Q-050), SpellbinderAI (pinned declares one) | not ported. `tools/modernuo-stems.txt` predates pinned d4531cd9, which added Raptor |
| Void creatures | 12 | BaseVoidCreature and its 10 children, plus ServUO's `SpeedInfo` | left. BaseVoidCreature is the Covetous void-pool mutation system (1,416 lines across the folder) and belongs with that row. `SpeedInfo` is ServUO's speed table, which ModernUO replaces with `npc-speeds.json` (port recipe, Q-008) |
| AI types | 6 | MysticAI, NinjaAI, PaladinAI, SamuraiAI, SpellweavingAI, OrcScoutAI | left: each needs a member on pinned's `AIType` enum and a `ChangeAIType` branch, a patch to an upstream file. D-41 (Mystic) and D-44 (OrcScout) already record creatures running without two of them |
| Store mount statuettes | 7 | CoconutCrab, Eowmu, HungryCoconutCrab, Lasher, SkeletalCat, Triton, Windrunner | left: each calls `ConfirmMountStatuetteGump`, the Ultima Store mount statuette, which is in the port list's Dropped tier (no donations) |
| Bosses with peerless items | 5 | AbyssalInfernal, DreadHorn, PrimevalLich, ShimmeringEffusion, Travesty | left: peerless rewards (ParrotItem, statuettes, ImprisonedDog), timers and a ShadowDweller summon. With the peerless and boss-box work (F-40) |
| Other | 13 | see below | left, each with a reason |

**The 13 "other":**
- **Drelgor:** decision for Chase (Headlines).
- **ParoxysmusSwampDragon:** clean, but it exists only as ChiefParoxysmus's statuette reward (ParoxysmusSwampDragonStatuette, absent), so it goes with the Chief in P121.
- **HumanBrigand:** the whole ServUO file is commented out (`/* ... */`). Not content.
- **AcidPopper:** an Item (it burns webs), not a creature. It sits in the creature folder only by path.
- **Gregorio:** needs `GuiltyQuest`, an ML quest (the quest framework was declined twice).
- **GargishOutcast and GargishRouser:** gargish cloth under ServUO names. Pinned has them as `Gargish*Type1` (AGENTS.md, equivalents). The Rouser also needs the Mysticism spell `RisingColossusSpell` and `VoidManifestation`.
- **VoidManesfistation:** needs `RisingColossusSpell` and three void crystals.
- **FrostDrake:** its base `ColdDrake` calls Pet Training.
- **LeatherWolf:** `LeatherWolfSkin` sits in ServUO's 30-type `SAQuestItems.cs`, and the wolf has a timer behaviour.
- **StoneMonster:** UndeadGargHorn (same file) and UndeadGargoyleMedallions.
- **Macaw:** needs `MacawSpawner`.
- **TheButcher:** needs `PumpkinCarvingKit`, 7 types in one file, and ServUO's `AI_Necro`.

Several of these are cheap. That is the next prompt's list.

## What was ported (ServUO file -> our file)

All of them go to `server/customizations/<ServUO path>/<ServUO file name>`. The file names stay ServUO's even where
the class name differs, so `progress.py`'s stem proxy counts them. Each file starts with a provenance header.

| ServUO | Ours | Notes |
|---|---|---|
| Mobiles/Named/NightTerror.cs | Mobiles/Named/NightTerror.cs | AI_NecroMage -> AI_Mage (Q-050) |
| Mobiles/Normal/AbyssalAbomination.cs | same path | AI_NecroMage -> AI_Mage; MortalStrike/Whirlwind via GetWeaponAbility |
| Mobiles/Normal/ArchDaemon.cs | same | Shadowlords and Evil allegiances, as stock Daemon |
| Mobiles/Normal/BulbousPutrification.cs | same | |
| Mobiles/Normal/DreadWarhorse.cs | same | (string name) constructor dropped (pinned BaseMount takes no name; stock Nightmare's shape); `BodyValue = 116` dropped (pinned has no BodyValue; 0x74 is already 116) |
| `Mobiles/Normal/DreamWraith .cs` | same, with the space | AI_NecroMage -> AI_Mage |
| Mobiles/Normal/EffetePutridGargoyle.cs | same | |
| Mobiles/Normal/EffeteUndeadGargoyle.cs | same | ServUO's corpse name with its double space, kept |
| Mobiles/Normal/EnragedCollosus.cs | same (class EnragedColossus) | |
| Mobiles/Normal/EnragedEarthElemental.cs | same | LuckyCoin 3% (P2's item) |
| Mobiles/Normal/GargoyleGuardian.cs | same | spell and melee hooks take pinned's extra `damage` argument and call pinned's base (monster-ability triggers; none on this creature) |
| Mobiles/Normal/Grubber.cs | same | `Combatant` override is `Mobile`, not ServUO's `IDamageable`; same body |
| Mobiles/Normal/Icehound.cs | same (class IceHound) | ParalyzingBlow |
| Mobiles/Normal/Lifestealer.cs | same | AI_NecroMage -> AI_Mage |
| Mobiles/Normal/Mimic.cs | same | OSI's Mimic. The shard's ChestMimic (cc-P50) is unchanged and is a different type |
| Mobiles/Normal/MinotaurGeneral.cs | same | on stock MinotaurCaptain |
| Mobiles/Normal/OrcChopper.cs | same | `Tribe => Orc` dropped (its OppositionGroup is already given); IsEnemy in stock Orc's shape |
| Mobiles/Normal/Ortanord.cs | same | a no-op OnDeath not ported |
| Mobiles/Normal/PalaminoHorse.cs | same (class Palomino) | (string name) constructor dropped, as DreadWarhorse |
| Mobiles/Normal/PutridUndeadGargoyle.cs | same | AI_Mystic -> AI_Mage (D-41) |
| Mobiles/Normal/RenegadeChangeling.cs | same | on stock Changeling, morphing intact |
| Mobiles/Normal/SAPixie.cs | same | |
| Mobiles/Normal/SkeletalDrake.cs | same | AI_NecroMage -> AI_Mage; `Tribe => Undead` dropped (OppositionGroup given) |
| Mobiles/Normal/SpeckledScorpion.cs | same | on stock Scorpion |
| Mobiles/Normal/Turkey.cs | same | **body 95 is on pinned's invalid-body list** (`Server/Mobiles/Mobile.cs:232-239`, SafeBody makes it 0); ServUO comments it out "Used for Turkey" (`Server/Mobile.cs:9726`). Ported as a `SafeBody` override on the Turkey alone (virtual, `Mobile.cs:7261`), no core patch. ServUO's two constructors kept (see Tests); the gobble timer is not saved, as in ServUO |
| Mobiles/Normal/Wight.cs | same | AI_NecroMage -> AI_Mage; **Cold Wind deviation** |
| Mobiles/Normal/TigersClawMaster.cs | same | on our TigersClawThief (CC6 batch 2); ServUO's title "of the Serpent's Fang Sect" kept as written |
| Mobiles/Normal/FireRabbit.cs | same | on stock VorpalBunny |
| Mobiles/Normal/TreefellowGuardian.cs | same | AI_Mystic -> AI_Mage (D-41); Dismount |
| Items/Quest/TigerClawKey.cs | same | a PeerlessKey, DragonFlameKey's shape; no Citadel altar here |
| Items/Resource/AnimalPheromone.cs | same | on ServUO also a Tinkering hitching-post resource; no such recipe in pinned or ours yet |
| Quests/TreefellowWood.cs | same | |

**Every file:** `[SerializationGenerator(0, false)]`, partial, `[Constructible]`, `CorpseName` and `DefaultName` as
overrides, and serialization by the generator. The range-perception and speed arguments are dropped, so each runs at
16 and the Medium fallback (port recipe traps 1 and 2, Q-008; the test pins both). `SetWeaponAbility` became
`GetWeaponAbility`. `DateTime.UtcNow` became `Core.Now`.

**How the files were made, so a reviewer knows what to distrust:**
- A scratch converter did the mechanical part: the header attribute, property bodies to expressions, the Name and
  CorpseName moves, and the constructor arguments.
- Every file was then read and hand-fixed: base constructors, pinned signatures, weapon abilities, braces.
- The expected values in the test were extracted from the ServUO files by a second script, not from the ports.

## What changed (file:line)

- `D:\ShatteredLegacy\server\customizations\`: the 32 new files above, plus `Quests/` as a new folder. The two
  behaviour lines worth a look: `Mobiles/Normal/Turkey.cs:59` (SafeBody) and `Mobiles/Normal/Wight.cs:62` (the Cold Wind
  deviation).
- `D:\ShatteredLegacy\server\tests\Mobiles\Normal\CCP119CreatureVerification.cs` (new, 8 facts).
- `D:\ShatteredLegacy\tools\playtest-bot\uobot\checks.py:573-631`: `P119_SAMPLE` (:578), `p119_1` (:582) and
  `_p119_fight` (:597), before the reset section.
- `D:\ShatteredLegacy\CHANGELOG.md:32-40` (2026.10.15.5, Added and Staff) and `VERSION` (2026.10.15.5).
- `testing\bot-triage.md` (a P119 group, P119-1 in "Checks built") and `testing\playtest-steps.json` (P119-1 to P119-4).
- Regenerated by their tools, no hand edits:
  - `tools/spawn-orphans.txt` (19 -> 18);
  - `tools/expansion-coverage.json` and the README expansion block (`expansion_coverage.py`);
  - `tools/progress.json`, `dashboard.html` and the README progress block (`progress.py`).
- The bot's three run folders under `testing/bot-runs/` (machine output).

## Tests

`server/tests/Mobiles/Normal/CCP119CreatureVerification.cs`, eight facts:

1. `EachCreatureResolvesAndConstructsWithItsServUOValues`: for all 29, checks
   - the name resolves, the full name is right, and the parent is right;
   - ServUO's name, corpse name, body, hue, fame and karma, and the AI as ported;
   - perception 16 and speed 0.25/0.5 (the two traps);
   - its own generator attribute and its own (Serial) constructor.
2. `EachCreatureSurvivesASaveAndReload`: a round trip through the generated serializer (CC6 batch 8's shape).
3. `ASpawnerFillsWithEachCreature`: a spawner entry in lower case fills with the type.
4. `TheWeaponAbilitiesAreServUOsSetWeaponAbilityCalls`: 200 samples each for five creatures, and no other port declares one.
5. `TheAbyssGuardianThrowsItsHatchetForFiftyPhysical`: exactly 50, read on the tick it lands (D15).
6. `TheOrcChopperSparesAKinMaskWearerAndBurnsTheMaskWhenAttacked`.
7. `TheLeafItemsResolveAndTheMasterDropsItsKeyOnEveryDeath`: five real kills and corpses.
8. `ToxicElementalIsStockAcidElementalByAliasAndWasNotPorted`: pins the alias. It would pass with or without a port of
   our own, so the gate for that mistake is `TypeIdentityVerification`, not this fact.

**Seen failing first** (`build.sh --tests-only`), with five deliberate breaks:
- Lifestealer.cs moved out of the tree;
- IceHound's GetWeaponAbility deleted;
- hatchet damage set to 40;
- the chopper's `item.Delete()` deleted;
- the master's key drop deleted.

Result: **1,171 tests, 9 failed.** Each of facts 1 to 7 failed for its own break:
- 1, 2 and 3: "Lifestealer resolves to no type: not ported";
- 4: the collections differ;
- 5: "Expected: 75, Actual: 85";
- 6: the mask was not deleted;
- 7: the key was null.

The other two failures were `TypeIdentityVerification` catching ToxicElemental (Headlines). The breaks were restored
from copies and compared byte for byte with `cmp`.

**Then two real defects, each found by these facts, each fixed in the port:**
- **First full run after the restore, 3 failed:** `Turkey` had been collapsed to `Turkey(bool tamable = false)`. That form has no parameterless
  constructor, so `Activator.CreateInstance` threw. The spawner path still worked; reflection did not. ServUO's two
  constructors are restored.
- **Second, 1 failed:** the turkey's body was 0. Pinned's `SafeBody` rejects 95, which ServUO unlocked for the turkey.
  Fixed with a `SafeBody` override.

**Final:** `docker/uo/build.sh -t sl-modernuo:cc-p119` (all three gates, the image built): **1,172 tests, 1,172
passed.** That includes every earlier shard fact, among them CC6 batch 7's pinned spawn-orphan count (18), which
these ports do not move.

**The full server suite, unfiltered**, in the same builder image (`dotnet test ModernUO.slnx -c Release --no-restore`,
seccomp unconfined, no network):
- `Server.Tests.dll`: 910 total, **893 passed, 0 failed**, 17 skipped;
- `UOContent.Tests.dll`: 2,359 total, **2,268 passed, 0 failed**, 91 skipped. That includes the 1,172 shard facts.

The skips are the suites' own `[Skip]`s; none is ours.

**The bot's own unit tests** (`python -m unittest discover -s tests` in `tools/playtest-bot`): 38 run, 1 failure,
`test_installer_dry_run_prints_the_call_and_registers_nothing`. That test asserts the task "SL overnight play tests" is
not registered, and on this machine it is (`schtasks /query`: Ready, next run 10/16 01:30). It fails with or without
this change, because it is about the machine, not the code.

## Port-list numbers

`tools/port-list.json` through `progress.py`'s counter, before (HEAD) and after (this tree):

| | before | after |
|---|---|---|
| Creatures row | 80 / 193 | **109 / 193** |
| Base items row (AnimalPheromone) | 167 / 298 | 168 / 298 |
| Ride-along (TigerClawKey; not counted) | 11 / 361 | 12 / 361 |
| Port list, counted | 283 / 983 (28.8%) | **313 / 983 (31.8%)**, 1 of 16 systems in |

The 10-13 totals (905 counted) differ from today's 983 because other ports since then added candidates. TreefellowWood
sits under ServUO `Quests/`, which the port list does not scan yet. **The Creatures row cannot reach 193 by porting**:
8 of its candidates are done under other names and 8 are already in pinned (the table above), so 177 is the real
ceiling unless the proxy learns about either.

## Play-test items added

Through the normal notes import (the For Chase list below), with Who and steps added by hand to
`testing/bot-triage.md` and `testing/playtest-steps.json`:

| id | Who | What |
|---|---|---|
| P119-1 | BOT (built: `p119_1`) | five creatures spawn, fight back, die to a player and leave a corpse |
| P119-2 | EYES | the bodies ServUO itself calls guesses, and the other unusual ones, draw and animate |
| P119-3 | EYES | the two mounts can be ridden |
| P119-4 | BOT-PARTIAL | the Abyss Guardian's hatchet (the damage is a shard test; the throw is Chase's eyes) |

**P119-1 was built and run** (`Run-OvernightPlaytests.ps1 -SkipBuild -Only P119-1 -SkipSoak -NoEmail`). It ran on
this tree's image (`sl-modernuo:cc-p119`, tagged as `sl-modernuo:bot`, labelled `sl.dirty=1` on 97462b3) and on a
scratch copy of the test world. **It took three runs to get the check itself right**, and all three run folders are
kept:

| Run folder | Result | Why |
|---|---|---|
| `testing/bot-runs/2026-10-15-0955` | FAIL 0/3 | The shared 55-hit player killed the IceHound, then the orc chopper's crushing blow killed the player (transcript: "You take extra damage from the crushing attack!", then "You have died"), and every later swing was a ghost's. **A check defect.** Fixed with a fresh character per run at Str 250 and 175 hits |
| `testing/bot-runs/2026-10-15-1011` | FAIL 0/3, the same way each run | 4 of 5 died every run; the Ortanord never did. Its ServUO resistances are 80-90 physical, so a bare-handed hit does 0 damage even at 1 hit point (60 s of swings; Tactics climbed 104 to 140 from those swings). **Its values working as written, a poor sample.** Swapped for the Lifestealer |
| `testing/bot-runs/2026-10-15-1016` | **PASS 3/3** | All five appear with the port's body, die, and leave a corpse whose amount is that body. The player ends at 149/178, 150/177, 167/176: they fought back |

**The test shard boots clean from this tree.** The first run's `shard-start.log` reads:
- `Loading world done (206840 items, 35039 mobiles)`;
- `[ShardVersion] Shattered Legacy 2026.10.15.5`;
- one warning, "Command stats already registered", which P95's start log from before this change also has.

No exception appears in any of the three runs' `shard.log`, across about 22 minutes of fights between them (15, 5 and 2). The bot
says "rule 1 held: both real shards are exactly as they were".


## Deviations and decisions for Chase

1. **Wight, Cold Wind (proposed, unnumbered).**
   - **What changes:** ServUO's Wight has two weapon abilities, Mortal Strike and Cold Wind, and picks one per use.
     Pinned has no Cold Wind weapon ability (`WeaponAbility.cs`, 32 slots); the effect exists only inside stock
     `LadyOfTheSnow.OnGaveMeleeAttack`. So the Wight always uses Mortal Strike.
   - **Reverses when:** a `ColdWind` WeaponAbility is added. That is ServUO's `Abilities/ColdWind.cs`, 100 lines, plus
     its slot in `WeaponAbility.Abilities`, which is an upstream file, so it would be a patch.
   - **Reaches:** Wight and FrostMite (the third ServUO user, LadyOfTheSnow, is stock).
   - **Where it is recorded:** the Wight's header and the test. The overseer numbers it.
2. **D-41, cited, no new number:** PutridUndeadGargoyle and TreefellowGuardian run AI_Mage for ServUO's AI_Mystic, as
   FairyDragon does. The Treefellow has Spellweaving and no Magery, so in practice it fights in melee.
3. **Q-050, cited:** six creatures run AI_Mage for ServUO's AI_NecroMage. Pinned's MageAI casts Necromancy from skill,
   so this is not a deviation.
4. **Decision: ServUO's Drelgor.** The shard's `DrelgorTheImpaler` (customizations root, its own design: the Old Haven
   Chivalry quest target) shares the name "Drelgor the Impaler" with ServUO's `Drelgor`, an Old Haven creature with a
   region check. Port ServUO's as well (two Drelgors), or keep ours as the only one? I kept ours and ported nothing.
5. **The spawn-orphan line on the status page** ("19 names ... still spawn nothing") is hand-kept judgment. It is 18
   today, and `tools/spawn-orphans.txt` was regenerated to say so (the one name gone is Niporailem, CC9's). The
   judgment line itself is not edited here.

## For Chase

None of these creatures is in the world yet: they exist, and staff can `[add` them. ServUO's own XML spawns would
place six of them: BulbousPutrification (Felucca), the two Effete gargoyles, Lifestealer and Ortanord (Ter Mur), and
SpeckledScorpion (Ilshenar). Placing them is a spawn-data decision for later.

**Rebuild the test shard** (console, Test shard, Rebuild) before trying these.

In game on the test shard:

1. **A fight (the bot runs this one):** `[add IceHound`, `[add OrcChopper`, `[add Lifestealer`, `[add EffeteUndeadGargoyle` and `[add Wight` next to a player and kill each: each shows, fights back, dies and leaves a corpse.
2. **Bodies by eye:** `[add` EffeteUndeadGargoyle, PutridUndeadGargoyle, Wight, SkeletalDrake, DreamWraith, NightTerror, Mimic, GargoyleGuardian, EnragedColossus and Ortanord, and walk close to each: each draws as a whole creature and animates when it moves and attacks (ServUO's files call the undead gargoyle and Wight bodies guesses).
3. **The two mounts:** `[add DreadWarhorse` and `[add Palomino`, tame each and ride it: you ride a dark warhorse and a palomino horse, and can dismount.
4. **The Abyss Guardian:** `[add GargoyleGuardian`, then as a player cast Magic Arrow at it a few times: about two casts in five it throws an axe back for 50 physical.

## Left for the next prompt

- **Cheap leaf ports:** Macaw (+MacawSpawner), StoneMonster (+2 items), LeatherWolf (+LeatherWolfSkin and its timer),
  TheButcher (+PumpkinCarvingKit's 7 types; ServUO's AI_Necro), GargishOutcast (gargish cloth -> pinned's Type1 names).
- **With Covetous Void Spawn:** BaseVoidCreature and its 10 children.
- **P121:** the 25 Pet Training callers, and ParoxysmusSwampDragon with ChiefParoxysmus.
- **A decision each:** the 6 AI types (each an AIType patch), Drelgor, and the 5 peerless bosses.

## Repo size rule

No pending file in either repo is over 5 MB. The largest is a bot transcript at 237 KB
(`testing/bot-runs/2026-10-15-1011/transcripts/P119-1-run1.txt`). Build logs, drafts and the converter scripts stayed
in my session scratchpad, outside both repos. Docker images stayed in Docker.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the notes were written:

```
Repo Result
---- ------
code dry run
docs dry run
```

- **code:**
  - the 32 ported files, `Quests/` among them;
  - the test file;
  - `tools/playtest-bot/uobot/checks.py`;
  - `CHANGELOG.md` and `VERSION`.
- **docs:**
  - this note;
  - P118's note, from its STOPPED run (the dry run also lists `cc-P118-port-bulk-orders.md` for archiving);
  - `testing/bot-triage.md` and `testing/playtest-steps.json`;
  - the three bot-run folders and the importer's `testing/` output (machine output);
  - the regenerated `tools/` files, `README.md` and `dashboard.html`.

P119 DONE
