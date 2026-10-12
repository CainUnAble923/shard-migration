#Requires -Version 5.1
# Pester (3.4, the one Windows ships) tests for tools\Import-PlayTests.ps1 and the rules in tools\playtests.py (cc-P83).
#
#     Invoke-Pester D:\UO\shard-migration\tools\tests\Import-PlayTests.Tests.ps1
#
# Each Context copies fixtures\playtests (four notes files shaped like the real ones, and three T-rows in
# docs\client-test-queue.md's own format) into a fresh temp root and runs the real script against it with
# -First 90, so the real notes folder is never read or written. Needs Python 3 on PATH, as the script does.

$here    = Split-Path -Parent $MyInvocation.MyCommand.Path
$script  = Join-Path (Split-Path -Parent $here) 'Import-PlayTests.ps1'
$lib     = Join-Path (Split-Path -Parent $here) 'playtests.py'
$fixture = Join-Path $here 'fixtures\playtests'

function New-Root {
    $r = Join-Path ([IO.Path]::GetTempPath()) ('playtests-' + [guid]::NewGuid().ToString('N'))
    Copy-Item -LiteralPath $fixture -Destination $r -Recurse
    $r
}
function Invoke-Import([string]$Root, [switch]$WhatIf) {
    # A switch cannot cross -File as -WhatIf:$false (it arrives as a string), so it is added only when wanted.
    $a = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $script, '-Root', $Root, '-First', '90')
    if ($WhatIf) { $a += '-WhatIf' }
    $out = & powershell.exe @a 2>&1 | ForEach-Object { [string]$_ }
    [pscustomobject]@{ Code = $LASTEXITCODE; Lines = @($out); Text = ($out -join "`n") }
}
function Read-Doc([string]$Root) { Get-Content -LiteralPath (Join-Path $Root 'testing\play-tests.json') -Raw | ConvertFrom-Json }
function Get-Item2($Doc, [string]$Id) { @($Doc.items | Where-Object { $_.id -eq $Id })[0] }
function Set-Result([string]$Root, [string]$Id, [string]$Status, [string]$Note) {
    # The service's own call, so the result is set exactly as a click on the page sets it.
    $code = "import sys; sys.path.insert(0, r'" + (Split-Path -Parent $lib) + "'); import playtests as pt; pt.set_result(r'" + $Root + "', '" + $Id + "', '" + $Status + "', '" + $Note + "')"
    & python -B -c $code
}

