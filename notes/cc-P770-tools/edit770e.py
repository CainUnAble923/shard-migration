import os, sys
os.chdir('kit770')
def edit(path, pairs):
    raw = open(path, encoding='utf-8', newline='').read(); nl = '\r\n' if '\r\n' in raw else '\n'; s = raw.replace('\r\n', '\n')
    for old, new in pairs:
        n = s.count(old)
        if n != 1: sys.exit('%s: %d matches for %r' % (path, n, old[:80]))
        s = s.replace(old, new)
    open(path, 'w', encoding='utf-8', newline='').write(s.replace('\n', nl)); print('edited', path)
edit('Answer-Question.ps1', [(
"if ($Source -eq 'remote') { Write-Host 'The watch wakes the Golem for it (the agent runs the watch now; else within 10 minutes).'; exit 0 }",
"if ($Source -eq 'remote' -and $env:GOLEM_AGENT -eq '1') { Write-Host 'The watch wakes the Golem for it (the agent runs the watch now; else within 10 minutes).'; exit 0 }")])
edit('Remote-Agent.ps1', [(
"    $eap = $ErrorActionPreference; $ErrorActionPreference = 'Continue'\n    $out = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $l.Script @($l.Args) 2>&1",
"    $eap = $ErrorActionPreference; $ErrorActionPreference = 'Continue'\n    $env:GOLEM_AGENT = '1'   # cc-P770: what it runs knows the agent ran it (Answer-Question.ps1 leaves the wake to the watch)\n    $out = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $l.Script @($l.Args) 2>&1")])
