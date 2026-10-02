# Bug list: defects to look at fixing

Distinct from `patch-backlog.md`, which is about capability ModernUO does not have. This file is
about things that are **wrong**: ours, ServUO's, and ModernUO's.

**The rule that governs most of this file**, set by S2's D-4 and followed since:

> A ServUO bug that produces a *missing* result is copied faithfully. Fixing it would hand our
> players behavior no OSI or ServUO player gets, which is a fidelity deviation in the direction
> nobody thinks to check a wiki for. A ServUO bug that produces a *broken* result is fixed.

"Missing" means a branch never fires, a drop never rolls, a name reads oddly. "Broken" means the
game shows the wrong thing or a player cannot proceed. D-10, D-16 and D-46 are the three fixes; §3
is everything left alone.

**The `Dn` numbers in this file are local to this file** and are not the `D-n` deviations in
`fidelity-principle.md`. Only the hyphen tells them apart, which is thin, so: **the next free number
here is D47** (2026-10-02; re-derive with `grep -rhoE "\bD[0-9]+\b" notes docs | sort -u` before trusting it). I collided four of them on 2026-09-26 by numbering new rows from the highest in
section 1 without reading section 2, and `notes/gate-integrity.md` was written against the wrong
two as a result. Read the whole file before taking a number.

---

## 1. Open, ours, worth fixing

