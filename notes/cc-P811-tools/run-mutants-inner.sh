#!/usr/bin/env bash
# Inside the container: the real Casino sources and facts, then each mutant over them, and back. One line each.
cd /build/modernuo
U=Projects/UOContent
mkdir -p $U/Casino
cp /m/t/Misc/CasinoVerification.cs Projects/UOContent.Tests/Tests/Misc/
F='FullyQualifiedName~CasinoVerification'
run() {
  errs=$(dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -3)
  if [ -n "$errs" ]; then echo "== $1: DID NOT COMPILE: $errs"; return; fi
  out=$(dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter "$F" --logger 'console;verbosity=normal' 2>&1)
  fails=$(echo "$out" | grep -E '^\s+Failed ShatteredLegacy' | sed -E 's/.*Verification\.//; s/\(.*//; s/ \[.*//' | sort -u | tr '\n' ' ')
  echo "== $1: ${fails:-NONE RED}"
}
for d in /m/mut/*/; do
  cp /m/c/Casino/*.cs $U/Casino/
  cp "$d"*.cs $U/Casino/
  run "$(basename "$d")"
done
cp /m/c/Casino/*.cs $U/Casino/
run real
