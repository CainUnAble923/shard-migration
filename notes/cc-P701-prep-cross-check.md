# P701: cross-check of the SoS swap preparation

October 27, 2026. Review only. ModernUO and Chase's decision to replace both
Trammel and Felucca geography remain the starting point. Map names and author
data are credited to Zigholtul, Siege of Sosaria Trammel Map 3.0.

The preparation is useful, but it is not one ready-to-install dataset. The main
conflicts are Haven's missing Felucca town core, proposed hostile or unguarded
settlements that the region drafts guard, Vesper's different guard footprints,
and dungeon teleporters whose interior landings miss both region drafts.
The champion proposals do not intersect the proposed town guards.

## Inputs and how this review was possible

P673 is present in the assigned work copy. None of the P692 through P699 output
paths was present in its checkout when this review began. All eight result
commits were available in the local Git object database. I read them with
`git show`, without merging, switching branches, or restoring their files into
the working tree. These are the exact reviewed snapshots:

| Prep | Commit | Notes and principal data read |
| --- | --- | --- |
| P692 | `d71c81e848c4afad52a7cace3e2ad7763a35a59a` | `cc-P692-sos-trammel-regions-data.md`, its shorter pointer, and `cc-P692-tools/trammel-regions.json` plus mapping/review tables |
| P693 | `98c18ebd8488fae14a00b344c75b49a8bf7c5e57` | `cc-P693-sos-felucca-regions-data.md`, its shorter pointer, `cc-P693-tools/felucca-regions.json`, champion and stock mapping data |
| P694 | `1f8b0f8158e411295115f31f4eddb936992a691e` | `cc-P694-sos-dungeon-decoration-port.md`, its pointer, both complete and both sealed CFGs, teleporter and type CSVs |
| P695 | `f8c5099050c973f57890701999cda5128bf3499d` | `cc-P695-sos-town-rosters.md`, `cc-P695-tools/rosters.json` |
| P696 | `4843d5bd5d52fb3d1c3d9d7e0969bf34a9735d99` | `cc-P696-sos-champion-sites.md`, `cc-P696-data/stock-sites.csv`, `candidate-sites.csv` |
| P697 | `a86062aaf6da291c39b8558f4ef471eeba75f997` | `cc-P697-sos-wiki-and-credits.md`, `wiki-drafts/world-map.md`, `towns-new.md`, `credits-sosaria.md` |
| P698 | `34502e993b0565aead8c89ccc885c7113bf7967f` | `cc-P698-sos-stock-spawner-plan.md`, `cc-P698-tools/spawner-plan.csv`, area and source summaries |
| P699 | `8c78bf4df07b80bf206977bf080a689def78556e` | `cc-P699-review-p673.md`, `cc-P699-review-p673-plan.md` |

Paths in this table are under `notes/`. To reproduce a read before these files
land, use `git show <commit>:notes/<path>`. The checkout's absence of those files
is an integration dependency, not evidence that the preparation was never done.
Repeat the joins below if integration changes any of these snapshots.

I also read P673, P669's relevant reports, P672's cast references, the local author
XML/CFG/source record, and the queued P674 through P691 swap briefs. Runtime
semantics were checked in read-only `D:/UO/ModernUO-pinned`, at
`d4531cd94b739613155225c234900de9f47d2c88`, and canonical shard sources where cited.
No web page or live service was consulted.

### Newer decisions that supersede the plan's open questions

The queued P674-P690 briefs carry **Chase's decisions, October 27 at 06:30**:
Haven moves as planned; the test shard gets a fresh world with no character or
house migration; Blackthorn moves to Fold zone 5 before 1.0 through P691; and
unfinished land and unpopulated author dungeons stay closed. These are newer
than P673's questions and override contrary prep recommendations. They do not
authorize P701 to wipe, deploy or change the plan files.

## Method and counted scope

The one-time data inspection parsed these actual artifacts:

