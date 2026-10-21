// Shattered Legacy patch (cc-P240, F-6): the world map's fog of war, fed by the shard's packet 0xF4.
using System;
using System.Collections;
using System.IO;
using System.IO.Compression;
using System.Linq;
using ClassicUO.Game.Managers;
using ClassicUO.IO;
using FluentAssertions;
using Xunit;

namespace ClassicUO.UnitTests.Game
{
    public class ShardFogOfWarTests
    {
        // The server's way (ClusterFExplorationPackets.SendFullExplored): a BitArray of the facet's chunks, CopyTo bytes,
        // gzip.
        private static byte[] FullPayload(int facet, params (int cx, int cy)[] walked)
        {
            int w = ShardFogOfWar.ChunkWidth(facet), h = ShardFogOfWar.ChunkHeight(facet);
            var bits = new BitArray(w * h, false);
            foreach (var (cx, cy) in walked)
                bits[cy * w + cx] = true;

            byte[] raw = new byte[(bits.Length + 7) / 8];
            bits.CopyTo(raw, 0);
            using var output = new MemoryStream();
            using (var gz = new GZipStream(output, CompressionLevel.Optimal, leaveOpen: true))
                gz.Write(raw, 0, raw.Length);
            return output.ToArray();
        }

        // ClusterFExplorationPackets.Send: [0xF4][u16 BE length][sub][facet][u32 BE payload length][payload].
        private static byte[] Packet(byte sub, byte facet, byte[] payload)
        {
            int total = 9 + payload.Length;
            var b = new byte[total];
            b[0] = 0xF4;
            b[1] = (byte)(total >> 8);
            b[2] = (byte)total;
            b[3] = sub;
            b[4] = facet;
            b[5] = (byte)(payload.Length >> 24);
            b[6] = (byte)(payload.Length >> 16);
            b[7] = (byte)(payload.Length >> 8);
            b[8] = (byte)payload.Length;
            payload.CopyTo(b, 9);
            return b;
        }

        private static int[] Clear(uint[] pixels) =>
            pixels.Select((p, i) => (p, i)).Where(t => t.p != ShardFogOfWar.FogPixel).Select(t => t.i).ToArray();

        [Fact]
        public void The_chunk_table_is_the_servers()
        {
            ShardFogOfWar.ChunkWidth(0).Should().Be(768);
            ShardFogOfWar.ChunkHeight(0).Should().Be(512);
            ShardFogOfWar.ChunkWidth(2).Should().Be(288);
            ShardFogOfWar.ChunkHeight(2).Should().Be(200);
            ShardFogOfWar.ChunkWidth(4).Should().Be(181);
            ShardFogOfWar.ChunkHeight(5).Should().Be(512);
        }

        [Fact]
        public void A_known_chunk_bit_reveals_exactly_that_chunk()
        {
            ShardFogOfWar.Reset();
            ShardFogOfWar.Apply(ShardFogOfWar.FullExplored, 1, FullPayload(1, (400, 300))).Should().BeTrue();

            uint[] pixels = ShardFogOfWar.FogPixels(1, out int w, out int h);
            pixels.Should().NotBeNull();
            w.Should().Be(769, "one chunk per pixel, plus a column of fog past the server's edge");
            h.Should().Be(513);
            Clear(pixels).Should().Equal(new[] { 300 * w + 400 }, "only the walked chunk is clear");
            ShardFogOfWar.IsExplored(1, 400, 300).Should().BeTrue();
            ShardFogOfWar.IsExplored(1, 401, 300).Should().BeFalse();
            ShardFogOfWar.IsExplored(1, 400, 301).Should().BeFalse();
        }

        [Fact]
        public void A_dungeon_chunk_east_of_5120_is_kept_like_any_other()
        {
            ShardFogOfWar.Reset();
            int cx = 5300 / 8, cy = 300 / 8; // Felucca's dungeons sit east of x 5120 on the same map
            ShardFogOfWar.Apply(ShardFogOfWar.FullExplored, 0, FullPayload(0, (cx, cy))).Should().BeTrue();
            uint[] pixels = ShardFogOfWar.FogPixels(0, out int w, out _);
            Clear(pixels).Should().Equal(cy * w + cx);
        }

        [Fact]
        public void A_delta_reveals_the_listed_chunks_and_only_on_its_facet()
        {
            ShardFogOfWar.Reset();
            byte[] delta = { 0x00, 0x05, 0x00, 0x07, 0x01, 0x00, 0x00, 0x02 }; // (5, 7) and (256, 2)
            ShardFogOfWar.Apply(ShardFogOfWar.DeltaExplored, 3, delta).Should().BeTrue();

            uint[] pixels = ShardFogOfWar.FogPixels(3, out int w, out _);
            Clear(pixels).Should().BeEquivalentTo(new[] { 7 * w + 5, 2 * w + 256 });
            ShardFogOfWar.HasData(2).Should().BeFalse("Malas's delta is not Ilshenar's");
        }

        [Fact]
        public void The_servers_packet_parses_through_the_handler()
        {
            ShardFogOfWar.Reset();
            byte[] packet = Packet(ShardFogOfWar.FullExplored, 2, FullPayload(2, (10, 20), (11, 20)));
            var reader = new StackDataReader(packet);
            reader.Seek(3); // the parser hands the handler the bytes after the id and the length
            ShardFogOfWar.Receive(null, ref reader);

            ShardFogOfWar.IsExplored(2, 10, 20).Should().BeTrue();
            ShardFogOfWar.IsExplored(2, 11, 20).Should().BeTrue();
            ShardFogOfWar.IsExplored(2, 12, 20).Should().BeFalse();
        }

        [Fact]
        public void No_data_means_no_fog()
        {
            ShardFogOfWar.Reset();
            for (int facet = 0; facet < ShardFogOfWar.MapSizes.Length; facet++)
            {
                ShardFogOfWar.HasData(facet).Should().BeFalse();
                ShardFogOfWar.FogPixels(facet, out _, out _).Should().BeNull("a server that sends no 0xF4 gets no fog");
            }

            ShardFogOfWar.HasData(7).Should().BeFalse("a facet the server has no table for");
        }

        [Fact]
        public void Mining_depletion_and_bad_data_draw_nothing()
        {
            ShardFogOfWar.Reset();
            ShardFogOfWar.Apply(0x03, 1, FullPayload(1, (1, 1))).Should().BeFalse();
            ShardFogOfWar.Apply(0x04, 1, new byte[] { 0, 1, 0, 1, 1 }).Should().BeFalse();
            ShardFogOfWar.Apply(ShardFogOfWar.FullExplored, 1, new byte[] { 1, 2, 3 }).Should().BeFalse();
            ShardFogOfWar.Apply(ShardFogOfWar.DeltaExplored, 9, new byte[4]).Should().BeFalse();
            ShardFogOfWar.HasData(1).Should().BeFalse();
        }

        [Fact]
        public void A_new_login_starts_empty()
        {
            ShardFogOfWar.Apply(ShardFogOfWar.DeltaExplored, 4, new byte[] { 0, 1, 0, 1 }).Should().BeTrue();
            int before = ShardFogOfWar.Version;
            ShardFogOfWar.Reset();
            ShardFogOfWar.HasData(4).Should().BeFalse();
            ShardFogOfWar.Version.Should().NotBe(before, "a drawn layer rebuilds");
        }
    }
}
