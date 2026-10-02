"""cc-P28: break the launcher one way at a time, run Launch-Settings.Tests.ps1, restore.

    python notes/cc-P28-tools/mutate_launcher.py [m1 m2 ...]

Each mutation is an exact, single-occurrence text replacement. Every file is restored
from its original bytes and checked by SHA-256 after each run, pass or fail.
"""
import hashlib, subprocess, sys, pathlib

APP = pathlib.Path(r"D:\ShatteredLegacy\player-package\payload\app")
TESTS = r"D:\ShatteredLegacy\player-package\tests\Launch-Settings.Tests.ps1"

M = {
    "m1": ("Launch-Settings.ps1", "        $s.saveaccount = $false; $s.autologin = $false", "        # mutated: plain -Test no longer forces them off"),
    "m2": ("Launch-Settings.ps1", "        $s.saveaccount = $true; $s.autologin = $true", "        # mutated: a profile no longer turns them on"),
    "m3": ("Launch-Settings.ps1", "$Account -cnotmatch '^[a-z0-9-]{1,24}$'", "$Account -notmatch '^[a-z0-9-]{1,24}$'"),
    "m4": ("Launch-Settings.ps1", "    if ($hasAccount -and -not $Test) { throw", "    if ($false) { throw"),
    "m5": ("Launch-Settings.ps1", "        $t.SettingsName = \"settings.test.$Account.json\"", "        # mutated: profile shares settings.test.json"),
    "m6": ("Play.ps1", "if ($target.Profile) { $tazArgs += '-skiploginscreen' }", "# mutated: no -skiploginscreen"),
    "m7": ("Update.ps1", "if ($Account) { $playArgs += @('-Account', $Account) }", "# mutated: relaunch drops -Account"),
}

def sha(b): return hashlib.sha256(b).hexdigest()[:12]

for key in (sys.argv[1:] or list(M)):
    fname, old, new = M[key]
    p = APP / fname
    orig = p.read_bytes()
    text = orig.decode("ascii")
    assert text.count(old) == 1, (key, text.count(old))
    try:
        p.write_bytes(text.replace(old, new).encode("ascii"))
        r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", TESTS],
                           capture_output=True, text=True)
        fails = [l.strip()[6:] for l in r.stdout.splitlines() if l.strip().startswith("FAIL")]
        print(f"{key} {fname}: exit {r.returncode}; failed: {', '.join(fails) or 'NONE'}", flush=True)
    finally:
        p.write_bytes(orig)
        assert sha(p.read_bytes()) == sha(orig)
        print(f"   restored {fname} {sha(orig)}", flush=True)
