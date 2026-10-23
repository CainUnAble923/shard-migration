# P472: Review of away mode and email controls (P149)

2026-10-23. Review only. No code changes.

## In plain words

- Another Gmail user can pass the sender check by putting Chase's address in a quoted display name, if that user also has a current reply code.
- Concurrent updates can undo Away mode off, and the parked-prompt filter can run a task whose prerequisite is blocked.
- Reply handling has gaps around error contents, throttling, and code locking. The findings below include suggested fixes and missing regression cases.
- For Chase: no action was taken against the running Golem, email account, shards, or Haven. These findings are for a later fix prompt.

## Scope

Read both work copies' AGENTS.md, the direction decision, the task-list working agreement, and `notes/cc-P149-away-mode-and-email-controls.md`. A search of the notes found no separate P149 review beside it. The findings below do not repeat P149's listed setup limitations or deviations.

Reviewed the current source, including later changes to email formatting and delivery:

- `D:\UO\golem\Away.ps1`, `golem.ps1`, `Golems.ps1`, `Set-Away.ps1`, `Mail-Commands.ps1`, `Mail-Hidden.vbs`, and the relevant README sections.
- `D:\UO\golem\GolemMail.ps1`, `GolemOutbox.ps1`, the reply-delivery branch in `TinkerMail.ps1`, and `TinkerLib.ps1`'s `Send-TinkerMail` to trace the outgoing body.
- `D:\UO\golem\tests\Golem.Tests.ps1`, especially the P149 facts.
- Code work copy: `scripts/Shard-Console.ps1`, `scripts/tests/Shard-Console.Tests.ps1`, `web-console/golem-actions.json`, `web-console/console-actions.json`, `web-console/static/app.js`, and the relevant cases in `web-console/tests/test_actions.py` and `test_remote_golems.py`.
- Later context: `notes/cc-P157-plain-english-emails.md` and P410's email-controls limitation. P410 already records that Tinker emails lack reply codes, so that is not a new finding here.

All finding locations below are in `D:\UO\golem\Away.ps1`. Its reviewed SHA256 is `D4D4DC5F097CF89689822DACE44CC36FE928F07162CC05179D0B773AE0DEFDEB`.

## Findings

1. **bug**, `D:\UO\golem\Away.ps1:390`: The sender regex accepts `From: "<ckfleming@gmail.com>" <review-other@gmail.com>` as Chase, although the actual mailbox is `review-other@gmail.com`; with Gmail-domain authentication results and a current code, `away off` passes validation. Parse exactly one mailbox with a proper address parser, compare its actual address, and add rejection cases for quoted display names and multiple mailboxes.

2. **risk**, `D:\UO\golem\Away.ps1:399` and `:400`: The authentication regexes treat the word boundary after `gmail.com` as an exact domain check, so `header.d=gmail.com.review.invalid` and `header.from=gmail.com.review.invalid` both pass. Compare complete parsed domain tokens against `gmail.com` and add suffix-domain rejection cases; this probe establishes a validation weakness, not a verified Gmail delivery bypass.

3. **bug**, `D:\UO\golem\Away.ps1:93` and `:36`: An event update reads the whole away state and later saves that snapshot without locking, so an overlapping `Set-AwayMode $null` can successfully save off and then be overwritten with the event's older `on=true` state. Serialize the entire read, update, and save transaction for every away-state writer, use a unique temporary file, and add an interleaving test that keeps off authoritative.

4. **bug**, `D:\UO\golem\Away.ps1:153` and `:159`: With P101 parked, P102 depending on P101, and P103 depending on P102, the filter excludes P102 but returns P103 because it checks dependencies only against the original parked IDs. Compute the blocked dependency chain before selecting a task, and extend the parking test to cover an indirect dependency and reversed queue order.

5. **risk**, `D:\UO\golem\Away.ps1:275`: When the code-file mutex times out, execution still reads, modifies, and writes the code list without owning the lock, allowing competing processes to lose updates or defeat one-time consumption. Stop or retry when `WaitOne` returns false, and add a timeout test proving that neither the body nor file access runs without ownership.

