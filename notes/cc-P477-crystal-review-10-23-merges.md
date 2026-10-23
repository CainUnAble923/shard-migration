# cc-P477: a read-only code review of the 10-22 evening and 10-23 server merges

**Golem:** Crystal (cloud). **Date:** 2026-10-23. **Branch:** `golem/Crystal/P477` (shard-migration only; no code changed).

## In plain words

- **The tutorial (Chase is testing it today).** On the test shard the nine core lessons hold together. Each one starts,
  finishes and clears up after itself. The practice items cannot hold a player's things, so they cannot take any
  with them. A relog, a restart or dying in the middle never leaves a player stuck: the lesson starts again, and the
  "Reset this lesson" button always works. Graduation pays once. I found no new way to get stuck on the test shard.
- **The tutorial's biggest problem is for the next live, not the test shard.** Since P289 the tutorial only runs
  on the test shard, but P371's island gate still runs everywhere. On a live shard, every new player would be held
  on New Haven island with nothing that lets them graduate or skip. Codex flagged this in its P475 review. I
  confirmed it, and no fix is queued. There is no live shard today (retired and deleted on 10-14 until the fresh
  1.0 world, `README.md:112`), so no one is stuck now. It must be fixed before the 1.0 live opens.
- **One reward repeats:** every character on an account that graduated (or skipped) gets its own tier-6 "loop" loot
  box the first time it logs in. On the test shard a player can delete the character and make a new one at once, so
  the boxes never run out. On live it is one box per character slot, then one more per slot every 7 days. This is
  P371's code (merged 10-21, a range neither P379 nor P428 reviewed), but it pays out at the end of the tutorial.
- **Small:** the core lessons lost the "Open the World Map / Journal / options" buttons for TazUO (Codex's P475,
  finding 2, confirmed).
- **Other merges:** P277 (the rideable dragons), P410, P287 and P288 have nothing to report. P408 (the Halloween
  Sorcerer's Dungeon) turns itself on tomorrow, 10-24, on every shard that has the code. Today that is the test
  shard only, since there is no live shard. Two of Codex's open findings would then be playable there: the double
  ring purchase and pets' kills counting. And it cannot be held off without also stopping the Halloween bank decor. P281's guild hall `clear` can remove the wrong
  guildmaster (staff tool, test shard only).
- Nothing was built or run: a cloud Golem cannot build the shard. Each draft asks for a failing test first.

Range reviewed: `da1a0cb..0f1871f` of shattered-legacy-infrastructure `main` (P428's head to today's head, P475's
merge; nothing newer when I finished). Merges in it: P408, P410, P277, P281, P287, P288, P289 with P475. Paths:
`server/`, `client/patches/` (no changes) and `docker/uo/` (only `COMMANDS.md`). Pinned ModernUO `d4531cd9` was read
from GitHub for `PlayerMobile.cs` and `AccountHandler.cs`.

Already known, so not reported again: everything in P428 and P429, the queued P451 to P460, Codex's per-merge reviews
of P408, P277 and P281, and Valorite's P461 review of P408 (P476 turns P461 into drafts). The two Codex P475 findings
are repeated here (T1, T3) because nothing queued names them, and the tutorial is under test today.

## Tutorial findings (P289, P475 and the graduation path)

### T1. On a live shard, every new player would be held on New Haven island for good (wrong behavior, severe; blocks the 1.0 live)

- **Where:** `server/customizations/Tutorial/ClusterFTutorial.cs:46-47` (P289: `Enabled` needs `testCenter.enable`);
  `Tutorial/TutorialIslandGate.cs:13`, `:17` and `:27-28` (P371: the gate is on by default and reads only
  `clusterf.tutorial.islandGate` and the loop count); `Tutorial/TutorialGumps.cs:44-61` (Rook offers lessons, skip
  and graduate only to an active record).
- **What goes wrong:** on a server with `testCenter.enable` false, `OnLogin` never calls `TryEnter`, so a new
  account's record stays `NotStarted`. `NeedsGraduation` is still true for any Player-level character on the island
  with loop 0. It blocks walking off the island, recall, gate, Mark and boats. Rook's gump shows "Status: NotStarted"
  and "Nothing more to teach you here", with no skip button, because skip needs `IsActive`. Nothing else ever sets
  the loop to 1. The new player is held on the island for good.
- **How it is hit:** the fresh 1.0 live opens on a build with P289 and P371 in it (anything from 2026.10.23.2 on),
  with `testCenter.enable` false, and a new player makes a character. There is no live shard today. Accounts that graduated or skipped before are fine, because `OnLogin` gives their characters
  loop 1. This is Codex's P475 finding 1, which I confirmed.
- **Also:** on the test shard, an account whose tutorial character was deleted mid-tutorial is held the same way.
  `CharacterSerial` points at a deleted character, so no character is a participant and none can skip. P453
  item 3 ("re-point only when that character is deleted") covers that part. Make sure that P453 keeps it.
- **Needs a server?** No for the logic, and the test has no live shard to check against.

**Prompt draft:**

```
# CC task P??: the island gate follows the tutorial: no gate where the tutorial is off

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** P289 made the tutorial test-shard only (ClusterFTutorial.Configure), but P371's island gate still holds
every loop-0 player on New Haven island on every shard. On live no one is entered, Rook offers no skip, and nothing
grants loop 1, so a new live player can never leave the island. Gate only where the tutorial runs.

Found by cc-P477 (Crystal), finding T1, and Codex's P475 review, finding 1.

## What to do

1. `server/customizations/Tutorial/TutorialIslandGate.cs`: `NeedsGraduation` also needs `ClusterFTutorial.Enabled`.
   Keep the `clusterf.tutorial.islandGate` setting as a second switch. Keep the test seams settable.
2. Prefer one rule over a second setting: when the tutorial is off, a loop-0 character is not stopped, and nothing
   about its loop or Young status changes.
3. Tests (`server/tests/Tutorial/GraduationLoopVerification.cs`): with `ClusterFTutorial.Enabled = false`, a new
   loop-0 player can move off the island, recall and gate. With it true, the gate still stops them. Show the first
   one red against today's code.
4. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`).
5. CHANGELOG, Fixed: "New characters on a shard without the tutorial can leave New Haven island again."
6. Notes: `notes\cc-P??-island-gate-follows-tutorial.md`. Last line `P?? DONE`. (There is no live shard today;
   this must be in before the 1.0 live opens.)

