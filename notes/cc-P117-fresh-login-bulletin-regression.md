# cc-P117: a fresh account's first login no longer showed the bulletin (bot P64-1, P64-2)

2026-10-15. Prompt: `D:\UO\cc-prompts\cc-P117-fresh-login-bulletin-regression.md`. A fix in the shard, a regression
test, and a bot re-run of P64-1 and P64-2 only. Not committed (the Golem commits after DONE). Both repos were clean at
the start.

## Headlines

- **The cause, in one line:** the bulletin shows only the current version's player notes, and since 2026-10-14 the
  newest versions hold only a `### Staff` list. So `ShardVersion.UnseenNotesFor` returned nothing, and no bulletin was
  sent at all.
- **A real game bug, not a bot artifact.**
  - Any real new player who logged in while the newest version was Staff-only got no bulletin and never saw the latest
    player notes.
  - So did any player who had missed the last player-facing version.
  - No code between 36c7ae9 and 68631cb caused it. The changelog's shape changed: P95, P98, P100 and P103 are not
    involved.
- **The fix:** the bulletin shows the newest version **at or below the current one that has player lines**, once per
  account. Its title is still "Shattered Legacy <the version the shard runs>". When the notes are from an older
  version, their heading says so: "Patch notes (2026.10.13.4)".
- **The welcome gump and the achievements are untouched.**
  - They never crowded the bulletin out: it simply was not sent.
  - The order is as before: the welcome gump and achievements on login, then the bulletin after its existing 2 s delay.
- **"50 in a skill" and "10,000 gold in the bank" on a first login are expected on the test shard, not bugs**
  (evidence below). Left as they are.
- **Tests:**
  - 1 new fact, seen failing first on exactly this bug.
  - The shard's test gate, **1,164 of 1,164**.
- **The bot, P64-1 and P64-2 only, against the working tree: 3/3 PASS each,** title 'Shattered Legacy 2026.10.15.3'
  (a Staff-only version). Rule 1 held.

## The evidence

**What the bot saw** (`testing\bot-runs\2026-10-15-0130`, commit 68631cb):
- On the account's first login: four ACHIEVEMENT UNLOCKED gumps and "Welcome to New Haven", and no bulletin.
- All three runs were the same.

**Why there was no bulletin.**
- **The code.** `ClusterFBulletinSystem.OnLogin` (`ClusterFBulletin.cs:100-117`) sends the bulletin only when there
  are unread notices or `ShardVersion.UnseenNotesFor(acct)` is not null. Before this fix, `UnseenNotesFor` returned
  null whenever `CurrentNotes.IsEmpty`. `IsEmpty` counts only Added, Changed and Fixed; Staff lines are never
  player notes (cc-P64).
- **The data.** `git show 68631cb:VERSION` is `2026.10.14.19`, and that section of the changelog is:

  ```
  ## 2026.10.14.19

  ### Staff
  - The Shard Console's window, taskbar button and dialogs show the same icon as its desktop shortcut.
  ```

  So `CurrentNotes.IsEmpty` was true and nothing was sent.
- **At 36c7ae9** (P64-1 passed 3/3 on 2026-10-13), `VERSION` was `2026.10.13.4`, whose section has an `### Added`
  line (the new paperdoll art). That is the only difference between the two runs that matters here.
- **The new fact reproduced it.** A fresh account, with the newest section Staff-only, gets `null` from
  `UnseenNotesFor`: "Assert.IsType() Failure: Value is null". That is exactly "no bulletin".
- **It was never a TestAccountWipe artifact.** The seen mark lives on the account (`FlagValues["bulletin.seenVersion"]`),
  and the bot's accounts are new every run. The code path above returns null before any seen mark is read.

**Why a brand-new character earns "50 in a skill" and "10,000 gold in the bank".**
- **The gold:** with `testCenter.enable` true, `CharacterCreation.cs:245-249` runs pinned `TestCenter.FillBankbox`
  (and our test kit) on every new character. Pinned's fill puts bank checks for 1,000,000 gold and 60,000 gold coins
  in the bank (`Special Systems/Engines/TestCenter.cs:238-245`). "Double-Digit Thousands" (`ClusterFAchievements.cs:902`,
  bank gold 10,000) fires at once. **Test shard only**, and expected; it would not happen on live, which runs without
  the test center.
