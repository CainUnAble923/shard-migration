# Codex review: P795

CC task P795: the Drover's Handbook (Herding spellbook). Reviewed by Codex (`codex exec review`, read-only) after P795 DONE and before the Golem's commit, 2026-11-05 08:23.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Not reviewed: timed out after 6 minutes.

## shard-migration

Verdict: patch is incorrect (confidence 0.95). The new verification helper masks failures and bypasses the required build route. The recorded final gated build succeeded, but the server implementation is outside this repository's changes and was not independently reviewed here.

- **medium** [P2] Preserve build and test failures in the verification helper (`notes\cc-P795-tools\run-facts.sh:16`)
  If compilation or a test fails, this helper can still exit successfully: the pipelines discard `dotnet` exit statuses, the inner shell continues after failed builds, and the final `head` normally returns zero. Failed compilation can also leave `--no-build` testing assemblies inherited from the builder image rather than the changed code. Route verification through the task-required `build.sh` and propagate its failure status instead of introducing this alternate route. This also undermines the failure-confirmation requirement in [AGENTS.md:339???343](../../AGENTS.md#L339-L343).

(1.2 minutes, 283,607 tokens)
