"""cc-P666: the first-play fact's vet step follows the isle rule."""
p = 'D:/UO/golems/Iron/ShatteredLegacy/server/tests/Tutorial/TutorialFirstPlayVerification.cs'
t = open(p, 'rb').read().decode('utf-8')
crlf = '\r\n' in t
t = t.replace('\r\n', '\n')
old = '''        vet.OnMovement(p.Pm, new Point3D(p.Pm.X + 10, p.Pm.Y, p.Pm.Z));
        var offer = p.Pm.FindGump<TutorialVetResurrectGump>();
        Assert.NotNull(offer);
        offer!.OnResponse(p.Ns, Press(1));
        Assert.False(pet.IsDeadBondedPet);
'''
new = '''        vet.OnMovement(p.Pm, new Point3D(p.Pm.X + 10, p.Pm.Y, p.Pm.Z));
        // cc-P666: on the isle, a Young owner's pet within 3 tiles of the vet comes back at once, with no window.
        Assert.Null(p.Pm.FindGump<TutorialVetResurrectGump>());
        Assert.False(pet.IsDeadBondedPet);
'''
assert t.count(old) == 1
t = t.replace(old, new)
if crlf:
    t = t.replace('\n', '\r\n')
open(p, 'wb').write(t.encode('utf-8'))
print('ok')