**Done means:** with the tutorial off, no player is held on the island. With it on, the gate is unchanged.
```

### T2. Every later character on a graduated account gets its own tier-6 loop box (wrong behavior: a reward that repeats)

- **Where:** `Tutorial/ClusterFTutorial.cs:80-85` (on login: graduated, or skipped while skipping counts, means
  `ClusterFLoops.Graduate`); `Tutorial/ClusterFLoops.cs:23` (the loop count is kept per character serial) and
  `:47-60` (`CompleteLoop` pays when the character's loop is below 1); `LootBoxes/ClusterFLootBoxes.cs:69-70` (the
  loot record is per character serial), `:96-101` and `:218-221` (`loop:1` pays a box once per record);
  `LootBoxes/ClusterFLootTable.cs:133` (`LoopTier = 6`, the top tier).
- **What goes wrong:** the loop count and the loot record are both kept by character serial. A new character on an
  account that graduated (or skipped, with `clusterf.tutorial.skipCountsAsGraduation` at its default true) starts
  at loop 0 with an empty record. At its first login it "completes loop 1" and gets a tier-6 Loop box, with a
  Capstone fanfare. The box is account-bound (`LootBoxItems.cs:146`), but its gold and items are not.
- **How it is hit:** a player graduates (or skips), then makes characters to collect a box on each. On the test shard
  pinned's 7-day delete delay is off (`server/patches/AccountHandler-test-center-deletion.patch`; pinned
  `AccountHandler.cs:221`), so delete, recreate and log in pays a tier-6 box every few minutes. On a live shard it would be one
  box per free slot at once, and then one per slot every 7 days. P371's notes say a character's first loop is
  idempotent, but nothing makes the box once per account.
- **Not mine to decide:** whether a later character should be on loop 1 at all is P371's design, from Chase's
  2026-10-21 decision. What is wrong is the box. The fanfare and box are for "completing loop 1", and a new
  character on an old account completed nothing.
- **Needs a server?** No for the logic. Whether any test-shard account has already done this needs the game PC
  (count `loop:1` records per account).

**Prompt draft:**

```
# CC task P??: the first-loop box is once per account; later characters get loop 1 quietly

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** P371 gives each later character on a graduated (or skipped) account loop 1 at its first login, and that
goes through ClusterFLoops.CompleteLoop, which pays a tier-6 Loop box per character. Deleting and recreating a
character pays again (at once on the test shard, every 7 days per slot on live). Keep the loop 1 record and drop
the box and fanfare for characters that did not earn it.

