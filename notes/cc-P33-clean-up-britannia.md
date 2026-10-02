# cc-P33: F-3, Clean Up Britannia ported, with the Custodians as our layer

2026-10-02. Brief: `D:\UO\cc-prompts\cc-P33-clean-up-britannia.md`. Work is in `D:\ShatteredLegacy`, **uncommitted, not
deployed, nothing placed in any world**. Final image `sl-modernuo:cc-p33` (`sl-modernuo:latest` not moved). No commit
landed during the task (both repos still at `a5be9d7` / `045b313` when I checked at the end).

## Headlines

1. **All four stages are built and green.** Points framework and table, barrels and appraisal, the store and both
   NPCs, the Custodian layer and Civic Token retirement. **447 of 447** tests (421 before, **26 new facts**), every new
   fact watched red for its own mutation first (section 8). The build did not stop at a gate.
2. **The anti-farm rule holds for every metal, leather, scale and all 16 of our extended resources: 0 of 4,419 crafted
   piece-resource pairs out-earn their materials**, and the Smith Guild salvage bag (D-98) gives back less than the
   piece took at Mining 300 for every metal. **But OSI's own table breaks the rule for wood and cloth**: 255 pairs out-earn
   their materials, by about one point each (section 5). That is OSI's value table, which the brief says is not ours to
   tune, so I pinned the measurement and left it. **Decision 1 for Chase.**
3. **Magic properties pay nothing extra.** ServUO adds `Imbuing.GetTotalWeight / 30` to crafted gear. Pinned has no
   imbuing and no property-weight table (ServUO `ItemPropertyInfo.cs` plus `Imbuing.cs`, about 3,300 lines), so the
   term is 0: a magic weapon pays only its ingots. That is a large cut in what players earn from trashing loot. **Decision 2.**
4. **85 of OSI's 134 rewards do not exist in pinned or ours** and are left out of the store (49 are in, including
   `ScrollOfAlacrity` as pinned's `ScrollofAlacrity`). The store tops out at 150,000; nothing at 250,000 and up exists
   (all 24 pigments, the six 300,000 charms, Vollem). List in section 6. **Decision 3.**
5. **One pinned patch pair was unavoidable for fidelity**: OSI pays for any trash barrel, a house's included, and
   pinned's `TrashBarrel` and `TrashChest` have no hook. Two small patches (`server/patches/Trash{Barrel,Chest}-clean-up-britannia.patch`,
   12 and 37 added lines) call into ours. Argued in section 3.
6. **Civic Tokens were wider than the brief listed.** Besides `AwardTokens` and the shop, tokens also came from the
   Custodians' Apprentice task (`joinScrip: 5`) and from every Civic Contract (`voucherReward`, 10 to 500). All are
   gone; the Civic Contracts now pay gold only. Balances are cleared at world load (section 7).
