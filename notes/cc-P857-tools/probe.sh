#!/usr/bin/env bash
# cc-P857 (P856's probe): run probe-inner.sh on IMAGE with a code copy's carpet files. RED=<mutant file in red/> swaps
# the carpet code for that file (the code before the change, or a broken copy) to watch the facts fail.
T=D:/UO/golems/Iron/shard-migration/notes/cc-P857-tools
SL=${SL:-D:/UO/golems/Iron/ShatteredLegacy/server}
IMAGE=${IMAGE:-sl-uo-builder:bot}
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= -e RED=${RED:-} \
  -v "$SL/customizations/Items/Addons:/m/c:ro" -v "$SL/tests/Items/Addons:/m/t:ro" -v "$T/red:/m/red:ro" \
  -v "$T/probe-inner.sh:/m/inner.sh:ro" "$IMAGE" bash /m/inner.sh
