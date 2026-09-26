# The New Haven board's quest menu, and four small items beside it

Date: 2026-09-26. Agent: Claude Code. Pinned ModernUO `7c9215d97`. Brief: build Q-058 option 2 under the six
constraints of its answer; D13, D15, D16 and D17 from `docs/bug-list.md`; optionally the fireball assertion.

**Status: built, every gump asserted in the gate, FINAL green. Not placed on the live shard:** placing is a deploy,
and deploys are Chase's. No new D-number. **D-90 restated** (section 7). No new question.

> Double-clicking the board opens a two-page menu of all 26 quests, each row showing its state as the stock predicates
> give it. Picking a row calls the stock path on that quest. Everything after the pick (offer, accept, progress,
> report-back, reward) is the stock gump. The "take ten" loop the wishlist described now works: the gate takes ten
> in a row through the menu and is refused on the eleventh, in words.

---

## 1. What changed

| File (in `D:\ShatteredLegacy`) | Lines | What |
|---|---|---|
| `server/customizations/Engines/ML Quests/Items/NewHavenQuestBoard.cs` | 147 -> 481 | the menu (`NewHavenQuestPickerGump`), `CanUse`, `GetRowState`, `OnPick`, tooltip line 4-5, `Place()` (D13) |
| `server/tests/Engines/MLQuests/NewHavenQuestBoardVerification.cs` | 349 -> 881 | rewritten: 10 facts, all gump assertions on the wire (section 6) |
| `server/tests/Route/ShardTestClock.cs` | 230 -> 292 | the hit-point rule (D15), the true statement about `Epoch` (D16), the regen guard fact |

No patch. Nothing in `server/patches/` or `docker/` changed. `notes/port-recipe.md` gains a section on writing
timed and gump facts (D15, D16, and three test-NetState traps this task hit).

**Longer than the estimate.** Q-058 said ~120-150 lines; the board file grew by 334. About a third is comments
(the re-check list, the reason for each re-verification); the rest is the menu, the row states and `OnPick`. The
test file doubled because every gump is now read off the wire rather than asserted headless.

---

## 2. The menu

- **`OnDoubleClick`** runs `CanUse` (below) and sends `NewHavenQuestPickerGump`. The stock single random pick,
  `MLQuestSystem.OnDoubleClick`, is no longer called from the board. Nothing else about the board changed: same type,
  same graphic, same quests, same registration.
- **Rows**, in `QuestTypes` order: a reply button (only where there is something to do), the skill's name
  (`AosSkillBonuses.GetLabel`, the cliloc the stock objective uses), the quest's own title cliloc, and a state label.
  Header: "Pick a quest. You carry N of 10." and, when full, a red line saying that is the most you can carry.
- **Button ids are 1-26, the row's index in the static `QuestTypes` table.** That table is code, not a snapshot. The
  handler maps id to type and nothing else; everything about the quest is looked up again at the click (section 4).
- **The menu holds a reference to the board and to the player, and nothing else.** No list, no state, no cache.

### 2.1 Why two pages, and what I checked about size

26 rows do not fit a small game window at a readable height. Two options exist in the gump protocol:

- **A scrolling area** does not work here. The only scrolling element is an html gump's scrollbar, which scrolls the
  text inside one element; buttons cannot be put inside it.
- **Client-side pages** (`{ page n }` plus page buttons) are switched by the client with no round trip and no server
  state. So: **two pages of 13**, "More quests" and "Back".

What I checked, server side, in pinned source:

| Limit | Where | This menu |
|---|---|---|
| Packet length field is a `u16` (65,535) | `DynamicGump.Compile` -> `WritePacketLength` | **919 bytes**, measured in the gate |
| One 64 KB static compile buffer per gump | `BaseGump._packetBuffer`, `0x10000` | as above |
| Layout and strings buffers grow on demand from 512 KB | `DynamicGumpBuilder`, `GumpLayoutBuilder` (`0x80000`) | layout 4,375 chars, 30 strings |
| One string is at most `ushort.MaxValue` chars | `WriteInternalizedString` | longest is 67 |
| 512 open gumps per NetState, then disconnect | `NetStateGumps.GumpCap` | the menu is `Singleton`: a second double-click replaces it, pinned |
| Button ids of a `DynamicGump` are **not** checked against the layout on reply | `GumpSystem.DisplayGumpResponse` checks only legacy `Gump` | the handler bounds-checks; forged ids pinned (section 4) |

