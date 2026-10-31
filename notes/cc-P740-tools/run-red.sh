#!/usr/bin/env bash
# cc-P740: each mutant (mutate.py) against the P740 facts; red-<name>.txt per mutant.
OUTROOT="C:/Users/ckfle/AppData/Local/Temp/claude/D--UO-golems-Iron-shard-migration/05eadec1-1186-4790-a3c9-46bbeb603ba6/scratchpad/mutants"
cd "$(dirname "$0")"
python -P mutate.py "$OUTROOT" || exit 1
F="FullyQualifiedName~TutorialIsleWalkFixes4Verification|FullyQualifiedName~TutorialIsleBandageWaitVerification|FullyQualifiedName~TutorialIsleWakeVisibleVerification"
for m in olddark fastup noline lightfirst windowsearly notable nowren nohint hoard shortrise; do
  SRC="$OUTROOT/$m" timeout 900 bash probe.sh "$F" > "red-$m.txt" 2>&1
  echo "$m: $(grep -E '^\s+(Passed|Failed):' "red-$m.txt" | tr -s ' ' | tr '\n' ' ') $(grep -c 'error CS' "red-$m.txt") compile errors"
done
echo RED-DONE
