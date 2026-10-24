# P530: Clean Up Britannia design and build comparison

The full comparison is
[cc-P530-clean-up-britannia-design-vs-build.md](cc-P530-clean-up-britannia-design-vs-build.md),
in the Design item / Built or not / Where in code / Gap / Size table form. This
lane note preserves the wrapper's separate requested filename without duplicating
the report.

Compared F-3, the completed P33/P175 prompts and notes, Chase's October 22
decisions in queued P414/P415, and the P432 review with local main. Code snapshot:
`f2853e86ca96c89d8f97a6c3a17c9fd2661ad41d`. Notes snapshot:
`8a5ee4cf7e1a46313d25f68279569cb9c257f73f`. Both HEADs matched local main.

Built source includes character points and lifetime rank, shared valuation,
barrels/appraisal, the two-NPC store, owned trash bags, craft reject routing,
Civic Token retirement, magic-property premiums, and earned Fame-based corpse
value. Counted 122 active rewards against the ServUO reference's 134; all active
reference prices match. The report lists every omitted reward. P193 has since
added the human fishing-set pieces and hook, but their cleanup store rows are
still absent.

P414 is queued: stop producing bundles, track contract progress through points
earned after acceptance, retain existing rewards, redeem old bundles once, and
handle old contracts. P415 is queued: add single/nearby corpse menu targets for
any player, check owner/backpack and loot rights, warn about contents, reuse
actor-aware points, and produce no bundles. The report also carries P175's
disclosed limits and the unresolved P432 findings. P432's suggestion to remove
contract gold payouts conflicts with P414's prompt; P414's retained rewards are
the baseline used here.

No code, tests, or docs/ files changed. No lane tests or build were required or
run. No Haven connection, deployment, account action, commit, merge, push, or
branch switch. Commands used Windows PowerShell 5.1. Stop-request checks were
made between steps. Installed builds, saved-world state, client presentation,
and live behavior remain unverified.

`tools/progress.py --dry-run` completed with the two work-copy path overrides.
Its attempted progress.json write was suppressed in memory, and the original
file remained byte-identical. Global source counts were not used as coverage.

Final checks passed: citation paths and line bounds resolve, local Markdown
links resolve, table columns are consistent, and both notes are ASCII with no
em dashes or trailing whitespace. Both files are below 5 MB. Whitespace checks
passed in both repositories. The code work copy is clean; only these two new
notes appear in the migration work copy.

Both HEADs still match the measured local main refs. No stop-request file was
present at the final check. No P530 work remains.

P530 DONE
