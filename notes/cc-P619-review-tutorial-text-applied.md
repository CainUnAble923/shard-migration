# P619: review of the applied tutorial text

Reviewed October 25, 2026. Notes only. Code HEAD: `57924e6c965237f430f5229dd5c454d62b9c0d5c`. Notes HEAD before this file: `8e4358c9062e23d03e5f31bf17a50cb21197a18e`. P609's implementation is `bc465d4fbaa5f3680667353dfda3a13f033c641c`, merged by `2a3cf3b`.

Read both work copies' AGENTS.md, the direction decision, task list, both P609 notes, and the P588 proposals. Compared P609's changed text with the current canonical source and the lesson checks. Current source includes the subsequent P610 and P613 fixes; citations below refer to this work copy, not P609's earlier line numbers.

## Findings

### 1. Medium (P2): the move instructions omit the double-click needed to ready a move

**Location:** `server/customizations/Tutorial/TutorialWingTrials.cs:171` and `:173`.

**What happens:** Bushido says to open its book and "click Honorable Execution"; Ninjitsu says to "click Focus Attack." In the local TazUO source, a single click on a spellbook index label selects its page. Casting or readying the move requires a double-click on the label or icon. A new player following these instructions literally can swing the katana without readying the move, so the lesson stays unfinished. The checks at `TutorialWingTrials.cs:656` and `:657` require a current move from that school. This wording was already present before P609 and remains in the applied text; it was not a finding in the earlier reviews checked below.

**Evidence:** `D:/UO/tazuo-sl-build/src/src/ClassicUO.Client/Game/UI/Gumps/SpellbookGump.cs:1342` handles a single label click by setting `_enqueuePage`; `:1354` casts on a label double-click, and `:793` casts on an icon double-click. The controls register these separate handlers at `:498`, `:499`, and `:734`.

**Fix:** Say "double-click Honorable Execution" and "double-click Focus Attack." For example: "Equip the loaned katana, open the Book of Bushido, and double-click Honorable Execution. With war mode on, double-click the blue training echo."

### 2. Medium (P2): Tab is described as entering war mode regardless of the current mode

**Location:** `server/customizations/Tutorial/TutorialWingTrials.cs:161`, `:171`, `:173`, and the completion instructions at `:705`.

**What happens:** The weapon and move hints tell the player to press Tab for war mode. With TazUO's toggle behavior, doing that while already in war mode turns it off. Restarting a weapon lesson or moving between combat lessons does not reset the player's war mode, so repeating the instructed sequence can leave double-clicks opening the echo's character window instead of attacking. There is also no instruction to return to peace before following the completion message's "Double-click Rook": a player still in war mode sends an attack request instead of opening Rook's lesson menu. The tutorial's `Finish` and `Return` paths at `:485` and `:497` do not change war mode.

**Evidence:** In the same local client tree, `Game/Scenes/GameSceneInputHandler.cs:1737` handles Tab; with `HoldDownKeyTab` off, `:1752` calls `ToggleWarMode`. `Game/GameActions.cs:32` toggles to the opposite mode, and `:681` turns a mobile double-click into an attack when war mode is on. The spellbook interaction and the war-mode instruction are separate problems: fixing the click count in finding 1 does not fix this sequence.

**Fix:** Make the instructions conditional: "Turn war mode on if it is off; Tab switches between war and peace." Add "Return to peace mode before double-clicking Rook" to the combat completion guidance. These instructions should also acknowledge a customized or hold-to-use Tab setting if the tutorial intends to cover those profiles.

### 3. Low (P3): the stealing checklist no longer tells the player where the purse is

**Location:** `server/customizations/Tutorial/TutorialTradeTrials.cs:156` and `:164`.

**What happens:** P609 replaces "lift the purse from the chest" with "empty your hands and steal the purse." Its new general hint discusses both the wooden chest and the blue practice person, but never says to open the unlocked chest or that the purse is inside it. The person has a separate backpack item, a brass trinket. A new player can reasonably look for the purse on that person or on the ground after finishing the lockpicking task.

**Evidence:** `TutorialTradeTrials.cs:470` puts the brass trinket in the person's pack; `:479` creates the purse, and `:481` puts it in the chest. Pinned ModernUO's `Projects/UOContent/Skills/Stealing.cs:63` opens a targeting cursor, so the player needs to expose and target the actual item, rather than just open the chest.

**Fix:** Restore the location and explain the next action: "Stealing: open the unlocked wooden chest, empty both hands, then use Stealing on the purse inside." Keep the nearby Skills instruction for opening the skill list.

