# P699: review of P673's Sosaria swap plan

Codex lane, 2026-10-27. Review only. Chase's choice to replace both facets stands.

**Finding:** S1, S2, S3, S7 and S8 are not a sufficient playable go-live set as written. They can be an integration build kept closed to ordinary players. Opening that build needs the travel, Felucca rules, world regeneration and closure work below. Site A is a reasonable proposed home for the isle, with qualifications below. The plan needs clearer ownership and smaller work units before implementation starts.

Severity: **Blocker** prevents opening the swapped test shard to players. **High** needs an assigned fix before the affected feature opens or before 1.0. **Medium** needs a corrected requirement or estimate. These are review recommendations, not new approvals or changes to P673.

Paths beginning `server/`, `docker/` or `player-package/` refer to the code work copy. Pinned source references are under `D:\UO\ModernUO-pinned`, verified at `d4531cd94b739613155225c234900de9f47d2c88`. Other paths refer to this notes repo.

## Release blockers

### R1. The initial release leaves known unsafe content enabled

**Severity: Blocker. Affects the go-live set and S4, S5, S9, S12, S13, S14, S15, S16.**

P673 itself places unsafe gates and teleporters in S4, displaced decoration in S5, stock spawns in S9, champions in S12, Felucca regions in S13 and seals in S14. Those follow player access. Both facets change on day one. S3 protects only Trammel. A player can cross a public gate into the wrong terrain or enter an unsealed dungeon before the later waves fix it. Retaining stock spawners also leaves monsters and vendors on the old map. These are explicit deferred responsibilities in P673, not newly inferred terrain failures.

**Fix:** either keep ordinary players out until these safety portions are integrated, or include them in the atomic opening: S4 travel repairs, removal or correction of unsafe S5/S9 placements, S12 repair or disablement, S13 rules, S14 closures and a small S15 route smoke check. New population and cosmetic work can follow only in areas made safe first. Put credits from S16 in the first distributed package. P673 says credit precedes player access but schedules S16 at the 1.0 gate, after test-shard access.

### R2. There is no owned conversion of the existing test world

**Severity: Blocker. Affects S2, S7, S8 and the swap opening.**

The final questions offer preserving characters and banks or a fresh test world. The preservation option also moves characters, deeds houses and regenerates world items. No S prompt owns that whole operation. Editing cfg/JSON and seed locations does not retarget saved items. For example, `ClusterFNewHavenServicesSeeder.cs:224` explicitly describes a seeder that moves nothing; `ClusterFRootdeepSeeder.cs:106-121` builds entrance teleporters, while its startup check at line 198 checks map availability rather than performing a town relocation. S8's Blackthorn deletion addresses only one part.

**Fix:** add an explicit swap procedure, conditional on Chase's recorded choice. For preservation, inventory and handle offline logout positions, pets, boats, houses and house contents, runes/runebooks, existing treasure maps/SOS targets, custom seeders and generated stock content. Define what is retained, moved, invalidated or replaced. Rehearse against a disposable save copy, with repeatability, backup and rollback proof. For a fresh test world, define the retained account/character policy explicitly. Do not silently interpret a recommendation in P673 as authorization. Release the matching package, overlay, image/configuration and save as one versioned set; rollback must restore the corresponding set too.

### R3. S1 cannot keep Gate 4 unchanged

**Severity: Blocker. Affects S1.**

S1.6 says the existing no-EA-files gate still holds while S1 ships full map assets. `player-package/Build-PlayerPackage.ps1:463-469` rejects every `.mul`, `.uop`, `.idx` and `.def`, rejects EA filenames, and rejects shipped `app/uo-overrides/` files. A third-party attribution does not change those checks. The payload README at line 128 still makes the blanket statement. This is a concrete build-contract contradiction, not a conclusion about legal rights.

**Fix:** state an explicit, narrow map-vendor exception consistent with Chase's whole-map choice. Preserve the general prohibition, allow only the named assets with expected hashes and provenance, and update the gate, its tests and package wording together. Prove an unrelated or altered map still fails. Record the governing policy change for overseer promotion; this lane must not edit `docs/`.

### R4. A package version file is not yet a server admission mechanism

**Severity: Blocker. Affects S1 and server ownership.**

