#!/usr/bin/env bash
# cc-P801: every mutant from mutate801.py, one container, jail facts only. Writes mutants-final.txt: which facts each one turned red.
set -u
T=D:/UO/golems/Iron/shard-migration/notes/cc-P801-tools
CUST=D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Tutorial
TESTS=D:/UO/golems/Iron/ShatteredLegacy/server/tests/Tutorial
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  -v "$CUST:/m/c:ro" -v "$TESTS:/m/t:ro" -v "$T/mutants:/m/mut:ro" -v "$T/run-mutants-inner.sh:/m/inner.sh:ro" \
  sl-uo-builder:cc-p801 bash /m/inner.sh > "$T/mutants-final.txt" 2>&1
echo finished >> "$T/mutants-final.txt"
