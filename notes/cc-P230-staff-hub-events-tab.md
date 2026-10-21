# cc-P230: Staff Hub Events tab, GM-run monster surges (F-30 second batch)

Copper Golem, 2026-10-21. Server only. Branch `golem/Copper/P230` in both repos. Image `sl-modernuo:cc-P230`.

## Headlines

- **The Events tab is open.** `[SL` (GameMaster and up, live and test) now has a working fourth tab. A GM picks a creature
  template, sets the spot (Here or Target), radius, waves, count per wave and interval, then presses Start or Dry run.
  Start broadcasts, spawns wave 1 at once and the rest on the interval. While a surge runs, the tab shows its progress
  with End, Go there and Give extra.
- **Templates** are saved creature groups in their own versioned save file. Three starters ship: Orc raid, Undead rising,
  and Ogre warband (a named Ogre Lord boss with adds). Every creature in them is a pinned type. A GM can add more (New)
  or delete one.
- **Cleanup.** Every creature and gate a surge makes is flagged in the run and, by serial, in a small save file. End
  deletes what is left and closes the gates. A restart mid-surge deletes them all at world load, with no prizes.
- **Options per surge:** moongates from Britain and New Haven to a staging spot; a **no-loot zone** (a player who dies
  inside keeps everything, with no patch); and **prizes in any mix**:
  - top N by damage over the whole surge get the top prize;
  - everyone else who did damage, or who was present for at least half the run, gets the share prize;
  - the GM hands out extras by target.

  The GM names every prize item; gold is the default.
- **No patch, no core edit.** Our own small system; pinned's champion spawn and the ServUO invasions were read and not
  reused (Part 1).
- **Tests:** 8 new facts in `server/tests/Misc/StaffHubEventsVerification.cs`, each seen failing first at its own
  assertion. The full suite is green through `docker/uo/build.sh`: 1,879 tests, 1,875 passed, 0 failed, 4 skipped, and
  the image was built.

## Part 1: prior art, and the choice (written before building)

**Where the sources were.** Neither `D:\UO\ModernUO-pinned` nor `D:\UO\ServUO-pub57` exists on this PC. I read pinned
from the builder image, as AGENTS.md says (`sl-uo-builder:cc-P229`, `/build/modernuo`: the patched build tree at
d4531cd9, copied to scratch). I read ServUO pub57 from GitHub (`ServUO/ServUO` at tag `pub57`: the tree listing and three
raw files, saved to scratch, never built or run).

**Pinned champion spawns** (`Engines/CannedEvil/ChampionSpawn.cs`, 1,534 lines). A `ChampionSpawn` is a world `Item`:
- It owns an altar, a platform, an idol and a region (`:170-181`).
- It escalates by **kills** (`OnKillsChanged` `:260`, `AdvanceLevel` `:674`).
- It keeps `MaxSpawn` alive (`Respawn` `:766-817`, `250 - sublevel * 40`), drawing from a fixed per-type table
  (`ChampionSpawnInfo.Table`, `ChampionSpawnInfo.cs:44`).
- It ends in a champion with skulls, titles and power-scroll rewards.

A surge is the opposite shape: GM-chosen creatures, a fixed number per wave on a **timer**, and nothing placed on the
map. Reusing `ChampionSpawn` would put an altar and platform in the world and pay champion rewards, so the class is
**not reused**. Two of its patterns are:
- the spawn point: up to 20 random points in the area, `Map.GetAverageZ` then `Map.CanSpawnMobile`, else the centre
  (`GetSpawnLocation` `:819-845`);
- `Home` and `RangeHome` on each creature (`:792-797`).

**Pinned `Engines/Events/EventScheduler.cs`** (146 lines) is a calendar timer: hourly, daily, weekly, monthly and yearly
recurrence (`:25-75`, `ScheduleEvent` `:87-107`). A GM starts a surge on the spot, so surges do not go through the
scheduler. A scheduled surge (for example every Saturday) could be added later by calling `ClusterFSurge.Start` from a
`ScheduledEvent`. That is not built here.

**ServUO pub57 town invasions.** Two exist, and both are tied to their own content:
- `Services/Revamped Dungeons/BlackthornDungeon/InvasionSpawner/InvasionController.cs` (647 lines), Minax's city
  invasions. A world-item controller sends waves of 8 to 10 per spawn rectangle plus a captain (`SpawnWave` `:177`). The
  wave advances on kills (`OnDeath` `:262`, `CompleteWave` `:327`). `RemoveSpawn` kills what is left (`:421`). Rewards go
  by the beacon's looting rights in range (`OnEndInvasion` `:367-401`).
