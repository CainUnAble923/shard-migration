#!/usr/bin/env bash
# cc-P856: run probe-inner.sh on IMAGE with a code copy's winter set files (SL=<copy>/server). RED=<mutant folder in red/>.
T=D:/UO/golems/Iron/shard-migration/notes/cc-P856-tools
SL=${SL:-D:/UO/golems/Iron/ShatteredLegacy/server}
IMAGE=${IMAGE:-sl-uo-builder:bot}
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= -e RED=${RED:-} \
  -v "$SL/customizations:/m/c:ro" -v "$SL/tests/Misc:/m/t:ro" -v "$T/red:/m/red:ro" \
  -v "$T/probe-inner.sh:/m/inner.sh:ro" "$IMAGE" bash /m/inner.sh
