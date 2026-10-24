# Codex review: P409

CC task P409: Town Houses, our own design (leaseholds with rentals and sublets in towns) (design not. Reviewed by Codex (`codex exec review`, read-only) after P409 DONE and before the Golem's commit, 2026-10-24 04:51.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## shard-migration

Verdict: patch is incorrect (confidence 0.96). The notes cover the requested sections and remain research-only, but the design leaves concrete gaps in subtenant access, payout safety, downtime handling, and its acceptance tests. These should be resolved before the notes become implementation prompts.

- **medium** [P2] Account for intentional gold sinks in conservation tests (`notes\cc-P409-town-houses-design.md:247`)
  The proposed assertion that shard gold remains unchanged through leasing and subletting contradicts the design's consumed town rent and 10% town fee. L2 repeats the same unchanged-total test. Specify conservation as remaining gold plus recorded sinks equaling starting gold; otherwise a faithful implementation fails the acceptance test, while refunding consumed rent could incorrectly pass it.
- **medium** [P2] Persist enough timing state to exclude downtime from grace (`notes\cc-P409-town-houses-design.md:284`)
  The saved timing fields are `paid through` and `grace started`, and the design says overdue processing catches up from those timestamps. Those fields alone cannot distinguish seven days online from seven days offline. Skipping the first startup sweep only postpones eviction by 15 minutes. Specify persisted accumulated grace uptime or downtime adjustment, including how missed rent during shutdown is treated, and add a multi-day restart test.
- **medium** [P2] Preserve escrow when a bank deposit fails (`notes\cc-P409-town-houses-design.md:247`)
  When a recipient's bank is full and account gold is unavailable, `Banker.Deposit` can return false and `DepositUpTo` can pay only part of the amount (`Banker.cs:209-316`). Zeroing escrow before depositing, without retaining an unpaid balance, therefore destroys the subtenant's money. Specify a pending-payout balance or another failure-safe delivery mechanism, and test a full bank. This also follows the source-verification requirement in [AGENTS.md:58-60](../AGENTS.md#L58-L60).
- **medium** [P2] Design subtenant access through the house region (`notes\cc-P409-town-houses-design.md:101`)
  For the recommended private-house option, opening a room door does not let a subtenant enter: `HouseRegion.OnMoveInto` rejects anyone without `House.HasAccess`, and its login handler ejects non-friends. Neither the room design nor L3 specifies how these checks are handled. Define room/common-path access and login behavior without granting house-wide friend or co-owner privileges, and test a private leasehold. These engine checks need the pinned-source verification required by [AGENTS.md:58-60](../AGENTS.md#L58-L60).

(1.4 minutes, 315,586 tokens)
