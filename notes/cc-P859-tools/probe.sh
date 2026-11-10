#!/usr/bin/env bash
# cc-P859: run probe-inner.sh on IMAGE with the code copy's horn files (SL=<copy>/server). RED=stub runs the facts against
# red/stub (same API, no behaviour) and the image's own store and Clean Up Britannia files.
T=D:/UO/golems/Iron/shard-migration/notes/cc-P859-tools
SL=${SL:-D:/UO/golems/Iron/ShatteredLegacy/server}
IMAGE=${IMAGE:-sl-uo-builder:bot}
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= -e RED=${RED:-} \
  -v "$SL/customizations:/m/c:ro" -v "$SL/tests:/m/t:ro" -v "$T/red:/m/red:ro" \
  -v "$T/probe-inner.sh:/m/inner.sh:ro" "$IMAGE" bash /m/inner.sh