- **The skill:** the bot creates its characters with two skills at 50 (`uobot/client.py:251`, `skills=((0, 50), (1, 50),
  ...)`), as a real player may at creation. "You've Read the Introduction" (`ClusterFAchievements.cs:373`, any skill 50)
  is right for any new character who picks a 50 skill.
- "Set foot in Trammel" (New Haven) and "logged in for the first time" are right for every new character.
- **None of these is a bug,** and none of them hid the bulletin. Left as they are.

## What changed, with file:line (`D:\ShatteredLegacy`)

| File:line | Change |
|---|---|
| `server/customizations/ShardVersion.cs:306-323` | `UnseenNotesFor`: the newest player notes at or below Current (`LatestPlayerNotes`), unless the account's seen version is the same or newer (`CompareVersions`) |
| `server/customizations/ShardVersion.cs:326-342` | `LatestPlayerNotes()`: from Current's section downwards, the first with an Added, Changed or Fixed line; null if none, or if Current has no section |
| `server/customizations/ShardVersion.cs:345-364` | `CompareVersions(a, b)`: date versions part by part as numbers (2026.10.13.10 after 2026.10.13.4; 2026.10.13.2 after 2026.10.13) |
| `server/customizations/ShardVersion.cs:11-15` | the header comment says what the bulletin shows now |
| `server/customizations/ClusterFBulletin.cs:107-108` | the comment at the login hook |
| `server/customizations/ClusterFBulletin.cs:437-442` | the title is `ShardVersion.Current` (the notes' version only if there is no Current); the subtitle reads "What changed most recently:" when the notes are older than Current |
| `server/customizations/ClusterFBulletin.cs:460-462` | the notes heading: "Patch notes", or "Patch notes (<version>)" when they are older than Current |
| `server/tests/Misc/PatchNotesVerification.cs:184-262` | the new fact (below); `using System.Linq` |
| `CHANGELOG.md`, `VERSION` | 2026.10.15.4, one `### Fixed` line (Deviations, item 1) |

**What did not change:**
- Marking seen is still `ShardVersion.MarkSeen(acct, notes)` with the version shown, on any reply to the bulletin.
- A Staff-only release does not show an account its notes again, because the account has already seen the newest
  player notes.
- A new player-facing version shows again. An older seen value is compared by number, not text.

## Tests

**New fact, `PatchNotesVerification.AStaffOnlyVersionStillShowsAFreshAccountTheNewestPlayerNotesUnderTheCurrentVersion`.**
It uses a changelog shaped like today's: 2026.10.03.2 and 2026.10.03 Staff-only on top, then 2026.10.02.2 and
2026.10.02 with player lines.
- a fresh account is shown 2026.10.02.2;
- the bulletin's title is "Shattered Legacy 2026.10.03.2" (the current version), its heading "Patch notes
  (2026.10.02.2)", with "All patch notes" and nothing about a wiki;
- All patch notes marks them seen, and the next login has nothing (P64-2);
- an account shown 2026.10.02.2 before the Staff-only versions is not shown it again;
- a new player version (2026.10.04) shows again, titled with its own version, with the plain heading "Patch notes";
- a changelog with no player lines at all shows nothing.

**Seen failing first.**
- With the fact added and the code unchanged, `docker/uo/build.sh --tests-only`: **1,164 tests, 1,163 passed, 1
  failed**, this fact: "Assert.IsType() Failure: Value is null". A fresh account got no notes: the bug.
- With the fix: **1,164 of 1,164**.
- After the changelog edit, again: **1,164 of 1,164**. The changelog is copied into the image and parsed by other facts.

**The existing facts held unchanged.** That includes cc-P22's "an account sees a version's notes once" (with `VERSION`
naming an older version than the newest section) and cc-P64's "TheBulletinHasNoWikiButtonAndAllPatchNotesOpensTheHistory".

