# cc-P774 (fix-up of P763): pieces placed in the world

**None.** P763 (and this fix-up) places no item, static, addon, sign, wall, door or decoration on any map. There are no
mapops, no spawner or decoration file changes, and no `MoveToWorld` of a world piece.

| Item ID | Location | Facing |
|---|---|---|
| (none) | | |

Why P763 went to a build review: the integrator's classifier matched "Decorative" in the patch name
`server/patches/SetToDecorativeGump-loot-box-herbalist.patch`. That patch is a one-line hook in ModernUO's plant gump
(`SetToDecorativeGump.cs`). It awards a Herbalist loot box when a player sets a plant's status to decorative. "Decorative"
there is a plant status, not world decoration. P768 (the Gold Golem's review) found the same.

How this was checked, on the merged tree (`golem/Iron/P774` = main with `golem/Iron/P763` merged in):
- `git diff --name-only main` in the code copy lists only loot box code, its tests, one migration, two patches, three
  guild/season files that award boxes, `apply-patches.sh`, `CHANGELOG.md` and `VERSION`. No `Data/`, decoration, spawn
  or map files are among them.
- The added lines hold no `MoveToWorld`, `AddonComponent`, `Static(` or mapops call, apart from a test fixture that moves
  a test mobile. The full search is in `notes\cc-P774-tools\placement-search.txt`.

No renders or isorender: nothing is built, so there is nothing to render (the reviewer agreed: "No renders are needed
because nothing is built"). P763's in-game shots of opened boxes are in `notes\cc-P763-shots\`.
