# cc-P13: grove tracking brought forward; canonical writes WoodDiscoveryEntry v1

Brief: `cc-P13` (pasted). Nothing is committed, deployed, restarted or retagged for live. `docs/`,
`docker/uo/docker-compose.yml` and `server/uo/modernuo/Projects/` were not edited. The stale tree was
read, not written.

Changes in `D:\ShatteredLegacy`'s working tree (four files, uncommitted):

| File | Change |
|---|---|
| `server/customizations/WoodDiscoveryEntry.cs` | `WoodLocationRecord` added; entry keeps a grove list; **writes v1**; reader keeps groves instead of collapsing them |
| `server/customizations/ClusterFLumberjackingExtension.cs` | Chop hook records facet, region and point on first find, and again on every later find |
| `server/customizations/ForestersLogbookGump.cs` | Grove count per entry, one line per grove, footer shows groves |
| `server/tests/Misc/AccountDataSerializerVerification.cs` | P11's file extended: 3 facts updated, 4 added (7 total) |

**Result:** red 260/265 against a mutant, then green **265/265** through `docker/uo/build.sh`. Image
`sl-modernuo:cc-p13-grove` built. **`sl-modernuo:latest` was deliberately not moved**; its ID is
`16b0f49e6828…` before and after.

## 0. Corrections to the brief

- **P11's work was not uncommitted.** Both `WoodDiscoveryEntry.cs` and
  `AccountDataSerializerVerification.cs` were committed in `cd64314` ("Shard work, 2026-09-30 08:09"),
  and `D:\ShatteredLegacy`'s tree was clean when I started. I built on that commit; nothing was reverted.
- **The canonical files are not under `Misc/`.** They sit flat in `server/customizations/`. Only the
  test file is under `Misc/`.
- The repo holding `server/` and `docker/` is `D:\ShatteredLegacy`, not this one.

## 1. What differs from the June tree, and why

Compared with `diff -w --strip-trailing-cr` against `server/uo/modernuo/Projects/UOContent/Misc/`.

**`OutridersGuildmaster.cs` and `ResourceInfo.cs` are not part of this feature.** Each differs only in
the length of a `// ── … ──` comment rule. They contain no code difference, so they were not pulled in.

