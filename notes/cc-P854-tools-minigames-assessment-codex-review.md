# Codex review: P854

CC task P854: assess staff tools and minigames from the 11-07/11-08 scout. Reviewed by Codex (`codex exec review`, read-only) after P854 DONE and before the Golem's commit, 2026-11-08 14:15.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.99). The assessment covers all requested folders and supplies the requested shortlist, but it incorrectly identifies ticketed travel as missing and omits explicit source licensing conditions for Color Wars. Both affect decisions this assessment is intended to support.

- **medium** [P2] Record Color Wars' explicit credit-preservation terms (`notes\cc-P854-tools-minigames-assessment.md:43`)
  Color Wars does state distribution terms in its source headers. For example, `Event Items/EventBox.cs`, `EventEnd.cs`, and `EventEthereal.cs` identify Vorspire as the original author and permit distribution and modification only while leaving the credit notes intact. The blanket claim of no stated license and the table's Omni-only credit omit this requirement. Record the header-preservation condition and original author here and in the intake assessment so any subsequent reuse follows the actual terms.
- **medium** [P2] Account for the existing ticket teleporter (`notes\cc-P854-tools-minigames-assessment.md:35`)
  Pinned ModernUO already implements `Server.Engines.MLQuests.Items.TicketTeleporter` in `Projects/UOContent/Engines/ML Quests/Items/Teleporters.cs`: it checks for a configurable ticket type, refuses passage without it, and invokes `ITicket.OnTicketUsed` for consumption. The claim that none takes an item is therefore incorrect, and the proposed new pass teleporter duplicates existing functionality. Revise the comparison and recommendation around reusing this implementation, consistent with [AGENTS.md:231???232](../AGENTS.md#L231-L232).

(1.4 minutes, 421,522 tokens)
