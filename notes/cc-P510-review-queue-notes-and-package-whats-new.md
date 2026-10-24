# P510: review of queue notes and the package What is new

Reviewed 2026-10-23 against ShatteredLegacy HEAD `579ad58f8f478280b03b8cf80f1ee9a5b3001a27`.
P153 implementation `cde0d3f` is in local `main`, merged by `86b7c75`.
This is a notes-only review. No code or tests were changed.

Read `cc-P153-queue-notes-and-package-whats-new.md` first; no P153-specific review was beside it.
P288 replaced the package summary generator, so I also read its implementation notes and Codex review,
plus `cc-P464-review-package-notes-autofill.md` and its review. Their findings are not repeated here.

## Findings

1. **bug**, `scripts/Shard-Console.ps1:7619`: When the running prompt is in `claimed\<Golem>`, `Get-GolemExtra` reads only the top-level prompt path, so its running row loses the Summary and actual model, showing the filename in gray and defaulting to Opus even though Open prompt finds the file. Use `Find-HandedPromptPath` for the summary read too, and add a fixture with a claimed Fable prompt that checks its running note, model, and exported queue row.

2. **bug**, `scripts/Shard-Console.ps1:5092`: For a prompt without a Summary, the paragraph reader skips only Model, Kind, and Summary headers, so the current prompt format's `**Touches:** docs-only` becomes the queue note instead of the opening prose. Skip the other prompt metadata fields before collecting prose, and add a no-Summary fixture containing Touches, Agent, and Lane tests headers before the opening sentence.

These are ours to fix. No additional package finding or staff-only text reaching players was confirmed
beyond the existing P288 and P464 reports.

## Evidence and verification

- Read the queue parser, prompt text collection and cache, queue rows, desktop grid and selection handling,
  Open prompt, and status export in `scripts/Shard-Console.ps1`; read the P125 and P153 queue facts in
  `scripts/tests/Shard-Console.Tests.ps1`.
- Read the current package parser, summary generation, Git collection, Notes/Refill/Build wiring, and
  build-plan handling in `scripts/Shard-Console.ps1`, along with the P153 and P288 package facts.
  Checked the P153 web model picker in `web-console/static/app.js` and its tests in
  `web-console/tests/test_pages.py`. The previously reported package defects remain outside this finding list.
- Ran existing facts using Windows PowerShell **5.1.26100.9711**:
  `SL_FACT_FILTER=^P153_.*Queue|^P153_.*Package|^P153_.*Notes|^P153_.*WhatsNew|^P288_`, then
  `powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\tests\Shard-Console.Tests.ps1`.
  **10 passed, 0 failed**, all in `scripts/tests/Shard-Console.Tests.ps1`:
  `P153_TheQueueRowsAreInRunOrderWithANoteEach`, `P153_TheStatusFileCarriesTheQueueRows`,
  `P153_TheSuggestedWhatsNewLine`, `P153_ThePackageTabHasTheSuggestionAndItsList`,
  `P288_ClientCommitsMakeTheLineAndServerOnlyCommitsDoNot`,
  `P288_NothingNewSaysNoClientChangesSinceTheVersion`, `P288_ALongListIsCutToFit`,
  `P288_ShortNamesComeFromPromptTitles`, `P288_ThePublishedCommitFromItsZipOrItsBuildTime`,
  and `P288_TheNotesBoxFillsAndRefills`.
- Reproduced finding 1 with the real `Get-GolemExtra`, `Get-PromptInfo`, and `Get-QueueRows` against an
  isolated local prompt folder. With the file only under `claimed\Valorite`, `Find-HandedPromptPath`
  returned its correct path, but the collected text was null and the row was
  `Note=cc-P510-review-queue.md; Model=Opus; Grey=True`. Putting identical text in the top-level folder
  produced `Note=Review the queue notes and package summary.; Model=Fable; Grey=False`.
- Reproduced finding 2 with an in-memory prompt containing Model, Touches, Agent, and Lane tests metadata,
  no Summary, and the prose `Review queue notes for missing entries. Write findings only.`
  `Get-QueueRows` returned `Note=Touches: docs-only; Grey=True`.
- The current queue fact supplies already parsed prompt objects, and its no-Summary fixture has only
  Kind metadata. The status fact checks row count and shape, so neither fixture catches these defects.
  No new test or gate was added, and no repair or red/green repair verification is claimed.
- Probe files were under paths verified with `git check-ignore` and were removed after use. Ran
  `tools/progress.py --dry-run` with both work-copy paths set, exit 0; suppressed its internal
  `Path.write_text` calls in memory because even dry-run normally writes `tools/progress.json`.
  No generated progress file was changed. Git whitespace checks passed.

The full console and web suites were not rerun. Live package contents, launcher display, Haven state,
and the external Golem runtime are unverified. No Haven connection, deployment, package build,
commit, merge, push, or branch switch was performed.

P510 DONE
