# Player package, and the two server-side things behind it

2026-09-26. Brief: a zip Chase can hand to family (unzip, double-click, playing), after first checking two live-config
findings (A), making the test shard reachable from the LAN (B), then building the package (C).

**Headline: the brief's proposed fix for A.1 is wrong, and it would have broken every client.** Both A findings
rested on the premise that the server sees each client's real address. It does not. Under Docker Desktop, **every
connection reaches ModernUO from `172.19.0.1`**, the bridge gateway, whether it came from loopback, the LAN or the
internet. That one fact changes both answers, and it is measured, not read.

---

## For Chase: what to change on the live shard, and what not to

Nothing below has been applied. All of it needs a live restart, which is yours.

### A.1, the relay address

**Do NOT set `"serverListing.address": null` with `autoDetect: true`.** Tried on the test shard: the server detected
the public IP correctly (`Auto-detected public IP address (216.247.206.76)`) and still relayed the client to
**`172.19.0.2:2594`**, the container's internal address, which nothing outside Docker can reach. On live that is
every stock client, LAN and internet alike.

**The package does not need any live change.** It sets TazUO's `ignore_relay_ip: true`, which ignores the relay's
address *and port* and reconnects to the server it logged in to. Proven by logging in with the packaged client (C.4).

**If you want stock clients (Razor, ClassicUO, the EA client) to work from outside the house too**, the only setting
that does it on this topology is the literal public address:

```json
"serverListing.address": "216.247.206.76",
"serverListing.autoDetect": "False",
```

Expected effect after a restart: every client is relayed to `216.247.206.76:2593`. Internet clients reach it. LAN
clients reach it through the router's hairpin NAT, which I measured working: a TCP connect from this machine to
`216.247.206.76:2593` succeeds. **Cost: it is a literal.** When the ISP changes the address, ddns fixes DNS within
5 minutes but every stock client breaks until you edit this line and restart. Package users are unaffected either
way. Your call; my recommendation is to leave live as it is and point people at the package.

**Why the hostname does not work instead:** inside the container, `shatteredlegacyuo.com` resolves to
**`192.168.1.58`** (`docker exec sl-modernuo-test getent hosts shatteredlegacyuo.com`), because the router answers
that name with the LAN address. `serverListing.address: "shatteredlegacyuo.com"` would therefore advertise exactly
what it advertises today.

### A.2, the account limit

It is **one limit for the whole shard, not five per household.** Every account is counted against `172.19.0.1`, so
the limit is the total number of accounts auto-creation can ever make. **Measured on a copy of live's accounts:
4 more can be created, then everyone is refused.** Recommended:

```json
"accountHandler.maxAccountsPerIP": "25",
```

Expected effect after a restart: 24 more accounts can be created (one live account already counts), after which new
names are refused as now. Why 25 rather than "unlimited": auto-creation is open to the internet, and this setting is
now the only ceiling on account spam, because the per-IP rate limiter exempts private addresses and so exempts
everyone (`IPRateLimiter.Verify` returns early on `IsPrivateNetwork`, `IPRateLimiter.cs:59`; read, not probed). 25
covers a family with room for alts. Raise it when it bites; it is one line.

---

## Part A: the evidence

### A.1: the brief's code reading is right, and its premise is not

Pinned `Misc/ServerList.cs`, as the brief said: a non-null `serverListing.address` sets
`_useServerListingAddressConfig` (`:64-68`), and `OnServerListEvent` then uses that address for everyone (`:91-94`).
The per-client branch (`:95-102`) only swaps in the public IP when **`!ns.Address.IsPrivateNetwork()`**, meaning the
client's address as ModernUO sees it.

What ModernUO sees:

- `docker logs sl-modernuo`: **34 of 34** `Client:` lines are `172.19.0.1`.
- Test shard: probes from `127.0.0.1` and from `192.168.1.58` were both logged as `172.19.0.1`.
- `172.19.0.1` is inside `172.16.0.0/12`, which `NetworkUtilities.IsPrivateNetworkV4` (`:22`) counts as private.
- The container's own end is `172.19.0.x:2593` (`Listening:` lines), also private.

So with `autoDetect`, `localAddress` is private, the client looks private, no swap happens, and the relay carries the
container's address. **Probed, not deduced:** test shard set to `address: null`, `autoDetect: "True"`, restarted,
logged in with a protocol probe: `server list ... listed ip 172.19.0.2`, `RELAY 0x8C -> 172.19.0.2:2594`. Reverted
and re-probed: `RELAY 0x8C -> 192.168.1.58:2594`.

