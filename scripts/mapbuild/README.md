# scripts/mapbuild

The general parts of the Rootdeep map build (cc-P167, cc-P180, cc-P181), kept as a module so the next dungeon, building
or hole starts from tested code instead of a copy of `build_burrows.py`. Read `notes/map-building-playbook.md` first;
it says which rules these tools enforce and which checks to run before showing Chase a picture.

| Module | What it is | Rootdeep-specific? |
|---|---|---|
| `uofiles.py` | read and write the client map files the way pinned ModernUO reads them (land uop, statics mul, tiledata), `restore_scratch`, `verify`, the walkable-set gate `same_cells` | no |
| `walls.py` | the wall rule measured on OSI buildings (`wall_pieces`, `walls_for`), inner and outer corners, the visible strip, opening groups and doorway frames per wall set, the one-piece-per-tile check | no |
| `scatter.py` | seeded weighted placement: clusters with gaps, never two identical pieces side by side | no |
| `isorender.py` | an isometric renderer with the client's tile layout and sloped land (`Scene.from_map`, `from_multi`, `render`, `tile_px`) | no (needs art.mul unpacked; `MAPBUILD_ART`) |
| `survey.py` | study tools: ModernUO decoration files, the corner and density survey of an OSI room block, land grids | no |
| `audit.py` | the land slope audit (ring steps and spikes, the way vseUOAware's diagnose_land_transitions reports corners) | no |
| `checklist.py` | the pre-render checklist functions; a build's driver prints the table | no |

Rootdeep's own files stay in `notes/cc-P167-tools/`: `build_burrows.py` (the driver: zones, rings, decor, corners,
frames, the gate), `plan-sets.json` (the look: seeds, weights, rules), `plan-cells.json` (the walkable record the
gate compares against), `render_burrows.py` (the picture set), `checklist.py` (the checklist driver).

Run everything with `python -P` (the `-I` flag hides the user-site numpy and Pillow). ASCII only.

Proof the move changed nothing: P181 re-ran the round 2 plan on the module before changing any rule and diffed
`statics-placed.csv`, `land-summary.csv` and `plan-cells.json` against the round 2 output: identical apart from the
lair arch, which moved from a hard-coded proposal to the stone set's `frameNS` rule (same two tiles, same ids).
