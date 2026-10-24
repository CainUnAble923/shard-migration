# CC task P409: Town Houses, our own design (leaseholds with rentals and sublets in towns)

Iron, 2026-10-24. Design notes only: no code, no deploy, no world change. Built on P405's knives-town-houses section and
Chase's 10-22 answers to its questions 13 and 14. Every engine fact below was read in `D:\UO\ModernUO-pinned`
(`d4531cd94`); paths are under `Projects\` unless they say otherwise. Knive's code
(`D:\UO\third-party\code\knives-town-houses\`) was read only, as a behavior reference; nothing there was built or run.

## In plain words

- This is the plan for **Town Houses**: a player can rent (or buy) a real building inside a town, such as a shop in
  Britain, and it works like a house: their own doors, lockdowns, friends and bans, while the town guards keep
  working around and inside it. It counts as the account's one house.
- Rent is taken from the bank each week, with a few days' grace and warnings; a tenant who stops paying has their
  belongings packed into a crate in their bank, never thrown away. A tenant may sublet a room to another player.
- It closes every hole P405 found in the download (copied decorations, refunds of money never paid, a deposit made
  from nothing, all town houses sharing one footprint) because nothing is ported: we build it on ModernUO's own house code.
- **For you:** 12 choices at the end ("Open questions for Chase"), each with a recommendation; the main ones are
  rent only or also sale, the rent amount, the grace days, and how many per town. Nothing gets built until you answer.

## The name

**Leasehold** for the building, **Lease Sign** for its sign, `[Leaseholds` for the staff command (P405's rename
candidates). Code names: `ClusterFLeasehold`, `ClusterFLeaseSign`, `ClusterFLeaseholdRegion`. "Town house" stays the
plain word in player text ("Town houses for lease").

## 1. How it plays

### Staff place a leasehold (once per building)

1. A GM stands in an empty town building and types `[Leaseholds new`.
2. They target two corners of each floor rectangle (one or more), then give the Z range (lowest and highest floor of
   the part being leased: a whole shop, or only the upstairs above a shop).
3. They target the sign spot (outside the front door) and the ban spot (the street, outside every rectangle).
4. They target each door of the building that becomes the tenant's door. The tool swaps each for a house door of the
   same art and facing (`GenericHouseDoor`, `Items\Construction\Doors\HouseDoors.cs:42`, `:45`) and keeps the
   original, unchanged, on the internal map, to put back if the leasehold is ever removed.
5. They set the terms (rent, period, sale price if sale is on, lockdowns and secures; the gump suggests numbers from
   the floor area) and the requirements (open questions 1 to 3, 8, 11).
6. The tool **refuses** the site when:
   - a rectangle spans two different regions (half in Britain, half outside), or the sign spot is in another region
     than the rectangles: the leasehold takes its guard rules from the region it sits in (section 2);
   - the area overlaps any house, leasehold or other multi (`BaseHouse.FindHouseAt`, `BaseHouse.cs:1434`);
   - an NPC, a spawner, a moongate or teleporter, or a bank or vendor stand is inside it (towns keep their services);
   - the ban spot is inside the area or not walkable.
7. While setting up, the area is shown with hued markers on its floor tiles (removed when done), so staff see exactly
   which tiles become private before saving. A loose rectangle that takes in part of a street would eject passers-by
   (P405, `HouseRegion.cs:95-128`); the preview is the guard against it.
8. A vacant site is only its **Lease Sign**: "For lease: 1,500 gold a week, 120 lockdowns. Double-click to view."
   No house, no private region, the building stays an ordinary public town building until it is leased.

`[Leaseholds` also lists every site (town, state, tenant, paid until), goes to one, edits terms (they apply from the
next period), puts a site on hold, ends a lease (with the belongings packed as in an eviction) and removes a vacant
site (doors put back).

### A player leases one

1. Double-click the Lease Sign: the terms, the floor plan size, lockdowns and secures, the rules, and **Lease**.
2. The checks, in this order: the player is not Young (if open question 11 says so); **the account holds no house**
   (`BaseHouse.HasAccountHouse`, `BaseHouse.cs:3541`); the first period's rent is in the bank (or the sale price).
3. The gold is taken (`Banker.Withdraw`, `Mobiles\Townfolk\Banker.cs:158`, which also takes account gold). The
   leasehold is created over the building with the player as owner. From then on it is a house in every way the
   engine knows: the house gump, friends and co-owners, lockdowns, secures, bans, "I wish to lock this down", instant
   logout for friends, house combat rules.
4. A leasehold counts as the account's one house automatically: the engine keeps its house table by owner
   (`BaseHouse.cs:29`, `:80`), and every placement, deed and transfer asks `HasAccountHouse` (`Multis\HouseDeed.cs:36`,
   `:64`; `Multis\Houses\HousePlacementTool.cs:195`, `:1989`, `:2092`; `BaseHouse.cs:2287`, `:2360`). So a tenant cannot
   place a deed house, and a house owner cannot lease.

### Rent

- **Period:** weekly (open question 3). Rent is due on the same weekday and hour it began.
- **Paid from:** first the lease's own **prepaid credit**, then the bank. Prepaying: drop gold or a bank check on the
  Lease Sign ("Rent box"); it is consumed into credit, up to 4 periods ahead. The credit is real gold the tenant gave,
  so it is returned to their bank when the lease ends for any reason.
- **No refunds** of rent already used, and none of a sale price (open question 1): the money is the town's.
- One timer for the whole shard (every 15 minutes) walks the list of leaseholds and charges what is due. Nothing
  hangs on a per-lease timer, so a restart loses nothing: each lease saves the time it is paid through.

### Missed rent

1. **Due and unpaid:** "Your rent for the town house in Britain is overdue" at login and on the house sign; the sign
   shows "Overdue". The sweep tries again every day.
2. **Grace** (open question 4, recommended 7 days): the tenant and friends can still come and go and take things out,
   but nothing new can be locked down or secured, and no sublet can start. Paying the arrears ends it at once.
3. **Eviction** at the end of the grace:
   - every item of the tenant and their friends inside the area (lockdowns, secures, contents, loose items, addons as
     their deeds, as the stock moving crate does, `BaseHouse.cs:853` `MoveAllToCrate`, `:1239` `DropToMovingCrate`)
     goes into one **Lease Belongings** crate;
   - the crate goes into the tenant's bank with the bank's own drop (as the test kit's fill does, it is not refused
     at the bank's item limit, `docs\feature-queue.md:1665-1669`); the bank is then over its limit until they empty
     the crate, and says so;
   - the house is removed, the original doors and sign come back, the site is vacant again;
   - an email-style in-game letter (and a login message) lists what happened.
   Nothing is ever deleted. A crate is never sent to another account.
4. **Ending a lease by choice:** the tenant presses "End lease" on the sign gump, waits for the current period to run
   out (or ends now and loses it), and their things are packed the same way. The unused prepaid credit goes back.

### Sublets (rooms)

- **Who:** the tenant of a leasehold (open question 7). Not any house owner: rooms need walls we placed and can check.
- **What:** a **room** is one rectangle inside the leasehold's area and Z range with one door; the tenant draws it
  with the same targeting, and the door becomes a room door (a house door that opens for the room's subtenant, the
  tenant and co-owners).
- **Terms:** the tenant sets the room rent and period (1 to 4 weeks, like the stock vendor rental durations,
  `Mobiles\Vendors\RentedVendor.cs:12-20`) and a share of the leasehold's lockdowns (for example 20 of 120).
- **Money, never made from nothing:** the subtenant pays a period up front from their bank into the room's escrow
  (a number on the lease, backed by gold taken). At the end of each period the escrow is paid to the tenant's bank,
  less the town's fee (open question 7, recommended 10%, a gold sink). Ending early by the tenant returns the
  subtenant's unused escrow; ending early by the subtenant forfeits it. This is the stock rented vendor's model
  (renewal moves held gold, `RentedVendor.cs:330-357`).
- **Limits:** rooms per leasehold by size (recommended 1 per 50 floor tiles, at most 4); one room per account; a room
  is not a house (it does not count against the subtenant's one house); a room cannot be sublet again.
- **What the subtenant can do:** enter through their door, lock down or secure up to their share inside the room only,
  and nothing else in the leasehold. When their rent lapses, or the leasehold ends, their room's things go to their
  own bank in a crate, as in an eviction.

### Decoration rules

- The building's own fixtures (the statics in the map, and the town decoration items placed by `[Decorate`) stay the
  town's: they are never lockdowns, never part of a sale, never movable, never removed or recreated. The tenant brings
  and takes only their own things.
- Lockdowns and secures as a stock house of about the same floor area (open question 8).
- Addons and furniture deeds work as in any house (they need the target inside the house, which the leasehold
  answers through its own area).
- No house customizing (it is not a `HouseFoundation`), no boats or other multis, no house placement inside
  (`HouseRegion.AllowHousing` is false, `Regions\HouseRegion.cs:44`).
- Player vendors: not in the first build (open question 9): their inventories and rentals add a second set of
  money rules that the eviction would have to settle.

## 2. Engine facts (pinned, file:line)

### What `BaseHouse` gives us

| Fact | Where |
|---|---|
| `abstract partial class BaseHouse : BaseMulti`; ctor `BaseHouse(int multiID, Mobile owner, int maxLockDown, int maxSecure)` | `UOContent\Multis\Houses\BaseHouse.cs:21`, `:44` |
| The footprint is two abstract members a subclass gives: `Area` (rectangles) and `BaseBanLocation` | `:336`, `:337` |
| Lists: `CoOwners`, `Friends`, `Access`, `Bans`; limits `MaxCoOwners` 15, `MaxFriends` 140 (AOS) | `:440-446`; `:25`, `:97`; checked at `:2807`, `:2877` |
| `LockDowns`, `Secures` (with per-item `SecureLevel`), `MaxLockDowns`, `MaxSecures` | `:514`, `:516`; `:437`, `:403` |
| Under AOS rules the limits come from `GetAosMaxLockdowns` / `GetAosMaxSecures`, both virtual, and both **0** when the house has no `HousePlacementEntry` (a leasehold has none), so the leasehold must override them | `:677-699` |
| Locking down needs a co-owner (`LockDown` checks `IsCoOwner`); not virtual | `:2159-2161` |
| Under AOS any character on the owner's account is the owner (`IsOwner` checks `AccountHandler.CheckAccount`) | `:3554-3556` |
| `Doors` (a list of `BaseDoor`), `Sign` (`HouseSign`), `MovingCrate`, `Price`, `RestrictDecay`, `DecayType` (virtual) | `:448`, `:518`, `:530`, `:546`, `:104`, `:110` |
| `AllHouses`, a static list of every house | `:334` |
| `UpdateRegion` is virtual: it builds a `HouseRegion` and registers it; it runs on map and location change and in `Deserialize` | `:1645-1658`; `:1596`, `:1678`, `:3165` |
| `IsInside(Point3D, int)` is virtual and by default reads the **multi component list** tiles, not `Area` | `:1513-1545` |
| `FindHouseAt` asks the map for multis in the sector at that point, then `IsInside` | `:1434-1450` |
| Hand-written serialization, version 15 | `:2910-2914`, `:3004-3008` |
| `OnAfterDelete` deletes the sign and **every door in `Doors`**, and only unlocks the lockdowns (they stay on the floor, movable) | `:3371-3420` |
| Demolish refunds `Price` to the bank under AOS (or gives the deed), from the owner's house gump | `UOContent\Gumps\Houses\ConfirmDemolishHouseGump.cs:99-113`; `Gumps\Houses\HouseGumpAOS.cs:1447-1466` |
| A sign with an ownerless house lets a co-owner or friend **claim** it | `Multis\Houses\HouseSign.cs:155-175` |
| Stock houses are `[SerializationGenerator(0, false)] partial` subclasses of `BaseHouse` | `Multis\Houses\Houses.cs:7-8`, `:42-43` |

### The one-house rule today

- The house table is keyed by owner (`BaseHouse.cs:29`, filled at `:80` and on owner change `:354-368`). `HasHouse`
  (`:3523`) and `HasAccountHouse` (`:3541`, every character on the account) read it. Any `BaseHouse` subclass with an
  owner counts, so a leasehold counts with no code of ours.
- Enforced at: house deeds (`Multis\HouseDeed.cs:36`, `:64`), the placement tool (`HousePlacementTool.cs:195`,
  `:1989`, `:2092`), claiming from a sign (`HouseSign.cs:145`, `:167`), house transfer (`BaseHouse.cs:2287`, `:2360`,
  `:3799`). Staff (GameMaster and up) are exempt everywhere.
- Not enforced anywhere by a house that makes itself: Knive's purchase never asks (P405). Ours asks at lease time.
- The shard changes none of this: no customization or patch calls or overrides `HasAccountHouse` (searched
  `server\customizations` and `server\patches` in the code repo).

### Regions: what a leasehold inside a guarded town needs

- `HouseRegion` is built with **no parent** (`base(null, house.Map, HousePriority, GetArea(house))`,
  `UOContent\Regions\HouseRegion.cs:18`) at priority `DefaultPriority + 1` (`:12`; `DefaultPriority` is 50,
  `Server\Regions\Region.cs:126`). Its area is every `Area` rectangle at **full height** (`GetArea`, `:46-62`, with
  `ConvertTo3D`), so an upstairs-only lease would also take the shop below it.
- Region lookup: a sector's regions are ordered by priority, then by child level (`Region.cs:252`), and `Find` returns
  the first that contains the point (`:291-310`). So a house region (51) wins over a town (50) where they overlap.
- Guards are found by walking up the parent chain: `GetRegion<T>` (`Region.cs:458`), `IsPartOf<T>` (`:539`). Every
  guard check starts from the mobile's region: `from.Region.GetRegion<GuardedRegion>()`
  (`UOContent\Regions\GuardedRegion.cs:63`, `:86`, `:113`). With no parent, a house in Britain is **outside** the
  guards: a free-fire room in the middle of town.
- A region's default handlers pass to its parent: `OnAggressed` (`Region.cs:768`), `OnSpeech` (`:836`),
  `OnBeginSpellCast` (`:845`), `AllowHousing` (`:793`); `GuardedRegion` overrides them to call the guards (`:140`,
  `:184`, `:199`, `:209`, `:226`), and `HouseRegion.OnSpeech` calls `base.OnSpeech` first (`HouseRegion.cs:226-228`).
  So with the town as its parent, "guards!" and criminal acts inside a leasehold reach the town's guards.
- Moving between regions runs `OnExit` and `OnEnter` only up to the shared ancestor (`Region.cs:909-940`). Stepping
  from Britain into a leasehold whose parent is Britain enters the house region only: no "you have left the
  protection of the guards" message.
- A child region takes its parent's priority unless the constructor that names both is used
  (`Region.cs:147`, `:159-178`), so a leasehold region can be the town's child and still outrank it (51).
- Britain is a `TownRegion` (a `GuardedRegion`, `UOContent\Regions\TownRegion.cs:5`) at priority 50
  (`Distribution\Data\regions.json:118-131`), and its inns and banks are unnamed child `TownRegion`s with
  `NoLogoutDelay` (`regions.json:133-150`). So the leasehold's parent must be **the region found at the building**
  (`Region.Find` at the sign spot, before the leasehold's own region is registered), not "the town": a leasehold over
  an inn's rooms keeps the inn's rules.
- Regions load before the world (`Server\Main.cs:671-672`), so a leasehold being loaded can find its parent.
- Shard code that asks what region it is in, and how a leasehold with a town parent answers (all as wanted):
  climbing is refused in towns and houses (`server\customizations\ClusterFClimbing.cs:279`); the Chest of Sending works
  in a house (`Items\Tools\ChestOfSending.cs:97`, `:209`); deployable traps are refused in guarded regions
  (`Items\Traps\Deployable\DeployableTraps.cs:389`); the Fountain of Youth pool is never in town (`FountainOfYouth\FountainPool.cs:250`).

**The change it needs (one stock patch):** a second `HouseRegion` constructor that takes a parent, a priority and a
3D area: `HouseRegion(BaseHouse house, Region parent, int priority, Rectangle3D[] area)`. `ClusterFLeaseholdRegion :
HouseRegion` uses it, and `ClusterFLeasehold.UpdateRegion` builds that region (the Z range kept, the parent found as
above). About 10 lines, as `server\patches\HouseRegion-parent.patch`; the stock houses are untouched. Deriving from
`HouseRegion` (not a region of our own) matters: stock and shard code ask `IsPartOf<HouseRegion>` (the list above).

### The footprint: multis and component lists

- A multi's component list is `MultiData.GetComponents(ItemID)` (`Server\Items\BaseMulti.cs:88`), one cached list per
  multi id (`Server\Client\MultiData.cs:52-53`); an id with no client multi gets the one shared
  `MultiComponentList.Empty` (`:53`, `:185`).
- Knive's town house uses id 0x1DD6 (`Items\TownHouse.cs:67`, `:332`). The client's multi data has no multi 0x1DD6
  (looked up in `D:\UO\ClassicUO\ClassicUO\Ultima Online Classic\multi.idx`: "No multi found for ID 7638"), so the
  client draws nothing there (good), but pinned hands every such house the shared `Empty` list, and Knive's
  `Components.Resize` (`TownHouse.cs:142-143`) resizes that one list for every unknown multi in the game.
- A per-instance list is the stock way: `HouseFoundation` overrides `Components` (`Multis\Houses\HouseFoundation.cs:117`),
  and `MultiComponentList` has a copy constructor and `Resize` (`MultiData.cs:189`, `:637`).
- The map registers a multi in every sector its component list's bounds cover (`Server\Maps\Map.cs:759-773`), so the
  list's size must span the leasehold's rectangles for `FindHouseAt` to find it everywhere inside.
- So `ClusterFLeasehold`: an id with no client multi (to be confirmed in TazUO in build L1: nothing drawn), a
  per-instance empty component list sized to the rectangles' bounds, built from the site's rectangles on every load
  (never saved), and `IsInside` overridden to "inside one of the rectangles and inside the Z range".

### Doors

- Town doors are plain `BaseDoor`s (`Items\Construction\Doors\BaseDoor.cs:11`); they lock with keys (`UseLocks`, `:322`)
  and know nothing of houses. House doors are `BaseHouseDoor` (`HouseDoors.cs:59`, `ISecurable`): under AOS they use
  the house's security levels instead of keys (`:136`; the access check `CheckAccess`, `:99-118`).
- Because `OnAfterDelete` deletes every door in `Doors` (above), the town's own doors must never be put in that list.
  Hence the swap in "Staff place a leasehold": house doors made for the lease are deleted with it; the town's originals
  wait on the internal map and come back.

### Money

- `Banker.Withdraw(from, amount)` takes account gold first, then bank gold and checks (`Banker.cs:158-200`);
  `Deposit` (`:209`) and `DepositUpTo` (`:316`) put it back. Both work for a player who is offline (they use the
  bank box), which the rent sweep needs.
- The stock rented vendor holds rent as escrow and moves it on renewal, never creating gold (`RentedVendor.cs:330-357`),
  and rebuilds its timer on load from the saved expiry time (`:199`). Our rent and room escrow follow that.

## 3. The holes P405 found, and how this design closes each

P405's line references were spot-checked in the download this session (`TownHouseSign.cs:900-910`, `:1000-1006`,
`:736-746`, `:814-817`; `RentalContract.cs:98-101`; `TownHouse.cs:140-144`): they say what P405 says.

| Hole (P405) | In the download | Closed by |
|---|---|---|
| **Decoration dupe** | With "keep items", buying makes the building's decorations the owner's movable lockdowns (`TownHouseSign.cs:903-909`); clearing the house recreates every recorded decoration (`:1000-1032`), so each cycle gives a fresh set | No decoration sale at all. Fixtures stay the town's, never lockdowns, never movable, never recreated. Nothing in our code makes an item from a record. Test: lease, decorate, end the lease, and the item count in the area is what it was before the lease plus nothing |
| **Refunds of money never paid** | Demolish refunds `House.Price` (`ConfirmDemolishHouseGump.cs:103-108`) and the pack-up drops a check for it (`TownHouseSign.cs:1199`); staff buy free (`:738`, `:745`) but `House.Price` is still set (`:816`); the price can be changed on an owned sign | `ClusterFLeasehold.Price` is always 0 and `GetDeed` returns nothing, so the stock demolish pays nothing; and the leasehold's sign gump has no demolish (it is our own `ShowSign`, not the stock gump's option). What was paid is kept only as a record. No refunds except the tenant's unused prepaid credit, which is gold they gave. Staff cannot lease with payment waived; a staff test lease is marked so and moves no money either way. Changed terms apply from the next period |
| **Sublet deposit from nothing; possible double deposit** | `RentalContract.DepositTo` makes `new Gold(Price)` (`RentalContract.cs:100`); `Delete` can run `PackUpHouse`, whose house delete deletes the sign, which deletes the contract again (`:250-258`, `:330-385`, `TownHouse.cs:268-286`) | Room money is escrow backed by gold taken from the subtenant. Every payout zeroes the escrow first, then deposits; ending a room is one method that settles once (a settled flag), and the house's delete never pays anything. Test: total gold on the shard (banks, packs, escrows) is the same before and after leasing, subletting, paying, evicting and ending |
| **Every town house shares one footprint** | `Components.Resize` on the cached list (`TownHouse.cs:142-143`, `TownHouseSign.cs:797-798`), which on pinned is the shared `Empty` (section 2) | A per-instance list per leasehold, built from its own rectangles. Test: two leaseholds of different sizes, each `IsInside` only its own, and an unrelated unknown multi's list is still empty |
| **One house per account bypass** | Purchase asks no limit (no `HasAccountHouse` in `TownHouseSign.cs`) | Leasing asks `HasAccountHouse`; the leasehold's owner makes it count everywhere else (section 2). Tests both ways |
| **No guard zone inside** | `HouseRegion` with no parent (`HouseRegion.cs:18`) | The leasehold region's parent is the region at the building (the patch above). Test: a criminal act inside a Britain leasehold calls the guards; the same outside stays as before |
| **Region area edited in place** | `RUOVersion.UpdateRegion` writes into `Region.Area` (`RUOVersion.cs:47-58`), get-only on pinned (`Region.cs:212`) | `UpdateRegion` overridden: a new region each time, the stock way (`BaseHouse.cs:1645-1658`) |
| **Global hooks** | A speech handler runs `FindHouseAt` on every line anyone says (`General.cs:27`, `:72-114`); a world-save hook rechecks every sign (`:47-60`) | None. Speech inside is the house region's own (stock); the rent sweep is one 15-minute timer over the leaseholds only |
| **Loose rectangles trap passers-by** | `HouseRegion` ejects non-friends from a private house (`HouseRegion.cs:95-128`) | The setup preview, the "one region" and "ban spot outside" checks, and refusing any NPC, spawner or service inside |

## 4. Save safety

### New saved types, each versioned

| Type | Base | Saves | Version |
|---|---|---|---|
| `ClusterFLeaseSign` (the site) | `HouseSign` (itself `[SerializationGenerator(0, false)]`, `HouseSign.cs:9`) or `Item` | rectangles, Z range, ban spot, terms, state (vacant, leased, grace, hold), the leasehold, the original doors, the lease record | `[SerializationGenerator(0)]`; each later field a new version with a migration file in `server\migrations\` as the shard does |
| `ClusterFLeasehold` | `BaseHouse` | its site, nothing it can rebuild (the component list and region are rebuilt on load) | `[SerializationGenerator(0, false)] partial`, the stock pattern (`Houses.cs:7-8`) |
| `ClusterFLeaseholdRegion` | `HouseRegion` | nothing (built by `UpdateRegion`) | not saved |
| `ClusterFLeaseDoor`, `ClusterFRoomDoor` | `GenericHouseDoor` | the room (for a room door) | `[SerializationGenerator(0)]` |
| The lease and each room | embedded records on the site (tenant, paid through, credit, grace started, room rectangles, subtenant, escrow, share) | | versioned with the site |
| `ClusterFLeaseBelongings` | `Container` | nothing extra | `[SerializationGenerator(0)]` |

The site is the source of truth; the leasehold is rebuilt around it. Rent is computed from saved times (paid through,
grace started), never from a timer's state, so a restart or a long downtime only means the sweep catches up.

### What a failed or missed load does

- **A type that fails to load** stops the world load with ModernUO's prompts (as a newer save does on an older build, seen
  on the test shard in October). That is why each build prompt tests a save and load round trip in the
  test host, and loads the shard's own last test save before it merges.
- **The leasehold is missing but its site says leased** (the house failed to load, or was deleted by staff): the site
  goes to **hold**. No rent is charged, no eviction runs, the tenant gets a login message, and `[Leaseholds` shows it
  for staff, who re-make the house from the site (same tenant, same terms) or end the lease. Nothing is deleted.
- **The site is missing but a leasehold exists:** the leasehold marks itself orphaned on load. It stays a house as it
  is, rent frozen, until staff re-link or end it. Never deleted automatically.
- **The parent region is gone** (a town region renamed in a later `regions.json`): the leasehold takes the region found
  at its sign spot that day, which may be none (the facet), and logs it for staff. Guards may then not cover it until
  a GM checks it: a warning in `[Leaseholds`.
- **Downtime:** the grace runs only while the server is up, and an eviction never happens on the first sweep after a
  start. A shard down for a weekend never evicts anyone on Monday morning.
- **Removing the feature later:** a staff command ends every lease (belongings packed to banks, credit returned, doors
  restored) and removes the sites; the types stay in the code, as stubs if need be, so old saves still load.

## 5. Build plan

Staff tools first, then leasing and rent, then sublets; each leaves the shard working, and nothing appears to players
until build L2 and staff place a site.

| # | Prompt | Touches | Size | What it builds | Tests |
|---|---|---|---|---|---|
| L0 | Pick the buildings (survey) | docs-only, map | S | Renders and a list of 2 to 4 empty buildings per major town (open question 6), each with rectangles, Z range, sign and ban spots, doors; none with an NPC, bank or spawner inside | none (a list for Chase to approve) |
| L1 | Leasehold core and staff tools | server-patches, server | M | `HouseRegion-parent.patch`; `ClusterFLeaseSign`, `ClusterFLeasehold`, `ClusterFLeaseholdRegion`, the per-instance component list, `IsInside` by rectangles and Z; door swap and restore; `[Leaseholds new`, `list`, `go`, `edit`, `hold`, `remove`, and `assign <me>` (a staff test lease, no money); the placement checks and preview | xUnit in the shard's test host: the region chain finds Britain's guards inside and `IsPartOf<HouseRegion>`; `FindHouseAt` inside, outside, above and below the Z range; two leaseholds keep their own footprints and `MultiComponentList.Empty` stays empty; site removal puts the original doors back; save and load round trip; the tenant's `HasAccountHouse` is true. Test shard: one site in Britain made with the tool, screenshots by the Tester (the client draws nothing odd; doors and lockdown work) |
| L2 | Leasing and rent | server | M | The Lease Sign gump; lease (one-house check, payment); the lease house gump (stock options without demolish, transfer or customize; with End lease and Rent box); the 15-minute sweep; credit; warnings; grace; eviction to a bank crate; hold and orphan handling | rent taken once per period across a restart; a tenant with no gold gets the warnings, then the grace, then eviction, with every item in the crate (counted) and none deleted; total gold conserved (count before and after); a house owner cannot lease and a tenant cannot place a deed house; a staff test lease moves no money; first sweep after a start never evicts; hold when the house is missing |
| L3 | Sublets | server | M | Rooms: draw, room door, terms, escrow, the town fee, subtenant lockdowns inside the room only (the leasehold region routes "I wish to lock this down" for a subtenant), room end and eviction to the subtenant's bank, rooms ending with the leasehold | escrow conserved through pay, renew, end early by either side, and the leasehold's eviction; a room ends and pays once even when the house is deleted in the same tick; a subtenant cannot lock down outside the room; one room per account |
| L4 | Guides and notes | docs-only | S | Player guide page, staff guide (placing a site), patch notes lines, play-test plan items | none |
| L5 | Place the sites | server (data) | S | The approved L0 list as a data file `[Leaseholds` can load, idempotent like the shard's seeders (`ClusterFRegistrarOfficeSeeder.cs` and others) | a second load changes nothing; each site passes the placement checks |

L1 touches a stock file through a patch, so it goes through the integrator's full build; L2 and L3 are custom code
only. None of these is Codex-lane work (L1 needs the test shard).

## 6. Open questions for Chase

Each has a recommendation first.

1. **Rent, sale, or both?** (a) **Rent only** (recommended: a steady gold sink, and buildings come back when players
   leave); (b) each site staff choose: rent or sale; (c) sale only, with sublets.
2. **Rent amount.** (a) **Staff set per site, the gump suggesting about 25 gold per floor tile per week** (a 7 by 7 shop
   about 1,200 a week) (recommended); (b) a flat price by town (Britain 5,000 a week, a small town 2,000); (c) by tile
   only, no staff choice.
3. **Rent period.** (a) **Weekly, prepay up to 4 weeks** (recommended); (b) daily; (c) every 4 weeks.
4. **Grace before eviction.** (a) **7 days** (recommended); (b) 3 days; (c) 14 days. During grace nothing new can be
   locked down; paying ends it.
5. **Belongings on eviction.** (a) **A crate in the tenant's bank, even past the bank's item limit** (recommended);
   (b) a crate held by the town's banker for 30 days, then gone; (c) left in place, locked, until paid (keeps the
   building out of use).
6. **How many per town.** (a) **2 to 4 in each major town, 1 in a small one, picked in L0** (recommended start);
   (b) every empty building; (c) Britain only, as a pilot.
7. **Sublets.** Who: (a) **leasehold tenants only** (recommended) or (b) any house owner (Knive's way). The cut:
   (a) **10% to the town, a gold sink** (recommended) or (b) none. Limits: **1 room per 50 floor tiles, at most 4;
   one room per account; a room is not a house** (recommended), or (b) rooms count as the account's house.
8. **Lockdowns and secures.** (a) **As a stock house of about the same floor area** (recommended); (b) Knive's
   suggestion from the area; (c) staff set each.
9. **Player vendors in a leasehold.** (a) **Not in the first build** (recommended); (b) yes, as in a house.
10. **Which facets.** (a) **Trammel and Felucca towns both** (recommended: the same buildings, two sites); (b) Trammel
    only; (c) also Malas, Tokuno and Ter Mur towns later.
11. **Who may lease.** (a) **Any non-Young character on an account with no house** (recommended); (b) anyone, Young
    too; (c) a minimum account age (for example 7 days).
12. **Private or public.** (a) **As any house: the tenant chooses, with bans and ejection** (recommended); (b) always
    public (shops), no ejection; (c) private only.

## What I could not verify

- That TazUO draws nothing for a multi id with no client multi (the client data has none for 0x1DD6; the drawing is
  for L1 to see on the test shard).
- How the stock AOS house gump behaves on a house with no `HousePlacementEntry` beyond the lockdown counts (L1 reads
  it when it overrides them).
- Whether the shard's own regions differ from pinned's `regions.json` in the towns L0 picks (the tool reads the live
  region at each site, so it does not depend on it).

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun -CodeRepo D:\UO\golems\Iron\ShatteredLegacy -DocsRepo D:\UO\golems\Iron\shard-migration -Branch golem/Iron/P409 -NoRefresh`:
code clean (nothing changed), docs dry run (this notes file only). No file over 5 MB.

P409 DONE
