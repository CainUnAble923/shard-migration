# P538: art on disk, unused inventory work notes

2026-10-24. Codex lane, Valorite tower. Research and notes only.

The requested catalog is [cc-P538-art-unused.md](cc-P538-art-unused.md). This file is the run note at the outer prompt's requested path. Both filenames are intentional.

## Work completed

Read AGENTS.md in both work copies before substantive work, then the migration work copy's direction-decision.md and tasks.md. Read the art-library references in notes, including P177, P201, P265, P266, P364, and P365. The shared master library was readable at `D:\UO\third-party\ART-LIBRARY.md`; a notes copy was not found. Read its sections and each catalog set's local SOURCE.txt.

Compared the code work copy's `player-package/vendor/shattered-legacy-art/registry.csv`, SOURCE.txt, and skins.json. Also read `player-package/vendor/paperdoll-sos/SOURCE.txt` to catch the separately vendored paperdoll art. Checked unpacked art files rather than repeating the library's historical file totals. Expanded the moongate colors and Hestia painting-family shorthand where folders exist.

The catalog groups art by P436 guild and League menus, P481 tutorial scenery and markers, mounts and pets, hall and home decor, dungeon kits and encounters, seasonal effects, equipment, and whole maps. Every main catalog row identifies the set, describes the art, records license flags, suggests a feature, and gives a real file under that set's folder. SOURCE.txt in that folder supplies the terms and author evidence.

Corrected stale disk labels by separating existing registry imports from candidates. In particular, the P265 guild-hall packs, P365 Thagoras mounts and juvenile stages, P362 container and scroll skins, and the SoS paperdoll vendor are already imported. Partly imported packs have their own section. Named leftover animations were compared against registry source filenames and source SHA-256 values. The mount shortlist was checked the same way.

Read `server/customizations/Mobiles/Evo/ShardBodyTypes.cs` and `EvoPetData.cs` and searched tracked customization references to the calf body values. The calves are registered but have no calf evo-line assignment in this source tree. Numeric hue, coordinate, cliloc, and unrelated item-ID hits do not establish a calf consumer. Save contents and live placements were not inspected.

## Findings and limits

The closest existing-art matches are the Quest/Guild buttons and dark UI frames for P436, tutorial markers and animated scarecrow targets for P481, bird and moose mount candidates, and the remaining furniture and scenery sets. The report includes attribution and EA/RIP/IP/replacement flags. It preserves specific restrictions, including DRC1K's noncommercial and no-modification terms, the unknown original machine author in Mad Scientist, and the ModernUO applicability question raised by the Chinese boat's ServUO-exclusive wording.

The catalog establishes local presence and absence of registry source attribution. It does not prove global runtime nonuse of every file or detect every renamed derivative and duplicate inside another vendor. No client visual review, animation action test, free-slot assignment, author contact, publication check, or world inspection was performed. Suggestions are possible future uses, not a decision to import the art or build a new feature.

## Verification

- All PowerShell commands ran under Windows PowerShell 5.1, confirmed by `$PSVersionTable.PSVersion` reporting `5.1.26100.9711`. No PowerShell tests or scripts were added.
- Lane tests: none, as requested. No code changed and no build was needed. No new test or gate was added.
- Ran `python tools\progress.py --dry-run` with SL_SHARD and SL_MIGRATE pointing at these work copies. Exit code 0. The tool unexpectedly rewrote tools/progress.json even with --dry-run: build() writes that snapshot before main() checks the flag. The initial working tree was clean. Restored only that generated output to its original HEAD bytes, then confirmed it has no diff. README and other generated files were unchanged. This existing tool behavior is ours to fix in a separate code task; no fix is included here.
- Checked the Golem's stop-request path between work steps. No request was present at those checks.
- Final review found no missing main-table file witnesses or SOURCE files, no missing named partial animations, no registered source hash among those partial candidates, and no omitted existing icon exclusion. Markdown table structure, absence of em dashes and trailing whitespace, and the 5 MB limit checked cleanly. Code work copy remained clean; only the requested notes remain changed in the migration work copy.

No art was generated, moved, copied, added, or registered. No docs directory, code, service inventory, world, account, or live system was changed. No Haven connection, deployment, commit, merge, push, or branch switch was made.

P538 DONE
