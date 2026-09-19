# CC4 Despise — the first Revamped Dungeons port

2026-09-19. One dungeon, complete: DespiseRevamped. Built through `build.sh`, 48 tests green (44 + 4 new,
one proved red on purpose), and the spawns generate on the real Trammel map: 47 spawners, 227 creatures,
save and reload identical. Shard commit `fa2463c`. Nothing here has been seen in a client.

The brief asked four questions beyond the port; they are answered in §3 (regions), §4 (spawns),
§5 (ReforgedSuffix) and §10 (the row re-costed). Deviations are §7, paper-only differences §8, the one
upstream patch §9, what it cost §11.

**Counts that moved while doing this, so nobody plans from the old ones:**

- **"DespiseRevamped's 4 files" is 13 ServUO `.cs` files plus a 1,975-line XmlSpawner XML.** The four in the
  directory (1,695 lines) are a hub; nine more (3,278 lines) live under `Mobiles/`, `Items/` and `Misc/`,
  and the dungeon does not exist without them. 4,973 lines of C# in, 4,684 out in 14 files. **The
  ShatteredLegacy commit message says "12 files, 4,269 lines"; that figure was summed in my head and is
  wrong. 13 and 4,973 are counted (§2).** Eleven for eleven.
- **The XML asks for 229 creatures and can hold 227.** Two rows ("DespiseRevamped #13" at 5495,748 and
  "#14") have MaxCount 9 over eight entries capped at one each. Same on ServUO.
- **The 30 lower-level spawners construct nothing on ServUO pub57 as shipped** (§4.3, Q-044). Read, not run.
- **HEAD did not build.** `e1e3c36` (today, "MAKE X ... confirmed in a client") calls a gump-builder overload
  the pinned commit does not have. §9.2, Q-045.

---

## 1. The headline, and what "done" was measured against

`docs/tasks.md`: *"Done when: each dungeon builds and its spawns generate."* Both halves were measured, the
second on the real map and not only in the test host:

| Gate | Result |
|---|---|
| `build.sh` (patches, tests, image) | green, `sl-modernuo:cc4`; 16 patches applied, 48 tests passed, `structured customizations installed: 484` (470 + 14) |
| Test `DespiseRevampedVerification` (4 facts) | 47 spawners generated from the table, every one full to capacity, every spawn a `DespiseCreature` from the right roster with a power in the spawner's range, lower level ≥ 4; the controller finds 15 + 15 army spawners inside the dynamic lower region **with a competing static "Despise" region registered first**; travel rules; ankh → orb → possess → release; overlord immune to players; a possessed creature is not auto-stabled and a stock pet is |
| Headless run 1, fresh save, real map, `[SetupDespise` fired by a throwaway probe 3 s after start | `Despise setup complete`; controller placed, `good=15 evil=15`; four regions registered and `Region.Find` returns each by name; **47 spawners running, 227 spawned, 227 in their rectangles, z 5–70, 3 at the spawner's own tile (the 20-attempt fallback)**; upper levels n=77 power 1–5, lower n=150 power 4–8; 2 ankhs, 6 gates, 48 gate teleporters, 56 entities tagged `despise`; `Saving world done`, `Writing world save snapshot done`, `Shutting down`; 0 errors |
| Headless run 2, reload run 1's save | `Loading world done (802 items, 318 mobiles)`; "controller present from save"; **every count identical to run 1** (15/15, 47/227, 150/43/34 mobiles per region, 2/6/48); save, shutdown, 0 errors. The +1 mobile over 90 + 227 is the ClusterF seeder, as in CC2/CC3/CC9 |
| Headless run 3, the final image (probe removed), fresh save | `Loading world done (617 items, 90 mobiles)`, listeners, save, shutdown, 0 errors |
| The red proof | `CanAutoStable => false` removed from `DespiseCreature`: **47 passed, 1 failed** — "the possessed Despise creature must not be stabled (ServUO CanAutoStable)". Restored; green |

Warnings in every headless log, all three pre-existing and unrelated: `Command stats already registered`
(a customization), and the two `AccountPrompt` lines a fresh save always prints.

Logs: `build-A..E.log`, `build-RED.log`, `build-FINAL.log`, `run1-priority50.log`, `run1.log`, `run2.log`,
`run3.log` in the task's scratch folder.

---

## 2. What "4 files" turned out to be

Read before anything was written (`AGENTS.md`: pre-flight, read the files). The dependency walk from the
four directory files, with the ServUO line counts:

