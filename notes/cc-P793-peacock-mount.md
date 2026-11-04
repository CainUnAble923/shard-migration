# cc-P793: tamable peacock mount

Iron Golem, 2026-11-04. Code copy `D:\UO\golems\Iron\ShatteredLegacy` and docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P793`, not committed (the Golem commits). Nothing deployed, packaged or published. The shared Test
Shard was not touched; the play was on a private proof shard, 127.0.0.1:2596. Main only, not the isle release.

## In plain words

- **Players can tame and ride a peacock.** It is a new low-level mount with an ostard's numbers: Animal Taming 29.1, one
  follower slot, eats fruit and grain. It uses art already in the client, and it draws properly under a rider.
- **Where to find them:** three peacocks each on two open meadows north of Trinsic. They appear by themselves on an existing
  world after a restart, with nothing for staff to run.
- **It works with the pet leash:** the leash shrinks a peacock into its own peacock figurine.
- **Peacocks cannot be trained with Pet Training**, unlike ostards. ServUO's training table is kept exact, and a new row
  broke that rule, so I left it out.
- **For you:** one thing needs a decision, and it is not about peacocks. While testing I found that the Butcher's Eye imbue
  should crash its own rare drop every time it comes up (details under "Found on the way"). Do you want a fix queued? And
  say if you want peacocks trainable.

## The parts

| # | Part | What was done |
|---|---|---|
| 1 | Check first | **Done.** Pinned's `bodyTable.cfg` has no row for 1440, so it was typed Empty. The client types it ANIMAL (`mobtypes.txt:1300`) and draws it through `Bodyconv.def:733`. TazUO's `Game/Data/Mounts.cs` maps 0x3ECF to 0x05A0 (1440), height 9, and 0x3ECF's tiledata animation is 0, so that mapping stands. Confirmed in game, see the shots. |
| 2 | The creature | **Done.** `server/customizations/Mobiles/Mounts/Peacock.cs`: `BaseMount`, body 1440, mount item 0x3ECF, generated serialization, no saved fields of its own. No loot. |
| 3 | Body type | **Done.** A row in `ShardBodyTypes.Entries` (1440, Animal), the shard's route for a body pinned does not type: pinned's `Distribution/Data` stays pinned. A fact checks `CanOpenDoors` is false. |
| 4 | Leash art | **Done, it was missing.** Pinned's `shrink.json` stops short of 1440 (highest row 0x0592). `server/data/shrink.json` holds the one row, 0x05A0 to 0xA0C0. `ShrinkTable-shard-rows.patch` reads it on top of pinned's, so Tracking and a pet's trade get the art as well as the leash. New `COPY` line in the Dockerfile and `apply_patch` line in `apply-patches.sh`. |
| 5 | Spawns | **Done.** Two meadows on Trammel, a spawner each: 3 peacocks, home range 12, every 10 to 20 minutes. |
| 6 | Config | **Done.** `Configuration/peacock.json` (`PeacockTable.cs`), written with the defaults on first start. A bad file is refused whole and the table in force stays. `[Peacock status\|reload\|seed [dryrun]`. |
| 7 | Existing worlds | **Done.** Seeded on the tick after every world load, a spawner per meadow only if none is there. |

### The meadows

Found on the Siege of Sosaria land by `notes\cc-P793-tools\meadows.py` and `meadows2.py`: open grass, flat, no static in the
16 by 16 block, outside every region rectangle and fence by 10 tiles, and on the mainland reachable on foot from a Trinsic
region tile (`checkspots.py`, 881 steps).

| Meadow | Spot | Checked |
|---|---|---|
| Trinsic road meadow | 1986, 2244, 0 | 625 of 625 tiles of the home range standable; played in TazUO |
| West meadow | 1800, 2172, 8 | same mainland walk, 0 statics in its 16 by 16 block; seeded in the shard log, **not visited in the client** |

The first candidate, 1878, 2076, was rejected: open, but a pocket of only 8,016 reachable tiles.

## Tests

`server/tests/Mobiles/Mounts/PeacockVerification.cs`, 12 facts: body, item, taming numbers and food against a real
`DesertOstard`; a real tame through Animal Taming's own target and timer; owner rides and dismounts, a stranger cannot;
save and load tamed and ridden; the leash's figurine, with pinned's rows unchanged; the seed, a second seed and a dry run;
no meadow under a fence; the table's numbers reach new peacocks and not saved ones; a bad file refused; off seeds nothing;
no loot.

**Seen failing first** (P764's method, each rule undone in a mutant, the facts run in the builder image:
`notes\cc-P793-tools\mutate793.py`, `probe793.sh`, `run-mutants.sh`, `mutant-logs\`, `mutant-summary.txt`). The unchanged code
passes 12 of 12. All 15 mutants go red, and every fact goes red in at least one:

| Mutant | Undoes | Fails |
|---|---|---|
| nobodyrow | the body type | ItIsAnAnimal... |
| wrongitem | mount item 0x3ECF | ItIsAnAnimal..., ItsOwnerRides..., ItRoundTrips... |
| notame | tamable | ARealTame..., ItIsAnAnimal... |
| noride | riding | ItsOwnerRides..., ItRoundTrips... |
| food | fruit and grain | ItIsAnAnimal... |
| nocfg | the table's tame skill | NewPeacocksTakeTheTablesNumbers... |
| nosave | saving | ItRoundTrips... |
| loot | no loot | ItCarriesNoLoot, TheLeashShrinks... (a pack with gold in it) |
| noshrink | the figurine row | TheLeashShrinks... |
| noidem | the seed's check for what is there | TheSeedGivesEachMeadowOneSpawner... |
| dryplaces | dry run | ADryRunPlacesNothing |
| offignored | enabled | WithTheTableOffNothingIsSeeded |
| nohome | the home range | TheSeedGivesEachMeadowOneSpawner... |
| novalidate | the slot check | TheShippedDefaultsRoundTrip... |
| fenced | a meadow under a fence | NoMeadowLiesUnderAFence |

`nosave` and `noshrink` survived the first pass, because the mutants were bad: an `AfterDeserialization` hook does not run on a
direct round trip, and the tests read `shrink.json` from beside their own build. Both were remade and went red
(`mutant-rerun.txt`); `mutant-summary.txt` still shows the first pass for those two.

**Gated build** (`docker\uo\build.sh -t sl-modernuo:cc-p793`, logs in `notes\cc-P793-tools\`, UTF-16):

| Run | Result | Cause |
|---|---|---|
| 1 | compile error | my test used LINQ on `GetItemsInRange` |
| 2 | 3 failures | see the training row below; `TreasureMapLevel` is -1 for none, my test said 0 |
| 3 | 2 failures | the tamer was killed mid-tame (below); Butcher's Eye (below) |
| **4** | **green: `gated-build.log`** | 3,053 tests: 3,047 passed, 6 skipped, 0 failed. `EXIT=0` |

**Run 3's tame failure was not the peacock.** It passed 12 of 12 alone and failed in 5 of 12 full-suite probe runs (the suite's run order varies). A logged
run showed the tamer dead, killed by a chest mimic standing on (1000,1000) in Ter Mur, left there by some other fact, with the
peacock's combatant empty. I did not find which fact leaves it. The Peacock facts now have their own spot, 1793, 1179
(`suite-flake-evidence.txt`).

## TazUO shots

`notes\cc-P793-shots\`, one real TazUO run on the private proof shard (`sl-modernuo:cc-p793`, 127.0.0.1:2596, the test-shard lock
held). The world is a copy of the bot world, so it is an existing world with no peacocks in it: `shard.log` shows
`[Peacock] placed a peacock spawner` for both meadows, `Peacock meadows: 2 placed, 0 already there, of 2.` The rig is P764's,
copied into `notes\cc-P793-tools\`, with `Shots793.py`. On that private copy only, `clusterf.tutorial.islandGate` is off, so a new
character can leave the isle.

All 10 checks in `walk.log` pass. Runs 1 and 2 failed the two riding checks, and both times the script was at fault: it picked a
wild peacock, then stood 7 tiles from the tamed one ("That is too far away to ride").

- `1-wild-peacock.jpg`: **three wild peacocks** on the meadow, in different facings and poses.
- `2-tamed.jpg`, `3-walking-a/b/c.jpg`: tamed, then a burst just after "all follow me". These show a peacock beside the character, not the
  pet following: the character had not started moving in the burst, and in the run before, the tamed one was 7 tiles behind.
- `4-ridden.jpg`, `5-ridden-walking-a/b/c.jpg`: **the rider on the peacock**, legs and tail drawn under him; mount layer 16079
  (0x3ECF). The pose changes as it walks.
- `6-dismounted.jpg`: back on the ground.
- `7-figurine.jpg`: **the peacock figurine** in the backpack (fourth row) and the line "a peacock shrinks into a figurine".

The blue skill lines down the left are the proof shard's test-center mode on a new admin character.

**Not proved:**
- **Fight animations** (attack and hurt). P59 left them unverified and nothing here fought. The client has attack frames for 1440.
- **Idle and feed animations in the client.** The body is typed Animal, which is what allows them, and the shots do not show one.
- **A pet following its owner in the client.** Following is stock pet behaviour and no part of this task; the shots do not show it.
- **The real save and load** was the facts' round trip, not a restart with a ridden peacock.
- **The ridden walk animation** is judged by eye from the stills. `framediff.py`'s counts cannot separate it from the camera moving
  and wild birds wandering.

## Found on the way

**Butcher's Eye's rare part always throws (not fixed: outside this prompt).** `ClusterFImbueEffects.ButcherOn` (line 341) calls
`Activator.CreateInstance(type)` on a part from `ButchersEyeRareParts`. That needs a parameterless constructor. All 13 parts in
the list have only `(int amount = 1)` (counted, one by one). So each time the 2% rare roll hits, it should throw
`MissingMethodException` during the kill instead of dropping the part.
- Seen once for real: `DeathHooksVerification.AKilledNonBondedPetPaysNoImbueKillEffect`, run 3, on `SilverSnakeSkin`. The other 12
  were not run; the claim for them rests on the matching constructor.
- It is also why that fact fails at random: only when the 2% roll hits.
- The fix looks like one line, passing the amount: `Activator.CreateInstance(type, 1)`. Unverified, I did not try it.
- Live effect not checked: whether a player sees anything, or what the throw skips. Worth a look on Haven's logs by someone allowed there.

**Another random failure:** `EodonRemainderVerification.TheInfernusDropsFireFromCombat...` failed once in 12 full-suite probe
runs. It is in code I did not touch; cause not looked into.

## Deviations and decisions for Chase

- **Trainable or not.** I first added a Pet Training row copied from the ostards. It broke `TheTablesAreServUOs` (the table is pinned
  to ServUO's 137 rows), and its 1-to-3 slot range clamped `controlSlots` in the config. I removed it instead of changing that fact.
  Peacocks are untrainable, as a tamable with no row is (the Scaled Swamp Dragon too), and a fact says so. To make them trainable,
  override `TrainingDefinition` on the creature, as `CrimsonDrake.cs:103` does.
- **Moved meadows:** changing a spot in `peacock.json` adds a spawner there and leaves the old one in the world for staff to delete.
- **`Eowmu`:** ServUO's `Eowmu` uses the same body and mount item. It is not on the shard. A later port would look like the peacock.
- **Sound:** it uses the ostard's 0x270, as the reference did. I did not look for a bird sound.
- **Fidelity:** this is original content, not an OSI creature. `AGENTS.md` wants deviations recorded in
  `docs\fidelity-principle.md`, and the Golem rule forbids editing `docs\`, so it is recorded here.
- **Touches:** the prompt names server and server-patches. The new data file also needed `docker\uo\Dockerfile`.
- **The third-party code** was read as reference only, none copied. Its numbers are stock `DesertOstard` numbers from pinned. WiKKiD is
  credited in the CHANGELOG and in `Peacock.cs`. It has no stated terms.

## CHANGELOG and VERSION

`2026.11.04`, the first of the day here. Another Golem may also take it, so the integrator may renumber.
- **Added:** the peacock (crediting WiKKiD).
- **Staff:** `Configuration/peacock.json` and `[Peacock`.

## Files

- **ShatteredLegacy:**
  - new: `server/customizations/Mobiles/Mounts/Peacock.cs`, `PeacockTable.cs`, `PeacockSystem.cs`, `server/data/shrink.json`,
    `server/patches/ShrinkTable-shard-rows.patch` (checked with `patch --fuzz=0`), `server/tests/Mobiles/Mounts/PeacockVerification.cs`;
  - changed: `server/customizations/Mobiles/Evo/ShardBodyTypes.cs`, `docker/uo/Dockerfile`, `docker/uo/apply-patches.sh`,
    `CHANGELOG.md`, `VERSION`.
- **shard-migration:** this file, `notes\cc-P793-tools\`, `notes\cc-P793-shots\`.

P793 DONE
