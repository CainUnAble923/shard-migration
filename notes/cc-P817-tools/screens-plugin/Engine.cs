// cc-P817 (test only, never shipped; P731's plugin shape): steps TazUO's character creation screens from inside the
// client, for the shots, because window messages posted to the client no longer reach it on this PC (the P762 way). On the
// client's own tick (its main thread): once the creation screen is up, it waits 10 s (the race row's shot), shows the
// profession page (CharCreationGump.SetStep(ChooseProfession)), and 10 s later the start map with Warrior chosen (the
// gump's _selectedProfession set, then SetStep(ChooseCity)), as clicking Next and Warrior would. It creates nothing.
// Log: P817Screens.log beside the dll.
using System;
using System.Collections;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.InteropServices;

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

        private const BindingFlags All = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static;
        private static string _dir;
        private static DateTime _seen;
        private static int _stage;

        private static void Log(string text)
        {
            try { File.AppendAllText(Path.Combine(_dir, "P817Screens.log"), DateTime.Now.ToString("HH:mm:ss.fff ") + text + Environment.NewLine); }
            catch { }
        }

        public static void Install(IntPtr header)
        {
            _dir = Path.GetDirectoryName(typeof(Engine).Assembly.Location) ?? ".";
            var h = (PluginHeader*)header;
            h->Tick = (IntPtr)(delegate* unmanaged[Cdecl]<void>)&OnTick;
            Log("installed, client version " + h->ClientVersion);
        }

        private static Type T(string fullName) =>
            AppDomain.CurrentDomain.GetAssemblies().Select(a => a.GetType(fullName, false)).FirstOrDefault(t => t != null);

        private static object Get(object o, string name)
        {
            var t = o.GetType();
            var p = t.GetProperty(name, All);
            return p != null ? p.GetValue(o) : t.GetField(name, All)!.GetValue(o);
        }

        [UnmanagedCallersOnly(CallConvs = new[] { typeof(CallConvCdecl) })]
        private static void OnTick()
        {
            try { Step(); }
            catch (Exception e) { Log("error: " + e); _stage = 99; }
        }

        private static void Step()
        {
            if (_stage >= 3) { return; }
            var gumps = (IEnumerable)T("ClassicUO.Game.Managers.UIManager")!.GetProperty("Gumps", All)!.GetValue(null)!;
            object gump = null;
            foreach (var g in gumps) { if (g.GetType().Name == "CharCreationGump") { gump = g; break; } }
            if (gump == null) { return; }
            if (_stage == 0) { _seen = DateTime.Now; _stage = 1; Log("creation screen seen"); return; }

            var gt = gump.GetType();
            var stepType = gt.GetNestedType("CharCreationStep", All)!;
            var setStep = gt.GetMethod("SetStep", All)!;
            var since = DateTime.Now - _seen;
            if (_stage == 1 && since > TimeSpan.FromSeconds(10))
            {
                setStep.Invoke(gump, new[] { Enum.ToObject(stepType, 1) });
                _stage = 2;
                Log("profession page shown");
            }
            else if (_stage == 2 && since > TimeSpan.FromSeconds(20))
            {
                var game = T("ClassicUO.Client")!.GetProperty("Game", All)!.GetValue(null)!;
                var dict = (IDictionary)Get(Get(Get(Get(game, "UO"), "FileManager"), "Professions"), "Professions");
                object warrior = null;
                var names = new System.Collections.Generic.List<string>();
                foreach (var k in dict.Keys)
                {
                    var n = (string)Get(k, "Name");
                    names.Add(n);
                    if (string.Equals(n, "Warrior", StringComparison.OrdinalIgnoreCase)) { warrior = k; } // the client keeps names upper case
                }

                Log("professions the client lists: " + string.Join(", ", names));
                gt.GetField("_selectedProfession", All)!.SetValue(gump, warrior);
                setStep.Invoke(gump, new[] { Enum.ToObject(stepType, 3) });
                _stage = 3;
                Log("start map shown (Warrior chosen)");
            }
        }
    }
}