| ServUO file | Lines | Why it is in the port |
|---|---|---|
| `Services/Revamped Dungeons/DespiseRevamped/Setup.cs` | 107 | the brief's four |
| `.../DespiseController.cs` | 796 | " |
| `.../Region.cs` | 335 | " |
| `.../AI.cs` | 457 | " |
| `Mobiles/Normal/DespiseCreature.cs` | 432 | the base every spawn, the AI and the region are typed against; declares `Alignment` |
| `Mobiles/Normal/DespiseGoodCreatures.cs` | 503 | the eight good spawns the XML names |
| `Mobiles/Normal/DespiseEvilCreatures.cs` | 510 | the eight evil spawns |
| `Mobiles/Bosses/DespiseBosses.cs` | 489 | `DespiseBoss`, the two overlords, the two lieutenant wisps; the controller spawns them |
| `Items/Quest/WispOrb.cs` | 607 | the possession item; controller, region, AI and ankh all use it |
| `Items/Quest/PutridHeart.cs` | 53 | dropped by `Region.OnBeforeDeath` |
| `Items/Functional/DespiseAnkh.cs` | 103 | `Setup` places two |
| `Items/Internal/DespiseTeleporter.cs` | 346 | `DespiseTeleporter`, `GateTeleporter` and its inner teleporter; `Setup` places six gates |
| `Misc/WeakEntityCollection.cs` | 235 | `Setup`/`[DeleteDespise` tag and tear down everything placed |
| **13 files** | **4,973** | |
| `RevampedSpawns/DespiseRevamped.xml` | 1,975 | the 47 XmlSpawner definitions; without them nothing spawns |

Read and **not** ported: `Mobiles/NPCs/MysteriousWisp.cs` (635) and `Services/PointsSystems/DespiseCrystals.cs`
(51) — §7, D-29/D-30. Also read for a decision: `Services/Town Cryer/Quests/WishesOfTheWispsQuest.cs`
(`WhisperingWithWispsQuest`, hooked from the ankh and the region).

Out, in `server/customizations`, mirroring ServUO's paths as `apply-patches.sh` requires:

| File | Lines | Notes |
|---|---|---|
| `Services/Revamped Dungeons/DespiseRevamped/DespiseController.cs` | 757 | |
| `.../AI.cs` | 491 | the three duplicated bodies shared through `DespiseAIHelper` |
| `.../Region.cs` | 416 | |
| `.../DespiseSpawns.cs` | 186 | **new**: `DespiseSpawner : Spawner` + the 47-row table, generated from the XML by script |
| `.../Setup.cs` | 143 | |
| `Items/Quest/WispOrb.cs` | 605 | |
| `Mobiles/Normal/DespiseCreature.cs` | 458 | |
| `Mobiles/Bosses/DespiseBosses.cs` | 440 | |
| `Items/Internal/DespiseTeleporter.cs` | 312 | inner teleporter lifted to top level as `GateInternalTeleporter` |
| `Mobiles/Normal/DespiseGoodCreatures.cs` | 298 | |
| `Mobiles/Normal/DespiseEvilCreatures.cs` | 293 | |
| `Misc/WeakEntityCollection.cs` | 192 | a `GenericPersistence` subclass, same save layout as ServUO's |
| `Items/Functional/DespiseAnkh.cs` | 76 | |
| `Items/Quest/PutridHeart.cs` | 26 | |
| **14 files** | **4,684** | plus `server/tests/.../DespiseRevampedVerification.cs` 331 and `server/patches/BaseCreature-PlayerMobile-can-auto-stable.patch` 28 |

Every `new X(`, every base class and every overridden member was checked against `D:\UO\ModernUO-pinned`
before the first build; the 37 new type names were collision-checked against the pinned tree and ours
(all absent). The `Alignment` enum was **not** redeclared: CC9 batch 5 put it in `EpiphanyHelper.cs`
(namespace `Server.Mobiles`, same three values) and said this port should take it from there.

**The multiplier for the row.** The directory count understated Despise by 3.25× in files and 2.9× in lines
before the XML. S9 saw this shape (its "co-port 140" bucket) without pricing it per dungeon; §10 does.

---

## 3. What a region costs to bring across

**ServUO's region definitions map onto ModernUO's almost member for member. The cost is not the mapping;
it is one trap that the test host cannot see.**

Despise's regions are **dynamic**: `DespiseController.BeginTimer` constructs four `DespiseRegion : BaseRegion`
objects with `Rectangle2D[]` bounds and calls `Register()`; nothing comes from `regions.json`. ModernUO has
the same `BaseRegion(string, Map, int priority, params ReadOnlySpan<Rectangle2D>)` constructor, `Register()`
and `Unregister()`, and every virtual the file overrides except one:

