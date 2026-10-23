# P463: review of P281 guild hall placement

Reviewed October 23, 2026. Review notes only; no code changes.

## Findings

1. **bug**, `server/customizations/ClusterFGuildHallPlacement.cs:290`: `clear warriors` deletes a preexisting `WarriorGuildmaster` within one tile of the post even if this command never placed that NPC or hall, because `FindNpc` checks only type and horizontal proximity before `Clear` deletes its result; an NPC on another floor also qualifies. Persist the serial of each NPC this command creates and clear only those owned NPCs, with regression cases for a preexisting NPC at the post, one on another floor, and an owned NPC moved away from its post.

2. **bug**, `server/customizations/ClusterFGuildHallPlacement.cs:180`: If an existing new hall's closed front doors have missing or changed links, `place smithing dryrun` or `place merchants dryrun` changes those links through the unconditional assignments at lines 182 and 183. Guard link changes with `!dryRun` and extend `server/tests/Misc/GuildHallPlacementVerification.cs:218` to assert that a dry run preserves existing door properties, rather than checking only item and mobile counts in an empty hall.

3. **risk**, `server/tests/Misc/GuildHallPlacementVerification.cs:54`: `TheTableIsTheDesignFile` compares the server table with `GuildHallPlacementDesignCopy.Json`, so editing `design/guild-halls/halls.json` without regenerating either C# file leaves the test green and runs the old placement; the build scripts do not run `gen.py --verify`. Gate the build on the real design file matching the generated data, or copy the actual JSON into the test output and compare it directly, with an unregenerated design edit as the failing case.

These are source-backed findings, not runtime reproductions. The current design and generated files match. Finding 3 is the same test pattern identified for the separate decor templates in P419, now identified in P281's placement test.

## Placement checks

No additional road blockage, stock decoration collision, nearby spawner conflict, or stranded travel stop was found by P281's file-based checker. Ran its existing checks for every entry in this work copy's `design/guild-halls/halls.json`, using its current `GuildHallDecorTemplates.cs`; all passed. The checker was imported with `CODE`, `PLAN`, and `TEMPLATES` redirected in memory to this work copy, and given explicit hall keys so it did not rewrite `check.out.txt`.

For the Smiths' Serpent's Hold building and the Merchants' Magincia building, also compared outdoor reachability before and after blocking their multi footprints in the existing walk model. Neither disconnected any additional outdoor tile outside its footprint. Both sites fall inside pinned Trammel town regions (`Distribution/Data/regions.json:2184` and `:2316`); `TownRegion.cs:5` inherits `GuardedRegion`, whose `AllowHousing` returns false at `GuardedRegion.cs:151`.

Inspected pinned teleporter endpoints near the halls. No endpoint coincides with the new building footprints, NPC posts, or decor placements. P281's Artificers' arc orb gate is decorative `GuildHallDecor`, not a functional teleporter. No additional door or teleporter stranding defect was established.

Unverified: current world saves, player houses or hand-placed items in those saves, roaming spawn positions, actual player movement through doors and stairs, recall execution, and persistence through a real server restart. The offline walk model omits the engine's diagonal corner rules and simplifies stairs, and it does not model the new buildings' interiors. Passing it does not prove player traversal. No client, shard, Haven, or container connection was made.

## Review scope and verification

Read both work copies' `AGENTS.md`, the direction decision and task list, `notes/cc-P281-guild-halls-placement.md`, and its adjacent `cc-P281-guild-halls-placement-codex-review.md`. The earlier P281 findings about open-door duplication, replacement stock signs after SignGen, and the generator checking a different repository are excluded here.

Reviewed P281's code and data: `server/customizations/ClusterFGuildHallPlacement.cs`, `ClusterFGuildHallPlacementData.cs`, `design/guild-halls/halls.json`, `server/tests/Misc/GuildHallPlacementVerification.cs`, and `GuildHallPlacementDesignCopy.cs`. Traced related behavior through `ClusterFGuildHallSeeder.cs`, `GuildHallDecor/GuildHallDecorSeeder.cs`, `GuildHallDecorTemplates.cs`, and the build scripts. Read the map checker, walk model, map loader, multi reader, generator, and P281's recorded check and proof output. Consulted P419's decor review to distinguish existing decor concerns from this placement review.

Verified engine behavior against read-only `D:/UO/ModernUO-pinned` at `d4531cd94b739613155225c234900de9f47d2c88`: `Map.MobileEnumerator.cs:55` discards Z for range lookup; `BaseDoor.cs:62` stores the mutable link; `BaseDoor.Use` consumes it; `Houses.cs:43` defines the Guild House layout. Also checked `BaseMulti.cs`, town and guarded region classes, and pinned spawn, decoration, region, and teleporter data.

Ran `python -B -P notes/cc-P281-tools/gen.py <this code work copy> --verify`: generated files match the design file. Python probes used `-B` to avoid writing bytecode. No new tests were written, no code was changed, and no server build or C# test suite was run, consistent with this prompt's lane tests being none. Progress artifacts were not refreshed because this task requests only the review note and changes no content coverage.

P463 DONE
