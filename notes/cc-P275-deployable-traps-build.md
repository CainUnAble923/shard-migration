# cc-P275: deployable traps, phase 1 build (P201's design, as recommended)

## In plain words

- Tinkers can now craft eight trap kits, and Remove Trap sets them on the floor (and picks them up again), gaining
  skill both ways. Traps only ever catch monsters, and only while their owner stands within 12 tiles.
- A trap fires a few times and then waits for its owner to re-set it by hand, so nobody can farm with them while away.
  The Thieves' Den gives one more trap at Journeyman, and Master's traps work on bosses.
- The Rootdeep Burrows get the trap lesson (two practice nets in the Stacks; catching a rat finishes it) and eight
  stock floor traps, placed the next time `[ClusterFSeedRootdeep` runs.
- Four pieces of art (and pack icons) are requested; placeholders stand in until they land. Nothing was deployed.

2026-10-21, the Silver Golem (Opus), branch golem/Silver/P275 of both repos. Prompt:
`D:\UO\cc-prompts\claimed\Silver\cc-P275-deployable-traps-build.md`. Chase approved P201's recommendations D1 to D7
("Lets get this"). Not committed (the Golem commits after DONE). Both repos were clean at the start. Nothing was run
against any world, no shard was started, nothing deployed, the package was not built.

## Headlines

