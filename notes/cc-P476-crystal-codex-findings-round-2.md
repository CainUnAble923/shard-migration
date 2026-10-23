# cc-P476: Crystal turns the Codex reviews P423 to P474 into fix-up prompt drafts (round 2)

**Golem:** Crystal (cloud). **Date:** 2026-10-23. **Branch:** `golem/Crystal/P476` (shard-migration only; no code changed).
**Checked against:** code `main` at `0f1871f` (P475's merge), pinned ModernUO `d4531cd9`, ServUO pub57 where a port
follows it.

## In plain words

- I checked the 38 Codex code reviews in main from P423 to P474: P423-P426, P430-P435, P437-P450, P461-P474. P427,
  P428, P429, P436 and P451-P460 are prompts, not reviews. Each review's own `-codex-review.md` (Codex reading the
  notes) found nothing about the code.
- **185 findings:**
  - 80 confirmed and 13 partly real.
  - 19 are real but may be meant (Chase's call).
  - 45 are missing tests with no bug behind them.
  - 6 are blocked: the rolled work orders P470 reviews are not built.
  - 13 need the game PC: Golem tooling, third-party tools, client measurements.
  - 4 were already queued (P453, P413).
  - 4 were not bugs, or were only the wording of notes.
- **There is no live shard.** It was retired and deleted on 10-14, until the fresh 1.0 world (`README.md:112`).
  Everything below is on the test shard today, and on 1.0 if not fixed. Some helper notes I used said "live now";
  that is wrong, and I took it out.
- **Six urgent drafts.** Each is an exploit that pays, or a loss for players:
  1. **Reward shops pay twice.** A player can open several "confirm" windows on one balance and accept them all. This
     is in Blackthorn, Void Pool and Sorcerer's Dungeon. Sorcerer's Dungeon turns itself on tomorrow, 10-24.
  2. **Clean Up Britannia:**
     - A trash barrel pays a whole stack's points for one item: drop 1,000 ingots, split one off, take the rest back.
     - Asking the Warden for a new trash bag deletes the old one and everything in it, wherever it is.
     - `[cleanupall` deletes other players' kills and house floor items through walls, and pays the sweeper for them.
  3. **High Seas fishing:** every cast in Gravewater Lake catches a legendary fish. Lobster traps catch what is rare
     where their owner stands, not where the trap is.
  4. **The tutorial's Rootdeep Vault:** a trainee can farm the Overdraft boss for gold and Dawnstone. A trainee who
     dies after the kill cannot get back in to their corpse.
  5. **Bulk orders:** closing the reward list and claiming again pays 2% instead of 20%. Some large dining deeds can
     never be finished.
  6. **Recipe gating:** each Fletching rank hands out another sellable pattern book. Survey Saddle Roll schematics
     count as known without being learned.
- **Eighteen drafts can wait.** They are listed under "Drafts that can wait", most valuable first. Two more items:
  P470's six findings go to whoever builds F-38's rolled orders, and P472 and P469 need the game PC.
- **New, found while checking (not in any review):**
  - The Void Pool shop has the same double-pay.
  - All eight post-Valorite metals and Dawnstone can be resmelted at 0 Mining.
  - The caltrops trap's "slow" does not slow walking.
  - A League Hall deed decays on the ground when its house is deleted.
  - Experimental Room cooldowns reset at every restart.
  - The CompassionPigment has the League pigment's trade gap.
- Nothing was built or run: a cloud Golem cannot build the shard. Every draft asks for a red test first.

## How the checking was done

Seven read-only helper sessions each re-checked one group of reviews against `0f1871f` and pinned ModernUO. Each
reported a verdict, severity and file:line. Their working tables are summarized below. I re-read these claims myself
before writing the urgent drafts:
- The reward confirm: `Gumps/BaseRewardGump.cs:167-171` checks the balance only when it sends the confirm. `:186-205`
  delivers, then calls `RemovePoints`. `BlackthornDungeon/Gumps.cs:21` drops the deduction's result.
- The barrel: `CleanUpTrash.cs:74-79` fixes the points by serial at drop, and `:109-112` confirms by serial. Pinned
  `Mobile.LiftItemDupe` (`Mobile.cs:5235-5262`) leaves the lifted amount on the original serial.
- Gravewater: `FishInfo.cs:325-328`, the only location branch without `info.Roll`. The trap: `FishInfo.cs:241-249`
  reads `from.Map/Location/Region`.
- The Vault: `RootdeepVault.cs:152` (the cleared flag is checked only on entry) and `:175-187` (it is set at the kill).

Verdicts: **confirmed** (real in today's code), **partly** (part of it real), **policy** (real, maybe intended:
Chase decides), **test gap**, **blocked**, **needs PC**, **queued**, **not a bug**. Severity: **urgent** means an
exploit that pays, a loss for players, or a crash or save problem.

## Every finding and its verdict

C is `server/customizations/`. "Draft" names the draft below. "Chase" means the "For Chase" list. "-" means a test
gap or note with no draft of its own.

| Finding | What | Verdict | Severity | Today's code (main 0f1871f) | Draft |
|---|---|---|---|---|---|
| P423 #1 | Large dining tinker deeds can ask for exceptional/metal that utensil smalls can never carry | confirmed | normal | BO/CraftBOD.cs:365-374 (RollLarge reads only `entries[0]`); BO/CraftBulkEntries.cs:662-670 (ButcherKnife first, then Spoon, Fork, Plate, Knife, Goblet); ... | U5 |
| P423 #2 | Turn-in does not put an offer back into the 2016 cache | confirmed | normal | BO/BulkOrderVendors.cs:301-368 TurnIn (nothing touches the BODEntry); BO/BulkOrderSystem.cs:108-131 CanGetBulkOrder, :723-740 CheckCache (only time refills it); ... | U5 |
| P423 #3 | Reopening a pending large-deed reward banks 2% not 20% | confirmed | **urgent** | BO/BulkOrderVendors.cs:167 (`pending * 0.02` always); BO/BulkOrderSystem.cs:278-282 (turn-in: 0.2 for LargeBOD); BO/BODRewardsGump.cs:243-303 (gump not closable, but ... | U5 |
| P423 #4 | Foresters/Alembic guild masters accept deeds and act on open gumps while `ContentFeatureFlags.BulkOrders` is off | confirmed | normal | BO/BulkOrderGivers.cs:135-150 TryTurnIn (checks only `NewSystemEnabled` = `Core.TOL`, BulkOrderSystem.cs:56); :114-129 Act (no flag); :177-183 ... | U5 |
| P423 #5 | Master Chef's Apron adds its exceptional bonus to every craft | policy | normal | BO/Items/MasterChefsApron.cs:38-39; server/patches/CraftItem-chefs-apron.patch:6 (in shared GetExceptionalChance); test asserts it for Blacksmith: ... | Chase |
| P423 #6 | Carpentry furniture +300 / composite longbow +250 point bonuses vs OSI 210/360 | policy | minor | BO/CraftRewardCalculators.cs:215, :305-308 | Chase |
| P423 #7 | Reward prices differ from OSI (SI mallet 450, Mechanic title 225, barrel 625, smith maps 600/850/950/1050) | policy | minor | BO/BODRewardCollections.cs:208 (live: RunicMalletAndChisel 450), :177, :263, :115, :124, :128, :131 (placeholders) | Chase |
| P423 #8 | Jewelry large deeds grow `_makeable` without bound | confirmed | minor | BO/LargeTinkerBOD.cs:44-50 (new array per deed via GemEntries :63-73); BO/CraftBOD.cs:330, :340-352 (dictionary keyed by array reference) | U5 |
| P423 #9 | Reward-list test compares the price list with itself | test gap | minor | server/tests/Services/BulkOrders/BulkOrderCraftsVerification.cs:745 | U5 |
| P423 #10 | Book tests skip withdraw/buy transactions | test gap | minor | same file :497-505 (calls `Reconstruct` directly) | U5 |
| P424 #1 | Client full sync accepts a short/empty gzip and wipes the facet | partly | minor | client/patches/0004-world-map-fog-of-war.patch:130-145 (no length check before `_explored[facet] = bits`) | W16 |
| P424 #2 | Exploration records of deleted characters are never removed | confirmed | normal | ClusterFAccountData.cs:92-100 (`_exploredChunks` keyed by serial, only ClearExploration :105); written per char at ClusterFAccountData.cs ~:535-545; created for all 6 ... | W16 |
| P424 #3 | Each exploration delta rebuilds and uploads the whole facet texture | needs PC | minor | patch:210-229 (rebuild when global `Version` changes), Version++ per delta :167 | - |
| P424 #4 | Login-reset test calls Reset directly, not EnterWorld | test gap | minor | patch:509-515; hook at patch:339 | W16 |
| P425 #1 | A seeded world started without the map overlay sends players onto void land | partly | minor | ClusterFRootdeepSeeder.cs:179 (MapBuilt gates seeding only); docker/uo/Start-TestShard.ps1:162-167 (`-NoMapOverlay`); pinned Items/Misc/Teleporter.cs:236-245 | - |
| P425 #2 | Seeder rerun after a destination change adds a second teleporter | queued | normal | ClusterFRootdeepSeeder.cs:70-79, :234-246, :315-326 (FindTeleporter matches on `PointDest`) | P413 (add) |
| P425 #3 | FindTeleporter accepts an inactive or wrong-Z teleporter as present | partly | minor | ClusterFRootdeepSeeder.cs:318-326 (no `Active`/Z check) | P413 (add) |
| P425 #4 | Route helper height math differs from the server's | queued | minor | shard-migration/notes/cc-P188-tools/build_way_in.py:94-96 (`(min+max)//2`), :105-109; pinned Server/Maps/Map.cs:282 | P413 |
| P425 #5 | W1 test forces MapBuilt and calls OnMoveOver; no walk, pet or ghost coverage | test gap | minor | server/tests/Regions/RootdeepWayInVerification.cs:107-180 | - |
| P426 #1 | Gravewater Lake gives rare and legendary fish with no chance roll | confirmed | **urgent** | HS/Items/Fish/FishInfo.cs:325-328 (no `info.Roll`), rows :58 (Holy Mackerel 102.9) and :86 (Zombie Fish 115.1), box :437-439 (Malas); every other location branch ... | U3 |
| P426 #2 | A lobster trap picks its catch from its owner's map, location and region | confirmed | **urgent** | HS/Items/Fish/FishInfo.cs:241-249 (`from.Map/Location/Region`), :330 (`from.Region` again), :286 (deep water = trap point on owner's map); HS/Items/LobsterTrap.cs:341 ... | U3 |
| P426 #3 | Save during Charybdis's 3 s teleport leaves it on Map.Internal after restart | confirmed | normal | HS/Mobiles/Charybdis.cs:44-47 (unsaved `_lastLocation/_lastMap`), :156-165 (Internalize then DelayCall 3 s), :180-185 (null map returns), :596-601 ... | U3 |
| P426 #4 | Felucca sea-champion death drops a `ChampionSkull(None)` | confirmed | minor | HS/Mobiles/BaseSeaChampion.cs:44; pinned UOContent/Mobiles/Special/BaseChampion.cs:236-261 (no None check); ServUO BaseChampion.cs:267 checks it | U3 |
| P426 #5 | Artifact lottery: last ticket never wins (`>` against inclusive roll) | confirmed | minor | HS/Mobiles/BaseSeaChampion.cs:149, :157 | U3 |
| P426 #6 | Fishing patch test skips the SOS and bottle paths | test gap | minor | server/tests/Services/HighSeasFishingVerification.cs:348 | U3 |
| P426 #7 | Trap tests set state directly; no retrieval, access or timer-resume coverage | test gap | minor | same file :404-416, :454 | U3 |
| P426 #8 | Undocumented spawn-bounds change from ServUO | policy | minor | HS/Mobiles/BaseSeaChampion.cs:285-300 | Chase |
| P430 #1 | Credited trainee can stay in the Vault and farm the respawning Overdraft | confirmed | **urgent** | Regions/RootdeepVault.cs:152 (cleared flag checked only on entry, via OnMoveInto :63-74); Tutorial/TutorialCreature.cs:32-48 (engages any participant); ... | U4 |
| P430 #2 | Credit seals the Vault before the player leaves: relog ejects them; a dead trainee cannot return to their corpse | confirmed | **urgent** | Regions/RootdeepVault.cs:182 (flag set at the kill), :232-246 (TurnOut on login), :140-157 (MayEnter refuses a cleared player or ghost), :206 (TryCrawl refuses ghosts) | U4 |
| P430 #3 | Credit through a pet is lost if the unbonded pet died first | partly | minor | Regions/RootdeepVault.cs:162-163, :177 (uses `entry.Damager` and the pet's current ControlMaster); pinned BaseCreature.cs:3686-3687 (`SetControlMaster(null)` on ... | U4 |
| P430 #4 | Crawlway found by radius 24 around the corpse; a kill in the Deposit Hall misses it | partly | minor | Regions/RootdeepVault.cs:191; mouth :103 (5160,1159) vs Deposit Hall (5143,1133), dy 26 | U4 |
| P430 #5 | Hoarding Rat's called Penny Rats are unowned and pile up across leader respawns | confirmed | normal | Mobiles/Burrows/VaultCreatures.cs:126-143 (no Spawner, no list, no cleanup on death :145-150); spawner 2-3 min: ClusterFRootdeepSeeder.cs:104 | U4 |
| P430 #6 | Burrow Mother's brood list and count not saved | confirmed | minor | Mobiles/Burrows/WarrenCreatures.cs:162-163 (plain fields), :229-233, OnDeath cleanup | U4 |
| P430 #7 | Interior and Dawnstone tests force map readiness and call MutateResource | test gap | minor | server/tests/Regions/RootdeepVaultVerification.cs:331; server/tests/Items/StarterResourcesVerification.cs:207 | U4 |
| P431 #1 | Merchants' Apprentice task checks for 500 gold but never takes it | confirmed | normal | `customizations/ClusterFGuildSystem.cs:220-221` (ItemOnly, ItemID 0.0), `:346-353` (has-gold check), `:400-410` (consumes only when `Skills[ItemID].Base < 0.0`, never ... | W9 |
| P431 #2 | Smith/Custodian Join button has no guildmaster-range check | confirmed | minor | `customizations/SmithGuildmasterGump.cs:311-325`, `customizations/SanitationWardenGump.cs:269-285` (CanJoin only); compare `ClusterFGuildSystem.cs:1200-1205` ... | W9 |
| P431 #3 | No test for `ReplaceStarterItem` / `OwnsCopy` | test gap | - | `customizations/ClusterFGuildStarterPath.cs:442-509`; `grep ReplaceStarterItem server/tests` finds nothing | W9 |
| P432 #1 | Trash barrel keeps the first stack's value by serial: split, retrieve, return 1 = full pay | confirmed | **urgent** | `customizations/Services/CleanUpBritannia/CleanUpTrash.cs:74-79` (keyed on serial, points fixed at drop), `:109-112,127` (confirm by serial, pay stored points); ... | U2 |
| P432 #2 | Second matching stack merges, is deleted, then scores 0 | confirmed | normal | `patches/TrashBarrel-clean-up-britannia.patch:29` (records after `base.OnDragDrop`); `PIN/Projects/Server/Items/Container.cs:411-437` (`TryDropItem` stacks first); ... | U2 |
| P432 #3 | Crafted Sandals pay a flat 2 pts against 0.4 pts of leather | policy | normal | `customizations/Services/PointsSystems/CleanUpBritanniaData.cs:461` (Sandals 2.0), `:454` (Leather 0.10), `:121-135` (table first); ... | Chase |
| P432 #4 | Asking the Warden for a new trash bag deletes the old bag and its contents, wherever it is | confirmed | **urgent** | `customizations/TrashBag.cs:76-91` (`old.Delete()` on every owned bag); `customizations/SanitationWardenGump.cs:117` (button reads "Trash bag (free)", no warning), ... | U2 |
| P432 #5 | `[cleanupall` deletes every eligible ground item in radius 10: no LOS, Z, house or loot-rights checks | confirmed | **urgent** | `customizations/ClusterFCustodianSystem.cs:367-388`; `:130` (any monster corpse eligible); `PIN/.../Corpses/Corpse.cs:465-468` (`IsChildVisibleTo`), `:863` ... | U2 |
| P432 #6 | Corpse accepted whole; blessed/quest descendants valued and deleted | partly | minor | `ClusterFCustodianSystem.cs:130,163-173`; `PIN/.../Corpse.cs` has no `CheckHold`/`OnDragDrop` override, so items can be put into monster corpses | U2 |
| P432 #7 | Store confirm checks only X/Y distance to the trader | confirmed | minor | `customizations/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:436-441`; `PIN/Projects/Server/Mobiles/Mobile.cs:3076` (`InRange(Point3D,int)` is 2D) | U2 |
| P433 #1 | Gloomsilk cloth does not colour goza mats | confirmed | minor | `customizations/ClusterFStarterResources.cs:118-124`; `PIN/.../Craft/DefTailoring.cs:50-53` (exact `Cloth`/`UncutCloth` only), `:8-14`; ... | W14 |
| P433 #2 | Dawnstone recycle needs 45 Mining only in the guild bag | confirmed (broader) | normal | `customizations/SmithGuildSalvageBag.cs:62-78`; `PIN/.../Craft/Core/Resmelt.cs:77-92` and `PIN/.../Containers/SalvageBag.cs:75-87` (`_ => 0.0`); our ... | W11 |
| P433 #3 | `EachCraftsAt45AndNotAt44Point9` only calls `ConsumeRes` | test gap | - | `tests/Items/StarterResourcesVerification.cs:344-398` | W11 |
| P433 #4 | No test for Rootwood board / Burrowhide hides substitution | test gap | - | `patches/CraftItem-shard-hooks.patch:17-18`; `tests/Items/StarterResourcesVerification.cs:353-355` stocks leather and logs only | W11 |
| P433 #5 | Young cap test never frees a slot or checks summons | test gap | - | `tests/Regions/OldHavenBurrowsRegionVerification.cs:222-283` (tamed result only printed at `:271`); logic `customizations/.../OldHavenBurrowsRegion` ... | - |
| P434 #1 | Survey Saddle Roll schematics (Cartography) count as known without learning | confirmed | normal | `customizations/Engines/Craft/ClusterFRecipeGate.cs:130-133` (non-gated system returns Exempt before the `item.Recipe` check at `:135`), `:260-270`; ... | U6 |
| P434 #2 | Stock scroll/book learned on character A reaches the account only on A's next login | partly | minor | `customizations/Engines/Craft/ClusterFRecipeStore.cs:64-65,147-177`; `PIN/.../Skill Items/Misc/RecipeScroll.cs:79` | U6 |
| P434 #3 | Hidden item's details page opens through a details button (`3 + 7*i`); Last Ten lists locked items | confirmed | minor | `PIN/.../Craft/Core/CraftGump.cs:511-530` (no `IsKnown`), `:300-320` (Last Ten); `PIN/.../CraftGumpItem.cs:72-84` (`needsRecipe` stock-only); no patch touches these ... | U6 |
| P434 #4 | Pre-v3 craft guild members seeded at their rank, so that rank's book grants are never delivered | confirmed / needs PC | normal | `customizations/ClusterFGuildPromotion.cs:115-126`, `:152-157`; seeded from `ClusterFAccountData.cs:924` | U6 |
| P434 #5 | Fletching ranks 1-4 each deliver another tradeable Band IV book until one is read | confirmed | **urgent** | `customizations/ClusterFGuildPromotion.cs:160-167,182-197` (duplicate check is `Knows`, not "delivered"); ... | U6 |
| P434 #6 | Staff `revoke`/`forgetall` comes back from an alt's character recipes | confirmed | minor | `customizations/Engines/Craft/ClusterFRecipeStore.cs:105-128` (this character only), `:155-161` (alt's `Sync` re-adds), `:311-333` | U6 |
| P434 #7 | No lifecycle test for `AccountRecipeScroll` | test gap | - | `tests/Engines/Craft/RecipeGatingVerification.cs:467`; `customizations/Engines/Craft/RecipeItems.cs:39-47,138` | U6 |
| P435 #1 | Small commission can ask for dragon armour in a metal; the crafted piece is scale, so it never matches | confirmed | normal | `customizations/ClusterFSmithCommissions.cs:149-153` (dragon in small pool), `:197-214,537` (picker checks makeability only), `:720-728` (`resource != c.Material`); ... | W10 |
| P435 #2 | Large dragon set priced from the rolled ore it does not need | policy | normal | `customizations/ClusterFSmithCommissions.cs:338-342` (IgnoreMaterial, x2.5), `:579-595`, `:628-639` | Chase |
| P435 #3 | Large reward test asserts only `%3` and `>=15` for Seals | test gap | - | `tests/Misc/SmithCommissionRewardsVerification.cs:110-112` | W10 |
| P435 #4 | No test through the book/guildmaster; nothing calls `TurnInLargePiece`/`CompleteLarge` | test gap (part queued) | - | `tests/Misc/SmithCommissionRewardsVerification.cs:122-145` (`Complete` with a bare Longsword); grep finds no large-completion call in `server/tests` | P454 + W10 |
| P437 #1 | Negative Hall Renown setting raises the balance | partly | minor | `customizations/LeagueShop/LeagueShop.cs:148,198`; `customizations/ClusterFAccountData.cs:665-670` (`SpendRenown` accepts a negative amount); ... | W7 |
| P437 #2 | Pending dye target still works after the pigment leaves the pack | confirmed | normal | `customizations/LeagueShop/LeagueShopItems.cs:154-164,173-197` (checks only `_pigment.Deleted`); `PIN/.../Network/Packets/IncomingItemPackets.cs:35`, ... | W7 |
| P437 #3 | No test reaches `NoRoom` | test gap | - | `tests/Misc/LeagueShopVerification.cs:92,182`; code `LeagueShop.cs:179-190,219-223` reads correctly | W7 |
| P437 #4 | No test of a stale confirm, or of a title bought on another character | test gap | - | `tests/Misc/LeagueShopVerification.cs:199-213,484` | W7 |
| P438 #1 | Spent trap keeps its old 30-min decay bucket | confirmed | normal | DT:145 sets `LastMoved` directly (no `UpdateDecayRegistration`); DTs:340-352 `CountOut` counts spent traps toward the allowance; pin:Server/Items/Item.cs:340-355 ... | W2 |
| P438 #2 | Rearm skips the area cap | confirmed | minor | DT:496-520 `ReSet` → `ResetCharges` (:122-131) with no `ArmedNear`; the cap is checked only at placement, DTs:402, :434-446; payload path DT:530-532 | W2 |
| P438 #3 | Snare and shackle holds on players never call `Harm` | confirmed | normal (behind an off flag) | DT:242-250, :340-352 call `Hold` only; `Harm` is called only via `Damage` (:381-385) and gas (:269); DTs:59 `clusterf.traps.pvp` defaults to false, :289 | W2 |
| P438 #4 | Caltrops and bear trap bleed bleed-immune creatures | confirmed | normal | DT:255, :327 `BleedAttack.BeginBleed`; pin:UOContent/Items/Weapons/Abilities/BleedAttack.cs:29-37 (the immunity check is only in `OnHit`), :61-68; ... | W2 |
| P438 #5 | PvP mode can hit guildmates, party and pets | policy | - | DTs:281 excludes only the owner; :289-294 then defers to `CanBeHarmful` | Chase |
| P438 #6 | Traps can be placed in an unguarded SafeZone | not a bug (minor UX) | - | DTs:388-393; pin:UOContent/Engines/ConPVP/SafeZone.cs:7,17 (a `GuardedRegion` with guards off); pin:UOContent/Misc/Notoriety.cs:162-165 blocks harm | - |
| P438 #7 | Thin trap tests (damage, decay, safe zone, rearm cap, mixed targets) | test gap | - | server/tests/Items/Traps/DeployableTrapsVerification.cs:165, :341, :524 (as cited) | W2 |
| P439 #1 | Low-skill drinker makes a high-skill alt Young | policy | minor | FoY:388 checks only the drinker; :469-475 sets Young on every character; FoY:239 `maxSkillTotal` defaults to 0 (off); pin:UOContent/Mobiles/PlayerMobile.cs:3796-3801 ... | Chase |
| P439 #2 | Drink through walls or from another floor | confirmed | minor | FoY:113-114 `InUseRange` uses `m.InRange` (X/Y only, pin:Server/Mobiles/Mobile.cs:3076); :355, :406, :425 never check line of sight or Z | W13 |
| P439 #3 | Gate cast inside the sanctum lets others gate in | confirmed | minor | server/customizations/FountainOfYouth/FountainSanctumRegion.cs:57-65 (only Mark, RecallTo, GateTo); pin:UOContent/Spells/Seventh/GateTravel.cs:43, :47; ... | W13 |
| P439 #4 | No save/load test of the account reset | test gap | - | server/tests/Misc/FountainOfYouthVerification.cs:493-525 serializes only the addon (:506) | W13 |
| P439 #5 | Preservation test uses a trainer quest and never checks stats | test gap | - | FountainOfYouthVerification.cs:134-136 (`TheArtOfWar` as `otherQuest`) | W13 |
| P440 #1 | Arms Lore crafted roll runs before runic attributes (armor) | confirmed | minor | server/patches/BaseArmor-arms-lore.patch:17 (after `CheckSkill` inside the exceptional branch); pin:UOContent/Items/Armor/BaseArmor.cs:603, :606-609 ... | W12 |
| P440 #2 | DI-only nonexceptional weapon counted as non-magic | confirmed | minor | server/customizations/ClusterFArmsLore.cs:173-175 excludes `WeaponDamage` for every weapon; :163-164 | W12 |
| P440 #3 | Ownership test never targets another player's gear | test gap | - | server/tests/Skills/ArmsLoreMattersVerification.cs:318-336 (`other` is created but unused; only a ground katana) | W12 |
| P440 #4 | No edge tests (exhausted, max 1, Self Repair, +40 over cap) | test gap | - | ArmsLoreMattersVerification.cs:209 (as cited) | W12 |
| P440 #5 | Repair weakening tested only on katanas | test gap | - | ArmsLoreMattersVerification.cs:432 (as cited) | W12 |
| P441 #1 | Zero-durability wood rows still inflate hit points | confirmed | minor | server/customizations/ClusterFWoodBonuses.cs:206, :236 always assign `DurabilityBonus +=`; pin:UOContent/Misc/AOS.cs:1638-1650, :1727-1740 (unscale/scale on every ... | W12 |
| P441 #2 | Phantom Staff ignores the wood's elemental split | policy | minor | ClusterFWoodBonuses.cs:220-226 writes the split; pin:UOContent/Items/Weapons/ML Weapons/Artifacts/PhantomStaff.cs:20-27 forces 50 cold / 50 poison; the tooltip (pin ... | Chase |
| P441 #3 | No runic and wood overlap test | test gap (blocked) | - | server/customizations/ResourceInfo.cs:504-525: wood runic ranges are empty, so no overlap is reachable today | - |
| P441 #4 | No repair test for wood bonuses | test gap | - | server/tests/Items/ExtendedWoodBonusesVerification.cs:209, :242 | W12 |
| P442 #1 | Changing quality on worn armor leaves player resists stale | partly | minor | pin:UOContent/Items/Armor/BaseArmor.cs:189-199 (Quality setter: no `UpdateResistances`, unlike Resource :241-262); ... | W12 |
| P442 #2 | X1/X2 set resource and quality directly, not through real crafts | test gap | - | server/tests/Items/ExceptionalMaterialVerification.cs:105 (as cited) | - |
| P442 #3 | No old-save fixture | test gap | - | ExceptionalMaterialVerification.cs:38 (as cited) | - |
| P443 #1 | Taste ID on food and stationary Hiding train to cap | policy | - | server/customizations/ClusterFSkillGain.cs:331-333, :386-387; pin:UOContent/Skills/AntiMacroSystem.cs:96 (`Enabled = false`); TasteID.cs never consumes the food | Chase |
| P443 #2 | Apprentice bonus can overshoot a lowered total cap | policy | minor | server/customizations/Regions/ApprenticeTraining.cs:228-235; ClusterFSkillCaps.cs:30 (`totalCap` defaults to 0, off) | Chase |
| P443 #3 | Tactics rate model rolls per swing time, not per hit | test gap (rate report) | - | server/tests/Skills/SkillGainRateVerification.cs:178-181; pin:UOContent/Items/Weapons/BaseWeapon.cs:2520-2523 (Tactics is checked in `ScaleDamageAOS`, on hits) | - |
| P443 #4 | P191 notes headline: Imbuing "140 in 3.5 h" is really time to 120 | not game code (notes wording) | - | shard-migration notes/cc-P191-cont-earned-skill-gain.md:12 | - |
| P443 #5 | Fivefold crystal is not 5× faster once the chance saturates | not game code (notes wording) | - | notes/cc-P191...:215; pin SkillCheck.cs:145 | - |
| P443 #6 | No test of the production defaults with keys absent | test gap | - | SkillGainRateVerification.cs:273-300 always sets both keys; ClusterFSkillGain.cs:41-42, :92-95 | - |
| P443 #7 | S1 asserts only "reached 50" | test gap | - | SkillGainRateVerification.cs:437 | - |
| P444 #1 | Two reward confirmations open, points for only one: both deliver | confirmed | **urgent** | C/Gumps/BaseRewardGump.cs:169 (balance checked only before the confirm is sent), :254-259 `Confirm` (range and item only), :186-203 `OnConfirmed` delivers, then ... | U1 |
| P444 #2 | Spawn rectangles lose their east and south edge (XmlSpawner Width/Height are inclusive) | confirmed | minor | C/Services/Revamped Dungeons/BlackthornDungeon/BlackthornSpawns.cs:144 `Math.Max(1, d.Width)`; ServUO XmlSpawner2.cs:10754, :10756 `Random(m_Width + 1)`; pinned ... | W4 |
| P444 #3 | Minax roll uses converted luck where ServUO's Blackthorn call passes raw luck | policy | minor | C/.../Items/MinaxArtifacts.cs:101-106 (`LootPack.GetLuckChanceForKiller` / `GetLuckChance`), used at :172 and :200; ServUO BlackthornData.cs:61 passes ... | Chase |
| P444 #4 | Fourth Felucca castle entrance teleporter is at z 9; ServUO puts it at z 12 | confirmed (source misread); needs PC for the walking z | minor | C/.../BlackthornDungeon/Generate.cs:55 `(dest 6440,2680,20), at (1517,1420,9)`, header :16-17 states the opposite of the source; ServUO Generate.cs: `new ... | W4 |
| P444 #5 | Shield facing gump places from a stale response (other facet, deed given away) | confirmed | normal (urgent if you count the scam) | C/.../BlackthornDungeon/Items/DecorativeShardShields.cs:284-310: checks only `_shield.Deleted` and `_house != null`, places at `sender.Mobile.Map` :305, deletes the ... | W4 |
| P444 #6 | Hitching post stable/claim untested | test gap | normal | `DungeonHitchingPost` appears only in T/.../BlackthornDungeonVerification.cs (placement :168, deletion); C/Items/Addons/DungeonHitchingPost.cs:79-145 `EndStable`, ... | W4 |
| P445 #1 | Stock spawners make reward bosses outside the mini champion waves | policy; needs PC | normal | Pinned Distribution/Data/Spawns/post-uoml/termur/Abyss.json:209-230 (spawner at 974,161,-11 with `FireElementalRenowned` maxCount 18); the controller is at ... | Chase |
| P445 #2 | A save between a boss death and the next 1 s slice leaves the level stuck for good | confirmed | normal | C/Services/MiniChampionSystem/MiniChampSpawnInfo.cs:39-41 `[Tidy]` creature list, :72-76 counts kills only from dead entries still in the list, :61 `MaxSpawned = ... | W5 |
| P445 #3 | Survivors moved to `_despawns` are no longer leashed | confirmed | minor | C/.../MiniChampionSpawn.cs:317 moves them into `_despawns`; `OnSlice` :266-305 slices only `_spawnList`; `Despawn` :256 runs only from `Stop` | W5 |
| P445 #4 | Several completed Experimental gems each pay out during one cooldown | confirmed | normal | C/Services/Underworld/ExperimentalRoom/ExperimentalRoomChest.cs:39-41, :57-59 (any `Complete` gem, no cooldown or owner check); C/.../ExperimentalGem.cs:140 cooldown ... | W5 |
| P445 #5 | A save during rockfall leaves Navrey with CantWalk true after load | confirmed | minor | C/Services/Underworld/Navreys Lair/NavreysController.cs:348 sets it, :389 only the unsaved timer clears it, `AfterDeserialization` :296-307 does not clear it; pinned ... | W5 |
| P446 #1 | Card prints `Damage -1--1` for an NPC without SetDamage | confirmed | minor | C/ClusterFCreatureLevels.cs:471; pinned P/Mobiles/BaseCreature.cs:572, :582 (default -1); `TryAppraise` :369-372 accepts any BaseCreature, vendors included | W14 |
| P446 #2 | Cold and chaos breath described as "Breathes fire" | confirmed | minor | C/ClusterFCreatureLevels.cs:479-482, :497 skips the FireBreath type; pinned BaseInstrument.cs:243 tests the ability type; pinned Mobiles/Abilities/Fire ... | W14 |
| P446 #3 | A paragon's poison is shown at the base level | confirmed | minor | C/ClusterFCreatureLevels.cs:484-492; pinned BaseCreature.cs:1930-1932 (`CheckPoisonImmunity`), :2687 (`OnGaveMeleeAttack`), both raise the level for a paragon | W14 |
| P446 #4 | Ability group shown by its wrapper name; one weapon ability chosen at random | confirmed | minor | C/ClusterFCreatureLevels.cs:494-507 (`GetType().Name` of each ability, one `GetWeaponAbility()` call) | W14 |
| P446 #5 | Card rows of 424 px are cropped; the resist row measures 447 px | needs PC | minor | C/ClusterFCreatureLevels.cs:534, :550 (`AddLabelCropped(.., W - 36, ..)`) | PC |
| P446 #6 | No save/load test for level and con | test gap | minor | T/Mobiles/CreatureLevelsVerification.cs (no Serialize or RoundTrip); the level is recomputed (C/ClusterFCreatureLevels.cs:169-206) | - |
| P447 #1 | A player-made magic trap hurts a Young player in Old Haven | policy | minor | pinned P/Items/Containers/TrappableContainer.ExecuteTrap.cs:88 `from.Damage(_trapPower)` with no Young or notoriety check | Chase |
| P447 #2 | Guild exception lets a guildmate, ally or enemy attack a Young player | policy | minor | pinned P/Misc/Notoriety.cs:221-226 returns true before any Young check | Chase |
| P447 #3 | Retire skips Vorlak strays at x > 3680 or y > 2600 | partly; needs PC | minor | C/ClusterFOldHavenSeeder.cs:351-353 (X 3520-3680, Y 2420-2600), used for strays :168 and spawners :131, :287, :332; the old Vorlak spawner (header :14-15) was ... | W14 |
| P447 #4 | The gain that crosses 50 in an accelerated quest gets both bonuses | confirmed | minor | C/Regions/ApprenticeTraining.cs:191-195 reads `AcceleratedStart` after the gain; pinned Skills/SkillCheck.cs:273-276 (x2-5) then `BaseFixedPoint` set → ... | W14 |
| P447 #5 | Cancelling the quest leaves the training buff shown | confirmed | minor | C/Regions/ApprenticeTraining.cs:168-172 (a zero gain returns before `RefreshBuff`); pinned MLQuestEntry.cs:449-459 `Cancel` has no hook into it | W14 |
| P447 #6 | One-tile gap at x 3545 between New Haven and the training area | confirmed | minor | C/Regions/ApprenticeTraining.cs:297 starts at x 3546; pinned Distribution/Data/regions.json:1523 New Haven `x2: 3545` (exclusive end) | W14 |
| P447 #7 | No region-level tests of Young protection (combat, theft, expiry) | test gap | normal | T/Regions/OldHavenNewPlayerSafeVerification.cs:179 (region names only) | W14 |
| P448 #1 | Pets sparring (owner or own pets, Felucca) get the full multiplier | policy | normal | C/ClusterFPetGainSpeed.cs:57-66 (no opponent context); server/patches/SkillCheck-pet-gain-speed.patch:9; pinned SkillCheck.cs:252 (anti-macro for PlayerMobile only) | Chase |
| P448 #2 | The boost also makes stat rolls more frequent (P172 said stats were unchanged) | policy | minor | patch :9; pinned SkillCheck.cs:30 (`usePub45StatGain` defaults to Core.ML), :283-308 (stat roll inside `Gain`, even at cap); the pet stat delay of 5 min (:27) still ... | Chase |
| P448 #3 | Tests skip the Mobile.CheckSkill wrappers, cap/lock, transfer, EvoPet loops, Focus | test gap | minor | T/Skills/PetGainSpeedVerification.cs:119, :244-297 (calls `SkillCheck.CheckSkill` directly, GreyWolf only) | - |
| P449 #1 | Graduation pet pick lost on close, logout or full followers; "ask the recruiter again" has no recruiter path | queued (P453 item 2); confirmed on main | urgent (reward lost), test shard only today | C/Tutorial/ClusterFTutorial.cs:242 (Graduated set before rewards), :270 (pick is a gump only); C/Tutorial/TutorialGumps.cs:258-261 (retry text); recruiter shows ... | P453 |
| P449 #2 | Farm pet, skip, remedial: StationsDone cleared, a second bonded pet | queued (P453 item 1); confirmed on main | urgent (pays: second bonded evo pet), test shard only | ClusterFTutorial.cs:204-214 (StartRemedial clears StationsDone incl. PetKey, no participant check); TutorialFarm.cs:122-126 (StepOf reads PetKey), :186; ... | P453 |
| P449 #3 | An alt can skip, graduate or run stations for the trainee | partly: mostly fixed by P289; rest queued (P453 item 3) | normal, test shard only | Fixed: IsParticipant (ClusterFTutorial.cs:56-59, compares CharacterSerial) now gates RunStation :134, CompleteStation :153, Skip :174, Graduate :230. Left: ... | P453 |
| P449 #4 | No real disconnect/reconnect test (LogoutMap, pending pet) | test gap; partly queued (P453 item 8 has "close the pick", not a real reconnect) | test gap | T/Tutorial/GraduationLoopVerification.cs:202; T/Misc/TutorialVerification.cs:121; pinned Mobile.cs:1320 | P453 |
| P449 #(overlap) | Crystal's P477 T1 (island gate on live) and T2 (per-character loop box) | P449 does NOT raise either. T1 and T2 confirmed by me on main (see section 3) | T1 urgent (stuck), T2 urgent (pays) | T1: TutorialIslandGate.cs:13, :16-17, :27-28; ClusterFTutorial.cs:46-47, :69-76. T2: ClusterFTutorial.cs:80-85; ClusterFLoops.cs:23, :28, :47-60; ... | P477 T1/T2 |
| P450 #1 | Monster-steal hook rolls specials and skill gain after TryStealItem refused (weapon in hand, Young, SafeZone) | confirmed | normal | server/patches/Stealing-monster-stealing.patch:9-14 (hook runs whenever the pack is non-empty); MS/Core/StealingHandler.cs:128-215 (no empty-hands, Young or SafeZone ... | W8 |
| P450 #2 | A boss outside any listed place is NotHere even for a Master ("bosses anywhere") | confirmed (code contradicts its own header and P142's ladder) | normal | MS/Core/ThievesDenStealRules.cs:207-210 (None returns before the boss check), :159 (`_ => int.MaxValue`); header :12-15; notes cc-P142:24, :104 | W8 |
| P450 #3 | No death-path tests (gem kept, protected items, no corpse copy) | test gap | test gap | T/Services/Monster Stealing/MonsterStealingVerification.cs:380-399 (ghost body, Offer called directly); MonsterStealingShardRulesVerification.cs:694 | W8 |
| P461 #1 | Several 50-point ring confirmations accepted for one balance | confirmed | **urgent (pays)**; on (test shard) 10-24 | C/Gumps/BaseRewardGump.cs:167-171 (balance checked only when the confirm is sent), :186-205 (item delivered, then RemovePoints), :254-259 (Confirm checks range only); ... | U1 |
| P461 #2 | Jack's pumpkins hatch untracked undead, also after off/remove and after a reload | confirmed | minor | TOSD/Creatures/JackThePumpkinKing.cs:98, :132-139 (pumpkin placed, not tracked), :149-155 and :182-186 (timer restarts on load), :217 (spawn not added to ... | W1 |
| P461 #3 | Pumpkin placed at the attacker's spot 1 s later, wherever they are | confirmed | minor | TOSD/Creatures/JackThePumpkinKing.cs:98 (1 s delay), :105-140 (reads `from.Map`/`from.X` with no region, event or Deleted check) | W1 |
| P461 #4 | Enchanted Origin roll drops ServUO's SA (Stygian) equipment pool | confirmed | minor (fidelity, undisclosed) | TOSD/EnchantedOriginArtifacts.cs:88; pinned Misc/Loot.cs:668 (no isStygian argument), SA tables at :9, :15, used only by RandomWeapon :423-425 and RandomRangedWeapon ... | W1 |
| P461 #5 | Two queued skill confirmations on one ring: the second overwrites the first | confirmed | minor (a re-pick, no stacking: both write slot 0) | TOSD/Items/EscapingAndSterlingRewards.cs:47-53 (HasSkillBonus checked only on double-click), :171-176 (confirm writes `SetValues(_index...)` with no recheck) | W1 |
| P461 #6 | Toy, heart and pumpkin tests never advance the clock | test gap | test gap | T/Services/Seasonal Events/TreasuresOfSorceresDungeon/SorcerersDungeonVerification.cs:853-860, :930-935; 11 facts, none calls `ShardTestClock.Advance` or the confirm ... | W1 |
| P462 #1 | No test that a ridden dragon stops fighting | test gap | minor (dormant: staff-only, not tamable, nothing places or sells it) | T/Mobiles/Mounts/RideableDragonVerification.cs:94-130; C/Mobiles/Mounts/RideableDragons.cs:9-11, :47 (Tamable false), :56, :71 (GameMaster-constructible) | - |
| P462 #2 | Serializer test copies an unmounted dragon only | test gap | minor (dormant) | RideableDragonVerification.cs:79-92 | - |
| P462 #3 | No stable/claim or auto-stable test | test gap | minor (dormant) | RideableDragonVerification.cs:94 onward; no other reference to either type in C/ | - |
| P463 #1 | `clear` deletes a same-type guildmaster it did not place (and place skips ours) | confirmed | minor (staff tool, test shard only) | C/ClusterFGuildHallPlacement.cs:69-86 (FindNpc: type within 1 tile, any Z), :208-218 (place skips), :290-297 (clear deletes) | P477 O2 |
| P463 #2 | `place ... dryrun` relinks existing doors | confirmed | minor (dry run writes, though only toward the intended link) | C/ClusterFGuildHallPlacement.cs:180-184 (unconditional `west.Link`/`east.Link`) | P477 O2 |
| P463 #3 | Placement test hashes the C# copy, not `design/guild-halls/halls.json` | test gap | test gap | T/Misc/GuildHallPlacementVerification.cs:51-57; T/Misc/GuildHallPlacementDesignCopy.cs:8 | P477 O2 |
| P464 #1 | A title with quotes becomes `"`, which the web console rejects (HTTP 400) | confirmed | minor (staff tool, a visible error) | scripts/Shard-Console.ps1:1901 (curly quotes become `"`; straight quotes kept); web-console/server.py:133 (TEXT rule forbids 0x22), :140 (packageNotes) | W17 |
| P464 #2 | Staff-only feature advertised when a follow-up commit adds no changelog line | confirmed | minor (a suggestion Chase reads before publishing) | scripts/Shard-Console.ps1:1967 (the staff-only exclusion needs `$added.Count`) | W17 |
| P464 #3 | A single name over 120 characters gives a blank line, Empty false | confirmed (edge case) | minor | scripts/Shard-Console.ps1:1771 (`WhatsNewMax = 120`), :1912-1928 (Join-WhatsNew skips any phrase that does not fit; all skipped gives ''); :1863-1879 (prompt-title ... | W17 |
| P465 #1 | KhaldunZealot's BoneKnight replacement escapes surge tracking, End and restart cleanup | confirmed | normal | `ClusterFSurge.cs:542` (only the made creature is tracked), `:596-599` (a deleted Zealot is dropped), `:610-612` (the surge then auto-ends), `:700-721` (End deletes ... | W6 |
| P465 #2 | A stale End button or Give-extra cursor acts on whatever surge is running now | confirmed | minor | `StaffHubGump.cs:793-796` (End calls `ClusterFSurge.End`, which reads global `Active`, `ClusterFSurge.cs:662`), `StaffHubGump.cs:804-811` and `ClusterFSurge.cs:785` ... | W6 |
| P465 #3 | A non-bonded pet that dies before the next 1 s sample loses its owner's credit | confirmed | minor | `ClusterFSurge.cs:211` uses `pet.GetMaster()`. A dead non-bonded pet is deleted (pinned `Mobile.cs:4899-4902`), and `BaseCreature.OnDelete` clears its master (pinned ... | W6 |
| P465 #4 | The Give-extra cursor still mints the prize after the GM is demoted | confirmed | minor | `StaffHubGump.cs:807-811` (target callback, no access check), `ClusterFSurge.cs:783-807` (`GiveExtra`, no access check). Only `Respond` checks access, at ... | W6 |
| P465 #5 | An exception in Award stops the timer and skips cleanup; pressing End again repays | partly | minor | `ClusterFSurge.cs:673-698`: `Finish` stops the timer (`:675`), then `Award` (`:687`), then `RemoveEverything` (`:690`), with no try/finally. `Give` at `:777` records ... | W6 |
| P465 #6 | No audit log for surge start/end, template edits or extra grants | policy | normal | `StaffHubGump.cs:789-827` and `:1250-1271` (template save) call helpers directly. The only log line in `StaffHub/` is `ClusterFSurge.cs:872`. Pinned ... | Chase |
| P465 #7 | An invulnerable NPC template (Banker) never dies, so the surge never auto-ends | confirmed | minor | `ClusterFSurgeTemplates.cs:95-101` accepts any BaseCreature, and `ClusterFSurge.cs:610` ends only when every creature is gone. Pinned `BaseVendor.cs:50` ... | W6 |
| P466 #F01 | A chicken hit followed by a fatal trap (no source) gives Fowl Play | confirmed | minor | `ClusterFJokeAchievements.cs:283-289` (`FindMostRecentDamager(true)`). Pinned `TrappableContainer.ExecuteTrap.cs:88` (`from.Damage(_trapPower)`, null source), ... | W15 |
| P466 #F02 | Survive your own blast, then die to self-poison within 1 s, and Self-Detonation fires | confirmed | minor | `ClusterFJokeAchievements.cs:256-264`, `:290`, and patch `BaseExplosionPotion-self-blast-achievement.patch:7`. Pinned `BasePoisonPotion.cs:19` (`ApplyPoison(from, ... | W15 |
| P466 #F03 | The `_selfBlast` dictionary keeps survivors forever (through logout and character deletion) | confirmed | minor | `ClusterFJokeAchievements.cs:253` (static `Dictionary<Mobile,long>`), `:259` (set), `:264` (removed only at that player's death) | W15 |
| P467 #1 | P237's `gen_layout.py` and `protected.py` hard-code the Bronze worktree | confirmed | minor | shard-migration `notes/cc-P237-tools/gen_layout.py:7-9` (`SL = 'D:/UO/golems/Bronze/ShatteredLegacy'`, OUT, REG), `protected.py:17` (`CUS = ...Bronze...`). The ... | W17 |
| P467 #2 | The lantern animation test passes if the frames shrink to `[0]` | test gap | minor | `player-package/tests/Build-UoOverrides.Tests.ps1:456-462` checks the anim ID and that each frame is registered, but not the sequence, interval or start. ... | W17 |
| P468 #1 | Chopping with a full backpack drops the bound deed on the floor, where it decays | confirmed | normal | `LeagueHall.cs:314` (Deed), `:468` (`OnDroppedToWorld` refuses, but is bypassed). Pinned `BaseAddon.cs:84-121` (`OnChop`: `Delete()` at `:108`, then ... | W7 |
| P468 #2 | An open Hall confirm keeps the old price and AP need after staff raise them | confirmed | minor | `LeagueShopGumps.cs:179` (`Entry = entry` snapshot), `:222` (`Purchase(pm, Entry)`), `:350` (prices are resolved only when the row is clicked). `LeagueShop.Purchase` ... | W7 |
| P468 #3 | A house transfer gives gated decor to another account; chopping then strands a deed bound to the old buyer | policy | minor | `LeagueHall.cs:277-315` (`_boundAccount` on the addon, but nothing stops a transfer). Pinned `BaseHouse.cs:3836` (`Owner = to`), `BaseAddon.cs:88` (`OnChop` needs ... | Chase |
| P468 #4 | No save/load round trip for the deed, dyed case, or trophy wall offset | test gap | minor | `server/tests/Misc/LeagueHallVerification.cs:279`, `:332` (in memory only). The fields are serialized (`LeagueHall.cs:279-289`, `:324-330`, `LeagueHallComponent` ... | W7 |
| P469 #1 | uotinker backups made in the same second overwrite the first backup | needs PC | normal | Third-party source `D:/UO/third-party/code/uotinker/uotinker-0.2.0/src/Core.cs:1153` (also `:318`, `:584`, `Tables.cs:14`) is on the game PC only, not in any repo here | W18 (PC) |
| P469 #2 | UORegionEditor imports `{x,y,width,height}` as a 1-tile region at 0,0 | needs PC | normal | `R/ModernUoJson.cs:107` is PC only. The pinned half is confirmed: `Rectangle3DConverter.cs:102-121` accepts `x/y/w/width/h/height` | W18 (PC) |
| P469 #3 | UORegionEditor exports ServUO `Jail` as a `$type` pinned does not register | needs PC | normal | `R/ModernUoJson.cs:49` is PC only. Pinned `RegionJsonRegistration.cs:14` registers `JailRegion` | W18 (PC) |
| P469 #4 | uotinker's self-test cannot fail (it logs values, exit code 0) | needs PC | minor | `T/src/SelfTest.cs:115`, `:414`, `MainForm.cs:866`, PC only | W18 (PC) |
| P470 #1 | P235 treats large ore 1:1 with ingots | blocked | n/a | The rolled-order system is not built. The only order defs are the fixed ones in customizations/ClusterFWorkOrderSystem.cs (e.g. "Bronze Consignment" :548, "Verite ... | F-38 build |
| P470 #2 | Accepted offers refill at once, so Rush has no daily limit | blocked | n/a | Proposal only (P235 note :360, :445). The offer board does not exist in main. | F-38 build |
| P470 #3 | Haul examples ignore the mule cap (130 ore, 800 logs) | blocked | n/a | Proposal only (P235 note :310, :430, :437) | F-38 build |
| P470 #4 | Whole-gold rounding breaks the 1.5x bound (457.5 to 458) | blocked | n/a | Proposal only (P235 note :377, :443) | F-38 build |
| P470 #5 | Removing a def strands active entries | blocked (the code facts are confirmed) | would be a player loss if a def were ever removed | customizations/ClusterFWorkOrderSystem.cs:258-279 (WorkOrderEntry stores only DefKey/GuildKey/dates); customizations/GuildContractLedgerGump.cs:523-529 (TurnIn ... | F-38 build |
| P470 #6 | Proposal numbers rely on an untracked numbers.py; no tests planned | blocked | n/a | Proposal only. tests/Misc/GuildResourcesVerification.cs:343 does not cover gathering rewards (as stated) | F-38 build |
| P471 #1 | With the Testing Token on, the footer says "waived" and enables Upgrade with no usable source tool; the handler then refuses | confirmed | minor | customizations/ClusterFRequirements.cs:232-238 (`AllMet \ | W17 |
| P471 #2 | `Price` with overlapping costs shows both lines green but payment refuses | not a bug (latent) | n/a | customizations/ClusterFRequirements.cs:147-150 counts each cost alone; customizations/GuildResources.cs:319-324 `Has(pm, materials)` refuses the combined bill, so ... | - |
| P471 #3 | Tests set Base/Cap and never check the effective Value (the +5 pickaxe bonus) | test gap | n/a | tests/Misc/RequirementColorsVerification.cs:93-94 (Base/Cap set directly), :149 (the pickaxe goes to the pack via `Give`) | W17 |
| P471 #4 | Forged-button tests fail several requirements at once; the rich menu checks never press the button | test gap | n/a | tests/Misc/RequirementColorsVerification.cs:326-337 | W17 |
| P472 #1 | Sender regex accepts Chase's address inside another sender's quoted display name | needs PC | (urgent if real: someone else could control the Golem, but they would need a current reply code) | `D:\UO\golem\Away.ps1:390`. Away.ps1, Golem.Tests.ps1, Mail-Commands.ps1 and the rest are in none of the four repos (searched all four for Away.ps1 / Set-AwayMode / ... | W18 (PC) |
| P472 #2 | The auth-results regex accepts `gmail.com.<suffix>` | needs PC | normal | Away.ps1:399-400 | W18 (PC) |
| P472 #3 | An away-state event save can overwrite a concurrent "off" (no lock) | needs PC | normal | Away.ps1:36, :93 | W18 (PC) |
| P472 #4 | The parked filter misses indirect dependencies (P103 on P102 on parked P101) | needs PC | normal | Away.ps1:153, :159 | W18 (PC) |
| P472 #5 | When the code-file mutex times out, the body still runs | needs PC | normal | Away.ps1:275 | W18 (PC) |
| P472 #6 | Exception text, paths and possible secrets go into the emailed reply | needs PC | normal | Away.ps1:533, :535 | W18 (PC) |
| P472 #7 | A verified unknown command gets replies without limit and does not spend its code | needs PC | minor | Away.ps1:410, :518 | W18 (PC) |
| P473 #1 | Staff place on 10-23, shard down until 11-03: decor never comes down | partly | minor | customizations/ClusterFSeasonalSwitch.cs:201-219: with `last == false` and out of season on both checks, Sync returns early (:206) and never calls Down; ... | W17 |
| P473 #2 | Placement test has no door/approach exclusions | test gap | n/a | tests/Misc/HalloweenDecorVerification.cs:76-91 (checks only banker distance and teleporter tiles) | - |
| P474 #1 | Outrider's "mounted pace" and Hollow Oak's "lumbering pace" do not change movement | confirmed | minor | customizations/Mobiles/Bestiary/HavenHuntCreatures.cs:85-86 and BestiaryMiniBosses.cs:91-92 set only ActiveSpeed/PassiveSpeed. PIN ... | W3 |

## Drafts: urgent first

### U1 (urgent). Reward shops: one balance, several confirms, several rewards

```
# CC task P??: reward shops take the points before they give the reward (Blackthorn, Void Pool, Sorcerer's Dungeon)

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** BaseRewardGump checks the balance only when it sends the confirm window. Confirming delivers the item
first and then deducts, and the deduction's "not enough" result is ignored. A player who opens several confirms on
one balance and accepts them all gets every reward. Blackthorn and Sorcerer's Dungeon share the base. The Void Pool
shop repeats it in its own override. Sorcerer's Dungeon switches itself on 10-24 (cc-P477 O1), so this one goes
first.

Found by cc-P444 #1, cc-P461 #1 (Codex), and the Void Pool by cc-P476 (Crystal). Checked by cc-P476 against 0f1871f.

## What to do

1. `server/customizations/Gumps/BaseRewardGump.cs`: replace `virtual void RemovePoints(double)` (:180) with
   `virtual bool TryRemovePoints(double)` (base: false). In `OnConfirmed` (:186-205), before `CreateInstance`:
   refuse with 1073122 when `GetPoints(User) < citem.Points`, then `TryRemovePoints`, and refuse if it returns
   false. If the pack drop fails, refund (a `RefundPoints` hook) and delete the item.
2. `ConfirmRewardGump.Confirm` (:254-259): also require `from == User`, as well as the range check.
3. `server/customizations/Services/Revamped Dungeons/BlackthornDungeon/Gumps.cs:21` and
   `server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/SorcerersDungeonRewards.cs:56`: return
   the `DeductPoints` result.
4. `server/customizations/Services/Revamped Dungeons/Covetous Void Spawn/Gumps.cs:263-297`: the same order in its own
   `OnConfirmed`. Debit first and check the result (:293 ignores it today), then refund if the drop fails.
5. Model: Clean Up (`CleanUpBritanniaRewards.cs:250`) and the BOD shop (`BODRewardsGump.cs:164`) already re-check at
   confirm.
6. Tests, each red first (Blackthorn, Void Pool and Sorcerer's Dungeon verification files): a balance of one row's
   price, two confirms built and both confirmed. Expect one item and 0 points left. A full pack refunds.
7. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`). CHANGELOG, Fixed (no how-to): "Event and
   dungeon reward shops can no longer give two rewards for one set of points."
