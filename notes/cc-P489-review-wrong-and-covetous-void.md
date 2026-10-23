# P489: review of the Wrong and Covetous Void Spawn ports

Reviewed 2026-10-23. Code HEAD: `d58c75e`. Notes HEAD before this review: `5923b9c`.
This is a source review only. No code or tests changed, no build or game test ran, and no connection to Haven was made.

Read `AGENTS.md` in both work copies, the direction decision and task list, `notes/cc-P221-cont-fixup-port-wrong-and-covetous-void.md`, and the original `notes/cc-P194-port-wrong-and-covetous-void.md` it references. No separate P221 or P194 review note was found. Previously recorded deviations, open questions, and fixed defects are excluded from the findings below.

Paths in findings are relative to the code work copy. `Wrong/` below means `server/customizations/Services/Revamped Dungeons/WrongDungeon/`; `Covetous/` means `server/customizations/Services/Revamped Dungeons/Covetous Void Spawn/`.

## Findings

1. **bug: Wrong's spawn conversion drops the remaining XML entries** `Wrong/WrongSpawns.cs:64` keeps only the first entry of each `Objects2` value, reducing total capacity across both facets from 116 to 68 and leaving creatures such as `BrigandCannibalMage` unspawned; the existing test at `server/tests/Services/Revamped Dungeons/WrongDungeon/WrongRevampedVerification.cs:173` asserts the truncated capacity. Restore every entry separated by `:OBJ=` and check the complete type/count lists against an independent source fixture, rather than deriving the expected composition from `WrongSpawns.Definitions`.

2. **bug: Wrong's capture resurrection runs before the player becomes a ghost** `Wrong/Region.cs:115` calls `Resurrect()` during `Region.OnDeath`, but pinned ModernUO invokes that hook before `Mobile.OnDeath` changes the body to a ghost, so a normal death ends with a ghost in the cell; `server/tests/Services/Revamped Dungeons/WrongDungeon/WrongRevampedVerification.cs:387` starts with a ghost and calls the region directly. Schedule the first capture's resurrection after the normal death processing, with appropriate lifetime checks, and test a living player's actual `Kill()` path through the deferred callback.

3. **bug: pending reward confirmations can give rewards without payment** `Covetous/Gumps.cs:293` delivers the item before calling `DeductPoints` and ignores its failure, while `server/customizations/Gumps/BaseRewardGump.cs:254` confirms without rechecking the balance, so two pending purchases approved against the same balance can both deliver after the first spends the points. Recheck and successfully reserve or deduct the cost at confirmation, refund it if delivery fails, and cover two pending confirmations sharing one affordable balance.

4. **bug: a placed cauldron loses all remaining charges on reload** `Covetous/Items/CauldronOfTransmutation.cs:29` leaves `_charges` outside serialization and restores only the expiration time, so the loaded addon has zero charges even when it was usable before the save; the reward test creates and deletes the addon at `server/tests/Services/Revamped Dungeons/Covetous Void Spawn/CovetousVoidSpawnVerification.cs:718` without round-tripping it. Serialize the remaining charges with the appropriate version handling and test a partially used addon through a save and reload.

5. **risk: a tunnel can lead into a locked room without a return bedroll** `Wrong/Items/BedrollSpawner.cs:41` includes `(5868,554,15)`, but the nearest bedroll in its table is seven tiles away, so the four-tile search at `Wrong/Items/BedrollSpawner.cs:249` cannot establish a return link when either room tunnel chooses it; the room's doors are locked, and its exit has not been checked in a client. Add the missing room's return bedroll or select only room destinations with a reachable return link, and test every destination instead of only membership in `RoomDestinations`.

6. **bug: only one player's best single battle score updates per battle** `Covetous/VoidPoolStats.cs:74` returns immediately after the first qualifying player, so other first-time participants or players beating their personal records keep missing or stale entries. Process the entire score table, accumulate whether anything changed, and test a battle in which two players both improve.

7. **bug: the next battle erases the record battle's player scores** `Covetous/VoidPoolStats.cs:294` stores `CurrentScore` by reference in `BestWave.Score`, and `Covetous/VoidPoolController.cs:282` clears that dictionary when the next battle starts, leaving the record's wave and total intact but its player scoreboard empty. Copy the dictionary when creating `BestWave` and test that starting another battle preserves the record's player rows, including through a save.

8. **risk: restart cleanup can delete the new battle's first wave** `Covetous/VoidPoolController.cs:775` makes the battle eligible immediately after load, but the cleanup at `Covetous/VoidPoolController.cs:781` deletes all Covetous creatures in the region ten seconds later, so a player present during that window can trigger a new wave that is then removed without its tracked wave list being cleared. Complete old-spawn cleanup before enabling the next battle and cover a controller reload with a connected player present through the first ten seconds.

9. **risk: Cora's death and artifact delivery have no regression coverage** `server/tests/Services/Revamped Dungeons/Covetous Void Spawn/CovetousVoidSpawnVerification.cs:565` exercises Cora's abilities and then deletes her at line 593, while the artifact test exercises `DropRandomArtifact()` separately, leaving the death handler at `Covetous/Creatures/Cora.cs:363`, looting rights, and full-backpack fallback untested. Add a real kill with controlled randomness and eligible and ineligible damagers, checking both backpack delivery and the bank fallback.

