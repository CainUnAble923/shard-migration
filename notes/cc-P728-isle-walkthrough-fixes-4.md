# cc-P728: fixes from Chase's walk of Tutorial Island (round 4)

Iron Golem, 2026-10-28. Code copy `D:\UO\golems\Iron\ShatteredLegacy`, docs copy `D:\UO\golems\Iron\shard-migration`,
both on `golem/Iron/P728`, from main `56c0038` (P727 has landed P721 there). Not committed, nothing deployed, Haven not
touched.

## In plain words

- **Waking on the beach (test shard).** A new character now lies on the sand until the player moves. The first move
  gets them up and the first lesson starts. After 8 seconds without a move, "Move to get up." shows, and after a minute
  they get up anyway. Nothing else pops up while they lie there: the patch notes, the first achievement window and the
  welcome lines come 2 seconds after they stand, and the guild welcome waits until the character is in town.
- **The cloak comes in a chest.** At the clothes stop a chest appears (with a sparkle and a chime) holding the cloak.
  Double-click the chest, then drag the cloak to the backpack or onto the character. Only that player can open it, and
  it vanishes once they have the cloak. It comes back with a new cloak if the cloak was lost.
- **The farm fight starts with the pitchfork.** Right after the pet is chosen, Wren hands the pitchfork. The order is
  now: hold it, war mode, the pet's commands, then the rats and snake. When the rows are clear, Wren, the System and the
  lesson window all say "The cabbage rows are clear! Go back to Wren..." and the arrow points at her. Wren never says
  "0 more" now. Every finished lesson names the next one and points at its signpost, and typing `[lesson` opens the
  lesson window again.
- **Pip and other new isle pieces appear by themselves.** At every restart of the test shard, anything the isle should
  have and is missing (like Pip) is put out on the isle and on every copy, and the server log lists it.
- **For you:** walk the isle again on the next test build. Please check how the character looks while lying for a long
  time: the server cannot hold the fallen pose, so the client may draw them standing in the dark until they move (see
  "Decisions" below). Nothing else to decide.

## The items