Pixel size: the box is 520 x 411 at (50, 50), so it ends at (570, 461), inside 640 x 480. **That 640 x 480 is the
smallest classic client window is from memory, not measured**, and how a client draws the rows (label widths, the
hues) is a client check, not a gate one.

---

## 3. Row states, and which stock predicate gives each

The Q-058 answer asks for five: available, held, ready to turn in, done, locked at 50. **The menu shows seven**,
because two more states are real on the stock path and a player who cannot see them will ask. Every one is read off a
stock predicate. `GetRowState` evaluates them in this order:

| Label | State | Stock predicate |
|---|---|---|
| "Taken from a trainer" | held, not from this board | `context.FindInstance(quest) != null`, and **FindQuest step 1's predicate** false: `instance.Quester != board && (quest.IsEscort \|\| instance.QuesterType != typeof(board))` |
| "Ready to turn in" | held here, objective met or reward waiting | `instance.ClaimReward \|\| instance.IsCompleted()` |
| "Taken, in progress" | held here, otherwise | step 1's predicate true |
| "Done" | turned in | `quest.OneTimeOnly && context.HasDoneQuest(quest)` (the check inside `MLQuest.CanOffer`) |
| "Past 50: gone" | locked at 50 | any `objective.CanOffer(board, pm, false)` false; for these 26 that is `GainSkillObjective.CanOffer` |
| "No room: 10 held" | would be offered, but the log is full | `context.IsFull` (the first check inside `MLQuest.CanOffer`) |
| "Available" | on offer | `!quest.IsChainTriggered && !context.IsDoingQuest(quest) && quest.CanOffer(board, pm, context, false)` |
| "Not offered" | anything else `CanOffer` refuses | fallback; unreachable for these 26 today |

**"Available" is exactly `RandomStarterQuest`'s eligible pool** (`MLQuestSystem.cs:663-695`), and the gate asserts
that equivalence for every row in two different player states. Every non-available, not-held label is a case in which
stock `CanOffer` is already false; the label only says which of its checks refuses.

**Where I could not avoid our own logic, stated rather than hidden:**

1. **"Taken from a trainer" versus "Taken, in progress"** needs FindQuest step 1's predicate, and `FindQuest` is
   private. The menu restates it (`MLQuestSystem.cs:327-331`). If upstream changes it, the copy does not follow; it is
   item 4 of the file's re-check list.
2. **The order of the labels** is ours where two apply at once. A quest turned in is also past 50 (its skill got
   there), and shows "Done". A full log with a quest past 50 shows "Past 50: gone". Stock `CanOffer` checks `IsFull`
   first; the menu shows the more permanent reason instead. It changes the words, never the answer: all of these
   rows are refused by stock `CanOffer` and have no button.
3. **"Ready to turn in" covers two stock states**, `IsCompleted` and `ClaimReward` (reported back, reward not yet
   taken). One label; `OnPick` sends the right stock gump for each.
4. **A failed instance** cannot be told from one in progress without a label of our own. None of the 26 can fail (no
   timed objective); stock sends nothing for a failed quest, and so does `OnPick`.

---

## 4. The response handler, what it re-verifies, and why

The menu is a snapshot the client holds and can answer at any time. So the reply is trusted for exactly one thing,
**which row was pressed**, and everything else is judged against the world at the click:

1. **Reply is from the player the menu was built for**, and the id is 1-26. Anything else, including 0 (close),
   27, -1, `int.MaxValue` and `int.MinValue`, does nothing. Needed because `DisplayGumpResponse` validates button ids
   for legacy `Gump` only; a `DynamicGump` receives whatever the client sends.
