# Codex review: P863

CC task P863: port Color Wars as an opt-in staff team event. Reviewed by Codex (`codex exec review`, read-only) after P863 DONE and before the Golem's commit, 2026-11-10 17:52.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.98). The change implements the requested staff-run event and includes tests and proof notes, but cleanup and restart recovery leave actionable gameplay defects. Build and client results were inspected through the supplied notes, not independently rerun.

- **medium** [P2] Restore pending resurrection work when loading a run (`server\customizations\StaffHub\StaffColorWars.cs:1043`)
  If the world is saved after a participant dies but before their resurrection timer fires, restarting restores the participant as dead but never schedules `Revive` again. `Timer.DelayCall` callbacks are not persisted, and this load path only registers the region. That participant remains a ghost rather than automatically returning to battle. Recover dead participants when restoring the run, with coverage for a save during the resurrection delay.
- **medium** [P2] Check for an active run before calculating its leader (`server\customizations\StaffHub\StaffColorWars.cs:437`)
  Running `[ColorWars end` when no event is open calls `Leader(null)` and throws before reaching the inactive-run guard in the other overload. This also occurs when a second GM presses End on a stale gump after another GM finishes the event. Check `Active` before calculating the leader so these supported entry points return the intended 'not open' message.
- **medium** [P2] Clear event poison before restoring personal belongings (`server\customizations\StaffHub\StaffColorWars.cs:734`)
  If a living participant leaves while poisoned, or staff end the battle while they are poisoned, `Leave` restores their belongings and removes event membership without clearing the poison. ModernUO's poison timer continues damaging them after teleportation, so an event attack can kill them outside the protected arena with their personal inventory restored. Clear event damage effects before returning players and their equipment.
- **medium** [P2] Reclaim split kit stacks outside the participant's inventory (`server\customizations\StaffHub\StaffColorWars.cs:706`)
  A player can split the lent arrows, bandages or reagents, drop the new stack on the arena floor, and leave. The new stack is absent from `p.Kit`, and this cleanup searches only the departing player's inventory, so the dropped supplies survive the event. Repeated joining and leaving therefore generates unlimited permanent supplies, contrary to the lent-and-reclaimed kit behavior. Track split items or prevent their transfer outside the managed kit.

(1.9 minutes, 730,398 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.95). The verification scripts violate the task's explicit build/test restriction despite the separately reported green gated build. This review covers the documentation repository's uncommitted artifacts; the server implementation and version changes are not present in this diff.

- **medium** [P2] Run the verification through the required build entry point (`notes\cc-P863-tools\run-facts.sh:16`)
  P863 explicitly requires building and testing only through `docker/uo/build.sh`, but this runner invokes `dotnet build` and `dotnet test` directly against the unrelated P872 builder image; `run-mutants-inner.sh` does the same. These runs overlay selected files onto an older build tree instead of exercising the patch routing and complete sources used by the supported gate. Route the red/green verification through the required entry point rather than maintaining this parallel test path (see [AGENTS.md:85???90](../../AGENTS.md#L85-L90)).

(0.8 minutes, 353,031 tokens)
