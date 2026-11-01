# cc-P753: continue P750: the live shots of the guild headquarters on the Siege of Sosaria land

## In plain words

- **The in-game pictures are taken and the P750 moves show.** At Fort Viridian, the Rangers' guildmaster and a player
  both show in the fort's open inner court. The League's sign at Valunstead keep and the Tinkers' sign at Hammerhill
  both show beside their doors.
- **The Custodians' travel stop in Hammerhill moves up onto the hall's front step.** At the old spot on the street
  (1560,974), a player arriving was completely hidden behind the house across the lane. The stop is now the top step
  at the hall's south doors (1561,973), where you see yourself arrive next to the hall's sign.
- **The Tinkers' travel stop stays.** A player there shows; only his legs are behind a low wall.
- **For you:** nothing to try or deploy. One small thing to know: the Smiths' forge at Serpent's Hold (already on
  your list from P708) also makes a second `[ClusterFGuildHalls place` say "placed 1 thing" when it placed nothing.

## The shots (`notes\cc-P753-review\`)

How they were taken: P750's `run-shots750.ps1`, then this task's copy `notes\cc-P753-tools\run-shots753.ps1`. Each run
used a private shard on 2596 (a fresh copy of the bot world), the `test-shard` lock (taken and released each time) and
the `sl-modernuo:cc-P750` image. The new stop was shot on `sl-modernuo:cc-P753`.

| Check | Shot | Seen |
|---|---|---|
| Rangers' guildmaster, Fort Viridian (1002,985) | `rangers-guildmaster-player.jpg` | The Tester (999,989, white robe) and the cloaked Outriders guildmaster both stand in the inner court. Nothing is drawn over either. |
| League sign, Valunstead keep (567,321,18) | `league-sign-player.jpg` | The brass board shows on the gate tower's south face, right of the keep's steps. The Tester (562,324) is on the steps' west side. |
| Tinkers' sign, Hammerhill (1494,1025,8) | `tinkers-sign-player.jpg` | The board hangs on the workshop's east wall, beside the red double door, and shows. |
| Tinkers' stop (1495,1023,5): model 42% | `tinkers-sign-player.jpg` | **He shows.** His head and body are clear, and his legs are behind the low rubble wall in front of him. The model's 42% is about that lower half, so it reads right here. A player at the stop is easy to see. **No move.** |
| Custodians' stop (1560,974,5): model 100% | `custodians-stop-player.jpg` | **Hidden.** The middle of the view, where he stands, shows only the corner pillar and wall of the house south of the lane. **Moved** (below). |
| The new Custodians' stop (1561,973,7) | `custodians-stop-new-player.jpg` (image cc-P753) | He shows whole, on the top step at the south doors, with the Custodians' sign beside him. |
| `place`'s reply | `proof-log.txt` | See below. |

The admin shots (`*-admin.jpg`) only show the Golem's Admin standing where he logged out. They are kept because the
runner takes them, but they show nothing for these checks.

### `place`'s reply in the log

- **The first `place`:** "Guild halls done: placed 44 thing(s), 0 already standing." Each hall has its own "placed ..."
  line. The Rangers' line ends "the OutridersGuildmaster at (1002, 985, 0)".
- **No old-site line, as expected.** The bot world was never placed with P708's table, so there is no old site to
  clear. The line that P750 split off ("took away from its old site ...") is still covered only by P750's code facts
  3 and 5. They ran green again in this task's gated build.
- **The second `place`** (the `replace-again` scene) adds nothing to the halls: "placed 1 thing(s), 43 already
  standing". The one thing is the Smiths' forge decor at Serpent's Hold:
  - its row is refused ("Nothing was placed"), but the hall's line still reads "placed decor smiths/forge (5
    piece(s))" and counts it, on the first `place` and the second alike;
  - this is P708's known forge refusal (excluded by the prompt). It is noted here only because it makes "the second
    place adds nothing" read as 1.

### The first try, and the runner change

On P750's runner, the windows TazUO opens at login covered the middle of the game view, which is where the Tester
stands: the patch-notes bulletin, the paperdoll and the quest popup (`first-try\rangers-guildmaster-player.jpg`).

