#!/usr/bin/env bash
# cc-P810: a throwaway container from the main builder image: this copy's StaffHub code and the facts, then the facts.
# For quick red and green; the gate is the gated build. Usage: run-facts.sh <log> [mutant dir] [filter]
set -u
LOG="$1"; MUT="${2:-}"; FILTER="${3:-FullyQualifiedName~StaffEventsVerification|FullyQualifiedName~StaffHub}"
IMG=sl-uo-builder:cc-P808
S=D:/UO/golems/Iron/ShatteredLegacy/server
EXTRA=()
if [ -n "$MUT" ]; then EXTRA=(-v "$MUT:/m/mut:ro"); fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= -e FILTER="$FILTER" \
  -v "$S/customizations:/m/c:ro" -v "$S/tests:/m/t:ro" "${EXTRA[@]}" "$IMG" bash -c 'cd /build/modernuo
U=Projects/UOContent
cp /m/c/StaffHub/*.cs $U/StaffHub/
if [ -d /m/mut ]; then cp /m/mut/*.cs $U/StaffHub/; fi
cp /m/t/Misc/StaffEventsVerification.cs Projects/UOContent.Tests/Tests/Misc/
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E " error " | sort -u | head -30
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter "$FILTER" --logger "console;verbosity=normal" 2>&1 | grep -v warning' > "$LOG" 2>&1
grep -a -E '^\s*(Passed|Failed|Total tests):|^\s+Failed | error |Assert\.|Expected:|Actual:|Exception :|at Server\.|at ShatteredLegacy' "$LOG" | sed -E 's/\[\/build.*//' | cut -c1-220 | head -60
