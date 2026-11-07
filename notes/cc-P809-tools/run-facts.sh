#!/usr/bin/env bash
# cc-P809: a throwaway container from the main builder image: this copy's Pets code, facts and the AOS patch, then the facts.
# For quick red and green; the gate is the gated build. Usage: run-facts.sh <log> [nopatch] [mutant dir]
set -u
LOG="$1"; NOPATCH="${2:-}"; MUT="${3:-}"
IMG=sl-uo-builder:cc-P808
S=D:/UO/golems/Iron/ShatteredLegacy/server
EXTRA=()
if [ -n "$MUT" ]; then EXTRA=(-v "$MUT:/m/mut:ro"); fi
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= -e NOPATCH="$NOPATCH" \
  -v "$S/customizations:/m/c:ro" -v "$S/tests:/m/t:ro" -v "$S/patches:/m/p:ro" "${EXTRA[@]}" "$IMG" bash -c 'cd /build/modernuo
U=Projects/UOContent
if [ -z "$NOPATCH" ]; then sed "s/\r$//" /m/p/AOS-horse-barding.patch | patch -p1 --fuzz=0 --no-backup-if-mismatch || echo PATCH-FAILED; fi
mkdir -p $U/Pets; cp /m/c/Pets/*.cs $U/Pets/
if [ -d /m/mut ]; then cp /m/mut/*.cs $U/Pets/; fi
mkdir -p Projects/UOContent.Tests/Tests/Mobiles
cp /m/t/Mobiles/HorseBardingVerification.cs /m/t/Mobiles/PetPerchVerification.cs Projects/UOContent.Tests/Tests/Mobiles/
dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore -v q 2>&1 | grep -E " error " | sort -u | head -30
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E " error " | sort -u | head -30
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter "FullyQualifiedName~HorseBardingVerification|FullyQualifiedName~PetPerchVerification" --logger "console;verbosity=normal" 2>&1 | grep -v warning' > "$LOG" 2>&1
grep -a -E 'PATCH-FAILED|^\s*(Passed|Failed|Total tests):|^\s+Failed | error |Assert\.|Expected:|Actual:|Exception :' "$LOG" | sed -E 's/\[\/build.*//' | sort -u | cut -c1-220 | head -60
