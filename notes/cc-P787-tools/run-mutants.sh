#!/usr/bin/env bash
# cc-P787: runs every mutant (mutants.py) through probe.sh; mutant 9 is pinned's Beekeeper.cs without the patch.
HERE="D:/UO/golems/Iron/shard-migration/notes/cc-P787-tools"
MUT="${1:?mutant folder}"
OUT="$HERE/red-mutants.txt"
: > "$OUT"
for n in 1 2 3 4 5 6 7 8 9 10 11; do
  echo "=== mutant $n" >> "$OUT"
  if [ $n = 9 ]; then
    touch "$HERE/Beekeeper.pinned.cs"
    VEND="$HERE/Beekeeper.pinned.cs" bash "$HERE/probe.sh" "FullyQualifiedName~BeekeepingVerification" 2>&1 | grep -E "error|  Passed |  Failed |Total tests" >> "$OUT"
  else
    find "$MUT/m$n" -name '*.cs' -exec touch {} +
    SRC="$MUT/m$n" bash "$HERE/probe.sh" "FullyQualifiedName~BeekeepingVerification" 2>&1 | grep -E "error|  Passed |  Failed |Total tests" >> "$OUT"
  fi
done
echo "=== done" >> "$OUT"
