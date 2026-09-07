# S5 — one ServUO quest translated onto ModernUO's ML quest engine

**Status: done. The mapping holds for four of five objective types, and the fifth is not
a mapping problem.** Committed 2026-09-07. Answers Q-023.

`JourneyToTheAthenaeumIsleQuest` builds through `docker/uo/build.sh`, registers, is offered
by its quester, tracks both of its objective types, completes, and pays the right reward.
Five new tests, all passing; the gated build is green at **14 tests** (4 S1 + 5 S2 + 5 S5).

The honest headline is narrower than "it works", and the narrowing is the useful part:

> **The objective mapping is not the constraint. The bespoke-objective tail is.**
> 164 of the 203 missing quests use exactly one standard objective type and translate
> mechanically. **39 do not**, because they hand-write a `BaseObjective` subclass that has
> no counterpart on either side of the table — 25 of them a class literally called
> `InternalObjective`. `QuestionAndAnswerObjective` is 2 of those 39, not the whole tail.
> Counts and the full class list in section 8.

---

## 1. What was translated, and why that one

**`JourneyToTheAthenaeumIsleQuest`** (ServUO `Scripts/Quests/JourneyToTheAthenaeumIsleQuest.cs`,
175 lines), offered by `QueenZhah` (`Scripts/Mobiles/NPCs/Zhah.cs`). Ter Mur / Stygian Abyss,
in scope: `Configuration/expansion.json` runs Endless Journey with `SA` true.

It is **the only quest in ServUO that uses two different standard objective types in one
definition.** Scanned all 6,144 script files for classes containing `AddObjective`, grouped
each class body by the `new *Objective(` types inside it:

| Quests using ≥2 distinct objective types | Result |
|---|---|
| `JourneyToTheAthenaeumIsleQuest` | `SlayObjective` + `ObtainObjective` — **the pick** |
| `TheGreatVolcanoQuest` | `InternalObjective` + a **commented-out** `ObtainObjective` |
| `FindCallingScrollObjective`, `KillHordeMinionsObjective`, `FindIngredientObjective` | `QuestObjective`, the **pre-ML** quest system (DarkTides, UzeraanTurmoil, WitchApprentice). Different engine entirely, not in scope. |

So the brief's "pick a quest that tests at least two of those" has exactly one answer in the
whole content source. That is itself a finding: **ServUO's 408 ML quests are almost entirely
single-objective-type**, which is why the per-quest translation is as mechanical as it turned
out to be.

