"""verify233.py (fresh editor, read-only, SHME_KIND=measure): every earlier contract (verify232 with its V2.32 expectations) plus V2.33.
builtins.V233_EXP = {'standback': bool, 'camrec': bool, 'sprintcalm': bool}. V2.33 checks: ABP knobs / DB routes, snapshot setter +
entry override present, stand-back DB entries (clip + back loop), component SHM_UpdateCameraV21 census (orbit / recentre / latch nodes,
no LINKED GetLastHitBy), SHM_Telemetry writes TelemetryLine (no PrintString), parent move-frame select (2 SelectFloat into the IA_Move
frames), child control-yaw writer + CamRecScale setter, device scales, DA CamRecEnabled, IntentTickPrePhysics false, the gated runner
in use (gate233.log RUNNER_START this session). Prints VERIFY233 {... ALL_OK}."""
import builtins, json, pathlib
X = dict(getattr(builtins, 'V233_EXP', {}))
builtins.V232_EXP = {'camera': True, 'bfexit': True, 'loadedbf': True, 'floorguard': True}
builtins.V232_EXPV = {'CamOrbitEnabled': True, 'CamOrbitLagTau': 0.3, 'CamOrbitFreq': 5.0, 'CamOrbitMaxSprint': 16.0, 'CamOrbitMaxJog': 8.0, 'CamOrbitMaxWalk': 2.0,
                      'SwingFloorGuard': 1.5, 'SwingPelvisComp': 0.0, 'SHM232_StartBind': 0.0,
                      'SHM224_DB_JRBwd': 'PSD_SHM232_JogRevBwdX', 'SHM224_DB_JRBwdM': 'PSD_SHM232_JogRevBwdX', 'SHM231_DB_JRBwdS': 'PSD_SHM232_SlowRevBwdX', 'SHM230_DB_JRBwdL': 'PSD_SHM232_LoadRevBwdX'}
g = {'__name__': 'v232'}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V232_20261027/verify232.py', encoding='utf8').read(), g)
import unreal as u
bad = list(g.get('bad', [])); B = g['B']; graph = g['graph']; pn = g['pn']; tid = g['tid']
from qa_graph import info as qinfo, src as qsrc
V = '/Game/GraceRanger/SHME/Animations/V233/'
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
abp = u.load_asset(AP); cdo = u.get_default_object(abp.generated_class()); sda = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default')
k = {'SHM233_StandBackOn': float(cdo.get_editor_property('SHM233_StandBackOn')), 'SHM233_DB_StandBack': cdo.get_editor_property('SHM233_DB_StandBack').get_name(),
     'SHM211_DB_Sprint': cdo.get_editor_property('SHM211_DB_Sprint').get_name(), 'CamRecEnabled': bool(sda.get_editor_property('CamRecEnabled')),
     'IntentTickPrePhysics': bool(sda.get_editor_property('IntentTickPrePhysics')), 'CamRecMaxErr': float(sda.get_editor_property('CamRecMaxErr'))}
if X.get('camrec') and abs(k['CamRecMaxErr'] - 110.0) > 1e-3: bad.append('CamRecMaxErr %s want 110' % k['CamRecMaxErr'])
k['CamRecMinSpeed'] = float(sda.get_editor_property('CamRecMinSpeed'))
if X.get('camrec') and abs(k['CamRecMinSpeed'] - 170.0) > 1e-3: bad.append('CamRecMinSpeed %s want 170' % k['CamRecMinSpeed'])
if X.get('standback'):
    if k['SHM233_StandBackOn'] != 2.0 or k['SHM233_DB_StandBack'] != 'PSD_SHM233_StandBackStart2': bad.append('standback knobs %s' % k)
elif k['SHM233_StandBackOn'] != 0.0: bad.append('standback knob on without promotion')
if bool(X.get('camrec')) != k['CamRecEnabled']: bad.append('CamRecEnabled %s want %s' % (k['CamRecEnabled'], bool(X.get('camrec'))))
if X.get('sprintcalm') and k['SHM211_DB_Sprint'] != 'PSD_SHM233_SprintCalm': bad.append('sprintcalm DB %s' % k['SHM211_DB_Sprint'])
if k['IntentTickPrePhysics']: bad.append('IntentTickPrePhysics true')
snap = [tid(pn(n)) for n in B.find_nodes(graph(abp, 'SHM_Snapshot'))]; mmg = [tid(pn(n)) for n in B.find_nodes(graph(abp, 'Update_MotionMatching'))]
gr = {'snapshot_setter': any(t.endswith('|SetSHM233_StandBack') for t in snap), 'timer': any(t.endswith('|SetSHM233_SBT') for t in snap),
      'entry_override': any(t.endswith('|GetSHM233_SBT') for t in mmg), 'route_db_getters': sum(t.endswith('|GetSHM233_DB_StandBack') for t in mmg)}
