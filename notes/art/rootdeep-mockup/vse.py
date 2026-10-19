"""cc-P141: a batch client for the local vseUOAware MCP server (P134's fixed copy, started from .mcp.json exactly
as Claude Code starts it). Same JSON-RPC over stdio as notes/cc-P134-tools/mcp_smoke.py, kept open for many calls.

    from vse import Vse
    with Vse() as v:
        text = v.call('find_item_id_by_name', {'tileDataFilePath': v.uo('tiledata.mul'), 'searchText': 'cave'})
"""
import json, os, subprocess

MCP_JSON = r'D:\UO\shard-migration\.mcp.json'


class Vse:
    def __init__(self, exe=None):
        self.exe = exe   # cc-P180: another build of the server (bin\P180 holds the render offset fix) instead of .mcp.json's

    def __enter__(self):
        cfg = json.load(open(MCP_JSON, encoding='utf-8'))['mcpServers']['vseUOAware']
        self.uo_dir = cfg['env']['VSEUOAWARE_UO_DIR']
        env = dict(os.environ, **cfg.get('env', {}))
        self.p = subprocess.Popen([self.exe or cfg['command']] + cfg.get('args', []), stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, env=env, text=True,
                                  encoding='utf-8')
        self.i = 0
        self._rpc('initialize', {'protocolVersion': '2025-06-18', 'capabilities': {},
                                 'clientInfo': {'name': 'cc-p141-mockup', 'version': '1'}})
        self._send({'jsonrpc': '2.0', 'method': 'notifications/initialized'})
        return self

    def __exit__(self, *a):
        self.p.stdin.close()
        self.p.wait(timeout=20)

    def uo(self, name):
        return os.path.join(self.uo_dir, name)

    def _send(self, msg):
        self.p.stdin.write(json.dumps(msg) + '\n')
        self.p.stdin.flush()

    def _rpc(self, method, params=None):
        self.i += 1
        msg = {'jsonrpc': '2.0', 'id': self.i, 'method': method}
        if params is not None:
            msg['params'] = params
        self._send(msg)
        while True:
            line = self.p.stdout.readline()
            if not line:
                raise SystemExit('vseUOAware closed stdout')
            r = json.loads(line)
            if r.get('id') == self.i:
                return r

    def call(self, tool, args):
        r = self._rpc('tools/call', {'name': tool, 'arguments': args})
        res = r.get('result', r)
        text = '\n'.join(c.get('text', '') for c in res.get('content', []))
        if res.get('isError'):
            raise RuntimeError('%s failed: %s' % (tool, text))
        return text