| Artifact | Counted contents |
| --- | --- |
| P692 `trammel-regions.json` | 198 definitions, 1,182 rectangles |
| P693 `felucca-regions.json` | 150 definitions, 1,121 rectangles |
| P695 `rosters.json`, `settlements` | 52 roster entries |
| P694 `teleporter-ends.csv` | 200 directed placements, each with source and destination XYZ |
| P696 `stock-sites.csv` | 17 source champion entries, with stock and proposed coordinates |
| P696 `candidate-sites.csv` | Six alternatives: A and B for LL06, LL07 and LL11 |
| P698 `spawner-plan.csv` | 4,304 stock rows and 107 new-area requests |

Region containment uses each individual rectangle and its Z bounds, with
exclusive upper edges. Champion checks intersect the whole initial 48 by 48
rectangle with active guard footprints in both region drafts, including lodging
coverage inherited from guarded parents. A bounding box around a town or a
roster search area is not a substitute for its rectangles.

"Outside every region" below means outside every explicit candidate definition.
ModernUO still has a map default region. This inspection establishes data
agreement or disagreement, not safe terrain, a loaded region, or actual movement.

## Disagreements and fixes

### 1. Haven has different names and law on the two facets

**High. Owners: P678/S7, P676/S3 and P686/S13.**

P692 calls the broad no-housing island `Haven Island`, adds a provisional guarded
`New Haven` core, and parents `The Albatross Bar and Grill in Haven` to that core.
P693 retains the broad unguarded `Haven`, has no `New Haven` core, and parents
`The Albatross Bar and Grill` to the island. P695's `Haven` roster is for the
rebuilt New Haven service hub, independently on both facets. P673 S13 says the
towns match, while P693 explicitly leaves the town core for later work.

**Fix:** P678 supplies one surveyed HavenSpots layout and an explicit per-facet
start and service policy. P676 and P686 consume its town core and shop footprints,
with a name table separating the island, town and inn. Keep broad island housing
rules separate from the guarded core. Preserve active Trammel `New Haven` name
consumers; do not create a Felucca character start simply because its town has
services. Resolve Ocllo's old name and lodging disposition explicitly.

### 2. Zero roster guards does not disable a guarded region

**High. Owners: P682/S10, P676/S3 and P686/S13.**

| Place | P695 proposal | Both region drafts |
| --- | --- | --- |
| Plunderers Peak | Unguarded market, no law guards | `TownRegion`, `GuardsDisabled: false` |
| Red Baron Stronghold | Later hostile toll encounter, no public services or law guards | Active guarded `TownRegion` |
| Red Dagger Keep | Later smuggling encounter, no public law guards | Active guarded `TownRegion` |

Pinned `Regions/TownRegion.cs:5` derives from GuardedRegion;
`GuardedRegion.cs:33,50` controls disabling. An NPC headcount of zero does not
turn that law off. The author type and our proposed story are different inputs.

**Fix:** agree a jurisdiction and encounter disposition for each place before
placing enemies or publishing safety claims. Either retain the author's law and
revise the roster, or approve an unguarded or divided footprint and document the
deviation. Hold the hostile encounters until that choice and the boundary checks
are complete. P673's generic garrison instruction for Castle Dunbain and Tigerclaw
also needs P695's distinction between friendly shelter and hired enemies.

### 3. Named forts in the rosters are not independent town regions

**Medium, High if a placement assumes guard protection. Owners: P682, P676, P686.**

These roster names have no standalone candidate region on either facet. Their
first supplied landmarks do have the following containing wild region:

| Containing region in both drafts | Roster landmarks |
| --- | --- |
| Yew Forest | Fort Whitestone, Fort Viridian, Yew Forest Guardpost, Mistveil Ruins |
| Britain Forest North | Fort Stormhammer, Castle Dunbain |
| Britain Forest South | Fort Silverblood, Brit Forest Guard Barracks, Brit Forest Guardpost, Camp Ironfang, Ivanguard Manor, Dhampire Ruins |
| Trinsic Jungle | Camp Bloodwater Basin, Chapel of Saint Lucia |
| Covetous Forest | Tigerclaw Fortress |

This is the complete list of 15 point-only roster names unmatched to a standalone
native name after accounting for Haven and Heartwood naming. Jhelom has a native
region even though its roster lacks copied region metadata. No ordinary civic
town in the Trammel roster was missing after those name reconciliations.

**Fix:** maintain a place-to-region table using these wild parents until a building
survey justifies another footprint. Do not invent guard rectangles around a point.
P682 must hold any friendly-shelter/hostile-yard arrangement without verified
separation. Garrison staffing remains distinct from legal guard jurisdiction.

