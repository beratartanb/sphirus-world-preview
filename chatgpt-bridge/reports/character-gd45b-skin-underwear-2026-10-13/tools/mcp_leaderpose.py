"""GD45: add the runtime leader-pose assignment for the skinned garments to BP_Player_MM's UserConstructionScript through the editor's
ModelContextProtocol Blueprint toolset (the only sanctioned way to edit Blueprint graphs from automation here).
    Construction script:  entry -> Henley.SetLeaderPoseComponent(Manny) -> Shorts.SetLeaderPoseComponent(Manny)
The construction script chains to the parent's automatically (no parent-call needed, unlike BeginPlay) and runs on every spawn, so the
follower references are instance-level (a LeaderPoseComponent set on the SCS template is not instanced: PIE showed the template name).
usage: python mcp_leaderpose.py inspect|apply   (session id from data/mcp_sid.txt; server started with ModelContextProtocol.StartServer)"""
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
    if d.get('result', {}).get('isError'): raise RuntimeError(name + ': ' + txt[:600])
    try: return json.loads(txt).get('returnValue', txt)
    except Exception: return txt
def g(ref): return {'refPath': ref}
mode = sys.argv[1] if len(sys.argv) > 1 else 'inspect'; rep = {}
types = {}
for key, flt in (('set', 'SetLeaderPoseComponent'), ('henley', 'HenleyAl'), ('shorts', 'ShortsAl'), ('manny', 'MannyAl')):
    cands = tool('find_node_types', {'graph': g(UCS), 'type_id_filter': flt, 'context_pins': []}); types[key] = cands; print(key, cands)
pick = {}
pick['set'] = next(t for t in types['set'] if t.endswith('|SetLeaderPoseComponent') and 'SkinnedMesh' in t)
for key in ('henley', 'shorts', 'manny'):
    nm = {'henley': 'HenleyAl', 'shorts': 'ShortsAl', 'manny': 'MannyAl'}[key]
    pick[key] = next(t for t in types[key] if t.endswith('|' + nm) and ('Varsay' in t or 'Default' in t))
print('PICK', pick)
pins_set = tool('get_node_type_pins', {'graph': g(UCS), 'type_id': pick['set']}); print('SET PINS', json.dumps(pins_set)[:800])
entry = tool('find_nodes', {'graph': g(UCS), 'title': '', 'entry_points_only': True}); print('ENTRY', entry)
entry_info = tool('get_node_infos', {'nodes': entry}); print('ENTRY INFO', json.dumps(entry_info)[:1200])
rep.update({'types': types, 'pick': pick, 'pins_set': pins_set, 'entry': entry, 'entry_info': entry_info})
if mode == 'apply':
    def mk(type_id, x, y):
        n = tool('create_node', {'graph': g(UCS), 'type_id': type_id, 'pos': {'x': x, 'y': y}}); print('CREATED', type_id, n); return n
    n_set1 = mk(pick['set'], 400, 0); n_set2 = mk(pick['set'], 800, 0); n_hen = mk(pick['henley'], 100, 200); n_sho = mk(pick['shorts'], 500, 200); n_man = mk(pick['manny'], 100, 320)
    # the entry's "then" already feeds the existing Parent: ConstructionScript node -> chain after that node
    e_out = next(p for p in entry_info[0]['output_pins'] if p['name'] == 'then'); parent_ref = e_out['connected_pins'][0]['node'] if e_out['connected_pins'] else None
    chain_from = parent_ref if parent_ref else entry[0]; print('CHAIN FROM', chain_from)
    infos = tool('get_node_infos', {'nodes': [n_set1, n_set2, n_hen, n_sho, n_man, chain_from]}); rep['infos'] = infos; print('INFOS', json.dumps(infos, ensure_ascii=False)[:3000])
    def info_of(node_ref):
        for inf in infos:
            if inf.get('node', {}).get('refPath') == node_ref['refPath']: return inf
        raise RuntimeError('no info for ' + node_ref['refPath'])
    def find_pin(node_ref, direction, names):
        inf = info_of(node_ref); pins = inf['output_pins'] if direction == 'EGPD_Output' else inf['input_pins']
        for p in pins:
            if any(p.get('name', '').lower() == k.lower() for k in names): return p['pin_id'], p
        for p in pins:
            if any(k.lower() in p.get('name', '').lower() for k in names): return p['pin_id'], p
        raise RuntimeError('pin not found %s %s %s; have %s' % (node_ref['refPath'][-40:], direction, names, [p.get('name') for p in pins]))
    conns = []
    def connect(o, i):
        r = tool('connect_pins', {'output_pin': o[0], 'input_pin': i[0]}); conns.append(r); print('CONNECT', o[1].get('name'), '->', i[1].get('name'), r)
    src_then = find_pin(chain_from, 'EGPD_Output', ['then'])
    if src_then[1].get('connected_pins'): print('WARNING: source then already connected:', src_then[1]['connected_pins'])
    connect(src_then, find_pin(n_set1, 'EGPD_Input', ['execute']))
    connect(find_pin(n_set1, 'EGPD_Output', ['then']), find_pin(n_set2, 'EGPD_Input', ['execute']))
    hen_out = find_pin(n_hen, 'EGPD_Output', ['henley']); sho_out = find_pin(n_sho, 'EGPD_Output', ['shorts']); man_out = find_pin(n_man, 'EGPD_Output', ['manny'])
    connect(hen_out, find_pin(n_set1, 'EGPD_Input', ['self', 'target', 'hedef']))
    connect(man_out, find_pin(n_set1, 'EGPD_Input', ['leader', 'newleader', 'lider']))
    connect(sho_out, find_pin(n_set2, 'EGPD_Input', ['self', 'target', 'hedef']))
    connect(man_out, find_pin(n_set2, 'EGPD_Input', ['leader', 'newleader', 'lider']))
    comp = tool('compile_blueprint', {'blueprint': g(BP), 'warnings_as_errors': False}); print('COMPILE', comp); rep['compile'] = comp; rep['connections'] = conns
    rep['dsl_after'] = tool('read_graph_dsl', {'graph': g(UCS)}); print('DSL AFTER', str(rep['dsl_after'])[:1200])
(R/'data'/('mcp_leaderpose_%s.json' % mode)).write_text(json.dumps(rep, indent=1, ensure_ascii=False), encoding='utf-8'); print('DONE', mode)