2. **`CanUse`, the same checks a double-click runs**: board not deleted and on a real map, player not deleted, **same
   map** as the board (in range on another facet is refused; `InRange` alone ignores the map), within 2 tiles, ML
   quests enabled, the board has quests, the player is a `PlayerMobile` and alive. Refusals say 1019045, as the
   stock double-click does.
3. **The quest is looked up again** (`MLQuestSystem.FindQuest(type)`) and must still be one of the board's.
4. **`GetRowState` is recomputed from scratch** and dispatched: available -> `quest.SendOffer(board, pm)`; held here ->
   stock's held-quest branch (reward offer, report-back or progress); taken from a trainer -> "You took that quest
   from a trainer. Take it back to them."; anything else -> `quest.CanOffer(board, pm, context, true)`, so the board
   speaks the stock refusal (1075454, 1077772 or 1080107), **plus**, when the log is full, a plain line saying so
   (Q-058 constraint 4: 1080107 alone is "I have nothing for you", which does not say why).

**The double-click-twice case.** Three layers, each pinned:

- The menu is `Singleton`, so the second double-click closes the first on the server. **The gump system then drops
  any reply to the first** (it is no longer in the player's gump list); pinned by answering both.
- The one live menu is re-verified at the click regardless. The case that matters is two menus in flight around
  one accept: open the menu, pick EnGuarde (offer open), double-click again (the new menu still shows EnGuarde
  available, correctly: it is not yet held), accept the offer, then answer the newer menu with EnGuarde. **The
  player gets the stock progress gump for the quest they now hold, never a second offer or a second instance.**
  Pinned.
- **Why this layer is not optional.** Stock `MLQuest.CanOffer` does **not** check `IsDoingQuest`, and neither does
  `OnAccept`. Stock keeps a held quest from being offered twice only because `RandomStarterQuest` skips held quests
  and the offer gump is a singleton. A handler that sent `quest.SendOffer` for a cached "available" row would reopen
  exactly the hole the stock picker avoids.

**Every stale case the brief names is pinned in one fact** (`AButtonIsJudgedByTheWorldAtTheClickNotByTheMenu`), each
as: open a menu that shows EnGuarde with its button, change the world, press it, assert no offer and no instance.
Walked away (1019045); same spot on Felucca (1019045); board moved to `Map.Internal` (1019045); board deleted
(nothing); skill passed 50 (1077772, from the board); ten quests taken meanwhile (1080107, from the board); the quest
taken from Recaro meanwhile (no offer, still one instance, the trainer line sent); dead (nothing); six forged ids;
close.

**What is stock after the pick, and stays stock:** the offer gump's Accept, the report-back's Continue and the reward
gump's Accept do no range check of their own, and never did (`QuestOfferGump.OnResponse` calls `OnAccept`, which
calls `CanOffer`, which checks the log, done records and objectives, not distance). A player can open an offer at the
board, walk off and accept it; so can a player at Recaro. Stock behaviour, not ours, not changed.

---

## 5. Save shape: byte-identical, and now pinned

**`SaveShapeIsUnchanged`** serializes a board at `HomeLocation` on Trammel with `LastMoved = Core.Now` and compares
the bytes to a constant:

`090000001010160400AE0D0D0A0EC5C10201010000000000000000` (27 bytes)

**The constant was captured from HEAD's own code, before the board changed** (build 0 below: the unchanged
`9d47298` board, plus a capture fact that failed on purpose to print its bytes). So the comparison is against the
board as it is in the repo today, not against itself. The new board produces the same 27 bytes.

**Watched red** (red run 1): one `[SerializableField(0)] private int` added at version 0, which is the quiet way to
break a save, gives different bytes and the fact goes red.

**The loud way cannot happen silently.** My first red-run attempt bumped `[SerializationGenerator(0, false)]` to `1`.
**It does not compile**: the generator's output calls a migration `Deserialize` overload that does not exist
(`CS1501` in `NewHavenQuestBoard.Serialization.g.cs`). So a version bump without a migration file is a red builder
stage on its own, and the fact covers the other shape, a new field at the same version.

---

## 6. The gump facts, all in the gate