| ServUO `DespiseRegion` override | ModernUO | Cost |
|---|---|---|
| `OnDeath(Mobile)`, `OnBeforeDeath(Mobile)`, `OnDoubleClick(Mobile, object)`, `OnEnter(Mobile)`, `OnLocationChanged(Mobile, Point3D)`, `AllowHousing`, `AlterLightLevel` | same names, same signatures (`Region.cs:748-876`) | none |
| `CheckTravel(Mobile, Point3D, TravelCheckType)` on `Region` | `BaseRegion.CheckTravel(Mobile, Point3D, TravelCheckType, out TextDefinition)` (`BaseRegion.cs:171`); `SpellHelper.CheckTravel` consults destination **and** current region (`SpellHelper.cs:669-679`), as RunUO does | one signature, five minutes |
| `GetEnumeratedMobiles()/Items()`, `GetPlayers()` | `GetMobiles()/GetItems()` return `List<T>`, `GetPlayers()` unchanged, `GetPlayerCount()` unchanged | rename |
| `EventSink.OnEnterRegion` (used by the controller to dissolve the orb when its owner leaves any Despise region) | **absent** | `DespiseRegion.OnExit(m)` → `DespiseController.OnLeaveDespise(m)`, which does the same test (`Region.Find(m.Location, m.Map).IsPartOf<DespiseRegion>()`) after the mobile has moved. `OnExit` also fires on logout internalisation (Mobile.cs:2435), which is when ServUO's handler fired too |
| `Region.IsPartOf(Type)` | `IsPartOf<T>()` | rename |
| `Timer.DelayCall(..., TimerStateCallback, state)` | `DelayCall<T>(delay, Action<T>, state)` or a lambda | mechanical |

**The trap: priority.** ServUO passes `Region.DefaultPriority` (50), the same value as the static "Despise"
`DungeonRegion` these four sit inside, and wins the tie because RunUO's `Sector` sorts dynamic regions
ahead of static ones. Pinned ModernUO has the same "dynamic regions go first" arm in `Region.CompareTo`
(`Region.cs:238-247`) **but constructs every region, `regions.json` ones included, through the constructor
chain that sets `Dynamic = true`** (`Region.cs:143-165`; `Dynamic` is get-only), so the arm never fires,
equal priority falls through to `reg.ChildLevel - ChildLevel` (0), and `List.Sort` leaves the order
unspecified. In practice the static dungeon won: headless run 1 at priority 50 printed
`Find(5400,800)=Despise Find(5400,560)=Despise ...` for every probe point and `good=0 evil=0` — the
controller's `CreateSpawners` walks `_lowerRegion.GetItems()`, which tests `Find(item.Location).IsPartOf(this)`,
so it found none of its 30 army spawners, and every creature's `Region` was the static one
(`mobiles=0` in all four). **The test host had passed the same code, because it loads no `regions.json`.**

Fix: `DespiseRegion.DespisePriority = DefaultPriority + 1` (51). Same outcome ServUO gets from its sort;
recorded as a paper-only difference (§8). The test now registers a `DungeonRegion("Despise", Trammel, 50,
5377-5631 × 516-1022)` first, asserts `Find` returns it, then asserts ours win after the controller exists
and it comes back when the controller is disabled or deleted. The probe caught it; the test pins it.

**Rule for the rest of the row:** every runtime region that overlaps a `regions.json` region needs a
priority above 50, and only a run against the real image proves it. Eight region subclasses are in the row
(Blackthorn `BlackthornDungeon : DungeonRegion`, `BlackthornCastle : GuardedRegion`; Covetous
`VoidPoolRegion : BaseRegion`; Exodus `ExodusChestRegion : BaseRegion`, `VerLorRegCity : DungeonRegion`;
Wrong `WrongLevel3`, `WrongJail : DungeonRegion`; Despise done). All three bases exist in ModernUO with the
same names.

**Cost, measured:** `Region.cs` 335 lines in, 416 out (30 of them the comment above); about 40 minutes of
the pre-flight went to the region layer, and the trap cost one extra build and one headless run, roughly
five minutes, once the probe existed. Without the probe it ships silently.

---

## 4. Do the spawns actually generate

### 4.1 XmlSpawner → ModernUO `Spawner`, field by field

ModernUO has no XmlSpawner and no `[XmlLoad`. The XML was parsed by script (47 `<Points>` rows) and carried
as data in `DespiseSpawns.Definitions`; the mapping is in the file header and is:

