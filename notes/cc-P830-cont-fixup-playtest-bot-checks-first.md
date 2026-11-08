# CC task P830: fix-up for P223 (the play-test bot's first-half checks did not merge)

## In plain words
- P223's batch of new play-test bot checks can now go into main. They clashed with P224's batch, which merged first, because both had added the same helpers (skills, spells, right-click menus) to the bot in slightly different ways.
- The bot now has one shared set of those helpers that both batches use. All 118 checks load with no duplicate names, and the bot's 77 unit tests pass.
- P223 found a bug where `[RemoveStealArties` breaks after someone steals an artifact. It is now **D98** on the bug list. P223 had called it D96, but P224 had already used D96 and D97.
- Nothing for you to do.

## Headlines
- Both repos are on `golem/Gold/P830`, which was main (ShatteredLegacy `a2956ad`, shard-migration `5d1a17ba`). I merged `golem/Gold/P223` into it instead of checking out P223, because the hand-off says not to switch branches. The result is the same: P223's work merged with main, ready for the integrator.
- No changes under `server\` or `docker\uo\`, so no Docker build was needed.
- Tests: `python -m unittest discover -s tests` in `tools\playtest-bot`: 77 of 77 OK (P223 had 42; main has added more since). `python -m compileall` is clean. Importing `uobot.checks` and `uobot.run` registers 118 checks with no duplicate ids.
- I did not run a live bot night here. This is a merge fix-up, and no check's logic changed beyond the shared helpers below.

## Conflicts resolved
ShatteredLegacy, `tools/playtest-bot/uobot/`:
- **packets.py**: both sides added `use_skill`, `cast_spell`, `context_menu_request`, a context-menu reply and `parse_context_menu`. They send the same bytes. Kept one copy of each. They are built on P223's `text_command`. P223's `weapon_ability` is kept. The reply is `context_menu_response` (P224's name), with `context_menu_select = context_menu_response` so P223's calls still work. The one `parse_context_menu` gives each entry its cliloc under both `"cliloc"` (P224's checks read this) and `"number"` (P223's checks read this). I removed P223's second, non-conflicting copy of the parser, which would otherwise have overridden it.
- **client.py**: kept HEAD's 0xBF 0x14 handler (it also keeps P224's 0xBA quest-arrow branch) and its `context_menus` list. `self.menus` is now the same list object, so P223's `menu_pick` and `menu_click` still see the menus. I removed P223's duplicate `Client.context_menu` method. Git had auto-merged it in, and it would have silently replaced P224's. Both return the same dict. P223's flags/effects/0xA1 handling, `use_skill`, `gump_rows` and `row_at` are kept.
- **checks.py**: for the patch-history page walk, I kept P224's version, which reads the "Page x of N" counter (cap 400). It also fixes the problem P223 hit with its flat 200. I import both `checks_p223` and `checks_p224` at the end.
- **run.py**: for deleting a character when the account is full, I kept P224's version, which waits for the slot to actually empty and fails clearly if it does not. P223's version did the same thing with a fixed 2-second sleep.

shard-migration:
- **docs/bug-list.md**: both sides had added a new row called D96. P224's D96 (Visual Builder undo) and D97 (Start-TestShard address) stay. P223's `[RemoveStealArties` row becomes **D98**. The "next free" header now says D99 and explains the renumbering. I checked that D98 was not used anywhere else in `notes`/`docs` text.
- **notes/cc-P223-playtest-bot-checks-first.md**: changed D96 to D98 throughout, including its draft fix prompt, so the notes match the bug list.
- `testing/bot-triage.md` and `testing/playtest-steps.json` merged without conflicts.

P830 DONE
