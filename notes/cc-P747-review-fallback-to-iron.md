# cc-P747: build reviews fall back to Iron after 2 hours

Iron Golem, 2026-10-31. Kit changes in `D:\UO\golem` (not a git repo: scratch copy, red, green, md5, backup, install).
Docs copy `D:\UO\golems\Iron\shard-migration` and code copy `D:\UO\golems\Iron\ShatteredLegacy`, both on
`golem/Iron/P747`. Nothing committed, nothing deployed, Haven not touched.

## In plain words

- **A build review nobody takes now goes to Iron.** If a review of building or decoration work is still unclaimed two
  hours after it opens, the merge Golem gives it to Iron as Iron's next task. golem.log says
  `build review: cc-P<n>-review-build-... unclaimed for N minutes: assigned to Iron`.
- **Iron reviews in a fresh session.** Iron never reviews in a session that has just finished a prompt, so it is never
  the session that built the work. Iron rests for a moment and opens a new session for the review. You may get a short
  "Resting: a build review needs a fresh session" email when this happens.
- **No more unreviewed merges on a timer.** A review that runs past 8 hours no longer lets the work merge by itself.
  The log says once that it is still waiting. Only a review verdict or `Skip-BuildReview.ps1 -Prompt <nn>` lets it
  through.
- **Your answers keep their place.** When you answer a question, that prompt stays first even if someone presses Run
  next on another prompt right after; the other one goes straight after it. This fixes P741 jumping ahead of P740
  on 10-30.
- Nothing for you to do. Reviews still unclaimed in the queue now get assigned to Iron at the merge Golem's next round,
  as soon as they are two hours old.

## What changed

### 1. The fallback (`Golems.ps1`, `Invoke-BuildReviewGate`, new `Invoke-BuildReviewFallback`)

- New settings: `buildReviewFallbackMinutes` (default 120) and `buildReviewFallbackGolem` (default `Iron`). Neither is in
  `settings.json`, so the defaults apply.
