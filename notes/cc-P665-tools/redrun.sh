#!/usr/bin/env bash
# cc-P665 red run: each mutant (mutate.py) against the new facts; a summary per mutant in red-<name>.txt.
cd "$(dirname "$0")"
HERE="$(pwd -W 2>/dev/null || pwd)"
for m in ${MUTANTS:-shared clone norestore nosave loop panels}; do
  TUT="$HERE/m-$m" timeout 1500 bash probe.sh "FullyQualifiedName~TutorialVisionScene" > "red-raw-$m.txt" 2>&1
  {
    echo "== mutant $m"
    grep -E "error CS|^Total tests" "red-raw-$m.txt" | sort -u
    grep -E "^  (Passed|Failed) " "red-raw-$m.txt" | sed -E 's/ShatteredLegacy.Tests.TutorialVisionSceneVerification.//; s/ \[[^]]*\]$//'
  } > "red-$m.txt"
done
