# P671: review of P661, the Fold and its copy maps

Reviewed October 26, 2026. Notes only. No code changed.

Three findings: one High and two Medium. The persistence findings concern error handling when map registration is wrong, not a collision or missing map in today's configuration. The travel finding matters before players are routed to the Fold.

## Scope and evidence

Code work copy: `18fdae2`, including P661 implementation commit `6b7efbabb5ac4914c4dd44aecbb9397782fecad4`. Notes work copy: `081e4fcece8d725bb2e90460ded1b7097d9b25ab`. Pinned source: `D:\UO\ModernUO-pinned`, clean at `d4531cd94b739613155225c234900de9f47d2c88`, matching `docker/uo/Dockerfile:3`.

I read both working agreements, the direction decision, the task list, both `cc-P661-*.md` notes, and P481 design sections 3.1, 11 and 12. I reviewed every code file P661 lists:

- `server/customizations/Fold/FoldMaps.cs`
- `server/customizations/Fold/FoldRegions.cs`
- `server/customizations/Fold/FoldCommands.cs`
- `server/customizations/Fold/FoldSavedMapCheck.cs`
- `server/customizations/ClusterFAnkhs.cs`
- `server/tests/Regions/FoldVerification.cs`
- `CHANGELOG.md` and `VERSION`

Shard references below are relative to the code work copy. Pinned references are relative to `D:\UO\ModernUO-pinned`. Findings are conclusions from the cited source paths, not runtime reproductions. No build or test lane was run or added for this review.

I checked P605's design review and its Codex review, P481's Codex review, and P661's Codex review for duplicates. P661's review had no findings. I do not repeat P481's offline reservation and party-vision findings, or P605's existing pet-transfer, tutorial gate, scene recovery, and visibility findings. The Help routes below are specific paths not identified in those reviews.

## Findings

### 1. High: stop startup when another world owns a reserved index

**Location:** `server/customizations/Fold/FoldMaps.cs:85-92`; related acceptance check at `:79-82` and accessors at `:53-62`.

**Trigger and result:** Add a map definition for a different world at index 40, then start with a save containing Fold-copy-8 entities. `MapLoader.Configure` registers the JSON map first. `FoldMaps.Configure` logs the conflict and continues. World loading then resolves every saved map byte 40 to the conflicting world. Players' return maps, creatures, and dropped items all resolve to that world. `FoldSavedMapCheck` sees non-null maps and cannot report the mistake. `FoldMaps.Copy(8)` also returns the conflicting map, and `IsFold` classifies it as a Fold copy by index alone.

The comment that this refusal avoids moving contents is therefore incorrect: it avoids replacing the JSON entry, but allows saved Fold contents to load into it. An existing map with the expected name and client ID also passes without checking its file index, dimensions, or rules.

**Evidence:** pinned `Projects/Server/Maps/MapLoader.cs:103-118` installs definitions into the same global table; `Projects/Server/Main.cs:667-673` loads the world after configuration; `Projects/Server/Serialization/IGenericReader.cs:120` resolves saved maps solely through `Map.Maps[ReadByte()]`. Pinned `Mobile.cs:6467,6492` and `Item.cs:2976` consume that result. Those last two files are under `Projects/Server/Mobiles/` and `Projects/Server/Items/` respectively.

**Fix:** Validate all reserved slots before world load and fail startup on an incompatible occupant. Make repeat configuration recognize maps this registration owns, or validate their complete definition, rather than accepting a matching label and client ID. Do not overwrite the conflicting map and continue. A follow-up test should put an incompatible map at 40 and prove startup refuses before loading any saved entity.

**Current exposure:** No conflict found in pinned `Distribution/Data/map-definitions.json` or the canonical customization registrations. This is a conditional save-safety defect in the newly added collision branch.

### 2. Medium: missing-map recovery loses the original index on the next save

**Location:** `server/customizations/Fold/FoldSavedMapCheck.cs:67-78`; the recovery promise is in `:12-14`.

**Trigger and result:** Load an item or creature saved on 40 while that index is unregistered. The reader returns null. `Run` logs the entity and leaves it in the world dictionaries with a null map. If the server saves before registration is repaired, the entity's map is written as byte 255. Registering 40 on a later start cannot restore it because the latest save no longer says 40. The entity remains outside the world. Recovering its original placement requires an older save or independent records.

Nothing is explicitly deleted, but retaining the entity is insufficient to support the header's claim that registering the index again brings it back on the next start. P661's missing-index fact checks only the first load and `Deleted == false`, so it does not exercise this failure.

**Evidence:** pinned `Projects/Server/Serialization/BufferWriter.cs:468` writes a null map as `0xFF`. `Projects/Server/Items/Item.cs:977-980,1135-1138` includes the map field for a null map, and `Projects/Server/Mobiles/Mobile.cs:2441` writes the creature's map. `Projects/Server/Serialization/GenericEntityPersistence.cs:335-354` schedules entities for saving without excluding null-map entities. `FoldSavedMapCheck` preserves no original index.

**Fix:** Treat unresolved saved maps as a startup failure before normal saves can replace the recoverable snapshot, or preserve the original index in a recovery mechanism and restore it explicitly. Clarify that any interim recovery must use the original save. A follow-up should exercise load with 40 absent, save, restore 40, then reload both an item and a creature. It must either recover their original placement or prove the bad save was refused.

