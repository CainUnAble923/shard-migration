# cc-P867: take the docker-build lock, run gated-build.ps1, release the lock.
$t = 'D:\UO\golems\Iron\shard-migration\notes\cc-P867-tools'
$lock = 'D:\UO\golem\Use-GolemLock.ps1'
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Take docker-build -Minutes 60 -Wait
powershell -NoProfile -ExecutionPolicy Bypass -File "$t\gated-build.ps1"
powershell -NoProfile -ExecutionPolicy Bypass -File $lock -Release docker-build
