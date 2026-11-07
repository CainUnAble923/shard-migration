#!/usr/bin/env bash
# cc-P811: every mutant from mutate811.py in one container. Writes mutants.txt.
set -u
T=D:/UO/golems/Iron/shard-migration/notes/cc-P811-tools
S=D:/UO/golems/Iron/ShatteredLegacy/server
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  -v "$S/customizations:/m/c:ro" -v "$S/tests:/m/t:ro" -v "$T/mutants:/m/mut:ro" -v "$T/run-mutants-inner.sh:/m/inner.sh:ro" \
  sl-uo-builder:cc-p810 bash /m/inner.sh > "$T/mutants.txt" 2>&1
echo finished >> "$T/mutants.txt"