S1.5 requires the server to refuse an old package, but assigns the work to package/client only and specifies no signal the server receives. The current `app/package-version.txt` is read by the launcher/updater (`Play.ps1:264`, `Update.ps1:231-239`). That local stamp alone cannot tell the server which map an already running client draws. An unchanged UO executable version cannot distinguish the two packages either.

**Fix:** give the server side an owner and specify how the required map/package revision is reported and enforced before world entry. Acceptance must cover an old package, a direct client launch, an already running old client and a partly updated install. Check that the current package's map build actually succeeded before admitting it. A launcher update check alone does not meet the stated server refusal requirement.

## Missing coverage and implementation risks

### R5. S2 has the map-reader precedence backwards and needs stronger parity proof

**Severity: Blocker. Affects S1, S2, P662.**

Pinned `Projects/Server/TileMatrix/TileMatrix.cs:100-124` tries `map1.mul` before `map1LegacyMUL.uop`. S2 asks to check UOP before MUL. If the pristine SoS MUL is findable while mapops changes exist only in the UOP overlay, the server can read unpatched land and patched statics. `Build-MapOverlay.ps1` currently calls the package applier, which writes a UOP. Directory precedence alone does not resolve competing file formats with different names.

Also, `Map.cs:62,78,96-105` makes the file index readonly and derives `Map.Felucca` from `Maps[0]`. Replacing Felucca after `MapLoader.Configure` must replace its entry in `Map.AllMaps`, not append another map with index 0 (`MapLoader.cs:104-118`). The Fold example adds previously unused maps and is not a complete replacement recipe.

**Fix:** choose one authoritative post-mapops land representation and ensure an unpatched MUL cannot shadow it. Verify resolved paths and resulting tile/static content, including Burrows and isle edits, on Trammel, Felucca and the Fold. Add map-registry uniqueness and preserved id/index/rules/season checks. Include vendor hashes, patch revision, applier revision and both generated client maps in stamp invalidation. Test a stale map0 output and an interrupted rebuild. Three scenic client shots do not establish full client/server parity.

### R6. The assessment omits stock C# travel and recovery tables

**Severity: Blocker for recovery/travel; High for other omitted systems. Affects S4, S7, S8, S12.**

`cc-P669-tools/geo.py:stock_points` reads selected data files and PMList. Its general C# scan reads our customizations and patches, not pinned stock C#. Confirmed unassigned source tables include:

| Source under pinned `Projects/UOContent/` | Actual consumer and required owner |
|---|---|
| `Engines/Help/StuckMenu.cs:25-122,290-310` | Fixed recovery destinations, followed by direct player/pet movement on either facet or return from other facets. Assign to S4/S8 before opening. |
| `Mobiles/PlayerMobile.cs:104-121,4078-4129` | Young death recovery destinations. Dungeon `Entrance` selects the starting point for choosing a recovery site. Assign to S7/S8. |
| `Mobiles/Special/Harrower.cs:15-31,121-134` | Separate boss and gate destinations on Felucca. Moving `GenChamps.cs` altars alone does not cover these. Assign to S12. |

These omissions are confirmed in source. Their individual SoS terrain grades are **unverified** here, so this is not a claim that every destination is broken. Region `Entrance`, `GoLocation`, height ranges, parent, priority and specialized behavior also need review, not just rectangle centers or preserved names. `Regions/DungeonRegion.cs:24` exposes the entrance consumed by Young recovery.

**Fix:** add a stock C# and data-consumer inventory before declaring the coordinate work complete. Include quest generators, conditional systems such as factions, and cross-facet destinations into Trammel/Felucca. For each consumer, publish the file and disposition: checked, moved, disabled or intentionally retained. Keep optional systems closed if their checks are deferred. Add recovery from death and Help/Stuck to S17, including a return from an unchanged facet.

### R7. Our coordinate scan misses real placement tables

**Severity: High, with S7 portions required for opening. Affects S7/S8 estimates.**

P669's regexes do not generally read target-typed `new(...)`, named records with coordinates after strings, constant ranges or coordinates assembled from fields. Concrete counterexamples:

