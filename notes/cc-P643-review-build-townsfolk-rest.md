# P643: Review of P631 townsfolk and rest

Reviewed October 26, 2026. Documentation only. Code snapshot: ShatteredLegacy `a3f017e`; notes snapshot: shard-migration `0bc9e00`. P631's implementation is commit `7f55d21`, merged as `efc8af9`. Pinned ModernUO is still `d4531cd94b739613155225c234900de9f47d2c88`.

## Scope and evidence

Read both work-copy AGENTS.md files, the governing-document index, direction decision, task list, subsystem policy, fidelity principle and standing question answers. Compared `notes/cc-P631-build-townsfolk-rest.md` with `notes/cc-P566-design-townsfolk-features.md` and the completed P631 prompt at `D:/UO/cc-prompts/completed/cc-P631-build-townsfolk-rest.md`. That prompt records Chase's October 25 choices: Mara, Ellis and the existing innkeeper; 25 gold, 120 seconds without harm, 60-second reuse. Those choices are consistent with the implementation note. I did not find a separate October 25 decision-log file to independently verify that conversation.

P631 explicitly builds stage 1 only. Rest, the existing innkeeper extension, placement, package text and client acceptance are later stages in both the design and P631's prompt drafts. Their absence is not a finding against this stage.

Read both earlier reviews, `notes/cc-P566-design-townsfolk-features-codex-review.md` and `notes/cc-P631-build-townsfolk-rest-codex-review.md`. The findings below are additional findings, not repeats of P631's earlier review.

Canonical implementation and test files reviewed:

- `server/customizations/Townsfolk/ClusterFTalkRules.cs`
- `server/customizations/Townsfolk/ClusterFTownsfolkService.cs`
- `server/customizations/Townsfolk/ClusterFTownsfolk.cs`
- `server/data/townsfolk-talk.json`
- `server/tests/Townsfolk/TownsfolkTalkVerification.cs`
- `docker/uo/Dockerfile`, plus P631's `CHANGELOG.md` and `VERSION` diff

Also traced the relevant pinned speech, region, movement and gump-dispatch code and checked canonical patches for changes to those paths. Paths below are relative to the code work copy unless prefixed `pinned/`, which means `D:/UO/ModernUO-pinned/Projects/`.

## Findings

### F1. Medium (P2): Players can move the stationary residents through inherited speech

**Location:** `server/customizations/Townsfolk/ClusterFTownsfolk.cs:94`, especially the fallback at line 96; `server/tests/Townsfolk/TownsfolkTalkVerification.cs:64` and `:444`.

**What happens:** `Mara move` is not a dialogue alias, so it reaches `BaseCreature.OnSpeech`. In a guarded town, the stock AI recognizes a living nearby player's named move command. Its handler assigns a random adjacent `Location` directly, without checking `CantWalk`. It runs even with townsfolk talk switched off. Repeating it can displace Mara or Ellis from their chosen interaction tile, and the changed location is normal saved mobile state. That defeats the design's stationary residents and can put them in the way of tutorial props or away from their intended landmark.

**Evidence:** `pinned/UOContent/Mobiles/BaseCreature.cs:2522` recognizes a human in a guarded region, and `:2886` forwards unhandled speech to AI. `pinned/UOContent/Mobiles/AI/BaseAI/OnSpeech.cs:42` admits the named command; `:73` checks keyword `0x9D`; `:95` writes `Mobile.Location`. `pinned/Server/Mobiles/Mobile.cs:2559` calls `SetLocation`, whose body at `:7352` has no `CantWalk` guard. New Haven is a `TownRegion`, which derives from `GuardedRegion` (`pinned/UOContent/Regions/TownRegion.cs:5`). This is a source trace, not a client reproduction.

**Fix:** Keep the move command from relocating these two custom residents, using a narrow resident/AI override that leaves stock vendors alone. Add a regression through real `DoSpeech` with the move keyword in a guarded town, with talk both on and off. Advance beyond the stock five-second throttle and check that repeated attempts leave the location unchanged. The current fixture creates a plain `BaseRegion`, and the identity test only checks the `CantWalk` flag, so neither exercises this behavior.

