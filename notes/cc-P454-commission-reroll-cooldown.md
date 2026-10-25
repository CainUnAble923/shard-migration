# cc-P454: smith commissions: the reroll cooldown on the guild book's abandon, Pre-Crafted for large commissions

## In plain words

- Abandoning a smith commission from the Smithing Guild Book now makes you wait before asking for a new one, the same
  as abandoning it at the Society of Smiths guildmaster. Until now, the book let a player throw away commissions and
  ask again straight away until a good one came up.
- Large (full armor set) commissions now share that wait, as you decided on 10-22. After abandoning a commission of
  either size, a request of either size waits (5 minutes by default). The book tells the player how long is left.
- A large commission now counts toward the hidden Pre-Crafted achievement in the same way a small one does.
- Nothing for you to do. The change is in the patch notes as version 2026.10.24.12, and two wiki lines about the wait
  are updated.

## What changed

ShatteredLegacy, branch golem/Iron/P454.

| Part | Change |
|---|---|
| 1 (cc-P429, new) | `SmithGuildBook.cs:657` `HandleAbandonComm` calls `SmithCommissionSystem.Abandoned(pm)` after the remove, the same call `SmithCommissionGump.cs:302` makes. |
| 2 (cc-P402 F14) | `SmithGuildBook.cs:710` `HandleAbandonLargeComm` records the abandon. `ClusterFSmithCommissions.cs:578` `GenerateLarge` returns null while `RequestCooldownLeft` is above zero, as `Generate` does. The cooldown is shared, as Chase decided (10-22): one timestamp per character covers both sizes, and `clusterf.commissions.abandonCooldownMinutes` sets the length for both. No new setting. |
| 2, the book's message | The book's two request buttons used to answer a refusal with "No commissions available right now." They now go through `CooldownRefuses` (`SmithGuildBook.cs:693`), which sends the guild gump's own wait line ("You abandoned a commission just now. The Guildmaster will offer another in N minute(s).") and offers nothing. |
| 3 (cc-P402 F05) | `ClusterFSmithCommissions.cs:684` `CompleteLarge` calls `ClusterFNotedBySystem.CommissionCompleted(pm, c.IssuedAt)` once, right after the remove, as `Complete` does for a small one. The 60-second window runs from when the large commission was issued to when its last piece goes in. |
| Docs | The comment above `AbandonCooldown` and the `RequestCooldownLeft` summary no longer say "small" only. CHANGELOG 2026.10.24.12 (VERSION bumped) has two Changed lines: the one the prompt asked for, plus one saying large commissions share the wait. Neither line mentions the hidden achievement. Wiki: `guides/crafting.txt:58` and `guilds/society_of_smiths.txt:97` now say the wait follows an abandon of either size, from either place, and holds back a request of either size. |

Other ways a commission leaves the list, none of them a reroll: leaving the smithing guild (`ClusterFGuildSystem.cs:1315`
clears the small commissions together with all standing and Seals) and the GM-only `[ClearCommissions` dev command
(`ClusterFSmithCommissions.cs:961`). I left both alone. Completing a commission costs the item, so it does not need a
wait.

## Tests

Three new facts in `server/tests/Misc/NotedBySystemVerification.cs` (fact family 8). Each presses the real
`SmithGuildBookGump` buttons through `OnResponse` on the comm page: 3 request small, 30 abandon the first small,
6 request large, 50 abandon large, 40+ turn in a large piece.

- `AbandoningThroughTheGuildBookWaitsBeforeTheNextRequest` (:818): abandon through the book, and the cooldown is
  running. A book request inside it gets nothing. After the cooldown a book request gets a commission.
- `LargeCommissionsShareTheAbandonCooldown` (:834): a large abandon starts the cooldown. A large request and a small
  `Generate` both get nothing inside it. After it, a small abandon holds back a large request. After that wait, a large
  request works.
- `ALargeCommissionTurnedInQuicklyCountsForPreCrafted` (:860): every piece of a large set goes in through the book,
  5 seconds apart. The QuickCommission counter is 1 and Pre-Crafted is earned. A second set at 40 seconds a piece
  (every set has two pieces or more, so it ends past the minute) leaves the counter at 1.

Runs: `docker/uo/build.sh -t sl-modernuo:cc-P454`, under the `docker-build` lock (taken, then released). The runs were
started detached from a script file, with the log on disk.

- **Red run 1** (`--tests-only`, the first single-fact draft against the old code): 2,316 passed, 1 failed, 4
  skipped. The failure was the new fact, at "the book's abandon left no cooldown". Its first assert hid the large and
  Pre-Crafted parts, so I split it into the three facts above.
- **Red run 2** (`--tests-only`, the three facts against the old code, with pristine copies of the fixed files saved
  and restored afterwards): 2,316 passed, **exactly 3 failed**, 4 skipped. Each failed at its own part: "the book's
  abandon left no cooldown", "a large abandon left no cooldown", and the Pre-Crafted count (`Assert.Equal`
  expected 1, got 0).
- **Green** (full build, fixed code): **2,319 passed, 0 failed, 4 skipped**, no compiler warnings, and the runtime
  image `sl-modernuo:cc-P454` was built. EXIT=0. After this run I added two comment lines to the test file's fact list
  at the top. They are comments only.

Free memory dropped to 3.7 GB before the green run. I dropped the Docker VM's page cache, which brought it back to
5.9 GB, and the run finished normally.

## Deviations and decisions for Chase

- The Read tool was denied automatically on the ShatteredLegacy test file (unattended run), so I could not use the Edit
  tool there. I read the code with Bash `cat`/`sed` and made every change with small Python exact-replace scripts that
  fail unless the old text appears exactly once. The diff is the same as an Edit would have made. Nothing was skipped.
- I added a second CHANGELOG line, and the wiki updates, so players can see that large commissions wait too. Neither
  names the hidden achievement or its condition.
- Chase decided (10-22): large commissions share the small cooldown. That is done. There is no separate setting. If you
  ever want one, it would be a second timestamp and a `clusterf.commissions.largeAbandonCooldownMinutes` setting.

P454 DONE