7. **Two defects found on the way, one fixed:** a Custodian could `[cleanup` a *player's* corpse with all their gear
   (fixed: a player's corpse is not litter). And ours, **not fixed**, out of scope: `CraftResources.GetType`
   (`customizations\ResourceInfo.cs:1095`) stops the wood range at Frostwood, so all eight extended woods report type
   `None` and `GetInfo` returns null for them (section 10).

## 1. Check first, answered

### 1.1 The smallest faithful points framework

Pinned has no points framework (`class PointsSystem` absent from `D:\UO\ModernUO-pinned\Projects`). Built
`customizations\Services\PointsSystems\PointsSystem.cs`, about 270 lines, shaped on ServUO
`Services/PointsSystems/PointsSystem.cs`:

- Kept: a double per `PlayerMobile` (ServUO `PointsEntry`), `AwardPoints` capped at `MaxPoints` (`:120`),
  `DeductPoints` refusing an overdraft (`:149`), `AutoAdd`, a derived entry per system (`GetSystemEntry`, `:198`), one
  save file for every system.
- Storage: pinned's `GenericPersistence` keyed by `PlayerMobile`, the pattern of pinned
  `Engines/CannedEvil/ChampionTitleSystem.cs`. File `Saves/PointsSystem/PointsSystem.bin`. Entries leave with a
  deleted character (`[OnEvent(nameof(PlayerMobile.PlayerDeletedEvent))]`).
- Left out: loyalty gump, titles, kill and quest hooks, `ConvertFromOldSystem`. Nothing here uses them.
- `PointsType` holds only `CleanUpBritannia`; the save writes the name, not the number, so adding one never
  renumbers a save. An unknown name or version fails loudly (the D40 rule).

**Virtue Artifacts needs the same framework, and can reuse this one.** ServUO `VirtueArtifactsSystem.cs` is a
`PointsSystem` with per-character points, `AwardPoints`, `GetPoints`, `SetPoints` (all here) plus a `ProcessKill`
override. Pinned has the kill event it needs: `BaseCreature.CreatureDeathEvent` (`UOContent/Mobiles/BaseCreature.cs:3216`).
So that port adds one `PointsType` value and a subscriber. Its own gate is separate: ServUO enables it only during a
seasonal event (`SeasonalEventSystem.IsActive(EventType.VirtueArtifacts)`), which pinned does not have.

### 1.2 The 134 rewards

Counted from ServUO `Services/CleanUpBritannia/CleanUpBritanniaRewards.cs`, 134 `Rewards.Add` lines (the brief's 134
holds). Resolved by script against every `class` in pinned `Projects` and `server\customizations`, then searched for
other names (case, partial names, `TypeAlias`, same art id). **49 exist** (48 by name, plus `ScrollOfAlacrity` =
pinned `ScrollofAlacrity`, `Items/Special/Special Scrolls/ScrollofAlacrity.cs:10`). **85 do not.** The full list is in
section 6, with ServUO line numbers. Near-equivalents found but **not** used: ServUO's `ChestOfDrawers` (0xA2C,
lockable, cliloc 1022604) looks like pinned's `Drawer` (`Items/Containers/FurnitureContainer.cs:142`, same art,
not lockable), and `FootedChestOfDrawers` (0xA30) like pinned's `FancyDrawer`. They are different items; I left both
out.

### 1.3 What else scores items, and what was retired

The only item scorer in ours was `ClusterFCustodianSystem` itself (`MaterialTokens`, `EstimateVendorGold`,
`ComputeTokens`). Work orders, guild ledgers, smith BODs, commissions and the Artificer orders all count types and
amounts; none values an item. So nothing else needed to read Clean Up's table.

Retired, all of it:

| What | Where it was | Now |
|---|---|---|
| Token math | `ClusterFCustodianSystem.cs:99-160` (old) | `ComputePoints`: Clean Up's `GetPoints`, or the corpse rule |
| `AwardTokens` | `:216` (old) | `AwardPoints`, Clean Up points on the character |
| Ranks | `:228` (old), 100 / 500 / 2,000 / 5,000 tokens | `Ranks`, 25 / 125 / 500 / 1,250 lifetime points (section 4.4) |
| Token shop | `SanitationWardenGump.cs:254-310` (old) | gone; the gump opens the one store |
| Apprentice scrip and standing | `ClusterFGuildSystem.cs:252`, `joinRep: 25, joinScrip: 5` | both 0 |
| Civic Contract vouchers and standing | `ClusterFWorkOrderSystem.cs:2404-2490` | both 0; gold only |
| Token balances | `CharacterGuildData.GuildCurrency["custodians"]` | cleared at world load |

The F-3 entry says `AwardTokens` is account-level. It was not by this build: cc-P18 moved guild data to the character
(`ClusterFAccountData.cs:115-121`). Moot now.

### 1.4 Where the Officer and the barrels stand

- **OSI / ServUO:** ServUO places neither. `TheCleanupOfficer` and `CleanupTrashBarrel` appear only in its
  placement-tool list (`Data/objects.xml:875`, `:6329`), in no spawn or decoration file. From memory, OSI's Cleanup
  Officers stand at city banks, New Haven's included. **Unverified**: nothing in either tree says so.
- **Pinned's decoration** has no trash barrel or trash chest of any kind (`TrashBarrel` appears in pinned only in
  `BaseHouse.cs:2043`, a house barrel, and `categorization.json`).
- **Ours:** `[ClusterFPlaceCleanUp [dryrun]` (Administrator, `[ShardCommand]` WorldSetup / Skips / TestFirst). It
  places the Officer **on the caller's own tile** and a Clean Up barrel one tile east, each skipped if one already stands
  near (15 tiles for an Officer, 3 for a barrel) or if the tile cannot hold it. Nothing is moved or deleted; there is no
  world-load hook. The floor height is the caller's, so nothing is guessed (the test host has no map files, and I would
  not hard-code a z inside the bank building; cc-P17 PT-05 is what that costs).
