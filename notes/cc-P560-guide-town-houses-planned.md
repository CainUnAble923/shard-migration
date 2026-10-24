# P560: Town Houses planned player guide

October 24, 2026. Documentation only. Nothing was published or deployed.

## Delivered

- [Town Houses (planned)](wiki-drafts/town-houses.md): a short player page clearly labeled coming later. Covers rentals and room sublets in towns, planned guard coverage, the account's one-house limit, and the exclusion of inn rooms and guild halls.
- [Task notes](cc-P560-guide-town-houses.md): the notes filename explicitly requested by the embedded task. This longer file is the notes destination requested by the lane handoff.

## Sources and decisions

- Read both work copies' root AGENTS.md files and the migration copy's direction-decision.md, tasks.md, and docs index. No docs directory was edited.
- [P409 design](cc-P409-town-houses-design.md), especially "In plain words," "How it plays," and "Open questions for Chase": source for the planned rental and sublet concept. Its suggested prices, periods, grace, storage, site counts, and room entitlements are proposals, not confirmed gameplay.
- [P542 handoff](cc-P542-cont-fixup-town-houses-design.md): restored the design without implementing the feature.
- Read Chase's calls directly in `D:/UO/overseer/decisions-2026-10-22.md:24-25`: native rentals and sublets approved, guarded towns allowed, counts as the account's one house, and F-44 inn rooms and F-49 halls excluded.
- [P550 review](cc-P550-review-town-houses-design.md), especially "Chase's calls versus the design": prevents carrying forward P409's inn example or presenting its proposed room-renter house exemption as settled. The guide promises no exemption for subtenants and no approved sale option.

The guide keeps player-facing language free of engine details. Prices, timing, locations, storage, room rules, purchases, and belongings recovery remain undecided or awaiting confirmation. No launch date is promised.

## Verification and limits

- Read the finished draft against the settled calls and the design's open questions. Reviewed for plain American English and no em dashes.
- Searched canonical `server/customizations` and `server/patches` for `ClusterFLeasehold`, `ClusterFLeaseSign`, `ClusterFLeaseholdRegion`, `TownHouse`, and `Leaseholds`; no matches. This is a name search, not proof about every possible implementation. No running-server availability or behavior was verified.
- No tests added or run, as specified by "Lane tests: none." No code or build changes require a Docker build.
- Ran `tools/progress.py --dry-run` successfully with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies. It unexpectedly rewrites `tools/progress.json` inside `build()` before checking the dry-run flag (`tools/progress.py:722`, `:732`, `:737`). Restored that generated file byte for byte from HEAD, leaving only the requested notes and draft. This is an existing reporting-tool defect, outside P560's scope; its unrelated status warnings do not establish Town Houses availability.
- Final formatting review found no em dashes or trailing whitespace in the three new Markdown files. Each is below 5 MB. Windows PowerShell reports version 5.1.26100.9711.
- No Haven connection, deployment, commit, merge, push, or branch switch. Code work copy remains unchanged.

P560 DONE
