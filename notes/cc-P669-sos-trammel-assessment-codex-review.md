# Codex review: P669

CC task P669: impact assessment, replacing stock Trammel with the Siege of Sosaria map. Reviewed by Codex (`codex exec review`, read-only) after P669 DONE and before the Golem's commit, 2026-10-26 17:31.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.99). The assessment provides substantial map measurements and useful comparisons, but its server-impact inventory double-counts expressions, assigns placements to incorrect facets, and misses important placement formats. Those defects undermine the reported rework counts, and the requested notable-place render set remains incomplete.

- **medium** [P2] Include placements outside the supported coordinate patterns (`notes\cc-P669-tools\geo.py:111`)
  The inventory misses substantial requested content: TutorialCorePlacement's `Ground(3402, 2617)` and other death/healer/gate locations never match, and ClusterFNewHavenServicesSeeder's large `new("MetalDoor ...", x, y, z)` decoration table is reduced to one point. Bot calls such as `move_player(a, p, 3512, 2581, 14)` are also omitted. The assessment nevertheless claims to have counted these placements and specifically grades the missing tutorial spots. Extend the extraction and manually reconcile the required categories before regenerating the assessment; [AGENTS.md:61???65](../../AGENTS.md#L61-L65) requires counting the artifacts rather than treating keyword candidates as results.
- **medium** [P2] Supply renders for the remaining notable settlements (`notes\cc-P669-sos-trammel-assessment.md:52`)
  The task requests a client-style render of each notable new or moved place, but the delivered picture set omits Elmhaven, Kettleburg, Elandrim Nur Shaz and Fort Yondall. Fort Yondall is even recommended as one of the first four pieces to lift, without a picture for Chase to evaluate. Complete the settlement/keep survey and add the missing renders and index entries before presenting the recommendation as finished.
- **medium** [P2] Count each coordinate expression only once (`notes\cc-P669-tools\geo.py:136`)
  Explicit `new Point3D(x, y, z)` expressions match both the first pattern and the bare-tuple pattern, so the collector counts them twice. The published 813 rows contain 308 repeated `(source-line, x, y)` rows; for example, TutorialCorePlacement's three station expressions are each duplicated. This inflates the impact totals and the counts used to estimate rework. Deduplicate overlapping matches and regenerate the outputs and assessment, consistent with [AGENTS.md:61???65](../../AGENTS.md#L61-L65).
- **medium** [P2] Resolve the facet of each placement rather than each file (`notes\cc-P669-tools\geo.py:128`)
  Searching the entire file, including comments, assigns unrelated coordinates to Trammel/Felucca. For example, EodonGeneration's Ter Mur gate and vines become nine `ours (both)` entries because its comments mention both facets; StealableArtifacts' Malas and Ter Mur entries are likewise graded against Trammel. Consequently, the claimed 467 shared coordinates and associated rework counts are not a geography inventory. Resolve each placement's actual map and exclude unrelated patch context before publishing these totals, as required by [AGENTS.md:61???65](../../AGENTS.md#L61-L65).

(2.5 minutes, 970,105 tokens)
