#!/usr/bin/env bash
# cc-P804: every mutant from mutate804.py, one container, Herbalism facts only. Writes mutants3.txt.
set -u
T=D:/UO/golems/Iron/shard-migration/notes/cc-P804-tools
S=D:/UO/golems/Iron/ShatteredLegacy/server
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  -v "$S/customizations:/m/c:ro" -v "$S/tests:/m/t:ro" -v "$S/patches:/m/p:ro" -v "$T/mutants:/m/mut:ro" -v "$T/run-mutants-inner.sh:/m/inner.sh:ro" \
  sl-uo-builder:cc-p800 bash /m/inner.sh > "$T/mutants3.txt" 2>&1
echo finished >> "$T/mutants3.txt"
