# P634: Town Houses, stage 1

Written 2026-10-26 by the Iron Golem (Claude Code). Builds the first stage of [cc-P409-town-houses-design.md](cc-P409-town-houses-design.md) as corrected by [cc-P550-review-town-houses-design.md](cc-P550-review-town-houses-design.md). Chase's decision (10-25 evening, `D:/UO/overseer/decisions-2026-10-23.md` 20:15 entry, "P550 ... Codex defaults"): weekly rent first with sublets; room tenants count toward the one-house entitlement; belongings protected; deadlines count server uptime.

## In plain words

- Players will not notice anything yet. On the test shard only, staff can now turn an empty town building into a "town house site" with `[Leaseholds new`, mark its doors with `[Leaseholds door`, and give a player a free test lease with `[Leaseholds assign`.
- With a test lease, the building works like the player's own house (house sign, locked house doors, lockdowns, friends, and it counts as the account's one house), while the town guards still answer inside it. `[Leaseholds end` gives the building back with its original town doors.
- There is no rent, no way for a player to lease, and no packing of belongings yet. Before ending a test lease, empty the house: whatever is still locked down is left loose in the building.
- Nothing for you to do now. The rent, the belongings crate, sublets and picking real buildings are the next stages (drafted at the end).

## Status

Done. The Iron Golem (Opus), branch `golem/Iron/P634` of both repos, not committed (the Golem commits). The gated build is green (section 4). No shard was started, no world command run, no site placed anywhere, no package built or published, nothing deployed, no Haven contact. The `docker-build` lock was held for the gated build only.

## 1. What "stage 1" means here

P409's build plan is L0 (pick buildings, a survey), L1 (leasehold core and staff tools), L2 (leasing and rent), L3 (sublets), L4 (guides), L5 (place the sites). L0 is a list, not something to play. The smallest playable slice is **L1**: the leasehold core with a staff test lease, built with the corrections P550 says L1 must carry (its corrections 1, 2, 5 and the decay half of 6).

