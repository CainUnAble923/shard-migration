"""cc-P134 Part C smoke test: speak MCP (JSON-RPC over stdio) to the built vseUOAware server, exactly as Claude Code
does when it starts a stdio server from .mcp.json, using that file's command and env.

    python mcp_smoke.py list                     tools/list (names and parameters)
    python mcp_smoke.py call <tool> '<json args>' tools/call
"""
import json, os, subprocess, sys

MCP_JSON = r'D:\UO\shard-migration\.mcp.json'


def start():
    cfg = json.load(open(MCP_JSON, encoding='utf-8'))['mcpServers']['vseUOAware']
    env = dict(os.environ, **cfg.get('env', {}))
    p = subprocess.Popen([cfg['command']] + cfg.get('args', []), stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, env=env, text=True, encoding='utf-8')
    return p


def rpc(p, i, method, params=None):
    msg = {'jsonrpc': '2.0', 'id': i, 'method': method}
    if params is not None:
        msg['params'] = params
    p.stdin.write(json.dumps(msg) + '\n')
    p.stdin.flush()
    while True:
        line = p.stdout.readline()
        if not line:
            raise SystemExit('server closed stdout; stderr:\n' + p.stderr.read())
        r = json.loads(line)
        if r.get('id') == i:
            return r


def main():
    p = start()
    try:
        r = rpc(p, 1, 'initialize', {'protocolVersion': '2025-06-18', 'capabilities': {},
                                     'clientInfo': {'name': 'cc-p134-smoke', 'version': '1'}})
        print('initialize:', json.dumps(r.get('result', r).get('serverInfo', r)))
        p.stdin.write(json.dumps({'jsonrpc': '2.0', 'method': 'notifications/initialized'}) + '\n')
        p.stdin.flush()
        if sys.argv[1] == 'list':
            tools = rpc(p, 2, 'tools/list')['result']['tools']
            print('%d tools' % len(tools))
            for t in tools:
                props = t.get('inputSchema', {}).get('properties', {})
                print('%s(%s)' % (t['name'], ', '.join(props)))
        else:
            r = rpc(p, 2, 'tools/call', {'name': sys.argv[2], 'arguments': json.loads(sys.argv[3])})
            res = r.get('result', r)
            print('isError:', res.get('isError'))
            for c in res.get('content', []):
                print(c.get('text', c))
    finally:
        p.stdin.close()
        p.wait(timeout=20)


if __name__ == '__main__':
    main()
