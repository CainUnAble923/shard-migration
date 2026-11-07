#!/usr/bin/env bash
# cc-P808: a throwaway container from a builder image with this copy's Scavenger files and facts, then the facts. Quick red and
# green only; the gate is the gated build. Usage: run-facts.sh <builder image> <log> [filter]
set -u
IMG="$1"; LOG="$2"; FILTER="${3:-FullyQualifiedName~ClockworkScavengerVerification|FullyQualifiedName~MuleModuleVerification}"
S=D:/UO/golems/Iron/ShatteredLegacy/server
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  -v "$S/customizations:/m/c:ro" -v "$S/tests:/m/t:ro" "$IMG" bash -c "cd /build/modernuo
U=Projects/UOContent
mkdir -p \$U/Mobiles/ClockworkScavenger; cp /m/c/Mobiles/ClockworkScavenger/*.cs \$U/Mobiles/ClockworkScavenger/
cp /m/c/Mobiles/Mule/MuleModuleData.cs \$U/Mobiles/Mule/
cp /m/c/ClusterFGuildmasterExtension.cs \$U/Misc/
cp /m/t/Mobiles/ClockworkScavengerVerification.cs Projects/UOContent.Tests/Tests/Mobiles/
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -30
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning" > "$LOG" 2>&1
grep -a -E '^\s*(Passed|Failed|Total tests):|^\s+Failed | error |Assert\.|Expected:|Actual:|Exception :' "$LOG" | sed -E 's/\[\/build.*//' | sort -u | cut -c1-230 | head -60