Verified missing before starting: `grep -rn "Athenaeum" D:\UO\ModernUO-pinned\Projects\`
returns nothing, and all 13 dependent types are absent (table in section 3).

### Why not a Valley of One quest

**The seven Valley of One quests are unrepresentative, and would have proved less than this
one does.** None of the seven uses two objective types, and three of the seven use a
hand-written `InternalObjective` that has no counterpart at all:

| Quest | Objectives | Reward |
|---|---|---|
| `TimeIsOfTheEssenceQuest` | 1 × `DeliverObjective` (360 s timer) | message only |
| `UnitingTheTribesQuest` | 5 × `ObtainObjective` | item |
| `TheGreatHuntQuest` | 1 × `SlayObjective` | item |
| `EmptyNestQuest` | 1 × **`InternalObjective`** | item |
| `TheGreatVolcanoQuest` | 1 × **`InternalObjective`** | item |
| `PrideOfTheAmbushQuest` | 1 × **`InternalObjective`** | item |
| `TheGreatApeQuest` | 1 × `SlayObjective` | item |

That is the one-line answer the brief asked for, and it comes with a consequence worth
stating: **Valley of One is a bad first batch.** 3 of 7 need a hand-written objective, which
is a much higher bespoke rate than the 19% across the 203. Section 8 names better batches.

---

## 2. Verdict, objective by objective

The three questions per row are the brief's: **same inputs**, **same trigger**, **same
player-visible result**.

| ServUO | ModernUO | Inputs | Trigger | Player-visible result | Verdict |
|---|---|---|---|---|---|
| `SlayObjective` | `KillObjective` | same | same | same | **Holds** — proven by test |
| `ObtainObjective` | `CollectObjective` | same | same | same | **Holds** — proven by test |
| `ApprenticeObjective` | `GainSkillObjective` | units differ ×10 | same | **loses region-scoped gain and its enter/leave messages** | **Holds with a named loss** — and upstream already made this exact translation |
| `DeliverObjective` | `DeliverObjective` | destination *name* moves to an attribute | same | same, **if** `[QuesterName]` is set | **Holds with a required extra step**; no `StartingItem` |
| `EscortObjective` | `EscortObjective` | fame/compassion stop being parameters | same | same for every ServUO call site | **Holds** — the dropped parameters are unused across all 30 uses |
| `QuestionAndAnswerObjective` | — | — | — | — | **No counterpart.** Out of scope by the brief; 2 files |

Nothing here was declared to hold because the build was green. Two rows are pinned by tests
that fail if the behaviour moves; three are read from source and are marked as read, not run.

### 2.1 Slay → Kill — holds. Verified by test.

`KillObjectiveCountsThroughHandleKill`.

- **Inputs.** ServUO `SlayObjective(Type[] creatures, string name, int amount, string region,
  int seconds)`. ModernUO `KillObjective(int amount, Type[] types, TextDefinition name,
  QuestArea area)`, plus `TimedKillObjective(TimeSpan, …)`. Same five inputs. The region is a
  name string on both (`QuestHelper.FindRegion(name)` vs `QuestArea(name, region, forceMap)`);
  ModernUO's `QuestArea` additionally takes an optional `ForceMap`, which ServUO has no way to
  express. Strictly more expressive, not less.
- **Trigger.** ServUO `SlayObjective.Update(Mobile)`. ModernUO `MLQuestSystem.HandleKill`,
  called from `BaseCreature.cs:3376` in `OnDeath`. Both use `IsAssignableFrom`, so subclasses
  count on both. Both check the region/area containment on the *creature*, not the player.
- **Player-visible.** Byte-identical messages: `1075050` ("You have killed all the required
  quest creatures of this type") on the last kill, `1075051` ("~1_val~ more left") otherwise.
  Both count past the target rather than clamping. Gump line: ServUO draws cliloc `1072204`
  ("Slay") + count + name; ModernUO's `KillObjective.WriteToGump` draws `1072204` + count +
  name. Same cliloc, same order.

### 2.2 Obtain → Collect — holds. Verified by test.

`CollectObjectiveCountsOnlyMarkedQuestItems`, `QuestCompletesAndPaysTheRightReward`.

- **Inputs.** ServUO `ObtainObjective(Type obtain, string name, int amount, int image, int
  seconds, int hue)`. ModernUO `CollectObjective(int amount, Type type, TextDefinition name)`
  + `TimedCollectObjective`. **`image` and `hue` have no counterpart**: ModernUO derives the
  gump item image from the cliloc via `CollectObjective.LabelToItemID`. In practice this
  matters only for detailed rendering, and it has an escape hatch — see section 2.2.1.
- **Trigger.** Same on both, and it is the same player action: toggling quest-item status on
  an item in the backpack. ServUO `ObtainObjective.Update(Item)` sets `QuestItem` and adjusts
  a stored `CurProgress`; ModernUO `MLQuestSystem.MarkQuestItem` → `OnMarkQuestItem` →
  `CollectObjectiveInstance.CheckComplete`.
- **Player-visible.** Same. Both mark the item and send `1072353` / `1072354` on toggle;
  ModernUO sends them from `PlayerMobile.cs:4030/4034` rather than from the objective. Both
  also refuse an item inside a sub-container with the same `1074769` — checked, because a
  difference there would have been invisible in a test that drops items straight into the
  pack (ServUO `Items/Containers/Container.cs:128`, ModernUO `PlayerMobile.cs:4024`).

  **One real internal difference, and it favours ModernUO.** ServUO stores an incrementing
  `CurProgress`; ModernUO recomputes `GetCurrentTotal()` from the backpack on every check.
  ServUO's counter can drift out of step with the pack — drop a marked item and the counter
  does not move. ModernUO cannot drift. The test pins the ModernUO semantics explicitly
  (mark → complete, unmark → not complete) so a regression in either direction shows.

#### 2.2.1 The gump-render gap, and why it closed

This is the one place the translation needed a decision rather than a rename.

ServUO's `BaseQuest` lets a quest override `RenderObjective(MondainQuestGump, bool)` and draw
its own objective page. This quest does exactly that: it passes developer strings
("Obtain Gargish Document - Challenge Rite") to the ten `ObtainObjective`s **and then throws
them away**, drawing clilocs `1150933`–`1150942` instead, one plain line per document
(`JourneyToTheAthenaeumIsleQuest.cs:110`).

**ModernUO's `MLQuest` has no per-quest gump override.** Objectives write themselves through
`BaseObjective.WriteToGump`. On the face of it that is a lost capability.

It is not, here. `CollectObjective.ShowDetailed => false` renders exactly the one-line
localized form ServUO hand-drew, instead of "Obtain ⟨n⟩ ⟨item⟩" plus an item image. So the
cliloc goes onto the objective where ServUO put the throwaway string, and the player sees the
OSI line. Upstream precedent for the same move: `Definitions/Heritage.cs:102` and
`Definitions/BlightedGrove.cs:105`.

It also avoids a latent bug: `LabelToItemID(1150933)` yields 72061, far outside the valid
0x0001–0x4000 item range. ModernUO warns about this in debug mode. `ShowDetailed = false`
skips that call entirely.

**Cost of the general case, if a future quest needs a render ModernUO cannot express:** the
options are a `BaseObjective` subclass with a custom `WriteToGump` (additive, no patch —
that is what `GargishDocumentObjective` is), or a patch to `QuestLogDetailedGump` /
`QuestOfferGump`. So far only the first has been needed.

### 2.3 Apprentice → GainSkill — holds, with a named loss

**Not exercised by this quest.** Read from source, and corroborated by something better than
reading: **upstream has already made this exact translation, for these exact quests.**

ServUO's New Haven skill-training quests use
`ApprenticeObjective(SkillName.Chivalry, 50, "Old Haven Training", 1077720, 1077721)`.
ModernUO's `Definitions/NewHavenSkillTraining.cs:27` has
`new GainSkillObjective(SkillName.Chivalry, 500, true, true)` for the same quest. All 20-odd
follow the same shape. So the mapping is not a hypothesis; it is what ModernUO already ships.

- **Inputs.** `cap 50` → `thresholdFixed 500`: ServUO compares `Skills[skill].Base >=
  MaxProgress`, ModernUO compares `BaseFixedPoint >= ThresholdFixed` (tenths). **A port that
  copies the number instead of multiplying it by ten produces a quest that completes
  instantly.** ServUO's `useReal` equivalent is implicit (`.Base`); ModernUO makes it a flag
  and upstream passes `true`, which is `.Fixed`, not `.Base` — a deliberate upstream choice,
  not ours to second-guess.
- **Trigger.** Both fire on a skill-gain check. ServUO `Update(Skill)`; ModernUO
  `GainSkillObjectiveInstance.IsCompleted()` re-reads the skill.
- **Player-visible, and here is the loss.** ServUO's acceleration is **region-scoped**: an
  `ApprenticeRegion` turns accelerated gain on while the player is inside it, and the two
  cliloc arguments are the enter and leave messages. ModernUO's `Accelerate` flag instead
  grants the **Scroll of Alacrity** mechanism — `pm.AcceleratedSkill` plus a fixed
  **15-minute** window from acceptance (`GainSkillObjective.cs`, consumed at
  `Skills/SkillCheck.cs:245`). Different shape, and the enter/leave messages have nowhere
  to go.

  ModernUO also **adds** a gate ServUO's objective does not have: `CanOffer` refuses with
  `1077772` ("I cannot teach you, for you know all I can teach!") when the player is already
  at or above the threshold.

- **Cost to close the gap.** An `ApprenticeRegion` equivalent is a `Region` subclass with
  `OnEnter`/`OnExit` setting and clearing `AcceleratedSkill`, plus region definitions. Call
  it one file and a definitions blob; not costed further, because **it affects exactly 1 of
  the 203 missing quests** (section 8) — every other Apprentice quest is already shipped by
  ModernUO. Not worth building for one quest.

### 2.4 Deliver → Deliver — holds, with a required extra step

**Not exercised by this quest.** Read from source.

- **Inputs.** ServUO `DeliverObjective(Type delivery, string deliveryName, int amount, Type
  destination, string destName, int seconds)`. ModernUO `DeliverObjective(Type delivery, int
  amount, TextDefinition name, Type destination, bool spawnsDelivery)` + `TimedDeliverObjective`.

  **`destName` has no parameter.** ModernUO renders the destination as
  `QuesterNameAttribute.GetQuesterNameFor(Destination)`, which falls back to the raw C# type
  name when the attribute is absent. So **every Deliver quest ported must put `[QuesterName]`
  on its destination type or the quest log shows a class name to the player.** That is a
  one-line-per-type step, not a gap, but it is a step a mechanical translation will skip.

  ModernUO **adds** `spawnsDelivery`, which ServUO expresses through `Quest.StartingItem`
  instead — see below.

- **Trigger.** Same action, different type test. ServUO `Update(object)` fires when the
  object is a `BaseVendor` assignable to `Destination`. ModernUO `MLQuestSystem.HandleDelivery`,
  reached from `OnDoubleClick(IQuestGiver, PlayerMobile)`. Both are "double-click the
  destination NPC". ModernUO's is the wider net (`IQuestGiver`, not `BaseVendor`).

- **Player-visible, two differences.**

  1. **Full-backpack behaviour is opposite.** ServUO's `OnAccept` calls `PlaceInBackpack` per
     item and, on failure, sends `503200` + `1075574` and **removes the quest**. ModernUO's
     `SpawnDelivery` calls `pack.DropItem` unconditionally, with the comment "Confirmed: on
     OSI items are added even if your pack is full". Both are deliberate; ModernUO claims the
     OSI behaviour and ServUO implements a guard. Under the fidelity principle ModernUO's is
     the one to keep. **No action, log only.**
  2. **`Quest.StartingItem` has no counterpart.** ServUO supports a quest begun by
     double-clicking an item rather than an NPC, and `DeliverObjective` branches on it in both
     `OnAccept` and `Update`. ModernUO's engine has no item-started quest concept.
     **Cost, unmeasured** — it needs a `MLQuestSystem` entry point and an item base class, and
     it is a *framework* gap, not a per-quest one. Flagged as **Q-025** rather than guessed at.
  3. Failure message is identical on both: `1074813`.

- **Two-step hand-in.** ModernUO splits the hand-in that ServUO does in one go:
  `MLQuestInstance.ContinueReportBack` consumes the collected/delivered items and sets
  `ClaimReward`; `ClaimRewards` creates the reward. Two gump clicks, which is OSI's own flow.
  This bit the spike — see section 5.2 — and the test now drives both steps in order.

### 2.5 Escort → Escort — holds

**Not exercised by this quest.** Read from source.

- **Inputs.** ServUO `EscortObjective(string region, int fame = 10, int compassion = 200, int
  seconds = 0, int label = 0)`. ModernUO `EscortObjective(QuestArea destination)` — destination
  only. Fame and compassion are hardcoded in `EscortObjectiveInstance.CheckDestination`:
  `Titles.AwardFame(pm, 10, true)` for young players and Haven Island, otherwise
  `VirtueSystem.AwardVirtue(pm, VirtueName.Compassion, 200)` — **400** for a prisoner escort,
  which ServUO's default cannot express at all.

  Dropping two parameters looks like a loss. It is not, and this is measurable:
  **all 30 `new EscortObjective(` call sites in ServUO pass either `(region)` or
  `(label, region)`. Zero pass fame or compassion.** So the mapping loses nothing that
  ServUO's content actually uses.

  The `label` cliloc is the one input with nowhere to go; ModernUO renders
  `Destination.Name`, which is a `TextDefinition` and therefore takes the same cliloc. Same
  value, different field.

- **Trigger.** Both poll on a 5-second timer for the escort creature being inside the
  destination region, and both abandon on the player being out of range for too long.
- **Player-visible.** ModernUO says `1042809` on arrival ("We have arrived! I thank thee,
  ~1_PLAYER_NAME~!") and auto-opens the reward via `MLQuestSystem.OnDoubleClick`.
- **One ServUO behaviour with no counterpart, and it is not an escort behaviour.**
  `EscortObjective.OnCompleted` schedules `ResponsibilityQuest` for a murderer who has not
  done it. That is a hook into a different quest, not part of escorting; it drops out with
  `ResponsibilityQuest` itself, which ModernUO also lacks. **Log only.**

---

## 3. What the port actually cost

**6 files, 1,063 ServUO lines in, 745 ModernUO lines out, plus a 284-line test.**

| Ported | ServUO source | Lines in | Lines out |
|---|---|---|---|
| `Engines/ML Quests/Definitions/AthenaeumIsle.cs` | `Quests/JourneyToTheAthenaeumIsleQuest.cs` + `Mobiles/NPCs/Zhah.cs` | 245 | 144 |
| `Items/Books/GargishDocuments.cs` | same path | 448 | 232 |
| `Items/Books/BaseLocalizedBook.cs` | same path | 129 | 141 |
| `Items/Books/Note.cs` | same path | 88 | 73 |
| `Mobiles/Normal/MinionOfScelestus.cs` | same path | 153 | 155 |
| **total** | | **1,063** | **745** |
| `server/tests/Engines/MLQuests/AthenaeumIsleQuestVerification.cs` | — | — | 284 |

**Every one of the 13 dependent types was absent from pinned ModernUO**, checked before the
first build per the `LuckyCoin` rule:

`QueenZhah`, `MinionOfScelestus`, `ChallengeRite`, `AnthenaeumDecree`, `LetterFromTheKing`,
`OnTheVoid`, `ShilaxrinarsMemorial`, `ToTheHighScholar`, `ToTheHighBroodmother`,
`ReplyToTheHighScholar`, `AccessToTheIsle`, `InMemory`, `ChronicleOfTheGargoyleQueen1` — all
`MISSING`. The array walk then found two more one level down: `BaseLocalizedBook` and `Note`,
the base classes of the ten documents. Neither exists in ModernUO, and neither has an
equivalent under another name — `Items/Books/` upstream is `BaseBook`, `BookContent`,
`BookPageInfo` and four coloured books, all authored-text, none cliloc-paged.

**The ratio is the point: 12% of the work was the quest, 88% was its content.** The objective
translation is 15 lines. The books, the creature and the NPC are 730.

---

## 4. Registration: how the quest reaches the engine

ServUO's `MondainQuester` declares its quests with `public override Type[] Quests`. ModernUO
maps quester type → quest list inside `MLQuestSystem`, populated from
**`Distribution/Data/MLQuests.cfg`** — a tab-separated data file, one line per quest, and the
route every one of upstream's 240 quests uses.

**We cannot use that route as-is.** `apply-patches.sh` mirrors `.cs` only and explicitly
reports anything else as "not installed", so the cfg would have to be a `.patch` against a
307-line **CRLF** data file whose tail changes whenever upstream adds a quest. That is a patch
built to break on a bump, and to break at the end of the file where the diff context is
weakest.

**Chosen instead: `MLQuestSystem.Register(quest, questerTypes)`, a public method on the engine
itself**, called from a `Configure()` hook in our own file
(`Engines/ML Quests/Definitions/AthenaeumIsle.cs`). Ordering is safe and checked, not assumed:
`Projects/Server/Main.cs:441` invokes every `Configure()` before
`Projects/Server/Main.cs:448` invokes any `Initialize()`, and `MLQuestSystem.Initialize()` is
what calls `Generate()` on each registered quest. Our registration therefore lands before the
engine walks its table.

This is using the engine's API, not adding a second mechanism: `Register` is the same method
the cfg loader calls internally.

**But it is unexercised upstream.** `grep -rn "MLQuestSystem.Register" D:\UO\ModernUO-pinned\Projects\`
returns nothing outside `MLQuestSystem.cs` itself. Every stock quest comes from the cfg file.
A public API with zero upstream callers is exactly the kind of thing that gets refactored away
or reordered without anyone noticing, so `QuestIsRegisteredAndOfferedByItsQuester` exists
specifically to fail when it does. That test is the whole reason this choice is safe to make.

---

## 5. Verification: what ran, what did not, and what the route could not do

Route: S4's. `server/tests/Engines/MLQuests/AthenaeumIsleQuestVerification.cs`, mirrored to
`Projects/UOContent.Tests/Tests/…`, run by `docker/uo/build.sh`.

```
docker/uo/build.sh -t sl-modernuo:s5
```

**Result: 13 patches applied, 14 tests passed, `sl-modernuo:s5` built, exit 0.**

| Test | What it pins |
|---|---|
| `QuestIsRegisteredAndOfferedByItsQuester` | `MLQuestSystem.Register` put the quest in the table and in `QueenZhah.MLQuests`; `CanOffer` passes for a fresh player |
| `ObjectivesTranslateOneForOneFromServUO` | 11 objectives in ServUO's order, `ObjectiveType.All`, 1 reward, the ten clilocs `1150933`–`1150942`, `ShowDetailed` false, `OneTimeOnly`/`HasRestartDelay` false — i.e. ServUO's `BaseQuest` defaults |
| `KillObjectiveCountsThroughHandleKill` | 10 kills through the real `MLQuestSystem.HandleKill` entry point, asserted one at a time |
| `CollectObjectiveCountsOnlyMarkedQuestItems` | an unmarked item in the pack does not count; `MarkQuestItem` completes it; unmarking un-completes it |
| `QuestCompletesAndPaysTheRightReward` | kills alone are not enough; 10 kills + 10 marked documents completes; hand-in consumes all ten documents and pays one `ChronicleOfTheGargoyleQueen1` with 500 charges; the instance is removed |

### 5.1 A gap in the S4 test route, found here: no BaseCreature can be constructed

**Every public `BaseCreature` constructor throws in the S4 test host.** The chain is
`BaseCreature..ctor` → `GetSpeeds` → `NPCSpeeds.GetSpeeds`, which does
`_speedsByLevel[SpeedLevel.Medium]` and raises `KeyNotFoundException` when the table is empty.
`NPCSpeeds.Configure()` fills it from `Data/npc-speeds.json` and **returns silently** when the
file is not under `Core.BaseDirectory` — which in the test host it is not.

This is not our bug and not new. Upstream hit it too and worked around it by constructing
creatures through the `Serial` deserialization constructor:
`UOContent.Tests/Tests/Engines/Pathing/BitmapAStarAlgorithmTests.cs:356`, comment "requires
the npc-speeds.json table loaded — not available in tests".

A quest test has to build real creatures, so the fixture registers the table's `Medium` row
itself, values verbatim from pinned `Distribution/Data/npc-speeds.json`
(`active 0.25`, `passive 0.5`).

**This will bite every future creature or quest test, and the fix belongs in the route rather
than in each test file.** Raised as **Q-026**; not fixed here, because changing `build.sh` or
`apply-patches.sh` inside a content spike is exactly the kind of scope creep this project
declines. Four of the five tests failed on this before the workaround, which is the evidence.

### 5.2 One thing the spike got wrong, and what it taught

The first version of `QuestCompletesAndPaysTheRightReward` set `instance.ClaimReward = true`
and called `ClaimRewards()`. **The reward was paid and the ten quest documents stayed in the
backpack.** A test written to a weaker assertion would have called that a pass.

The cause is real engine behaviour, not a bug: ModernUO puts item consumption in
`ContinueReportBack` (the report-back gump click) and reward creation in `ClaimRewards` (the
reward gump click). Setting the flag by hand skips the first. The test now drives both, in
order, as `MLQuestSystem.OnDoubleClick` would.

Worth recording because it is the shape of the failure this project keeps paying for: the
green thing was green for the wrong reason.

### 5.3 What is NOT verified, and needs the batched client spot check

Headless testing reaches the engine but not the client. These are **left unverified and
flagged**, not worked around:

1. **Every gump.** The offer gump, quest log, report-back gump and reward gump are packet
   layouts. `ShowDetailed = false` rendering the ten documents as ten single localized lines
   is read from `CollectObjective.WriteToGump`, **not seen**. So is `BaseLocalizedBook`'s
   paged reader and `Note`'s scroll gump — both were rewritten from ServUO's `Gump` API onto
   ModernUO's `DynamicGumpBuilder`, which is a genuine rewrite, not a rename.
2. **`QueenZhah` renders as a gargoyle.** Body 667, `Race.Gargoyle`, `HairItemID 0x42AB`. No
   gargoyle NPC exists anywhere in pinned ModernUO to copy from, so the body/hair pairing is
   from ServUO and unconfirmed against a client.
3. **`Shout`.** `CanShout`/`Shout` fires from `BaseCreature.OnMovement` at `BaseCreature.cs:2816`
   and needs a moving `PlayerMobile` with a `NetState`.
4. **`MinionOfScelestus` in the world.** Spawning, loot, the mount-knockoff on melee, and the
   return-home teleport. Same status as `GreaterPoisonElemental` from P2.
5. **Nothing places any of it.** No spawner, no `QueenZhah` in the world, no Athenaeum Isle
   teleporter. The quest is registered and completable; it is not *reachable* by a player.
   Deliberate — placement is a separate decision, like the fountain in S2 (Q-021).

---

## 6. Deviations, for `docs/fidelity-principle.md`

| ID | Deviation | Why | Cost to close |
|---|---|---|---|
| **D-S5-1** | `MinionOfScelestus` loses `SetSpecialAbility(SpecialAbility.DragonBreath)` | `SpecialAbility` is ServUO's Pet Training system, declined in CC6. `Saurosaurus` precedent: a creature that loses one ability still ships | the Pet Training subsystem, already costed in S3 |
| **D-S5-2** | `MinionOfScelestus` loses `TaintedLifeAura` | ModernUO's `BaseCreature` has no such flag. ServUO reads it in `BaseWeapon.cs:2773/2787` and `AOS.cs:454` to suppress life leech against the creature | one additive `virtual bool` + **2 patches** into `BaseWeapon` and `AOS`. Both are `UOContent`, not core. Cheap, but it buys one creature |
| **D-S5-3** | `QueenZhah` is undressed | Her seven items — `LeatherTalons`, `GargishLeatherChest`, `GargishLeatherLegs`, `GargishClothWingArmor`, `GargishLeatherArms`, `GargishLeatherKilt`, `SerpentStoneStaff` — are all absent from ModernUO | **~470 ServUO lines across 7 files**, all leaf equipment. Ordinary content work; do it with the next gargoyle-equipment batch, not inside a spike |
| **D-S5-4** | `ChronicleOfTheGargoyleQueen1.Initialize()` became a static initializer | ServUO relies on `Initialize()` being reflection-discovered to fill a constant array. The values are constants; building them in a static field removes the dependency on discovery order | none — behaviourally identical |
| **D-S5-5** | Deliver: full-backpack behaviour differs (ModernUO adds items anyway) | Not our change. ModernUO states it is OSI-correct and ServUO's guard is the deviation. Under `docs/fidelity-principle.md` ModernUO's is the one to keep | none; log only |
| **D-S5-6** | Apprentice→GainSkill loses region-scoped acceleration and its enter/leave messages | ModernUO uses the Scroll of Alacrity 15-minute window instead | an `ApprenticeRegion` equivalent. Affects **1** of the 203 missing quests. Not worth it |

D-S5-1 and D-S5-2 are the honest answer to "does this creature behave like ServUO's": **no, it
loses two abilities.** Its stats, resistances, skills, loot, poison, treasure level, mount
knockoff and home-return are verbatim.

---

## 7. What a batch of ten more would cost

The measurement from this one, split the way it actually divides:

| | This quest |
|---|---|
| Objective translation | **15 lines**, mechanical once the table in section 2 is known |
| Quest + quester definition | 144 lines |
| Content dependencies (items, creature, base classes) | **730 lines across 4 files, 15 types** |
| Test | 284 lines, 5 facts |
| Build cycles | 3 (one `MessageType` namespace error, one NPCSpeeds fixture gap, one two-step hand-in error) |

**A batch of ten, from the 164 single-standard-objective quests:**

- **Objective translation: near zero.** Ten quests × ~15 lines. The table in section 2 is the
  whole recipe, and it does not need re-deriving.
- **Content dependencies: the entire cost, and it is not a quest cost.** Every quest needs its
  items, its target creature and its quester ported first. This one needed 15 types. That is
  ordinary CC-track content work priced at CC rates, and the P2 measurement applies: ~1:10 per
  simple file, batches amortising the build cycle.
- **A shared test file, not ten.** One `[Fact]` per quest asserting objective shape and one
  end-to-end completion per *pattern* (kill, collect, deliver, escort), not per quest. The
  engine is the thing under test and it is the same engine every time.
- **Two per-batch gotchas that will otherwise be silent:** `[QuesterName]` on every Deliver
  destination type (2.4), and `cap × 10` for any GainSkill threshold (2.3).

**Honest estimate: a day for ten, and eight-tenths of it is porting items and creatures, not
quests.** Stated as an estimate, not a measurement — the only measured datum is this one
quest, and its dependency count (15 types) is on the high side because it needed two book base
classes that the next nine will not.

**The cheapest possible first batch is not Valley of One.** Ranked by dependency depth from
section 8's grouping, the `Quests/TieredQuests` and `Town Cryer` clusters are single-objective
Obtain quests against items that are largely already in ModernUO. Valley of One is 3-of-7
bespoke objectives and needs the Eodon creature set underneath it.

---

## 7.1 Phase timings, and a build-cycle number worth correcting

Phase timings are **estimated from the session, not instrumented** — say so rather than
publishing a number that was not measured.

| Phase | Estimate |
|---|---|
| Read `AGENTS.md`, `docs/subsystem-policy.md`, the S3/S4 notes and the S5 brief | ~10 min |
| Choose the quest: scan all 6,144 ServUO files for multi-objective quests, read Valley of One, confirm the pick is missing from ModernUO | ~15 min |
| Read ModernUO's engine: `MLQuest`, `MLQuestSystem`, `MLQuestEntry`, all six objective files, rewards, registration, `IQuestGiver` | ~25 min |
| Dependency walk: 13 named types, then `BaseLocalizedBook`/`Note` one level down, then the gargoyle outfit | ~10 min |
| Write the five source files | ~35 min |
| Write the test | ~15 min |
| Build, fix, rebuild (3 cycles) | ~20 min |
| Map the remaining three objective types against source; classify the 203 | ~20 min |
| Write this note | ~25 min |

**Two build-cycle numbers, measured, not estimated:**

| | Wall clock |
|---|---|
| `build.sh --tests-only`, nothing changed (all layers cached) | **20 s** |
| `build.sh --tests-only`, one changed file under `server/customizations` | **266 s** |

The second is the one that matters, because it is what every edit costs. A changed
customization invalidates the `COPY server/customizations/` layer, which invalidates
`apply-patches.sh` and the full `dotnet publish ModernUO.slnx`, and the test run follows.

**This is materially larger than the 0:44 warm cycle recorded in `notes/cc2-timed-port.md`
for P2, and section 7's "a day for ten" assumes the 266 s figure, not the 44 s one.** I am not
claiming P2 was wrong: P2 predates S4, so its cycle did not compile `UOContent.Tests` and did
not run a test gate. Different route, different number. But **0:44 is no longer the cost of a
build cycle on this repo**, and anything planning a batch off it will be optimistic by about
6x. Whoever runs the next batch should re-measure rather than take either figure on trust.

The practical consequence for a batch: **edit several files, then build once.** At 4.5 minutes
a cycle, a per-file build loop is the dominant cost; at three cycles for this whole port, it
was not.

---

## 8. The 203, classified — the number that actually decides the batch

Reproduced S3's counts independently before using them: **240 ModernUO `MLQuest` subclasses,
408 ServUO `BaseQuest`/`TierQuest` subclasses, 203 that ModernUO lacks by class name**
(matching both `X` and `XQuest` forms, since ModernUO drops the suffix). Three for three
against S3.

Then grouped the 203 by the objective types their class bodies construct:

| Objective types used | Quests | Maps? |
|---|---|---|
| `ObtainObjective` only | **73** | → Collect, 1:1 |
| `SlayObjective` only | **44** | → Kill, 1:1 |
| `EscortObjective` only | **29** | → Escort, 1:1 |
| **`InternalObjective`** (hand-written per quest) | **25** | **no counterpart** |
| `DeliverObjective` only | **17** | → Deliver, 1:1 |
| `CollectionsObtainObjective` | 3 | custom `ObtainObjective` subclass (CloakOfHumility) |
| `QuestionAndAnswerObjective` | 2 | **no counterpart** — out of scope by the brief |
| `ApprenticeObjective` only | 1 | → GainSkill, 1:1 |
| `SlayObjective` + `ObtainObjective` | 1 | **this quest** |
| One-off bespoke subclasses | 7 | `BloodCreatures`, `AcidCreatures`, `Discord`, `Peacemaking`, `Provocation`, `BountyQuest`, `FishQuest` |
| `InternalObjective` + `ObtainObjective` | 1 | `TheGreatVolcanoQuest` |
| **total** | **203** | |

**164 translate mechanically. 39 need a hand-written objective.** That is the number the
batch plan should be built on, and it is not the number anyone was looking at:
`QuestionAndAnswerObjective` is **2 of the 39**, and the brief was right to set it aside — but
setting it aside does not clear the tail. `InternalObjective` alone is **12.5× larger**.

Two caveats on this count, stated because the alternative is being the tenth wrong count in
this repo:

1. **It is derived by parsing class bodies for `new *Objective(`.** A commented-out
   constructor counts — `TheGreatVolcanoQuest` and this quest are both inflated by exactly
   that. A quest that builds objectives in a loop over a table counts once per distinct type,
   which is right, but a quest that adds objectives from a helper method outside its class
   body would be missed.
2. **A class body ends at the next `class` keyword**, so a quest declaring a nested
   `InternalObjective` before its constructor would have its outer objectives truncated. In
   ServUO the constructor comes first in every case checked, but this was not checked for all
   203.

**The full class list, grouped, is in the appendix below.** Publish the list beside the count.

An `InternalObjective` is not expensive individually — it is a `BaseObjective` subclass with a
hand-written `Update` and gump line, and ModernUO's `BaseObjective`/`BaseObjectiveInstance`
pair supports exactly that (`GargishDocumentObjective` in this port is one, at 8 lines). It is
expensive **collectively**, because each one is bespoke logic that has to be read and
understood rather than translated. Twenty-five of those is a different kind of work from
seventy-three renames.

---

## 9. Answer to Q-023, and what it changes

> **The mapping holds.** ModernUO's ML quest engine is behaviourally complete for four of the
> five objective types, with two named, cheap losses (region-scoped skill acceleration
> affecting 1 quest; a destination-name attribute step affecting 17). ServUO's framework
> decline stands, and stands more firmly than before: porting it would add a second engine to
> do a job the one we have does correctly.

Consequences:

- **CC3's quest decline is reversed**, as S3 predicted — but the reopened content is
  **164 quests**, not 203, without further work on the bespoke-objective tail.
- **Valley of One is reopened and is a poor first batch** (section 1). Myrmidex Threat is
  reopened on the same evidence and was not examined here.
- **`QuestionAndAnswerObjective` is a smaller question than it looked**, and
  `InternalObjective` is a much larger one. Whoever writes the next quest task should be
  costing the second, not the first.

---

## 10. What a `MODERNUO_COMMIT` bump must re-verify

Added to the checklist in `notes/s1-armour-sets.md` section 3 and `notes/s4-test-route.md`
section 2. `docker/uo/build.sh` covers all of it; these are the specific things it is
watching for.

1. **`MLQuestSystem.Register` still exists and still runs before `Initialize()`.** No upstream
   caller, so nothing but our test protects it. If `Main.cs` ever interleaves `Configure` and
   `Initialize`, the quest registers too late and `Generate()` never runs on it.
2. **`MLQuestSystem.HandleKill` is still called from `BaseCreature.OnDeath`**
   (`BaseCreature.cs:3376` at `7c9215d97`). Move that call and the build stays green while
   kill objectives silently stop counting.
3. **`CollectObjective.ShowDetailed` still exists.** Removing it would put an "Obtain 1 …"
   line and a garbage item image into the quest log for all ten documents.
4. **`NPCSpeeds.RegisterSpeed` and `NPCSpeeds.SpeedClassEntry` are still public.** The test
   fixture cannot construct a creature without them (5.1). If the route is fixed under Q-026,
   delete the workaround rather than leaving both.
5. **`ContinueReportBack` still consumes items and `ClaimRewards` still creates the reward.**
   If those merge, the test's two-step drive becomes a double hand-in.

---

## 11. Questions opened

- **Q-025** — `Quest.StartingItem`: ModernUO's engine has no item-started quest. How many of
  the 203 need it, and is it a framework addition we would accept? Unmeasured, non-blocking.
- **Q-026** — the S4 test route cannot construct a `BaseCreature`. Fix belongs in
  `apply-patches.sh` or the fixture, not in each test file. Non-blocking; worked around here.

---

## Appendix — the 203, by objective type

Generated from the same scan as section 8. Format: `ClassName<TAB>path relative to
D:\UO\ServUO-pub57\Scripts`.

### ObtainObjective — 73
ABrokenVaseQuest	Mobiles\NPCs\Axem.cs
ALittleSomething	Quests\ALittleSomething.cs
ATinkersTaskQuest	Quests\Eodon\MyrmidexThreat\Quests.cs
AWorthyPropositionQuest	Mobiles\NPCs\Aliabeth.cs
AllThatGlitters	Quests\TieredQuests\ThepemTieredQuests.cs
ArmorUp	Quests\TieredQuests\ZosilemTieredQuests.cs
BibliophileQuest	Mobiles\NPCs\QuartermasterFlint.cs
BlackOrderBadgesQuest	Mobiles\NPCs\Sarakki.cs
ClockworkPuzzleQuest	Mobiles\NPCs\Nibbet.cs
CrackingTheWhipQuest	Quests\SummonFiend.cs
CrystallineFragmentsQuest	Mobiles\NPCs\Neil.cs
Curiosities	Mobiles\NPCs\Gretchen.cs
DabblingontheDarkSide	Quests\TieredQuests\ZosilemTieredQuests.cs
DoneInTheNameOfTinkeringQuest	Mobiles\NPCs\Tobin.cs
EvidenceQuest	Mobiles\NPCs\Sarakki.cs
ExterminatingTheInfestationQuest	Quests\Eodon\MyrmidexThreat\Quests.cs
FeatherInYerCapQuest	Mobiles\NPCs\Cailla.cs
FirendOfTheFeyQuest	Quests\SummonFey.cs
GatheringOfEvidence	Quests\GatheringOfEvidence.cs
GatheringProof	Quests\GatheringOfEvidence.cs
GreenWithEnvyQuest	Quests\Vernix.cs
HeartOfIceQuest	Mobiles\NPCs\Neil.cs
HiddenTreasuresQuest	Quests\Eodon\MyrmidexThreat\Quests.cs
HonorOfDeBoorsQuest	Quests\HonorOfDeBoorsQuest.cs
HuteCoutureQuest	Mobiles\NPCs\Ahie.cs
ImpressivePlaidQuest	Mobiles\NPCs\Tallinin.cs
InTheBellyOfTheBeastQuest	Mobiles\NPCs\Frazer.cs
InTheWeeds	Mobiles\NPCs\FarmerNash.cs
KnowledgeoftheSoulforge	Quests\KnowledgeoftheSoulforge.cs
MakingContributionHeartwoodQuest	Quests\Spellweaving.cs
MakingContributionSanctuaryQuest	Quests\Discipline.cs
MasteringtheSoulforge	Quests\MasteringtheSoulforge.cs
MessageInBottleQuest	Mobiles\NPCs\Tholef.cs
MetalHead	Quests\TieredQuests\ThepemTieredQuests.cs
MisplacedQuest	Mobiles\NPCs\Cohenn.cs
Missing	Quests\Missing.cs
MysticsJourneyQuest	Quests\Ortlem.cs
NeedsOfManyHeartwoodQuest	Quests\Spellweaving.cs
NeedsOfManyPartHeartwoodQuest	Quests\Spellweaving.cs
NiceShirtQuest	Mobiles\NPCs\Tallinin.cs
PeptaQuest	Quests\PeptaQuest.cs
PerfectTimingQuest	Quests\Mad Scientist\Sutek.cs
PinkistheNewBlack	Quests\TieredQuests\ThepemTieredQuests.cs
PristineCrystalLotusQuest	Quests\The Ritual\Quests.cs
ProtectorsEssenceQuest	Mobiles\NPCs\Neil.cs
PureValorite	Quests\TieredQuests\ZosilemTieredQuests.cs
PuttingThePiecesTogetherQuest	Mobiles\NPCs\Axem.cs
RockAndHardPlaceQuest	Quests\BlightedGrove.cs
ScalesOfADreamSerpentQuest	Quests\The Ritual\Quests.cs
ScrapingtheBottom	Mobiles\NPCs\Xenrr.cs
SecretsoftheSoulforge	Quests\SecretsoftheSoulforge.cs
ShearingKnowledgeQuest	Mobiles\NPCs\Laifem.cs
SimpleBowQuest	Mobiles\NPCs\Cillitha.cs
SomethingFishy	Mobiles\NPCs\Barreraak.cs
StitchInTimeQuest	Mobiles\NPCs\Clairesse.cs
TaleOfTailQuest	Mobiles\NPCs\Cailla.cs
TastyTreats	Quests\TieredQuests\ThepemTieredQuests.cs
TearsOfASoulbinderQuest	Quests\The Ritual\Quests.cs
TheBrainyAlchemist	Quests\TieredQuests\ZosilemTieredQuests.cs
TheExchangeQuest	Mobiles\NPCs\Aliabeth.cs
TheForbiddenFruit	Quests\TieredQuests\ZosilemTieredQuests.cs
TheSecretIngredientQuest	Quests\FriendsOfTheLibrary.cs
TheZealotryOfZipactriotlQuest	Quests\Eodon\MyrmidexThreat\Quests.cs
ThievesBeAfootQuest	Mobiles\NPCs\QuartermasterFlint.cs
ToTurnBaseMetalIntoVerite	Quests\TieredQuests\ZosilemTieredQuests.cs
TokenOfLoveQuest	Quests\RatmenSanctuaryQuest.cs
UnfadingMemoriesOneQuest	Quests\UnfadingMemories.cs
UnitingTheTribesQuest	Quests\Eodon\Valley of One Quest\Quests.cs
UnusualGoods	Quests\UnusualGoods.cs
WatchYourStepQuest	Mobiles\NPCs\Lucius.cs
WhosMostHumbleQuest	Quests\CloakOfHumility\CloakOfHumilityQuest.cs
WondersOfTheNaturalWorldQuest	Mobiles\NPCs\Lefty.cs
YeOldeGargishQuest	Mobiles\NPCs\Axem.cs

### SlayObjective — 44
AForcedSacraficeQuest2	Services\Town Cryer\Quests\APleaFromMinocQuest.cs
AmbushingTheAmbushersQuest	Quests\TieredQuests\PercolemTieredQuests.cs
BadCompany	Quests\BadCompany.cs
BigJobQuest	Mobiles\NPCs\Cloorne.cs
BoundToTheLandQuest	Mobiles\NPCs\FrightenedDryad.cs
BouraBouraAndMoreBouraQuest	Quests\TieredQuests\PercolemTieredQuests.cs
BouraBouraQuest	Quests\TieredQuests\PercolemTieredQuests.cs
ChillInTheAirQuest	Mobiles\NPCs\Tiana.cs
ClearingCovetousQuest	Services\Town Cryer\Quests\APleaFromMinocQuest.cs
CowardsQuest	Quests\RatmenSanctuaryQuest.cs
DestructionOfZipactriotlQuest	Quests\Eodon\MyrmidexThreat\Quests.cs
DishBestServedColdQuest	Mobiles\NPCs\Tiana.cs
DoughtyWarriors2Quest	Quests\DoughtyWarriorsQuest.cs
DoughtyWarriors3Quest	Quests\DoughtyWarriorsQuest.cs
DoughtyWarriorsQuest	Quests\DoughtyWarriorsQuest.cs
EndingtheThreat	Quests\EndingtheThreat.cs
FilthyLifeStealersQuest	Quests\The Ritual\Quests.cs
FineFeastQuest	Mobiles\NPCs\Saril.cs
GentleBladeQuest	Mobiles\NPCs\Fabrizio.cs
GuiltyQuest	Mobiles\NPCs\Natalie.cs
HeroInTheMakingQuest	Mobiles\NPCs\Saril.cs
InsecticideAndRegicideQuest	Quests\Eodon\MyrmidexThreat\Quests.cs
IntoTheVoidQuest	Mobiles\NPCs\Agralem.cs
IronWillQuest	Quests\SummonFiend.cs
ItMakesMeSickQuest	Quests\TieredQuests\PercolemTieredQuests.cs
ItsAMadMadWorldQuest	Quests\TieredQuests\PercolemTieredQuests.cs
ItsGhastlyJobQuest	Mobiles\NPCs\Cailla.cs
OfVorpalsAndLettacesTheGardnerQuest	Quests\Eodon\MyrmidexThreat\Quests.cs
PaladinsOfTrinsic2	Services\Town Cryer\Quests\PaladinsOfTrinsic.cs
PestControlQuest	Quests\Eodon\MyrmidexThreat\Quests.cs
RaptorliciousQuest	Quests\TieredQuests\PercolemTieredQuests.cs
RevengeOfTheSlithQuest	Quests\TieredQuests\PercolemTieredQuests.cs
RightingWrongQuest2	Services\Town Cryer\Quests\RightingWrongQuest.cs
RightingWrongQuest3	Services\Town Cryer\Quests\RightingWrongQuest.cs
ShotAnArrowIntoTheAirQuest	Mobiles\NPCs\Kashiel.cs
SpringCleaningQuest	Quests\RatmenSanctuaryQuest.cs
TheArisenQuest	Mobiles\NPCs\Naxatillor.cs
TheDreamersQuest	Quests\TieredQuests\PercolemTieredQuests.cs
TheGreatApeQuest	Quests\Eodon\Valley of One Quest\Quests.cs
TheGreatHuntQuest	Quests\Eodon\Valley of One Quest\Quests.cs
TheSaltySeaQuest	Quests\Eodon\MyrmidexThreat\Quests.cs
TheSlithWarsQuest	Quests\TieredQuests\PercolemTieredQuests.cs
TrogAndHisDogQuest	Mobiles\NPCs\Cailla.cs
WeveGotAnAntProblemQuest	Quests\TieredQuests\PercolemTieredQuests.cs

### EscortObjective — 29
EscortToBritainQuest	Quests\Escortables.cs
EscortToCoveQuest	Quests\Escortables.cs
EscortToDugan	Quests\EscortToDugan.cs
EscortToJhelomQuest	Quests\Escortables.cs
EscortToMaginciaQuest	Quests\Escortables.cs
EscortToMinocQuest	Quests\Escortables.cs
EscortToMoonglowQuest	Quests\Escortables.cs
EscortToNujelmQuest	Quests\Escortables.cs
EscortToSerpentsHoldQuest	Quests\Escortables.cs
EscortToSkaraQuest	Quests\Escortables.cs
EscortToTrinsicQuest	Quests\Escortables.cs
EscortToVesperQuest	Quests\Escortables.cs
EscortToWrongEntrance	Services\Revamped Dungeons\WrongDungeon\Quests\EscortToWrongEntrance.cs
EscortToYewQuest	Quests\Escortables.cs
FreedomQuest	Mobiles\NPCs\Lenley.cs
KodarsRescueQuest	Mobiles\NPCs\Kodar.cs
NewHavenAlchemistEscortQuest	Mobiles\NPCs\Escortables.cs
NewHavenBankEscortQuest	Mobiles\NPCs\Escortables.cs
NewHavenBardEscortQuest	Mobiles\NPCs\Escortables.cs
NewHavenBowyerEscortQuest	Mobiles\NPCs\Escortables.cs
NewHavenCarpenterEscortQuest	Mobiles\NPCs\Escortables.cs
NewHavenDocksEscortQuest	Mobiles\NPCs\Escortables.cs
NewHavenFarmEscortQuest	Mobiles\NPCs\Escortables.cs
NewHavenInnEscortQuest	Mobiles\NPCs\Escortables.cs
NewHavenMageEscortQuest	Mobiles\NPCs\Escortables.cs
NewHavenMapmakerEscortQuest	Mobiles\NPCs\Escortables.cs
NewHavenTailorEscortQuest	Mobiles\NPCs\Escortables.cs
NewHavenWarriorEscortQuest	Mobiles\NPCs\Escortables.cs
ResponsibilityQuest	Quests\HumanHeritage.cs

### InternalObjective — 25
AForcedSacraficeQuest	Services\Town Cryer\Quests\APleaFromMinocQuest.cs
APleaFromMinocQuest	Services\Town Cryer\Quests\APleaFromMinocQuest.cs
AVisitToCastleBlackthornQuest	Services\Town Cryer\Quests\AVisitToCastleBlackthornQuest.cs
BuriedRichesQuest	Services\Town Cryer\Quests\BuriedRichesQuest.cs
CatchMeIfYouCanQuest	Quests\The Ritual\Quests.cs
EmptyNestQuest	Quests\Eodon\Valley of One Quest\Quests.cs
ExploringTheDeepQuest	Services\Town Cryer\Quests\ExploringTheDeepQuest.cs
GettingEvenQuest	Quests\Eodon\MyrmidexThreat\Quests.cs
GoingGumshoeQuest	Services\Seasonal Events\TreasuresOfKhaldun\Quest\GoingGumshoeQuest.cs
GoingGumshoeQuest2	Services\Seasonal Events\TreasuresOfKhaldun\Quest\GoingGumshoeQuest.cs
GoingGumshoeQuest3	Services\Seasonal Events\TreasuresOfKhaldun\Quest\GoingGumshoeQuest.cs
GoingGumshoeQuest4	Services\Seasonal Events\TreasuresOfKhaldun\Quest\GoingGumshoeQuest.cs
HuntmastersChallengeQuest	Services\Town Cryer\Quests\HuntmastersChallengeQuest.cs
LeadingIntoBattleQuest	Quests\DiscoveringAnimalTraining\DiscoveringAnimalTraining.cs
PaladinsOfTrinsic	Services\Town Cryer\Quests\PaladinsOfTrinsic.cs
PrideOfTheAmbushQuest	Quests\Eodon\Valley of One Quest\Quests.cs
RightingWrongQuest	Services\Town Cryer\Quests\RightingWrongQuest.cs
RightingWrongQuest4	Services\Town Cryer\Quests\RightingWrongQuest.cs
TamingPetQuest	Quests\DiscoveringAnimalTraining\DiscoveringAnimalTraining.cs
TeachingSomethingNewQuest	Quests\DiscoveringAnimalTraining\DiscoveringAnimalTraining.cs
TheTreasureChaseQuest	Services\Town Cryer\Quests\BuriedRichesQuest.cs
ToolsOfTheTradeQuest	Services\Town Cryer\Quests\BuriedRichesQuest.cs
UsingAnimalLoreQuest	Quests\DiscoveringAnimalTraining\DiscoveringAnimalTraining.cs
WhisperingWithWispsQuest	Services\Town Cryer\Quests\WishesOfTheWispsQuest.cs
WishesOfTheWispQuest	Services\Town Cryer\Quests\WishesOfTheWispsQuest.cs

### DeliverObjective — 17
AccessToTheStacksQuest	Quests\FriendsOfTheLibrary.cs
AemaethOneQuest	Quests\AemaethQuests.cs
AemaethTwoQuest	Quests\AemaethQuests.cs
BureaucraticDelayQuest	Quests\FriendsOfTheLibrary.cs
FathersGratitudeQuest	Quests\GhostOfCovetous.cs
FriendsOfTheLibraryQuest	Quests\FriendsOfTheLibrary.cs
GhostOfCovetousQuest	Quests\GhostOfCovetous.cs
JackTheVillainQuest	Quests\HonorOfDeBoorsQuest.cs
LastWordsQuest	Mobiles\NPCs\DenthesJournal.cs
NewSpinQuest	Mobiles\NPCs\Laifem.cs
RumorsAboundQuest	Mobiles\NPCs\Egwexem.cs
SavedHonorQuest	Quests\HonorOfDeBoorsQuest.cs
SpecialDeliveryQuest	Quests\FriendsOfTheLibrary.cs
TimeIsOfTheEssenceQuest	Quests\Eodon\Valley of One Quest\Quests.cs
UnfadingMemoriesThreeQuest	Quests\UnfadingMemories.cs
UnfadingMemoriesTwoQuest	Quests\UnfadingMemories.cs
WeavingFriendshipsQuest	Mobiles\NPCs\Laifem.cs

### CollectionsObtainObjective — 3
CommunityServiceLibraryQuest	Quests\CloakOfHumility\CloakOfHumilityQuest.cs
CommunityServiceMuseumQuest	Quests\CloakOfHumility\CloakOfHumilityQuest.cs
CommunityServiceZooQuest	Quests\CloakOfHumility\CloakOfHumilityQuest.cs

### QuestionAndAnswerObjective — 2
QuestOfSingularity	Quests\Sacred Quest\QuestOfSingularity.cs
TheQuestionsQuest	Quests\CloakOfHumility\CloakOfHumilityQuest.cs

### AcidCreaturesObjective — 1
UntanglingTheWebQuest	Quests\Vernix.cs

### ApprenticeObjective — 1
EyesOfRangerQuest	Mobiles\NPCs\Walker.cs

### BloodCreaturesObjective — 1
ATangledWeb	Quests\ATangledWeb.cs

### BountyQuestObjective — 1
ProfessionalBountyQuest	Services\Expansions\High Seas\Quests\ProfessionalBountyQuest\ProfessionalBountyQuest.cs

### DiscordObjective — 1
WieldingTheSonicBladeQuest	Quests\Bard Mastery Quests\SirBerran.cs

### FishQuestObjective — 1
ProfessionalFisherQuest	Services\Expansions\High Seas\Quests\ProfessionFishQuest\ProfessionalFisherQuest.cs

### InternalObjective + ObtainObjective — 1
TheGreatVolcanoQuest	Quests\Eodon\Valley of One Quest\Quests.cs

### InternalObjective + ObtainObjective + SlayObjective — 1
JourneyToTheAthenaeumIsleQuest	Quests\JourneyToTheAthenaeumIsleQuest.cs

### PeacemakingObjective — 1
TheBeaconOfHarmonyQuest	Quests\Bard Mastery Quests\SirFelean.cs

### ProvocationObjective — 1
IndoctrinationOfABattleRouserQuest	Quests\Bard Mastery Quests\SirHareus.cs