- **Proposal: New Haven bank first**, standing beside the banker (Sarsmea Smythe, 3492,2577 per
  `ClusterFNewHavenSeeder.cs:56`). Plain trash barrels need nothing: house barrels already pay through the patch.

### 1.5 Per-character storage, the version bump, and the old Civic Token data

- **Clean Up points and lifetime points:** `CleanUpBritanniaEntry` (Points, Lifetime), version 0, in the points save
  above. A new saved type, not on `PlayerMobile`, so no pinned change and no `PlayerMobile` version bump. Round-trip
  fact: `ThePointsSaveRoundTrips` (two characters, every field, the reader stops on the last byte).
- **The version bump is the trash bag**: `TrashBag` 0 -> 1, adding `Owner`. `server\migrations\Server.Items.TrashBag.v0.json`
  (no fields) lets the generator read a version 0 bag; `MigrateFrom(V0Content)` leaves it ownerless. Round-trip fact:
  `TheBagsOwnerSurvivesASaveAndAVersion0BagHasNone` (version 1 survives; version 0 bytes, built as the pre-cc-P33 build
  wrote them, load with no owner and read to the last byte).
- **Old Civic Token data: cleared on load**, not merely left unread (`ClusterFCustodianSystem.RetireCivicTokens`, on
  `EventSink.WorldLoad`). Why: left unread, the balance would be harmless, but the token-earned *standing* would not.
  The standing drives the rank everywhere (directory, rank names, work order gates), so a Chief of tokens would stay
  Chief with no points. The load removes every character's "custodians" scrip and sets its Custodian standing from
  lifetime points. Idempotent (a second load changes nothing), logged once with counts. It needs no fresh world, which
  matters because AGENTS.md rule 7 still says the project never requires one.

## 2. Stage 1: framework and table

- `Services\PointsSystems\PointsSystem.cs` (section 1.1).
- `Services\PointsSystems\CleanUpBritanniaData.cs`: `GetPoints` (ServUO `:37-178`) with every special case in ServUO's
  order; `GetPointsForEquipment` (`:748-813`); the table **generated from ServUO's file line by line** (494 rows, every
  one counted; the brief gave no count). **453 resolve** to a type here and are in the table with ServUO's line number.
  **41 do not**; they stay as `// MISSING :line Type = value` comments so a later port only uncomments them (list in
  `notes\cc-P33-tools\missing-entries.txt`). One rename: ServUO `MetallicClothDyeTub` = pinned `MetallicClothDyetub`.
- Changed from ServUO, each argued:
  - **Imbuing weight term = 0** (Headline 3). Gap, not choice.
  - **Treasure maps use ServUO's old-system column.** ServUO picks the new-system values under
    `TreasureMapInfo.NewSystem` (= `Core.EJ`, true here), but pinned's maps are the old system (levels 0-7), and the
    new column would pay a level 6 map 50 points (its `default`). The old column describes the maps this shard drops.
  - **`IVvVItem`, `Bait`**: neither exists in pinned; nothing is a VvV item, no bait case.
  - **Craft systems**: ServUO walks `CraftSystem.Systems` in first-use order; pinned has no such list, so ours walks
    the eleven pinned systems in a fixed order. No type was found in two systems that would make the order matter.
  - **`ICombatEquipment`** = `BaseWeapon`, `BaseArmor`, `BaseClothing`, `BaseJewel`, the four ServUO classes that
    implement it.
