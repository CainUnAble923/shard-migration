# cc-P35: does the player package install everything on a clean Windows PC?

2026-10-03. Agent: Claude Code. Brief: `D:\UO\cc-prompts\cc-P35-clean-machine-test.md`. Runs after P44.

**Nothing committed, published or deployed.** No ssh, no container touched. EA's installer was not run. Git in
`D:\ShatteredLegacy` was read with `--no-optional-locks` only. Precondition checked: `player-package\` changed after P44
only in P44's own commit `8825eb8`, and that commit touches only the three files P44's notes list. Scratch:
`D:\UO\cc-p35-work\` (628 MB: two extracted test runs, the new build, dry-run output, a doctored zip). Sandbox run folders
go in `D:\UO\clean-test-results\`.

> **Headlines**
>
> 1. **The package does NOT install everything today. zlib.dll is real, and it breaks a clean PC.** The brief's fact 3
>    (zlib.dll is dead weight) is wrong for the shipped build. The shipped `ClassicUO.Utility.dll` P/Invokes `zlib`
>    (`compress`, `compress2`, `uncompress`, `zlibVersion`). TazUO loads `zlib.dll` **3.4 s after start, before the
>    login screen**, and with it `VCRUNTIME140.dll`, which Windows does not ship. On a PC with no Visual C++
>    Redistributable, the game should fail at start. The tek-director laptop almost certainly had the redistributable,
>    which is why nobody saw this.
> 2. **Fix: ship Microsoft's `vcruntime140.dll` app-local** in `app\tazuo\`. It is 14.50.35719.0, from Visual Studio
>    18's `VC\Redist` folder, and licensed for redistribution (section 3). It is proven to win the search: on this PC
>    TazUO loads it from `app\tazuo\` even though System32 has the newer 14.51.
> 3. **Gate 6 is in.** It was **red** on 2026.10.02.0840, naming both zlib.dll files and `VCRUNTIME140.dll`. It is
>    **also red on 2026.10.03.1316, Chase's current post-P44 build: do not publish 1316.** It is **green** on the new
>    build 2026.10.03.1332. Gates 1 to 5, `-CheckZip`, `-GateSelfTest` and both test files are green.
> 4. **Windows Sandbox is OFF on CHASES-TOWER**, so the B5 smoke test was not run. The setting to turn on is in
>    section 7. The kit is built and dry-run on the host; the first real boot is Chase's.
> 5. Fact 2's conclusion holds (VCRUNTIME140 is the only gap in the import tables). Its list of native libraries was
>    short: the zip has **29** native Windows binaries with imports, not four.

---

## 1. The import table (A1). Every non-shipped import and where it resolves

Scan: every `.dll`/`.exe` in `ShatteredLegacy-2026.10.02.0840.zip`, PE import tables parsed in PowerShell (the same code
is now gate 6). **294 PE files**: 172 IL-only .NET assemblies (only import `mscoree.dll`, which CoreCLR never resolves)
and 122 native or ReadyToRun x64 images. No 32-bit native file. 93 of the 122 are ReadyToRun framework assemblies with
**no** imports. The 29 that import something:

`clrgc, clrgcexp, clrjit, coreclr, createdump.exe, e_sqlite3, FAudio, FNA3D, hostfxr, hostpolicy, libgcc_s_seh-1,
libstdc++-6, libtheorafile, libvosk, libwinpthread-1, Microsoft.DiaSymReader.Native.amd64, mscordaccore,
mscordaccore_amd64_amd64_10.0.1226.42308, mscordbi, msquic, SDL3, System.IO.Compression.Native, TazUO.exe, zlib`, and
in `x64\`: `FAudio, FNA3D, libtheorafile, SDL3, zlib`.

Every distinct imported DLL (static unless marked), with what resolves it:

| Import | Resolves to | Imported by (count) |
|---|---|---|
| `SDL3.dll`, `libgcc_s_seh-1.dll`, `libstdc++-6.dll`, `libwinpthread-1.dll` | **shipped** in `app\tazuo\` | FAudio/FNA3D (4), libvosk chain (MinGW runtime) |
| **`VCRUNTIME140.dll`** | **nothing on a clean PC** (before this task) | `zlib.dll`, `x64\zlib.dll` |
| `kernel32, user32, gdi32, advapi32, ole32, oleaut32, shell32, ws2_32, winmm, imm32, version, setupapi, bcrypt, crypt32, ntdll, dbghelp, iphlpapi, secur32, sspicli, msvcrt` | Windows System32 | 29, 9, 2, 11, 7, 6, 3, 2, 3, 2, 2, 2, 1, 1, 2, 1 (createdump), 1, 1, 1, 10 |
| `rpcrt4` (delay), `oleaut32` (delay) | System32 | DiaSymReader.Native |
| `version` (delay), `api-ms-win-core-winrt-l1-1-0` (delay) | System32 / Windows API set | coreclr |
| `api-ms-win-crt-{convert,environment,filesystem,heap,locale,math,runtime,stdio,string,time,utility}-l1-1-0` | Universal CRT (`ucrtbase.dll`), part of Windows 10 and later | 15 at most each |

**The allowlist** (`player-package\native-import-allowlist.txt`, 33 entries: 21 DLLs, 11 UCRT API sets, 1 WinRT API set)
is exactly the system names above, nothing pasted. The brief's examples `dxgi`, `d3d11`, `d3dcompiler_47` and `dwmapi`
are **not** on it: nothing in the zip imports them (FNA3D reaches D3D through SDL at run time, not through its import
table). Each entry cites a Microsoft page. These are API reference pages whose Requirements table names the DLL with a
minimum client of Windows 10 or earlier, or the page noted below. A subagent opened every page, and the URLs are in the
allowlist file itself. Caveats it found:

- `oleaut32`: the pages name the DLL but have no minimum-client row.
- `version.dll`: the DLL row names the API set `api-ms-win-core-version-l1-1-0.dll`, and `version.dll` appears only
  in the page metadata.
- `dbghelp`: "included in all supported versions of Windows" (dbghelp-versions page). Only `createdump.exe` imports
  it.
- `msvcrt`: only an archived VS2008 page and the porting guide call it a Windows component. The current CRT page
  does not mention it.
- `api-ms-win-core-winrt-l1-1-0`: confirmed only on an archived Windows 10 API-set page. It is delay-loaded by
  coreclr.
- UCRT: learn.microsoft.com/cpp/windows/universal-crt-deployment says the UCRT is a Windows component and is used
  from System32 on Windows 10 and later.

Second line of evidence, a stock install: `Inside-Start.ps1` checks every allowlist name in the fresh sandbox (a System32
file for DLLs, `LoadLibraryW` for all) and writes the result into `baseline.txt`. **Not yet run on a clean box** (section
7). On this PC all 33 resolve (dry run).

**Loader rule gate 6 uses.** An import counts as shipped only if a file of that name is in `app/tazuo/`, the folder
TazUO.exe starts from. Microsoft's DLL search-order page says a DLL's dependencies are searched "as if they were loaded
by using only their module names", which for an unpackaged app means the application's folder and then System32
(learn.microsoft.com/windows/win32/dlls/dynamic-link-library-search-order). The importing file's own folder is not
counted: Windows searches it only under `LOAD_LIBRARY_SEARCH_DLL_LOAD_DIR`, which depends on the caller. Every shipped
dependency, including `x64\`'s SDL3, is also in `app\tazuo\`, so the strict rule loses nothing. Runtime proof of the rule
is in section 2.

## 2. zlib.dll (A2): loaded. Evidence

**Shipped assemblies.** I built a small metadata reader (`System.Reflection.Metadata`, in scratch) and ran it over all
**263 managed assemblies** in `D:\UO\TazUO\client` (TazUO 26.0909.63), including the plugins and IronPython. It listed
every ModuleRef, every P/Invoke whose module contains `zlib`, and every user string containing `zlib`.
- `ClassicUO.Utility.dll`, `SafeNativeMethods`: `zlib!zlibVersion`, `zlib!compress`, `zlib!compress2`,
  `zlib!uncompress` (two overloads). It also has a ModuleRef `libz`, the Unix name.
- `TazUO.dll` strings: a "managed zlib" option (`mog_tazuo_forcemanagedzlib`, `ManagedZlib`) that is **opt-in**, and a
  legacy `-zlib` launch argument. Native zlib is the default.
- IronPython's `zlib` is its own managed module (only user strings, no P/Invoke).
- So the brief's fact 3, read from upstream HEAD, does not hold for the build we ship.

**At runtime.** This answers only "is zlib.dll loaded", because VCRUNTIME140 is installed on this PC.
- Chase's own running TazUO (the 0840 package, logged in to TEST, started 13:20), read-only module list: `zlib.DLL`
  from `...\0840\app\tazuo\` and `VCRUNTIME140.dll` from `C:\WINDOWS\SYSTEM32\`.
- Scratch copy of **1316**, test shard address, no login: `zlib.DLL` from the scratch `app\tazuo\` **3.4 s after
  start**, before the login screen. TazUO loads it while reading the UO files, so it is not avoidable by never playing.
- Scratch copy of the **new 1332**: `zlib.DLL` at 3.4 s, and **`VCRUNTIME140.dll` 14.50.35719.0 from the scratch
  `app\tazuo\`**, not System32's 14.51. The app-local copy wins the search, so a PC with no redist will find it.

**Decision: loaded, so ship `vcruntime140.dll` app-local.** `zlib.dll` imports only `VCRUNTIME140.dll`, not
`vcruntime140_1.dll` (x64 C++ exception handling), so one file.
- Source: `C:\Program Files\Microsoft Visual Studio\18\Community\VC\Redist\MSVC\14.50.35710\x64\Microsoft.VC145.CRT\vcruntime140.dll`.
  That is version 14.50.35719.0, 123,472 bytes, SHA-256 `184146852727a9db4eea06178716bec3cdbb1015c911f6b0f915b184ad7775b2`,
  Authenticode Valid, Microsoft Corporation.
- Vendored at `player-package\vendor\vc-runtime\` with a `SOURCE.txt`. The build checks the hash and the signature,
  refuses if TazUO's folder ever brings its own copy, and gate 3 checks the shipped copy byte for byte.
- zlib.dll is zlib 1.2.11, linker 14.0. Any 14.x vcruntime runs code built with an older 14.x toolset.
- No exception entry is needed, and gate 3 is untouched (nothing excluded).

**Alternative not taken:** turn on TazUO's managed zlib and drop zlib.dll. That is a per-profile option, so the launcher
cannot set it before the first login. The only pre-login route is the `-zlib` argument, which TazUO's own strings call
legacy and crash-prone. Shipping the runtime changes nothing about how the game runs.

## 3. Licence for vcruntime140.dll

- learn.microsoft.com/visualstudio/releases/2026/redistribution (the target of `aka.ms/vs/18/redistribution`, which
  VS 18's own `Licenses\1033\Redist.txt` points to). It is the "Distributable Code" list for VS Enterprise,
  Professional, **Community** and Build Tools. Under "Visual C++ Runtime Files" it allows copying any file in
  `[VisualStudioFolder]\VC\redist` (except the `debug_nonredist` folders) with your program, unmodified, subject to the
  licence terms. Binaries from the public redist download pages are "limited to licensed Visual Studio users".
- learn.microsoft.com/cpp/windows/redistributing-visual-cpp-files: app-local deployment is allowed. Microsoft "don't
  recommend" it for servicing reasons, because Windows Update then cannot patch the copy.
- **For Chase to confirm, not a blocker:** the right to redistribute rests on his VS 18 Community licence (installed on
  CHASES-TOWER), whose own "Distributable Code" terms apply, for example no use of Microsoft's trademarks. I judged the
  terms clear enough to proceed rather than stop.
- README's "What is in here" now names the file, says it is Microsoft's and unmodified, and links the terms (4 lines).

## 4. Gate 6: runs

| Zip | Result |
|---|---|
| 2026.10.02.0840 (`-CheckZip`) | **RED**: `app/tazuo/x64/zlib.dll imports VCRUNTIME140.dll` and `app/tazuo/zlib.dll imports VCRUNTIME140.dll`. 122 native checked, 172 skipped |
| 2026.10.03.1316 (`-CheckZip`, Chase's post-P44 build) | **RED**, same two lines |
| 2026.10.03.1332 (fresh build into scratch, and `-CheckZip`) | **GREEN**: 123 checked (122 plus vcruntime140.dll), 172 skipped |
| 1332 with a made-up line `app/tazuo/gone.dll` in the exceptions file | **RED**: "names app/tazuo/gone.dll, which the zip does not hold". File restored byte for byte (hash-checked) |
| 1332 doctored with `app/Collect-Evidence.ps1` added | **RED (gate 4)**: "is part of the clean-test kit and must not ship" |

Other gates on the fresh build: gates 1 to 5 pass in the build; `-CheckZip` passes gates 4, 6 and 5; `-GateSelfTest`
stops at gate 1 as designed; `tests\Build-UoOverrides.Tests.ps1` 8/8; `tests\Launch-Settings.Tests.ps1` 13/13.

Skipped by gate 6, and stated in the code:
- `lib64/`, `osx*/`, `linux*/`, `*.so*` and `*.dylib`: never loaded on Windows.
- Files not named `.dll`/`.exe`.
- IL-only .NET assemblies.
- Exception-file entries (there are none).

Static **and** delay-load imports are both checked.

**Not covered by gate 6 (P/Invokes, which load lazily and are not in import tables):** `IronPython.Modules.dll`
P/Invokes `msvcr100` (a 2010 runtime, not on a clean PC, not shipped). It is used only by Python's `msvcrt` module
console functions (`_getch`, `_kbhit`, `_putch` and the like), so a player script that calls them would fail. That is
rare and was never in scope. Every other ModuleRef across the 263 assemblies is a Windows DLL, a shipped file, or a
Unix/macOS name.

## 5. The sandbox kit (Part B), `player-package\clean-test\`

| File | Runs | What |
|---|---|---|
| `Start-CleanTest.ps1` | host | Checks Sandbox (`WindowsSandbox.exe`, then the feature's state) and says plainly how to turn it on. `-Mode Published` (default) or `-Mode Build [-Zip]`: newest `dist\ShatteredLegacy-<stamp>.zip`, refused unless its sha256 and bytes match its `.version.json`. `-VGpu`. `-WriteOnly` writes the run folder without opening it. |
| `Inside-Start.ps1` | sandbox logon | `baseline.txt` first, then the zip (Build) or a `.url` shortcut (Published), `READ ME FIRST.txt` and Collect-Evidence on the desktop, then opens the README |
| `Collect-Evidence.ps1` + `.bat` | sandbox, by Chase | `evidence.txt` (`evidence-2.txt` and so on on reruns), and copies EA's `logs\*` to `results\ea-logs\` |
| `READ ME FIRST.txt` | | Chase's steps (section 6) |

Everything is ASCII. The build's gate 2 now reads `clean-test\` for non-ASCII too. Its CRLF half is in
`Start-CleanTest.ps1`: the repo stores LF (`.gitattributes eol=lf`), so it copies the kit into the run folder with CRLF
and refuses if any bare LF survives. That copy is what gets mapped **read only**, not `clean-test\` itself. The kit is
**excluded** from the zip because it lives outside `payload\`. **Gate 4** proves it, failing on any `clean-test/` path
or kit file name, shown red above.

**A run folder** `D:\UO\clean-test-results\<yyyyMMdd-HHmmss>\` holds `clean-test.wsb`, `kit\` (read only at
`C:\SL\kit`, plus `run.json` and the allowlist) and `results\` (read/write at `C:\SL\results`). In Build mode the zip's
folder is also mapped read only at `C:\SL\dist`. The `.wsb` generated by
`Start-CleanTest.ps1 -Mode Build -Zip D:\UO\cc-p35-work\dist\ShatteredLegacy-2026.10.03.1332.zip -WriteOnly` (run folder
`20261003-133443`):

```xml
<Configuration>
  <vGPU>Disable</vGPU>
  <Networking>Enable</Networking>
  <MemoryInMB>8192</MemoryInMB>
  <MappedFolders>
    <MappedFolder>
      <HostFolder>D:\UO\clean-test-results\20261003-133443\kit</HostFolder>
      <SandboxFolder>C:\SL\kit</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
    <MappedFolder>
      <HostFolder>D:\UO\clean-test-results\20261003-133443\results</HostFolder>
      <SandboxFolder>C:\SL\results</SandboxFolder>
      <ReadOnly>false</ReadOnly>
    </MappedFolder>
    <MappedFolder>
      <HostFolder>D:\UO\cc-p35-work\dist</HostFolder>
      <SandboxFolder>C:\SL\dist</SandboxFolder>
      <ReadOnly>true</ReadOnly>
    </MappedFolder>
  </MappedFolders>
  <LogonCommand>
    <Command>powershell.exe -NoProfile -ExecutionPolicy Bypass -File C:\SL\kit\Inside-Start.ps1</Command>
  </LogonCommand>