if not (gr['snapshot_setter'] and gr['timer'] and gr['entry_override'] and gr['route_db_getters'] >= 3): bad.append('stand-back graph %s' % gr)
d2 = u.load_asset(V + 'PSD_SHM233_StandBackStart2'); e2 = [d2.get_animation_asset(i).get_name() for i in range(d2.get_num_animation_assets())] if d2 else []
if sorted(e2) != ['A_RB_Jog_Rear', 'SHM233_StandBack2_Jog_Bwd']: bad.append('stand-back DB2 entries %s' % e2)
comp = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent')
cam = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateCameraV21'))]
def linked_lhb(bp, gn):
    return sum(1 for n in B.find_nodes(graph(bp, gn)) if tid(pn(n)).endswith('|GetLastHitBy') and any(o.connected_pins for o in qinfo(pn(n)).output_pins))
cen = {'nodes': len(cam), 'orbit': sum('CamOrbit' in t for t in cam), 'rec': sum('CamRec' in t for t in cam), 'latch': sum('MoveLatch' in t for t in cam), 'lhb_linked': linked_lhb(comp, 'SHM_UpdateCameraV21')}
if cen['nodes'] < 1000 or cen['orbit'] < 30 or cen['rec'] < 20 or cen['latch'] < 10 or cen['lhb_linked']: bad.append('camera function census %s' % cen)
tel = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_Telemetry'))]
telok = {'set_line': any(t.endswith('|SetTelemetryLine') for t in tel), 'print': any('PrintString' in t for t in tel)}
if not telok['set_line'] or telok['print']: bad.append('telemetry %s' % telok)
par = u.load_asset('/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/BP_ExampleCharacter_MotionMatching')
ev = {pn(n).rsplit('.', 1)[-1]: pn(n) for n in B.find_nodes(graph(par, 'EventGraph'))}
mf = {vn: tid(qsrc((ev[vn], 'InRot_Yaw'))[0][0]).split('|')[-1] if vn in ev and qsrc((ev[vn], 'InRot_Yaw')) else None for vn in ('K2Node_CallFunction_55', 'K2Node_CallFunction_39')}
if not all(v and 'SelectFloat' in v for v in mf.values()): bad.append('move frame select %s' % mf)
gp = u.load_asset('/Game/GraceRanger/BP_GR_Player')
sig = [tid(pn(n)) for n in B.find_nodes(graph(gp, 'GR_UpdateSHMSignals'))]
wr = {'set_ctl': sum(t.endswith('SetControlRotation') for t in sig), 'latch_set': any(t.endswith('|SetGR233_MoveLatchOn') for t in sig), 'scale_set': any(t.endswith('|SetCamRecScale') for t in sig)}
gcdo = u.get_default_object(gp.generated_class())
wr['pad'] = float(gcdo.get_editor_property('GR233_RecPadScale')); wr['mouse'] = float(gcdo.get_editor_property('GR233_RecMouseScale'))
if wr['set_ctl'] != 1 or not wr['latch_set'] or not wr['scale_set'] or wr['pad'] != 1.0 or abs(wr['mouse'] - 0.35) > 1e-4: bad.append('BP_GR_Player writer %s' % wr)
glog = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/SHME_V233_20261027/gate233.log'
gate = glog.exists() and 'RUNNER_START gates G1-G5' in glog.read_text(encoding='utf8', errors='replace')
if not gate: bad.append('gated runner not in use')
print('VERIFY233 ' + json.dumps({'v232_bad': g.get('bad', []), 'knobs': k, 'standback_graph': gr, 'db2': e2, 'camera_census': cen, 'telemetry': telok,
                                  'move_frame': mf, 'writer': wr, 'gated_runner': gate, 'bad': bad, 'ALL_OK': not bad}, default=str))
