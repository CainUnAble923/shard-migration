#!/usr/bin/env bash
# cc-P838 (P820's): inside a builder image. Install the branch's Tutorial files, its tests and P801's Notoriety patch, then run the jail
# facts (and the trade-trial facts the merge touched). With RED=<mutant>, red/<mutant>/*.cs go over the branch's files.
cd /build/modernuo
U=Projects/UOContent/Tutorial
mkdir -p $U
cp /m/c/*.cs $U/
cp /m/t/*.cs Projects/UOContent.Tests/Tests/Tutorial/ 2>/dev/null || { mkdir -p Projects/UOContent.Tests/Tests/Tutorial; cp /m/t/*.cs Projects/UOContent.Tests/Tests/Tutorial/; }
patch -p1 --fuzz=0 < /m/p/Notoriety-lesson-shown-color.patch || echo "PATCH FAILED"
if [ -n "${RED:-}" ]; then cp /m/red/$RED/*.cs $U/; touch $U/*.cs; echo "== RED mutant: $RED ($(ls /m/red/$RED))"; fi
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release -v q 2>&1 | grep -E ' error |Build succeeded' | sort -u | head -20
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build \
  --filter "${FILTER:-FullyQualifiedName~TutorialJailVerification|FullyQualifiedName~TutorialTradeTrialVerification|FullyQualifiedName~TutorialVerification}" \
  --logger 'console;verbosity=normal' 2>&1 | grep -E '^\s+(Failed|Passed) ShatteredLegacy|Total tests|Passed:|Failed:|error' | sed -E 's/^\s+//' | grep -vE '^Passed ShatteredLegacy' | sort -u | head -60