- **Built as the design recommends, D1 to D7.** Four new files under
  `server\customizations\Items\Traps\Deployable\`:
  - `DeployableTraps.cs`: the rules and every number. All of section 3's numbers are settings
    `clusterf.traps.<trap>.<name>` (charges, radius, damage, holds, slow, the Tinkering and Remove Trap gates), plus
    `clusterf.traps.pvp` (false), `presenceRange` (12), `decayMinutes` (30), `spentDecayMinutes` (2), `areaCap` (6),
    `areaCapRange` (8), `setRange` (2) and `practiceHoldSeconds` (4).
  - `DeployableTrapKit.cs`: the eight kits (`SnareNetKit`, `CaltropsKit`, `GasTrapKit`, `BlastTrapKit`, `DartTrapKit`,
    `BearTrapKit`, `AlarmTrapKit`, `ShackleTrapKit`), loading by drop, the set (target, arming time, the hidden set's
    stealth step).
  - `DeployedTrap.cs`: the set trap. Fires, presence, owner credit, charges, hand re-set, decay, Detect Hidden reveal,
    Remove Trap disarm and salvage.
  - `TrapLesson.cs`: The Stacks as a child region of the Vault, the Echo's practice nets, the lesson key.
- **The Tinkering ladder** gets the eight kits in pinned's Traps group (`TinkeringCraftRegistrations.RegisterDeployableTraps`),
  gates 30 to 110 (each gains to 50 above, but never past the shard's stock top of 130), ingredients as section 3 (cloth and spider's silk; ingots, springs,
  gears, a bolt, a Paralyze scroll).
- **The Burrows map is in main** (P188, merge `7e1f887`), so the eight stock floor traps went in as seeder rows
  (`ClusterFRootdeepSeeder.FloorTraps`). They are placed by the next `[ClusterFSeedRootdeep` (dry run first), not by
  this prompt.
- **No new patch.** Remove Trap's target reaches the trap through cc-P199's `IRemoveTrapTrainingKit` hook (it hands the
  skill's target to the item), and Detect Hidden through cc-P195's `IRevealableItem` hook.
- **Tests:** 12 new facts (`server\tests\Items\Traps\DeployableTrapsVerification.cs`), each seen red for its own
  reason in one of two deliberately broken builds, then green; the full gate is in "Build record".

## What each decision became

### D1 and D2: Remove Trap, Tinkering, Poisoning, Alchemy, the Den

| Rule | Where | Number |
|---|---|---|
| Setting a trap is a Remove Trap use: the kit's own Remove Trap minimum, arming time `4 - RT/100` s (1 s hidden) | `DeployableTraps.CanSetAt`, `DeployableTrapKit.SetTarget` | snare 0, caltrops 20, dart 30, alarm 30, gas 40, bear 50, blast 60, shackle 80 |
| Set gain: `CheckSkill(RemoveTrap, min, min + 50)` on every set and re-set | `DeployableTrapKit.Set`, `DeployedTrap.ReSet` | |
| Hit gain: `CheckSkill(RemoveTrap, min + 40, min + 120)` on every fire (the owner is present by rule) | `DeployedTrap.Fire` | the shackle's reaches 200 |
| Disarm gain: the owner rolls the set window and always packs the trap back into a kit; anyone else rolls `CheckTargetSkill` on the same window and salvages the kit on a success (a Den Grandmaster always succeeds) | `DeployedTrap.OnRemoveTrap` | |
| Poisoning: a poison potion dropped on a gas trap is a Poisoning use on the potion's own window and loads `min(potion level, Poisoning / 25)`; the potion is spent either way | `DeployableTrapPayloads.Load` | |
| Alchemy: an explosion potion dropped on a blast trap loads lesser, normal or greater (20-40, 30-60, 40-80 fire) | same | |
| Darts: fukiya darts dropped on a dart trap load up to 5, a poisoned dart keeps its poison | same | |
| Den Journeyman: one more trap out (`1 + RT/50`, +1) | `DeployableTraps.MaxOut` | |
| Den Master: traps work on bosses (`ThievesDenStealRules.IsBoss`), at half damage and half hold; below Master a boss walks through, the trap stays armed and the owner reads the design's line | `DeployableTraps.Shrugs`, `OwnerMayTrapBosses` | |

### D3: the eight traps

| Trap | Fires on | Effect | Charges (exceptional) |
|---|---|---|---|
| Snare net | a step within 0 (1 at RT 100, 2 at 200) | `Frozen` for 4 + RT/50 s | 1 (2) |
| Caltrops | a step into radius 1 | 5-10 physical, bleed, active speed doubled 8 s | 5 steps |
| Gas | a step into radius 2 | the loaded poison on every target in radius 2 | 1 (2) |
| Blast | a step into radius 2 | the loaded charge's fire damage on every target in radius 2 | 1 |
| Dart | a step within the snare's reach | 25-50 physical, the dart's poison while it lasts | one per dart, up to 5 |
| Bear trap | a step onto its own tile | `Frozen` 6 + RT/50 s, 15-30 physical, bleed; opens again for the next snap | 3 (4) |
| Alarm | a step into radius 2 | tells the owner "Your alarm at <region>, <x>,<y>: <creature>." with sound 0x495 | 10 |
| Shackle | a step within the snare's reach | `Frozen` 3 + RT/50 s on every target in radius 1 | 1 (2) |

Damage is the kit's roll x `0.5 + RT/200` x 1.2 exceptional x 1.5 for a hidden set's first hit on a creature with no
combatant. Flyers pass over the snare, caltrops and bear trap; the incorporeal list (Shade, Spectre, Wraith, Bogle,
Wisp, Energy Vortex, Blade Spirits, Air and Poison Elemental) passes through those and the dart; paragons take half
the holds and the slow. A creature with Detect Hidden rolls once per trap (`DH + Random(21) - 10` against concealment
`RT (+20 hidden) + Random(21) - 10`); a spot reveals the trap for 10 s and tells the owner.

### D4: monster-only

`DeployableTraps.IsTarget`: a wild, living, unsummoned `BaseCreature` that is a monster, not a vendor or invulnerable,
and a tutorial creature only for an owner it engages; then the owner's `CanBeHarmful`. Players, pets, summons and
dead bonded pets never trigger. With `clusterf.traps.pvp` on and the trap in Felucca, anyone the owner may harm is a
target and the hit calls `owner.DoHarmful(victim)`.

### D5: presence, credit, charges

- **Presence** (`DeployableTraps.OwnerPresent`): same map, within 12 tiles, alive, logged in (`NetState`). The alarm
  needs only the map and the login.
- **Credit:** every damage is `AOS.Damage(target, owner, ...)`, every poison `ApplyPoison(owner, ...)`, every bleed
  `BeginBleed(target, owner)`. The fact checks the owner is in `DamageEntries` and holds `GetLootingRights`.
- **Charges, no timers:** a spent trap does nothing until the owner double-clicks it (or drops a fresh payload on a gas,
  blast or dart trap). Nothing re-arms on a clock; the bear trap opening between its own three snaps is the design's
  one exception. The only clocks are litter (the world's item decay: 30 minutes from the last set, 2 once spent) and
  the holds and slow themselves.

### D6: the Rootdeep Stacks lesson

- `RootdeepStacksRegion` (x 5156-5168, y 1132-1142) is a child of the Vault at priority +2. Walking in and teleporting
  in are asked of the Vault outright, so the Vault's rules hold unchanged. No existing region fact changed (their
  points are outside the Stacks; all Rootdeep facts pass).
- A participant who has not done the lesson and carries no practice net gets two on entry, with the Echo's line naming
  the Hoarding Rat. A practice net: no skill to set, 1 charge, a 4 s hold, the Burrows only (double-clicked anywhere
  else it crumbles), never salvaged.
- Any Penny Rat or Hoarding Rat held by a participant's net (practice or real) adds `burrows.trap` to
  `TutorialRecord.StationsDone`, the same no-schema pattern as the Vault's own key, with the Echo's line.
- **The eight floor traps:** P201's tiles, checked against the built floor (`notes\cc-P167-tools\plan-cells.json`: all
  eight are floor) and the decor list (`statics-placed.csv`: nothing on any of them).

| Row | Tile | Class |
|---|---|---|
| T1, T2 Deposit Hall | 5146,1134; 5151,1139 | `MushroomTrap` |
| T3, T4 Warren descents | 5161,1195; 5201,1195 | `SpikeTrap` (west floor) |
| T5 the Thicket's gap | 5157,1222 | `SawTrap` (north floor) |
| T6, T7 the Gloom ring | 5165,1235; 5232,1252 | `GasTrap` (floor, Greater poison) |
| T8 the Queen's lair mouth | 5183,1247 | `StoneFaceTrap` |

  P201 said every tile sits outside every spawner's home range. **Counted, that is not true for T6 and T7:** T6 is
  inside the Gloom north hatchery's box (5166,1236, range 5) and T7 inside the east weavers' (5232,1250, range 4). It
  does not matter: pinned's `GasTrap` hurts players only (`GasTrap.cs:64`), so no spawn dies on it. The fact checks
  the rule for the five classes that hurt creatures, and they all pass.

### D7: art

- **Stock for six:** fishing net 0x0DC8 (snare), floor spikes 0x119A / 0x11A0 (caltrops), keg 0x1940 (blast), bear
  trap 0xB2C5 / 0xB2C3, cowbell 0x4C5A / 0x4C5B (alarm). Tiledata read from the 7.0.117.0 client: all walkable except
  **the keg, which is Impassable**. That is why the area traps fire on a creature entering their radius rather than
  on a step onto the item.
- **Placeholders until the art lands:** gas trap = green potion 0x0F0A (hued), dart trap = fukiya darts 0x2806,
  shackle = Magic Trap scroll 0x1F39 (hued). The snare's sprung look is the set net hued grey. The ids are in
  `DeployableTraps.SetArt` / `SpentArt`, one line each to swap.
- **The bear trap's client check:** tiledata knows 0xB2C5 "Bear Trap On" and 0xB2C3 "Bear Trap Off" (no flags), and
  P201 rendered both from this client's art. The art registry claims neither (nor any trap id used here). The package
  ships no art above 0x8000 yet, so whether TazUO draws a static at 0xB2C5 is still unproven. It is a play test
  (below).

#### Art request list (P152's pipeline)

Filed with `scripts\art\New-ArtRequest.ps1` on this PC: all five returned `ok`, in `D:\UO\art\requests\`. **This PC's
art store was empty before** (no other request, no review or archive folders), so it may not be the store Chase's
console reads. The filing script is `notes\cc-P275-tools\file-art-requests.ps1`. Run it on the console PC if these
five do not show in the Art tab. It refuses an id that already exists, so a second run is safe.

| Id | Title | Slots (44 x 44, transparent, 8 KB) | Subject |
|---|---|---|---|
| `trap-snare-net` | Snare net, sprung | sprung, icon | a rope net bundled tight round nothing, pegs pulled, on stone; icon: a folded net with a peg |
| `trap-dart-launcher` | Dart trap, floor launcher | set, sprung, icon | a palm-sized iron plate with a spring tube and a dart tip, half-buried; sprung: the tube open and empty |
| `trap-gas-canister` | Gas trap, canister | set, sprung, icon | a squat iron canister, cork, tiny bellows, green glass window; sprung: cracked, green stain |
| `trap-shackle-ring` | Shackle trap, rune ring | set, sprung, icon | a faint blue-grey chalk rune circle with four marks; sprung: scuffed through |
| `trap-icons` | Pack icons for the stock traps | bear, caltrops, blast, alarm, practice net | pack icons matching each stock ground art |

Destination `game-item`, folder `player-package\vendor\shattered-legacy-art\art`. The style line is the design's
section 7.2. When they land, the ids are registered through P26 (`find-free-art.py`, `registry.csv`), and the
placeholders in `DeployableTraps.SetArt` / `SpentArt` are swapped.

## Tests

`server\tests\Items\Traps\DeployableTrapsVerification.cs`, 12 facts:

| Fact | What it checks |
|---|---|
| `EachTrapFiresOnAMonsterAndNeverOnAPlayerPetOrSummon` | for all eight: hidden, owner sees it, a stranger does not; a player, a pet and a summon walk in and nothing happens (charges kept); a troll walks in and the trap's own effect lands and a charge goes |
| `ThePvpSwitchLetsAFeluccaTrapHitAPlayerAndFlagsTheOwner` | setting on: Trammel still spares a player; Felucca hits one and the owner is in the victim's aggressors |
| `ATrapFiresOnlyWhileItsOwnerIsPresentAndTheDamageIsTheOwners` | dormant at 13 tiles, logged out, on Felucca, dead; fires at 12; owner in `DamageEntries` with looting rights; the alarm fires with its owner 40 tiles off |
| `ChargesRunOutAndOnlyAHandReSetRearmsATrap` | bear trap 3 snaps then spent (art, 2-minute decay), a fourth troll walks over; double-click re-sets; exceptional 4; a spent gas trap refuses re-set until a Greater poison potion is dropped on it |
| `RemoveTrapSetsAndDisarmsAndGainsOnBoth` | the set rolls (0, 50), a hit (40, 120); real gains on the set and the disarm; the owner gets the kit back; a stranger salvages an exceptional bear trap |
| `BelowMasterABossWalksThroughAndAMastersTrapHoldsIt` | the Burrow Mother: no Den and Journeyman, nothing; Master, held; Journeyman's +1 trap out |
| `FlyersIncorporealAndSharpEyedCreaturesShrugTrapsOff` | an eagle over a snare; a wraith through a dart but not the gas; a Detect Hidden 200 troll spots caltrops (revealed, not fired) |
| `ATrapRefusesBadGround` | out of reach, the setter's own tile, Remove Trap too low, an empty gas kit, a guard zone, the fourth trap at RT 100 |
| `TheStacksHandOutPracticeNetsAndANettedRatCompletesTheLesson` | the region and its parent; two nets once; a practice net holds a Penny Rat and the key lands; no salvage; crumbles outside the Burrows |
| `TheRootdeepFloorTrapsAreStockClassesOffEveryHomeRangeAndPlacedOnce` | 8 rows, distinct tiles, each its class and in the Burrows, the home-range rule, placed once by the seeder |
| `TinkeringMakesTheEightKitsAtTheirGates` | each kit once in the Traps group, its gate to gate + 50 capped at 130; the bear trap's ingredients |
| `TheKitAndTheTrapSurviveARoundTrip` | a kit and a trap with every field non-default; the loaded trap is back in the registry, and leaves it on delete |

The two existing Rootdeep seeder facts (`RootdeepVaultVerification`, `RootdeepWayInVerification`) now also delete the
floor traps the seeder lays, so they leave no litter. Their assertions are unchanged.

**Red first** (`notes\cc-P275-tools\redbreak.py`, two deliberately broken builds of the builder stage, the focused
filter `DeployableTrapsVerification|Rootdeep`; the code was restored afterwards and checked byte for byte by
SHA-256 against the green copy):

| Run | Breaks | Result |
|---|---|---|
| red A | pets, summons and players count as targets; the presence range ignored; the set's gain window (min, min + 60); Master never trusted with bosses; guard zones allowed; the shackle's gate 100; a loaded trap not registered | 8 failed, each on its own assertion: the tinkering gate "Expected (110, 160)"; the pet held "Assert.False"; the guard-zone set "Assert.Null ... not null"; the round trip "Item not found in set"; presence "Expected 3"; the boss at Master "Expected True"; the Trammel player "Assert.False"; the gain window "Collections differ" |
| red B | the hand re-set does not restore charges; flyers trip ground traps; a netted rat completes nothing; T3 moved to 5165,1195; the owner not flagged | 5 targeted facts failed on their own assertions: re-set "Expected 3"; the lesson "Expected True"; "T3 Warren west descent: spikes is inside Great Burrow: rotworm's home range"; the flag "Filter not matched"; the eagle "Assert.False". A sixth, the Remove Trap fact, failed on a **test bug** (the netted troll still stood on the tile where the test then set the bear trap, and the tile rule rightly refused). The test was fixed (`dx: -1`); the green runs pass it |

(Red A ran before the gain cap below: its tinkering failure read "Expected (110, 160)"; the fact now expects
(110, 130), and the break, a gate of 100, still fails it.)

**Build record** (docker-build lock held throughout and released after; logs in the session scratchpad):

| Run | Result |
|---|---|
| builder, first compiles | three compile errors fixed: `TravelCheckType` needs `Server.Spells`; `Region` has no `CheckTravel` (the parent is cast to `BaseRegion`); an unassigned `out` in `Set`. Then one test compile error (a ref-struct enumerable `.ToList()`) |
| focused, first | 33 of 34 (the focused filter plus the craft registration and paging facts): the Remove Trap fact set a bear trap at Remove Trap 0.2, a test bug |
| red A, red B | above |
| `docker\uo\build.sh -t sl-modernuo:cc-P275`, cycle 1 | **2,037 tests, 1 failed:** `CraftCeilingsVerification.K1(Tinkering)` "Expected 130, Actual 160": the shackle kit taught Tinkering past the shard's stock top (deviation 9). No image |
| the same, cycle 2 | **green: 2,037 tests, 2,033 passed, 4 skipped, 0 failed**; image `c67d8425c736` carries VERSION 2026.10.21.16 and the new patch notes (read back from the image) |

## Deviations from the design, and decisions for Chase

1. **Payloads are loaded after the craft, not crafted in.** The design listed the poison potion, the explosion potion
   and the darts as recipe ingredients, and "arming a gas trap is a Poisoning use". Here the kit is crafted without
   them and the payload is dropped on it: the Poisoning check happens there, with the potion's window. This keeps one
   potion per set and lets a spent gas, blast or dart trap be reloaded in place. Same skills, same windows.
2. **Area traps fire on a creature entering their radius.** The design gave area traps an effect radius but no trigger
   rule. The keg is Impassable, so nothing could step on a blast trap. Single-target traps keep the RT-grown trigger
   (0, 1, 2).
3. **Not built in phase 1** (each small, none in the prompt's list):
   - the Apprentice "[set by <name>]" hover;
   - the gas cloud lingering 3 s;
   - the alarm's 10 s hue flash for the party;
   - the "losing its set" warning at 1 minute;
   - the creature that spots a trap stopping a tile short (it simply does not trigger it);
   - arming spoiled by damage (moving or dying spoils it).
4. **The caltrops' slow is a runtime change to the creature's `ActiveSpeed`, restored by a timer.** A world save in the
   8-second window would keep that one creature slow until it dies. Pinned has no unsaved speed modifier. Noted, not
   fixed.
5. **A spotting roll is remembered per trap and is not saved;** after a restart a creature may roll again.
6. **The design's home-range claim for T6 and T7 was wrong** (above). Harmless, because `GasTrap` hurts players only.
7. **Fidelity register:** P201 section 8 asks for one D-number with eight rows (the overseer edits `docs\`). Nothing in
   `docs\` was touched.
8. **The wiki page** "Deployable traps" (P201 section 8) is not written.
9. **The kits' Tinkering gains stop at 130, not gate + 50.** The design has the eight recipes carry Tinkering from 30 to
   160. The shard's craft ceilings (decided; `CraftCeilingsVerification` K1) stop every stock iron recipe at 130, and
   above that only the extended metals teach. A shackle kit teaching to 160 from iron broke that gate in cycle 1. So
   the blast kit gains 90 to 130 and the shackle 110 to 130 (`TinkeringCraftRegistrations.StockTop`). If the traps
   should carry Tinkering past 130, that is a decision against the ceilings design, not a number to change here.
10. **`tools\progress.py` was not run**, as recent prompts do not: its README block would conflict between Golems.

## For Chase

- **Setup:** rebuild the test shard from this branch (`sl-modernuo:cc-P275`). On the test shard first, run
  `[ClusterFSeedRootdeep dryrun`: it should report 8 floor traps to place (and the spawners and so on it already
  places). Then run `[ClusterFSeedRootdeep`.
- **Play tests:**
  1. The bear trap's art: `[add BearTrapKit`, set it, and see the jaws (0xB2C5) and, after a snap, shut (0xB2C3) in
     TazUO. If nothing draws, say so and the placeholder changes.
  2. A hidden set: hide, set a snare, and stay hidden.
  3. A net on a Penny Rat in The Stacks with a tutorial character: two practice nets on entry, the rat held, the
     Echo's "Held." line.
  4. The alarm's line names the region and coordinates.
  5. The Burrows floor traps after the seeder: the mushroom puffs by the decoy chests, the spike tile on each descent.
- **Art:** five requests are in this PC's `D:\UO\art\requests\`. If the console does not show them, run
  `notes\cc-P275-tools\file-art-requests.ps1` on the console PC.
- **To turn on Felucca trap PvP** later: `clusterf.traps.pvp` true in `modernuo.json`.

## Repo size

The largest new file is `DeployableTrapsVerification.cs` (about 30 KB). Nothing near 5 MB. Scratch (logs, the pinned
source extract, break originals) is in the session scratchpad, outside both repos.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -NoRefresh -NoArchive -CodeRepo
D:\ShatteredLegacy -DocsRepo D:\UO\shard-migration -Branch golem/Silver/P275` (this Golem's own clones). Code: 11 files
pending (CHANGELOG.md, VERSION, the seeder, the Tinkering registrations, the two Rootdeep tests, the four new trap
files, the new test). Docs: 3 (this note and the two files in `notes\cc-P275-tools\`). Neither is BLOCKED.

```
Repo Result
---- ------
code dry run
docs dry run
```

P275 DONE
