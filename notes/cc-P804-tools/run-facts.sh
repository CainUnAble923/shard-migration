#!/usr/bin/env bash
# cc-P804: a throwaway container from a builder image: this copy's customizations, facts and the four new patches, then the facts. For
# quick red and green; the gate is the gated build. Usage: run-facts.sh <builder image> <log> [filter]
set -u
IMG="$1"; LOG="$2"; FILTER="${3:-FullyQualifiedName~HerbalismVerification}"
S=D:/UO/golems/Iron/ShatteredLegacy/server
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= \
  -v "$S/customizations:/m/c:ro" -v "$S/tests:/m/t:ro" -v "$S/patches:/m/p:ro" "$IMG" bash -c "cd /build/modernuo
for p in Skills-herbalism skills-json-herbalism FeatureFlagManager-skill-count Plants-herbalism-lane; do sed 's/\r$//' /m/p/\$p.patch | patch -p1 --fuzz=0 --no-backup-if-mismatch || echo PATCH-FAILED \$p; done
U=Projects/UOContent
mkdir -p \$U/Herbalism; cp /m/c/Herbalism/*.cs \$U/Herbalism/
cp /m/c/ClusterFAchievements.cs /m/c/ClusterFGuildStarterPath.cs /m/c/ClusterFGuildSystem.cs \$U/Misc/
cp '/m/c/Services/Plants/Raised Garden Beds/RaisedGardenPlantItem.cs' \"\$(find \$U -name RaisedGardenPlantItem.cs)\"
cp /m/c/Tutorial/TutorialTradeTrials.cs \$U/Tutorial/
cp /m/t/Misc/HerbalismVerification.cs Projects/UOContent.Tests/Tests/Misc/
cp /m/t/Engines/Craft/CraftCeilingsVerification.cs Projects/UOContent.Tests/Tests/Engines/Craft/
dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -30
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -30
cp Distribution/Data/skills.json Projects/UOContent.Tests/bin/Release/net10.0/Data/skills.json
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning" > "$LOG" 2>&1
grep -a -E 'PATCH-FAILED|^\s*(Passed|Failed|Total tests):|^\s+Failed | error |Assert\.|Expected:|Actual:|Exception :' "$LOG" | sed -E 's/\[\/build.*//' | sort -u | cut -c1-210 | head -60
