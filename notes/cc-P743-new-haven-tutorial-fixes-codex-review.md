# Codex review: P743

CC task P743: New Haven tutorial fixes (Echo's sparring, extra farm, mining path, horse taming, bard. Reviewed by Codex (`codex exec review`, read-only) after P743 DONE and before the Golem's commit, 2026-10-31 23:07.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.99). The stable-horse lesson is blocked by Trammel's healing restrictions and can also become untreatable through regeneration. The mage demonstration does not enforce the requested observation period. Runtime gates and TazUO/render evidence were not verified during this read-only review.

- **high** [P1] Allow the trainee to bandage the uncontrolled stable horse (`server\customizations\Tutorial\NewHavenLessons.cs:551`)
  For an ordinary player on Trammel, `BandageContext.BeginHeal` calls `CanBeBeneficial`, and pinned `Notoriety.Mobile_AllowBeneficial` rejects healing uncontrolled creatures. This horse remains uncontrolled until after healing, and neither the existing yard-region exception nor the Pip exception covers it. Consequently, the first required bandage is refused and Animals cannot complete. Add a trainee-scoped beneficial exception and test through `BandageContext.BeginHeal`; the new test's direct `horse.Heal` call bypasses this restriction.
- **medium** [P2] Preserve the mage demonstration before accepting completion (`server\customizations\Tutorial\NewHavenLessons.cs:138`)
  A player who immediately follows the casting instructions can finish Magery before the demonstration has shown two spells, potentially before its first projectile appears. `OnTargetDamaged` still finishes immediately, and `Return` deletes the demo and cancels its timer; nothing enforces the requested 10???15-second demonstration followed by the player's cast. Track the demonstration phase and defer completion until the required demonstration has been shown.
- **medium** [P2] Keep the untreated horse injured until it is bandaged (`server\customizations\Tutorial\NewHavenLessons.cs:586`)
  If the player waits several minutes after starting Animals, ordinary horse hit regeneration restores the horse to full health without setting `Healed`. `BandageContext.BeginHeal` then refuses treatment because the patient is undamaged, while `Tamable` remains false. The blood items are only decoration and do not prevent regeneration. Suppress regeneration or maintain an injury until the trainee actually treats the horse so waiting cannot strand the lesson.

(1.8 minutes, 839,580 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.99). The required fresh-character client proof is explicitly unfinished despite the DONE marker, and the test probe masks failures. This repository contains notes and supporting artifacts, so the separate server implementation was not verified in this review.

- **high** [P1] Complete the required player walkthrough before marking DONE (`notes\cc-P743-new-haven-tutorial-fixes.md:210`)
  The note explicitly defers the horse, bard fight and mage demonstration to a follow-up, and the screenshots use a teleported existing Tester rather than a fresh isle graduate. P743 requires proving each item in TazUO with a new character, including the Animals completion regression. Location screenshots and server facts do not establish that these player interactions work. Complete that walkthrough and attach its evidence before emitting DONE; [AGENTS.md:45???46](../../AGENTS.md#L45-L46) explicitly prohibits the completion marker before the work is finished because it triggers the Golem immediately.
- **medium** [P2] Propagate test failures through the probe pipeline (`notes\cc-P743-tools\probe743.sh:16`)
  When `dotnet test` fails but prints any non-warning output, `grep -v warning` succeeds, making the inner shell, Docker invocation and probe all return zero. This makes failed verification runs appear successful to callers. Enable `pipefail` inside the container's `bash -c` command or explicitly preserve the test exit status; setting it only in the outer script would not fix this pipeline. This recreates the failure-masking problem documented in [AGENTS.md:339???346](../../AGENTS.md#L339-L346).

(0.9 minutes, 426,536 tokens)