The brief's three questions:

- **Does autoDetect give LAN clients the LAN address and internet clients the public one?** No, on this code path it
  gives both the container's address. Upstream's advice assumes the server sees real client addresses, which is true
  on bare metal or Docker with host networking, and false under Docker Desktop's port publishing.
- **ipify once at startup?** Yes. `AutoDetection()` is called only from `Initialize()` (`:55-60`) and `_publicAddress`
  is never written again. A changed public IP stays stale until a restart. Moot here, because that branch never fires.
- **Can a LAN client be relayed to the public IP?** Under autoDetect, no; it gets the container address, which is
  worse. Under the literal-IP option above, yes, all of them, and that needs hairpin NAT. Measured working today for
  2593: TCP connect to `216.247.206.76:2593` from this LAN machine succeeds. The same test on 2594 fails, which is
  what we want (the router forwards 2593 only).

**DNS, which the brief did not know about:** public resolvers say `shatteredlegacyuo.com` is `216.247.206.76`
(Cloudflare and Google DNS-over-HTTPS). Inside the house, every lookup, even one addressed to `1.1.1.1` on port 53,
comes back `192.168.1.58`, because the UniFi router answers it. That is why the package's default target works from
inside the house without hairpinning, and why `-Lan` is a convenience rather than a necessity.

### A.2: how the limit is counted

`AccountHandler.CanCreate(ip)` (`Accounting/AccountHandler.cs:242`) compares `IPTable[ip]` against
`maxAccountsPerIP`. `IPTable` counts each account once, under the **first** entry of its `LoginIPs` (`:42-45`,
incremented in `Account.LogAccess` when `LoginIPs` is empty, `Account.cs:1044-1048`). It is checked **only when
creating an account**, in `CreateAccount` (`:262`). Existing accounts keep logging in regardless. The IP is
`NetState.Address`, the TCP peer as ModernUO sees it: `172.19.0.1` for everyone, relayed or not.

**What the sixth person sees:** the server logs `Account 'x' not created, ip already has 5 accounts` and rejects the
login with `ALRReason.BadComm` (255). TazUO clamps 0x82 codes above 8 to 8 (`ServerErrorMessages.cs`), which is
cliloc 3000037, **"Couldn't connect to Ultima Online. Please try again in a few moments."** That is misleading,
because trying again never works. The README tells players to tell Chase instead of waiting.

**Proven on the test shard.** Its save held 2 accounts first seen from `172.19.0.1`; the probe created 3, and the
4th was refused with reason 255 and that log line. After `-Fresh` (an exact copy of live's accounts, from live's
18:10 save) it created 4 and refused the 5th: **live has room for 4 more accounts, shard-wide.**

---

## Part B: the test shard, reachable from the LAN

### What changed (shard repo)

- `docker/uo/docker-compose.test.yml`: `"2594:2594"` (tcp and udp) instead of `"127.0.0.1:2594:2593"`, with a
  comment saying why the ports must match.
- `Configuration-test/modernuo.json` (not tracked): `listeners` `0.0.0.0:2594`, `serverListing.address`
  `192.168.1.58`. Migrated in place from `0.0.0.0:2593` / `127.0.0.1`, and it keeps no BOM.
- `docker/uo/Start-TestShard.ps1` and `docker/uo/test-shard.sh`: both apply that shape **on every run**, so a fresh
  seed gets it and an old copy migrates. Both refuse to start if the file still mentions `:2593"` afterwards. The PS
  script no longer writes the file with `Set-Content -Encoding UTF8`, which added a BOM. New `-SkipBuild` switch to
  start the existing image without `build.sh`, which I needed so as not to tag `latest`. It can also be used on its
  own.

### Proof

| Check | Before | After |
|---|---|---|
| `192.168.1.58:2594` from this machine | closed | open |
| relay from a probe login via `127.0.0.1:2594` | by reading the old config (not probed): `127.0.0.1:2593`, which on this host **is the live shard**. The trap the brief described was already armed; only the launchers' `ignore_relay_ip` kept test clients off live | `192.168.1.58:2594` |
| relay via `192.168.1.58:2594` | unreachable | `192.168.1.58:2594` |
| `216.247.206.76:2594` (from outside, via hairpin) | closed | closed |
| live `sl-modernuo` | Up | Up, not restarted (uptime ran through the whole task) |

