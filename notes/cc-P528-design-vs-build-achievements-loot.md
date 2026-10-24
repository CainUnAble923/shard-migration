# P528: achievements and loot design compared with the build

The full comparison is
[cc-P528-achievements-loot-design-vs-build.md](cc-P528-achievements-loot-design-vs-build.md),
using P515's Design item / Built or not / Where in code / Gap / Size table form. This
lane note uses the wrapper's separate filename so both requested paths are present without
duplicating the report.

Compared F-40/F-41, the accessory specifications, P263, and P231 with local main code
`f2853e86ca96c89d8f97a6c3a17c9fd2661ad41d`. The design/notes snapshot was
`99f25629d390acc690296e2cd8edc168a4338523`. Both work-copy HEADs matched local main.
Remote main and the running shard were not checked.

The report distinguishes implemented event hooks and rewards from uncalled hooks,
placeholders, deliberately deferred work, and correctness findings still present in source.
Main gaps are boss-box delivery, later-loop achievement replay, accessory loop and companion
integration, real reward sources, scroll combination, and features waiting for player
progression, chapter completion, or commission expiry. Existing achievement, accessory,
and flying-loot reviews are retained as follow-up evidence rather than treated as fixes.

Chase's October 23 League answers are respected: no AP ceiling or title count is published,
hidden titles stay secret in player guidance, the existing box bands stay, and the shop is
recognized as delivered. The internal tables are not a player wiki. The later recycling
ownership answer in queued P457 is also carried forward.

No code, tests, or docs/ files changed. No lane tests or build were required or run.
No Haven connection, deployment, account action, commit, merge, push, or branch switch.
Commands used Windows PowerShell 5.1. Stop-request checks were made between steps.

`tools/progress.py --dry-run` exited 0 using the work-copy path overrides. Its generated
`tools/progress.json` was immediately restored and verified byte-identical. Global source
counts were not used as feature coverage.

Final checks passed: source paths and cited line numbers resolve, Markdown links resolve,
table columns are consistent, and both notes use ASCII with no em dashes or trailing
whitespace. Both files are below 5 MB. Whitespace checks passed in both repositories.
The code working tree is clean, and only these two new notes appear in the migration
working tree. Both HEADs still match their measured local main refs. No stop-request file
was present at the final check. No work remains in this docs-only task.

P528 DONE
