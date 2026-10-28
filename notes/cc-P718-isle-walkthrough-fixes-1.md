# cc-P718: fixes from Chase's walk of Tutorial Island (round 1)

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`, both
on `golem/Iron/P718`. The code copy is based on main at P675; P717 is not in it. Not committed, nothing deployed,
Haven not touched.

## In plain words

- **The isle's people speak first (test shard).** Tamsin on the beach, Wren at the farm gate and Elara in the lodge
  now say "Double-click me (two quick left clicks on me)..." over their heads when a new player comes near. They say
  it again every 30 seconds until the player has used them.
- **The cloak is a keepsake, and the clothes lesson is real.** The blue "cloak of the Wakening Isle" now waits on a
  table by the clothes rack, and the player drags it onto their character to wear it. It is theirs for good: kept on
  death, and it can't be sold, traded, banked or dropped. The backpack lesson now starts by opening the character
  window (double-click yourself) and waits until the player does.
- **The farm is calmer and teaches more.** The rats and snakes stay inside the field fence, behind a new gate, and
  ignore players until their pest lesson. Wren first teaches "all follow me" and "all guard me", then opens the gate.
  She hands over bandages, says how to use them, and how to make more with scissors and cloth. On the isle each skill
  now rises at most once every 10 seconds, so a rat fight no longer floods the screen. The signposts are proper
  standing posts.
- **For you:** walk the isle again on the next test build. Please look at the field gate, the clothes table and the
  new signposts; I couldn't take in-game pictures. Decide whether the cloak should give a small bonus (none for now;
  options below). The 200 you saw as the Tactics cap is the shard's real cap today: F-12's lower caps for the first
  loop aren't built yet.

## The items

| # | What Chase saw | What changed | Where (code copy, `server/customizations/`) |
|---|---|---|---|
| 1 | A newcomer doesn't know to double-click Tamsin | Tamsin, Wren and Elara say a "Double-click me" line to the one player (SayTo) when that player comes within 8 tiles, and again every 30 s while the player stays near, from the NPC's AI think. Each stops once used: Tamsin once double-clicked (or once a lesson is done or running), Wren once the pet is chosen, Elara once the League lesson is done. The other NPCs a trainee must double-click were checked. Sera is double-clicked as a ghost, after the lesson's own line points at her. Merrin answers "bank". Tobin is optional. Rook is in New Haven. None of them got a greeting. | `Tutorial/TutorialGreeting.cs` (new); `TutorialGuide.cs`, `TutorialFarm.cs` (Wren), `LeagueRegistrar.cs` (Elara) |
| 2 | The cloak is taken away | A new `WakeningIsleCloak`: blessed, and `Nontransferable`, which pinned uses to refuse a drop on the ground, into any container but the backpack, onto another mobile, a trade and a vendor sale. It has an owner. Nothing deletes it at the lesson's end, the skip, graduation or leaving the isle. It is no longer the lesson's "supply", which `Cancel` used to delete. Characters who already left without one get none. | `Tutorial/TutorialCorePlacement.cs`, `TutorialCoreTrials.cs` |
| 3 | No way to learn client settings | An optional lesson, "Client tips: always run", offered at any time in Tamsin's and Rook's windows and never needed to graduate. P719's notes aren't in main yet, so the path comes from our TazUO's own source: Options, then Gameplay, then Movement, then "Always run" (`MovementTab.cs`, `language.ini` `mog_movementtab_running_alwaysrun`). The page also has a button that opens TazUO's options window, for clients that answer our command handshake. More tips are added as rows of `TutorialClientTips.Tips`. "Done" finishes the lesson: the server can't see a client setting, and an optional page needs no evidence. | `Tutorial/TutorialClientTips.cs` (new), `TutorialStations.cs` (station `client.tips`, wing `Client`), `TutorialGumps.cs` |
| 4 | New clients start with the paperdoll closed | The backpack lesson comes first and is the first that needs the character window, so I put the step there rather than in the clothes lesson. Its first step is to open the character window ("double-click your own character, or click the paperdoll button"). That is seen through pinned's `EventSink.PaperdollRequest`, which both routes raise. Only then does opening the practice bag count. The clothes lesson's hint still says to drag onto the character window. | `TutorialCoreTrials.cs`, `TutorialTrialProgress.cs` (`OpenedPaperdoll`) |
| 5 | The cloak starts in the bag | A table (stock 0x0B8F) beside the clothes rack, and the trainee's own cloak lies on it. Only its owner (or staff) can lift it. The hint teaches drag and drop. The lesson is done when the cloak is worn, whether dragged onto the paperdoll or double-clicked from the bag. One cloak per character: a restart puts no second one out, a lost one comes back on the table with "Hint and arrow", and none is placed while they have theirs. | `TutorialCorePlacement.cs` (`ClothesTable`, `WakeningIsleCloak.EnsureOnTable`) |
| 6 | The farm signpost reads as debris | The old art, 0x0B97, is the arm that hangs a shop sign from a wall, so on the ground it looks like a stick. Both isle signposts are now stock 0xA854, a standing post with its sign board. The chat post is named "Farm signpost: say 'I am ready to learn'", and the lesson's arrow now points at the post itself, not the stop in front of it. The seeder removes the old post. The farm gate's sign (0x0B97 plus a board, 0x0BCF) is the same standing post, named "Farm signpost: Wren the Farmhand at the gate". The generated farm layout is unchanged. The isle's farm addon swaps the art as it is built, and `FixGateSign` mends a farm placed before. | `TutorialCorePlacement.cs`, `TutorialFarm.cs` |
| 7 | Rats attack at once and can reach the player | A pest fights only a trainee on the pest part of the farm lesson, or that trainee's pet. To anyone else it is not an enemy, can't harm them, and takes no damage from them. A pest never steps outside the field fence (`CheckMovement`), so it respawns and stays inside. The field gets a gate in its east gap that only a trainee on the pest part (or later) or staff can open. Wren opens it when the pest part starts. It closes by itself like any gate, and the trainee double-clicks it to open it again. | `TutorialFarm.cs` (`FarmPest`, `TutorialPestGate`, `PestField`) |
| 8 | Skill-gain spam, "12.2 / 200" | Cause and fix below. | `Tutorial/TutorialSkillPace.cs` (new), `Fold/FoldRegions.cs`, `ClusterFSkillGain.cs` |
| 9 | Bandages are never explained | When Wren hands the bandages: "Here are some bandages. To heal, double-click a bandage in your backpack, then click yourself or your hurt pet...", then "Later you can make your own bandages: double-click a pair of scissors, then click a pile of cloth to cut it into bandages." The step still counts once a bandage really heals. | `TutorialFarm.cs` |
| 10 | Pet commands are never taught | Step 2 now begins with the commands. Wren tells the pet to stay and explains "all follow me", "all guard me", the pet's name instead of "all", and the pet's right-click menu. The evidence is the pet's own order, so speech and the menu both count. Follow comes first, then guard, then the pest part opens. At least one pest must fall to the pet under "all kill": "Now let your pet fight one: say 'all kill'...". With no pet along, the commands are skipped. | `TutorialFarm.cs` (`BeginCommands`, `CheckCommands`) |

### Item 8: why the gains came so fast, and the cap

- **Why.** Every swing rolls Tactics and Anatomy (pinned `BaseWeapon.cs:2524`, `:2527`), on the window 0 to the
  skill's cap. At 11.6 against the cap of 200, pinned's gain chance is about 0.48 a roll (`SkillCheck.cs:122-131`).
  The shard rolls it twice (P191's 2 attempts), so each skill gained on about three swings in four. Below 10.0, pinned
  gains on every use. There is no isle boost (the apprentice training region is Old Haven's woods only) and no bug: it
  is the shard's rate at the bottom of a 200 cap.
- **Fix.** On the Wakening Isle and its copies, a player gains each skill at most once per 10 seconds (setting
  `clusterf.tutorial.gainSecondsPerSkill`; 0 turns it off). The Fold's region refuses the roll inside that window
  (`FoldRegion.AllowGain`), and every gain is noted (`ClusterFSkillGain.ObserveAttempt`). Off the isle nothing changes.
- **The 200.** It is the real cap a new character has today (`ClusterFSkillCaps`, D64), so the display is correct.
  F-12's ladder (50 in loop 0) is not built (`ClusterFLoops.ResetLevelAndSkillsForF12` is empty), and P709 says not to
  pretend to enforce it. Nothing was changed there. When F-12 is built, the isle's cap will come with it.

### The cloak's bonus: a proposal (not built)

None for now. If you want one, any of these suits a brand-new character and stops mattering soon after:
- **+1 Hit Point Regeneration while Young** (off once Young ends). This is my pick: small, and gone when Young is.
- **+5 Physical Resist** (a newbie cloak's worth; outclassed by any real armor).
- **+1 Luck** (cosmetic, symbolic).

## Decisions and deviations

- **The paperdoll step is in the backpack lesson, not the clothes lesson.** The prompt said the clothing step "or" the
  first lesson that needs it. The backpack lesson comes first and already opens the backpack from the character
  window.
- **The field gate is one gate, not two halves.** Every wooden gate's art is impassable open or shut (tiledata 0x0841
  to 0x0848), and pinned swings a gate in a north-south fence one tile east (`BaseDoor` offsets). So two halves stood
  on both tiles outside the gap, Wren's and the one below it, and nobody could get in (bot run 2). Now it is one gate
  on the gap's south tile, swinging onto Wren's own tile, and a plain fence piece (0x0837) closes the gap's north
  tile. **Please look at it in game**: I could not take a picture.
- **An older bug fixed on the way:** a copy of the isle whose seeding was refused (the isle's land was missing then)
  was still marked "seeded (0 pieces)" and never seeded again. The overnight bot's world had six such copies, and bot
  run 1 woke a trainee on an empty copy. Now a copy counts as seeded only if something was placed, and a claim reseeds
  an empty one (`TutorialCopies.cs`). If the shared test shard has such copies, they mend themselves at their next
  use.
- **Greeting and gain timers use `Core.TickCount`**, not `Core.Now`. A test host's NetState resets `Core.Now` to the
  wall clock as it sends (D16), so the first version could not be tested. In the shard both clocks move together.
- **The Read tool was denied** (unattended run) for `TutorialCoreTrials.cs` and for the new test file part-way
  through. Edits went through Python scripts instead (`notes\cc-P718-tools\edit_*.py`). Nothing was skipped.
- **The Client tips "Done" button is an acknowledgement, not evidence.** The core lessons' rule (evidence only) is
  kept for the core. This lesson is optional and the server cannot see a client setting.

## Facts

New: `server\tests\Tutorial\TutorialIsleWalkFixesVerification.cs`, with 10 facts:
- Tamsin greets on approach, not again within 30 s, again after it, never out of range, and stops after use.
- Wren greets until the pet is chosen.
- The cloak: on the table, owner only, one per character, comes back when lost, can't be dropped, the lesson is done
  when worn, and it is kept after the skip, off the isle.
- The client tips are in Tamsin's window before the core is done, finish with Done, and are not core.
- The backpack lesson waits for a real PaperdollRequest.
- The signposts: standing and named, the arrow points at the chat post, the old post is removed, and the farm's gate
  sign is mended in place without losing the farm.
- Pests ignore earlier trainees and their pets, the gate opens only on the pest part, and pests can't step out of the
  field.
- The isle's gain pace (one gain per interval, per skill), while off the isle the gain on every swing is unchanged.
- Wren's bandages and lines.
- The pet commands, in order, with the pet's kill.

Also new, in `TutorialCopiesVerification.cs`: a copy whose seeding placed nothing is seeded again at the next claim.

Changed facts, for the intended behaviour:
- The backpack evidence (character window, then bag) in the tutorial test helpers and `TutorialTrialProgressVerification`.
- `TutorialVerification`'s real-hook walk (now opens the character window, and takes the cloak from the table).
- The station list (adds `client.tips`): `TutorialVerification`, `TutorialTradeTrialVerification` (39 stations, 28
  wing stations not counting the any-time one).
- Rook's menu shows the any-time lesson before the core is done (`TutorialFirstPlayVerification`).
- The supplies fact no longer counts the cloak as a supply.
- The farm seeder counts the gate and its fence piece, and the addon's sign art (`TutorialFarmVerification`).
- The farm's pest flow does the commands first.
- `TutorialCopiesVerification`'s pest fact marks the commands done.

**Seen failing first.** The new API doesn't exist before the change, so as in P663 and P717,
`notes\cc-P718-tools\mutate.py` writes copies of the code with behaviour put back, and `probe.sh` runs the facts on
`sl-uo-builder:cc-P675` with the copy mounted (`redrun.sh`; summaries in `notes\cc-P718-tools\red\`):

| Copy | What it puts back | Failed |
|---|---|---|
| `old` | Every item as before P718: no greetings; the cloak in the bag and transferable; no any-time tips; the bag alone finishes the backpack lesson; the old signposts and arrow, no swap, no mending; pests fight any trainee and roam; no gate check; no isle pace; the old bandage lines; no commands and no pet kill | **10 of 10** new facts, each on its own item |
| `fine` | Greetings with no interval | Tamsin's and Wren's greeting facts |
| `fine2` | Greetings that never stop after use; Wren past the pet; the cloak taken back when the lesson ends | Both greeting facts and the cloak fact |
| `copies` | Refused seeding still marked seeded, and never retried | The new copies fact (8 of 9 others pass) |

The `old`, `fine` and `fine2` copies were run before the field gate became one gate. The pest fact failed there on
the pests fighting an earlier trainee, which that change does not touch.

Then green: 200 of 200 tutorial tests on the probe (`green-tutorial.txt`).

## Build

`docker/uo/build.sh -t sl-modernuo:cc-P718`, run detached under the `docker-build` lock (released each time). Windows
had 1.2 to 5.8 GB free, after dropping the Docker VM's page cache each time.
1. Green: 2708 passed, 0 failed, 6 skipped.
2. Green: 2709 passed, with the copies fix.
3. **Green, `EXIT=0`**: "Built sl-modernuo:cc-P718 with patches applied and 2709 shard test(s) passing." 2715 tests:
   2709 passed, 0 failed, 6 skipped (the usual client-data facts). This build has the one-gate field
   (`gated-build-3.log`).

## The bot route: green

This is P707's route (`isle.py`), copied to `notes\cc-P718-tools\isle.py` and changed for these lessons. It opens the
character window first, takes the cloak from the table, says "all follow me" and "all guard me", and opens the field
gate if it has shut, from either side. After a scratch it bandages itself at once. Rook's and the New Haven start's
spots were updated for P678's move. It ran on P707's private shard (`proof-shard.ps1`, port 2596, a copy of the
overnight bot's world, the isle overlay), under the `test-shard` lock (released). The shard is down.

| Run | Result |
|---|---|
| 1 | Woke on an empty copy: the copy seeding bug above. Fixed, rebuilt. |
| 2 | Every new step passed (character window, cloak from the table, both commands), then no way into the field: the two gate halves. Fixed (one gate), rebuilt. |
| 3 | Into the field, pests cleared in 34 s. The heal failed on bot timing: the pet was guarding in the field ("That is too far away"), and the scratch regenerated while the bot went back to Wren. Bot fixed. |
| 4 | Not fresh (the account's tutorial was run 3's character); restarted on a fresh world. |
| 5 | All ten lessons; the bot also has to open the gate from inside to leave the field (a player double-clicks it). Bot fixed. |
| **6** | **0 failed checks.** A fresh character went from the beach to beside Rook in 147 s (farm 51 s, pests 20 s). Tamsin, Wren and Elara each said their "Double-click me" line as the bot came near. (`runs\run6-playlog.txt`, `runs\run6-console.txt`) |

## Not done

- **No in-game pictures** of the gate, the table, the signposts or the client tips page. The isle shot tool needs a
  TazUO session, and it wasn't worth the time this round. The bot proved every one by packets, and the greetings by
  their overhead lines.
- **No package change** is needed: no new clilocs, and all the art is stock.
- **Nothing deployed.**

## Files

- Code copy: `CHANGELOG.md` and `VERSION` (2026.10.28.2).
- `server/customizations/`: `ClusterFSkillGain.cs`, `LeagueRegistrar.cs`, `Fold/FoldRegions.cs`, and in `Tutorial/`:
  `ClusterFTutorial.cs` is untouched; changed are `TutorialCopies.cs`, `TutorialCorePlacement.cs`,
  `TutorialCoreTrials.cs`, `TutorialFarm.cs`, `TutorialGuide.cs`, `TutorialGumps.cs`, `TutorialStations.cs` and
  `TutorialTrialProgress.cs`; new are `TutorialClientTips.cs`, `TutorialGreeting.cs` and `TutorialSkillPace.cs`.
- `server/tests/`: in `Tutorial/`, `TutorialIsleWalkFixesVerification.cs` (new), `TutorialCopiesVerification.cs`,
  `TutorialFarmVerification.cs`, `TutorialFirstPlayVerification.cs`, `TutorialIsleVerification.cs`,
  `TutorialTradeTrialVerification.cs` and `TutorialTrialProgressVerification.cs`; and `Misc/TutorialVerification.cs`.
- This repo: this file, and `notes\cc-P718-tools\` (`probe.sh`, `mutate.py`, `redrun.sh`, `red\`, `isle.py`,
  `islegrid.py`, `runs\`, the edit scripts, the build log and the green log; 1.1 MB).

P718 DONE
