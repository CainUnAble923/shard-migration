#!/usr/bin/env bash
# cc-P849: inside a builder image. Install the copy's League office files and their facts, then run them. With RED=<mutant>,
# red/<mutant>/Appraiser.cs goes over the copy's.
cd /build/modernuo
cp /m/c/Requisitions/Appraiser.cs Projects/UOContent/Requisitions/
cp /m/c/ClusterFRegistrarOfficeSeeder.cs /m/c/ClusterFRegistrarOfficeLayout.cs Projects/UOContent/Misc/
cp /m/t/LeagueOfficeDecorVerification.cs /m/t/RegistrarOffice*.cs Projects/UOContent.Tests/Tests/Misc/
if [ -n "${RED:-}" ]; then cp /m/red/$RED/Appraiser.cs Projects/UOContent/Requisitions/; touch Projects/UOContent/Requisitions/Appraiser.cs; echo "== RED mutant: $RED"; fi
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release -v q 2>&1 | grep -E ' error |Build succeeded' | sort -u | head -20
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build \
  --filter "FullyQualifiedName~LeagueOfficeDecorVerification|FullyQualifiedName~RegistrarOffice" \
  --logger 'console;verbosity=normal' 2>&1 | grep -E '^\s+(Failed|Passed) ShatteredLegacy|Total tests|Passed:|Failed:|error' | sed -E 's/^\s+//' | grep -vE '^Passed ShatteredLegacy' | sort -u | head -60
