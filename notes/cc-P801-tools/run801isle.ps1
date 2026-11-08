# cc-P801: the jail lesson on the release image, private proof shard, under the test-shard lock.
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Take test-shard -Minutes 20 -Wait
Start-Process python -ArgumentList '-P D:\UO\golems\Iron\shard-migration\notes\cc-P801-tools\stage801.py --name "Iron Stock"' -WindowStyle Hidden -RedirectStandardOutput D:\UO\golems\Iron\p740-proof\stage-out.txt -RedirectStandardError D:\UO\golems\Iron\p740-proof\stage-err.txt
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\UO\golems\Iron\shard-migration\notes\cc-P801-tools\run-tazuo.ps1 -Image sl-modernuo:cc-p801-isle -Character "Iron Stock" -Script Walk801Isle.py -Out D:\UO\golems\Iron\shard-migration\notes\cc-P801-review\shots-isle -MaxMinutes 7
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Release test-shard
