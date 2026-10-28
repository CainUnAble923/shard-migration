r"""cc-P678: the console drops ClusterFSeedNewHavenServices (retired with the ML plaza's decoration).
    python -P edit_console.py
"""
ROOT = "D:/UO/golems/Iron/ShatteredLegacy/scripts/"


def edit(name, reps):
    p = ROOT + name
    raw = open(p, "rb").read()
    bom = raw[:3] == b"\xef\xbb\xbf"
    s = raw.decode("utf-8-sig")
    for a, b in reps:
        assert s.count(a) == 1, (name, a[:60])
        s = s.replace(a, b)
    open(p, "wb").write((b"\xef\xbb\xbf" if bom else b"") + s.encode("utf-8"))


edit("Shard-Console.ps1", [
    ("""        Title  = 'Existing world: New Haven services, NPCs and guild halls, in this order'
        Source = 'notes/cc-P17-playtest-bugs-1.md:624-637 (a fresh world runs the first two after the spawn files, :634-637)'
        Steps  = @(
            (New-OrderStep 'ClusterFSeedNewHavenServices' 'dryrun')
            (New-OrderStep 'ClusterFSeedNewHavenServices')
            (New-OrderStep 'ClusterFSeedNewHaven' 'dryrun')""",
     """        Title  = 'Existing world: New Haven NPCs and guild halls, in this order'
        # cc-P678: ClusterFSeedNewHavenServices (the ML plaza's decoration and stand-in Healer) retired with the plaza.
        Source = 'notes/cc-P17-playtest-bugs-1.md:624-637 (a fresh world runs the first two after the spawn files, :634-637)'
        Steps  = @(
            (New-OrderStep 'ClusterFSeedNewHaven' 'dryrun')"""),
])

edit("tests/Shard-Console.Tests.ps1", [
    ("""    # cc-P678 retired ClusterFOldHavenCleanup (on SoS it would delete New Haven's own vendors), so ten of the eleven.
    $eleven = 'ClusterFSeedGuildHalls', 'ClusterFSeedNewHaven', 'ClusterFSeedOldHaven', 'ClusterFSeedInstitutions',
              'ClusterFSeedNewHavenServices', 'ClusterFSeedResetStone', 'ClusterFSeedMineCamp', 'ClusterFSouthMineDecor',""",
     """    # cc-P678 retired ClusterFOldHavenCleanup (on SoS it would delete New Haven's own vendors) and
    # ClusterFSeedNewHavenServices (the ML plaza's decoration), so nine of the eleven.
    $eleven = 'ClusterFSeedGuildHalls', 'ClusterFSeedNewHaven', 'ClusterFSeedOldHaven', 'ClusterFSeedInstitutions',
              'ClusterFSeedResetStone', 'ClusterFSeedMineCamp', 'ClusterFSouthMineDecor',"""),
    ("""    # cc-P678: ClusterFOldHavenCleanup retired, so eight.""",
     """    # cc-P678: ClusterFOldHavenCleanup and ClusterFSeedNewHavenServices retired, so seven."""),
    ("""            'ClusterFSeedNewHavenServices', 'ClusterFSeedOldHaven', 'ClusterFSeedResetStone', 'ClusterFSouthMineDecor'""",
     """            'ClusterFSeedOldHaven', 'ClusterFSeedResetStone', 'ClusterFSouthMineDecor'"""),
])
print("ok")