Found by cc-P477 (Crystal), finding T2.

## What to do

1. `server/customizations/Tutorial/ClusterFLoops.cs`: split recording from paying. Add
   `RecordLoop(pm, loop)` (sets the per-character flag, no box, no fanfare). The login path at
   `Tutorial/ClusterFTutorial.cs:80-85` uses it for every character except the one that graduated. That one already
   got its box in `Graduate` (:245) or `Skip` (:187).
2. Keep `Graduate` and `Skip` paying exactly once, for the character that did it.
3. Tests (`server/tests/Tutorial/GraduationLoopVerification.cs`): graduate on character A (one Loop box). Log in a
   new character B: loop 1, no box, no Capstone fanfare. Delete B, make C: still no box. Repeat for a skipper with
   skipCountsAsGraduation true. Show B's box red against today's code.
4. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`).
5. CHANGELOG, Fixed (no how-to): "A new character on an account that already finished the tutorial no longer gets
   the first-loop box again."
6. Notes: `notes\cc-P??-first-loop-box-once.md`, with the count of `loop:1` boxes per account on the test shard
   (game PC). Last line `P?? DONE`.

**Done means:** one first-loop box per account, and the tests show it.
```

### T3. The core lessons lost TazUO's "open the window" buttons (cosmetic)

- **Where:** `Tutorial/TutorialCoreTrials.cs:104-110` (`Show` sends `TutorialTrialGump` only);
  `Tutorial/TutorialGumps.cs:163-168` (the `Windows` buttons live on `TutorialStationGump`);
  `Tutorial/ClusterFTutorial.cs:147` (only the optional wings still get them).
- **What goes wrong:** before P289, Movement (Options), Speaking (Journal) and Getting around (World Map) showed
  `TutorialStationGump`, with a button that opens that TazUO window on a client that answered P103's handshake. Now
  each core lesson shows `TutorialTrialGump`, which has no such button. The lesson text still names the windows.
  Codex's P475 finding 2, confirmed. P475's restore of the argument covers the wings only.
- **How it is hit:** every TazUO player in the three lessons. Nothing breaks.

**Prompt draft:**

