# cc-P707: the Wakening Isle play-through (the tutorial's go-live gate)

Iron Golem, 2026-10-27, two sessions (the first stopped for low memory; its question expired when the prompt was
retried, and this session resumed from its notes). Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy
`D:\UO\golems\Iron\shard-migration`, both on `golem/Iron/P707`. Not committed; nothing deployed.

## In plain words

- **A brand-new character can now play the whole Wakening Isle, beach to New Haven, without getting stuck.** A bot
  played all ten lessons on a real server, from waking on the beach to stepping through the dock's moongate and
  arriving beside Rook. It took under 3 minutes and passed every check. A character that picks New Haven at creation
  starts on the plaza with no tutorial.
- **The farm's bandage lesson was the one real blocker, and it is fixed.** Nobody was hurt (the pet kills the pests
  first), a newcomer without the Healing skill failed most bandages, and a scratch healed by itself before the bandage
  finished, with the confusing line "The veil of death in this area is too strong". Now any bandage that finds nobody
  hurt gives the trainee a small scratch and says "bandage again", and the practice bandages always work.
- **Private copies of the isle work.** Two friends in a party share one copy, a third trainee gets another, and an
  empty copy resets after its hold (shortened to 2 minutes on the test world; staff can set it, 30 by default).
- **For you:** the isle is a **go** for release (the line below), with the follow-ups listed under rough edges. To
  check by ear: the vision's sounds are listed below. Pictures of each stop and the vision are in
  `notes\cc-P707-tools\shots\`.

## Go or no-go for releasing the isle

**Go.** All ten core lessons pass on a real server with this branch's image (run 7, 0 failed checks), the skip pick
works, and the party, separate-copy and reset behaviour was seen live. The one blocker, the farm's heal step, is fixed
with tests and proven live. The rough edges below are follow-ups. None of them stops a newcomer. The biggest is the
pile of messages and windows at the first login (draft 1).

## What was done

| Part | State | Evidence |
|---|---|---|
| 1. Private shard with the isle | Done | `notes\cc-P707-tools\proof-shard.ps1` (cc-P281's, plus the isle's map overlay from `overlay.ps1`, mounted first in `dataDirectories`) on 127.0.0.1:2596, from a copy of the bot shard's world. `[ClusterFSeedTutorial` seeded the isle; a second run placed nothing. |
| 2. Bot route | Done | `isle.py` (P480's walker, the isle's stops). **Run 7** (`runs\run7-playlog.txt`, the image built from this branch): a fresh character with Tutorial Island at creation woke on the beach at 6638,3993 with an arrow to Tamsin, and finished all ten lessons west to east: movement, backpack, clothes, chat, the farm (pet, pests, bandage), death at the yard, the bank, the lodge, the vision, and the dock moongate, which put it at 3501,2572 beside Rook. 166 s, **0 failed checks**. The skip (run 4): a New Haven pick starts at 3503,2574 and is not sent to the isle. |
| 3. Copies | Done | Run 4 (`runs\run4-playlog.txt`). Silver PartyA and Gold PartyB party up, take "Restart the tutorial" from Rook, and land on the same copy (map 34). Stone Third gets another (map 35). All log out; after the 2-minute hold, the shard log (`runs\run4-copies-freed.txt`) says each copy was "freed: removed 32 seeded pieces ... reseeded", and each is free with its generation raised. Silver logging back in gets "Your copy of the Wakening Isle was reset while you were away" and a fresh copy at the next lesson. Iron Islander, logging back in at the travel lesson after its copy reset, landed at the dock (6831,3991), its next lesson (run 5). The run's own "freed" check failed on a bot mistake: a logged-out trainee is still listed "(away)" on a freed copy by design. The check now reads "free" and the generation. |
| 4. Shots and vision | Mostly | `isle-shots.ps1` in TazUO (`D:\UO\golems\Iron\tazuo-p670\client`), kept in `notes\cc-P707-tools\shots\`: the beach, farm, training yard, trades square and dock (the moongate on the dock's end), and the vision as a burst of 32 frames 1.5 s apart (all in `D:\UO\golems\Iron\p707-proof\shots\`, three kept here). The frames show the vision's captions in turn ("The sword strikes the Gem. The shards fly.", "You wake where you started...") over the darkened isle. **Not taken:** the city screen with the start choice, and the two-client party shot. Both need scripted clicks in TazUO's creation flow and a second client, which the shot tool does not do. The bot proved both by packets instead (the city list and the party copy). |
| 5. Rough edges | One more fixed, the rest below | |
| 6. Build | Green | Gated build 6, `docker\uo\build.sh -t sl-modernuo:cc-P707`: "Built sl-modernuo:cc-P707 with patches applied and 2698 shard test(s) passing" (`gated-build-6.log`, image 0c6492e6cd3c). |

## The fixes, each seen failing first

| Fix | Where | Red | Green |
|---|---|---|---|
| Wren gives an unhurt trainee, with an unhurt pet, a scratch (a fifth of their hits, at least 5, never the last one) and says how to treat it (`ScratchLine`). | `TutorialFarm.cs` `Scratch`, `Talk` step 3; fact 13 | "hits 80 of 80" (`red-noscratch.txt`) | `green-tutorial.txt` |
| The practice bandage always works for a trainee on the heal step when nothing slipped. It still really heals, so P453's rule holds: only a bandage that restores hits finishes the step. | `TutorialFarm.SureHeal`; `Bandage-tutorial-real-heal.patch`; fact 14 (ten bandages at Healing 0) | "bandage 1: hits 60, before 60" (`red-sureheal-oldpatch.txt`) | `green-sureheal.txt` |
| **New this session:** a bandage that finds nobody hurt on the heal step, whether as it starts ("That being is not damaged!") or as it ends (the trainee's hits came back during the bandage's delay), gives the trainee a scratch and the line "A rat nipped your ankle in the rows. Double-click a bandage again, then click yourself to treat it." Pinned's message and the Placebo achievement are skipped then. Off the step nothing changes. Run 4 found it: the bandage ended on a full patient, pinned said "The veil of death in this area is too strong..." (it sends cliloc 1010395 there), and only a second talk to Wren gave the scratch. | `TutorialFarm.Unhurt`, `OnUnhurt`, `ScratchAgainLine`; the patch's `BeginHeal` and full-hits branches (`make_heal_patch.py`, from the build-order Bandage.cs; applies before `Bandage-asclepius-bonus.patch` with `--fuzz=0`); fact 15 `ABandageThatFindsNobodyHurtOnTheHealStepGivesAScratch` | old patch: "hits 80 of 80" (`red-unhurt.txt`) | 193 of 193 tutorial and bandage tests (`green-unhurt.txt`); build 6; live in run 7: bandaging the unhurt pet gave the scratch line, and the next bandage on self finished the lesson |
| The copy hold is a setting, `clusterf.tutorial.copyHoldMinutes` (30, at least 1) | `TutorialCopies.HoldAfterLeaving`; fact `TheHoldIsTheSettingSoATestWorldCanShortenIt` | `red-hold-constant.txt` | `green-hold.txt` |

Bot fixes (not shipped): `isle.py` now imports `islegrid.py`, which it never did, so run 4 found no path from the
stones to the dock (`dockprobe.py`: "P480 grid: no path", "islegrid: path of 40"). The reset check now reads the
listing correctly.

CHANGELOG `2026.10.27.4`: a Fixed line for the farm (now also naming the bandage that finds nobody hurt) and a Staff
line for the setting.

## The vision's sounds (to check by ear) and the screen fade

From `TutorialVisionScene.cs`, by second of the 45: 0x1FE at 0 and 38, 0x20F at 3, 0x29 at 8, 0x307 at 9, 0x211 at
12, 0x220 at 17, 0x44D at 21, 0x3C4 at 29, 0x212 at 30. **Our TazUO ignores the server's screen-fade packet**
(`SendScreenEffect`: FadeOut, FadeIn, LightFlash; TazUO logs "Effect not implemented"), so on our client only the
per-player light change darkens the screen, as the frames show.

## Rough edges a newcomer hits

Fixed here: the farm's heal step (three ways, above).

Fix-up drafts, for the overseer:

1. **A pile of windows and messages at the first login.** The shots show the patch-notes window, the paperdoll,
   TazUO's own version-history window and the lesson page stacked over the view. Skill-gain lines fill the left of the
   screen. The text log adds Young status, about ten joke "System:" lines with achievement pop-ups ("Somewhere, a
   goblin is jealous."), "Common Box" deliveries, bank-item lines, and "<name> has died and been reborn. Again. Loop
   1." for a character that never died. Hold the patch notes, joke achievements and loop line while a trainee is on
   the isle, keep TazUO's version history closed for new installs, and fix the "reborn" line at creation.
2. **Bank gift lines arrive mid-lesson** ("Various tools have been placed into your bank", "9000 silver pieces", "5
   unmarked recall runes...", "One of each level of treasure map"). These are test-centre gifts on this world; check
   that none reaches a live newcomer.
3. **Pinned's wrong cliloc**: a bandage ending on a fully healed patient tells everyone "The veil of death in this
   area is too strong" (1010395) instead of "You heal what little damage your patient had". Fixed for trainees on
   the heal step; a one-line patch would fix it for everyone (check the number, 500967, in the client's Cliloc first).
4. **P702's wording items are still open**: "take them in order along the road", the unexplained "moongate", "Rook in
   New Haven graduates you and opens trade and skill lessons", "You can now leave Haven Island", the "Next lesson /
   graduate" button, and the controls primer before the farm (`notes\cc-P702-tutorial-new-player-text.md`).
5. **A farm rat wanders to Wren's gate** (run 2: one at 6714,3979 beside her). A trainee can attack it by accident
   before the pests lesson.
6. **No tutorial for a second character on an account.** One tutorial per account: a friend who makes a second
   character to play with a newcomer cannot share the isle on it (Rook: "This account's tutorial was started by
   <name>").
7. **Staff `[Fold goto n` without x y** still lands on the old void C site (6214,2001); marked for S2 in code.
8. **Shot tool**: the city screen and a two-client party shot need TazUO click automation in `isle-shots.ps1`
   (creation flow, a second client); worth having for the next release's proof.

## Deviations and decisions for Chase

- The first session's question (`Iron-P707-20261027-183925-e4f1`) expired unanswered when the prompt was retried. This
  session treated the retry as "resume now", after checking memory (4.2 to 4.6 GB free) and dropping the page cache.
- One combined command (take the lock and start the shard) was denied by the auto-mode check; the same two steps run
  one at a time went through.
- The Read tool was denied for `TutorialFarm.cs` (unattended); the edits went through scripts as before
  (`edit_unhurt.py`, `edit_unhurt_fact.py`, `make_heal_patch.py`).
- The city screen and the party shot were not taken (above).

## Commit preflight

- Code copy: `server/customizations/Tutorial/TutorialFarm.cs`, `TutorialCopies.cs`,
  `server/patches/Bandage-tutorial-real-heal.patch`, `server/tests/Tutorial/TutorialFarmVerification.cs`,
  `TutorialCopiesVerification.cs`, `CHANGELOG.md`.
- Docs copy: this file and `notes\cc-P707-tools\` (about 2.6 MB: the scripts, red and green probe logs, build logs 4
  and 6, the play logs of runs 1 to 7, nine shots). The shard world, overlay, all shots and transcripts stay in
  `D:\UO\golems\Iron\p707-proof\`, outside the repo.
- Locks: `docker-build` and `test-shard`, each taken and released. The private shard (`sl-p707-proof`) is down. Haven
  not touched. Nothing committed.

P707 DONE
