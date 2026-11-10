"""cc-P862: write the red mutants into red/ from the real Battle Chess files (each mutant replaces the file after "__").
Each change breaks one behaviour a fact claims; a mutant that every fact still passes would mean a fact checks nothing.
  python -P make_mutants.py"""
import os

SRC = "D:/UO/golems/Iron/ShatteredLegacy/server/customizations/BattleChess"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "red")
os.makedirs(OUT, exist_ok=True)


def mutate(name, tag, changes):
    s = open(os.path.join(SRC, name), encoding="utf-8").read()
    for old, new in changes:
        if old not in s:
            raise SystemExit("%s: not found: %r" % (tag, old[:70]))
        s = s.replace(old, new, 1)
    open(os.path.join(OUT, "%s__%s" % (tag, name)), "w", encoding="utf-8").write(s)
    print("wrote", tag, name, len(changes), "change(s)")


# The rules: no en passant, castling through an attacked square, and a refusal that does not say why.
mutate("ChessRules.cs", "m-rules", [
    ("            else if (EnPassantSquare == to)", "            else if (false && EnPassantSquare == to)"),
    ("!IsAttacked(new Square(5, rank), enemy) && !IsAttacked(new Square(6, rank), enemy)", "true"),
    ("            refusal = WhyNot(piece, from, to);", "            refusal = \"Illegal move.\";"),
    ("        if (HalfMoves >= 100)", "        if (HalfMoves >= 1000)"),
])

# The seeder: places a board at every load, whether or not one stands there.
mutate("BattleChessSeeder.cs", "m-seed", [
    ("        if (!s.Enabled || Find() != null)", "        if (!s.Enabled)"),
])

# The game: the taken piece stays, results are not booked, the promotion choice is ignored, an invitation does not check
# the range, a piece deleted by staff leaves the game running.
mutate("BattleChessGame.cs", "m-game", [
    ("            victim?.Vanish();\n", "\n"),
    ("            BattleChessRecords.Book(winner, Opponent(winner));", "            // not booked"),
    ("        _pending.Promotion = kind;", "        _pending.Promotion = PieceKind.Queen;"),
    ("        else if (guest.Map != Board.Map || !guest.InRange(Board.Center, S.StartRange))", "        else if (false)"),
    ("            Abort(\"A piece was removed from the board, so the game was stopped. No result was kept.\");", ""),
])

# The board: the rim's corners swapped and the squares' colours inverted.
mutate("BattleChessBoard.cs", "m-board", [
    ("        (0, 0) => CornerNW,", "        (0, 0) => CornerSE,"),
    ("    public static bool IsDark(Square s) => (s.File + s.Rank) % 2 == 0;", "    public static bool IsDark(Square s) => (s.File + s.Rank) % 2 == 1;"),
])

# The records: the version is not checked, and draws are not saved.
mutate("BattleChessRecords.cs", "m-records", [
    ("        if (version is < 0 or > CurrentVersion)", "        if (false)"),
    ("            writer.WriteEncodedInt(r.Draws);", "            writer.WriteEncodedInt(0);"),
])

# The settings: a move limit of 0 minutes is let through.
mutate("BattleChessSettings.cs", "m-settings", [
    ("        Range(s.MoveMinutes, 1, 120, nameof(MoveMinutes), errors);", ""),
])
