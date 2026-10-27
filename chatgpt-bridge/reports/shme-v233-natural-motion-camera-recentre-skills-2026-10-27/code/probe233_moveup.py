"""probe233_moveup.py (measure): upstream expression trees of every AddMovementInput in BP_ExampleCharacter_MotionMatching EventGraph
(depth 6) -> which rotation builds the movement input frame. Prints MOVEUP233 {...}."""
import unreal as u, json, pathlib, sys
P = pathlib.Path(u.Paths.project_dir()).resolve(); sys.path.insert(0, str(P / 'Saved/Codex/GraceRanger_QA_20260914/Scripts'))
from qa_graph import pn, info
from editor_toolset.toolsets.blueprint import BlueprintTools as B
AR = u.AssetRegistryHelpers.get_asset_registry()
ap = ['/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_ExampleCharacter_MotionMatching']
bp = u.load_asset(ap[0]); out = {'asset': ap, 'trees': []}
nodes = {}
for g in B.list_graphs(bp):
    if pn(g).split(':')[-1].split('.')[-1] != 'EventGraph': continue
    for n in B.find_nodes(g): nodes[pn(n)] = n
def tree(p, d=0, seen=None):
    seen = seen or set()
    if p in seen or d > 7: return '...'
    seen.add(p); ni = info(p); t = str(ni.type_id).rsplit('|', 1)[-1]
    kids = {}
    for q in ni.input_pins:
        if str(q.name) in ('execute', 'then'): continue
        if q.connected_pins: kids[str(q.name)] = [tree(pn(c.node), d + 1, seen) for c in q.connected_pins]
        elif str(q.value) not in ('', 'None'): kids[str(q.name)] = str(q.value)[:40]
    return {t + ' ' + p.rsplit('.', 1)[-1]: kids}
for p in nodes:
    if 'AddMovementInput' in str(info(p).type_id): out['trees'].append(tree(p))
(P / 'Saved/Codex/SHME_V233_20261027/probe233_moveup_int.json').write_text(json.dumps(out, indent=1))
print('MOVEUP233 ' + json.dumps(out)[:6000])
