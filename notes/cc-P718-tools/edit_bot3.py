p = r"D:\UO\golems\Iron\shard-migration\notes\cc-P718-tools\isle.py"
s = open(p, encoding="utf-8").read()


def rep(old, new):
    global s
    assert s.count(old) == 1, old[:70]
    s = s.replace(old, new)


rep('''def open_field_gate(pl, log):
    """cc-P718: Wren opens the field gate; if it has swung shut, double-click each closed half."""
    c = pl.c
    for spot in FIELD_GATE:
        for gid in GATE_CLOSED:
            g = pl.item_at(spot, gid, 0)
            if g:
                pl.go(BELOW_WREN, 0)''', '''INSIDE_GATE = (6712, 3979)                 # the field's side of the gate


def in_field(xy):
    return 6696 <= xy[0] <= 6712 and 3968 <= xy[1] <= 3982


def open_field_gate(pl, log, stand=None):
    """cc-P718: Wren opens the field gate; if it has swung shut, double-click it (from outside, or from the field)."""
    c = pl.c
    stand = stand or BELOW_WREN
    for spot in FIELD_GATE:
        for gid in GATE_CLOSED:
            g = pl.item_at(spot, gid, 0)
            if g:
                pl.go(stand, 0)''')
rep('''def t_death(pl, log):
    c = pl.c''', '''def t_death(pl, log):
    c = pl.c
    if in_field(pl.pos()):  # cc-P718: still in the field after the farm; the gate may have swung shut
        open_field_gate(pl, log, INSIDE_GATE)''')
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
