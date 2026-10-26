"""fix_v231_inspect_tick.py (editor job): install_v231_inspect.py disconnected ALL exec links into SHM_PerfLapCam when it inserted the resolver
(PerfLapCam had two sources: the camera call and the ELSE of the CameraPhysicalSignalsEnabled branch). Restores branch.else -> PerfLapCam.
Prints the exec sources before/after and the flag's DA value. builtins.V231_SAVE saves. Prints INSPECTTICK231 {...}."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import connect, src, pn, info
import builtins, json
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
CP = '/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent'; bp = u.load_asset(CP)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
tick = graph(bp, 'SHM_Tick'); tn = [pn(n) for n in B.find_nodes(tick)]
plc = [p for p in tn if tid(p).split('|')[-1] == 'SHM_PerfLapCam']; assert len(plc) == 1, plc
cs = [p for p in tn if tid(p).split('|')[-1] == 'SHM_UpdateCameraSignals']; assert len(cs) == 1, cs
br = src((cs[0], 'execute')); assert br and 'IfThenElse' in br[0][0] and br[0][1] == 'then', br
out = {'before': [(a.rsplit('.', 1)[-1], b) for a, b in src((plc[0], 'execute'))], 'branch': br[0][0].rsplit('.', 1)[-1]}
connect((br[0][0], 'else'), (plc[0], 'execute'))
out['after'] = [(a.rsplit('.', 1)[-1], b) for a, b in src((plc[0], 'execute'))]
da = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default'); out['CameraPhysicalSignalsEnabled'] = str(da.get_editor_property('CameraPhysicalSignalsEnabled'))
st, errs = compile_ok(bp); out['status'] = str(st); out['errs'] = errs[:6]
ok = 'UP_TO_DATE' in str(st) and not errs; out['ok'] = ok
if ok and getattr(builtins, 'V231_SAVE', False): save(bp); out['saved'] = True
print('INSPECTTICK231 ' + json.dumps(out, default=str))
