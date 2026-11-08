"""cc-P817: P762's creation762.ps1 as creation817.ps1: the client is a given TazUO folder (a package's app\\tazuo, or
a private client build with that package's ExternalImages copied in), and the overrides come from the package's own
Build-UoOverrides.ps1 (-App), as Play.ps1 makes them. Steps also take "wait" with fractions and a "burst" of shots."""
import os

src = r"D:\UO\golems\Iron\shard-migration\notes\cc-P762-tools\creation762.ps1"
dst = r"D:\UO\golems\Iron\shard-migration\notes\cc-P817-tools\creation817.ps1"
s = open(src, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:70]
    s = s.replace(a, b)


rep("<#\n  creation762.ps1 (cc-P762;", "<#\n  creation817.ps1 (cc-P817: the client from -ClientSource as given, its ExternalImages from -App's package, the\n  overrides from -App's own Build-UoOverrides.ps1; a \"burst\" step: { \"do\": \"burst\", \"name\": \"x\", \"n\": 6, \"ms\": 2000 }.\n  From creation762.ps1, cc-P762;")
rep("[string]$Account = ('p762n' + (Get-Random -Minimum 10000 -Maximum 99999)),",
    "[string]$Account = ('p817n' + (Get-Random -Minimum 10000 -Maximum 99999)),\n    [Parameter(Mandatory)][string]$App,")
rep("[string]$Work = 'D:\\UO\\golems\\Iron\\p762-proof\\tazuo',", "[string]$Work = 'D:\\UO\\golems\\Iron\\p817-proof\\tazuo',")
rep("[string]$ClientSource = 'D:\\UO\\tazuo-sl-build\\client'", "[string]$ClientSource = ''")
a = s.index("$client = Join-Path $Work 'client'")
b = s.index("Say ('override (with our clilocs")
s = s[:a] + """if (-not $ClientSource) { $ClientSource = Join-Path $App 'tazuo' }
$client = Join-Path $Work 'client'
[void](& robocopy $ClientSource $client /MIR /XD Data LegionScripts Logs Screenshots /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
# The package's own pictures, whatever client runs (a private build has none).
[void](& robocopy (Join-Path (Join-Path $App 'tazuo') 'ExternalImages') (Join-Path $client 'ExternalImages') /E /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
$ovDir = Join-Path $Work 'uo-override'
$override = & (Join-Path $App 'Build-UoOverrides.ps1') -UoDir 'D:\\UO\\UltimaOnlineVanilla' -OutDir $ovDir -ListDir $ovDir
""" + s[b:]
rep("$settings = Join-Path $client 'settings.p762.json'", "$settings = Join-Path $client 'settings.p817.json'")
rep("            'wait' { Start-Sleep -Seconds ([double]$s.s) }",
    """            'wait' { Start-Sleep -Milliseconds ([int]([double]$s.s * 1000)) }
            'burst' {
                for ($k = 1; $k -le [int]$s.n; $k++) {
                    $proc.Refresh(); $h = $proc.MainWindowHandle
                    $p = Join-Path $Out ([string]$s.name + '-' + $k + '.jpg')
                    if (Save-LegionShot $h $p) { Say ('shot: ' + $p) }
                    Start-Sleep -Milliseconds ([int]$s.ms)
                }
            }""")
s = s.replace("Add-Type -TypeDefinition @'\nusing System;\nusing System.Runtime.InteropServices;\npublic static class P762Post {",
              "Add-Type -TypeDefinition @'\nusing System;\nusing System.Runtime.InteropServices;\npublic static class P817Post {")
s = s.replace("[P762Post]", "[P817Post]")
open(dst, "w", encoding="utf-8").write(s)
print("ok", "P762Post" in s)
