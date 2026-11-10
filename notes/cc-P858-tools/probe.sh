#!/usr/bin/env bash
# cc-P858 (P857's probe): build and run the lamp and wagon facts (and the store facts) on IMAGE with a code copy's files.
# RED=<folder in red/> overlays that folder's files (same relative paths) on the copy's: the code before the change or a
# mutant. FILTER overrides the test filter.
T=D:/UO/golems/Iron/shard-migration/notes/cc-P858-tools
SL=${SL:-D:/UO/golems/Iron/ShatteredLegacy/server}
IMAGE=${IMAGE:-sl-uo-builder:bot}
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= -e RED=${RED:-} -e FILTER="${FILTER:-}" \
  -v "$SL/customizations:/m/c:ro" -v "$SL/tests:/m/t:ro" -v "$T/red:/m/red:ro" \
  -v "$T/probe-inner.sh:/m/inner.sh:ro" "$IMAGE" bash /m/inner.sh