### F2. Medium (P2): An accepted dialogue reload can swallow stock pet orders

**Location:** `server/customizations/Townsfolk/ClusterFTalkRules.cs:100` and `:370`; `server/customizations/Townsfolk/ClusterFTownsfolkService.cs:170`.

**What happens:** The reserved set omits actual stock commands such as `all follow me` and `all guard me`. Adding `all follow me` to a topic's aliases passes validation. If a resident is closer than the player's pet, it handles that speech first, marks the event handled and gives its flavor answer. The later pet dispatch skips its AI because the same event is already handled. A table accepted as safe can therefore change ordinary pet control, contrary to the design's speech-command contract. The shipped table does not currently contain this alias.

**Evidence:** A local probe compiled the unchanged canonical parser and accepted an `all follow me` alias with no errors. The actual stock keywords are `0x16C` and `0x16B` in `pinned/UOContent/Mobiles/AI/BaseAI/OnSpeech.cs:159`. The distance-sorted dispatch is at `pinned/Server/Mobiles/Mobile.cs:5728`, and the `!e.Handled` AI guard is at `pinned/UOContent/Mobiles/BaseCreature.cs:2886`. Suppression of a live pet's order was not run.

**Fix:** Complete the reserved-command validation against the pinned command handlers, including these multiword forms. At dispatch, also preserve recognized stock service/control keywords before claiming generic dialogue. Add a parser regression and a real dispatch regression with a resident closer than a controlled pet, carrying keyword `0x16C`, so the assertion observes the pet receiving its order rather than only a matcher result.

### F3. Medium (P2): Region keys are not validated before replacing a good table

**Location:** `server/customizations/Townsfolk/ClusterFTalkRules.cs:274` and `:327`; `server/customizations/Townsfolk/ClusterFTownsfolkService.cs:93`.

**What happens:** A profile's region is accepted as any nonempty string. Changing `New Haven` to `New Havn` successfully replaces the working table, with no errors, and that resident then stops answering because its runtime region cannot match. A valid but unintended region such as `Britain` is accepted too. The innkeeper profile can likewise be widened from `the New Haven Inn` to `New Haven`. Once stage 2 uses that profile, conversations would follow that broader gate. This finding does not claim an unimplemented rest eligibility bypass.

The design calls for an allowed region key and validation before swapping tables. Checking only that the value is a string turns a common data typo into a successful but broken reload.

**Evidence:** The parser probe accepted the typo, `Britain`, and the widened innkeeper region. Starting with the shipped table loaded, reloading the typo file returned `success=True`, `replaced=True`, `errors=0`. Runtime eligibility reads that string directly. Pinned `Region.IsPartOf` follows region names and ancestry (`pinned/Server/Regions/Region.cs:515` and `:545`); it cannot correct the typo.

**Fix:** Validate the launch tag-to-region mapping: plaza and trades use `New Haven`, innkeeper uses `the New Haven Inn`. Keep descendant-region acceptance in runtime checks. Reject a mismatched key before replacing `Current`; do not depend on live region registration during startup. Add typo and broader-region reload regressions that assert the previous table stays in use.

### F4. Low (P3): Additional topic IDs can inject markup into the menu

**Location:** `server/customizations/Townsfolk/ClusterFTalkRules.cs:337`; `server/customizations/Townsfolk/ClusterFTownsfolk.cs:158` and `:171`.

**What happens:** Additional topics are allowed, but their IDs receive only a nonempty-string check. The menu displays an unknown ID directly through `Label` and `TutorialStyle.Html`. That helper adds a color wrapper without escaping the text. An accepted extra topic whose ID is `<BASEFONT COLOR=#000000>Extra topic` therefore supplies client HTML instead of a plain label. Control characters and excessively long IDs also escape the response-text validation. This requires staff-authored table data; it is not a player chat injection.

