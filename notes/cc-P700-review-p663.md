# P700: code review of P663

Reviewed October 27, 2026. Three new medium-severity findings remain in the current source. No code changed.

## Scope and source versions

Code HEAD: `6c5846a07a115879251f1678d8e05b3991965b92`. Notes HEAD before this edit: `3bafa9d12d611ea534b4847013fbf30a326be734`. Reviewed P663 (`f983acc`) with the already merged P705 fixes (`3676148`), rather than reporting those fixed issues again. This replaces this note's earlier missing-prerequisite status.

Read both work copies' `AGENTS.md`, the direction decision and task list, P481 sections 4, 7, 11 and 12, its F3 requirements, and P673 section 1.4. The supplied notes copy still lacks `cc-P663-*.md`, but the completed implementation is now in the code copy. Read `cc-P663-tutorial-moves-to-isle.md` and its Codex review from `D:/UO/shard-migration/notes/` as read-only evidence. Also read P705's implementation note and review there. No original repository was modified.

Review covered P663's tutorial sources, `CharacterCreation.cs`, `Fold/FoldRegions.cs`, the cliloc additions, and the changed tutorial tests. Followed account persistence and pinned ModernUO's gump reply and Young death paths where needed. All code paths below are relative to the supplied ShatteredLegacy work copy unless marked otherwise.

## New findings

### 1. Medium (P2): existing trainees never resume at the first unfinished stop

**Location:** `server/customizations/Tutorial/ClusterFTutorial.cs:97`, especially `:100` and `:105`; `server/customizations/Tutorial/TutorialStart.cs:206`.

**What happens:** An already enrolled character with saved core progress has no pending creation choice on its next login. The login cancels its active trial, then only points to Tamsin or Rook. It never moves the character to the first unfinished lesson. A pre-P663 InCore character standing in New Haven therefore remains there after login instead of resuming at the matching isle stop. An orphan's replacement that chooses the isle is always placed on the beach, even when its inherited first unfinished lesson is farther along the road. This misses F3 item 3's explicit resume rule. The exclusion for old characters that never enrolled should not suppress recovery for an active trainee.

**Fix:** Add an active-core recovery path that selects `CoreLeft(record).FirstOrDefault()` and crosses to a safe position at that stop on the trainee's lesson map, preserving done keys and taking pets through the crossing helper. Keep never-enrolled characters and trainees with all core lessons finished out of this relocation. Reuse it when adopting an orphaned active core record. Keep the current supply cancellation and regeneration behavior.

**Coverage gap:** `server/tests/Tutorial/TutorialIsleVerification.cs:182` starts a fresh character on the isle before adding old keys. It checks lesson order, not relocation of an existing trainee. The reconnect case at `:448` checks that the character stays on the isle and gets a fresh token, not that it resumes at the unfinished stop. Add a case starting an active legacy trainee in New Haven with some saved core keys, then assert its position after login; include an orphan replacement and an old saved travel key.

### 2. Medium (P2): retained Rook windows can teleport players from anywhere

**Location:** `server/customizations/Tutorial/TutorialGumps.cs:217` and `:260`; `server/customizations/Tutorial/ClusterFTutorial.cs:297`.

**What happens:** Open Rook's page as a skipper, keep it open, and leave New Haven. Skipping gives loop 1, so leaving the island is permitted. Clicking Restart later still calls `StartRemedial`, which immediately teleports the player and nearby controlled pets to the Fold. Neither the reply nor that method checks whether the player is alive, on Rook's map, or near him. An active trainee's retained core lesson button has the same problem. This turns ordinary tutorial buttons into a remote escape to the protected isle, including from a dungeon. The dedicated Go to the Wakening Isle button already checks Rook's proximity at `TutorialGumps.cs:222`, but the other buttons bypass that check.

**Evidence:** Pinned `D:/UO/ModernUO-pinned/Projects/UOContent/Gumps/Base/GumpSystem.IncomingPackets.cs:39` looks up the outstanding gump, `:57` validates the button, and `:166` invokes its response. It adds no NPC distance or map check. These are buttons the player actually received, so no invented button reply is required.

