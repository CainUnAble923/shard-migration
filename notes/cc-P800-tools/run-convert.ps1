#Requires -Version 5.1
# cc-P800: a saved old League sash meets a real world load, twice. The caller holds the test-shard lock.
param([string]$Image = 'sl-modernuo:cc-p800', [string]$Out = 'D:\UO\golems\Iron\shard-migration\notes\cc-P800-shots\convert')
$ErrorActionPreference = 'Continue'
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P800-tools'
$name = 'sl-p800-proof'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\run-tazuo.ps1" -Image $Image -Character 'Iron Old' -Script Convert800.py -Out $Out -MaxMinutes 5 -KeepShard
Copy-Item -LiteralPath 'D:\UO\golems\Iron\p740-proof\walk.log' -Destination (Join-Path $Out 'walk.log') -Force
# A real load, then a real login of the character, then a load and a login again: the second pair must change nothing.
$acc = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golem\Get-GolemTestAccount.ps1' -Golem Iron -Role admin -Json 2>$null | Select-Object -Last 1) | ConvertFrom-Json
foreach ($n in 1, 2) {
    docker restart $name | Out-Null
    for ($i = 0; $i -lt 90; $i++) {
        Start-Sleep -Seconds 2
        $l = docker logs --since 1m $name 2>&1 | Out-String
        if ($l -match 'Listening') { break }
    }
    Start-Sleep -Seconds 8
    & python -P "$t\login-probe.py" ([string]$acc.Username) ([string]$acc.Password) 'Iron Old' *> (Join-Path $Out "login-$n.txt")
    Start-Sleep -Seconds 3
    docker logs $name > (Join-Path $Out "load-$n.log") 2>&1
    "load and login $n done"
}
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\proof-shard.ps1" -Work 'D:\UO\golems\Iron\p740-proof\shard' -Down