**Evidence:** The unchanged parser accepted that extra topic with no errors. `server/customizations/Tutorial/TutorialStyle.cs:39` interpolates its argument, and `pinned/UOContent/Gumps/Base/Legacy/GumpHtml.cs:50` forwards the text to the gump string table. The NPC name is escaped at line 153 of the resident file, but topic labels are not. Actual client rendering remains unverified.

**Fix:** Give IDs a bounded plain identifier syntax, rejecting whitespace-only IDs, markup and control characters. Escape every table-derived menu label before passing it to HTML. Add a parser regression for the example and a gump-content assertion showing that a fallback label cannot add HTML tags.

### F5. Low (P3): The required packet and menu lifecycle checks are still missing

**Location:** `server/tests/Townsfolk/TownsfolkTalkVerification.cs:67`, `:282`, `:378` and `:386`.

**What is missing:** The privacy test watches the service's own `Replied` event, which reports the intended recipient after the send. The bystander has no NetState and no outgoing bytes are inspected. A regression that broadcasts the actual message while retaining that event payload could still pass. The menu helper removes a gump with reflection and calls `OnResponse` directly. It never tests the real packet lookup for a closed/replayed gump or logout/reconnect, and it does not cover a same-character replacement session, deleted NPC, map change, LOS change or table reload while a menu is open. P566 explicitly requires those cases for the talk surface.

**Fix:** Give speaker and bystander test NetStates and inspect the actual outgoing NPC speech packets. Exercise menu responses through `GumpSystem.DisplayGumpResponse` for close/replay/disconnect/session cases, then cover the listed eligibility and reload changes. See each added regression fail before its corresponding fix or deliberate mutation, as the working agreements require.

This is a coverage finding, not a claim that the engine currently permits cross-session replay. Pinned `UOContent/Gumps/Base/GumpSystem.IncomingPackets.cs:39` looks up a gump within the sending NetState, and `:157` removes it before calling the callback; `pinned/UOContent/Gumps/Base/GumpSystem.cs:39` clears disconnected-session gumps. Those engine protections are why a direct callback probe alone would not establish a network exploit.

## Save/load and other limits

The new resident's tag uses generated serialization version 0 without changing a saved stock class's parent or fields. The existing test serializes and deserializes the tag and name. It does not verify equipped clothing, a complete world save/restart, or world placement idempotence. Those remain explicitly assigned to stage 3, so they are acceptance work still owed, not a new save-corruption finding. Rest money, combat history, cooldown persistence and saved innkeeper integration cannot be reviewed as implemented behavior because stage 2 is absent.

P631's note reports its build and red/green runs. I read that evidence but did not independently rerun the shard build or its test suite. No client, live world, saved accounts, Haven service or Docker daemon was contacted. No claim here certifies the final runtime image or in-client appearance.

## Validation

The only executable behavior probe was a small offline .NET 10.0.201 console program linking the unchanged canonical `ClusterFTalkRules.cs`. Its only engine shim supplies `Core.BaseDirectory`; it uses the actual shipped JSON and prints parser/reload results. It is diagnostic scratch, not a new shard test. Files are under the existing ignored `downloads/p643-review/` directory, verified with `git check-ignore downloads/p643-review/probe.csproj`. The canonical JSON and C# files were not edited. No new test, code fix, deployment, commit, merge, push or branch switch is part of P643.

Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies, under Windows PowerShell 5.1.26100.9711. Exit 0. The tool writes `tools/progress.json` even in dry-run mode; its original bytes were captured and restored, with an exact byte comparison afterward. No progress-data change is included in this review.

Final checks: both repositories passed git diff --check. The code work copy has no tracked changes; the notes work copy contains only this new review. No docs/ file changed. The note is valid UTF-8, below 5 MB, and contains no em dashes, replacement characters or trailing whitespace. Every scratch artifact is below 5 MB. Stop-request checks between steps found no request.

P643 DONE
