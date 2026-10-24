# P550: Town Houses design review

Reviewed October 24, 2026. Documentation only. No code or world changes.

The native leasehold approach fits Chase's decision, but P409 is not ready to become build prompts. It needs corrections to region creation, multi bounds, room permissions, belongings recovery, money settlement, and decay. P542 restored the design unchanged; it did not resolve the earlier review findings.

## Evidence and scope

- Design: [P409](cc-P409-town-houses-design.md), especially lines 28-127, 169-219, and 239-337.
- Earlier findings: [P409 Codex review](cc-P409-town-houses-design-codex-review.md). Its access, payout, downtime, and gold-accounting concerns remain valid against the source read here.
- Handoff: [P542](cc-P542-cont-fixup-town-houses-design.md), lines 12-18, and its [review](cc-P542-cont-fixup-town-houses-design-codex-review.md).
- Chase's actual calls: `D:/UO/overseer/decisions-2026-10-22.md:24-25`, read directly. P405's questions are at [lines 1193-1199](cc-P405-servuo-batch-1022.md#open-questions-for-chase).
- Code work copy HEAD and local `main` both resolve to `82ba93fdd3e047646cdf63cb4f468b9a30b90270`. There is no difference from that main in `server/customizations`, `server/patches`, or `docker/uo`.
- The Dockerfile pins `d4531cd94b739613155225c234900de9f47d2c88`. The read-only `D:/UO/ModernUO-pinned` checkout reports the same HEAD and a clean working tree. Its housing sources are the engine evidence below. The canonical customizations and patches contain no Town Houses implementation or changes to the cited house region, house sign, and bank methods. The existing `HousePlacement-climbed-tile.patch` adds a climbing restriction, not a housing exception.

Source abbreviations below: `U/` means `D:/UO/ModernUO-pinned/Projects/UOContent/`; `S/` means `D:/UO/ModernUO-pinned/Projects/Server/`. File names and line numbers refer to that checkout, not `server/uo`.

## Chase's calls versus the design

| Settled call | Review |
|---|---|
| Rentals and sublets, built natively | P409 includes both and correctly rejects the downloaded implementation. Keep both in the scope. A rent-only first release can mean no outright sale; it must not quietly mean dropping sublets from the accepted feature. |
| May sit inside guarded towns | The proposed parented house region is the right direction. The missing-parent fallback at P409:281-283 permits an unguarded leasehold with only a warning. That fails the stated promise that town guards keep working inside. Require a safe recovery path before occupancy resumes. |
| Counts as the account's one house | Correct for the principal tenant: a real `BaseHouse` with an owner enters the stock owner table (`U/Multis/Houses/BaseHouse.cs:76-83`, `:3541-3556`). The proposed exemption for room renters at P409:111-113 and :325 is an additional policy choice, not an answer Chase already gave. It could allow a house plus a rented town room. Resolve that explicitly before L3. |
| F-44 inn rooms and F-49 halls are not Town Houses | P409:190-191 explicitly contemplates a leasehold over an inn's rooms. Remove that example and exclude the inn and guild hall sites from placement. Keeping an inn's region rules does not satisfy the exclusion. P409 has no clear hall exclusion either. An empty building check alone does not protect a reserved hall or inn. |

Do not reopen these settled calls as general questions about whether Town Houses should exist. [P532's S049 row](cc-P532-open-questions-for-chase.md), line 124, still recommends deferring leaseholds; that recommendation predates or misses the recorded answer and should not override it.

## Corrections required before implementation

### 1. The proposed region constructor patch is insufficient

P409:198-203 says one `HouseRegion` constructor plus an override of `ClusterFLeasehold.UpdateRegion` supplies the region. However, `BaseHouse.m_Region` is private, and `BaseHouse.Region` has only a getter (`U/Multis/Houses/BaseHouse.cs:40`, `:439`). Stock `UpdateRegion` assigns that private field at :1645-1658. The subclass cannot replace it as described. Registering a separate region leaves the stock `Region` property, ban-location handling, mobile enumeration, and deletion cleanup disconnected from it (:410-431, :1277, :3380-3383).

Recommended answer: add a narrow virtual region factory used by stock `UpdateRegion`, alongside the parent/3D constructor. The leasehold returns its region from that factory; `BaseHouse` continues to own registration and cleanup. Argue and build the actual patch before assigning L1's size. A second region field or a hidden `Region` property is not an adequate substitute.

### 2. Resizing an empty multi does not give it the required sector bounds

P409:218-219 proposes an instance-specific empty component list resized to the building. Isolation from the shared `Empty` list is correct, but sizing alone is insufficient. `Resize` sets `m_Min` and `m_Max` to zero and expands them only when it visits actual tiles (`S/Client/MultiData.cs:637-716`). An empty list therefore still has zero minimum and maximum bounds. Map sector registration uses those bounds, not `Width` and `Height` (`S/Maps/Map.cs:775-779`). `FindHouseAt` searches only multis registered in the point's sector (`U/Multis/Houses/BaseHouse.cs:1434-1447`).

The consequence inferred from these methods is that lookup can fail in every part of a building outside the house origin's sector, even when `IsInside` returns true there. A test entirely within one sector would miss it.

Recommended answer: specify how an invisible multi obtains real per-instance minimum and maximum bounds, including offsets and map registration on load. Assess a narrow bounds hook versus server-side components with their collision and drawing effects. Do not promise that empty `Resize` solves it. L1 must cover a building crossing sector boundaries, lookup at every edge, and save/load reconstruction.

### 3. Room doors and speech routing do not implement room rights

Private-house movement requires `HasAccess`, location changes can eject the player, and the static login handler ejects non-friends (`U/Regions/HouseRegion.cs:33-41`, :81-125, :137-185). The login handler is not a virtual instance method that `ClusterFLeaseholdRegion` can simply override. `BaseHouse.HasAccess`, `IsFriend`, and `IsCoOwner` are also nonvirtual (:3563-3565, :3612, :3641-3665). Adding the renter to `Access` alone still fails the login check. Adding every renter as a friend or co-owner grants broader rights than a room.

Storage has a separate barrier. `LockDown` and `Release` require a co-owner; `AddSecure` and `ReleaseSecure` require the owner (`U/Multis/Houses/BaseHouse.cs:2157-2164`, :2394-2423, :2539-2543). These methods are nonvirtual. Secure levels name household roles, not an individual renter (:2516-2535). Stock accessibility can deny a renter access to their own locked container (:1457-1500). Routing speech to these same methods still fails.

Recommended answer: describe the required engine hooks for room access, login, item use, securing, release, and container access. Keep guards and stock combat restrictions in those paths. Provide a common route from street to room, and reject overlapping rooms, shared doors, blocked exits, and room rectangles that capture stairs or other tenants' routes. Recheck permissions when a target or gump response arrives. Do not grant temporary co-owner or owner status to perform an operation. L3 may need upstream patches; P409's claim that L2 and L3 are custom-code-only is premature.

### 4. Belongings cannot be divided reliably without ownership records

The house stores a `List<Item>` of lockdowns and secure records containing an item and a security level, not a depositor (`U/Multis/Houses/BaseHouse.cs:55-57`, :3920-3941). `GetItems` selects movable items by location without attributing them to an account (:1247-1267). Location alone cannot distinguish the landlord's furniture, a subtenant's chest, a visitor's dropped bag, and a town fixture. Moving everything in a room to its renter invites theft by rearranging someone else's belongings before eviction.

Recommended answer: record the responsible account and lease/room for each accepted lockdown, secure, and addon, with explicit ownership transfer rules. Prevent the principal tenant and co-owners from releasing or taking a room renter's registered property. Set a separate policy for loose items; promise recovery for registered property, not unverifiable ownership of every loose object. Never collect corpses, mobile inventories, town fixtures, or another account's belongings by a broad area sweep. Containers and their contents need consistent ownership rules.

Stock packing is also incomplete for the promise at P409:86-94. `MoveAllToCrate` walks managed lists, not all loose items, and drops addon-container contents on the ground before converting the addon to a deed (`U/Multis/Houses/BaseHouse.cs:853-996`, especially :954-977). Stock addon placement checks actual house ownership at `U/Items/Addons/BaseAddon.cs:198-202`; room addon rights cannot be assumed.

Specify packing order: settle each room's recorded property to that account, preserve addon contents and state, then pack the principal tenant's property. Only release the site after delivery or durable recovery storage is confirmed. A room's quota must include nested container contents and stay within the building's total storage; limits need enforcement when containers gain contents, not just when first secured.

### 5. Separate permanent sites from disposable houses, signs, and doors

P409 leaves the site base type as `HouseSign` or `Item`. That choice affects survival. `HouseSign`'s constructor dereferences its house owner; its owner reference has a private generated setter; deleting a house sign deletes its house (`U/Multis/Houses/HouseSign.cs:12-23`, :47-54). House deletion deletes its sign and doors (`U/Multis/Houses/BaseHouse.cs:3386-3397`). A permanent site must not disappear with the house it records.

Recommended answer: a separate persistent site item owns terms, original doors, tenant records, escrow, and recovery state. A disposable house sign refers to that site. Explicitly override the sign's player interaction for lease management rather than calling stock `HouseSign.OnDoubleClick`, which opens the stock gump (:129-135). Do not assume a method named `ShowSign` supplies a stock extension point.

There is also a vacant-door contradiction. Setup swaps doors at P409:34, but a vacant site has no house at :48-49. A `BaseHouseDoor` whose `FindHouse` returns null denies access (`U/Items/Construction/Doors/HouseDoors.cs:99-105`, :138-146). Keep town doors in service while vacant. Swap only when the lease becomes active and restore on every end, including eviction. Preserve linked door pairs, facing, closed position, lock state, and the exact originals. Failed setup must roll back the swap.

### 6. Make lease expiry the only ordinary decay path

P409 lists `RestrictDecay` but never requires disabling normal house decay. The engine defaults `houseDecay.enable` to true, and an inactive account can condemn a house (`U/Multis/Houses/BaseHouse.cs:110-151`, :1301-1310). Collapse schedules `Decay_Sandbox`, which deletes the house (:627-635, :659-673). Stock deletion unlocks property in the world and destroys a secure strongbox rather than performing the promised bank recovery (:3400-3455).

Recommended answer: make leaseholds ageless through their type, independent of ordinary house refresh. Rent and inactivity use one lease-ending operation. That operation must run before destructive base deletion for staff removal, account deletion, and unexpected sign/house deletion as well as eviction. `U/Accounting/Account.cs:331-349` directly deletes an account's houses before deleting its characters, so recovery solely on the next sweep is too late. Do not describe an already deleted house as harmless just because its site will enter hold.

Abandonment still needs a rule after disabling decay. An absent tenant with enough bank gold can renew indefinitely; an orphan can freeze a scarce site indefinitely. Recommend using the existing account inactivity threshold as a trigger for a warned lease termination, with normal recovery, and an age-sorted staff list for holds/orphans. The stock account threshold is 180 days (`U/Accounting/Account.cs:22`, :268-279); adopting it for leases is a recommendation, not an existing lease behavior. Avoid permanent outright sales in the first release because the proposed rent sweep would never reclaim them.

## Money, timing, and exploit risks

**Escrow can be lost by the specified settlement order.** P409:247 says to zero escrow before depositing. `Banker.Deposit` can return false for a full bank, and `DepositUpTo` can return only part of the amount (`U/Mobiles/Townfolk/Banker.cs:209-268`, :316-367). Offline delivery does not guarantee delivery. Move escrow into a saved pending payment record, then reduce that debt only by what was delivered. A settled flag prevents duplicate settlement; it must not erase an unpaid balance. Keep recovery balances outside an item that house deletion destroys.

**The gold acceptance equation is wrong.** Town rent and the town's sublet fee are intentional sinks. P409:247 and L2 cannot require the same total gold before and after. Require `starting gold = remaining spendable gold + prepaid credit + room escrow + pending payments + recorded sinks`, with starting held balances included if present. Count account gold, physical gold, and checks once. Refunds and payouts move real balances; they never increase this total. Validate positive rents, bounded terms and credit, rounding, and arithmetic overflow.

**The timing fields do not support the downtime promise.** Saved wall-clock `paid through` and `grace started` do not measure online grace. Skipping the first sweep only delays eviction until the next sweep. Recommend a persisted server-uptime counter and lease deadlines measured against it, so neither rent nor grace accrues during downtime. Carry forward from the prior paid deadline on late payment; charging only once and setting the deadline from the current time grants free overdue occupancy. Define what is owed during grace and how long a payment extends the lease. Once grace is exhausted, evict at most once. Repeated restarts must not reset the grace budget.

**Missing guards must not become a usable attack pocket.** P409's parent lookup must exclude the leasehold's own region on repeated updates and check the whole occupied 3D area, not merely the sign tile. If the expected town parent cannot be recovered, stop new occupancy and charging, preserve property in recovery storage, and close the affected lease until staff repair it. A financial hold alone does not restore guard coverage. The parent chain is material: `S/Regions/Region.cs:458-475` resolves region types through parents, and `U/Regions/GuardedRegion.cs:199-233` handles criminal actions there.

**Every lease state needs server-side enforcement.** Grace must reject new lockdowns, secures, addons, room starts, and storage growth through existing containers while allowing recovery and release. Using `IsActive = false` globally would also block release in stock methods. A stale gump must not lease an already occupied site or use old terms after an edit. Recheck site state, account entitlement, terms version, and payment in one operation. Staff test assignments must not create refundable credit or silently displace a paid tenant.

**Over-limit bank crates can become cheap remote storage.** The proposed forced bank delivery preserves property but bypasses normal capacity. Repeated lease/end cycles could use it to bank arbitrarily large collections. Recommend account-bound recovery crates that reject deposits, cannot be traded, and only allow withdrawal. Retain normal total-item accounting, cap the property's admitted storage, and prevent new leases or room rentals until prior recovery storage is cleared. This needs full-bank and nested-container checks, not just a successful forced drop.

**No vendors is mostly supported, but make it explicit.** A house without a placement entry currently gets zero vendor capacity (`U/Multis/Houses/BaseHouse.cs:774-789`), and a player's employment contract checks that capacity (`U/Items/Misc/PlayerVendorDeed.cs:42-61`). Keep this restriction explicit instead of supplying a stock placement entry that incidentally enables vendors. Barkeepers have their own capacity method (`BaseHouse.cs:791`); decide whether they are excluded too. Any later vendor support must settle inventory and rentals during lease termination.

## Remaining design questions and recommended answers

These are recommendations for the next design revision, not newly accepted decisions and not blockers to completing this review.

| Question | Recommended answer |
|---|---|
| Does a rented room consume the account's house entitlement? | Treat it as consuming that entitlement unless Chase explicitly approves an exception. A room is not a second `BaseHouse` owner, so this needs a saved reservation checked by lease offers, room offers, deeds, placement, transfer, and ownerless-house claims. Cover alts on the same account. Do not implement a UI-only check. |
| Rent or outright sale? | Weekly rent first, with sublets still planned. Sale requires a separate abandonment policy and must never refund an unpaid or staff-assigned price. |
| Where may staff place sites? | Use an approved town-building list with explicit inn, hall, service, street, and travel-route exclusions. Revalidate when activating a lease, not only during the original survey. A marker preview helps staff but is not proof of safe geometry. |
| What can the principal tenant do to a room renter? | Enter for management if that remains desired, but no taking or releasing their registered property. Bans, door changes, and removal of common-path access cannot bypass paid room rights. Terminating the room invokes its refund and packing procedure. |
| What happens to a room when the principal lease enters grace? | Warn its renter, stop renewals and new room offers, retain access to recover property, and end the room through settlement if the principal lease ends. Do not accept payment for a term the building lease cannot honor without an explicit refund guarantee. |
| What is the early-end refund? | Specify a deterministic prorated refund of unearned room rent when the landlord, staff, or principal eviction ends it. Apply a stated rounding rule and charge the town fee only on earned rent. Keep the proposed renter-forfeiture rule visible in the offer if retained. |
| Can a landlord change room price or storage midterm? | No change to a paid term. Present new terms for explicit acceptance at renewal. Reserve each room's storage so landlord use cannot consume its promised share. |
| Who receives a friend's items and a deleted character's recovery? | Record the principal account's entitlement for agreed shared-house property and each room account's separate property. Resolve delivery to a surviving character on the same account. For a deleted account, retain a staff recovery record and follow an explicit account-deletion policy. A literal forever-bank guarantee cannot survive deletion of that bank. |
| What reclaims abandoned buildings? | Rent default plus the recommended inactivity rule, both using the same settlement operation. Staff repair holds/orphans from a visible queue; no silent, permanent rent-free occupancy. |
| Starting prices, supply, and storage? | Use P409's staff-set weekly price and limited-site approach as provisional defaults. Survey first and pilot in Britain. Derive AOS storage explicitly through the virtual capacity methods; without overrides it is zero (`BaseHouse.cs:677-699`). Include room shares in that total. Prices and quotas remain untested balance proposals. |

## Required evidence in the later build prompts

No tests are added or run for this documentation-only review. Before the feature ships, its implementation prompts should require tests seen failing first for these behaviors:

- The correct parented region is held by `BaseHouse.Region`, guard handling still works, repeated region rebuilds do not create self-parenting or leaked regions, and a missing parent cannot leave a usable unguarded leasehold.
- `FindHouseAt` works across sector boundaries, disconnected floor rectangles, height limits, and reloads. Two sites never share mutable component state.
- A private-house room renter can enter, log in, use their own storage, and leave, while another room's property and the landlord's storage remain protected. Test alts, pets, stale targets, bans, and a blocked common path.
- Main tenancy and the chosen room entitlement policy are enforced in both directions against placement, deeds, transfers, and claims, including preexisting gumps.
- Full and missing banks retain exact pending payouts across restart. Double termination and house/sign deletion in the same tick cannot pay twice. The accounting equation includes consumed rent and fees.
- A restart after a long shutdown preserves the remaining grace and paid time. Repeated restarts cannot extend grace. Paying arrears and editing terms have explicit expected deadlines and amounts.
- Eviction, voluntary ending, inactivity, staff deletion, and account deletion preserve the agreed property and room payouts before destructive cleanup. Include a filled addon container and secure strongbox, and prove no town fixture or other account's item enters the wrong crate.
- Town doors work while vacant; each lease/end cycle restores the same original doors and preserves linked pairs. The permanent site survives disposable house/sign deletion.
- Ordinary house decay cannot bypass lease settlement. Full recovery storage cannot accept deposits or enable a repeated over-limit banking shortcut.

## Verification and limits

Read both work-copy agreements and the required direction/task documents. Used Windows PowerShell 5.1 for local inspection. Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointed at these work copies. It completed but unexpectedly rewrote `tools/progress.json`: `build()` writes that file at lines 720-724 before `main()` checks the dry-run return at line 737. Restored that incidental generated change to its initially clean state. This tool defect is recorded here only; no tool fix belongs in this design review. No content counts from its general report are used as review evidence.

This is source-based design analysis. The region-factory and empty-bounds failures follow from the cited implementations; they were not reproduced in a running server. No Docker build, client session, save/load experiment, or map survey ran. Actual site geometry, live region overrides, unknown-multi rendering in TazUO, timing under crashes, and preservation of every supported addon remain unverified. The third-party download was not re-audited; this review relies on current engine and shard sources rather than repeating P405's download defect claims as newly proved facts.

Only this notes file is intended to change. No code, `docs/`, accounts, saves, services, or live systems were changed. No Haven connection, commit, merge, push, or branch switch occurred.

Final checks: the code work copy is clean, and this notes file is the only retained docs-repo change. The note is below 5 MB, contains no em dashes or trailing whitespace, and its local Markdown links resolve. No lane tests apply to this task.

P550 DONE
