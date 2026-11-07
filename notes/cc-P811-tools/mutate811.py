# cc-P811: one folder per break under mutants/, each with the one mutated Casino file. Each break must turn a fact red.
import os, shutil
SRC = 'D:/UO/golems/Iron/ShatteredLegacy/server/customizations/Casino'
OUT = 'D:/UO/golems/Iron/shard-migration/notes/cc-P811-tools/mutants'
C, L, SL, B, SD = 'CasinoSettings.cs', 'CasinoLedger.cs', 'SlotMachine.cs', 'Blackjack.cs', 'CasinoSeeder.cs'
X = [
 ('generous', C, 'Name = "Gem", Weight = 1, Hue = 0x59, PaysThree = 1000', 'Name = "Gem", Weight = 1, Hue = 0x59, PaysThree = 3000'),
 ('nocap', C, '        else if (s.SlotPayback() >= s.MaxPaybackPercent)', '        else if (false)'),
 ('cherrycalc', C, '            back += 3 * c * c * (1 - c) * PaysTwoCherries;', '            back += 3 * c * c * PaysTwoCherries;'),
 ('natural2to1', C, '        if (s.BlackjackPaysNumerator > s.BlackjackPaysDenominator * 3 / 2)', '        if (false)'),
 ('nobetcheck', C, 'if (bets is not { Count: >= 1 and <= 6 } || bets.Any(b => b is < 1 or > 1_000_000))', 'if (false)'),
 ('kindcheck', C, '            if (p.Kind is not ("Slot" or "Blackjack"))', '            if (false)'),
 ('youngok', L, '        if (pm.Young && !CasinoSettings.Current.AllowYoung)', '        if (false)'),
 ('nolimit', L, '        if (gold > Allowance(pm))', '        if (false)'),
 ('nobookin', L, '        In[(int)game] += gold;\n        DayIn', '        DayIn'),
 ('nobookout', L, '        Out[(int)game] += gold;\n', ''),
 ('nosaveopen', L, '        writer.WriteEncodedInt(OpenBets.Count);\n        foreach (var (m, gold) in OpenBets)\n        {\n            writer.Write(m);\n            writer.WriteEncodedInt(gold);\n        }', '        writer.WriteEncodedInt(0);'),
 ('refundtwice', L, '        _refunds.Clear();\n        if (n > 0)', '        if (n > 0)'),
 ('anyversion', L, '        if (version is < 0 or > CurrentVersion)', '        if (version < 0)'),
 ('stopoff', SL, '            roll -= s.Weight;\n', ''),
 ('twocherries', SL, '        return cherries == 2 ? S.PaysTwoCherries : 0;', '        return 0;'),
 ('farplay', SL, ' || !pm.InRange(machine.GetWorldLocation(), S.UseRange))\n        {\n            refusal = "You are too far from the machine.";', ')\n        {\n            refusal = "You are too far from the machine.";'),
 ('deadplay', SL, '        if (!pm.Alive)\n        {\n            refusal = "The dead cannot play.";', '        if (false)\n        {\n            refusal = "The dead cannot play.";'),
 ('anybet', SL, '        if (!S.SlotBets.Contains(bet))', '        if (false)'),
 ('nopay', SL, '        CasinoLedger.Pay(pm, won, CasinoGame.Slots);\n', ''),
 ('gumpspin', SL, '            var result = SlotGame.Play(pm, _machine, _bet, out var refusal);', '            SlotResult result = null; string refusal = null;'),
 ('hardace', B, '        soft = aces && total + 10 <= 21;', '        soft = false;'),
 ('standsoft', B, '            if (v < 17 || v == 17 && soft && hitsSoft17)', '            if (v < 17)'),
 ('pushlose', B, '        return p == d ? BlackjackOutcome.Push : BlackjackOutcome.Lose;', '        return BlackjackOutcome.Lose;'),
 ('natural32', B, '        BlackjackOutcome.Natural => stake + stake * num / den,', '        BlackjackOutcome.Natural => stake + stake * 3 / 2,'),
 ('twohands', B, '        if (Hands.TryGetValue(pm, out var open) && open.Live)', '        if (false)'),
 ('noopenbet', B, '        CasinoLedger.OpenBets[pm] = bet;\n\n        if (IsNatural', '\n        if (IsNatural'),
 ('nodoublestake', B, '        var refusal = CasinoLedger.TryTake(pm, hand.Bet, CasinoGame.Blackjack);\n        if (refusal != null)\n        {\n            return refusal;\n        }\n\n        hand.Bet *= 2;', '        hand.Bet *= 2;'),
 ('nobust', B, '        if (Value(hand.Player) > 21)\n        {\n            Settle(pm, hand, BlackjackOutcome.Bust);\n        }\n        else if', '        if (false)\n        {\n        }\n        else if'),
 ('nodress', B, '        _cards = new Static(0xFA3) { Name = "playing cards" };\n        _cards.MoveToWorld(new Point3D(X, Y, Z + 6), Map);', '        return;'),
 ('cardsstay', B, '            _cards.Location = new Point3D(X, Y, Z + 6);', '            _cards.Location = _cards.Location;'),
 ('seedtwice', SD, '            if (p.Kind == "Slot" && !StandsAt<SlotMachine>(map, at))', '            if (p.Kind == "Slot")'),
 ('seedclosed', SD, '        if (!s.Enabled)\n        {\n            return 0;\n        }', ''),
]
shutil.rmtree(OUT, ignore_errors=True)
n = 0
for name, f, old, new in X:
    s = open(os.path.join(SRC, f), encoding='utf-8').read()
    if s.count(old) != 1:
        print('NO MATCH', name, s.count(old)); continue
    d = os.path.join(OUT, name); os.makedirs(d)
    open(os.path.join(d, f), 'w', encoding='utf-8', newline='').write(s.replace(old, new)); n += 1
print(n, 'mutants')
