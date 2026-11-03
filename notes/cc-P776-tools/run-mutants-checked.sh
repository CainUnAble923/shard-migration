#!/usr/bin/env bash
# cc-P776 (resumed after the reboot): like run-mutants.sh, one mutant at a time, but checks free memory before each
# and stops (MEMORY_LOW) under 4 GB, so a run cannot push the PC out of memory again.
# Usage: run-mutants-checked.sh <mutant folder> <names file> <log folder>
set -u
DIR="$1"
NAMES="$2"
LOGS="$3"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$LOGS"
while read -r name; do
  [ -z "$name" ] && continue
  docker run --rm --privileged alpine:3.20 sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches' > /dev/null 2>&1
  free=$(powershell.exe -NoProfile -Command "[math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory/1MB,1)" | tr -d '\r')
  if awk "BEGIN{exit !($free < 4)}"; then echo "MEMORY_LOW free=${free}GB before $name; stopped"; exit 9; fi
  SRC776="$DIR/$name/Encounters" bash "$HERE/probe776.sh" "FullyQualifiedName~RandomEncounterVerification" > "$LOGS/$name.txt" 2>&1
  failed=$(grep -c "^  Failed " "$LOGS/$name.txt")
  exitline=$(grep "PROBE_EXIT=" "$LOGS/$name.txt")
  if [ "$failed" -gt 0 ]; then verdict=KILLED; else verdict=SURVIVED; fi
  echo "$name $verdict failed=$failed free=${free}GB $exitline $(grep '^  Failed ' "$LOGS/$name.txt" | sed 's/.*Verification\.//; s/ \[.*//' | tr '\n' ' ')"
done < "$NAMES"
