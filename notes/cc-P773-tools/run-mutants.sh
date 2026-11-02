#!/usr/bin/env bash
# cc-P773 (P769's): runs the P773 facts on the unmutated copy (baseline) and on each mutant (mutate773.py), one log each.
# Usage: run-mutants.sh <mutants folder> <log folder>
set -u
MUT="$1"; LOGS="$2"
HERE="$(cd "$(dirname "$0")" && pwd)"
FILTER='FullyQualifiedName~P773_'
mkdir -p "$LOGS"
bash "$HERE/probe773.sh" "$FILTER" > "$LOGS/baseline.txt" 2>&1
echo "baseline: $(grep -a -E '^\s*(Passed|Failed|Total tests):' "$LOGS/baseline.txt" | tr -s ' ' | tr '\n' ' ')"
for d in "$MUT"/*/; do
  name=$(basename "$d")
  SRC773="${d%/}" bash "$HERE/probe773.sh" "$FILTER" > "$LOGS/$name.txt" 2>&1
  failed=$(grep -a -E '^\s+Failed ShatteredLegacy' "$LOGS/$name.txt" | sed -E 's/^\s+Failed ShatteredLegacy\.Tests\.[A-Za-z]+\.//; s/ \[.*$//' | sort -u | tr '\n' ';')
  echo "$name: $(grep -a -E '^\s*(Passed|Failed|Total tests):' "$LOGS/$name.txt" | tr -s ' ' | tr '\n' ' ') | $failed"
done