### 4. Vesper's lodging extends guard coverage on Trammel only

**High. Owners: P676 and P686.**

P692 retains six lodging rectangles in `Vesper / subregion 1`, as an active
TownRegion. P693 retains four and removes the two wholly outside the Vesper town:

- x `[2776,2792)`, y `[952,984)`.
- x `[2768,2776)`, y `[960,976)`.

These are different actual guard footprints, not just different child names.
P692 also records Kettleburg/Skara Brae equal-priority intersections at
x `[723,724)`, y `[2316,2359)`, and x `[732,733)`, y `[2364,2420)`.
Those peer overlaps survive on Felucca at its higher common town priority.

**Fix:** survey the detached Vesper lodging and keep it unguarded until a valid
town connection is established, or redraw an approved town/inn boundary on both
facets. Resolve the Kettleburg/Skara ownership and the Britain/castle overlaps
from one geographic boundary review. Equal priority between unrelated regions
does not state which town should win.

### 5. The region drafts use independent policies, not just different facet rules

**High for installation. Owners: P676 and P686, coordinated with P678.**

P693 was written without P692's output. P692 generally puts wild regions at 10,
ordinary towns/dungeons at 50 and hazards at 60. P693 generally uses wild 50 and
town/dungeon 60, with castles at 61. Child naming and classes also differ.
P692 carries 47 stock candidates and a new Haven core; P693 leaves unmatched
stock names in its disposition table rather than its runtime array.

Important semantic differences include:

| Place or family | P692 | P693 | Required resolution |
| --- | --- | --- | --- |
| Swamp of Desolation | Surface `NoHousingRegion`, priority 10 | `DungeonRegion`, priority 60 | Decide surface lighting, young-player and housing behavior; geography alone cannot choose it. |
| Sea Market | Guarded TownRegion | Unguarded TODO SeaMarketRegion | Record an explicit facet exception or change the candidate. P695's mirrored garrison proposal cannot imply guards on both. |
| Five Mondain dungeon roots | MondainRegion | Stock Felucca DungeonRegion | Preserve justified facet travel differences; do not normalize class names blindly. |
| Lodging children | Named TownRegion children | Mostly unnamed BaseRegion children with parents | Compare effective inherited law, logout and housing behavior. Different class names alone do not prove lost guards. |

The five roots are Blighted Grove, The Painted Caves, The Palace of Paroxysmus,
The Prism of Light and Sanctuary. Pinned `Region.cs:231-252` orders regions by
dynamic status, priority and child depth. Its parent forwarding at
`:768-775,805-809,836-845` means a BaseRegion inn can inherit guard hooks.
`SeaMarketRegion.cs` derives from BaseRegion and is marked TODO.

**Fix:** approve one shared geographic and name mapping, then a small explicit
facet-rule difference table. Review retained stock cave, field, mine and entrance
names against their consumers. Replace each facet slice, rather than appending
duplicate old definitions or replacing the entire world file. Strip P692's
handoff metadata before installation and preserve native parent ordering.

### 6. Seven interior teleporter landings miss both region drafts

**High before the affected route opens. Owners: P683/S6, P676/S3, P686/S13, S18.**

Joining every P694 destination to the actual P692 and P693 rectangles gives the
same exceptions on both facets. These seven landings are intended dungeon
interiors, so default wilderness behavior is not an adequate final disposition:

| P694 directed IDs | Section | Destination XYZ | Region disagreement |
| --- | --- | --- | --- |
| T073, T074 | Everstar Estuary, Entrance | `(6369,3729,-16)`, `(6369,3730,-16)` | Everstar's only region is x `[6490,6790)`, y `[3224,3494)`. |
| T079, T080 | Everstar Estuary, Level 1 Exit | `(6227,3730,-16)`, `(6227,3731,-16)` | These internal destinations also miss that region. |
| T125, T126, T127 | Murkmere Dwelling, Entrance | `(6468,3297,24)`, `(6469,3297,24)`, `(6470,3297,24)` | At y 3297 the supplied Murkmere region ends at exclusive x 6420. |