| # | What Chase saw | What changed | Where (code copy, `server/customizations/` unless said) |
|---|---|---|---|
| 1 | Too many popups at the first login; the washed-ashore moment lost | The first login's other windows and lines wait in a hold (`TutorialWake.Hold`) until the trainee has stood up, and come 2 s after that (`HeldDelay`). A handler that runs before the tutorial's login handler sees the pending isle choice (`TutorialStart.WillWake`, read without side effects); one that runs after sees the trainee lying. If no wake-up plays (every copy in use, no client), the tutorial's login handler releases the hold at once. A disconnect while lying drops the hold; the next login runs the handlers again. The full list is below. | `Tutorial/TutorialWake.cs`, `TutorialStart.cs`, `ClusterFTutorial.cs`, `ClusterFAchievements.cs`, `ClusterFBulletin.cs`, `ClusterFGuildStarterPath.cs`, `CharacterCreation.cs` |
| 2 | Stay down until the player moves | No timed stand. The first move request, a step or a turn, gets the trainee up and is spent on it (the step is refused). Pinned refuses a frozen step in `Mobile.CanMove` before `EventSink.Movement` or any region hook, and lets a frozen turn through with no hook at all, so this needs one call at the top of `PlayerMobile.Move`: `server/patches/PlayerMobile-tutorial-wake-move.patch` (below). Each second while lying the light comes up as before, the waves wash every 6 s, "Move to get up." comes at 8 s (System line and over their head), and at 60 s they get up anyway. | `Tutorial/TutorialWake.cs`, the new patch, `docker/uo/apply-patches.sh` |
| 3 | The cloak in a chest that appears | `TutorialCloakChest`: a wooden chest (bright cyan, the lesson props' hue) appears on the clothes table for one trainee, with a sparkle (0x376A) and pinned's sparkle sound (0x1F5), holding their cloak. Only its trainee or staff can open it or take from it; nothing can be dropped in. It vanishes (a puff) once the cloak is out and on them, worn or in the backpack. One cloak per character as before: a trainee with no cloak gets the chest again with a new cloak at the lesson's start, restart or Hint and arrow; one who has theirs gets none. In a party (one copy), a second chest goes on the nearest free tile beside the table. A cloak still lying loose on the table from P718 is taken off it. The hint now says: double-click the chest, then drag the cloak to the backpack or onto the character. | `Tutorial/TutorialCorePlacement.cs` (`TutorialCloakChest`), `TutorialCoreTrials.cs` |
| 4 | The pitchfork comes too late | Once the pet is chosen, the combat part starts with the weapon: Wren hands the pitchfork with how to hold it (drag to the hand on the character window, or double-click it), then war mode, then the pet's commands (follow, then guard), then the gate opens on the pests (`BeginCombat`, `CheckCommands`). With no pet along at war mode the commands are skipped. A trainee who did the commands under the old order goes straight on to the pests once armed and in war mode. | `Tutorial/TutorialFarm.cs` |
| 5 | The pet before the pests | Not changed here (P726). The order now is pitchfork, war mode, commands, pests. P726 moves the pet and its commands after the pests by moving those two pieces alone: the weapon and war mode no longer depend on the commands, and nothing here reads the pet before the pests except the commands themselves. | |
| 6 | "Defeat 0 more", no next step after the pests | Wren's pest-part line is `PestsNow`: the pests to go, or, with the count reached, what is still missing (the pet's kill on "all kill", or the trainee's own strike). It never says "0 more". When the rows are clear (`Cleared`): Wren says "The cabbage rows are clear! Go back to Wren at the farm gate and double-click her." over her head, the same goes over the trainee's head and in the System line, the lesson window comes back (even if closed) with that line at the top as "Now: ...", and the arrow turns to Wren. Wren's next answer spends the line. **Every lesson's end**: "Lesson finished: X." used to be all, with the arrow stopped. Now the next lesson is named in the System line and over the trainee's head, with "Click Next lesson in the lesson window, or follow the arrow to its signpost and double-click it", the arrow points at that lesson's signpost (double-clicking it starts the lesson), and "If you closed the lesson window, type [lesson and press Enter" (also on the finished window). **`[lesson`** is a new player command: the running lesson's window again (with its "Now" line), or the next lesson's. | `Tutorial/TutorialFarm.cs`, `TutorialCoreTrials.cs` (`NowStep`, `PointToNext`, `Reopen`, `TutorialTrialGump.Now`) |
| 7 | Pip missing, no bandages, after an update | A new setting, `tutorial.seedMissingOnLoad` (true), runs the idempotent isle seed at every world load while the tutorial is on (the test shard now; live once the isle opens there): the Fold's isle (with Rook and New Haven's vet), then every seeded copy, which gets what its seeding places now and lacks (`TutorialCopies.TopUpSeeded`). The new pieces join what the copy's reset removes. Copies not seeded yet are seeded at their next claim, as before. The server log says what was placed. A new setting, not the old `tutorial.seedOnWorldLoad` (false), because that one is already written as false in each shard's config; the old one still forces the seed as before. | `Tutorial/TutorialRecruiter.cs` (`TutorialSeeder.SeedMissing`), `TutorialCopies.cs` |

### Every gump and message a new character gets at the first login (server side)

Read from every `PlayerLoginEvent` handler in the code copy (19) and in pinned (24), and from character creation. Only
the visible ones are listed; the rest send nothing a player sees (caps, bank limit, recipe sync, League title and pack,
companions, guild ranks, music, tree stumps, the exploration and depletion packets, the TazUO handshake, Rootdeep and
Despise, the vision's and the wing lessons' recovery after a cut-off login, and pinned's party, plants, virtues, pets, gifts (accounts older than the gift's start only) and polls (only
while a poll runs)).

