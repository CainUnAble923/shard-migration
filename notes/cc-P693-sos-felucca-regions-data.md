# P693: Felucca regions on the Siege of Sosaria land, as data

2026-10-27. Data and notes only, for S13. Credit Zigholtul for Siege of Sosaria
Trammel Map 3.0 and its region geometry. ModernUO remains the server.

## Result and scope

[felucca-regions.json](cc-P693-tools/felucca-regions.json) is a native ModernUO
region array containing the SoS geography on `Map: Felucca`. It contains 150
definitions and 1,121 nonempty rectangles. It is a candidate for S13, not a
runtime installation. No code, patch, live configuration, map, save, account,
service, or deployment changed.

P692's output was not present in these work copies. This conversion therefore
uses the author's Trammel section directly, preserving the pinned Felucca
conventions where identified below. S13 must reconcile it with the final P692/S3
data before installation. This task finishes the data handoff; it does not claim
to finish S13 or its gameplay proofs.

The source and target file lists are part of the deliverable:

| File | Contents |
| --- | --- |
| [felucca-regions.json](cc-P693-tools/felucca-regions.json) | Native array, with `$type`, `Map`, `Name`, `Priority`, `Area`, and optional native properties. Contains only Felucca. |
| [felucca-region-mapping.csv](cc-P693-tools/felucca-region-mapping.csv) | Every author Trammel region, its target array index, name, type, parent, rectangle counts, priority, go-point source, and conversion remarks. All indices are zero-based. |
| [stock-felucca-mapping.csv](cc-P693-tools/stock-felucca-mapping.csv) | Every pinned Felucca definition, including unnamed lodging, with its replacement or unresolved disposition. |
| [champion-areas.json](cc-P693-tools/champion-areas.json) | Every stock GenChamps Felucca entry, altar and ejection coordinates, default spawn rectangle, candidate regions at the altar, and guard overlaps. Review data, not native region-loader input. |
| [region-review.json](cc-P693-tools/region-review.json) | Input hashes, counted totals, exact geometry exceptions, unresolved go points, guard/dungeon overlap results, literal lookup candidates, and dependencies. Review data, not native region-loader input. |

Only `felucca-regions.json` is a region-loader array. When S13 installs its final
version, it must replace the old Felucca slice of the assembled `Data/regions.json`
and retain other facets. Appending it would duplicate old regions and names;
replacing the whole world array with it would remove other facets.

## Sources checked

Working agreements were read in both work copies, along with
`docs/direction-decision.md`, `docs/tasks.md`, P673's swap plan, P669's assessment,
and `notes/sos-author-data/SOURCE.txt`. No files under `docs/` were edited.

Data sources, whose exact SHA-256 fingerprints are in `region-review.json`:

- `notes/sos-author-data/Regions.xml`, specifically `Facet name="Trammel"` for
  the new geography. Its Felucca section is old geography, not an SoS Felucca
  conversion. Its separate Sosaria section is not this task's selected map.
- `notes/sos-author-data/locations-trammel.xml` for source-backed staff anchors
  that lie inside the converted region. No map-average Z was invented.
- `notes/cc-P669-tools/out/felucca-summary.csv`, and the `felucca.py` and `geo.py`
  source that explains its measurements.
- `D:/UO/ModernUO-pinned/Distribution/Data/regions.json` and
  `Distribution/Data/map-definitions.json` for the shard's pinned format and
  Felucca baseline. The read-only checkout's HEAD was verified as
  `d4531cd94b739613155225c234900de9f47d2c88`.
- `D:/UO/ModernUO-pinned/Projects/UOContent/Engines/CannedEvil/GenChamps.cs` for
  champion entries. `ChampionSpawn.cs:190-194`, `:198-207`, and `:1365-1372`
  establish the actual area and runtime region behavior.

The canonical shard's `server/customizations/` and `server/patches/` were checked
for region definitions, region-data patches, and literal name lookup candidates.
`Fold/FoldRegions.cs` still defines the old Trammel-only mirror; moving it and
adding its Felucca twin remain S2 work. The GuardedRegion witness patch does not
provide new Felucca region geometry. The stale `server/uo/` tree was not read.

## Counts and mapping

P669's **272** is the number of pinned Felucca rectangles, sampled at their
centers. It is not a count of named regions. Counting the pinned array gives
**107 definitions, 272 rectangles**. P669 grades 185 centers unchanged, 54 moves,
and 33 rework. Those grades cannot establish that an entire rectangle is safe,
and the summary does not identify each graded rectangle.

