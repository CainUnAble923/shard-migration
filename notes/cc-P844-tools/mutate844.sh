#!/usr/bin/env bash
# cc-P844: the bench fact red on two mutants (m1: BenchId back to 0x0B2D; m2: the seeder skips TakeAwayOldPipBench), then green.
S=C:/Users/ckfle/AppData/Local/Temp/claude/136edbd9b201f108/f2fe8515-6261-49d3-bffd-e5af4a72dee6/scratchpad
H=$(dirname "$0")
F='FullyQualifiedName~TutorialIsleCoastVerification'
SRC=$S/m1 bash "$H/probe.sh" "$F" > "$H/red-m1.txt" 2>&1
SRC=$S/m2 bash "$H/probe.sh" "$F" > "$H/red-m2.txt" 2>&1
bash "$H/probe.sh" "$F" > "$H/green-probe.txt" 2>&1
echo finished