`notes\cc-P753-tools\shots753.ps1` (a copy of `shots750.ps1`) changes three things:
- it moves the game view to x 540, right of those windows;
- it drops the saved paperdoll (`gumps.xml`);
- it seeds the proof shard's profile ("Shattered Legacy P750 proof") from the TEST one. The client keeps a profile per
  server name and made a fresh one with default settings on first login, so the second try's view did not move until
  the third run.

`run-shots753.ps1` takes `-Spec`, `-Image` and `-Out`.

## The Custodians' stop

- **The measure:** a new docs fact 6 in `tools/tests/test_guild_hqs_sos.py`, "a player arriving at each moved hall's
  travel stop shows". It uses fact 4's figure measure, with a limit of half the figure, not a quarter. At the Tinkers'
  stop, 42% showed plainly in game, and a player arriving does not need more than that.
  - **Red** on P750's design: exactly "custodians: the travel stop at (1560, 974, 5) is 100% covered" (Tinkers 42%,
    the rest 0%). `notes\cc-P753-tools\red\red-fact6-p750-design.txt`.
- **The scan:** `notes\cc-P753-tools\scan_stop.py` (output in `scan_stop.txt`) runs facts 2, 3 and 6's checks on every
  tile from 1552-1569 by 972-981:
  - The street tiles in front of the doors read 62-100% covered.
  - (1560,972,10) reads 0%, but it is the west door leaf's tile.
  - **(1561,973,7)**, the top stone step outside the east leaf, reads 0%. It is open sky and joined on foot to
    Hammerhill's bank and to the guildmaster. The east leaf (EastCCW) swings onto 1562,973, so the step stays clear.
- **The move:** `design/guild-halls/halls.json`, Custodians' travel: (1561, 973, 7), "the top step at the south doors
  (P753: 1560,974 was hidden by the house south of the lane)".
  - `gen.py` rewrote `ClusterFGuildHallPlacementData.cs` and `GuildHallPlacementDesignCopy.cs` (new design SHA-256),
    and `gen.py --verify` matches.
- **Green:**
  - docs `test_guild_hqs_sos.py` 6 of 6. The Custodians' stop reads 0%, joined to the guildmaster and the bank
    (`green\test-guild-hqs-sos.txt`).
  - `check.py` (P281's hall checks): all 18 halls ok; Custodians: "stop reaches the town (290 tiles in the box); npc
    reachable from the stop; npc cuts no walk" (`green\check.out.txt`). It rewrote P708's tracked `check.out.txt`
    (line endings only), and I restored it from git.
  - **Gated build** (`notes\cc-P753-tools\gated-build.ps1`, `docker/uo/build.sh -t sl-modernuo:cc-P753`, under the
    `docker-build` lock, taken and released): **EXIT=0, 2,845 tests: 2,839 passed, 6 skipped, 0 failed**
    (`green\gated-build-summary.txt`; the full log is git-ignored).
  - The live shot on that image (above).
- **CHANGELOG:** a new `2026.10.31.6`, Staff; VERSION 2026.10.31.6 (2026.10.31.5 was main's newest).

## Deviations and decisions for Chase

- **The stop's limit:** fact 6 lets a stop be up to half covered, not fact 4's quarter, because of the Tinkers' shot.
  If you want every stop fully clear, the Tinkers' stop (42%) would move too.
- **A denied search:** the unattended run denied a Grep of the code copy for other uses of "1560, 974" (to check that
  no other code or test names the old stop). I did not retry it. The gated build ran every server test green with the
  stop moved, and the docs copy has no other use.
- **The memory dip:** free memory dropped to 3.7 GB once between runs (the Docker VM's page cache). Dropping that
  cache (the usual one-line alpine command) brought it back to 7 GB. No container was touched.

## Files

- **Code copy:**
  - `design/guild-halls/halls.json`;
  - `server/customizations/ClusterFGuildHallPlacementData.cs` and `server/tests/Misc/GuildHallPlacementDesignCopy.cs`
    (generated);
  - CHANGELOG.md, VERSION.
- **Docs copy:**
  - `tools/tests/test_guild_hqs_sos.py` (fact 6);
  - `notes/cc-P753-tools/`: `shots753.ps1`, `shots753.json`, `shots753b.json`, `run-shots753.ps1`, `scan_stop.py`,
    `scan_stop.txt`, `gated-build.ps1`, `red/`, `green/`;
  - `notes/cc-P753-review/`: the shots and logs;
  - this file.

P753 DONE