8. Notes `notes\cc-P??-reward-shops-pay-once.md`. Game PC: compare test-shard reward counts with point balances for
   these three shops, if the logs allow. Last line `P?? DONE`.

**Done means:** no confirm can deliver without a successful deduction, in all three shops, and the tests show it.
```

### U2 (urgent). Clean Up Britannia: the barrel's stack exploit, the trash bag wipe, the custodian's sweep

```
# CC task P??: Clean Up Britannia fix-up: barrel points by what is deleted, the trash bag keeps its contents, sweeps respect loot rights and walls

**Model:** Opus
**Touches:** server
**Golem:** any

**Summary:** Three player-facing bugs in the Clean Up and Custodian systems. (1) A trash barrel fixes a dropped
stack's points by serial at drop time. Splitting the stack leaves the original serial on the piece lifted out, so
one ingot thrown back pays for the whole stack, every 3-minute empty. A second stack that merges into the first
scores 0. (2) Asking the Warden for a new trash bag deletes every old bag the player owns, with its contents,
wherever it is. It is a blessed container, so players keep things in it. (3) `[cleanupall` deletes every eligible
item within 10 tiles: through walls, other players' kills, and unlocked items on house floors. It pays the
sweeper. The single `[cleanup` also ignores corpse loot rights.

Found by cc-P432 #1, #2, #4, #5, #6, #7 (Codex); widened by cc-P476 (Crystal). Checked against 0f1871f.

