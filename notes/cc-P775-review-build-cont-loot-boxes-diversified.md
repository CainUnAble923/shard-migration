# cc-P775: build review of P774 (fix-up of P763, loot boxes more varied and more useful)

Iron Golem, 2026-11-02, fresh session (did not build P774). Docs copy `D:\UO\golems\Iron\shard-migration`, code copy
`D:\UO\golems\Iron\ShatteredLegacy`, both on `golem/Iron/P775`. Nothing in P774's files was edited.

## In plain words

- **The loot box update (P763, fixed up as P774) passes its build review.** It builds nothing in the world: no walls,
  doors, signs or decoration. It only went to a build review because one patch file has "Decorative" in its name,
  and that word means a plant's status there, not map decoration.
- **I checked that myself in the code**, not only from P774's own list.
- **Nothing for you to do.** The integrator merges P774 when this branch comes in.

## What I checked

1. **Guide read in full:** `notes\guides\building-and-decorating.md`, sections 1-11, including the wall/corner
   east-south rule, stairs, roofs, signs, shores and What to use where.
2. **Review folder present:** `git ls-tree origin/golem/Iron/P774 -- notes/cc-P774-review` lists `placed.md`. It was
   copied to the scratchpad with `git archive` and read. It says P774/P763 places no piece in the world, with an
   empty placed table, and gives the reason the classifier picked it up. There are no renders or shots in the folder,
   and none are needed: there is nothing built to render (guide section 8 asks for a render of each building or area;
   there are none).
3. **The diff checked independently** (`git diff main...origin/golem/Iron/P774` in the code copy, 22 files):
   - Every file is loot box code, its tests, one migration, two patches, three guild/season files that award boxes,
     `apply-patches.sh`, `CHANGELOG.md` and `VERSION`. No `Data/` decoration, spawn, mapops or map file.
   - Added lines searched for `MoveToWorld`, `AddonComponent`, `Static(`, `Point3D`, `Decorate`, `mapops`, `Spawner`,
     `.Location =` and facet names. Only two hits: a test fixture moving a test mobile
     (`Pm.MoveToWorld(new Point3D(1400, 1400, 0), Map.Trammel)`) and a `TreasureMap` reward item created for a box.
     Neither places anything in the world.
   - `SetToDecorativeGump-loot-box-herbalist.patch` is one added line in ModernUO's plant gump
     (`ClusterFLootBoxes.OnPlantDecorative(from, _plant)`), awarding a Herbalist box when a plant is set to
     decorative. Not world decoration.
   - `ClusterFSeasonalSwitch.cs` adds a spring season whose up and down lists are empty (`_ => new List<string>()`):
     it places and removes nothing.
4. **Checklist items against the work:** walls and corners, doors, stairs, wall-mounted items, roofs, signs, shores,
   bridge and dock heights, foliage, piece choice: none apply, because no piece is placed. Nothing to fail.

Not part of the build review, noted for whoever reads this: `ClusterFGuildPromotion.cs` now calls
`ClusterFLootBoxes.CheckGuildRanks(pm)` at two places in the promotion path (one "first check records the ranks held",
one "the promotion's Society box"); P763's facts and the gated build (2,950 passed, 0 failed) cover it, so I left it.

## Verdict

BUILD REVIEW P774: PASS

P775 DONE