| # | What | Impact | Where |
|---|---|---|---|
| **D37** | **The console's `-DryRun` did not reach an action that runs in its own window.** `Invoke-ConsoleButton` built the child's argument line from action, shard, snapshot, phrase and `-Yes` and **never passed a mode**, and a child with no mode ran for real. **Correction, 2026-09-29, after reading the code and probing it:** the missing flag is real, but in the committed code it was **not reachable from a dry console**. A dry parent printed the plan and returned (`scripts/Shard-Console.ps1`, the old `:1580`) *before* the phrase dialog and `Start-Process`, and a WinForms probe showed the click handler does see `$script:dry = True`. **A console that shows the phrase dialog and opens a window was not in `-DryRun`.** `scripts/shard-console.log` has `live.stop` at 13:50:52 and snapshot create, restore and delete at 14:28 to 14:33, but it does not record the mode, so **how that console came to be live is unverified**. §6 item 2 of the note assumed a dry click opens a window, and T-018 was written against that; it never did | T-018 stopped `sl-modernuo` and T-017 ran snapshot Create, Restore and Delete on test for real, 2026-09-29. Either way the child's safety depended on a flag nobody passed | **FIXED 2026-09-29, verified by facts, not yet in a client.** (1) The parent always names the mode: `Get-ChildArgumentLine` (`:488`) puts `-Mode DryRun` or `-Mode Execute` straight after `-File`. (2) The child refuses: `Resolve-RunMode` (`:507`) returns `refuse` for any `Mutates` action, or unknown action, given no mode, and the entry exits 2 before reading any state (`:2023-2028`). Any dry signal wins over `Execute`. (3) Every headless run prints a banner before anything else, `DRY RUN`, `RUNNING FOR REAL` or `REFUSED`, and sets the window title to match (`Get-ModeBanner`, `:519`). (4) **A dry click on a window action now goes through the same phrase dialog and yes/no box as a real one, and opens the window**, which prints and runs nothing, so a dry run exercises the path that failed; the dialogs say DRY RUN in their titles. Headless use now needs `-Mode Execute`; nothing else calls it. **Facts** (`scripts/tests/Shard-Console.Tests.ps1:633-820`, 53 to 63, all green): every window action on every shard, clicked through `Invoke-ConsoleButton` with `Start-Process` recorded, dry and real; then the real child `powershell.exe` run on the captured lines for `live.stop`, `snapshot.restore` and `snapshot.delete` with a compiled recording `docker.exe` first on PATH, **zero docker calls** dry and with the old no-mode line. Each gate was broken on purpose and went red, file restored byte-identical. **Re-run T-017 and T-018 in the client.** `notes/shard-console.md` §6, §6.1 |
| **D34** | **`GargoyleAlchemist` shares a full type name with a pinned `[TypeAlias]`, and a saved one may come back as a `Glassblower`.** Ours is `Server.Mobiles.GargoyleAlchemist` (`ClusterFGargoyleVendors.cs:37`). Pinned's `Glassblower` carries `[TypeAlias("Server.Mobiles.GargoyleAlchemist")]` (`Mobiles/Vendors/NPC/Glassblower.cs:6`). **`TypeCache` files an alias under its full name in the same maps as real types** (`AssemblyHandler.cs:251-263`), and `FindTypeByName`/`FindTypeByHash` return the **first** type in the bucket (`:188-228`). Which one is first is an ordering fact that cannot be read from source | **unverified, and the window is now.** `ClusterFRoyalCitySeeder` seeds these vendors, so a fresh world creates and saves them. If saves resolve through that map, the NPC comes back as the wrong type. `GargoyleStoneCrafter` collides case-insensitively only, which is less bad and the same shape | **one fact settles it**, and it should run before anyone plays on a fresh world: assert `AssemblyHandler.FindTypeByFullName("Server.Mobiles.GargoyleAlchemist", false) == typeof(GargoyleAlchemist)`, then the same across a save round trip. If it fails, rename ours. About thirty minutes. `notes/reachability-audit.md` §8.1. **TABLED by Chase 2026-10-01: gargoyle and race work goes last, after the base game.** Measured the same day: `GargoyleAlchemist` is placed only by `ClusterFRoyalCitySeeder.cs:57,60` at two Ter Mur Royal City spots, the seeder is run by hand (nothing runs it on start), Ter Mur is not a start town (F-10, open), and the type already has two tests in `server/tests/TypeIdentity/TypeIdentityVerification.cs:75,97`. So nothing is accruing in the world the testers use. **Fix this before F-10 ships or before Royal City is seeded into the world that becomes live, whichever comes first** |
| **D33** | **Up to 219 of 768 item files in `server/customizations` are in no player's reach.** Measured by the CC9-close task: every `.cs` file whose declared types are named by **no other file** in customizations, `server/patches`, pinned `Projects`, or pinned `Distribution/Data`. 263 of 768 files, less the ten `ClusterF*` registered by `Configure`, two ML quest files and 32 GM-only staff suits, leaves **219**. By directory: `Items/Artifacts/Equipment` 132, `Artifacts/Decorative` 28, `Equipment/Weapons` 20, `Equipment/Armor` 14, `Jewelry` 11, consumables 6, other 8 | **29% of the ported tree may be unobtainable**, and the batch that found it turned up **18 more on top of D32's thirteen** (the twelve-piece Villainous Epiphany suite, five Virtue armour pieces, `AudChar`). **It is an upper bound**: it cannot see a type reached by a base-type pick, by reflection, by a `typeof` list in its own file, or by pinned's random loot. **But 11 of 11 sampled by hand are real orphans**, and seven of those eleven have the same gate | **this changes what the backlog is.** Of CC9's 24 remaining `upstream` files, a patch would make them compile and would put **one** of them in a player's hands; the rest are gated on Clean Up Britannia, the Virtue Artifacts points system, ServUO's treasure-chest tables, or a boss neither tree has. So the work is not patch work, it is **reachability** work, and it converges on a small number of subsystems. **Measure it exactly before batch 2 ships another 45 files.** P2's proposed `content_index.py reach` (`notes/backlog-remeasure-2026-09-28.md` §6.1, about 60 lines) is the instrument. `notes/cc9-close.md` §7  **MADE EXACT 2026-09-29, and both my numbers and my framing were wrong.** It is **340 of 570 ported content files, 60%**, not 219 of 768: the 219 were confirmed 219 of 219 with **zero false orphans**, and **121 more were found**. But the important correction is the shape. I wrote that the work "converges on a small number of subsystems". It does not. **Five one-file gates reach 117 files**, and the first ten gates, about 14 units of work, reach 167. Clean Up Britannia is the largest single gate at 47 files and ranks **tenth**, because it is a 20-unit subsystem. The cheap end is craft registration files in a pattern our tree already has (`KingsCollectionCarpentryRecipes`, `OrcMaskTailoringRecipe`): blacksmithy reaches 33 files, tailoring 26, tinkering 17, carpentry 8, **90 files for four hook files**. 80 files sit behind no gate worth naming. `notes/reachability-audit.md` §3  **The ranked gate numbers are an upper bound, proved 2026-09-29 by building gates 1, 2, 4 and 7.** They reached **50 files, not the predicted 84**. One assumption broke, three times: **the audit counted an `AddCraft` entry as reach whether or not a player can meet the entry's other conditions.** Tailoring predicted 26 and delivered 1, because 25 are recipe-gated and nothing hands out the recipes; carpentry predicted 8 and delivered 2, because the Darkwood pieces need peerless ingredients nothing drops; tinkering 17 delivered 14. Blacksmithy hit 33 of 33 exactly, and only because every one of its entries takes iron ingots. **A source is not a path until its own preconditions are reachable too**, which is the same recursion D32 and Q-066 are about. Gate 9 has the same shape and should be checked before it is trusted: pinned's commented-out drop code runs only if the boss is placed. `notes/craft-registrations.md` §0 |
| **D32** | **Thirteen recipes for items already in our tree have no source at all.** The Tiger Pelt set (`TigerPeltBustier`, `Chest`, `Collar`, `Helm`, `Legs`, `LongSkirt`, `Shorts`, `Skirt`) and the Dragon Turtle Hide set (`Arms`, `Bustier`, `Chest`, `Helm`, `Legs`) are ported and present. In ServUO they are crafted from recipes 560-584, and those recipes reach a player **only** through `TimeOfLegends.CheckRecipeDrop`, an Eodon kill drop, or an Eodon treasure chest. **We have neither.** Nothing in customizations constructs any of the thirteen either | **thirteen finished items that no player can ever obtain**, which is precisely the present-but-unreachable content the Q-064 answer called misleading. Worse than a missing item, because the type table says it is there | their gate is bigger than the garments': each Tiger Pelt recipe needs `TigerPelt` (4 per piece, from `WildTiger`) and each Dragon Turtle recipe needs `DragonTurtleScute`. **Neither resource class exists in pinned or ours, and `WildTiger` is not in ours.** A creature-plus-resource port per set, bounded, not a subsystem. Opened as **Q-066**. `notes/q-064-recipe-garments.md` §6  **Superseded in scope by D33 on 2026-09-29: these thirteen are not the problem, they are a sample of it.** |
| **D30** | **There are two Nginx Proxy Manager instances, both called `sl-proxy`, and the apex `shatteredlegacyuo.com` is configured on the wrong one.** Haven (`192.168.1.61`) runs the real web stack: NPM, `sl-wiki`, `sl-downloads`, `sl-dashboard` and `sl-vaultwarden`. Its NPM has exactly three proxy hosts, `wiki.`, `get.` and `vault.chasekfleming.com`, and **no entry for the apex**. A second `sl-proxy` on the Windows box (`192.168.1.58`) holds the apex, and nothing forwards 80 or 443 there | **the site has never been reachable from the internet**, and looked fine throughout because the router's split DNS answers `shatteredlegacyuo.com` with `192.168.1.58`. Two sessions were misled by reading `docker` output from whichever daemon happened to answer. `wiki.` and `get.` *are* reachable from outside, proved 2026-09-28, which is what ruled out the ISP and the forwards | `D:\UO\Haven-Website-Runbook.md`, owned by its own chat. **`docker info --format "{{.Name}}"` says which daemon a command actually reached**; use it before trusting any `docker ps` on this project. Related: `sl-website` runs nowhere, `get.` serves an empty directory and the wiki has no start page, because Haven runs the containers while the Windows box holds the content in `D:\ShatteredLegacy\docker\` |
| **D31** | **Haven's address is DHCP, not reserved**, and the router forwards 80 and 443 to that literal IP (`192.168.1.61/24 ... dynamic noprefixroute enp1s0`) | **the website and the household password vault would go dark together** on a new lease, with nothing on screen saying why. Vaultwarden is the reason this is not a cosmetic row | a UniFi DHCP reservation against Haven's MAC. Thirty seconds. In the runbook as step 6. CHASE |
| **D27** | **Every item built in a shard test reads tiledata row 0, so every piece of armour is `Layer.Invalid` and silently goes to the backpack instead of being worn.** `TileData`'s static constructor returns early under `Core.IsRunningFromXUnit` (pinned `Server/TileData.cs:293-301`), so `MaxItemValue` stays 0; `Item.ItemData` is `ItemTable[m_ItemID & TileData.MaxItemValue]` (`Server/Items/Item.cs:732`), and that **mask** is why seeding rows alone changes nothing. `BaseArmor` takes its layer from `ItemData.Quality` (`Items/Armor/BaseArmor.cs:166`), `Item.CanEquip` rejects `Invalid` (`Server/Items/Item.cs:2150`), and the creation path's `EquipItem` then packs the piece without complaint | **any fact that equips armour and asserts on what is worn is asserting nothing**, and it passes. The existing armour-set facts set `item.Layer` by hand, which is why this went four months unnoticed. Same family as D15: the test host quietly differs from the shard | found while writing the D26 fact, which could not assert "worn" until it seeded the six gargish cloth rows **and** set `MaxItemValue` to `0xFFFF` by reflection, restoring both in `finally`. All 148 tests pass with that in place. `notes/d26-gargoyle-kilt.md` §3.2 has the tiledata parser. **Belongs in `notes/port-recipe.md` and the `ShardTestClock` family of written-down test-host truths**, with D15 and D16 . **AUDITED 2026-09-27, and the answer is zero.** All 147 facts classified: **0 false passes**, 19 working around it, 24 in scope and sound, 104 out of scope. Not because the facts were careful, but because apart from D26's, **no fact drives a path that checks a layer at all**: they place items with `Mobile.AddItem`, which has no layer check. Guard added, `server/tests/Route/TestHostTileData.cs`. The shared seeding mechanism was deliberately **not** built, with the trigger named: the second fact that drives an `EquipItem` path with armour or a weapon. Three corrections to my brief: `MaxItemValue` is set at `:382`, not `:381`; **`BaseWeapon` takes its layer from `ItemData.Quality` too** (`Weapons/BaseWeapon.cs:199`), so an unqualified `Dagger` or `Longsword` is `Invalid` in a test as well; and `Bounds` is not an `ItemData` member. `notes/d27-worn-item-facts.md`  **CLOSED 2026-09-28.** The shared mechanism exists: `server/tests/Route/TestTileRows.cs`, a `TileRows` table of **nine** named row constants (D26's six, D28's three, no row no fact uses) and `TestTileRows.Seed(params)` returning an `IDisposable` scope that saves and restores both the rows and the mask. Both facts moved onto it and **neither keeps any reflection**; `grep SetMaxItemValue server/tests` now hits one file. The scope has its own gate fact. Full `build.sh`, **151/151**. `notes/test-host-truths.md` |
| **D21** | **Docker Desktop's port publishing hides every client address.** Every connection reaches ModernUO from `172.19.0.1`, the bridge gateway, whether it came from loopback, the LAN or the internet: 34 of 34 `Client:` lines on live, and probes from both `127.0.0.1` and `192.168.1.58` logged identically | **three features are silently off.** `ServerList` cannot tell a LAN client from an internet one, so `autoDetect` relays everyone to the container's own address; `maxAccountsPerIP` is a **shard-wide total**, not per household; and `IPRateLimiter` exempts every client as private (`IPRateLimiter.cs:59`). Any per-IP ban would ban everybody | `notes/player-package.md` A.1. Reverses under host networking, or on a Linux host where Docker preserves the source address. Neither is small. **Until then, treat every per-IP feature as off** |
| **D23** | **`sl-ddns` is unhealthy and rewrites Cloudflare every ten minutes.** It reads the record back through the router's split DNS, which answers `192.168.1.58`, so it never sees the value as correct although Cloudflare already holds `216.247.206.76` | API churn, and a health status nobody can trust | give ddns-updater a public resolver. Which setting does that is unverified |
| **D24** | **The content index still cannot see enum members as owners, or source-generated property names.** `unknown: Good` appears where `Good` is a ServUO enum member, and the four `unknown` files in the artifacts row probably resolve that way. Pinned's `[SerializableField] private int _recipeID;` emits `RecipeID`, which a ServUO file using the generated name reads as missing. Its same-graphic check reads only `: base(0x...)`, so **"no twin found" means "not found by this check"**, not "none exists" | files sit in `unknown` that are really co-port, and a few "absent" types may have pinned equivalents | `notes/index-blindspots.md`, "What the fixed index still cannot see". Left deliberately, to change one variable at a time while reproducing S9. Enum owners are the next fix and will move files between buckets  **FIXED 2026-09-27 (overnight A).** **25 files change bucket** across the five rows on today's tree and 4 in the artifacts row on the S9 tree, **every one of them from the enum fix**; the generated-name fix moves no file in any row, and 19 more keep their bucket but change which names they need. All listed by name. `--legacy` did not move: 567/320/81/10/44, 1,022 of 1,022, and its JSON is **byte-identical** to the run before the change. The generated-name mapping was not guessed: the generator ships only as a compiled analyzer DLL, so it was loaded from the NuGet cache and `GetPropertyName` invoked directly on every field name in pinned and ours, **603 of 603 agreeing**. `hidden` now reports `twin` / `none found` / `not run` per type, so "no twin" no longer reads as "none exists". `notes/index-blindspots.md` Part D  P2 added two more fixed-mode fixes on 2026-09-28 (decimal graphics in the same-graphic check; preprocessor lines no longer read as names), `--legacy` still 567/320/81/10/44. **The re-measure's real finding is not the 25 moved files.** Only **41 of 725** candidate files, 5.7%, were ever merely waiting on a name. But legacy labels 229 files "needs an upstream member", and on the fixed instrument **only 84 still do: 145 of 229, 63%, never needed a patch at all.** The backlog was not mostly smaller, it was mostly *misfiled as patch work*. `notes/backlog-remeasure-2026-09-28.md` |
| **D15** | **The test host regenerates one hit point every 8 ms**, in every fact. `UOContentFixture` never runs `RegenRates.Configure`, so `Mobile.DefaultHitsRate` is `TimeSpan.Zero`, `HitsTimer` runs at a zero interval and a damaged mobile gains a hit on every wheel tick: 125 a second | any fact that reads hit points across an `Advance` after damage is measuring regeneration, not the effect. One fact was bitten (D11) and two work around it deliberately | **Q-060 answered: leave it, write the rule down, and add a guard fact.** The rule belongs in the `ShardTestClock` header and `notes/port-recipe.md`  **The guard fact exists**, written 2026-09-26 in `7dfe7d1` along with the rule in `notes/port-recipe.md`. This row outlived its own fix by three days |
| **D16** | Two `ShardTestClock` truths its own header does not state. **`Arm()` leaves dropped timers flagged `Running`**, so an object created before an `Arm()` holds a timer that can never fire or restart. And **`Core.Now` is wall-clock after any fact that makes a test NetState**, because `PacketTestUtilities.CreateTestNetState` sets `Core._now = DateTime.UtcNow` (`:62`), so `Epoch` is not the process-wide base the header implies | harmless today: every timed fact creates its objects after `Arm()`, and nothing reads the date or time of day. A later fact that does either would be wrong and would look right | `notes/gate-integrity.md` A.5. Fix the header when something next touches that file  **The header is now complete (2026-09-28).** And a correction that matters more than the fix: **the two statements this row called false were corrected on 2026-09-26 in `7dfe7d1`, and nobody updated this row.** D16's clock half was written into the header and into `notes/port-recipe.md` then. What was genuinely missing was the `Arm()` and `Running` half, which the row correctly described as *not stated* rather than stated falsely. I read the row, not the file, and briefed work that was three days done. See §1b |
| **D17** | `NewHavenQuestBoardVerification.cs`'s header still says no fact there can send a gump. **D12 made that false** | a note that will send the next reader down the headless route for no reason | drop the sentence in the Q-058 picker task, which rewrites that file anyway |
| **D14** | **Nothing places a Fountain of Fortune**, three weeks after Q-021 answered where it goes (Ter Mur `1121, 957, -42`). `grep -rn "1121, 957\|FountainOfFortune()" server/` finds only the constructor and its test | the LuckyCoin's only reachable outcome is still its failure message, which is what D-4 of S2 said in September | an answered question that was never implemented. **Built by cc-P27 (`eccf5af`):** `[ClusterFSeedFountainOfFortune [dryrun]` places it at OSI's point, in the middle of a pool. **Open only until Chase confirms in game that the shore is reachable on foot** (cc-P27 1.2) |
| **Q-009 / D3** | `docker-compose.yml` carries an **uncommitted change** repointing the live script mount at `server/customizations` read-only. Directionally right, never verified, deploy-affecting | live shard | **CHASE decides.** Oldest open item on the project |
| **D4** | **Build cost is 6x the published estimate.** 20s unchanged, 266s with one changed file, against `cc2-timed-port.md`'s 0:44 which predates S4 and neither compiled nor ran tests | every batch estimate is optimistic | fix the estimate, not the build |
| **D6** | The runtime image ships **16 test-infrastructure assemblies of 53**, because the Dockerfile publishes `ModernUO.slnx` | inert, cosmetic | Q-032. **The trap:** that same publish line is the compile gate. Any fix must lose the test assemblies *and* still fail the build on a deliberately broken test |
| **D5** | `server/uo/` build tree is stale and predates the F1 recovery | confusing, not harmful | leave; gitignored and generated |
| **D2** | ModernUO has no `Quest.StartingItem` equivalent. **How many of the 203 quests need one is unmeasured** | blocks an unknown slice of the quest row | Q-025, measure before the quest batch |
| **D39** | **The reachability audit's gate predictions are unreliable, and the planning curve built on them is worse.** Four gates have now been built against their predicted file counts: tailoring predicted 26 and delivered 1; gates 9 and 12 predicted 9 greedy (17 alone) and delivered 2 (cc-P7); gate 3 predicted 24 and delivered **0**, because its premise, "entries in pinned's lists", describes lists that do not exist (cc-P8 §2.2). Only gate 5 hit its number, 17 of 17 | **the numbers are an upper bound and the audit says so**, but they are being used as a roadmap. §3's cumulative curve ("gates 1-5: 5 units, 117 files, 31%") is the figure quoted when scoping, and three of its five inputs are now known wrong. Scoping the next tasks off it will keep producing briefs whose stated value cannot be delivered | **the instrument counted a reference as reach without checking the entry's other conditions.** Fix is a correction pass over §3 recording delivered against predicted per gate, and a restated curve. Cheap, blocked on nothing. Until then, treat any gate's file count as a ceiling and re-derive before briefing it. `notes/reachability-audit.md` §3; `notes/cc-P7-*.md` §0; `notes/cc-P8-*.md` §0, §2.2 **CORRECTED 2026-09-30 (cc-P12).** Two things in this row were understated. **Nine gates have been built or attempted, not four**, and the headline planning figure was worse than reported: "gates 1-5: 5 units, 117 files, 31%" was **65 files, 17% delivered**, with no prediction left in it. Full curve restated with delivered and predicted in separate columns (all 27: 292 predicted becomes 227, of which 70 delivered). **Cause, in one line: the instrument finds the code site that would put a type in the world and stops there**, never asking whether that site's own preconditions are met, and the hand grouping on top read "pinned declares the owner" as "pinned has the list". **Blacksmithy and gate 5 hit exactly because their sources are terminal**: the only precondition is something already in play, and pinned has the identical slot. §3.1.3 now rates each unbuilt gate; note that **gate 11 looks like one unit and is the shape that has already failed three times**. `notes/cc-P12-audit-correction.md` |
| **D44** | **Talisman and quiver stat bonuses are probably never removed on unequip.** Pinned adds them under one name and removes them under another (`UOContent/Misc/AOS.cs:598` vs `:620`; cc-P25 2.6). Read from code, **not yet seen at runtime** | repeated equip and unequip would stack Str, Dex or Int until a restart. **Unbounded since Chase's 2026-10-02 decision to remove every stat ceiling** (`notes/p25-decisions-2026-10-02.md`): the 500 clamp was its only backstop, and past 32767 the status packet shows garbage (`OutgoingMobilePackets.cs:523-542`) | first a fact that equips and unequips a `BonusStr 10` talisman three times and expects no offset left (cc-P25 Part 5). If red, a pinned patch in `AOS.cs` or our own wrapper. Next defect batch |
| **D45** | **Meditation's start chance gets worse as Int rises.** The chance uses the absolute mana deficit, `(50 + (Med - (ManaMax - Mana)) * 2) / 100` (ours `customizations/Meditation.cs:83`, same as pinned `Skills/Meditation.cs:76`), so a bigger pool needs more mana in hand before meditation can start | at Med 120: 56 mana needed at Int 200, 356 at Int 500. Harmless at OSI's 125, felt once stats pass it, which they now will (no ceilings, p25-decisions) | ours, no patch: make the deficit relative to the pool (cc-P25 Part 5 row 7). A deviation once made. Next defect batch |
| **D46** | **The content index's own test suite has one stale failure.** Its twin-sweep fact names `GauntletsOfAnger`, which cc-P8 deleted (D35). Also, `GuildResources.SatchelTypes` (cc-P22) makes `GemologistsSatchel` read as reached, since the tool counts a type read as reach (cc-P27 3.5) | a red tool suite trains people to ignore it; one false reach | tools only: new example for the twin fact, `SatchelTypes` into `READER_SITES`, and `docker/uo/apply-patches.sh` added to the audit's reproduction line (cc-P27 8.2). Small; next tools pass |

