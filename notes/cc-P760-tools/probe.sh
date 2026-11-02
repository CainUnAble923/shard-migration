#!/usr/bin/env bash
# cc-P760 probe (P763's pattern): builds UOContent and the tests in a builder image with every changed or new file of
# server/customizations and server/tests mounted over its copy, then runs the tests matching $1.
# PROBE_MODE=red mounts only the new and changed tests (the code before the change); green (default) mounts everything.
# Usage: probe.sh <filter> [image]. Top-level customizations live in Projects/UOContent/Misc; folders keep their path.
set -u
FILTER="$1"
IMAGE="${2:-sl-uo-builder:cc-P762}"
PMODE="${PROBE_MODE:-green}"
CODE="D:/UO/golems/Iron/ShatteredLegacy"
UC=/build/modernuo/Projects/UOContent
UT=/build/modernuo/Projects/UOContent.Tests/Tests
M=()
cd "$CODE"
while IFS= read -r f; do
  case "$f" in
    server/customizations/*.cs)
      [ "$PMODE" = red ] && continue
      rel="${f#server/customizations/}"
      case "$rel" in */*) dst="$UC/$rel";; *) dst="$UC/Misc/$rel";; esac
      M+=(-v "$CODE/$f:$dst");;
    server/tests/*.cs)
      rel="${f#server/tests/}"
      M+=(-v "$CODE/$f:$UT/$rel");;
  esac
done < <( { git diff --name-only HEAD; git ls-files --others --exclude-standard; } | sort -u )
echo "mounted ${#M[@]} args ($PMODE)"
MSYS_NO_PATHCONV=1 docker run --rm --network=none --security-opt seccomp=unconfined "${M[@]}" \
  "$IMAGE" bash -c "cd /build/modernuo && dotnet build Projects/UOContent/UOContent.csproj -c Release --no-restore 2>&1 | grep -E ' error ' | sort -u | head -40 ; dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore 2>&1 | grep -E ' error |Build succeeded|Error\(s\)' | sort -u | head -40; [ '$FILTER' = none ] || dotnet test --no-build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore --filter '$FILTER' --logger 'console;verbosity=normal' 2>&1 | grep -v warning | tail -150"