```
# CC task P??: the core lesson pages keep the TazUO window buttons

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** P289's trial page (TutorialTrialGump) replaced the station page for the core lessons, and with it the
P103 buttons that open TazUO's options, Journal and World Map. Put them on the trial page.

Found by cc-P477 (Crystal), finding T3, and Codex's P475 review, finding 2.

## What to do

1. `server/customizations/Tutorial/TutorialCoreTrials.cs`: `TutorialTrialGump` takes `canOpenWindows`
   (`TazUOClientCommand.CanRunCommands(pm.NetState)`) and adds `TutorialStationGump.Windows` buttons for the
   station's TazUO features, with the same response code. Use button ids that do not clash with 1 and 2.
2. Tests (`server/tests/Misc/TazUOClientCommandVerification.cs` or TutorialVerification): the Movement, Speaking
   and Getting-around trial pages have the button for a handshake client, and none for another client.
3. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`). CHANGELOG, Fixed, one line.
4. Notes: `notes\cc-P??-trial-page-window-buttons.md`. Last line `P?? DONE`.
```

### Checked in the tutorial, and fine

- **Order and start:** `Start` refuses a lesson out of order, a ghost (it points to the healer), and anyone but the
  recorded character (`IsParticipant`). A finished lesson shows its "done" page and gives nothing again.
- **Supplies:** the practice cloak, bag and bank token are made per trial, deleted by instance when the trial ends
  or is cancelled ("even if moved to the bank"), and deleted at world load if one is left over. The bag refuses
  every drop (`OnDragDrop`, `OnDragDropInto`), so nothing of the player's can be inside it when it is deleted. No
  player item is deleted by a lesson.
- **Death lesson:** pinned moves a Young player's movable items to the backpack, not the corpse
  (`PlayerMobile.cs:2446-2449`, `:2469-2472`), as the lesson says. `PlayerDeathEvent` comes after
  `YoungDeathTeleport` (`:2563`), so the move back to the farm wins. A ghost who logs out comes back with no trial,
  is pointed at the healer, and the healer's offer and gump still work without one. A player who is not Young keeps
  their things on the corpse four tiles from the healer, and the gump says "while you are Young".
- **Relog and restart:** `OnLogin` cancels the trial (`ClusterFTutorial.cs:69`); the 250 ms tick cancels it at
  logout; finished stations live in the saved record. The orphan arrow fix in `GuildDirectionArrow` is right.
- **Graduation:** `Graduate` sets `Graduated` before paying, `IsActive` is then false, and a stale recruiter gump
  can only return "You are not in the tutorial". The `tutorial:graduation` box and the first-loop box are once per
  character record. The second pet is P453's (item 1).
- **Reset:** a participant's "Reset this lesson" clears only that station, and moves `InWings` back to `InCore`,
  which pays nothing.
- **For the overseer:** P453 item 3 was written before P289. `RunStation`, `CompleteStation`, `Skip` and `Graduate`
  now check `IsParticipant`, which compares `CharacterSerial`. What is left of item 3 is the recruiter gump's
  `record is { IsActive: true }` (`TutorialGumps.cs:44`, which shows buttons to other characters, but they do nothing),
  and `StartRemedial`'s re-pointing. Its line numbers have moved.

## Other findings

### O1. Treasures of Sorcerer's Dungeon turns itself on 10-24, and cannot be held off on its own (wrong behavior, timing)

- **Where:** `server/customizations/Services/Seasonal Events/TreasuresOfSorceresDungeon/Generate.cs:58-66` (the switch
  borrows the Halloween dates); `server/customizations/ClusterFSeasonalSwitch.cs:104-106` and `:136` (`StartKey`,
  `EndKey` and **`AutomaticKey`** all read `clusterf.seasonal.halloween.*`).
- **What goes wrong:** the switch acts at the first hourly check of 10-24 and calls `Up` on any shard with P408's
  code. The `[SorcerersDungeon` command is `CommandShard.TestFirst`, but the automatic switch does not look at that.
  The only way to keep it off is to turn `clusterf.seasonal.halloween.automatic` off, and that also stops the
  Halloween bank decor going up (P267), or to run `[SorcerersDungeon off` after it turns on. Tomorrow it goes up on
  the test shard (the only shard: there is no live, `README.md:112`) with two open findings:
  - P461 finding 1: a player can queue several 50-point ring confirmations and accept them all for one balance (an
    exploit that pays).
  - Codex's P408 finding 3: a pet killed in the dungeon counts toward kill tallies and artifacts.
  P476 drafts the fixes. They will not be merged by tomorrow.
- **How it is hit:** the test shard runs a build with P408 on 10-24 (which build it runs needs the game PC). With no
  live shard, the exploit only touches test characters; it matters for next October's live season, and for any
  League or Renown balance carried from the test world into 1.0.
- **For Chase (recommended):** nothing urgent. Leave it on for testers, or run `[SorcerersDungeon off` after the
  first hourly check on 10-24. The draft below makes this a setting of its own.

**Prompt draft:**

```
# CC task P??: Sorcerer's Dungeon gets its own "automatic" setting

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** P408's event borrows the Halloween season's settings through datesFrom, including .automatic, so staff
cannot keep the event off without also stopping the Halloween bank decor. Borrow only the dates.

Found by cc-P477 (Crystal), finding O1.

## What to do

1. `server/customizations/ClusterFSeasonalSwitch.cs`: `AutomaticKey` uses the switch's own `Name`
   (`clusterf.seasonal.sorcerersdungeon.automatic`), and `StartKey`/`EndKey` keep `DatesFrom`. Update the header
   comment and `Generate.cs`'s header (deviation 1).
2. Decide the default with Chase: true keeps today's behavior. False makes staff turn it on by hand.
3. Tests: with the Halloween decor's automatic on and the event's off, the hourly check in season brings up the
   decor and not the event, and the reverse.
4. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`). `docker/uo/COMMANDS.md`: name the new
   setting in the `[SorcerersDungeon` row. CHANGELOG, Staff, one line.
5. Notes: `notes\cc-P??-tosd-own-automatic.md`. Last line `P?? DONE`.
```

### O2. The guild hall `clear` can delete a guildmaster it did not place, and leave its own (staff tool, wrong behavior, minor)

- **Where:** `server/customizations/ClusterFGuildHallPlacement.cs:69-86` (`FindNpc`: any mobile of the exact type
  within 1 tile of the post), `:208-219` (place skips when one is found), `:289-297` (clear deletes the one found).
- **What goes wrong:** the sign, building and doors are our own types and carry the hall key, but the guildmaster is
  found by type and place. Nine of the 18 types are pinned stock guildmasters (`MageGuildmaster`,
  `WarriorGuildmaster`, `HealerGuildmaster`, `ThiefGuildmaster` and others, in `ClusterFGuildHallPlacementData.cs`),
  and these halls are stock buildings. If a stock-spawned guildmaster of the same type is within a tile of the post,
  `place` reports it "standing" and places none. `clear` deletes the stock one (its spawner makes another) and
  leaves ours if both are there. That breaks the header's "clear removes exactly what place placed".
- **How it is hit:** staff on the test shard, in a stock building whose spawner puts the same guildmaster near the
  post. Whether any does needs the world on the game PC (P281's screenshots show the posts, not the spawners).

**Prompt draft:**

```
# CC task P??: guild hall placement remembers its guildmasters by serial

**Model:** Sonnet
**Touches:** server
**Golem:** any

**Summary:** cc-P281's placer finds a hall's guildmaster by type within a tile, so a stock guildmaster of the same
type stops ours being placed, and clear deletes the stock one. Remember the placed NPC as the sign remembers its
stock sign.

Found by cc-P477 (Crystal), finding O2. Do it with P281's two Codex findings (doors by closed position, the stock
sign after [SignGen) if those are not queued by then.

## What to do

1. `server/customizations/ClusterFGuildHallPlacement.cs`: keep the placed guildmaster's serial per hall (on the
   `GuildHallSign`, a new serialized field with a version bump, or in a small saved table). `FindNpc` checks that
   serial first. `place` places ours unless that one stands, and `clear` deletes only that one.
2. Tests (`server/tests/Misc/GuildHallPlacementVerification.cs`): a stock `MageGuildmaster` next to the post. Place
   puts ours too, and clear removes ours and leaves the stock one. Red first.
3. Build and run the tests (`docker\uo\build.sh -t sl-modernuo:cc-P??`). CHANGELOG, Staff, one line.
4. Notes: `notes\cc-P??-guild-hall-npc-by-serial.md`. Last line `P?? DONE`.
```

## Checked in the other merges, nothing new

- **P277 (rideable dragons):** both are `[Constructible(AccessLevel.GameMaster)]`, not tamable, and placed or sold
  by nothing. Bodies 2086 and 2087 are registered as Animal (`ShardBodyTypes.cs`). The stats are a stock horse's.
  The client side (rider height, package) is in P277's own notes.
- **P408:** the new `PointsType.SorcerersDungeon` is appended at the end of the enum, so saved points keep their
  meaning. `MinaxArtifacts.ApplyProperties` going public changes nothing for Blackthorn. `Remove` deletes only
  tracked serials. The spawner pauses only running stock spawners, saves them by serial and restarts exactly those.
  A spawn already queued in the 3-8 second delay can land in the next room during the 1-3 minute room change
  (ServUO's, harmless). The rest is in Codex's P408 review and P461.
- **P281:** test-shard guard on place, clear and runes. `go` has no guard, but it is Administrator and moves only the
  caller. The door and `[SignGen` findings are Codex's.
- **P410, P287, P288:** no `server/`, `client/patches/` or `docker/uo/` code, apart from P408's `COMMANDS.md` rows,
  which match the commands.

## What I could not check from GitHub alone

- Nothing was built and no test was run. P289's 93-check play-through was not re-run on the merged build (Codex's
  P475 notes ask for that too). Chase's test today is the first run of the merged tutorial.
- There is no live shard (retired and deleted 10-14, `README.md:112`), so T1 and O1 matter for the 1.0 live and
  the test shard only. Which build the test shard runs needs the game PC.
- Whether test-shard characters are Young (the death lesson's "your things come back" depends on it). Pinned's
  `Young` also needs `ContentFeatureFlags.YoungPlayerSystem`.
- Whether any stock spawner places a same-type guildmaster near a P281 post (O2).
- How many test-shard accounts already have more than one `loop:1` box (T2).

P477 DONE