- Ours (registered): **values for the 16 extended ingots and boards**, continuing OSI's top tier by the post-valorite
  multipliers our smith commissions already use (`ClusterFSmithCommissions.PostValMultiplier`, 1.5 to 5.0):
  ingots 15 / 20 / 25 / 30 / 35 / 40 / 45 / 50 (Platinum to Celestial, from valorite's 10), boards 4.5 / 6 / 7.5 / 9 /
  10.5 / 12 / 13.5 / 15 (Ironwood to Starwood, from frostwood's 3). **Crafted-gear rate for each equals its ingot or
  board value exactly**, so ours can never out-earn its materials. Ores and logs pay nothing, as OSI's do.
- Left out: the Cleanup Point Exchange (`:815-901`).

## 3. Stage 2: barrels and Appraise for Cleanup

- `Services\CleanUpBritannia\CleanUpTrash.cs`: ServUO `BaseTrash`'s bookkeeping (`AddCleanupItem` `:80-117`,
  `ConfirmCleanupItem` `:119-133`, the payout block of each `Empty`, the "Appraise for Cleanup" entry `:30-52`). ServUO
  keeps the list on the container and never saves it; pinned's containers have no such field, so it is held beside
  them in a `ConditionalWeakTable`, also unsaved.
- `Services\CleanUpBritannia\CleanupTrashBarrel.cs`: ServUO's "Trash - Keep Britannia Clean", ported. Takes only items
  with value, empties and pays at once.
- **The patch, argued.** OSI pays for any trash barrel, a house's included (ServUO `TrashBarrel : BaseTrash`). Pinned's
  `TrashBarrel` and `TrashChest` (`Items/Misc/`) have no hook, and house barrels are made by pinned's own `BaseHouse`
  (`:2043`). Alternatives rejected:
  1. *Our barrel only, plain barrels unpaid.* A registered deviation a wiki reader would trip over: OSI's guides tell
     players to use their house barrel.
  2. *Swap plain barrels for ours.* Needs a `BaseHouse` patch instead, which is bigger, and leaves existing barrels.
  3. *A replacement file for each.* Copies pinned logic; a patch that fails beats copied logic that drifts
     (`docs/subsystem-policy.md`).

  So two patches, each only calls into ours: on drop, record; on empty, confirm and pay; one context-menu override.
  The chest also refuses a **blessed item with no value** rather than destroying it, as ServUO's `TrashChest` does
  (`:56-90`); pinned's chest destroys it. Routed in `docker\uo\apply-patches.sh` beside P32's two, which is outside the
  brief's listed directories but is the only way a patch reaches the build (P32's precedent).
- Not ported: ServUO's 1% chance that an emptied barrel drops its item in the Cavern of the Discarded (SA). It is not
  part of Clean Up.

## 4. Stages 3 and 4: the store, the NPCs, the Custodian layer

### 4.1 The store (`Services\CleanUpBritannia\CleanUpBritanniaRewards.cs`)

