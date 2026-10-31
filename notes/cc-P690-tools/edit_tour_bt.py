"""cc-P690: tour.py run 14: the treasure map's dig entry by its cliloc; Blackthorn's walk to the storeroom near the
hatch first, then the last stretch exactly, with both hatches avoided until they are the goal. python -P edit_tour_bt.py"""
import os

p = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tour.py")
s = open(p, encoding="utf-8").read()


def rep(a, b):
    global s
    assert s.count(a) == 1, a[:80]
    s = s.replace(a, b)


rep('''            c.pick_context(menu, ent[0])''', '''            c.pick_context(menu, 6148)   # "Dig For Treasure" (run 14: pick_context takes the cliloc, not the entry)''')
rep('''        except Exception:
            pass

    def ok(self, x, y):''', '''        except Exception:
            pass
        # run 14: the two cellar hatches are server items (not in teleporters-sos.json); avoid them unless the goal
        self.avoid |= {(3618, 2620), (1519, 1437)}

    def ok(self, x, y):''')
rep('''    ok = w.go(BT_BESIDE, 0, what="to the storeroom beside the hatch")''', '''    # run 14: one level a tile found no path to the storeroom's floor (the keep stands on the castle's z15 floors);
    # walk to the castle near the hatch, then the last stretch with every level of a tile
    w.go(BT_BESIDE, 6, what="to Blackthorn Castle's keep")
    ok = w.pos() == BT_BESIDE or w.go_exact(BT_BESIDE, (BT_BESIDE[0] - 40, BT_BESIDE[1] - 40, BT_BESIDE[0] + 40, BT_BESIDE[1] + 40),
                                         what="into the storeroom")''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