- `server/customizations/ClusterFGuildStarterPath.cs:216,228,242` places a mine liaison, artificer and lookout using `GuildLocation` rows. P669's `geo-files.csv` reports that file as only two unchanged points. Those are not an inventory of its placements.
- `server/customizations/ClusterFNewHavenServicesSeeder.cs:90-190` contains decoration rows such as doors, forges and signs. P669 reports only one point in the file. S7 lists the seeder, but the assessment understates its work and S5 can duplicate its fittings.
- `server/customizations/ClusterFRootdeepSeeder.cs:82-121` defines the mouth, the generated downward teleporters and the ladder's return destination. S7 names the region and stock-spawn filter, but does not explicitly assign this actual entrance seeder. Changing `OldHavenBurrowsRegion.HoleEntrance` alone leaves these constants and generated items behind.

**Fix:** enumerate evaluated placement rows and ranges, preferably through the data-producing methods, with source provenance and facet. Include guild directory arrows and the actual NPCs they point to, seeder idempotency and relevant fixtures. Give S7 the complete Rootdeep entrance/exit conversion. Recount the work from that inventory instead of treating P669's literals as the complete custom surface. P669 also grades patch text and infers a facet for a whole file, so its counts are triage figures, not unique live-object counts.

### R8. Reusing Old Haven changes quest meaning and cleanup behavior

**Severity: High, with town safety required for opening. Affects S7/S9.**

Moving the start and changing an achievement does not relocate Old Haven training. Pinned `Engines/ML Quests/Definitions/NewHavenSkillTraining.cs:10-27` gives Cleansing Old Haven its localized directions and accelerated gain objective. Our `Regions/ApprenticeTraining.cs` binds training regions to those quests. `ClusterFOldHavenStockSpawns.cs:40-41` still refuses the town crier, and `ClusterFOldHavenCleanup.cs:111-121` identifies the future town area for vendor/spawner cleanup. These live behaviors were written for ruins, not an inhabited start town.

**Fix:** choose the new training/undead area and move the relevant objectives, region rules, spawns, directions and return path together. Retire or retarget ruin cleanup commands and the crier exclusion. Ensure regenerated undead do not populate the new guarded town by accident. Prove a trainer quest through completion, accelerated gain in its intended area, death recovery and return to the trainer. Give this work a separate S7 subprompt rather than hiding it under relocation.

### R9. Shared terrain creates unowned mirrors beyond the isle

**Severity: High. Affects S2, S7, S13 and the isle.**

S2 correctly adds a Felucca Fold mirror, but `FoldRegions.cs:124-129` currently refuses to send home anything not on Trammel. A second registered region alone will not make that code protect Felucca. Its `Home` already reads CharacterCreation dynamically; it is not a separate hard-coded 3503,2574 destination needing another edit.

The retained Burrows mapops also appears on Felucca when file index 1 is shared. `OldHavenBurrowsRegion.cs:61` and `ClusterFRootdeepSeeder.cs` supply Trammel-only rules and items. P673 does not say whether the Felucca copy is inaccessible or playable. Housing, travel and player escape need a disposition even if no intended gate goes there.

**Fix:** make the mirror's containment and send-home logic facet-aware, with player and pet checks on both facets and staff exemptions. Explicitly close the Felucca Burrows copy or supply its intended rules and population. Inventory all private painted areas shared by the file so this does not recur with future Fold zones.

### R10. The waves do not actually own disjoint files or have complete inputs

**Severity: High. Affects S1/S2/S3/S7/S13/S14/P662.**

S1 owns the applier and rebased-patch consumption while S2 owns the rebase and overlay. Each requires client/server proof with the other's output. S3 redraws New Haven before S7 selects its final layout; S7 then redraws the same regions. S3 needs S14's no-housing list, while S14 runs later. S2, S7, S14 and P662 can all change `trammel.mapops`. P673 both says P662 ships with S1 and orders it after S2. Build locks do not resolve overlapping edits or inconsistent artifact revisions.

**Fix:** agree the vendor manifest, file layout, `HavenSpots` interface, region ownership and closure inventory first. Build against those contracts, then run one integration proof after the paired outputs exist. Give one owner each mapops revision and serialize rebase, hatch, isle and seam changes. S7 should choose coordinates; S3/S13 should consume them and own region data. Rewrite the wave table around those actual dependencies, with a coordinated activation after integration rather than a per-prompt deploy.

