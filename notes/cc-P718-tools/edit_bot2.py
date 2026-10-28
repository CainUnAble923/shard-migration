p = r"D:\UO\golems\Iron\shard-migration\notes\cc-P718-tools\isle.py"
s = open(p, encoding="utf-8").read()
old = """    order = [c.serial] if scratched else ([pet] if pet else []) + [c.serial]
    for who in order:
        n = len(c.messages)
        c.sleep(1.2)
        c.dclick(band)
        if not c.wait_target(5):
            log("  the bandage gave no target cursor")
            continue
        c.target_obj(who)
        log("  -> bandage on %s" % ("the pet" if who != c.serial else "yourself"))
        if c.find_text(r"Your bandage restored health", since=n, timeout=14):
            break
        pl.drain()"""
new = """    # cc-P718: the pet may be guarding in the field ("That is too far away"); after a scratch ("nipped") the bot bandages
    # itself at once, as the line tells a player to, before the scratch regenerates away.
    who = c.serial if scratched or not pet else pet
    for _ in range(4):
        n = len(c.messages)
        c.sleep(1.2)
        c.dclick(band)
        if not c.wait_target(5):
            log("  the bandage gave no target cursor")
            continue
        c.target_obj(who)
        log("  -> bandage on %s" % ("the pet" if who != c.serial else "yourself"))
        said = c.find_text(r"Your bandage restored health|nipped|too far away|not damaged", since=n, timeout=14)
        if c.find_text(r"Your bandage restored health", since=n):
            break
        if said is None:
            c.find_text(r"Your bandage restored health|nipped", since=n, timeout=8)
            if c.find_text(r"Your bandage restored health", since=n):
                break
        who = c.serial
        pl.drain()"""
assert s.count(old) == 1
s = s.replace(old, new)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
