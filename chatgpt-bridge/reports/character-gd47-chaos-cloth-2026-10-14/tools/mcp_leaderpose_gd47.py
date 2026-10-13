"""GD47: runtime leader pose for the Chaos Cloth components in BP_Player_MM's UserConstructionScript through the editor MCP Blueprint
toolset (pattern: GD45 tools/mcp_leaderpose.py). Existing chain (GD45): entry -> Parent: ConstructionScript -> Henley.SetLeaderPose(Manny)
-> Shorts.SetLeaderPose(Manny). Appended at the chain end: -> HenleyCloth.SetLeaderPoseComponent(Manny) -> ShortsCloth.SetLeaderPoseComponent(Manny).
usage: python mcp_leaderpose_gd47.py inspect|apply   (session id in data/mcp_sid.txt)"""
import sys, json, urllib.request, pathlib
R = pathlib.Path(__file__).resolve().parents[1]; SID = (R/'data'/'mcp_sid.txt').read_text().strip(); URL = 'http://127.0.0.1:8000/mcp'
TS = 'editor_toolset.toolsets.blueprint.BlueprintTools'; BP = '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_Player_MM.BP_Player_MM'; UCS = BP + ':UserConstructionScript'
_id = [100]
def rpc(method, params):
    _id[0] += 1; body = json.dumps({'jsonrpc': '2.0', 'id': _id[0], 'method': method, 'params': params}).encode('utf-8')
    req = urllib.request.Request(URL, data=body, headers={'Content-Type': 'application/json', 'Accept': 'application/json, text/event-stream', 'Mcp-Session-Id': SID})
    with urllib.request.urlopen(req, timeout=180) as r: return json.loads(r.read().decode('utf-8', 'replace'))
def tool(name, args):
    d = rpc('tools/call', {'name': 'call_tool', 'arguments': {'toolset_name': TS, 'tool_name': name, 'arguments': args}})
    c = d.get('result', {}).get('content', []); txt = '\n'.join(x.get('text', '') for x in c if x.get('type') == 'text')
    if d.get('result', {}).get('isError') or 'error' in d: raise RuntimeError(name + ': ' + (txt or json.dumps(d))[:600])
    try: return json.loads(txt).get('returnValue', txt)
    except Exception: return txt
def g(ref): return {'refPath': ref}
mode = sys.argv[1] if len(sys.argv) > 1 else 'inspect'; rep = {}
types = {}
for key, flt in (('set', 'SetLeaderPoseComponent'), ('hcloth', 'HenleyClothAl'), ('scloth', 'ShortsClothAl'), ('manny', 'MannyAl')):
    types[key] = tool('find_node_types', {'graph': g(UCS), 'type_id_filter': flt, 'context_pins': []}); print(key, types[key])
pick = {'set': next(t for t in types['set'] if t.endswith('|SetLeaderPoseComponent') and 'SkinnedMesh' in t)}
for key, nm in (('hcloth', 'HenleyClothAl'), ('scloth', 'ShortsClothAl'), ('manny', 'MannyAl')):
    pick[key] = next(t for t in types[key] if t.endswith('|' + nm) and ('Varsay' in t or 'Default' in t))
print('PICK', pick)
entry = tool('find_nodes', {'graph': g(UCS), 'title': '', 'entry_points_only': True})
sub = tool('get_connected_subgraph', {'node': entry[0]})   # returns node infos already
def infos_of(nodes):
    out = []
    for n in nodes:
        if not n or not n.get('refPath'): continue
        try: out += tool('get_node_infos', {'nodes': [n]})
        except Exception as e: print('SKIP', n, str(e)[:120])
    return out
