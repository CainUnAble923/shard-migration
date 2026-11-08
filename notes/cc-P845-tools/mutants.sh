#!/usr/bin/env bash
# cc-P845: each fix put back as it was, one at a time; each must turn the bench fact red. Logs in mutant-logs/.
cd /d/UO/golems/Iron/shard-migration/notes/cc-P845-tools
mkdir -p mutant-logs
F='FullyQualifiedName~TutorialIsleCoastVerification'
run() { M_NAME=$1 M_FILE=$2 M_SED=$3 bash mutant.sh "$F" > mutant-logs/$1.txt 2>&1; }
run m1-crosswise-piece TutorialFarm.cs 's/BenchId = 0x0B2C;/BenchId = 0x0B2D;/'
run m2-no-swap TutorialFarm.cs 's/OldPipProps\.Concat\(crosswise\)/OldPipProps/'
echo ALLDONE > mutant-logs/done.txt
