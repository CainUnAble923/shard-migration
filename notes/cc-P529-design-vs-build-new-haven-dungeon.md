# P529: New Haven dungeon design and build comparison

The full comparison is
[cc-P529-new-haven-dungeon-design-vs-build.md](cc-P529-new-haven-dungeon-design-vs-build.md),
in the Design item / Built or not / Where in code / Gap / Size table form. This
lane note preserves the wrapper's separate requested filename without duplicating
the report.

Compared P24, Chase's dungeon decisions, revised P36, F-45 and the Rootdeep
creature/Vault work, P188, and queued P413 with local main. Code snapshot:
`f2853e86ca96c89d8f97a6c3a17c9fd2661ad41d`. Notes/design snapshot:
`8512bdb0ff5d2161e329b23446e8a4ba4ef1a491`. Both HEADs matched local main.

Built source includes the map patch and delivery path, single-hole entrance,
regions, bestiary, materials, scripted Vault drops, crawlway, floor traps, and
trap lesson. Gaps include the larger P413 entrance, choppable Rootwood targets,
Brood Pit mini-champion wiring, puzzle/chamber integration, dungeon set pieces,
part-consuming upgrades/recipes, and the repeatable replacement quest. The report
also carries unresolved map-failure, seeder-upgrade, Vault-recovery, reinforcement,
crafting, and runtime-proof findings from existing reviews.

No code, tests, or docs/ files changed. No lane tests or build were required or
run. No Haven connection, deployment, account action, commit, merge, push, or
branch switch. Commands used Windows PowerShell 5.1. Stop-request checks were
made between steps. Installed maps, published package, saved-world contents, and
live play remain unverified.

`tools/progress.py --dry-run` completed with the two work-copy path overrides.
Its attempted progress.json write was suppressed in memory, and the original
file remained byte-identical. Global source counts were not used as coverage.

Final checks passed: citation paths and line bounds resolve, local Markdown links
resolve, table columns are consistent, and both notes are ASCII with no em dashes
or trailing whitespace. Both are below 5 MB. Whitespace checks passed in both
repositories. The code work copy is clean; only these two new notes appear in the
migration work copy. Both HEADs still match their measured local main refs. No
stop-request file was present at the final check. No P529 work remains.

P529 DONE