P692 retains out-of-region author staff points for these dungeons with warnings;
P693 selects other contained points. For example, Everstar's Trammel staff point
is `(6366,3730,-16)`, while Felucca's is `(6505,3471,-1)`. Changing the staff
point does not repair the actual travel destination.

**Fix:** survey the arrival pads, each connected level, doorway and Z before
correcting the region or teleporter. Do not stretch a single rectangle across
packed dungeon cells to include them. Keep the surface entrance rows sealed;
T079 and T080 are still active in P694's sealed files and need an explicit
disposition too. Update staff anchors, entrance/recovery metadata, both facet
regions and the route inventory from the same verified layout.

### 7. Fourteen surface return destinations have no explicit candidate region

**Medium pending survey. Owners: P683, P676, P686 and P687/S14.**

The remaining 14 of the 21 uncovered destination records per facet are surface
returns. They can legitimately use a default wild region. They still need a
walkable landing, closure check and intended housing/law disposition:

| P694 directed IDs | Dungeon | Surface destination XYZ |
| --- | --- | --- |
| T033-T036 | Azurite Caverns | x 4284, y 561-564, z 0 |
| T055-T056 | Black Widow Pit | x 2125-2126, y 3435, z 10 |
| T066-T068 | Bleak Wind Tunnels | x 473-475, y 3306, z 0 |
| T103-T104 | Iguana Cove | x 946-947, y 1535, z 60 |
| T134-T136 | Nimaku Lava Basin | x 1407-1409, y 3473, z 2 |

All these rows remain active in the sealed files. Azurite's four return tiles
fall inside P673's proposed northeast snow closure, x 4224-4479, y 256-767.
Keeping an exit active must not strand someone inside that fence.

**Fix:** give each group an explicit default-wilderness or surveyed named-region
disposition. P683 and P687 must choose a safe return policy for Azurite before
any entry or recovery route can use it. Verify the safe side of the closure and
the route back to public services. Do not add guarded regions merely to make a
containment count reach zero.

### 8. Champion areas are clear, but the two prep files describe different positions

**Medium handoff requirement. Owner: P685/S12, with P686.**

P693's `champion-areas.json` describes stock generator coordinates. P696 proposes
moving LL06, LL07 and LL11, plus replacing LL08's ejection point. Treat P696 as
the placement proposal and P693 as baseline review evidence.

The full 48 by 48 areas for all 17 stock positions and all 17 proposed positions
have no intersection with active town guards in either candidate region file.
All six A/B alternative rectangles are also clear. The row list is LL01-LL12
and D1-D5 in `stock-sites.csv`, plus LL06A/B, LL07A/B and LL11A/B in
`candidate-sites.csv`. No champion-in-town defect was found in these drafts.

Fire/D4's ejection point `(2923,3406,8)` is inside Serpent's Hold. That is an exit
landing, not the Fire champion area. P696 already identifies that distinction.

**Fix:** carry the selected altar/controller, whole spawn rectangle and ejection
point together. Repeat the overlap check against final P686 law and P687 fences,
including after any fallback. Preserve the random LL types and fixed dungeon
types. Verify the platform, reachable spawn floor and ejection route in game.
Assign P699's separate Harrower destination inventory to P685 as well; these
17 GenChamps entries do not cover it.

### 9. Stock spawn keep candidates still enter proposed guarded towns

**High review queue, not proof of a live fault. Owners: P681/S9, P676 and P686.**

P698 marks these five mixed hostile Outdoors records per facet as `keep`, based
on local tile grades, while both region drafts put their home inside guarded
Serpent's Hold. Source rows below are one-based and identify each record exactly:

| Home XYZ | Trammel Outdoors row | Felucca Outdoors row |
| --- | ---: | ---: |
| 3024,3566,15 | 79 | 294 |
| 3013,3591,15 | 129 | 230 |
| 2966,3591,11 | 290 | 125 |
| 2963,3617,3 | 325 | 26 |
| 3042,3590,5 | 363 | 134 |

Files are `Spawns/shared/trammel/Outdoors.json` and
`Spawns/shared/felucca/Outdoors.json` under pinned `Distribution/Data`.
The mix includes GiantSerpent, Lizardman, Ratman and SilverSerpent; these are
not just harmless town livestock. The ledger preserves home and walking ranges
of 30. P698 does require a later region check, so its keep label is provisional.

