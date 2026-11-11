# cc-P878: build review of P877 (fix-up of P861: extra NPC name lists and [VBuild statify)

## In plain words

- I checked the Iron Golem's P877 fix-up (the freeze tool for fountains and other addons, and the name rule that
  keeps Mara the steward's name) against the building guide. It passes.
- It places nothing new in your world. The fountains and NPCs in the pictures were put down only on a throwaway copy
  of the world, to show the tool working.
- The pictures show the Fountain of Youth being left alone by the freeze tool, the stone fountain frozen and put
  back exactly as it was, and the second Mara renamed to Gaye while the steward stays Mara.
- Nothing for you to do. P877 can merge.

Iron Golem, 2026-11-10. Reviewer of branch `golem/Iron/P877` (both copies), read with fresh eyes against
`notes\guides\building-and-decorating.md` (read in full: short checklist, walls and corners, roofs, doors, stairs,
facing, heights, land, markers, proof, Stratics section, What to use where, P734 lessons).

## What I read

- `notes/cc-P877-review/placed.md` (present), `shots/walk.txt`, and P877's notes
  `notes/cc-P877-cont-fixup-names-and-statify.md`.
- The code diff `main...origin/golem/Iron/P877` in ShatteredLegacy: `AddonStatify.cs` (new), `ClusterFVisualBuilder.cs`,
  `ClusterFSeasonalSwitch.cs` (`IsTracked`), `ShardNames.cs`, `names-shard.json`, `GargishOutcast.cs`, the Dockerfile
  line and two test files. **No** seeder, decoration file (`server/data/Decoration/`), map static, mapop or permanent
  addon placement is in the diff. The only world-changing code is a staff command (`[VBuild statify`) that turns an
  addon a staff member targets into plain statics at the same spots, as one undo step.
- Every image in the folder (10):
  - `main-square-fountains-3651-2600.jpg` (isorender of main's New Haven square, x 3640-3668, y 2588-2614);
  - `shots/p877-1` to `p877-7` (TazUO, default camera);
  - `p861-shots/p861-3`, `-4`, `-5` (P861's own fountain proof).

## Checked one by one

| Guide item | Applies? | Finding |
|---|---|---|
| Walls and whole corners (2.2) | No walls placed | The buildings in frame are existing New Haven buildings, untouched by P877. |
| Doors (2.4) | None placed | - |
| Stairs (4.2) | None placed | - |
| Wall-mounted items (3) | None placed | - |
| Roofs (2.3) | None placed | Existing roofs in frame are clean; nothing stray on them. |
| Signs (2.5, 6) | None placed | No rune markers used. |
| Shores, bridges, docks, heights (4, 5) | None | No walkable join added. |
| Foliage (5) | None placed | - |
| Facing of multi-part addons (3) | Yes, proof only | Both fountains are round, one-variant addons; the 16 stone fountain pieces sit at pinned's offsets (listed in placed.md, matching `StoneFountainAddon`) and draw whole in the isorender and every shot. |
| Statify keeps the look | Yes | `p877-3` (addon) vs `p877-4` (statics) vs `p877-5` (undo): the fountain draws identically in all three; same for `p861-3/4/5`. Art, hue and position are kept, as the code says (`new Static(c.ItemID) { Hue, Light }` at `c.Location`). |
| Seeded pieces not frozen | Yes | `p877-1/2`: the Fountain of Youth at 3651,2600 still stands after the refused statify; `AddonStatify.SeededTypes` lists it and the seven other seeder-kept addons, so no frozen copy can sit under a re-seeded one (guide 2.6, no leftover duplicates). |
| Placed on land at the right Z | Yes | placed.md: every part at z 0 on paving of land z 0; isorender shows both fountains flat on the cobbles, not floating or sunk. The stone fountain's east rim reaches the beige corner stone of the brick-path diamond in the shots; it is a throwaway proof spot, not shipped, so not a fault. |
| Better piece on disk (10) | No | Nothing is chosen for a place: the tool keeps whatever addon staff target. |
| Names (no build) | Yes | `p877-6`/`p877-7`: "Mara the provisioner" becomes "Gaye the provisioner"; "Mara the town steward" keeps her name. |
| Proof left for review (8) | Yes | placed.md, an isorender, default-camera shots and the walk log are all there (P876's item 1 is met). |

Nothing in P877 is a build in the guide's sense, and nothing it shows breaks a rule of the guide.

BUILD REVIEW P877: PASS

P878 DONE