### 4. Low (P3): the documented reseed does not apply the saved rat's new name

**Location:** `shard-migration/notes/cc-P609-apply-tutorial-text.md:13`; related player text at `server/customizations/Tutorial/TutorialCoreTrials.cs:54` and constructor at `TutorialCorePlacement.cs:219`.

**What happens:** P609 tells Chase to run `[ClusterFSeedTutorial` after deployment so the already placed rat receives the new name. That command only places missing creatures. An existing `TutorialDeathEcho` is filtered out before construction, and no rename is performed. After the recommended command, the lesson can still direct a player to "the pale gray rat" while its displayed name remains "the pale death echo." Changed station-marker titles have the same persistence issue.

**Evidence:** `TutorialRecruiter.cs:129` delegates seeding to `TutorialCorePlacement.Seed`. `TutorialCorePlacement.cs:75` supplies the death-echo constructor, `:80` filters out creatures found at their existing spots, and `:107` only constructs the remaining entries. Existing station markers are likewise excluded at `:71`, while their `Name` is assigned only in the constructor at `:137`; `Brighten` at `:140` changes only the hue. There is no saved-rat rename hook in this class.

**Fix:** Correct the handoff note to say that reseeding alone will not update saved names. Describe a staff-controlled rename or deliberate replacement on the test world, or request a narrow saved-name upgrade for the rat and affected markers. Check the displayed names on that world afterward. No world objects were changed for this review.

## Scope, previous reviews, and checks

The P609 source inventory reviewed under `server/customizations/Tutorial/` is:

- `ClusterFLoops.cs`
- `ClusterFTutorial.cs`
- `TutorialCorePlacement.cs`
- `TutorialCoreTrials.cs`
- `TutorialCreature.cs`
- `TutorialFarm.cs`
- `TutorialGumps.cs`
- `TutorialIslandGate.cs`
- `TutorialPetCare.cs`
- `TutorialRecruiter.cs`
- `TutorialStations.cs`
- `TutorialTradeTrials.cs`
- `TutorialWingTrials.cs`

Also checked P609's changed assertions in `server/tests/Misc/TutorialVerification.cs`, `server/tests/Tutorial/TutorialFirstPlayVerification.cs`, and `server/tests/Tutorial/GraduationLoopVerification.cs`; its comment change in `tools/playtest-bot/uobot/checks_p224_rootdeep.py`; its `CHANGELOG.md` and `VERSION` changes; and the explicitly excluded draft `docker/wiki/content/pages/uo/drafts/tutorial.txt`. The draft's stale names and previews were already disclosed by P609 and are not new findings here. Read `TutorialTrialProgress.cs` and the relevant supply, placement, pet-stage, and pinned skill implementations to check the lesson instructions.

Checked the prior tutorial reviews from P289, P291, P420, P421, P475, P480, P502, P503, P523, P573, P588, and P609. P609's pet-description clipping finding is not repeated. The earlier ownership, pending-pet, bandage allowance, loan cleanup, false action evidence, and goat interference findings are also excluded. Findings 1 and 2 concern instructions retained by P609, rather than newly introduced behavior. Finding 3 concerns information removed by P609; finding 4 concerns its application advice.

No broken interpolation was found. A read-only comparison of the interpolated expressions on P609's removed and added tutorial lines found no removed expressions and only the added `{fee}` from the documented localized-message replacement. The retained weapon-skill expression, farm `{0}` quantities and their `string.Format` calls, station titles, progress counts, and vet-fee substitutions were also checked in source. This comparison does not verify client rendering.

Pinned engine evidence is from `D:/UO/ModernUO-pinned` at `d4531cd94b739613155225c234900de9f47d2c88`. Client evidence is from the local `D:/UO/tazuo-sl-build/src` checkout at `3212623f6`, which has existing local changes. The cited spellbook, input-handler, and GameActions files have no local changes. The installed or published client binary was not identified or run, so its exact correspondence to this source remains unverified.

No code, tests, or files under `docs/` changed. Lane tests are none. No build, gameplay test, client session, save/load, Docker operation, account operation, or Haven connection was performed. The findings follow source paths; actual text wrapping, the current world's saved names, customized key bindings, and the described interaction sequences remain unverified in a running client.

The required `tools/progress.py --dry-run` completed with exit 0 using both work-copy path overrides. Its incidental `tools/progress.json` write was restored to the exact original bytes. Its historical status prose and counts are not used as evidence for tutorial behavior.

P619 DONE
