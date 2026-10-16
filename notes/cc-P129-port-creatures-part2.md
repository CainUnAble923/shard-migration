# cc-P129: Port list, Creatures part 2 (the Pet Training callers, P119's leftovers, and the two Drelgors)

2026-10-16. Prompt: `D:\UO\cc-prompts\cc-P129-port-creatures-part2.md` (handed by the Golem; first handed at 09:30 into a
session whose context P128 had spent, which stopped it untouched, then re-handed into this fresh session). Both repos
were clean at the start. Model: Fable, as the prompt asks.

## Headlines

- **36 creature types ported in 29 files, plus 19 leaf types in 14 files.** The Creatures row goes **109 to 138 of 193**;
  the port list **417 to 446 of 983 (45.4%)**. The numbers are below, counted by `progress.py`.
- **Every creature P119 left for Pet Training is in, except the three already in pinned under their own names.** P119's
  25 "calls Pet Training" became 22 real candidates (Slith, StoneSlith, ToxicSlith are stock); all 22 are in: 17
  normal creatures and the four ML peerless bosses ported here, and Navrey, who turned out to be CC6 batch 8's
  `NavreyNightEyes` all along (below). Each `SetSpecialAbility`,
  `SetAreaEffect` and `SetMagicalAbility` call is kept as ServUO wrote it and lands on cc-P121's profile; where pinned has
  the same ability by nature (a cold drake's aura, a lion's heal) the profile lists it once and pinned fires it.
- **The four peerless bosses were one `ParrotItem` away, not "with the peerless work".** P119 sorted them by their Pet
  Training calls, so it never costed them; the dependency scan here found `BasePeerless` already ours (CC6 batch 8) and
  every artifact, statuette and resource they drop in pinned or ours except the pet parrot. The parrot (`ParrotItem`,
  `PetParrot`) is a 2-file port plus **one upstream patch**, the perch's `Parrot` field, which pinned dropped. That
  retires D-72 (the Crystal Hydra's parrot pack, restored here too).
- **Drelgor, both of them.** The shard's `DrelgorTheImpaler` is **`VorlakTheImpaler`** now ("Vorlak the Impaler"; zero
  hits for the name in ServUO or pinned, and no D&D or OSI figure I know of), design, loot and abilities untouched, with
  `[TypeAlias("Server.Mobiles.DrelgorTheImpaler")]` so every saved one loads and his existing spawner's entry still
  resolves. ServUO's `Drelgor` is ported faithfully and seeded where ServUO's spawn data puts him (3651,2509, Trammel), by
  the Old Haven seeder on its next `missing` run. **Chase chooses Vorlak's new spot** (For Chase); nothing moved.
- **P119's leftovers are in**: Macaw with its gold-foil nest, StoneMonster, LeatherWolf and its pack, TheButcher with the
  Jack O' Lantern carving kit (7 types), GargishOutcast with the gargish robe.
- **Gates:** 18 new facts, every one seen failing first (17 under one deliberate break set, the 18th under a second
  break aimed at it); the gated build green at **1,373 of 1,373** shard facts; the full server suite green on its second
  run (the first failed one P128 fact, a flake, below); the test world booted twice on the image, the saved
  DrelgorTheImpaler mobiles loading as Vorlak through the alias.
- **Deviations, all small and all recorded below:** the Frost Mite joins the Wight's Cold Wind gap; the saber-toothed
  tiger loses Int on taming (no `OnAfterTame` hook); the leather wolf cannot be tinker-repaired (no `IRepairableMobile`);
  the gargish outcast takes names from pinned's gargoyle list; Drelgor's region check names a region the shard does not
  have, so his taunt is silent until it does.

## Sorting the candidates (re-derived from the trees, not from the brief)

P119's "Calls Pet Training" group, 25 names, re-scanned here with a dependency script (every `new X(`, `typeof(X)`, base
class and static reference against pinned's declarations, the shard's, and pinned's `[TypeAlias]` strings):

| Group | n | Files | What happened |
|---|---|---|---|
| Already in pinned | 3 | Slith, StoneSlith, ToxicSlith | not candidates (P119 said so) |
| Clean, ported | 15 | BloodFox, ColdDrake, DragonWolf, FrostDragon, FrostMite, GiantTurkey, Lion, OsseinRam, SabertoothedTiger, ShadowDweller, StygianDrake, Triceratops, Viscera, CrimsonDrake, PlatinumDrake | ported; the two drakes needed `ElementType` and `IElementalCreature`, two tiny types from ServUO's `MobileInterfaces.cs` |
| One leaf away, ported | 2 | IronBeetle (+UndamagedIronBeetleScale), WildTiger (+3 pelts) | ported with the items |
| Peerless, one parrot away, ported | 4 | ChiefParoxysmus (+ParoxysmusSwampDragonStatuette, +ParoxysmusSwampDragon), CrimsonDragon, LadyMelisande (+AlbinoSquirrelImprisonedInCrystal), MonstrousInterredGrizzle (+InfernalOoze, same file) | ported, with ParrotItem, PetParrot and the perch patch |
| Already ported under the spawn-data name | 1 | Navrey | CC6 batch 8 ported her as `NavreyNightEyes` (`Mobiles/Bosses/Navery/NavreyNightEyes.cs`), the name pinned's spawn data uses, so the stem proxy cannot see her and P119's list carried her as unported (the same trap as the Clan ratmen, Q-056). Not ported again |

