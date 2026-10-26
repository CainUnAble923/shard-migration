# P659: fix the two Medium findings from P657

## In plain words

- Old courier letters: if someone still holds several Exchange letters from before the one-job rule, the server now tears up the replaced ones when it restarts. Before, a replaced letter could become payable again after the newer one was delivered and the server restarted. Players notice nothing unless they had such a stockpile.
- Guard witness log (test shard only): a second crime by the same person in the same instant and spot, such as a victimless crime right after an attack, now gets its own log entry and its own witnesses. Before, it was folded into the earlier attack, and someone who only saw the second act could be listed as a witness to the first.
- Both are in the patch notes for 2026.10.26.10.
- Nothing for you to do.

## What was done

Code work copy `D:\UO\golems\Iron\ShatteredLegacy`, branch `golem/Iron/P659`, base `3b4d321` (P656 merged). Both P657 findings were checked against today's code first; both still held.

| Finding | Done or skipped | Fix | Test (red against the base code) |
|---|---|---|---|
| 1. An obsolete courier letter becomes payable again after a restart | Done | `ClusterFExchangeLetter.Claim` takes a `loading` flag. On load, the letter that loses the per-courier claim (the earlier expiry) is deleted, whichever loads first. The load hook is the generator's default deferred `[AfterDeserialization]` (it emits `Timer.DelayCall`), so the delete runs after the whole world is loaded. Issuing a new letter is unchanged. No new saved field. | `AnOlderLetterStaysReplacedAfterARestart`, 4 cases: older or newer loads first, times the newer one is delivered or deleted. Each then restarts again while the older letter is unexpired and tries to deliver it. Red in all 4: `Assert.False(older.IsOutstanding)` was True after the second restart. Control `ALoneLetterStillPaysAfterARestart` passed red and green. |
| 2. The action matcher still absorbs a separate victimless crime | Done | `ClusterFGuardWitness.SameAction` now joins only an incident that is still an open criminal flag (kind `CriminalAction`, no victim yet) and only for a callback that names a victim (aggression or assist). A victimless callback always starts its own incident. A finished incident is never joined again. This follows the stock order: `Mobile.DoHarmful` and `DoBeneficial` raise the criminal flag first (`OnHarmfulAction` / `OnBeneficialAction` -> `CriminalAction`), then the aggression or assist callback. The merge branch now always completes the open flag: kind, victim, action place, and witnesses filtered to those who saw the victim's place. | `ALaterActInTheSameMomentAndPlaceIsItsOwnIncident`: an attack; a newcomer steps into view; a victimless crime with no clock advance and no culprit move; then a second attack on the same victim. It needs 3 incidents, the newcomer absent from the first, the second at the culprit's spot with no victim. Red: `Expected: 2, Actual: 1`, with the output showing `#1 Aggression Victim ...: Victim, Newcomer`. The existing one-action/two-callback control (`ACrimeIsRecordedAtTheEventWithExactlyItsWitnesses`, `OneActionIsOneIncidentAndADistinctOffenseIsAnother`) and the pet case still pass. |

### How the tests ran

Red and green runs used throwaway containers from `sl-uo-builder:cc-P656` (the image for the base commit). The work copy was mounted read-only, and a scratchpad `probe.sh` / `run.sh` copied in only the named files (P647's method). The red run copied only the two test files, so it ran against the base production code. Red: 6 tests, 5 failed (the 4 restart cases and the witness fact), 1 passed (the lone-letter control). Green, with the two production files synced: `PersuasionVerification` and `GuardWitnessVerification` complete, 36 of 36 passed.

The restart in the letter test is a simulation. It clears the in-memory claim table and invokes the letter's real `AfterDeserialization` hook on the surviving letters, by reflection. It is not a full world save and load.

### Gated build

`docker/uo/build.sh -t sl-modernuo:cc-P659`: green, `EXIT=0`. 2648 tests: 2644 passed, 0 failed, 4 skipped (the `MapCheckRealDataVerification` facts that need client map data, skipped as usual). The new facts are among the passed. Images `sl-uo-builder:cc-P659` and `sl-modernuo:cc-P659` were built under the `docker-build` lock, which is released. The first launch failed before building: from PowerShell, `bash` resolved to WSL's relay once Docker Desktop was up (`execvpe(/bin/bash) failed`). The relaunch named Git Bash (`C:\Program Files\Git\bin\bash.exe`) explicitly.

### Files changed (code work copy)

- `server/customizations/ClusterFExchangeLetter.cs`: durable replacement on load.
- `server/customizations/ClusterFGuardWitness.cs`: the narrowed matcher and the merge branch.
- `server/tests/Skills/PersuasionVerification.cs`: facts 13 (two).
- `server/tests/Regions/GuardWitnessVerification.cs`: one new fact and a header line.
- `CHANGELOG.md` and `VERSION`: `2026.10.26.10`, with one player Fixed line (Persuasion) and one Staff line (guard witness log).

## Limits and what was not done

- Finding 2 is fixed by the stock callback order, not by an action identity. The review offered both; the engine gives no action context to the region callbacks without a new patch on `Mobile.DoHarmful`. Two edge cases remain. If one action ever raised the criminal flag twice, the extra flag is its own victimless incident. An aggression or assist arriving with no flag of its own, in the same moment and place as an earlier unfinished victimless flag, would complete that flag. Stock always raises an act's own flag immediately before its callback, so the newest open flag is that act's.
- The pet-owner suppression defect from `cc-P647-fix-weekend-review-findings-codex-review.md` is a separate finding (P657 says so too) and was not touched.
- Finding 1 deletes replaced letters silently at load. They were already worthless: `Deliver` tears them up with a message. Actual legacy stockpiles in the live world were not inspected.
- No shard start, client session, save or account operation, or Haven connection. Docker Desktop was stopped at the start. It was started under the `docker-build` lock and left running.

## Preflight

Both repositories pass `git diff --check`. The code work copy changes only the six files listed; the notes repo changes only this file. This note is plain ASCII. No `docs/` file changed. No commit, merge, push or branch switch was made.

P659 DONE