## What to do

1. Barrel (`server/customizations/Services/CleanUpBritannia/CleanUpTrash.cs:56-127`,
   `server/patches/TrashBarrel-clean-up-britannia.patch`):
   - Record `(dropper, amount dropped)` before `base.OnDragDrop`, so a stack that merges is still counted.
   - Price items when the barrel deletes them (`ConfirmCleanupItem`, :86-114), from the amount they hold then. Split
     a merged stack's credit by what each dropper added.
   - Drop a record when its item leaves the barrel (lift or remove), through the patch.
   - `CleanupTrashBarrel` and TrashChest confirm at once, so they are not affected. Keep them as they are.
2. Trash bag (`server/customizations/TrashBag.cs:76-91`): before deleting an old bag, move its contents into the new
   bag, or into the pack and then the bank. Or refuse while any old bag holds items. Add one line to the Warden's
   button (`SanitationWardenGump.cs:117`).
3. Sweep (`server/customizations/ClusterFCustodianSystem.cs:367-388`, single target :296-333). Per item:
   - Same map, |dz| <= 8, and `pm.InLOS(item)`.
   - No house, or a house the sweeper has access to.
   - For a corpse: `CheckLoot(pm, null)`, not `IsCriminalAction(pm)`, and no item that `IsChildVisibleTo` hides from
     pm.
   - At :130 and :163-173, refuse a corpse whose contents hold Blessed or QuestItem items or a non-empty container.
