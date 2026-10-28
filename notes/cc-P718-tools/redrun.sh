#!/usr/bin/env bash
# cc-P718 red run: each mutant copy (mutate.py) against the new facts; summaries in red/red-<name>.txt.
cd "$(dirname "$0")"
MUT="${MUT:?set MUT to a scratch folder}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server/customizations"
mkdir -p red
for m in ${MUTANTS:-old fine fine2}; do
  python -I mutate.py "$CODE" "$MUT/m-$m" "$m" || { echo "mutate $m failed" > "red/red-$m.txt"; continue; }
  SRC="$MUT/m-$m" timeout 1500 bash probe.sh "FullyQualifiedName~TutorialIsleWalkFixesVerification" > "$MUT/raw-$m.txt" 2>&1
  {
    echo "== $m"
    grep -E "error CS|^Total tests|Passed:|Failed:" "$MUT/raw-$m.txt" | sort -u
    grep -E "^  (Passed|Failed) " "$MUT/raw-$m.txt" | sed -E 's/ShatteredLegacy.Tests.TutorialIsleWalkFixesVerification.//; s/ \[[^]]*\]$//'
    python -I ../cc-P663-tools/fails.py "$MUT/raw-$m.txt"
  } > "red/red-$m.txt"
done
