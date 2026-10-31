# Codex review: P751

CC task P751: fix the seven items from P746's build review (isle coast, farm, farmhouse, lodge). Reviewed by Codex (`codex exec review`, read-only) after P751 DONE and before the Golem's commit, 2026-10-31 17:01.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is correct (confidence 0.81). No actionable defects found in the changes. The fixes have supporting tests, renders and real-client walk evidence; the lodge sign's departure from the requested coordinates is documented with visibility shots. I did not rerun the build or tests.

No findings.

(1.4 minutes, 1,024,392 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.94). The changes provide substantial fix and build evidence, but the real-character walk still misses lesson detours and records height transitions exceeding the review's explicit acceptance limit. Server implementation correctness was not independently verified in this docs-repository review.

- **medium** [P2] Include the lesson detours in the real-character walk (`notes\cc-P751-tools\walk_paths.py:33`)
  The route walks consecutive stop markers and adds building-door excursions, but never enters the fenced field to reach the pests or walks the training-yard echo/Sera detours. Those are actual lesson paths: `build-isle-ship.txt` lists them separately under the server-walker checks. Consequently, the saved TazUO run does not prove the prompt's ???every lesson path??? requirement, particularly traversal of the farm gate beside the changed fence. Add these detours to the client route and save the resulting log and shots.
- **medium** [P2] Resolve the excessive height changes before accepting walk proof (`notes\cc-P751-review\README.md:35`)
  The new walk log records farmhouse transitions of +4 and +3 Z (and the reverse), plus a 4-Z transition at the moongate platform. These exceed the explicit maximum of 2 in [the building guide](notes/guides/building-and-decorating.md#L235-L236), which P748 item 6 specifically required this task to verify. Successful traversal is useful evidence, but reporting ???no step over 4??? does not satisfy that acceptance condition. Adjust these joins and repeat the walk, or obtain an explicit exception rather than marking the review item complete.

(1 minutes, 522,466 tokens)
