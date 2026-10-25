# Codex review: P457

CC task P457: Noted by the System fix-up 2: bard check, mining streak, ground at the destination, 15. Reviewed by Codex (`codex exec review`, read-only) after P457 DONE and before the Golem's commit, 2026-10-24 19:48.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.93). The main condition fixes appear implemented, but recycling still excludes loot contrary to Chase's explicit decision. I inspected the changes and reported build evidence in the notes; I did not independently run the Docker build or tests.

- **medium** [P2] Allow loot in the recycling eligibility check (`server\customizations\ClusterFNotedBySystem.cs:838`)
  When a player recycles fresh loot, this predicate rejects it because it requires both `PlayerConstructed` and a recorded matching crafter. Chase's explicit F07 decision allows items the recycler crafted **or loot**. The notes acknowledge deliberately excluding loot, but that leaves the requested behavior unimplemented. Preserve the rejection of another player's crafts while allowing eligible loot, and add a positive loot test.

(0.8 minutes, 366,258 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.96). The new note explicitly records an implementation that omits the requested loot exception. This repository contains only the task note as an uncommitted change; the server changes and reported test results could not be verified from this diff.

- **medium** [P2] Honor the explicit loot exception in the F07 decision (`notes\cc-P457-noted-fixups-2.md:104`)
  Chase's appended decision explicitly permits items the recycler crafted **or loot**, but the recorded implementation excludes loot entirely. Existing achievement wording does not override that instruction. Include the loot eligibility path and a positive loot test, rather than treating this already-settled requirement as a question for Chase.

(0.3 minutes, 92,431 tokens)