### 3. Medium: Help transport bypasses the Fold's exit rules

**Location:** `server/customizations/Fold/FoldRegions.cs:39-58`, with `server/customizations/Tutorial/TutorialIslandGate.cs:24-38` providing no source-side restriction on Fold maps.

**Trigger and result:** A non-staff player standing on a Fold map can use Help's stuck transport, subject to its ordinary use and combat checks. `FoldRegion` inherits `CanUseStuckMenu == true`. The stuck timer chooses Trammel, or Felucca for a murderer, and calls `MoveToWorld` directly. A Young player also has Help's Young-player transport, which directly moves them to New Haven. Neither route calls `SpellHelper.CheckTravel`. The existing tutorial movement guard applies only when the source is Haven or Rootdeep, so it allows these moves from the Fold.

This leaves a direct player-controlled exit alongside the intended tutorial gate. Once trainees are placed here, it can bypass the final travel lesson and the copy manager's intended exit handling. Young-player transport also does not transfer pets. This is separate from the already documented Haven-to-Fold entry restriction.

**Evidence:** pinned `Projects/Server/Regions/Region.cs:766` permits the stuck menu by default; `Projects/UOContent/Engines/Help/HelpGump.cs:308-316` opens it; `Projects/UOContent/Engines/Help/StuckMenu.cs:291-307` picks the destination and moves directly. `HelpGump.cs:355-370` handles Young-player transport without consulting the travel region. The shard's `PlayerMobile-tutorial-island-gate.patch` delegates direct moves to `TutorialIslandGate.CanMove`, whose island predicate excludes maps 32 to 48.

**Fix:** Give Help recovery an explicit Fold policy before opening the isle. Refuse the standard stuck menu or provide recovery to a safe point in the trainee's copy. Route Young-player transport through the same approved recovery or exit policy. A `CanUseStuckMenu` override alone does not cover the Young button. Follow-up checks should exercise both actual Help responses for a loop-0 trainee on 32 and a private copy, including the pet and reservation result.

## Other requested checks

**Normal save/load on 32 to 48:** The priority-3 registration runs after priority-2 JSON maps and before world load. The map index is distinct from client ID and file index. The normal item and mobile readers resolve the same registered map object, so there is no special six-facet serialization limit here. Player load preserves the destination in `LogoutMap`; actual login restores `Map` and `Location` at pinned `Projects/Server/Mobiles/Mobile.cs:1320-1324`. P661 tests one player on 40 and records a scratch restart on 32 and 33. Successful item, container, pet, and offline-player round trips across every reserved index were not independently run here.

**Housing, spells, and child regions:** With the current default regions, `HousePlacement.Check` rejects Fold housing through `IsPartOf<NoHousingRegion>` at pinned `Projects/UOContent/Multis/Houses/HousePlacement.cs:76-79`. Recall, Mark, and Gate Travel pass the caster through `SpellHelper.CheckTravel`, which checks the current and destination regions at `Projects/UOContent/Spells/Base/SpellHelper.cs:633-645`. The P661 region overrides therefore reach those spells. Parenting later zone regions to the Fold default preserves inherited travel, housing ancestry, and light behavior. A parentless registered region would replace that coverage, as P661 already records. I found no additional housing defect in the current implementation.

**Mirror region:** Its exclusive rectangle end correctly covers x 6160 through 6639 and y 1832 through 2279, through the full normal Z range. Deferring the move avoids moving recursively during a region change, and `SendHome` rechecks map and position before acting. A saved player parked on Internal enters the mirror when login restores their Trammel position, so `OnEnter` can schedule recovery then. Staff remain exempt. The stock pet helper's range and order limits still apply; that limitation was already identified by P605 and is not a new finding here. Mirror recovery with a real login and pets was not rerun.

**Memory:** Each map owns separate sector storage and lazily creates a separate `TileMatrix`; matrices sharing file index 1 share cached block references, not one entire matrix or one set of streams. See pinned `Projects/Server/Maps/Map.cs:73-105` and `Projects/Server/TileMatrix/TileMatrix.cs:71-181,221-332`. The default-region approach avoids registering map-wide sector coverage. The ankh survey's Fold skip avoids repeated static-file scans while retaining its later item scan. I found no additional memory defect in this fixed pool. P661's reported memory and first-use timings are test-host measurements, not independently reproduced live budgets. No occupied-pool load test was performed here.

## Validation and limits

No Haven connection, deployment, Docker operation, account change, code edit, new test, branch switch, commit, or push. Local PowerShell commands ran in Windows PowerShell 5.1 (`5.1.26100.9711`). Runtime reproduction of the three findings remains unverified; the report supplies source paths, triggers, and follow-up acceptance checks.

The required progress reporter completed with both work-copy paths set and `--dry-run`. As in P605, I intercepted its unconditional `tools/progress.json` write in memory, preserving this task's notes-only scope. It reported shard version `2026.10.26.11`; no progress, README, or dashboard artifact was changed. The first attempt to print the captured report hit the console's character encoding limit; printing an ASCII-safe rendering completed successfully.

P671 DONE
