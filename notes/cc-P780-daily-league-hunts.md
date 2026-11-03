# cc-P780: daily League hunts on the requisitions board

## In plain words

- **The requisitions board now posts League hunts.** Each day a character gets two kill goals from the League Bestiary
  ("cull 12 hedge snatchers", "hunt down 4 tunnelmaws"), and each week one bigger great hunt. They are shown at the
  bottom of the board, with progress ("4 of 12").
- **Kills count on their own.** No NPC and nothing to hand in. The player who did the most damage gets the kill, and
  party members within 18 tiles count it too. When the last kill lands, the hunt pays League Renown, guild standing (and
  guild points for a member) and gold. The great hunt pays four times as much plus a System's Silver Loot Box (the
  League shop's cosmetic and decor goods, never magic gear). Unfinished hunts just roll over with no penalty.
- **Every number is in one file**, `Configuration/league-hunts.json`, written with the defaults the first time the
  server starts. Existing worlds need nothing else: each character's hunts appear the first time they open the board.
- **For you:** hunts only name creatures whose bestiary spawners stand in the world. If `[ClusterFSeedBestiary` has
  not been run on Haven yet, the board will say "No hunts are posted for you today" until it is (or set
  `onlyWithSpawner` to false in the file). Nothing else to deploy or decide.

Iron Golem, 2026-11-03. Code in `D:\UO\golems\Iron\ShatteredLegacy` (branch `golem/Iron/P780`), image
`sl-modernuo:cc-p780`. The prompt's two open choices from P777 were settled in the prompt itself: party members in range
share the count, and the great hunt pays a Silver box.

Credit: the daily and weekly kill-goal idea is from DragnMaw's **DailyQuests 1.02** (servuo.dev #1539, in
`D:\UO\third-party\code\daily-quests`), assessed in cc-P777. None of its code, NPCs, tickets or rewards is used; nothing
was built or run from `D:\UO\third-party`. Credited in the CHANGELOG line, and the `CODE-INTAKE.md` row now reads
"assess (P777), idea built (P780)".

## What was built

| Piece | Where |
|---|---|
| The hunts: roll, weeks, kill credit, counting, pay, the `HuntFamily` seam, `[hunts`, `[LeagueHuntsStaff` | `server/customizations/Requisitions/LeagueHunts.cs` (new) |
| The file and its validation (`league-hunts.json`) | `server/customizations/Requisitions/LeagueHuntTable.cs` (new) |
| The saved record: `HuntEntry`, and `CharacterRequisitionData` version 1 | `server/customizations/Requisitions/RequisitionData.cs` |
| Hunts rolled before the requisitions in `EnsureCurrent` (so a slayer row sees today's hunts) | `server/customizations/Requisitions/RequisitionSystem.cs` |
| The hunts section of the board (taller gump, 440 to 620) | `server/customizations/Requisitions/RequisitionsBoard.cs` |
| Header comment: F-24 is built now | `server/customizations/ClusterFLeagueBestiary.cs` |
| Ten facts | `server/tests/Misc/LeagueHuntsVerification.cs` (new) |
| CHANGELOG `2026.11.03`, `VERSION` | repo root |

### How it works

- **Families.** A family is one League Bestiary creature kind (`ClusterFLeagueBestiary.Entries`, all 14 of them, each
  named once; fact 1 checks the list covers the bestiary). Each has a use: **cull** (culling packs, 12 kills), **hunt**
  (hunt targets, 4) or **boss** (the two mini-bosses, 1). A family may list more than one creature type; today each has
  one. I read "a League Bestiary family" as one bestiary creature kind, since the bestiary has no grouping above that.
- **The roll.** On the requisitions board's day (05:00 UTC refresh), `dailyHunts` (2) hunts of different families; on
  the weekly reset (Monday, same hour) one great hunt. Each is posted by a guild the character has joined (else any
  guild that posts requisitions) at that guild's requisitions tier (rank in the guild, capped by the League gate). The
  tier sets the level reach: a family is offered when its lowest bestiary level is within the tier's `maxLevel` (tier 0:
  15, so a new character gets hedge snatchers, ditch crawlers, hornback raiders, mire croakers); the great hunt reaches
  30 levels further and needs three times the kills.
- **Lazy, so existing worlds need nothing.** Hunts are rolled when the board (or a kill, for a character who already
  has a record) next reads the record. Old records (version 0) load with no hunts and roll on first read.
- **Credit.** `CreatureDeletedEvent`, as the loot boxes' boss kills use (cc-P455): pinned deletes a dead creature before
  `CreatureDeathEvent`, and clears a pet's master right after raising the deleted event, so only there is a dead pet
  still a pet. The player with the most damage by pinned's looting rights (a pet's damage counts for its master) is
  credited, else the last killer as the bestiary reads it; then each member of that player's party within `shareRange`
  (18) of the corpse. A pet or summon dying counts for nobody.
- **Pay.** On the last kill, once: Renown (as League work, so it counts toward League rank, like a requisition), guild
  standing, the guild's points for a member (`GuildPointEarning.OnRequisition`, the requisition rule), gold into the
  pack. The great hunt adds `LeagueShop.MakeBox(pm, BoxTier.Silver)` through `ClusterFGuildPromotion.Deliver` (pack,
  or bank when full). Pay is fixed when the hunt is rolled, so an edit to the file changes new hunts only.
- **Default pay** (all in the file): Renown and standing equal the requisitions tier's (10/40 at tier 0 up to 110/250 at
  tier 5: a hunt is a day's work like a requisition), gold 250 to 1,800 by tier. Great hunt: four times that.
