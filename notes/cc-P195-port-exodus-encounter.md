# cc-P195: port The Exodus Encounter

Prompt: `cc-P195-port-exodus-encounter.md`. Branch `golem/Bronze/P195` in both work copies. Date: 2026-10-21.
Source: ServUO pub57 `Scripts/Services/Revamped Dungeons/TheExodusEncounter/` (38 row files) plus the pieces ServUO
keeps elsewhere (the generator, the spawn XML, the decoration cfg, six craft recipes, the Mining blackrock row, the
stock minion's component drop, the Detect Hidden reveal). Authority: pinned ModernUO (`D:\UO\ModernUO-pinned`).

## Headlines

- The whole encounter is on the shard: 43 files under `server/customizations/Services/Revamped Dungeons/TheExodusEncounter/`
  (9 creatures, 1 NPC, 13 items, 10 artifacts, 3 resources, the controller, the region, the spawns, the decoration,
  the generator, the shared statics), 4 leaf files ServUO had in its engine (BaseDecayingItem, NexusAddon,
  IRevealableItem, AbyssalCloth), one craft registration file, one engine patch (Detect Hidden reveals
  IRevealableItem), three one-hunk edits to shard files (loot box tier, monster stealing's zealot key, the Thieves'
  Den place rule).
- Port list row: The Exodus Encounter 1 / 38 before, 38 / 38 after (`tools/progress.py` on this branch).
- Nothing was blocked by the client: every item id, the Nexus art (19316 to 19327), body 1248 and the dungeon's
  tiles are in our client data. Clilocs could not be read by tool (the compressed Cliloc.enu); every number is
  ServUO's and is listed in the play tests for the bot to confirm.
- Two shard rules met the port and the shard won both: Clockwork Exodus is a loot box boss (F-40, tier 5) and the six
  recipes sit under the shard's recipe gate (cc-P78). Everything else is ServUO's, with the recipe's standard
  substitutions (AI_Mage for AI_Mystic, HasAura for SetAreaEffect, GetWeaponAbility, MonsterAbilities) and the
  deviations listed for Chase below.
- Tests: `server/tests/Services/Revamped Dungeons/TheExodusEncounter/ExodusEncounterVerification.cs`, 10 facts,
  each seen failing first on a mutated copy of the tree (the section below), then the full gate green and a headless
  boot of `sl-modernuo:cc-P195` on a scratch world.
- Nothing is placed at boot. Chase runs `[GenExodusEncounter` once on the live shard (Staff patch note).

## What changed, with file:line

All paths under `D:\ShatteredLegacy\server\` unless noted. ServUO paths are under `Scripts/`.

### The shared pieces

- `customizations/Services/Revamped Dungeons/TheExodusEncounter/ExodusEncounter.cs:28-136`: the places ServUO
  hard-codes (controller 849,648,-40; Exodus 854,642,-40; arrival 764,640,0; gate 761,641,0; ankh 757,641,0; Hunter
  946,641,-79), `Wear` (ServUO `BaseCreature.SetWearable`, :72), the valiant-reward set (ServUO's
  `PlayerMobile.HasValiantStatReward`, saved by `ExodusEncounterPersistence`, :138), and the stock
  `ExodusMinion` corpse drop of a Mechanical Component one time in five (ServUO `Mobiles/Normal/ExodusMinion.cs:225`,
  through the creature death event, :88).
- `VerLorRegController.cs:15-139`: ServUO's controller (item 7107 at 849,648,-40). `Start`/`Stop` (:57-59) are the
  static calls ServUO has; `StartHere`/`StopHere` (:62, :89) the instance work (raise Clockwork Exodus at
  854,642,-40 home 4; delete him). `IsRunning` is the command property; `Exodus` the saved boss.
- `Region.cs:18-201`: "Ver Lor Reg" is not in our regions.json, so `ExodusRegions.Register` (:44) builds
  `VerLorRegCity` (a DungeonRegion, priority +1, ServUO's four rectangles from `Data/Regions.xml`, go 840,571,0)
  on Ilshenar at startup (:36). `OnDeath` of the boss (:136) stops the controller and starts the exit (:147): the
  1010589 warning at eight minutes, the move to one of ServUO's eight `RandomLocations` and a new Exodus two minutes
  after (`PlayersHere`, :158, D-20). `CheckTravel` allows teleport only, as ServUO's `AllowTeleport` region does.
- `ExodusSpawns.cs:35-154`: ServUO `Spawns/TheExodusEncounterQuest.xml`, 17 rows as `Definitions` (:40), the spawner
  pattern (`Spawner(amount, 5 min, 10 min, 0, rect)`, one entry per type, `Respawn()`), and `PlaceArchZealot` (:144)
  for the row that is a single Mobile, not a BaseCreature.
- `ExodusDecoration.cs:11-48`: ServUO `Data/Decoration/Ilshenar/TheExodusEncounter.cfg`: 39 Nexus points and the
  Keypunch Reader at 1987,88,-28.
- `ExodusMiningBonus.cs:12-60`: ServUO `Services/Harvest/Mining.cs:116`, the blackrock row (100 Mining, 0.1,
  1077180) appended to pinned's ore bonus table at world load, idempotent (`Apply`, :36).
- `Generate.cs:18-72`: `[GenExodusEncounter` (WorldGeneration, Replaces: deletes the collection first) and
  `[DeleteExodusEncounter` (WorldRemoval); ServUO `Services/Revamped Dungeons/TheExodusEncounter/Generate.cs`. Every
  placed thing is in the `exodusencounter` weak entity collection.

### Mobiles (`Mobiles/`)

- `ClockworkExodus.cs:31-328`: body 1248, 50,000 hits, AI_Mage (D-1), BleedAttack by `GetWeaponAbility` (:113), the
  aura of energy as `HasAura`/`AuraDamage` with ServUO's `AreaEffects.cs:234-249` numbers (:116-147, D-2), three
  vortices per new target spot on every melee blow given or taken and every spell (:210-257), the gold rain within
  eight (:179-207, `GoldTimer` :286), one artifact in five to a random player with looting rights (:155), `MinHits`
  saved per instance (ServUO's static, D-14), `Instances` kept clean on delete, `IRareSelfRepairSource` for F-40.
- `DeathVortex.cs:12-90`: the trap (0x3789, 15 seconds) draining mana or stamina on trigger.
- `ExodusDrone.cs`, `ExodusJuggernaut.cs`, `ExodusMinionLord.cs`, `ExodusSentinel.cs`: ServUO's four clockwork
  ExodusMinion-likes with pinned's `MonsterAbilities.MagicalBarrier` and `EnergyBoltCounter` (ServUO's
  `m_FieldActive` barrier and `OnDamagedBySpell` bolt are these two in pinned, `Mobiles/Monsters/ML/...`).
- `ExodusZealot.cs:12-74`: hooded shroud and spellbook worn, title "The Exodus Zealot"; the thief's key source
  (monster stealing, below).
- `DupresChampion.cs`, `DupresKnight.cs`, `DupresSquire.cs`: Dupre's men (FightMode.Aggressor, blue, gear via `Wear`);
  ServUO's `CanBeParagon => false` is `OnBeforeSpawn` undoing a paragon roll (D-5).
- `ExodusArchZealot.cs:18-196`: Hunter, a blessed Mobile that cannot walk, the Talk context entry (6146) and his
  ten-page gump (1153670 to 1153689), and the human-to-gargish dagger swap on drop.

### Items (`Items/`)

- `ExodusChest.cs:21-287`: a hidden, locked, poison-trapped DecorativeBox with ServUO's loot (1,500 to 3,000 gold,
  gems, 20 percent smoke bombs, potions, an essence, a peerless ingredient, one chest in five a ritual key), revealed
  at 98 Detect Hidden within three tiles (`CheckReveal`, :78) or sensed by a passing rogue of 80 or more
  (`CheckPassiveDetect`, :86, through a 5x5 `ExodusChestRegion` of its own since pinned has no passive detect
  hook), deleted five minutes after the reveal (:101). Unlocked chests are deleted after a load, as ServUO does.
- `ExodusNexus.cs:18-542`: the Nexus machine (a NexusAddon of 13 components, hued broken), ServUO's depth-first
  circuit path over a `SideLength` square (:60-148), the gump (`NexusGameGump`) and its logic split into `Respond`
  (:231) and `ButtonFor` (:326) so the facts can play it; `Solve` (:210) prints a punch card and turns the machine
  on for ten minutes; a wrong step shocks for 60 energy three times, frozen (D-10).
- `ExodusSacrificalDagger.cs:20-202`: the dagger (a BaseKnife of 0x0F52, a week's lifespan of its own, as ServUO),
  `Sacrifice` (:80) is the target's work (10,000 karma, Ritual2); `ExodusSacrificalGargishDagger` (:194) is the
  gargish one (D-6).
- `ExodusSummoningAltar.cs:18-157`: the deed (class `ExodusSummoningAlter`, ServUO's spelling), `Build` (:85, the
  target's way in; :97 the checks on a tile given by hand, D-21) is the target's work, `CheckExodus` (:78) the 75/60 percent gate, `ShrineSpots` (:21) ServUO's eight tome spots.
- `ExodusSummoningRite.cs:11-96`: the rite, `Read` (:51), Ritual1.
- `ExodusTomeAltar.cs:27-290`: the tome and its four hued steps (`ExodusAlterAddon`), seven minutes, the ritual list
  per party member (`RitualArray`, :251), `HasUsedRite` (:76) standing in for ServUO's `PlayerMobile.UseSummoningRite`
  (D-12), Begin the Ritual (`SendConfirmationsExodus`, :149: the owner, the party, everyone within five tiles, every
  member's rite and dagger and robe) and `SendBattleground` (:188: the party and its pets to 764,640,0 on Ilshenar,
  the robes burned, the tome deleted two seconds later).
- `ExoticToolkit.cs:10-60`, `KeypunchReader.cs:12-81` (`CheckItems`, :62: fifty cards and a kit make a Nexus deed),
  `MechanicalComponent.cs` (Tinkering 80 makes a kit), `PunchCard.cs` (six hours), `RobeofRite.cs` (hue 2702, its own
  week's clock), `ExodusAlterAddon.cs`.
- `Loot/`: the ten artifacts (`Asclepius`, `BracersofAlchemicalDevastation`, `ClockworkLeggings`, `DupresSword`,
  `HygieiasAmulet`, `ScrollofValiantCommendation`, and the four gargish ones). The scroll's one-time +5 StatCap uses
  the saved set in `ExodusEncounter` (D-13). Two weapon attributes ServUO sets have no pinned counterpart (D-15).
- `Resources/`: `GoldDust` (0x4C09), `NexusCore` (0x4B82), `SmallPieceofBlackrock` (0x0F28); the two commodities
  carry `DescriptionNumber`.

### Leaf files ServUO keeps in its engine

- `customizations/Items/Functional/BaseDecayingItem.cs:14-162`: ServUO `Items/Functional/BaseDecayingItem.cs`, the
  ten-second slice, `Lifespan`/`UseSeconds`, the 1072517 property line, restarted after load; `DecayingLifespan`
  (:100) is the same property line and expiry for the dagger and robe, which decay on their own base classes.
- `customizations/Items/Addons/NexusAddon.cs:10-54`: ServUO `Items/Addons/NexusAddon.cs` (13 components, ServUO's
  doubled 19319 kept), the deed.
- `customizations/Skills/IRevealableItem.cs:9-21`: ServUO `Skills/DetectHidden.cs`'s interface.
- `customizations/Items/Resource/AbyssalCloth.cs:11-36`: the Robe of Rite's cloth (0x1767, hue 2075); no source on
  the shard yet (D-8).
- `patches/DetectHidden-revealable-items.patch` (applied at `docker/uo/apply-patches.sh:556`): pinned's
  `DetectHidden.cs` reveals an `IRevealableItem` (ServUO `Skills/DetectHidden.cs:116-126`) after the trap branch.
  Alternatives argued: a shard-side `[OnEvent]` has no hook on the skill's target; a copy of the whole skill file
  would shadow pinned's. The hunk is three lines.

### Shard files touched

- `customizations/Engines/Craft/ExodusCraftRegistrations.cs:29-97`: ServUO's six recipes (`DefBlacksmithy.cs`,
  `DefCarpentry.cs`, `DefInscription.cs`, `DefTailoring.cs`, `DefAlchemy.cs` in pub57): the dagger (Blacksmithy
  95 to 120, 12 iron, 2 blue diamond, 2 fire ruby, 10 blackrock, never exceptional), the altar deed (Carpentry 95
  to 120 with Magery 75; 10 boards, 5 Nexus Cores, 5 Gold Dust, 10 blackrock), the rite (Inscription 95 to 120; 5
  scrolls, 5 Gold Dust, 2 Nexus Cores), the robe (Tailoring 101.5 to 120; 15 cloth, 10 abyssal cloth, 2 Nexus Cores,
  2 Gold Dust), Nexus Core and Gold Dust (Alchemy 90 to 120). `Register` is idempotent and runs at ServerStarted.
- `customizations/LootBoxes/ClusterFLootTable.cs:126`: `["ClockworkExodus"] = 5` in `BossTier`.
- `customizations/Services/Monster Stealing/Core/StealingHandler.cs:122-127`: `MakeSpecialFor` gives an
  `ExodusZealot` one of the four ritual keys (ServUO `StealingHandler.cs:95-99`).
- `customizations/Services/Monster Stealing/Core/ThievesDenStealRules.cs:200-206`: a zealot outside the covered
  places counts as `StealPlace.FacetDungeon` (the Exodus Dungeon is not in the place table; the rank rule still
  applies).
- `docker/uo/apply-patches.sh:556-558`: the new patch's apply line.
- `CHANGELOG.md`: `## 2026.10.20.17` (Added, Staff); `VERSION` 2026.10.20.17.

### Docs repo

- `testing/playtest-steps.json`: P195-1 to P195-10; `testing/bot-triage.md`: the P195 table.
- This file.

## Client check

Done first, from `D:\UO\tool-trials\client-data-copy` (the vseUOAware tools errored all session; `tiledata.mul`,
`artidx.mul` and `mobtypes.txt` were parsed directly). Every ServUO item id used resolves in tiledata (0x0F52,
0x406A, 0x14F0, 0x1767, 0x1F0D, 0x4C09, 0x4B82, 0x0F28, 0x2DF5, 0x3789, 0x1F6A, 0x9A9E, 0x4CA7, 0x3F3A, 0x1F43,
0x4D1C, 0x13CB, 0x1411, 0x4A5F, 0x1413, 0x13B9, 0x0905, 0x1088, 0x41A7); the Nexus art 19316 to 19327 is present;
body 1248 is in mobtypes.txt; the tome's step tiles and the shrine floor range 0x149F to 0x14D6 are present. Nothing
is missing. Clilocs: not verifiable by tool (Cliloc.enu is the compressed form); listed in the play tests.

## Tests

`server/tests/Services/Revamped Dungeons/TheExodusEncounter/ExodusEncounterVerification.cs` (10 facts, the
Sequential UOContent collection, every fact clears every Exodus object first and last, Ver Lor Reg and the shrine
region registered in the fact that needs them):

1. `GenerateBuildsTheEncounterAndDeleteRemovesIt`: the report; the controller running with its boss at 854,642,-40 in
   Ver Lor Reg; the gate, the ankh, 39 Nexus (broken, each with a path), the reader, Hunter; 16 spawners from 17 rows,
   capacity 90 all spawned on the right map with the right range and delays, 12 hidden locked chests with regions;
   delete removes all of it and `AnyPresent` turns false.
2. `EveryCreatureConstructsRoundTripsAndKeepsItsShape`: the nine creatures construct, round-trip, keep body/hue/hits/
   fame; the four clockworks carry both abilities; the lord's lowercase name; the zealot's shroud; the boss's body,
   hits, MinHits, BleedAttack, aura, Instances; every spawn row's type name resolves.
3. `EveryItemConstructsAndRoundTrips`: 30 item types construct (through `Loot.Construct`, as `[add` does) and round-trip (id, hue, label), the tome with its owner; the dagger's, robe's
   and card's clocks; the tome's steps and owner; the nexus's side and path; the chest's gold and lock; the scroll's
   owner.
4. `TheRitualBuildsTheTomeAndCarriesThePartyToVerLorReg`: the deed refuses a tile that is not a shrine floor, builds the tome at 1858,875,12 with a party, a
   second deed refuses, a stranger's rite is ignored, the dagger before the rite does nothing, the rite marks
   Ritual1 and `HasUsedRite`, a second rite refuses, the dagger marks Ritual2 and gives karma; a far member holds the
   ritual; the owner's go moves both to 764,640,0 on Ilshenar without robes and the tome is gone in two seconds.
5. `TheBossDeathStopsTheControllerAndTheExitRaisesANewExodus`: the MinHits gate at 50/70/100 percent; three
   vortices once per spot, gone in fifteen seconds; the kill stops the controller; eight minutes warn; ten minutes
   move the player to a RandomLocation and raise a new boss; the controller round-trips with its boss.
6. `TheHiddenChestIsSensedRevealedAndGone`: 97 fails, 98 within three reveals, four tiles does not; passive never
   at 79, sometimes at 90, never at five tiles; the reveal shows it (maybe a key) and five minutes delete it and its
   region; `GiveRituelItem`.
7. `TheNexusPuzzleRepairsTheMachineAndAWrongStepShocks`: the toolkit opens the puzzle; the right arrows end in a
   punch card, hue 0, ten minutes broken again; a wrong arrow takes hits, freezes, frees in fifteen seconds; too far
   closes the session.
8. `TheKeypunchReaderTheComponentAndTheScrollDoTheirJobs`: Tinkering 79.9 fails and 80 makes the kit; 49 cards and
   a kit do nothing, 50 make the deed and keep the kit; the scroll gives +5 once and the second is refused.
9. `TheBossIsALootBoxBossTheZealotYieldsAKeyAndTheCraftsmanPathIsRegistered`: `ClusterFLootBoxes.IsBoss`, tier 5;
   `StealingHandler.MakeSpecialFor` yields a key; the six craft entries are present with the dagger's blackrock and
   `ForceNonExceptional`; the blackrock bonus row is added once.
10. `DecayingItemsCountDownAndExpire`: the card's six hours tick down ten seconds a slice; card, dagger, robe and
    tome expire.

### Seen failing first

One break per fact on the real tree (`p195_breaks.py` in the session scratchpad: pristine copies and SHA-256 hashes
taken first, the ten facts run alone on the builder image `sl-uo-builder:cc-P195` with the broken files mounted over
their copies, the same `dotnet test` the gate runs, then the files restored and hashed byte-identical). Log
`probe-P195-red.log`: 10 run, 10 failed, each by its own break.

| Fact | Break | Red |
|---|---|---|
| 1 generate and delete | the boss's `RangeHome` 4 to 5 (`VerLorRegController.cs`) | Expected 4, actual 5 |
| 2 creatures | the lord's name capitalised | Strings differ: "exodus minion lord" |
| 3 items | the tome's steps one z higher | Expected (1857, 874, -6), actual (1857, 874, -5) |
| 4 the ritual | the party range 5 tiles to 50 | Assert.False: a member ten tiles off no longer holds the ritual |
| 5 boss death and exit | `ExitWarning` 8 min to 9 | the player is still at 840,600,0 ten minutes after the kill |
| 6 the hidden chest | `CheckReveal` 98 to 99 Detect Hidden | Assert.True: 98 no longer reveals |
| 7 the nexus puzzle | `RepairDuration` 10 min to 20 | Expected hue 1987, actual 0 (still running at ten minutes) |
| 8 the reader, component, scroll | `CardsNeeded` 50 to 51 | Assert.True: fifty cards no longer make the deed |
| 9 loot box, stealing, crafts | the boss's tier 5 to 4 | Expected 5, actual 4 |
| 10 decaying items | the punch card's lifespan 21600 to 21000 | Expected 21600, actual 21000 |

The Detect Hidden patch is not covered by a fact (the test host installs no skill callbacks); the patch gate applies
it (`[patches] Applied: DetectHidden-revealable-items.patch` in every cycle's log) and P195-3 is the bot's.

### Full gate

`docker\uo\build.sh -t sl-modernuo:cc-P195` (patches gate, test gate, image), run detached from the agent shell under
the docker-build lock (taken 21:19, released 21:49 CDT; free memory 9.4 GB of 31.7 before the first cycle). Logs
`build-P195-c1.log` to `build-P195-c7.log` and `probe-P195-1.log` to `-5.log` in the session scratchpad.

| Cycle | Result |
|---|---|
| 1 | content red: `[OnEvent]` needs `using ModernUO.CodeGeneratedEvents`; `CanFortify` is not a pinned jewel member (dropped) |
| 2 | content red: `WeaponAttributes` on armor and `HitManaDrain` have no pinned home (D-15); `Effects.PlaySound` takes a point; the mining hook's `WorldLoad` delegate shape |
| 3 | tests red: `Body` compares by `BodyID`; `StaticTarget` needs `using Server.Targeting`; `CraftRes` is a list, not a collection with `GetAt` |
| 4 | tests red: xUnit2031 (no `Where` before `Assert.Single`) |
| 5 | compiles; 1,643 tests, 1,634 passed, 5 failed: the tome has no parameterless ctor (ServUO's takes an owner; left out of the generic loop), `new Party(leader)` does not set the leader's `Party`, the nexus shock killed a 55-hit test character (D-10), the exit never found the player (D-20), and the shard's `CommandDeclarationVerification` wanted `[ShardCommand]` on ServUO's two debug gump commands (`[ExodusArchZealotGump`, `[TomeAltarGump`: DevTool, added) |
| 6 | 1,643 tests, 1,636 passed, 3 failed: `GoldDust`'s optional amount defeats `Activator.CreateInstance` (the loop uses `Loot.Construct`, as `[add` does), the deed's `StaticTarget` masked its tile id to 0 (D-21), the exit (D-20: the player was now flagged before `MoveToWorld`, but pinned's `GetPlayers` walks clients) |
| probes 1 to 5 | the ten Exodus facts alone on the builder image with the edited files bind-mounted (about 90 seconds each, no lock): found D-20, D-21 and that `EquipItem` refuses in the host (`AddItem`, cc-P193's finding); probe 5: 10 of 10 green |
| red probe | the ten breaks: 10 of 10 red (table above); files restored byte-identical |
| 7 (full) | **green: 1,643 tests, 1,639 passed, 4 skipped (the map-data facts, as always), 0 failed; image `sl-modernuo:cc-P195` built** (labels sl.commit=7e1f887, sl.dirty=1: the branch uncommitted); all ten Exodus facts in the run |

### Headless boot

`sl-modernuo:cc-P195` on a copy of the overnight bot's scratch world (`D:\UO\bot-shard\world\Saves`, 29 MB; the Backups
and Archives folders left empty in the copy), the world folder mounted as the compose file mounts it, the bot's
Configuration with listeners 127.0.0.1:2593 and autosave off, client data from the UOAlive 7.0.116.0 folder, no port
published, under the test-shard lock (21:49 to 21:51 CDT; the nightly bot was idle, last run 01:30). `boot-P195-1.log`,
`boot-P195-2.log` in the session scratchpad; the scratch world was deleted after.

- boot 1: `[ShardVersion] Shattered Legacy 2026.10.20.17 (119 version(s) in the changelog)`, `Loading world done
  (210942 items, 35148 mobiles) (3.79 seconds)`; stopped with `docker stop -t 90`, which SaveOnShutdown turns into a
  save: `Saving world done`, `Writing world save snapshot done (0.78 seconds)`, `...saved in 891 ms`, `Shutting down`.
- boot 2 on that save: `Loading world done (212980 items, 35335 mobiles) (2.58 seconds)`, saved the same way.
- Zero `Exception` lines in either log. The only ERR line is the bot configuration's own test-center warning about
  port 2593 (loopback here, nothing published); the one WRN is the stock `stats` command double registration, which
  every boot prints.
- The encounter was not generated in the boot (the container console takes no `[` commands); nothing in that world
  is a type of this port, so the load proves the assembly and the new types' registration, and the facts prove the
  generate, the round trips and the save shapes. `[GenExodusEncounter` on the test shard is P195-1.

## Port-list numbers

| Row | Before | After |
|---|---|---|
| The Exodus Encounter | 1 / 38 | 38 / 38 |

`SL_SHARD=D:/UO/golems/Bronze/ShatteredLegacy python tools/progress.py` reports the row complete (38 candidates,
38 done).

## Deviations and decisions for Chase

Numbered D-n; each is the port's choice, Chase's to overturn.

- D-1 AI_Mystic is AI_Mage. Pinned has no mystic AI; AI_Mage casts from the skills the boss has. The same mapping
  cc-P194 used for AI_Necro. His Mysticism and Necromancy 120 stand for resists and the record.
- D-2 The aura fires every five seconds (pinned's `AuraInterval`), not ServUO's every-tick-with-30-second-cooldown.
  cc-P194's D-147 shape. Numbers (20 to 30 energy, range 5, 1072073, the sparks) are ServUO's.
- D-3 The gargish dagger has no race lock: pinned weapons have no `RequiredRace`. Hunter still swaps it only for a
  gargoyle, as ServUO does.
- D-4 `Alterable` attributes (the human artifacts alterable into the gargish ones at a tinker) are dropped: pinned has
  no alteration system. The gargish artifacts drop in their own right from the ten-strong table, as in ServUO.
- D-5 `CanBeParagon => false` on Dupre's men is `OnBeforeSpawn` turning a rolled paragon back; pinned has no
  virtual. The clockworks and zealots can be paragons in both.
- D-6 ServUO's spawn XML has two rows at the same spot twice (the duplicate chest rows); kept as rows, so there are 16
  spawners not 14. The capacity is ServUO's 90.
- D-7 Hunter the Arch Zealot is placed by the generator, not spawned: he is a Mobile, not a BaseCreature, and a Spawner
  cannot make him.
- D-8 Abyssal cloth has no source on the shard: ServUO gets it from Underworld's sliths and the abyss peerless. The
  robe's recipe needs ten. Until Underworld or a vendor lands, the robe comes from the chests, the zealots and the
  Craftsman cannot make it. F-note for the queue if Chase wants a vendor line.
- D-9 The six recipes are under the shard's recipe gate (cc-P78): hidden until learned. ServUO shows them on
  skill. The gate's rule stood everywhere else, so it stands here; the scroll of each recipe is not placed anywhere
  yet, so Chase decides where (a drop from the clockworks is the obvious spot).
- D-10 The Nexus's shock is 60 energy as ServUO's `DoDamage`; a fresh test character has about 55 hits and died of
  the first shock before it could be frozen, so the fact gives it 125 Strength first. Nothing changed in the item.
- D-11 1114444 ("The lock is beyond your ability") is used by the chest as ServUO does; the number is nonlocal for
  the Exodus set but is a stock cliloc.
- D-12 ServUO's `PlayerMobile.UseSummoningRite` flag (set by the rite, cleared by the dagger) is read from the tome's
  own ritual lists (`HasUsedRite`): pinned's PlayerMobile is not patched for one flag, and the lists are what the
  flag stood for. A difference: in ServUO the flag outlives the tome; here a decayed tome forgets the rite, so the
  dagger needs a new rite. Seven minutes is the window either way.
- D-13 `HasValiantStatReward` is a saved set in `ExodusEncounter` (GenericPersistence "ExodusEncounter"), not a
  PlayerMobile flag, for the same reason.
- D-14 `MinHits` is per boss instance and saved; ServUO's is a static (one boss at a time makes them the same).
- D-15 Two attributes have no pinned home: `WeaponAttributes.HitLightning` on the bracers (armor carries no weapon
  attributes in pinned) and `HitManaDrain` on Dupre's sword (pinned has no such attribute). Both are commented at the
  line. The rest of each artifact is ServUO's.
- D-16 Clockwork Exodus is tier 5 in the loot box table (the same tier as the other 50,000-hit bosses in it); the
  shard rule (F-40) wins over ServUO's loot-only death.
- D-17 The ExodusMinionLord's name is ServUO's lowercase "exodus minion lord"; kept (names stay ServUO's).
- D-18 Nothing is placed at boot. ServUO's Initialize placed the controller on every boot; here `[GenExodusEncounter`
  is the one way in, as for every other generated place on the shard.
- D-20 The exit's "every player in the city" is `PlayersHere` (pinned's `GetMobiles` filtered to players of Player
  access), not pinned's `GetPlayers`: pinned's walks connected clients only, ServUO's walks the sectors' players
  (a logged-out character standing in Ver Lor Reg is moved too, as ServUO does). `Region.cs:158`.
- D-21 The Summoning Altar deed's `Build` has a `(from, tile, itemID)` overload the target calls; the facts use it
  because a `StaticTarget` masks its item id to 0 in the test host (no tile data, D27). Same checks, same order.
- D-19 ServUO's `ExodusTomeAltar.Altar` static is never assigned by ServUO; its null test in the deed always passes.
  Kept as ServUO runs it rather than fixed into a one-tome-per-shard rule ServUO never had.
- Q-1 ServUO's chest stealing (`StealingHandler`) gives the key to a thief of any skill; the shard's rank rule
  (`ThievesDenStealRules`) applies to the zealot. The zealot's rank is 0 (no entry), so the first rank's rule holds.

## For Chase

- Rebuild the test shard from this branch (`sl-modernuo:cc-P195`), then as staff run `[GenExodusEncounter` once.
  The report line counts everything it placed. `[DeleteExodusEncounter` takes it all down.
- See: `[go 849 648 -40` (Ilshenar; the controller and Clockwork Exodus beside it at 854,642), `[go 761 641 0` (the
  exit moongate and the ankh), `[go 946 641 -79` (Hunter), `[go 1969 114 -28` (the Exodus Dungeon's halls),
  `[go 2011 67 -27` (a Nexus machine), `[go 1987 88 -28` (the Keypunch Reader), `[go 1858 876 12` on Trammel (the
  Shrine of Compassion, the tome's spot).
- Play tests P195-1 to P195-10 in `testing/playtest-steps.json`; the bot takes the server-sent parts (triage table).
- Decide D-8 (abyssal cloth's source) and D-9 (where the recipe scrolls drop) when convenient; neither blocks the
  encounter's fighting, stealing or chest paths.

## Repo size rule

No file over 5 MB; the largest new file is `ExodusNexus.cs` (542 lines). No binaries.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, run 21:51 CDT. The script
reads the main desks (`D:\ShatteredLegacy`, `D:\UO\shard-migration`), not this Golem's work copies, so the pending files
it lists are another task's (cc-P226, Arms Lore) in flight on those desks; this branch's files are committed by the
Golem from `D:\UO\golems\Bronze\...` after P195 DONE. Result table as printed:

```
Repo    Result
----    ------
code    dry run
docs    dry run
scripts clean
```

Also printed: "prompts with a finished note: left: cc-P180, cc-P181, cc-P185 (note does not end in DONE or STOPPED
yet)", none of them this task's.

P195 DONE
