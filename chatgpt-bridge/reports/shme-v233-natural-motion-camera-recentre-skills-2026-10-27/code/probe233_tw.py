"""probe233_tw.py (measure): BP_GR_Player graphs that SET or READ TW_CameraWorldYaw / CT_VisualCameraYaw / ContinuityRevision, the branch
in front of the EventGraph SetControlRotation, and the list of graphs. Prints TW233 {...}."""
import unreal as u, json, pathlib, sys
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Saved/Codex/GraceRanger_QA_20260914/Scripts'))
from qa_graph import pn, info
from editor_toolset.toolsets.blueprint import BlueprintTools as B
bp = u.load_asset('/Game/GraceRanger/BP_GR_Player')   # the in-game pawn parent (the Sandbox copy is NOT in the chain)
VARS = ('TW_CameraWorldYaw', 'CT_VisualCameraYaw', 'ContinuityRevision', 'TW_', 'GR_CamAuto', 'Recenter', 'AutoAlign', 'CameraFollow')
out = {'graphs': [], 'sets': {}, 'gets': {}, 'branch20': None}
def tree(p, d=0, seen=None):
    seen = seen or set()
    if p in seen or d > 5: return '...'
    seen.add(p); ni = info(p); t = str(ni.type_id).rsplit('|', 1)[-1]; kids = {}
    for q in ni.input_pins:
        if str(q.name) in ('execute', 'then'): continue
        if q.connected_pins: kids[str(q.name)] = [tree(pn(c.node), d + 1, seen) for c in q.connected_pins]
        elif str(q.value) not in ('', 'None'): kids[str(q.name)] = str(q.value)[:30]
    return {t + ' ' + p.rsplit('.', 1)[-1]: kids}
for g in B.list_graphs(bp):
    gn = pn(g).split(':')[-1].split('.')[-1]; out['graphs'].append(gn)
    try: ns = B.find_nodes(g)
    except Exception: continue
    for n in ns:
        p = pn(n); t = str(info(p).type_id)
        for v in VARS:
            if v in t:
                k = 'sets' if '|Set' in t or 'VariableSet' in t else 'gets'
                out[k].setdefault(gn, set()).add(t.rsplit('|', 1)[-1])
        if gn == 'EventGraph' and p.endswith('K2Node_IfThenElse_20'): out['branch20'] = tree(p)
        if 'VariableSet' in t or '|Set' in t:
            if 'TW_CameraWorldYaw' in t: out.setdefault('tw_set_trees', []).append({gn: tree(p)})
out['sets'] = {k: sorted(v) for k, v in out['sets'].items()}; out['gets'] = {k: sorted(v) for k, v in out['gets'].items()}
(P / 'Saved/Codex/SHME_V233_20261027/probe233_tw_game.json').write_text(json.dumps(out, indent=1, default=str))
print('TW233 ' + json.dumps({'sets': out['sets'], 'branch20': out['branch20'], 'n_tw_set': len(out.get('tw_set_trees', []))}, default=str)[:5000])
