"""cc-P682: the code copy's three small edits (Dockerfile, console fresh-world order, its fact), each by exact text."""
import sys

ROOT = "D:/UO/golems/Iron/ShatteredLegacy/"


def edit(rel, old, new):
    p = ROOT + rel
    s = open(p, encoding="utf-8", newline="").read()
    crlf = "\r\n" in s
    o, n = (old.replace("\n", "\r\n"), new.replace("\n", "\r\n")) if crlf else (old, new)
    if s.count(o) != 1:
        sys.exit(f"{rel}: expected one match, found {s.count(o)}")
    open(p, "w", encoding="utf-8", newline="").write(s.replace(o, n))
    print("edited", rel, "crlf" if crlf else "lf")


edit("docker/uo/Dockerfile",
     "COPY server/data/Decoration/ /build/modernuo/Distribution/Data/ShatteredLegacy/Decoration/\n",
     "COPY server/data/Decoration/ /build/modernuo/Distribution/Data/ShatteredLegacy/Decoration/\n"
     "# cc-P682 (SoS swap S10): the people of the author's new towns and keeps and the wild on his new land, in pinned's\n"
     "# spawn format beside pinned's own (Data/Spawns/sos/{towns,keeps,wild}), built by the stock [GenerateSpawners (made by\n"
     "# shard-migration notes/cc-P682-tools/build_spawns.py).\n"
     "COPY server/data/Spawns/ /build/modernuo/Distribution/Data/Spawns/\n")

edit("scripts/Shard-Console.ps1",
     "                New-StockStep ('[GenerateSpawners Data/Spawns/' + $f) 'Developer' 'pinned. A spawn file ported content comes through. Re-running replaces, not duplicates.'\n"
     "            }\n",
     "                New-StockStep ('[GenerateSpawners Data/Spawns/' + $f) 'Developer' 'pinned. A spawn file ported content comes through. Re-running replaces, not duplicates.'\n"
     "            }\n"
     "            # cc-P682 (SoS swap S10): the people of the author's new towns and keeps and the wild on his new land, our\n"
     "            # files in pinned's spawn format (server/data/Spawns/sos, made by shard-migration notes/cc-P682-tools).\n"
     "            (New-StockStep '[GenerateSpawners Data/Spawns/sos/**/*.json' 'Developer' 'pinned command, our data: the SoS new towns, keeps and new land (cc-P682). Re-running replaces, not duplicates.')\n")

edit("scripts/tests/Shard-Console.Tests.ps1",
     """Fact 'TheFreshWorldGroupIsTheFourteenSpawnFilesThenShameThenDespiseThenSave' {
    $fresh = @($groups | Where-Object { $_.Key -eq 'fresh' })[0]
    $c = @($fresh.Items)
    $spawn = @($c | Where-Object { $_.Command -like '`[GenerateSpawners *' })
    Assert-Equal 14 $spawn.Count 'reachability-audit section 5 lists twelve paths (the brief said ten); cc-P678 adds pre-UOML Haven''s two'
    $pinned = 'D:\\UO\\ModernUO-pinned\\Distribution'
    if (Test-Path $pinned) {
        foreach ($s in $spawn) {
            $rel = $s.Command.Substring('[GenerateSpawners '.Length)
            Assert-True (Test-Path (Join-Path $pinned $rel)) "$rel exists in pinned Distribution"
        }
    }
    $rest = @($c | Select-Object -Skip 14 | ForEach-Object { $_.Command })""",
     """Fact 'TheFreshWorldGroupIsTheFifteenSpawnStepsThenShameThenDespiseThenSave' {
    $fresh = @($groups | Where-Object { $_.Key -eq 'fresh' })[0]
    $c = @($fresh.Items)
    $spawn = @($c | Where-Object { $_.Command -like '`[GenerateSpawners *' })
    Assert-Equal 15 $spawn.Count 'reachability-audit section 5 lists twelve paths (the brief said ten); cc-P678 adds pre-UOML Haven''s two; cc-P682 the SoS set'
    Assert-Equal '[GenerateSpawners Data/Spawns/sos/**/*.json' $spawn[14].Command 'cc-P682: the SoS set, after the stock files'
    $pinned = 'D:\\UO\\ModernUO-pinned\\Distribution'
    if (Test-Path $pinned) {
        foreach ($s in @($spawn | Select-Object -First 14)) {
            $rel = $s.Command.Substring('[GenerateSpawners '.Length)
            Assert-True (Test-Path (Join-Path $pinned $rel)) "$rel exists in pinned Distribution"
        }
    }
    $rest = @($c | Select-Object -Skip 15 | ForEach-Object { $_.Command })""")