The author's Trammel section contains **150 definitions, 1,128 rectangles**.
Its old Felucca section contains **128 definitions, 505 rectangles** and was not
used as the replacement geography. The 150 source rows are all represented in
the native array. Five empty rectangles and two Vesper lodging rectangles are
omitted, as itemized below, producing 1,121 target rectangles.

| Native type | Definitions |
| --- | ---: |
| TownRegion | 32 |
| BaseRegion | 53 |
| NoHousingRegion | 5 |
| SeaMarketRegion | 1 |
| DungeonRegion | 51 |
| PoisonedTreeRegion | 1 |
| AcidRiverRegion | 1 |
| CrystalFieldRegion | 1 |
| IcyRiverRegion | 1 |
| MondainRegion | 2 |
| JailRegion | 1 |
| GreenAcresRegion | 1 |

The full name and type list is `felucca-region-mapping.csv`, not a keyword count.
`stock-felucca-mapping.csv` accounts for the baseline as follows:

| Disposition | Definitions |
| --- | ---: |
| Replaced by an author Trammel footprint | 41 |
| Replaced by parent-linked lodging | 15 |
| Ocllo superseded by Haven, awaiting S7's guarded town core | 1 |
| Old outside-town guard regions retired in this candidate | 2 |
| Named stock definitions with no verified author replacement | 47 |
| Old Ocllo lodging with no verified replacement | 1 |

The unresolved named definitions are the individual Britain and Yew fields,
surface caves and mines, Wrong/Covetous/Despise entrance and passage regions, and
Moonglow/Skara Brae fields listed individually in that CSV. They were not silently
copied onto different land. S13 must review whether to redraw or retire them and
check their consumers. General wilderness coverage alone does not preserve their
individual names or any old housing restriction.

## Native conversion and geometry exceptions

- XML `rect x/y/width/height` becomes `x1/y1/z1/x2/y2/z2`; the ends are exclusive.
  `zrange` and per-rectangle `zmin` are retained. Default vertical bounds are
  explicitly -128 through 128, matching `Region.MinZ/MaxZ` at `Region.cs:127-128`.
  Explicit Z avoids the JSON rectangle converter's different implicit upper bound
  (`Rectangle3DConverter.cs:152-157`).
- XML nesting becomes a flat list, with parents earlier than their children and
  `Parent: { Name, Map: Felucca }`. The loader resolves those parents by name
  (`RegionByNameConverter.cs:75`) and restores child levels
  (`RegionJsonSerializer.cs:61-66`). Every parent in this source has a name.
- Untyped author regions become `BaseRegion`; `Jail` and `GreenAcres` become the
  registered `JailRegion` and `GreenAcresRegion`. The four hazard type names gain
  the native `Region` suffix. Every emitted type appears in pinned
  `Regions/RegionJsonRegistration.cs`.
- Canonical stock names remain `The Heartwood`, `The Painted Caves`,
  `The Prism of Light`, and `The Palace of Paroxysmus`. The author's shorter
  forms are recorded in the mapping CSV. This preserves current native names;
  it does not add aliases to `Region.Find`.
- The five matching stock Mondain dungeon roots remain `DungeonRegion`, as in
  pinned Felucca. The two author entrance/exit Mondain regions retain their
  author type. Their travel restrictions and the hazard children require review
  before activation; registered placeholder classes are not proof of content
  fidelity.
- XML `logoutDelay active="false"` becomes `NoLogoutDelay: true`; rune names and
  explicit entrances are retained. Stock music is retained where a canonical
  stock name matches, and inherited music is explicit on children where present.
  Retained entrances are source coordinates, not surveyed destinations.
- Towns, dungeons, Mondain areas, no-housing areas, and jail use priority 60 so
  broad priority-50 wilderness does not mask them. Lodging and hazard children
  inherit their parent's priority. Lord British Castle and Blackthorn Castle use
  61; Green Acres remains 1. This is an explicit conversion choice for the
  overlapping author layout. `Region.CompareTo` compares priority, then child
  level (`Region.cs:251-252`); equal-priority, unrelated overlaps must not be
  relied upon to select a rule.
- The AcidRiver source row 87 has empty rectangles 9, 59, 122, 124, and 147.
  Their exact source attributes are in `region-review.json`. They cover no tiles
  and are omitted without expanding them.
- Vesper lodging source row 45 has two rectangles wholly outside Vesper's town
  footprint: x 2776-2791/y 952-983 and x 2768-2775/y 960-975, inclusive. They are
  omitted so a lodging child's parent lookup cannot grant guards outside the
  declared town. The other four lodging rectangles remain. This is a candidate
  rule-boundary correction, not proof that the omitted tiles are wilderness on
  the actual map.