**Not proven from a second machine.** None was available to me. WSL has only the `docker-desktop` distro, and I did
not probe other hosts on the LAN. What stands in for it: the firewall rule that admits LAN and internet traffic to
the live 2593, `Docker Desktop Backend`, is program-scoped (`com.docker.backend.exe`, TCP and UDP, any port, any
remote, Public profile, and the Ethernet profile is Public), so 2594 now gets the identical treatment. **Chase, from
any other machine in the house:**

```powershell
Test-NetConnection 192.168.1.58 -Port 2594
```

`TcpTestSucceeded : True` closes it.

### D19, `-Fresh` blocked at the owner prompt: fixed, and the failure is now loud

**Cause, probed:** `Persistence.Load` resolves every saved entity's type through `SerializedTypes.db`
(`Persistence.cs:39-53`). `-Fresh` seeded `Accounts/` without it, so every account hit `ctor == null → continue`
(`GenericEntityPersistence.cs:322`) silently, `Accounts.Count` was 0, and `AccountPrompt` blocked on stdin.
Reproduced by hand: a save holding only `Accounts/` printed `This server has no accounts` and the prompt.

**Fix:** both scripts seed `SerializedTypes.db` beside `Accounts/`. `-Fresh -SkipBuild` then loaded the accounts,
reached `Listening: ...:2594`, and never prompted.

**Detection:** after `compose up`, the PS script reads the log since the container's own `StartedAt` until it sees
either `Listening: ...:2594` or the prompt. On the prompt it prints the `docker attach` recipe (y, name, password,
detach with Ctrl+P Ctrl+Q, not Ctrl+C) and exits non-zero. **Watched failing:** run against a container stuck at the
prompt, it printed that and exited 1. `test-shard.sh` got the seed fix but not the detector.

### New defects, for `docs/bug-list.md` (D19 was the brief's; D20 is taken by `armour-set-completion.md`)

| # | What | Impact | Kind / where |
|---|---|---|---|
| **D19** | `-Fresh` blocked at the owner prompt | test shard unusable after `-Fresh` | ours. **Fixed** in this task (above) |
| **D21** | **Docker Desktop's port publishing hides every client address**: all connections arrive from `172.19.0.1`. So `ServerList` cannot tell LAN from internet, `maxAccountsPerIP` is a shard-wide total, and `IPRateLimiter` exempts everyone as private. Any per-IP ban or firewall entry in ModernUO is equally blind | A.1 and A.2 above; any future IP ban would ban everybody | ours (topology). Reverses when the shard runs with host networking, or on a Linux host where Docker preserves source addresses; neither is a small change. Until then, treat every per-IP feature as off |
| **D22** | `docker-compose.test.yml` and `docker-compose.yml` share compose project `uo` (same directory), so compose reports `sl-modernuo` and `sl-ddns` as **orphans of the test stack**. `docker compose -f docker-compose.test.yml down --remove-orphans` would stop the live shard | one flag away from a live outage | ours. One line: `name: sl-uo-test` at the top of the test file (then remove the old test container once by hand). Not done here: it changes the test stack's network and was outside the brief |
| **D23** | `sl-ddns` is `unhealthy` and "updates" Cloudflare every 10 minutes: it reads the record through the router's split DNS (`192.168.1.58`) and so never sees it as correct, although Cloudflare already holds `216.247.206.76` | API churn; a health status nobody can trust | ours. Likely fix: give ddns-updater a public resolver. Unverified which of its settings does that |

---

## Part C: the package

### Where things live, and why