## 1b. Our own documentation defects, because a wrong note costs as much as a wrong line

**2026-09-29: the Clean Up Britannia framing was wrong, and it came from a misread table.** The
CC9-close note cited Clean Up Britannia as the gate for 21 types across three sections, and D33
repeated it. Those citations were all `CleanUpBritanniaData.Entries`, which is **the points a player
earns by turning an item in**, not the reward table. None of those types is a Clean Up reward. The
real gate for five of them is the Virtue Artifacts system; two have no source in ServUO at all.

CC found and corrected this itself, in the same task, by rebuilding the instrument that produced the
claim. Worth recording for the shape rather than the detail: **a table that lists a type is not
evidence of what that table does with it**, and a name that reads like "rewards" is not a reward
table. The sample that made the original claim look solid (seven of eleven hand-checked) survives,
because those seven really are rewards. A correct sample and a wrong generalisation.


**2026-09-29, mine: I sized a batch that could not ship, and only found out because I asked the
right question by luck.** The CC9-close brief listed `NystulsWizardsHat`, `GypsyHeaddress`,
`MalabellesDress` and `JesterHatOfChuckles` as ports. All four are museum collection rewards, the
same case as the Zoo and Library types I excluded by name in the same document, and the jester hat
is additionally a twin of pinned's `JesterHatofChuckles`, which `AssemblyHandler` already resolves
because its lookup is **case-insensitive**. `MysticBook` is likewise pinned's `MysticSpellbook`,
value for value, and CC9 batch 5 had already written that down five weeks ago.