- `Services/Tomb of Kings/Arisen Invasion/ArisenController.cs` (280 lines).

cc-P196 ported Blackthorn's invaders but left the controller for a later prompt (cc-P196 notes `:27`, `:335`). Neither
is a GM tool.
- **Taken as ideas:** waves drawn from a list of creature types, a cleanup that removes what is left, and prizes by who
  did the damage and who was in range.
- **Not taken:** the beacon, the city table, the XmlSpawner attachments.

**The choice.** Our own small system in `server/customizations/StaffHub/`, with no patch and no core edit:
- surge templates in their own versioned save file (like `ClusterFStaffHubSpots`);
- one live surge, run by a one-second timer;
- every creature and gate it makes recorded by serial in a second small save file, so a restart deletes them at world
  load.

## What changed

ShatteredLegacy repo:

| File | What |
|---|---|
| `server/customizations/StaffHub/ClusterFSurge.cs` (new) | `SurgeSettings` `:39` (defaults and limits); `SurgePrize` `:76` (parse "Gold 2000", give to a backpack); `SurgeRun` `:152` (one surge: creatures, gates, ticks, presence, damage, awards; `SampleDamage` `:201`, `WasPresent` `:234`); `ClusterFSurge` `:237`: gate spots `:246`, `Problems` `:275`, `Plan` `:354` (Dry run), `Start` `:417`, `OpenGates` `:454`, `SpawnWave` `:472`, `SpawnPoint` `:548`, `Tick` `:575`, `OnCreatureDeath` `:619`, no-loot `InNoLootZone` `:633` / `OnPlayerDeath` `:637`, `End` `:660`, `Finish` `:673`, `Winners` `:724`, `Award` `:752`, `GiveExtra` `:783`, the restart save `WriteTo` `:818` / `ReadFrom` `:835` / `CleanUpAfterRestart` `:856`. |
| `server/customizations/StaffHub/ClusterFSurgeTemplates.cs` (new) | Templates in `Saves/StaffHubSurgeTemplates` (version 0, `:37`); the starters `:60`; `SeedIfNeverSeeded` `:77` (once, the flag is saved); `CreatureType` `:95`; `ParseCreatures` `:107` ("Orc*4, OrcishMage*2"); `Save` `:157`; `WriteTo` `:216` / `ReadFrom` `:238`. |
| `server/customizations/StaffHub/StaffHubGump.cs` | The Events tab is a real button (`:176`, labelled "Events (live)" while a surge runs); Events button, text and switch IDs `:82-116`; `DrawEvents` `:558` (setup), `DrawSurge` `:649` (running or just ended); `SurgeInput` `:711` and `ApplySurgeInput` `:720` (the boxes and checkboxes are read on any button, `:873`); `RespondEvents` `:756`; tab range now 4 `:875`; `StaffHubTemplateGump` `:1203` (New template). |
| `server/customizations/StaffHub/ClusterFStaffHub.cs` | Header line for Events `:13`; `StaffHubState.Surge` `:695`. |
| `server/tests/Misc/StaffHubEventsVerification.cs` (new) | 8 facts, below. |
| `server/tests/Misc/StaffHubVerification.cs` | `NoButtonIdMeansTwoThings` `:755`: the Events tab button counts as chrome, and the Events setup gump joins the "no two tabs share an ID" comparison. |
| `server/tests/Misc/StaffHubReadabilityVerification.cs` | `EveryTab` `:105`: the Events setup joins the solid-panel check. |
| `CHANGELOG.md`, `VERSION` | New section 2026.10.21.3 (Added, Staff). VERSION bumped from 2026.10.21.2, whose section was already committed. |

Two new save files: `Saves/StaffHubSurgeTemplates/StaffHubSurgeTemplates.bin` and `Saves/StaffHubSurge/StaffHubSurge.bin`.
Both are pinned `GenericPersistence`s with their own version, and an unknown version throws (the D40 rule). The account
data is not touched.

### How each part works

