# cc-P291: the tutorial's wing trials, part 2 (trades, animals, bard, thieving, non-skill wings): not started, waiting on P289

2026-10-23. Prompt: `D:\UO\cc-prompts\claimed\Iron\cc-P291-tutorial-wing-trials-trades-and-more.md`, handed by the
Golem to the Iron Golem. Work copies on branch `golem/Iron/P291`, both clean.

## In plain words

- Nothing was built. The gathering, crafting, animal, bard, thieving and tour trials have to sit on top of P289 (the
  tutorial's core trials and where every station is placed), and P289 has not been merged yet.
- P290 (part 1 of the wing trials) stopped for the same reason this morning.
- P291 can go again after P289 is merged into main. Nothing for you to do unless you want P289 to run sooner.

## For Chase

The prompt says: "Run after P289 is in main; if it is not, stop with `P291 STOPPED: waiting on P289`." I checked:

- `D:\UO\cc-prompts\queue\cc-P289-tutorial-core-trials-playable.md` is back in the queue (not completed).
- `git ls-remote origin refs/heads/main` gives `fbebe83` (the P288 merge) in shard-migration and `4c2af57` in
  ShatteredLegacy. No commit on either main mentions P289.
- P289 exists only as unfinished work: branches `golem/Iron/P289` (WIP commit `dc21ef4`, tool logs and a fixes patch)
  and `golem/Valorite/P289` (Codex hand-off notes, stopped for lack of Docker). Neither is merged.

Order that unblocks the tutorial: P289, then P290 and P291 (these two touch different trials and could run side by side).

No files were changed in either repo besides this note.

P291 STOPPED: waiting on P289
