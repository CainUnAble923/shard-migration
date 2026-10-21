# cc-P229: the League reward shop and AP-gated titles (F-13)

Copper Golem, 2026-10-21. Server only. Branch `golem/Copper/P229` in both repos. Image `sl-modernuo:cc-P229`.

## Headlines

- **The League Shop exists.** AP opens a row and never closes it; Renown pays. It is stocked with F-13's approved starter
  table, all 14 rows (0 to 1,750 AP), at F-13's prices. Two doors open it: the League Registrar's menu ("League Shop") and a
  new button in the achievements window's footer.
- **`SpendRenown` finally has a caller.** A purchase takes exactly the price from the Renown balance. LifetimeRenown, and so
  League rank, does not move (proved by a test, fact 4).
- **League titles.** Three are bought in the shop; five more unlock free at 100 / 250 / 500 / 1,000 / 1,750 AP and stay
  unlocked even if AP later drops. A title picker (from the shop, the Registrar and the achievements window) sets the one
  shown after the character's name, through pinned's `Mobile.Title`: no core edit.
- **Account data v21.** Titles are stored per account in a new versioned `LeagueTitleRecord` (each character's shown title
  is kept inside it by serial). A v20 save loads with no titles.
- **The System's loot boxes use P79's `LootBox` item, not P79's roll** (see Deviations): the box is bound, opens in a guarded
  town or house with P79's reveal and fanfare, but holds only League goods from rows its own AP opens. No placeholder row
  was needed.
