# cc-P429: Crystal turns the 10-22 Codex review findings into fix-up prompt drafts

**Golem:** Crystal (cloud). **Date:** 2026-10-22. **Branch:** `golem/Crystal/P429` (shard-migration only; no code changed).
**Checked against:** code `main` at `da1a0cb` (P274's merge), pinned ModernUO `d4531cd`, ServUO pub57 where a port
follows it.

## In plain words

- I read the eleven Codex reviews that are in main: P400 to P404, P407, and P418 to P422. Then I checked every finding
  marked bug or risk against today's code.
  - The table has 68 rows from Codex (70 findings; two pairs in P420 and P421 are the same bug).
  - 38 are real bugs or real partly: 37 confirmed, plus P402 F01, whose other half is already queued.
  - 8 are real but may be what was meant (Chase's call). 18 are missing tests with no bug behind them.
  - 2 are blocked until F-12 is built.
  - 2 were already queued: P400 #1 in P412, and P402 F08's `_released` in P427.
  - P407 #2 is also my own P428 finding 1.
  - None was plain wrong.
- I also found two more while checking:
  - **Boss loot boxes and the rare Self Repair roll never happen.** Their death hook reads the creature after the game
    has already deleted it. P263's notes said so on 10-21, and nobody queued it.
  - **The Smith Guild Book's "abandon" skips P263's reroll cooldown**, so the cooldown can be dodged.
- Four drafts are urgent, each an exploit that pays or a loss for players:
  1. **League Register:** one repair deed repairs many items. The Field Satchel refuses the resources it is meant to
     hold, charges 50 currency for drops it then refuses, and works as free item-count storage in the bank and house.
  2. **Requisitions:** the Appraiser buys any plain exceptional weapon for about 85 gold. It costs three ingots to make,
     so this prints gold. The same system refuses every spellbook it asks for, because spellbooks are blessed.
  3. **Tutorial:** a second bonded pet through remedial training, and endless free bandages. Tutorial pests are safe
     practice dummies for anyone, and another character on the account can run the trainee's tutorial.
  4. **Smith commissions:** the reroll cooldown is skipped through the guild book.
- The rest can wait: death hooks, Music Room, Noted by the System, Eodon, the stump message, guild hall decor, and
  Artificers text.
- Nothing was built or run, because a cloud Golem cannot build the shard. Every draft asks for a red test first.
  Where a verdict needs the client or the live world, the table says so.
- I did not cover P423 (Verite, still in progress), or P424-P426 (still in the queue). P405 (ServUO research), P406
  (patch notes) and P417 (design) are not code reviews.
- I read the guides' Contradictions lists (P381-P389). They are design and history disagreements, not bugs, with two
  exceptions: P387's boss box (urgent list above, draft W1) and P383's stale Artificers gump text (draft W7).

## How the checking was done

I read every finding and the code it cites. Five read-only helper sessions each re-checked one group of notes against
`da1a0cb` and pinned ModernUO and reported a verdict with file:line. I then re-read the claims the drafts depend on
most myself:
- P418 #1, the repair target (`LeagueRepair.cs:89-112`, deed `:175`).
- P420 #3, the remedial pet (`ClusterFTutorial.cs:202` clears `StationsDone`; `:255` and `TutorialFarm.cs:186` key on
  it).
- The new guild book abandon (`SmithGuildBook.cs:649-658`, no `Abandoned` call; only `SmithCommissionGump.cs:302`
  records it).
- The boss box (pinned `Mobile.Delete` sets `Deleted` at `Mobile.cs:2503`, after `OnDelete` at `:2489`; `OnDeath`
  deletes NPCs at `:4899-4902`).
- All four P422 findings.

Verdicts: **confirmed** (the failure is real in today's code), **policy** (real, but may be intended: Chase decides),
**test gap** (only a missing test; no bug found), **queued** (already in a queued prompt), **not a bug** / **blocked**
(no current failure).

## Every finding and its verdict

C is `server/customizations/`. "Draft" names the prompt below that carries it.

| Finding | What | Verdict | Severity | Today's code | Draft |
|---|---|---|---|---|---|
| P400 #1 | Stump floats at the tree's raised Z | queued | wrong behavior | C/ClusterFLumberStumps.cs:23 | P412 |
| P400 #2 | A polearm user is told to equip an axe at a stump | confirmed | cosmetic | C/ClusterFLumberStumps.cs:121 | W5 |
| P400 #3 | No two-player last-batch test | test gap | test gap | tests/Engines/Harvest/ChoppedTreeStumpsVerification.cs:81 | W5 |
| P400 #4 | No save/reload test | test gap | test gap | same file :153 | W5 |
| P400 #5 | No mark-again-after-cleanup test | test gap | test gap | same file :115-142 | W5 |
| P401 #1 | Skill cap 200 at loops 0 and 1 | blocked (F-12 not built) | none today | C/ClusterFSkillCaps.cs:154, :176; C/Tutorial/ClusterFLoops.cs:40 is a stub on purpose | F-12 build |
| P401 #2 | `CompleteLoop` accepts any higher loop | blocked (no caller but graduation) | none today | C/Tutorial/ClusterFLoops.cs:47-62; only caller `Graduate` (:34) | F-12 build |
| P401 #3 | No ladder transaction tests | test gap (nothing to test yet) | test gap | tests/Tutorial/GraduationLoopVerification.cs:266 | F-12 build |
| P402 F01 | "Never reached you" and "bard never hit" lost on heal to full | Geography Major half queued (P427); bard half (:621) confirmed | wrong behavior, minor | C/ClusterFNotedBySystem.cs:609, :621 | P427 + W3 |
| P402 F02 | Empty-vein streak survives a successful swing elsewhere | confirmed | wrong behavior, negligible | server/patches/Mining.cs:299; C/ClusterFNotedBySystem.cs:767 | W3 |
| P402 F03 | Ground read at the departure tile, with no Z | confirmed | wrong behavior, minor | C/ClusterFNotedBySystem.cs:777-791, :815; pinned Mobile.cs:4103 vs :4386 | W3 |
| P402 F04 | Remote Work refused at exactly 15 tiles | confirmed | wrong behavior, trivial | C/ClusterFNotedBySystem.cs:626 | W3 |
| P402 F05 | A large commission never counts for Pre-Crafted | confirmed | wrong behavior | C/ClusterFSmithCommissions.cs:675-695 | U4 |
| P402 F06 | Mule Train counts off-facet or dead followers | confirmed | cosmetic | C/ClusterFNotedBySystem.cs:861 | W3 |
| P402 F07 | Recycling credits another player's fresh craft | policy (P263 lines 149-151 accept it) | exploit that pays, small | C/ClusterFNotedBySystem.cs:738-756 | Chase |
| P402 F08 | Static tables never pruned | `_released` queued (P427); the rest are keyed by player, not a bug | cosmetic | C/ClusterFNotedBySystem.cs:647 | P427 |
| P402 F09 | Per-runebook counters grow | confirmed | cosmetic (save size) | C/ClusterFNotedBySystem.cs:694; C/ClusterFAchievements.cs:473 | W3 (optional) |
| P402 F10 | Ground lookup and definition scan on every step | confirmed (unmeasured cost) | none measured | C/ClusterFNotedBySystem.cs:815; C/ClusterFAchievements.cs:1253 | W3 (optional) |
| P402 F11 | No positive tests for snow, Mule Train, final tiers | test gap | test gap | tests/Misc/NotedBySystemVerification.cs | W3 |
| P402 F12 | Hooks tested directly, not through the patches | test gap (this is how F03 got through) | test gap | same file :300, :384, :431 | W3 |
| P402 F13 | Crafted-only untested at large, tailoring, disabled | test gap | test gap | same file :704; C/LargeBODItemFill.cs:68 | W3 |
| P402 F14 | Large commission reroll has no cooldown | policy (P263 line 246 discloses it) | exploit that pays | C/SmithGuildBook.cs:684; C/ClusterFSmithCommissions.cs:570 | U4 |
| new | The guild book's small abandon skips the reroll cooldown | confirmed | exploit that pays | C/SmithGuildBook.cs:649-658 | U4 |
| P403 #1 | A failed autosave still shows "all saved" | confirmed | data loss (staff tool) | web-console/static/music.js:175-177, :193 | W2 |
| P403 #2 | Overlapping saves can land out of order | confirmed (rare race) | data loss (staff tool) | music.js:158-174; web-console/music.py:404-437 | W2 |
| P403 #3 | Save to repo does not wait for in-flight saves | confirmed | wrong behavior (staff tool) | music.js:179-191 | W2 |
| P403 #4 | An unreadable notes file is read as empty, then overwritten | confirmed | data loss (staff tool) | web-console/music.py:395-402, :425-437 | W2 |
| P403 #5 | Missing mp3 or older package: an unknown music ID | confirmed server side; the client effect needs the game PC | wrong behavior (dormant: no tracks assigned) | player-package/payload/app/Build-UoOverrides.ps1:727; C/Music/ClusterFShardMusic.cs:245, :541 | W2 |
| P403 #6 | Fight ends in a region with no music: the fight track keeps playing | confirmed server side; the client effect needs the game PC | wrong behavior (dormant) | C/Music/ClusterFShardMusic.cs:589-590 | W2 |
| P403 #7 | The Config.txt cache ignores which tracks were accepted | confirmed | wrong behavior (dormant) | Build-UoOverrides.ps1:711, :733-738 | W2 |
| P404 #1 | Pet, summon or provoked kills give no bestiary credit | confirmed | wrong behavior | C/ClusterFLeagueBestiary.cs:174 | W1 |
| P404 #2 | Stats, resists, loot not asserted | test gap | test gap | tests/Mobiles/Bestiary/LeagueBestiaryVerification.cs:~300 | W1 |
| P404 #3 | Poisons not registered in the fixture | test gap (results depend on order) | test gap | same file, constructor; no `EnsurePoisons` | W1 |
| P404 #4 | No spawn population test | test gap | test gap | same file :~352 | W1 |
| P407 #1 | Eodon entries weighted 100 instead of by MaxCount | confirmed | wrong behavior (rare tigers 3x too common) | C/Services/Expansions/Time Of Legends/EodonSpawns.cs:147 | W4 |
| P407 #2 | Hatchling: StatLossAfterTame instead of OnAfterTame | confirmed (also P428 finding 1) | wrong behavior (staff `[add` only today) | .../Mobiles/DragonTurtleHatchling.cs:65 | W4 |
| P407 #3 | Infernus fire not tested through combat and timer | test gap | test gap | tests/Services/TimeOfLegends/EodonRemainderVerification.cs:478 | W4 |
| P407 #4 | Rerun test ignores old creatures and refill | test gap | test gap | same file :~762 | W4 |
| P418 #1 | Repair target does not recheck the deed or kit | confirmed | exploit that pays | C/LeagueRegister/LeagueRepair.cs:89-112, :175, :211 | U1 |
| P418 #2 | Field Satchel refuses resources going into its satchels | confirmed | wrong behavior (feature broken) | C/LeagueRegister/LeagueConsolidation.cs:110; pinned Container.cs:274 | U1 |
| P418 #3 | A satchel with 4+ stacks hits the 4-item limit | confirmed | wrong behavior | LeagueConsolidation.cs:95, :133; pinned Container.cs:247 | U1 |
| P418 #4 | A refused drop still takes the 50 currency | confirmed | player loss | LeagueConsolidation.cs:136, :138, :150 | U1 |
| P418 #5 | A paid purchase or unbind can drop at your feet | confirmed | player loss, minor | LeagueConsolidation.cs:49-55, :75-77; C/LeagueRegister/LeagueRegister.cs:196, :206 | U1 |
| P418 #6 | The item-count discount also applies in bank and house | confirmed (small today; large once 2 and 3 are fixed) | exploit that pays (free storage) | LeagueConsolidation.cs:98-106 | U1 |
| P418 #7 | Combined turn-in skips complete deeds in bags | confirmed | wrong behavior, minor | C/LeagueRegister/LeagueRegister.cs:298 | U1 |
| P418 #8 | Blaze repair is free with no cooldown | policy (cc-P280:14, :94, :114 make it the Blaze benefit) | none if intended | LeagueRegister.cs:317-328 | Chase |
| P418 #9 | Tests miss the drop, routing and pending-target paths | test gap | test gap | tests/Misc/LeagueRegisterVerification.cs:337, :474 | U1 |
| P418 #10 | No item save/load tests; record end not asserted | test gap (the read path itself is right) | test gap | same file :420; AccountDataSerializerVerification.cs:276 | U1 |
| P419 #1 | Placing at a shifted anchor doubles the set | policy (cc-P265:315: "place twice at one point places once") | wrong behavior (staff, test shard) | C/GuildHallDecor/GuildHallDecorSeeder.cs:75-77 | W6 |
| P419 #2 | No fit or door check before placing | policy (templates are drafts, cc-P265:415) | wrong behavior (staff, test shard) | GuildHallDecorSeeder.cs:98 | W6 |
| P419 #3 | Tower "door" walls are impassable decor | policy (open: are towers entered? cc-P265:379-384) | cosmetic for now | C/GuildHallDecor/GuildHallDecorArt.cs:151, :162, :169, :182, :194 | Chase |
| P419 #4 | A rerun after a template edit keeps stale rows | confirmed | wrong behavior (staff, test shard) | GuildHallDecorSeeder.cs:75-87 | W6 |
| P419 #5 | The design test hashes the copy, not the real JSON | test gap (they agree today) | test gap | tests/Misc/GuildHallDecorVerification.cs:62 | W6 |
| P420 #1 | Another character on the account runs the active tutorial | confirmed | wrong behavior (the trainee loses its rewards to the alt) | C/Tutorial/TutorialGumps.cs:44; C/Tutorial/ClusterFTutorial.cs:124, :144, :164, :201, :218 | U3 |
| P420 #2 | The graduation pet choice can be lost for good | confirmed | wrong behavior (reward lost) | ClusterFTutorial.cs:229, :255; TutorialGumps.cs:63, :254 | U3 |
| P420 #3 = P421 #2 | Remedial training gives a second bonded pet | confirmed | exploit that pays | ClusterFTutorial.cs:202; C/Tutorial/TutorialFarm.cs:186 | U3 |
| P420 #4 = P421 #1 | Unlimited, tradeable step-3 bandages | confirmed | exploit that pays (1 gp each at healers) | TutorialFarm.cs:158-160, :225-231 | U3 |
| P420 #5 | Tutorial record edge cases untested | test gap (reader and writer match) | test gap | C/ClusterFAccountData.cs:446, :1272-1302 | U3 |
| P420 #6 | Losing Young mid-tutorial untested | test gap (no tutorial code reads Young) | test gap, low | ClusterFTutorial.cs:53-57 | none |
| P421 #3 | Reseeding with the farm door open adds a door | confirmed | wrong behavior (rare) | TutorialFarm.cs:381-392 | U3 |
| P421 #4 | The heal step passes on the skill roll, not on a heal | confirmed | wrong behavior | TutorialFarm.cs:235-241; pinned Bandage.cs:372-445 | U3 |
| P421 #5 | Pen animals are stock (meat, wool, taming) | policy (F-35 wants a pen of tamables; only pests are tutorial-only) | exploit, negligible | TutorialFarm.cs:67 | Chase |
| P421 #6 | Pests are free practice targets for outsiders | confirmed | exploit that pays (AFK weapon, Tactics and Anatomy gains) | C/Tutorial/TutorialCreature.cs:37-48; pinned BaseWeapon.cs:858, :1340 | U3 |
| P421 #7 | One species can fill the pen | policy (F-35 does not ask for one of each) | cosmetic | TutorialFarm.cs:342 | Chase |
| P421 #8 | No spawn lifecycle or save tests | test gap | test gap | tests/Tutorial/TutorialFarmVerification.cs:150 | U3 |
| P422 #1 | Blessed-item refusal blocks every requested spellbook | confirmed | wrong behavior (book requests can never be filled) | C/Requisitions/RequisitionItems.cs:316, :74-75; C/Requisitions/Appraiser.cs:125; pinned Spellbook.cs:122 | U2 |
| P422 #2 | The Appraiser buys plain exceptional weapons as magic | confirmed | exploit that pays (about 85 gp for 3 ingots, no limit) | RequisitionItems.cs:202-210, :389-395; RequisitionTable.cs:99-105; pinned BaseWeapon.cs:671-673 | U2 |
| P422 #3 | Moving the refresh hour back re-rolls today's requests | confirmed (staff setting or clock change) | wrong behavior, minor | C/Requisitions/RequisitionSystem.cs:127-129 | U2 |
| P422 #4 | A null list in requisitions.json breaks reload | confirmed (staff config) | wrong behavior (staff) | C/Requisitions/RequisitionTable.cs:440, :541 | U2 |
| new | Boss loot boxes and the rare Self Repair roll never fire | confirmed (P263 notes :258-268, the P387 guide) | wrong behavior (a whole reward never pays) | C/LootBoxes/ClusterFLootBoxes.cs:166-170; C/ClusterFRareSelfRepair.cs:42-46, :57-60 | W1 |

Every bug or risk finding of P400-P404, P407 and P418-P422 is in the table (P402 labels its fourteen F01-F14). P404's #5 and P419's #6 are nits and are
not in the table (P419 #6, the activator test that only checks order, is real and could ride W6).

## Drafts: urgent first

### U1 (urgent). League Register: repair deeds, the Field Satchel, purchases

```
# CC task P??: League Register fix-up: repair targets, Field Satchel holding and fees, safe delivery

**Model:** Opus
**Touches:** server
**Golem:** any

**Summary:** Codex's P418 review of P280 (the League Register) found a repair exploit and a Field Satchel that refuses
the resources it was built to hold. Crystal's P429 confirmed seven bugs against main da1a0cb. Fix them together; they
share files and tests.

Found by cc-P418 (Codex), checked by cc-P429 (Crystal), findings P418 #1-#7, #9, #10.

## What to do

All in server/customizations/LeagueRegister/. Pinned is ModernUO d4531cd; no shard patch touches Container.cs,
BaseHouse.cs or Mobile.AddToBackpack.

1. Repair targets (LeagueRepair.cs:89-112; deed :175, kit :211). The callback checks only the target. Today A opens a
   target, hands the deed to B, B opens one too, and both repair; banking the deed after opening the target also
   works. Pass the source item into BeginTarget. In the callback, require it not deleted, still in that player's
   backpack, and (kit) UsesRemaining > 0, before Repair and used().
2. Field Satchel CheckHold (LeagueConsolidation.cs:110). Pinned Container.cs:274 walks up the parents with the item
   being inserted. So ore, logs, hides and essences going into a guild satchel inside the Field Satchel are refused,
   and that includes the routing hooks (CompactOreSatchelRoutingHook.cs:187, ClusterFLumberjackingExtension.cs:118).
   Refuse non-satchels only on direct insertion into the Field Satchel. Let the parent walk through.
3. Its item limit (:95, :133). Pinned Container.cs:247 counts item.TotalItems + 1 against MaxItems 4, so any guild
   satchel with 4+ stacks is refused. Count satchel families (Items.Count) yourself, and keep the backpack seeing +0.
4. Fees (:136, :138, :150). Merge spends 50 before base refuses (duplicate family, the limit above, weight, a full
   parent). Move the charge after a successful insertion. No charge for moving a satchel within the Field Satchel.
5. Delivery (LeagueConsolidation.cs:49-55, :75-77; LeagueRegister.cs:196, :206). Payment, deleting the old logbooks
   and unbinding all happen before an unchecked AddToBackpack, which drops the item at the player's feet (pinned
   Mobile.cs:7594-7605). Place the new item first (PlaceInBackpack). On failure, delete it and refuse with "Make room
   in your pack", before taking anything.
6. The 0-items discount (:98-106) also applies in the bank box and in house secure storage (pinned Container.cs:247,
   BaseHouse.cs:719, :1377 read TotalItems). P280 promised one pack slot only. Keep the discount only while the satchel
   is directly in the owner's backpack, or refuse it in banks and secure containers. Once 2 and 3 are fixed this is
   about 500 stacks stored as 1 item, so do not ship 2-3 without 6.
7. Combined turn-in (LeagueRegister.cs:298) scans only top-level backpack items. Search recursively, as
   ClusterFSmithBODPayout.CanPay does (:129-130).
8. Tests (tests/Misc/LeagueRegisterVerification.cs). Write each one red first, through the real paths (OnDragDropInto,
   OnDragDrop, TryDropItem, the target callback), not Merge + DropItem:
   - The deed handed over while a target is pending: the second repair fails.
   - Ore dropped on a compact satchel inside the Field Satchel lands there.
   - A 20-stack satchel is accepted, and a fifth satchel is refused with no charge.
   - Full pack (items, and weight) on buy and unbind: nothing taken, nothing on the ground.
   - Bank TotalItems counts a populated Field Satchel's contents.
   - A nested complete deed is turned in.
   - Item save/load for the Register owner, a part-used kit, a populated Field Satchel and an upgraded pack, with the
     reader position checked (P418 #10).
9. Build and run the tests (docker\uo\build.sh -t sl-modernuo:cc-P??).
10. CHANGELOG: Fixed lines in player words (satchels accept resources again; a refused drop no longer costs currency;
    a full pack no longer drops your purchase). Do not describe the repair exploit.
11. Notes: notes\cc-P??-league-register-fixups.md. Last line `P?? DONE`.

**Not in this prompt:** Blaze repair being free with no cooldown (P418 #8) is the P280 design; Chase decides.

**Done means:** each of the seven bugs has a test that was red and is green.
```

### U2 (urgent). Requisitions: the Appraiser prints gold; spellbook requests cannot be filled

```
# CC task P??: Requisitions fix-up: Appraiser magic test, spellbook turn-ins, refresh day, config nulls

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** Codex's P422 review of Requisitions and Leads found the Appraiser paying about 85 gold for any plain
exceptional weapon, which costs three ingots to make, with no limit. It also found the blessed-item rule refusing every
spellbook that requests ask for. Crystal's P429 confirmed all four findings on main da1a0cb.

Found by cc-P422 (Codex), checked by cc-P429 (Crystal), findings P422 #1-#4.

## What to do

All in server/customizations/Requisitions/.

1. Plain crafting bonuses are not magic. Pinned BaseWeapon.OnCraft (:671-673) gives every exceptional weapon
   WeaponDamage 35. RequisitionProperties.PropertyCount (RequisitionItems.cs:202-210) counts it, so AppraiserPricing
   (:389-395) pays weapon base 25 + 25 per property + intensity, about 85 gp, for a crafted dagger. Exclude
   crafted-quality bonuses (an exceptional item's own DI, and armor's exceptional resist bonus if counted) from
   IsMagic, PropertyCount and the price, for both the Appraiser and the board. Check whether ImbueCatalogue's count
   path (:204) counts them too. Decide whether the board's "magic" requests should still accept a crafted exceptional
   item. Write that decision in the notes.
2. Spellbooks (RequisitionItems.cs:316; Appraiser.cs:125). Pinned Spellbook (:122) is blessed, so the blanket blessed
   refusal rejects the "spellbook" and "necrobook" kinds (:74-75), even the books a Lead drops. Allow ordinary
   spellbooks through one shared eligibility rule, keeping the refusal for other blessed items. Is a blessed spellbook
   sold to the Appraiser fine? Ask in the notes if unsure, and default to no.
3. Refresh day (RequisitionSystem.cs:127-129). Moving refreshHourUtc back, or a clock correction, makes DayIndex go
   backwards, and a filled set re-rolls. Keep a monotonic last-issued day; force stays explicit.
4. Config nulls (RequisitionTable.cs:440, :470, :541). "themes": null or "areas": null passes validation, is published
   as Current, and then throws. Reject null lists and rows before publishing, and keep the old table.
5. Tests, each red first:
   - A crafted exceptional dagger (through the real craft, not set attributes) is not magic and the Appraiser will not
     buy it.
   - A crafted spellbook fills a spellbook request; a Lead-dropped book turns in.
   - Refresh-hour change after filling: no new set that day.
   - A null themes reload is refused and Current is unchanged.
6. Build and run the tests (docker\uo\build.sh -t sl-modernuo:cc-P??).
7. CHANGELOG: Fixed ("Spellbook requisitions can be filled."; "The Appraiser no longer pays a magic price for plain
   exceptional crafts."). The second is player-visible; word it plainly, with no how-to.
8. Notes: notes\cc-P??-requisitions-fixups.md. Last line `P?? DONE`.

**Done means:** the four tests were red and are green, and the notes say whether the live Appraiser has already bought
crafted items (for that, the game PC: the server log or the Appraiser's gold out).
```

### U3 (urgent). Tutorial and farm: second pet, free bandages, practice dummies, the wrong character

```
# CC task P??: tutorial fix-up: one pet per account, bounded bandages, pests refuse outsiders, the recorded character

**Model:** Opus
**Touches:** server
**Golem:** any

**Summary:** Codex's P420 and P421 reviews of the tutorial framework (P80) and farm (P276) found two exploits that pay
(a second bonded pet, endless bandages) and free combat-skill practice on tutorial pests. They also found that any
character on the account can run the trainee's tutorial, and that the graduation pet can be lost. Crystal's P429
confirmed all of them on main da1a0cb.
The farm only seeds on the test shard today (TutorialFarm.cs:71, :295, clusterf.tutorialFarm.allowLive), so this
blocks turning it on live. Pests and the recruiter are wherever the tutorial is.

Found by cc-P420 and cc-P421 (Codex), checked by cc-P429 (Crystal): P420 #1-#5, P421 #1-#4, #6, #8.

## What to do

All in server/customizations/Tutorial/.

1. Pet entitlement (P420 #3 = P421 #2). The "pet taken" marker lives in StationsDone (TutorialFarm.cs:186), which
   StartRemedial clears (ClusterFTutorial.cs:202). So: farm pet, skip, remedial, then a second pet from the Farmhand
   or the graduation pick (:255). Store PetClaimed on TutorialRecord (a nested version bump with an old-version
   reader), set it in ChoosePet and the graduation pick, and read it in StepOf and :255.
2. Pending pet (P420 #2). Graduated is set before the rewards (:229), and the pick is a gump only (:255-258). Closing
   it, a disconnect or a restart loses it for good, and TutorialGumps.cs:254 promises a recruiter retry that does not
   exist. Persist PetClaimPending, clear it only when GivePet succeeds, and let the recruiter reopen the pick.
3. The recorded character (P420 #1). TutorialGumps.cs:44 and the station, skip and graduate handlers (:124, :144,
   :164, :218) check the account record, never CharacterSerial; StartRemedial (:201) even re-points it. Require
   CharacterSerial == pm.Serial (or re-point only when that character is deleted) in RunStation, CompleteStation,
   Skip, Graduate and StartRemedial. Show other characters a read-only page.
4. Bandages (P420 #4 = P421 #1; TutorialFarm.cs:158-160, :225-231). Reissue checks only the current backpack, so
   banking or trading the stack and asking again gives 10 more, sold at 1 gp each (pinned SBHealer.cs:28). Record the
   issue (a count or key on the record) and cap it, or give blessed, unsellable TutorialBandage that are deleted when
   the step ends.
5. The heal step (P421 #4; :235-241) completes on a Healing or Veterinary skill roll (pinned Bandage.cs:444-445 rolls
   skills even on a failed treatment). Add a small patch hook after a real heal in BandageContext.EndHeal (pinned
   Bandage.cs:379-422) and complete the step from it, not from SkillUsed.
6. Pests for outsiders (P421 #6; TutorialCreature.cs:37-48). The pest drops damage late. An outsider still swings and
   rolls weapon, Tactics and Anatomy checks (pinned BaseWeapon.cs:858, :1340, :2524-2527), against a target that never
   fights back or dies. Refuse the harmful action before the swing for anyone who is not a participant: a region
   AllowHarmful, or a patch hook in CanBeHarmful.
7. Reseeding with the door open (P421 #3; :381-392). The open SouthCW door sits at +1,+1 (pinned BaseDoor offsets), so
   FindDoor misses it. Match by the closed position.
8. Tests, each red first: (tests/Misc/TutorialVerification.cs, tests/Tutorial/TutorialFarmVerification.cs)
   - Skip then remedial after a farm pet gives no second pet, also across a save and load.
   - Close the pick: the recruiter offers it again; one claim only.
   - An alt pressing station, skip and graduate changes nothing.
   - Move the bandages out and ask again: no new stack, or the cap holds.
   - A failed treatment with a passed skill roll leaves step 3; a real heal completes it.
   - An outsider's swing at a pest runs no skill check.
   - Reseed with the door open: one door.
   - Tutorial record round trips for skipped, remedial and graduated, with a trailing sentinel (P420 #5).
   - Pen and pest respawn after death and taming (P421 #8).
9. Build and run the tests (docker\uo\build.sh -t sl-modernuo:cc-P??).
10. CHANGELOG: Fixed lines in player words, no how-to for the exploits.
11. Notes: notes\cc-P??-tutorial-fixups.md, including how many accounts on live (if the tutorial is live: game PC)
    already took two pets, from the evo pet records. Last line `P?? DONE`.

**Not in this prompt (Chase decides):** whether pen animals stay stock, with meat, wool and taming open to visitors
(P421 #5; F-35 implies yes), and whether the pen must hold one of each species (P421 #7).

**Done means:** every test above was red and is green.
```

### U4 (urgent, small). Smith commissions: the reroll cooldown is skipped through the guild book

```
# CC task P??: smith commissions: cooldown on the guild book's abandon, Pre-Crafted for large commissions

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** P263 put a cooldown on abandoning a smith commission and requesting a new one (the reroll fix). It is
recorded only from SmithCommissionGump (:302). The Smith Guild Book's own abandon button (SmithGuildBook.cs:649-658)
removes the commission without recording it, so a member rerolls through the book with no wait. Large commissions
have no cooldown at all (disclosed by P263) and never count for the Pre-Crafted achievement.

Found by cc-P429 (Crystal; the book bypass is new), and cc-P402 (Codex) F05 and F14.

## What to do

1. server/customizations/SmithGuildBook.cs, HandleAbandonComm (:649): call SmithCommissionSystem.Abandoned(pm) when a
   commission is removed, as SmithCommissionGump.cs:302 does.
2. Large commissions (F14): HandleAbandonLargeComm (:684) records a cooldown, and
   ClusterFSmithCommissions.GenerateLarge (:570) checks RequestCooldownLeft. Ask Chase in the notes whether large ones
   should share the small cooldown or have their own (clusterf setting). Default: share.
3. Pre-Crafted for large commissions (F05): ClusterFSmithCommissions.CompleteLarge (:675-695) calls
   ClusterFNotedBySystem.CommissionCompleted(pm, c.IssuedAt) once, after the Remove, as the small path does (:755).
4. Tests, each red first: abandon through SmithGuildBookGump's button and then request: refused within the cooldown;
   the same for large; turn in every piece of a large commission inside and outside the Pre-Crafted time.
5. Build and run the tests (docker\uo\build.sh -t sl-modernuo:cc-P??).
6. CHANGELOG: a Changed line ("Abandoning a commission from the Smith Guild Book now waits like abandoning one at the
   guild."). Do not write the hidden achievement's condition.
7. Notes: notes\cc-P??-commission-reroll-cooldown.md. Last line `P?? DONE`.

**Done means:** no abandon path skips the cooldown, and the tests show it.
```

## Drafts that can wait (most valuable first)

### W1. Creature-death hooks that read a deleted creature: boss boxes, rare Self Repair, bestiary credit

```
# CC task P??: death hooks: boss loot boxes and the rare Self Repair roll actually fire; pets' kills count for the bestiary

**Model:** Opus
**Touches:** server
**Golem:** any

**Summary:** Pinned deletes a non-player creature inside Mobile.OnDeath (Mobile.cs:4899-4902) before BaseCreature
raises CreatureDeathEvent. Delete sets Deleted (Mobile.cs:2503) and clears a pet's master. Two shard handlers on that
event require Deleted == false, so they never act on any creature: P79's first-kill boss loot box
(ClusterFLootBoxes.OnCreatureDeath, :166-170, through IsBoss -> ClusterFRareSelfRepair.IsHighEndSource :57-60) and
the rare Self Repair roll (ClusterFRareSelfRepair.OnCreatureDeath, :42-46). P263 found this (notes/cc-P263-*.md
:258-268) and moved its own handler to CreatureDeletedEvent, which runs first while the creature is whole. P79's
handler was left. Separately, the League bestiary credits only a PlayerMobile LastKiller, so tamers', summoners' and
bards' kills never count.

Found by cc-P263 (noted, not queued), the cc-P387 guide, cc-P404 (Codex) #1-#4, checked by cc-P429 (Crystal).
P427 is fixing the same ordering for levelable gear (ClusterFLevelGear); use the same pattern as P427, and if P427 has
merged, reuse its helper.

## What to do

1. server/customizations/LootBoxes/ClusterFLootBoxes.cs:166 and server/customizations/ClusterFRareSelfRepair.cs:42:
   move both to CreatureDeletedEvent with P263's guard (Hits <= 0 && !IsDeadPet; ClusterFNotedBySystem.cs:583-587),
   where Deleted is still false, the corpse holds its loot and the damage list is whole. Check bc.Corpse is set and
   filled at that point (pinned Mobile.Kill :4847-4872, BaseCreature.OnDeath). Keep a bonded pet's death on
   CreatureDeathEvent if either should ever see one (they should not).
2. Audit every other [OnEvent(CreatureDeathEvent)] handler in server/customizations for reads of Controlled, Summoned,
   GetMaster, ControlMaster or Deleted. Found so far:
   - Imbuing/ClusterFImbueEffects.cs:317 (`!bc.Controlled`) pays kill effects such as Butcher's Eye for killing a
     non-bonded pet.
   - Requisitions/RequisitionLeads.cs:221-226 resolves a pet killer through GetMaster, which is still set on the
     killer (the killer is not deleted), so that one is fine.
   Fix what reads the deleted victim's master. Say which handlers you checked in the notes.
3. server/customizations/ClusterFLeagueBestiary.cs:174: resolve the killer as stock does (BaseCreature.cs:3570,
   GetDamageMaster) before the PlayerMobile check.
4. Tests, each red first, through a real Kill(), not by calling the handler:
   - A boss killed by a player gives the first-kill box.
   - A high-end creature's corpse gets the Self Repair roll (force the 1-in-500).
   - A pet's, a summon's and a provoked creature's kill records the bestiary entry for its master.
   - A killed non-bonded pet pays no imbue kill effect.
   - LeagueBestiaryVerification: EnsurePoisons in the fixture (P404 #3), and stat, resist and loot asserts against
     P364's table (P404 #2).
5. Build and run the tests (docker\uo\build.sh -t sl-modernuo:cc-P??).
6. CHANGELOG: Fixed ("The first time you help defeat a boss, its loot box now arrives."; "Kills by your pets and
   summons now count for the League bestiary.").
7. Notes: notes\cc-P??-death-hooks.md. Last line `P?? DONE`.

**Done means:** the boss box and the Self Repair roll each have a real-kill test that was red and is green.
```

### W2. Music Room data loss, and the in-game music fallbacks before the first track ships

```
# CC task P??: Music Room saves that cannot lose notes; music fallbacks for a missing or unknown track

**Model:** Sonnet
**Touches:** web-console, server, player-package
**Golem:** home (client checks need the game PC)

**Summary:** Codex's P403 found four ways the Music Room (P367) can lose or misreport Chase's notes, and three
in-game music faults that wait for the first track to be assigned. Today ShardMusicTracks.All and ShardMusicTable.Rows
are empty, and the launcher returns early (Build-UoOverrides.ps1:704). Crystal's P429 confirmed all seven on main
da1a0cb.

Found by cc-P403 (Codex) #1-#7, checked by cc-P429 (Crystal).

## What to do

1. web-console/static/music.js:
   - send's catch (:175-177) keeps the record dirty and failed. status() and beforeunload (:193) count failed records.
     A retry happens on the next edit or a Retry button.
   - Serialize saves per track (:158-174): one in flight, then one follow-up.
   - flush (:179-183) awaits in-flight saves and stops Save to repo when any failed.
2. web-console/music.py:
   - notes() (:395-402): only a missing file is empty. On a read or parse error, or a wrong shape, save_note refuses
     and never writes, and GET reports the error.
   - save_note (:404-437) takes a revision and refuses a stale one (409).
3. Server, before the first track ships: C/Music/ClusterFShardMusic.cs:589-590. When the area has no music (Invalid),
   send the music from before the fight, or stop the music, not 0x6D FF FF.
4. Launcher, player-package/payload/app/Build-UoOverrides.ps1:
   - :711: put the accepted track lines in the cache stamp and bump the stamp format.
   - :727: a missing mp3 keeps its Config.txt line pointing at a stock fallback (a fallback column in shard-music.txt).
5. On the game PC: what TazUO does with an unknown music ID, and with 0x6D FF FF after a looping track. Write it down.
6. Tests, each red first:
   - web-console/tests: failed save then reload warns; reversed arrival keeps the newer note; Save to repo during a
     slow save commits the latest; a malformed notes file is untouched after a save.
   - Music-Overrides.Tests.ps1: missing then restored track.
   - ShardMusicVerification: fight ends in the default region.
7. Notes: notes\cc-P??-music-room-saves-and-fallbacks.md. Last line `P?? DONE`.

**Done means:** no Music Room path reports saved when it is not, and the three in-game cases have tests.
```

### W3. Noted by the System: the remaining condition bugs

```
# CC task P??: Noted by the System fix-up 2: bard check, mining streak, ground at the destination, 15 tiles, Mule Train

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** Codex's P402 review of P263 found small condition bugs in the hidden achievements beyond the two P427
already fixes. Crystal's P429 confirmed them on main da1a0cb. Do this after P427 merges and reuse its damage record.
Do not write any hidden condition in plain words in the CHANGELOG or the notes summary.

Found by cc-P402 (Codex) F01 (the :621 half), F02, F03, F04, F06, F09, F10, F11-F13, checked by cc-P429 (Crystal).

## What to do

All in server/customizations/ClusterFNotedBySystem.cs unless named.

1. :621 uses the victim's damage list as proof a player never hit it. That list empties at full HP and after 2
   minutes (pinned Mobile.cs:2043, :55-59, :5880). Use the record P427 builds for :609.
2. :767 and server/patches/Mining.cs:297-302: clear the empty-swing streak on a successful harvest.
3. :777-791, :815: the movement event fires before SetLocation (pinned Mobile.cs:4103, :4386), so ground is read at
   the departure tile, and GroundAt has no Z, so land under a floor counts. Read the destination and the player's Z.
   Land counts only when no walkable static or multi surface is at or below the player's Z, and a field only within
   step height.
4. :626: the range check is inclusive (pinned Mobile.cs:3076). Use RemoteWorkRange - 1 so 15 counts, as the header
   says (:20).
5. :861: require bc.Map == pm.Map and !bc.IsDeadPet.
6. Optional, cheap:
   - Stop the per-runebook marker once its last tier is earned, and set 1 rather than increment (:694; F09).
   - In the step handler, check equipment before GroundAt, and cache definitions by trigger (F10).
7. Tests, each red first, through the real patched paths where one exists (F12): the bard case after heal to full;
   empty A, success at B, empty A; a step onto and off lava and a floor over snow land; owner at 14, 15, 16; off-facet
   and dead followers. Also positive tests for the snow, Mule Train and final tiers (F11), and crafted-only at the
   large deed, large commission, tailoring and setting-off (F13).
8. Build and run the tests (docker\uo\build.sh -t sl-modernuo:cc-P??).
9. CHANGELOG: one Fixed line, "Some hidden achievements now check their conditions more carefully." Nothing more
   specific.
10. Notes: notes\cc-P??-noted-fixups-2.md. Last line `P?? DONE`.

**Not in this prompt (Chase decides):** F07, recycling a fresh item another player crafted. P263 accepted it as
"yours in practice". Either record the real crafter, or reword the achievements.
```

### W4. Eodon fix-up: spawn weights, the hatchling's tame, the climbing vine

```
# CC task P??: Eodon fix-up: XmlSpawner weights, the hatchling's first tame, no climbing while paralyzed

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** Three fixes to P198's Eodon port, from Codex's P407 and Crystal's P428. This one prompt replaces P428's
drafts 1 and 2; queue this instead of them.

Found by cc-P407 (Codex) #1-#4 and cc-P428 (Crystal) findings 1-2, checked by cc-P429.

## What to do

In server/customizations/Services/Expansions/Time Of Legends/.

1. EodonSpawns.cs:147: every entry gets probability 100. ServUO's XmlSpawner weights the available entries by MaxCount
   (XmlSpawner2.cs:8339-8408), so with equal weights a white tiger in Wildlife #4 is 1/8 instead of 1/25. Pass
   entry.MaxCount as the probability, and fix the header (:17).
2. Mobiles/DragonTurtleHatchling.cs: drop StatLossAfterTame (:65) and override OnAfterTame with ServUO's body (cap,
   55% skill cut, keep stats). The shard has had the hook since cc-P130 (BaseCreature.PetTraining.cs:152, the
   AnimalTaming patch :27). Pinned adds the owner before the hook, so a first tame is Owners.Count == 1; or pass
   alreadyOwned through PetTrainingHooks.OnTamed, which also helps the other ported creatures noting the same
   deviation. Fix the header (:9-11).
3. Items/ClimbingVine.cs:33-42: refuse when Paralyzed, Frozen or casting.
4. Tests, each red first (tests/Services/TimeOfLegends/EodonRemainderVerification.cs):
   - Each generated entry's probability equals its MaxCount.
   - A real tame of a hatchling: skills about 0.9 x 0.45 of wild, stats kept, no second cut on a re-tame. This
     replaces the flag-only assert at :189.
   - A paralyzed player cannot climb.
   - Infernus fire through OnActionCombat and the one-second tick (P407 #3).
   - Rerun deletes the first run's creatures (P407 #4).
5. Build and run the tests (docker\uo\build.sh -t sl-modernuo:cc-P??).
6. On the test shard after [GenEodon (game PC): is there a walking way down from the Barako clifftop (679,1757,100)?
   Say so in the notes; do not add a down-vine here.
7. CHANGELOG: Fixed ("The Eodon cliff vines cannot be climbed while paralyzed."), and a Staff line for the hatchling.
8. Notes: notes\cc-P??-eodon-fixups.md. Last line `P?? DONE`.
```

### W5. Stumps: fold into the queued P412

Not a new prompt. P412 already rewrites `ClusterFLumberStumps.cs`. Add to P412, or to its fix-up if it has started:

```
Also (from cc-P400 #2-#5, checked by cc-P429):
- ClusterFLumberStumps.cs:121, OnChop: accept any equipped lumber tool (BaseAxe, or a polearm, whose harvest system is
  Lumberjacking; pinned BasePoleArm.cs:32), so a polearm gets "not enough wood" (500493), not "equip an axe"
  (500487). A test with an equipped Bardiche, red first.
- Tests (ChoppedTreeStumpsVerification.cs):
  - Two players finish on a bank with one batch left: one stump, and the deadline unchanged.
  - The same bank is marked again after expiry, after a refill and after a manual delete.
  - Save and reload: no stump in the world.
```

### W6. Guild hall decor seeder: shifted anchors, edited templates, the design test

```
# CC task P??: guild hall decor seeder: refuse overlapping or out-of-date placements; test the real design file

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** Codex's P419 review of P265 found that placing a set one tile off doubles it, that a re-run after a
template edit keeps stale rows, and that the design test hashes the C# copy, not design/guild-hall-decor/templates.json.
Test shard only today (the seeder refuses live, GuildHallDecorSeeder.cs:43-47). Do it before F-49 starts tuning
templates.

Found by cc-P419 (Codex) #1, #2, #4, #5 (and nit #6), checked by cc-P429 (Crystal).

## What to do

1. GuildHallDecorSeeder.cs:75-87: store a template hash on each placed GuildHallDecor (a new saved field: generator
   version 0 to 1 with its migration). Refuse a placement whose template changed ("clear first"), or whose footprint
   meets the same set at another anchor.
2. :98 (optional, Chase may want it with F-49): preflight every row for impassable statics and items and for doors.
   The dry run reports the conflicts, and nothing is placed on a conflict.
3. tests/Misc/GuildHallDecorVerification.cs:62: compare against the real templates.json (copy it to the test output),
   so an edit to the JSON alone goes red.
4. Tests, each red first: a shifted anchor is refused; an edited row offset is refused; a JSON-only edit goes red.
   Optional: VirtualCheckActivatorVerification also runs the initializer (P419 #6).
5. Build and run the tests (docker\uo\build.sh -t sl-modernuo:cc-P??). Notes: notes\cc-P??-hall-decor-seeder.md. Last
   line `P?? DONE`.

**Not in this prompt (Chase decides):** P419 #3, whether the towers' door walls should open (cc-P265:379-384).
```

### W7. Artificers' guildmaster text still describes the old rules

```
# CC task P??: Artificers' guildmaster and join text match the current rules

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** The P383 guide (Codex) kept two code-versus-design contradictions that are plain wrong text in game.
- server/customizations/ArtificersGuildmasterGump.cs:197 says "Upon joining the Artificers' Order you receive: ...",
  but since F-9 Decision 3 and P15 the rewards come with the Apprentice task (ClusterFGuildSystem.cs:313, :382, :427).
- ArtificersGuildmasterGump.cs:157-158 says "Higher ranks unlock greater caps", and the join message at
  ClusterFGuildSystem.cs:508 says standing unlocks higher caps and more slots. P82 replaced both with learned tiers
  (ArtificersImbueGump.cs:1767).

Found by the cc-P383 guide (Codex), checked by cc-P429 (Crystal).

## What to do

1. Reword those three texts to the current rules: rewards on the Apprentice task; power from learned tiers and site.
   Use the wiki draft notes/wiki-drafts (the P383 guide page) for wording.
2. Any test that pins the old text: update it.
3. Build and run the tests (docker\uo\build.sh -t sl-modernuo:cc-P??). Notes: notes\cc-P??-artificers-text.md. Last line
   `P?? DONE`.
```

## For Chase (policy calls, no draft)

- **P418 #8:** Blaze repair (League Register) is free, unlimited, and covers banked gear and gear handed over by
  someone else. P280 designs it that way. Keep it, or add a cost or a cooldown?
- **P402 F07:** recycling achievements count a fresh item another player crafted. P263 accepts this. Keep it, or record
  the real crafter?
- **P402 F14:** a cooldown for large commissions too? U4 defaults to sharing the small one.
- **P421 #5 / #7:** should the farm pen stay stock animals (meat, wool, taming open to visitors), and must it hold one
  of each species?
- **P419 #3:** are the guild hall towers meant to be walked into?
- **P401 #1-#3:** belong to the F-12 build: cap from the permanent max level, one loop at a time with its scroll. Hand
  them to whoever writes F-12's prompt.

## What I could not check from GitHub alone

- Nothing was built or run. Every verdict is from reading code against pinned ModernUO `d4531cd` and ServUO pub57.
- What the client does with an unknown music ID or `0x6D FF FF` (P403 #5, #6): the game PC.
- Whether the tutorial, its farm, the Appraiser and the League Register are live, and so whether U1 to U3 have already
  been used: the game PC (the server logs, the evo pet records, the Appraiser's gold out).
- P422's notes merged during this run. I checked all four of its findings myself (no helper).

P429 DONE
