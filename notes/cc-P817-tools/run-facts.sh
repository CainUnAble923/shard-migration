#!/usr/bin/env bash
# cc-P817 (P813's): a throwaway container from main's builder image (cc-P812, this branch's base), for quick red and
# green; the gate is the gated build. Usage: run-facts.sh <log> red|green [filter]
#   red:   main's code, plus only what the facts need to compile: the new TutorialBankerVoice.cs (not hooked in anywhere),
#          and the changed facts (not TutorialIsleWalkFixes4Verification.cs, whose updated wake fact names a new constant).
#   green: every file this prompt changed.
set -u
LOG="$1"; WHICH_="$2"; FILTER="${3:-FullyQualifiedName~P817_}"
IMG=sl-uo-builder:cc-P812
S=D:/UO/golems/Iron/ShatteredLegacy/server
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= -e FILTER="$FILTER" -e WHICH="$WHICH_" \
  -v "$S/customizations:/m/c:ro" -v "$S/tests:/m/t:ro" "$IMG" bash -c 'cd /build/modernuo
U=Projects/UOContent
T=Projects/UOContent.Tests/Tests
cp /m/c/Tutorial/TutorialBankerVoice.cs $U/Tutorial/
if [ "$WHICH" = green ]; then
  cp /m/c/ClusterFStartChoices.cs $U/Misc/
  for f in TutorialStart TutorialWake TutorialStations TutorialCoreTrials TutorialFarm TutorialCorePlacement; do cp /m/c/Tutorial/$f.cs $U/Tutorial/; done
  cp /m/t/Tutorial/*.cs $T/Tutorial/   # every tutorial fact and the shared helper (TutorialTestStart.ToTheFarm)
fi
cp /m/t/Misc/SchoolGateVerification.cs $T/Misc/
for f in TutorialIsleVerification TutorialIsleWalkFixes2Verification TutorialIsleBandageWaitVerification; do cp /m/t/Tutorial/$f.cs $T/Tutorial/; done
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E " error " | sort -u | head -30
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter "$FILTER" --logger "console;verbosity=normal" 2>&1 | grep -v warning' > "$LOG" 2>&1
grep -a -E '^\s*(Passed|Failed|Total tests):|^\s+Failed | error |Assert\.|Expected:|Actual:|Exception :' "$LOG" | sed -E 's/\[\/build.*//' | cut -c1-220 | head -70