**Fix:** Require a living player near Rook on `HavenSpots.Map` at response time for every player-facing action that sends them from his page to the isle. Use one shared check for the explicit travel button, core lesson buttons, and remedial entry. Keep staff command authorization separate. Add retained-window cases after walking away, changing maps, and dying; assert no relocation or remedial state change.

### 3. Medium (P2): remedial and return trips bypass the missing-isle fallback

**Location:** `server/customizations/Tutorial/TutorialStart.cs:202`; `server/customizations/Tutorial/ClusterFTutorial.cs:304`.

**What happens:** On a world where `TutorialWorld.IsleReady()` is false, P705 safely redirects a new Tutorial Island choice to New Haven without entering the tutorial. However, a character that chose New Haven and skipped can ask Rook for remedial training on that same world. `StartRemedial` changes the record to Remedial and clears its lessons before calling `SendToIsle`, which never checks readiness. The player and pets are moved to the unbuilt beach. Seeding refuses that map, so there is no Tamsin or dock gate there. Rook's return-to-isle buttons also call this unchecked helper. This is a remaining entry path, distinct from the initial-creation fallback already fixed by P705.

**Fix:** Check readiness at the shared entry boundary and report failure without moving the player or pets. Make callers honor a success result; remedial entry must preserve the skipped record and its progress when entry fails. Add a skipper-at-Rook case with `IsleReady` false, then a successful retry after readiness becomes true. No readiness failure was reproduced in a running shard during this review.

## Requested checks

### Eligibility and choice consumption

`TutorialStart.Decide` at `server/customizations/Tutorial/TutorialStart.cs:95` and `ConsumeAtLogin` at `:139` implement the table as follows:

| Account or character state | Tutorial Island | New Haven | Review result |
|---|---|---|---|
| Fresh, NotStarted | Enter on this character and go to the isle, subject to readiness | Enter and skip, using the existing achievement and loop path | No additional table defect found. |
| InCore on another living character | Start in Haven and name the recorded character | Start in Haven without taking ownership | No additional table defect found. The same protection covers InWings and Remedial. |
| Graduated | Start in Haven with a finished-account message | Start in Haven | Account remains finished. Unlike the literal combined F3 table row, Rook offers no Remedial button to graduates; see the requirement ambiguity below. |
| Skipped | Start in Haven and bind this character for Rook's remedial offer | Start in Haven | No additional table defect found. The actual remedial trip has findings 2 and 3. |
| Recorded trainee deleted mid-core | Adopt this character and retain completed keys | Adopt and skip | Ownership recovery works; placement is finding 1. |
| Character with no recorded start choice | No automatic enrollment or creation-choice movement | Same | Correct for never-enrolled pre-go-live characters. Active records still need the separate resume handling in finding 1. |
| Staff | No enrollment or pending choice | Same | The real creation path selects Green Acres before calling `OnCreated`; the display-city fallback is also safe after P705. |

Requirement ambiguity: F3 item 6 combines Graduated and Skipped and says Rook offers Remedial training. The code accepts only Skipped (`ClusterFTutorial.cs:299`), consistent with the skipper-specific wording in P481 section 7 and F3 item 7. The overseer should clarify that combined row. Intent to reopen a graduated account is unverified; this review does not infer a new reward entitlement from the ambiguous table.

The choice is keyed by character serial in the account data (`TutorialStart.cs:75`, `:84`), not by one shared account flag. `ConsumeAtLogin` removes that character's key before applying the result (`:147`). A second login finds no choice; a different character cannot consume the first one's key. `ClusterFAccountData.cs:305` and `:533` read and write the flag values. The disconnect test serializes and reads a separate data object, then consumes the original live record. It supports the serialization layout and once-only behavior but is not a real restart test. No additional choice-consumption defect found by source inspection.

### Pets crossing

