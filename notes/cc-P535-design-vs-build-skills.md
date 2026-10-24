# P535: skills design against the build

The full requested comparison is [cc-P535-skills-design-vs-build.md](cc-P535-skills-design-vs-build.md). This file uses the outer prompt's notes filename; the report uses the task body's filename.

Main contains P191's two-attempt, onefold-amount defaults and the shared gain/material hooks. P283's higher training content and P282's player progression are not implemented by those defaults. The report also compares the broader skills mastery rewards and preserves later decisions that refine the October 2 design. It distinguishes missing content from conditional paths, older proposals, and unverified details.

Read both work-copy AGENTS.md files first, followed by the required direction/task guidance. Checked the skills passdown and design, P191 and its integration records, P283, P282, later skill decisions, relevant prior comparisons, canonical customizations, registered patches, existing tests, and pinned ModernUO.

No code or configuration changes, docs/ edits, Haven connection, deployment, commit, merge, push, or branch switch. No tests added or run; lane tests none. No new art is requested. Stop requests are checked between steps. Final validation is recorded below before completion.

Validation used Windows PowerShell 5.1.26100.9711 and local Python. The training table was compared with the actual pinned SkillName enum: all 58 entries appear exactly once, with display-name aliases resolved and no missing or extra skills. The report cites the enum file and lists the skill membership in its table; this is a coverage check, not a count of completed features.

Checked every explicit C/, P/, T/, and U/ source reference for file existence and cited line bounds. Checked local Markdown links, four-column table structure, plain American English, absence of em dashes, trailing whitespace, and file sizes. Both notes are below 5 MB. Reviewed later decisions separately from the original design, including the metal ladder, school content gate, Imbuing rework, effect bounds, and current map behavior. Runtime and incomplete source-audit limits are stated in the report.

Ran tools/progress.py --dry-run with SL_SHARD and SL_MIGRATE pointing to these work copies and SL_SERVUO pointing to the read-only reference. It completed successfully. Suppressed only its known incidental tools/progress.json write in the invocation, leaving no generated-file changes. No reporter inventory total is used as evidence for a completed skill path.

Final scope checks found the code work copy clean and only the two requested new notes in the migration work copy. git diff --check passed in both work copies; the new notes also passed direct whitespace checks. The stop-request file was absent at the final review. Completion markers are added only after this review.

P535 DONE