Describe 'Import-PlayTests' {

    Context 'a P71-style numbered list after a deploy code block' {
        $root = New-Root
        $r = Invoke-Import $root
        $doc = Read-Doc $root
        It 'exits 0 and says what it added' {
            $r.Code | Should Be 0
            $r.Text | Should Match 'added P91-1: Nerve Strike'
        }
        It 'imports the three in-game steps, numbered by their place in the checklist' {
            @($doc.items | Where-Object { $_.prompt -eq 'P91' }).Count | Should Be 3
            # A short lead-in is a label; with no second ': ' after it, the rest is the step and nothing is 'expect'.
            (Get-Item2 $doc 'P91-2').label | Should Be 'Stable slots'
            (Get-Item2 $doc 'P91-2').what | Should Match '^Taming, Lore and Veterinary 200'
            (Get-Item2 $doc 'P91-2').expect | Should Be ''
        }
        It 'splits what to do from what should happen' {
            $i = Get-Item2 $doc 'P91-1'
            $i.what | Should Be 'Nerve Strike at Bushido 200 against a monster, twenty times'
            $i.expect | Should Match '^about one strike in twenty does not paralyze'
        }
        It 'reads the deploy version from the notes' {
            (Get-Item2 $doc 'P91-3').version | Should Be '2026.10.10'
        }
        It 'never takes a list from Headlines or Decisions' {
            $r.Text | Should Not Match 'Not a checklist'
        }
        Remove-Item -LiteralPath $root -Recurse -Force
    }

    Context 'a P67-style list mixed with deploy and docs steps' {
        $root = New-Root
        [void](Invoke-Import $root)
        $doc = Read-Doc $root
        $p92 = @($doc.items | Where-Object { $_.prompt -eq 'P92' })
        It 'keeps only the three play-tests' {
            $p92.Count | Should Be 3
            ($p92 | ForEach-Object { $_.text }) -join ' ' | Should Not Match 'docker tag|Promote to|Not a test'
        }
        It 'numbers them 1 to 3, not by the notes'' own step numbers' {
            ($p92 | ForEach-Object { $_.id }) -join ',' | Should Be 'P92-1,P92-2,P92-3'
            (Get-Item2 $doc 'P92-1').label | Should Be 'Carpentry'
        }
        It 'counts what it skipped' {
            $doc.prompts.P92.skipped | Should Be 3
        }
        Remove-Item -LiteralPath $root -Recurse -Force
    }

    Context 'a STOPPED prompt and an unparseable one' {
        $root = New-Root
        $r = Invoke-Import $root
        $doc = Read-Doc $root
        It 'skips a prompt whose notes end STOPPED, and says so' {
            @($doc.items | Where-Object { $_.prompt -eq 'P93' }).Count | Should Be 0
            $r.Text | Should Match "skip P93: notes do not end 'P93 DONE'"
        }
        It 'adds one "read the notes" item for a DONE prompt with nothing to parse' {
            $u = @($doc.items | Where-Object { $_.prompt -eq 'P94' })
            $u.Count | Should Be 1
            $u[0].id | Should Be 'P94-0'
            $u[0].what | Should Be 'P94: checklist not parsed, read the notes'
            $doc.prompts.P94.parsed | Should Be $false
        }
        Remove-Item -LiteralPath $root -Recurse -Force
    }

    Context 'the old T-rows' {
        $root = New-Root
        [void](Invoke-Import $root)
        $doc = Read-Doc $root
        It 'keeps their ids and status' {
            (Get-Item2 $doc 'T-001').status | Should Be 'open'
            (Get-Item2 $doc 'T-009').status | Should Be 'pass'
            (Get-Item2 $doc 'T-040').status | Should Be 'fail'
        }
        It 'finds the bug a Fail produced, even on a wrapped result line' {
            (Get-Item2 $doc 'T-040').bug | Should Be 'D41'
            $doc.summary.unloggedFails | Should Be 0
        }
        It 'never writes the .md file' {
            (Get-FileHash (Join-Path $root 'docs\client-test-queue.md')).Hash | Should Be (Get-FileHash (Join-Path $fixture 'docs\client-test-queue.md')).Hash
        }
        Remove-Item -LiteralPath $root -Recurse -Force
    }

    Context '-WhatIf' {
        $root = New-Root
        $r = Invoke-Import $root -WhatIf
        It 'prints what it would add and writes nothing' {
            $r.Text | Should Match '\(dry run\) added P91-1'
            $r.Text | Should Match 'Nothing was written'
            Test-Path (Join-Path $root 'testing\play-tests.json') | Should Be $false
        }
        Remove-Item -LiteralPath $root -Recurse -Force
    }

    Context 're-import with no change' {
        $root = New-Root
        [void](Invoke-Import $root)
        $file = Join-Path $root 'testing\play-tests.json'
        $before = (Get-FileHash $file).Hash
        $r = Invoke-Import $root
        It 'adds nothing and does not rewrite the file' {
            $r.Text | Should Match '(?m)^no change:'
            $r.Text | Should Not Match 'added '
            (Get-FileHash $file).Hash | Should Be $before
        }
        Remove-Item -LiteralPath $root -Recurse -Force
    }

    Context 'a result survives re-import, and a changed checklist is flagged' {
        $root = New-Root
        [void](Invoke-Import $root)
        Set-Result $root 'P91-2' 'fail' 'the 24th was accepted'
        Set-Result $root 'P91-1' 'pass' ''
        # The notes change after import: step 2's text is edited and a step is added at the end.
        $notes = Join-Path $root 'notes\cc-P91-numbered-list.md'
        $t = [IO.File]::ReadAllText($notes)
        $t = $t.Replace('The 24th is refused, and 23 fit.', 'The 25th is refused, and 24 fit.')
        $t = $t.Replace("the five lines.`n", "the five lines.`n4. Fire Horn: all four bard skills 200: damage close to 120.`n")
        [IO.File]::WriteAllText($notes, $t)
        $r = Invoke-Import $root
        $doc = Read-Doc $root
        It 'keeps every result' {
            (Get-Item2 $doc 'P91-2').status | Should Be 'fail'
            (Get-Item2 $doc 'P91-2').note | Should Be 'the 24th was accepted'
            (Get-Item2 $doc 'P91-1').status | Should Be 'pass'
        }
        It 'flags the changed step and keeps what it said before' {
            $i = Get-Item2 $doc 'P91-2'
            $i.textChanged | Should Be $true
            $i.previousText | Should Match 'The 24th is refused'
            $i.text | Should Match 'The 25th is refused'
            (Get-Item2 $doc 'P91-1').textChanged | Should Be $false
            $r.Text | Should Match 'text changed P91-2 \(result kept: fail\)'
        }
        It 'adds the new step at the end and never reorders' {
            (Get-Item2 $doc 'P91-4').what | Should Be 'all four bard skills 200'
            $ids = @($doc.items | Where-Object { $_.prompt -eq 'P91' } | ForEach-Object { $_.id }) -join ','
            $ids | Should Be 'P91-1,P91-2,P91-3,P91-4'
        }
        It 'lists the Fail at the top of the file and in SUMMARY.md' {
            $doc.summary.failed | Should Be 2
            @($doc.summary.failures | Where-Object { $_.id -eq 'P91-2' }).Count | Should Be 1
            (Get-Content -LiteralPath (Join-Path $root 'testing\SUMMARY.md') -Raw) | Should Match 'P91-2\*\* \(P91, [0-9T:-]+Z\) NOT LOGGED'
        }
        It 'does nothing more on a third run' {
            (Invoke-Import $root).Text | Should Match '(?m)^no change:'
        }
        Remove-Item -LiteralPath $root -Recurse -Force
    }
}