- OSI's section: the 49 at ServUO's prices, generated from ServUO's file with line numbers, the 85 missing kept as
  comments. Buying is ServUO `BaseRewardGump.OnConfirmed` (`Gumps/BaseRewardGump.cs:172-193`) and its confirm gump
  (`:218-246`, on pinned's `BaseConfirmGump`); a Scroll of Alacrity gets a random skill (`Gumps.cs:36-42`).
- Ours, after OSI's, labeled "Custodian supplies": **100 bandages 15, 5 refresh potions 3, 3 greater heal potions 5.**
- **Sorted by price, each section** (stable, so equal prices keep OSI's order). OSI's list was already in rising order,
  so OSI's section reads exactly as ServUO lists it.
- Gump: ServUO's layout and art ids; ServUO sizes each row from the item art (`CollectionItem`), which pinned lacks, so
  rows are a fixed height. A small layout difference, not a content one.

### 4.2 The NPCs

- `TheCleanupOfficer` (ServUO `Creatures/TheCleanupOfficer.cs`, ported): double-click within 5 tiles opens the store.
- The Sanitation Warden's gump: a "Clean Up Britannia store" button (members and non-members; OSI's store is open to
  all) and, for members, "Trash bag (free)". The store needs a Warden or an Officer within 5 tiles, as ServUO's confirm
  does; opened from the guild directory far away, it says where to go.

### 4.3 The trash bag

Free; one per character, **by owner**: the bag records its owner (`TrashBag` v1), `TrashBag.IssueTo` deletes every bag
the character owns wherever it is (bank, house, ground) and gives one. Only the owner can dump it. A version 0 bag has
no owner and dumps for no one (there should be none on a fresh world). Joining gives one only if the character owns
none.

### 4.4 The Custodian layer (`ClusterFCustodianSystem.cs`)

- `[cleanup`, `[cleanupall`, the trash bag: Clean Up points by Clean Up's table. An item worth nothing is still litter
  and is still cleaned ("no turn-in value").
- **Corpse rule (ours):** `CorpseBasePoints` 0.10 (an iron ingot's worth) plus every item inside at its Clean Up value.
  So a corpse never pays more than its loot would in a barrel, plus the base.
- **Ranks key on lifetime Clean Up points**, from any source (a house barrel counts). Spending never lowers them. The
  character's "custodians" guild standing is kept equal to floor(lifetime) on every award, on joining and at load
  (`SyncStanding`), so the directory, the rank names and the Civic Contract gates all follow it with no other change.
  Thresholds **25 / 125 / 500 / 1,250**: the old ladder divided by 4, because tokens paid at least 1 per item and 2 or
  more per corpse, while Clean Up pays an iron weapon about 1 point, most litter nothing, and a corpse its contents.
  **A judgment, not a measurement; Chase's to adjust** (one array).
- Civic Contracts: gates rescaled the same way (0 / 25 / 125 / 500 / 1,250), standing and vouchers 0, gold kept.
  Civic waste bundles now count only items with Clean Up value (1 per 5), so sweeping worthless litter no longer fills
  a contract.
- Resets: the reset stone's "Guilds" option and `[guild reset custodians` also clear the Clean Up points, since they
  are the rank now. The reset gump's confirm line says so.
- **Craft X (F-1's hook, P18 `:332`, `:356`):** a reject goes into the crafter's **own** trash bag if it is in their
  pack, after smelting, the salvage bag and scissors, before the chosen rejects bag (where P18 left the hook). The run's
  summary says "N to the trash bag". Safe because a crafted piece pays no more than its materials (section 5), apart
  from OSI's wood and cloth.
- **Fixed (ours, an old defect): a player's corpse is not litter.** `IsEligible` returned true for every corpse, so
  `[cleanup` and `[cleanupall` would delete a dead player's corpse and everything on it.

## 5. The anti-farm facts

Measured by `CleanUpCraftHost.Measure` over **every** craftable piece of combat equipment in all eleven craft systems,
made of every resource its system offers (our extended ones included, registered as the server does at
`ServerStarted`), against the most valuable form of the material (a log or its board, an ingot). 3 craft entries could
not be built in the host and were skipped.

- **Metals, leathers, scales and all 16 of ours: 0 of 4,419 pairs out-earn their materials.** OSI's metal rates are
  at or below the ingot values (.47 vs .50, .73 vs .75, 1.47 vs 1.50, the rest equal), and truncation only lowers them.
- **With the guild salvage bag in the loop**, every metal from iron to Celestial at Mining 300: a 25-ingot plate chest
  salvages back less than it took (the D42 clamp, `cost - 1`), so craft, salvage, craft again and trash never beats
  trashing the ingots. The red run without the clamp gives back 51 ingots, 5.1 points for 2.5.
- **OSI's wood and cloth rates do not hold the rule.** OSI pays crafted wood gear .17 / .33 / .67 / 2.17 / 3.17 a
  board (oak to frostwood) against boards of .10 / .25 / .50 / 2.0 / 3.0, plain wood .1 against .05, and cloth gear .1
  a cloth against cloth worth 0. Heartwood is equal and never out-earns. **255 pairs out-earn** (oak 29, ash 37, yew 40,
  bloodwood 40, frostwood 40, plain wood 32, cloth 37), by **at most about one point a piece** after truncation (e.g. a
  bloodwood quarterstaff pays 13 for 12 points of boards; a jester suit pays 2 for cloth worth 0). The full list is
  `notes\cc-P33-tools\osi-excess.txt`. The fact `OsisWoodAndClothRatesLetACraftedPieceOutEarnItsMaterials` pins it.

## 6. The 85 missing rewards (left out of the store)

By price, ServUO line in brackets:

- **1,000** (6): Mailbox (:17), HumansAndElvesRobe (:18), GargoylesAreOurFriendsRobe (:19), WeArePiratesRobe (:20), FollowerOfBaneRobe (:21), QueenDawnForeverRobe (:22)
- **5,000** (7): LillyPad (:24), LillyPads (:25), Mushrooms1 (:26), Mushrooms2 (:27), Mushrooms3 (:28), Mushrooms4 (:29), NocturneEarrings (:30)
- **10,000** (12): SherryTheMouseStatue (:32), RefinementAmalgamator (:33), ChaosTileDeed (:34), HonestyVirtueTileDeed (:35), CompassionVirtueTileDeed (:36), ValorVirtueTileDeed (:37), SpiritualityVirtueTileDeed (:38), HonorVirtueTileDeed (:39), HumilityVirtueTileDeed (:40), SacrificeVirtueTileDeed (:41), JusticeVirtueTileDeed (:42), StewardDeed (:43)
- **15,000** (3): YuccaTree (:75), TableLamp (:76), Bamboo (:77)
- **20,000** (9): HorseBardingDeed (:79), SnakeSkinBoots (:82), BootsOfTheLavaLizard (:83), BootsOfTheIceWyrm (:84), BootsOfTheCrystalHydra (:85), BootsOfTheThrasher (:86), NaturesTears (:88), PrimordialDecay (:89), ArachnidDoom (:90)
- **50,000** (14): SophisticatedElvenTapestry (:92), OrnateElvenTapestry (:93), ChestOfDrawers (:94), FootedChestOfDrawers (:95), DragonHeadAddonDeed (:97), NestWithEggs (:98), FishermansHat (:102), FishermansTrousers (:103), FishermansVest (:104), FishermansEelskinGloves (:105), FishermansChestguard (:106), FishermansKilt (:107), FishermansArms (:108), FishermansEarrings (:109)
- **75,000** (2): FirePitDeed (:130), PresentationStone (:131)
- **80,000** (1): Beehive (:132)
- **250,000** (24): IntenseTealPigment (:142), TyrianPurplePigment (:143), MottledSunsetBluePigment (:144), MossyGreenPigment (:145), VibrantOcherPigment (:146), OliveGreenPigment (:147), PolishedBronzePigment (:148), GlossyBluePigment (:149), BlackAndGreenPigment (:150), DeepVioletPigment (:151), AuraOfAmberPigment (:152), MurkySeagreenPigment (:153), ShadowyBluePigment (:154), GleamingFuchsiaPigment (:155), GlossyFuchsiaPigment (:156), DeepBluePigment (:157), VibranSeagreenPigment (:158), MurkyAmberPigment (:159), VibrantCrimsonPigment (:160), ReflectiveShadowPigment (:161), StarBluePigment (:162), MotherOfPearlPigment (:163), LiquidSunshinePigment (:164), DarkVoidPigment (:165)
- **300,000** (6): LuckyCharm (:167), SoldiersMedal (:168), DuelistsEdge (:169), NecromancersPhylactery (:170), WizardsCurio (:171), MysticsMemento (:172)
- **500,000** (1): VollemHeldInCrystal (:174)

Most are single-file items in ServUO `Services/CleanUpBritannia/Items/` (48 `.cs` files there with `Pigments/`, counted) plus the pigments,
the HS fishing set and the virtue tiles. Their own dependencies are **not measured** here; that is the D32/D33 question.

## 7. Facts, and red / green

26 new facts in `server\tests\Services\` (421 tests before, 447 after):

| File | Facts |
|---|---|
| `CleanUpBritanniaPointsVerification.cs` | 9: table sample = ServUO (iron 0.10, valorite 10.0, boards, leathers, gems, gold 0.01, rope 1,600, stealables, lockpick, the dye tub rename; 469 rows, all items); special cases (runic hammer and kit by uses, power scrolls 105-120, SoT, treasure map levels 0-7, slime statuette, pigments, ancient SOS); crafted gear truncated; anti-farm ours; anti-farm OSI wood and cloth (pinned); salvage bag in the loop; per character not per account; spending lowers points never lifetime; save round-trip and loud failures |
| `CleanUpBritanniaBarrelVerification.cs` | 5: Appraise = barrel payout (all four clilocs); Clean Up barrel refuses junk, pays at once; pinned barrel pays each dropper on empty; pinned chest pays at once, refuses blessed junk; every container offers Appraise |
| `CleanUpBritanniaStoreVerification.cs` | 5: OSI's 49 at ServUO's prices by tier, sorted; ours last at 15 / 3 / 5 and deliver; buying spends the price only; both NPCs open it, neither from afar; the placement command's dry run and re-run |
| `CustodianLayerVerification.cs` | 7: bag free and one per character wherever the old one is; owner round-trip and version 0; dump pays Clean Up values, owner only; rank follows lifetime from any source and does not drop on spending (and a non-member's points count on joining); corpse rule and player corpses; Civic Tokens gone from award, source, display and save; Craft X into the crafter's own bag only |

**Red first, every one, by mutation of the production code** (scratchpad `redrun.py`, copied to
`notes\cc-P33-tools\`; every mutated file restored and checked byte-identical to its saved copy afterwards):

- Run 1, 11 mutations (a table value, a runic rate, ceiling in place of truncation, our rate above our ingot, OSI's
  wood rates flattened, the D42 clamp removed, points keyed by account, lifetime following points, lifetime not
  written): **all 9 stage 1 facts red**, and the 3 existing `SalvageBagIngotReturnVerification` facts with them. The
  salvage fact went red on another mutation's account, so:
- Run 1b, the clamp alone: the salvage fact red for its own reason ("salvage 5.1 >= materials 2.5").
- Run 2, 14 mutations across stages 2-4: **15 of 15 targeted facts red**; the rank fact for another mutation's reason, so:
- Run 3: the rank sync removed alone, and the bag's owner written at version 0 with no bump: both red for their own
  reasons.
- Run 4: the dry run places: the placement fact red.
- Run 5: the standing sync writes for non-members: the rank fact red on its non-member assertion.
- Then green: **447 of 447**, final `build.sh` all three stages, `sl-modernuo:cc-p33`. No `cc-p33-red` image exists
  (red runs stop at the test gate). `sl-modernuo:latest` is unchanged (`246b0d5813e5`).

One flake caught and fixed in my own test: pinned's `new SOS()` rolls a random level, and level 4 is ancient
(2,500), so the 100-point case now sets `Level = 1`.

## 8. Deviation text for the register (numbers are the overseer's)

| ID | Text | Effect | Visibility | Source |
|---|---|---|---|---|
| D-next | **Ours (F-3).** The Custodians are a layer on Clean Up Britannia: `[cleanup`, `[cleanupall` and the Custodian trash bag earn Clean Up points, valued by Clean Up's own table; Civic Tokens are retired | Custodian work earns the points OSI's barrels pay and the store spends | `visible` | `cc-P33` 4.4 |
| D-next | **Ours (F-3).** A corpse cleared by a Custodian pays 0.10 points plus each item inside at its Clean Up value; Clean Up has no corpse rule. A player's corpse is never litter | corpses pay what their loot would, plus a little | `visible` | `cc-P33` 4.4 |
| D-next | **Ours (F-3).** No Cleanup Point Exchange stone: points are per character and the shard will allow one character per account (F-4) | points cannot be pooled across characters | `visible` | `cc-P33` 2 |
| D-next | **Ours (F-3).** The Clean Up store lists each section by price, and adds a "Custodian supplies" section (100 bandages 15, 5 refresh potions 3, 3 greater heal potions 5), opened by the Cleanup Officer and the Sanitation Warden alike. OSI's items and prices are unchanged; 85 of OSI's 134 rewards are not in the store because the items do not exist here | a shorter OSI list, plus three consumables | `visible` | `cc-P33` 4.1, 6 |
| D-next | **Ours (F-3).** The Custodian trash bag is free and one per character: asking for a new one deletes the old one wherever it is; only its owner can dump it | a lost bag is replaced for free | `visible` | `cc-P33` 4.3 |
| D-next | **Ours (F-3).** Custodian ranks follow lifetime Clean Up points from any source, which spending never lowers: Junior 25, Custodian 125, Senior 500, Chief 1,250. Civic Contracts gate on the same numbers and pay gold only | rank is a lifetime total, not a balance | `visible` | `cc-P33` 4.4 |
| D-next | **Ours (F-3).** Values for our 16 extended ingots and boards (ingots 15 to 50, boards 4.5 to 15); crafted gear of them pays exactly its material | our materials are worth points; crafting them never adds any | `visible` | `cc-P33` 2 |
| D-next | **Gap (F-3).** Clean Up pays crafted gear nothing for its magic properties: ServUO's imbuing-weight term (`CleanUpBritanniaData.cs:800-805`) needs a property-weight table pinned does not have. Reverses when ServUO's `ItemPropertyInfo` weights are ported | magic gear pays its materials only | `visible` | `cc-P33` 2 |
| D-next | **Ours (F-3).** Treasure maps pay ServUO's old-system values though the shard runs Endless Journey, because pinned's maps are the old system | a level 6 map pays 1,000, not 50 | `minor` | `cc-P33` 2 |

## 9. Go-live

- **Civic Tokens:** cleared by the server itself at world load (`RetireCivicTokens`), once, logged as
  "Civic Tokens retired (cc-P33): cleared N token balance(s), re-synced M Custodian standing(s)". On the fresh world
  there will be nothing to clear and the line will not print. On any older world it clears balances and puts every
  Custodian's rank back to Volunteer (lifetime 0), which is the intent of "nothing converts".
- Old trash bags (version 0) have no owner and cannot be dumped; their owners ask a Warden for a new one.
- Nothing is placed by the server: the Officer and Clean Up barrels need `[ClusterFPlaceCleanUp` (below).

## 10. Defects and loose ends found (not fixed here)

1. **Ours: `CraftResources.GetType` (`customizations\ResourceInfo.cs:1089-1097`) stops the wood range at `Frostwood`**,
   so the eight extended woods (308-315) are `CraftResourceType.None` and `CraftResources.GetInfo` returns null for
   them. Anything that asks a wood's type or info gets nothing for Ironwood to Starwood. Found by the anti-farm
   measurement, which works around it. One line to fix (`<= CraftResource.Starwood`), but every caller of `GetType`
   and `GetInfo` should be checked first, so it is a task of its own.
2. **A farm that predates this task, narrowed but not closed:** Civic waste bundles (1 per 5 items) fill Civic
   Contracts for gold. Bundles now count only items with Clean Up value, but cheap vendor items with value (bottles
   0.25, lockpicks 0.10) still turn into bundles. Worth a look with F-18/F-25's economy pass.
3. **AGENTS.md vs the brief:** AGENTS.md rule 7 still says nothing may require a fresh world; the F-3 entry and this
   brief say one is coming. Nothing here depends on it (the token clear runs on any world), but one of the two
   documents is stale.

## 11. Decisions for Chase

1. **OSI's wood and cloth rates** let a crafted wooden or cloth piece out-earn its materials, by about a point
   (section 5). (a) Keep OSI's numbers, as the fidelity rule says, and accept it; or (b) a registered deviation capping
   crafted wood and cloth gear at its material's value. I built (a).
2. **The imbuing-weight gap** (Headline 3): accept that magic gear pays its materials only, or schedule a port of
   ServUO's property weights (a subsystem by size, roughly the `ItemPropertyInfo` tables).
3. **The 85 missing rewards** (section 6): leave them out, or schedule their ports. The top of the store (250,000 and
   up) is all missing.
4. **The rank ladder** (25 / 125 / 500 / 1,250) and **CorpseBasePoints** (0.10) are judgments; adjust if wanted.

## 12. Checklist for Chase (test shard)

Build is `sl-modernuo:cc-p33`. Deploy it to the test shard yourself first; nothing here deployed it.

1. Stand beside the New Haven banker (or wherever you want the Officer). Run `[ClusterFPlaceCleanUp dryrun` and read
   the line: it should say it would place the Officer at your tile and the barrel one east. Then run
   `[ClusterFPlaceCleanUp`. Run it once more: both "already at".
2. Trash a few items in the Clean Up barrel and in a house trash barrel: valorite ingots, a crafted plate chest, a
   power scroll, gold. First right-click the barrel, choose **Appraise for Cleanup**, target each in your pack, and
   note the numbers. Then drop them in: the Clean Up barrel pays at once; the house barrel pays when it empties (3
   minutes, or 50 items). The "received approximately N points" message should match the sum of the appraisals.
3. Double-click the Officer: the store opens, OSI's items first by price, then "Custodian supplies" at 15, 3 and 5.
   Buy one supply. Then talk to the Sanitation Warden, open the store from the gump, and buy again.
4. As a Custodian, press **Trash bag (free)** twice. The first bag disappears (try leaving it in the bank first); your
   points do not change.
5. Craft and trash: make an iron or colored-ingot weapon, appraise it and appraise its ingots; the weapon is never
   worth more. (A wooden or cloth piece can be, by a point: Decision 1.) Optional: Craft X in "exceptional only" with
   your trash bag in your pack; rejects land in the bag.

## Files

`D:\ShatteredLegacy`:

- New: `server\customizations\Services\PointsSystems\{PointsSystem,CleanUpBritanniaData}.cs`;
  `server\customizations\Services\CleanUpBritannia\{CleanUpTrash,CleanupTrashBarrel,CleanUpBritanniaRewards,TheCleanupOfficer,ClusterFCleanUpPlacement}.cs`;
  `server\patches\{TrashBarrel,TrashChest}-clean-up-britannia.patch`; `server\migrations\Server.Items.TrashBag.v0.json`;
  `server\tests\Services\{CleanUpBritanniaPoints,CleanUpBritanniaBarrel,CleanUpBritanniaStore,CustodianLayer}Verification.cs`.
- Changed: `server\customizations\{ClusterFCustodianSystem,TrashBag,SanitationWarden,SanitationWardenGump,ClusterFCraftRejects,ClusterFCraftRun,ClusterFGuildSystem,ClusterFWorkOrderSystem,ClusterFDevTools}.cs`;
  `docker\uo\apply-patches.sh` (routes the two patches).

`D:\UO\shard-migration`: this note; `notes\cc-P33-tools\` (the resolver and generators, the mutation script, the
missing table rows, the OSI excess list).