| P550 correction | Stage 1 |
|---|---|
| 1. The region constructor patch is not enough (`m_Region` private, `Region` get-only) | Built as P550 recommends: a narrow virtual `CreateRegion` that stock `UpdateRegion` calls, so `BaseHouse` still owns the region (its `Region`, ban location and cleanup), plus a protected `HouseRegion` constructor with parent, priority and 3D area. |
| 2. Resizing an empty multi keeps zero bounds, so `FindHouseAt` fails outside the origin sector | Each leasehold builds its own component list through `MultiComponentList`'s public reader constructor, with real min and max and no tiles. A loaded item enters its map before its own fields are read (pinned `Item.Deserialize`), so after load the leasehold re-enters the map through `BaseMulti.ItemID`, the only public way to the map's sector lists. Proved across sector lines and after a save and load. |
| 5. A permanent site, separate from the disposable house, sign and doors; doors swapped only while leased | `ClusterFLeaseSite` is its own item at the street spot. Vacant, the building keeps its own town doors. Leased, each registered town door steps aside to the internal map, keeping its exact location, and a house door of the same art takes its place (a linked pair stays linked). When the leasehold goes, however it goes, the same doors come back. |
| 6. Lease expiry the only decay path | The leasehold is ageless by type (`DecayType` override), price 0, no deed (so a player's demolish is refused by the stock gump), no vendors. |

Settled calls applied: the leasehold counts as the account's one house (a real `BaseHouse` with an owner, and assignment checks `HasAccountHouse`). Inn and guild hall exclusion: a site is refused when any floor tile is in another region than the street spot, which refuses an inn's or bank's own child region and anything half out of town. A guild hall that is plain town region is not caught by that; L0's approved list is the guard there (draft A).

Left for later stages, each named in the drafts: rent, prepaid credit, grace, eviction and the belongings crate (L2); room rights, sublets and the room entitlement (L3); multi-rectangle buildings and the marker preview (L1b, draft B); the missing-parent recovery beyond a staff warning; the lease sign's own gump; the survey and data file.

## 2. What was added (ShatteredLegacy)

| File | What |
|---|---|
| `server/patches/BaseHouse-leasehold-region.patch` (new) | `BaseHouse.UpdateRegion` calls a new `protected virtual HouseRegion CreateRegion() => new HouseRegion(this)` and registers its result if not null (a leasehold mid-load answers null and updates again after). `HouseRegion` gains `protected HouseRegion(BaseHouse house, Region parent, int priority, Rectangle3D[] area)`. Stock houses build exactly the region they did before. Made against the assembled tree (`sl-uo-builder:cc-P632`; no shard patch touches either file), `--fuzz=0`. |
| `docker/uo/apply-patches.sh` | Registers it after `HousePlacement-climbed-tile.patch`, with its reason. |
| `server/customizations/Leaseholds/ClusterFLeasehold.cs` (new) | `ClusterFLeasehold : BaseHouse`: id 0x1DD6 (no client multi, P409's lookup), the footprint (`Components`, `IsInside` by the rectangle and the floor range, `Area`), `CreateRegion` (the region at the street spot, never a house region, as parent; `ParentMissing` when it is not the town the site was made in), ageless, price 0, no deed, no vendors, provisional storage (8 lockdowns per floor tile, 1 secure per 16), and `OnAfterDelete` telling the site. `ClusterFLeaseholdRegion : HouseRegion`. `ClusterFLeaseDoor : BaseHouseDoor`, made from a town door's art, sounds and offset. |
| `server/customizations/Leaseholds/ClusterFLeaseSite.cs` (new) | `ClusterFLeaseSite : Item` (invisible to players): rectangle, lowest and highest floor, the town region's name, the leasehold, the test-lease flag, the town doors. `WhyNotSite` (1 to 32 tiles each way, floors 0 to 60 apart, street spot outside, every floor tile in the street spot's region, no house, no other site overlapping, no creature, no spawner, moongate, teleporter or multi inside), `Create`, `AddDoor`, `WhyNotAssign` (vacant, a player, the account's one house, doors present and closed, the site checks again), `AssignTest`, `EndLease`, `OnLeaseholdDeleted`. `[Leaseholds new <lowest z> <highest z> \| door \| assign \| end \| list \| go <n> \| remove` (GameMaster, `CommandShard.TestOnly`). |
| `CHANGELOG.md`, `VERSION` | 2026.10.26.6 (P633, not yet merged here, took .5), one Staff line. |

## 3. Tests: red first, then green

`server/tests/Multis/LeaseholdVerification.cs`, 5 facts, in a test-made `GuardedRegion` "P634 Town" far from any loaded town:

1. `ALeaseholdIsAHouseInsideTheTownsGuards`: `BaseHouse.Region` is the leasehold region, its parent the town; a point inside finds it, `IsPartOf<HouseRegion>`, and `GetRegion<GuardedRegion>()` is the town; the street is still the town; a second `UpdateRegion` builds a new region with the same parent and the old one is gone. `HasAccountHouse` is true; ageless; price 0; no deed; no vendors; lockdowns above 0.
2. `FindHouseAtWorksAcrossSectorsAndOnlyBetweenTheFloors`: a 16 by 16 building crossing x 6016 and y 128: found at all four corners (one at the top floor) and the middle; not one tile outside each way, 1 below the lowest floor or 1 above the highest. A second, 4 by 6, leasehold finds only its own; their lists are separate; `MultiComponentList.Empty` stays width 0 with no tiles.
3. `TownDoorsStepAsideWhileLeasedAndComeBack`: a linked pair of town doors registered (a second registration refused); leased, each is on the internal map at its own spot, and a lease door of the same closed art stands there, finds the house, and is linked to its partner. Ended: the lease door is deleted, the town doors are back where they were, still linked. Leased again and the house deleted directly (as staff, a staff demolish or an account deletion would): the doors come back.
4. `UnsafeSitesAndSecondHousesAreRefused`: a street spot inside, an overlap, a creature inside, a building half out of the town; a leased site cannot be given again; a player whose account holds a leasehold cannot be given a second.
5. `SitesAndLeaseholdsSurviveSaveAndLoad`: the site round-trips its rectangle, floors, town, leasehold, test flag and door. The leasehold is saved, taken off the map, and read into a fresh object: it is found at the far corner (another sector) and at the origin, with its town-parented region.

Run on `sl-uo-builder:cc-P632` (this branch's base, merge `313d94d`) with the two sources and the fact file copied in, the patch applied with `patch -p1 --fuzz=0`, and `dotnet test` filtered with the gate's flags.

- **Red A, P409 as written** (mutant: the stock region with no parent, a per-instance copy of the empty list as its footprint, no re-entry after load, no door restore, no placement checks): all 5 failed. Fact 1 `Assert.IsType() Failure ... Expected: typeof(ClusterFLeaseholdRegion)`; facts 2, 3 and 5 `Assert.Same() Failure` at the first `FindHouseAt` off the origin sector; fact 4 `Assert.Contains() Failure: Sub-string not found`.
- **Red B, no re-entry after load only**: fact 5 alone failed (`Assert.Same() Failure` at the far corner after the load); the other 4 passed.
- **Red C, no door restore only**: fact 3 alone failed (`Expected: Trammel, Actual: Internal` for the town door after the lease ended).
- **Green**: 5 of 5.

The patch itself has no separate red: without it the leasehold does not compile (`CreateRegion` has nothing to override), which is not a behavioural failure. Red A is the behavioural proof that the region it enables is what fact 1 checks.

## 4. The gated build

The gate script (`docker/uo/` build script, `-t sl-modernuo:cc-P634`) under the `docker-build` lock: `[patches] All 168 patches applied successfully.` (the new one included), then the shard tests: total 2570, passed 2566, skipped 4, failed 0 (the 5 new facts among them), then the image. Last lines: `Built sl-modernuo:cc-P634 with patches applied and 2566 shard test(s) passing.` and `EXIT=0`. Lock released.

## 5. What I could not verify

- The client: that TazUO draws nothing for multi 0x1DD6, how the stock house sign and AOS house gump look on a leasehold, and lockdowns by speech in the building. No shard was started (draft A's acceptance).
- Real town buildings: the facts use a test region. Whether Britain's buildings, statics and floors suit single rectangles is L0's survey.
- A full world save and restart: the site and the leasehold round-trip through their own serializers in the test host, and the leasehold re-registers after its load; the world loader's order across a whole save was not exercised.
- The login handler: stock `HouseRegion.OnLogin` uses `FindHouseAt`, so it applies to a leasehold as to any house; not exercised.

Risks recorded for staff while it is test-only: ending a lease uses the stock house deletion, which unlocks lockdowns where they stand and destroys a secure strongbox (P550 correction 4); so empty a test house before ending it (CHANGELOG says so). A test tenant can transfer the house through the stock gump; L2 removes transfer.

## 6. Remaining stages as prompt drafts

For the overseer to number. All `Touches: server` unless stated; none may run at the same time as another (they share `server/customizations/Leaseholds/`). Keep everything test-shard only until draft E.

### Draft A: Town Houses survey and test-shard acceptance (L0)

**Model:** Opus

**Touches:** docs-only, map

**Summary:** P634 built the leasehold core and staff tools behind the test shard. Pick the buildings and try one in the client.

1. Read `notes/cc-P409-town-houses-design.md`, `notes/cc-P550-review-town-houses-design.md` and `notes/cc-P634-build-town-houses.md`.
2. Survey Britain first (then the other major towns): 2 to 4 empty buildings each, with rectangle, lowest and highest floor, street spot and doors, excluding inns, guild halls (F-49), banks, vendors' stands, services, streets and travel routes. Renders with the vseUOAware tools. A list for Chase to approve.
3. On a private scratch copy of the test world (test-shard lock; never Chases-Tower's live world), make one Britain site with `[Leaseholds`, give the Tester a test lease, and record in the packaged TazUO client: nothing drawn for the house, the sign and house gump, doors, lockdown by speech, guards called on a criminal act inside, a private house ejecting a stranger, login inside, end of lease restoring the doors.
4. Notes with screenshots; no code unless a defect is found, then a fix-up prompt draft.

### Draft B: Town Houses buildings of several rectangles, and the marker preview (L1b)

**Model:** Opus

**Touches:** server

**Summary:** Stage 1 sites are one rectangle. Let a site be several floor rectangles (an L-shaped shop, an upstairs) with a preview of the tiles that become private.

1. Read the P409 and P550 designs and P634's notes. Bump `ClusterFLeaseSite` and `ClusterFLeasehold` to version 1 with a list of rectangles (a migration file in `server/migrations/`), keeping version 0's single rectangle.
2. The footprint list spans all rectangles; `IsInside` and the region area are the union; placement checks every rectangle (one region, no overlap, nothing inside); `[Leaseholds new` takes rectangles until the staff member is done; hued markers show them before saving and are removed after.
3. Red-then-green facts: a building in two disconnected rectangles finds the house in both and not between; save and load from version 0 and 1; markers leave nothing behind. Gated build. Notes; CHANGELOG Staff line.

### Draft C: Town Houses leasing and rent (L2)

**Model:** Opus

**Touches:** server

**Summary:** Players lease a site: weekly rent from the bank on server uptime, grace, and eviction into a protected belongings crate, per P550's money, timing and belongings corrections.

1. Read the P409 design (Rent, Missed rent), P550 (corrections 4 and 6, Money, timing and exploit risks) and P634's notes.
2. The lease sign gump (terms, Lease, Rent box, End lease) replacing the stock sign interaction; one-house check and payment in one operation, rechecked on every reply; a persisted server-uptime counter, with paid-through and grace measured on it; the 15-minute sweep; arrears carried forward from the paid deadline; evict at most once.
3. One lease-ending operation before any destructive deletion (eviction, choice, staff removal, account deletion through a hook before `Account.Delete` deletes houses, unexpected sign or house deletion): recorded property and addons (with contents) to an account-bound, withdraw-only belongings crate; a saved pending-payment record for credit refunds; no new lease while recovery storage is unclaimed. Remove house transfer and demolish from the lease gump.
4. Red-then-green facts: the accounting equation with sinks; rent once per period across restarts; downtime adds neither rent nor grace; grace blocks new lockdowns but allows taking things out; eviction delivers every recorded item, nothing deleted, no town fixture or other account's item packed; full bank keeps the pending payout; double termination pays once. Gated build. Notes; CHANGELOG player lines once a player can lease (still test shard).

### Draft D: Town Houses sublets (L3)

**Model:** Opus

**Touches:** server, server-patches

**Summary:** A principal tenant rents a room to another player, with real room rights, per P550 correction 3 and the settled call that a room tenant's account counts as having its one house.

1. Read the P409 design (Sublets), P550 (correction 3, the room questions) and the L2 notes.
2. Engine hooks for room access, login, item use, locking down, securing, release and container access (patches where the stock methods are not virtual), never granting co-owner or owner status; room doors; a common path from street to room; overlapping rooms, shared doors and blocked exits refused.
3. A saved room reservation checked by lease offers, room offers, deeds, placement, transfer and ownerless-house claims (alts on the same account included). Room escrow with the town fee, a deterministic prorated refund, settled once; rooms end through the L2 operation.
4. Red-then-green facts per P550's evidence list for rooms. Gated build. Notes.

### Draft E: Town Houses guides and placing the approved sites (L4 and L5)

**Model:** Opus

**Touches:** server (data), docs-only

**Summary:** After drafts A to D: load Chase's approved buildings from a data file, idempotently, and write the player and staff guides.

1. A data file of the approved L0 sites that a `[Leaseholds load` command places like the shard's seeders (a second load changes nothing; each site passes the placement checks again on load and when a lease starts).
2. Player guide, staff guide, patch-note lines, play-test plan items, and the custom-system and fidelity register text for the overseer to promote.
3. Live enablement is a separate, authorized release.

P634 DONE
