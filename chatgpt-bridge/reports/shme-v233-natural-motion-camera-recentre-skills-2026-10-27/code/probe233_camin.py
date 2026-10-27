"""probe233_camin.py (editor job, SHME_KIND=measure): who writes / reads the control rotation and builds the movement input frame?
For the pawn chain (BP_Player_MM -> BP_GR_Player -> BP_PBI_Player) and the controller(s) every graph is scanned for AddMovementInput,
GetControlRotation, SetControlRotation, AddControllerYawInput / AddYawInput, K2_SetActorRotation; per hit graph + node + linked inputs.
Writes Saved/Codex/SHME_V233_20261027/probe233_camin.json; prints PROBE233 {...}. Read-only (no compile, no find_node_types)."""
import unreal as u, json, pathlib, sys
P = pathlib.Path(u.Paths.project_dir()).resolve()
sys.path.insert(0, str(P / 'Saved/Codex/GraceRanger_QA_20260914/Scripts'))
from qa_graph import pn, info
from editor_toolset.toolsets.blueprint import BlueprintTools as B
KEYS = ('AddMovementInput', 'GetControlRotation', 'SetControlRotation', 'AddControllerYawInput', 'AddYawInput', 'K2_SetActorRotation', 'GetBaseAimRotation')
AR = u.AssetRegistryHelpers.get_asset_registry()
cands = []
for n in ('BP_Player_MM', 'BP_GR_Player', 'BP_PBI_Player', 'BP_GR_InputBase', 'BP_GR_PlayerController', 'BP_PC_GR', 'BP_GM_GR_GraceRanger'):
    for a in AR.get_assets_by_path('/Game', recursive=True) if False else []: pass
flt = u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/Engine', 'Blueprint')], package_paths=['/Game/GraceRanger', '/Game/ActionAdventureMovementS'], recursive_paths=True)
for a in AR.get_assets(flt):
    nm = str(a.asset_name)
    if any(k in nm for k in ('Player', 'InputBase', 'Controller', 'PC_', 'Camera')) and not nm.startswith(('BP_LTP', 'BP_QA')): cands.append(str(a.package_name))
out = {'scanned': cands, 'hits': {}}
for ap in cands:
    try: bp = u.load_asset(ap)
    except Exception: continue
    if not bp: continue
    try: graphs = B.list_graphs(bp)
    except Exception: continue
    for g in graphs:
        gname = pn(g).split(':')[-1].split('.')[-1]
        try: nodes = B.find_nodes(g)
        except Exception: continue
        for n in nodes:
            try: ni = info(pn(n))
            except Exception: continue
            t = str(ni.type_id)
            if not any(k in t for k in KEYS): continue
            ins = []
            for p in ni.input_pins:
                if p.connected_pins: ins.append(str(p.name) + '<-' + ','.join(pn(q.node).rsplit('.', 1)[-1] for q in p.connected_pins))
            out['hits'].setdefault(ap.rsplit('/', 1)[-1], []).append({'graph': gname, 'node': pn(n).rsplit('.', 1)[-1], 'type': t.rsplit('|', 1)[-1], 'in': ins[:6]})
(P / 'Saved/Codex/SHME_V233_20261027/probe233_camin.json').write_text(json.dumps(out, indent=1))
print('PROBE233 ' + json.dumps({k: [(h['graph'], h['type']) for h in v] for k, v in out['hits'].items()})[:3000])
