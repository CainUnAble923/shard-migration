# Codex review: P456

CC task P456: Music Room saves that cannot lose notes; music fallbacks for a missing or unknown trac. Reviewed by Codex (`codex exec review`, read-only) after P456 DONE and before the Golem's commit, 2026-10-25 14:28.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The patch addresses most requested paths, but stale revisions can still overwrite newer notes, lost responses strand retries, and Save to repo can report completion before newer edits are saved. The task notes also explicitly defer the requested in-client audio verification.

- **medium** [P2] Drain newly queued edits before completing flush (`web-console\static\music.js:218`)
  While Save to repo waits for a slow save, the fields remain editable. If another edit occurs shortly before that save completes, its debounce timer has not fired, so `again` is still unset and the awaited promise resolves. This final check only inspects failures, allowing the commit to proceed with the older note and report success while the latest edit is still pending. Recheck and drain timers and in-flight saves before completing the flush, or prevent edits during the operation.
- **medium** [P2] Recover safely when a successful save loses its response (`web-console\static\music.js:196`)
  If the server writes a note but its response is lost, the catch marks the record failed while the browser retains the old revision. Retry, subsequent edits, and Save to repo then repeatedly submit that stale revision and receive 409. Following the reload instruction can discard newer unsaved edits. Add reconciliation or idempotent retry handling so a transport failure after a successful write does not permanently strand the dirty record.
- **medium** [P2] Preserve revision history when clearing a record (`web-console\music.py:460`)
  Clearing a record resets its revision, allowing previously used revisions to recur. For example, a tab holding revision 1 can overwrite a newer note after another tab clears the record and creates a replacement at revision 1. The stale request then passes the revision check and silently replaces the newer note. Retain a monotonically increasing revision across clears, such as through a tombstone.

(1.1 minutes, 262,146 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.94). The only change in this repository is the new task note; implementation and test claims in the separate code repository were not verified here. The note documents a remaining stale-save hole and an explicitly required runtime check that was not completed.

- **medium** [P2] Complete the required game-PC verification before declaring DONE (`notes\cc-P456-music-room-saves-and-fallbacks.md:123`)
  Part 5 explicitly requires checking the two packet cases on the game PC, but this delivery substitutes source analysis and leaves the actual check to Chase. Source analysis does not verify the installed client's behavior. Obtain runtime evidence for both cases, or mark the task incomplete rather than emitting DONE; [AGENTS.md:45???46](../AGENTS.md#L45-L46) prohibits the completion marker before the work is finished because the Golem acts on it immediately.
- **medium** [P2] Preserve revision identity when clearing a track (`notes\cc-P456-music-room-saves-and-fallbacks.md:125`)
  Resetting the revision to zero allows stale saves after a clear-and-recreate cycle: tab A holds revision 1, tab B clears the record and creates a new note at revision 1, then tab A's stale save is accepted and overwrites B's note. This violates the prompt's stale-revision refusal requirement, beyond the revision-zero case acknowledged here. Preserve a monotonically increasing revision or tombstone across clears and test this cycle.

(0.6 minutes, 126,158 tokens)
