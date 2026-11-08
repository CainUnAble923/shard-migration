# cc-P846: the lodge shots on the private proof shard (2596) with the package client and the release copy's map.
& powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'shots823.ps1') `
    -Spec (Join-Path $PSScriptRoot 'shots846.json') -Out 'D:\UO\golems\Iron\shard-migration\notes\cc-P846-shots' `
    -CodeRepo 'D:\UO\golems\Iron\p846-isle' -Bot 'D:\UO\golems\Iron\p823-proof\bot' `
    -Work 'D:\UO\golems\Iron\p846-proof\work' -Port 2596 -App 'D:\UO\golems\Iron\p846-pkg\app' *> 'D:\UO\golems\Iron\p846-proof\shots-console.txt'
"EXIT=$LASTEXITCODE" | Out-File -Append -FilePath 'D:\UO\golems\Iron\p846-proof\shots-console.txt'
