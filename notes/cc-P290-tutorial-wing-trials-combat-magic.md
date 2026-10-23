# cc-P290: the tutorial's wing trials, part 1 (combat, healing and magic): not started, waiting on P289

2026-10-23. Prompt: `D:\UO\cc-prompts\claimed\Iron\cc-P290-tutorial-wing-trials-combat-magic.md`, handed by the Golem
to the Iron Golem. Work copies on branch `golem/Iron/P290`, both clean.

## In plain words

- Nothing was built. The combat and magic trials have to sit on top of P289 (the tutorial's core trials and where
  everything is placed), and P289 has not run yet.
- P290 can go again after P289 is merged into main. Nothing for you to do unless you want P289 to run sooner.

## For Chase

The prompt says: "Run after P289 is in main; if it is not, stop with `P290 STOPPED: waiting on P289`." I checked:

- `D:\UO\cc-prompts\queue\cc-P289-tutorial-core-trials-playable.md` is still in the queue (not claimed or completed).
- `git ls-remote origin refs/heads/main` gives `72f410f` (the P287 merge), the same as local main. No commit on main
  mentions P289, in either repo; I fetched origin main for both to check.
- No P289 notes in `notes\`. The only other P289 file is a superseded fix-up under `_superseded\`.

No files were changed in either repo besides this note.

P290 STOPPED: waiting on P289
