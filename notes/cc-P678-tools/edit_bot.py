r"""cc-P678: the play-test bot's New Haven spots, moved with the town (they run once the server reads SoS, S2).
    python -P edit_bot.py
"""
ROOT = "D:/UO/golems/Iron/ShatteredLegacy/tools/playtest-bot/uobot/"

REPS = {
    "checks_p224_vbuild.py": [
        ("""# The square: new characters used to start a tile from the board at (3502, 2573, 14) (T-039). The work box sits
# east of it, well inside the admin's view.
SQUARE = (3503, 2574, 14)""",
         """# The square: new characters start a tile from the board (T-039; cc-P678: HavenSpots.Start in the author's Haven, the
# board at 3633,2585). The work box sits east of it, well inside the admin's view.
SQUARE = (3634, 2586, 0)"""),
    ],
    "checks_p224_guilds.py": [
        ("""    "smithing": ("BlacksmithGuildmaster", (3469, 2536, 41), "Society of Smiths"),
    "custodians": ("SanitationWarden", (3506, 2560, 21), "The Custodians"),""",
         """    "smithing": ("BlacksmithGuildmaster", (3645, 2617, 0), "Society of Smiths"),     # cc-P678: The Haven Blacksmith
    "custodians": ("SanitationWarden", (3662, 2549, 0), "The Custodians"),           # cc-P678: the League field office"""),
        ("""    # Open ground beside the square (the Warden's post is on a building at z 21: the second trial's orc could not be
    # reached there), and the creature's damage pinned to 1 as well as its hits, so a dragon cannot kill the Custodian.
    move_player(a, p, 3512, 2581, 14)""",
         """    # Open ground near the square (cc-P678: the tutorial's training yard behind the Little Shop of Magic; the Warden's
    # post is indoors), and the creature's damage pinned to 1 as well as its hits, so a dragon cannot kill the Custodian.
    move_player(a, p, 3633, 2562, 0)"""),
    ],
    "checks.py": [
        ("""The board's spot: NewHavenQuestBoard.HomeLocation (3502, 2573, 14), :69.""",
         """The board's spot: NewHavenQuestBoard.HomeLocation (HavenSpots.QuestBoard, 3633, 2585, 0; cc-P678)."""),
    ],
}

for name, reps in REPS.items():
    p = ROOT + name
    s = open(p, encoding="utf-8").read()
    for a, b in reps:
        assert s.count(a) == 1, (name, a[:60])
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
