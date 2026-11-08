#!/usr/bin/env bash
# Inside the container: install the real sources, then each mutant over them, and restore.
cd /build/modernuo
U=Projects/UOContent/Tutorial
FACTS='FullyQualifiedName~TutorialJailVerification'
install_real() { cp /m/c/TutorialJail.cs /m/c/TutorialTradeTrials.cs /m/c/TutorialWingTrials.cs /m/c/TutorialCoreTrials.cs $U/; }
run_facts() {
  errs=$(dotnet build Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-restore -v q 2>&1 | grep -E ' error ' | sort -u | head -3)
  if [ -n "$errs" ]; then echo "DID NOT COMPILE: $errs"; return; fi
  out=$(dotnet test Projects/UOContent.Tests/UOContent.Tests.csproj -c Release --no-build --filter "$FACTS" --logger 'console;verbosity=normal' 2>&1)
  fails=$(echo "$out" | grep -E '^\s+Failed ShatteredLegacy' | sed -E 's/.*TutorialJailVerification\.//; s/\(.*//; s/ \[.*//' | sort -u | tr '\n' ' ')
  total=$(echo "$out" | grep -E 'Total tests:' | tr -d ' ')
  echo "${fails:-NONE RED} ($total)"
}
install_real
cp /m/t/TutorialJailVerification.cs Projects/UOContent.Tests/Tests/Tutorial/
echo "== clean: $(run_facts)"

for d in /m/mut/*/; do
  name=$(basename "$d"); target=$(cat "$d/target")
  install_real
  cp "$d/$target" "$U/$target"
  touch "$U/$target"
  echo "== $name: $(run_facts)"
done
