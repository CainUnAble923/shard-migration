# Codex review: P673

CC task P673: plan the Siege of Sosaria swap (Trammel and Felucca) and re-site the Wakening Isle. Reviewed by Codex (`codex exec review`, read-only) after P673 DONE and before the Golem's commit, 2026-10-26 21:04.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.98). The plan substantially covers the requested re-site and swap work, but its package-gate assumption is false and its deployment ordering leaves known travel and region defects exposed.

- **medium** [P2] Include travel fixes and Felucca regions in the atomic swap (`notes\cc-P673-sos-swap-plan.md:420`)
  This go-live sequence exposes both swapped facets before S4 fixes destinations already identified as landing in walls, and leaves Felucca's regions unchanged until S13 in wave 4. Players can therefore use broken gates and encounter misplaced guard zones during the explicitly playable interval. Include S4 and S13 in the atomic deployment, or keep the affected travel and facet unavailable until they land. This also follows the working-shard invariant in [AGENTS.md:81-83](../AGENTS.md#L81-L83).
- **medium** [P2] Plan an explicit package-gate exception for the map asset (`notes\cc-P673-sos-swap-plan.md:161`)
  S1 ships `.uop` and `.mul` files, but `player-package/Build-PlayerPackage.ps1:463-469` rejects those extensions and EA filenames regardless of who supplied them. Gate 4 therefore cannot remain unchanged as stated: the proposed package would fail its build. Add a narrowly scoped, hash-verified exception and corresponding negative tests to S1, and revise the README claim to acknowledge the replacement map.

(2.8 minutes, 747,106 tokens)
