// cc-P859 RED stub: Mister Gobbles with no name. Never shipped.
using ModernUO.Serialization;

namespace Server.Mobiles;

[SerializationGenerator(0, false)]
public partial class MisterGobbles : Turkey
{
    [Constructible]
    public MisterGobbles() : base(false) { }
}
