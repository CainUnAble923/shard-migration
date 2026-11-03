#!/usr/bin/env bash
# cc-P776: probes every mutant mutate776.py made; a mutant whose facts all pass is a SURVIVOR (a gate that did not fail).
# Usage: run-mutants.sh <mutant folder> <log folder>
set -u
DIR="$1"
LOGS="$2"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$LOGS"
tr -d '\r' < "$DIR/mutants.txt" > "$LOGS/.names"  # mutants.txt is written on Windows (CRLF)
while read -r name; do
  [ -z "$name" ] && continue
  SRC776="$DIR/$name/Encounters" bash "$HERE/probe776.sh" "FullyQualifiedName~RandomEncounterVerification" > "$LOGS/$name.txt" 2>&1
  failed=$(grep -c "^  Failed " "$LOGS/$name.txt")
  exitline=$(grep "PROBE_EXIT=" "$LOGS/$name.txt")
  if [ "$failed" -gt 0 ]; then verdict=KILLED; else verdict=SURVIVED; fi
  echo "$name $verdict failed=$failed $exitline $(grep '^  Failed ' "$LOGS/$name.txt" | sed 's/.*Verification\.//; s/ \[.*//' | tr '\n' ' ')"
done < "$LOGS/.names"