The facts drive a real test `NetState`, read every gump off `ns.SendBuffer` by its serial and type id, and inflate it
with the managed `ZLibStream`, the method `GumpOnTheWireVerification` proves. **Every button goes back through
`GumpSystem.DisplayGumpResponse`**, with the bytes a client's 0xB1 carries, so the gump system's own lookup and
removal are in the test, not bypassed by calling `OnResponse`.

| Fact | Pins, on the wire |
|---|---|
| `BoardIsQuesterForExactlyTheTwentySixNewHavenTrainingQuests` | as before, plus: none of the 26 is chain-triggered, has a `NextQuest` or is an escort, so FindQuest's steps 2-3, which the menu does not run, can never apply |
| `SaveShapeIsUnchanged` | section 5. **Watched red** |
| **`DoubleClickFromTheGroundOpensTheMenu`** | the override: menu on the wire from a board on the ground, 1042593 never; a second double-click replaces it (one menu open); out of reach and same spot on another facet give 1019045 and no menu. **Watched red** |
| `TheMenuListsAllTwentySixOnTwoPagesWithinTheLimits` | 919-byte 0xDD; pages 1 and 2 and no 3; both page buttons; all 26 title clilocs once, in order; every skill cliloc; 26 buttons, ids 1-26; "You carry 0 of 10"; the box inside 640 x 480 |
| `EachRowShowsTheStateTheStockPredicatesGive` | one player with a quest from Recaro, one in progress here, one ready, one turned in, one past 50, 21 available: every row's label, button and `GetRowState`; then filled to 10: the rest read "No room", the banner shows. Both times: **"Available" equals stock's eligible pool, row for row** |
| `TheBoardCarriesTheWholeStockLoopAndTakeTen` | pick EnGuarde: the stock `QuestOfferGump` carrying `@#1078186@`; Accept: typed to the board; pick again: `QuestConversationGump`; Fencing 50: `QuestReportBackGump` -> Continue -> `QuestRewardGump` -> Accept: `RecarosRiposte` in the pack, done; row "Done", no button. **Then ten in a row through the menu**, all typed to the board, in pick order; the eleventh row "No room", and a forced press gets 1080107 from the board **and** the full-log line, no offer, still ten |
| **`AButtonIsJudgedByTheWorldAtTheClickNotByTheMenu`** | section 4. **Watched red** |
| `SkillAtFiftyLocksTheQuestOnTheBoardToo` | 49.9 available, 50.0 locked; Chase's character on the wire: 25 "Available", EnGuarde "Past 50: gone" with no button (Q-059) |
| `AQuestTakenAtTheBoardIsNotTheTrainersToTakeBack` | unchanged: Recaro says 1080107 to a board-quest holder |
| `PlaceFindsABoardOnAnyMapAndMovesItRatherThanBuildingASecond` | D13, section 8 |

Four of the old seven facts were stated against `RandomStarterQuest`, which the board no longer calls. Their content
moved: "offers every untaken quest", "held is never offered again" and "completed is never offered again" are now
row states and the loop, asserted on the menu the player sees.

**Not asserted in the gate, and why:**

- **The tooltip's five lines.** It is an object property list, not a gump, and asserting it means implementing
  `IPropertyList` in the test. The text is in section 7 and is a client check.
- **How a client draws the menu**: whether a label is clipped at its width, how the hues look, whether 640 x 480 is
  really the floor. Wire bytes are right; drawing is a client check.

---

## 7. The tooltip, and D-90 restated

**Lines 4 and 5.** Line 4 was "One quest at a time here. Say no to see a different one." Both halves became false.
Line 5 was about one quest and becomes plural. Lines 1-3 are unchanged, still five lines:

1. *Get these early! When a skill reaches 50, its quest is gone for good.*
2. *Your whole skill counts, not just what you gain after. At 45, you only need 5 more.*
3. *The number in your skill list is what counts, and magic items raise it. Take quests first.*
4. *Double-click for all 26 quests. Take the ones you want.*
5. *Bring them back to this board, not the trainer. You can carry 10 quests in all.*