| XmlSpawner | ModernUO | |
|---|---|---|
| `<Name>` | `Name` | the controller finds "DespiseRevamped Good #n" / "Evil #n" by name, exactly as ServUO's does |
| `<CentreX/Y/Z>` | `Location` | |
| `<X> <Y> <Width> <Height>` | `SpawnBounds` at full Z (-128, depth 256), as ModernUO's own legacy import does (`BaseSpawner.cs:323-341`) | |
| `<Range>5` | `WalkingRange = 5` → `RangeHome` on the creature | |
| `<IsHomeRangeRelative>True` | `SpawnLocationIsHome = true` | |
| `<MaxCount>`, `<MinDelay>/<MaxDelay>` (minutes) | `Count`, `MinDelay`/`MaxDelay` | |
| `Type,{RND,a,b}:MX=n` | one `SpawnerEntry` per type, probability 100, `maxCount = n` | **`{RND,a,b}` has no counterpart**: entries take fixed `Parameters` only (`BaseSpawner.cs:1151-1179`). The roll is `PowerMin/PowerMax` on the new `DespiseSpawner : Spawner`, and `DespiseCreature.OnAfterSpawn` applies it — identical to constructing with the argument, because ServUO's own constructor is `Power = powerLevel` after `_power = 1` |
| `<SmartSpawning>True` | none | D-34 |
| `DoReset = true` | `Reset()` | both stop the spawner and remove its spawns (`XmlSpawner2.cs` `Reset()`, `BaseSpawner.cs:490`) |
| `DoRespawn = true` | `Running = true; Respawn()` | `XmlSpawner.Respawn` calls `Start()` itself; ModernUO's does not, and after a `Reset()` the timer would stay off |
| `[XmlLoad` then `[SetupDespise` | `[SetupDespise` generates the 47 when none exist, then creates the controller | same objects, one command (§8) |

`Spawner.Respawn()` fills a spawner immediately, which is also what `[GenerateSpawners` does for ModernUO's
own files (`ImportSpawnersCommand.cs:168-177`), so a fresh setup is populated at once.

### 4.2 What generated

Test host (no map files: `TileMatrix` warns and serves an empty land block, `TileData` is skipped under
xUnit, so `CanSpawnMobile` sees passable land at z 0): 47 spawners, 227 spawns, every spawner full to its
capacity, every spawn inside its rectangle. Real map (headless runs 1 and 2): the same 47/227, **all 227
inside their rectangles at z 5–70**, 3 of them at the spawner's own tile — `GetSpawnPosition`'s fallback after
20 failed random attempts (`BaseSpawner.cs:549-640`), which XmlSpawner also has. By type, run 1:
BirlingBlades 13, Darkmane 20, Dendrite 13, DespiseUnicorn 17, DivineGuardian 12, Echidnite 10, Fairy 10,
ForestNymph 15, Hellion 15, Naba 14, Phantom 15, Prometheoid 15, Sagittarri 8, Silenii 19, Skeletrex 16,
Ursadane 15 — all sixteen roster types appear.

### 4.3 The two-argument entries (Q-044)

The 17 upper-level rows read `Silenii,{RND,1,5}`. The 30 lower-level rows read
`Phantom,{RND,4,8},{RND,1,5}` — **two** constructor arguments. XmlSpawner matches a constructor by argument
count (`XmlSpawner2.cs:11283-11340`, fed by `BaseXmlSpawner.ParseObjectArgs` at `:7473`, on the main spawn
path at `XmlSpawner2.cs:9268-9276`), and every Despise creature has only `()` and `(int)`. Read literally,
`CreateObject` returns null and the spawner logs "invalid type specification": **on pub57 as shipped the
battlefield spawns nothing.** The version-3 fixer that appends `,{RND,1,5}` only touches spawners in the
Good/Evil regions, and these stand at y 782–973, in the lower level, so the XML shipped this way.

This is a reading, not a run; this machine cannot build ServUO. The port rolls **4–8** in the lower level
(the first, original argument; `WispOrb.MinPowerToConscript` is 4 and the orb refuses power > 5, so
conscripts of 4–5 fighting an army of 4–8 is the evident design) and 1–5 above. D-35. Two numbers in the
table reverse it.

### 4.4 229 requested, 227 possible

`Respawn()` spawns `Count` times, but each entry is capped at its own `maxCount`, and two rows ask for 9 with
eight entries capped at 1. XmlSpawner has the same per-entry `MX` cap, so 227 is the ServUO figure too. The
first test run asserted 229 and failed; the assertion now derives capacity from the data and asserts both
numbers.

---

## 5. ReforgedSuffix

