"""cc-P135 red-first for the console facts: one break at a time in scripts\\Shard-Console.ps1, the P135_ facts run,
the file restored and proved byte-identical by SHA-256. Writes redfirst-console.txt beside this script."""
import hashlib, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONSOLE = r'D:\ShatteredLegacy\scripts\Shard-Console.ps1'
FACTS = r'D:\ShatteredLegacy\scripts\tests\Shard-Console.Tests.ps1'
OUT = os.path.join(HERE, 'redfirst-console.txt')

BREAKS = [
    ('C1 the safety check lets any validate-art subcommand through (render included)',
     "-and @($Config.ArtSubcommands) -ccontains $sub -and", "-and"),
    ('C2 a reported exit code is not reported: exit 1 fails the run',
     "if ($code -ne 0 -and $s.Named -and $s.Named.Contains('ReportExit') -and $code -eq [int]$s.Named['ReportExit'])", "if ($false)"),
    ('C3 the child line drops -Body',
     "    if ($Body -match '^\\d{1,5}$') { $a += ' -Body ' + $Body }\n", ""),
    ('C4 Check a .vd with no body runs check-vd anyway instead of propose',
     "            if ($Body) {\n                if ($Body -notmatch", "            if ($true) {\n                if ($Body -notmatch"),
    ('C5 a map button no longer says the console cannot run the command',
     "        $steps.Add((New-PlanStep -Kind say -Text 'Type it in a client on the shard you mean; the console cannot run in-game commands. It reads and reports, and nothing it places outlives its timer.'))\n", ""),
    ('C6 the tab is added after Diagnostics instead of after World setup',
     "$worldPage, $artPage, $diagPage,", "$worldPage, $diagPage, $artPage,"),
    ('C7 the headless entry does not name the map and art family (its banner and plan say test)',
     "    if ($Action -like 'art.*' -or $Action -like 'map.*') { $sk = 'mapart' }\n", ""),
]


def sha(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def run_facts(label):
    env = dict(os.environ)
    env['SL_FACT_FILTER'] = 'P135_|TheFormBuildsFromACapture'
    p = subprocess.run(['powershell.exe', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', FACTS], capture_output=True, text=True, env=env, timeout=1200)
    lines = [l for l in (p.stdout + p.stderr).splitlines() if l.strip().startswith(('PASS', 'FAIL')) or 'facts,' in l or l.startswith('        ')]
    return lines


def main():
    original = open(CONSOLE, 'rb').read()
    h0 = sha(CONSOLE)
    report = ['cc-P135 red-first, console facts (SL_FACT_FILTER=P135_|TheFormBuildsFromACapture), %s' % CONSOLE, 'original sha256 %s' % h0, '']
    report.append('== baseline (unbroken)')
    report += run_facts('baseline')
    report.append('')
    for label, old, new in BREAKS:
        text = original.decode('ascii')
        if text.count(old) != 1:
            report.append('== %s: ANCHOR FOUND %d TIMES, SKIPPED' % (label, text.count(old)))
            continue
        open(CONSOLE, 'wb').write(text.replace(old, new).encode('ascii'))
        report.append('== BREAK %s' % label)
        try:
            report += run_facts(label)
        finally:
            open(CONSOLE, 'wb').write(original)
        report.append('restored, hash identical: %s' % (sha(CONSOLE) == h0))
        report.append('')
    report.append('== after the last restore')
    report += run_facts('final')
    report.append('final sha256 %s identical: %s' % (sha(CONSOLE), sha(CONSOLE) == h0))
    open(OUT, 'w', encoding='ascii', newline='\n').write('\n'.join(report) + '\n')
    print('\n'.join(report))


if __name__ == '__main__':
    main()