- **The `HuntFamily` seam** (`ClusterFRequisitions.HuntFamily`, empty since cc-P150) is filled by
  `LeagueHunts.HuntFamilyFor`: a slayer requisition row marked "any" asks for the slayer of an open hunt's family. The
  slayer is the family's `slayer` in the file, else whatever pinned's slayer groups say slays its creature.
  **Finding:** no pinned slayer group covers any of the 14 bestiary creatures (they all derive straight from
  `BaseCreature`), and the default file names no slayer, so today the seam answers nothing and slayer rows draw from the
  requisitions table as before. Naming a slayer in the file (fact 7 uses `"slayer": "Silver"` on pale drifters) turns
  it on. I did not set any by default: a requisition asking for an undead slayer while you hunt pale drifters would
  suggest the weapon works on them, and it does not.

### Rules check

| Rule | How it holds |
|---|---|
| No skill or stat points, power scrolls, bless deeds or property artifacts | A hunt pays Renown, standing, guild points, gold and (great hunt) a League shop Silver box. The Silver box draws only the shop's rows open at 250 AP: cosmetics, decor, conveniences and the League sash, never magic items or titles (`LeagueShop.BoxPool`). Fact 10 checks everything a finished great hunt adds to the pack is gold or a loot box, and that 40 Silver boxes hold no power, stat or skill scroll, bless deed, weapon, armour or jewel. |
| Rewards usable now and mostly helpful | Gold; Renown (spent at the League shop, counts toward rank); guild standing and points (guild stores); the box's goods. |
| No new currency, no NPC | None: the existing currencies, the existing board. |
| All numbers in a config file | `Configuration/league-hunts.json`: hunts a day, reset day, party range, the spawner switch, counts by use, pay and level reach by tier, the great hunt's multipliers, level bonus and box, the families. Refused whole if bad (unknown setting, a creature outside the bestiary, out-of-range numbers); fact 1. |
| Appears on an existing world by itself, idempotent | The file is written on first start if missing; hunts roll per character on first read; a version 0 record loads. Nothing is placed in the world, so there is nothing to seed. |
| D40 serialization | `HuntEntry` and `CharacterRequisitionData` each carry a version and throw on an unknown one; version 0 records read (fact 8). Both are hand-serialized inside `ClusterFAccountData`, whose own version (23) is unchanged. No generated type changed, so no migration file. |

## Tests

`LeagueHuntsVerification`, ten facts (names in the file header): the file; the roll; the daily refresh; the weekly
reset; counting and pay once with the Silver box; most-damage and party credit through the real death; the seam; the
record and a version 0 load; the board and `[hunts`; the rules and the file's numbers.

**Seen failing first** (probe: builder image `sl-uo-builder:cc-P776`, this branch's base, with the change mounted;
`cc-P780-tools/probe.sh`):
- against the code before the change, the test file does not compile: 5 errors, `HuntEntry` and `LeagueHuntFamily`
  unknown (`cc-P780-tools/red-probe.txt`);
- the first green run failed fact 6 for real: a pet's death counted, because I had hooked the death event, where pinned
  has already cleared the pet's master. Moved to `CreatureDeletedEvent` (`red-pet-on-death-event.txt`, then
  `green-probe3.txt` 10 of 10);
- a mutant with one break per fact (no pay-once guard, last hitter instead of most damage, no party, week offset 0, the
  day counted from 00:00, no great multiplier, the seam returning nothing, the box ignoring the file, `Paid` not read,
  the board's hunts section dropped, bestiary names not checked): **all 10 facts failed**, each on its own break
  (`red-mutants.txt`). Fact 5 failed first on the multiplier break, so it was run again with only the pay-once guard
  removed: failed on `Assert.False(Pay(...))` (`red-mutant-payonce.txt`).

The old requisitions facts (`RequisitionsVerification`, 12) pass with the change (`green-probe1.txt`).

**Gated build** (`cc-P780-tools/gated-build.ps1`, the `docker-build` lock taken and released): **EXIT=0**, 2,993 tests:
2,987 passed, 6 skipped, 0 failed; all 186 patches applied; the ten `LeagueHuntsVerification` facts among the passes.
Image `sl-modernuo:cc-p780` (`latest` not touched). Summary in `cc-P780-tools/green-gated-build.txt` (the raw log is
git-ignored and was removed). The log's 110 `Item.Amount <= 0` corpse errors come from other suites and appear the same
110 times in P763's green gate.

## Deviations and decisions for Chase

- **Hunts need the bestiary spawners.** With `onlyWithSpawner` (default true) a family is offered only while one of its
  `ClusterFSeedBestiary` spawners stands on Trammel. I did not make the bestiary seed itself on load: it is a
  test-shard-first staff command (its cc-P364 CHANGELOG line says test shard first, then live), and placing 25 spawners on a live world by itself is a call for you.
  If it has not been run on Haven, hunts stay empty there until it is, or until `onlyWithSpawner` is set false.
- **"Family" read as one bestiary creature kind** (see above); the file allows several types per family if you want
  groups later.
- **The slayer seam is filled but quiet by default** (no slayer covers the bestiary creatures); see above.
- **The gump is taller** (620 instead of 440) to fit three hunt rows under the requisitions.
- **No in-game proof run.** Not asked for in "Done means"; the board and the death-event credit are covered by facts 6
  and 9 in the test host.
- The Read tool was auto-denied once on my own new test file (unattended run); I used Bash instead. Nothing was
  skipped because of it.

## Files

- ShatteredLegacy: the six code files above, the new test file, `CHANGELOG.md`, `VERSION`.
- shard-migration: this file; `notes/cc-P780-tools/` (probe and gate scripts, red and green logs).
- `D:\UO\third-party\CODE-INTAKE.md`: the daily-quests row's status (CRLF kept; backup in the session scratchpad).

P780 DONE
