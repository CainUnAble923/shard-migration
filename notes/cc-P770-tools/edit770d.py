import os, sys
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kit770'))


def edit(path, pairs):
    raw = open(path, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in raw else '\n'
    s = raw.replace('\r\n', '\n')
    for old, new in pairs:
        n = s.count(old)
        if n != 1:
            sys.exit('%s: %d matches for %r' % (path, n, old[:90]))
        s = s.replace(old, new)
    open(path, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl))
    print('edited', path, repr(nl))


edit('Golems.ps1', [
(r"""function Test-GolemLocal($g) { ([string]$g.machine -ieq [string]$env:COMPUTERNAME) }""",
r"""function Test-GolemLocal($g) { ([string]$g.machine -ieq [string]$env:COMPUTERNAME) }
# cc-P770: is this Golem reached through its agent from here? On another PC, with an agent this console knows
# (remote\<name>\agent.json, written when its agent first reports). A command for it then goes to remote\<name>\commands.
function Test-GolemViaAgent([string]$Root, $g) {
    if (-not $g -or (Test-GolemLocal $g)) { return $false }
    Test-Path -LiteralPath (Join-Path $Root ('remote\' + [string]$g.name + '\agent.json'))
}"""),
])
edit('Set-RunNext.ps1', [
(r"""    if ($g -and -not (Test-GolemLocal $g)) {""", r"""    if (Test-GolemViaAgent $Root $g) {"""),
])
edit('Assign-Prompt.ps1', [
(r"""    if ($gR -and -not (Test-GolemLocal $gR)) {""", r"""    if (Test-GolemViaAgent $Root $gR) {"""),
])
t = 'tests/Lane.Tests.ps1'
edit(t, [
(r"""    Copy-Item -LiteralPath (Join-Path $p770Kit 'settings.json') -Destination $r
    $r""",
r"""    Copy-Item -LiteralPath (Join-Path $p770Kit 'settings.json') -Destination $r
    # Gold's agent reports to this console (the web console writes remote\Gold\agent.json when it first does).
    New-Item -ItemType Directory -Path (Join-Path $r 'remote\Gold') -Force | Out-Null
    [IO.File]::WriteAllText((Join-Path $r 'remote\Gold\agent.json'), '{"golem":"Gold"}')
    $r"""),
(r"""    Assert-True (($keys -join ',') -eq 'runnext,runnext-cancel') ('and its cancel: ' + ($keys -join ',') + ' ' + $o2)""",
r"""    Assert-True (($keys -join ',') -eq 'runnext,runnext-cancel') ('and its cancel: ' + ($keys -join ',') + ' ' + $o2)
    # Without an agent this console knows (a fixture's made-up PC, or an agent never set up), it stays a pick here, as before.
    Remove-Item -LiteralPath (Join-Path $r 'remote\Gold\agent.json') -Force
    . $Lib
    Assert-True (-not (Test-GolemViaAgent $r (Get-GolemByName (Read-GolemRegistry (Join-Path $r 'golems.json')) 'Gold'))) 'no agent.json: not through an agent'
    Assert-True (-not (Test-GolemViaAgent $r (Get-GolemByName (Read-GolemRegistry (Join-Path $r 'golems.json')) 'Iron')) -or $env:COMPUTERNAME -ine 'CHASES-TOWER') 'Iron on this tower: never through an agent'"""),
])