| What | From | Now |
|---|---|---|
| "You wake on cold sand, soaked and aching..." and the dark light, the waves | the tutorial (`TutorialWake.Play`) | **the scene**: first and alone |
| "Move to get up." (8 s without a move) | the tutorial | new (item 2) |
| "You wake on a quiet shore: the Wakening Isle." and "Follow the arrow and double-click Tamsin...", arrow to Tamsin | the tutorial (`TutorialStart.SendToIsle`) | after standing (as before, now at the first move) |
| "Still Breathing" achievement window, its fanfare (System line, line over the head, sparkle and sound) and its loot box ("You have received a Common Box!"), plus any skill or login-count achievement the new character already meets | `ClusterFAchievementSystem.OnLogin` | **held**: 2 s after standing |
| The patch notes and unread bulletins (`BulletinGump`) | `ClusterFBulletinSystem.OnLogin` (2 s after login) | **held**: 2 s after standing, then its own 2 s |
| "Welcome to New Haven" guild window (Guild Board) | `GuildWelcome.OnLogin` | **cut on the isle**: not shown on the Fold, and not marked shown, so it comes at the character's first login in town |
| "Welcome to Shattered Legacy." (and on a test center 11 more lines about the bank, every 10 s for two minutes) | `CharacterCreation` (pinned's `WelcomeTimer`) | **held, and the greeting alone** for a character waking on the isle; the bank lines are cut there (the bank's contents are unchanged) |
| "You will enjoy the benefits and relatively safe status of a young player for N more hours." | pinned `Account.OnLogin` | **kept**, at once: one line, and moving it needs a patch to pinned for little gain |
| "Welcome, X! There are currently N users online..." | pinned `LoginStats` | not sent: nothing calls it in pinned |

TazUO's own first-run pages are client side (P729).

## The patch: `PlayerMobile-tutorial-wake-move.patch`

One call at the top of `PlayerMobile.Move`: `if (Server.Tutorial.TutorialWake.OnMoveRequest(this)) return false;`. It
is true only while that trainee lies on the beach (a dictionary lookup otherwise). Made with `diff -u` against the
`PlayerMobile.cs` that every earlier patch leaves (pinned plus the 14 patches that touch it, applied in
`apply-patches.sh` order with `--fuzz=0`), registered after `PlayerMobile-craft-order-hurt.patch`, checked with
`patch --fuzz=0 --dry-run`, and reported "Applied" in the gated build.

Alternatives, and why not:
- **No freeze, a region hook** (`FoldRegion` refusing the step through `Region.CanMove`): catches a step but not a turn,
  which changes the server's facing with no hook, and an unfrozen body could be pushed. Most first key presses are a
  turn.
- **No freeze, a timer watching the direction and the location**: catches both, but late (up to the timer's period),
  and the client has already drawn the character turning or stepping while "lying".
- **`EventSink.Movement`**: pinned raises it only after the frozen check (`Mobile.CanMove`), so a frozen trainee never
  reaches it, and turns never raise it.
- **Watching for pinned's "You are frozen" message**: sent through `SendLocalizedMessage`, with no hook.

## Decisions and deviations

- **The pose while lying.** The server cannot hold the fallen pose: a client shows an animation for its length, then
  draws the character in its usual stance. P721's wake-up was 5 s, so this hardly showed. Now a trainee may lie much
  longer, and a client may draw them standing in the dark until they move. The dark, the waves and the lines still say
  it, and "Move to get up." comes at 8 s. I wanted to read TazUO's source for how it ends a death animation sent by the
  server (`D:\UO\TazUO\src`, a Grep for `AnimationFromServer|AnimationInterval`); the unattended run denied it. **For
  Chase:** please look at it in game; if it shows standing, P729 (client side) could hold the last frame.
- **The first move is spent on getting up.** The step (or turn) is refused and the trainee gets up; the next one walks.
  That matches "the first move makes them get up".
- **The chest is movable, but nobody can lift it.** Pinned lets nothing be lifted out of an immovable container: the
  first bot run's lift came back CannotLift, and a host probe (`cc-P728-tools\ChestLiftProbe.cs`) showed the same for a
  plain cloak in a plain immovable wooden chest, while a movable chest worked. So the chest is movable, refuses its own
  lift for players (`CheckLift`), and never decays. A fact now lifts the cloak through pinned's own `Mobile.Lift`, and
  fails (CannotLift) with the chest immovable (`red-immovable.txt`). On the way I tried making the cloak transferable
  while in its chest; the probe showed that was not the cause, and it was reverted.
- **The guild welcome waits for town** rather than being held until standing: on the isle no Guild Board or guild is in
  reach. A trainee who goes to New Haven through the moongate sees it at their next login there.
- **The test center's eleven bank lines are cut for a trainee waking on the isle**; they were the bulk of the "welcome
  texts". The bank's contents are unchanged, and a character starting in New Haven still gets all of them.
- **A finished lesson's arrow points at the next lesson's signpost**, not at the lesson's own spot: the signpost starts
  the lesson on a double-click, and walking to the spot alone does not.
- **Denied in this unattended run, as the rules ask me to list them:** the Read tool on the code copy's files (edits
  went through Python scripts in the scratchpad, as P718's did; nothing was skipped); a Grep of `D:\UO\TazUO\src` (above);
  a Grep of `D:\UO\ModernUO-pinned\Projects\Server\Mobiles\Mobile.cs` for the lift's refusal reasons (I wanted to know
  which check refused the chest's cloak; the host probe answered it instead).
- **The isle-only branch.** `release/isle-20261028` has the same `PlayerMobile` patch stack as main (no `PlayerMobile`
  patch differs), and every line these edits anchor on is there in the same form (`ClusterFGuildStarterPath.cs`,
  `CharacterCreation.cs`, `ClusterFAchievements.cs` and `ClusterFBulletin.cs` differ from main elsewhere, not at these
  lines; the tutorial files these edits touch are identical). So this change should cherry-pick onto it as it is,
  patch included. Its bot route needs P722's New Haven spots (`make_isle_bot.py` here works from P727's route; P722's
  differs only in Rook's and the New Haven start's spots).

