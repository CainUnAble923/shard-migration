#!/usr/bin/env bash
# cc-P802: the red run. Turns each new behaviour of this prompt off in the container's copies (one sed each), so every
# P802 fact is watched failing against the real code. Usage (inside run-facts.sh's container): mutate.sh <UOContent dir>
set -u
U="$1"
f() { find "$U" -name "$1" | head -1; }
m() { # file, from, to: fails loudly when the text is not there (a mutation that no longer applies proves nothing)
  local file; file=$(f "$1")
  grep -qF -- "$2" "$file" || { echo "MUTATION MISSING in $1: $2"; exit 1; }
  python3 - "$file" "$2" "$3" <<'PY' 2>/dev/null || perl -0pi -e 'BEGIN{$a=shift;$b=shift} s/\Q$a\E/$b/' "$2" "$3" "$file"
import sys
p, a, b = sys.argv[1:4]
s = open(p, encoding='utf-8').read()
open(p, 'w', encoding='utf-8').write(s.replace(a, b))
PY
  echo "mutated $1"
}
# 7: the caps at creation; the window's notes; the welcome window; the login chat request
m CharacterCreation.cs 'ClusterFSkillCaps.ApplyTo(capped);' ';'
m TutorialWelcome.cs 'if (!TutorialWake.IsHolding(pm))' 'if (true)'
m TutorialWake.cs 'TutorialWelcome.Lying(pm);' 'ClusterFTutorial.SystemLine(pm, LyingLine);'
m TutorialWelcome.cs 'm is PlayerMobile pm && (TutorialWake.IsHolding(pm) ||' 'm is PlayerMobile pm && false && (TutorialWake.IsHolding(pm) ||'
# 4: the farm only with the tutorial seed (as before)
m TutorialFarm.cs ': ClearHaven(false);' ': ClusterFTutorial.Enabled ? ClearHaven(false) : "old New Haven farm: took away 0 thing(s).";'
# 2: the travel lesson as the old tour's loan, no evidence, Mark refused
m TutorialTradeTrials.cs 'if (trial.Key == TravelKey) { TickTravel(trial); }' ''
m TutorialTradeTrials.cs 'ArmTravel(trial); // cc-P802 item 2' 'Lend(trial, new RecallRune());'
m TutorialIslandGate.cs 'TravelCheckType.Mark => MarkLesson(mobile),' 'TravelCheckType.Mark => false,'
# 1: the tour stop's lesson only in the System window; the explained skills only in the System window
m TutorialTradeTrials.cs 'trial.Latest = stops[i].Text;' ''
m TutorialWingTrials.cs '_ => Trade(key)?.Line' '_ => null'
m TutorialWingTrials.cs '"combat.weapons" => ResistingSpellsLine,' '"combat.weapons" => null,'
# 6: every moved lesson back on the open trades yard
m NewHavenLessonPlaces.cs 'private static Point2D P2(Point3D p) => new(p.X, p.Y);' 'private static Point2D P2(Point3D p) => TradesYard;'
# 3 and 8: the lessons back in the training yard, no teachers
m NewHavenLessons.cs '"magic.mysticism" => new Point3D(3653, 2477, 0),' ''
m NewHavenLessons.cs '"magic.necromancy" => new Point3D(3686, 2475, 0),' ''
m NewHavenLessons.cs 'var teachers = SeedTeachers(map, dryRun);' 'var teachers = "";'
m NewHavenLessons.cs 'int placed = 0, moved = 0;' 'int placed = 0, moved = 0; return "teachers: placed 0, moved 0.";'
