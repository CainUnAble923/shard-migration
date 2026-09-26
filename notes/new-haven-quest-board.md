# The New Haven training board

Date: 2026-09-26. Agent: Claude Code. Pinned ModernUO `7c9215d97`. Spec: `docs/community-scripts-wishlist.md`,
"The New Haven quest board - costed 2026-09-19, ready to build".

**Superseded in part, 2026-09-26:** the board now opens a quest menu (Q-058 option 2). Sections 3 (tooltip line 4),
4.1 (one quest at a time) and 6.1 (no gumps in the test host) no longer describe the board, and D-90 is restated in
`notes/new-haven-quest-picker.md` section 7. The rest stands.

**Status: built, gated, proved headless, committed. Not placed on the live shard: placing it is a deploy, and deploys
are Chase's.** One deviation, **D-90**. Two questions, **Q-058** and **Q-059**, neither blocking.

The headline is narrower than the spec expected, and the narrowing is what matters:

> The board works on the stock path: the real offer gump with the real quest text, reached from the tile where every
> new character arrives, without taking a step. **But the stock path gives a multi-quest quester one quest at a time,
> picked at random**, so the spec's "take ten, push them to 50, take ten more" loop is not reachable through the
> board as built (Q-058). **It does not lift the lockout at 50 either, and should not without a separate decision**
> (Q-059).

---

## 1. What was built

| File (in `D:\ShatteredLegacy`) | Lines | What |
|---|---|---|
| `server/customizations/Engines/ML Quests/Items/NewHavenQuestBoard.cs` | 147 | the board, its registration, the placement command |
| `server/tests/Engines/MLQuests/NewHavenQuestBoardVerification.cs` | 349 | 7 facts |

No patch. Nothing in `server/patches/` changed.

- **`NewHavenQuestBoard : QuestGiverItem`**, graphic `0xA0C5`, `Movable = false`, name "New Haven training board".
- **Registered as quester for the 26 quests** by `MLQuestSystem.Register(quest, typeof(NewHavenQuestBoard))` in
  `Configure`, the S5 route (`apply-patches.sh` carries `.cs` only, so `Data/MLQuests.cfg` is not ours to extend). It
  **reuses the instance the trainers already hold** (`MLQuestSystem.FindQuest(type)`), so board and trainer share one
  quest object. Registering twice is a no-op, pinned.
- **The 26**: counted as the classes deriving `MLQuest` in pinned `Engines/ML Quests/Definitions/NewHavenSkillTraining.cs`
  (`grep -c ": MLQuest$"` = 26): `CleansingOldHaven TheRudimentsOfSelfDefense CrushingBonesAndTakingNames
  SwiftAsAnArrow EnGuarde TheArtOfWar TheWayOfTheBlade ThouAndThineShield DefyingTheArcane StoppingTheWorld
  ScribingArcaneKnowledge TheMagesApprentice ScholarlyTask TheRightToolForTheJob KnowThineEnemy BruisesBandagesAndBlood
  TheInnerWarrior TheArtOfStealth BecomingOneWithTheShadows WalkingSilently EyesOfARanger TheWayOfTheSamurai
  TheAllureOfDarkMagic ChannelingTheSupernatural TheDeluciansLostMine ItsHammerTime`. Each is one
  `GainSkillObjective(skill, 500, useReal: true, accelerate: true)`, `OneTimeOnly`, one skill each (26 distinct), all
  pinned by the test.
- **The one override**, `OnDoubleClick`: the stock body minus `IsChildOf(from.Backpack)`. **Still possible in pinned,
  in our own file:** `QuestGiverItem.OnDoubleClick` is `public override` on an `abstract partial` class and is not
  sealed (`Engines/ML Quests/Items/QuestGiverItem.cs`); the range check (2 tiles, cliloc 1019045) is kept.
- **Placement: `[PlaceNewHavenQuestBoard`** (Administrator). It places one board at `(3502, 2573, 14)` Trammel, or moves an
  existing one there, and **never deletes one** (section 4.4 says why). Nothing places the board on world load; the
  final image's fresh world has none (headless run 3).