## Facts

New: `server\tests\Tutorial\TutorialIsleWalkFixes4Verification.cs`, 6 facts:
1. The first login's windows wait until the trainee stands up: the first achievement is not earned and has no window
   while lying (its handler ran before the tutorial's), it comes 2 s after the first move, and the guild welcome is not
   shown on the isle.
2. The trainee lies until their first move: still down at 38 s, the light up, the move refused and spent getting up,
   unfrozen, the next move an ordinary one; another trainee gets up at 60 s; a disconnect ends the lie.
3. The cloak in a personal chest: on the table, owned, the cloak inside, nothing loose on the table, the hint; nobody
   carries the chest off; another trainee cannot take from it; nothing goes in; a restart makes no second chest; lifted
   with pinned's `Mobile.Lift` into the backpack, the chest vanishes and no new one comes; lost, Hint and arrow brings
   it back with a new cloak; worn, the lesson is done and the chest goes.
4. The farm fight: the pitchfork at once with Wren's line, the commands not counting before the weapon and war mode,
   then war mode puts the pet on stay, follow and guard open the pests; an old-order trainee goes straight on.
5. The cleared rows and every finished lesson: Wren names the strike still missing (never "0 more"); the last pest
   brings back the closed lesson window with "Now: The cabbage rows are clear!...", and the arrow; `[lesson` reopens it;
   Wren's answer spends it; a finished lesson sets the arrow, and `[lesson` opens the next lesson's window.
6. The seed at load: Pip removed from a seeded copy comes back and is recorded for the reset; nothing while the
   tutorial is off; nothing more the second time.

Changed, for the intended behaviour: P721's wake fact and its "awake" helper (up at the first move), P721's pitchfork
fact (the pitchfork first), P718's cloak fact (from the chest), P718's pest-gate and pet-command facts and P276's farm
fact (the new order), and `TutorialVerification`'s real-hook walk (the cloak from the chest).

**Seen failing first** (`cc-P728-tools\probe.sh` mounts the code over `sl-uo-builder:cc-P727`; `mutate.py` writes a
copy of the customizations with each item's behaviour put back behind the new API):

| Run | What it puts back | Failed |
|---|---|---|
| `old`, without the patch (`red-old.txt`) | nothing held; up at 5 s; the cloak loose on the table; the pitchfork after the commands; "Defeat 0 more", the old echo line, no next-lesson pointer; no top-up of the copies | **6 of 6**, each on its own item |
| the real code without the patch (`red-nopatch.txt`) | `PlayerMobile.Move` as pinned's | facts 1 and 2, at "up after the move" |
| an immovable chest (`red-immovable.txt`) | the chest as first written | fact 3, at the lift: CannotLift |

Then green: the 6 new facts, and 486 of 487 tutorial, achievement, guild, bulletin, creation, Haven and graduation facts
(1 skipped, the client-data fact; `probe3.txt`).

## Build

`docker/uo/build.sh -t sl-modernuo:cc-P728`, detached, under the `docker-build` lock (released each time), after
dropping the Docker VM's page cache. Windows had 0.8 to 4.4 GB free; other Golems were busy.
1. Red: `CommandDeclarationVerification` wants every registered command to declare its category; `[lesson` had none.
   Fixed (`[ShardCommand(CommandCategory.Player)]`).
2. Green, `EXIT=0`, 2741 passed. Then the bot run found the chest's lift (above).
3. **Green, `EXIT=0`**: "Built sl-modernuo:cc-P728 with patches applied and 2741 shard test(s) passing." 2747 tests:
   2741 passed, 0 failed, 6 skipped (the usual client-data facts). `PlayerMobile-tutorial-wake-move.patch`: Applied
   (`green-gated-build.txt`, `gated-build-3.log`).

## The bot route: green

`cc-P728-tools\isle.py`, made by `make_isle_bot.py` from P727's route, on the private shard (`proof-shard.ps1`, port
2596, a fresh copy of the overnight bot's world, P727's isle overlay: its map-ops hash is this branch's), under the
`test-shard` lock (released). The shard is down.

| Run | Result |
|---|---|
| 1 | The bot looked for the cloak under the wrong key (`parent`, where the client keeps `container`). Fixed in the route. |
| 2 | The cloak's lift came back into the chest: the immovable chest (above). Fixed, rebuilt. |
| 3 | **0 failed checks** (`runs\run3\playlog.txt`), the isle in 166 s. |

Run 3, the new checks: "You wake on cold sand"; "Move to get up."; still lying, no first-lesson lines and **no window
opened while lying**; the first step refused, spent getting up; then "You wake on a quiet shore" and the arrow to
Tamsin. A chest appears by the clothes rack; opened, the cloak inside; dragged to the paperdoll; the chest vanishes.
Wren hands the pitchfork first; held; war mode; "all follow me"; "all guard me", and the gate opens; the pests cleared;
**the lesson window says "Now: The cabbage rows are clear..." and the arrow points at Wren**; Wren never said "0 more".
Then the rest of the isle as before, the moongate to Rook at 3632,2584, and the New Haven pick on the plaza.

**Item 7 on a real world**: both proof shards logged at load "Seed on load, the Fold: Tutorial: placed 10 station
markers, 8 NPCs/echo/vets, 1 moongate, 2 walking tiles, 2 doors, 8 props. Tutorial farm on the isle: placed 1 farm
addon, 3 door, 2 Farmhand, 2 spawners" (the bot world's Fold had never been seeded) and "the copies: nothing missing"
(correct: its six seeded copies already held every piece; at the bot's claim, copy 1's seeding placed nothing and
recorded the 369 pieces already there). The Admin's `[ClusterFSeedTutorial` dry
run then found nothing to place.

## Files

- Code copy (uncommitted): `Tutorial/TutorialWake.cs`, `TutorialStart.cs`, `ClusterFTutorial.cs`,
  `TutorialCorePlacement.cs`, `TutorialCoreTrials.cs`, `TutorialFarm.cs`, `TutorialRecruiter.cs`, `TutorialCopies.cs`;
  `ClusterFAchievements.cs`, `ClusterFBulletin.cs`, `ClusterFGuildStarterPath.cs`, `CharacterCreation.cs`;
  `server/patches/PlayerMobile-tutorial-wake-move.patch` (new) and `docker/uo/apply-patches.sh`; the new fact file and
  five changed test files; `CHANGELOG.md` (section 2026.10.28.7: 5 Changed, 1 Fixed, 1 Staff) and `VERSION`.
- Docs copy: this file and `notes\cc-P728-tools\` (probe and mutants, red and green outputs, the gated build script and
  logs, the CHANGELOG script, the bot route, its maker, the proof shard script, the three runs, the lift probe).
- Outside the repos: `D:\UO\golems\Iron\p728-work\` (the overlay copy and the shard copy); it can be deleted.

P728 DONE
