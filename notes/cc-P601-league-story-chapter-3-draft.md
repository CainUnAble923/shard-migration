# P601: League story Chapter 3 draft handoff

October 25, 2026. Draft for Chase to edit.

The playable draft is [League Chapter 3: One More Victory](cc-P601-league-chapter-3-draft.md), the filename requested in the task body. This handoff uses the separate notes filename requested by the lane wrapper.

The draft follows the Verite chapter in `docs/league-storyline.md`: a private Doom Gauntlet trial, the Crossguard holding its dead to a circuit, the reveal that the pieces feed on every reset, and release for this party when the piece is taken. It includes setting, playable beats, NPC dialogue, a single short story rewind, solo and party encounter proposals, the blade-piece reward, retry handling, and six nonblocking editing questions for Chase. It reserves the Unbound, the unlooped-world vision, and the permanent choice for later chapters.

Both work copies' AGENTS.md files were read, along with the direction decision, task list, P593 draft, handoff and review, League storyline, relevant F-24 decisions, and source details cited in the draft. The draft keeps P593's practical Registrar, ordinary human details, short dialogue, explicit objectives, and separation of proposals from verified source facts.

New story details and mechanics are proposals. Exact map placement, instance isolation, encounter balance, duration, effects, travel, reconnect behavior, and reward persistence remain unverified. No live shard or client behavior was inspected.

Scope: two Markdown notes only. No code or `docs/` edits, new art dependency, Haven connection, deployment, commit, push, merge, or branch change. Lane tests are none; no tests are needed or added for this prose-only task.

Review completed: checked the draft against Chapter 3's feeding reveal, the later chapters' reserved reveals, private-map and solo-or-party rules, and the chapter-waiver decision. Both notes use plain American English and contain no em dashes. Both are below 5 MB. The code work copy remains clean; the migration work copy contains only these two new notes. No tests were added or run, as specified by this prose-only task.

`python tools/progress.py --dry-run` completed successfully with `SL_SHARD` and `SL_MIGRATE` pointed at these work copies. As already recorded by P593, the tool writes `tools/progress.json` during `build()` before checking the dry-run flag. The command preserved the original snapshot bytes and restored them afterward; byte equality was confirmed. No generated progress change remains, and no tool fix was made in this writing task.

P601 DONE
