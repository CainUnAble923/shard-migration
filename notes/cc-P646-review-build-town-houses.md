# P646: Review of P634 Town Houses

Reviewed October 26, 2026. Documentation only. No code changed.

P634 builds the staff-assigned leasehold core, not the full rental system. The additional findings below concern that core. Rent, room rights, payment recovery, and belongings packing are explicitly later stages in [P634's build note](cc-P634-build-town-houses.md), so their absence is not presented as a new defect here.

## Scope and evidence

Read both work-copy agreements, the direction and task documents, [P409's design](cc-P409-town-houses-design.md), [P542's handoff](cc-P542-cont-fixup-town-houses-design.md), [P550's corrections](cc-P550-review-town-houses-design.md), and both P634 notes. Chase's adoption of P550's Codex defaults is recorded directly at `D:/UO/overseer/decisions-2026-10-23.md:60`. The earlier reviews of P409, P542, P550, and [P634](cc-P634-build-town-houses-codex-review.md) were checked to avoid repeating findings. Previously reported issues are not counted again below.

Reviewed P634's listed implementation files:

- `server/customizations/Leaseholds/ClusterFLeasehold.cs`
- `server/customizations/Leaseholds/ClusterFLeaseSite.cs`
- `server/patches/BaseHouse-leasehold-region.patch`
- `server/tests/Multis/LeaseholdVerification.cs`
- The patch registration in `docker/uo/apply-patches.sh`, and the corresponding `CHANGELOG.md` entry and `VERSION`.

Code HEAD: `a3f017e279e29eed0ac12c506ef51e6310291583`. Notes HEAD before this review: `d6e456176a8a274b30173450d48c250177ef33c7`. The read-only ModernUO checkout and Dockerfile both pin `d4531cd94b739613155225c234900de9f47d2c88`.

Paths below beginning `U/` mean `D:/UO/ModernUO-pinned/Projects/UOContent/`; `S/` means `D:/UO/ModernUO-pinned/Projects/Server/`. Other code paths are relative to ShatteredLegacy. These are source findings with explicit triggering conditions, not claims of observed live exploits.

## New findings

### 1. Medium (P2): A lease can make a town's fixed addon container removable

**Where:** `server/customizations/Leaseholds/ClusterFLeaseSite.cs:147` and `:249`.

**What happens:** The safety scan permits existing fixed addon containers and their components. Assignment then makes their location part of a house owned by the tenant. Unlike ordinary `BaseAddon.OnChop`, which requires membership in `house.Addons` (`U/Items/Addons/BaseAddon.cs:88`), `BaseAddonContainer.OnChop` requires only house ownership and an unsecured container (`U/Items/Addons/BaseAddonContainer.cs:69-113`). It drops the contents, deletes the fixture, and gives its deed to the tenant. The axe target reaches this operation through `IChoppable` (`U/Engines/Harvest/Core/HarvestTarget.cs:52-54`); targeting a container component forwards to the addon (`U/Items/Addons/AddonContainerComponent.cs:48-52`). An immovable, unsecured `ArcaneBookshelfEastAddon`, for example, has a non-null deed and satisfies this path.

This violates P409's decoration rule that existing town fixtures never become the tenant's property and are never removed. The lease code need not add the fixture to `house.Addons` for this particular exploit. No claim is made that an approved town building currently contains one: the survey has not established that. The staff tool accepts such a building today.

**Fix:** For the current stage, reject sites containing unowned addon containers, including fixtures whose components intersect the leased area. Alternatively, record and protect original fixtures through the relevant chop, secure, lockdown, and release paths. Protecting only the eventual eviction packer would leave the live chop path open.

**Missing test:** Place an immovable town addon container with contents before creating the site. Creation or assignment must refuse it, or a tenant's axe must leave the original serial, contents, and deed count unchanged. Separately verify that an addon placed by the tenant can still be redeeded. Existing leasehold facts never exercise a fixed fixture.

### 2. Medium (P2): The ban destination need not be a walkable street tile

**Where:** `server/customizations/Leaseholds/ClusterFLeaseSite.cs:108` and `server/customizations/Leaseholds/ClusterFLeasehold.cs:69`.

**What happens:** The street target is checked for being outside the rectangle and sharing its region, but never for a supporting surface or clearance. Its exact XYZ becomes `RelativeBanLocation`. A target inside an impassable wall, in unsupported space, or at the wrong floor height can therefore pass. The house engine later assigns that location directly on private-house login and ejection, without a fit check (`U/Regions/HouseRegion.cs:33-40`, `:97-108`). A stranger can be moved into an unusable location instead of safely onto the street. P409's setup rules explicitly require a walkable ban spot.

**Fix:** Validate the destination's surface and character clearance before creation and again before assignment. Use the map's fit checks with surface required, and reject destinations inside other private houses or unsafe structures. Preserve a safe destination when later edits or placement changes invalidate the original.

**Missing test:** Refuse blocked and unsupported street targets, then exercise a non-friend's login or ejection and verify that the actual destination is the validated walkable tile. `UnsafeSitesAndSecondHousesAreRefused` currently checks only a street target inside the building.

### 3. Medium (P2): The other-multi check examines origins instead of occupied footprints

**Where:** `server/customizations/Leaseholds/ClusterFLeaseSite.cs:124` and `:147-151`.

**What happens:** `FindHouseAt` checks houses, but the remaining `BaseMulti` exclusion runs through `GetItemsInBounds`. That iterator yields an item only when its origin is inside the rectangle (`S/Maps/Map.ItemEnumerator.cs:292`). A non-house multi whose origin is just outside the rectangle can extend tiles into the leased volume and escape both checks. The additional origin-Z comparison can likewise miss components extending into the floor range. This contradicts P409's refusal of overlap with any other multi, and allows the lease's private region to cover part of another structure.

**Fix:** Inspect multis registered in the sectors covering the proposed volume and test their world-space components or occupied bounds for intersection, including Z. Do not substitute `GetMultisInBounds` without inspecting its semantics: it also filters by origin (`S/Maps/Map.MultiEnumerator.cs:254`). The sector registration already spans each multi's component bounds (`S/Maps/Map.cs:694-701`, `:759-779`).

**Missing test:** Put a non-house multi's origin outside the proposed rectangle while one of its components intersects it. Site creation and later assignment must both refuse it. Include a genuinely separated structure as a passing case. The existing unsafe-site fact covers another lease site and a creature, but no non-house multi.

### 4. Medium (P2): A partially registered door pair can still operate a hidden original

**Where:** `server/customizations/Leaseholds/ClusterFLeaseSite.cs:226-230`, `:262`, and `:265-270`.

**What happens:** Staff can register just one leaf of a linked town-door pair. Assignment accepts that list, moves the registered original to the internal map, and links replacements only when both originals were registered. The untouched town leaf retains its link to the hidden original. Opening it runs stock `BaseDoor.Use`, which sets `Link.Open = true` without checking that the partner is on the same map (`U/Items/Construction/Doors/BaseDoor.cs:385-389`). The hidden original changes art and moves by its swing offset (`:81-90`), while the visible lease replacement does not follow. Its timer cannot close it on the internal map because `CanClose` calls `CheckFit`, which refuses that map (`:242-265`). Ending the lease restores it in its changed open position because `RestoreDoors` only changes its map. Thus the originals do not remain unchanged while leased, and the double door loses its expected linked behavior.

**Fix:** Require a complete linked pair or chain before assignment, refusing links to unregistered doors or doors belonging to another site. Where a partial conversion is deliberately supported, isolate the saved originals' links and preserve their closed positions and state for restoration. Do not leave public doors pointing at internal-map originals.

**Missing test:** Register only one of a linked pair and require assignment to fail safely. Then register both and exercise opening, closing, termination, and a serialization round trip, checking links, exact closed positions, and original state. The current door fact registers both leaves and never calls `Use`.

## Verification and limits

This was a source review. No tests were added or run; the prompt specifies no lane tests and no code changes. P634's reported green build was read, not independently rerun. No Docker command, shard startup, client session, world command, full-world restart, or town survey ran. The suggested regression cases must be observed failing before their future fixes and passing afterward. Actual occurrence at a chosen town building remains unverified, especially the fixture and non-house-multi cases.

The existing round-trip fact was read in full. It resolves references against already existing entities and does not restart a complete world. That limitation was already disclosed by P634 and is not a new finding here. The door round trip suggested above concerns door state and links, which the current fact does not serialize and exercise.

All inspection used Windows PowerShell 5.1. Ran `tools/progress.py --dry-run` with both path overrides pointing to these work copies: exit 0. Its known incidental write to `tools/progress.json` was restored byte for byte, leaving no generated change. No content counts from that report are used as review evidence.

Only this notes file is retained as a change. No code, `docs/`, saves, accounts, services, or live systems were changed. No Haven connection, commit, merge, push, or branch switch occurred.

Final checks: the code work copy is clean; this note is the only notes-repo change. The note is below 5 MB, contains no em dashes or trailing whitespace, and its local Markdown links resolve.

P646 DONE
