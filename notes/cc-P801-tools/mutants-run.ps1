powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Take docker-build -Minutes 45 -Wait
& 'C:\Program Files\Git\bin\bash.exe' D:/UO/golems/Iron/shard-migration/notes/cc-P801-tools/run-mutants.sh
powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Use-GolemLock.ps1 -Release docker-build
