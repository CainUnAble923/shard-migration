# P407: review of the Eodon remainder port

Reviewed 2026-10-22. Notes only; no code changed. Reviewed the P198 implementation merged by P354, including the current files, the P354 merge diff, and both task notes. No Haven connection, build, test-shard action, or game test was performed.

## Findings

1. **bug** - `server/customizations/Services/Expansions/Time Of Legends/EodonSpawns.cs:147`: Every entry gets probability 100, but ServUO weights available entries by their maximum counts, so the wildlife mix changes, especially in Wildlife #1, #2, #3, and #4, whose total cap is below the sum of their entry limits. Set the probability in proportion to `entry.MaxCount` and add a regression assertion for the generated entry weights.

2. **bug** - `server/customizations/Services/Expansions/Time Of Legends/Mobiles/DragonTurtleHatchling.cs:65`: The hatchling takes an extra half-stat penalty and misses ServUO's additional first-tame skill reduction and cap changes; P198 records this deviation because the tame hook is supposedly unavailable, but our existing Pet Training code already provides it. Remove the substitute stat penalty and implement the source behavior through that hook, preserving its first-tame check by fixing the call order or explicitly passing first-tame state, with a test of actual tame results rather than the flag at test line 189.

3. **risk** - `server/tests/Services/TimeOfLegends/EodonRemainderVerification.cs:478`: The fire fact calls `DropFire` and `OnMoveOver` directly and checks expiration, so it does not verify the combat callback, its cooldown, or damage to a stationary target on the one-second timer. Add clock-driven assertions through `OnActionCombat` and a target standing on a fire tile, checking damage before expiration and no second drop before the cooldown.

4. **risk** - `server/tests/Services/TimeOfLegends/EodonRemainderVerification.cs:762`: The generator rerun checks spawner counts but never checks that their old wild creatures disappear, that refill ticks respect both caps, or that deletion and replacement work after reloading the collection. Add a lifecycle test retaining the first generation's creatures, checking their deletion on replacement, advancing refill ticks to the limits, and exercising replacement after a save and reload.

## Evidence behind the findings

- Finding 1: ServUO `Scripts/Services/XmlSpawner/XmlSpawner Core/XmlSpawner2.cs:8377` adds each available entry's `MaxCount` to its probability range, selects against that range at lines 8403-8408, and uses that selection for nonsequential spawning at line 8943. Pinned ModernUO `Projects/UOContent/Engines/Spawners/BaseSpawner.cs:867` instead sums the supplied `SpawnedProbability` values and selects against them at lines 886-893. For the first draw from an empty Wildlife #4 row (`EodonSpawns.cs:73`), a white tiger therefore has probability 1/8 here versus 1/25 in ServUO. The same entry table appears in Wildlife #1, #2, and #3. No reason for changing the weights appears in P198 or P354.
- Finding 2: ServUO `Scripts/Services/Expansions/Time Of Legends/Mobiles/DragonTurtleHatchling.cs:56` applies the first-tame skill and cap changes. Our `server/customizations/Services/Pet Training/BaseCreature.PetTraining.cs:152` declares the virtual hook, `PetTrainingHooks.cs:170` dispatches it, and `server/patches/AnimalTaming-pet-training.patch:27` wires it into taming. Pinned `Projects/UOContent/Skills/AnimalTaming.cs:428` halves stats for the substitute flag and adds the owner at line 440, before our patched hook call. ServUO `Scripts/Skills/AnimalTaming.cs:450` calls the creature hook before adding the owner. Copying the hatchling override alone would therefore leave its `Owners.Count == 0` guard ineffective on ordinary first tames.
- Finding 3: Test line 493 calls `DropFire`, line 502 directly invokes the movement handler, and line 511 advances beyond the fire lifetime. Production `Infernus.cs:64` owns the combat callback and cooldown; lines 132-155 own the ticking damage. The fact never asserts their damage or scheduling behavior.
- Finding 4: Test lines 762-767 count replacement items, and the individual-entry tests spawn once with a one-entry spawner. Pinned `BaseSpawner.cs:292` and `SpawnerEntry.cs:162` enforce total and per-entry caps, and `BaseSpawner.cs:1285` removes tracked spawns on deletion. These source checks support the current implementation; the finding is missing integration coverage, not a confirmed population leak.

## Other results

