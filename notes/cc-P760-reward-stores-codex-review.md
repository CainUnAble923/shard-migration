# Codex review: P760

CC task P760: reward stores (guild and society, event tokens, achievements, a bigger League shop). Reviewed by Codex (`codex exec review`, read-only) after P760 DONE and before the Golem's commit, 2026-11-01 18:39.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.96). The four store types are substantially implemented, with approval and verification evidence in the companion notes. However, token attribution, missing League price configuration, and malformed-configuration handling need correction. Tests were not rerun during this read-only review.

- **medium** [P2] Reject null price rows without throwing (`server\customizations\RewardStores\RewardStorePrices.cs:172`)
  A configuration such as `{"rows":{"ap.robe":null}}` deserializes successfully but throws `NullReferenceException` here. Neither `Apply` nor the startup loader catches that exception, so this bypasses the promised whole-file refusal and can abort startup instead of retaining the active prices. Validate that each row is non-null and report it through the existing error list.
- **medium** [P2] Include League rows in the configurable price table (`server\customizations\RewardStores\RewardStorePrices.cs:49`)
  The approved plan promises that every store's placeholder prices, including the League additions, can be retuned through `reward-stores.json`. This enumeration excludes the League shop, so its rows are absent from the generated file and rejected as unknown if added manually; their prices and AP requirements remain hardcoded. Keeping the existing League implementation is compatible with the plan, but its pricing still needs to consult the shared configuration.
- **medium** [P2] Aggregate damage by player before choosing the token recipient (`server\customizations\RewardStores\FestivalStore.cs:150`)
  When a player splits damage between themselves and pets, this selects the largest individual damage entry rather than the player responsible for the most damage. For example, 300 player damage plus 300 pet damage loses to another player's 400 damage. Pinned ModernUO's `FindMostTotalDamager` does not aggregate masters' contributions. Aggregate player-attributed damage before selecting the winner so Festival Tokens reach the intended recipient.

(3 minutes, 1,751,032 tokens)

## shard-migration

Verdict: patch is correct (confidence 0.8). No blocking defects found in this repository???s new plan, implementation notes, proof scripts, or screenshots. This verdict covers the docs-repo changes only; the server implementation and its tests are outside this diff and were not independently verified.

No findings.

(0.8 minutes, 352,275 tokens)
