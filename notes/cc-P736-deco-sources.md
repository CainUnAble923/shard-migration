# cc-P736: two player-built decoration sources for the building guide

## In plain words

- The building guide (`notes/guides/building-and-decorating.md`) now lists the UO.com contest-winning castles and UO
  Home Decor as sources, plus the UO.com winning keeps and two shard contests found by searching, each with what it
  is good for (section 9, the table under "Player-build sources").
- A new section 9.4, "Ideas from player builds", lists what the best player builds do: layered walls and floors,
  a roof shape per building, courtyards and villages inside the walls, one colour plus one accent, rooms furnished by
  what they are for, light where people are, and not too much clutter. Each idea names the stock art we already have
  for it.
- Ten small reference pictures (bar, keep workshop, farm, seven castles) are in `notes/guides/deco-refs/`, with where
  each came from.
- Something to decide later: corner spires (0x460F-0x4627) and the marble checker floor are newer art; a later build
  prompt should check that our player client draws them before using them. Nothing for you to do now.

## Merge order (for the integrator)

P734 (commit e5b1dcf, the guide's first version) was finished but not on `main` when this ran, so this branch carries
`notes/guides/building-and-decorating.md` as P734 wrote it plus this prompt's additions. **Merge P734 first, then
P736.** Git will report an add/add conflict on that one file; take P736's copy whole
(`git checkout --theirs notes/guides/building-and-decorating.md`). P736 changed only two places in it: the block after
"What could be reached (2026-10-29)" in section 9, and the new section 9.4 before section 10. Everything else in the
file is P734's text unchanged (checked: the file was written from `git show e5b1dcf:...` before editing).

## What was looked at

| Source | Looked at | Reached how |
|---|---|---|
| UO.com contest-winning castles | All 20 winners (Publish 101, 104, 106, 112), the main shot and three cut-away shots each (80 images) | Page and images downloaded with curl |
| UO.com contest-winning keeps | 6 of 16 (Robin's Nest, Villa Crowley, Citadel of the Far East, Desert Rose, 8 of Hearts, Queen's Retreat) | WebFetch for the list, curl for images |
| UO.com Customizable Keep & Castle Contest rules | The rules page | WebFetch |
| UO Home Decor | 40 images: 8 bedrooms, 5 bars, 6 landscape/roof, 5 waterfalls, Cassie Darksong's keep (5 rooms and roof), Tanelorn's dock house, the Runic Library, Lady Treasure Isle's farm, manor, shop and outside, two fireplace guides, the 2016 castle contest entries; text of the home-tour index and how-to indexes | The front page answered 406 to plain curl; I used WebFetch for the pages and plain curl for the images, which answered 200. (A retry of the page with browser-like headers was refused by the session's permission check, rightly; I did not pursue it.) |
| UO Forever 2025 Halloween contest | Rules, judging notes, winners, 5 entry images | WebFetch; images from i.imgur.com |
| UO Outlands King's Faire contest | Rules page (no entry images) | WebFetch |
| forum.uo.com 2023 Halloween winners, North Harbor contest | Not reached: 403, as P734 found | search snippets only |
| towerdenteoffores.blogspot.com | Read; it is a scraped copy of Stratics' Better Homes & Castles "Flowers" page | WebFetch |

The main finding about the castle and keep contests: the contest copies only what the house-customization tool
places (rules page), so those pictures teach shells (walls, roofs, floors, stairs, room plans), not furniture. UO Home
Decor and the shard contests are where furnished rooms are.

## Art IDs added to the guide

Read from `D:\UO\UltimaOnlineVanilla\tiledata.mul` with the vseUOAware `find_item_id_by_name` tool (it prints the ID
plus 0x4000; the guide has the item IDs). Names verified; facings and which wall set each belongs to were **not**
rendered in this prompt, and the guide says so where it matters.

| Search | Item IDs |
|---|---|
| battlement | 0x0072-0x0076, 0x0173, 0x0179-0x017D, 0x01A4, 0x02C7-0x02CD |
| spire | 0x460F-0x4627, 0x4642, 0x4643 (names say "South" only) |
| stained glass | 0x29A0-0x29BF |
| marble floor checker | 0x50E5, 0x50E6 |
| waterfall | 0x34ED-0x3528; frames 0xB1AB-0xB1BC |
| vines | decorative 0x0CEB-0x0CF2; grapevines 0x0D1B-0x0D24 (0x0C5E-0x0C60 are the pumpkin vines the farm uses) |
| anvil, forge | anvil 0x0FAF/0x0FB0; forge 0x0FB1; large forge 0x197E-0x19A9 |
| spinning wheel, loom | 0x1015-0x101E; upright loom 0x105F-0x1066; loom bench 0x1049/0x104A |
| ladder | wooden 0x0899-0x08A4; rope 0x08A5/0x08A6 |
| railing | 0x07D7/0x07D8 |
| planter | 0x44EF-0x44F1 |
| bed | 0x0A5A-0x0A91; four-post 0x4C68-0x4C7F |
| trophy | 0x1E60-0x1E6D; marlin 0x44E9-0x44EE |
| weapon rack | 0x41AD-0x4227 (several sets) |
| flower bed | 0x4B22-0x4B2A |

"dye tub" found nothing in tiledata (the item uses another art name); the guide mentions dye tubs only as what the
player room had, without an ID.

## Thumbnails

Ten JPEGs, 480 px at most, 17-70 KB each (limit 200 KB), in `notes/guides/deco-refs/` with `README.md` giving builder,
source page and image URL for each. Chosen to cover different lessons: walls and walk (Gothic Rose), roofs and court
(Feudal Castle), symmetry and towers (Sandstone Castle), village inside walls (House on the Ruins), plaza (Township),
furnished hall (Terrace Gardens), feast hall (Heorot), bar, workroom, farm.

## Checks

- Every `#anchor` link in the guide resolves to a heading, and every thumbnail the guide names exists (a short Python
  check, run after the edit).
- No server, map or ShatteredLegacy change; no tests apply to notes. `tools/progress.py` was run with `SL_SHARD` and
  `SL_MIGRATE` pointed at the Iron work copies; it rewrote `README.md`, `dashboard.html` and `tools/progress.json`.
- Scratch downloads (castle and keep images, UO Home Decor sample, contact sheets) stayed in the session scratchpad,
  not the repo.

P736 DONE
