// Shattered Legacy patch (cc-P240, F-6): fog of war on the world map.
//
// The shard tracks which 8x8-tile chunks each character has walked through and sends them in its own variable-length
// packet 0xF4 (server\customizations\ClusterFExplorationManager.cs, ClusterFExplorationPackets):
//   [0xF4][u16 length][u8 sub][u8 facet][u32 BE payload length][payload]
//   sub 0x01 full explored: gzip of the facet's bit set (bit i = chunk cy * width + cx, least significant bit first,
//            .NET BitArray.CopyTo); 0x02 delta: u16 BE cx, u16 BE cy per newly walked chunk;
//   0x03 and 0x04 (mining depletion) are not drawn here.
// The world map draws a dark layer over every chunk not walked, on a facet the server has sent. A server that sends
// no 0xF4 (any other shard) gets no fog. Each new login starts empty (EnterWorld), and the shard resends on login.
// Profile.WorldMapShowFog (the world map's right-click menu, "Fog of war") turns the layer off.

using System;
using System.IO;
using System.IO.Compression;
using ClassicUO.IO;
using Microsoft.Xna.Framework.Graphics;

namespace ClassicUO.Game.Managers
{
    public static class ShardFogOfWar
    {
        public const byte PacketId = 0xF4;
        public const int ChunkSize = 8;
        public const byte FullExplored = 0x01;
        public const byte DeltaExplored = 0x02;

        // A fogged chunk: black at 216 of 255 (premultiplied), so the land still shows faintly through it.
        public const byte FogAlpha = 216;
        public const uint FogPixel = (uint)FogAlpha << 24;

        // The server's own table (ClusterFExplorationManager.MapSizes). Its chunk index is cy * width + cx with these
        // widths, so the client must use the same ones, whatever size the client's map files are.
        public static readonly (int W, int H)[] MapSizes =
        {
            (6144, 4096), // 0 Felucca
            (6144, 4096), // 1 Trammel
            (2304, 1600), // 2 Ilshenar
            (2560, 2048), // 3 Malas
            (1448, 1448), // 4 Tokuno
            (1280, 4096)  // 5 TerMur
        };

        private static readonly byte[][] _explored = new byte[MapSizes.Length][];

        /// <summary>Goes up on every change, so a drawn layer knows to rebuild.</summary>
        public static int Version { get; private set; }

        public static int ChunkWidth(int facet) => (MapSizes[facet].W + ChunkSize - 1) / ChunkSize;
        public static int ChunkHeight(int facet) => (MapSizes[facet].H + ChunkSize - 1) / ChunkSize;
        private static int ByteCount(int facet) => (ChunkWidth(facet) * ChunkHeight(facet) + 7) / 8;

        public static bool HasData(int facet) => facet >= 0 && facet < MapSizes.Length && _explored[facet] != null;

        public static bool IsExplored(int facet, int cx, int cy)
        {
            if (!HasData(facet) || cx < 0 || cy < 0 || cx >= ChunkWidth(facet) || cy >= ChunkHeight(facet))
                return false;

            int i = cy * ChunkWidth(facet) + cx;
            return (_explored[facet][i >> 3] & (1 << (i & 7))) != 0;
        }

        public static void Reset()
        {
            Array.Clear(_explored);
            Version++;
        }

        /// <summary>The 0xF4 handler: the reader stands after the id and the length.</summary>
        public static void Receive(World world, ref StackDataReader p)
        {
            if (p.Remaining < 6)
                return;

            byte sub = p.ReadUInt8();
            byte facet = p.ReadUInt8();
            int length = (int)p.ReadUInt32BE();
            if (length < 0 || length > p.Remaining)
                return;

            Apply(sub, facet, p.Buffer.Slice(p.Position, length));
        }

        /// <summary>One 0xF4 message. False when it is not one this layer draws, or is malformed.</summary>
        public static bool Apply(byte sub, byte facet, ReadOnlySpan<byte> payload)
        {
            if (facet >= MapSizes.Length)
                return false;

            switch (sub)
            {
                case FullExplored:
                    {
                        byte[] bits = new byte[ByteCount(facet)];
                        try
                        {
                            using var gz = new GZipStream(new MemoryStream(payload.ToArray()), CompressionMode.Decompress);
                            int read = 0, n;
                            while (read < bits.Length && (n = gz.Read(bits, read, bits.Length - read)) > 0)
                                read += n;
                        }
                        catch (InvalidDataException)
                        {
                            return false;
                        }

                        _explored[facet] = bits;
                        Version++;
                        return true;
                    }

                case DeltaExplored:
                    {
                        if (payload.Length % 4 != 0)
                            return false;

                        _explored[facet] ??= new byte[ByteCount(facet)];
                        int w = ChunkWidth(facet), h = ChunkHeight(facet);
                        for (int o = 0; o < payload.Length; o += 4)
                        {
                            int cx = (payload[o] << 8) | payload[o + 1];
                            int cy = (payload[o + 2] << 8) | payload[o + 3];
                            if (cx >= w || cy >= h)
                                continue;

                            int i = cy * w + cx;
                            _explored[facet][i >> 3] |= (byte)(1 << (i & 7));
                        }

                        Version++;
                        return true;
                    }

                default:
                    return false; // 0x03 and 0x04, mining depletion: not this layer's
            }
        }

        /// <summary>
        /// The fog layer's pixels, one per chunk, packed as the Color texture wants them (0 is clear, FogPixel is fog),
        /// with one more column and row of fog so the map beyond the server's edge stays dark. Null with no data.
        /// </summary>
        public static uint[] FogPixels(int facet, out int width, out int height)
        {
            width = height = 0;
            if (!HasData(facet))
                return null;

            int w = ChunkWidth(facet), h = ChunkHeight(facet);
            width = w + 1;
            height = h + 1;
            var pixels = new uint[width * height];
            Array.Fill(pixels, FogPixel);
            byte[] bits = _explored[facet];
            for (int cy = 0; cy < h; cy++)
            {
                for (int cx = 0; cx < w; cx++)
                {
                    int i = cy * w + cx;
                    if ((bits[i >> 3] & (1 << (i & 7))) != 0)
                        pixels[cy * width + cx] = 0;
                }
            }

            return pixels;
        }

        // ---- the drawn layer --------------------------------------------------------------------------------------

        private static Texture2D _texture;
        private static int _textureFacet = -1, _textureVersion = -1;

        /// <summary>The layer for a facet, rebuilt when the data changed; null with no data.</summary>
        public static Texture2D Texture(GraphicsDevice device, int facet)
        {
            if (!HasData(facet))
                return null;

            if (_texture == null || _texture.IsDisposed || _textureFacet != facet || _textureVersion != Version)
            {
                uint[] pixels = FogPixels(facet, out int w, out int h);
                if (_texture == null || _texture.IsDisposed || _texture.Width != w || _texture.Height != h)
                {
                    _texture?.Dispose();
                    _texture = new Texture2D(device, w, h, false, SurfaceFormat.Color);
                }

                _texture.SetData(pixels);
                _textureFacet = facet;
                _textureVersion = Version;
            }

            return _texture;
        }
    }
}
