p = r"D:\UO\golems\Iron\ShatteredLegacy\server\customizations\Tutorial\TutorialFarm.cs"
s = open(p, encoding="utf-8").read()


def rep(old, new):
    global s
    assert s.count(old) == 1, old[:80]
    s = s.replace(old, new)


# -- header
pairs = [("""namespace Server.Tutorial
{
    public static class TutorialFarm
    {""", """// cc-P721 (Chase 10-28 09:16 to 09:31): the heal step has a patient who stays hurt, Pip the farm boy (his hits never
// come back by themselves, and he is cut again after each heal), Wren says that a bandage takes a few seconds, and on the
// isle a trainee's bandage says how long to wait, shows a cue over their head, says plainly when it fails, and takes 4 s
// on themselves (Bandage-tutorial-wait-lines.patch). Before the pests, Wren hands a pitchfork (kept, like the cloak)
// and waits until it is held, then until war mode is on (Tab, or the Peace/War button); the pest part also wants one
// pest struck by the trainee themselves.

namespace Server.Tutorial
{
    public static class TutorialFarm
    {"""),
# -- lines
("""        public const string HealLine = "Here are some bandages. To heal, double-click a bandage in your backpack, then click yourself or your hurt pet. A successful heal finishes this step.";""",
 """        public const string HealLine = "Here are some bandages. To heal, double-click a bandage in your backpack, then click yourself or your hurt pet. A successful heal finishes this step.";
        // cc-P721: the heal step's patient, and how long a bandage takes.
        public const string PipLine = "Here are some bandages. Pip, my helper, cut his arm on the fence. Double-click a bandage in your backpack, then click Pip.";
        public const string WaitLine = "A bandage takes a few seconds. You will see 'You begin applying the bandages': stand still and wait until 'You finish applying the bandages'. A bandage that heals finishes this step.";
        public const string PipNotYouLine = "You are not hurt. Pip is the one who needs it: double-click a bandage, then click Pip beside Wren.";
        public const string FumbleLine = "You fumble the bandage. Try again: double-click a bandage, then click your patient.";
        public const double IsleSelfBandageSeconds = 4.0;"""),
("""        public const string GuardDoneLine = "Your pet guards you. I opened the field gate for you: walk into the cabbage rows, say 'all kill', then click a rat or grass snake for your pet to attack. Defeat {0} pests. If the gate swings shut, double-click it to open it.";""",
 """        public const string GuardDoneLine = "Your pet guards you. Now a weapon: I put a pitchfork in your backpack. Drag it onto your character's hand in your character window, or double-click it, to hold it.";
        // cc-P721: the weapon and war mode, before the first fight.
        public const string WeaponKey = "farm.weapon";
        public const string WarKey = "farm.war";
        public const string WeaponDoneLine = "You hold the pitchfork. Now press Tab, or click the Peace/War button on your character window, to switch to war mode: that is how you fight. Press Tab again for peace mode when you are done.";
        public const string WarDoneLine = "You are in war mode. I opened the field gate for you: walk into the cabbage rows and double-click a rat or grass snake to attack it yourself, then say 'all kill' and click one for your pet. Defeat {0} pests. If the gate swings shut, double-click it to open it.";
        public const string StrikeLine = "Now strike one yourself: in war mode, double-click a rat or grass snake.";"""),
("""        public const string NoPetForCommandsLine = "You have no pet with you, so the command lesson is skipped. I opened the field gate: defeat {0} rats or grass snakes in the cabbage rows.";""",
 """        public const string NoPetForCommandsLine = "You have no pet with you, so the pet commands are skipped. Now a weapon: I put a pitchfork in your backpack. Drag it onto your character's hand in your character window, or double-click it, to hold it.";"""),
# -- step 3 talk: Pip and the wait
("""                case 3:
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

                    break;""", """                case 3:
                    var gift = GiveBandages(pm);
                    var pip = FindPip(hand.Map); // cc-P721: a patient who stays hurt
                    hand.SayTo(pm, gift switch
                    {
                        BandageGift.NoneLeft => NoMoreBandagesLine,
                        BandageGift.NoRoom => NoRoomForBandagesLine,
                        _ when pip != null => PipLine,
                        _ => Scratch(pm) ? ScratchLine : HealLine
                    });
                    if (gift is BandageGift.Given or BandageGift.HasSome)
                    {
                        hand.SayTo(pm, WaitLine); // cc-P721
                        hand.SayTo(pm, MakeBandagesLine); // cc-P718 item 9
                        pip?.PointTo(pm);
                    }

                    break;"""),
# -- the commands chain grows
("""        public static bool CommandsDone(PlayerMobile pm) => Has(pm, FollowKey) && Has(pm, GuardKey);""",
 """        /// <summary>cc-P721: the pet commands, then the weapon in hand and war mode: what the pest part waits for.</summary>
        public static bool CommandsDone(PlayerMobile pm) =>
            Has(pm, FollowKey) && Has(pm, GuardKey) && Has(pm, WeaponKey) && Has(pm, WarKey);"""),
("""            var pets = PetsOf(pm);
            if (pets.Count == 0)
            {
                var record = RecordOf(pm)!;
                record.StationsDone.Add(FollowKey);
                record.StationsDone.Add(GuardKey);
                OpenFieldGate(pm.Map);
                return false;
            }

            if (!Has(pm, FollowKey))""", """            var pets = PetsOf(pm);
            var noPet = pets.Count == 0;
            if (noPet)
            {
                var record = RecordOf(pm)!;
                record.StationsDone.Add(FollowKey);
                record.StationsDone.Add(GuardKey);
                GivePitchfork(pm); // cc-P721: the weapon and war mode still come first
            }
            else if (!Has(pm, FollowKey))"""),
("""            _watching.Add(pm);
            if (!_watchTimer.Running)
            {
                Timer.StartTimer(TimeSpan.FromMilliseconds(500), TimeSpan.FromMilliseconds(500), WatchAll, out _watchTimer);
            }

            return true;
        }""", """            _watching.Add(pm);
            if (!_watchTimer.Running)
            {
                Timer.StartTimer(TimeSpan.FromMilliseconds(500), TimeSpan.FromMilliseconds(500), WatchAll, out _watchTimer);
            }

            return !noPet;
        }"""),
("""            else if (Has(pm, FollowKey) && pets.Exists(p => p.ControlOrder == OrderType.Guard))
            {
                record.StationsDone.Add(GuardKey);
                _watching.Remove(pm);
                OpenFieldGate(pm.Map);
                ClusterFTutorial.SystemLine(pm, string.Format(GuardDoneLine, PestsToClear));
                return true;
            }

            return false;""", """            else if (Has(pm, FollowKey) && !Has(pm, GuardKey) && pets.Exists(p => p.ControlOrder == OrderType.Guard))
            {
                record.StationsDone.Add(GuardKey);
                GivePitchfork(pm); // cc-P721
                ClusterFTutorial.SystemLine(pm, GuardDoneLine);
            }
            else if (Has(pm, GuardKey) && !Has(pm, WeaponKey) && HoldsPitchfork(pm))
            {
                record.StationsDone.Add(WeaponKey);
                ClusterFTutorial.SystemLine(pm, WeaponDoneLine);
            }
            else if (Has(pm, WeaponKey) && !Has(pm, WarKey) && pm.Warmode)
            {
                record.StationsDone.Add(WarKey);
                _watching.Remove(pm);
                OpenFieldGate(pm.Map);
                ClusterFTutorial.SystemLine(pm, string.Format(WarDoneLine, PestsToClear));
                return true;
            }

            return false;"""),
# -- the pitchfork, Pip and the bandage hooks, before the gate section
("""        // -- cc-P718 item 7: the field gate --""", """        // -- cc-P721: the pitchfork --

        /// <summary>The trainee's own pitchfork in hand (either hand layer).</summary>
        public static bool HoldsPitchfork(PlayerMobile pm) =>
            pm.FindItemOnLayer(Layer.TwoHanded) is TutorialPitchfork || pm.FindItemOnLayer(Layer.OneHanded) is TutorialPitchfork;

        /// <summary>Once per character: a pitchfork in the backpack, unless they have theirs. Null when none was given.</summary>
        public static TutorialPitchfork? GivePitchfork(PlayerMobile pm)
        {
            if (HoldsPitchfork(pm) || pm.Backpack?.FindItemByType<TutorialPitchfork>() != null)
            {
                return null;
            }

            var fork = new TutorialPitchfork(pm);
            if (!pm.PlaceInBackpack(fork))
            {
                fork.Delete();
                ClusterFTutorial.SystemLine(pm, "Your backpack is too full for the pitchfork. Make room, then double-click Wren again.");
                return null;
            }

            return fork;
        }

        // Trainees who have struck a pest themselves this run (in memory, like the count).
        private static readonly HashSet<Serial> _struck = new();

        public static void NoteStruck(PlayerMobile pm) => _struck.Add(pm.Serial);

        public static bool HasStruck(PlayerMobile pm) => _struck.Contains(pm.Serial);

        // -- cc-P721: the heal step's patient and the bandage on the isle --

        /// <summary>Pip, the hurt farm boy beside Wren, on <paramref name="map"/>, or null.</summary>
        public static TutorialWoundedHelper? FindPip(Map? map)
        {
            if (map == null)
            {
                return null;
            }

            foreach (var m in map.GetMobilesInRange(TutorialWorld.Ground(map, PipSpot), 3))
            {
                if (m is TutorialWoundedHelper pip && !pip.Deleted)
                {
                    return pip;
                }
            }

            return null;
        }

        /// <summary>Pip's place: by the barrel south of the gate, out of the way of the gate and Wren.</summary>
        public static readonly Point2D PipSpot = new(6715, 3981);

        /// <summary>A trainee on the Wakening Isle (or a copy of it).</summary>
        public static bool IsleTrainee(Mobile m) => m is PlayerMobile pm && ClusterFTutorial.IsParticipant(pm) && TutorialWorld.IsOnIsle(pm);

        /// <summary>Asked by Bandage-tutorial-wait-lines.patch for the delay (healer, patient, pinned's seconds).</summary>
        public static Func<Mobile, Mobile, double, double>? BandageSeconds { get; set; }

        /// <summary>Raised by the patch as a bandage begins (healer, patient, seconds).</summary>
        public static Action<Mobile, Mobile, double>? BandageBegun { get; set; }

        /// <summary>Raised by the patch when the healing roll fails (healer, patient).</summary>
        public static Action<Mobile, Mobile>? BandageFumbled { get; set; }

        public static double IsleSeconds(Mobile healer, Mobile patient, double seconds) =>
            healer == patient && IsleTrainee(healer) ? Math.Min(seconds, IsleSelfBandageSeconds) : seconds;

        public static void OnBandageBegun(Mobile healer, Mobile patient, double seconds)
        {
            if (healer is not PlayerMobile pm || !IsleTrainee(pm))
            {
                return;
            }

            pm.PrivateOverheadMessage(MessageType.Emote, 0x3B2, false, "*bandaging*", pm.NetState);
            ClusterFTutorial.SystemLine(pm, $"This bandage takes about {Math.Ceiling(seconds)} seconds. Stand still until you see 'You finish applying the bandages'.");
        }

        public static void OnBandageFumbled(Mobile healer, Mobile patient)
        {
            if (healer is PlayerMobile pm && IsleTrainee(pm))
            {
                ClusterFTutorial.SystemLine(pm, FumbleLine);
            }
        }

        // -- cc-P718 item 7: the field gate --"""),
# -- hooks
("""            Unhurt = OnUnhurt; // cc-P707 run 4""", """            Unhurt = OnUnhurt; // cc-P707 run 4
            BandageSeconds = IsleSeconds; // cc-P721
            BandageBegun = OnBandageBegun;
            BandageFumbled = OnBandageFumbled;"""),
# -- unhurt: send to Pip; healed Pip is cut again
("""            if (healer is not PlayerMobile pm || StepOf(pm) != 3 ||
                patient != pm && (patient as BaseCreature)?.ControlMaster != pm || !Scratch(pm))
            {
                return false;
            }

            pm.SendMessage(ScratchAgainLine);
            return true;""", """            if (healer is not PlayerMobile pm || StepOf(pm) != 3 ||
                patient != pm && (patient as BaseCreature)?.ControlMaster != pm)
            {
                return false;
            }

            // cc-P721: with Pip there, the trainee is sent to him; a scratch of their own would heal by itself.
            if (FindPip(pm.Map) is { } pip)
            {
                pm.SendMessage(PipNotYouLine);
                pip.PointTo(pm);
                return true;
            }

            if (!Scratch(pm))
            {
                return false;
            }

            pm.SendMessage(ScratchAgainLine);
            return true;"""),
("""        private static void OnBandageHealed(Mobile healer, Mobile patient)
        {
            if (healer is PlayerMobile pm)
            {
                OnHealed(pm);
            }
        }""", """        private static void OnBandageHealed(Mobile healer, Mobile patient)
        {
            if (healer is PlayerMobile pm)
            {
                OnHealed(pm);
            }

            (patient as TutorialWoundedHelper)?.WoundAgainSoon(); // cc-P721
        }"""),
# -- pest count wants a strike by the trainee
("""            // cc-P718 item 10: at least one pest falls to the pet on "all kill", when the trainee has a pet with them.
            if (!_petKilled.Contains(pm.Serial) && PetsOf(pm).Count > 0)
            {
                ClusterFTutorial.SystemLine(pm, PetKillLine);
                return;
            }

            _pestsKilled.Remove(pm.Serial);
            _petKilled.Remove(pm.Serial);""", """            // cc-P718 item 10: at least one pest falls to the pet on "all kill", when the trainee has a pet with them.
            if (!_petKilled.Contains(pm.Serial) && PetsOf(pm).Count > 0)
            {
                ClusterFTutorial.SystemLine(pm, PetKillLine);
                return;
            }

            // cc-P721: and the trainee has attacked one themselves.
            if (!_struck.Contains(pm.Serial))
            {
                ClusterFTutorial.SystemLine(pm, StrikeLine);
                return;
            }

            _pestsKilled.Remove(pm.Serial);
            _petKilled.Remove(pm.Serial);
            _struck.Remove(pm.Serial);"""),
# -- staff/test CountPest credits the strike too
("""        public static void CountPest(PlayerMobile pm) => CountPest(pm, true);""",
 """        public static void CountPest(PlayerMobile pm)
        {
            NoteStruck(pm); // staff and tests credit the trainee's own strike too (cc-P721)
            CountPest(pm, true);
        }"""),
# -- seeding Pip
("""            if (TutorialFarmhand.Find(map) != null) { present++; }""", """            // cc-P721: Pip, the heal step's patient, when his spot is clear (he is optional: Wren falls back to a scratch).
            if (FindPip(map) != null) { present++; }
            else if (!dryRun && TutorialCorePlacement.FitsOn(TutorialWorld.Ground(map, PipSpot), map))
            {
                var spot = TutorialWorld.Ground(map, PipSpot);
                new TutorialWoundedHelper { Direction = Direction.West, Home = spot, RangeHome = 0 }.MoveToWorld(spot, map);
                hands++;
            }

            if (TutorialFarmhand.Find(map) != null) { present++; }"""),
# -- the pest notes the trainee's own blow
("""            if (from != null && !Fights(from))
            {
                return;
            }

            base.Damage(amount, from, informMount, ignoreEvilOmen);
        }""", """            if (from != null && !Fights(from))
            {
                return;
            }

            if (from is PlayerMobile striker)
            {
                TutorialFarm.NoteStruck(striker); // cc-P721: the trainee's own blow
            }

            base.Damage(amount, from, informMount, ignoreEvilOmen);
        }"""),
# -- the classes, after the gate class
("""            base.Use(from);
        }
    }
}""", """            base.Use(from);
        }
    }

    /// <summary>
    /// cc-P721: the farm's pitchfork, handed out by Wren for the first fight. Kept like the isle's cloak: blessed, and
    /// Nontransferable (no sale, trade, bank or drop: pinned Item and GenericSellInfo).
    /// </summary>
    [SerializationGenerator(0, false)]
    public partial class TutorialPitchfork : Pitchfork
    {
        [SerializableField(0)]
        [SerializedCommandProperty(AccessLevel.GameMaster)]
        private Mobile? _owner;

        [Constructible]
        public TutorialPitchfork() : this(null) { }

        public TutorialPitchfork(Mobile? owner)
        {
            _owner = owner;
            Name = "farmhand's pitchfork";
            LootType = LootType.Blessed;
        }

        public override bool Nontransferable => true;

        public override void HandleInvalidTransfer(Mobile from) =>
            from.SendMessage(0x3B2, "Your farmhand's pitchfork is yours alone. Keep it in your backpack or hold it.");
    }

    /// <summary>
    /// cc-P721: Pip, the farm boy beside Wren, cut on the fence: the heal step's patient. His hits never come back by
    /// themselves (CanRegenHits), so he is still hurt when the bandage lands, and he is cut again a little after each
    /// heal for the next trainee. Nothing can harm him.
    /// </summary>
    [SerializationGenerator(0, false)]
    public partial class TutorialWoundedHelper : BaseCreature
    {
        public static readonly TimeSpan WoundAgainAfter = TimeSpan.FromSeconds(20);
        private TimerExecutionToken _wound;

        [Constructible]
        public TutorialWoundedHelper() : base(AIType.AI_Animal, FightMode.None, 10, 1)
        {
            Name = "Pip";
            Title = "the farm boy, cut on the fence";
            Body = 0x190;
            Hue = 0x83EA;
            SetStr(60);
            SetDex(40);
            SetInt(40);
            SetHits(60);
            CantWalk = true;
            AddItem(new Shirt { Movable = false, Hue = 0x2C });
            AddItem(new ShortPants { Movable = false, Hue = 0x455 });
            AddItem(new Sandals { Movable = false });
            AddItem(new Item(0x203B) { Movable = false, Hue = 0x2C, Layer = Layer.Hair });
            Wound();
        }

        public override bool IsInvulnerable => true;
        public override bool ClickTitle => true;
        public override bool CanRegenHits => false;

        /// <summary>Down to a third of his hits.</summary>
        public void Wound() => Hits = Math.Max(1, HitsMax / 3);

        public void WoundAgainSoon()
        {
            _wound.Cancel();
            Timer.StartTimer(WoundAgainAfter, Wound, out _wound);
        }

        public override void OnAfterDelete()
        {
            base.OnAfterDelete();
            _wound.Cancel();
        }

        [AfterDeserialization(false)]
        private void AfterLoad() => Wound();

        /// <summary>An arrow from the trainee to Pip.</summary>
        public void PointTo(PlayerMobile pm)
        {
            if (pm.Map == Map)
            {
                pm.QuestArrow?.Stop();
                pm.QuestArrow = new GuildDirectionArrow(pm, this, Location, Map, "Pip, the hurt farm boy");
            }
        }
    }
}"""),
]
for o, n in pairs:
    rep(o, n)
open(p, "w", encoding="utf-8", newline="").write(s)
print("ok")
