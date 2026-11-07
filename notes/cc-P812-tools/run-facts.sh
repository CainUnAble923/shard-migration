#!/usr/bin/env bash
# cc-P812: a throwaway container from a main builder image: this copy's StaffBuildTools code, the Visual Builder and the facts.
# For quick red and green; the gate is the gated build. Usage: run-facts.sh <log> [mutant dir] [filter]
set -u
LOG="$1"; MUT="${2:-}"; FILTER="${3:-FullyQualifiedName~StaffBuildToolsVerification|FullyQualifiedName~VisualBuilderVerification|FullyQualifiedName~PlaceBuildVerification}"
IMG=sl-uo-builder:cc-p811
S=D:/UO/golems/Iron/ShatteredLegacy/server
EXTRA=()
if [ -n "$MUT" ]; then EXTRA=(-v "$MUT:/m/mut:ro"); fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= -e FILTER="$FILTER" \
  -v "$S/customizations:/m/c:ro" -v "$S/tests:/m/t:ro" "${EXTRA[@]}" "$IMG" bash -c 'cd /build/modernuo
U=Projects/UOContent
mkdir -p $U/StaffBuildTools; cp /m/c/StaffBuildTools/*.cs $U/StaffBuildTools/
cp /m/c/ClusterFVisualBuilder.cs $U/Misc/
if [ -d /m/mut ]; then for f in /m/mut/*.cs; do if [ "$(basename $f)" = ClusterFVisualBuilder.cs ]; then cp $f $U/Misc/; else cp $f $U/StaffBuildTools/; fi; done; fi
cp /m/t/Misc/StaffBuildToolsVerification.cs Projects/UOContent.Tests/Tests/Misc/
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E " error " | sort -u | head -30
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter "$FILTER" --logger "console;verbosity=normal" 2>&1 | grep -v warning' > "$LOG" 2>&1
grep -a -E '^\s*(Passed|Failed|Total tests):|^\s+Failed | error |Assert\.|Expected:|Actual:|Exception :|at ShatteredLegacy' "$LOG" | sed -E 's/\[\/build.*//' | cut -c1-240 | head -60