## Evidence and scope

The first finding corrects a claim in P194's notes, rather than repeating an existing finding: 68 is the capacity of the truncated port, not the capacity of ServUO's source data. The comparison parsed `D:/UO/ServUO-pub57/RevampedSpawns/WrongRevamped.xml` with Python's XML parser, split every `Objects2` value on `:OBJ=`, and compared the resulting type/count pairs with `Wrong/WrongSpawns.cs`. Both files contain 38 spawner rows; 18 rows differ, listed below as nine locations shared by both facets. The other rows match their entry lists.

| Spawner center X,Y | Port line, Felucca / Trammel | Entries omitted on each facet | Capacity per facet, port / source |
|---|---|---|---|
| 5690,534 | 64 / 79 | EvilMage 1; Executioner 1 | 1 / 3 |
| 5724,561 | 65 / 80 | Executioner 1 | 1 / 2 |
| 5858,579 | 67 / 82 | HungryOgre 1; LizardmanDefender 2; LizardmanSquatter 2 | 1 / 6 |
| 5828,530 | 70 / 85 | Archmage 1 | 1 / 2 |
| 5825,593 | 71 / 86 | LizardmanSquatter 3 | 2 / 5 |
| 5703,639 | 73 / 88 | DemonicJailor 2 | 5 / 7 |
| 5860,554 | 74 / 89 | CaveTrollWrong 1; LizardmanSquatter 2 | 1 / 4 |
| 5800,575 | 75 / 90 | HungryOgre 2; LizardmanSquatter 3 | 2 / 7 |
| 5659,562 | 76 / 91 | BrigandCannibalMage 1; Executioner 1 | 5 / 7 |

Capacity here is `min(spawner MaxCount, sum(entry MX))`, summed across the file, including prisoner rows: the XML requests 126 and permits 116; the port requests 126 and permits 68. This is a source capacity measurement, not an observed population on the real terrain. ServUO's parser explicitly splits `:OBJ=` in `Scripts/Services/XmlSpawner/XmlSpawner Core/XmlSpawner2.cs:12694`, and its spawn loop caps both entry and total counts at line 9013. For example, XML line 42 has Fezzik, EvilMage and Executioner, while the port's line 64 has only Fezzik; XML line 546 includes the cannibal mage omitted at port line 76.

For finding 2, pinned `Projects/Server/Mobiles/Mobile.cs:4872` calls `Region.OnDeath(this)` and then `OnDeath(c)`; `Alive` at line 947 depends on the body, `Resurrect` at line 4566 acts only when not alive, and the player ghost body is assigned at line 4911. `Projects/UOContent/Mobiles/PlayerMobile.cs:2482` calls the base death handler. No shard patch changes that ordering. This is a call-order finding, not an observed in-game resurrection failure.

For finding 3, `server/customizations/Services/PointsSystems/PointsSystem.cs` implements `DeductPoints` as a boolean operation that refuses an overdraft. Pinned `Projects/UOContent/Gumps/Base/BaseGump.cs:43` defaults `Singleton` to false, and `NetStateGumps.cs:81` permits multiple pending confirmation gumps. Opening another reward list closes the list, not an outstanding confirmation.

For finding 5, a read-only scan of every `BedrollSpawner.Entries` coordinate found no entry within four tiles of `(5868,554,15)`; the closest are `(5861,560,15)`, `(5864,561,15)` and `(5867,561,15)`, each seven tiles away by the range check. `Wrong/WrongDecoration.cs` places that room's doors at `(5863,554,15)` and `(5863,555,15)`, and `Wrong/Items/WrongBarredMetalDoor.cs:97` refuses a closed locked door. Actual movement and alternative escape routes remain unverified, so this is a risk rather than a confirmed player-stranding report.

Findings 2 through 8 retain behavior also present in the corresponding ServUO sources. These are candidates for the working agreements' rule allowing repair of copied behavior that is broken; this review makes no fidelity decision and changes none of that code. Finding 1 is a porting error. Finding 9 is a test gap, not evidence that Cora's artifact drop currently fails.

Reviewed the canonical Wrong and Covetous source folders, their generator data and tests, and the shared files P221 lists: `server/customizations/Gumps/BaseRewardGump.cs`, `server/customizations/Misc/WearableExtensions.cs`, `server/customizations/Services/CommunityCollections/CollectionItem.cs`, `server/customizations/Services/PointsSystems/VoidPool.cs`, `PointsSystem.cs`, `server/patches/PlayerMobile-void-pool-context.patch`, and its routing in `docker/uo/apply-patches.sh`. Dependency checks used the clean pinned ModernUO checkout at `d4531cd94b739613155225c234900de9f47d2c88` and the read-only ServUO checkout at `d76bf44`.

No additional boss-loot defect was established beyond P194's already documented omissions. Cora's actual death rewards, real map traversability, terrain-dependent spawn success, and restart behavior remain unverified at runtime. No new tests were written, so there is no new red/green test claim.

Verification: the read-only XML and coordinate checks completed successfully, and `git diff --check` found no whitespace problems. Ran `tools/progress.py --dry-run` against this work copy with `Path.write_text` suppressed in memory because its report builder otherwise writes `tools/progress.json` even in dry-run mode; the report completed and no generated files changed. Only this review note is added; the code work copy is clean.

P489 DONE
