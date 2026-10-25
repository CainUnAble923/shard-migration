# P592: achievements and loot boxes guide refresh

Updated October 25, 2026. Documentation only.

## Changes

- Refreshed `notes/wiki-drafts/achievements-and-loot-boxes.md` for P455: first-boss boxes work during ordinary kills. Explained eligibility, the per-character first reward for each boss type, and the exclusion of paragons.
- Added a general P457 update about corrected hidden achievement checks, without publishing hidden names, conditions, thresholds, or titles.
- Applied Chase's October 23 rule: publish no AP ceiling or title count, list visible titles by name, and keep hidden titles secret. Removed the old numeric title-count dispute.
- Updated sources and marked the boss-box, AP publication, and Renown spending disputes as resolved. Preserved the remaining planned features and unverified gear-strength comparison.

## Evidence reviewed

- `notes/cc-P455-death-hooks.md` and current code `server/customizations/LootBoxes/ClusterFLootBoxes.cs:86` (repeat handling), `:164` (boss eligibility), `:173` (ordinary death award path), and `:200` (boss-type source key).
- Existing regression case `server/tests/Misc/DeathHooksVerification.cs:126` exercises a player killing a boss through the game's death path. Read only; not rerun for this documentation change.
- `notes/cc-P457-noted-fixups-2.md` and current `server/customizations/ClusterFNotedBySystem.cs:680`, `:686`, `:842`, `:874`, `:974`, and `:1029` confirm the updated checks. The P457 review still flags the recycling loot exception; the guide makes no claim that every hidden achievement issue is resolved and gives no recycling instructions.
- `docs/feature-queue.md:2018` records Chase's October 23 answers. Item 6 at `:2027` settles AP/title publication; item 5 confirms the delivered shop.

## Validation and limits

- Reviewed the complete draft diff against the requested scope and source evidence.
- Checked relative Markdown links, absence of em dashes, file sizes below 5 MB, and whitespace with `git diff --check`.
- Lane tests: none, as requested. No tests added or changed; no build needed for prose edits.
- Only the requested draft and this task note changed. No code, `docs/`, progress artifacts, or other guides changed. No commits, branch changes, deployments, or Haven connections.
- Running-shard availability and configuration remain unverified. The draft retains that limitation.

P592 DONE