- **Sources: `D:\ShatteredLegacy\player-package\`** (shard repo, tracked). It is shard infrastructure, like
  `docker/`. Not in `downloads/`, because `.gitignore` excludes the whole folder, so nothing there is tracked
  (`client-patcher` included).
  - `Build-PlayerPackage.ps1`: the builder, which runs on Chase's machine.
  - `payload\`: exactly what goes in the zip besides TazUO: `Play Shattered Legacy.bat`, `README.txt`,
    `app\Play.ps1`, `app\Setup.ps1`, `app\Play-Lan.bat`, `app\Play-Test.bat`, `app\Setup.bat`.
  - `LICENSE-TazUO.txt`: TazUO is BSD 2-Clause, and redistributing binaries requires shipping the notice.
- **Output: `player-package\dist\ShatteredLegacy-<date>.zip`**, gitignored (a line added to `.gitignore`). Kept out of
  `downloads/` too, because `docker/downloads` exists and may serve it; publishing is a separate decision for Chase.

### Contents (73 MB, 749 entries)

One top folder. `Play Shattered Legacy.bat`, `README.txt`, `app\` with the scripts and `VERSION.txt` (TazUO
`26.0909.63`, shard commit), and `app\tazuo\`: the TazUO client, **740 files copied byte-identical** from
`D:\UO\TazUO\client`. It excludes `settings*.json` (Chase's saved logins for every shard), `Data\` (profiles,
characters, journals, screenshots), `LegionScripts\` (Chase's `IR_*` scripts), `logs`, `Cache`, `*.pdb`, and
the macOS natives. **Nothing of EA's.** The TazUO *launcher* and updater are not shipped, only the client.

### How it behaves

- **`Play Shattered Legacy.bat`**: `-NoProfile -ExecutionPolicy Bypass -File app\Play.ps1`, and it pauses on error
  so the window does not vanish.
- **`Play.ps1`**: clears Mark of the Web from the package once. It runs `Setup.ps1`, TCP-checks the target (5 s) and
  says in plain words if it is down. It then writes the TazUO settings with no BOM, **preserving the player's saved
  username and password**, and forces only `ip`, `port`, `ultimaonlinedirectory`, `clientversion` (read from
  `client.exe`), `ignore_relay_ip: true` and empty `plugins`. `-Test` uses its own `settings.test.json` so a test
  login is never offered to live.
- **`Setup.ps1`**: looks in `app\uo-path.txt`, EA's registry key (`...\EA Games\Ultima Online Classic\InstallDir`,
  HKLM both views and HKCU), then the usual install folders. It requires 7 named files and **`client.exe` >= 7.0.114.40**,
  because the server kicks older (`clientVerification`). An installed but unpatched 7.0.24.0 therefore gets "open the
  UO launcher and let it finish updating", rather than a kick 20 seconds into the login screen. If nothing is found it
  asks, then reads `uo.com/client-download/` for the installer link. It downloads that installer only if the link
  is the one checked below and the SHA-256 matches, then unblocks and runs it interactively. Any mismatch or failure
  stops with the manual instructions, and nothing half-installed is left.

### EA's download, verified 2026-09-26

`https://uo.com/client-download/` links `https://downloads.eamythic.com/uo/installers/UOClassicSetup_7_0_24_0.exe`:
18,827,017 bytes, `Last-Modified 2021-03-26`, SHA-256 `c19f93f9...ba1ced7a6`, identical to the copy already in
`D:\UO`. **It is not Authenticode-signed** (`Get-AuthenticodeSignature`: `NotSigned`), so the pinned hash is the only
integrity check available. It is a 7.0.24.0 stub; EA's launcher then patches to current, which on this machine is
**7.0.117.0** (`D:\UO\UltimaOnlineVanilla\client.exe`, registered as EA's `InstallDir`).

**Admin rights: EA's installer, not ours, and unverified.** Its manifest says `asInvoker`, but it writes
`HKLM\SOFTWARE\WOW6432Node\Electronic Arts\...`, which a standard user cannot. I did not run it. The package itself
needs none. Setup and the README say any UAC prompt comes from EA.

### Client version: 7.0.117.0 against the server's 7.0.114.40

The server's data (`client-data/classic-client`, `client.exe` 7.0.114.40) and EA's current data (7.0.117.0) differ.
Hash-compared, 7.0.117.0 against the server's copy:

- **Same:** `facet02-05`, `map0x`, `multi.idx/.mul`, `Multimap.rle`, `staidx/statics` 2, 3, 4, 5 and the `x` variants.
- **Different:** `map0/1/1x/2/2x/3/4/5/5x LegacyMUL.uop`, `statics0/1` + `staidx0/1`, `tiledata.mul`, `hues.mul`,
  `radarcol.mul`, `MultiCollection.uop`, `facet00/01`.

Statics, parsed block by block: **338 of 458,752 blocks differ in Felucca and 1,149 in Trammel.** They are
concentrated in x 6144-7167, y 3072-3583 (the extended east edge) and around Skara Brae (x 736-1023, y 2120-2559).
**The land in the map UOPs is not compared** (hash-only; a UOP can differ in its container alone), so terrain is
unverified.

**What breaks:** where statics differ, the client draws what the server does not collide with, or the reverse:
walls you walk through, or invisible blockers, localised to those areas. **The server accepts the newer client**
(`Restricting client version to 7.0.114.40 or newer`), and the packaged client sat at the character list for 45
seconds without a kick. **What the package does about it: nothing, deliberately.** Pinning players to 7.0.114.40
would mean shipping EA's files, which the brief rules out. The real fix is server-side, and it is Chase's: **Q-063.**

### What I ran

From a **clean folder**: the zip extracted with `Expand-Archive`, then **every file stamped with
`Zone.Identifier ZoneId=3`**, which is what Explorer does after a browser download.

| Run | Result |
|---|---|
| `Play Shattered Legacy.bat` (default) | setup found `D:\UO\UltimaOnlineVanilla` via the registry; TCP check to `shatteredlegacyuo.com:2593` passed; `settings.json` written with no BOM; **TazUO started** (`[TazUO - 26.909.63.0]`, responding) and generated its `Data\` from the UO files; MOTW cleared. **Did not log in to live**: that would create an account on the live shard |
| `app\Play-Lan.bat` | `192.168.1.58:2593` passed the check; TazUO started. No login, same reason |
| `app\Play-Test.bat` | `settings.test.json` correct; then **the packaged TazUO, launched with that file plus only autologin credentials, logged in to the test shard: `Valid credentials for 'pkgprobe1'` → second connection → `Account 'pkgprobe1' at character list`.** The second connection is the relay, followed with `ignore_relay_ip` back to `:2594` |
| `app\Play-Test.bat`, test shard stopped | "Cannot reach TEST SHARD ... only runs when Chase starts it"; TazUO not started |
| `app\Setup.bat "C:\Windows"` | refused, listing the 7 missing files; saved path unchanged |
| `Setup.ps1 -DownloadOnly` | fetched the installer via the uo.com page; SHA-256 matched |

**Not done:** no character was created and nobody entered the world, because screen access for the client was
declined. So in-game behaviour is unobserved. I did not run EA's installer, so the "not installed" branch is proven
up to the download, not through installation. I did not run SmartScreen: MOTW is simulated, and SmartScreen only
fires for Explorer launches.

### Traps hit, and gates that now catch them

- **PowerShell 5.1 ignores `-Include` next to `-LiteralPath`** and returns every file. My first build pushed all 740
  client binaries through the CRLF text rewrite meant for `.bat` files. Windows refused the resulting `TazUO.exe`
  ("not a valid application for this OS platform"). **Caught only because the package was actually run.** Fixed with
  `Where-Object` on the extension, and a comment says why.
- **`ZipFile.CreateFromDirectory` on .NET Framework writes `\` separators**, which the zip spec forbids. Entries are
  now written with `/`; 0 of 749 contain `\`.
- The builder's three gates, **each watched red, then green**:
  1. *No personal data*: excluded by name, then every staged json/txt/ini/xml/cfg is scanned for a non-empty
     `username`/`password`. Red: `-GateSelfTest` plants a canary login and the build stops.
  2. *ASCII-only scripts*: red with a planted em dash in `Play.ps1`, which was then restored (hash checked).
  3. *Client byte-identical to source*: red when run with the `-Include` bug restored in a throwaway copy of the
     builder (735 of 740 differ).
- Traps 1-5 from the brief are handled: no BOM, ASCII-only, 5.1-only cmdlets, `.bat` wrappers, `Unblock-File`.
  Trap 6 is covered in the README. Trap 7 is above.

### Test-shard side effects, restored

`-Fresh` wiped the test world, so I backed it up first and restored it at the end. It is Chase's world from before,
running again on the new config. Probe accounts `pkgprobe1`-`3` exist in it (created before the backup), and on the
test shard only. `D:\UO\TazUO` was read, never written.

---

## Numbering

- **No D-number.** Nothing here deviates from OSI behaviour.
- **Bug-list D19** (brief's; fixed here), **D21, D22, D23** proposed. D20 was taken by
  `notes/armour-set-completion.md`, committed at 18:19 during this task.
- **Q-063.** The brief said Q-061 was free; the same concurrent commit took Q-061 and Q-062.
- Checked with `grep -rhoE "\b[DQ]-[0-9]+\b" notes docs | sort -u` after that commit landed.

## Reproducing

- Relay/login probe: a 70-line Python script speaking 0xEF, 0x80, 0xA0 and 0x8C unencrypted (this session's scratch;
  it belongs in `tools/` if it is wanted again): `python relayprobe.py HOST PORT ACCOUNT PASSWORD`.
- Statics diff: walk `staidxN.mul` 12-byte entries in both folders and compare each block's sorted 7-byte records.
- Package: `.\player-package\Build-PlayerPackage.ps1`, then `-GateSelfTest` after any change to the exclusions.
