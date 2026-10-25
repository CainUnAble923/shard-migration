# P616: League story Chapter 4 draft handoff

October 25, 2026. Draft for Chase to edit.

The playable draft is [League Chapter 4: The Last Morning](cc-P616-league-chapter-4-draft.md), the filename requested in the task body. This handoff uses the separate notes filename requested by the lane wrapper.

The draft follows the Blaze chapter in `docs/league-storyline.md`: a race into a private Ice Dungeon trial, the Blade in the deepest ice, the Unbound as former League members willing to end Britannia to end its prison, their leader's history with Elara, and the Blade's vision of a quiet, empty world that ended. It includes setting, playable beats, dialogue, the fourth piece, solo and party handling proposals, and six nonblocking editing questions for Chase.

The voice follows P593 and P601: practical dialogue, ordinary personal details, readable objectives, and clear separation between proposed scenes and implemented behavior. This chapter uses a race and a vision with no required story rewind. The vision shows the cost of ending the loop outright, without claiming that Chapter 5's Sunder outcome destroys the world. The permanent choice, titles, cosmetics, and lasting effects remain in Chapter 5; the Point and Setting reveals remain reserved.

Both work copies' AGENTS.md files were read, along with the direction decision, task list, P593 and P601 drafts, handoffs and reviews, League storyline, relevant F-24 decisions, and the Registrar and rank source details cited in the draft. New characters, their shared history, the cutting frame, specific vision scenes, and mechanics are proposals. Exact placement, instance isolation, balance, duration, effects, travel, reconnect behavior, party handling, and reward persistence remain unverified. No live shard or client was inspected.

Scope: two Markdown notes only. No code or `docs/` edits, new art dependency, Haven connection, deployment, commit, push, merge, or branch change. Lane tests are none; no tests are needed or added for this prose-only task.

Review completed: checked the draft against Chapter 4's required reveals, the earlier drafts' continuity, Chapter 5's reserved choice and continuing-loop outcomes, private trial maps, solo-or-party access, and F-24's rank and waiver decisions. Both notes use plain American English, contain no em dashes, have working relative file links, and are below 5 MB. The code work copy remains clean; the migration work copy contains only these two new notes. No tests were added or run. The stop-request file was absent at the checks between steps and after review.

`python tools/progress.py --dry-run` completed successfully with `SL_SHARD` and `SL_MIGRATE` pointed at these work copies. As recorded by P593 and P601 and confirmed in the tool source, `build()` writes `tools/progress.json` before the dry-run flag is checked. The original snapshot bytes were preserved and restored afterward; byte equality was confirmed. No generated progress change remains, and no tool fix was made in this writing task.

P616 DONE
