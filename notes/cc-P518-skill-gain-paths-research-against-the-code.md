# P518: skill gain paths research against the code

The requested per-group comparison is [cc-P518-skill-gain-paths-vs-code.md](cc-P518-skill-gain-paths-vs-code.md), the filename specified in the task body. This run note occupies the separate filename specified in the Golem handoff.

The comparison checks P283 against current canonical skill gain code, P191, and its P202/P204 integrations, with pinned ModernUO source references. It retains the historical 23 served / 16 open skill partition and the additional three bard follow-ups, and qualifies Focus regeneration when positive skill gear exhausts its direct gain chance early. P443's review findings are not repeated.

Code HEAD: `6f540be8b84f63f76b8852fe638039b363b66a6b`. Notes HEAD at entry: `668b31b751198e926e2507cff679c70cac87f00b`. Pinned ModernUO: `d4531cd94b739613155225c234900de9f47d2c88`.

Research only. No code, docs directory, live settings, saves, or services changed. No Haven connection, deployment, commit, merge, push, or branch switch. Existing tests were read, not run; lane tests are none and no new tests were written. Runtime limits are explicit in the comparison.

Validation: counted 58 unique table entries and the named 23/16 partition; checked local links, cited source file existence, formatting, and note sizes. No em dashes. Progress reporter --dry-run exited zero with work-copy overrides; restored its progress.json side effect byte for byte. Final scope is these two notes only. Stop requests were checked between steps.

P518 DONE
