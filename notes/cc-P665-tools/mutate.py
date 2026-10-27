"""cc-P665 red runs: one copy of the edited Tutorial folder per behaviour, with that behaviour taken out behind the new
API (which does not exist before the change, so the facts cannot compile against the old code). Copies go to m-<name>/
beside this file; redrun.sh mounts each over the builder image and runs the facts.

    python -P mutate.py <code copy>/server
"""
import os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRV = sys.argv[1]
F = 'TutorialVisionScene.cs'
MUTANTS = {
    # sounds to everyone in range (pinned Effects.PlaySound), and no light of its own
    'shared': {F: [("    private static void Sound(Scene s, int soundId) => s.Player.NetState?.SendSoundEffect(soundId, s.Player.Location);",
                    "    private static void Sound(Scene s, int soundId) => Effects.PlaySound(s.Player.Location, s.Map, soundId);"),
                   ("        if (LightOf(m) is { } level)", "        if (false && LightOf(m) is { } level)")]},
    # the echo is a Clone in all but name: it copies the skills too
    'clone': {F: [("            FacialHairHue = m.FacialHairHue\n        };\n",
                   "            FacialHairHue = m.FacialHairHue\n        };\n        for (var i = 0; i < m.Skills.Length; i++) { f.Skills[i].Base = m.Skills[i].Base; }\n")]},
    # an early end does nothing but forget the scene: still frozen, dark, figures left standing
    'norestore': {F: [("        scene.Timer.Cancel();\n        foreach (var e in scene.Placed)",
                       "        scene.Timer.Cancel();\n        if (!completed) { return; }\n        foreach (var e in scene.Placed)"),
                      ("    public static void Restore(PlayerMobile pm, Map? map)\n    {\n",
                       "    public static void Restore(PlayerMobile pm, Map? map)\n    {\n        return;\n")]},
    # the save leaves the scenes out
    'nosave': {F: [("        foreach (var (player, mapIndex, placed) in TutorialVisionScene.Snapshot())",
                    "        foreach (var (player, mapIndex, placed) in TutorialVisionScene.Snapshot().Take(0))")]},
    # the vision records a real loop (what the scene must never do)
    'loop': {F: [("            case Length: // Light restored, released.\n",
                  "            case Length: // Light restored, released.\n                ClusterFLoops.CompleteLoop(pm, ClusterFLoops.LoopOf(pm) + 1);\n")]},
    # the panels show whatever the setting says
    'panels': {F: [("        if (!ShowPanels) { return; }\n", "")]},
}

for name, files in MUTANTS.items():
    out = os.path.join(HERE, 'm-' + name)
    shutil.rmtree(out, ignore_errors=True)
    shutil.copytree(os.path.join(SRV, 'customizations', 'Tutorial'), out)
    for rel, pairs in files.items():
        p = os.path.join(out, rel)
        s = open(p, encoding='utf-8', newline='').read()
        crlf = '\r\n' in s
        s = s.replace('\r\n', '\n')
        for old, new in pairs:
            assert s.count(old) == 1, (name, old[:60])
            s = s.replace(old, new)
        open(p, 'w', encoding='utf-8', newline='').write(s.replace('\n', '\r\n') if crlf else s)
    print('mutant', name)