**The data model is June's, unchanged on the wire.** `WoodLocationRecord` is `(FacetName, RegionName,
Point3D, DateTime, AmountChopped)` in that order, and v1 is WoodKey + TotalChopped + State + count +
records. The proof is that the live save's 276 bytes re-serialise **byte for byte** (fact 2). A save
written by the June build or by this one reads under either.

Things I changed from June, each for a concrete reason:

1. **Grove merging checks facet and region.** June's `FindNearbyLocation` compares X/Y only. A chop at
   (1000,1000) on Felucca merged into a Trammel grove at the same coordinates. The migrated `Unknown`
   grove sits at (0,0), so a chop near the origin on any facet merged into it too. Either case gives a
   record whose facet is wrong for chops counted under it, which matters once the record is a
   teleport target. Canonical `OreDiscoveryEntry.FindNearbyLocation` has the **same facet-blind bug**
   (`OreDiscoveryEntry.cs:142`). I did not touch it: out of scope. **Proposed bug-list row**, ours to fix.
2. **Region labels are honest.** June (and today's ore hook, `CompactOreSatchelRoutingHook.cs:223-224`)
   label any unnamed region "Wilderness". Pinned `HouseRegion` is constructed with a `null` name
   (`UOContent/Regions/HouseRegion.cs:18`), so June logged a chop inside a house as Wilderness.
   `WoodLocationRecord.RegionLabel` now gives: the region's name if it has one; "Wilderness" only for
   the facet's default region (`Region.IsDefault`, `Server/Regions/Region.cs:228`); otherwise the
   region's **type name**, e.g. `HouseRegion`. Parents are not walked, because a named town would hide
   an unnamed house inside it. `Mobile.Region` is never null (`Mobile.cs:1551`).
3. **`FirstFound` is the earliest grove, not `Locations[0]`.** That is P11's reader semantics. Groves
   are appended in time order, so the two agree today. The earliest-grove rule stays right if a list
   is ever reordered.
4. **A null map records the `Unknown` sentinel**, not a made-up facet. Harvesting with a null map
   should not happen; if it does, the record reads as "no known location".
5. **Gump:** each entry keeps its "first cut / first found" date and total, and gains a grove count
   and one line per grove, as in June. The footer shows groves in place of total chopped, as in June.
   The longer label would collide with the Discovery Report button at `W - 210`. Groves with no known
   location print "location not recorded" instead of June's "Unknown, Unknown | (unknown location)".
   The grove lines put coordinates in front of players, as June did while it was live.

Every call the hook makes was checked against pinned `7c9215d97`: `Map.Name` (`Server/Maps/Map.cs:127`),
`Region.Name`/`IsDefault` (`Region.cs:202,228`), `Mobile.Region`, `Point3D.Zero`, and
`IGenericReader.ReadPoint3D`/`IGenericWriter.Write(Point3D)`. The last pair is already used by
`OreLocationRecord`. Callers of `WoodDiscoveryEntry` in canonical today: `ClusterFAccountData`
(serialise), `ClusterFLumberjackingExtension`, `ClusterFWorkOrderSystem`, `ForestersGuildmasterGump`,
`ForestersLogbookGump`, `ForestersLogbook` (comment). Only the lumberjacking hook and the logbook gump
use anything other than `State`/`TotalChopped`. `FirstFound` was get-only before and has no writer
outside the entry. No admin seed command exists for wood (there is one for ore at
`ClusterFCompactAdminTools.cs:398`).

## 2. Versions

- **Written: 1.** P11's "stays 0 for the rollback image" comment is removed; the reason it gave is void.
- **Read: 0 and 1.** v0 is read forward as one `("Unknown", "Unknown", Point3D.Zero, FirstFound,
  TotalChopped)` grove, June's migration. v1 is read and **kept**. Any other version throws
  `InvalidDataException`, which is P11's behaviour, unchanged.
- **Consequence:** the rollback image `f390c877` still reads what this writes (same v1). **Images built
  from canonical before this change cannot** (`bc04a35bf344` `uo-modernuo:latest`, `sl-modernuo:latest`,
  `setcomplete`). Their v0-only or P11 readers will either misread or collapse. Any world saved by a
  P13 build must not be loaded by a pre-P13 image. That is D29/D40's mechanism again, pointed the
  other way.

## 3. Tests: red, then green

Every fact is in `AccountDataSerializerVerification`, namespace `ShatteredLegacy.Tests`.

| # | Fact | Mutant (red) | Real code |
|---|---|---|---|
| 1 | `AnAccountWithEveryCollectionNonEmptySurvivesAWriteAndARead`: now with Ironwood in **3 groves on 3 facets** and Starwood in 1; every grove field compared, bytes read == written | **FAIL** `Expected: 3 Actual: 1` | PASS |
| 2 | `TheWoodDiscoveriesThatStoppedTheLiveShardReadBackToTheLastByte`: live bytes keep their `Unknown` groves; re-written they are **version 1 and byte-identical to the save** | **FAIL** version `Expected: 1 Actual: 0` | PASS |
| 3 | `AWoodDiscoveryEntryOfAnUnknownVersionFailsLoudly` (P11's, unchanged) | pass | PASS |
| 4 | `AWoodTypeFoundInSeveralGrovesRoundTripsAsVersion1`: first int written is 1; every field of 3 groves; sub-second ticks; negative Z | **FAIL** `Expected: 1 Actual: 0` | PASS |
| 5 | `AVersion0SaveReadsForwardAsOneUnknownGrove`: hand-written v0; one Unknown grove with the **old FirstFound ticks** and amount = TotalChopped; written back as 1 | **FAIL** `Expected: 1 Actual: 0` | PASS |
| 6 | `GrovesMergeOnlyOnTheSameFacetAndRegion`: 15-tile edge (221 in, 242 out); other facet, other region and the (0,0) Unknown grove never match | **FAIL** Trammel grove returned for Felucca | PASS |
| 7 | `RegionLabelsNeverCallAnUnnamedRegionWilderness` | pass | PASS |

**The mutant** was the real file with two changes: `Serialize` reverted to P11's v0 writer (version 0,
then `FirstFound`, groves dropped), which is exactly the constraint this task lifts; and June's
facet-blind merge. Run: `build.sh --tests-only`, **260/265, the five expected failures and no others**.
The file was then restored from a copy, `sha256sum -c` confirmed it (`f2314b59…`), and the full build
went green. Facts 3 and 7 pass under the mutant because neither mutation touches them; that is the
right result, not a gap.

Green: `bash docker/uo/build.sh -t sl-modernuo:cc-p13-grove` → `Built sl-modernuo:cc-p13-grove with
patches applied and 265 shard test(s) passing.` That is P11's 261 plus 4. Zero `warning CS` lines in
the log.

**Not tested:** the chop hook and the gump. The hook needs a `PlayerMobile` with an account on a real
facet, and test fixtures have no maps loaded. The hook's logic lives in the tested entry methods and
`RegionLabel`. What is untested is the wiring: that the hook passes `m.Map.Name`, `m.Region` and
`m.Location`. **In-client check proposed** (row below).

## 4. For whoever builds grove teleportation

This task did not build it: no command, no ledger tier. The data is **sufficient** for it:
`Map.TryParse(FacetName)` plus `Location`. What that feature must handle:

- **Teleporting to an arbitrary logged coordinate is a large gameplay power and an exploit surface.**
  The recorded `Location` is **where the player stood** when the log dropped, not where the tree is.
  A location logged inside a dungeon, a house, a guarded or no-recall area, or somewhere the player was
  carried or teleported to, is still a valid `Point3D`.
- **Gate on `RegionName`, which is now honest.** An unnamed non-default region is logged by type name
  (`HouseRegion`), never as Wilderness. Named regions carry their real name, so a dungeon grove says
  `Covetous`, not Wilderness. A sensible default is to allow only `Wilderness` and an allow-list of
  named outdoor regions, and to **re-check the destination at teleport time** (`Region.Find` plus the
  usual recall/travel checks), because houses get placed and regions change after the grove was logged.
- **`HasKnownLocation == false` means no destination.** Migrated v0 groves are `Unknown`/(0,0,0).
  `Map.Parse("Unknown")` **throws** (`Map.cs:1768-1805`); no facet is named Unknown (the seven are in
  `Distribution/Data/map-definitions.json`). Use `TryParse`, and refuse.
- The live world's four `CainUnAble` entries are all Unknown groves. Chase has ruled that world is not
  being kept, so this matters only for a world that started on a v0 build.

## 5. Proposed rows (not written to `docs/`)

- **`docs/bug-list.md`, ours to fix:** `OreDiscoveryEntry.FindNearbyLocation` ignores facet (and
  region). A vein on one facet absorbs ore mined at the same X/Y on another, and the (0,0) seed
  location absorbs anything near the origin. Evidence `OreDiscoveryEntry.cs:142-153`. Same fix as §1.1.
  The ore hook's "Wilderness" default (`CompactOreSatchelRoutingHook.cs:224`) also labels houses as
  wilderness. Low severity until ore locations are used for anything but display.
- **`docs/client-test-queue.md`:** chop a colored log on Trammel, then again within 15 tiles, then 20
  tiles away, then on Felucca at the same X/Y. The logbook shows 3 groves with the right facet, region
  and coordinates, and the first grove's amount is the sum of the first two chops.
- **D40's row:** P11's "writer stays v0" is superseded; canonical writes v1 as of P13.
- **Deploy caution (D29):** do not load a world saved by a P13 build on any pre-P13 image (§2).

## 6. Unverified

- No world save has been loaded on `sl-modernuo:cc-p13-grove`. P11 §5's open question stands: whether
  the rest of a June-written world loads on a September build.
- The gump's layout with many groves was not seen in a client. It sits in the same scrolling HTML
  area, 400 px tall, that June's version used.
- `tools/progress.py` was not run. It rewrites this repo's README block, and the brief confined me to
  `notes/` here.
