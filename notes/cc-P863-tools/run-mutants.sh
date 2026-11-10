#!/usr/bin/env bash
# cc-P863: every mutant from mutate863.py in one container. Writes mutants.txt.
set -u
T=D:/UO/golems/Iron/shard-migration/notes/cc-P863-tools
S=D:/UO/golems/Iron/ShatteredLegacy/server
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  -v "$S/customizations:/m/c:ro" -v "$S/tests:/m/t:ro" -v "$T/${MUTD:-mutants}:/m/mut:ro" -v "$T/run-mutants-inner.sh:/m/inner.sh:ro" \
  sl-uo-builder:cc-P872 bash /m/inner.sh > "$T/${OUTF:-mutants.txt}" 2>&1
echo finished >> "$T/${OUTF:-mutants.txt}"
