// cc-P740: P731's plugin for ClassicUO's .NET Framework host (delegates in place of UnmanagedCallersOnly).
// cc-P731 (test only, never shipped): a TazUO plugin that makes a brand-new character from the character list, so the
// character's first login is TazUO's own. When the server's character list (0xA9) arrives, it waits 3 s and sends the
// 0xF8 create-character packet in create.bin (beside this dll; made by notes/cc-P731-tools/make_create_bin.py) once,
// through the client's own plugin Send. The server then answers as for the creation screen, and TazUO enters the world.
// Log: P731Create.log beside the dll.
using System;
using System.IO;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;
using System.Threading;

namespace Assistant
{
    public static unsafe class Engine
    {
        [StructLayout(LayoutKind.Sequential)]
        private struct PluginHeader
        {
            public int ClientVersion;
            public IntPtr HWND;
            public IntPtr OnRecv;
            public IntPtr OnSend;
            public IntPtr OnHotkeyPressed;
            public IntPtr OnMouse;
            public IntPtr OnPlayerPositionChanged;
            public IntPtr OnClientClosing;
            public IntPtr OnInitialize;
            public IntPtr OnConnected;
            public IntPtr OnDisconnected;
            public IntPtr OnFocusGained;
            public IntPtr OnFocusLost;
            public IntPtr GetUOFilePath;
            public IntPtr Recv;
            public IntPtr Send;
            public IntPtr GetPacketLength;
            public IntPtr GetPlayerPosition;
            public IntPtr CastSpell;
            public IntPtr GetStaticImage;
            public IntPtr Tick;
            public IntPtr RequestMove;
            public IntPtr SetTitle;
            public IntPtr OnRecv_new, OnSend_new, Recv_new, Send_new;
            public IntPtr OnDrawCmdList;
            public IntPtr SDL_Window;
            public IntPtr OnWndProc;
            public IntPtr GetStaticData;
            public IntPtr GetTileData;
            public IntPtr GetCliloc;
        }

        // cc-P740: ClassicUO's .NET Framework host turns each pointer back into a delegate of its own type, so the hooks use
        // cuoapi.dll's OnPacketSendRecv (the old OnRecv and Send fields, byte[] by ref), not OnRecv_new.
        private static CUO_API.OnPacketSendRecv _send;
        private static CUO_API.OnPacketSendRecv _onRecv; // kept: the host holds only its pointer
        private static string _dir;
        private static int _sent;

        private static void Log(string text)
        {
            try { File.AppendAllText(Path.Combine(_dir, "P731Create.log"), DateTime.Now.ToString("HH:mm:ss.fff ") + text + Environment.NewLine); }
            catch { }
        }

        public static void Install(IntPtr header)
        {
            _dir = Path.GetDirectoryName(typeof(Engine).Assembly.Location) ?? ".";
            var h = (PluginHeader*)header;
            _send = (CUO_API.OnPacketSendRecv)Marshal.GetDelegateForFunctionPointer(h->Send, typeof(CUO_API.OnPacketSendRecv));
            _onRecv = OnRecv;
            h->OnRecv = Marshal.GetFunctionPointerForDelegate(_onRecv);
            Log("installed, client version " + h->ClientVersion);
        }

        private static int _picked;

        private static bool OnRecv(ref byte[] data, ref int length)
        {
            // cc-P740: ClassicUO stops at the shard list (no -skipserverselect); pick its first entry, as a click would.
            if (length > 8 && data[0] == 0xA8 && Interlocked.Exchange(ref _picked, 1) == 0)
            {
                var pick = new byte[] { 0xA0, data[6], data[7] };
                Log("shard list (0xA8): picking entry " + ((data[6] << 8) | data[7]));
                new Thread(() =>
                {
                    Thread.Sleep(1000);
                    int n = pick.Length;
                    var ok = _send(ref pick, ref n);
                    Log("sent 0xA0: " + ok);
                }) { IsBackground = true }.Start();
            }

            if (length > 0 && data[0] == 0xA9 && Interlocked.Exchange(ref _sent, 1) == 0)
            {
                Log("character list (0xA9, " + length + " bytes): creating in 3 s");
                new Thread(() =>
                {
                    Thread.Sleep(3000);
                    var b = File.ReadAllBytes(Path.Combine(_dir, "create.bin"));
                    int n = b.Length;
                    var ok = _send(ref b, ref n);
                    Log("sent 0xF8 create (" + n + " bytes): " + ok);
                }) { IsBackground = true }.Start();
            }

            return true;
        }
    }
}
