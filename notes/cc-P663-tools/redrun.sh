#!/usr/bin/env bash
# cc-P663 red run: each per-fact revert (mutate.py) against the new facts; a summary per mutant in red-<name>.txt.
cd "$(dirname "$0")"
HERE="$(pwd -W 2>/dev/null || pwd)"
for m in order pets table choice step reconnect remedial cities golive; do
  TUT="$HERE/m-$m" timeout 1500 bash probe_full.sh "FullyQualifiedName~TutorialIsleVerification" > "red-raw-$m.txt" 2>&1
  {
    echo "== mutant $m"
    grep -E "error CS|^Total tests|Passed:|Failed:" "red-raw-$m.txt" | sort -u
    grep -E "^  (Passed|Failed) " "red-raw-$m.txt" | sed -E 's/ShatteredLegacy.Tests.TutorialIsleVerification.//; s/ \[[^]]*\]$//'
    python -I fails.py "red-raw-$m.txt"
  } > "red-$m.txt"
done
echo done > red-done.txt
