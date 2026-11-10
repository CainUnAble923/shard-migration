#!/usr/bin/env bash
# cc-P862: the red runs, then green. RED 0: the facts with no Battle Chess code (the state before the change: they cannot
# even compile). RED 1-6: each mutant from make_mutants.py in place of its real file. GREEN: the real code.
# Output: probe-<label>.txt for each, and red-all.txt (the summary lines of all of them).
T=D:/UO/golems/Iron/shard-migration/notes/cc-P862-tools
cd "$T"
NOCODE=1 bash probe.sh red0-before > /dev/null
for m in m-rules__ChessRules.cs m-seed__BattleChessSeeder.cs m-game__BattleChessGame.cs m-board__BattleChessBoard.cs \
         m-records__BattleChessRecords.cs m-settings__BattleChessSettings.cs; do
  bash probe.sh "red-${m%%__*}" "$m" > /dev/null
done
bash probe.sh green > /dev/null
{
  for f in probe-red0-before.txt probe-red-m-rules.txt probe-red-m-seed.txt probe-red-m-game.txt probe-red-m-board.txt \
           probe-red-m-records.txt probe-red-m-settings.txt probe-green.txt; do
    echo "=================== $f"
    grep -E 'mutant:|no Battle Chess|Build (succeeded|FAILED)|^\s+(Passed|Failed) ShatteredLegacy[^[]*$|Total tests|Passed:|Failed:|error CS' "$f" | head -30
  done
} > red-all.txt
echo done