## Differences from Trammel and Felucca rule choices

All target region maps and parent maps are `Felucca`. Felucca retains map index
and ID 0 and `FeluccaRules`; S2 changes its terrain file index to 1. Region JSON
does not set any of those map properties. Pinned `Map.cs:30-38` defines
`FeluccaRules = None`, while Trammel includes movement, beneficial, and harmful
restrictions. Copying town shapes does not copy Trammel's map protections. PvP
remains a map/game-system rule, including inside a guarded town; guards respond
to crimes rather than turning the town into Trammel.

There are **31 active TownRegion definitions**, including castle areas, and one
disabled town, Buccaneer's Den. These are definitions, not 31 separate towns.
Ordinary forests, seas, islands, caves, and dungeon roots have no guarded type or
guarded ancestor. Town lodging remains linked to its town. The child-footprint
review identified only the Vesper exception above.

Buccaneer's Den explicitly has `GuardsDisabled: true`, and its lodging is a
`BaseRegion`, not a fresh active `TownRegion`. `TownRegion` derives from
`GuardedRegion` (`TownRegion.cs:5`), and the disabled property is checked by
`GuardedRegion.IsDisabled` (`GuardedRegion.cs:33,50`). This avoids re-enabling
guards in an inn through a separately active child.

The old `Moongates` and `T2A Arena` GuardedRegions are omitted. P673 says to keep
stock Felucca guard behavior; this prompt explicitly calls for no guards outside
towns. This candidate follows the prompt, records the difference, and leaves
gate placement to S4. No old guarded gate rectangle is copied into wilderness.
Sea Market uses the author's Felucca `SeaMarketRegion`, not its Trammel
`TownRegion`, so it adds no outside-town guards. The native market class is a
TODO placeholder; no special market behavior is claimed.

The source marks additional places as towns. This candidate follows that
classification, including Plunderers Peak, Red Baron Stronghold, Red Dagger
Keep, Seraphim Peak, Skaddria Naddheim, and the source spelling `Viligant Valley`.
Their classification is an S13 review question, not a conclusion drawn from
their names. Other added town areas include Valunstead, Hammerhill, Kameron
Kove, Elmhaven, Kettleburg, Fort Yondall, and Elandrim Nur Shaz. The complete
guarded set is identified by type and `GuardsDisabled` in the native array.

Haven is a special unresolved case. The author supplies a broad unguarded
`NoHousingRegion`, and no guarded town core. Stock Felucca's Ocllo is guarded.
This candidate keeps the broad Haven area unguarded rather than extending
guards across its island. S7/S13 must add a verified town-sized guarded region
and reconcile the Haven/Ocllo/New Haven names. The source's ServUO
`smartNoHousing` property has no directly copied native property; native housing
semantics need review, not an invented JSON switch.

Dungeon definitions carry native dungeon light and housing behavior
(`DungeonRegion.cs:25-32`). Felucca also loses the dungeon stuck-menu option
through that existing map check. `DungeonRegion` alone does not implement every
travel ban or seal a new dungeon. S14 must provide seals and unfinished-area
fences, and S18 must provide spawns and opening proofs. Embedded author spawn
objects are not emitted as imaginary region JSON properties.

## Champion areas

`champion-areas.json` lists all **17** pinned entries: 12 `LLChampionSpawn` and
five `DungeonChampionSpawn`, with their complete coordinates. The five fixed
dungeon types are UnholyTerror, VerminHorde, ColdBlood, Abyss, and Arachnid. The
last LL entry is ForestLord; the other LL entries randomize their type.

P669 grades only the altar points: 11 unchanged, three moves, three rework. Its
summary does not say which individual altar got which grade, and it does not
grade an entire spawn area or its ejection location. No per-entry terrain grade
has been invented here.

Pinned `ChampionSpawn.SetInitialSpawnArea` uses x/y minus 24 through x/y plus 24,
with exclusive ends: a **48 by 48** rectangle. Those stock default rectangles
are included for review. They have **zero geometric overlaps with the candidate
active town guard rectangles**. The candidate active town rectangles also have
zero overlaps with the candidate DungeonRegion/MondainRegion rectangles. These
are geometric comparisons, not terrain or gameplay proofs.

`ChampionSpawn.UpdateRegion` creates and registers `ChampionSpawnRegion` at
runtime; its parent is `Region.Find` at the altar. This type is not registered
for region JSON. A static BaseRegion with a champion name would not reproduce
its activation, housing, or other behavior. No such substitute was added.
S12 must finalize the altar, ejection point, and whole spawn footprint on SoS,
then repeat the guard check with the final S13 regions and verify the runtime
parent. This data does not move or activate a champion.