</Configuration>
```

Element names and values were checked against
learn.microsoft.com/windows/security/application-security/application-isolation/windows-sandbox/windows-sandbox-configure-using-wsb-file:
- `vGPU` and `Networking` take Enable, Disable or Default.
- `MemoryInMB` is a number of MB.
- `ReadOnly` takes true or false.
- `LogonCommand/Command` holds a single command.

The page contradicts itself on relative `HostFolder` paths, so every path here is absolute. `wsb.exe` exists from
Windows 11 24H2 (windows-sandbox-cli page). CHASES-TOWER is 25H2 build 26200, but the feature is off, so it is not
there.

**Mark of the Web (Build mode).** I read a real browser download's stream on this host: a public servuo.dev download in
Downloads. It is ASCII with no BOM, `[ZoneTransfer]`, `ZoneId=3`, then optional `ReferrerUrl` and `HostUrl`, CRLF
between lines and a single NUL after the last. Other downloads there carry only `ZoneId` and `HostUrl`. `Inside-Start`
writes exactly that form: `ZoneId=3`, `HostUrl=https://get.shatteredlegacyuo.com/ShatteredLegacy-Setup.zip`, NUL. The
dry run read back 94 bytes, 2 CRs, last byte `00`. Published mode needs none of this, and `evidence.txt` records the
real downloaded zip's stream so the two can be compared.