### Why `0xA0C5`, the standing bulletin board

Chase asked for "a board or quest stone". Tiledata names four free-standing-capable candidates; all four have art in the
shard's client (`artLegacyMUL.uop`, checked by hash, client 1.25.35):

| Graphic | Tiledata name | Why not / why |
|---|---|---|
| `0x1E5E`/`0x1E5F` | bulletin board | wall-hung; in an open plaza it floats |
| `0x2311`/`0x2312` | bulletin board | the house-addon player board (`PlayerBBSouth/East`); reads as a house fixture |
| `0x0ED4` | (guildstone) | a stone reads as a guildstone, a different interaction players already know |
| **`0xA0C5`** | **standing bulletin board** | free-standing, one facing, impassable; every UO town has boards and players double-click them |

A bulletin board says "read me, double-click me" to a UO player before any text does. That is the whole job.

---

## 2. The placement question, answered with data

**Where a new character arrives: `(3503, 2574, 14)` Trammel.**

- Our `CharacterCreation.cs` (a full-file replacement of stock) offers exactly one starting city, `ConstructAvailableStartingCities`
  (`server/customizations/CharacterCreation.cs:129-136`): `"New Haven", "The Bountiful Harvest Inn", 3503, 2574, 14,
  Trammel`. With `Core.SA` true `GetStartLocation` returns the client's pick, which can only be that one. Headless:
  `arrival: New Haven / The Bountiful Harvest Inn at (3503, 2574, 14) Trammel; starting cities offered: 1`.
- Pinned's own data agrees to the tile: stock `NewHavenStartingCities` (`CharacterCreation.cs:112-114`) has the same
  row, and `Distribution/Data/regions.json` gives the `New Haven` region its `GoLocation` at exactly `3503, 2574, 14`.
- **The label lies.** The row says "The Bountiful Harvest Inn", but the inn's region is `3493-3510, 2513-2530`,
  about 45 tiles north. The arrival point is the town's centre, not the inn.

**Where the main square is: the same place.** No data file names a "square", so I measured the tiles. The Trammel
statics (`statics1.mul`, read with a scratch parser, then re-read by the server in headless run 1) show a raised,
stepped 9 x 9 plaza at `3502-3510, 2572-2580`: stone steps (`0x0917`/`0x0918`) at z14/16/18, wooden benches, flowerpots,
a lamp post at each corner (`3503,2573`, `3509,2573`, `3503,2579`, `3509,2579`), and the contribution statue
(`0x2FF6`) at its centre `(3506, 2576)`. The bank's east wall is at x 3492, just west. **Our own seeder already calls
this spot the square**: `ClusterFNewHavenSeeder.cs:13` puts Sir Helper at `3503, 2574, 14` with the area label "Town
square", and the headless run found him standing on the arrival tile.

**Distance from arrival to the square's centre: 3 tiles in UO range (dx 3, dy 2; 3.6 Euclidean).** The arrival tile is
the plaza's north-west corner, beside its lamp post. **They are the same spot**, so the board goes there, and **no
second board and no placement Q-number**.

**The board's tile, `(3502, 2573, 14)`:** one tile diagonal from the arrival tile. Its land is z14 with no statics
(`land 0x03FB z14; avgZ 14; statics` in run 1), `Map.CanFit(h16, blocksFit)` is true, and it is **in reach (range 2)
from the arrival tile**, so a new character can double-click it without taking a step. It sits off the spawn tile
(Sir Helper is on that) and outside the plaza's steps, next to the corner lamp post.

---

## 3. The board's text, and where it had to differ from the brief

The five lines are tooltip properties (`AddNameProperties`). `ObjectPropertyList` has five `~1_NOTHING~` string
slots (`ObjectPropertyList.cs:31-38`), so five is the ceiling. Under the name and "Quest Giver":

1. *Get these early! When a skill reaches 50, its quest is gone for good.*
2. *Your whole skill counts, not just what you gain after. At 45, you only need 5 more.*
3. *The number in your skill list is what counts, and magic items raise it. Take quests first.*
4. *One quest at a time here. Say no to see a different one.*
5. *Bring it back to this board, not the trainer. You can carry 10 quests in all.*

