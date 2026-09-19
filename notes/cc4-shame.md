# CC4 Shame — the second Revamped Dungeons port

2026-09-19. One dungeon, complete: Shame Revamped, on Trammel and Felucca. Built through `build.sh`, 54 tests green
(48 + 6 new, one proved red on purpose), and the spawns generate on the real map: 194 spawners, 384 spawns (268
creatures, 116 locked chests), save and reload identical. No upstream patch. Nothing here has been seen in a client.

The brief asked three things beyond the port; they are answered in §3 (regions: Shame needs none, and the Despise
trap does not arise), §4 (XmlSpawner argument shapes: none in this file) and §5 (ReforgedSuffix: zero). Deviations
are §7, paper-only differences §8, the two ServUO readings that deserve a question §9, the row re-costed §10, cost §11.

**Counts that moved while doing this, so nobody plans from the old ones:**

- **"Shame's 11 files" is 19 ServUO `.cs` files plus an 8,159-line XmlSpawner XML.** The eleven in the directory
  (3,390 lines) are the whole dungeon *except* what its spawn file names: **116 of the XML's 194 rows spawn
  `TreasureLevel1-4`**, which are Nerun's Treasure Chest Pack in `Items/Containers/` and not in ModernUO, and the
  cave troll's four pack items and the vortex's Void Core live under High Seas and `Items/Resource`. 4,137 lines of
  C# in, 3,772 out in 20 files (§2). Counted, not summed in my head.
- **The XML asks for 386 and can hold 384** (§4.3). 97 rows per facet and the two facets are the same multiset.
- **Despise's §10 profile said "Pet Training 2" for Shame. It is 12 lines across 8 creatures** (§7): the profile
  counted files, and the tokens to count are `SetSpecialAbility|SetAreaEffect|SetWeaponAbility|IAuraCreature`.
- **Two ServUO behaviours were read that look like bugs** (§9): the wall teleporters are inert until the first troll
  dies and active from then on, and an altar whose challenge times out answers "already summoned" until restart.
  One is reproduced, the other fixed with one line and logged (D-43). Both are readings, not runs.

---

## 1. The headline, and what "done" was measured against

`docs/tasks.md`: *"Done when: each dungeon builds and its spawns generate."* Both halves measured, the second on the
real map and not only in the test host:

