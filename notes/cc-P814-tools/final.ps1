# cc-P814: both gated builds under the docker-build lock, the red runs, then the walks under the test-shard lock.
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P814-tools'
$lock = 'D:\UO\golem\Use-GolemLock.ps1'
$proof = 'D:\UO\golems\Iron\p740-proof'
$review = 'D:\UO\golems\Iron\shard-migration\notes\cc-P814-review'
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Take docker-build -Minutes 40 -Wait
docker run --rm --privileged alpine:3.20 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\gated-build.ps1" -Repo 'D:\UO\golems\Iron\ShatteredLegacy' -Tag 'sl-modernuo:cc-p814' -Log "$t\gated-build.log"
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\gated-build.ps1" -Repo 'D:\UO\golems\Iron\p814-isle' -Tag 'sl-modernuo:cc-p814-isle' -Log "$t\gated-build-isle.log"
& 'C:\Program Files\Git\bin\bash.exe' "$($t -replace '\\','/')/red.sh"
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Release docker-build
$a = (Get-Content -Raw "$t\gated-build.log") -replace "`0",''
$b = (Get-Content -Raw "$t\gated-build-isle.log") -replace "`0",''
if ($a -match 'EXIT=0' -and $b -match 'EXIT=0') {
    powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Take test-shard -Minutes 25 -Wait
    Start-Process python -ArgumentList "-P $t\stage814.py --name `"Iron Stock`"" -WindowStyle Hidden -RedirectStandardOutput "$proof\stage-out.txt" -RedirectStandardError "$proof\stage-err.txt"
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\run-tazuo.ps1" -Image sl-modernuo:cc-p814-isle -Character "Iron Stock" -Script Walk814Isle.py -Out "$review\shots-isle" -MaxMinutes 6
    Copy-Item "$proof\walk.log" "$review\shots-isle\walk.txt" -Force
    Start-Process python -ArgumentList "-P $t\stage814.py --name `"Iron Main`"" -WindowStyle Hidden -RedirectStandardOutput "$proof\stage-out.txt" -RedirectStandardError "$proof\stage-err.txt"
    & powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$t\main\run-tazuo.ps1" -Image sl-modernuo:cc-p814 -Character "Iron Main" -Script Walk814Main.py -Out "$review\shots-main" -MaxMinutes 5
    Copy-Item "$proof\walk.log" "$review\shots-main\walk.txt" -Force
    powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Release test-shard
}
'done' | Out-File -FilePath "$t\final-done.txt"
