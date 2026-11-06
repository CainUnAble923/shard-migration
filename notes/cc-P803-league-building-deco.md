# cc-P803: New Haven League building: replace the bulletin board and a full decoration review

## In plain words

- **Nothing has changed in the game yet.** The League building's board and decoration work has not started.
- **Why:** the prompt says to wait until P799 has merged, because the release version must be built on top of it. P799 and its last fix-up, P814, are not on main or the release branch yet.
- **For you:** pick A or B on the Golem card or by email. A starts now on top of P814's finished release diff, which I recommend. B waits for the merge.

## State

Iron Golem, 2026-11-06. No code or map changed, no build run, and no lock taken.

Checked at 10:12:

- `origin/main` is `08b4d3f`, without P799, P806 or P814.
- `release/isle-20261028` is `5816efe`, without P799's port.
- `golem/Iron/P814` is pushed and not on main. It has no build review file yet in the merge queue.
- P814's release diff (`notes\cc-P814-tools\p814-release-isle-20261028.diff`, on the P814 branch) holds P799's port, and `sl-modernuo:cc-p814-isle` built green.

P803 STOPPED: asked Chase (Iron-P803-20261106-101223-c38c)