**Zero hits in the Despise cluster.** Grepped all 13 ported files plus `MysteriousWisp.cs` and
`DespiseCrystals.cs`: the only occurrence is `MysteriousWisp.cs:263`, `RunicReforging.GenerateRandomItem(...,
ReforgedPrefix.None, ReforgedSuffix.None)` — a real use, in the declined vendor, not a cosmetic line. Nothing
to decide here and nothing built. Across the row, **all 138 hits are in `BlackthornDungeon/`** (§10 table);
the other four dungeons have none. The naming-carrier decision is a Blackthorn decision and only that.

---

## 6. How the four files were converted

Beyond the recipe's mechanical transformation (`[SerializationGenerator(0, false)]` partials, `[Constructible]`
with the collapsed `(int powerLevel = 1)`, `DefaultName`, `GetWeaponAbility()` for `SetWeaponAbility`, range
perception 10 and speed arguments dropped):

- **Serialized properties with side-effect setters.** `[SerializableProperty(n)]` on a hand-written property
  makes the generator declare the backing field itself (`_pet`, `_anchor`, ...); declaring it too is a
  CS0102 collision (build A, eight errors). Where the setter has real side effects that must not run on
  load — `Power` and `Progress` (a level-up), `Enabled` (`BeginTimer`) — the storage is a
  `[SerializableField(n, getter: "private", setter: "private")]` field with the ServUO property written
  beside it (`LeverPuzzleController.cs:105` is the pinned precedent for the accessibility arguments).
- **`IEntity` and `List<GateInternalTeleporter>` fields** serialize through the generator with no hand-written
  tags (`EffectController.cs:39`, `ChampionSpawn.cs:75`).
- **`Delete()` overrides** became `OnDelete()` (WispOrb: list removal and pet unlink before the item goes) or
  `OnAfterDelete()` (boss kills its wisp; gate deletes its eight teleporters; controller unregisters its
  regions and clears `Instance`).
- **ServUO's `Deserialize` tail** (`Instance = this`, spawner lists, `BeginTimer`, sequence recovery,
  `Timer.DelayCall(EndSequence)`) is `[AfterDeserialization]`. The version < 2/4/5 upgrade paths and the
  version-0 `PointsSystem.DespiseCrystals.ConvertFromOldSystem` conversion are for saves that never
  existed here and were dropped, as was the `CheckSpawnersVersion3` command and its hook (it renamed two
  misspelled creature types in saved spawner entries and re-created the six gates it had just placed; the
  corrected spellings are what the table carries).
- **`EventSink.Login`** → `[OnEvent(nameof(PlayerMobile.PlayerLoginEvent))]` on a static method, the
  `LightCycle.cs:61` shape. `EventSink.OnEnterRegion` → §3.