I took those names from P2's batch table, which was produced by an instrument that cannot see
collections or craft tables and **said so**. I carried the list forward without the caveat attached
to it. The reachability rule in §1 of that brief is the only reason the batch did not ship four
items nobody could get and two duplicate types.

**The rule this suggests: a list produced by the instrument is a list of candidates, and the word
"candidate" has to survive the copy into the next document.** Every time it has been dropped, the
next reader has treated a measurement as a decision.


**2026-09-28, mine, and it is a process defect rather than a one-off: I briefed three tasks from
this file without checking whether this file was current.** P1 came back with five corrections, and
the two that matter are the same mistake twice. I told it to fix two false statements in the
`ShardTestClock` header and to write D15's guard fact if it was missing. Both had been done on
2026-09-26, in commit `7dfe7d1`, and **the rows still described the work as outstanding.** D16's
fix column even said "fix the header when something next touches that file"; something had.

Three smaller ones in the same brief: I said port-recipe needed all three truths when it already
held two; I wrote that CC had *measured* the fixture side effects when D27 §5 had *deduced* them
from `Item.cs`, which is a different and weaker claim; and I restated D27 unqualified as "every
`BaseArmor` and `BaseWeapon` is `Layer.Invalid`" when it holds only for those that do not set their
own layer, which `BestialArms` now does.

