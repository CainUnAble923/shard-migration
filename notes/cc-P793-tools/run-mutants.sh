#!/usr/bin/env bash
# cc-P793 (P764's): the Peacock facts on the unmutated copy (baseline) and on each mutant (mutate793.py), one log each.
# Usage: run-mutants.sh <mutants folder> <log folder>
set -u
MUT="$1"; LOGS="$2"
HERE="$(cd "$(dirname "$0")" && pwd)"
FILTER='FullyQualifiedName~PeacockVerification'
mkdir -p "$LOGS"
for d in "$MUT"/*/; do
  name=$(basename "$d")
  SRC="${d%/}" bash "$HERE/probe793.sh" "$FILTER" > "$LOGS/$name.log" 2>&1
  failed=$(grep -a -E '^\s+Failed ShatteredLegacy' "$LOGS/$name.log" | sed -E 's/^\s+Failed ShatteredLegacy\.Tests\.[A-Za-z]+\.//; s/ \[.*$//' | sort -u | tr '\n' ';')
  echo "$name: $(grep -a -E '^\s*(Passed|Failed|Total tests):' "$LOGS/$name.log" | tr -s ' ' | tr '\n' ' ') $(grep -a -c ' error ' "$LOGS/$name.log") errors | $failed"
done
