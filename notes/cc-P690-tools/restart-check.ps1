# cc-P690: restart the private fresh world once (SaveOnShutdown saves on SIGTERM), then read the boot: the load, the
# seeders that run at load (Royal City's moongate, after [MoonGen deleted it), Eodon's gate check. The caller holds the
# test-shard lock. Output: <p690-proof>\restart-check.txt (the owner's password is not in a reboot's log: no prompt).
$ErrorActionPreference = 'Continue'
$name = 'sl-p690-proof'
$out = 'D:\UO\golems\Iron\p690-proof\restart-check.txt'
$since = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
"restart at $since" | Out-File -FilePath $out -Encoding ascii
docker restart -t 60 $name | Out-Null
for ($i = 0; $i -lt 120; $i++) {
    Start-Sleep -Seconds 2
    $l = (docker logs --since $since $name 2>&1 | Out-String) -replace "\x1b\[[0-9;?]*[a-zA-Z=>]", ''
    if ($l -match 'Listening:') { break }
}
$l -split "`r?`n" | Where-Object { $_ -match 'Loading world|World: |Save|saved|RoyalCity|Eodon|moongate|Tutorial\]|New Haven seed|Rootdeep|Blackthorn|error|Exception|Listening:' } |
    ForEach-Object { $_.Substring(0, [Math]::Min(240, $_.Length)) } | Out-File -FilePath $out -Append -Encoding ascii
Get-Content $out
