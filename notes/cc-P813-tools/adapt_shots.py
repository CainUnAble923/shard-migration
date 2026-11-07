"""cc-P813: turn P762's isle-shots762.ps1 (copied as shots813.ps1) into this prompt's shot runner."""
p = r"D:\UO\golems\Iron\shard-migration\notes\cc-P813-tools\shots813.ps1"
s = open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)


rep("<#\n  isle-shots742.ps1", "<#\n  shots813.ps1 (cc-P813: the client is the built player package's own app\\tazuo, with its ExternalImages art and\n  gumps, and its own Build-UoOverrides.ps1 builds the records and land overrides as Play.ps1 does; stage813.py runs\n  beside it as the admin a Legion script asks for commands. From P762's) isle-shots742.ps1")
rep("    [string]$ClientSource = 'D:\\UO\\tazuo-sl-build\\client',",
    "    [Parameter(Mandatory)][string]$App,   # cc-P813: the unzipped package's app folder\n    [string]$ClientSource = '',")
rep("    [int]$Port = 2594,", "    [int]$Port = 2596,")
# the client: the package's own tazuo folder, as it ships (no art copied in: it is already there)
rep("""[void](& robocopy $ClientSource $client /MIR /XD Data LegionScripts Logs Screenshots /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
$artOut = Join-Path $client 'ExternalImages\\art'
New-Item -ItemType Directory -Path $artOut -Force | Out-Null
Copy-Item -Path (Join-Path $CodeRepo 'player-package\\vendor\\shattered-legacy-art\\art\\*.png') -Destination $artOut -Force
Say ('client: ' + $client + ', ' + @(Get-ChildItem -LiteralPath $artOut -Filter '*.png').Count + ' art PNGs')""",
    """if (-not $ClientSource) { $ClientSource = Join-Path $App 'tazuo' }
[void](& robocopy $ClientSource $client /MIR /XD Data LegionScripts Logs Screenshots /NFL /NDL /NJH /NJS /NP /R:1 /W:1)
$artOut = Join-Path $client 'ExternalImages\\art'
$gumpOut = Join-Path $client 'ExternalImages\\gumps'
Say ('client: ' + $client + ', ' + @(Get-ChildItem -LiteralPath $artOut -Filter '*.png').Count + ' art PNGs, ' + @(Get-ChildItem -LiteralPath $gumpOut -Filter '*.png').Count + ' gump PNGs')
foreach ($id in @(23211..23222)) { if (-not (Test-Path -LiteralPath (Join-Path $gumpOut "$id.png"))) { Say "MISSING gump $id.png in the package client" } }""")
a = s.index("$override = & (Join-Path $CodeRepo 'player-package\\payload\\app\\Build-UoOverrides.ps1')")
b = s.index("Say ('override: ' + $override)")
s = s[:a] + ("$override = & (Join-Path $App 'Build-UoOverrides.ps1') -UoDir 'D:\\UO\\UltimaOnlineVanilla' -OutDir $ovDir -ListDir $ovDir\n") + s[b:]
# the admin hands, started before the shots and stopped after
rep("# 4. the shots\n", """# 4. the shots, with stage813.py (the admin) beside them
$stageLog = Join-Path $Out 'stage813-console.txt'
$stage = Start-Process -FilePath 'python' -ArgumentList @('-P', ('"' + (Join-Path $PSScriptRoot 'stage813.py') + '"'), '--port', "$Port", '--bot', ('"' + $Bot + '"')) -WindowStyle Hidden -RedirectStandardOutput $stageLog -RedirectStandardError ($stageLog + '.err') -PassThru
Start-Sleep -Seconds 20
Say ('stage813: ' + ((Get-Content -Raw $stageLog -ErrorAction SilentlyContinue) -replace '\\s+', ' '))
""")
rep("$acc = $null\nSay 'done'", "$acc = $null\ntry { if (-not $stage.HasExited) { $stage.Kill() } } catch {}\nSay 'done'")
open(p, "w", encoding="utf-8").write(s)
print("ok")