- **Part 2, templates.** The starters are Orc raid (Orc x4, OrcishMage x2, OrcBomber, OrcCaptain), Undead rising
  (Skeleton x3, Zombie x3, Ghoul x2, SkeletalMage x2, BoneKnight) and Ogre warband (Ogre x3, Ettin; the boss is an
  OgreLord named "Grumak the Breaker", who comes with the last wave). Every type was checked in pinned
  `Mobiles/Monsters/Humanoid/{Melee,Magic}` (16 of 16 found), and fact 6 resolves each at runtime. A creature type must
  be a `BaseCreature` with a constructor that needs no arguments. That uses pinned's own `GetConstructor(out _)`, which
  counts a constructor whose parameters are all optional. I found that rule because `Gold(int amount = 1)` failed my
  first check.
- **Part 3, running a surge.** The layout follows the approved mockup's parts:
  - background 9270;
  - tabs on 2445;
  - 4005 go arrows (Here, Target, Staging here, New);
  - 4017 to delete a template;
  - 2117/2118 radios for the templates;
  - 210/211 checkboxes for gates, no-loot and the three prize modes.

  **Start** broadcasts "A surge! <template> gathers near <region, x, y, z on facet>." in hue 0x35. Each later wave and
  the end are broadcast too. **Dry run** sends the plan and every problem as lines, and makes nothing. The **moongates**
  are two stock pinned `Moongate`s (not dispellable, hue 0x26, named "a surge moongate"), both on Trammel:
  - Britain: pinned `Distribution/Data/Locations/trammel.json` "Britain / Center", 1475, 1645, 20;
  - New Haven: three tiles south of `ClusterFNewHavenSeeder.BankAnchor`.

  They lead to the staging spot, or to the surge spot when none is set.
- **Part 4, cleanup.** End (or the surge ending by itself: last wave out, every creature dead) deletes the creatures and
  gates. The restart file holds the live run's creature and gate serials. At world load `CleanUpAfterRestart` deletes
  only those serials that are still a creature or a moongate, so a serial that now means something else is left alone.
- **Part 5, no-loot zone.** Pinned raises `PlayerDeathEvent` from `PlayerMobile.OnDeath` (`PlayerMobile.cs:2609`), after
  `Mobile.Kill` has made the corpse and set `Corpse`. Inside a running surge's radius, the handler moves the corpse's
  contents back into the backpack. Equipped items land in the pack, not worn, which is where a Young player's items go
  (`PlayerMobile.GetParentMoveResultFor`). **Register as ours:** agents do not edit `docs/`, so the line for
  `docs/fidelity-principle.md` (or wherever our deliberate "ours" behaviours are listed) is, for promotion: *"Staff Hub
  monster surges may set a no-loot zone: a player who dies inside the surge radius while it runs keeps all items in
  the backpack (cc-P230). Not OSI."*
