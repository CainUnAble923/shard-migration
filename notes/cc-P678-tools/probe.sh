#!/usr/bin/env bash
# cc-P678 probe (P705's probe.sh): the changed customizations and the tests bind-mounted over a builder image's copies;
# runs the tests matching $1.   CODE=<server folder> IMAGE=<builder> probe.sh <filter>
# Top-level customizations land in UOContent/Misc/ in the build tree; CharacterCreation.cs is a replacement file.
set -u
FILTER="$1"
IMAGE="${IMAGE:-sl-uo-builder:cc-P710}"
CODE="${CODE:-D:/UO/golems/Iron/ShatteredLegacy/server}"
C="$CODE/customizations"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined \
  -v "$C/Tutorial:$UC/Tutorial" \
  -v "$C/CharacterCreation.cs:$UC/Engines/Character Creation/CharacterCreation.cs" \
  -v "$C/ClusterFAchievements.cs:$UC/Misc/ClusterFAchievements.cs" \
  -v "$C/ClusterFNewHavenSeeder.cs:$UC/Misc/ClusterFNewHavenSeeder.cs" \
  -v "$C/ClusterFNewHavenServicesSeeder.cs:$UC/Misc/ClusterFNewHavenServicesSeeder.cs" \
  -v "$C/ClusterFResetStone.cs:$UC/Misc/ClusterFResetStone.cs" \
  -v "$C/LeagueRegistrarGump.cs:$UC/Misc/LeagueRegistrarGump.cs" \
  -v "$C/Engines/ML Quests/Items/NewHavenQuestBoard.cs:$UC/Engines/ML Quests/Items/NewHavenQuestBoard.cs" \
  -v "$C/FountainOfYouth:$UC/FountainOfYouth" \
  -v "$CODE/tests/Tutorial:$UT/Tutorial" \
  -v "$CODE/tests/Misc:$UT/Misc" \
  -v "$CODE/tests/Engines/MLQuests:$UT/Engines/MLQuests" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning"
