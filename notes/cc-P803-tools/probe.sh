#!/usr/bin/env bash
# cc-P803: run the office facts on a builder image with this copy's changed files dropped in (throwaway container).
#   probe.sh <code copy> <builder image> <out file> [filter]
set -u
REPO=$1; IMG=$2; OUT=$(realpath -m "$3")
FILTER=${4:-'FullyQualifiedName~RegistrarOfficeVerification|FullyQualifiedName~LeagueOfficeDecorVerification|FullyQualifiedName~RequisitionsVerification'}
STAGE=$(mktemp -d)
cd "$REPO"
for f in $(git status --porcelain | awk '{print $2}' | grep -E '^server/(customizations|tests)/.*\.cs$'); do
  case "$f" in
    server/customizations/*/*) d="Projects/UOContent/${f#server/customizations/}";;
    server/customizations/*) d="Projects/UOContent/Misc/${f#server/customizations/}";;
    server/tests/*) d="Projects/UOContent.Tests/Tests/${f#server/tests/}";;
  esac
  mkdir -p "$STAGE/$(dirname "$d")"; cp "$f" "$STAGE/$d"; echo "$f -> $d"
done > "$OUT"
W=$(cygpath -m "$STAGE")
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined -e MODE= -v "$W:/stage:ro" "$IMG" bash -c "cd /build/modernuo
cp -r /stage/. .
dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -20
dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -20
dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -E '^\s+Failed |Total tests:|^\s+Passed:|^\s+Failed:|Error Message|Assert|^\s+at ShatteredLegacy' | sed -E 's/ \[[0-9.]+ m?s\]//' | head -80" >> "$OUT" 2>&1
rm -rf "$STAGE"
echo "PROBE DONE" >> "$OUT"