## The bot re-run

`Run-OvernightPlaytests.ps1 -Only P64-1,P64-2 -SkipSoak -NoEmail` (3 runs each by default). No full nightly, no soak.
Report: `testing\bot-runs\2026-10-15-0905\report.md`.

- **Code under test:** working tree at fe7e11b (this fix, uncommitted).
- **Version:** VERSION 2026.10.15.3, a Staff-only section: the real failing case.
- **World:** a copy of the test world's backup 2026-10-15-14-05-01, accounts wiped, bot accounts only.

```
09:06:28    P64-1      run 1: PASS  title 'Shattered Legacy 2026.10.15.3'; All patch notes button yes; wiki text none
09:06:35    P64-1      run 2: PASS  title 'Shattered Legacy 2026.10.15.3'; All patch notes button yes; wiki text none
09:06:43    P64-1      run 3: PASS  title 'Shattered Legacy 2026.10.15.3'; All patch notes button yes; wiki text none
09:06:43    P64-2      run 1: PASS  history gump after All patch notes: yes; bulletin on relog: none (observed during the matching P64-1 run)
09:06:43    P64-2      run 2: PASS  history gump after All patch notes: yes; bulletin on relog: none (observed during the matching P64-1 run)
09:06:43    P64-2      run 3: PASS  history gump after All patch notes: yes; bulletin on relog: none (observed during the matching P64-1 run)
09:06:46    rule 1 held: both real shards are exactly as they were
09:06:47    Overnight play tests: 2 pass, 0 fail, 0 flaky
```

- I added the changelog's 2026.10.15.4 line only **after** this run.
- So the bot tested the Staff-only case. That is the case that failed, and it is the one the bulletin now handles by
  showing older notes.
- The run folder is new machine output in shard-migration (`testing\bot-runs\2026-10-15-0905\`). It goes in with this
  prompt.

## Deviations and decisions for Chase

1. **The patch-note line is under `### Fixed`, not a "### Player" heading.** The changelog's format (its own comment)
   has Added, Changed, Fixed and Staff lists, and only those reach players. A player saw this bug, so it is a player
   line, and Fixed is that list.
2. **What a returning player sees.**
   - Someone who already saw the newest player notes sees no bulletin after a Staff-only update, as before.
   - Someone who missed a player update (for example away since 2026.10.13.4) now sees those notes the next time they
     log in. Before, a later Staff-only release silently skipped them.
3. **The title is always the version the shard runs,** as P64-1 expects ("bulletin with the current version").
   - When the notes are older, the heading names their version and the subtitle says "What changed most recently:".
   - The alternative was to title the bulletin with the older version. That would make the shard look like it runs an
     old build, so I did not.
4. **Not bugs, left as they are:** the "10,000 gold in the bank" and "50 in a skill" achievements on a new character on
   the test shard. They come from the test center's bank fill and from the character's own creation skills.
5. **The next nightly run will see 2026.10.15.4,** a version with a player line, so its P64-1 tests the plain case
   again. The Staff-only case is now pinned by the new shard fact, which runs in every build.

## For Chase

A Staff-only update made the server skip the login bulletin entirely, so a real new player would have missed the
patch notes. It now shows the newest player notes under the current version. **Rebuild the test shard** (console, Test
shard, Rebuild).

## Repo size

No pending file over 5 MB; the largest change is the test file, plus 88 lines. Build output stayed in Docker; scratch
logs stayed in my session scratchpad.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`, after the notes were written:

```
Repo Result
---- ------ 
code dry run
docs dry run
```

code: `CHANGELOG.md`, `VERSION`, `server/customizations/ShardVersion.cs`, `server/customizations/ClusterFBulletin.cs`, `server/tests/Misc/PatchNotesVerification.cs`. docs: this note, the bot run folder `testing/bot-runs/2026-10-15-0905/` and the importer's `testing/` output (machine output).

P117 DONE
