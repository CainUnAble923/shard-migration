# cc-P86: Shard Console "Disconnect VPN" button

Prompt: `D:\UO\cc-prompts\cc-P86-console-vpn-disconnect.md`. Builder (console script and tests); no shard build. Not
committed (autopilot commits after DONE). Both repos were clean at the start.

## Headlines

- **Proton VPN for Windows has no supported scripted disconnect.**
  - There is no command line (Proton's CLI is Linux-only).
  - There is no local API.
  - Its `protonvpn:` and `proton-vpn:` URI keys carry no command.
  - Stopping or killing `ProtonVPNService` is **rejected**: Proton's Advanced kill switch keeps blocking every connection outside the tunnel after a disconnect or a stopped service, so Chase could be left offline.
  - So for Proton the button **opens Proton's own window** and says plainly what to click, and to turn the Advanced kill switch off first.
- **WireGuard for Windows tunnels** are ended by `wireguard.exe /uninstalltunnelservice <tunnel>`, which is what WireGuard's own Deactivate does. The tunnel's config stays, and its firewall rules go with the service. It needs an elevated console; when the console is not elevated, it says so and offers to reopen itself as administrator.
- **Another app's tunnel, or any other VPN adapter, is only named:** "disconnect it in its app". On this PC the two WireGuard tunnel services belong to **WiFiman Desktop**, and standalone WireGuard is not installed. No adapter is ever disabled and no VPN service is ever stopped; the safety check refuses both.
- **The button:**
  - It sits in the PUBLIC DNS tile and on the Diagnostics tab, and goes through the plan and `Test-PlanSafety` machinery with a dry-run plan.
  - It is greyed unless the tile says VPN ON or something VPN-shaped is up. It is refused as SYSTEM.
  - After a click it re-checks every few seconds for up to two minutes and reports the result: green, or what is still up.
  - When the VPN is off but public DNS still has its address, it **offers** (never does by itself) `docker restart sl-ddns`.
- **Proof:**
  - 10 new facts for the enable judge and for the plan in every case (Proton, WireGuard elevated and not, another app's tunnel, an unknown VPN, a route only, none, SYSTEM), plus the safety rules.
  - **205 / 205** facts green. They went red when the code was broken on purpose.
  - The button run for real on this PC with no VPN up was a clean no-op.
  - I did not connect or disconnect any VPN.

## Part A: findings, with sources

Read on 2026-10-13. The overseer's facts were re-checked.

- **Proton VPN v5.1.8** is installed at `C:\Program Files\Proton\VPN\v5.1.8\` (712 files). There is also a `v5.1.7` folder, and `ProtonVPN.Launcher.exe` in the parent folder.
  - Services: "ProtonVPN Service" is running (manual start). "ProtonVPN WireGuard" (`ProtonVPN.WireGuardService.exe ... ProtonVPN.conf`) is stopped; this is Proton's own tunnel when it uses the WireGuard protocol.
  - Processes: `ProtonVPN.Client` runs in session 1 (Chase's). `ProtonVPNService` and `ProtonVPN.NrptWatchdog` run in session 0.
  - **No command line.** I scanned the `ProtonVPN.*.dll` files for argument handling. The only "disconnect" strings are UI and log text ("Disconnect", "Disconnecting from VPN due to no servers available"), plus "Minimized" for start-up. There is no `--disconnect`-style switch.
  - **URI handlers are inert.** `HKCU\Software\Classes\protonvpn` and `proton-vpn` exist as URL protocols with **no `shell\open\command`**, so nothing can be invoked through them. No `protonvpn://` URL appears in the code.
  - **Settings are encrypted.** `%LOCALAPPDATA%\Proton\Proton VPN\Storage\UserSettings.*.json` holds its settings encrypted with Windows DPAPI, so the kill switch mode cannot be read from disk. (Nothing from it was copied here.)
  - **Public docs.** Proton's command-line client (`protonvpn-cli`, with `disconnect` and `killswitch --on/--off`) is for Linux; no Windows CLI was found. On Windows, the kill switch is set in the app (Settings > Connection > Kill switch). The **Advanced kill switch** "prevents all outgoing and incoming connections outside the VPN interface" and "stays active if you manually disconnect the VPN". The standard one blocks traffic until the app reconnects to the same server. Sources: [Proton: permanent kill switch](https://protonvpn.com/blog/permanent-kill-switch), [protonvpn-cli man page](https://dyn.manpages.debian.org/unstable/protonvpn-cli/protonvpn.1), [Manjaro forum on the Linux CLI kill switch](https://forum.manjaro.org/t/protonvpn-kill-switch-and-internet-in-command-line/108748).
  - **`ProtonVPN.RestoreInternet.exe`** ships with the app. Judging by its name it removes the kill switch's blocking filters; that is unverified, as I did not run it. Using it would be a recovery tool rather than a disconnect, so the button never runs it, and the safety check refuses it.
- **WireGuard:**
  - `C:\Program Files\WireGuard\` holds only a `Data` folder, which is not readable without admin. **WireGuard for Windows itself is not installed** (no `wireguard.exe`).
  - The services `WireGuardTunnel$wg30c06d17` and `WireGuardTunnel$wgb89e5f1d` are stopped and set to automatic. Their binary is `C:\Program Files\WiFiman Desktop\WireGuard\wireguard.exe /tunnelservice "C:\Program Files\WiFiman Desktop\<tunnel>.conf"`, so they are **WiFiman Desktop's** (Ubiquiti) tunnels.
  - `/uninstalltunnelservice` on those would delete WiFiman's service under it, so the button only names them.
- **Adapters now:** Ethernet (the LAN) and two Hyper-V vEthernet adapters are up; Wi-Fi and Bluetooth are down. No VPN adapter is up, and the route to 1.1.1.1 is on the LAN.

## Kill switch analysis and the method per VPN

| Method | Kill switch effect | Verdict |
|---|---|---|
| Proton: stop or kill `ProtonVPNService` | The Advanced kill switch's filters stay in place, so the PC is offline until Proton reconnects or RestoreInternet runs (unverified). The standard kill switch also blocks while the app tries to reconnect | **Rejected.** The safety check refuses any step naming ProtonVPNService, ProtonVPN.WireGuardService, RestoreInternet, taskkill, `net stop`, Stop-Service, Stop-Process, Disable-NetAdapter or `netsh interface` |
| Proton: kill the client | The service keeps the tunnel; nothing is disconnected | Rejected (same rule) |
| Proton: a URI or CLI | None exists (above) | Not available |
| **Proton: open its window and click Disconnect** | A manual disconnect with the standard kill switch: traffic flows. With the Advanced one: blocked until it is turned off, so the instruction says to turn it off first | **Chosen.** The plan's `launch` step is `ProtonVPN.Launcher.exe` |
| **WireGuard for Windows: `wireguard.exe /uninstalltunnelservice <tunnel>`** | WireGuard's "block untunneled traffic" firewall rules belong to the tunnel service and are removed with it; the config stays | **Chosen**, elevated only. The safety check allows `wireguard.exe` only with exactly that switch and a plain tunnel name |
| A tunnel another app installed (WiFiman) | Uninstalling its service would break that app's own state | **Named only:** "disconnect it in WiFiman Desktop" |
| Any other VPN adapter | Disabling an adapter needs admin and can leave it disabled | **Named only:** "disconnect it in its app" |

## The button

- **Action:** `vpn.disconnect`, group Network, label "Disconnect VPN". It changes something, so a headless run without `-Mode Execute` is refused (D37); its banner reads "VPN ... No shard is touched."
- **Where:**
  - In the PUBLIC DNS tile, under its line, as P83's links sit in the PLAY TESTS tile.
  - On the Diagnostics tab, whose caption mentions it.
- **When it is enabled:** `Test-VpnButtonEnabled` turns it on when any of these holds:
  - the tile's word is VPN ON
  - a VPN-shaped adapter is up (the console's existing `Test-VpnAdapter` pattern)
  - a WireGuard tunnel service is running
  - Proton's WireGuard service is running
  - the route leaves the LAN

  Otherwise it is greyed, and its tooltip starts "No VPN is on". The facts behind it (`Get-VpnFacts`) are re-read at most every 30 s on the tile's 1 s timer, and never in the facts' own forms.
- **The plan (`Get-VpnPlan`), by case:**
  - **None up:** one refuse step, "No VPN is up: nothing to disconnect." A clean no-op.
  - **SYSTEM:** refused. Proton runs in Chase's session.
  - **Proton:** a say step with the instruction (Disconnect; turn the Advanced kill switch off first), then a launch step for `ProtonVPN.Launcher.exe`.
  - **A WireGuard for Windows tunnel:** an exec step `wireguard.exe /uninstalltunnelservice <tunnel>` when elevated. When not elevated, a say step "needs an elevated console", and the console offers (Yes/No) to reopen itself with `-Verb RunAs`; this one stays open.
  - **Another app's tunnel, an unknown VPN, or a route only:** named, nothing run.
  - **Every plan** ends by saying the tile will re-check.
- **After a click:**
  - `Update-VpnRecheck` asks the tile for a fresh probe every ~5 s for up to 2 minutes, since Proton is clicked by hand.
  - On green it says "VPN off: PUBLIC DNS is green".
  - On WRONG IP (VPN off, DNS still the VPN's address) it offers to restart sl-ddns (`docker restart sl-ddns`, a plan that passes `Test-PlanSafety`). Declined, it says ddns corrects it within its interval.
  - After two minutes still up, it says what is still up.
- **Tooltip** in P84's table (`vpn.disconnect`). The P84 fact requires one for every action.

## Proof

- **Facts** (`scripts\tests\Shard-Console.Tests.ps1`), 10 new:
  - `P86_TheButtonIsOnOnlyWhenAVpnIsUp`
  - `P86_WithNoVpnUpThePlanIsACleanNoOp`
  - `P86_ProtonIsOpenedWithWhatToClickAndNeverStopped`
  - `P86_AWireGuardTunnelIsEndedByItsOwnExeOnlyWhenElevated`
  - `P86_AnotherAppsTunnelAndAnUnknownVpnAreNamedNotTouched`
  - `P86_RefusedAsSystem`
  - `P86_TheSafetyCheckRefusesEveryUnsafeWayToEndAVpn` (seven unsafe steps)
  - `P86_TheDdnsRestartIsOfferedAsASafePlan`
  - `P86_TheButtonsSitByTheTileAndOnDiagnosticsGreyedWithNoVpn`
  - `P86_OnThisPcWithNoVpnUpTheRealFactsGiveANoOp`
- **Red:** four deliberate breaks made 5 facts fail: the judge always on, the WireGuard step without elevation, the SYSTEM refusal removed, and the service-stop rule removed. Restored `cmp`-identical.
- **Green:** **205 / 205** (195 before).
- **Real runs on this PC, with no VPN up:**
  - `Shard-Console.ps1 -Action vpn.disconnect -DryRun` printed `1. REFUSE No VPN is up: nothing to disconnect.` and "(dry run: nothing was run)".
  - `-Mode Execute -Action vpn.disconnect` printed the VPN banner and the same refusal; nothing ran.
  - The real facts read: route on the LAN, 0 VPN adapters, 0 of 2 tunnels running (both WiFiman's), Proton tunnel off, not elevated.
- **Not done, by the prompt's rule:** I did not connect or disconnect any VPN. The real test is below.

## Deviations and decisions for Chase

1. **Proton cannot be disconnected by a script, safely or at all.** The button opens Proton and tells you what to click. If Proton later ships a Windows CLI or local API, the plan's Proton branch is the one place to change.
2. **WireGuard for Windows is not installed;** the two tunnel services are WiFiman Desktop's. The WireGuard path is built and tested, but has nothing to act on here today. Should WiFiman's tunnels be ended by the button too (uninstalling the tunnel service under WiFiman)? I chose no, since it may break WiFiman's state.
3. **`ProtonVPN.RestoreInternet.exe`** looks like Proton's tool for a PC the kill switch left offline. It is unverified and never run. Worth noting for an emergency.
4. **A greyed button shows no tooltip in WinForms** (a disabled control gets no hover events). The tile's own tooltip still explains it.
5. **Reopening the console elevated** (for a WireGuard tunnel) opens a second console window; the first stays open.

## For Chase: the real test

1. **Standard kill switch.** Connect Proton VPN as usual, with the kill switch off or standard.
   - Within ~30 s the PUBLIC DNS tile should read VPN ON and the "Disconnect VPN" button should become clickable.
   - Click it: Proton's window comes up, and the console's output says to click Disconnect.
   - Click Disconnect in Proton.
   - Within a few seconds the console should say "VPN off: PUBLIC DNS is green", or offer to restart sl-ddns if public DNS still has the VPN's address.
   - Check that a web page loads.
2. **Advanced kill switch.** Turn on Proton's Advanced kill switch, connect, click the button, and follow the instruction to turn the kill switch off before disconnecting. Then check that a web page loads. If anything leaves you offline: reconnect Proton, or turn the kill switch off in Proton's settings.
3. **sl-ddns.** If you accept the sl-ddns restart, the PUBLIC DNS tile should turn green within a minute or two.

## Patch notes

`CHANGELOG.md` 2026.10.13.8 `### Staff`: one line. `VERSION` is 2026.10.13.8.

## Commit preflight

`powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\Commit-ShardWork.ps1 -DryRun`:

```
Repo Result
---- ------
code dry run
docs dry run
```

P86 DONE