A separate pair at `(5728,3209,-3)` is inside Papua: Trammel LostLands row 15,
Felucca LostLands row 66, both SwampDragon with range 100. A tameable creature is
not automatically an unsafe encounter, but this range needs a civic-space review.

**Fix:** flag the ten mixed-hostile records for P681's town-boundary review rather
than importing them automatically as unchanged. Survey whether the town boundary
is overbroad or the encounter must move. Keep matching habitat within 20 tiles,
or record a drop and any dependent encounter work. Review the two SwampDragon
records separately. Then check full spawn/wandering footprints, including homes
outside a town whose ranges enter it. P698's four named new-town overrides are
not a complete jurisdiction check.

### 10. Decoration conversion is complete as data, not as closure coverage

**High before opening. Owners: P683, P679/S4, P687 and S18.**

P673 calls the author file 775 decoration lines containing doors, teleporters and
props. P694 resolves that to 200 placed teleporters, no doors or props, and an
unplaced MISC template. Its sealed versions omit 70 surface entrance placements
and retain 130 exits/internal links. Facet-specific MapDest values are already
corrected. These parts of P699 R11 are addressed by preparation, not outstanding
conversion work.

However, Boulder Tunnel, Guardians Power Plant and Kal-Berbesia have empty
entrance sections. P694 cannot supply their seals. P692 also flags XML-embedded
CrystalFieldTele spawning that is outside this CFG conversion. P698 inventories
stock spawns, not every such XML object or generated travel route.

**Fix:** P683 starts with the two sealed CFGs, installs each only on its matching
facet, and reconciles stock/generated routes and existing items. Use one dungeon
access inventory covering entrances, internal links, exits, walk-ins, spell
arrivals and recovery routes, with an explicit held state for missing data.
Assign the XML spawn object a checked stock equivalent, separate implementation,
or documented deferral. Do not treat a converted region class as executing XML
spawning. P687 enforces destination closures where needed; S18 removes only the
opened dungeon's holds after encounters and a safe return work.

### 11. Wiki names are backed, but publication must use the final status inventory

**Medium. Owners: P689/S16, P682, P687 and S18/S19.**

I found no unsupported place name in the new wiki drafts. A missing standalone
native region is not a nonexistent landmark: Yew Fort of the Damned is in the
author's location list and P695's explicitly held hostile sites. Fortress
Calcifina is a dungeon in both region drafts and is described as such. Dawn and
the separate Sosaria-facet towns are consistently excluded. Haven Catacombs and
Rootdeep are consistently distinct.

P695 now supplies proposed people for names whose wiki entries still say no
roster or inhabitants have been established. That is an editorial update, not
proof those people exist. The wiki's range notation also copies exclusive XML
upper edges into ordinary ranges, so it should not become a placement contract.
P697 correctly calls the pages drafts and does not claim services or quests run.
Its world-map paragraph proposing that Blackthorn stay out of 1.0 is now stale:
the queued decision requires its move through P691 before 1.0.

**Fix:** publish from a final place/status table that distinguishes native region,
point-only landmark, proposed roster, working services, safe access and sealed
content. Link each public entry to its actual disposition; update the wording to
acknowledge proposals without promising their implementation. Keep upper-edge
semantics in staff data. Reconcile older Haven/dungeon guide directions at
publication. Replace the Blackthorn omission wording with its planned Fold
relocation, keeping access unconfirmed until P691 passes. Carry Zigholtul's
credit into the first distributed package, then
all P697 destinations. Current online reuse terms remain unverified here.

### 12. Area names, closures and population holds need one shared contract

**High before enabling an affected area. Owners: P687, P681, P682 and P688/S15.**

P695 holds its Glimmerwood and Echoback actors for S19; P698 requests coverage
while holding fenced portions; P697 describes broad planned closures. P673's
boxes are survey cells, not the full named regions. For example, its Glimmerwood
seam cells end at y 3071, whereas P692/P693's Glimmerwood begins at y 3077. The
Echoback campsite `(4454,2586,5)` is outside the proposed edge-cell fence at
x 4096-4223. A name-based hold is conservative, but is not proof a specific fence
covers that actor or entrance.

