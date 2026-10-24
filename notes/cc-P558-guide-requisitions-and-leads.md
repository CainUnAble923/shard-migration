# P558: Requisitions and Leads player guide handoff

October 24, 2026. The unattended wrapper names this note, while the enclosed brief names `cc-P558-guide-requisitions.md`. Both are supplied.

The player guide is [wiki-drafts/requisitions.md](wiki-drafts/requisitions.md). The detailed [work note](cc-P558-guide-requisitions.md) contains the source inventory, October 23 decisions, P452 change map, and verification limits.

The draft covers the personal board, turn-in procedure, intensity and slayers, tier gates and rewards, daily refresh, personal Leads and the 40-kill guarantee, and Appraiser locations and sales. It follows Chase's accepted behavior and marks all P452 fix areas as changing soon. Spellbook sales remain explicitly unpromised.

Only Markdown notes were added. No code or tests changed. No live service was contacted, and nothing was committed or deployed.

## Final checks

- Read the completed guide against the canonical source paths listed in the detailed note, including the default tier, reward, and Lead chance rows. Confirmed the ordinary spellbook constructor's blessed status directly in pinned ModernUO.
- All relative Markdown links in the guide and both notes resolve. All added files are UTF-8, contain no em dashes or trailing whitespace, and are below 5 MB.
- `git diff --check` completed cleanly in both work copies. The separate file inspection covered the newly added, untracked Markdown too.
- Code work copy remains clean. The migration work copy has only the guide and the two notes named above. Nothing under `docs/` changed.
- Ran `tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies. Exit 0. The reporter writes `tools/progress.json` even in dry-run mode; its starting bytes were saved in memory and restored afterward, leaving no unrelated snapshot change.
- Lane tests: none. No new tests or gates were added. Live settings, placement, deployment, and client behavior remain unverified.
- The stop-request file was absent at the final step boundary.

P558 DONE
