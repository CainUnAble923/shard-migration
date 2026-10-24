# P561: wiki drafts cross-check, round 3

October 24, 2026. Documentation-only review in the Golem's Valorite-tower work copies.

Read both work-copy AGENTS.md files, the direction decision, task list, prior cross-check and task notes, the requested new drafts, canonical customizations and patches, player-package sources, relevant wiki source pages, pinned ModernUO, and the recorded October 22 Town Houses decisions. No generated server/uo tree was read. Initial worktrees were clean. Code HEAD: `1c9c5d8bbf9ab4d9a8dd288aace3afff549479dd`; notes HEAD: `21d5e1c0a539d20b7e2a475fa4852223a14b0265`; pinned upstream: `d4531cd94b739613155225c234900de9f47d2c88`.

Deliverable: [round 3 cross-check](wiki-drafts/cross-check-2026-10-24b.md). Its inventory lists every requested topic and each new player-guide input. Town Houses has design and review notes, not a player draft; it is reviewed in that form. The report supplies specific source-backed corrections and marks live/package/client assumptions unverified.

The new mining, cleanup, Register, and requisition guides mostly agree with current source. Older wiki pages still promise bundle creation, material-based ore orders, and outdated Register behavior. P452's requisition warnings remain current. The launcher guide must retain its distinction between a rebuild timeout and total launch time; its usual-speed claim is unmeasured. The companion guide needs an explicit test-world qualifier and a conditional town-vet location. P550's Town Houses design concerns remain relevant and are not accepted implementation rules or shipped guarantees.

Only review notes are being added. No draft, code, wiki source, configuration, accounts, saves, services, or file under docs/ was edited. No Haven connection, deployment, download, commit, merge, push, or branch switch occurred. No lane tests apply; no tests or gates were added, so no red/green cycle applies. Runtime behavior, active settings, publication, and shared-world placement were not verified.

The task wrapper requests this longer note filename, while the embedded brief requests [cc-P561-wiki-cross-check-3.md](cc-P561-wiki-cross-check-3.md). Both are supplied, following P539's convention.

Ran `python tools/progress.py --dry-run` with `SL_SHARD` and `SL_MIGRATE` pointing to these work copies: exit 0. It reported shard version `2026.10.24.10`; its broader status and content figures are not certified by this review. The tool writes `tools/progress.json` despite dry-run mode. Preserved the original bytes in memory and restored that incidental write exactly, leaving no generated change. Windows PowerShell was confirmed as version 5.1.

Final document checks passed: all six player-guide inventory links appear once, local Markdown links resolve, explicit source paths and line anchors exist, final newlines are present, and no em dashes or trailing whitespace were found. Each new file is below 5 MB. Git whitespace checks passed in both work copies. The code work copy remains clean; the notes work copy contains only the report and these two task notes. Stop-request checks remained absent. All requested review work is finished; publication and later implementation checks are explicitly outside this documentation task.

P561 DONE
