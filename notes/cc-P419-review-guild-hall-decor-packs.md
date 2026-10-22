# P419: review of the P265 guild hall decor packs

Reviewed October 22, 2026. Notes only. No code, tests, art, configuration, or world data changed.

## Findings

1. **risk**, `server/customizations/GuildHallDecor/GuildHallDecorSeeder.cs:76`: Existing placements are recognized only at the exact saved anchor, so placing the vat again one tile east creates another full vat with coincident rows at offsets (-1,0,0), (0,-1,0), and (0,0,0) relative to the original anchor. Detect intersecting existing placement footprints and refuse the conflicting placement with a useful message; add a shifted-anchor case beside the existing same-anchor test.

2. **risk**, `server/customizations/GuildHallDecor/GuildHallDecorSeeder.cs:98`: Placement directly calls `MoveToWorld` without checking the transformed footprint against terrain, occupied blocking volumes, or existing doors, so the immovable vat, counters, stands, crystals, and railings can obstruct a hall entrance or path, and dry run still lists them as placeable. Preflight the whole placement, allowing intentional support stacks, and reject conflicts before creating anything; add occupied-tile and door-clearance cases to `server/tests/Misc/GuildHallDecorVerification.cs:171`.

3. **risk**, `server/customizations/GuildHallDecor/GuildHallDecorArt.cs:151`: The door variants `large-2q`, `medium-1h` (:162), `small-a8` (:169), `wbrick-12` (:182), and `wcol-11` (:194) all have Impassable and height 20, and their instances are plain `GuildHallDecor` items with no door behavior, so players cannot open or walk through those apparent entrances. Keep these facade pieces outside usable routes, or provide a functional doorway arrangement and verify passage with player movement tests before using a tower as accessible hall structure.

4. **risk**, `server/customizations/GuildHallDecor/GuildHallDecorSeeder.cs:83`: After a template edit, a re-run at the same anchor skips saved row numbers without comparing their art, position, hue, or template version, so tuning offsets does nothing and inserting a row can leave old pieces while creating an extra copy of the shifted final row. Give placements a template version and require an explicit clear and replacement when it changes, or reconcile stable row identities; cover an edited-template re-run in the seeder tests.

5. **risk**, `server/tests/Misc/GuildHallDecorVerification.cs:62`: `TheTemplatesAreTheDesignFile` hashes `GuildHallDecorDesignCopy.Json`, not the actual design file, so editing `design/guild-hall-decor/templates.json` without regenerating either C# file leaves this test green and the server on the old layout. Add a build check against the real JSON, or copy the real JSON into the test output and compare it directly; the files do agree in the reviewed tree.

6. **nit**, `server/tests/Misc/VirtualCheckActivatorVerification.cs:26`: The startup regression test checks only method ordering, so an empty `VirtualCheckActivatorFirst.Configure` would still pass while the startup crash could return. Also execute the initializer and verify that it sets the activator before `VirtualCheck.Configure`, preserving and restoring static state in the test.

## What checked out

- No same-anchor re-run duplication found with an unchanged template. The existing seeder test covers that case, group-only placement, dry runs, and clearing only owned decor.
- No pickup or theft defect found in the reviewed code. Every seeded piece, including stock counters, forge, anvil, flasks, and orbs, uses the same constructor with `Movable = false` at `GuildHallDecorSeeder.cs:267`, and `Decays` is false at :270.
- Pinned ModernUO rejects ordinary lifting through `Projects/Server/Mobiles/Mobile.cs:5070` and `Projects/Server/Items/Item.cs:2277`. Its stealing handler rejects immovable world items unless explicitly registered as stealables at `Projects/UOContent/Skills/Stealing.cs:222`; the decor seeder does not register them, and `Projects/UOContent/Engines/Stealables/StealableArtifacts.cs:231` looks up actual item instances.
- The command handlers pass `TestCenter.Enabled` into placement and clear, which refuse mutations when it is false. No live-shard refusal bypass found in those handlers.
- Read-only comparisons found no differences between the catalog's names, flags, weights, light values, and heights and the package tiledata records, and no missing referenced PNG. Catalog: `server/customizations/GuildHallDecor/GuildHallDecorArt.cs`, 179 pieces and 279 IDs; package: `player-package/vendor/shattered-legacy-art/records.json` and `art/28016.png` through `art/28294.png`.
- The normalized current design SHA-256 is `1f6657ad5fb46118ffa263015c7335317548381652af5c9678bd7a5b48f2aa77`, matching both generated C# constants. Counted template rows in `design/guild-hall-decor/templates.json`: alembic 51, smiths 5, artificers 8, structure 69.
- The early activator call matches pinned ModernUO's implementation: `VirtualCheckGump.Configure` assigns the activator, and `VirtualCheck.Configure` checks it. No current defect found in the initializer itself.

## Scope and evidence

Read both work copies' `AGENTS.md`, the direction decision and task list, `notes/cc-P265-guild-hall-decor-packs.md`, and all six source files in `notes/cc-P265-tools/`: `decor.py`, `first_templates.py`, `breaks.py`, `pkg_breaks.py`, `find_spot.py`, and `proof.ps1`.

Reviewed the P265 file list: the three `server/customizations/GuildHallDecor/` C# files; `VirtualCheckActivatorFirst.cs`; the art registration call in `ShatteredRunestone.cs`; `server/tests/Misc/GuildHallDecorVerification.cs`, `GuildHallDecorDesignCopy.cs`, and `VirtualCheckActivatorVerification.cs`; the design JSON; the package records, registry, credits section, and relevant `Build-UoOverrides.Tests.ps1` coverage; and the changelog and version. Inspected the small and large tower door PNGs, `art/28267.png` and `art/28249.png`.

Checked engine behavior against read-only `D:/UO/ModernUO-pinned` at `d4531cd94b739613155225c234900de9f47d2c88`. In particular, `Projects/UOContent/Engines/Pathing/Movement.cs:211` through :228 rejects overlapping impassable item volumes, while `Projects/Server/Items/Item.cs:1174` moves items without a placement-fit check.

Verification was source inspection and read-only data comparisons. No new tests were written, and no existing test suite or server build was run, consistent with this prompt's lane tests being none. The package suite includes launch tests that contact a shard port, so it was read without execution. No Haven or shard connection, container operation, deployment, or account operation occurred.

Unverified: actual hall door and path clearance, player interaction in a running client, rendering and animation in game, and behavior after a real world save and reload. P265 identifies these as draft layouts without selected hall sites and leaves client proof to a continuation; this review does not establish that any existing hall is currently obstructed. The placement and test concerns above are source-backed review findings, not runtime reproductions.

Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies. It completed successfully but rewrote `tools/progress.json` despite that flag; restored that initially clean file to its original HEAD bytes. Only this review note remains changed.

P419 DONE
