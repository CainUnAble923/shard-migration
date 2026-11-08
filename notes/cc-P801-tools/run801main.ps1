# cc-P801: the jail lesson on main's image, private proof shard, under the test-shard lock.
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Take test-shard -Minutes 20 -Wait
Start-Process python -ArgumentList '-P D:\UO\golems\Iron\shard-migration\notes\cc-P801-tools\stage801.py --name "Iron Main"' -WindowStyle Hidden -RedirectStandardOutput D:\UO\golems\Iron\p740-proof\stage-out.txt -RedirectStandardError D:\UO\golems\Iron\p740-proof\stage-err.txt
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\UO\golems\Iron\shard-migration\notes\cc-P801-tools\main\run-tazuo.ps1 -Image sl-modernuo:cc-p801 -Character "Iron Main" -Script Walk801Main.py -Out D:\UO\golems\Iron\shard-migration\notes\cc-P801-review\shots-main -MaxMinutes 7
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Release test-shard
