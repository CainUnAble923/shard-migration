# Codex review: P288

CC task P288: the player package's 'What is new' line fills itself. Reviewed by Codex (`codex exec review`, read-only) after P288 DONE and before the Golem's commit, 2026-10-23 03:39.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The console autofill and refill wiring is present, but official Legion script changes can be omitted or incorrectly included. Runtime verification was blocked by PowerShell language-mode restrictions; the requested real-fill notes were not available in this work copy.

- **medium** [P2] Anchor script promotions to the package build time (`scripts\Shard-Console.ps1:9064`)
  If the published package was built after its source commit, this compares promotions against the commit timestamp rather than the published package's build time. For example, a script promoted between a morning commit and an afternoon package build is incorrectly advertised as new since that package, and remains advertised on subsequent refills. Use the published version's build timestamp for the promotion cutoff, independently of the resolved source commit.
- **medium** [P2] Compare promoted scripts rather than entire tagged dev trees (`scripts\Shard-Console.ps1:9068`)
  When Chase promotes only selected scripts, these tag diffs do not represent what became official. `Publish-LegionScripts.ps1` tags the entire dev commit, while its promotion accepts a subset of scripts. Two successive promotions from the same dev commit therefore produce an empty diff even when the second promotion changes players' scripts; conversely, different dev commits can report scripts that were never promoted. Use the actual promoted script selections or official manifest snapshots.

(1.9 minutes, 732,191 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.91). This repository's only change is the P288 notes file, which records the requested real fill, test results, deviations, and completion marker. No actionable defects were found in this documentation-only change; the console implementation and tests are in the separate code repository and were not verified here.

No findings.

(0.4 minutes, 92,986 tokens)