**D-90, restated for `docs/fidelity-principle.md`** (Claude promotes; `docs/` not edited here). It replaces the row in
`notes/new-haven-quest-board.md` §5:

| # | What | Player-visible effect | Reverses when |
|---|---|---|---|
| **D-90** | A New Haven training board: a standing bulletin board at the town square, `(3502, 2573, 14)` Trammel, **with our own quest menu**. Double-clicking it lists the 26 stock New Haven skill-training quests with each one's state (available, taken, ready to turn in, done, past 50, taken from a trainer, no room), and picking one opens the **stock** ML quest path for that quest. It takes them back when they are done. **Neither the board nor the menu existed on OSI or in ServUO.** | A new player can see all 26 from the tile they arrive on, pick the ones they want and hold up to 10 at once, without finding 26 trainers across town first. The quests, their text, the offer/accept/progress/report-back/reward gumps, the rewards, the 50-point lockout and the 10-quest cap are unchanged; where you pick them up, and the list you pick from, are new. A wiki will not mention the board or the menu. | **Stock skill-gain rates.** `ClusterFSkillGain` at `chanceAttempts` 1 and `amountMultiplier` 1 (or disabled: `clusterf.skillGain.enabled`) restores the window in which walking town to find trainers is feasible, and the board stops being necessary. To reverse: `[remove` every board in the world **after warning players** (held board quests are dropped at the next restart, E3), then delete `NewHavenQuestBoard.cs` and its test in a later deploy, once no save holds the type. Reach: 26 quests, one item, one gump. |

**What widened, for the fidelity argument.** Before, the board chose nothing; the engine's random pick did. Now the
player chooses from a list only we display. The list's contents are still the stock predicates' answers, word for
word in what they allow and refuse, and the gate asserts that equivalence per row. So the new wiki debt is one line:
"double-click the board for a list; pick one". What the menu adds that stock never had is the visibility of all 26
at once and the "taken from a trainer" and "no room" explanations, which stock gives as the bare 1080107.

---

## 8. Part B

### D13: `Place()` now searches every map. Close.

It walks `World.Items` for any undeleted board on any map, `Map.Internal` and containers included, counts Trammel and
elsewhere separately, and keeps the best one: already home, then standing on Trammel, then any. It moves that one home
and never builds a second while one exists. The message keeps the Trammel count and adds the rest ("found 1 on
Trammel, 1 elsewhere"), says where a moved board came from, and says so when more than one exists (the others are left
where they are; deleting one is a GM decision because of E3). Pinned: a board on `Map.Internal` is moved home with its
serial, not duplicated; a second on Felucca is reported and left; with the home one gone, the Felucca one is moved.

### D17: the stale header sentence. Close.

The test file's header now says the opposite and says how: every gump is read off the wire and every button goes back
through the gump system.

### D15: the rule is written down, and a guard fact pins the artefact. Close.

- **The rule**, in `ShardTestClock.cs`'s header and in `notes/port-recipe.md`: *read hit points on the tick the damage
  lands, never after an `Advance`*, with why (125 hits a second), how to read a hit that lands inside an `Advance`
  (8 ms steps, keep the lowest), and when to revisit Q-060 (anything measured over seconds).
- **`ShardTestClockVerification.ADamagedMobileRegainsExactlyOneHitPerWheelTick`**, beside
  `SliceAloneDoesNotAdvanceTheClock`: a player at 50/50 takes 20, reads 30 on the damage tick, and **31 one 8 ms tick
  later**. Asserts behaviour only, so a harmless refactor of how the rate is stored cannot turn it red; logs
  `DefaultHitsRate` and the handler for whoever reads the failure. **Watched red** (red run 1: `DefaultHitsRate` set
  to 1 s inside the fact for that build only, as a pinned-commit bump or a fixture `RegenRates.Configure` would do):
  `Expected: 31, Actual: 30`.

### D16: the header now says what is true. Close.

