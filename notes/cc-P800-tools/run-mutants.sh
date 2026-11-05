#!/usr/bin/env bash
# cc-P800: every mutant from mutate800.py, one container, sash facts only. Writes mutants2.txt: which facts each one turned red.
set -u
T=D:/UO/golems/Iron/shard-migration/notes/cc-P800-tools
CUST=D:/UO/golems/Iron/ShatteredLegacy/server/customizations
TESTS=D:/UO/golems/Iron/ShatteredLegacy/server/tests/Misc
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  -v "$CUST:/m/c:ro" -v "$TESTS:/m/t:ro" -v "$T/mutants:/m/mut:ro" -v "$T/run-mutants-inner.sh:/m/inner.sh:ro" \
  sl-uo-builder:cc-p800 bash /m/inner.sh > "$T/mutants2.txt" 2>&1
echo finished >> "$T/mutants2.txt"
