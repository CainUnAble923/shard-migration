"""cc-P610 (P533 U4 part 5): playthrough.graduate fails a graduation whose rewards are missing.

    python -P -m unittest test_graduation_rewards     (from this folder)

A stand-in client plays the graduation exchange with the server's lines and gumps chosen per test: nothing connects to a
shard. A graduation with no companion pick or no graduation box must leave failed checks; one with both must not; a
character that already has its farm pet passes without a pick.
"""
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import playthrough  # noqa: E402


class Gump:
    def __init__(self, texts, buttons=()):
        self.texts = list(texts)
        self.buttons = list(buttons)


class FakeClient:
    """Just what graduate() reads. Pressing Graduate (button 3) makes the server's answer appear."""

    def __init__(self, pick, box, wording="new"):
        self.gumps, self.messages, self.items = [], [], {}
        self.pack, self.contents_ = 0x40000001, []
        self.pick, self.box, self.wording = pick, box, wording

    def gump_text(self, g):
        return g.texts

    def gump_buttons(self, g):
        return g.buttons

    def reply_gump(self, g, button):
        new = self.wording == "new"
        if button == 4 and self.pick:   # Rook's "Choose your pet" opens the pick again
            self.gumps.append(Gump(["You earned a pet: choose one" if new else "You have earned a companion. Choose one:"]))
            return
        if button != 3:
            return
        self.messages.append({"text": "System: You finished the tutorial. You can now leave Haven Island." if new else
                              "System: Graduated. New Haven survived you."})
        self.messages.append({"text": "System: Double-click your reward box here in town to open it." if new else
                              "System: Open that box here in town."})
        if self.pick:
            self.messages.append({"text": "System: You earned a pet. Click Choose beside the pet you want." if new else
                                  "System: You have earned a companion."})
            self.gumps.append(Gump(["You earned a pet: choose one" if new else "You have earned a companion. Choose one:"]))
        if self.box:
            serial = 0x40000100
            self.items[serial] = {"graphic": 0x9A8}
            self.contents_.append(serial)
            self.box_serial = serial

    def sleep(self, s):
        pass

    def find_text(self, pattern, since=0):
        return next((m for m in self.messages[since:] if re.search(pattern, m["text"] or "")), None)

    def wait_gump(self, pred, timeout=8, since=0):
        return next((g for g in self.gumps[since:] if pred(g)), None)

    def backpack(self):
        return self.pack

    def contents(self, serial):
        return list(self.contents_)

    def opl(self, serial):
        if self.box and serial == getattr(self, "box_serial", None):
            return ["a reward box", "earned for finishing the New Haven tutorial" if self.wording == "new" else
                    "earned for graduating the New Haven tutorial"]
        return []

    def dclick(self, serial):
        if self.box and serial == self.box_serial:
            self.messages.append({"text": "You open the box and receive its contents."})
            elixir = 0x40000200
            self.items[elixir] = {"graphic": 0x24E2}
            self.contents_.append(elixir)


class FakePlayer:
    def __init__(self, c):
        self.c = c

    def go(self, *a, **k):
        return True

    def drain(self):
        pass

    def open_pack(self):
        pass

    def log(self, text):
        pass


class Log(playthrough.Log):
    def __init__(self):
        self.fails = []
        self.lines = []

    def __call__(self, text):
        self.lines.append(text)


class GraduationRewards(unittest.TestCase):
    def setUp(self):
        self._station = playthrough.recruiter_station
        playthrough.recruiter_station = lambda pl, key: Gump(["Graduate", "Choose your pet"])

    def tearDown(self):
        playthrough.recruiter_station = self._station

    def run_graduation(self, pick, box, expect_pick, wording="new"):
        c = FakeClient(pick, box, wording)
        log = Log()
        try:
            playthrough.graduate(FakePlayer(c), log, "core", expect_pick=expect_pick)
        except TypeError:
            playthrough.graduate(FakePlayer(c), log, "core")   # the driver before cc-P610 has no expect_pick
        return log.fails

    def test_a_missing_pick_and_box_fail_the_graduation(self):
        fails = self.run_graduation(pick=False, box=False, expect_pick=True)
        self.assertTrue(any("pick" in f for f in fails), fails)
        self.assertTrue(any("graduation box" in f for f in fails), fails)

    def test_a_missing_box_fails_even_with_the_pick(self):
        fails = self.run_graduation(pick=True, box=False, expect_pick=True)
        self.assertTrue(any("graduation box" in f for f in fails), fails)

    def test_a_full_graduation_passes_in_either_wording(self):
        for wording in ("new", "old"):
            fails = self.run_graduation(pick=True, box=True, expect_pick=True, wording=wording)
            self.assertEqual([], [f for f in fails if "pick" in f or "box" in f or "graduated" in f or "town" in f
                                  or "companion" in f or "elixir" in f], (wording, fails))

    def test_a_farm_pet_holder_passes_without_a_pick(self):
        fails = self.run_graduation(pick=False, box=True, expect_pick=False)
        self.assertEqual([], [f for f in fails if "pick" in f], fails)


if __name__ == "__main__":
    unittest.main()
