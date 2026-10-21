"""cc-P276 red run: break the code on purpose (one break per fact), or restore it. Originals saved in the scratch folder
given as the second argument.

    python -P redbreak.py A <scratch>
    python -P redbreak.py restore <scratch>
"""
import os
import shutil
import sys

ROOT = r"D:\ShatteredLegacy\server\customizations"
FILES = {
    "farm": os.path.join(ROOT, r"Tutorial\TutorialFarm.cs"),
    "layout": os.path.join(ROOT, r"Tutorial\TutorialFarmLayout.cs"),
    "tutorial": os.path.join(ROOT, r"Tutorial\ClusterFTutorial.cs"),
    "evo": os.path.join(ROOT, r"Mobiles\Evo\EvoPetData.cs"),
}

A = [
    # fact 1: the live refusal gone
    ("farm", "            if (!IsTestShard() && !AllowLive)", "            if (false)"),
    # fact 2: one porch step the north-facing piece
    ("layout", "        (0x0725, 3382, 2611, 17), // wooden stairs", "        (0x0722, 3382, 2611, 17), // wooden stairs"),
    # fact 3: the pet pick not remembered
    ("farm", "            RecordOf(pm)!.StationsDone.Add(PetKey);\n", ""),
    # fact 4: graduation offers the pick whatever the farm gave
    ("tutorial", "        if (RecordOf(pm)?.StationsDone.Contains(TutorialFarm.PetKey) != true)", "        if (true)"),
    # fact 5: the cat's second stage not Chase's pick
    ("evo", 'new EvoStage(2, "cub", new[] { 1309 }', 'new EvoStage(2, "cub", new[] { 1310 }'),
]


def main():
    mode, scratch = sys.argv[1], sys.argv[2]
    save = os.path.join(scratch, "p276-red-originals")
    if mode == "restore":
        for key, path in FILES.items():
            shutil.copyfile(os.path.join(save, key + ".cs"), path)
        print("restored")
        return
    os.makedirs(save, exist_ok=True)
    for key, path in FILES.items():
        dst = os.path.join(save, key + ".cs")
        if not os.path.exists(dst):
            shutil.copyfile(path, dst)
    for key, old, new in A:
        path = FILES[key]
        s = open(path, encoding="utf-8", newline="").read()
        o = old.replace("\n", "\r\n") if old.replace("\n", "\r\n") in s and "\r\n" in s else old
        n = new.replace("\n", "\r\n") if o != old else new
        if s.count(o) != 1:
            sys.exit("break not found once in %s: %r" % (key, old[:70]))
        open(path, "w", encoding="utf-8", newline="").write(s.replace(o, n))
    print("applied", len(A), "breaks")


if __name__ == "__main__":
    main()
