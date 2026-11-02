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


edit('Remote-Agent.ps1', [
(r"""    Write-AgentLog ('  ' + [string]$cmd.key + ' exited ' + $code + ': ' + $last)
    @{ id = [string]$cmd.id; code = [int]$code; result = $last; lines = @($lines | Select-Object -Last 60) }""",
r"""    Write-AgentLog ('  ' + [string]$cmd.key + ' exited ' + $code + ': ' + $last)
    # cc-P770: a Run next, an answer or a retry is acted on by the watch (it wakes an idle Golem for its Run next pick), run
    # now through this PC's own Golem Watch task, whose session can open the terminal; this long-running agent's could not
    # (Gold, 11-01 14:39: "wt.exe ... Access is denied"). Without the task the watch's own 10 minutes still come.
    if ($code -eq 0 -and [string]$cmd.key -in @('runnext', 'answer', 'retry')) {
        $tr = (& schtasks.exe /run /tn 'Golem Watch' 2>&1 | Out-String).Trim()
        Write-AgentLog ('  the watch run now for it: ' + $(if ($LASTEXITCODE -eq 0) { 'Golem Watch started' } else { 'not started (' + $tr + '); the watch comes within 10 minutes' }))
    }
    @{ id = [string]$cmd.id; code = [int]$code; result = $last; lines = @($lines | Select-Object -Last 60) }"""),
])

edit('join/Sweep.ps1', [
("""'Codex lanes:'; & powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\\UO\\golem\\Codex.ps1 -Action lanes | ForEach-Object { '  ' + $_ }
""",
"""'Codex lanes:'; & powershell.exe -NoProfile -ExecutionPolicy Bypass -File D:\\UO\\golem\\Codex.ps1 -Action lanes | ForEach-Object { '  ' + $_ }
# cc-P770: questions open on the other PCs (their agents' copies in remote\\<Golem>\\questions.json); Answer-Question.ps1 -Id <id>
# -Choice <n> here sends the answer to that PC.
. D:\\UO\\golem\\Questions.ps1; $rq = @(Get-RemoteOpenQuestions 'D:\\UO\\golem')
'Remote questions: ' + $(if ($rq.Count) { [string]$rq.Count + ' open' } else { 'none open' })
foreach ($q in $rq) { '  ' + $q.Golem + ' ' + $q.Id + ' (asked ' + $q.AskedAt + '): ' + $(if ($q.Question.Length -gt 140) { $q.Question.Substring(0, 140) + '...' } else { $q.Question }); '    choices: ' + (@(for ($i = 0; $i -lt $q.Choices.Count; $i++) { [string]$i + ' ' + $q.Choices[$i] }) -join ' | ') + '; answer: Answer-Question.ps1 -Id ' + $q.Id + ' -Choice <n>' }
"""),
])