`TutorialWorld.PetsCrossing` (`server/customizations/Tutorial/TutorialWorld.cs:139`) includes controlled living and ghost pets owned by this character, excludes stabled, deleted and Internal pets, and collects all of its pets on Fold maps when the owner is on the Fold, regardless of distance or order. Entry from Haven takes pets within 12 tiles on the owner's map. `Cross` at `:162` moves the player first, verifies arrival, then moves the collected pets, so a refused player move does not strand pets at the destination.

Initial arrival when a move is needed, the dock exit, skipping on the isle, and remedial entry use that helper. The dock path at `TutorialCorePlacement.cs:270` checks the destination before crossing. No additional pet-selection defect found. Readiness and authorization of entry remain findings 2 and 3. Real mounted-pet, ghost-pet and save/restart crossings were not exercised.

### HavenSpots completeness and remaining Trammel references

The destinations specifically required by P673 section 1.4 are centralized after P705:

| Destination or rule | Consumer |
|---|---|
| Skip and ordinary creation start | `TutorialStart.Cities`, `OnCreated`, `SendHome`; `CharacterCreation.TutorialOffCities` |
| Rook | `TutorialRecruiter.Spot`, lookup and seeding |
| Dock exit beside Rook | `TutorialCorePlacement.GateExit` and the gate crossing |
| Haven island bounds | `TutorialIslandGate.IsOnIsland`; Fold maps also count as the island |
| Fold mirror send-home | `Fold/FoldRegions.cs:89`, through `HavenSpots.Start` and `.Map` |
| Town vet, public moongate and healer tour stop | `TutorialCorePlacement.FindTownVet`, town-vet seeding and trade-tour stop delegates |

No remaining literal `Map.Trammel` occurs in these core files: `TutorialCorePlacement.cs`, `TutorialCoreTrials.cs`, `TutorialFarm.cs`, `TutorialRecruiter.cs`, `TutorialIslandGate.cs`. Searched their actual source, not the generated `server/uo/` tree.

Remaining executable references in `server/customizations/Tutorial/` are listed here so the result is auditable:

| File | Lines | Meaning |
|---|---|---|
| `HavenSpots.cs` | 16 | Haven's configured facet. |
| `TutorialStart.cs` | 64, 65 | City-screen entries deliberately sent as Trammel under P481 section 7. |
| `TutorialTradeTrials.cs` | 223, 490, 496, 502 | Haven trade reach checks, spawned props and creatures, harvest-bank lookup. |
| `TutorialWingTrials.cs` | 51, 57, 209, 222, 310, 316, 553, 778, 785, 786, 787 | Haven wing ground, fit, reach, props and yard-region handling. |

The trade and wing references are intentional F3 scope: those lessons stay in Haven and move with S7. Their yard, farm, workshop and tour coordinates are still spread across their own layouts and trial definitions. Changing `HavenSpots` alone will not relocate that whole content set, but P673 assigns that work to S7; it is not a new P663 defect. Likewise, the mirror region's old rectangle and missing Felucca twin are explicitly S2 work, not fresh findings here. `TutorialWorld.MapOf` still returns the single map 32 as F3 requires; private copies belong to P664.

## Earlier reviews and verification limits

Compared against P663's automatic review and P705's follow-up review, P481 and P673's design reviews, and the earlier tutorial reviews P420, P421, P475, P480, P502, P503, P523, P573 and P619. Did not repeat dock surface height, tutorial-off creation coordinates, staff display coordinates, existing reward and loan issues, or the already assigned copy, vision and swap work. P705's notes-probe exit-status finding is outside this server review.

This was a source review only. No build, tests, client session, live save, or deployment was run; no new tests were added. The source paths establish the missing checks and relocation logic, but runtime reproductions and fixes remain unverified. P663's note records Chase's approval to defer the bot walk and client screenshots to P664; that approved deferral is not reported as a new finding.

Windows PowerShell 5.1 was confirmed for inspection. Only this notes file changed. No Haven connection, `docs/` edit, commit, merge, push or branch switch. Progress files were not regenerated because this is a notes-only review and the progress script writes generated files even with `--dry-run`. The stop-request file was absent at the last step check.

P700 DONE
