# P584: review of the P459 guild hall decor seeder fix

Reviewed October 25, 2026. Notes only. P459 commit `66898a0762ff0f5d0320b477318a84f56e916e9b` is an ancestor of local code `main`; the reviewed code HEAD and main both resolve to `8b0ccb80c00aedd9898be6f453d419b0a2119f2c`.

## Additional findings

1. **bug**, `server/customizations/GuildHallDecor/GuildHallDecorArt.cs:151` (also :162, :169, :182, :194): The tower entrance pieces still have Wall and Impassable without Door, so ghosts cannot pass through a closed entrance, and ordinary item use refuses their double-click because they are dead; a player who dies inside a tower can lose the doorway as an exit after it closes. Add the Door flag consistently to the generator, server catalog, and package records, and cover dead-player passage with the same movement check used for living players.

2. **bug**, `server/customizations/GuildHallDecor/GuildHallDecorSeeder.cs:490`: `GetMobilesAt(Location)` ignores elevation, and this loop treats every returned mobile as an obstruction, so a ghost, hidden staff member, or mobile on another floor at the doorway's X/Y can hold the door open indefinitely. Apply the stock door's alive, visibility, and vertical-overlap checks, and extend the closing test with those nonblocking cases while retaining the living-player obstruction case.

3. **bug**, `server/customizations/GuildHallDecor/GuildHallDecorSeeder.cs:131`: The same-set overlap guard compares only X/Y, so a vat anchored at `(1300,1300,0)` prevents another at `(1300,1300,40)` even though the vat pieces are only eight units high and the placements do not intersect. Compare vertical volumes as well as tile coordinates, and add a separated-floor placement beside the shifted-anchor regression test at `server/tests/Misc/GuildHallDecorVerification.cs:355`.

4. **risk**, `server/tests/Misc/GuildHallDecorVerification.cs:296` and :413: Persistence coverage round-trips only a closed, current-version door and simulates a legacy item by assigning a null hash, so it never exercises either restoring a saved-open door or decoding the actual version-0 format. Add a saved-open reload case that runs the deserialization hook and verifies closed art, visibility, and subsequent opening, plus a version-0 payload case that verifies the saved ownership fields and the clear-first refusal.

These are source-backed review findings, not runtime reproductions. None repeats the findings in the adjacent P459 review: open tower door preflight, hall placement success reporting and dry runs, stock doorway elevation checks, removed or renamed groups, and name-only template hashes remain outside this report.

## Evidence and verification

Read both work copies' `AGENTS.md`, the direction decision and task list, `notes/cc-P459-hall-decor-seeder.md`, and `notes/cc-P459-fix-guild-hall-decor-seeder-refuse-overlapping-codex-review.md`. Also consulted the P419 and P463 reviews and the P516 design comparison to distinguish earlier findings and accepted tower limitations.

Reviewed P459's seeder, generated templates, design JSON, migration JSON, hall placement integration, Dockerfile, changelog/version diff, `server/tests/Misc/GuildHallDecorVerification.cs`, and `server/tests/Route/TestTileRows.cs`. Traced related behavior through `GuildHallDecorArt.cs`, the hall placement tests, `TestHostTileData.cs`, and `player-package/vendor/shattered-legacy-art/records.json`. Read the generator changes in `notes/cc-P265-tools/decor.py`, the render helper in `notes/cc-P459-tools/render_tower.py`, and inspected `notes/cc-P459-tower-large.png`.

Engine evidence is from read-only `D:/UO/ModernUO-pinned`, verified at `d4531cd94b739613155225c234900de9f47d2c88`:

- `Projects/UOContent/Engines/Pathing/Movement.cs:268` enables ignoring doors for dead mobiles, but :213 recognizes Door tile flags or specific stock art IDs, not the custom tower IDs. `Projects/Server/Mobiles/Mobile.cs:4968` routes dead item use to `OnDoubleClickDead`; `Projects/Server/Items/Item.cs:4462` supplies the refusal inherited by the tower door.
- `Projects/Server/Maps/Map.MobileEnumerator.cs:34` converts the Point3D lookup to Point2D. `Projects/UOContent/Items/Construction/Doors/BaseDoor.cs:287` filters closing obstructions by life, visibility, and overlapping elevation; the new custom door does not.
- Vat records at `server/customizations/GuildHallDecor/GuildHallDecorArt.cs:18` through :26 have height 8. The new overlap guard discards Z before its later collision preflight can consider those heights.

Read-only data comparisons confirmed that every generated row matches the real design's art, name, piece, offsets, hue, door switch, and hidden switch. The normalized design SHA-256 is `dc16354762caa5435089f29107beb2effe72590ae11d7c164d77d57705885cb2`, matching the generated constant. The tower entrance catalog rows and their package records all lack the Door flag.

No additional stale-template duplication was established beyond the adjacent review. No additional living-player doorway or interior reachability defect was established: the existing movement test covers the templates on a flat map. The small tower's doorway-only interior and the white column tower's lack of an upper floor are explicitly documented P459 limitations, not new findings.

No new tests were written, and no C# suite or server build was run; lane tests are none. Current saves, real-site collisions, client traversal and rendering, and actual save/restart behavior remain unverified. No Haven connection, shard connection, container operation, deployment, or account operation occurred.

Ran `tools/progress.py --dry-run` with both work-copy roots supplied; exit 0. It rewrote `tools/progress.json` despite dry run, so restored its original bytes and verified equality. Only this review note is intended to remain changed.

P584 DONE
