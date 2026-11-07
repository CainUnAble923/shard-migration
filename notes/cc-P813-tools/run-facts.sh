#!/usr/bin/env bash
# cc-P813: a throwaway container from main's builder image (cc-P812), for quick red and green; the gate is the gated
# build. Usage: run-facts.sh <log> red|green [filter]
#   red:   only the two new files (DesignGumpArt.cs, Items/FinishersBanner.cs, so the facts compile) and the facts; the
#          three gumps and ShatteredLegacyArt.Apply as main has them.
#   green: every file this prompt changed.
set -u
LOG="$1"; MODE_="$2"; FILTER="${3:-FullyQualifiedName~DesignGumpArtVerification}"
IMG=sl-uo-builder:cc-P812
S=D:/UO/golems/Iron/ShatteredLegacy/server
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= -e FILTER="$FILTER" -e WHICH="$MODE_" \
  -v "$S/customizations:/m/c:ro" -v "$S/tests:/m/t:ro" "$IMG" bash -c 'cd /build/modernuo
U=Projects/UOContent
cp /m/c/DesignGumpArt.cs $U/Misc/
cp /m/c/Items/FinishersBanner.cs $U/Items/
if [ "$WHICH" = green ]; then
  cp /m/c/ShatteredRunestone.cs /m/c/ClusterFAchievements.cs $U/Misc/
  cp /m/c/Tutorial/TutorialGateSkip.cs $U/Tutorial/
  cp /m/c/LeagueShop/LeagueShopGumps.cs $U/LeagueShop/
fi
cp /m/t/Misc/DesignGumpArtVerification.cs /m/t/Misc/AchievementsLayoutVerification.cs Projects/UOContent.Tests/Tests/Misc/
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E " error " | sort -u | head -30
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter "$FILTER" --logger "console;verbosity=normal" 2>&1 | grep -v warning' > "$LOG" 2>&1
grep -a -E '^\s*(Passed|Failed|Total tests):|^\s+Failed | error |Assert\.|Expected:|Actual:|Exception :|covers button' "$LOG" | sed -E 's/\[\/build.*//' | cut -c1-220 | head -60