Three of the brief's statements were wrong against the source, so the text says what the code does:

- **"`useReal: true` means skill gained before accepting counts."** Half right, for the wrong reason. Credit for
  prior skill comes from the objective's **absolute threshold** (`ThresholdFixed = 500`; `IsCompleted` compares the
  current value), with or without `useReal`. What **`useReal` switches** is *which* value: `skill.Fixed` instead of
  `BaseFixedPoint`. `Fixed` is `Value * 10` (`Server/Skills.cs:228`), and `Value` is **base, plus a stat-derived
  offset, plus skill mods** (`NonRacialValue`, `:250-300`). So items **and stats** count. The offset is
  `(RawStr*StrScale + RawDex*DexScale + RawInt*IntScale) * (100 - base)`, capped at `StatTotal * (100 - base)`, with the
  scales from `Distribution/Data/skills.json` divided by 100 (`Skills.cs:407-416`). For board skills: **Mining**
  (Str 0.2) with 60 Str locks at **base 43.2**; **Magery** (Int 0.15) with 100 Int at **base 41.2**; **Fencing**
  (Str 0.045, Dex 0.055) with 60/60 at **base 46.8**. **Computed from the source, not measured in a run.** The
  wishlist's "claim the quests before gearing up" is right as far as it goes; stats do the same thing, earlier.
  Line 3 names the number the player actually sees in their skill list, which covers both.
- **"Take ten matching what you are about to do."** Not reachable from the board (section 4.1, Q-058). Line 4 says what
  it does instead. The 10 cap is still real across all questers, so line 5 keeps it.
- **The turn-in goes to the board, not the trainer.** The quests' own text says "Return to Recaro in New Haven", and
  on the stock path Recaro cannot take it back (section 4.3). Line 5 says so. The brief did not mention this.

---

## 4. How the stock path actually behaves, each point proved

### 4.1 One quest at a time, chosen at random (Q-058)

`MLQuestSystem.FindQuest` (`MLQuestSystem.cs:315-367`): step 1 returns any quest held from a quester of this *type*, so
with one board quest held every click shows its progress gump; step 4 is `RandomStarterQuest` (`:663-695`), a uniform
random pick among the eligible. **Headless run 1:** holding `TheMagesApprentice`, **10 clicks gave 0 offer gumps and
10 progress gumps.** Stock behaviour for any quester with more than one quest; the trainers each hold one, so nobody
saw it. The wishlist's premise that "quests already held are filtered by the existing system" is true; what it did not
anticipate is that holding one also **blocks the rest**.

### 4.2 Held, completed and past-50 are filtered by the stock system, not by us

- **Held**: `RandomStarterQuest` skips `IsDoingQuest` (`:677`). Pinned: `HeldQuestIsNeverOfferedAgain`.
- **Completed**: `OneTimeOnly` plus `HasDoneQuest` in `MLQuest.CanOffer` (`MLQuest.cs:136-150`). Pinned:
  `CompletedQuestIsNeverOfferedAgain` drives the real turn-in (`ContinueReportBack`, `ClaimRewards`, reward in the pack)
  and then drops the skill back under 50, so `OneTimeOnly` is the only thing refusing. Headless: turned in at the
  board, `EmberStaff` in the pack, **offered again 0 times in 40 clicks**.
- **Past 50**: `GainSkillObjective.CanOffer`. Pinned: `SkillAtFiftyLocksTheQuestOnTheBoardToo` (49.9 offered, 50.0 not).
  Headless: all 26 at 50 puts **cliloc 1077772 on the wire**, spoken by the board.

### 4.3 A quest taken at the board is not the trainer's to take back

The instance records `QuesterType = NewHavenQuestBoard`. Recaro's step 1 matches only his own type, and his step 4 skips
a quest the player is doing, so he says 1080107 "I'm sorry, I have nothing for you at this time". Pinned on the wire in
`AQuestTakenAtTheBoardIsNotTheTrainersToTakeBack`. The reverse should hold by the same code, a quest taken from Recaro goes back to Recaro; **read from source, not pinned**.

