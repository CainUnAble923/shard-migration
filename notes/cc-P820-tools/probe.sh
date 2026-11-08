#!/usr/bin/env bash
# cc-P820: run probe-inner.sh on IMAGE (default sl-uo-builder:bot) with this branch's files. RED=<mutant folder in red/>.
T=D:/UO/golems/Iron/shard-migration/notes/cc-P820-tools
SL=D:/UO/golems/Iron/ShatteredLegacy/server
IMAGE=${IMAGE:-sl-uo-builder:bot}
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= -e RED=${RED:-} -e FILTER="${FILTER:-}" \
  -v "$SL/customizations/Tutorial:/m/c:ro" -v "$SL/tests/Tutorial:/m/t:ro" -v "$SL/patches:/m/p:ro" -v "$T/red:/m/red:ro" \
  -v "$T/probe-inner.sh:/m/inner.sh:ro" "$IMAGE" bash /m/inner.sh