**Dry runs on the host** (paths pointed at scratch; nothing on Chase's desktop):
- `Inside-Start`: baseline written, correctly **NOT CLEAN** for this PC (dotnet 6 to 10, 32 VC++ uninstall keys,
  vcruntime loads, EA key present, RTX 4080). All 33 allowlist names ok. Zip copied, sha256 checked, stream written.
- `Collect-Evidence`: every section fills. It shows `password` as `<redacted>`. I fixed PS 5.1's `\u003c` escaping
  after the first dry run.

**The launcher does not log its window.** Play.ps1 and Setup.ps1 write nothing to a file, and only Update.ps1 keeps
`update-log.txt`. `evidence.txt` says so. No logging was added here. **Follow-up:** a transcript from Setup.ps1 would
turn step 2's notes into evidence.

## 6. Chase's steps (the same in `READ ME FIRST.txt`)

1. Extract the zip with right-click, Extract All. In Build mode it is already on the sandbox desktop, marked as
   downloaded. In Published mode, double-click "Download Shattered Legacy" first.
2. Double-click `Play Shattered Legacy.bat`. Say yes to EA's installer, tick EA's license yourself, accept the defaults,
   then touch nothing. The launcher waits for EA's patch (about 10 minutes) and carries on by itself. Note:
   - how long it took;
   - anything you had to click that README.txt did not mention;
   - whether Windows asked for permission once or twice;
   - whether EA's window closed by itself or the launcher printed "Close it yourself";
   - whether EA's installer started the patcher on its own.

   Collect-Evidence copies EA's `logs\patcher.*.Log` for you.
3. When the game opens, log in to live with a throwaway account name, make a character, walk a few steps, and open the
   paperdoll and backpack.
4. Leave the game running and double-click `Collect-Evidence.bat` on the sandbox desktop.
5. Screenshot anything that looked wrong. Close the sandbox only after Collect-Evidence says "Written": closing it
   throws everything away, including the patch.

Repeat steps 2 to 4 with `-VGpu` only if the first pass had a graphics problem.

## 7. B5 smoke test: NOT RUN, because Windows Sandbox is off

`Win32_OptionalFeature` reports `Containers-DisposableClientVM` with InstallState 2 (disabled), and
`WindowsSandbox.exe` is absent. Hyper-V (`Microsoft-Hyper-V-All`) and `VirtualMachinePlatform` are on, and a hypervisor
is present, so the hardware is ready. **The one setting, which is Chase's call because it needs a restart:** Start, type
"Turn Windows features on or off", tick **Windows Sandbox**, OK, restart. Or from an admin PowerShell:
`Enable-WindowsOptionalFeature -FeatureName Containers-DisposableClientVM -All -Online`
(learn.microsoft.com/.../windows-sandbox/windows-sandbox-install). `Start-CleanTest.ps1` prints the same. I did not
enable it.

## 8. Zip size

| Build | Bytes | Entries |
|---|---|---|
| 2026.10.02.0840 | 80,074,387 | |
| 2026.10.03.1316 (post-P44) | 80,079,461 | 977 |
| 2026.10.03.1332 (this task, scratch) | 80,139,908 | 978 |

1316 to 1332 adds 60,447 bytes: `vcruntime140.dll` compressed, plus the README lines. 1332 is in
`D:\UO\cc-p35-work\dist\`, not `dist\`. Its VERSION.txt says "+ uncommitted player-package changes", so Chase rebuilds
after committing.

## 9. Not verified

- Anything inside a real Windows Sandbox: that the LogonCommand runs and maps `C:\SL\...` as written, that WARP
  renders TazUO, that EA's installer and patcher run on a bare box, and that `baseline.txt` says CLEAN. In particular,
  I have not checked whether stock Windows 11 already has `vcruntime140.dll` in System32. `baseline.txt` reports it.
- That a PC with no redist fails on 1316 exactly as predicted. That is inferred from the import table and the load
  order, not watched. On 1332 the app-local copy loads first, so the outcome on a bare box should not depend on this.
- The VS Community licence condition (section 3).

## 10. Files

`D:\ShatteredLegacy\player-package\`:
- `Build-PlayerPackage.ps1`: +176/-1. Gate 6, vcruntime vendoring, gate 2 extended to `clean-test\`, gate 4 kit
  check, header docs.
- `payload\README.txt`: +4.
- New: `native-import-allowlist.txt`, `native-import-exceptions.txt` (comments only), `vendor\vc-runtime\`
  (`vcruntime140.dll`, `SOURCE.txt`), and `clean-test\` (5 files).

`D:\UO\shard-migration\docs\client-test-queue.md`: one row added, **T-049** (highest was T-048).

## 11. Checklist for Chase

0. **Turn on Windows Sandbox** (section 7) and restart. Without it, step 3 just prints how.
1. Run `Commit-ShardWork.ps1`. It picks up the `player-package\` changes above and the T-049 row.
2. Build the package (`player-package\Build-PlayerPackage.ps1`). Gate 6 must say passed. **Do not publish yet, and
   never publish 1316: it fails gate 6.**
3. `player-package\clean-test\Start-CleanTest.ps1 -Mode Build` and follow `READ ME FIRST.txt` in the sandbox.
4. Bring `evidence.txt` and `baseline.txt` (in `D:\UO\clean-test-results\<run>\results\`) back to the overseer chat.
5. If it passes, publish, then run `Start-CleanTest.ps1` once more in Published mode (real download, real Mark of the
   Web).

Scratch, safe to delete: `D:\UO\cc-p35-work\` (628 MB) and the write-only run folder
`D:\UO\clean-test-results\20261003-133443\`.
