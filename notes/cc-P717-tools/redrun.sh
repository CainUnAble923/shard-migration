#!/usr/bin/env bash
# cc-P717 red run: each mutant (mutate.py) against the isle facts, then the real code (green); a summary per run in
# red/red-<name>.txt. Mutant copies go to $MUT (git-ignored scratch), never into the repo.
cd "$(dirname "$0")"
MUT="${MUT:?set MUT to a scratch folder}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server/customizations"
mkdir -p red
for m in ${MUTANTS:-nolock forced hidden nostaff deleted nounlock norelock legacy shared green}; do
  if [ "$m" = green ]; then
    unset SRC
  else
    python -I mutate.py "$CODE" "$MUT/m-$m" "$m" || { echo "mutate $m failed" > "red/red-$m.txt"; continue; }
    export SRC="$MUT/m-$m"
  fi
  timeout 1500 bash probe.sh "FullyQualifiedName~TutorialIsleVerification" > "$MUT/raw-$m.txt" 2>&1
  {
    echo "== $m"
    grep -E "error CS|^Total tests|Passed:|Failed:" "$MUT/raw-$m.txt" | sort -u
    python -I ../cc-P663-tools/fails.py "$MUT/raw-$m.txt"
  } > "red/red-$m.txt"
done
echo done > "$MUT/red-done.txt"