- **Tests:** 12 new facts in `server/tests/Misc/LeagueShopVerification.cs`, each seen failing first. The full suite is
  green through `docker/uo/build.sh`: 1,883 tests, 1,879 passed, 0 failed, 4 skipped, and the `sl-modernuo:cc-P229` image
  was built (run 3, 2026-10-21; the first full run's five failures were fixed, see "Full suite" below).

## What changed

ShatteredLegacy repo:

| File | What |
|---|---|
| `server/customizations/LeagueShop/LeagueShop.cs` (new) | `LeagueShop`: the stock table `:92` (14 rows), `Check`, `Purchase` `:155` (re-checks everything, items all or none, then `SpendRenown`), the League hues `:84-86`, the League rune `:228`, the loot box pool `:265` and `MakeBox` `:293`. `LeagueTitles` `:315`: the nine titles, `Sync` `:343` (AP titles, never removed), `Choose` `:365` (sets `pm.Title`), `OnLogin` `:395` (puts the account's choice back on the character). |
| `server/customizations/LeagueShop/LeagueShopGumps.cs` (new) | `LeagueShopGump` `:22` (the store window, Clean Up's frame and row layout), `LeagueShopConfirmGump` `:151` (the confirm step, a cc-P169 `RequirementList` and `DrawFooter`), `LeagueTitleGump` `:218` (the picker). |
| `server/customizations/LeagueShop/LeagueShopItems.cs` (new) | `LeagueTabard` `:20`, `LeagueCloak` `:39`, `LeagueRegaliaRobe/Cloak/Sandals` `:50-73`, `LeagueBanner` `:85`, `LeagueTrophyStatuette` `:99` (engraved with the buyer's name and AP), `LeaguePigment` `:139`. |
| `server/customizations/ClusterFAccountData.cs` | `LeagueTitles` property `:222`; v21 read `:458-459`; `CurrentVersion = 21` `:494`; v21 write at the end of `Serialize`; `LeagueTitleRecord` class `:1277` (own `CurrentVersion = 0`, refuses an unknown version). |
| `server/customizations/ClusterFAchievements.cs` | `TryGrant` calls `LeagueTitles.Sync` after adding AP `:1218`; the achievements gump's footer gets "League Shop" and "Titles" (`BtnLeagueShop`/`BtnTitles` `:1842-1843`, drawn `:1989-1992`, handled `:2255-2265`). |
| `server/customizations/LeagueRegistrarGump.cs` | `BtnShop = 27`, `BtnTitles = 28` `:43-44`; "League Shop" on the Achievements row's right `:134`, "Titles" on the Guilds Overview row's right `:136`; handled `:405-411`. |
| `server/tests/Misc/LeagueShopVerification.cs` (new) | 12 facts, below. |
| `server/tests/Misc/AccountDataSerializerVerification.cs`, `RequisitionsVerification.cs` | The version bump, as cc-P150 did it for v20: three "written again it is the current version" asserts 20 -> 21, and the Requisitions fact's hand-built v19 save now also trims the v21 title record (12 bytes when empty). |
| `CHANGELOG.md`, `VERSION` | New section 2026.10.21.3 (Added, Staff); VERSION bumped from 2026.10.21.2 (that section was already committed). |

### Part 1: the currencies, re-verified on the current tree

The P75 cites had moved. Found today: `GrantRenown` `ClusterFAccountData.cs:629` (feeds `LifetimeRenown` unless the source
is Commission), `SpendRenown` `:642` (balance only), `RenownSource` `:651`. AP is added in `ClusterFAchievements.cs:1216`
(`TryGrant`). League rank is stored per character (`ClusterFLeagueRanks.GetRank`, `ClusterFLeagueRanks.cs:228`) and
promotion reads `data.LifetimeRenown` (`Evaluate`, `:295`), so a purchase can never lower either. Fact 4 checks rank,
LifetimeRenown and the promotion's Lifetime Renown line before and after two purchases.

### Part 2: the store window

Shaped like `CleanUpBritanniaRewardGump` (`Services/CleanUpBritannia/CleanUpBritanniaRewards.cs:300`, re-verified): the
same scroll frame art (0x1F40 / 0x1F42 / 0x1F43 / 0x39-0x3B / 0x2635), 40-pixel rows, five a page, Clean Up's page buttons,
its buy button art (0x837), and its grey item art (0x3E9) on a locked row. Each row shows the label, "N Renown" and its AP:
"Requires 500 AP" when locked, "250 AP" (or "Open to all") when open, "Owned" for a held title.

**cc-P169's requirement colours have merged** (`ClusterFRequirements.cs`), so I used them: the price is green when you can
pay, red when not, dim grey on a locked or owned row; the AP text is green when met, red ("Requires 500 AP") when not; a
locked row's name is dim grey. The window's own heading is dark text, not cc-P169's ice white heading, because that white is
made for the dark panels and does not read on Clean Up's parchment.

The confirm step is its own gump: the item, then a `RequirementList` (Achievement Points have / need, Renown have / need,
"Title not yet held" for a title row, an info line "Renown spent never lowers your League rank"), then cc-P169's footer with
"Buy for N Renown", live only when every line is met. Buying re-checks everything server side (`LeagueShop.Purchase`).

### Part 3: the stock, row for row

| AP | Row (F-13) | Renown | What it hands over |
|---|---|---|---|
| 0 | Title: "Registered Adventurer" | 25 | the title "the Registered Adventurer" |
| 0 | League tabard, League hue, cannot be dyed | 50 | `LeagueTabard`: pinned `Surcoat` art 0x1FFD/0x1FFE (`MiddleTorso.cs:51`); hue 1323; `Dye` refuses |
| 0 | System's Loot Box, Bronze | 40 | a P79 `LootBox` named "System's Bronze Loot Box", 1 item (see below) |
| 100 | Hair restyling deed | 75 | pinned `HairRestylingDeed` (`Items/Deeds/HairRestylingDeed.cs`) |
| 100 | League rune | 60 | pinned `RecallRune`, `LootType.Blessed`, marked at `ClusterFNewHavenSeeder.RegistrarAnchor` one tile west (she faces west), Trammel, "the League Registrar, New Haven" |
| 250 | League banner, wall decor | 150 | `LeagueBanner`: the pole banner art 0x15AE/0x15AF (pinned veteran `Banner.cs:146` uses 0x15AE-0x15F4); hue 1323 |
| 250 | League cloak, a hue sold nowhere else | 200 | `LeagueCloak`: pinned `Cloak` art 0x1515; hue 1713 |
| 250 | System's Loot Box, Silver | 150 | "System's Silver Loot Box", 2 items |
| 500 | Achievement trophy statuette | 250 | `LeagueTrophyStatuette`: art 0x2848/0x2849, tiledata "sculpture" (pinned `ManStatuetteSouthArtifact` / `EastArtifact`, `SEDecorationArtifacts.cs:373`, `:384`); shows "Awarded to <name>" and "<AP> Achievement Points" at purchase |
| 500 | League-hue pigment, one use | 300 | `LeaguePigment`: art 0xEFF, hue 1323, one use, the Clean Up pigments' checks (dyes artifacts and enhanced magic items, `BasePigmentsOfTokuno.IsValidItem`) |
| 500 | Title: "Veteran of the League" | 200 | the title "the Veteran of the League" |
| 1000 | System's Loot Box, Gold | 400 | "System's Gold Loot Box", 3 items, P79's major fanfare (tier 4) |
| 1750 | League regalia: robe, cloak and sandals | 1000 | `LeagueRegaliaRobe` (0x1F03), `LeagueRegaliaCloak` (0x1515), `LeagueRegaliaSandals` (0x170D); hue 1223 |
| 1750 | Title: "the System's Favorite" | 500 | the title "the System's Favorite" |

**The League hues** (classic-client `hues.mul`, read with the vseUOAware hue tool; searched as hex and decimal across pinned
UOContent and our `customizations` and `patches`: no hue use of any of them; all above the 1,001 a cloth dye tub reaches):

| Hue | hues.mul name | Used on |
|---|---|---|
| 1323 (0x52B) | Blues #22 | tabard, banner, pigment, League sash in the loot boxes |
| 1713 (0x6B1) | Yellows #12 | League cloak |
| 1223 (0x4C7) | Pinks #22 | regalia (robe, cloak, sandals) |

**The loot boxes.** P79's `LootBox` (`LootBoxes/LootBoxItems.cs:49`, re-verified) is used as the box: bound to the buyer's
account, opened only in a guarded town or a house where the opener is a friend, with P79's reveal gump and fanfare. Its
contents are not P79's roll (`LootBoxRoller.Roll`): they are drawn from the shop's own cosmetic, decor and convenience rows
**whose AP the box's own row needs or less** (Bronze 0 AP, Silver 250, Gold 1,000), plus P79's `BoundCosmeticSash` in the
League hue (so Bronze has two kinds: tabard or sash). Bronze 1 draw, Silver 2, Gold 3; no gold and no Renown. A line in the
System's voice comes with each purchase (`LeagueShop.BoxLines`).

### Part 4: titles

- **Shown through pinned's `Mobile.Title`** (`Server/Mobiles/Mobile.cs:1032`): `AddNameProperties` puts it after the name
  in the name property (1050045, `:3360-3371`) and the click name uses it too (`:8081`). Setting it needs no core edit.
  Nothing else in our code sets a player's `Title` (searched).
- **Stored per account** in `LeagueTitleRecord` (ClusterFAccountData v21): `Owned` (title keys, bought or AP-unlocked) and
  `Shown` (each character's shown title by serial). The record carries its own version and refuses one it does not know.
  `OnLogin` re-applies the stored choice so the record is what shows.
- **AP titles stay unlocked:** `LeagueTitles.Sync` adds every AP title the account has reached and never removes one; it
  runs when an achievement is earned (`TryGrant`), at login, and whenever the titles are read.
- The picker lists all eight: held titles can be chosen (the shown one is marked), the rest say "Requires N AP" or
  "League Shop". "No League title" clears it.

### Parts 5 and 6: guardrails and veteran rewards

Nothing in the shop has item properties; no power scrolls, artifacts, bless deeds, skill or stat items. Fact 9 creates every
row's items (and every box's contents) and checks none is gear, a power scroll, or an artifact or enhanced magic item. The
only blessed item is the League rune, which is F-13's approved row. Veteran rewards are not touched; the +1% XP per vet level
waits for F-12, as the prompt says.

## Tests

`server/tests/Misc/LeagueShopVerification.cs`, 12 facts:

1. `ABuyWithEnoughRenownAndApTakesExactlyThePrice`
2. `OneRenownShortIsRefusedAndNothingIsTaken`
3. `ApBelowTheRowIsRefusedEvenWithRenownToSpare` (also a title row)
4. `APurchaseLeavesLifetimeRenownAndLeagueRankUnchanged`
5. `ATitleRowIsBoughtOnce`
6. `ATitleUnlockedByApStaysUnlocked`, and `EarningAnAchievementUnlocksItsApTitles`
7. `ThePickedTitleShowsOnTheMobile` (one title per character, login re-applies, none clears, an unheld title is refused)
8. `TheAccountsTitlesRoundTripThroughASave` (v21 round trip, a v20 save reads with none, an unknown record version is refused)
9. `TheStockIsF13sStarterTableAndHandsOverNoMagicItem` (row for row against F-13's table; hues; tabard refuses a dye tub;
   the rune is blessed and marked; the top AP title is at most the AP all achievements give, counted from the definitions)
10. `ALootBoxHoldsOnlyRowsItsOwnApOpens` (20 boxes of each tier)
11. `TheWindowGreysLockedRowsAndTheConfirmStepListsTheRequirements` (window, confirm, both doors, the picker)

**Seen failing first.** I ran `docker/uo/build.sh -t sl-modernuo:cc-P229 --tests-only` with the implementation
deliberately broken (each break marked and then reverted from a saved copy): purchase skipped its checks and charged one
Renown extra and cut LifetimeRenown; the cloak's price was 201; the box pool ignored AP; `Sync` removed AP titles below the
AP; `Choose` did not set `Title`; the window said "Locked" instead of "Requires 500 AP"; `Serialize` left the titles out;
`TryGrant` did not call `Sync`. Result: all 12 new facts failed, each at the expected assertion (for example fact 1:
"Expected 125, Actual 124"; fact 3: "Expected NeedsAp, Actual Bought"; fact 7: "Expected the System's Favorite, Actual
null"; fact 11 at the "Requires 500 AP" line). Fact 4 failed at its Renown line (the extra Renown came first), so its
LifetimeRenown line was not reached in that run. Five existing save-format facts (four in AccountDataSerializerVerification,
one in RequisitionsVerification) also failed, as they should with titles missing from the save. Run total: 1,883 tests,
17 failed, 4 skipped.

**Full suite, real code, run 1** (`docker/uo/build.sh -t sl-modernuo:cc-P229`): 1,883 tests, 1,874 passed, **5 failed**,
4 skipped; no image built. The five, and what I did:
- `LeagueShopVerification.TheStockIsF13sStarterTableAndHandsOverNoMagicItem`: my own fact caught that the 2,500 AP title
  could not be reached (the live total is 1,955 AP). The title was removed (Deviation 2).
- `AccountDataSerializerVerification` x3 (`AVersion13...`, `AVersion14...`, `AVersion15...`) and
  `RequisitionsVerification.TheRecordSurvivesAWriteAndAReadAndAVersion19SaveLoadsWithNoBoard`: each asserts the save's
  version is the current one, 20 ("Expected 20, Actual 21"). Updated exactly as cc-P150 did for its own bump (commit
  d8c08c3): 20 -> 21, and the Requisitions fact's hand-made v19 save also trims the empty v21 title record.

**Run 2, after those fixes: not finished.** Claude Code stopped the build mid-compile (UOContent had not finished; no test
ran) because the PC was critically low on memory.

**Run 3, same code, green.** A later session (19 GB free) took the docker-build lock and ran
`docker/uo/build.sh -t sl-modernuo:cc-P229`: "Test Run Successful. Total tests: 1883, Passed: 1879, Skipped: 4", then
"Built sl-modernuo:cc-P229 with patches applied and 1879 shard test(s) passing." All 12 LeagueShop facts and the
updated save-format facts passed. Lock released. No code changed between run 2 and run 3.

## Deviations and decisions for Chase

1. **Loot boxes: P79's box, the shop's own contents.** P79's roll does not fit F-13's guardrails: it includes magic gear with
   item properties (`LootBoxRoller.MagicGear`), greater strength and agility potions, and Renown that `LootBox.Open` grants as
   `RenownSource.Achievement`, so it would count toward League rank (buying a box with Renown would raise rank). So the boxes
   use P79's `LootBox` item and draw only from F-13's kinds, and only from rows the box's own AP opens. If you want them to
   reach higher (for example a small chance of a regalia piece in Gold), that is one line in `LeagueShop.BoxInfo`.
2. **AP titles are ours.** F-13 asks for titles AP unlocks for free but names none. I used "the Noted" 100, "the
   Accomplished" 250, "the Distinguished" 500, "the Renowned" 1,000, "the Illustrious" 1,750, on the shop's own AP tiers.
   Rename or re-space them in `LeagueTitles.All`.
   **F-13's AP total is out of date.** F-13 says a player who earns everything has 2,505 AP. Counted today from the live
   definitions (fact 9, every achievement not retired): **1,955 AP**. cc-P55 Part G retired some achievements since F-13
   was written. I first had a sixth title at 2,500 AP; the count showed nobody could reach it, so I removed it. The shop's
   top row (1,750 AP) is still reachable, with 205 AP to spare; worth knowing before any tier is raised.
3. **Titles read as "Name the Title".** Pinned draws the title right after the name, so the bought titles show as "the
   Registered Adventurer" and "the Veteran of the League" (F-13 lists them without "the").
4. **The tabard is pinned's Surcoat art.** Pinned has no tabard item; tiledata's "tabard" (0xE412 static, item 0xA412) is a
   late art id that I did not want to depend on in the shipped client. The Surcoat is the classic sleeveless tabard look.
5. **Only the tabard refuses a dye tub**, as F-13 says. The cloak and regalia hues are above what a cloth dye tub reaches, so
   a player who dyes them cannot get the League hue back, but they can dye them. Say if those should refuse too.
6. **Items are not account-bound** (only the loot boxes are, as P79 binds them). F-13 does not ask for it; cosmetics can be
   traded or sold.
7. **No League registration needed to buy.** F-13's rule is AP and Renown only; the achievements window opens the shop
   anywhere, so there is no range check.
8. **One shown title per character, owned titles per account.** The prompt says "stored per account"; the owned set is
   account-wide, and each character picks its own from it.

## For Chase (in the client)

1. Talk to Elara Voss (League Registrar, New Haven). The main menu has "League Shop" on the Achievements row and "Titles" on
   the Guilds Overview row. Open the achievements window (`[achievements`): "League Shop" and "Titles" sit
   at the right of the footer.
2. In the shop: rows your AP has not reached are greyed with "Requires N AP" in red and have no button; rows you cannot
   afford show the price in red. Press an open row: the confirm window lists AP and Renown in green or red, and Buy.
3. Check the hues on the tabard (try a dye tub on it: refused), the cloak and the regalia; place the banner and the trophy in a
   house (the trophy's hover shows your name and AP); use the rune to recall to the Registrar; open a Bronze box in town.
4. Titles: with 100 AP, open Titles and pick "the Noted"; your name should read "Name the Noted" on hover. Log out and in:
   it stays. "No League title" clears it.
5. To try each tier, `[ClusterFAchievement grant` (Administrator) earns achievements, which pay AP and Renown. I found no
   staff property that sets AP or Renown directly (`LeagueLifetimeRenown` on a player sets only the lifetime figure).

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, 2026-10-21:

```
Repo Result
---- ------
code dry run
docs dry run
```

Neither repo BLOCKED. Code: the 9 files above plus `CHANGELOG.md` and `VERSION`. Docs: this note and the bot's
`testing/bot-runs/2026-10-20-2359/` (machine output).

Re-run after the green suite, 2026-10-21: same Result table (code dry run, docs dry run), neither BLOCKED.

P229 DONE
