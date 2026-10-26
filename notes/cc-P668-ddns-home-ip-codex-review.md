# Codex review: P668

CC task P668: DDNS always publishes the home IP, even with the tower's VPN on. Reviewed by Codex (`codex exec review`, read-only) after P668 DONE and before the Golem's commit, 2026-10-26 17:09.
Findings never block the commit: high ones go to the done email under "Codex flagged" and to the overseer's list, D:\UO\overseer\codex-flags.md.

## ShatteredLegacy

Verdict: patch is incorrect (confidence 0.97). The main architecture addresses VPN-dependent IP discovery, but mismatch handling and persistent learning have correctness gaps, and the proof can inherit live DNS credentials. Required VPN-on connectivity remains unverified. Unit-test execution was limited by the read-only sandbox's prohibition on temporary files.

- **high** [P1] Override inherited production credentials in the proof (`scripts\tests\ddns\Test-DdnsHomeIp.ps1:38`)
  When the invoking shell already exports `CF_ZONE_ID`, `CF_API_TOKEN`, and `DOMAIN`, Compose gives those variables precedence over `--env-file`. The supposedly isolated proof then uses production credentials and the production domain, and its successful scenarios can publish `8.8.4.4` to the live apex. Explicitly replace and restore those process variables, or override the updater's entire CONFIG with literal dummy values in the proof compose file.
- **medium** [P2] Complete the required VPN-on connectivity verification (`docker\uo\docker-compose.yml:27`)
  The task explicitly requires confirming that the container reaches Haven with ProtonVPN enabled, but the implementation notes state that only VPN-off connectivity was checked. The `VpnOn` proof substitutes an internal stub and therefore cannot establish whether ProtonVPN permits either configured route. Complete the real VPN-on, read-only reach check before treating this requirement as finished; otherwise the updater may safely refuse forever rather than follow home-IP changes.
- **medium** [P2] Refuse service after the public lookups disagree (`docker\homeip\homeip.py:88`)
  After an earlier successful lookup, a disagreement only sets `agreed=False`; `current()` continues serving the previous address for up to 15 minutes. Consequently, the updater can still publish an address during the fake-mismatch scenario that the prompt requires to leave DNS untouched. The integration test misses this because its disagreement scenario starts with an empty cache. Invalidate the served answer on disagreement and test disagreement after a successful lookup.
- **medium** [P2] Avoid permanently blacklisting a genuine home-address change (`docker\uo\ddns-gate\gate.py:176`)
  If the home address changes while Haven temporarily serves its cached previous address, the tower's new home egress can be learned as a VPN exit after 900 seconds. This overlaps Haven's allowed 900-second cache lifetime. Once Haven catches up, the gate permanently refuses the actual home address because learned exits never expire or get reconsidered. Account for Haven's stale-answer window before learning, or provide a safe reconciliation mechanism.

(1.8 minutes, 498,445 tokens)

## shard-migration

Verdict: patch is incorrect (confidence 0.97). The documentation explicitly leaves a required real-VPN acceptance check unfinished while signaling completion. Only the two changed documentation files were available in this repository; the implementation and reported test results could not be independently verified here.

- **medium** [P2] Complete the VPN-on verification before marking the task done (`notes\cc-P668-ddns-home-ip.md:189`)
  Parts 2 and 6 explicitly require confirming container-to-Haven connectivity and the updater's chosen address with the actual VPN on. The notes acknowledge that neither was verified; the simulated VpnOn scenario cannot establish whether ProtonVPN permits this network path. If it blocks both paths, DNS updates remain stuck. Complete that verification without changing live DNS, or request Chase's help and mark the task stopped rather than done, as required by [AGENTS.md:44???48](../AGENTS.md#L44-L48).

(0.5 minutes, 131,478 tokens)
