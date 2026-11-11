# Codex review: P877

CC task P877: fix-up for P861 (CC task P861: port extra NPC name lists and [VBuild statify): its bui. Reviewed by Codex (`codex exec review`, read-only) after P877 DONE and before the Golem's commit, 2026-11-10 18:25.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.94). The fountain refusal and requested review artifacts are present, with recorded build and in-game verification. However, the fixed-identity protection remains incomplete and can rename stock quest NPCs. Tests were not independently rerun.

- **medium** [P2] Preserve fixed identities of stock quest NPCs too (`server\customizations\Names\ShardNames.cs:232`)
  When a stock quest NPC shares a town with an older randomly named namesake, this exemption still allows the quest NPC to be renamed. For example, pinned ModernUO's `Regina` (`Engines/ML Quests/Definitions/HonestBeggar.cs`) derives from `BaseCreature`, has `DefaultName => "Regina"`, and matches the female name list, but satisfies neither exemption here. The hourly sweep can therefore permanently rename her even though quest text and items identify her as Regina. Recognize stock fixed identities as well as the custom NPC types, and add a regression test covering a stock quest giver.

(2.5 minutes, 1,031,627 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.83). No actionable defects found in this repository's changes. The requested P877 review folder contains an isorender, client screenshots and placement details consistent with the recorded checks. Server implementation changes reside in the separate code repository and were not verified here; tests were not rerun.

No findings.

(0.7 minutes, 328,361 tokens)