## Open questions and limits for S13

1. Reconcile the full town, dungeon, name, and priority mapping with P692/S3 once
   that output lands. Shared geography should have one approved shape per place,
   with explicit Felucca rule differences.
2. Supply Haven's guarded town core through S7. Decide how Ocllo's old name and
   lodging map to it. Do not guard the author's entire broad Haven region.
3. Review the 47 named stock regions and Ocllo lodging with no verified author
   replacement, including housing and name consumers. Their individual source
   rows are in `stock-felucca-mapping.csv`.
4. Confirm the added town classifications, the outside-town gate/arena guard
   retirement, and the priority choices above. Those choices are visible data,
   not changes applied to the server.
5. Resolve staff go points. `region-review.json` lists 44 definitions with no
   supplied/contained source anchor, including unnamed child regions. It also
   lists ten retained author go points outside their own region: Fire, Ice,
   Misc Dungeons, Blackthorn Castle, Shrine of Chaos, Shrine of Honesty,
   Shrine of Honor, Shrine of Justice, Shrine of Sacrifice, and Shrine of
   Spirituality. They are retained as evidence, not approved staff destinations.
   The native loader does not reproduce ServUO's automatic map-average-Z center
   calculation; do not use omitted GoLocation values as valid destinations.
6. Resolve author entrances against the final S4/S7 routes. No MULs were present
   at this work copy's P481 scratch SoS map path. Dry land, statics, walls,
   walkability, terrain Z, and client appearance are **unverified**.
7. Review hazard children and the two Mondain entrance/exit regions. Native
   damage-region classes are marked TODO in pinned source; some inherit travel
   restrictions even where damage effects are unimplemented. Registration is
   not proof of equivalent ServUO behavior. No hazard subsystem was ported.
8. Validate named lookups and runtime region overlays in S13. The review JSON
   includes literal lookup candidates from canonical code with both candidate
   and pinned-name presence. The scan includes comments and other facets, and
   is explicitly not a resolved compatibility count. For example, fish code
   already uses some shorter Mondain names than pinned native regions. Preserve
   the pinned names here and review those existing consumers separately.
9. Coordinate S2's Fold mirror relocation/twin, S12's final champions, and S14's
   fences and seals. Ordinary no-housing regions do not perform turnback or
   dungeon sealing behavior. These runtime systems were not reimplemented here.

## Validation and handoff

No lane tests or build were requested for this data-only task. No persistent
test or script was added. Windows PowerShell 5.1 was confirmed as 5.1.26100.9711;
inline Python 3.12.10 performed the data conversion and checks.

The same inline data check was run before and after writing the artifacts.
Before: exit 1, FileNotFoundError for `felucca-regions.json`. After: exit 0. It
checks native property names and registered types, Felucca maps and parents,
earlier parent definitions, unique names, nonempty bounded rectangles, explicit
Z bounds, Buccaneer's Den disabled guards, no external GuardedRegion types,
150 source mappings, all 107 stock dispositions, and all 17 champion areas
without active guard overlaps. This is structural validation only. Native .NET
deserialization, server startup, live guard behavior, PvP, housing, travel, and
client movement remain unverified and belong to S13's build/runtime proof.

An additional negative probe changed the first map to Trammel in memory only.
The same check exited 1 with an assertion at row 0; rerunning against the
unchanged files exited 0. A separate source comparison confirmed that every
target rectangle exactly equals its author rectangle except the seven recorded
omissions, and all recorded source fingerprints still match. No region
geometry was redrawn by guessing coordinates.

`tools/progress.py --dry-run` ran with `SL_SHARD` and `SL_MIGRATE` pointing at
these two work copies and exited 0. It reported the existing filename-based
port-list snapshot, 833/983, and setup 7/7. That report does not measure SoS
region readiness; no port or progress-state change is claimed. The helper's
documented dry-run is not fully read-only: `progress.py:722` writes
`tools/progress.json` inside `build()`, before the dry-run return at `:737`.
The generated snapshot change was inspected and restored to its clean starting
version. This is an existing tooling defect, outside this data-only task; it
was recorded here rather than fixed in code.

Final scope: five data files listed above, this designated note, and the shorter
task-brief notes path as a pointer to this note. Every new file is below 5 MB;
the largest is `felucca-regions.json` at 195,120 bytes. The new text contains no
em dashes. The code work copy is unchanged. Haven was never contacted, nothing
was deployed, and no commit, merge, push, or branch switch was performed. Stop
requests were checked between steps and none was present at final review.

P693 DONE