6. **risk**, `D:\UO\golem\Away.ps1:533` and `:535`: Command exceptions and child-process output flow into the emailed result without redaction, and a synthetic exception retained both its full Windows path and a secret marker in the final formatted body. Send a short approved failure description, retain raw diagnostics locally, and add tests that reject full paths and synthetic credentials in both direct and Tinker-routed replies.

7. **risk**, `D:\UO\golem\Away.ps1:410` and `:518`: A verified unknown command receives a reply without spending its code or recording a rate-limit attempt, so repeating one message produced three replies under a limit of one per hour. Add a separate reply or attempt quota while preserving the ability to correct a typo with the same code, and test repeated unknown messages against that quota.

## Probe evidence

Ran isolated commands with `powershell.exe -NoProfile`, Windows PowerShell **5.1.26100.9444**. The probes dot-sourced the actual function definitions, replaced file access and delivery with memory-only stubs, and supplied synthetic headers, state, and errors. They did not execute the live hook, acquire its real mutex, send mail, connect to IMAP or SMTP, or change its files.

| Case | Observed result |
| --- | --- |
| Ordinary Chase mailbox, Gmail-domain auth, synthetic current code | Accepted, as expected. |
| Ordinary other Gmail mailbox with the same auth and code | Rejected, as expected. |
| Other Gmail mailbox with Chase's address inside its quoted display name | Accepted; .NET's `MailAddress.Address` independently identified the other mailbox. |
| Authenticated-domain strings ending in `gmail.com.review.invalid` | Accepted by the validation regexes. |
| Off saved between an event's state read and save | Off was saved, then `Test-AwayOn` returned true after the stale event save. |
| P101 parked, P102 depends on P101, P103 depends on P102 | Filter returned `cc-P103-c.md`. |
| Fake mutex returns false from `WaitOne` | Protected body still ran. |
| Command throws an error containing a synthetic full path and `token=DEMO_SECRET_VALUE` | Actual mail formatter retained both in the reply's first line. |
| Same verified unknown message repeated under an hourly limit of one | Three unknown replies, zero accepted commands, original code unused. |
| Clock exactly at the saved away deadline | `Test-AwayOn` returned false; `Update-AwayMode` saved off and produced `away-ended`. |

The dependency, sender, locking, error-content, and repeated-unknown probes exposed the current failures before any fix. No implementation or permanent test was added, so there is no claimed passing fix run.

## Missing coverage and limits

The sender fact at `D:\UO\golem\tests\Golem.Tests.ps1:2731` tests an ordinary wrong address and failed or missing authentication, but misses quoted display names, multiple mailboxes, and domain suffixes. The parking fact at `:2824` covers direct dependencies and overlapping areas, but misses dependency chains. The digest and expiry fact at `:2871` runs sequentially and does not exercise an off request overlapping an event or digest update. The unknown-command fact at `:2784` deliberately keeps a typo's code usable, but limits only accepted commands and does not check repeated unknown replies. The reviewed P149 facts do not cover mutex timeout or sensitive error text in outgoing replies.

I found no normal timed-expiration bug that leaves away mode enabled forever, and no additional defect in the reviewed console button allowlist or web rendering. I found no direct placement of the saved IMAP password into an outgoing reply; finding 6 concerns unfiltered error or command output, and its secret marker was synthetic.

Real Gmail acceptance of the crafted From header, a real authenticated email round trip, a real concurrent-process race, SMTP failure recovery, scheduled-task behavior after reboot, and actual credential exposure remain unverified. The live credentials and mailbox were not read. The full Golem, Shard Console, and browser suites were not run for this notes-only review; the existing relevant tests were read, and the isolated probes above were run instead.

Ran `tools/progress.py --dry-run` with both work-copy path overrides. It completed but writes `tools/progress.json` even in dry-run mode; restored that generated snapshot to its previously clean HEAD contents so the review leaves only this note changed. No files over 5 MB were added, and no commit, merge, push, branch switch, deployment, or Haven connection was performed.

P472 DONE
