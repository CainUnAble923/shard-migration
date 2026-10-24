# P509: Review of the play-test decisions inbox (P146)

Reviewed 2026-10-23. Notes only. These are our inbox defects and test gaps to fix later, not ModernUO or ServUO defects.

P146 is in local code `main`: commit `858ae66` is an ancestor. Read `notes/cc-P146-playtest-decisions-inbox.md`; no separate P146 review was present beside it. The findings below do not repeat that note's known importer, triage, or environmental issues.

## Findings

1. **bug**, `shard-migration/tools/decisions.py:244`: Answers join to questions only by their positional ID, so inserting a bullet before an answered question silently attaches its answer to a different question; a scratch example moved "Use oak for the door" onto "Add a lamp?" as `P900-D2`. Give questions persistent IDs and check the saved question revision before applying an answer, with regression coverage for inserted, reordered, and renumbered entries.

2. **bug**, `shard-migration/tools/decisions.py:259`: The list is built only from current notes and the overlay, so removing an answered question leaves its answer in `decisions.json` but hides it from the page, new-answer counts, and Copy new answers; the scratch removal returned empty copy text while the stored answer still existed. Include unmatched stored answers as archived questions using their saved question text, and test removal and temporary loss of a notes source.

3. **risk**, `shard-migration/tools/decisions.py:439`: Taken requests carry only IDs, so an overseer who copied answer A can silently mark a later answer B taken, and a delayed undo at line 443 can reopen an answer subsequently taken into another prompt, making it eligible for another task. Require the answer revision and expected taken record on these transitions, reject stale requests under the existing lock, and test stale take and repeated undo sequences.

4. **bug**, `docker/test-queue/html/index.html:361`: Replacing the list's `innerHTML` discards unsaved decision text when a Where chip changes or another card saves, because the textarea at line 430 is rebuilt only from the saved answer. Preserve drafts by decision ID across renders and loads, and add a browser regression that types a draft, changes a chip or saves another card, and checks that the draft survives.

5. **risk**, `shard-migration/tools/tests/test_decisions.py:410`: The page tests check source substrings and ASCII but never execute the renderer with hostile answer text or identity fields, so an escaping regression could pass the suite. Add a DOM test using quotes, tags, and a `</textarea>` payload in answers and writer names, asserting literal text and no injected elements or event execution.

## Evidence and limits

- Read the P146 implementation files and tests: `tools/decisions.py`, `tools/playwhere.py`, `tools/opsdata.py`, `tools/tests/test_decisions.py`, and the P146 fact in `tools/tests/test_play_who.py` in shard-migration; `docker/test-queue/server.py`, `docker/test-queue/html/index.html`, and `docker/test-queue/README.md` in the code repo. Also checked `playtests.py`'s notes discovery, DONE check, normalization, and lock, plus the overlay and current stored-answer joins.
- Ran the existing `tools/tests/test_decisions.py`: 20 passed, one failed, no errors in the completed run. The failure is `RealFiles.test_every_you_decide_item_is_replaced_by_its_decisions`: the later `P378-4` DECISION row has no replacement in the overlay. This is current data drift, not a new P146 implementation finding.
- The existing P146 `test_play_who.py` fact also fails on current items without Where metadata, including `M-001`. This review does not change their triage.
- Test runner adaptations were in memory only: point SERVER/PAGE at this code work copy and create temporary directories with ordinary inherited permissions under `shard-migration/.venv/p509/`, proven ignored by `git check-ignore`. Earlier attempts using Python's private temporary-directory permissions failed during setup with `PermissionError`; the adapted decision run reached every assertion and exercised the service on loopback.
- Direct calls to the unchanged Python functions with scratch notes and stores reproduced findings 1 through 3. The saved-answer audit of the current repo mirror found no unmatched IDs or mismatched question text; these fixtures demonstrate failure modes, not evidence that Chase's existing answers have already been corrupted.
- Finding 4 follows the actual chip handler, save/load path, list replacement, and textarea renderer. Browser reproduction remains unverified: installed headless Chrome exited before Selenium could create a session. The scratch service was stopped in cleanup.
- No unescaped player data was found in the reviewed decision renderer: `esc` at `index.html:272` covers text and attributes, `md` escapes before formatting, and answer text, writer names, dates, and textarea content use those helpers. Browser execution of malicious payloads remains unverified because Chrome could not start; finding 5 records the missing automated coverage.
- Ordinary answer writes load and save under the existing lock, and repeated take requests against the same taken state do nothing. Finding 3 concerns changes between the overseer's read and write, not a claim that every retry applies a decision twice.
- Ran the required progress reporter with `--dry-run` and both work-copy path overrides. Its known `tools/progress.json` write was intercepted in memory to keep this review notes only; report generation completed and no reporter file changed.
- No production code or tests were changed or added. No Haven connection, deployment, account change, commit, merge, push, or branch switch occurred. All PowerShell commands ran through Windows PowerShell 5.1.

Final validation passed: only this notes file is pending, it is under 5 MB, it contains no em dashes, and both repos pass `git diff --check`. The stopping-point file was absent at the final check.

P509 DONE