4. Store confirm (`server/customizations/Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:436-441`): the same map,
   the trader not deleted, and within 5 tiles in 3D.
5. Tests, red first:
   - `server/tests/Services/CleanUpBritanniaBarrelVerification.cs`:
     - drop 1,000 iron ingots, lift 1 (`Mobile.LiftItemDupe`), take the 999 back, drop the 1 back, empty: about
       0.1 points, not 100;
     - two droppers onto one stack each get their share.
   - The custodian tests:
     - a bag holding an ingot in the bank, then a new bag: the ingot survives;
     - the sweep skips an item behind a wall, an item 20 Z up, another player's instanced corpse, and an unlocked
       item in a house the sweeper cannot use.
   - The store: confirming from another facet buys nothing.
6. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`). CHANGELOG, Fixed (no how-to): "Trash
   barrels pay for what is actually thrown away. A new trash bag no longer destroys the old one's contents. The
   custodian's sweep only takes what you could pick up yourself."
7. Notes `notes\cc-P??-clean-up-fixups.md`. Game PC: the largest single Clean Up awards on the test shard. Last line
   `P?? DONE`.

**Not in this prompt (Chase decides, see "For Chase"):** the Sandals price (P432 #3), and whether the trash bag
stays a free blessed container that keeps its contents on death.
```

