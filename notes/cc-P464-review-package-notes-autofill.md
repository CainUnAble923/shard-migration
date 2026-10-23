# P464: review of the player package What is new autofill

Reviewed 2026-10-23 against ShatteredLegacy HEAD `4c2af57`, including the P288 implementation commit `5a0b764`. This is a notes-only review. No code or tests were changed.

Read `cc-P288-package-notes-autofill.md` and `cc-P288-package-notes-autofill-codex-review.md` first. The earlier review's script-promotion cutoff and selected-script comparison findings are not repeated here.

## Findings

1. **bug**, `scripts/Shard-Console.ps1:1901`, with `web-console/server.py:140`: A title containing curly double quotes produces straight double quotes, such as `Hestia "hero" robes`, but the web console rejects that generated Notes value with HTTP 400 because its input rule forbids double quotes. Normalize quoted names to characters the web input accepts, or support quotes through the existing structured argument path, and add a regression that passes the generated line through `Console.page_args`.

2. **risk**, `scripts/Shard-Console.ps1:1967`: The staff-only exclusion requires a newly added changelog line, so an art follow-up with no changelog change can advertise a feature that is still staff-only; an unchanged Staff entry plus a dragon art edit produced `Rideable red dragon` with an empty `LeftOut` list. Carry the feature's visibility into follow-up commits, or require an explicit player-visible designation when there is no new player line, and cover a staff-only original followed by an unlogged art fix.

3. **risk**, `scripts/Shard-Console.ps1:1919`: A prompt-derived name longer than the 120-character limit is discarded whole, so a single 144-character name produced a blank `Line` while `Items` still contained the entry and `Empty` was false. Shorten an individual name at a word boundary before joining, with a usable fallback, and add a case where the first or only name exceeds the limit.

These are ours to fix. Findings 2 and 3 use injected inputs to establish the edge cases; neither was observed in the current shipping history.

## Evidence and verification

- Read the P288 functions, Git fact gathering, desktop Notes/Refill wiring, and relevant build-plan handling in `scripts/Shard-Console.ps1`; the package branch in `scripts/Get-WebConsoleList.ps1`; and the P153/P288 facts in `scripts/tests/Shard-Console.Tests.ps1`.
- Read the Notes field, autofill, Refill, and text rendering in `web-console/static/app.js`; the twin in `web-console/console-actions.json`; the phone test in `web-console/tests/test_pages.py`; and its data in `web-console/tests/fixtures/fake_list.py`.
- Checked the receiving input rules and `Console.page_args` in `web-console/server.py`, the ASCII requirement and notes output in `player-package/Build-PlayerPackage.ps1`, and the local changelog/history used by the suggestion.
- Ran the existing console facts with Windows PowerShell **5.1.26100.9444**, using `SL_FACT_FILTER=^P288_|^P153_.*Package|^P153_.*Notes|^P153_.*WhatsNew` and `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\tests\Shard-Console.Tests.ps1`: **8 passed, 0 failed**. These were `P153_TheSuggestedWhatsNewLine`, `P153_ThePackageTabHasTheSuggestionAndItsList`, and the six `P288_` facts at lines 8514, 8531, 8539, 8549, 8568, and 8588.
- Ran separate in-memory PowerShell 5.1 probes against the existing functions for all three findings. The quote probe produced `Hestia "hero" robes`; a Python import of the real web server module and direct call to `Console.page_args(None, {'inputs': ['packageNotes']}, {'packageNotes': notes})` returned `(400, 'packageNotes is not allowed: ...')` without starting a server.
- Reproduced finding 2 with an identical before/after changelog containing only `### Staff` and `- A rideable red dragon for staff to try.`, an empty added-line array, and a commit titled `CC task P999: rideable red dragon` touching `player-package/vendor/shattered-legacy-art/art/28295.png`. The suggestion included the dragon; the existing test only covers a shipping commit that adds its Staff line in that same commit.
- Reproduced finding 3 with `('custom decoration collection ' * 5).Trim()` as the title's name and one art path. The existing long-list fact checks many short names, not one name that cannot fit.
- Called `Get-WhatsNewFacts` directly against this local work copy with version `2026.10.18.1122`, without a ZIP commit or Legion repo, then called `Get-PackageSuggestion`. It resolved `ac9eee3` and reproduced the documented headline: `Tutorial farm, Rootdeep map, fog of war, League hunt bestiary, Kitsune ears and tail, New Haven community art and more`; the staff-only P277 dragon and P265 guild-hall decor remained excluded. No additional repeat-entry defect was confirmed on this history.
- Ran `python -B tools\progress.py --dry-run` in the notes work copy with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies: exit 0. Despite that flag, `build()` rewrote `tools/progress.json`; restored that initially clean generated file byte-for-byte from HEAD, leaving only this review note changed.

The full web suite and browser test were not rerun. Live published-package state, actual launcher display, and actual script promotions are unverified; no Haven connection, deployment, package build, commit, merge, push, or branch switch was performed. No new test or gate was added, so no red/green claim is made for a repair.

P464 DONE
