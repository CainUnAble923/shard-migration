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

        // Raw pointers both ways: a delegate made from a function pointer in the same process comes back as the
        // client's own delegate type and cannot be cast (the first try), so the hook is UnmanagedCallersOnly and the
        // client's Send_new (OnPluginSend_new(IntPtr, ref int)) is called through its pointer.
        private static delegate* unmanaged[Cdecl]<IntPtr, int*, byte> _sendNew;
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
            _sendNew = (delegate* unmanaged[Cdecl]<IntPtr, int*, byte>)h->Send_new;
            h->OnRecv_new = (IntPtr)(delegate* unmanaged[Cdecl]<IntPtr, int*, byte>)&OnRecvNew;
            Log("installed, client version " + h->ClientVersion);
        }

        [UnmanagedCallersOnly(CallConvs = new[] { typeof(CallConvCdecl) })]
        private static byte OnRecvNew(IntPtr data, int* length)
        {
            if (*length > 0 && *(byte*)data == 0xA9 && Interlocked.Exchange(ref _sent, 1) == 0)
            {
                Log("character list (0xA9, " + *length + " bytes): creating in 3 s");
                new Thread(() =>
                {
                    Thread.Sleep(3000);
                    var b = File.ReadAllBytes(Path.Combine(_dir, "create.bin"));
                    int n = b.Length;
                    byte ok;
                    fixed (byte* p = b) { ok = _sendNew((IntPtr)p, &n); }
                    Log("sent 0xF8 create (" + n + " bytes): " + ok);
                }) { IsBackground = true }.Start();
            }
            return 1;
        }
    }
}