### U3 (urgent). High Seas fishing: Gravewater's free legendaries, traps that fish where their owner stands

```
# CC task P??: High Seas fishing fix-up: Gravewater rolls, traps fish their own water, Charybdis survives a save

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** Gravewater Lake's branch in FishInfo has no chance roll. Every successful cast at 115.1 Fishing gives a
legendary Zombie Fish, and at 102.9 a Holy Mackerel. A lobster trap rolls its catch from its owner's map, location
and region, not its own. Traps left anywhere roll Ice's Blue Lobster (or any region's rare) every minute while the
owner stands there. Both are inherited from ServUO. Also: a save during Charybdis's 3-second teleport strands it on
Map.Internal; a Felucca sea champion drops a ChampionSkull(None); the last artifact ticket never wins.

Found by cc-P426 #1-#5 (Codex). Checked by cc-P476 against 0f1871f.

## What to do

All under `server/customizations/Services/Expansions/High Seas/`.
1. `Items/Fish/FishInfo.cs:325`: add `&& info.Roll(from, baitStr, bump)` to the Gravewater branch, like every other
   branch (:310-333).
2. `FishInfo.GetSpecialItem` (:241-249, :330): when `harvestItem` is a `LobsterTrap`, take the map, location and region
   from the trap (`harvestItem.Map`, `.Location`, `Region.Find`). Keep the owner's skill. `Items/LobsterTrap.cs:341`
   passes the owner; that stays.
3. `Mobiles/Charybdis.cs:156-165`, :596-601: in `AfterDeserialization`, a Charybdis on Map.Internal with a remembered
   map and location goes back and is unhidden. Save `_lastLocation/_lastMap` (version bump) or fall back to its spawn.
4. `Mobiles/BaseSeaChampion.cs:44`: no skull when `SkullType` is None (an `OnDeath` path that skips pinned
   `BaseChampion.cs:236-261`'s skull branch, or a small pinned patch guard). `:157`: `>=` for the lottery.
5. Tests (`server/tests/Services/HighSeasFishingVerification.cs`), red first:
   - 200 casts at a Gravewater point at 120 skill are not all Zombie Fish;
   - a trap in plain Trammel water with its owner standing in Ice, roll forced: no Blue Lobster;
   - Charybdis internalized mid-teleport, then saved and loaded: back on its map;
   - a Felucca kill leaves no skull;
   - one damager with 1 damage wins the artifact.
   Add the SOS and bottle paths (#6) and a trap retrieval test (#7) while there.
6. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`). CHANGELOG, Fixed (no how-to): "Gravewater
   Lake's rare fish are rare again. Lobster traps catch what lives where the trap is."
