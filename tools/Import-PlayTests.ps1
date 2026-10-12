#Requires -Version 5.1
<#
  Import-PlayTests.ps1 (cc-P83) - brings every DONE prompt's in-game checklist into testing\play-tests.json.

      .\tools\Import-PlayTests.ps1            import, write play-tests.json and SUMMARY.md, print what was added
      .\tools\Import-PlayTests.ps1 -WhatIf    print what would be added; write nothing

  It scans notes\cc-P*.md (P56 and later), imports each prompt whose notes end with the line "Pnn DONE", and
  merges it in. Idempotent: running it again adds nothing, never resets a result and never reorders. The T-rows
  of docs\client-test-queue.md are imported once; that file is never written.

  The rules live in tools\playtests.py, which this runs. The play-test service (D:\ShatteredLegacy\docker\
  test-queue\server.py) imports the same file and runs it every 60 s, so there is one parser, not two that
  drift. You rarely need this script: it is for -WhatIf, for a run while the service is down, and for the tests.

  Needs Python 3 on PATH (python or py). ASCII only.
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$Root,
    [int]$First = 56
)

# Not a parameter default: Windows PowerShell 5.1 leaves $PSScriptRoot empty there.
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $Root) { $Root = Split-Path -Parent $here }
$lib = Join-Path $here 'playtests.py'
$py = $null
foreach ($c in @('python', 'py')) {
    $cmd = Get-Command $c -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($cmd) { $py = $cmd.Source; break }
}
if (-not $py) { Write-Host 'Python 3 was not found (python or py on PATH). Install it, or let the play-test service import.' -ForegroundColor Red; exit 2 }

$a = @('-B', $lib, 'import', '--root', $Root, '--first', [string]$First)
if ($WhatIfPreference) { $a += '--dry-run' }
& $py @a
exit $LASTEXITCODE