**The rule that follows, and it belongs to whoever closes a task, not to whoever writes the next
brief: when a fix lands, update its row, even when the fix was incidental to some other task.** A
`Dn` row's disposition column is a record of what was *decided*, and it silently becomes a claim
about what is still *pending*. Nothing in this file distinguishes the two, so the only defense is
updating rows as work lands. Both stale rows above were closed by a commit that was doing something
else, which is exactly the case that gets missed.


**2026-09-28, mine: Q-064's answer rested on a premise nobody had checked.** I answered it "items
and recipes together, after checking whether pinned has the craftsman satchel path at all", which
framed the satchel as the gate. It is not. In ServUO the tailor's craftsman satchel drops a
**hard-coded** list, `501-505, 550-552`, and never 560-566
(`Services/MondainsLegacyQuests/BaseReward.cs:151-154`). The real source is an Eodon kill drop,
`TimeOfLegends.CheckRecipeDrop`. So the check I asked for would have come back "yes, pinned has it"
and would have answered the wrong question.

Where the premise came from is the useful part: `notes/index-blindspots.md` Part A reasons from
**pinned's** satchel, where only registered recipes can drop, and I inherited that into Q-064 as
"registering may be the whole job". Part A is correct about this shard and silent about ServUO. **A
note that is true of one tree quietly became an assumption about the other**, which is the same
failure as reasoning from ServUO's vocabulary to ModernUO's capability, running in the opposite
direction.

The trap it nearly caused: pinned's satchel draws from every `AddRecipe`-registered tailor recipe,
so registering the seven that way would leak them into quest satchels, which ServUO never does.
Pinned's `AddQuestRecipe` registers without entering the pool and is the correct call.


**2026-09-27, mine: I wrote D28's mechanism up as exotic when it is ordinary.** The row said the
inherited member "lives in no file, so no file-to-file diff can find it." It lives at ServUO
`GargishLeatherArms.cs:19`, an explicit `Layer = Layer.Arms;`, and a diff of the old parent's
constructor would have caught it. I had the layer-from-tile-row mechanism in hand from D27 and
stopped reading once it explained the symptom. **A mechanism that explains the symptom is not
thereby the whole mechanism**, and calling a defect undetectable discourages the very check that
would have found it. The real lesson is duller and more useful: the member list for a re-parent was
taken from **pinned's** version of the old parent instead of **ServUO's**.


**2026-09-27, mine: I gave D27's brief a reason that was not the reason.** I wrote that the
armour-set facts "sidestep it by setting `item.Layer` by hand, which is why four months of work
never tripped over it." CC disproved it directly: it deleted all nine hand-set layers and **all 18
set facts still passed**, because they place pieces with `Mobile.AddItem` (no layer check) and
`SetHelper` finds them by walking `Mobile.Items`, not by layer. The hand-set layers protect nothing
those facts assert. They do one thing, and it is the opposite of protection: **they hide the layer
the item really gets**, which is exactly how D28 got through. A plausible causal story, asserted
without a probe, nearly turned a real defect into a settled explanation.


Six D-numbers and one patch row have now been written claiming ModernUO lacks something it has.
All were caught in review or by a later batch, none reached a player, and all share one cause.

| What was wrong | Found by | Cause |
|---|---|---|
| **D-47**: `SkeletalLich` "casts Magery only; its Necromancy is set and unused" | review, Q-050 | stock `MageAI` carries the necromancer branch; it casts necro 44-48% of the time |
| **D-45**: `Spellbinder` loses "spirit-speak heal, teleport and dispel" | review, 2026-09-26, while building the D-register | pinned `MageAI` has all three as its own constants: `HealChance = 0.10`, `TeleportChance = 0.05`, `DispelChance = 0.75` (`:18-20`). ServUO's are 5%, 5%, 75%. **The whole deviation is 5 points of heal chance.** This is the `HealChance` trap already named in `AGENTS.md`, so the trap was written down and the entry it had already produced was never revisited |
| **D-44**: `GreenGoblinScout` loses "hide, blink and flee below 20%" | settled 2026-09-26. **The flee claim is wrong**, the other two stand | the scout runs `AI_Melee`, and pinned `MeleeAI` overrides `BaseAI`'s `FleeHealthThreshold => 0.0` to `0.2` with `FleeChance => 0.1` (`MeleeAI.cs:9-10`). Restate D-44 at two thirds its recorded size |
| **My own claim that pinned's AI base class was "not in the checkout"** | me, an hour later | I ran `find` in the cloud container, where only staged files exist, and read the empty result as a fact about the pinned tree. It is at `Projects/UOContent/Mobiles/AI/BaseAI/BaseAI.cs`. **The same error as the rest of this section, one level up:** an absence where I happened to look, taken as an absence in the thing itself. It reached a committed document. The check is to list the directory on the machine that holds the tree |
| **P1's top row**: `AI_NecroMage`, "189 lines for 20 creatures, best value on the board" | review, Q-050 | written from D-47 without checking pinned. Withdrawn |
| **D-55, D-56, D-62, D-68**: `DragonBreath` dropped as a Pet Training loss on four creatures | CC6 batch 5, Q-054 | pinned has it as `MonsterAbilities.FireBreath`/`ColdBreath`. **CC4 had already used it** |
| Three "losses" in one CC6 batch 3 brief: `SetAreaEffect(AuraDamage)`, `HealChance`, `SetMagicalAbility(Poisoning)` | CC6 batch 3, in pre-flight | the first two exist under other names; the third only ever ran in a `Deserialize` branch |
| CC9 §2b listing `GargishClothKilt` as an extract still to do | CC6 batch 5 | pinned registers that name as a `[TypeAlias]` of its stock armour |

**The single cause:** reasoning from ServUO's vocabulary to ModernUO's capability. A missing enum
member, a missing method name or a missing type name is evidence about the *name*. The check that
settles it is to grep pinned for what the thing **does**, and it takes one command.

**The counter-habit that works**, and the reason none of these shipped: every batch's pre-flight
greps both trees for every type it is about to touch, and reports what it finds rather than what the
brief told it. Batches 3, 4 and 5 each corrected their own brief this way, three times over.

## 2. Fixed, kept so the cause is not re-learned