`Epoch` is a floor, not a base. `Arm()` raises `Core.Now` to it only when it is lower; `CreateTestNetState` sets
`Core._now = DateTime.UtcNow` (`PacketTestUtilities.cs:62`), and `Arm()` then leaves the wall clock in place. So
`Core.Now` starts at `Epoch` only if no fact in the process has made a test NetState yet. The header, `Epoch`'s own
doc comment and `Arm()`'s doc comment all say so now, with the rule: measure from a `Core.Now` read inside the fact,
never from `Epoch`, and do not assert on the date or time of day. D16's other half (`Arm()` leaves dropped timers
flagged `Running`) was already stated where it bites, in the guard fact's "created after Arm" comment and in
`gate-integrity.md` A.5; I did not change `Arm()`.

### The fireball assertion: the reasoning does not work, left alone

**Off by one.** `BonusHits` 25 makes the player's `HitsMax` 150 (`PlayerMobile.cs:548-573`: `Str / 2 + 50 + BonusHits`,
ML caps `Str` at 150 and `BonusHits` at 25 for a Player), and the fact reads `taken = HitsMax - lowest`. A player can
lose at most `HitsMax`, so `taken` can never exceed 150, and a fireball changed to 500 would kill the player, read
`taken = 150`, and pass `InRange(taken, 120, 150)`. To catch damage rising, the player must be able to *survive* more
than the ceiling: `HitsMax` of at least 151. The ML caps put that out of reach for a player (the only thing above the
cap is `+20` under a `BakeKitsune` or `GreyWolf` animal form, the same file, which drags the transformation system into
a fireball fact). So bonus hits make the assertion catch nothing it does not already catch. **A route that would work,
not taken:** a `PlayerMobile` subclass in the test that records the `amount` passed to `OnDamage` before hits are
clamped, which measures the roll itself, uncapped. Worth doing when that file is next touched; it is not a build of its
own.

---

## 9. Verification