No additional unexplained creature stat, loot-table, or item behavior mismatch was found in the reviewed files. The source's unusual DesertScorpion damage assignments and the default four-card selection were preserved. P198 explains the omitted masteries, aggressor-only behavior without Myrmidex, silent spell words, Barako spawn height conversion, vine placement changes, and deletion of loaded fire.

No incompatible serialization-version change was found. These types first entered this ModernUO shard in P198 with generated version 0; P354 did not change their persisted fields, version attributes, or inheritance. Older ServUO versions are not an existing shard-save format. Current-format round trips are covered by the supplied tests; loading an actual older shard save was unverified in this review.

No uncapped population growth was found on the reviewed command paths. `EodonGeneration.Run` deletes its tagged prior generation before replacing it, the spawners have total and per-entry limits, and each fire item expires after 30-40 seconds. Fire can overlap between drops, but its lifetime bounds that overlap. Actual runtime population limits and post-reload cleanup remain unverified here.

A read-only comparison of every generated spawn row against `D:/UO/ServUO-pub57/Spawns/Eodon.xml` checked centers, rectangles, ranges, delays, retained types, tribe arguments, and per-entry limits. The reviewed table has 46 rows requesting 345 creatures. The desert reductions, omitted Myrmidex and quest entries, and Barako Z conversion match P198's stated choices; the only argument differences were enum letter casing. The complete row list is `EodonSpawns.Definitions`, `EodonSpawns.cs:65`.

## Reviewed file inventory

Paths below are relative to the code work copy. The Eodon prefix is `server/customizations/Services/Expansions/Time Of Legends/`.

| Path | Review |
|---|---|
| Eodon prefix + `Mobiles/Anchisaur.cs` | Compared with the same ServUO script path |
| Eodon prefix + `Mobiles/Gallusaurus.cs` | Same |
| Eodon prefix + `Mobiles/DesertScorpion.cs` | Same |
| Eodon prefix + `Mobiles/GreaterPhoenix.cs` | Same |
| Eodon prefix + `Mobiles/Infernus.cs` | Same, including nested fire and its timer |
| Eodon prefix + `Mobiles/DragonTurtleHatchling.cs` | Same, plus both taming pipelines |
| Eodon prefix + `Mobiles/BritannianInfantry.cs` | Same, plus pinned healing |
| Eodon prefix + `Mobiles/EodonTribesman.cs` | Same, including base and all tribe/role branches |
| Eodon prefix + `Items/DragonTurtleScute.cs` | Compared with ServUO `Items/Resources.cs` in the same Eodon directory |
| Eodon prefix + `Items/CardOfSemidar.cs` | Compared with the same ServUO script path |
| Eodon prefix + `Items/ClimbingVine.cs` | Same, including source startup placement |
| Eodon prefix + `EodonSpawns.cs` | Compared with ServUO `Spawns/Eodon.xml` and both spawner implementations |
| Eodon prefix + `EodonGeneration.cs` | Compared with ServUO `Scripts/Services/Expansions/TimeOfLegends.cs` and the collection implementation |
| `server/customizations/Mobiles/NPCs/WanderingShaman.cs` | Compared with the same ServUO script path and pinned parent |
| `server/customizations/Services/Pet Training/PetTrainingHelper.cs` | P198's comment change and hatchling definition resolution |
| `server/tests/Services/PetTraining/PetTrainingVerification.cs` | P198's table-test change |
| `server/tests/Services/TimeOfLegends/EodonRemainderVerification.cs` | Read every fact, including round trips and generation checks |

P354 introduced no server patch file. Also read the relevant existing taming and ability-hook patches, Pet Training hook/profile implementations, `WeakEntityCollection.cs`, and pinned spawner/creature implementations to resolve behavior outside the leaf files.

Reference heads: ModernUO `d4531cd94b739613155225c234900de9f47d2c88`, matching `docker/uo/Dockerfile`; ServUO pub57 `d76bf4443cf76d081ddaf8f57c87ff33749256af`. Reviewed code HEAD `1ecd9f3`; P354 merge `b240bb4`.

## Verification and limits

No tests were added or run, as requested for this notes-only review. The P198/P354 green and red-test claims were read as historical reports, not rerun or independently certified. Findings above come from source comparison and call-order inspection, not new runtime reproduction. No live data or `server/uo/` build tree was read.

Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing at these work copies. It completed, but `build()` writes `tools/progress.json` before the dry-run return (`tools/progress.py:722,737`), contrary to its help text. Restored that generated file to its initially clean HEAD content; only this review note remains changed.

P407 DONE