| # | What it was | Cost |
|---|---|---|
| D7 | A fresh test world blocks on `AccountPrompt` forever. No accounts means `ConsoleInputHandler.ReadLine()` on stdin: `docker ps` says Up, the listener never opens, the client hangs at "verifying account". The prompt fires at container start, so attaching later shows nothing to answer | **a week** |
| D8 | The test shard relayed clients onto the **live** shard. `Configuration-test` copied the live config, which advertises `192.168.1.58` with `autoDetect` false | a test session could silently run against live |
| D9 | `docker-compose.yml` mounted the **live world save**, so testing wrote into the real world | one stray account reached the live save before this was caught |
| D10 | `MAKE X` label invisible: `AddLabel` given `0x7FFF`, an RGB555 color, where a hue index belongs | open since June; affected the **live** shard |
| **D11** | **The build gate went red about one run in five, and the cause was not timing.** `CC6Batch8Verification`'s stygian fireball fact asserted a hit was still visible 4 s after the damage, in a host that regenerates 125 hits a second (D15). The player had 125 max hits, not the ~300 its comment assumed, because ML caps a player's `Str` at 150. So a roll of 126-150 killed and the fact passed; a roll of 120-125 left the player alive to regenerate, and the fact failed. **6 rolls in 31, 19.4% by construction**; measured 8/50 on HEAD and 15/60 in process, 0/50 after, plus 10/10 full `build.sh` runs. Fixed by reading the hit on the wheel tick it lands and asserting the fireball's own range | four wasted FINAL attempts on 2026-09-26, and **every green build claimed before it was a 4-in-5 draw**. My prompt's "wall-clock dependency", "streaks" and 35% rate were all noise |
| **D18** | **`progress.py` and `build.sh` disagreed on the test count by exactly one**, from CC6 batch 2 until 2026-09-26: 69 against 68, then 137 against 136, then 138 against 137. The cause was that `progress.py` counted the **substring** `[Fact]`, and `AthenaeumIsleQuestVerification.cs:7` carries one **in a comment**. It now counts attribute lines and agrees with the gate | every test count this project published for three weeks was one high | found and fixed in the armour-set task. The constant gap was the clue and nobody followed it |
| **D12** | **No shard test could assert on a gump**: the builder stage had none of the runtime stage's native libraries, so the first gump a test compiled killed the test host in `LibDeflateBinding`'s finalizer. Fixed with one 2.1 MB layer after the ModernUO clone, carrying exactly the runtime stage's list less what line 6 already had, and proved by `GumpOnTheWireVerification`, which was watched dying on the old Dockerfile and is kept as the gate for that layer | the quest board task spent most of ninety minutes proving its gumps headless instead. `libzstd` and `libargon2` were the same trap waiting for the first test to touch archives or password hashing |
| S8/D1 | The test route could not construct any `BaseCreature`. **The cause first recorded here was wrong** (Q-031): the data file was in the test output all along. Nothing called `NPCSpeeds.Configure` | a wrong diagnosis that survived a week |

**A diagnostic that proves nothing, learned 2026-09-26 while D19 had the shard blocked:**
`Test-NetConnection <host> -Port <published port>` against a Docker-published port **succeeds whether or
not the process behind it is listening**, because Docker's forwarder accepts the connection itself. It was
used to rule out the server side and it ruled out nothing; the answer was in `docker logs` the whole time.
`docker ps` saying Up is the same kind of non-evidence. For "is the shard actually accepting players", read
the log for the listener, or connect a client.

**The pattern in D7 through D9, worth naming:** three of the four were *test rig* defects that made
the rig quietly point at production. None was found by reasoning; each was found by asking the
machine. The week D7 cost was spent on four plausible fixes applied without first probing whether
the thing being fixed was the thing that was broken.

**Tooling, 2026-09-27: `device_commit_files` caches by staged path.** Committing the same
container path twice in a session writes the **first** version's bytes the second time, and still
reports `written`. Two doc edits were silently lost to this before it was spotted; the earlier
"the write was lost" incident in this section was very likely the same cause, not a stale read.
The rule: **give every commit a new file name**, then verify with `device_list_dir` and check the
byte count against what was written. Staging the file back immediately after a commit also serves
a stale copy, so it is not a check either.


## 2a. Closed 2026-10-02 (moved from section 1 by the overseer, each checked)