| Step | Result |
|---|---|
| **Build 0**, capture (`--tests-only`, HEAD's board + a capture fact + the new guard fact) | **red by design** on the capture fact only: `Expected: "CAPTURE"`, the bytes truncated in xUnit's message. 138 passed, **the new guard fact green on HEAD** |
| Build 0b, capture again with the bytes in the failure message | red by design, `SHAPE[0900...0000]`, 138 passed |
| Build 1 | **red, 5 facts, all mine**: menu 492 px tall against 480 (rows shrunk 24 -> 22 px); `NullReferenceException` in `SendSupportedFeature` moving a player with a test NetState across facets; replies ignored because `Mobile.NetState` does not set `NetState.Mobile`; `Place`'s fact counting boards other failed facts left. Section 10 |
| Build 2 | **red, 1 fact, mine**: after `Kill()` and `Resurrect()` the menu did not open. Reordered |
| Build 3 | **green, 141** |
| Red run 1a | version bump: **does not compile** (section 5) |
| **Red run 1** | `CanUse` skipped in `OnPick`, a field added at version 0, `DefaultHitsRate` = 1 s in the guard fact. **Red, exactly 3 facts**, each for its planted reason: `AButtonIsJudged…` ("walked away": an offer was sent), `SaveShapeIsUnchanged` (bytes differ), `ADamagedMobile…` (31 expected, 30). Restored from saved copies, `RED RUN` grep 0 |
| **Red run 2** | the override removed (method renamed, so stock `QuestGiverItem.OnDoubleClick` runs). **Red, exactly the 6 facts that open the menu by double-click**; `DoubleClickFromTheGround…` logs `(0xFFFFFFFF, 1042593)`, "That is not in your backpack". Restored |
| FINAL attempt 1 | **green, 141**, `sl-modernuo:picker` `55aea83d1300`. Then three repeat runs of the test step on its builder: 141 each |
| Probe (fact in `server/tests/Probe/`, deleted, never committed) | `Kill()` in the test host **deletes** an account-less `PlayerMobile` (`Deleted` true, `Map` null). So build 2's failure was not the board, and **the "dead" case in attempt 1 was testing a deleted player, and passed for the wrong reason** |
| **FINAL attempt 2** | "dead" rewritten as a real ghost (ghost body on a `Player`, `Alive` false, not deleted). **Green, 141, `sl-modernuo:picker` `8e21fbb1d681`**. Two more repeat runs: 141 each |

**FINAL: `sl-modernuo:picker` (`8e21fbb1d681`), green, attempt 2 of 2.** Attempt 1 was also green; it was rebuilt
because a case in it proved less than it said, not because anything failed. **No attempt went red on any fact**, and
no flake was seen in 7 full runs of the gate's test step across the two FINAL builders. **Not tagged `latest`**:
`sl-modernuo:latest` is still `07f8a69f4115`. build.sh retagged `sl-uo-builder:latest`, as it always does.

141 = 137 + 3 (the board file went from 7 facts to 10) + 1 (the regen guard). `tools/progress.py` counts 142, one more than
xUnit, which is D18's gap, unchanged.

**The "dead" case was not separately watched red.** Red run 1 skipped all of `CanUse`, and the first case in that
fact ("walked away") went red before "dead" ran.

**The running server otherwise.** Against `sl-modernuo:gate`, 479 files under `/modernuo` each: **`Server.dll` is
byte-identical**; `UOContent.dll` differs (the board); `ModernUO.dll` and `Server.Tests.dll` differ because both
reference `UOContent` (`Application.csproj:27`, `Server.Tests.csproj:17`) and rebuild with it; the test assemblies
differ. Nothing else.

## 10. Three test-NetState traps, for the next gump fact

All in `notes/port-recipe.md` now. None is a defect in shipping code; login does all three things correctly.

1. **`pm.NetState = ns` does not set `ns.Mobile`.** A real login sets both. Without it, every gump reply's
   `sender.Mobile` is null, and the stock quest gumps (`QuestOfferGump.OnResponse`: `sender.Mobile is not
   PlayerMobile pm` -> return) silently do nothing. Set `ns.Mobile = pm` too.
2. **A facet change with a test NetState throws** in `OutgoingAccountPackets.SendSupportedFeature` (no account).
   Set the NetState aside across the move.
3. **`Kill()` deletes an account-less `PlayerMobile`.** To test "dead", give a `Player` a ghost body.

## 11. For `docs/bug-list.md`

- **D13, D15, D16, D17: close.** Section 8.
- **New, §5 ModernUO upstream, proposed E4:** `GumpSystem.DisplayGumpResponse` checks a reply's button id against
  the layout only for legacy `Gump` (`if (baseGump is Gump gump)`); a `DynamicGump` receives any id the client sends.
  Every `DynamicGump` that indexes an array by button id trusts the client. Ours bounds-checks and a fact pins forged
  ids. **Report upstream**; not audited across stock gumps.
- **No new `Dn`.** The next free number there is still **D19**. The three traps in section 10 are route knowledge,
  written into `port-recipe.md`, not defects.

## 12. Not verified

- **In a real client**: the menu's look (label widths at 125 px, hues, the page buttons), the new tooltip lines, and
  a new character's double-click from the arrival tile. For `docs/client-check-backlog.md`, with the board's existing
  row.
- **`[PlaceNewHavenQuestBoard` typed at a console**; the facts call `Place()`, which it calls.
- **640 x 480 as the smallest classic window**: from memory (section 2.1).

## 13. What it cost

From the build logs' timestamps only; the reading before build 0 was not timed. Build 0 finished 16:04 and 16:07;
builds 1-3 16:17-16:22 (writing the menu and the tests fell between 16:07 and 16:15); red runs 16:24-16:29; FINAL 1
16:30; probe 16:33; FINAL 2 16:37. Each `build.sh` with a changed file took about 2-2.5 minutes, almost all of it the
`dotnet publish` that reruns on every change. Seven builds of the gate, three red-run builds (one stopped at compile) and a probe build is about
25 minutes of building for one file, which is D4's point.

## 14. Questions opened

None. The two states beyond Q-058's five, the order of labels where two apply, and the trainer and full-log lines are
decisions inside the constraints and are recorded above; the fireball paragraph is the answer the brief asked for.