- **Part 5, prizes.** Damage comes from pinned's per-creature `DamageEntries` (`Mobile.cs:974`), because pinned raises no
  damage event:
  - It is read every second and at each creature's death (`CreatureDeathEvent`). The creature is already deleted then,
    but its entries are intact.
  - A pet's damage counts for its master. Staff damage never counts.
  - Each entry object is tracked, so a hit after an entry expires or is cleared (a new `DamageEntry`, `RegisterDamage`)
    is counted from 0 and not lost.

  **Present** means inside the radius (UO's square range, `GetMobilesInRange`) on at least half of the one-second counts,
  alive or a ghost, players only. Prizes are paid on End or when the surge ends by itself:
  - top N damage dealers get the top prize;
  - other damage dealers, and players present for half the run, get the share prize, once each, and never on top of a
    top prize;
  - **Give extra** (target) pays the extra prize while the surge runs, or after it from the summary.

  A prize is any item type with an argument-free constructor: up to 60,000 if it stacks, up to 10 copies if not.
- **Part 6, live and test.** No surge path checks `TestCenter`. Fact 7 runs a whole surge with `TestCenter.Enabled`
  false. Access is the hub's: everything returns at once below GameMaster (fact 7 presses Start as a Counselor).

## Tests

`server/tests/Misc/StaffHubEventsVerification.cs`, 8 facts:

1. `ASurgeSpawnsTheRightCountPerWaveOnTheInterval`: on `ShardTestClock`, 3 waves of 4 every 30 s give 4 at once, still 4
   at 29 s, 8 at 30 s, then 13 at 60 s (the boss, named, comes with wave 3), and nothing more after. Every creature is
   of the template's types, inside the square, not tamable, and homed on the spot. Dry run's plan reads "13
   creature(s)" and nothing starts.
2. `EndLeavesNoFlaggedCreatureOrGate`: 10 creatures and 2 gates (in Britain and New Haven, both to the spot); one is
   killed; End deletes every creature and both gates. A second surge whose creatures all die ends by itself on the
   next tick.
3. `ARestartMidSurgeCleansUpOnLoad`: save mid-surge, drop the surge as a crash would (everything still in the world),
   load, `CleanUpAfterRestart` deletes exactly the 3 creatures and 2 gates. A serial now held by an unrelated item is
   left alone. An empty save cleans nothing. An unknown version throws.
4. `DamageShareAndPresenceAreCountedAsSpecified`:
   - Damage: a deals 50, then minutes later (that entry gone) 80 on the same ogre and 20 on another, 150 in all; b
     deals 40; the GM's 30 is not counted.
   - Presence: c stays, d leaves after a second, far is never there.
   - Prizes, top 1: a gets 2,000 gold (top only); b gets 500 (damage) and c gets 500 (present); d and far get nothing.
   - Extras are refused when the surge did not turn them on.
5. `TheGmHandsOutExtrasAndPrizesCanBeAnyMix`: with extras on, Give extra pays during the surge and from the summary after
   End, and refuses staff. With presence off, standing there earns nothing. Prize text must be an item type, with
   unstackables capped at 10.
6. `TheNoLootZoneKeepsADeadPlayersItems`: died inside the zone, the worn robe and packed sword are in the backpack and
   the corpse is empty. Outside the radius, or after End, they are on the corpse.
7. `TemplatesSaveAndLoad`: the three starters are seeded once and resolve. Bad input is refused by name (an unknown
   type, weight 0, empty, an item instead of a creature, an item as boss, a blank name). A saved template round-trips
   through a save. Deleted starters are not re-seeded. An unknown version throws. The New template gump saves and
   selects.
8. `TheEventsTabRunsASurgeThroughItsButtons`: on live:
   - The Events tab is a button; the art ids are 9270, 2117/2118 and 210/211.
   - Here plus the typed boxes and switches set the settings.
   - A non-number is refused by name. Dry run makes nothing. Start runs it.
   - The running view has End and Go there and no entry boxes. Go there moves the GM; End clears.
   - The summary has New surge.
   - A template is deleted from its row.
   - A Counselor's press does nothing.

The fixture saves and restores the template store, so the facts leave the real store as it was.

**Seen failing first.** I ran `docker/uo/build.sh -t sl-modernuo:cc-P230 --tests-only` with eight marked breaks in the
implementation (each marked `P230-BREAK`; the real files were saved first and copied back, `cmp` identical, no marker
left):
- the third wave one short;
- End leaving the gates;
- the restart cleanup skipping moongates;
- damage not tracking the entry object;
- extras only while running;
- the no-loot handler not moving items;
- templates load forgetting the seeded flag;
- the Events tab drawn as an image.

Result: 1,879 tests, **8 failed, exactly the 8 new facts**, each at its own assertion:

| Fact | Line | Failure |
|---|---|---|
| 1 | `:202` | "Expected (3, 13), Actual (3, 12)" |
| 2 | `:251` | both Moongates left |
| 3 | `:295` | "Expected 5, Actual 3" |
| 4 | `:373` | "Expected 150, Actual 100" |
| 5 | `:420` | "Extras are not on for this surge." |
| 6 | `:457` | Expected Backpack, Actual Corpse |
| 7 | `:513` | Seeded false after load |
| 8 | `:544` | the tab button not in the set |

**Before that, real code:**
- **Run 1** did not compile: `foreach` over `DamageEntries` needs `using Server.Collections` (the
  `ValueLinkListExt.GetEnumerator` extension).
- **Run 2:** 6 facts failed, all on one cause. `GetConstructor(Type.EmptyTypes)` refuses `Gold`, whose constructor is
  `Gold(int amount = 1)`, so "Gold 2000" was "not an item type". Fixed by using pinned's `GetConstructor(out _)`.
- **Run 3:** green.

**Full suite, real code** (`docker/uo/build.sh -t sl-modernuo:cc-P230`, docker-build lock taken and released): "Total
tests: 1879, Passed: 1875, Skipped: 4", then "Built sl-modernuo:cc-P230 with patches applied and 1875 shard test(s)
passing." `CHANGELOG.md` and `VERSION` were edited after this run. No test reads them (the patch-note facts carry their
own text).