- **`FightMode.Good` does not exist in ModernUO** and `FightMode.Evil` means something stricter. On pub57 the
  target-acquisition loop applies **no** karma filter for either mode — a candidate passes if `IsHostile`
  (Combatant relation, `BaseAI.cs:2968`) or `IsEnemy` (`BaseAI.cs:2932-2946`) — and `DespiseCreature.IsEnemy`
  is where the karma test lives (players with karma ≤ 1000 for good creatures, ≥ 1000 for evil ones,
  opposite-alignment Despise creatures). ModernUO's `Evil` mode **does** filter non-hostiles to karma < 0
  (`BaseAI.cs:868-876`), which would drop the good creatures' 0..1000 targets. Both map to `Closest`, which
  ranks by distance exactly as both modes do on both emulators (`GetFightModeRanking`'s default arm);
  `IsEnemy` is ported verbatim and does the work. `OnKarmaChange`'s Evil/Good/Aggressor swap became
  `AlignedFightMode`.
- **`WalkMobileRange(IPoint3D, ...)`**, which the possession AI needs for an Item anchor, was dropped by
  ModernUO (`AIMovement.cs:375` keeps only the `Mobile` form). Reproduced as `DespiseAIHelper.WalkToPoint`
  on `DoMove`/`GetDirectionTo`; the "move away" arm RunUO carried is unreachable from these callers and is
  not reproduced.
- **`Damage(int, Mobile, bool, bool)`** returns `void` here (`Mobile.cs:5900`); the boss's "return 0 unless a
  DespiseCreature hit me" is simply not calling base. Tested.
- **Context menu entries** take `(from, target)` in `OnClick` and use `Enabled` instead of `CMEFlags.Disabled`.
- **`NoLootOnDeath` and `GivesFameAndKarmaAward`** have no ModernUO members; `NoKillAwards = true` gates fame,
  karma and looting rights in `BaseCreature.OnDeath` (`:3287`) and `GenerateLoot` (`:3000`), which is what
  the two did on ServUO for a creature with no loot table. Paper-only (§8).
- **`Movement.Offset`** from inside `namespace Server.Items` resolves `Movement` to the namespace; fully
  qualified (build B).

---

## 7. Deviations — note-local numbering, for `docs/fidelity-principle.md`

Q-043's answer made D-numbers note-local. These are D-29 onward within this note.

| # | Deviation | Player notices | Reverses when |
|---|---|---|---|
| **D-29** | `PutridHeart` is inert: ServUO's `OnDoubleClick` awards `Amount` Despise crystal points and deletes the stack | Hearts pile up and cannot be redeemed | `Services/PointsSystems` (S7, gap register B7): one method, ~10 lines |
| **D-30** | `MysteriousWisp` not placed at (1303, 1088, 0), and the two `WhisperingWithWispsQuest`/`TownCryerSystem` hooks dropped (`DespiseAnkh.OnComponentUsed`, `DespiseRegion.OnDeath`), with the ankh's `OnMovement` hint | No vendor to spend crystal points with, no quest, no title deed | S7 for the vendor's prices; the Town Cryer quest system for the quest; `RunicReforging.GenerateRandomItem` (3,391 lines) for the vendor's stock. The wisp is 635 lines and needs all three |
| **D-31** | ServUO's `Container.DropToWorld` calls `WispOrb.CheckDrop` so an orb inside a dropped bag vanishes (`Container.cs:254`) | An orb inside a bag survives the bag being dropped; the orb itself still vanishes when dropped or put in another's container | a one-line hook in `Container.DropToWorld` (a patch) |
| **D-32** | `Silenii` and `Phantom` lose `SetMagicalAbility(MagicalAbility.Discordance)` and the `GetBardTarget`/`CanDoTarget` pair that served it | Neither creature discords its enemies | Pet Training's MagicalAbility group (B3, WAIT). The Saurosaurus precedent |
| **D-33** | `ForceNotoriety => true` absent: ServUO computes a possessed creature's notoriety from itself (`Notoriety.cs:188`, `:371`); ModernUO uses the master's | A possessed creature's name shows in its possessor's colour rather than its own karma colour | a `ForceNotoriety` virtual and two guards in `Notoriety.cs` (a patch) |
| **D-34** | `<SmartSpawning>True` has no counterpart: XmlSpawner idles a spawner while no player is near | The dungeon is populated whether or not anyone is in it; creatures are already wandering on arrival | nothing to build; note only |
| **D-35** | Lower level rolls power 4–8 where ServUO's XML, read literally, constructs nothing (§4.3, Q-044) | On pub57 the battlefield is empty; here it has the army the design implies | two numbers in `DespiseSpawns.Definitions` |
| D-1, D-2 | row-wide (`IsArtifact`, set slayers) — not present in this cluster | | |

---

## 8. Paper-only differences, not deviations

- **Region priority 51** instead of 50 (§3). Same `Region.Find` outcome as ServUO's sort.
- **`FightMode.Closest`** for both alignments (§6). Same target set on pub57, distance ranking on both.
  One nuance: ModernUO's acquisition requires `IsEnemy` even for a hostile (`BaseAI.cs:857`), ServUO
  accepts a hostile without it; a low-karma player attacking an evil Despise creature is still fought,
  because being hit sets `Combatant` on both emulators. Not observed to differ.
- **`NoKillAwards = true`** for `NoLootOnDeath = true` + `GivesFameAndKarmaAward => false` (§6). The
  creature has no loot table on either side; the region refuses to open its corpse on both.
- **One setup command.** `[SetupDespise` generates the spawners when none exist; ServUO needs `[XmlLoad`
  first. Same 47 objects, same names. `[DeleteDespise` reports what it removed.
- **`[DeleteDespise` unregisters the regions.** ServUO's controller has no delete hook, so its regions
  outlive it until restart. GM tooling, not OSI behaviour.
- **`CheckSpawnersVersion3`, `[TypeAlias]` on `Sagittarri`/`BirlingBlades`, the version-0/2/4/5 upgrade
  paths** dropped: save-upgrade code for saves that never existed here.
- **`DateTime.UtcNow` → `Core.Now`**, the ModernUO convention; equal on a running server.
- **Music.** The dynamic regions have no parent, so `Music` is `Invalid` on both emulators; entering one from
  the static dungeon sends the same stop-music packet ServUO sends.
- **Fresh worlds have no teleporters to convert.** `Setup` converts stock teleporters within 2 tiles of
  (5588, 631, 30) into `DespiseTeleporter`s; a `[TelGen`-less world has none (run 1: `despiseTeleporters=0`).
  The live world's state is unknown from here (never read `Saves/`).

---

## 9. The two upstream changes

### 9.1 `BaseCreature-PlayerMobile-can-auto-stable.patch` — the port's one patch, argued before writing

ServUO's `BaseCreature.CanAutoStable => true` is overridden `false` on `DespiseCreature`; `PlayerMobile.
AutoStablePets` skips such pets. ModernUO has neither (`PlayerMobile.cs:3610-3665` stables every controlled,
non-summoned, non-mount, non-escort pet; `CheckPets` and the logout path both call it). A possessed
Despise creature — `Controlled`, `ControlMaster` set — would be stabled on its master's logout, and the
orb's own cleanup runs later (the mobile is internalised after the logout delay, `OnExit` fires, the orb
deletes and unlinks a creature that is by then in the stable).

Alternatives, rejected:

1. **Release on `EventSink.Logout`.** Racy — `PlayerMobile` subscribes the same event and the order is
   assembly load order — and a deviation: ServUO keeps the possession across a logout.
2. **Delete the orb synchronously on logout.** Same deviation, and `OnExit` fires after `AutoStablePets` has
   already run on the logout path.
3. **Do nothing.** A `Commandable => false`, `IsBondable => false` creature in a player's stable, claimable.
   Worse than either.
4. **The patch.** `public virtual bool CanAutoStable => true;` beside `IsBondable` in `BaseCreature.cs` and
   one `if (!pet.CanAutoStable) continue;` in `AutoStablePets`. +10/-0 across two `UOContent` files, no
   core-project change, no serialization change. The S2 luck-patch shape.

Pinned by `APossessedDespiseCreatureIsNotAutoStabledOnLogoutButAStockPetIs` (a `GreyWolf` **is** stabled in the
same call, so the guard is proved narrow), and **proved red**: override removed, build `sl-modernuo:cc4red`
failed on exactly that assertion with 47 passing; override restored, green. PlayerMobile.cs now carries
three of our patches (`upstream_patches` in `progress-state.json` updated).

### 9.2 `CraftGumpItem-MakeX.patch` — HEAD did not compile (Q-045)

Not mine and not in scope, but the gate could not run around it. `e1e3c36` (Chase, 10:40 today, "Fix the
invisible MAKE X label, confirmed in a client") changed two lines of the patch from `builder.AddLabel(175,
390, hue, "MAKE X")` to `builder.AddHtml(175, 390, 150, 18, "<BASEFONT COLOR=#787878>MAKE X", false, false)`.
`DynamicGumpBuilder.AddHtml` at the pinned commit is `(x, y, w, h, ReadOnlySpan<char> text, ReadOnlySpan<char>
color = default, int size = -1, byte fontStyle = 0, TextAlignment align = Left, bool background = false, bool
scrollbar = false)` (`DynamicGumpBuilder.cs:80-84`); the two `false`s land on `color` and `size`, CS1503 ×4,
builder stage fails. The newest image in the local registry (`sl-modernuo:latest`, 4 days old) still has the
`AddLabel` lines, so whatever was confirmed was not built from this tree through `build.sh`.

Fix taken: the two trailing arguments dropped (`background`/`scrollbar` default to false). Same HTML string,
same colours, nothing else in the patch touched, dry-run clean against the pinned tree. `docs/client-check-
backlog.md`'s MAKE X pass predates this and should be re-run once; `progress-state.json` still describes
that patch as "Label still renders invisible (known)", which is now doubly stale. Flagged in the shard
commit and as Q-045.

---

## 10. The row, re-costed from what Despise taught

**S9's 255 is a filter count. Despise says the directory count of a dungeon understates its port by about
3× in files and lines, before its spawn XML.** The other five, profiled by grep for the dependencies
Despise exposed (candidates, not results — every one of these is a file that mentions the token, and S9's
rule that a keyword hit is an upper bound still stands):

| Dungeon | Dir files | Dir lines | Spawn XML lines | XmlSpawner | PointsSystem | ReforgedSuffix | WeakEntity | Region subclasses | Quest engine | Pet Training | IsArtifact |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Despise (done) | 4 → **13** | 1,695 → **4,973** | 1,975 | 1 | 1 | 0 | 2 | 1 file, 1 class | 0 (2 hooks) | 0 | 0 |
| Shame Revamped | 11 | 3,390 | **8,159** | 1 | 2 | 0 | 2 | 0 | 0 | 2 | 0 |
| WrongDungeon | 26 | 2,874 | 1,597 | 1 | 0 | 0 | 0 | 1 file, 2 classes | 1 | 1 | 1 |
| Covetous Void Spawn | 29 | 6,383 | none | 2 | 2 | 0 | 1 | 1 | 2 | 2 | 5 |
| TheExodusEncounter | 38 | 4,747 | none | 0 | 0 | 0 | 0 | 2 | 0 | 1 | 9 |
| BlackthornDungeon | 147 | 9,484 | 2,272 (two files) | 1 | 3 | **138** | 0 | 1 | 0 | 1 | 138 |

What each column now costs, from this task:

- **WeakEntityCollection: paid.** Ported once (192 lines), frees Shame ×2 and Covetous ×1.
- **XmlSpawner: a pattern, not a subsystem.** `DespiseSpawner` + a generated table. The generator script is
  40 lines of Python against the XML; Shame's 8,159-line XML is the one to budget for (it is 4× Despise's).
  Covetous and Exodus have no XML: their `XmlSpawner` hits are controllers that spawn directly.
- **Regions: a pattern plus one rule** (priority > 50 over a `regions.json` region; prove it on the real image).
  Seven more subclasses, all on bases ModernUO has.
- **PointsSystem: 8 files in the row** (Shame 2, Covetous 2, Blackthorn 3, Despise 1). Each is a D-29-shaped
  inert deviation until S7 lands. That is the eighth and ninth argument for S7 (B7, "unblocks 55") before
  Shame or Covetous, or a decision to carry the deviation.
- **ReforgedSuffix: 138, all Blackthorn.** Confirmed against the row; the decision is Blackthorn's alone.
- **IsArtifact: 138 Blackthorn + 15 elsewhere.** Worth zero (S9 §4); delete the line.
- **Pet Training: 7 files.** Saurosaurus precedent, one line each, log each.
- **Quest engine: Wrong 1, Covetous 2.** Read each; Town Cryer hooks drop (D-30 shape), ML quests may translate (S5).
- **The 3× multiplier** is the number to apply to each dungeon's directory count before believing it, and
  the co-port files live outside the row (S9's "elsewhere 140").

**Recommended order, changed from `docs/tasks.md`'s Shame → Wrong → Covetous → Exodus → Blackthorn:**
**Wrong first** (26 files, 2,874 lines, a 1,597-line XML, no PointsSystem, no ReforgedSuffix, two regions
on `DungeonRegion`), **then Exodus** (38 files, no XML, no XmlSpawner, no PointsSystem; two regions; the 9
`IsArtifact` are free; the unknown is whether the encounter rests on Exodus-boss mechanics ModernUO lacks —
read before committing), **then Shame** (11 files hide an 8,159-line spawn XML, two PointsSystem hits and two
Pet Training hits), **then Covetous** (6,383 lines, two direct-spawning controllers, two PointsSystem, two
quest hooks), **Blackthorn last**, after the ReforgedSuffix decision. Shame moved down because its directory
count is the smallest and its true cost is not.

---

## 11. What it cost

| Phase | Measure |
|---|---|
| Reading and pre-flight: `AGENTS.md`, `docs/tasks.md`, S9's CC4 row, the 15 ServUO files and the XML, ModernUO's region/spawner/AI/teleporter/persistence/context-menu/serializer code, every signature the cluster calls, 37 collision checks | the bulk of the task; not separately timed |
| Writing 14 files + test + patch | ~15 minutes |
| Builds | A 27 s (8 generator field collisions), B 31 s (1 mine, 4 from HEAD's MAKE X patch), C 136 s (test asserted 229, data holds 227), **D 133 s green**, E 94 s green (priority 51, test hardened), RED 90 s (1 failed, as intended), **FINAL 91 s green** |
| Headless runs | 113 s (priority 50, the trap), 113 s (fixed), 87 s (reload), ~85 s (final image) |
| Wall clock | HEAD's commit is 10:40 local and the session started after it; first build 11:36, final image 11:53, notes and commits after. About 1½ hours end to end, the first ~50 minutes reading |
| Context | ~700k tokens at the point of writing this note (15.0M budget → 14.3M); the finished task will be ~760k. Compare CC3's 278k for 17 leaf files: **a hub-and-spokes dungeon costs 2–3× a leaf batch of similar line count**, and the difference is reading, not writing |

**Not verified, per the standing rule, and batched for the client spot check:** appearance of the sixteen
creatures and two overlords (bodies, hues, sounds), the ankh graphics and the gate graphic, the possession UI
(double-click, targeting, the two context entries, the hue changes), the leash and aggression behaviour in
motion, a boss sequence end to end (Call to Arms → transport → overlord → cleanup, 90 minutes of timers),
`DespiseTeleporter` conversion on a world that has teleporters, recall/gate refusal at a real spellbook, and
`[DeleteDespise` on a world with players inside.
