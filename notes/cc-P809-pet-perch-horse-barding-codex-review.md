# Codex review: P809

CC task P809: pet perches and horse barding. Reviewed by Codex (`codex exec review`, read-only) after P809 DONE and before the Golem's commit, 2026-11-07 11:03.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.95). The implementation largely satisfies the requested features, with supporting notes, screenshots, and reported build results. However, null configuration handling breaks perch placement, and normal crafting cannot populate the implemented maker attribution. I inspected the source and artifacts but did not independently rerun the Docker build.

- **medium** [P2] Reject a null pet-kind list during configuration validation (`server\customizations\Pets\PetPerch.cs:72`)
  If `pet-perch.json` contains `"Kinds": null`, validation silently accepts it because this loop substitutes an empty collection. The accepted settings retain the null value, however, and `Takes()` subsequently throws when anyone targets a creature for placement. Reject null during validation so the existing fallback-to-defaults behavior handles this invalid configuration.
- **low** [P3] Register horse barding as eligible for a maker's mark (`server\customizations\Pets\HorseBarding.cs:312`)
  When a GM smith crafts exceptional horse barding, `CraftItem.IsMarkable()` returns false: its fixed markable-type table includes `DragonBardingDeed`, but not this new Item-derived type. Consequently, the crafting pipeline always passes `makersMark = false`, making this attribution branch and the crafted-by tooltip unreachable through normal crafting. Integrate the type with the marking eligibility check and cover that path in a test.

(2.9 minutes, 1,013,675 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.76). No actionable defects found in this repository???s new notes, proof artifacts, and helper scripts. The server implementation, patches, tests, changelog, and version bump are in the separate code repository, so their correctness and full task compliance remain unverified by this review.

No findings.

(0.7 minutes, 304,889 tokens)
