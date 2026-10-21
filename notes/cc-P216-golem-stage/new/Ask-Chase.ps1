#Requires -Version 5.1
<#
  Ask-Chase.ps1 (cc-P216): a Golem session asks Chase a question it must stop for. The question goes on the consoles'
  Golem card (a button per choice, a text box when free text is allowed) and to Chase by email; his answer comes back to
  the Golem, which hands it to a new session for the same prompt. After asking, the session stops with
  P<nn> STOPPED: asked Chase (<id>).

      powershell -NoProfile -ExecutionPolicy Bypass -File D:\UO\golem\Ask-Chase.ps1 -Question "<the whole question>"
          [-Choice "<label>|<what you will then do>"] [-Choice2 "..."] [-Choice3 "..."] [-Choice4 "..."] [-NoText]
          [-Context "<what Chase needs to see>"]
          [-Irreversible] [-Prompt P<nn>] [-Golem <name>] [-Root D:\UO\golem]

  -NoText: only the choices may answer it (the default also takes Chase's own words). -Irreversible: an answer leads to
  something that cannot be undone (deleting saves, deploying live, pushing main by hand); the card says so, and the
  Golem also flags such words by itself. The session's GOLEM_NAME says which Golem asks; the prompt is the one it is
  running. Prints the question's id. Exit 0 asked; 1 refused (the reason is printed). ASCII only.
#>
param(
    [Parameter(Mandatory)][string]$Question,
    [string[]]$Choice = @(),   # one per parameter from a command line (-File cannot pass a list): -Choice, -Choice2..4
    [string]$Choice2 = '',
    [string]$Choice3 = '',
    [string]$Choice4 = '',
    [switch]$NoText,
    [string]$Context = '',
    [switch]$Irreversible,
    [string]$Prompt = '',
    [string]$Golem = '',
    [string]$Root = '',
    [string]$PromptDir = '',   # testing: a fixture prompt folder
    [switch]$NoMail            # testing: log the email instead of sending it
)
$Here = Split-Path -Parent $MyInvocation.MyCommand.Path   # the scripts; -Root is the Golem's folder (tests: a fixture)
if (-not $Root) { $Root = $Here }
if (-not $Golem) { $Golem = [string]$env:GOLEM_NAME }
. (Join-Path $Here 'Questions.ps1')
# Checked here first, so a bad choice is said to the session at once.
try { $ch = ConvertTo-QChoices (@($Choice) + @($Choice2, $Choice3, $Choice4)) } catch { Write-Host ('Not asked: ' + $_.Exception.Message); exit 1 }
if ($NoText -and -not $ch.Count) { Write-Host 'Not asked: -NoText needs at least one -Choice.'; exit 1 }
$f = Join-Path ([IO.Path]::GetTempPath()) ('ask-chase-' + [guid]::NewGuid().ToString('N') + '.json')
$j = [ordered]@{ question = $Question; choices = [object[]]$ch; freeText = (-not $NoText); context = $Context; irreversible = [bool]$Irreversible; prompt = $Prompt }
[IO.File]::WriteAllText($f, ($j | ConvertTo-Json -Depth 5), (New-Object Text.UTF8Encoding($false)))
try {
    $a = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', (Join-Path $Here 'golem.ps1'), '-Event', 'Ask', '-Root', $Root, '-AskFile', $f)
    if ($Golem) { $a += @('-Golem', $Golem) }
    if ($PromptDir) { $a += @('-PromptDir', $PromptDir) }
    if ($NoMail) { $a += '-NoMail' }
    $out = & powershell.exe @a
    $code = $LASTEXITCODE
} finally { Remove-Item -LiteralPath $f -Force -ErrorAction SilentlyContinue }
Write-Host (($out | Out-String).Trim())
exit $code