### R11. S6 needs a facet conversion and a real closure inventory

**Severity: High. Safety portion belongs before opening; conversion before S18.**

The author data explicitly names `MapDest=Trammel`, including the Agurast entrance and exit (`notes/sos-author-data/SOS-Trammel-Dungeons.cfg:9-45`). Copying that data onto Felucca without changing destinations sends players to Trammel. The final line is also an unplaced template teleporter to 0,0,0, not a live decoration placement. The description "775 lines" is file length, not the number of objects to port.

S6 withholds author entrance teleporters and S14 fences walk-in entrances. Neither establishes that stock teleporters, generated gates, existing runes or travel spells cannot reach the closed interiors. A seal at a doorway alone does not cover those paths.

**Fix:** produce explicit per-facet objects and destination maps, omit template-only records, and test same-facet entry and return. Maintain one dungeon status inventory with all inbound paths and a safe way out. Enforce closures at the destination where necessary, including recall/gate/teleport, on both facets. S4, S6, S14 and S18 must consume that same inventory. Verify player rejection, not just the existence of a fence region. Assign Elandrim Nur Shaz people or an explicit closure too: S3 lists it as a guarded new town, while S10's population list omits it.

### R12. Geometric grading is not an acceptance test for usable placements

**Severity: High. Affects S3/S4/S5/S8/S9/S15/S17.**

P669's `Grader.grade` takes x/y only. Its impassable-static mask ignores vertical clearance, and it compares land Z with stock rather than validating the object's specified Z. It cannot decide whether a door is on a useful floor, a forge is reachable, an NPC is behind a counter or a dungeon passage connects. A dry/open/within-five-Z fact over unchanged literals in S8 would preserve some wrong placements. Stock-looking surroundings also do not prove the associated dynamic decoration is still needed; SoS may already supply the fitting as a static.

**Fix:** use the grader to prioritize inspection. Acceptance should use pinned movement/fit semantics at the intended elevation, include dynamic decoration, and check a reachable approach and intended function. Check doors through opening/closing, banks and vendors through use, and paired teleporters through a round trip. Resolve static/dynamic duplicates between S5, S6 and S7. For spawners distinguish home, spawn bounds and wandering range, and water/flying creatures, rather than requiring every range tile to be dry. Move a small critical-path walk check before release; retain S15's full survey later.

## Isle re-site and task size

### R13. Site A fits the recorded box, but its clearance and future-space claims need qualification

**Severity: Medium. Affects S2/P662 and later Fold zones.**

The shift (+424,+1992) is divisible by eight and yields the stated box 6594-6865,3905-4049. It preserves positions within map blocks. This supports a constant shift in the generator. It does not make the box edges block-aligned or establish future room layouts.

`cc-P673-tools/sitefind.py:box_sum` explicitly clips off-map area and counts it as empty. Thus `sitecheck.json`'s 161-tile clearance is distance to content, not an in-bounds buffer on every side. The south edge has 46 tiles left. The plan's table does disclose that, but "clear all round" overstates the result. `sitecheck.py` checks the isle box and sampled P669 points; it does not separately validate every future zone's access, vertical bounds or reserved-view margin. The point corpus is incomplete as R6/R7 show.

**Fix:** keep site A provisional, without rerunning the whole location decision. Check in-bounds margins explicitly, reserve future rectangles, include their own sea/wall/view margins, and verify against final region and inbound-travel inventories. Use exclusive rectangle ends 7168 and 4096 for the proposed whole-room mirror. Generate shifted stops, tests, command help and screenshots from one coordinate contract. After P662, prove the beach/dock surface and a complete tutorial route on a Fold copy. Before P662 there is void at the beach, so S2 must test tile selection and mirror behavior without asserting that an ordinary player can stand there.

### R14. Several S labels are workstreams, not one-session prompts

**Severity: High for scheduling.**

The following split is recommended from inspected responsibilities, not measured implementation times. Each unit needs its own bounded file/area list, failing-first gates where new checks are added, and build or client proof as appropriate.