P119's "Left for the next prompt" cheap list, 5 names: all 5 ported (Macaw +MacawSpawner/MacawNest; StoneMonster
+UndeadGargHorn; LeatherWolf +LeatherWolfFellow +LeatherWolfSkin; TheButcher +PumpkinCarvingKit; GargishOutcast
+GargishRobe). `UndeadGargoyleMedallions` is not ported: ServUO's only use is a commented-out pack line. `GargishRouser`
stays out: `RisingColossusSpell` and `VoidManifestation` are not in pinned (its Mysticism folder has 9 spells, no Rising
Colossus); the Rouser is meaningless without its summon.

ParoxysmusSwampDragon (P119's "goes with the Chief") came with the Chief. FrostDrake (P119's "its base ColdDrake calls Pet
Training") came with ColdDrake.

## What was ported (ServUO file -> our file)

All to `server/customizations/<ServUO path>/<ServUO file name>`; each file starts with a provenance header that names
every member that differs from ServUO and why.

| ServUO | Ours | Notes |
|---|---|---|
| Mobiles/Normal/BloodFox.cs | same | BleedAttack via GetWeaponAbility; GraspingClaw on the profile |
| Mobiles/Normal/ColdDrake.cs | same | DragonBreath on the profile (its twin runs ServUO's ColdDrake breath definition, 100% cold); the aura is pinned's HasAura with ServUO's coldAura numbers (15 cold / 5 s / range 10); DragonBlood dropped |
| Mobiles/Normal/FrostDrake.cs | same | a ColdDrake named "a cold drake", as ServUO |
| Mobiles/Normal/CrimsonDrake.cs | same | `[SerializableField(0)] _elementType` is ServUO's m_Type; two `[Constructible]` constructors kept (random element); TrainingDefinition is P130's |
| Mobiles/Normal/PlatinumDrake.cs | same | CrimsonDrake's shape |
| Mobiles/Normal/DragonWolf.cs | same | DragonBreath (default fire definition) |
| Mobiles/Normal/FrostDragon.cs | same | BleedAttack; frost breath; cold aura; OnAfterTame (Title = null) was a no-op, dropped |
| Mobiles/Normal/FrostMite.cs | same | **Cold Wind deviation** (below); cold aura |
| Mobiles/Normal/GiantTurkey.cs | same | three weapon abilities over Utility.Random(3); EssenceOfDisease, HowlOfCacophony |
| Mobiles/Normal/IronBeetle.cs | same | the mining pet; pinned's harvest API (Construct takes two arguments, Validate takes the land flag); the two mining context entries reproduced (pinned's are private); the mining timer restarts after a load and **is stopped on delete** (ServUO leaks it; D-4 rule) |
| Mobiles/Normal/Lion.cs | same | HealChance is CanHeal; Piercing |
| Mobiles/Normal/OsseinRam.cs | same | MortalStrike; BattleDefense, LifeLeech |
| Mobiles/Normal/SabertoothedTiger.cs | same | CanHeal; Slashing; **OnAfterTame deviation** (below) |
| Mobiles/Normal/ShadowDweller.cs | same | LifeLeech |
| Mobiles/Normal/StygianDrake.cs | same | MageryMastery (pinned's MageAI reads it as SmartAI, P121's patch) |
| Mobiles/Normal/Triceratops.cs | same | CanHeal; Piercing; FruitsAndVeggies |
| Mobiles/Normal/Viscera.cs | same | AuraOfNausea, StickySkin |
| Mobiles/Normal/WildTiger.cs | same (3 types) | on pinned's BaseMount (no name argument; DefaultName per type); CanRide is `[SerializableField(0)]`; GraspingClaw; CanHeal; `[TypeAlias("Server.Mobiles.Tiger")]` kept |
| Mobiles/Normal/Macaw.cs | same | in Server.Mobiles (ServUO's file says Server.Items; a namespace only); spawner link not persisted, as ServUO |
| Mobiles/Normal/StoneMonster.cs | same | six forms; GargoylesPickaxe is pinned's |
| Mobiles/Normal/LeatherWolf.cs | same (2 types) | the fellows timer; `Map.GetSpawnPosition` is pinned's `GetRandomNearbyLocation`; **IRepairableMobile deviation** |
| Mobiles/Normal/TheButcher.cs | same | AI_Necro -> AI_Mage (Q-050's reasoning) |
| Mobiles/Normal/GargishOutcast.cs | same | AI_Mystic -> AI_Mage (D-41); pinned's Gargish*Type1 cloth; **name-list deviation**; AcquireOnApproach dropped (pinned has no switch, it always does) |
| Mobiles/Normal/ParoxysmusSwampDragon.cs | same | on pinned SwampDragon's generated barding properties |
| Mobiles/Bosses/ChiefParoxysmus.cs | same | on our BasePeerless (D-79); PoisonBreath on the profile; **the pet-eating runs from a `Damage` override, not `OnDamage`**: pinned's `Mobile.Damage` calls `OnDamage` before it assigns the new hit points (`Mobile.cs:6009`, `:6029`), so a heal inside `OnDamage` is overwritten by the hit. ServUO assigns first. Found by the fact, which saw the chief lose 10 and gain nothing |
| Mobiles/Bosses/CrimsonDragon.cs | same | OnDamagedBySpell / OnGotMeleeAttack take pinned's damage argument; the GoodiesTimer as pinned's BaseChampion has it; **body 197 is on pinned's invalid-body list** (`Mobile.cs:232-239`; ServUO comments it out, "ML Dragon", `Server/Mobile.cs:9728`), so a `SafeBody` override keeps it, P119's Turkey shape. Found by the fact: the first build gave him body 0 |
| Mobiles/Bosses/LadyMelisande.cs | same | AI_NecroMage -> AI_Mage; SpawnHelpers takes ServUO's own altar-less arm (D-79); LootPack.Parrot is `ParrotItem.LootPack` |
| Mobiles/Bosses/MonstrousInterredGrizzle.cs | same (2 types) | AI_Spellweaving -> AI_Mage (D-41's shape); the ooze's AcquireIndirectTargets reproduced with pinned's GetMobilesInRange and the same filters; BalmOfProtection is ours (P127) |
| Mobiles/Named/Drelgor.cs | same | init and the next-message time are `[SerializableField]`s; **region deviation** |
| Mobiles/MobileInterfaces.cs (two types) | Mobiles/ElementType.cs, Mobiles/IElementalCreature.cs | one extracted type per file; IAuraCreature not ported (pinned's AuraEffect virtual) |
| Items/Addons/Parrot.cs | same | ParrotItem; `ParrotItem.LootPack` is pinned's commented-out LootPack.Parrot (10%) |
| Items/Addons/PetParrot.cs | same | Birth is `[SerializableField(0)]`; Frozen on load is `[AfterDeserialization]`; status through `NetState.SendMobileStatus` |
| Items/Addons/ParoxysmusSwampDragonStatuette.cs | same | on pinned's BaseImprisonedMobile |
| Items/Quest/AlbinoSquirrelImprisonedInCrystal.cs | same (2 types) | on pinned's Squirrel |
| Items/Quest/SAQuestItems.cs (3 types) | Items/Quest/UndamagedIronBeetleScale.cs, UndeadGargHorn.cs, LeatherWolfSkin.cs | one extracted type per file, LuckyCoin's precedent |
| Services/Expansions/Time Of Legends/Items/Resources.cs (3 types) | Services/Expansions/Time Of Legends/Items/TigerPelt.cs, WhiteTigerPelt.cs, BlackTigerPelt.cs | the pelts P128 said Kurak Ambusher's Essence waits for |
| Items/Internal/MacawSpawner.cs | same (2 types) | the nest and the spawn list are `[SerializableField]`s; the rewiring is `[AfterDeserialization]`; `Generate()` and its 23 Ter Mur points ported, called by nothing (For Chase) |
| Items/Decorative/PumpkinCarvingKit.cs | same (7 types) | CarvedBy is the pumpkin's `[SerializableField]`; pinned's BaseLight |
| Items/Equipment/Clothing/Cloaks.cs (GargishRobe) | Items/Equipment/Clothing/GargishRobe.cs | pinned gates wear by RequiredRace; CanBeWornByGargoyles has no pinned reader |

**Found already ours, not ported again:** GoldFoil (P128), the Grizzle armour set and ScepterOfTheChief (CC9),
BasePeerless (CC6 batch 8), BulbousPutrification (P119), LuckyCoin (P2), BalmOfProtection (P127), ParrotWafer (P128).

**Every file:** `[SerializationGenerator(0, false)]`, partial, `[Constructible]`, `CorpseName` and `DefaultName` as
overrides, the range-perception and speed arguments dropped (port recipe, Q-008), `SetWeaponAbility` as
`GetWeaponAbility`, `DateTime.UtcNow` as `Core.Now`, `Delete()` overrides as `OnAfterDelete`, `GetProperties` on
`IPropertyList`, `Flipable` as `Flippable`, and the ICommodity items in pinned's `int` shape.

## The one upstream patch: the parrot perch

`server/patches/ParrotPerchAddon-pet-parrot.patch` (one file, `Items/Addons/ParrotPerchAddon.cs`, both types), applied
last in `apply-patches.sh`. Generated against `D:\UO\ModernUO-pinned` (no other patch touches the file; applied at
`--fuzz=0` in the build).

- **What it adds:** ServUO's `Parrot` field on the perch and on the deed (`[SerializableField(0)]`, version 0 -> 1 on
  each, `MigrateFrom(V0Content)` empty: pinned's own `Migrations/*.v0.json` for both types carry no fields); the perch
  moves the parrot with it (`OnLocationChange`, `OnMapChange`), puts it away when chopped (`OnAfterDelete`), hands it
  to its deed (`Deed`) and gets it back from the deed (`Addon`); `RetainDeedHue`; the deed's property lines.
- **One difference from ServUO, argued:** ServUO's deed deletes its parrot in `OnAfterDelete` unless a `m_Safety` flag
  set by `DeleteDeed()` says the deed was consumed by placement. Pinned's `BaseAddonDeed` has no `DeleteDeed`: its target
  calls `m_Deed.Delete()` straight after `addon.MoveToWorld`. So the guard here is the parrot's own state: a parrot that
  is already in the world (standing on its new perch, which `OnMapChange` just placed it on) is kept; one still put away
  dies with the deed. Same outcome in every path a player can take; pinned by the parrot fact.
- **Alternatives rejected:** (1) a partial class on the perch: can add members but not a serialized field, a `Deed`
  override or `OnAfterDelete` on a type that already declares them; (2) the parrot remembering its perch and polling it
  from `OnThink`: no deed hand-off, so re-deeding a perch would strand or lose the parrot, a real loss for players; (3) no
  parrot: a 60% loot line gone from four bosses and the hydra's pack left dead, which is what D-72 recorded.
- `server/migrations/Server.Items.ParrotPerchAddon.v1.json` and `ParrotPerchDeed.v1.json` describe the new layout for
  the next bump (P127's practice; the build reads pinned's v0 files, not these).

## What changed, file:line

- `D:\ShatteredLegacy\server\customizations\`: the 43 new files above.
- `server/customizations/VorlakTheImpaler.cs` (renamed from `DrelgorTheImpaler.cs`, `git mv`): the class, the
  `[TypeAlias]`, the name, the corpse name and the header. Nothing else.
- `server/customizations/ClusterFAchievements.cs:29` (`TriggerKind.KillVorlak`, was KillDrelgor), `:106` (the words),
  `:363-370` (the `combat.drelgor` achievement's text and trigger; **the id stays `combat.drelgor`**: it is the key
  earned achievements are saved under), `:1241` (`victim is VorlakTheImpaler`).
- `server/customizations/ClusterFOldHavenSeeder.cs`: the Vorlak entry (type name, label, an `aliases` list holding
  `DrelgorTheImpaler` so a spawner placed under the old name is found, not duplicated, by a `missing` run), the new
  Drelgor entry (3651,2509, home range 50, one at a time, 30 minutes: ServUO's XmlSpawner row `Drelgor:MX=1:RT=30`),
  `SpawnConfig.Aliases` and `Matches`, and `FindExistingSpawners` counting aliases as managed.
- `server/customizations/Mobiles/Normal/CrystalHydra.cs:74-76`: `AddLoot(ParrotItem.LootPack)` restored (D-72).
- `server/patches/ParrotPerchAddon-pet-parrot.patch` (new), `docker/uo/apply-patches.sh` (its line and comment),
  `server/migrations/Server.Items.ParrotPerch{Addon,Deed}.v1.json` (new).
- `server/tests/Mobiles/Normal/CCP129CreatureVerification.cs` (new, 18 facts).
- `server/tests/Mobiles/Normal/CC6Batch{1,2,3,4,5,7}*.cs` and `Mobiles/Bosses/CC6Batch8Verification.cs`: the pinned
  spawn-orphan count, 18 -> 17 (IronBeetle resolves now), with a dated line each, as every batch before added one.
- `tools/playtest-bot/uobot/checks.py`: `P129_SAMPLE`, `p129_1`, and `_p119_fight` takes the sample as a parameter
  (P119-1 unchanged).
- `CHANGELOG.md` (2026.10.16.3, Added and Changed), `VERSION`, `docker/uo/SERVER.md` (the Old Haven and achievement
  rows).
- shard-migration: this note; `testing/bot-triage.md` (P129 group); `testing/playtest-steps.json` (P129-1 to P129-10);
  the files `progress.py` and `expansion_coverage.py` regenerate.

## Tests

`server/tests/Mobiles/Normal/CCP129CreatureVerification.cs`, **18 facts**:

1. `EachCreatureResolvesAndConstructsWithItsServUOValues`: all 34 creature types (the 29 ported plus FrostDrake's parent
   chain, the fellow, the parrot, the squirrel and the swamp dragon), each against ServUO's name, corpse, body, hue,
   fame, karma and AI as ported; perception 16 and speed 0.25/0.5; its own generator attribute and (Serial) constructor.
2. `EachCreatureSurvivesASaveAndReload`: a round trip through the generated serializer.
3. `TheElementalDrakesKeepTheirElementThroughASave`: a cold crimson drake's body, hue and damage, and its element after
   a round trip; the parameterless constructor's random element.
4. `ASpawnerFillsWithEachCreature`.
5. `TheProfilesCarryTheServUOSetAbilityCalls`: 20 creatures' stored and natural abilities, each listed exactly once in
   `AbilityNames`; the cold drake's aura is a natural twin; the platinum drake's profile is empty.
6. `TheWeaponAbilitiesAreServUOsSetWeaponAbilityCalls`: 300 samples each for seven creatures; nothing else declares one
   (the Frost Mite's absence is the Cold Wind deviation); the outcast's are its thrown weapon's.
7. `TheColdAurasAreServUOsColdAuraDefinition`: the four cold auras' numbers; 15 landed on a player at 0 cold resistance,
   read on the tick; six seconds of thinks land one aura, not two (the twin is not dispatched twice).
8. `TheLeafItemsResolveAndTheTigersYieldTheirPelts`: 16 leaf types resolve with their own generator attribute; the three
   pelts by tiger; clilocs; the robe's race; a Crystal Hydra dies with the parrot pack in its loot.
9. `TheLeatherWolfHowlsForThreeFellowsWhenItFightsAndSendsThemHomeAfter`: three fellows on the first tick, a lost one
   replaced on the next, all deleted once the fight ends.
10. `TheGoldFoilLoosesMacawsOnWhoeverLiftsItAndAMacawThatStraysForgetsItsNest`: 3 to 5 macaws on the lifter, the foil
    hidden then back after 60-90 s, a macaw 25 tiles off forgets the nest, the nest dies with the foil.
11. `TheCarvingKitCarvesAPumpkinOnceAndIsSpent`: through the real target; a barrel is refused.
12. `TheGargishOutcastIsAnArmedGargoyleOfEitherSex`: 20 outcasts.
13. `TheParrotStandsOnItsPerchFollowsItAndTravelsInItsDeed`: the patch: the perch moves the parrot, keeps it through a
    save, hands it to its deed when chopped (parrot put away), gets it back when the deed is placed (parrot back, deed
    spent without taking it), and a deed thrown away takes a put-away parrot with it; the ParrotItem's target.
14. `TheOozeBurnsWhoeverStandsInItForFortyPoison`: 40 on a player at 0 poison resistance; gone after 35 s.
15. `ChiefParoxysmusEatsAPetThatHitsHimAndPullsADistantPlayerIn`.
16. `LadyMelisandeTakesLifeOnlyWhenNearlyDead`: refused at half, taken at 5%, half the player's hits, then cooling down.
17. `TheCrimsonDragonTerrorizesAPlayerWhoWalksUpForFiveSeconds`: frozen, free after 5 s, five minutes of grace.
18. `DrelgorIsServUOsAndTheShardsImpalerAnswersToItsOldName`: Drelgor's kit and faction, his first think arming the
    taunt; Vorlak's values; `DrelgorTheImpaler` (short and full) resolving to `VorlakTheImpaler`; a spawner entry under
    the old name spawning him.

**Seen failing first**, two deliberate break sets on the real tree (`breaks.py` in my scratchpad: each break aims at
one fact, backups taken, restored after and compared byte for byte with `cmp`; `build.sh --tests-only`):

- **Set A, 16 edits and one file moved** (ShadowDweller.cs out of the tree; ColdDrake's aura 15 -> 7; Viscera's
  StickySkin call deleted; the turkey's BleedAttack arm deleted; CrimsonDrake's `[SerializableField]` removed; the wolf's
  MaxFellows 3 -> 2; the macaw's leash 20 -> 30; the kit not deleted after carving; the outcast's title deleted; the
  patch's deed handing a parrotless perch back; the ooze 40 -> 30; the Chief's heal deleted; Lady Melisande's take-life
  window 10%/2.5% -> 1%/0.25%; the dragon's terror 5 s -> 10 s; Vorlak's `[TypeAlias]` deleted; the base tiger's pelt
  4 -> 3; the blood fox's name changed): **1,373 tests, 17 failed**, every one a P129 fact aimed at, with its own
  message: "ShadowDweller resolves to no type: not ported" (three facts), "Expected: 15 Actual: 7" (the aura),
  "Expected: Cold Actual: Physical" (the element), "Expected: 3 Actual: 2" (the fellows), "Value is not null ...
  MacawSpawner" (the leash), "Expected: the Gargish Outcast Actual: null", "Expected: a pet parrot Actual: null" (the
  patch), "Expected: 85 Actual: 95" (the ooze), "the chief did not eat the pet: 49500 -> 49490", the Crimson Dragon
  still frozen, the kit not spent, Vorlak "Actual: null" under the old name, the turkey's and Viscera's abilities, and
  the blood fox's name. The pelt fact did **not** go red: its assertion reads the black tiger's pelt, and the break hit
  the base tiger's. Every other fact in the build stayed green (1,356 passed).
- **Set B, one edit** (the black tiger's pelt 4 -> 3): **1,373 tests, 1 failed**,
  `TheLeafItemsResolveAndTheTigersYieldTheirPelts`, "Expected: 4 Actual: 3".

So all 18 facts have been watched failing. Both restores compared identical to the backups.

**Gated builds** (`docker/uo/build.sh -t sl-modernuo:cc-p129`), seven in all, the first six red in the builder stage:
1-2. missing `using` directives (WeaponAbility is `Server.Items`, PooledRefList is `Server.Collections`,
SendMobileStatus is `Server.Network`) and `Effects.PlaySound(IEntity, Map, int)`, which pinned has not (the dragon's
goodies); 3-5. the test file: `Target.Cancel` is static, and three xUnit analyzer rules (`Assert.Single` over a count,
`Assert.Contains` over `Any`, the filtering `Assert.Single`); 6. **green compile, 12 facts red, two real defects in the
ports and one in the facts, plus the orphan count**: the Crimson Dragon had body 0 (197 is on pinned's invalid-body
list; ServUO comments it out, so a `SafeBody` override as cc-P119's Turkey), the Chief ate the pet and gained nothing
(pinned's `Mobile.Damage` calls `OnDamage` before it assigns the new hit points, so the heal is overwritten: the
eat-and-pull moved to a `Damage` override), the carver had no name so the pumpkin never read "carved", `TigerPelt(int
amount = 1)` is not a parameterless constructor to `Activator.CreateInstance` (the leaf items are made through their
`[Constructible]` constructor at its defaults now), the full alias name needs `fullName: true`, and the seven CC6 facts
that pin the spawn-orphan count at 18 (IronBeetle resolves now: 17). 7. **Green, 1,373 of 1,373, image
`sl-modernuo:cc-p129` built.** The 110 "Corpse ... amount of 0" log lines are the ones P121 recorded on P119's build.

**Full server suite, unfiltered**, in the green builder (`dotnet test ModernUO.slnx`, seccomp unconfined, no network),
twice:
- run 1: `Server.Tests.dll` 910 total, **893 passed, 0 failed**, 17 skipped; `UOContent.Tests.dll` 2,560 total, **2,468
  passed, 1 failed**, 91 skipped. The failure: `RaisedGardenVerification.AMoundGrowsWithoutWaterOrMaladies` (cc-P128),
  "Expected: Seed, Actual: BowlOfDirt" at its line 243. It passed in the gated run of the same tree a minute earlier.
- run 2: `Server.Tests.dll` 893 passed, 0 failed; `UOContent.Tests.dll` **2,469 passed, 0 failed**, 91 skipped.
So the garden fact is a flake on the base (1 in 3 runs of this tree), P128's to look at; nothing here touches plants.
For the overseer's bug list beside P121's Wisp Orb and loot-box flakes.

**The test world boots clean.** `sl-modernuo:cc-p129` on a scratch copy of the test world's newest automatic backup
(`Backups/Automatic/2026-10-16-16-45-01`, a world saved by the running test shard before this change; it holds
`Server.Mobiles.DrelgorTheImpaler` in its mobile table and no parrot perch):
- boot 1: `[ShardVersion] Shattered Legacy 2026.10.16.3 (65 version(s) in the changelog)`, `Loading world done (207268
  items, 34967 mobiles) (3.05 seconds)`, listening; stopped: `Saving world done`;
- boot 2 on that save: `Loading world done (208676 items, 35085 mobiles)`, no error, saved again on stop;
- the one ERR line in both is the live-port guard (Test Center on, port 2593: my scratch config), P121 had the same.
- **Unverified:** the perch migration against an instance. The save has no ParrotPerchAddon or ParrotPerchDeed, so
  the v0 -> v1 `MigrateFrom` ran for nothing; the generator compiled it, and the facts round-trip a v1 perch and deed.
  The first saved perch meets it when a player crafts one.
- A first try mounted `Saves` alone, as the port recipe's old harness does, and the save on stop failed ("Cannot create
  Saves: a directory with the same name exists") and emptied it: the engine publishes a save by renaming Saves
  (docker-compose.test.yml, cc-P37). The recipe's harness line should mount the parent; said in the overseer items.

## Port-list numbers

`tools/progress.py`, before (HEAD, after P128) and after (this tree):

| | before | after |
|---|---|---|
| Creatures row | 109 / 193 | **138 / 193** (+29 files: 24 under Mobiles/Normal, 4 under Mobiles/Bosses, 1 under Mobiles/Named) |
| Pet Training row | 4 / 11 | 4 / 11 |
| Base items row | 172 / 298 | 172 / 298 |
| Ride-along (not counted) | 12 / 361 | 14 / 361 |
| Reward (not counted) | 288 / 717 | 292 / 717 |
| Port list, counted | 417 / 983 (42.4%) | **446 / 983 (45.4%)**, 3 of 16 systems in |

The 14 leaf files land in the uncounted tiers (the pelts and the statuettes are reward-tier, the parrot ride-along) or
under paths the list does not scan (`Items/Quest`, `Items/Internal`, `Items/Decorative`, `Items/Equipment/Clothing`).
**The Creatures row's ceiling is 176 now**, not 193: P119's 8 proxy misses and 8 already-in-pinned, plus Navrey, who
is CC6 batch 8's `NavreyNightEyes`. 55 remain in the row: the 12 Void creatures (with Covetous), 6 AI types (each an
AIType patch), 7 store mount statuettes, 5 peerless bosses with the Underworld and store work (AbyssalInfernal,
DreadHorn, PrimevalLich, ShimmeringEffusion, Travesty), and the rest of P119's "other" (Gregorio's quest,
GargishRouser's colossus, VoidManesfistation, HumanBrigand's commented file, AcidPopper the item). **The gate "Things
to fight" cannot close on this row alone**: its measure is the spawn-orphan list, 17 today (tools/spawn-orphans.txt:
16 NPCs that come with the Underworld and High Seas vendor rows, and the Sphynx), so it closes with those rows, not
with creature ports. `tools/spawn-orphans.txt` regenerated (18 -> 17, the iron beetle).

## Play-test items added

Through the For Chase list below; Who and steps in `testing/bot-triage.md` (P129 group) and `testing/playtest-steps.json`:
P129-1 BOT (built, `p129_1`), P129-2 EYES (bodies), P129-3 EYES (ability lists and the cold aura), P129-4 EYES (riding a
tiger, pelts), P129-5 BOT-PARTIAL (the gold foil), P129-6 EYES (the carving kit), P129-7 EYES (the parrot), P129-8 EYES
(the four bosses), P129-9 CHASE (seeding Old Haven), P129-10 CC (test world boot).

**P129-1 was built and run** (`Run-OvernightPlaytests.ps1 -SkipBuild -Only P129-1 -SkipSoak -NoEmail`, this tree's
image `sl-modernuo:cc-p129` tagged `sl-modernuo:bot`, a scratch copy of the test world), twice; both run folders are kept:

| Run folder | Result | Why |
|---|---|---|
| `testing/bot-runs/2026-10-16-1202` | FAIL 0/3 | The fights add up. Run 3's transcript: the blood fox's Bleed Attack and bites left the player at 139 of 175, the cold drake's aura (15 cold every 5 s) and bites at 62, and the stygian drake's spells killed it; the dragon wolf, the Butcher and Drelgor met a ghost. Run 1 died at the fox (its bleed kept ticking). **A check defect**, P119-1's own first-run lesson in another form: P119's fight topped the player up once; it now refills the player's hits before every creature (`_p119_fight`, both samples) |
| `testing/bot-runs/2026-10-16-1220` | FAIL 0/3 | With the refill: the fox, the cold drake and the stygian drake die in runs 2 and 3, then **the dragon wolf takes the player from 175 to 59 in 2.5 s and kills it**. Its DragonBreath, stored on the profile and fired through the twin before the admin's pin to 1 hit, deals 16% of the breather's current hits (pinned FireBreath, 800-860 hits): the ability core dispatching a ported creature's breath, live. Run 1 died at the fox: Grasping Claw ("The blow from the creature's claws has made you more susceptible to physical attacks", cliloc 1070836, in the 1202 run-1 transcript too) plus bleed plus 16-22 bites against a Dex 10 player swinging every few seconds. **A sample defect:** the two breathers are out (OsseinRam and Macaw in), the player gets Dex 100 for its swings, and stamina is refilled with its hits |
| `testing/bot-runs/2026-10-16-1235` | FAIL 0/3 | The fox and the ram die 3 of 3 now; the stygian drake 1 of 3 (its spells kill the player in 8 s) and the macaw 0 of 3 (Dex 400-500 and Wrestling 120-140: dead in 13 s); the Butcher and Drelgor met ghosts. The sample again: a bare-handed fair kill is for creatures that cannot kill a 175-hit player first. Final sample: BloodFox, OsseinRam, LeatherWolfFellow, GargishOutcast (either body), ParoxysmusSwampDragon, Drelgor |
| `testing/bot-runs/TBD4` | TBD4 | TBD4 |

The creatures did what their ServUO values say: the fox bled, the drake's aura burned, the drake cast. The bot says
"rule 1 held: both real shards are exactly as they were" in both runs.

## Deviations and decisions for Chase

1. **Frost Mite, Cold Wind** (the Wight's deviation from cc-P119, now reaching its second creature, as that note said it
   would). ServUO's only weapon ability on the mite is Cold Wind; pinned has none, so the mite has no weapon ability.
   Reverses when a `ColdWind` WeaponAbility is added (ServUO `Abilities/ColdWind.cs`, 100 lines, plus its slot in the
   upstream `WeaponAbility.Abilities` table). Reaches Wight and FrostMite.
2. **Saber-toothed tiger, stat loss on taming.** ServUO's `OnAfterTame` halves Str and Dex only (Int kept) when Pet
   Training is on; pinned has no `OnAfterTame` hook, so `StatLossAfterTame` gives `AnimalTaming.ScaleStats(0.5)`, which
   halves Int too. Reverses when `AnimalTaming` gains the hook (P130 patches that file for slots anyway). Reaches this
   creature only.
3. **Leather wolf, not repairable.** ServUO's `IRepairableMobile` (iron ingots, like a golem) has no pinned equivalent:
   pinned's `Repair` and `Bandage` test `is Golem` by type. Reverses when pinned's repair takes an interface or a list.
   Reaches this creature only.
4. **Gargish outcast, names.** ServUO draws from "Gargoyle Male" and "Gargoyle Female" lists that pinned's `names.json`
   does not have (its gargish list is "gargoyle vendor", 8 names, used for both sexes here). Reverses when the two lists
   reach `names.json`. The alternative was an unnamed outcast.
5. **Drelgor's taunt is silent.** ServUO broadcasts his line to every player in the "Old Haven Training" region (an
   `ApprenticeRegion` in ServUO's `Regions.xml`); pinned's `regions.json` has no such region, so the check, kept as
   written, never holds. Reverses when the region is added here (a `regions.json` row; the shard has none of its own on
   Old Haven, only the Burrows below it). Reaches this creature only.
6. **Three AI substitutions, cited, no new number:** TheButcher AI_Necro and LadyMelisande AI_NecroMage on AI_Mage
   (Q-050: pinned's MageAI casts Necromancy from skill), GargishOutcast AI_Mystic and MonstrousInterredGrizzle
   AI_Spellweaving on AI_Mage (D-41's shape: pinned has neither AI; both still cast what their skills allow).
7. **D-79, cited:** the four bosses are walk-up fights on the altar-less BasePeerless like the seven before them;
   LadyMelisande's helper wave takes ServUO's own no-altar arm (four satyrs).
8. **D-72 retired:** the Crystal Hydra's parrot pack is back, and the four bosses drop their parrots.
9. **Two ServUO slips fixed under the D-4 rule (broken, not missing), both logged in the file headers:** the iron beetle's
   mining timer is stopped when the beetle is deleted (ServUO never stops it); `Loot.RandomScroll(0, Length, ...)` in
   four constructors passes an index past the table one time in n+1 and packs nothing (ServUO's `Construct` refuses it
   silently), so the ports pass `Length - 1`.
10. **The achievement id `combat.drelgor` keeps its name** though it now names Vorlak: it is the save key for earned
    achievements, so renaming it would un-earn it for everyone who has it. Its text and trigger follow the rename.
11. **For the overseer's registers:** items 1 to 5 as deviations; D-72's retirement; `UndeadGargoyleMedallions` and
    `GargishRouser` as not ported (reasons above); Navrey as already ported (NavreyNightEyes), a proxy miss like the Clan ratmen.
12. **Three things found in passing, none mine to fix:** (a) `RaisedGardenVerification.AMoundGrowsWithoutWaterOrMaladies`
    (P128) failed 1 of 3 runs of this tree in the unfiltered suite, "Expected: Seed, Actual: BowlOfDirt": a flake for
    the bug list beside P121's; (b) `notes/port-recipe.md`'s headless-harness `docker run` mounts `Saves`, `Backups` and
    `Archives` separately, and on this engine the save on stop then fails and empties `Saves` ("Cannot create Saves");
    the parent folder must be mounted, as `docker-compose.test.yml` says since cc-P37: the recipe line is stale;
    (c) `docs/feature-queue.md` (F-47 to F-49, dated today) was uncommitted in shard-migration when I finished: the
    overseer's own edit, made while this ran, not mine. The Golem's commit stages everything, so it rides along;
    both repos were clean when I started.
13. **The Golem's start phrase** did not match "golem please resume working on the shard tasks" (the word "resume"),
    which the previous session's note also hit with a missing "the"; `Test-GolemPhrase` is an exact match after
    stripping punctuation. I re-queued P129 and ran the hook's own hand-off by hand so its DONE is committed; a looser
    match (any message starting "golem" that contains "work") would spare the next session that.

## For Chase

**Rebuild the test shard** (console, Test shard, Rebuild) before trying these. Nothing new is on a spawner until the
Old Haven seeder is run (item 9); everything else exists for `[add`.

1. **A fight (the bot runs this one):** `[add BloodFox`, `[add OsseinRam`, `[add LeatherWolfFellow`, `[add GargishOutcast`, `[add ParoxysmusSwampDragon` and `[add Drelgor` next to a player and kill each: each shows, fights back, dies and leaves a corpse.
2. **Bodies by eye:** `[add` each of BloodFox, OsseinRam, FrostMite, Lion, Triceratops, SabertoothedTiger, CrimsonDrake, PlatinumDrake, StygianDrake, GiantTurkey, DragonWolf, Viscera, ShadowDweller, Macaw, StoneMonster (six forms), LeatherWolf, TheButcher, GargishOutcast, WildTiger, WildWhiteTiger and WildBlackTiger, and walk close: each draws as a whole creature and animates when it moves and attacks.
3. **Ability lists and the cold aura:** `[add ColdDrake`, `[props` it, open AbilityProfile: AbilityNames reads DragonBreath, AuraDamage, once each; a `[add Lion` reads Piercing, Heal; a `[add OsseinRam` reads BattleDefense, LifeLeech. Stand a player near the cold drake: 15 cold every five seconds, a blue swirl and "The intense cold is damaging you!".
4. **Ride a tiger, carve one:** tame a `[add WildTiger`, set CanRide true in `[props` and double-click it as its owner: you ride it. Kill and carve a `[add WildBlackTiger`: four black tiger pelts on the corpse.
5. **The gold foil:** `[add MacawSpawner` on open ground (a foil sheet with a nest); as a player pick the foil up (half the time it refuses to move): three to five vicious macaws attack, the foil vanishes for a minute or so and returns.
6. **Carve a pumpkin:** `[add PumpkinCarvingKit` in your pack, `[add CarvablePumpkinTall` on the ground; use the kit on the pumpkin: a carved face named "carved pumpkin", "Carved By" you, the kit spent; double-click the carved pumpkin to light it.
7. **A parrot:** in a house you own, `[add ParrotPerchDeed` and place it; `[add ParrotItem`, use it on the perch: a pet parrot sits there (a second item is refused). Drop a `[add ParrotWafer` on it (a pirate line); say things near it (it repeats one in twenty). Chop the perch: the deed reads "Includes a pet Parrot"; place it again: the same parrot is back.
8. **The bosses:** `[add ChiefParoxysmus` and send a pet at him (he eats it and heals; a player hitting him from range is pulled to his side); `[add LadyMelisande` (four enslaved satyrs appear); `[add MonstrousInterredGrizzle` and hit him (green ooze that burns 40 poison); `[add CrimsonDragon` and walk a player up (frozen five seconds with the terror line).
9. **Old Haven:** `[ClusterFSeedOldHaven dryrun` reports one spawner to create (Drelgor) and the rest skipped, Vorlak's old spawner among the skipped; `[ClusterFSeedOldHaven missing`; `[go 3651 2509` on Trammel: Drelgor the Impaler, a bone-armoured skeleton, in the ruins; `[go 3622 2488`: Vorlak the Impaler still spawns, under his new name, and killing him still earns "You Fought a Man Called 'The Impaler' and Won". **Then choose Vorlak's new spot**: his seeder entry (`ClusterFOldHavenSeeder.cs`, the first row) is where it was; I moved nothing.
10. **Test world boot:** done by CC on a scratch copy (below).

Also for Chase, not a test: ServUO places 23 macaw nests on the Ter Mur cliffs from its Time of Legends generator
(`MacawSpawner.Generate()`, ported, called by nothing). Say if you want them placed, and where it should be wired
(a staff command, or the seeder pattern).

## Repo size rule

No pending file in either repo is over 5 MB. The largest pending in the shard repo is `ClusterFAchievements.cs`
(111 KB, four edited lines); the largest new file is `CrimsonDragon.cs` (about 10 KB). In shard-migration the largest is
`testing/playtest-steps.json` (98 KB). Build logs, the scratch world (28 MB), the break sets, the dependency scanner
and the patch's staging folders stayed in the session scratchpad, outside both repos. Docker images stayed in Docker.

## Commit preflight

TBD
