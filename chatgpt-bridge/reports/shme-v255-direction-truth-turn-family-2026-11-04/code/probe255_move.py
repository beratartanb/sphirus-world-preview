"""probe255_move.py (measure): exec neighbourhood of IA_Move in the Integrated parent EventGraph, the V2.28 forward getter consumers in the GR redirect, and GR_UpdateSHMSignals anchors. Read only."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import src, pn, info, obj, op
PAR = '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_ExampleCharacter_MotionMatching'
g = op(PAR) + ':EventGraph'; N = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g))}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
n0 = N['K2Node_EnhancedInputAction_0']
print('IA pins out', [(str(o.name), [pn(q.node).rsplit('.', 1)[-1] + ':' + tid(pn(q.node)).rsplit('|', 1)[-1] for q in o.connected_pins]) for o in info(n0).output_pins])
b3 = N['K2Node_IfThenElse_3']
print('IF3 in', [(str(i.name), [pn(q.node).rsplit('.', 1)[-1] + ':' + tid(pn(q.node)).rsplit('|', 1)[-1] for q in i.connected_pins]) for i in info(b3).input_pins])
c83 = N['K2Node_CallFunction_83']
print('C83', tid(c83), [(str(o.name), str(o.pin_type) if hasattr(o, 'pin_type') else '') for o in info(c83).output_pins][:6], [(str(i.name)) for i in info(c83).input_pins])
PB = '/Game/GraceRanger/BP_GR_Player'; g2 = op(PB) + ':GR_UpdateSHMSignals'; N2 = [pn(n) for n in B.find_nodes(obj(g2))]
for p in N2:
    t = tid(p)
    if 'SetGR233_MoveLatch' in t or 'SetGR_SHM_CamOrbit' in t: print('SIG', p.rsplit('.', 1)[-1], t.rsplit('|', 1)[-1], [(s_[0].rsplit('.', 1)[-1], s_[1]) for s_ in src((p, 'execute'))])
g3 = op(PB) + ':GR_Impl_CP_PhysicalRedirect'; N3 = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(obj(g3))}
f = N3['K2Node_CallFunction_186']; print('FWD out', [(str(o.name), [pn(q.node).rsplit('.', 1)[-1] + ':' + tid(pn(q.node)).rsplit('|', 1)[-1] + '.' + [str(x.name) for x in info(pn(q.node)).input_pins if x.pin_id.index_id == q.index_id][0] for q in o.connected_pins]) for o in info(f).output_pins])
import unreal as _u
AR = _u.AssetRegistryHelpers.get_asset_registry()
print('JOGSTEADY', [str(a.package_name) for a in AR.get_assets_by_path('/Game', recursive=True) if str(a.asset_name) == 'PSD_CT_JogSteady'][:3] if False else '')
