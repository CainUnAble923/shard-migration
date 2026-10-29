#Requires -Version 5.1
<#
  ui.ps1 (cc-P731): drive the proof TazUO's own login screens by window messages (PostMessage: the real mouse and
  keyboard are never moved), for its character creation. Shots are the window as Save-LegionShot takes it; -X/-Y are
  pixels in that shot, turned into client coordinates here.

      ui.ps1 -Do start -Character <name>        (TazUO from p731-proof\tazuo\client, no Legion run until the world)
      ui.ps1 -Do shot -Name <name>              (p731-proof\ui\<name>.jpg)
      ui.ps1 -Do click -X <x> -Y <y> [-Double]
      ui.ps1 -Do type -Text <text>              (WM_CHAR per character)
      ui.ps1 -Do key -Key <virtual key code>    (e.g. 13 Enter, 8 Backspace)
#>
param(
    [Parameter(Mandatory)][ValidateSet('start', 'shot', 'click', 'type', 'key')][string]$Do,
    [string]$Character = '',
    [string]$Name = 'ui',
    [int]$X = 0, [int]$Y = 0,
    [string]$Text = '',
    [int]$Key = 13,
    [switch]$Double
)
$ErrorActionPreference = 'Stop'
. 'D:\UO\golem\LegionTest.ps1'
Add-Type -Namespace P731 -Name W -MemberDefinition @'
[DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h, uint m, IntPtr w, IntPtr l);
[DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
[DllImport("user32.dll")] public static extern bool ClientToScreen(IntPtr h, ref POINT p);
public struct RECT { public int L, T, R, B; }
public struct POINT { public int X, Y; }
'@
$work = 'D:\UO\golems\Iron\p731-proof'
$client = Join-Path $work 'tazuo\client'
$pidFile = Join-Path $work 'ui.pid'

function Win {
    $p = Get-Process -Id ([int](Get-Content $pidFile)) -ErrorAction Stop
    if ($p.MainWindowHandle -eq [IntPtr]::Zero) { throw 'no window' }
    $p.MainWindowHandle
}
function ToClient([IntPtr]$h, [int]$sx, [int]$sy) {
    $r = New-Object P731.W+RECT; [void][P731.W]::GetWindowRect($h, [ref]$r)
    $o = New-Object P731.W+POINT; [void][P731.W]::ClientToScreen($h, [ref]$o)
    @(($sx - ($o.X - $r.L)), ($sy - ($o.Y - $r.T)))
}

switch ($Do) {
    'start' {
        $settings = Join-Path $client 'settings.p731.json'
        $acc = (& powershell.exe -NoProfile -ExecutionPolicy Bypass -File 'D:\UO\golem\Get-GolemTestAccount.ps1' -Golem Iron -Role player -Json 2>$null | Select-Object -Last 1) | ConvertFrom-Json
        $set = New-LegionSettings '127.0.0.1' 2596 ([string]$acc.Username) (ConvertTo-CuoPassword ([string]$acc.Password)) 'D:\UO\UltimaOnlineVanilla'
        $set.autologin = $false   # stop at the character list: the new character is made there
        # the test-only creation plugin (p731-proof\plugin: sends create.bin's 0xF8 when the character list comes)
        $set.plugins = @('D:\UO\golems\Iron\p731-proof\plugin\out\P731Create.dll')
        [IO.File]::WriteAllText($settings, ($set | ConvertTo-Json -Depth 6), (New-Object Text.UTF8Encoding($false)))
        $acc = $null
        $override = Join-Path $work 'tazuo\uo-override\files-override.txt'
        $argv = @('-settings', ('"' + $settings + '"'), '-skiploginscreen', '-skipserverselect', '-lastcharactername', ('"' + $Character + '"'), '-uofilesoverride', ('"' + $override + '"'))
        $p = Start-Process -FilePath (Join-Path $client 'TazUO.exe') -ArgumentList $argv -WorkingDirectory $client -PassThru -RedirectStandardOutput (Join-Path $work 'tazuo-out.txt') -RedirectStandardError (Join-Path $work 'tazuo-err.txt')
        Set-Content -LiteralPath $pidFile -Value $p.Id -Encoding ASCII
        "started $($p.Id)"
    }
    'shot' {
        New-Item -ItemType Directory -Path (Join-Path $work 'ui') -Force | Out-Null
        $f = Join-Path $work ('ui\' + $Name + '.jpg')
        if (Save-LegionShot (Win) $f) { $f } else { 'no shot' }
    }
    'click' {
        $h = Win
        $c = ToClient $h $X $Y
        $l = [IntPtr](($c[1] -shl 16) -bor ($c[0] -band 0xFFFF))
        [void][P731.W]::PostMessage($h, 0x0200, [IntPtr]0, $l)       # WM_MOUSEMOVE
        Start-Sleep -Milliseconds 120
        $n = if ($Double) { 2 } else { 1 }
        for ($i = 0; $i -lt $n; $i++) {
            [void][P731.W]::PostMessage($h, 0x0201, [IntPtr]1, $l)   # WM_LBUTTONDOWN
            Start-Sleep -Milliseconds 60
            [void][P731.W]::PostMessage($h, 0x0202, [IntPtr]0, $l)   # WM_LBUTTONUP
            Start-Sleep -Milliseconds 90
        }
        "clicked client $($c[0]),$($c[1])"
    }
    'type' {
        $h = Win
        foreach ($ch in $Text.ToCharArray()) { [void][P731.W]::PostMessage($h, 0x0102, [IntPtr][int]$ch, [IntPtr]1); Start-Sleep -Milliseconds 40 }
        "typed $($Text.Length)"
    }
    'key' {
        $h = Win
        [void][P731.W]::PostMessage($h, 0x0100, [IntPtr]$Key, [IntPtr]1); Start-Sleep -Milliseconds 60
        [void][P731.W]::PostMessage($h, 0x0101, [IntPtr]$Key, [IntPtr]0xC0000001)
        "key $Key"
    }
}