| Label | Why the session estimate is weak | Suggested split |
|---|---|---|
| S1 | Vendor acquisition, gate exception, UOP packing, PS applier, updater/stamps, admission protocol and client timing | Asset/packer; launcher/update; server admission and integrated client proof. |
| S3/S13 | Region geometry plus specialized rules, training, docks, closures and both facets | Shared inventory/tooling, then named geographic groups with one region-data owner. |
| S4 | Gate placement, paired teleporter repair and staff menu conversion | Public gates; teleporter groups; staff menu. Prioritize player safety. |
| S5 | Semantic building matching and manual door validation cannot be inferred from bulk x/y grading | Triage/report tool, then town/dungeon batches with explicit dispositions. |
| S7 | Start/services, guild placements, training meaning, Rootdeep hatch, cliloc and isle integration | Coordinate contract and start; town services/guilds/training; Rootdeep connection; integration proof. |
| S8 | Different later dungeons, artifact tables and unrelated custom layouts | Blackthorn retirement; each affected dungeon; remaining named seeders/layouts. |
| S9/S10 | Vendors, wildlife and new terrain have different placement rules and large review surfaces | Existing towns first, then wilderness/dungeons; new towns individually and new-land habitat batches. |
| S14/S15 | Closures, artistic seam repair, whole-map movement analysis and bot repairs are separate jobs | Closure safety first; seam batches; movement tool and survey; bot route repairs. |
| S17 | A failed playthrough can create repairs across every preceding owner | Keep a final integration gate, with a repair/retest loop and a final passing log required. |

**Fix:** describe S1-S19 as workstreams and count executable prompts after splitting. S18 and S19 already promise repeated area prompts, so nineteen labels do not mean nineteen build sessions. This does not require changing the chosen scope.

### R15. S11's random-water proof can pass without proving a usable SOS location

**Severity: Medium. Affects S11/S15.**

Pinned `Items/Skill Items/Fishing/Misc/SOS.cs:23,175-220` samples the surface rectangle, tries at most fifty times, checks land water IDs and returns `Point3D.Zero` on exhaustion. The isle at x 6594 and beyond is outside that sampling rectangle, so asserting no pick lands inside it is vacuous for those facets. One thousand random successes also do not prove sailing access around the new landmass.

**Fix:** explicitly reject/handle the zero sentinel, use repeatable sampling, and check that accepted targets are reachable by boat in the intended water component. Add a dock-to-water route and return, not just a floating-at-dock test. Report sampling as sampling, with its limits. Existing saved SOS targets belong to R2 rather than this generation test.

## Recommended release sequence

1. Record answers to P673's outstanding choices before implementing their dependent branches. This review does not select answers for Chase.
2. Establish asset/package policy, map identity, coordinate and ownership contracts. Expand the coordinate inventory to stock consumers and evaluated custom tables.
3. Build S1/S2 together in a disposable environment, then integrate the isle patch in the agreed mapops order. Verify exact server/client output selection before relying on region tests.
4. Integrate S3/S7/S8, Felucca rules and the travel, placement and closure safety portions identified in R1. Rehearse the selected world procedure. Keep player access closed until this passes on the final artifact set.
5. Open only verified or explicitly gated areas. Complete population, treasure, remaining geographic batches and full route surveys before 1.0.
6. S17 must end in a passing playthrough after repairs, including recovery, both facets, a Fold tutorial copy, trainer completion and restart/save reload. A list assigning failures is useful evidence but is not the release gate passing. Keep unopened S18/S19 areas closed on both facets.

## Evidence and limits

Read both work-copy AGENTS files, the governing document index, direction record and task list; P673 and P669; P669's coordinate collector and CSV reports; P673's site tools and saved outputs; the author's region XML, location XML and dungeon cfg as reference data; and the code/pinned sources cited above. Author credit remains Zigholtul. No third-party code was executed.

No code or map assets changed. No builds, new tests, client sessions, save conversion, deployment or Haven connections were performed. Lane tests are none for this notes-only review. Source behavior and planning contradictions are verified by reading; actual SoS grades for the newly identified coordinates, path connectivity, client overrides, admission behavior and conversion outcomes remain unverified. The raw SoS files were not available in this work copy's P481 scratch folder, so the recorded site scan was inspected, not independently repeated. P669's published measurements are attributed assessment inputs, not remeasured totals here. New numeric site statements above are arithmetic on the recorded coordinates.

The companion `cc-P699-review-p673-plan.md` records this lane's scope and final preflight.

P699 DONE
