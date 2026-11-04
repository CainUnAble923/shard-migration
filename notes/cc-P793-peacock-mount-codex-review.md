# Codex review: P793

CC task P793: tamable peacock mount. Reviewed by Codex (`codex exec review`, read-only) after P793 DONE and before the Golem's commit, 2026-11-04 08:35.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.9). The mount, body typing, shrink art, automatic spawning, and tests largely satisfy the prompt. However, malformed configuration can escape validation and disrupt startup. I inspected the recorded build evidence but did not rerun Docker tests.

- **medium** [P2] Reject null spawn entries before validating their fields (`server\customizations\Mobiles\Mounts\PeacockTable.cs:155`)
  If `Configuration/peacock.json` contains `"spawns": [null]`, deserialization succeeds, but this dereference throws `NullReferenceException`. Because validation runs outside the JSON exception handler, the exception escapes both startup configuration and `[Peacock reload` instead of refusing the file and retaining the current table. Reject null entries with a validation error before accessing their fields.

(1.6 minutes, 472,135 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.79). No actionable defects found in this repository???s new notes, proof tools and screenshots. The server implementation is in the separate code repository, so its correctness and full task completion cannot be independently established from this diff.

No findings.

(1 minutes, 328,011 tokens)