### 4.4 A held quest is saved against the board's serial, and dies with it

`MLQuestInstance.Serialize` writes the quester's **serial only** (`MLQuestEntry.cs:520`), and `Deserialize` drops the
instance if that entity is gone (`:536-548`; upstream's own TODO says "Serialize quester TYPE too"). **So deleting the
board silently removes every board quest every player holds, at the next restart**, even though a replacement board
would take them over while the server keeps running. **Read from source, not probed across a restart.** It is why
`Place()` moves a board and never replaces one. It applies equally to the seeder's `replace` mode for the trainers.

### 4.5 `MaxConcurrentQuests` left alone

Still `10` (`MLQuestSystem.cs:17`), untouched, as the wishlist said. The board does not change it.

---

## 5. D-90: our own content

| # | What | Player-visible effect | Reverses when |
|---|---|---|---|
| **D-90** | A New Haven training board: a standing bulletin board at the town square, `(3502, 2573, 14)` Trammel, that offers the 26 stock New Haven skill-training quests through the stock ML quest path, one at a time, and takes them back when they are done. **It never existed on OSI or in ServUO.** | A new player can take the New Haven training quests from the tile they arrive on, without finding 26 trainers across town first. The quests, their text, rewards and the 50-point lockout are unchanged; only where you can pick them up is new. A wiki will not mention the board. | **Stock skill-gain rates.** `ClusterFSkillGain` at `chanceAttempts` 1 and `amountMultiplier` 1 (or disabled: `clusterf.skillGain.enabled`) restores the window in which walking town to find trainers is feasible, and the board stops being necessary. To reverse: `[remove` every board in the world **after warning players** (section 4.4: held board quests are dropped at the next restart), then delete `NewHavenQuestBoard.cs` and its test in a later deploy, once no save holds the type. Reach: 26 quests, one item. |

**The fidelity argument, written out.** This project ports content unchanged so a player can use UOGuide and Stratics
instead of a wiki only we can write, and every deviation is documentation debt only we can pay. Until now every piece
of work was a port or a fix. This is the first thing we have **invented**, and a player will find it on no wiki. So
the question is not whether it is useful, but whether it pays for the debt.

It does, because of a deviation we already made. The 26 quests are OSI content and the board changes none of them. What
makes them unreachable is **our** skill gain: `ClusterFSkillGain` at 3 attempts and 5x amount (live
`Configuration/modernuo.json`: `clusterf.skillGain.chanceAttempts` 3, `amountMultiplier` 5; defaults
`ClusterFSkillGain.cs:8-9`). On OSI a new player has hours between a starting 30 and the lockout at 50, enough to wander
New Haven and find trainers. On ours it is minutes, and whatever is not claimed in those minutes is gone for good, which
Chase confirmed in a client with Recaro (cliloc 1077772, "I cannot teach you, for you know all I can teach!"). So a
player on this shard already cannot have the OSI experience of these quests. The choice is between the OSI *location*
of the quests with most of them unreachable in practice, and a non-OSI *location* with all of them reachable. The
second is closer to what a player reading UOGuide's New Haven pages expects to be able to do.

The debt is kept small on purpose: **stock quests, stock gumps, stock text, stock rewards, stock lockout, stock cap**.
The board chooses nothing; the engine chooses. The only non-OSI facts a player must learn are "there is a board" and
"bring it back to the board", and the board's own tooltip says the second. It needs a shard-wiki entry saying it
exists, that it gives the standard quests, and that the 50-point lockout is OSI behaviour rather than ours (the
wishlist's "wiki debt" line, unchanged).

**For `docs/fidelity-principle.md`** (Claude promotes; `docs/` was not edited here): D-90 as above. If Q-058 goes to
option 2 (a picker), D-90 widens to "with our own quest menu" and should be restated then.

---

## 6. Verification

| Step | Result |
|---|---|
| Build 1 (09:38) | **red at compile, my test**: `HasGump`/`CloseGump` need `using Server.Gumps` |
| Build 2 (09:41) | **red, test host crashed**: `DllNotFoundException: libdeflate`. See 6.1 |
| Build 3 (09:45) | board facts all green; **red on `CC6Batch8…TheDragonsFireColumn…`**, the fireball fact. See 6.2 |
| Bisect (09:47) | the same tree **without my test**: 129/129 green |
| Flake measurement | 10 full runs each way with build.sh's own logger, plus earlier runs: **without my test the fireball fact failed 4/10**, with it 3/10. Pre-existing on HEAD |
| **Red run** (09:55) | override disabled (method renamed, so stock `QuestGiverItem.OnDoubleClick` runs): **red, exactly one fact**: `DoubleClickFromTheGroundReachesTheQuestSystem`, "Item not found: (board, 1077772)", **collection: `[(0xFFFFFFFF, 1042593)]`**, i.e. "That is not in your backpack" and nothing else. Restored |
| Probe builds (09:57, 10:00, 10:05, 10:09) | green, 136. Three probe fixes were mine (6.3) |
| Headless run 1 (10:09, probe image `5016a4c7f841`, fresh save) | section 6.4 |
| Headless run 2 (10:11, reload run 1's save) | `Loading world done (623 items, 91 mobiles)`; **`boards present from save: 1`**, same serial `0x40000274`, same tile; `Place()` twice: "already at (3502, 2573, 14) Trammel (1 on Trammel)"; save, shutdown, no error |
| FINAL build (probe deleted), attempts 1-3 (10:13-10:15) | **red, not mine**: attempts 1 and 3 the fireball flake; attempt 2 `CC6Batch4…TheFairyDragonRunsMageAIAndDropsItsWingAndOrb`, "1 draconic orb in 100 kills, range 2-25", a ~0.03% draw (Binomial(100, 0.1) ≤ 1) in a statistical fact that runs before mine |
| **FINAL build, attempt 4** (10:16) | **green**: 17 patches at `--fuzz=0`, `structured customizations installed: 640` (+1), `shard tests installed: 24` (+1), **136 tests passed** (129 + 7), image **`sl-modernuo:qboard`** (`dc74c1d74e7a`). **Not tagged `latest`**, so nothing here can reach the live container |
| Headless run 3 (final image, fresh save) | `Loading world done (617 items, 90 mobiles)`, no board placed by anything, save, shutdown; no warning but the usual three (`stats` already registered, no accounts, no owner account) |

`tools/progress.py` says 137 tests; xUnit ran 136. Its count was 130 against xUnit's 129 before this change, so the +1
is pre-existing and the +7 is right.

### 6.1 The test host cannot send a gump

The builder stage has no native `libdeflate` (the runtime stage installs `libdeflate-dev`, `docker/uo/Dockerfile:56`).
Every gump is deflate-packed on compile (`DynamicGump.Compile` -> `OutgoingGumpPackets.WritePacked`), and the first
attempt throws in `LibDeflateBinding`'s constructor, then again in its finalizer, which **kills the test host**.
**So no shard test can put a gump on a NetState**, which nobody had needed until now. The facts stop at what the stock
engine decides and at the plain messages it sends (0xC1 localized messages need no deflate), read off a real
`PacketTestUtilities.CreateTestNetState()`. The gump-level behaviour (the offer, the progress gump for a held quest,
the report-back) is proved in headless run 1 on the runtime image instead. Worth knowing before the next quest task
writes a gump assertion.

### 6.2 The fireball fact is flaky on HEAD

`CC6Batch8Verification.TheDragonsFireColumnLaysEightFieldsThatBurnOutAndAFieldCaughtBySaveDeletesItselfOnLoad`,
"the stygian fireball did no damage in 4 s". It runs **before** my class in every run (checked in each log), passed
6/6 alone, and failed in streaks of consecutive full runs whether or not my test was present, which suggests a
wall-clock dependency rather than pure chance. **Not fixed here**: it is batch 8's test, and it is flagged as a
separate task. Until it is fixed, `build.sh` goes red on it roughly one run in three; re-run, and read which fact failed.

### 6.3 The test's seven facts

| Fact | Pins |
|---|---|
| `BoardIsQuesterForExactlyTheTwentySixNewHavenTrainingQuests` | 26 distinct types, 26 on the board, the same instances as the trainers, each one `GainSkillObjective` at 500 with `UseReal`, one skill each, `OneTimeOnly`; `0xA0C5`, immovable; registering twice adds nothing |
| **`DoubleClickFromTheGroundReachesTheQuestSystem`** | **the override.** A board in the world, not in the pack: the engine answers (1077772 from the board's serial) and 1042593 never appears; out of reach gives 1019045. **Watched red** with the override removed |
| `OffersEveryUntakenQuestAndNothingElse` | a fresh character: all 26 on offer (2000 stock picks); one skill open: exactly that quest |
| `HeldQuestIsNeverOfferedAgain` | Fencing and Mining open; accept Fencing: the instance's quester type is the board, and only Mining remains on offer |
| `CompletedQuestIsNeverOfferedAgain` | the real turn-in, `RecarosRiposte` in the pack, skill back to 30.0, still refused (`OneTimeOnly`) |
| `SkillAtFiftyLocksTheQuestOnTheBoardToo` | 49.9 offered, 50.0 refused; **Chase's character (Fencing 51.0, rest fresh): 25 on offer, EnGuarde not among them** |
| `AQuestTakenAtTheBoardIsNotTheTrainersToTakeBack` | Recaro says 1080107 to a board-quest holder, on the wire; deleting the board leaves the instance, still typed to the board, while the server runs |

**The brief asked for a fact that the board "does offer" a quest whose skill is past 50, as the one that would go red
if the override regressed.** That fact would be false: the lockout is the objective's, not the backpack check's, and
the board keeps it (Q-059). The fact that goes red on a regressed override is `DoubleClickFromTheGround…`, and it was
watched going red.

### 6.4 Headless run 1, what reached the player

The probe (`server/customizations/Probe/NewHavenQuestBoardProbe.cs`, **deleted before FINAL, never committed**) ran 3 s
after start on a fresh save with the live config's copy (seeder on, ML quests on, skill gain 3/5):

- `ClusterF New Haven seed complete: created 40`; **Sir Helper on the arrival tile**; `quests on the board: 26`.
- Map, from the server's own tile matrix: arrival `land 0x03E9 z14`, board tile `land 0x03FB z14`, no statics on
  either; statue tile `0x2FF6@20` over the steps; `CanFit` true.
- `Place()`: "placed at (3502, 2573, 14) Trammel"; again: "already at … (1 on Trammel)". Board `0xA0C5`, immovable,
  named. **In reach from the arrival tile: True.**
- **A real player, a real socket.** A `PlayerMobile` with a fresh character's skills (three at 30), standing on the
  arrival tile, attached to a NetState the server accepted from a real TCP connection to its own `127.0.0.1:2593`.
  Double-click: **`QuestOfferGump` on the NetState; on the client socket, a `0xDD` compressed gump, 459 bytes,
  layout 1,543 chars, carrying the random pick's title cliloc 1077576 and description 1077577 (`TheMagesApprentice`)**.
  An earlier run of the same probe drew `EnGuarde` (1078186 / 1078190).
- Accepted: instance typed to the board. **10 clicks: 0 offers, 10 progress gumps.** Magery to 50: **report-back
  gump**. Turned in: `EmberStaff` in the pack, quest done; back to 30: **0 re-offers in 40 clicks**.
- Fencing 51: the stock pick covers 24 quests (26, less Fencing, less the finished Magery), **EnGuarde never**.
- All 26 at 50: no offer gump, **cliloc 1077772 on the wire**.
- Save, shutdown, no error, no exception.

Three probe bugs were mine, each costing a probe rebuild: I read the NetState list 1 s after connecting without sending
a seed (0 NetStates; a null reference then shut the server down), I walked the packet stream as if every packet were
length-prefixed (0x1D is fixed-length), and I wrote cliloc 1077772 as `0x107074` instead of `0x10720C`.

### 6.5 Not verified

- **In a real client**: that `0xA0C5` renders as the standing board it is named as, the five tooltip lines display
  (and are not truncated), and a new character's double-click from the arrival tile looks right. The wire bytes are
  right; how a client draws them is a client check. For `docs/client-check-backlog.md`.
- **`[PlaceNewHavenQuestBoard` itself** was not typed at a console (the container console takes only
  `save`/`shutdown`/`restart`); the probe called the method it calls, `Place()`.
- **Section 4.4 across a restart**: read from source, not probed.
- **Whether the live world has anything at `(3502, 2573)`** that a fresh world does not. The live save was not opened
  (it is not ours to read). Placement uses `MoveToWorld`, so it cannot fail, but a GM should look before running it.

---

## 7. What the brief had wrong, for the record

1. **"Batch 8 used D-79 through D-86."** It used through **D-89** (`notes/cc6-batch8.md:105-109`, `:171-173`: D-87
   `BloodDrinker`, D-88 the Gorgon Lens, D-89 statue animation). Next free is **D-90**. Q-057 was the highest Q; next
   free **Q-058**. Counted with `grep -rhoE "\b[DQ]-[0-9]+\b" notes docs | sort -u`.
2. **"`useReal: true` means gain before accepting counts."** See section 3: the absolute threshold does that; `useReal`
   makes items and stats count.
3. **"Take ten … take ten more."** Not reachable from one quester (Q-058).
4. **"A character past 50 can still accept that skill's quest."** Contradicts the brief's own board line 3 and the
   wishlist; not built (Q-059). What holds: the other 25 stay on offer.
5. **"The same shape as the Fountain of Fortune (Q-021)."** Q-021 was answered ("place it at its OSI coordinates"),
   but **nothing in the tree places a fountain**: `grep -rn "1121, 957\|FountainOfFortune()" server/` finds only the
   constructor and the test. The answer was never implemented. So "the shape" here is the one the repo actually uses
   for placement, a GM command in the file (`[SetupDespise`, `[ClusterFSeedNewHaven`), rather than a world-load hook.
   The fountain being unplaced is its own loose end, not fixed here.
6. **"Place it where new characters arrive, not decoratively in the square."** Here they are the same place.

---

## 8. For Chase: placing it (a deploy, not done)

1. Push, and deploy through the usual route. The class ships inert: nothing places a board on load.
2. In game, as Administrator: **`[PlaceNewHavenQuestBoard`**. Expect "New Haven training board placed at (3502, 2573,
   14) Trammel." Running it again only reports or moves it back. **Never `[remove` it casually**: every player's held
   board quests go with it at the next restart (section 4.4).
3. Client check: stand on the arrival tile, hover, double-click.

---

## 9. What it cost

| Phase | Time |
|---|---|
| Reading the spec, AGENTS, the ML quest engine, `CharacterCreation`, the seeder, regions, statics, tiledata, art | ~25 min (to ~09:35) |
| Writing the board and the first test | ~5 min |
| Builds 1-3 and the libdeflate rewrite of the test | ~8 min (09:37-09:45) |
| The fireball bisect and flake measurement | ~9 min (09:45-09:54) |
| The red run | ~2 min |
| Probe: four builds, three headless runs (three bugs of mine) | ~17 min (09:55-10:12) |
| FINAL: four attempts (three pre-existing flakes), run 3 | ~6 min (10:13-10:18) |
| Questions and this note | ~15 min |

About an hour and a half, against the wishlist's "one file, roughly 80 lines, no patch". The file is 147 lines with no
patch; the rest went on proving the stock path's behaviour, which is where the wishlist was wrong, and on a flaky test
that was not ours.

## 10. Questions opened

- **Q-058** - one quest at a time, random pick: keep, or add a picker (~120-150 lines, no patch)? Not blocking.
- **Q-059** - "past 50 can still accept": keep the stock lockout (built), or a separate, larger deviation? Not blocking.

No placement question: arrival point and square are the same spot (section 2).