## Deviations and decisions for Chase

1. **One surge at a time.** Start refuses while one runs. That is enough for one GM, and it keeps End and the restart
   cleanup simple. Say if you want two at once.
2. **How the prize modes combine** (my reading of "any mix", with the overseer's defaults):
   - Damage mode: the top N (default 3) get the top prize, and every other player who did damage gets the share prize.
   - Present mode: everyone present for half the run gets the share prize.
   - Nobody is paid twice; a top winner does not also get a share.
   - Prizes are paid on End and when the surge ends by itself, never after a restart.
   - Defaults: top 2,000 gold, share 500 gold, extra 1,000 gold. Damage and present are on, extras off.
3. **Damage that heals away unseen is lost.** Pinned clears a creature's damage entries when it is back at full health
   (`Mobile.cs:2043`). Damage done to a creature that heals to full before the next one-second read is not counted.
   On the live shard that needs a heal to full within the second. The test host regenerates 125 hits a second, so
   fact 4 lands its hits just before the read and says why.
4. **No-loot keeps items in the pack, not worn**, like a Young player's. Pinned's insurance step runs before the death
   event, so **an insured item is still charged its insurance fee** in a no-loot zone. Say if the zone should skip the
   fee (that would need a hook before `Insurance.CheckInsuranceOnDeath`, which is a patch).
5. **Gate spots are fixed:** Britain centre (pinned's [Go list) and three tiles south of the New Haven bank anchor, both
   Trammel. Not checked in a client (see For Chase). The staging spot is "Staging here" or, by default, the surge spot.
6. **Templates are shard-wide**, not per account. Saved spots are per account because they are personal; a raid
   template is shared kit.
7. **Surge creatures drop their normal loot**, are not tamable, and stay near the spot (`RangeHome` = the radius).
   Pinned's `OnBeforeSpawn` runs as the champion spawn does, so an Ilshenar surge can roll paragons. Say if surges should
   drop nothing.
8. **Limits:** radius 1 to 40, waves 1 to 20, 1 to 50 per wave, an interval of 10 to 3,600 seconds, up to 8 creature
   types a template, and up to 20 templates (the tab shows 8).
9. **A GM may name any item as a prize.** There are no F-13-style guardrails here, since it is a staff tool.
10. **Neither source tree is on this PC.** Pinned was read from the builder image and ServUO pub57 from GitHub
    (Part 1). Worth restoring `D:\UO\ModernUO-pinned` and `D:\UO\ServUO-pub57` on the Copper PC.
11. **Not built:** scheduled surges (EventScheduler, Part 1), and a per-surge choice of gate towns.

## For Chase (in the client, test shard)

1. `[SL`, then **Events**. The three starter templates are listed. Pick one, stand where you want it, press **Here**
   (or **Target**), set the radius, waves, count per wave and interval, and try **Dry run**: the plan prints in your
   journal and nothing spawns.
2. Tick **Moongates** and **No-loot zone**. Leave **Present, others** on and set the prize boxes. Then **Start**. Check
   the shard-wide message and both gates: Britain centre (1475, 1645) and south of the New Haven bank. Do they stand on
   open ground, and do they take you to the spot?
3. Watch the waves arrive on the interval. The tab shows the wave, the next wave's countdown, alive and killed counts,
   and top damage. With a player character, die inside the radius: you rise with everything in your backpack.
4. **Give extra** (if ticked) targets a player. **End**: the creatures and gates vanish, prizes arrive with a message,
   and the tab shows who got what. **New surge** goes back to the setup.
5. Restart test: start a surge, `[save`, restart the test shard. The console prints "Staff Hub: removed N creature(s)
   and gate(s)", and nothing of the surge is left.
6. **New** on the Events tab: make a template ("Orc*3, OrcishLord", boss "OrcCaptain" named as you like) and run it.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, 2026-10-21:

```
Repo Result
---- ------
code dry run
docs dry run
```

Neither repo is BLOCKED. Code: the 9 files above (`CHANGELOG.md`, `VERSION`, 3 StaffHub customizations, 3 test files,
`ClusterFStaffHub.cs`). Docs: this note. No file in either change is over 5 MB. The scratch copies of the pinned and
ServUO sources are in the session scratchpad, outside both repos.

P230 DONE