**Fix:** P687 publishes actual polygons, safe turnback/exit points and held routes
for each facet. P681 and P682 subtract those polygons and retained populations
from placement areas; P688 checks the resulting approaches. Keep conservative
holds until that survey resolves them. Do not broaden a fence to an entire
named region just to match prose, or open an actor because its anchor happens
to miss the old survey box. P698's six newly dry dungeon-strip components
357, 370, 349, 365, 348 and 395 stay with S18, not surface island population.

### 13. P699's release blockers still apply to the prepared data

**Blocker for player opening. Owners: the swap integration owner and relevant builds.**

The preparation does not make P673's S1/S2/S3/S7/S8 set safe to open alone.
Travel, Felucca rules, unsafe existing objects and spawns, champions and closures
remain separate work. P699 also identifies the package gate/admission contract,
server map-reader precedence, world initialization, recovery tables, Old Haven
training/cleanup and shared-file mirror behavior. None is implemented by notes
or a region/decoration candidate.

Source spot checks confirm the concrete build and map concerns: package
`Build-PlayerPackage.ps1` rejects map extensions, and pinned
`TileMatrix/TileMatrix.cs:100-124` tries MUL before UOP. Region DungeonRegion and
BaseRegion behavior does not seal entry by itself. These are contracts the build
prompts must fix, not a reason to change the chosen map or engine.

**Fix:** integrate the safety portions of travel, both-facet law, existing-content
handling and closures before ordinary player access, or keep access closed.
Coordinate mapops ownership and client/server output identity. Rehearse the
fresh-world initialization on disposable data. Drop P699 R2's character/house
preservation branch under the newer queued decision; do not revive migration
work from P673's older recommendation. Publish credits with the first
package. Require a final passing playthrough after repairs, including recovery
and restart/save reload. The queued decision resolves the world, Blackthorn and
closure choices; P699's older questions do not reopen them. Neither those
decisions nor this review authorize deployment from P701.

### 14. P691 needs a larger footprint than P673's proposed zone 5 box

**High before the Blackthorn move. Owners: P691, P675 and the Fold layout owner.**

P673 proposes zone 5 at inclusive x 6890-7150, y 3905-4080, or 261 by 176 tiles.
Canonical `server/customizations/Services/Revamped Dungeons/BlackthornDungeon/Region.cs:55`
declares `DungeonBounds = new(6151, 2301, 413, 539)`. That unchanged rectangular
region cannot fit inside the proposed zone. The whole site A mirror room is
only 352 tiles high, less than the existing dungeon's 539. An offset alone
cannot preserve that region within the current room. This is source geometry,
not a claim to have surveyed a replacement site or every dungeon floor.

**Fix:** P691 must reserve a sufficiently large, verified clear Fold footprint
with matching Trammel/Felucca mirror protection, or explicitly redesign and prove
the dungeon's footprint. Keep the selected move-before-1.0 requirement. Coordinate
mapops and privacy boundaries with P675 and the isle owner before copying tiles.
Audit all Blackthorn placement and rule coordinates, including the invasion-room
threshold, random relocation points, spawners and castle return routes, rather
than changing only the two files named in the summary. P692/P693's static
Blackthorn Castle data must also be reconciled with the runtime castle region
registered by this source file.

## What each Iron swap prompt should take

The queued briefs currently assign the following prompts to Iron. These are
input and acceptance handoffs, not permission to run them during P701.

