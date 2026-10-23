# P493: review of Golem test accounts (P215)

Reviewed on 2026-10-23 in the Verite work copies. Review only; no code changes.

Read both work copies' AGENTS.md, direction-decision.md, tasks.md, cc-P215-golem-test-accounts.md, and cc-P215-golem-test-accounts-codex-review.md first. The findings below do not repeat that review's pool-password, scheduled-identity, plaintext-delivery, or outstanding shard-proof findings.

## Findings

1. **bug** - `server/customizations/Misc/GolemTestAccounts.cs:234`: Character access levels are corrected only when the account's access level differs, so a `<golem>-player` account already at Player keeps any separately promoted staff character and the seed reports it as already right. Check every character independently of the account level, and add a regression case with a Player account whose existing character is GameMaster.

2. **risk** - `D:/UO/golem/tests/GolemTestAccounts.Tests.ps1:173`: The password-in-git check puts each real password into `git grep -e` arguments, exposing it in process command lines and potentially in process-creation audit logs when command-line recording is enabled. Send the search pattern through standard input with `git grep -f -`, and add a stand-in git check that rejects passwords in its arguments.

3. **risk** - `D:/UO/golem/GolemTestAccounts.ps1:127`: `Set-GtaFileAcl` discards the ACL command's output and never checks its exit code, so delivery continues after a failed local ACL restriction on the plaintext temporary file created at line 215; its grants also leave unrelated explicit permissions intact on an existing file. Establish an exact owner-and-SYSTEM ACL before writing credentials, stop on ACL failure, and test both command failure and an existing extra explicit grant.

## Evidence and test gaps

- Finding 1 is confirmed by the seed's branch and by pinned ModernUO at `d4531cd94b739613155225c234900de9f47d2c88`, whose worktree was clean: `Projects/UOContent/Network/Packets/IncomingAccountPackets.cs:248` selects the existing character without resetting its access level, and `Projects/Server/Commands.cs:293` authorizes commands from the character's level. `server/tests/Misc/GolemTestAccountsVerification.cs:149` changes only an account's level; it does not cover independent character drift. This was source review, not a running-shard reproduction.
- Finding 2 follows the real-key loop at `GolemTestAccounts.Tests.ps1:167` through its native git invocation. No real key files were opened, and whether Windows process-command-line auditing is enabled on any PC is unverified.
- For finding 3, dot-sourced the real library with `-LoadOnly` under Windows PowerShell 5.1.26100.9711 and substituted an in-memory `icacls.exe` function that set exit code 5: `Set-GtaFileAcl` returned normally with that failure code still present. The existing ACL assertion at `GolemTestAccounts.Tests.ps1:81` checks newly created files, not failed ACL commands or old explicit grants; the real delivery path was not run.

## Other checks

No additional live-shard guard bypass was found in the reviewed code. `GolemTestAccounts.cs:55` uses `TestAccountWipe.Refusal` (`TestAccountWipe.cs:80`), requiring the test role and allow flag and refusing a 2593 listener; `uobot/safety.py:51` and `:61` refuse the live port before connection and on relay. The current `docker/uo/docker-compose.yml` has no live shard service, and `docker/uo/retired/docker-compose.live.yml` keeps the old definition outside `services`. Whether any credentials actually authenticate on a running shard is unverified.

No additional direct password output was found in the normal bot login transcript or web password endpoint. Reviewed `uobot/client.py`, `golemcheck.py`, `run.py`, their P215 tests, `web-console/server.py`, `static/app.js`, and `tests/test_golem_accounts.py`, including the authorization, no-store response, and access-log paths. The endpoint deliberately returns a password to the authorized copy button.

Also reviewed the P215 portions of `docker/uo/Start-TestShard.ps1`, `tools/playtest-bot/Run-OvernightPlaytests.ps1`, the bot README, CHANGELOG and VERSION, and the local kit's `GolemTestAccounts.ps1`, `Get-GolemTestAccount.ps1`, `Kit.ps1`, `Export-GolemKit.ps1`, `Golems.ps1`, `Test-GolemReady.ps1`, README, `tests/GolemTestAccounts.Tests.ps1`, and `tests/Join.Tests.ps1`. No remote machines or services were contacted.

Validation:

- `tools/playtest-bot/tests/test_golemcheck.py`: 9 tests passed.
- `web-console/tests/test_golem_accounts.py`: 4 tests passed.
- Initial runs failed during fixture setup because Python's restricted temporary-directory permissions prevented child-file creation, including under the work copy. The successful rerun used an in-memory `tempfile.mkdtemp` adapter creating directories with inherited permissions inside the git-ignored `server/lib/p493-review-scratch` folder; test files and production code were unchanged.
- A synthetic malformed-key probe through the real helper and `golemcheck.account` did not expose its synthetic password in stdout, stderr, or the propagated exception. No real credentials were used.
- No new tests were added. The C# build gate, kit suites that read real passwords, account creation, delivery, and live authentication were not run for this review.
- `tools/progress.py --dry-run` completed against these work copies. It unexpectedly rewrote `tools/progress.json`; restored that file byte for byte from HEAD so the review changes only this note.
- Automatic approval review rejected scratch-folder removal with "blocked by policy." Synthetic fixtures remain in the git-ignored `server/lib/p493-review-scratch` folder; none contains real credentials or exceeds 5 MB.

P493 DONE
