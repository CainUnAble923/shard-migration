# cc-P23: live defect sweep (D42, D43, D41, D13)

Written 2026-10-01 by Claude (cc-P23). Brief: `D:\UO\cc-prompts\cc-P23-live-defect-sweep.md`.
Work is in `D:\ShatteredLegacy` (HEAD f49e693, clean before I started), uncommitted. Pinned ModernUO is
`D:\UO\ModernUO-pinned` at 7c9215d97; pinned paths below are relative to its `Projects\`. "Ours" paths
are relative to `D:\ShatteredLegacy\server\`. Line numbers are after this change unless marked HEAD.

## Headlines

- **D42 fixed: the salvage bag can no longer return as much as an item cost.** The skill still scales
  past 100; the *result* is clamped to `cost - 1`. A 25-ingot item gives 17 at Mining 100 and 24 from
  Mining 143 up (it gave 51 at 300). The worst case was not the plate chest: the **Dragon Barding Deed
  (750 ingots) returned 1,550 at Mining 300, a net 800 ingots per deed.** Capped at 749 now.
- **D43 fixed: the power scroll tab is gone from the Smith Seal catalog**, with a seam for F-12's level
  scrolls. Nothing was refunded. A read-only admin command, `[SmithSealScrollCensus`, counts every
  Blacksmithing power scroll by where it sits and the accounts holding seals, for Chase's refund call.
  **I have not run it on the live world** (out of bounds for me); the numbers are Chase's to get.
- **D41 fixed: the Guild Directory is one row per registered guild.** It renders 17 rows, not 18, on every
  world. "Show me the way" picks the guildmaster when it is pressed (nearest on your own map, else one on
  another map) and names the town. The brief's diagnosis was slightly off: the directory did not iterate
  NPCs found in the world, it iterated a static table of posts (`GuildLocations.All`). So the row count
  never depended on the world; it was 18 everywhere.
- **D13 was already fixed** on 2026-09-26 (commit 7dfe7d1): `Place()` has searched `World.Items`, every
  map, `Map.Internal` and containers, since then. `docs\bug-list.md:51` still lists it as open. The open
  question was what to do with a board found *off* Trammel. It used to be moved home silently. Now it is
  **reported and left alone unless the command is run with `move`**, and the command gained a `dryrun`.
- **Item 5: yes, the League Registrar shows the guild list.** Both of its guild buttons open the same
  `GuildProgressGump` as `[guild` and the board, so the D41 fix applies there too and the two cannot drift.
- **Builds:** red 338/347 with exactly the expected 9 failing; green **347/347**, image
  `sl-modernuo:cc-p23` (23f5e25e3962); mutation run 340/347 with exactly the expected 7 failing. Every new
  test except one fixture check was watched failing. `sl-modernuo:latest` (33aef6969ccb) not touched.
- **No numbering collision for P23.** `cc-prompts` holds P22, P23 and P24 (the renumbered New Haven
  dungeon brief); nothing else in `notes\` or `docs\` claims P23.

---

## 1. D42: the salvage bag ingot dupe

### Facts, re-read

- Pinned `UOContent/Items/Containers/SalvageBag.cs:94-98` clamps Mining to 100, then
  `amount = ((4 + mining) * craftResource.Amount - 4) * 0.0068`, floor 2 (`:100-108`).
- Ours at HEAD, `customizations\SmithGuildSalvageBag.cs:139-148`, copied it without the clamp ("use raw
  skill (no 100-cap) to reward extended Mining"), reading `from.Skills.Mining.Value`, which includes item
  bonuses. `Skill.Base` is not clamped by `Cap` (`Server/Skills.cs:173-194`), so Value really can be 300+.
- The overseer's arithmetic holds. For a 25-ingot item: Mining 100 gives floor(2596 x 0.0068) = 17;
  Mining 143.0 gives 24; Mining 143.3 gives 25 (equal to the cost); Mining 149.3 gives 26 (a profit);
  Mining 300 gives floor(7596 x 0.0068) = **51**, Mining 400 gives 68. The break-even barely depends on
  the cost, because it is where `(4 + m) x 0.0068` reaches 1, about Mining 143. The red run caught a
  3-ingot item at Mining 144.4 returning 3.
- **The barding deed is the biggest case.** The bag resmelts a `DragonBardingDeed` as iron
  (`SmithGuildSalvageBag.cs:239-243` HEAD), always counted as player-made, and its recipe is 750 iron
  ingots (pinned `Engines/Craft/DefBlacksmithy.cs:207`). At Mining 300 the old code returned 1,550.

### The shape, and where I land on it

I agree with the brief's shape: `min(raw, cost - 1)`, floor 2. The break-even question disappears,
because nothing can reach the cost. 17 of 25 at Mining 100 (pinned's own answer), rising to 24 of 25 at
143 and above, is a real reward for extended Mining and never a gain.

**Where the floor and the cap collide (fact 3).** For a 2-ingot item, `cost - 1` is 1 and pinned's floor
is 2. I let **the floor win: it returns 2**, its cost and never more. That is exactly what pinned returns
at every Mining, so extended Mining creates nothing there, and there is no profit, only break-even. It
is also moot today: no blacksmith recipe the bag can see costs 2. The costs are 3, 5, 6, 8, 9, 10, 12, 14,
15, 16, 18, 20, 24, 25, 28, 36 and 750 (logged by the test from the live `DefBlacksmithy` table with our
registrations).

### Changed

- `customizations\SmithGuildSalvageBag.cs`: the return is now `public static int IngotReturn(item,
  mining, cost)` (`:123`) with the clamp and a comment saying why, and `TryResmelt` calls it (`:163`).
  `TryResmelt` went from private to `internal` (`:141`) so a test can run the real salvage path; pinned
  UOContent already grants `InternalsVisibleTo` to UOContent.Tests (`UOContent/UOContent.csproj:57-59`).
  No saved field changed.
- `tests\Items\SalvageBagIngotReturnVerification.cs`, new.

### Tests

| test | what | red how |
|---|---|---|
| `AtMining100ATwentyFiveIngotItemReturnsFewerThan25` | brief 1, real PlateChest through `TryResmelt`: 17 | mutation (return cost - 1): got 24 |
| `AtMining300ATwentyFiveIngotItemReturnsAtMost24` | brief 2, the regression test | red run: "returned 51 ingots for a 25-ingot item" |
| `AtMining300ATwoIngotItemReturnsPinnedsMinimumAndNeverMoreThanItsCost` | brief 3 | red run: 4; mutation: 1 |
| `AnItemNotPlayerMadeReturnsTheFlatTwo` | brief 4 | mutation: 24 |
| `NoMiningValueReturnsAsMuchAsTheItemCost` | every recipe cost, Mining 0 to 400 by 0.1 | red run: cost 3 at Mining 144.4 returned 3 |
| `TheTestItemCostsTwentyFiveIngots` | fixture check (PlateChest is 25) | **never watched red**; it guards the others' premise |

### Other places that drop a pinned clamp (listed, not changed)

A read-only sweep (a sub-agent, 791 customization files, all 32 patches, the five replacement files
diffed against pinned) found **no other place that returns more than goes in**. I re-read the two that
matter myself; the rest are the sub-agent's reading, cited, not re-checked by me.

- **Re-checked: `patches\PlayerMobile-individual-stat-cap.patch`** replaces pinned's
  `Math.Min(base.Str/Int/Dex, 150)` (`UOContent/Mobiles/PlayerMobile.cs:594, :609, :624`) with
  `ClusterFStatCaps.IndividualStatCap`, default 500 (`customizations\ClusterFStatCaps.cs:10, :103`).
  Not a dupe, but stat-driven formulas downstream are uncapped (Str damage bonus, mana regen). **This
  contradicts `f12-levels-loops-caps.md`**, which calls `DefaultIndividualStatCap = 500` "dead config":
  it is live, as the read-side clamp on every player's Str, Int and Dex. F-12's stat work should know.
- **Re-checked: `customizations\ClusterFSmithBODSystem.cs:95`** copies pinned's large-BOD roll
  `(skill - 40) / 300` (`UOContent/Mobiles/Vendors/NPC/Blacksmith.cs:96`), which pinned bounded only by
  Blacksmithy stopping at 120 (26.7 percent). At 300 it is 86.7 percent. Not a dupe; the sub-agent notes a
  usability effect when the large slot is full. At F-12's 200 cap it is 53 percent.
- Sub-agent: `customizations\Meditation.cs:92` uses the skill's own cap as `maxSkill` (pinned
  `Skills/Meditation.cs:80` uses 100). Skill gain only; F-12 relies on this pattern on purpose.
- Sub-agent: `customizations\ClusterFSmithCommissions.cs:465, :512`, exceptional chance
  `(skill - 40) / 100`, reaches 100 percent at 140 and stops. Our own formula, bounded.
- Sub-agent: `customizations\RegenRates.cs:158-164`, armoured meditation above 200, never above the
  unarmoured value. Bounded.
- Sub-agent, false positives: the "no 120 cap" comments at `ClusterFSmithBODSystem.cs:374-389` and
  `ClusterFSmithCommissions.cs:781-796` set only the gain window for `CheckSkill` on turn-in; rewards
  come from material tier, not skill.
- Sub-agent, side note: `Items\Artifacts\Consumables\InfusedAlchemistsGem.cs:28` adds 1 to Alchemy Base
  directly, which can pass the skill's cap because `Skill.Base` clamps only to 0-65535.

### Register

- **D42 deviation:** OSI clamps Mining at 100 in the salvage bag's return (pinned `SalvageBag.cs:94-98`).
  The Smith Guild bag scales with Mining past 100 but never returns more than `cost - 1` (floor 2). Why:
  to reward extended Mining without a dupe. (The bag itself is our content; vanilla `SalvageBag` is
  untouched.)

---

## 2. D43: the Smith Seal catalog's power scrolls

### Facts, re-read

- `customizations\SmithSealCatalogGump.cs:99-108` (HEAD) sold `PowerScroll(SkillName.Blacksmith, 305 |
  310 | 315 | 320)` for 750, 2,000, 4,500 and 10,000 seals.
- Pinned `UOContent/Items/Special/Special Scrolls/PowerScroll.cs:272` `Use` sets
  `from.Skills[Skill].Cap = Value`. `CanUse` refuses when `skill.Cap >= Value` (`:252`), so with every
  cap at 300 a 305 scroll is usable.
- `customizations\ClusterFSkillCaps.cs:107-124` (HEAD) `Apply` writes the flat cap over every skill,
  unconditionally, and runs on `WorldLoad` (`:25`) and on login (`:31-37`). So the scroll lasts until the
  next login or world load. Confirmed.
- **Side finding:** by the same `CanUse` test, **every stock power scroll (105 to 120) is unusable on this
  shard**, because every cap is already 300. The player gets "Your skill is too high for this power
  scroll". Not changed; F-12 repoints scrolls at level anyway.

### What I chose: remove the tab, not hide it behind a flag

A disabled flag keeps four rows priced for caps of 305 to 320, numbers F-12's ceiling of 200 makes
meaningless, and keeps a sale path for an item the next login destroys one flag-flip away. F-12's level
scrolls will be different items with different prices and a +25 step, so none of the old rows would
survive into them. So the rows and the enum member are deleted, and the seam is a comment at the enum
(`SmithSealCatalogGump.cs:35-43`): add `LevelScrolls`, its label and its rows in the same position. The
sidebar already read its range from `CatLabels.Length`; `OnResponse` now does too (`:192`), where it used
to hard-code `<= 5`. That hard-coded 5 is what would have dangled.

### The census command

`customizations\SmithSealScrollCensus.cs`, new: `[SmithSealScrollCensus`, Administrator, declared
`CommandCategory.Diagnostic`. **It changes nothing, so there is no dry run to declare**: the command is
itself the dry run, and there is no refund command. It reports:

- every Blacksmithing `PowerScroll` in `World.Items` (pinned `Server/World/World.cs:86`), split by
  value (305 and up came only from the catalog; 120 and below is stock) and by place: player backpack
  (worn or carried at any depth), player bank, another mobile (a vendor, a pet), a container in the world,
  loose on a map, `Map.Internal`, each with serial, value and owner;
- characters whose Blacksmithing cap is above their other caps right now. That means a scroll used since
  the last `Apply`; the next login undoes it. Detected without knowing the configured cap;
- accounts and characters holding Smithing Seals, and the total.

It prints everything to the server console and the first 40 lines in game. To read seals across every
account I added two read-only views: `ClusterFAccountData.AllGuildData` (`ClusterFAccountData.cs:137`)
and `ClusterFAccountPersistence.All` (`:703`). **No saved field changed, so no version bump**; the
serializer is untouched.

The command for Chase, live or test, from an Administrator character:

    [SmithSealScrollCensus

### Changed

- `customizations\SmithSealCatalogGump.cs`: tab, rows and enum member removed; seam comment; category
  range from `CatLabels.Length`.
- `customizations\ClusterFSkillCaps.cs`: a comment above the loop in `Apply` (`:118-121`) and nothing else.
  The cap value is unchanged.
- `customizations\SmithSealScrollCensus.cs`, new.
- `customizations\ClusterFAccountData.cs`: the two read-only properties above.
- `tests\Misc\SmithSealCatalogVerification.cs`, new.

### Tests

| test | what | red how |
|---|---|---|
| `TheCatalogOffersNoPowerScrollAndLeavesNoButtonDangling` | brief 1. Every rendered category has no "Power Scroll" label; ids 0-300 pressed on every category with 100,000 seals hand over no Blacksmithing scroll (counted world-wide) and throw nothing; ids past the sidebar's range ignored | red run: the "Power Scrolls" tab label |
| `TheCensusCountsASeededWorld` | brief 2. 7 seeded Blacksmithing scrolls (6 catalog, 1 stock) in every place but "other mobile", plus a Tailoring scroll that must not count; seals on 3 characters of 2 accounts (801 in all); one raised cap. Asserted as deltas, so leftovers from other tests cannot skew it | mutation (bank read as backpack): failed |

---

## 3. D41: the Guild Directory listed the Artificers twice

### Facts, re-read

- The directory (`GuildProgressGump`, `customizations\ClusterFGuildSystem.cs`) drew one row per entry of
  `GuildLocations.All` (`customizations\ClusterFGuildStarterPath.cs:204-224` HEAD). That table has
  **18 entries for 17 guilds**: the Artificers' Order has a post in the New Haven Magery School and one
  in the Royal City of Ter Mur. So the duplicate was the Ter Mur post, as Chase read it.
- **The brief says the directory iterated guildmasters found in the world. It did not.** It iterated a
  static table. NPCs only changed the status column ("Guildmaster missing"). So the row count was
  **18 on a fresh world and 18 on the test world**, whatever NPCs existed. **After the change it is 17
  on both.** These counts are from the code, not from a running shard: the rows do not read the world.
  The test shows it by rendering with no guildmasters placed and with two of every one.
- **The authority on what guilds exist** is `ClusterFGuildSystem._byKey` (`ClusterFGuildSystem.cs:85`),
  exposed as `AllGuilds` (`:88`) and filled by `EnsureRegistered` (`:100`) with 17 `Register` calls:
  smithing, arcane, tailoring, tinkers, healers, bards, thieves, warriors, mining, rangers, maritime,
  merchants, foresters, artificers, custodians, dojo, keepers. I counted 17 `Register(new GuildDef(`
  lines, and the test asserts `AllGuilds.Count == 17`.

### Changed

- `ClusterFGuildSystem.cs`: `GuildProgressGump.Guilds()` (`:721`) is the row list, one per registered
  guild, in F-9's order (each guild's first post in `GuildLocations.All`; a guild with no post still gets
  a row, last, by key). Buttons `100 + i`, `200 + i` and `300 + i` index that list. The hall column
  shows the hall for a one-post guild and the towns for a guild with several ("New Haven, Ter Mur").
  The status column reads "Guildmaster missing" only when no post has its guildmaster.
- `ClusterFGuildStarterPath.cs`: `GuildLocation` gained `Town` (`:159`), a new constructor argument set
  on all 18 rows. The Ter Mur post's hall text went from "Royal City, Ter Mur" to "Royal City", town
  "Ter Mur". `GuildLocation` is not saved; this is display text only.
  `ShowTheWay(pm, string guildKey)` (`:594`) picks at click time: the nearest found guildmaster
  (Chebyshev distance, as `GuildLocation.FindNear` uses) on the player's own map. Otherwise the first
  found on another map, named with hall, town and facet, no arrow (an arrow cannot cross facets).
  Otherwise every post is reported missing, in P15's words: "The X's guildmaster is not at <hall> in
  <town> (x, y, map). Please tell a Game Master.", joined with "or" for several posts. The per-post
  `ShowTheWay(pm, GuildLocation)` stays, because three existing tests and the mine camp use it; its
  messages now name the town too.
- Not done, as the brief warned: hiding off-facet guildmasters.
- `tests\Misc\GuildDirectoryRowsVerification.cs`, new. It reads the gump as built (its `Entries`) and
  presses its own buttons through `OnResponse`.

### Tests

| test | what | red how |
|---|---|---|
| `AGuildWithTwoGuildmastersIsOneRow` | brief 1. Two Artificers' guildmasters on Trammel, one row | red run: 2 rows |
| `SeventeenGuildsAreSeventeenRowsWhateverTheNpcCount` | brief 2. 17 rows with 0 guildmasters placed and with 2 of every one; names equal `AllGuilds`; distinct buttons | red run: 18; mutation (hide rows with no NPC, the "obvious" fix): failed |
| `ShowMeTheWayFromTrammelPrefersATrammelGuildmasterAndNamesTheTown` | brief 3. From Trammel with guildmasters in both towns, the arrow targets the Trammel one and the message says "in New Haven"; Trammel's deleted, the message says "in Ter Mur" and "cannot cross facets", no arrow | red run: 2 rows |
| `AGuildWithNoGuildmasterRendersAndSaysSoWithoutAnArrow` | brief 4. Warriors with its guildmaster deleted: row present, status "Guildmaster missing", press gives P15's wording and no arrow | mutation (hide rows): failed |

Ter Mur is loaded in the test host (logged "Ter Mur is loaded in this host"), so the cross-facet branch ran.

---

## 4. D13: `NewHavenQuestBoard.Place()`

### Facts, re-read

- **Already fixed before this task.** `Place()` (`customizations\Engines\ML Quests\Items\NewHavenQuestBoard.cs:374`)
  has enumerated `World.Items.Values` since commit 7dfe7d1, 2026-09-26 ("Place() searches every map").
  `World.Items` is pinned's dictionary of every item by serial (`Server/World/World.cs:86`), whatever
  its map or parent, so it covers `Map.Internal` and items inside containers. No helper was assumed;
  that is the enumeration. A test for the `Map.Internal` case already existed.
- **`docs\bug-list.md:51` still lists D13 as open** ("searches Trammel only"). It is stale.
- What was left: an off-Trammel board was **moved home silently**.

### Decision: refuse and report, move only when told

For a board on Trammel away from its tile, `Place()` still moves it home; that is the command's stated
job and nothing about it is ambiguous. For a board on another facet, on `Map.Internal` or in a
container, it now **reports the board's serial and where it is, and moves nothing** unless run as
`[PlaceNewHavenQuestBoard move`. My reasoning:

- Somebody put it there: staff, a script, an `[Internalize`. Moving it silently could undo a deliberate
  placement, for example a board being kept off the map on purpose.
- Refusing costs players nothing. Held quests are saved against the board's serial, not its location
  (the file header's point 3), so the quests are safe wherever the board stands.
- Moving is still one command away, with the serial in hand, and the report says which.
- It never builds a second board in either case. That was the hazard.

The command now takes `[dryrun|move]` and declares `DryRun = "dryrun"` where it declared `NoDryRun`.
`Rerun = Skips` still holds. I left `Shard = Unverified` as it was. Nothing deletes a board, and
deduplication stays Chase's call: with more than one board, every run says "More than one board
exists; the others were left where they are."

For Chase, on any world:

    [PlaceNewHavenQuestBoard dryrun
    [PlaceNewHavenQuestBoard
    [PlaceNewHavenQuestBoard move      (only if the first said a board is off Trammel and you want it home)

### Tests (`tests\Engines\MLQuests\NewHavenQuestBoardVerification.cs`)

| test | what | red how |
|---|---|---|
| `PlaceFindsABoardOnAnyMapAndRefusesToMoveOneOffTrammelUnlessTold` | replaces the old "moves it" fact. A board on `Map.Internal` is found and reported with its serial, not moved; the dry run of `move` changes nothing; `move` brings the same board home; a Felucca second board is reported and left; Felucca alone is refused, not duplicated (brief 2) | red run: "moved to", not "not moved" |
| `PlaceWithABoardOnTrammelMakesNoSecondBoard` | brief 1, board on Trammel off its tile: moved, one board | mutation (Trammel boards off the tile made invisible): failed |
| `PlaceRunTwiceFromCleanMakesExactlyOneBoard` | brief 3, plus a dry run from clean places nothing | red run: no "Dry run" |

For the red run, `Place` took the new arguments and ignored them, so its behaviour was today's.

---

## 5. Does the League Registrar show the guild list?

**Yes.** `customizations\LeagueRegistrarGump.cs:232-235` ("Guilds Overview") and `:254-255` ("Guild
Referrals", then "Open the Guild Directory") both construct `GuildProgressGump`, the same class `[guild`
and the board open, so they render the D41 rows by construction. Chase to confirm in the client.

---

## Builds

All through `docker\uo\build.sh`, tag `sl-modernuo:cc-p23`. Logs were in the session scratchpad and not
kept in the repo.

1. **Red** (`--tests-only`, tests with today's behaviour): the first attempt did not compile, because of
   my test (`FindItemsByType` is not an `IEnumerable`; fixed with `GetAmount`). Second attempt: 347
   tests, 338 passed, **9 failed, exactly the 9 expected**, each for the reason in the tables above.
2. **Green** (full): **347/347**, image `sl-modernuo:cc-p23` 23f5e25e3962.
3. **Mutation** (`--tests-only`, four deliberate breaks: salvage returns `cost - 1`; census reads bank as
   backpack; the directory hides rows with no guildmaster; Trammel boards off the tile made invisible
   to `Place`): 340 passed, **7 failed, exactly the 7 expected**. The four files were then restored
   byte-identical (`cmp`) to the green build's copies.
4. **Final** `--tests-only` on the restored tree: **347/347**.

The serialization rule did not trigger: no saved type gained, lost or changed a field.

---

## Left for Chase to decide

1. **Refunds for D43.** Run `[SmithSealScrollCensus` on live. It lists every catalog scroll and where it
   is, and who has a Blacksmithing cap raised right now. A used scroll leaves no trace once the buyer
   relogs, so seals spent on scrolls already used cannot be counted from the world. If refunds matter,
   that needs a purchase log, and none exists.
2. **`docs\bug-list.md` D13** is stale (fixed 2026-09-26); D41, D42 and D43 can move to fixed after your
   client checks.
3. **Stock power scrolls (105-120) cannot be used on this shard at all** while every cap is 300. F-12
   changes what they do; until then they are dead drops.
4. **`ClusterFStatCaps`' 500 is live, not dead config** (section 1). F-12's stat ceilings need to account
   for the patch that reads it.
5. Smithing Seals per salvage are unchanged. Crafting an iron item and salvaging it now always costs at
   least one ingot, so seals cost metal, as at Mining 100 in pinned. Mentioned only because the seal
   economy changed shape with D42.

## Checklist for Chase

- [ ] Commit with `D:\UO\Commit-ShardWork.ps1`.
- [ ] Salvage a 25-ingot player-made item (a plate tunic) at high Mining: the return is less than 25
      (24 from Mining 143 up).
- [ ] Open the Smith Seal catalog: no Power Scrolls tab, four categories.
- [ ] Open the board's Guild Directory: the Artificers' Order appears once (hall column "New Haven, Ter
      Mur"), 17 rows in all. Press "Show me the way" on it from New Haven: the arrow, and "in New Haven".
- [ ] Open the League Registrar's Guild Referrals: the same 17 rows.
- [ ] Run `[PlaceNewHavenQuestBoard dryrun`, then `[PlaceNewHavenQuestBoard` twice: one board.
- [ ] Run `[SmithSealScrollCensus` on live and decide on refunds.
