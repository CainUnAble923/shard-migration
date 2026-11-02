#!/usr/bin/env bash
# cc-P764 (P769's): runs the P764 facts on the unmutated copy (baseline) and on each mutant (mutate764.py), one log each.
# Usage: run-mutants.sh <mutants folder> <log folder>
set -u
MUT="$1"; LOGS="$2"
HERE="$(cd "$(dirname "$0")" && pwd)"
FILTER='FullyQualifiedName~PetLeashVerification'
mkdir -p "$LOGS"
bash "$HERE/probe764.sh" "$FILTER" > "$LOGS/baseline.log" 2>&1
echo "baseline: $(grep -a -E '^\s*(Passed|Failed|Total tests):' "$LOGS/baseline.log" | tr -s ' ' | tr '\n' ' ')"
for d in "$MUT"/*/; do
  name=$(basename "$d")
  SRC="${d%/}" bash "$HERE/probe764.sh" "$FILTER" > "$LOGS/$name.log" 2>&1
  failed=$(grep -a -E '^\s+Failed ShatteredLegacy' "$LOGS/$name.log" | sed -E 's/^\s+Failed ShatteredLegacy\.Tests\.[A-Za-z]+\.//; s/ \[.*$//' | sort -u | tr '\n' ';')
  echo "$name: $(grep -a -E '^\s*(Passed|Failed|Total tests):' "$LOGS/$name.log" | tr -s ' ' | tr '\n' ' ') | $failed"
done