- At each merge round, a held ticket whose review is still in `queue\` (unclaimed) and at least that old is given to Iron:
  `Assign-Prompt.ps1 -Prompt P<review> -Golem Iron -RunNext -Root <golem folder> -PromptDir <cc-prompts>`. That is the
  overseer's own tool: it checks lane, areas and Touches, rewrites the `**Golem:**` line to `Iron` under the claim token,
  commits and pushes the queue in git mode, and picks the review as Iron's Run next.
- The record `merge-queue\review-P<nn>.json` gets `fallback` and `fallbackAt`, so it is done once:
  - `Iron`: it was assigned.
  - `claimed`: a Golem took the review first.
  - `refused: <why>`: Assign-Prompt refused (exit 2), logged once.
  - Any other failure is retried at the next round.
- The 60-minute widening no longer runs after the fallback. So a `buildReviewFallbackMinutes` set below
  `buildReviewWidenMinutes` cannot take the review back from Iron.
- `Assign-Prompt.ps1` now loads `Golems.ps1` and `golem.ps1` from its own folder, and uses `-Root` only for the data
  (golems.json, settings.json, RUN-NEXT). On the PCs both are the same folder. The change lets the facts run it on a
  test copy of the Golem folder and queue.
- The review prompt now says the work does not merge without a verdict, and that it goes to Iron after 120 minutes.
  The old text said "With no verdict line in 8 hours, P<nn> merges anyway". The opening also says "if your Golem did
  [build it], you are a fresh session that has not seen it".

### 2. A fresh session for a review (`golem.ps1`, `Hand-Off`)

- After a DONE, when the next prompt is a build review (`cc-P<n>-review-build-*.md`), it is not handed into that
  session. Iron rests with the new reason `review`, handled like `context`: the session is kept, it is not counted as
  resting for closing, the ready line, the email subject and the GolemMail text say so. It wakes a session on the
  review's model with `-WakeFor`. That fresh session's start phrase hands the review.
- The check runs for every review, whoever built the work. It is safe because a session that has just finished a
  prompt is the only kind that can have built the work. A session that only said the start phrase has built nothing.

### 3. A timeout never merges (`Invoke-BuildReviewGate`)

- Past `buildReviewHours` (8) the ticket stays held. The log says once (record `overdueLogged`):
  `build review: P<nn> has waited N minutes with no verdict (...): still held; only a verdict or Skip-BuildReview.ps1 -Prompt <nn> lets it through`.
- A record that an older kit marked `timeout` no longer lets a ticket through. The three live records with `timeout`
  (P691, P734, P741) belong to tickets that already merged, so nothing changes for them.
- Only `PASS`, `skipped` (Skip-BuildReview.ps1, or the prompt's `**Build review:** skip` line) or a FAIL's fix-up end the
  wait.

### 4. An answered prompt wins Run next (`golem.ps1`)

What happened on 10-30, from golem.log:

- 21:25:52: Chase answered P740's question. Retry put P740 back, picked to go next.
- 21:26:08: a Run next for P741 replaced the pick.
- 21:26:26: the session woken for P740 claimed P741.

Now:

- An answer's retry (`Invoke-RetryStoppedCore -Answered`, from the Answer event only) writes RUN-NEXT and
  `RUN-NEXT.answered` (or `RUN-NEXT-<Golem>.answered`). A pick that was already there moves to `RUN-NEXT.after`.
- While the answered prompt is still queued and holds RUN-NEXT, a new Run next (console button, Set-RunNext.ps1 or
  Assign-Prompt -RunNext) goes to `RUN-NEXT.after` instead. It replies "P741 goes next after P740: P740 resumes after
  Chase's answer and keeps its place".
- Cancel then clears only the waiting pick.
- Sort-Queue puts the pick first and the waiting pick second, so the status and console order agree.
- `Get-OtherRunNextPicks` counts the waiting pick as that Golem's, so other Golems leave it alone.
- When the answered prompt is handed (`Complete-RunNextPick`, used at both hand-off sites), the waiting pick becomes
  RUN-NEXT. The log says `run next: P741 goes next now (it waited behind P740)`.
- A manual Retry stopped prompt and an ordinary Run next work as before. The Shard Console reads RUN-NEXT, which is
  still one line.

## Tests

New facts in `D:\UO\golem\tests\Golem.Tests.ps1` (`-Only P747`). Each runs on a test copy of the Golem folder and
queue (temp folders, the fake ShadowIron merge world from P734, fake reviews), never the real queue:

- `P747_1_AnUnclaimedReviewGoesToIronAfterTwoHoursAsItsNextHandOff`:
  - At 70 minutes the review is only opened wider.
  - At 125 minutes the Golem line becomes `Iron`, RUN-NEXT names the review, it is logged and recorded, and P105 still
    waits. This is done once.
  - A claimed review is left alone.
  - `buildReviewFallbackMinutes 30` assigns it after 40 minutes, and the later widening does not take it back.
- `P747_2_AReviewIsNeverHandedIntoTheSessionThatBuiltTheWork`: after P100 DONE the review is not handed. The rest is
  `review`, one Opus session is woken for P101, and the fresh session's phrase hands it.
- `P747_3_ALateReviewNeverMergesOnItsOwnOnlyAVerdictOrASkip`:
  - At 9 hours the ticket is still held and nothing merges. That is logged once.
  - An old `timeout` record is held too.
  - Skip-BuildReview.ps1 lets it through.
  - The review prompt no longer says "merges anyway".
- `P747_4_AnAnsweredPromptKeepsItsPlaceAheadOfALaterRunNext` replays 10-30 with the real Answer-Question.ps1:
  - A Run next for P101 after the answer waits behind P100, and the status queue shows P100 then P101.
  - The woken session gets P100, then P101 becomes the pick.
  - Cancel keeps P100 first.
- P734's time-out check (it expected a merge after 9 hours) is replaced by a pointer to P747_3.

Results:

- **Red first** (the new facts against the unchanged live kit): 7 checks passed, 22 failed, and all four facts failed.
  Fact 4's failure is the 10-30 order (`cc-P101-b.md, cc-P100-a.md`). File: `notes\cc-P747-tools\red-golem-p747.txt`.
- **Green** against the scratch kit: 30 checks, 0 failed (`-Only P747`). After the install the same run against `D:\UO\golem` also passes 30 of 30,
  and P734's facts pass 30 of 30 (`notes\cc-P747-tools\green-golem-p747-live.txt`). P182 (Run next), P370_4 (per-Golem
  pick) and P216 (answers) facts on the final code: 18, 6 and 56 checks, 0 failed.
- **The whole kit suite on the changed kit** (`notes\cc-P747-tools\golem-suites-summary.txt`):
  - Golem.Tests: 1660 passed, 7 failed. The unchanged live kit, run at the same time, gave 1632 passed with the
    same 7 failed, in the same 4 facts:
    - the two usage-limit facts, which read a reset time near midnight (the run was at 23:24);
    - P184's two Touches-guessing facts (P734 found these too).
    So none of the failures is this change.
  - Assign 3/3, Lane 65/0, Codex 161/0, Tinker 199/0, RemoteAgent 90/0, GolemPower 133/0, GolemDays 53/0 and
    CommitShardWork 5/5: all green.
- **No shard build.** No server or client file changed, only the CHANGELOG and VERSION in the code copy.

## Installed

The live files were md5-checked against my scratch copy's originals (unchanged), backed up as `*.bak-20261101-P747`,
and replaced by rename: `Golems.ps1`, `golem.ps1`, `Assign-Prompt.ps1`, `GolemMail.ps1` and `tests\Golem.Tests.ps1`
in `D:\UO\golem`. The diff is `notes\cc-P747-tools\p747.diff`; the new facts alone are `p747-facts.ps1`. The Tinker
carries the kit to the other PCs as usual.

Live effect, seen in `merge-queue`: P743's review (P754, queued 2026-10-31 23:10, for Gold and Copper) is the one
pending now. Unless Gold or Copper claims it first, the merge round after 01:10 gives it to Iron.

## Deviations

- **The P734 fact changed:** its 9-hour time-out merge check is the very behaviour part 3 removes. The new check is in
  P747_3.
- **The CHANGELOG line** is a `### Staff` line under a new `## 2026.10.31.10`, and `VERSION` is bumped to match. The
  integrator renumbers at merge (cc-P213).

P747 DONE