| # | Closed how | Original row |
|---|---|---|
| D38 | Fixed 2026-09-29 (cc-P10). | **The console swallows the output of every `exec` step.** `Invoke-Plan` runs `& $s.Exe @a` (`scripts/Shard-Console.ps1`, the `'exec'` case, around `:1416-1421`), so the child's stdout goes to the function's return value, not the screen. The headless entry assigns it (`$ok = Invoke-Plan ...`, `:2088`) and the form discards it (`[void](Invoke-Plan ...)`, `:1723`). Only the exit code survives / **a failed rebuild says only "exited with 1"**: 2026-09-29 15:28-15:32, `test.rebuild` ran `Start-TestShard.ps1` for three minutes and failed with no gate name, test name or error on screen. Affects every ... |
| D36 | Fixed 2026-09-29 (cc-P10), verified on the test shard; the old live is retired. | **A `docker stop` does not save the world.** Measured 2026-09-29 on the test container with synchronous probe lines (the Serilog console sink is asynchronous, `Server/Logger/LogFactory.cs:25`, which is why "Shutting down" was never seen): on SIGTERM **no managed shutdown runs at all** in this image, not `AssemblyLoadContext.Unloading`, not `AppDomain.ProcessExit`, not `EventSink.Shutdown`; the process is gone in under a second with exit 143, whatever `-t` says. So `HandleClosed` (`Server/Main.cs:333-348`) never runs on a stop, and **the earlier text here was wrong on one point: `-t 60` does no... |
| D35 | Done 2026-09-29 (cc-P8). | **Two ported artifacts duplicate types pinned already has, under spellings that differ only by a transposition.** Ours `GauntletsOfAnger` against pinned's **`GuantletsOfAnger`** (pinned misspells the class), and ours `ShroudOfDeceit` against pinned's **`ShroudOfDeciet`**, where the spellings are swapped between file and class in the two trees. Both matched on cliloc (1094902, 1094914) / no player holds a duplicate, because ours are unreachable and pinned's are the ones champion spawns drop. But **the type table claims content pinned already has, reachably**, which is what makes a backlog count... |
| D29 | MOOT with D40: concerns the retired live image. | **The image the live shard is running no longer exists in the image store, and any `docker compose up` in `docker/uo` would destroy it.** `sl-modernuo` runs `sha256:36cc709a…` (container created 2026-06-29); `docker image inspect` on that ID says "No such image", and the `uo-modernuo` tag now resolves to a **different** image, `bc04a35bf344`, built 2026-09-06 10:45 in the middle of that day's direction changes, contents unrecorded. The running container holds the only copy of the server the live world was saved by. Separately, the running container no longer matches `docker-compose.yml` (its `... |
| D28 | Fixed 2026-09-27; verified in code 2026-10-02 (`BestialArms.cs:18`, `Layer = Layer.Arms`). | **`BestialArms` sits on the chest layer, not the arms layer.** ServUO's derives from `GargishLeatherArms`, whose constructor calls `base(0x302)`, and `BaseArmor` reads the layer from the tile row **at that moment**; only afterwards does `BestialArms` set `ItemID = 0x4052`, and changing an item ID does not recompute the layer. Our port onto `BaseSetArmor` passes `0x4052` straight to the base call, and `0x4052` is `Gargoyle Armor Plate`, quality 13, **InnerTorso** / **a gargoyle wearing any chest piece cannot equip Bestial Arms, and one wearing Bestial Arms cannot put a chest piece on.** Proved ... |
| D26 | Fixed 2026-09-27; verified in code 2026-10-02 (`customizations/CharacterCreation.cs:808-809` equips `GargishClothKiltType1/2`). | **A gargoyle created without a profession is dressed in a cloth chest and cloth *legs*, and no kilt.** `CharacterCreation.AddPants` (ours and pinned's, byte for byte) equips `GargishClothLegsType1/2` for `Race.AllowGargoylesOnly`. ServUO pub57's `AddPants` equips `GargishClothKiltArmor` there (`Scripts/Misc/CharacterCreation.cs:140`). Gargish legs cover the shin; the kilt covers the pelvis, and they sit on different layers, so legs alone leave the character in underwear / **every gargoyle a family member makes starts undressed**, on the first screen they ever see. Chase observed it in a client... |
| D25 | MOOT with D40 (2026-09-30): the old live world is retired and the test world becomes the next live. | **The live shard runs an image that predates everything since early September.** `docker inspect sl-modernuo --format "{{.Config.Image}}"` returns **`uo-modernuo`**, not `sl-modernuo:latest`. Its serialized type table holds no CC9 type at all, not even `GargishDagger` (measured across the live save, `Saves-test`, every automatic backup and the daily, hourly and monthly archives during the armour-set task) / **anything tested on the live shard will appear to be missing.** Chase searched the Add Menu for `gargishwarhammer` on 2026-09-27, found nothing, and the type has been in the tree since 202... |
| D22 | Fixed: `name: sl-uo-test` is at `docker/uo/docker-compose.test.yml:27` (verified 2026-10-02). | **`docker compose -f docker-compose.test.yml down --remove-orphans` would stop the live shard.** Both compose files sit in the same directory and so share the project name `uo`, which makes compose report `sl-modernuo` and `sl-ddns` as orphans of the test stack / one flag away from a live outage, on a command that reads as safe / one line, `name: sl-uo-test` at the top of the test file, then remove the old test container once by hand. Not done in the task that found it: it changes the test stack's network |
| D19 | Struck through earlier; closed. | ~~**`Start-TestShard.ps1 -Fresh` cannot produce a usable shard.**~~ It wipes `Saves-test`, re-copies the live `Accounts` folder in, builds, and starts the container. The copy succeeds (`Accounts.bin`, 1281 bytes, correct path), but **with no world save present ModernUO does not pick the accounts up**: `Loading world done` reports only what the seeders just created, `Accounts.Count` is 0, and `AccountPrompt.Initialize` blocks on `ConsoleInputHandler.ReadLine()` at "Do you want to create the owner account now?" The listener never opens / **every `-Fresh` run ends here.** This is the September de... |
| D20 | Struck through earlier; closed. | ~~**The S3/S9 content index cannot see `[TypeAlias]` names, or secondary types nothing references.** It strips string literals before indexing, so a name that exists only inside a `[TypeAlias(...)]` looks absent; and it resolves one primary type per file, so everything else in a discarded file vanishes unless some candidate happens to reference it / **this is what produced the kilts.** S9's own appendix prints `upstream: GargishClothKilt` for three of them and then bucketed them as needing a patch, when what they needed was ordinary content work. Measured: 45 alias-only names that are ServUO t... |
| D13 | Fixed 2026-09-26 (commit 7dfe7d1); cc-P23 confirmed and added report-and-leave for off-Trammel boards plus `dryrun`. | **`NewHavenQuestBoard.Place()` searches Trammel only.** A board on any other map, `Map.Internal` included, is invisible to the search, so `Place()` builds a second one and the first keeps every quest held from it / GM-only, and no board is placed yet / one line. Folded into the Q-058 picker task |
| D40 | MOOT 2026-09-30 (Chase). | **MOOT 2026-09-30, Chase: the old live world is retired and nobody plays it. The test world becomes the base for the next live, so recovering this save is not wanted. Do not spend work on it; P11's reader fix stays in the tree as harmless.** **The live shard has served nothing since 14:16 today, and every health check we own says it is fine.** World load stopped at `***** Bad deserialize of Server.ClusterFAccountPersistence (0x40128E03) *****`, an `ArgumentOutOfRangeException: Ticks must be between DateTime.MinValue.Ticks and DateTime.MaxValue.Ticks` thrown in `IGenericReader.ReadDateTime` fro... |
| D41 | Fixed by cc-P23 (`70f01e3`); Directory is one row per guild, 17 rows. Client check on Chase's list. | **The Guild Directory lists the Artificers twice.** Found in play 2026-10-01 on the test shard, after cc-P15's board. Chase's read is that the second row is the Ter Mur guildmaster, which F-9 anticipated: "a guild can have guildmasters in more than one town" / **the directory is iterating guildmasters, not guilds.** The tab is a list of guilds a player can join, so a guild with two NPCs should be one row, not two. Today it is seventeen guilds rendered as however many NPCs exist, and F-10 (Ter Mur) will make that worse rather than better / **the obvious fix is the wrong one.** Hiding off-facet ... |
| D42 | Fixed by cc-P23 (`70f01e3`); return clamped to `cost - 1`. Deviation D-98. | **The Smith Guild salvage bag returns more ingots than the item cost, above Mining about 143.** Ours deliberately drops pinned's Mining clamp of 100 (`customizations\SmithGuildSalvageBag.cs:139-148`, comment "use raw skill (no 100-cap) to reward extended Mining"; pinned clamps at `Items/Containers/SalvageBag.cs:94-98`). The return is `((4 + mining) * amount - 4) * 0.0068`, which crosses the input at mining about 143 and at 300 gives back 51 ingots for a 25-ingot item. Verified by the overseer 2026-10-01 against both files and by hand / **live ingot dupe.** The individual cap is 300 today and M... |
| D43 | Fixed by cc-P23 (`70f01e3`); power scroll tab removed. Refund census (`[SmithSealScrollCensus`) is Chase's call. | **The Smith Seal catalog sells Blacksmithing power scrolls whose cap is wiped at the next login.** The catalog sells +5 to +20 scrolls for 750 to 10,000 seals (`customizations\SmithSealCatalogGump.cs:104-107`); `PowerScroll.Use` raises the skill cap, then `ClusterFSkillCaps.Apply` writes the flat 300 back over every skill's `CapFixedPoint` on login or world load (`customizations\ClusterFSkillCaps.cs:107-124`, unconditional loop). Verified by the overseer 2026-10-01 / **live: players pay up to 10,000 seals and keep nothing.** No error is shown, so it reads as working until they relog / cc-P20 s... |

## 3. ServUO behavior copied on purpose, do not "fix" these

Every one of these reads like a typo and is ServUO's. They are here so the next reader does not
correct them, and so that if we ever change the rule we know what the list is.

**Unreachable branches and dead rolls**

- `ToxicSlith`'s drop switch rolls `Utility.Random(2)` over cases 0 and **2**, so the `SlithEye`
  branch never fires: a toxic slith drops a venom sac 2.5% of the time and never an eye.
- The fountain's buff branch rolls `Utility.Random(4)` over a **six**-case switch, so special
  protection and balm boost never fire (S2 D-4, the precedent for this whole section).
- `LowlandBoura.OnDeath` says `if (Controlled) return;` and then `if (!Controlled)`.
- `Race.RandomFacialHair(this)` returns an int and discards it on both emulators. It has never
  assigned facial hair to anyone.
- `GreenGoblinScout.OnThink` does not call the base, so no ML shout.

**Names and appearance**

- `PitFiend` is "a Pit fiend", capital P, and its header says it was copied from the daemon.
- The enslaved goblins' corpse is "an goblin corpse"; `PutridUndeadGuardian` is "an putrid undead
  guardian"; `SentinelSpider` is "a Sentinel spider".
- `EnslavedGreenGoblinAlchemist` is named "Green Goblin Alchemist" with no "Enslaved", and wears
  the free goblins' body 723 while its five siblings wear 334.

**Values that look wrong**

- `ClanRibbonPlagueRat` sets `Tamable = false` with a `MinTameSkill` of **−0.9**.
- `EnslavedGoblinMage` is a melee creature with 510 Int and no Magery.
- `LavaElemental`, `GargoyleShade`, the three sliths, `Gremlin`, `TrapdoorSpider`, `Skree` and
  `UndeadGuardian` set no Fame or Karma. `ForgottenServant` has no `[CorpseName]`.
- `GargoyleShade` has no Energy resistance.

**The eighteen character-creation differences found by D26's sweep are left alone on purpose.**
`notes/d26-gargoyle-kilt.md` §4 lists them: a different starting sword, a different staff, an apron
a gargoyle probably cannot wear that lands in the backpack, a branch unreachable on both sides, and
so on. D26 itself cleared the bar because the result was *visibly broken*, which is the D-4 rule at
the top of this file. The rest do not: **nobody consults a wiki about which weapon a gargoyle
swordsman starts holding**, so the misleading test does not bite, and changing them means diverging
from pinned for no player-visible gain. S13 (pinned sets no `FaceItemID`) matters only to the
Enhanced Client, which we do not ship.

**One correction to that sweep, which scoped itself to pinned as briefed.** It records
`GargishDagger` and `GargishPlateChest/Arms/Legs/Kilt` as absent and needing a port. They are absent
from **pinned** but present in **ours**, in `server/customizations/Items`. So S2, S16 and S17 are
cheaper than the note implies. S2 still has a real blocker: pinned sets the race *after*
`AddBackpack`, so a race branch there would see Human.

## 4. ServUO bugs we did fix, and why each cleared the bar

| # | What | Why it is "broken", not "missing" |
|---|---|---|
| D-10 | `GargishWarHammer` flips to `0x48C1`, not ServUO's `0x481` | `0x481` is a Prism of Light **pillar** graphic. Every other gargish weapon flips to itemID+1. ServUO's value turns a flipped war hammer into a pillar |
| D-16 | `DarkwoodCrown` flips to `0x3168`, not `0x3169` | `0x3169` is the flipped Vulture Helm. Same shape |
| D-46 | `ShameWall` sets `Visible = true` in its constructor | ServUO leaves `BaseAddon`'s `false`, so a fresh wall's teleporters are inert and **a player cannot push through it** until that wall's troll has died once (Q-046) |

## 5. ModernUO upstream

| # | What | Evidence | Disposition |
|---|---|---|---|
| **E1** | **`SetPassword` stores an unverifiable hash under SHA1/SHA2.** `_passwordAlgorithm` is still the enum default at the first `SetPassword`, so the phrase choice and the stamped algorithm disagree and `CheckPassword` can never match. With auto-account-creation on, a new player logs in once and never again | proven three ways in P1: the stored hash was exactly `SHA512("p1testpass")`, a packet capture confirmed correct credentials, and rewriting the hash to `SHA512("p1adminp1testpass")` fixed login immediately | **report upstream.** Costs us nothing now; the SHA2 block is reverted |
| **E3** | **A held ML quest is saved against its giver's serial only**, with no type (`MLQuestEntry.cs:520`, and upstream's own TODO at `:536` says "Serialize quester TYPE too"). `Deserialize` drops the instance if that serial is gone. **So deleting a quest giver silently removes that quest from every player's log at the next restart**, even though a replacement giver takes the quests over while the server keeps running | read from pinned source in `notes/new-haven-quest-board.md` §4.4; not probed across a restart | **report upstream.** Live hazard for us in two places: never `[remove` the New Haven board, and the New Haven seeder's `replace` mode for the 26 trainers has the same effect. `NewHavenQuestBoard.Place()` moves a board and never replaces one, for this reason |
| **E4** | **`CharacterCreation.AddPants` dresses a gargoyle in cloth legs where ServUO dresses it in a cloth kilt**, so a professionless gargoyle spawns with its pelvis bare. The port substituted `GargishClothLegs` for `GargishClothKilt` in the one branch; the profession branches all equip a kilt correctly (`:539`, `:576`, `:612`, `:649`, `:689`) | pinned `Engines/Character Creation/CharacterCreation.cs:787-809` against ServUO pub57 `Scripts/Misc/CharacterCreation.cs:103-142`, read side by side 2026-09-27. `GargishClothKiltType1` carries `[TypeAlias("Server.Items.GargishClothKiltArmor")]`, ServUO's exact type name, so the porter knew the mapping. Observed in a client | **fixed locally 2026-09-27 (D26); still to report upstream.** A transcription slip, one line, no save impact: the change affects newly created characters only and the two items carry identical stats |
| **E2** | ModernUO has **no armour set-bonus system**. Standard OSI content. We built it in 387 lines plus three small patches | S1, five passing tests, 111 files unblocked | **contribute upstream.** If taken, our maintenance on the highest-value thing we have built drops to zero |

---

## Keeping this file honest

- A defect found during a task goes in that task's `notes/` file first, with what proved it. It is
  promoted here in review.
- **When a fix lands, update its row the same day, even if the fix was incidental.** Two rows outlived
  their own fixes by three days in September 2026 and cost a re-brief. §1b.
- **A fix is not a fix until a test has been watched go red without it.** `AGENTS.md` requires the
  red proof and this file assumes it.
- Anything in §3 that a player actually complains about moves to §1 with their complaint attached.
  The rule in the banner is a default, not a verdict.
