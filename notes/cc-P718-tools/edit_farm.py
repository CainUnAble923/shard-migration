import os
os.chdir(r"D:\UO\golems\Iron\ShatteredLegacy\server\customizations\Tutorial")


def edit(p, pairs):
    s = open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, (p, old[:70], s.count(old))
        s = s.replace(old, new)
    open(p, "w", encoding="utf-8", newline="").write(s)


edit("TutorialFarm.cs", [
# -- header note
("""namespace Server.Tutorial
{
    public static class TutorialFarm
    {""", """// cc-P718 (Chase's isle walk, 10-28): step 2 begins with the pet commands (items 10): Wren sets the pet to stay and the
// trainee makes it follow ("all follow me") and guard ("all guard me"), by speech or the pet's menu; the pet's own order
// is the evidence, so either way counts. Then the pest part opens: Wren opens the field gate (TutorialPestGate, which only
// a trainee on that part or staff can open), the pests fight only such a trainee or their pet (item 7) and never step
// outside the field fence, and one of the pests must fall to the pet on "all kill". Step 3's line now says how to use a
// bandage and how to make more (item 9).

namespace Server.Tutorial
{
    public static class TutorialFarm
    {"""),
# -- constants
("""        public const string HealLine = "Double-click a bandage in your backpack, then click yourself or an injured pet. A successful heal finishes this step.";""",
 """        public const string HealLine = "Here are some bandages. To heal, double-click a bandage in your backpack, then click yourself or your hurt pet. A successful heal finishes this step.";
        // cc-P718 item 9: the one line on making more, said after the bandages are handed over.
        public const string MakeBandagesLine = "Later you can make your own bandages: double-click a pair of scissors, then click a pile of cloth to cut it into bandages.";

        // cc-P718 item 10: the pet commands, the first part of step 2.
        public const string FollowKey = "farm.cmd.follow";
        public const string GuardKey = "farm.cmd.guard";
        public const string CommandsLine = "Your pet obeys spoken commands. I told it to stay. Say 'all follow me' and it follows you; then say 'all guard me' and it guards you. You can say your pet's name instead of 'all', or click your pet with the right mouse button and choose a command from its menu.";
        public const string FollowDoneLine = "Your pet follows you. Now say 'all guard me', or choose Guard from your pet's menu.";
        public const string GuardDoneLine = "Your pet guards you. I opened the field gate for you: walk into the cabbage rows, say 'all kill', then click a rat or grass snake for your pet to attack. Defeat {0} pests. If the gate swings shut, double-click it to open it.";
        public const string NoPetForCommandsLine = "You have no pet with you, so the command lesson is skipped. I opened the field gate: defeat {0} rats or grass snakes in the cabbage rows.";
        public const string PetKillLine = "Now let your pet fight one: say 'all kill', then click a rat or grass snake.";
        public const string GateClosedLine = "Wren keeps this gate shut until your pest lesson. Double-click Wren the Farmhand first.";

        /// <summary>
        /// cc-P718 item 7: inside the field fence (P276's x 3381-3399, y 2603-2619, moved to the isle), where the pests stay.
        /// End points exclusive (Rectangle2D): x 6696-6712, y 3968-3982.
        /// </summary>
        public static readonly Rectangle2D PestField = new(OnIsle(new Point2D(3382, 2604)), OnIsle(new Point2D(3399, 2619)));

        /// <summary>cc-P718: the two tiles of the field's gate in its east fence (the layout leaves them open).</summary>
        public static readonly Point2D[] FieldGateSpots = [new(6713, 3978), new(6713, 3979)];"""),
# -- step 2 talk and step 3 talk
("""                case 2:
                    var left = Math.Max(0, PestsToClear - PestsKilled(pm));
                    hand.SayTo(pm, PestsKilled(pm) == 0 ? string.Format(PestsLine, PestsToClear) : string.Format(PestsLeftLine, left));
                    break;
                case 3:
                    var gift = GiveBandages(pm);
                    hand.SayTo(pm, gift switch
                    {
                        BandageGift.NoneLeft => NoMoreBandagesLine,
                        BandageGift.NoRoom => NoRoomForBandagesLine,
                        _ => Scratch(pm) ? ScratchLine : HealLine
                    });
                    break;""", """                case 2 when !CommandsDone(pm):
                    hand.SayTo(pm, BeginCommands(pm) ? CommandsLine : string.Format(NoPetForCommandsLine, PestsToClear));
                    break;
                case 2:
                    OpenFieldGate(hand.Map);
                    var left = Math.Max(0, PestsToClear - PestsKilled(pm));
                    hand.SayTo(pm, PestsKilled(pm) == 0 ? string.Format(PestsLine, PestsToClear) : string.Format(PestsLeftLine, left));
                    break;
                case 3:
                    var gift = GiveBandages(pm);
                    hand.SayTo(pm, gift switch
                    {
                        BandageGift.NoneLeft => NoMoreBandagesLine,
                        BandageGift.NoRoom => NoRoomForBandagesLine,
                        _ => Scratch(pm) ? ScratchLine : HealLine
                    });
                    if (gift is BandageGift.Given or BandageGift.HasSome)
                    {
                        hand.SayTo(pm, MakeBandagesLine); // cc-P718 item 9
                    }

                    break;"""),
# -- choose pet: begin commands
("""            RecordOf(pm)!.PetClaimed = true;
            ClusterFTutorial.SystemLine(pm, EchoPetLine);
            CheckDone(pm);
            return pet;""", """            RecordOf(pm)!.PetClaimed = true;
            ClusterFTutorial.SystemLine(pm, EchoPetLine);
            if (!CheckDone(pm) && StepOf(pm) == 2 && !CommandsDone(pm))
            {
                ClusterFTutorial.SystemLine(pm, BeginCommands(pm) ? CommandsLine : string.Format(NoPetForCommandsLine, PestsToClear));
            }

            return pet;"""),
# -- pest death: only the pest part counts, and whether the pet did it on command
("""                if (who is PlayerMobile pm && StepOf(pm) == 2 && credited.Add(pm))
                {
                    CountPest(pm);
                }
            }
        }

        public static void CountPest(PlayerMobile pm)
        {
            var n = PestsKilled(pm) + 1;
            _pestsKilled[pm.Serial] = n;

            if (n < PestsToClear)
            {
                pm.SendMessage(0x3B2, $"Farm pests defeated: {n} of {PestsToClear}.");
                return;
            }

            _pestsKilled.Remove(pm.Serial);""", """                if (who is PlayerMobile pm && PestPartOn(pm) && credited.Add(pm))
                {
                    CountPest(pm, ByPetOnCommand(pest, pm));
                }
            }
        }

        // cc-P718: a pest the trainee's pet damaged while under the kill command.
        private static bool ByPetOnCommand(FarmPest pest, PlayerMobile pm)
        {
            foreach (var entry in pest.DamageEntries)
            {
                if (entry.Damager is BaseCreature { Controlled: true } pet && pet.ControlMaster == pm && pet.ControlOrder == OrderType.Attack)
                {
                    return true;
                }
            }

            return false;
        }

        // Trainees whose pet has felled a pest on command this run (in memory, like the count).
        private static readonly HashSet<Serial> _petKilled = new();

        /// <summary>A pest counts for the trainee; staff and tests credit it as the pet's, on command.</summary>
        public static void CountPest(PlayerMobile pm) => CountPest(pm, true);

        public static void CountPest(PlayerMobile pm, bool byPetOnCommand)
        {
            if (byPetOnCommand)
            {
                _petKilled.Add(pm.Serial);
            }

            var n = PestsKilled(pm) + 1;
            _pestsKilled[pm.Serial] = n;

            if (n < PestsToClear)
            {
                pm.SendMessage(0x3B2, $"Farm pests defeated: {n} of {PestsToClear}.");
                return;
            }

            // cc-P718 item 10: at least one pest falls to the pet on "all kill", when the trainee has a pet with them.
            if (!_petKilled.Contains(pm.Serial) && PetsOf(pm).Count > 0)
            {
                ClusterFTutorial.SystemLine(pm, PetKillLine);
                return;
            }

            _pestsKilled.Remove(pm.Serial);
            _petKilled.Remove(pm.Serial);"""),
# -- the commands machinery, after CheckDone
("""        public enum BandageGift { Given, HasSome, NoneLeft, NoRoom }""", """        // -- cc-P718 item 10: the pet commands --

        public static bool CommandsDone(PlayerMobile pm) => Has(pm, FollowKey) && Has(pm, GuardKey);

        /// <summary>cc-P718: the pest part of step 2, after the commands: the pests fight the trainee only now.</summary>
        public static bool PestPartOn(PlayerMobile pm) => StepOf(pm) == 2 && CommandsDone(pm);

        /// <summary>The trainee's living pets on their map.</summary>
        public static List<BaseCreature> PetsOf(PlayerMobile pm)
        {
            var pets = new List<BaseCreature>();
            foreach (var f in pm.AllFollowers ?? [])
            {
                if (f is BaseCreature { Controlled: true, Alive: true, Deleted: false, IsDeadBondedPet: false } pet &&
                    pet.ControlMaster == pm && pet.Map == pm.Map)
                {
                    pets.Add(pet);
                }
            }

            return pets;
        }

        private static readonly HashSet<PlayerMobile> _watching = new();
        private static TimerExecutionToken _watchTimer;

        /// <summary>
        /// Starts the commands: the trainee's pets stay, and their orders are watched until they follow and then guard.
        /// False when the trainee has no pet with them: the commands are skipped and the field gate opens.
        /// </summary>
        public static bool BeginCommands(PlayerMobile pm)
        {
            var pets = PetsOf(pm);
            if (pets.Count == 0)
            {
                var record = RecordOf(pm)!;
                record.StationsDone.Add(FollowKey);
                record.StationsDone.Add(GuardKey);
                OpenFieldGate(pm.Map);
                return false;
            }

            if (!Has(pm, FollowKey))
            {
                foreach (var pet in pets)
                {
                    pet.ControlTarget = null;
                    pet.ControlOrder = OrderType.Stay;
                }
            }

            _watching.Add(pm);
            if (!_watchTimer.Running)
            {
                Timer.StartTimer(TimeSpan.FromMilliseconds(500), TimeSpan.FromMilliseconds(500), WatchAll, out _watchTimer);
            }

            return true;
        }

        private static void WatchAll()
        {
            foreach (var pm in new List<PlayerMobile>(_watching))
            {
                CheckCommands(pm);
            }

            if (_watching.Count == 0)
            {
                _watchTimer.Cancel();
            }
        }

        /// <summary>Reads the pets' orders (speech or menu, both set them): follow first, then guard. True when both are done.</summary>
        public static bool CheckCommands(PlayerMobile pm)
        {
            if (pm.Deleted || StepOf(pm) != 2 || CommandsDone(pm))
            {
                _watching.Remove(pm);
                return CommandsDone(pm);
            }

            var pets = PetsOf(pm);
            var record = RecordOf(pm)!;
            if (!Has(pm, FollowKey) && pets.Exists(p => p.ControlOrder == OrderType.Follow && p.ControlTarget == pm))
            {
                record.StationsDone.Add(FollowKey);
                ClusterFTutorial.SystemLine(pm, FollowDoneLine);
            }
            else if (Has(pm, FollowKey) && pets.Exists(p => p.ControlOrder == OrderType.Guard))
            {
                record.StationsDone.Add(GuardKey);
                _watching.Remove(pm);
                OpenFieldGate(pm.Map);
                ClusterFTutorial.SystemLine(pm, string.Format(GuardDoneLine, PestsToClear));
                return true;
            }

            return false;
        }

        // -- cc-P718 item 7: the field gate --

        /// <summary>The field gate's two halves on <paramref name="map"/>, open or closed.</summary>
        public static List<TutorialPestGate> FieldGates(Map? map)
        {
            var gates = new List<TutorialPestGate>();
            if (map == null)
            {
                return gates;
            }

            foreach (var spot in FieldGateSpots)
            {
                if (FindDoor(map, TutorialWorld.Ground(map, spot)) is TutorialPestGate gate)
                {
                    gates.Add(gate);
                }
            }

            return gates;
        }

        /// <summary>Wren opens the field gate (it closes again by itself, as any gate).</summary>
        public static void OpenFieldGate(Map? map)
        {
            foreach (var gate in FieldGates(map))
            {
                if (!gate.Open)
                {
                    gate.Open = true;
                }
            }
        }

        /// <summary>The gate's halves: the north one swings north, the south one south.</summary>
        public static TutorialPestGate[] MakeFieldGates() => [new(DoorFacing.SouthCW), new(DoorFacing.NorthCCW)];

        public enum BandageGift { Given, HasSome, NoneLeft, NoRoom }"""),
# -- seed the gates
("""            if (TutorialFarmhand.Find(map) != null) { present++; }""", """            // cc-P718 item 7: the field gate, closed, in the gap of the east fence.
            var gates = MakeFieldGates();
            for (var i = 0; i < FieldGateSpots.Length; i++)
            {
                var spot = TutorialWorld.Ground(map, FieldGateSpots[i]);
                if (FindDoor(map, spot) != null) { present++; gates[i].Delete(); }
                else if (dryRun) { doors++; gates[i].Delete(); }
                else { gates[i].MoveToWorld(spot, map); doors++; }
            }

            if (TutorialFarmhand.Find(map) != null) { present++; }"""),
# -- the pests: passive and fenced
("""    /// <summary>A farm pest: a tutorial-only creature (it engages only participants) that counts for the farm's step 2.</summary>
    [SerializationGenerator(0, false)]
    public abstract partial class FarmPest : TutorialCreature
    {
        protected FarmPest()
        {
        }
""", """    /// <summary>A farm pest: a tutorial-only creature (it engages only participants) that counts for the farm's step 2.</summary>
    [SerializationGenerator(0, false)]
    public abstract partial class FarmPest : TutorialCreature
    {
        protected FarmPest()
        {
        }

        // cc-P718 item 7: a pest fights only a trainee on the pest part of the farm lesson, or that trainee's pet; anyone
        // earlier in the lessons is never attacked, and a blow from them does nothing.
        public static bool Fights(Mobile? m)
        {
            var player = m is BaseCreature { Controlled: true } pet ? pet.ControlMaster : m;
            return player is PlayerMobile pm && TutorialFarm.PestPartOn(pm);
        }

        public override bool IsEnemy(Mobile m) => Fights(m) && base.IsEnemy(m);

        public override bool CanBeHarmful(Mobile target, bool message, bool ignoreOurBlessedness) =>
            Fights(target) && base.CanBeHarmful(target, message, ignoreOurBlessedness);

        public override void Damage(int amount, Mobile? from = null, bool informMount = true, bool ignoreEvilOmen = false)
        {
            if (from != null && !Fights(from))
            {
                return;
            }

            base.Damage(amount, from, informMount, ignoreEvilOmen);
        }

        // ...and never steps outside the field fence, even through an open gate.
        public override bool CheckMovement(Direction d, out int newZ)
        {
            int x = X, y = Y;
            Movement.Movement.Offset(d, ref x, ref y);
            if (!TutorialFarm.PestField.Contains(new Point2D(x, y)) && FoldMaps.IsFold(Map))
            {
                newZ = Z;
                return false;
            }

            return base.CheckMovement(d, out newZ);
        }
"""),
# -- the gate class, after the snake
("""        public override string CorpseName => "a snake corpse";
    }
}""", """        public override string CorpseName => "a snake corpse";
    }

    /// <summary>
    /// cc-P718 item 7: the farm field's gate. A light wood gate that a trainee opens only on the pest part of the farm
    /// lesson (or later), and staff always; Wren opens it when that part begins. It closes by itself, as any gate.
    /// </summary>
    [SerializationGenerator(0, false)]
    public partial class TutorialPestGate : LightWoodGate
    {
        [Constructible]
        public TutorialPestGate(DoorFacing facing) : base(facing) => Name = "farm field gate";

        public override void Use(Mobile from)
        {
            if (from.AccessLevel == AccessLevel.Player && !Open &&
                !(from is PlayerMobile pm && (TutorialFarm.PestPartOn(pm) || TutorialFarm.StepOf(pm) >= 3)))
            {
                from.SendMessage(0x3B2, TutorialFarm.GateClosedLine);
                return;
            }

            base.Use(from);
        }
    }
}"""),
])
print("ok")