| Prompt | Take from prep | Still prove or resolve |
| --- | --- | --- |
| P674 / S1, package | P697 credit snippets; P699 R3-R5 and R10 | Narrow hash-checked asset exception, actual admission signal, correct map0/map1 packs, invalidation and client/server parity. Credit the first package. |
| P678 / S7, Haven | P692/P693 Haven mismatch; P695 Haven roster; P698 surface-undead/service ledger; P699 R6-R10 | One HavenSpots contract, surveyed shops/core, full Rootdeep seeder/return conversion, cleanup/training/recovery behavior and no duplicate Elara/Rook. |
| P681 / S9, stock spawns | P698 stock rows and summaries; P695 service floors; findings 9 and 12 | Preserve import exclusions and identities, independently check Felucca, resolve town/range conflicts and closure overlaps, then pass actual spawn/fit checks. |
| P682 / S10, new people | P695 rosters and held names; P698 new-area requests; P692/P693 law | Fill only shortages after S7/S9, approve settlement allegiance, survey point-only sites and safe shelters, hold quest/patrol actors requiring implementation, measure usable-area density. |
| P683 / S6, author travel | P694 sealed facet CFGs, ends/pairs and type map; findings 6, 7 and 10 | Repair or explicitly hold mismatched landings, safe Azurite exits, empty entrance sections, existing-item collisions and complete route closures. |
| P684 / S11, treasure/houses/boats/SOS | Final P692/P693 regions; P698 island/fence distinctions; P699 R15 and the fresh-world decision | Exclude final towns/closures, omit old-world migration work, reject SOS zero failures, prove usable dock and sailing routes. |
| P685 / S12, champions | P696 stock/candidate CSVs; P693 baseline champion areas | Select three relocations and accompanying exits, replace LL08's exit, recheck final guard/fence intersections, platform/spawn access, and Harrower destinations. |
| P686 / S13, Felucca regions | P693 candidate plus P692 mapping and P695 law proposals; findings 1-8 | Reconcile shared geometry, Vesper, Haven core, names/priorities and explicit facet exceptions; retain Felucca rules and prove runtime consumers. |
| P687 / S14, fences/seals | Both region drafts; P694 held routes; P695/P698 population holds; P697 closure wording; P699 R11-R13 | One exact closure/access inventory, safe exits including Azurite, destination rejection, no housing, boats passing safely and mapops ownership. |
| P688 / S15, walking/bot | All finalized town bank/dock/gate and teleporter coordinates; P695 service circuits; P696 ejections; P699 R6/R12/R15 | Actual movement and reachable approaches, including recovery, both facets and water routes. A dry tile or a region join is not the route proof. |
| P689 / S16, credits/wiki | P697's three draft pages, P695 proposed roster and final closure/access statuses | Reconcile old directions, publish only checked access/services, complete all credit destinations and hand fidelity changes to the overseer. No lane edit to migration docs/. |
| P690 / S17, full playthrough | Final combined artifacts, P699's expanded playthrough list and queued decisions | Use a fresh private world, include P691 Blackthorn and recovery, repair and retest failures, and end with a passing log. |
| P691, Blackthorn move | P673's proposed Fold layout, queued move-before-1.0 decision, P692/P693 castle data and finding 14 | Reserve enough verified clear space, move all coordinates/rules and access, reconcile runtime castle regions, prove no old-site generation and safe entry/return. |

For the other queued owners: P675/S2 takes P699's map-reader, registry and mirror
corrections; P676/S3 takes the joint P692/P693 boundary and name review; P677/S8
takes the generator/recovery/coordinate gaps; P679/S4 takes the same route and
closure inventory; P680/S5 reconciles decoration with S7 and actual SoS statics.
S18 later consumes P694's per-dungeon held entrances and P695's dungeon actors,
while S19 consumes the exact unfinished-area holds and P698's reserved surveys.

## Verification and limits

This review used local committed artifacts and direct source inspection. Inline
Python performed one-time parsing, XYZ containment, rectangle intersections,
name reconciliation and spawner-home joins under Windows PowerShell 5.1.
No persistent test or gate was added; lane tests are none. The initial inspection
needed a correction to handle P693's valid unnamed child records. Final joins
include them and their parent guard coverage. No prep output was edited.

The complete uncovered-destination list is in findings 6 and 7. The complete
point-only roster list is in finding 3, the champion row sets in finding 8,
and the specific stock-spawn exceptions in finding 9. Counts refer to the
listed input files, not descriptions of them.

Unverified: SoS terrain and statics, landing Z and collision, loaded regions,
runtime law or housing, routes, service operation, actual spawns, closures,
package execution/admission, save conversion, live state and current online
reuse terms. No map asset was read or client/server started in P701. A proposed
fix above is an implementation handoff, not a claim it has been applied.

No code, migration docs/, service configuration, saves, accounts or map files
changed. No Haven connection, Docker operation, deployment, commit, merge,
push or branch switch occurred. The companion lane note records final checks.

P701 DONE
