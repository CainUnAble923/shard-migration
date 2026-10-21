# cc-P231: hidden joke achievements for OSI's easter-egg moments

Copper Golem, 2026-10-21. Server only. Branch `golem/Copper/P231` in both repos. Image `sl-modernuo:cc-P231`.

## Headlines

- **16 hidden achievements**, in a new **Mischief** category:
  - Run With Scissors set (Safety Third, x25, x100; Chase's wording kept exactly);
  - Chase's other 12: Not Trustworthy, Meditating in Plate, Mister Creosote, Placebo, Planned Obsolescence, Soul
    Searching, Boo, \*hic\*, Instant Justice, Self-Detonation, Sole Survivor (with a second tier, Sole Proprietor) and
    Fowl Play.

  Each one has a snarky flavor line plus the plain "(Earned: ...)" line written from its trigger (D73).
- **Every one fires from the game event, never from message text.**
  - **Nine one-line patches** sit at the exact branch where pinned refuses or reports the moment, because pinned raises
    no event there.
  - **Our own `Meditation.cs`** (a replacement) carries the armor hook.
  - **Pinned's own events** carry the other five, with no patch: the speech event with the client's keyword 0x0032, the
    speech event from a ghost, and `PlayerDeathEvent` for guards, fowl and self-detonation.
- **Rewards are small and one-time**: 130 AP and 19 Renown across all 16. Each achievement is earned once per account,
  so repeating an event (scissors, worn tools, fished boots) earns nothing past its tiers.
- **11 new facts** in `server/tests/Misc/JokeAchievementsVerification.cs`, each seen failing first at its own assertion.
  The full suite is green through `docker/uo/build.sh`: 1,894 tests, 1,890 passed, 0 failed, 4 skipped, and the image
  was built.
- **Part 3:** 11 more OSI moments are listed below with their wording and hook site, for Chase. None are built.

## What changed

ShatteredLegacy repo:

| File | What |
|---|---|
| `server/customizations/ClusterFJokeAchievements.cs` (new) | The 16 definitions (`RegisterJokes` `:59`, a `partial` of `ClusterFAchievementSystem`); `NotifyJoke` `:210` (counts per account in the saved achievement counters, then grants every tier reached); the hook class `ClusterFJokeAchievements`: hooks `:236-249`, the sins keyword `:221`, `BeforeBlast` `:256` (self-detonation mark), `OnSpeech` `:268`, `OnPlayerDeath` `:281`. |
| `server/customizations/ClusterFAchievements.cs` | 13 new `TriggerKind`s `:69-81` and their "(Earned: ...)" wording `:159-174`; `AchievementCategory.Mischief = 9` `:195`; the class made `partial` `:303`; `RegisterJokes()` called at the end of `RegisterAll` `:1128`. |
| `server/customizations/Meditation.cs` | `:80`, the hook beside "Regenerative forces cannot penetrate your armor!" (our replacement file, no patch). |
| `server/patches/*-achievement.patch` (9 new) | One added line each (CraftItem: four, one per worn-out-tool site). Table below. |
| `docker/uo/apply-patches.sh` | The nine `apply_patch` lines, last in the list, with their reason. |
| `server/tests/Misc/JokeAchievementsVerification.cs` (new) | 11 facts. |
| `server/tests/Misc/AchievementEarnedLineVerification.cs` | The registered and live counts, 79 to 95 (`:100`, `:323`), as earlier prompts did for their own additions. |
| `CHANGELOG.md`, `VERSION` | New section 2026.10.21.4 (Added, Staff). VERSION bumped from 2026.10.21.3, whose section was already committed (P230). |

No save format changed. The joke counters live in the existing per-account achievement counters
(`ClusterFAchievementSystem._counters`, saved by `ClusterFAchievementPersistence`), under keys `joke_<kind>`.

## Part 5: every hook, its pinned file and line, and whether it needed a patch

Line numbers are in the tree every earlier patch leaves (`sl-uo-builder:cc-P230`, `/build/modernuo/Projects/UOContent`).
That is also the tree the patches were made against. Where no other patch touches the file, the line is the same in
pristine pinned d4531cd9.

| Achievement | Event, where | Patch? |
|---|---|---|
| Safety Third, Run With Scissors, Unsupervised | `Items/Skill Items/Tailor Items/Misc/Scissors.cs:60-64`, the running refusal (80% chance, running, moved within one step's time; 1063305 "Didn't your parents ever tell you not to run with scissors in your hand?!") | `Scissors-running-achievement.patch` |
| Not Trustworthy | `Skills/Begging.cs:106-110`, the bad-karma branch of the begging timer (500406 "Thou dost not look trustworthy... no gold for thee today!") | `Begging-untrustworthy-achievement.patch` |
| Meditating in Plate | our `server/customizations/Meditation.cs:77-80` (a full replacement of pinned's), armor blocks it (500135) | none |
| Mister Creosote | `Items/Food/Food.cs:86-89`, `FillHunger` at Hunger 20 (500867) | `Food-too-full-achievement.patch` |
| Placebo | `Items/Skill Items/Misc/Bandage.cs:482-487`, `BeginHeal` on a patient at full health, not poisoned or bleeding (500955) | `Bandage-unhurt-patient-achievement.patch` |
| Planned Obsolescence | `Engines/Craft/Core/CraftItem.cs:1503-1505`, `:1723-1725`, `:1839-1841`, `:1930-1932` (each `if (toolBroken) tool.Delete()`, both `CompleteCraft` overloads, success and failure); `Engines/Harvest/Core/HarvestSystem.cs:235-237` (a harvest tool at 0 uses) | `CraftItem-` and `HarvestSystem-tool-worn-achievement.patch` |
| Soul Searching | pinned speech keyword 0x0032, the one `Misc/Keywords.cs:31` handles, read from `EventSink.Speech` (raised by `Mobile.DoSpeech`, `Server/Mobiles/Mobile.cs:5604`) | none |
| Boo | the same speech event from a dead player, spoken aloud (regular, whisper or yell) | none |
| \*hic\* | `Items/Food/Beverage.cs:868-871`, the drunk heave timer's hiccup (500849) | `Beverage-hiccup-achievement.patch` |
| Instant Justice | `PlayerDeathEvent` (`Mobiles/PlayerMobile.cs:2609`), last damager a `BaseGuard`; the instant kill damages with the guard as source first (`Mobiles/Guards/BaseGuard.cs:320-321`) | none |
| Fowl Play | `PlayerDeathEvent`, last damager a `Chicken`, `Rabbit` or `JackRabbit` | none |
| Self-Detonation | `Items/Skill Items/Magical/Potions/Explosion Potions/BaseExplosionPotion.cs:202`: before the potion damages its own thrower (pinned lets it, `SpellHelper.ValidIndirectTarget` returns true for self, `Spells/Base/SpellHelper.cs:415-418`), the thrower is marked; `PlayerDeathEvent` then finds them as their own last damager within a second | `BaseExplosionPotion-self-blast-achievement.patch` |
| Sole Survivor, Sole Proprietor | `Engines/Harvest/Fishing.cs:425-429`, `SendSuccessTo`'s `BaseShoes` branch (boots, shoes, sandals, thigh boots: Fishing's footwear table `:29`) | `Fishing-shoes-achievement.patch` |

**The patches, argued (AGENTS.md: a patch to an upstream file gets its alternatives argued first).** For each of the
nine sites I looked for, and rejected, these routes:
- **An event to subscribe to:** none is raised at any of them. Pinned's generated events cover login, death, creature
  death, character creation and similar; nothing covers a refusal, a worn tool or a hiccup.
- **Matching the message text:** the prompt forbids it, and the client could be speaking any language.
- **A subclass:** `Scissors`, `Food`, `Bandage`, `BaseExplosionPotion` and the craft and harvest systems are used by type
  everywhere, so a subclass would only cover items we spawn.
- **A full-file replacement:** that hides upstream drift; AGENTS.md calls `CraftItem`'s old replacement the cautionary
  case.

So each patch adds one line, a call into `ClusterFJokeAchievements`, beside the message it would otherwise have to
match. The patches go last in `apply-patches.sh` because they were made against the tree the other patches leave.
`CraftItem` already carries four patches and `Imbue-custom-property-hooks.patch` touches it after the others; no hunk
shares lines, and the build applies all nine with `--fuzz=0`. Three patches needed quoted `---`/`+++` paths (their paths
contain spaces), as `Bandage-searing-wounds.patch` has.

## Part 4: shape and rewards

All 16 are `hidden: true` in `AchievementCategory.Mischief`, and none has a progress bar. The category has no tab of its
own (League has none either), so an earned one shows under **All**, marked `[Secret]`, with its flavor and Earned lines.
An unearned one is invisible (`AchievementsGump`, hidden filter `ClusterFAchievements.cs:~2030`).

| Achievement | Earned: | Flavor | AP | Renown | Farming |
|---|---|---|---|---|---|
| Safety Third | tried to use scissors while running | Your parents tried. The scissors tried. Nobody can help you. | 5 | 1 | one-time |
| Run With Scissors | ... 25 times | At this point it's a lifestyle. | 10 | 2 | one-time (needs Safety Third) |
| Unsupervised | ... 100 times | We've stopped telling you. | 15 | 0 | one-time; no Renown, because they've stopped telling you |
| Not Trustworthy | begged and were told you do not look trustworthy | Even the beggars' marks have standards. You are below them. | 5 | 0 | one-time |
| Meditating in Plate | tried to meditate in armor | Inner peace, outer plate. The plate won. | 5 | 1 | one-time |
| Mister Creosote | tried to eat while already full | It's only wafer-thin. The System has moved out of range anyway. | 5 | 1 | one-time |
| Placebo | tried to bandage someone who was not hurt | They feel much better now. They felt fine before. Medicine. | 5 | 0 | one-time |
| Planned Obsolescence | wore out 100 tools | A hundred tools have given their lives so you could keep doing this. The tinkers thank you. | 15 | 5 | one-time |
| Soul Searching | said "I must consider my sins" | You considered them. The System has them in alphabetical order, if that helps. | 5 | 1 | one-time |
| Boo | spoke while a ghost | OOooOOoo. Very spooky. Nobody understood a word. | 5 | 0 | one-time |
| \*hic\* | drank until you hiccuped | The System is not angry. The System is disappointed. \*hic\* | 5 | 1 | one-time |
| Instant Justice | died to the town guards | Due process took about a quarter of a second. Efficient, really. | 10 | 0 | one-time |
| Self-Detonation | died to your own explosion potion | Throw it AWAY from you. The System thought that went without saying. | 10 | 0 | one-time |
| Sole Survivor | fished up 10 boots or shoes | Somewhere out there is a lot of barefoot sailors. | 5 | 2 | one-time |
| Sole Proprietor | fished up 100 boots or shoes | You could open a shop. Nothing would match. | 15 | 5 | one-time (needs Sole Survivor) |
| Fowl Play | died to a chicken or a rabbit | It went for the throat. The System will be telling this one for years. | 10 | 0 | one-time |
| **Total** | | | **130** | **19** | |

Renown is 0 wherever the event is a death or is cheap to repeat. It is at most 5, and only where the work is real (100
worn tools, 100 boots). Repeating any event after its last tier earns nothing; the counter keeps counting, harmlessly.

## Part 3: more OSI moments for Chase (not built)

The wording is pinned's own comment beside each message. The installed client's `Cliloc.enu` could not be read by the
cliloc tool (it found no entry for 500398, which pinned uses), so the client wording is **unverified**. Each hook would
be one line at the site given, in the same shape as the patches above.

| Proposed | Moment and exact wording | Hook site |
|---|---|---|
| Self-Trim | scissors used on yourself: "That doesn't seem like the smartest thing to do." / "That was an encounter you don't wish to repeat." / "Ha! You missed!" (1062845-1062847) | `Scissors.cs:55-58`, the branch above the running one (same patch) |
| Have You Tried Asking? | begging from a player: "Perhaps just asking would work better." (500398) | `Begging.cs:44-46` (same patch) |
| That Being Cannot Be Tamed | Animal Taming on a player or a non-creature: "That being cannot be tamed." (502469) | `Skills/AnimalTaming.cs:121-125` |
| Lockpick Graveyard | 100 lockpicks broken: "You broke the lockpick." (502074) | `Items/Skill Items/Thief/LockPick.cs:94-96` |
| Nothing to See Here | Detect Hidden finds nothing, x50: "You can see nothing hidden there." (500817) | `Skills/DetectHidden.cs:261` |
| Too Tired to Punch | attacking at no stamina: "You are too fatigued to attempt anything." (1004009) | `Items/Weapons/Fists.cs:79` |
| Party of One | inviting yourself to a party: "You cannot add yourself to a party." (1005439) | `Context Menus/AddToParty.cs:23` |
| Thou Art Too Encumbered | trying to move overweight (500109, wording unverified) | `Misc/StaminaSystem.cs:338` |
| Dismounted by Rope | knocked off your mount by a bola: "You have been knocked off of your mount!" (1040023) | `Items/Misc/Bola.cs:84` |
| The Fish Aren't Biting | fishing where nothing bites, x50: "The fish don't seem to be biting here." (503172) | `Engines/Harvest/Fishing.cs:90` (the harvest system's no-resources path) |
| Snapped It | broke a fishing pole: "You broke your fishing pole." (503174) | `Fishing.cs:95` (`ToolBrokeMessage`; already counted toward Planned Obsolescence by the HarvestSystem hook) |

## Tests

`server/tests/Misc/JokeAchievementsVerification.cs`, 11 facts. Each drives the game's own path:

1. `TheScissorsRefusalCountsAndItsThreeTiersFire`: Scissors' own target, 50 times standing (nothing), then running until
   100 refusals. After every attempt each tier is held exactly when the count has reached 1, 25 and 100.
2. `BeggingWithBadKarmaIsRefusedAsUntrustworthy`: `Begging.OnUse`, target a banker, the 2 s timer on `ShardTestClock`.
   Karma -15,000 is always refused (pinned's chance above 1); +15,000 never.
3. `MeditatingInArmorIsBlocked`: our `Meditation.OnUse` with a plate chest on; unarmored never.
4. `EatingWhileFullAndBandagingTheUnhurt`: `Ham.Eat` at Hunger 20 versus 5; `BandageContext.BeginHeal` on a full-health
   versus a hurt patient.
5. `AHundredToolsWornOutByRealCrafts`: 100 real `CraftItem.CompleteCraft` body sashes, each with a one-use sewing kit.
   The count matches every time and the tier lands at 100. A kit with uses left is not counted.
6. `SoulSearchingFromTheKeywordAndBooFromAGhost`: `DoSpeech`. The words with no keyword do nothing; the keyword does.
   Speaking alive is nothing; speaking dead is Boo.
7. `DrinkingUntilYouHiccup`: the heave timer at BAC 40 until the hiccup; a sober player never.
8. `DeathsByGuardsFowlAndYourOwnPotion`:
   - A `WarriorGuard`'s attack timer, with instant kill on (as the shard's config has it), gives Instant Justice.
   - A chicken and a rabbit give Fowl Play; an orc does not.
   - Your own `ExplosionPotion.Explode` gives Self-Detonation. Another player's potion does not, nor does damaging
     yourself to death some other way.
9. `FishingUpFootwearCountsToTenAndAHundred`: `Fishing.SendSuccessTo` with boots, shoes, sandals and thigh boots; a fish
   does not count.
10. `NoneFiresFromItsMessageTextAlone`: every message beside a hook is sent to the player (localized and overhead), the
    English lines are sent as text, and the player *says* them. Nothing is earned and every joke counter stays 0.
11. `TheyAreHiddenUntilEarned`: every joke definition is hidden, Mischief, and has its flavor and Earned lines (Safety
    Third's checked word for word). None is in any page of the list until earned; Safety Third, earned through the real
    scissors path, is then listed with `[Secret]` and both lines, and its next tier stays hidden.

Not driven in a fact: the harvest-tool and second `CompleteCraft` overload sites (the same one-line hook; the build
proves they apply and compile). Fishing is driven at `SendSuccessTo`, the method holding the hook, not through a whole
harvest.

**Seen failing first.** I saved `ClusterFJokeAchievements.cs`, applied ten marked breaks (`P231-BREAK`), ran
`docker/uo/build.sh -t sl-modernuo:cc-P231 --tests-only`, then copied the saved file back (`cmp` identical, no marker
left). The breaks:
- Unsupervised at 99;
- the begging, meditation, eating, tool, hiccup and fishing hooks emptied;
- `OnSpeech` matching text ("consider my sins", "\*hic\*") instead of the keyword;
- the guard branch off;
- Fowl Play not hidden.

Result: 1,894 tests, **11 failed, exactly the 11 new facts**, each at its own assertion:

| Fact | Line | Failure |
|---|---|---|
| 1 | `:180` | Unsupervised held at 99 |
| 2 | `:219` | |
| 3 | `:243` | |
| 4 | `:264` | |
| 5 | `:301` | "Expected 1, Actual 0" |
| 6 | `:322` | the words without the keyword earned it |
| 7 | `:357` | |
| 8 | `:383` | |
| 9 | `:438` | |
| 10 | `:471` | spoken text earned it |
| 11 | `:482` | not hidden |

**Real code, before that:**
- **Run 1:** `apply-patches.sh` refused the nine patches as unlisted; the list is explicit, not a glob.
- **Run 2:** three patches failed, because their spaced paths needed quoting.
- **Run 3:** `RegenRates` needed `using Server.Misc` in the test.
- **Run 4:** 3 failed:
  - a fresh test character has `ManaMax` 0, so Meditation said "at peace" before the armor check;
  - the "unhurt" patient started below full;
  - `AchievementEarnedLineVerification`'s live count, 73, needed the 16.
- **Run 5:** green.

**Full suite, real code** (`docker/uo/build.sh -t sl-modernuo:cc-P231`, docker-build lock taken and released): "Total
tests: 1894, Passed: 1890, Skipped: 4", "Built sl-modernuo:cc-P231 with patches applied and 1890 shard test(s)
passing." `CHANGELOG.md` and `VERSION` were edited after this run. No test reads them.

## Deviations and decisions for Chase

1. **Nine patches.** Pinned has no event at those moments (argued above). Each patch is one line, applied last.
2. **A Mischief category with no tab.** The jokes show under All once earned (as League's achievements do). A tab would
   mean re-laying the tab rows (five, then four with Quests); say if you want one.
3. **Sole Survivor's second tier is named Sole Proprietor.** The prompt gives tiers 10 and 100 but one name.
4. **Fowl Play counts Chicken, Rabbit and JackRabbit**, and not the Vorpal Bunny (a real monster, so no joke to die to
   one). One word to add it.
5. **Placebo is bandages only.** Close Wounds (Chivalry) has the same "not damaged" message (`Spells/Chivalry/
   CloseWounds.cs:50`) and is not hooked. A bandage on yourself at full health counts too.
6. **Planned Obsolescence counts crafting and harvesting tools.** That includes fishing poles, pickaxes and shovels, but
   not the Ancient Smithy Hammer's separate wear, which `CraftItem` deletes on its own lines. Enhance's hammer wear
   (`Engines/Craft/Core/Enhance.cs:108`) is not hooked either.
7. **Boo counts any speech aloud as a ghost** (regular, whisper or yell), not guild or alliance chat.
8. **Self-Detonation needs both** your own blast and you as your own last damager. A friend's potion that finishes you
   after your own blast does not count.
9. **Each earn also gives the usual achievement loot box** (`ClusterFLootBoxes.OnAchievementEarned`). At 5 to 15 AP that
   is the lowest tier, and the theme falls back to Explorer for an unmapped category (`ClusterFLootTable.cs:163-166`).
   Say if jokes should give no box.
10. **AP total.** The 130 AP raises the live total a player can reach (P229 counted 1,955; now 2,085). The League Shop's
    1,750 AP tier stays reachable without any joke.
11. **Neither `D:\UO\ModernUO-pinned` nor `D:\UO\ServUO-pub57` is on this PC** (as in cc-P230). Pinned was read from the
    builder image.

## For Chase (in the client, test shard)

1. Scissors in your pack, run, and double-click them on something while still running: the refusal, then "Safety Third"
   with its popup. `[achievements`, All: it is listed with [Secret]. The other 15 are invisible.
2. Eat until "too full", then once more (Mister Creosote). Bandage a healthy friend (Placebo). Meditate in plate
   (Meditating in Plate). Say "I must consider my sins" (Soul Searching). Die and say anything (Boo).
3. Drink ale until you hiccup (\*hic\*). In town, attack a guard's attention (Instant Justice). With 1 hit point, throw an
   explosion potion at your own feet (Self-Detonation).
4. Staff check: `[ClusterFAchievement list` shows the 16 under Mischief.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, 2026-10-21 (re-run after
this note was written):

```
Repo Result
---- ------
code dry run
docs dry run
```

Neither repo is BLOCKED. Code: 17 files (the 9 patches, `ClusterFJokeAchievements.cs`, `ClusterFAchievements.cs`,
`Meditation.cs`, `apply-patches.sh`, 2 test files, `CHANGELOG.md`, `VERSION`). Docs: this note. No file is over 5 MB.

P231 DONE
