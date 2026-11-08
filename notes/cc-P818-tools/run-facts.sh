#!/usr/bin/env bash
# cc-P818 (P817's run-facts.sh): a throwaway container from main's builder image (sl-uo-builder:cc-P802, this branch's
# base) for quick red and green; the gate is the gated build. Usage: run-facts.sh <log> red|green [filter]
#   green: every file this prompt changed.
#   red:   the same files, then each fix switched off by one sed (the mutants below), so every P818 fact must fail:
#     M1 the door and stop back on the north wall    M2 the lodge door hung WestCCW    M3 no upgrade pass (old door, sign)
#     M4 the signs back by the road's dip             M5 Elara faces north              M6 the hint and arrow as before
#     M7 Elara never calls
set -u
LOG="$1"; WHICH_="$2"; FILTER="${3:-FullyQualifiedName~TutorialLodgeDoorVerification|FullyQualifiedName~TutorialIsleWalkFixes2Verification|FullyQualifiedName~TutorialIsleReviewFixesVerification|FullyQualifiedName~TutorialIsleAddonsVerification|FullyQualifiedName~PlaytesterNotesVerification}"
IMG=sl-uo-builder:cc-P802
S=D:/UO/golems/Iron/ShatteredLegacy/server
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= -e FILTER="$FILTER" -e WHICH="$WHICH_" \
  -v "$S/customizations:/m/c:ro" -v "$S/tests:/m/t:ro" "$IMG" bash -c 'cd /build/modernuo
U=Projects/UOContent
T=Projects/UOContent.Tests/Tests
for f in TutorialWorld TutorialCorePlacement TutorialCoreTrials; do cp /m/c/Tutorial/$f.cs $U/Tutorial/; done
for f in TutorialLodgeDoorVerification TutorialIsleWalkFixes2Verification TutorialIsleReviewFixesVerification; do cp /m/t/Tutorial/$f.cs $T/Tutorial/; done
if [ "$WHICH" = red ]; then
  W=$U/Tutorial/TutorialWorld.cs; P=$U/Tutorial/TutorialCorePlacement.cs; C=$U/Tutorial/TutorialCoreTrials.cs
  sed -i "s/LodgeStop = new(6789, 4000)/LodgeStop = new(6782, 3994)/; s/LodgeDoor = new(6787, 4000)/LodgeDoor = new(6782, 3995)/" $W   # M1
  sed -i "s/new DarkWoodDoor(DoorFacing.NorthCW)/new DarkWoodDoor(DoorFacing.WestCCW)/" $P                                       # M2
  sed -i "s/if (!dryRun) { RemoveOldLodgeDoor(map); MoveLodgeSign(map); }/\/\/ M3/" $P                                          # M3
  sed -i "s/\"core.league\" => new Point2D(6789, 3984),/\"core.league\" => new Point2D(6782, 3989),/; s/LodgeSign = new(6788, 3984)/LodgeSign = new(6781, 3989)/" $P  # M4
  sed -i "s/ElaraFacing = Direction.East/ElaraFacing = Direction.North/" $P                                                      # M5
  sed -i "s/Its door is on the east side, facing you as you come along the road: take the paved walk south from the road, between the two fires, and double-click the door to enter./Double-click the door on its north side to enter./" $C  # M6 hint
  sed -i "/\"core.league\" when !TutorialCorePlacement.InLodge/d" $C                                                              # M6 arrow
  sed -i "s/elara.SayTo(pm, ElaraDoorLine);/return false;/" $C                                                                    # M7
  grep -c "6782, 3995\|WestCCW)\|// M3\|6782, 3989\|Direction.North;\|north side to enter\|return false;" $W $P $C
fi
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E " error " | sort -u | head -30
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter "$FILTER" --logger "console;verbosity=normal" 2>&1 | grep -v warning' > "$LOG" 2>&1
grep -a -E '^\s*(Passed|Failed|Total tests):|^\s+Failed | error |Assert\.|Expected:|Actual:|Exception :' "$LOG" | sed -E 's/\[\/build.*//' | cut -c1-200 | head -60
