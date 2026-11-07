#!/usr/bin/env bash
# cc-P809: the no-patch run and every mutant from mutate809.py in one container. Writes mutants2.txt.
set -u
T=D:/UO/golems/Iron/shard-migration/notes/cc-P809-tools
S=D:/UO/golems/Iron/ShatteredLegacy/server
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  -v "$S/customizations:/m/c:ro" -v "$S/tests:/m/t:ro" -v "$S/patches:/m/p:ro" -v "$T/mutants2:/m/mut:ro" -v "$T/run-mutants-inner.sh:/m/inner.sh:ro" \
  sl-uo-builder:cc-P808 bash /m/inner.sh > "$T/mutants2.txt" 2>&1
echo finished >> "$T/mutants2.txt"
