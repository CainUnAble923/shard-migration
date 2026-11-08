# Codex review: P853

CC task P853: assess creatures, mounts and gear systems from the 11-07/11-08 scout (breeding bloodli. Reviewed by Codex (`codex exec review`, read-only) after P853 DONE and before the Golem's commit, 2026-11-08 14:08.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.96). The note covers all twelve folders and supplies the requested shortlist, but omits an explicit research prerequisite and overstates ModernUO's existing ability coverage. Those gaps affect the assessment's recommendations.

- **medium** [P2] Distinguish existing abilities from ones requiring implementation (`notes\cc-P853-creatures-mounts-assessment.md:55`)
  Pinned ModernUO's MonsterAbility system does not already implement all these behaviors. For example, `EnergyBoltCounter.cs` delivers one immediate 50-damage counterattack against ranged attackers, whereas this download's `TripleBolt` schedules three bolts; the registered abilities in `MonsterAbilities.cs` also do not supply its teleport mechanic. The framework can support new implementations, but that is different from already providing them. Revise the equivalence and port-cost assessment so a skip decision does not erase potentially useful boss mechanics; [AGENTS.md:58???60](../AGENTS.md#L58-L60) requires source-verified content claims.
- **medium** [P2] Obtain the required breeding design before finalizing mount fit (`notes\cc-P853-creatures-mounts-assessment.md:26`)
  The task explicitly requires reading `claude/pet-breeding-design-notes.md`, or asking the overseer for its text if unavailable. Substituting the brief summary and another design document leaves that prerequisite unfinished, particularly before proposing a polar bear instead of the specified ice steed. Obtain the requested text and reconcile the bloodline recommendations before marking the assessment complete.

(1.6 minutes, 424,293 tokens)