7. Notes `notes\cc-P??-high-seas-fixups.md`. Game PC: count Zombie Fish and Holy Mackerel on the test shard. Last line
   `P?? DONE`.

**For Chase, not in this prompt:** lobster traps raise their owner's Fishing every minute, wherever the owner is and
offline (`Items/LobsterTrap.cs:322-325`, :275; ServUO's).
```

### U4 (urgent, test shard). The Rootdeep Vault: the Overdraft farm and the sealed corpse

```
# CC task P??: Rootdeep Vault fix-up: one Overdraft reward per trainee, and the Vault stays open until they leave

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** The Vault's "cleared" flag means both "rewarded" and "must leave", and it is set at the kill. A credited
trainee who stays inside can kill the respawning Overdraft every 3-4 minutes for its 100-gold pouch, Dawnstone ingot,
bandages and trinket. A trainee who dies after the kill (the respawned Overdraft still attacks them) is refused
re-entry from the landing ankh, and loses the corpse. Logging out before looting ejects them too. Split the flag.

Found by cc-P430 #1-#6 (Codex). Checked by cc-P476 against 0f1871f. The tutorial and the Vault run on the test
shard only (ClusterFTutorial.cs:46-47).

## What to do

1. `server/customizations/Regions/RootdeepVault.cs`:
   - Keep `VaultClearedKey` as "rewarded". Add a "left" key, set in `TryCrawl` (:204-228) and when a cleared player
     walks out.
   - `MayEnter` (:140-157) refuses only after "left". It lets a ghost, or a corpse owner whose corpse is inside, back
     in. `TurnOut` on login (:232-246) acts only after "left".
2. `server/customizations/Mobiles/Burrows/VaultCreatures.cs:282-291`: the Overdraft drops its reward only if a
   participant without `VaultClearedKey` is in its damage list. It does not engage a credited trainee
   (`IsEnemy`/`CanBeHarmful`).
3. Smaller:
   - `OnOverdraftDeath` (:175-187) credits through `DamageEntry.Responsible`, so a dead unbonded pet still credits its
     owner (#3).
   - Find the crawlway at its mouth (:103), not within 24 tiles of the corpse (:191) (#4).
   - The Hoarding Rat tracks its Penny Rats and removes them on death (`VaultCreatures.cs:126-150`) (#5).
   - The Burrow Mother saves or cleans up its brood (`WarrenCreatures.cs:162-163`) (#6).
4. Tests (`server/tests/Regions/RootdeepVaultVerification.cs`), red first:
   - a credited trainee's second Overdraft kill pays nothing;
   - credited, die inside, resurrect at the landing, walk back to the corpse: allowed;
   - credited, then log out and back in before crawling: not ejected;
   - a pet does all the damage and dies, then another player lands the last hit: the pet's owner is credited;
   - an Overdraft that dies in the Deposit Hall still opens the crawlway.
5. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`). CHANGELOG, Fixed (no how-to).
6. Notes `notes\cc-P??-rootdeep-vault-fixups.md`. Last line `P?? DONE`.

**Also:** the Overdraft is not slow on foot. Its speed is in W3, a separate draft.
```

### U5 (urgent). Bulk orders: the 2% reopen, dining deeds that cannot be finished, the off switch

```
# CC task P??: bulk orders fix-up: pending reward keeps its 20%, large dining deeds are finishable, the off switch covers the guilds

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:**
1. After a large deed's turn-in, closing the reward list (or logging out) and pressing Claim again offers 2% bank
   value instead of 20%, so 90% of the points' bank value is lost. Only the points are saved, not where they came
   from.
2. A large dining tinker deed rolls exceptional or a metal from its first entry (the butcher knife), but its spoon,
   fork and plate smalls can never be either. The deed can never be finished, and a bribe can push a deed into
   this.
3. The Foresters' and Alembic guild masters still take deeds while `ContentFeatureFlags.BulkOrders` is off.
4. A turn-in does not refill the 2016 order cache, as ServUO's does.

Found by cc-P423 #1-#4, #8 (Codex). Checked by cc-P476 against 0f1871f. All under
`server/customizations/Services/BulkOrders/`.

## What to do

1. `BulkOrderSystem.cs:701-760` (BODEntry): save the pending bank value (or a "large" flag) with the points, with a
   save version bump. Set it in `BulkOrderVendors.cs:333-337` (TurnIn), and read it at `BulkOrderVendors.cs:167`.
2. `CraftBOD.cs:365-374` (RollLarge) and `BulkOrderSystem.cs:366-398` (bribe):
   - Require exceptional only when every entry and its makeable twin can be exceptional
     (`SmallTinkerBOD.cs:46-48`, :61).
   - Require a material only when every entry can take one.
3. `BulkOrderGivers.cs:116`, :139 and :179: check `ContentFeatureFlags.BulkOrders`, as :162 does.
4. The shared turn-in success path (`BulkOrderVendors.cs`, before :366): port ServUO's `SetNextBulkOrder(type, pm,
   TimeSpan.Zero)`.
5. `LargeTinkerBOD.cs:44-50`: key `_makeable` by the base list, not a new array per deed (a slow leak).
6. Tests (`server/tests/Services/BulkOrders/BulkOrderCraftsVerification.cs`), red first:
   - a 210-point large turn-in, then the gump dropped, then Claim: the bank offer is 42, also after a save and load;
   - large dining deeds rolled 500 times are never exceptional or metal unless every small can be;
   - flag off: a carpentry deed dropped on the Foresters' master bounces;
   - cache at 0, then a turn-in: an order is ready;
   - 50 jewelry large deeds: the `_makeable` count is unchanged.
   Fix the self-comparing price test (:745, #9).
7. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`). CHANGELOG, Fixed.
8. Notes `notes\cc-P??-bulk-orders-fixups.md`. Last line `P?? DONE`.

**For Chase, not in this prompt:** the Master Chef's Apron adds its bonus to every craft (ServUO's; OSI is cooking
only), and the furniture, bow and reward prices that differ from OSI (P423 #5-#7).
```

### U6 (urgent). Recipe gating: pattern books per rank, schematics known for free

```
# CC task P??: recipe gating fix-up: each guild book once, own recipes in every craft system, old members get their books

**Model:** Opus
**Touches:** server
**Golem:** any

**Summary:**
1. Fletching ranks 1-4 each deliver another tradeable Band IV pattern book until one is read. The duplicate check is
   "knows", not "was given". Joining is free on every character.
2. The Survey Saddle Roll schematics (Cartography) count as known without being learned, because a system that is
   not band-gated returns Exempt before the item's own recipe is checked.
3. Craft guild members from before recipe gating are seeded at their rank and never get that rank's books.
4. Staff `revoke` and `forgetall` come back through an alt's sync.
5. A hidden item's details page and the Last Ten list still show locked recipes.

Found by cc-P434 #1-#7 (Codex). Checked by cc-P476 against 0f1871f.

## What to do

1. `server/customizations/ClusterFGuildPromotion.cs:160-167`, :182-197: keep a per-character `GrantedBooks` set
   (serialized, version bump). `Grant` skips a key that was already granted or is known.
2. `server/customizations/Engines/Craft/ClusterFRecipeGate.cs:126-138`: check `item.Recipe != null` before the
   `IsBandGated` early return, so `IsKnown` (:262-265) enforces an item's own recipe in every system.
3. `ClusterFGuildPromotion.cs:115-126` (`SeedFromStanding`): add a one-time catch-up that grants the books for ranks
   1 up to the seeded rank, at next login.
4. `server/customizations/Engines/Craft/ClusterFRecipeStore.cs:105-128`: `Forget` clears the key from every character
   on the account.
5. Optional, small: a patch to pinned `CraftGump.OnResponse` (:511-530) and `CraftGumpItem` (:72) refuses details for
   unknown recipes, and Last Ten (:300-320) filters them out.
6. Tests, red first:
   - `server/tests/Engines/Craft/RecipeGatingVerification.cs`:
     - Fletching 100 with rank-4 standing: one Update gives one book; a second Update, with the book unread, gives
       none;
     - a v2 guild record at rank 3 gets the rank 1-3 books once;
     - learn, sync an alt, revoke, sync the alt: still gone.
   - `server/tests/Mobiles/Mule/MuleModuleVerification.cs`: an unknown Survey Saddle Roll is not known, with gating
     on and off.
7. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`). CHANGELOG, Fixed.
8. Notes `notes\cc-P??-recipe-gating-fixups.md`. Game PC: how many pattern books are on the test shard, and whether
   any pre-v3 craft-guild members exist (this sizes item 3). Last line `P?? DONE`.
```

## Drafts that can wait (most valuable first)

Shared tail for every draft below: build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`), a CHANGELOG
line in player words (Staff for staff tools), notes `notes\cc-P??-<slug>.md` with last line `P?? DONE`. Every test
is shown red first.

### W1. Sorcerer's Dungeon fix-up: cleanup, pets' kills, the SA pool, the flaky test, its own switch

```
# CC task P??: Treasures of Sorcerer's Dungeon fix-up: everything it spawns goes at "off", owned pets earn nothing, its own automatic setting

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** Fixes for P408's port from Codex's P408 review, Valorite's P461 and Crystal's P477 O1. The double-pay
shop is U1, a separate prompt.

## What to do

All under `server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/`.
1. Cleanup (Codex P408 #2, P461 #2):
   - `Spawner.cs:283-286` (`Reset`) clears the spawn list without deleting it. Move those creatures to a saved
     cleanup list.
   - `Creatures/JackThePumpkinKing.cs:132-139`, :217: track each pumpkin and each hatched undead in the same list.
   - `Deactivate` (`Spawner.cs:136-166`) deletes the list and stops the pumpkins' timers.
2. Pumpkin placement (P461 #3, `JackThePumpkinKing.cs:98-140`): return when Jack is deleted, the event is off, or the
   attacker is no longer in Sorcerer's Dungeon.
3. Owned pets (Codex P408 #3): `SorcerersDungeonData.cs:127-129` reads `Controlled` after pinned's `OnDelete`
   cleared it (`BaseCreature.cs:3686-3687`). Read it from `DamageEntry.Responsible` or a pre-delete hook (the P455
   pattern).
4. The equipment pool (P461 #4, `EnchantedOriginArtifacts.cs:88`): pick weapons with ServUO's SA half
   (`isStygian = Utility.RandomBool()`), or record the deviation in P408's notes. Do the same at Blackthorn
   `MinaxArtifacts.cs:114`.
5. The ring (P461 #5, `Items/EscapingAndSterlingRewards.cs:171-176`): check again at confirm that the slot is unset.
6. The flaky test (Codex P408 #1, `server/tests/.../SorcerersDungeonVerification.cs:679`): make the artifact roll
   controllable in the tally test. Add clock-advanced tests for the toy, heart and pumpkin (P461 #6).
7. Its own switch (cc-P477 O1): `server/customizations/ClusterFSeasonalSwitch.cs:104-106`. `AutomaticKey` uses the
   switch's own name; the start and end keys keep `DatesFrom`. Add the new setting to the `[SorcerersDungeon` row of
   `docker/uo/COMMANDS.md`.
8. Tests:
   - "off" after a completed room leaves no event creature;
   - "off" with a pumpkin on the ground, then 10 s later: no undead;
   - a player's own unbonded pet killed in the dungeon adds no tally;
   - two ring confirms: the first skill stays;
   - the decor's automatic on and the event's off: in season, only the decor goes up.
```

### W2. Deployable traps: decay slot, rearm cap, criminal flag, bleed immunity, holds

```
# CC task P??: deployable traps fix-up: spent traps leave the allowance, rearm respects the area cap, snares flag, no bleed on the bleed-immune

**Model:** Sonnet
**Touches:** server
**Golem:** any

## What to do

All in `server/customizations/Items/Traps/Deployable/`.
1. `DeployedTrap.cs:145`: `SetLastMoved()`, not `LastMoved =`, so a spent trap leaves within 3 minutes instead of
   holding one of the owner's slots for up to 27 more (P438 #1).
2. `ReSet` (`DeployedTrap.cs:496-520`) and the payload drop (:530): refuse at `ArmedNear >= AreaCap` before anything is
   taken (P438 #2).
3. Snares (:242-250) and shackles (:340-352): call `Harm(t)` before `Hold`, for trap PvP (P438 #3).
4. Bleeding (:255, :327): skip `BleedImmune` creatures and Lich or Wraith form, as pinned `BleedAttack.cs:29-37` does
   (P438 #4).
5. Holds (:401-406, cc-P476): keep a per-mobile hold-until time, and unfreeze only when the last hold ends.
6. Tests (`server/tests/Items/Traps/DeployableTrapsVerification.cs`):
   - spent, then 3 minutes: deleted and the allowance freed;
   - six other armed traps, then rearm: stays spent;
   - with PvP on, an innocent snared: the owner is criminal;
   - caltrops on a Crystal Elemental: no bleed;
   - two overlapping holds: the victim stays frozen until the later one ends.

**Chase first:** friendly fire in trap PvP (P438 #5), before `clusterf.traps.pvp` is ever turned on.
```

### W3. Movement speeds that only change attack pace (P474, the Overdraft, caltrops)

```
# CC task P??: creature move speeds: set ActiveMoveSpeed where a creature is meant to be fast or slow on foot

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** Pinned takes walking pace from ActiveMoveSpeed/PassiveMoveSpeed (BaseCreature.cs:1130-1138). Four
places set only ActiveSpeed/PassiveSpeed, so the creature walks at the Medium table pace (0.45 s a step).

## What to do

1. `server/customizations/Mobiles/Bestiary/HavenHuntCreatures.cs:85-86`: the Snatcher Outrider gets fast move speeds.
2. `server/customizations/Mobiles/Bestiary/BestiaryMiniBosses.cs:91-92`: the Hollow Oak gets slow move speeds.
3. `server/customizations/Mobiles/Burrows/VaultCreatures.cs:271-273`: the Overdraft, the tutorial's "kiting lesson",
   gets slow move speeds.
4. `server/customizations/Items/Traps/Deployable/DeployedTrap.cs:413-442`: the caltrops slow scales and restores
   ActiveMoveSpeed and PassiveMoveSpeed too. Today it changes only the swing pace.
5. Tests:
   - `CurrentMoveSpeed` in the active state: Outrider < 0.45, Oak > 0.45, Overdraft > 0.45;
   - caltrops doubles `CurrentMoveSpeed` and restores it
     (`server/tests/Items/Traps/DeployableTrapsVerification.cs:178` checks only `IsSlowed` today).
```

### W4. Blackthorn port corrections

```
# CC task P??: Blackthorn fix-up: inclusive spawn rectangles, the z 12 castle teleporter, the shield gump re-checks

**Model:** Sonnet
**Touches:** server
**Golem:** any

## What to do

All under `server/customizations/Services/Revamped Dungeons/BlackthornDungeon/`.
1. `BlackthornSpawns.cs:144`: `Width + 1`, `Height + 1` (XmlSpawner's rectangles include their last row) (P444 #2).
2. `Generate.cs:55`: the fourth Felucca entrance teleporter stands at (1517,1420,12), not 9. P196 read ServUO's
   destination as the position. Fix the header (:16-17) and the test that pins the wrong z
   (`BlackthornDungeonVerification.cs:193`) (P444 #4).
3. `Items/DecorativeShardShields.cs:284-310`: the facing gump checks again that:
   - the deed is in the player's pack;
   - the player is on the house's map, and the house still exists, stands there and is co-owned by the player;
   - the shield fits.
   It places on the house's map. Today a deed sold while the gump is open is deleted from the buyer's pack (P444 #5).
4. A stable, save, claim test for `DungeonHitchingPost` (P444 #6).
5. Game PC: stand on Felucca 1517,1420 and read the walking z.
```

### W5. Mini champions and Underworld state across saves

```
# CC task P??: mini champions and Underworld: a boss level survives a save, survivors stay leashed, Experimental gems one per cooldown, Navrey walks after a load

**Model:** Sonnet
**Touches:** server
**Golem:** any

## What to do

1. `server/customizations/Services/MiniChampionSystem/MiniChampSpawnInfo.cs:39-41`, :72-76, :96: after a load, count
   creatures dropped as dead toward Killed. Today a save in the second after a boss dies leaves the level stuck for
   good (P445 #2).
2. `server/customizations/Services/MiniChampionSystem/MiniChampionSpawn.cs:266-305`: leash the living `_despawns` too
   (P445 #3).
3. `server/customizations/Services/Underworld/ExperimentalRoom/ExperimentalRoomChest.cs:39-41`, :57-59:
   - refuse a redeemer who is in cooldown, and put the redeemer in the table (P445 #4);
   - save the cooldown table (`ExperimentalRoomController.cs:15`, :22), which every restart clears today (cc-P476).
4. `server/customizations/Services/Underworld/Navreys Lair/NavreysController.cs:296-307`: clear Navrey's `CantWalk`
   after a load (P445 #5).
5. Tests: a boss level with the boss deleted, saved and loaded before the slice, then advances; two completed gems,
   one redeemed, the second refused; the cooldown survives a save and load; Navrey walks after a load.
```

### W6. Staff Hub surges

```
# CC task P??: Staff Hub surges: only safe creature types, stale buttons refuse, demoted staff cannot grant, pets' damage credits their owners

**Model:** Sonnet
**Touches:** server
**Golem:** any

## What to do

1. `server/customizations/StaffHub/ClusterFSurgeTemplates.cs:95-101`: refuse these template types:
   - creatures that replace themselves on death (KhaldunZealot), whose BoneKnight escapes cleanup (P465 #1);
   - vendors and invulnerable creatures, which never die, so the surge never ends (P465 #7).
2. `server/customizations/StaffHub/ClusterFSurge.cs`:
   - `End` and `GiveExtra` take the run the button was drawn for, and refuse another run (P465 #2;
     `StaffHubGump.cs:793-811`).
   - `GiveExtra` checks the caller's access (P465 #4).
   - Wrap `Finish`'s `Award` in try/finally, and keep a paid-set per run (P465 #5).
3. `ClusterFSurge.cs:208-230`: credit damage through `DamageEntry.Responsible`, so a pet that died before the sample
   still credits its owner (P465 #3).
4. Tests (`server/tests/Misc/StaffHubEventsVerification.cs`):
   - a KhaldunZealot template and a Banker template are refused;
   - a stale End leaves the new run active;
   - a demoted GM's cursor gives nothing;
   - a dead pet's hits credit its owner.

**Chase first:** an audit log of surge starts, ends and grants (P465 #6; recommended yes), and whether ghosts count as
"present" (cc-P476).
```

### W7. League Hall deeds and pigments

```
# CC task P??: League Hall and pigments: a chopped or orphaned Hall deed goes to the pack or bank, confirms re-price, pigments must be in the pack

**Model:** Sonnet
**Touches:** server
**Golem:** any

## What to do

1. `server/customizations/LeagueShop/LeagueHall.cs:277-315` (LeagueHallAddon):
   - Override `OnChop`. Refuse when the backpack cannot hold the deed (P468 #1). Today pinned drops the bound,
     Renown-bought deed at the player's feet, where it decays in an hour.
   - Send the deed to the bound account's bank box when the house is deleted (cc-P476). Pinned
     `BaseHouse.cs:3495` drops every addon deed on the ground.
2. `server/customizations/LeagueShop/LeagueShopGumps.cs:179`, :222: re-resolve the entry before `Purchase`, and show
   the confirm again if the price or AP changed (P468 #2).
3. `server/customizations/LeagueShop/LeagueShopItems.cs:175` and
   `server/customizations/Services/CleanUpBritannia/CleanUpPigments.cs:155-162`: the pigment must still be in the
   pack when the target lands (P437 #2 and cc-P476).
4. `server/customizations/ClusterFAccountData.cs:665-670`: `SpendRenown` refuses a negative amount (P437 #1).
5. Tests:
   - full pack, then chop: the addon stays and no deed is on the ground;
   - house deleted: the deed is in the bound account's bank;
   - price raised under an open confirm: the buyer is refused and nothing is charged;
   - a pigment moved to the bank, then the target lands: nothing is dyed.
   Add save and load tests for the deed (P468 #4) and the NoRoom path (P437 #3).

**Chase first:** gated decor that passes with a house transfer (P468 #3); dyes lost on chop (cc-P476).
```

### W8. Monster stealing: eligibility and bosses anywhere

```
# CC task P??: monster stealing: no special rolls when the steal was refused, and Masters can steal from bosses anywhere

**Model:** Sonnet
**Touches:** server
**Golem:** any

## What to do

1. `server/customizations/Services/Monster Stealing/Core/StealingHandler.cs:128-215`: refuse at the top of
   `HandleSteal` when pinned's `TryStealItem` would refuse: a weapon in hand, a Young thief, a SafeZone (pinned
   `Stealing.cs:99-110`) (P450 #1).
2. `server/customizations/Services/Monster Stealing/Core/ThievesDenStealRules.cs:207-210`: a boss outside any listed
   place uses the boss rank, as the header (:12-15) and P142 promise (P450 #2).
3. Tests (`server/tests/Services/Monster Stealing/MonsterStealingShardRulesVerification.cs`, through
   `Target.Invoke`):
   - a thief holding a weapon, or a Young thief, gets no special;
   - a Master next to a champion on open land is allowed, and an Initiate is refused.
   Add death-path tests (P450 #3).
```

### W9. Guild join: the Merchants' 500 gold and the join range

```
# CC task P??: guild join fix-up: the Merchants' apprentice task takes its 500 gold; joining needs the guildmaster nearby

**Model:** Haiku
**Touches:** server
**Golem:** any

## What to do

1. `server/customizations/ClusterFGuildSystem.cs:400-410`: consume for `ItemOnly` tasks (P431 #1). Today
   `Skills[0].Base < 0.0` is never true, so the gold stays.
2. `server/customizations/SmithGuildmasterGump.cs:311-325` and `server/customizations/SanitationWardenGump.cs:269-285`:
   require a guildmaster nearby (`ClusterFGuildSystem.cs:1200-1205`) (P431 #2).
3. Tests (`server/tests/Misc/GuildStarterPathVerification.cs`):
   - the apprentice task takes the 500 gold;
   - Join pressed from 20 tiles gives no join and no tools;
   - `ReplaceStarterItem` and `OwnsCopy` have tests (P431 #3).
```

### W10. Smith commissions: dragon armour in the small pool (add to P454 if it has not started)

```
# CC task P??: small smith commissions never ask for dragon armour in a metal

**Model:** Haiku
**Touches:** server
**Golem:** any

## What to do

1. `server/customizations/ClusterFSmithCommissions.cs:197-214`: keep `dragon_*` keys out of the small picker. Or let
   `IsMatch` (:720-728) accept scales for dragon pieces. Today the order cannot be finished, and abandoning it costs
   the cooldown (P435 #1).
2. Test: 500 small rolls at skill 120 with teaching off give no dragon key. Add a test of the small-path match and a
   stale second submit (P435 #4; P454 step 4 covers large).

Same file as the queued P454: the overseer may append this to P454 instead.
```

### W11. Resmelt and salvage: the metal's Mining requirement everywhere

```
# CC task P??: resmelting needs the metal's Mining skill, in the stock forge path and the salvage bag too

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** Pinned `Resmelt.cs:77-92` and `SalvageBag.cs:75-87` require 0 Mining for any metal they do not list.
Only the Smith Guild bag (`SmithGuildSalvageBag.cs:62-78`) applies Dawnstone's 45 and the post-Valorite tiers' up
to 200. A crafted piece gives back half its ingots at 0 Mining, which bypasses P56's harder post-Valorite smelting.

Found by cc-P433 #2 (Codex), widened by cc-P476.

## What to do

1. Move `SmithGuildSalvageBag.ResmeltDifficulty` somewhere shared.
2. Apply it through small patches to pinned `Resmelt.cs` and `SalvageBag.cs`.
3. Tests: a crafted Dawnstone dagger fails to resmelt at Mining 44.9 and succeeds at 45. The same for Platinum at its
   requirement. Add the craft-substitution tests (P433 #3, #4).
```

### W12. Arms Lore, wood bonuses, armor quality (small corrections)

```
# CC task P??: Arms Lore after runic properties, DI-only weapons count as magic, wood rows with no durability leave hit points alone

**Model:** Haiku
**Touches:** server
**Golem:** any

## What to do

1. `server/patches/BaseArmor-arms-lore.patch:17`: move the crafted roll after pinned `ApplyAttributesTo`
   (`BaseArmor.cs:606-609`) (P440 #1).
2. `server/customizations/ClusterFArmsLore.cs:163-175`: exclude `WeaponDamage` only for exceptional weapons
   (P440 #2).
3. `server/customizations/ClusterFWoodBonuses.cs:206`, :236: skip `DurabilityBonus +=` when the row's durability is 0
   (P441 #1). Today it adds 1-2 HP by rounding.
4. Optional (staff `[props` only): pinned's armor `Quality` setter updates the wearer's resists (P442 #1).
5. Tests:
   - runic exceptional armor at Arms Lore 180 has a gain chance;
   - a regular DI-only katana is rated magic;
   - a Ghostwood bow's hit points are unchanged by its row.
   Add P440 #3-#5 and P441 #4.
```

### W13. Fountain of Youth reach and gates

```
# CC task P??: Fountain of Youth: drink only within reach and sight; no gate out of the sanctum

**Model:** Haiku
**Touches:** server
**Golem:** any

## What to do

1. `server/customizations/FountainOfYouth/FountainSanctumRegion.cs:57-65`: refuse `GateFrom` for players, as
   `OldHavenBurrowsRegion.cs:110-114` does (P439 #3).
2. `server/customizations/FountainOfYouth/FountainOfYouth.cs:113-114`: within 16 Z and in line of sight (P439 #2).
3. Tests: a gate cast inside is refused; a player 20 Z above is refused. Add save and load of the account reset, and
   the stats check (P439 #4, #5).
```

### W14. Small corrections: Appraisal card, Old Haven training region, Gloomsilk goza

```
# CC task P??: small fixes: the Appraisal card's damage, breath and poison lines; the Old Haven training edges and buff; Gloomsilk colours goza mats

**Model:** Haiku
**Touches:** server
**Golem:** any

## What to do

1. `server/customizations/ClusterFCreatureLevels.cs`:
   - :471, no "-1--1" damage: use the weapon's range;
   - :479-482, name cold and chaos breath;
   - :484-492, a paragon's poison level;
   - :494-507, ability groups expanded, and every weapon ability listed (P446 #1-#4).
2. `server/customizations/Regions/ApprenticeTraining.cs`:
   - :297, start at x 3545;
   - :191-195, read "accelerated" before the gain;
   - :168-172, refresh the buff on quest cancel and on a zero gain (P447 #4-#6).
3. `server/customizations/ClusterFOldHavenSeeder.cs:351-353`: widen the stray-Vorlak bounds to the old spawner's
   reach (P447 #3).
4. `server/customizations/ClusterFStarterResources.cs:118-124`: Gloomsilk keeps its hue on goza mats (P433 #1).
5. Tests for each, plus region-level Young protection tests (P447 #7).
6. Game PC: an Appraisal card on a dragon in TazUO, for cropping (P446 #5).
```

### W15. Joke achievements: deaths credited to the right cause

```
# CC task P??: joke achievements: Fowl Play and Self-Detonation only for the death that earned them

**Model:** Haiku
**Touches:** server
**Golem:** any

## What to do

1. `server/customizations/ClusterFJokeAchievements.cs:253-264`, :280-292, and
   `server/patches/BaseExplosionPotion-self-blast-achievement.patch`: mark "blasting" only while the blast's damage
   runs (try/finally). Drop the static dictionary that keeps survivors forever (F02, F03).
2. Fowl Play and Instant Justice only when the latest damage entry is the death's (F01).
3. Tests: a chicken hit, then a sourceless trap death: no Fowl Play. A survived self-blast, then a self-poison death:
   no Self-Detonation, and nothing kept.
```

### W16. Fog of war: deleted characters' maps, short syncs

```
# CC task P??: fog of war: remove a deleted character's explored map; the client refuses a short full sync

**Model:** Haiku
**Touches:** server, client
**Golem:** any

## What to do

1. `server/customizations/ClusterFAccountData.cs:92-105`: add `RemoveExploration(serial)`, and call it from a
   `PlayerDeletedEvent` handler in `ClusterFExplorationSync.cs`. Each character keeps about 130 KB in the account
   save today (P424 #2).
2. `client/patches/0004-world-map-fog-of-war.patch:130-145`: accept a full sync only when it is the full length
   (P424 #1).
3. Tests: delete one of two characters; the other's bits survive and the deleted one's are gone after a round trip
   (`AccountDataSerializerVerification.cs:512`). A short gzip keeps the old bits.
```

### W17. Staff tools: package notes, P237 tools, the requirement footer, a season missed by downtime

```
# CC task P??: staff tool fixes: What-is-new quotes and long names, P237 tools find their checkout, the Testing Token footer, a season missed by downtime

**Model:** Sonnet
**Touches:** scripts, server, docs-only
**Golem:** any

## What to do

1. `scripts/Shard-Console.ps1`:
   - :1901, curly quotes become `'`, not `"`, which the web console refuses (`web-console/server.py:133`);
   - :1967, a staff-only prompt stays out of the line when a later commit adds no changelog line;
   - :1912-1928, cut an over-long name at a word boundary (P464 #1-#3).
   Tests in `scripts/tests/Shard-Console.Tests.ps1`.
2. shard-migration `notes/cc-P237-tools/gen_layout.py:7-9`, `protected.py:17`: read the checkout from `SL_SHARD`, not
   the Bronze worktree (P467 #1).
   `player-package/tests/Build-UoOverrides.Tests.ps1:458`: assert the lantern's frames, interval and start (P467 #2).
3. `server/customizations/ClusterFRequirements.cs:230-238`: some lines can be marked "not waivable". The Testing Token
   does not enable Upgrade without the source tool. Mark them in the four pickaxes and the Hammer (P471 #1). Add
   P471 #3-#4's tests.
4. `server/customizations/ClusterFSeasonalSwitch.cs:201-219`: save the last check date. A whole season missed by
   downtime still takes down what was placed (P473 #1).
```

### W18 (game PC). Golem Away mode and the third-party map tools

```
# CC task P??: on the game PC: Away mode's mail checks and locks; uotinker and UORegionEditor fixes or upstream reports

**Model:** Opus
**Touches:** golem tooling (D:\UO\golem), third-party tools
**Golem:** a home Golem (this code is in none of the four repos)

## What to do

1. `D:\UO\golem\Away.ps1` (P472), re-running P472's probes first:
   - :390, match the sender address, not the display name (urgent if it reproduces, though it needs a current reply
     code);
   - :399-400, anchor the auth-results domain;
   - :36, :93, :275, one lock for the state and code files, with no fall-through on timeout;
   - :153, :159, parked dependencies, transitively;
   - :533-535, no exception text or paths in mail;
   - :410, :518, unknown commands spend their code.
2. uotinker (P469 #1, #4) and UORegionEditor (P469 #2, #3): patch the local copies, or file upstream with P469's probe
   fixtures (`downloads/p469-review-probes/`). Until then, write a warning in the map pipeline notes.
3. Tests: P472's probes as Golem.Tests.ps1 facts, each red first.
```

### Not drafted

- **P425 #2, #3:** add a line to the queued P413: "delete or update the P188 teleporters the old way in placed
  (`ClusterFRootdeepSeeder.cs:315-326` matches on destination), so a reseed leaves one ladder teleporter." P425 #4:
  prove P413's route by server movement, not `build_way_in.py`'s height math.
- **P449 #1-#4:** queued in P453 (items 1-3, 8). P449 #3 is mostly fixed by P289; see cc-P477's note for the
  overseer.
- **P463 #1-#3:** the same as cc-P477 O2. Add to that draft: `ClusterFGuildHallPlacement.cs:180-184`, relink doors only
  when not a dry run; and test the real `halls.json`, not the C# copy.
- **P470 #1-#6:** the rolled work orders are not built. Give these six to whoever builds F-38's rolled orders. Also:
  a removed order definition would hold one of the 3 slots for good, because orders cannot be abandoned
  (`GuildContractLedgerGump.cs:523-529`, :555).
- **P462 #1-#3:** test gaps on staff-only dragons. Add them when Chase decides how players get one.

## For Chase (policy calls, no draft; my recommendation in each)

| Item | What | Recommend |
|---|---|---|
| P423 #5 | Master Chef's Apron adds its exceptional bonus to every craft (ServUO; OSI and its own tooltip say cooking) | Cooking only: gate on `MainSkill == Cooking` |
| P423 #6, #7 | Furniture, bow and some reward prices differ from OSI | Keep ServUO's until someone has a dated OSI table; only the mallet is buyable today |
| P426 (mine) | Lobster traps raise the owner's Fishing every minute, anywhere, offline | Gain only while the owner is within a screen of the trap |
| P426 #8 | Undocumented spawn bounds change | Write it beside D-138; no code |
| P432 #3 | Crafted Sandals pay 2 points against 0.4 of leather | Price player-made Sandals by material |
| P432 (mine) | The trash bag is a free blessed container that keeps contents on death | Make it hold only cleanup-eligible items |
| P435 #2 | Large dragon sets priced from the rolled ore they do not use | Price scale sets from a fixed tier |
| P438 #5 | Trap PvP can hit guildmates, party and pets | Exclude party and guild before PvP is ever on |
| P439 #1 | A low-skill drinker makes a high-skill alt Young (only with `maxSkillTotal` set) | Check each character's total |
| P441 #2 | Phantom Staff ignores the wood's elemental split | The artifact keeps its own split |
| P443 #1, #2 | Taste ID and stationary Hiding train to cap; the apprentice bonus overshoots a lowered cap | Accept #2 (stock); limit repeats for #1 with the earned-gain work |
| P444 #3 | Minax roll uses converted luck where ServUO's Blackthorn call passes raw | Keep the convention (ServUO's call looks like a slip) |
| P445 #1 | Stock spawners make Renowned reward bosses outside the mini champion waves (14 in Abyss.json) | Remove the stock Renowned entries where a mini champion runs; game PC to count them |
| P447 #1, #2 | A player-made box trap and the guild exception hurt Young players | Accept (stock) |
| P448 #1, #2 | Pets sparring get the full gain multiplier; stat rolls are more frequent | Accept #1 (standard training); write #2 in P172's notes |
| P465 #6 | No log of surge starts, ends and grants (60,000 gold per click) | Yes, log them |
| P465 (mine) | Ghosts count as "present" for the surge's share prize | Present means alive |
| P468 #3 | A house transfer gives gated Hall decor to another account | Refuse the transfer while bound addons stand |
| P468 (mine) | A dyed Hall piece comes back as an undyed deed when chopped | Keep the hue on the deed |

## What I could not check from GitHub alone

- Nothing was built and no test was run; each draft asks for a red test first.
- P472 (Away.ps1 and the Golem mail code) and P469 (uotinker, UORegionEditor) are only on the game PC (W18).
- Sizes that need the test shard's save: how many reward-shop doubles, Clean Up awards, Zombie Fish, pattern books and
  pre-v3 guild members exist (U1, U2, U3, U6); the Felucca walking z at 1517,1420 (W4); stock Renowned spawners in the
  Abyss (P445 #1); the Appraisal card's cropping (P446 #5).
- I spot-checked the urgent drafts' key claims myself (see "How the checking was done"). For the rest I relied on the
  helper sessions' file:line evidence, which named the exact lines; any line that moved before a draft is worked
  should be found by its quoted code.

P476 DONE
