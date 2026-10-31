"""cc-P690: shots690.ps1 from P716's shots.ps1: TazUO from the BUILT PACKAGE (its app\tazuo, and the override list its
own launcher built in tazuo-pkg.ps1: the SoS land) on the fresh world's private shard. python -P edit_shots690.py"""
import os

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "shots690.ps1")
s = open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)


rep("  shots.ps1 (cc-P716:", "  shots690.ps1 (cc-P690: the package's own TazUO and override list, the fresh world; from P716's shots.ps1) shots.ps1 (cc-P716:")
rep("[string]$Work = (Join-Path $env:TEMP 'p675-proof'),", "[string]$Work = 'D:\\UO\\golems\\Iron\\p690-proof\\shots-work',")
rep("[string]$Container = 'sl-p675-proof',", "[string]$Container = 'sl-p690-proof',")
rep("[string]$ClientSource = 'D:\\UO\\golems\\Iron\\tazuo-p670\\client'   # cc-P675: P674's client build (patch 0008); the shared one is stale",
    "[string]$ClientSource = 'D:\\UO\\golems\\Iron\\p690-proof\\package-on\\ShatteredLegacy-2026.10.31.1102\\app\\tazuo',   # cc-P690: the package's client\n"
    "    [string]$PackageOverride = 'D:\\UO\\golems\\Iron\\p690-proof\\package-on\\ShatteredLegacy-2026.10.31.1102\\app\\uo-overrides\\files-override.txt'")
a = s.index("$ovDir = Join-Path $Work 'uo-override'")
b = s.index("Say ('override: ' + $override)")
s = s[:a] + "# cc-P690: the package's own override list (its launcher built it from the player's UO folder: the SoS land)\n$override = $PackageOverride\n" + s[b:]
rep("'settings.p675.json'", "'settings.p690.json'")
open(p, "w", encoding="utf-8").write(s)
print("ok")
