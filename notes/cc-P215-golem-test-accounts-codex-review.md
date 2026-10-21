# Codex review: P215

CC task P215: every Golem gets its own Admin and Player account for play trials. Reviewed by Codex (`codex exec review`, read-only) after P215 DONE and before the Golem's commit, 2026-10-21 07:23.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.99). The Golem account switch breaks existing bulletin checks by using the wrong password when reconnecting pool accounts. The task's required own-shard and real shared-Test-Shard proofs also remain outstanding: the task notes explicitly defer them and report scratch-shard evidence instead.

- **medium** [P2] Preserve the pool password for bulletin-check reconnects (`tools\playtest-bot\uobot\run.py:193`)
  With `GOLEM_NAME` set, this replaces `playerPassword` with the Golem's password, but `checks.p64_1` still reconnects its `slbot-player2`???`4` account using `ctx.secrets["playerPassword"]`. Those accounts retain the original pool password, so the reconnect fails authentication, breaking P64-1 and preventing P64-2's result from being recorded. Update that reconnect to use `poolPassword`, as `Ctx.fresh` now does.

(1.4 minutes, 359,898 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.98). This repository contains only the new task note, not the implementation, so implementation correctness cannot be independently verified here. The note itself documents unmet acceptance criteria, plaintext credential storage, and a scheduled bot that still uses the old accounts.

- **high** [P1] Keep the task incomplete until the required shard proofs pass (`notes\cc-P215-golem-test-accounts.md:8`)
  The note explicitly defers the own-shard logins and the real shared-Test-Shard trade check, but ends with `P215 DONE`. Scratch-shard checks do not establish remote credential usability or the real shard's advertised-address connectivity. These are explicit acceptance criteria, not optional follow-ups. Record STOPPED until those checks can run; [AGENTS.md:44-46](../AGENTS.md#L44-L46) specifically prohibits DONE before completion because it triggers the Golem.
- **medium** [P2] Configure the scheduled bot to use its Golem's accounts (`notes\cc-P215-golem-test-accounts.md:234`)
  The note says the actual overnight scheduled task does not set GOLEM_NAME, so it continues using the old shared accounts despite the new conditional implementation. Step 4 requires the play-test bot to use the running Golem's accounts by default. Configure the scheduled entry point to resolve or supply its Golem identity and verify that execution path, rather than leaving the deployed bot opted out.
- **medium** [P2] Protect delivered credentials before declaring delivery complete (`notes\cc-P215-golem-test-accounts.md:227`)
  The documented delivery leaves passwords stored in plaintext until the first helper read. A Golem that never reads its file leaves that plaintext copy indefinitely, contrary to the task's requirement for a DPAPI file on each Golem's PC. Restrictive ACLs do not supply encryption at rest. Complete provisioning under the destination Golem's usable Windows session and verify DPAPI protection before treating delivery as successful.

(0.8 minutes, 142,996 tokens)
