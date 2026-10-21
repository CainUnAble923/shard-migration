# cc-P268: High Seas ships (galleons, ship combat, cannons): port assessment

Written 2026-10-21 by the Stone Golem (Opus), on branch golem/Stone/P268. Prompt:
`cc-prompts/claimed/Stone/cc-P268-high-seas-ships-assessment.md`. Docs-only: nothing in `D:\ShatteredLegacy` was
edited, nothing was built, nothing touched Haven or the test shard.

## Headlines

1. **This PC is missing the read-only sources the prompt names.** `D:\UO\ServUO-pub57`, `D:\UO\ModernUO-pinned`,
   `D:\UO\third-party\code\PORT-ASSESSMENT.md` (the folder `D:\UO\third-party\code` is empty) and
   `D:\ShatteredLegacy\client-data\` are all absent. As the prompt allows, I used the public repositories, cloned into
   this session's scratchpad (never into either repo):
   - ModernUO at `d4531cd94b739613155225c234900de9f47d2c88`, the same commit the shard pins, checked with `git rev-parse`.
     4,214 `.cs` files, matching AGENTS.md's count.
   - ServUO tag `pub57`, which resolves to `d76bf4443cf76d081ddaf8f57c87ff33749256af` (committed 2026-08-04).
     **Unverified:** that this is the same tree as Chase's local copy. My High Seas folder counts match the 2026-09-06
     feasibility doc to within a few lines per folder (Multis 15 files and 5,135 lines both times), so it is very likely
     the same release.
   - TazUO at the shard's pin `3212623f` (`client\TAZUO_COMMIT`).
   - P93's house format was read from the project copy, `notes\servuo-code-port-assessment.md`.
   - **The client data could not be checked.** The uoAware tool's saved folder points at the missing
     `client-data\classic-client-7.0.117.0`.
2. **Ships in ServUO: 101 files and 21,164 lines of High Seas ship code.** On top of that come 15 files and 5,523
   lines in `Multis/Boats` (ServUO's `BaseBoat` is 3,466 lines against pinned's 2,221), and about 36 shared files with
   small hooks. There are four galleons (Orcish, Gargish, Tokuno, Britannian) and a rowboat. Combat uses two cannon
   generations; the shard runs EJ, so the second (Culverin, Carronade, Blundercannon) is the live one. One hull-hits pool
   drives four damage states, then scuttling, emergency and permanent repair. AI pirate and merchant ships run the
   bounty quest. Sections 1 and 4.
3. **Pinned ModernUO already does the hard network half.** It builds and sends the High Seas smooth-move packet 0xF6
   to HS clients (`UOContent/Multis/Boats/BaseBoat.cs:1771-1846`, `BoatPackets.cs:30-63`). It loads
   `MultiCollection.uop` with the per-tile flags galleon fixtures need (`Server/Client/MultiData.cs:55-133, :107-121`).
   **It has no galleon, hits, cannon or mouse piloting.** Its BaseBoat hard-builds the classic four parts (tiller man,
   hold, two planks; `:120-138`) and has a four-ID facing switch (`:1994-2120`). Section 2.
4. **Client: TazUO is ready; no player package push is needed for any phase.** TazUO handles 0xF6 and 0xF7, loads
   multis from `MultiCollection.uop` or the .mul files, and steers a boat with the arrow keys and 0xBF 0x33. It has no
   ship UI, but every ship window in ServUO is a server gump. Players' game data comes from their own EA install
   (`player-package\Build-PlayerPackage.ps1:44-48`), which postdates High Seas by years. **One server-side check is
   open:** whether the shard's own `client-data\classic-client-7.0.117.0` holds multis 0x18-0x47. That folder is the one
   the server reads; the check needs Chase's PC. Section 3.
5. **Recommendation: port it in four phases**, starting with galleons that sail (phase 1, large: one engine patch plus
   about 4,000 ported lines). Phase 2 is hull damage and repair; it reverses D-132 so the sea champions damage boats.
   Phase 3 is cannons. Phase 4 is crews and the bounty quest, blocked on the Mondain's Legacy quest framework.
   **This reverses a recorded decision:** `docs/content-menu.md:61` lists "High Seas naval combat" as declined
   ("core surgery, not content"). Agents do not edit `docs\`, so Chase or the overseer must record the change. Section 6
   has the draft phase 1 prompt.

## 1. What the ships are, in ServUO pub57

Shorthand: HS/ = `Scripts/Services/Expansions/High Seas/`, BB = `Scripts/Multis/Boats/BaseBoat.cs`, BG =
`HS/Multis/BaseGalleon.cs`. Every count is `wc -l`. I spot-checked the stats against the files myself (MaxHits,
NorthID, MaxCannons, `IsClassicBoat` at BG:86, the empty `GargoyleShipwright.cs`).

### 1.1 The ships

| Ship (file, lines) | Multi IDs N/E/S/W | Damaged art | Hull hits | Cannon pads | Hold (stones) | How a player gets one |
|---|---|---|---|---|---|---|
| Orcish galleon (`OrcishGalleon.cs`, 347) | 0x18-0x1B (:10-13) | +4 per state, to 0x23 | 100,000 (:25) | 7 (:21), cannon damage ×1.3 (:22) | 14,000 (`GalleonHold.cs:24`) | 8 RuinedShipPlans joined (`HS/Items/RuinedShipPlans.cs:85-87`), plans from the bounty quest (`ProfessionalBountyQuest.cs:293`) |
| Gargish galleon (`GargishGalleon.cs`, 295) | 0x24-0x27 | to 0x2F | 140,000 (:24) | 7 | 12,000 | Shipwright, 200,002 gp, only in the Sea Market or Tokuno docks (`Scripts/VendorInfo/SBShipwright.cs:50-53`) |
| Tokuno galleon (`TokunoGalleon.cs`, 264) | 0x30-0x33 | to 0x3B | 100,000 | 5 | 16,000 | Shipwright, 150,002 gp (`SBShipwright.cs:52`); fishing gain bonus aboard (`Scripts/Misc/SkillCheck.cs:144`) |
| Britannian ship (`BritannianShip.cs`, 364) | 0x40-0x43 | one step only | 200,000 (:25) | 9 (:24), 2 deck addons | 28,000 | Sam's collection reward (`Scripts/Mobiles/NPCs/Sam.cs:109`) and the Ultima Store (`UltimaStore.cs:316`) |
| Rowboat (`Rowboat.cs`, 404) | 0x3C-0x3F | none | 25,000 (BB default) | 0 | none | Shipwright, 6,252 gp (`SBShipwright.cs:54`); deletes itself 5 min after it is left empty (BB:349-352) |

Classic boats under ServUO also get 25,000 hits (BB:286). The pumpkin rowboat and pumpkin cannon (Forsaken Foes) and
Rising Tide's manned cannon and plunder beacons are seasonal (12 files, 3,166 lines). They come later with events.

### 1.2 What a galleon is, against a classic boat

- It is built with `isClassic=false` (BG:99). It gets no tiller man, planks, hold item or keys; those are made only for
  classic boats (BB:330-341).
- **`AddFixtures` (BG:107-155) builds its parts from the multi's own tiles.** Each tile flagged None or Generic in
  `MultiData` becomes a fixture:
  - a mooring line (item IDs 0x14F8 and 0x14FA),
  - the hold and its extra hold tiles,
  - the wheel,
  - a weapon pad per cannon tile,
  - a deck item for the rest.
- Access uses a security list (NA, Denied, Passenger, Crewman, Officer, Captain; BG:21, `SecurityEntry` BG:1613), not
  keys.
- Its pilot is a mobile, `GalleonPilot` (531 lines). The pilot's context menu has emergency repair, ship repair, move
  pilot and the security gumps.
- Placing one hands out two ship recall runes (pack and bank, BG:443-520). Recall, Gate, Mark and Sacred Journey know
  galleons (`Scripts/Spells/Fourth/Recall.cs:132` and others).
- Paint: up to four coats, each wearing off over 14 days (BG:1060-1180). The Boat Painter sells eight hues and a
  remover.
- Mast tiles are left out of collision (BG:340-372).
- **There is no hatch.** `grep -i hatch` finds nothing; the prompt's "hatch" is the hold tiles.

### 1.3 Components

| Part | File (lines) | Does |
|---|---|---|
| Wheel | `HS/Multis/ShipWheel.cs` (98) | Use it to pilot: the player "mounts" the ship (`BaseBoat : IMount`, BB:31; `BoatMountItem.cs`, 49) and steers with the mouse. That is 0xBF sub 0x33, handled in `HS/Network/PacketHandlers.cs` (34) → `OnMousePilotCommand` (BB:2760). It refuses if you are unaboard, unauthorised, mounted, flying, or the ship is too damaged |
| Hold | `GalleonHold.cs` (141) | the container (capacities in 1.1); `HoldItem` tiles open it |
| Mooring lines | `MooringLine.cs` (217) | board the ship, or step to the nearest dock or land; dry dock entry |
| Pilot | `GalleonPilot.cs` (531) | a `BaseCreature`; repair and security menus |
| Fittings | `GalleonItem.cs` (63), `GalleonContainer.cs` (164) | `DeckItem`, `WeaponPad`; a 1,250-stone ship container (**unverified** how a player gets one: nothing calls its constructor) |
| Tracking | `ShipTracking.cs` (249) | an arrow to your ship, range 200 |
| Ship rune | `ShipRune.cs` (101) | becomes a recall rune linked to the galleon |
| Placement and access gumps | `HS/Gumps/` 7 files (1,048) | placement preview, security, access list, grant access, bounty board, cannon gump |

### 1.4 Combat

- **Two cannon generations, picked by `Core.EJ`** (BG:566-583, 600-636). This shard is EJ
  (`Configuration/expansion.json`, AGENTS.md), so it gets the second:
  - **Pre-EJ:** `BaseCannon : Item` in `Cannon.cs` (1,491 lines). Light and heavy ship cannons.
  - **EJ:** `BaseShipCannon : Container` in `ShipCannon.cs` (1,512 lines), with 100 hits and a 3-item magazine.
    Culverin (light, range 10), Carronade (heavy, range 10), Blundercannon (massive, range 12).
- **Ammunition** (`AmmoInfo.cs`, 169): cannonball, grapeshot, frost and flame cannonballs. Under EJ:
  - a cannonball does 5,000 to a ship;
  - grapeshot does 100-150 and strikes the mobiles on deck;
  - frost does 30-50 and flame 5,000, half physical and half element.
  - `SpecialAmmo.cs` (244) is never registered, so it is dead code.
- **Firing is manual**, through the cannon gump (`ShipCannon.cs:97-514`):
  1. swab and ramrod,
  2. a powder charge,
  3. load,
  4. a fuse cord,
  5. light the fuse with lit matches or a torch; it fires 1.5 s later.
- **Arc:** straight along the cannon's facing, widening by one tile every three. Ship damage is multiplied by the
  galleon's `CannonDamageMod`. Enemy cannons within a tile of the hit take the full damage (`OnShipHit` :787-872).
- **Who is an enemy** (BB:386-414): any ship on Felucca. Off Felucca, two player ships are never enemies; otherwise
  `CanBeHarmful` decides.
- **No grappling or boarding items.** A scuttled ship lets enemies aboard (BG:535-541).
- **Crafting the supplies** (`Scripts/Services/Craft`):
  - Blacksmithy: cannonballs, grapeshot, and the light and heavy cannon deeds, which also need Carpentry
    (`DefBlacksmithy.cs:843-875`).
  - Alchemy: black powder, fuse cord, potash, and match cord (pre-EJ only) (`DefAlchemy.cs:274-358`).
  - Tailoring: powder charges (`DefTailoring.cs:198-208`).
  - Tinkering: ramrod, swab, matches (`DefTinkering.cs:248-252, :439`).
  - Cooking: charcoal (`DefCooking.cs:242`).
  - The EJ cannon deeds are not crafted; they come from bounty loot and Rising Tide rewards
    (`BountyQuestSpawner.cs:652-667`).
  - **Unverified:** whether an EJ shard can still craft the pre-EJ deeds and what deploying one does. The recipes at
    `DefBlacksmithy.cs:869-875` sit outside the `Core.EJ` branches I read.

### 1.5 Damage, repair, sinking

- **One pool, hull hits.** Sails and the wheel have no damage of their own.
  - Damage states: 100, 75, 50 and 25 % (BB:460-469). Each state changes the multi ID and rebuilds the fixtures
    (BB:76-92).
  - Below 25 % the ship is scuttled (BB:287-290). Moderately damaged or worse, it moves slowly (BB:1988).
  - Cannons have their own hits and are destroyed at 0.
- **Emergency repair** (BB:1161-1272): 55 cloth and 25 boards let a scuttled ship sail for 6 minutes.
- **Permanent repair** (BB:1285-1448): only near shore or the Sea Market. It costs 17 wood and 17 cloth per point,
  less Carpentry/200 and Tailoring/200, and repairs in proportion to what you have.
- **Cannon repair** (`ShipCannon.cs:979-1038`): iron ingots, less Blacksmithy/200.
- **Combat never sinks a player ship;** at zero hits it is only scuttled.
  - Decay sinks an empty, unmoving ship (BB:2951-3007).
  - It docks at the owner's lighthouse if one is linked (`LighthouseAddon.cs:61`, hold moved at :109-110).
  - Otherwise the ship is deleted, cargo and all (BG:855-888).
  - AI ships force-decay 30 minutes after their captain dies (`BaseShipCaptain.cs:187-226`).

### 1.6 Crews and world content

| Piece | Files (lines) | Notes |
|---|---|---|
| Bounty quest, AI ships | `HS/Quests/ProfessionalBountyQuest` 12 (2,355) | `BaseShipCaptain` spawns an Orcish, Tokuno or Gargish galleon with 3-5 crew and auto-cannons; pirate and merchant captains and crews; capture alive with binding rope. **`ProfessionalBountyQuest : BaseQuest` and `BountyQuestObjective : BaseObjective`** (:12, :9): the Mondain's Legacy quest framework, which P193 found in neither pinned nor ours |
| Spawner | `HS/Spawners/BountyQuestSpawner.cs` (1,003) | ten zones: pirates by Jhelom, Moonglow and Tokuno; merchants in Trammel, Felucca and Tokuno |
| Sea Market | `HS/Regions/SeaMarket.cs` (425) | bounds 4529,2296 45×112 (:60); optional 20-minute boat limit; pirate chatter |
| Vendors | `HS/Mobiles/Vendors` 8 (619) | DockMaster (dry dock 2,500 gp, retrieve hold), Boat Painter, docks alchemist, tavern keeper. `GargoyleShipwright.cs` is 3 bytes, an empty file |
| Corgul | `HS/Mobiles/Corgul` 8 (1,030), `CorgulAltar.cs` (453), `CorgulRegion.cs` (222), `WarpRegion.cs` (155) | a boat-borne champion, excluded from P193 |
| Decoration | `HS/Generate.cs` (483) | `[DecorateHS`, `[DeleteHS` |

### 1.7 Totals by group (files, lines; lists in the agent table kept in this session, summarised)

| Group | Files | Lines |
|---|---|---|
| HS/Multis (ships and parts) | 15 | 5,135 |
| HS/Items/Cannons and Ammo | 12 | 4,534 |
| HS/Items/Resources (powder makings) | 6 | 428 |
| Other HS ship items (paint, plans, buoy, Corgul altar, smugglers) | 7 | 1,166 |
| HS/Gumps | 7 | 1,048 |
| HS Generate, Persistence, Network | 4 | 661 |
| HS/Regions | 4 | 827 |
| HS/Spawners (bounty; the charybdis spawner is fishing's) | 2 | 1,346 |
| HS/Quests/ProfessionalBountyQuest | 12 | 2,355 |
| HS/Mobiles/Corgul | 8 | 1,030 |
| Sea champions (already ported by P193) | 3 | 1,424 |
| HS vendors | 8 | 619 |
| HS/Items/Artifacts (Corgul and champion loot) | 13 | 591 |
| **HS ships subtotal** | **101** | **21,164** |
| `Scripts/Multis/Boats` (ServUO's BaseBoat family) | 15 | 5,523 |

The HS folder totals (138 files, 31,080 lines, of which 37 files and 9,916 lines are fishing) are from the measuring
agent. I recounted each top-level HS folder myself: Gumps 7/1,048, Items 57/13,750, Mobiles 21/3,174, Multis
15/5,135, Network 2/84, Quests 24/5,139, Regions 4/827, Spawners 2/1,346. That is 132 `.cs` in folders, plus
`Generate.cs` and `Persistence.cs` at the top. **The ships-versus-fishing split of the Items folder is the agent's
classification and I did not recount it.**

## 2. Pinned ModernUO's boat engine (d4531cd94)

Paths are relative to `Projects/`. `UOContent/Multis/Boats/` has 16 files and 3,747 lines (I counted 18 files and
4,014 lines with the two packet test files). BaseBoat.cs is 2,221 of those lines.

**Has:**

- `public abstract partial class BaseBoat : BaseMulti`, source-generated, version 5 (`BaseBoat.cs:22-23`). It saves
  the map item, nav point, facing, decay time, owner, both planks, the tiller man, the hold, the anchor flag and the
  ship name (:82-164).
- **Smooth movement.** `NewBoatMovement => Core.HS` (:230). One-tile moves send 0xF6 once to every `ns.HighSeas`
  client (:1771-1846, :1782-1784), and riders are moved with `NoMoveHS` (`Server/Items/Item.cs:619, :1660`,
  `Server/Mobiles/Mobile.cs:1652, :7381`). Pre-HS clients get ordinary updates. The packet layout is tested
  (`UOContent.Tests/Tests/Multis/Boats/BoatPacketTests.cs:19, :67`).
- **Anything on deck rides along.** The virtual `GetMovingEntities` (:1877, :1939-1984) moves every visible mobile and
  item inside the multi, so loose fixtures would move as cargo.
- **Multi data.** `MultiData.Configure` prefers `MultiCollection.uop` (`Server/Client/MultiData.cs:31, :55-133`). It
  keeps each tile's None/Generic flag (:107-121), exactly what ServUO's `AddFixtures` reads, and masks IDs with
  `& 0x3FFF` (:52-53). **Galleon IDs 0x18-0x47 load if the server's client data has them** (unverified: not run
  against client data).
- **Dry dock.** `CheckDryDock` (:590-632), `BaseDockedBoat` (`BaseDockedBoat.cs:10`, saves multi ID, offset and name),
  `ConfirmDryDockGump.cs`.
- **Deeds.** `BaseBoatDeed` (`BaseBoatDeed.cs:10`); placement through `MultiTarget` (:146); refused in dungeons,
  houses and champion spawns (:154-158). The shard patches it for the fountain sanctum
  (`server\patches\BaseBoatDeed-fountain-sanctum.patch`).
- **Six classic boats**, IDs 0x0-0x17, one 49-line file each holding boat, deed and docked deed.

**Lacks, with where a galleon breaks it:**

- **Fixed parts.** The constructor always creates a tiller man, a hold and two planks (:120-138). They are
  hard-wired into:
  - `UpdateComponents` (:256-291),
  - `OnLocationChange` and `OnMapChange` (:379-394),
  - `OnAfterDelete` (:367),
  - `Contains` (:1515-1520),
  - the moving-entity skip list (:1966),
  - `Move`'s type exclusion (:1795).

  A galleon needs these to be optional.
- **The four-ID facing switch.** `SetFacing` (:1994-2120) maps N/E/S/W to the virtual `NorthID` to `WestID`
  (:196-199) and re-places the tiller man and hold by fixed distances. A galleon instead rebuilds its fixtures per
  facing and per damage state.
- **No hits, damage states or scuttling.** Decay is the only damage: 9 days, then it sinks a z every 5 s and is deleted
  (:57, :424, :2177-2200).
- **No mouse piloting.** There is no `IMount` on BaseBoat, and the 0xBF subcommands stop at 0x32
  (`UOContent/Network/Packets/IncomingExtendedCommandPackets.cs:45-61`; I checked it).
- **Not virtual:** `Move`, `Teleport`, `SetFacing`, `Turn`, `CanFit`, `UpdateComponents`, `CheckDryDock`, the speech
  command set and the movement constants.
- **`CanFit` (:1416-1498)** has no mast-tile or overhead exemption. A galleon's masts and rigging would fail it.
- **No boat region, no galleons, no cannons, no rowboat.** `grep` for Galleon, ShipCannon, Hull and BoatRegion finds
  nothing. "Cannon" is only the Uzeraan quest addon.
- **No tests** of movement, turning, decay or deeds. Path tests exist (`UOContent.Tests/Tests/Engines/Pathing/Multi/`).
- **An upstream bug, found in passing:** `BaseBoatDeed.cs:80-83` sends "Boat placement is temporarily disabled." but
  has no `return`, so the deed is still placed. The docked form returns (`BaseDockedBoat.cs:104-108`). It matters only
  if the feature flag is ever turned off. It is worth a one-line fix in phase 1, since that phase patches this file
  anyway.

**What a port needs from the engine, then:** one `BaseBoat` patch (or a full-file replacement, the cc-P38 route). It
makes the classic parts optional behind an `IsClassicBoat` flag and adds a virtual `SetFacingComponents` and
`IsComponentItem` (ServUO's names). It adds virtual `IsExcludedTile` and `ExemptOverheadComponent` hooks to `CanFit`,
`IMount` with the 0xBF 0x33 handler and the driver-lock packet, and later the hits members. **ServUO's BaseBoat cannot
be dropped in:** it names galleon and captain types directly (BB:76, :723, :1188, :1291, :2073) and is written
against ServUO's core.

## 3. The client side

- **TazUO `3212623f`** (paths under `src/`):
  - 0xF6 and 0xF7 handlers are always registered (`ClassicUO.Client/Network/PacketHandlers/HandlerRegistry.cs:122-123`),
    with no version or HS gate.
  - Smooth boat movement interpolates the multi and its riders (`Game/Managers/BoatMovingManager.cs:205-383`). It is a
    profile option, **off by default** (`Configuration/Profile.cs:428`); with it off, the boat steps tile by tile.
  - Arrow-key steering sends 0xBF 0x33 (`Network/OutgoingPackets.cs:3748-3765`) while the player's mount graphic is
    0x3E96 (`Game/GameObjects/Mobile.cs:169-175`), which is ServUO's `BoatMountItem`. There is also a BoatControl gump
    from the top bar (`Game/UI/Gumps/BoatControl.cs`).
  - Multis load from `MultiCollection.uop` when `MainMisc.uop` is present, otherwise from multi.mul/idx with the
    post-7.0.9 16-byte record (`ClassicUO.Assets/MultiLoader.cs:25-48, :100`). No galleon ID ranges are special-cased.
    One boat hack makes every tile of a multi movable if any is (`Item.cs:392-399`).
  - **No ship gumps**: hold, cannon, security and tracking are all server gumps or quest arrows, so nothing client-side
    is missing.
  - Quirks: the facing byte of 0xF6 is dropped (`BoatMovingManager.cs:116`), a debug `Console.WriteLine` fires on every
    step (:121), and 0xF7 stops parsing at any sub-packet other than 0xF3 (`PacketList.cs:24-25`). None of these
    blocks a port.
- **Feature bit:** TazUO never reads the HS locked-feature flag (`Game/Data/LockedFeatures.cs:28` is defined and
  unused).
- **The player package:** it ships no EA data; the player's own EA install supplies it
  (`player-package\Build-PlayerPackage.ps1:44-48`, `payload\README.txt:10-14`). Today's EA download is far newer than
  High Seas (October 2010, client 7.0.9.0), so players' clients should have the galleon multis. **Unverified on this
  PC** (public knowledge; no EA folder here).
- **Server data, the one open check:** the server reads multis from the shard's `client-data\classic-client-7.0.117.0`.
  7.0.117 is years after 7.0.9, so it very probably holds 0x18-0x47 in `MultiCollection.uop`. **Unverified: the folder
  is not on this PC.** Phase 1's first step checks it, for example with uoAware `get_multi` or pinned's
  `MultiData.GetComponents(0x18)`. If a galleon multi is missing, phase 1 stops.
- **A package push: none required.** Optional: turning TazUO's smooth boat movement on by default in the package's
  profile seed. It is a nicety and can ride any later push.

## 4. Port effort, blockers and collisions

| Part | ServUO lines | Effort | Blockers |
|---|---|---|---|
| BaseBoat engine patch (optional classic parts, facing hooks, CanFit hooks, IMount, 0xBF 0x33) | n/a; ServUO BB is 3,466 vs pinned 2,221 | **M-L**, one patch on a saved stock type, no new saved fields | none; serialization unchanged if no field is added |
| Galleons, rowboat, fixtures, pilot, wheel, hold, mooring lines, security, deeds, docked deeds, placement gump | ~5,100 (Multis) + ~700 (gumps) | **L** | the multis in server client data (section 3) |
| Ship runes and the spells | ~100 + 4 spell hunks | S-M, a patch on four pinned spells and `RecallRune` (a saved stock type: version bump) | after galleons |
| Paint | ~240 | S | after galleons |
| Hits, damage states, scuttling, repairs | inside BB and BG, ~600 | **M**, plus **a version bump on BaseBoat** if classic boats get hits too (ServUO gives them 25,000). The cc-P127 migration route | after galleons |
| Cannons (EJ), ammo, powder, tools, resources, cannon gump | ~5,000 | **L** | after damage |
| Cannon crafting (five craft systems) | recipe hunks | M; the shard already registers recipes outside the stock files (`CookingCraftRegistrations`, P193) | after cannons |
| Bounty quest, AI captains and crews, bounty spawner, bounty board | ~3,500 | **L** | **the ML quest framework** (`BaseQuest`/`BaseObjective`, a `docs/subsystem-policy.md` decision); AI ships need cannons and damage |
| Sea Market, Tokuno docks regions, dock master, vendors | ~1,050 | M | a map check (below) |
| Orcish galleon for players | n/a | n/a | its only source is the bounty quest's plans (or staff `[add`) |
| Britannian ship for players | n/a | n/a | its sources are Sam's collection and the Ultima Store, neither of which exists here; staff-only until one does |
| Corgul | ~1,860 | M | its own prompt, after cannons |

**Collisions with the shard:**

- **The sea champions (P193).** `BaseSeaChampion.cs:7-8, :189-230` carries a `TryDamageBoat` that only pushes, and
  D-132 records it. Once hits exist (phase 2), D-132 reverses: put `boat.OnTakenDamage` back into `DoDamageBoat`.
  `:10` notes that `GetValidPoint` assumes a classic boat's size; with galleons at sea it needs the galleon branch
  ServUO has.
- **Housing and multis.** Galleons are multis placed through `BaseBoatDeed`, so the fountain sanctum patch
  (`BaseBoatDeed-fountain-sanctum.patch`) must be merged with ServUO's one-ship-per-player rule and placement gump in
  the same file. ServUO's deck addons use `BaseAddonDeed.CheckGalleonPlacement` (`Scripts/Items/Addons/BaseAddonDeed.cs:224`):
  a pinned addon patch, phase-1-optional (the Britannian's two addons only). House placement already refuses on boats
  through `CanFit`'s multi-tile test (`BaseBoat.cs:1446`).
- **Test-account wipe.** `server\customizations\Misc\TestAccountWipe.cs:243, :433-434` counts and deletes owned boats
  through `BaseBoat.Boats`, so galleons are covered once they register there. A galleon's pilot and fixtures must
  delete with it (ServUO does this, BG:855-888).
- **The map.** The shard ships its own Trammel edits (`player-package\vendor\shattered-legacy-map\trammel.mapops`).
  **Unverified:** the Sea Market (4529,2296), the bounty spawn zones and Corgul's rectangle (2400,2500) are open water
  on our facets. Phase 4 checks this with uoAware `check_walkability` or `inspect_map_region`. Galleons need room:
  their footprint is several times a classic boat's (numbers not measured; read them from `get_multi` in phase 1).
- **Expansion.** `Core.HS` and `Core.EJ` are both true here, so pinned's smooth movement is on today and the EJ cannon
  branch is the one to port. The pre-EJ `Cannon.cs` (1,491 lines) can be skipped.
- **Fidelity.** Phase 1 without hits means a galleon cannot be damaged. That is a recorded deviation until phase 2
  (next free D-number). Dry dock refuses only an unpristine ship, so before phase 2 every ship is pristine.

## 5. Phased plan

| Phase | Content | Size | Blocks / blocked by | Player package push |
|---|---|---|---|---|
| **1. Galleons that sail** | BaseBoat patch (optional classic parts, facing and CanFit hooks, IMount, 0xBF 0x33, driver lock, the deed `return` fix); BaseGalleon with fixtures, pilot, wheel, hold, mooring lines, security gumps, placement gump; Tokuno, Gargish, Orcish and Britannian galleons and the rowboat; deeds and docked deeds; Shipwright stock for Tokuno, Gargish and rowboat at ServUO prices (the region rule needs the Sea Market, so it sells anywhere until phase 4: a deviation, or hold the galleons until then; Chase's choice); dry dock through the mooring line. Orcish and Britannian staff-only | **L** (≈4,500 ported lines + one engine patch, 2-3 sittings) | first step: confirm galleon multis in the server's client data | **no** (optional: smooth-movement default on) |
| **2. Hull damage and repair** | hits on BaseBoat (version bump and migration), damage states and art, scuttle, emergency and permanent repair, pilot repair menus, decay into sinking; sea champions damage boats (D-132 reversed); ship runes and the four spells; paint | **M** (1-2 sittings) | after 1 | no |
| **3. Cannons and ship combat** | EJ ship cannons, ammo, powder charges, fuse, matches, ramrod, swab, resources, cannon gump, cannon deeds and deploying, cannon repair, crafting in five systems, Felucca enemy rules; MatchCord and Niter from P193's list | **L** (2 sittings) | after 2 | no |
| **4. Crews and the bounty quest** | AI captains, crews, bounty spawner and board, Sea Market and Tokuno docks regions, dock master and the other vendors, ruined ship plans (players' Orcish galleon) | **L** | after 3, and **after a decision on the ML quest framework**; a map check first | no |
| later | Corgul; Rising Tide and the pumpkin boat and cannon with events; the Britannian ship's sources | M each | after 3 or 4 | no |

## 6. Recommendation and draft phase 1 prompt

**Recommendation: go, phase 1 first, once the server's client data is confirmed to hold the galleon multis.**

- The network and multi-data halves already exist in pinned, so the engine work is one bounded patch, not core surgery.
  The old "declined" verdict (`docs/content-menu.md:61`) was written before this was measured.
- Each phase leaves a working shard, and no phase needs a migration event or a package push.
- Phase 2 is what makes the sea champions whole, so it follows directly.
- Phase 4 should wait for the quest framework decision rather than force a quest port around it.
- **Chase or the overseer must record the reversal in `docs/`**, either the content menu or the backlog's C8
  (`docs/backlog.md:80`). Agents do not edit `docs\`.

### Draft: CC task P2xx: High Seas galleons that sail (ships phase 1)

(Number to be assigned by the overseer; not saved to `cc-prompts\queue\`.)

**Model:** Opus

**Touches:** server (customizations, one BaseBoat patch, one BaseBoatDeed patch hunk), tests, CHANGELOG; no player
package push; test shard rebuild under the `test-shard` lock.

**Summary:** Port ServUO pub57's galleons so a player can buy, place, board, pilot, anchor and dry-dock a Tokuno or
Gargish galleon or a rowboat, with the Orcish galleon and the Britannian ship available to staff. No hull damage, no
cannons, no crews: those are phases 2 to 4 of `notes\cc-P268-high-seas-ships-assessment.md`.

Read first:
- `notes\cc-P268-high-seas-ships-assessment.md` sections 1.2, 1.3, 2 and 4.
- ServUO `Scripts/Services/Expansions/High Seas/Multis/*` (15 files), `High Seas/Gumps/ShipPlacementGump.cs`,
  `ShipSecurityGump.cs`, `ShipAccessListGump.cs`, `GrantAccessGump.cs`, `BaseShipGump.cs`, `High Seas/Network/*`,
  `Scripts/Multis/Boats/BaseBoat.cs` and `BaseBoatDeed.cs`, `Scripts/VendorInfo/SBShipwright.cs`.
- Pinned `UOContent/Multis/Boats/*`, `Server/Client/MultiData.cs`,
  `UOContent/Network/Packets/IncomingExtendedCommandPackets.cs`, and the shard's
  `server\patches\BaseBoatDeed-fountain-sanctum.patch`.

Steps:
1. **Gate:** confirm multis 0x18-0x47 are present in `D:\ShatteredLegacy\client-data\classic-client-7.0.117.0`
   (uoAware `get_multi`, or `MultiData.GetComponents` in a test host), and record each galleon's footprint. If any
   galleon multi is missing, stop and ask Chase.
2. **BaseBoat patch** (pinned's file, no new saved fields):
   - classic parts optional behind a virtual `IsClassicBoat` (true for the six classic boats, so they are unchanged);
   - virtual `SetFacingComponents`, `IsComponentItem`, `IsExcludedTile` and `ExemptOverheadComponent` used by
     `SetFacing`, `Move`, `GetMovingEntities` and `CanFit`;
   - `IMount` with `BoatMountItem`, the 0xBF 0x33 mouse-pilot handler and the driver-lock packet.

   Every classic-boat behaviour must be byte-for-byte unchanged: prove it with facts seen failing first.
3. **BaseBoatDeed hunk:** ServUO's one-ship-per-player rule (rowboats excepted) and the placement gump, merged with
   the fountain sanctum patch. Also add the missing `return` after the placement-disabled message
   (`BaseBoatDeed.cs:80-83`; record it as an upstream bug fix).
4. **Port** `BaseGalleon`, the four galleons, `Rowboat`, `GalleonPilot`, `ShipWheel`, `GalleonHold`, `MooringLine`,
   `GalleonItem`, `GalleonContainer`, `ShipTracking` and the five gumps into
   `server\customizations\Services\Expansions\High Seas\Ships\`. Use source-generated serialization.
   - Galleons take their hits fields now (saved, always full) so phase 2 needs no galleon version bump.
   - Leave out cannons, paint, ship runes and the spells; each gets a deviation row until its phase.
5. **Shipwright stock:** add the Tokuno galleon, Gargish galleon and rowboat deeds at ServUO's prices. ServUO sells the
   galleons only in the Sea Market and Tokuno docks regions, which do not exist yet, so ask Chase: sell them anywhere
   until phase 4 (a recorded deviation), or keep them staff-only until then.
6. **Tests:** construct, round-trip, place, turn, move a step and dry-dock each kind; check the fixtures follow on a
   turn; check riders move. Keep the existing pinned boat tests passing.
7. **Build** with `docker/uo/build.sh` (image tag per the Golem) and boot the test shard under its lock.
8. **Play tests for Chase:** buy a Tokuno galleon at a shipwright, place it at a dock, board by the mooring line,
   take the wheel and steer with the arrow keys, anchor, dry-dock.

Deviations to propose (next free D-numbers):
- galleons cannot be damaged until phase 2;
- no cannons until phase 3;
- the Shipwright's region rule, if step 5 sells anywhere;
- the Orcish galleon and the Britannian ship are staff-only.

Finishing: notes in `notes\cc-P2xx-...md`, last line `P2xx DONE`.

## 7. How this was done

- Three read-only research agents ran in parallel: one each for the ServUO ships, the pinned engine and TazUO.
- I recounted each agent's top-level counts myself and spot-checked the claims a decision rests on:
  - the galleon stats and IDs;
  - `IsClassicBoat` at BG:86;
  - the empty `GargoyleShipwright.cs`;
  - `MultiData`'s flag handling;
  - the 0xBF subcommand list;
  - the missing deed `return`;
  - the pinned `Move` type exclusion;
  - the bounty quest's `BaseQuest` base.
- **Not verified:**
  - the server's and players' client data;
  - the map at the Sea Market and the spawn zones;
  - how a `GalleonContainer` is obtained;
  - the Ultima Store price unit;
  - whether the pre-EJ cannon deeds are craftable under EJ;
  - how a pre-HS client copes with ServUO's unconditional 0xF6. That one is moot here: pinned filters on
    `ns.HighSeas`.
- The clones live only in this session's scratchpad.

P268 DONE
