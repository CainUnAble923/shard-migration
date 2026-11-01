#!/usr/bin/env bash
# cc-P714 (P750's probe-guild.sh shape): this branch's school-gate files over sl-uo-builder's patched tree; runs the tests
# matching $1. SRC (default: the code copy's customizations) may point at a mutant copy holding the same file names;
# APPLIED (default: the scratch copies with this branch's two patches applied) holds Spell.cs and PowerScroll.cs.
#     bash probe714.sh <filter> [image]
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-P753}"
CODE="D:/UO/golems/Iron/ShatteredLegacy/server"
SRC="${SRC:-$CODE/customizations}"
APPLIED="${APPLIED:-C:/Users/ckfle/AppData/Local/Temp/claude/D--UO-golems-Iron-shard-migration/6d4e7b5a-5442-4beb-9baa-2b87f19155fe/scratchpad/p714/applied/Projects/UOContent}"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
M=""
for f in ClusterFSchoolGate.cs ClusterFInitiation.cs ClusterFStartChoices.cs ClusterFSkillCaps.cs ClusterFSkillGain.cs; do
  M="$M -v $SRC/$f:$UC/Misc/$f"
done
M="$M -v $SRC/Tutorial/TutorialWingTrials.cs:$UC/Tutorial/TutorialWingTrials.cs"
M="$M -v $SRC/Tutorial/ClusterFTutorial.cs:$UC/Tutorial/ClusterFTutorial.cs"
M="$M -v $APPLIED/Spells/Base/Spell.cs:$UC/Spells/Base/Spell.cs"
for f in SchoolGateVerification.cs TestCenterVerification.cs; do
  M="$M -v $CODE/tests/Misc/$f:$UT/Misc/$f"
done
# Paths with spaces cannot ride -v; copy them in at start instead.
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined $M \
  -v "$SRC:/src714:ro" -v "$APPLIED:/applied714:ro" \
  "$IMAGE" bash -c "cp /src714/CharacterCreation.cs '$UC/Engines/Character Creation/CharacterCreation.cs' && \
    cp '/applied714/Items/Special/Special Scrolls/PowerScroll.cs' '$UC/Items/Special/Special Scrolls/PowerScroll.cs' && \
    cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