| Gate | Result |
|---|---|
| `build.sh` (patches, tests, image) | green, `sl-modernuo:cc4shame`; 16 patches applied, **54 tests passed**, `structured customizations installed: 503` — 483 at HEAD plus the 20 files in §2 (Despise's note wrote 484 for HEAD; `find server/customizations -mindepth 2 -name '*.cs'` says 503 now and 483 without these, so 484 was off by one) |
| Test `ShameRevampedVerification` (6 facts) | 194 spawners from the table on two facets, every one full to capacity (384), every spawn the right type inside its rectangle on the right facet, chests locked with loot and a magic trap, creatures homed per the XML's `IsHomeRangeRelative`; `Generate` stops a stock spawner in the dungeon and deletes a stock teleporter on an altar tile, places 6 altars / 6 walls / 6 trolls / 22 wall teleporters, is idempotent, and `DeleteShame` removes all of it and restarts the stock spawner; the altar summons only with points (or cost 0), the guardian takes damage only from its summoner and their pets until the last ten minutes, drops 3-5 crystals, the altar cools down ten minutes, a timed-out challenge frees it; the wall sinks 50 z when its troll dies and comes back with a new troll two minutes later; the three drops make the whetstone and the whetstone strips Damage Increase from an exceptional weapon only; ClayGolem carries no golem parts, CaveTroll carries its four powder ingredients, the aura/breath/drain mappings are in place; the mages' mana taint drains 30-40 on its 1.5 s tick and ends when the mage dies |
| Headless run 1, fresh save, real map, `Generate()` fired by a throwaway probe 3 s after start | `Shame Revamped setup!`; **per facet: 97 spawners running, 192 spawned, 192 inside their rectangles, 192 inside the `Shame` region**, z -30..44 (Trammel) / -23..44 (Felucca), 15 / 14 at the spawner's own tile (the 20-attempt fallback), 58 chests all locked holding 653 / 709 items, 3 altars (cost 10/20/30), 3 walls (4/4/3 pieces) each with its troll, 11 wall teleporters; `Region.Find` returns `Shame` at three probe points on both facets; 228 entities tagged `newshame` (194 + 6 + 6 + 22); world 3,499 items / 364 mobiles (90 + 268 + 6); `Saving world done`, snapshot written, `Shutting down`; no line matching warn/error/exception |
| Headless run 2, reload run 1's save | `Loading world done (3511 items, 365 mobiles)`: run 1's count plus the 6 altar teleporters (placed a second after the probe counted), the ClusterF seeder's mobile and its items, as in CC2/CC3/CC9/Despise; "altars present from save: 6"; **every probe count identical to run 1**, and every altar now reports its teleporter at its `TeleporterLocation` (3 per facet); save, shutdown, clean |
| Headless run 3, the final image (probe removed), fresh save | `Loading world done (618 items, 90 mobiles)`, listeners on 127.0.0.1, `Saving world done`, snapshot written, `Shutting down`; zero lines matching warn/error/exception |
| The red proof | `ClayGolem() : base(true)` changed to `base(false)`: **52 passed, 2 failed** — the golem assertion (`clay golem pack: Gold, IronIngot, ExecutionersCap`) as intended, and the mana-taint fact, which turned out to be racing mana regeneration in the test host and was hardened into a poll (§6). Restored; FINAL green |

Logs: `cc4shame-build-A..F.log`, `-RED.log`, `-FINAL.log`, `run1.log`, `run2.log`, `run3.log` under the session temp
folder (`%LOCALAPPDATA%\Temp\cc4shame\`), with the probe's `run.sh` and the scratch `Configuration` copy (loopback
listing, no ports published, no client, nothing deployed, `Saves/` never read).

---

## 2. What "11 files" turned out to be

Read before anything was written. The dependency walk from the eleven directory files, and from the XML's type list,
with the ServUO line counts:

| ServUO file | Lines | Why it is in the port |
|---|---|---|
| `Services/Revamped Dungeons/Shame Revamped/Generate.cs` | 254 | the brief's eleven: `[GenerateNewShame` / `[DeleteShame` |
| `.../ShameAltar.cs` | 243 | " the Guardian's Altar |
| `.../ShameCrystal.cs` | 50 | " the point currency |
| `.../ShameTeleporter.cs` | 105 | " the altar and wall teleporters |
| `.../ShameWall.cs` | 164 | " the cave-troll walls |
| `.../Items/{CorrosiveAsh,CursedOilstone,QuartzGrit,WhetstoneOfEnervation}.cs` | 67+65+66+83 | " the whetstone recipe |
| `.../Mobiles/Bosses.cs` | 327 | " ShameGuardian and the three level guardians |
| `.../Mobiles/Creatures.cs` | 1,966 | " the 22 creatures |
| `Services/PointsSystems/ShameCrystals.cs` | 51 | the crystal ledger; a `PointsSystem` subclass (S7). Ported as a seam, §7 D-37 |
| `Items/Containers/BaseTreasureChestMod.cs` | 121 | **named by 116 XML rows**: Nerun's Treasure Chest Pack base |
| `Items/Containers/TreasureChestMod.cs` | 351 | `TreasureLevel1-4` (the 292 lines the XML uses; `TreasureLevel1h` and the rest are not referenced and not ported) |
| `Items/Resource/VoidCore.cs` | 44 | UnboundEnergyVortex's 20% drop |
| `Services/Expansions/High Seas/Items/Resources/{SaltPeter,Potash,Charcoal,BlackPowder}.cs` | 45 ×4 | CaveTroll's pack; leaf resources with no cannon reference |
| **19 files** | **4,137** | |
| `RevampedSpawns/ShameRevamped.xml` | 8,159 | the 194 XmlSpawner definitions |

Also read, for a decision: ServUO's `Services/Pet Training/SpecialAbility.cs` and `AreaEffects.cs` (what the six
dropped or mapped abilities do, §7), `Items/Addons/BaseAddon.cs` (§9.1), `Services/XmlSpawner/.../XmlSpawner2.cs`
lines 9000-9030 (the per-entry cap, §4.3), `Server/Poison.cs` (`Poison.Parasitic` is `GetPoison("DeadlyParasitic")`).

Out, in `server/customizations`, mirroring ServUO's paths as `apply-patches.sh` requires:

| File | Lines | Notes |
|---|---|---|
| `Services/Revamped Dungeons/Shame Revamped/Generate.cs` | 265 | |
| `.../ShameSpawns.cs` | 305 | **new**: the 194-row table generated from the XML by script, plain `Spawner`s (no subclass needed: no constructor arguments, §4) |
| `.../ShameAltar.cs` | 265 | |
| `.../ShameWall.cs` | 190 | |
| `.../ShameTeleporter.cs` | 55 | |
| `.../ShameCrystal.cs` | 42 | |
| `.../Items/{CorrosiveAsh,CursedOilstone,QuartzGrit,WhetstoneOfEnervation}.cs` | 50+46+50+79 | |
| `.../Mobiles/Bosses.cs` | 295 | |
| `.../Mobiles/Creatures.cs` | 1,597 | the three mages' identical mana-taint bodies shared through `CorruptedManaTaint`, one instance per class; the two vortices' identical pull through `VortexTeleport` |
| `Services/PointsSystems/ShameCrystals.cs` | 36 | **the S7 seam**, not ServUO's class (§7 D-37) |
| `Items/Containers/BaseTreasureChestMod.cs` | 106 | |
| `Items/Containers/TreasureChestMod.cs` | 275 | `TreasureLevel1-4` only |
| `Items/Resource/VoidCore.cs` | 24 | |
| `Services/Expansions/High Seas/Items/Resources/{SaltPeter,Potash,Charcoal,BlackPowder}.cs` | 23 ×4 | CC5/CC8 will find these present |
| **20 files** | **3,772** | plus `server/tests/.../Shame Revamped/ShameRevampedVerification.cs` 744 (§6) and **no patch** |

Every `new X(`, every base class and every overridden member was checked against `D:\UO\ModernUO-pinned` before the
first build; the 37 new type names were collision-checked against the pinned tree and ours (all absent). Absent
from pinned ModernUO and resolved: `TreasureLevel1-4` (ported), `Saltpeter`/`Potash`/`Charcoal`/`BlackPowder`/
`VoidCore` (ported), `IAuraCreature` + `SetAreaEffect` (ModernUO's `HasAura`), `SetSpecialAbility` (§7),
`AIType.AI_Mystic` (D-41), `TreasureMapChance` (D-42), `TimesImbued` (§8), `PointsSystem` (D-37),
`Map.FindItem<T>` (a range-0 scan), `Container.ConsumeTotal(Type[], int[])` (the `ReadOnlySpan` form),
`ItemQuality` (`WeaponQuality`/`ArmorQuality`), `Mobile.BodyValue` (`Body`), `Poison.Parasitic` (`DeadlyParasitic`,
the same registered poison).

**The multiplier for this row, second data point.** Despise: directory ×3.25 in files. Shame: ×1.7 in files, ×1.2
in lines, because Shame's directory already holds its creatures where Despise's held only the hub. **The
directory count is not the number; the spawn XML's type list is part of the walk.** Profile the XML's `Objects2`
names against pinned ModernUO before costing a dungeon: here that one grep would have shown 116 rows naming a type
ModernUO does not have.

---

## 3. Regions: Shame needs none, and the Despise trap does not arise

Despise's regions were runtime `BaseRegion`s the controller registers, and the trap was that every pinned region
is `Dynamic`, so a runtime region at priority 50 lost the tie to `regions.json`'s static dungeon.

**Shame registers no region.** Nothing in the eleven files constructs one. What the creatures do is test
`Region.Find(c.Location, c.Map).IsPartOf("Shame")` before dropping a crystal, and `Generate.cs` uses
`Region.Find(5538, 170, 5)` on each facet to find the old spawners to reset. Both need only the **static** `Shame`
`DungeonRegion`, which pinned `Distribution/Data/regions.json` has on Trammel and Felucca (priority 50, two rectangles:
5377,2-5634,262 and 5635,2-5895,126, `GoLocation` 5395,126). `Region.IsPartOf(string)` exists (`Region.cs:545`).

So there is no tie to break and the priority rule from Despise §3 has nothing to apply to. Checked on the real image
rather than assumed: the probe printed `Find(5538,170)=Shame Find(5403,43)=Shame Find(5761,98)=Shame` on both facets,
and **all 384 spawns stood inside the `Shame` region** (`inShameRegion=192` per facet), so every creature's crystal
roll is live. The test registers the same two-rectangle `DungeonRegion` on both facets before generating, because the
test host loads no `regions.json`; `ResetOldSpawners` skips a facet whose `Region.Find` returns the map's default
region (there is no old population to reset), which is the one line the test host needed and the live server never
takes.

**Rule for the rest of the row, refined:** the priority rule applies to dungeons that *construct* regions (Wrong,
Covetous, Exodus, Blackthorn per Despise §3's list). A dungeon that only *reads* a region by name needs the name to be
in `regions.json` and nothing else. Grep the cluster for `new .*Region(` before budgeting a region layer.

---

## 4. Do the spawns actually generate

### 4.1 XmlSpawner → ModernUO `Spawner`, field by field

Same mapping as Despise §4.1, with the fields this file uses that Despise's did not (the header of `ShameSpawns.cs`
carries it too):

| XmlSpawner | ModernUO | |
|---|---|---|
| `<Name>` | `Name` | `Shame_Revamped` (78 rows) / `Shame_Chest` (116). `Generate.cs` tells ours from the old ones by these two names, exactly as ServUO's `ResetOldSpawners` does |
| `<Map>` | the facet | 97 Trammel, 97 Felucca, identical multisets; Despise was Trammel-only |
| `<Range>` | `WalkingRange` → `RangeHome` | **per row**, 1 to 35 (chests 1; creatures 3-35). Despise's were all 5 |
| `<IsHomeRangeRelative>` | `SpawnLocationIsHome` | **per row**: True on 52 rows (home = where it spawned), False on 142 (home = the spawner's tile). Same meaning on both emulators (`BaseSpawner.Spawn` sets `Home` from the flag); the test asserts `Home` both ways |
| `<MaxCount>`, `<MinDelay>/<MaxDelay>` (minutes) | `Count`, `MinDelay`/`MaxDelay` | creatures 2/2 min (76 rows) or 5/10 (2); chests 1/2 |
| `Objects2` `type:MX=n[:OBJ=...]` | one entry per type, probability 100, maxCount n | up to three types per row. Names case-corrected (the XML has `greaterWaterelemental`, `EvilMageLord`, `TreasureLevel2`, `mudpie`) |
| `<SmartSpawning>` | none | True on 70 rows, False on 124. D-34's shape from Despise; note only |
| `[XmlLoad` then `[GenerateNewShame` | `[GenerateNewShame` generates the 194 when none exist | same objects, one command (§8) |

`Spawner.Respawn()` fills each spawner at once, as `[GenerateSpawners` does for ModernUO's own files. Items spawn
through the same path as mobiles (`BaseSpawner.cs:1258-1270` sets `item.Spawner` and calls `OnAfterSpawn`;
`GetSpawnPosition` uses `CanSpawnItem` for an item), which is how the chests land and how a chest that deletes itself
after being opened gets replaced by its spawner 1-2 minutes later.

### 4.2 What generated

Test host (no map files, land at z 0): 194 spawners, 384 spawns, every spawner full to capacity, every spawn inside its
rectangle on its facet, 28 types present. Real map (runs 1 and 2): **the same 194/384, all inside their rectangles, at
z -30..44**, 29 at a spawner's own tile (the 20-attempt fallback, as Despise saw 3 of 227; chests on 2×2 rectangles
fall back more often). By type per facet, run 1: ChaosVortex 1, ClayGolem 2, CorruptedMage 4, CrazedMage 1,
DiseasedBloodElemental 5, EternalGazer 2, EvilMageLord 4, FlameElemental 3, GreaterAirElemental 4,
GreaterBloodElemental 5, GreaterEarthElemental 7, GreaterWaterElemental 9, Kraken 5, MoltenEarthElemental 8,
MudElemental 11, MudPie 20, Scorpion 17, SeaSerpent 4, ShameEarthElemental 2, ShameGreaterPoisonElemental 4,
StoneElemental 2, TreasureLevel1 10, TreasureLevel2 24, TreasureLevel3 19, TreasureLevel4 5, UnboundEnergyVortex 3,
VileMage 7, WindElemental 4 — all 28 names the XML uses. The chests came up locked (58 of 58 per facet) with loot in
them (653 and 709 items).

### 4.3 Constructor arguments and the per-entry cap (the Q-044 shape)

**None.** Every `Objects2` entry in this file is a bare type name: zero commas in any entry, zero `{RND`. Despise's
two-argument rows do not occur here, so no `DespiseSpawner`-style subclass and no power roll; plain `Spawner`s carry
the table.

**386 requested, 384 possible.** `Respawn()` spawns `Count` times but each entry is capped at its own `MX`
(XmlSpawner: `XmlSpawner2.cs:9008-9014`, `k + socnt < somax`; ModernUO: `SpawnerEntry.IsFull`). Two rows are short:
the `Shame_Chest` at 5402,58 on each facet asks for 2 over one `TreasureLevel2:MX=1`. Same on both emulators. One row
per facet (5761,98) carries `chaosvortex:MX=0` beside `unboundenergyvortex:MX=2`: an `MX=0` entry spawns nothing on
either emulator (the cap is `< 0`); it is carried in the table so a GM can raise it, and the `ChaosVortex` that does
spawn (one per facet) comes from the two `chaosvortex:MX=1` rows. The test derives capacity from the data and asserts
both numbers.

---

## 5. ReforgedSuffix

**Zero hits in the Shame cluster**, counted across all 19 ServUO files read. The one reforging call in the cluster is
`RunicReforging.GenerateRandomItem(item, 0, min, max)` in `BaseTreasureChestMod.AddLoot` (the chest pack reforges its
weapon/armour/jewellery/clothing drops when `RandomItemGenerator.Enabled`), which is D-38 and not a naming line.
Despise's row-wide reading stands: all 138 are Blackthorn's.

---

## 6. How the files were converted

Beyond the recipe's mechanical transformation (`[SerializationGenerator(0, false)]` partials, `[Constructible]` with
collapsed `(int amount = 1)` constructors, `DefaultName`/`CorpseName`, `GetWeaponAbility()` for `SetWeaponAbility`,
speed and perception arguments dropped, `Core.Now`):

- **Serialized `Type`.** `ShameAltar.GuardianType` is a generator `Type` field (`SmallBOD.cs:20` precedent) rather
  than ServUO's name string round-tripped through `ScriptCompiler.FindTypeByName`. `Map`, `Point3D`, `DateTime`,
  `Mobile`/`Item` subclass references all serialize through the generator with no hand-written tags.
- **`Damage(...)` returns `void`** (`Mobile.cs:5900`); `ShameGuardian`'s "return 0 unless the summoner" is not calling
  base. `Party` inside a `BaseCreature` subclass binds to `Mobile.Party` (an `object`), so the party branch is
  written `Server.Engines.PartySystem.Party.Get(from)` (build A).
- **Timers.** ServUO's `Timer.DelayCall(...)` with `Start()` and the chest's `ChestTimer` with `Priority` are
  `Timer.StartTimer(..., out TimerExecutionToken)` with `Cancel()`; `Timer` has no priority here. The chest's delete
  timer is started once (§8).
- **`OnDamagedBySpell(Mobile from, int damage)`** here; ServUO's is `(Mobile from)`.
- **`AOS.Damage(from, mob, dmg, false, 0, 0, 0, 0, 0, 0, 100)`**: ServUO's 14-argument form with `direct = 100`
  maps onto the pinned overload at `AOS.cs:47-50` (`chaos = 0, direct = 100, keepAlive/archer/deathStrike` default).
- **Pet Training abilities** (§7 for the losses): `SetSpecialAbility(DragonBreath)` is `GetMonsterAbilities() =>
  [MonsterAbilities.FireBreath]`, which carries the same numbers as ServUO's default `DragonBreathDefinition`
  (`SpecialAbility.cs:862-895`: 0.16 of current hits, 100% fire, 30-45 s between breaths, 1.0 s stall, 1.3 s effect
  delay, item 0x36D4, sound 0x227, animation 12; `FireBreath.cs:13-46` line for line). `SetAreaEffect(AuraDamage)` +
  `IAuraCreature.AuraEffect` is `HasAura` + `AuraRange`/`AuraBaseDamage`/`AuraFireDamage`/`AuraEffect`, set to ServUO's
  `fireAura` definition for `FlameElemental` and `LesserFlameElemental` (`AreaEffects.cs:572-575`: 5 s, range 5,
  damage 7, 100% fire). `LifeLeech` is `MonsterAbilities.DrainLifeAttack` (D-40 for the tuning).
- **`ClayGolem : Golem`.** ServUO's `Golem` calls a virtual `SpawnPackItems()` that `ClayGolem` overrides to nothing.
  ModernUO's `Golem` packs the ingots and parts inline inside `if (!summoned)`, and everything else its summoned branch
  changes (hue 2101, fire 50-60, fame/karma 10) `ClayGolem` overwrites afterwards, so `ClayGolem() : base(true)` is an
  exact reproduction with no member lost — verified by dumping the pinned `Golem` constructor, and pinned by the test
  and the red proof. `BaseCreature.GenerateLoot(true)` at construction (`BaseCreature.cs:376`, both emulators) is why
  the pack also holds gold: the test asserts the cap is there and none of the five golem parts are.
- **The three mages' mana taint** and **the two vortices' pull** were literal copies on ServUO (three static tables,
  two `DoTeleport` bodies). They are one helper each; each mage class still owns its own table, so a player tainted by
  a Burning Mage and a Crazed Mage at once is tracked twice, as on ServUO.
- **`ResetOldSpawners`** works on ModernUO `Spawner`s in the facet's `Shame` region instead of `XmlSpawner`s:
  `Reset()` for `DoReset = true`, `Running = true; Respawn()` for `DoRespawn = true` (Despise §4.1's mapping). The
  stock spawn files under pinned `Distribution/Data/Spawns` contain no Shame entries, so on a fresh world there is
  nothing to reset; whether the **live** world has spawners in Shame is unknown from here (`Saves/` never read) and
  the command handles either.
- **The test, six facts, 744 lines.** Two things the test host taught: (1) `Mobile.Kill()` hands `OnDeath` a **null**
  container until `Corpse.Initialize()` has registered `Mobile.CreateCorpseHandler`, which `UOContentFixture` does not
  call — every `OnDeath` here dereferences the corpse as ServUO's do, so the test registers the handler once
  (`EnsureCorpses`) rather than adding null guards the live server never needs; (2) a fresh `PlayerMobile` has 0
  hits, so the first point of damage kills it (`NewPlayer` sets `Hits = HitsMax`). Also: facts share one world in no
  fixed order, so each fact that places Shame objects clears every Shame object first and last (`ClearShame`); the
  mana-taint fact polls the clock in 8 ms steps for its 1.5 s tick because the tick sits in a coarser wheel ring and
  mana regenerates about two points per 100 ms in the test host (the Q-029 shape; the direct damage the same tick
  deals is regenerated before it can be read and is not asserted); `NameList.RandomName("male")` is `""` in the test
  host (no `names.json`), so the mages' names are not asserted.

---

## 7. Deviations — note-local numbering, for `docs/fidelity-principle.md`

Q-043 made D-numbers note-local; Despise used D-29 onward. These are **D-37 onward** within this note.

| # | Deviation | Player notices | Reverses when |
|---|---|---|---|
| **D-37** | **Crystals of Shame are inert and the altars cannot be paid.** `Services/PointsSystems` (S7) is not here; the port calls through a seam (`Services/PointsSystems/ShameCrystals.cs`, `Enabled => false`): `GetPoints` is 0, so every Guardian's Altar answers 1151623 "You are not yet worthy", and a crystal double-clicked is kept rather than consumed for nothing (Despise's D-29 shape) | The level guardians can never be summoned by a player, so `QuartzGrit` (Quartz Elemental only) is unobtainable and with it the Whetstone of Enervation; crystals pile up. A GM can `[props` an altar's `SummonCost` to 0 to run a fight | S7: derive the real `ShameCrystals` from `PointsSystem`, point the seam's three members at it, flip `Enabled`. The messages and ids S7 needs are in the seam's header |
| **D-38** | The chest pack's weapon/armour/jewellery/clothing drops are plain (`AddLoot` no longer reforges them) and the SA refinement roll (`RefinementComponent.Roll(this, 1, 0.08)`) is absent | Chest loot has no magic properties; no armour refinements from chests | `RunicReforging` (3,391 lines; the Blackthorn decision) and `Services/Refinement` |
| **D-39** | Four Pet Training abilities with no ModernUO counterpart dropped: `StickySkin` (MudPie: slows the attacker's swing 10 s), `ColossalRage` (StoneElemental, GreaterEarthElemental, MudElemental: 50% on being hit, 15 s cooldown), `SearingWounds` (MoltenEarthElemental: cauterises, blocks healing) | Those five creatures hit without their rider effects | Pet Training (B3, WAIT). The Saurosaurus precedent |
| **D-40** | `LifeLeech` (DiseasedBloodElemental) is `DrainLifeAttack`, ModernUO's standard life drain: same 5 energy/s for 5 s healing the attacker, but it triggers at 50% per melee hit against a target with more than 14 mana and takes 15 mana at once, where ServUO's is 10% per hit, costs the creature 5 mana, 10-30 s cooldown, no target-mana condition | The drain lands more often and costs the victim mana | a `LifeLeech`-tuned `MonsterAbility` subclass, ~30 lines, if play says it matters |
| **D-41** | `CrazedMage` runs `AI_Mage`; ServUO's is `AI_Mystic` and `AIType` here has no Mysticism AI | It casts Magery, not Mysticism | a Mysticism AI in ModernUO |
| **D-42** | `DiseasedBloodElemental.TreasureMapChance => 1.0` has no counterpart; the stock roll (`BaseCreature.cs:2966`, `TreasureMap.LootChance`) applies to its level-5 map | A level-5 map sometimes rather than always | a `TreasureMapChance` virtual (a patch); not worth one |
| **D-43** | **A timed-out challenge clears the altar.** ServUO's `EndDeadLineTimer` deletes the guardian but leaves `Guardian` set, so every later `CheckSummon` on that altar answers 1151621 "already been summoned" until the server restarts (only `Deserialize` clears it). One line added: `Guardian = null` after the `Delete`. Read, not run (§9.2) | The altar can be challenged again after a failed hour, as the design reads | removing that line, if ServUO's behaviour turns out to be intended |
| D-34 | `SmartSpawning` (70 rows) has no counterpart — Despise's note only | | |

Not a deviation but recorded here because it is a ServUO reading reproduced as is: **the wall teleporters** (§9.1).

---

## 8. Paper-only differences, not deviations

- **One setup command.** `[GenerateNewShame` generates the 194 spawners when none exist; ServUO needs `[XmlLoad`
  first (and re-issues it inside the command). Same objects, same names. `!Core.ML` returns a message instead of
  silence.
- **`[DeleteShame` removes the spawners too**, because they are tagged into the `newshame` collection; ServUO's
  leaves its `XmlSpawner`s in place. An altar deletes its teleporter and a live guardian, and a wall its troll, when
  the collection deletes them; ServUO leaves those behind. GM tooling, not OSI behaviour.
- **The chest's delete timer.** ServUO starts a 2-6 minute timer on first open; a second open sets the running timer's
  `Delay` to 1-2 s and calls `Start()`, which RunUO ignores on a running timer, so the first delay stands. Here the
  timer is started once.
- **The aura's cadence.** ServUO's `AreaEffect` fires at 40% per think once its 5 s cooldown has passed; ModernUO's
  fires every `AuraInterval` exactly. Same range, damage and type.
- **`TimesImbued > 0`** in the whetstone's refusal: no Imbuing here, so no weapon can be imbued and the test could never
  fire.
- **`Poison.Parasitic`** is `GetPoison("DeadlyParasitic")` on ServUO (`Server/Poison.cs:56`); `Poison.DeadlyParasitic`
  here is the same registered poison.
- **`Region.Find` guard** in `ResetOldSpawners` for a facet with no dungeon region (§3): never taken live.
- **Stock bases differ under us, not because of us.** `GreaterAirElemental : AirElemental` inherits pinned ModernUO's
  `AirElemental`, which packs no necromancy scroll where ServUO's packs one of four. That is the stock creature on
  this shard, not a Shame change; noted so nobody diffs it against ServUO and files it here.
- **`GreaterBloodElemental` sets hits twice** on ServUO (1350-1500, then 900-1000); both lines kept, the second wins
  on both.
- **`DateTime.UtcNow` → `Core.Now`**, the ModernUO convention.

---

## 9. Two ServUO readings worth a question (`notes/codex-questions.md` Q-046, Q-047)

### 9.1 The wall teleporters are inert until the first troll dies, then active whenever the wall stands

`ShameWallTeleporter.CanTeleport` returns true only while an adjacent `ShameWall` addon's `Visible` flag is set.
`BaseAddon`'s constructor sets `Visible = false` on both emulators (ServUO `BaseAddon.cs:66`, pinned `BaseAddon.cs:30`)
and nothing in the Shame code sets it true until the first `Reset()`, two minutes after the first troll dies. From
then on `Visible` stays true (it is a serialized `Item` flag) except during each two-minute sunk window — during which
the wall is 50 z below the floor and the tiles are walkable anyway. So, as shipped: a fresh wall blocks until its troll
is killed; after the first reset the pair of teleporters in front of and behind each piece moves a player through the
standing wall with 1072790 "The wall becomes transparent, and you push your way through it."

Reproduced, not corrected: it is a reading of two constructors and one flag, this machine cannot run ServUO, and the
message text suggests someone meant walking through the wall to be possible. The test pins the reading (`CanTeleport`
false before the first kill, true after the first reset). If the intended design is "impassable while the troll
lives", the fix is one condition in `CanTeleport` (test the wall's troll rather than `Visible`), and a client check is
the way to find out what the wall actually does with a player standing in front of it.

### 9.2 A timed-out challenge leaves the altar stuck (fixed, D-43)

`EndDeadLineTimer` on ServUO: `Guardian.Delete()`, message, `NextSummon = DateTime.UtcNow`, and `Guardian` still
references the deleted mobile; `CheckSummon` tests `Guardian != null` before anything else. Read against ServUO's
`ShameAltar.cs:151-164` and `:93-95`. Fixed with one line and logged rather than reproduced, because the surrounding
code (a cooldown reset to *now*, the "you failed" message) reads as an intent to allow another attempt, and the stuck
state would be invisible until a player hit it.

---

## 10. The row, re-costed from what Shame adds to what Despise taught

Two data points on the directory multiplier now: Despise ×3.25 (a hub with its creatures elsewhere), Shame ×1.7 (a
directory that holds its creatures, with its spawn file naming a chest pack elsewhere). **The profile that predicts
the cost is the spawn XML's type list plus the `Pet Training` token count, not the directory.** Applied to Despise
§10's table:

| Dungeon | Dir files | Spawn XML types absent from pinned ModernUO | `SetSpecialAbility\|SetAreaEffect\|SetWeaponAbility\|SetMagicalAbility` lines | PointsSystem |
|---|---|---|---|---|
| Despise (done) | 4 → 13 | 0 (all 16 in the cluster) | 2 (D-32) | 1 (D-29) |
| Shame (done) | 11 → 19 | **4 (`TreasureLevel1-4`), 116 of 194 rows** | **12** across 8 creatures (§7 D-39/D-40, plus 4 mapped) | 2 (D-37) |
| Wrong, Covetous, Exodus, Blackthorn | per Despise §10 | **not yet counted — count them before costing** | not yet counted | 0 / 2 / 0 / 3 |

What each column now costs, from this task:

- **Chest pack: paid.** `BaseTreasureChestMod` + `TreasureLevel1-4` are in; a later XML naming them costs nothing.
  `TreasureLevel1h` and the higher levels are 60 lines each if a file names them.
- **High Seas resources: five paid.** `Saltpeter`, `Potash`, `Charcoal`, `BlackPowder`, `VoidCore` exist now at
  ServUO's paths; CC5/CC8 should expect to find them.
- **Pet Training: the token count, not the file count.** Shame's "2" was 12. Each mapped line (breath, aura, life
  drain) is a one-line transformation; each unmapped one is a D-39 entry. Budget the grep.
- **PointsSystem: two dungeons carry it inert now, and Shame's loss is the larger** (the guardians are the level
  bosses; Despise lost a vendor). Covetous has two hits, Blackthorn three. The seam pattern means S7 can land behind
  the ports without touching them, but every dungeon ported before S7 ships with its point economy dead. That is the
  tenth argument for S7 (B7, 12 files / 2,857 lines, "unblocks 55") and it belongs before Covetous or with it.
- **Regions: the priority rule is for dungeons that construct regions** (§3). Shame constructs none.
- **WeakEntityCollection: paid** (Despise), used again here for 228 entities.

**Recommended order:** unchanged from Despise §10 — Wrong, Exodus, Covetous, Blackthorn — with one addition: before
each, grep its XML's `Objects2` names against pinned ModernUO and count the four ability tokens, and put the answers
in the brief.

---

## 11. What it cost

| Phase | Measure |
|---|---|
| Reading and pre-flight: `AGENTS.md`, `docs/tasks.md`, Despise's note, the 19 ServUO files and the XML (parsed by script), ServUO's Pet Training and XmlSpawner cap code, ModernUO's spawner/region/addon/teleporter/container/loot/poison/ability/timer code, every signature the cluster calls, 37 collision checks | the bulk of the task |
| Writing 20 files + test + probe | the middle third |
| Builds | A (2 errors: a `ref` to a property, `Party` binding to `Mobile.Party`), B (one xUnit analyzer rule), C (50/4: my ChaosVortex miscount, the null corpse, golem gold from `GenerateLoot(true)`, a 0-hit player), D (49/5: one failing fact's leftovers cascading into three others, D-43 not yet applied, `names.json`, mana regen), E (53/1: regen race), **F green 54**, RED (52/2: the golem as intended, plus the regen poll flake, hardened), **FINAL green 54**. Each full cycle 2-4 minutes |
| Headless runs | run 1 fresh with probe ~2 min, run 2 reload ~2 min, run 3 final image ~2 min |
| Context | ~540k tokens at the point of writing this note (15.0M budget → ~14.46M). Compare Despise ~700k for 14 files, CC3's 278k for 17 leaf files: **a dungeon whose creatures are already in its directory costs less than a hub, and the reading is still the larger half** |

**Not verified, per the standing rule, and batched for the client spot check:** appearance of the 22 creatures and
three guardians (bodies, hues; `MudPie` body 779 hue 2012, `CaveTroll` body 1 hue 638, the four hued elementals, the
two human mages with robes 1156/1157, `ChaosVortex` body 164 hue 34212), the chest art (the random crate/chest/keg
ids per level) and their lock/trap behaviour at a real lockpick, the whetstone's target cursor, the altar's
`ForceShowProperties` tooltip and its 1151623 refusal, the wall in motion (§9.1 is the one to look at first: stand a
character in front of a fresh wall, kill the troll, wait two minutes, walk into it), the vortex pull and the fire
breath/aura in a fight, and `[DeleteShame` on a world with players inside.