infos = [i for i in sub if isinstance(i, dict) and 'node' in i]
rep.update({'types': types, 'pick': pick, 'entry': entry, 'chain_nodes': [(i['node']['refPath'].rsplit('.', 1)[-1], i.get('type_id')) for i in infos]})
print('CHAIN', rep['chain_nodes'])
def outpin(inf, name): return next(p for p in inf['output_pins'] if p.get('name', '').lower() == name)
# chain end = the exec node with an unconnected 'then' (after the GD45 Shorts.SetLeaderPose)
ends = [i for i in infos if any(p.get('name') == 'then' for p in i['output_pins']) and not outpin(i, 'then')['connected_pins']]
print('ENDS', [(i['node']['refPath'].rsplit('.', 1)[-1], i.get('type_id')) for i in ends]); rep['ends'] = [i['node']['refPath'] for i in ends]
already = [i for i in infos if i.get('type_id') == pick['set'] and any(cp for p in i['input_pins'] if p['name'] == 'self' for cp in p['connected_pins'])]
if mode == 'apply':
    assert len(ends) == 1, 'expected one chain end'
    end = ends[0]
    def mk(type_id, x, y): return tool('create_node', {'graph': g(UCS), 'type_id': type_id, 'pos': {'x': x, 'y': y}})
    x0 = end.get('position', {}).get('x', 800) + 400
    n1 = mk(pick['set'], x0, 0); n2 = mk(pick['set'], x0 + 400, 0); nh = mk(pick['hcloth'], x0 - 300, 220); ns = mk(pick['scloth'], x0 + 100, 220); nm_ = mk(pick['manny'], x0 - 300, 340)
    ni = tool('get_node_infos', {'nodes': [n1, n2, nh, ns, nm_]}); by = {i['node']['refPath']: i for i in ni}
    def pin(node, direction, names):
        inf = by[node['refPath']]; pins = inf['output_pins'] if direction == 'out' else inf['input_pins']
        for p in pins:
            if any(p.get('name', '').lower() == k.lower() for k in names): return p['pin_id'], p
        for p in pins:
            if any(k.lower() in p.get('name', '').lower() for k in names): return p['pin_id'], p
        raise RuntimeError('pin %s %s; have %s' % (direction, names, [p.get('name') for p in pins]))
    conns = []
    def connect(o, i): r = tool('connect_pins', {'output_pin': o[0], 'input_pin': i[0]}); conns.append(r); print('CONNECT', o[1].get('name'), '->', i[1].get('name'), r)
    connect((outpin(end, 'then')['pin_id'], outpin(end, 'then')), pin(n1, 'in', ['execute']))
    connect(pin(n1, 'out', ['then']), pin(n2, 'in', ['execute']))
    connect(pin(nh, 'out', ['henleycloth']), pin(n1, 'in', ['self', 'target', 'hedef']))
    connect(pin(nm_, 'out', ['manny']), pin(n1, 'in', ['newleaderbonecomponent', 'leader']))
    connect(pin(ns, 'out', ['shortscloth']), pin(n2, 'in', ['self', 'target', 'hedef']))
    connect(pin(nm_, 'out', ['manny']), pin(n2, 'in', ['newleaderbonecomponent', 'leader']))
    rep['compile'] = tool('compile_blueprint', {'blueprint': g(BP), 'warnings_as_errors': False}); print('COMPILE', rep['compile']); rep['connections'] = conns
    sub2 = tool('get_connected_subgraph', {'node': entry[0]}); inf2 = [i for i in sub2 if isinstance(i, dict) and 'node' in i]
    rep['chain_after'] = [(i['node']['refPath'].rsplit('.', 1)[-1], i.get('type_id'), [cp['node']['refPath'].rsplit('.', 1)[-1] for p in i['input_pins'] if p['name'] in ('self', 'NewLeaderBoneComponent', 'execute') for cp in p['connected_pins']]) for i in inf2]
    print('CHAIN AFTER', json.dumps(rep['chain_after'], ensure_ascii=False))
(R/'data'/('mcp_leaderpose_%s.json' % mode)).write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding='utf-8'); print('DONE', mode)
