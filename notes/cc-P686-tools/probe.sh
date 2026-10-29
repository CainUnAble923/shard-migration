#!/usr/bin/env bash
# cc-P686 probe: the code copy's Regions tests over sl-uo-builder's copies (an image with P676's region patch built
# in); runs the tests matching $1. FELUCCA=1 also mounts the code copy's regions-felucca.json into
# Distribution/Data/ShatteredLegacy, as the Dockerfile copies it (without it: the red run, the file not shipped).
# FELUCCA_FILE may point at a mutant copy (mutate.py).
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-P685}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
UT=/build/modernuo/Projects/UOContent.Tests/Tests
DATA=/build/modernuo/Distribution/Data/ShatteredLegacy
EXTRA=()
if [ "${FELUCCA:-0}" = 1 ]; then EXTRA=(-v "${FELUCCA_FILE:-$CODE/data/regions-felucca.json}:$DATA/regions-felucca.json:ro"); fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "$CODE/tests/Regions:$UT/Regions" "${EXTRA[@]}" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
