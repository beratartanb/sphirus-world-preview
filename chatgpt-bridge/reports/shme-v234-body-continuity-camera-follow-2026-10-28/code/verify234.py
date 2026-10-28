"""verify234.py (fresh editor, read-only, SHME_KIND=measure): every earlier contract (verify233 -> verify232) plus V2.34.
builtins.V234_EXP = {'loco': bool, 'camfollow': bool, 'revkeep': bool, 'sprintcalm': bool}. verify233 runs with its V2.33 expectations;
the one V2.33 value V2.34 deliberately changes (CamRecMinSpeed 170 -> 60 with camfollow) is accepted. V2.34 checks: DA / ABP values,
SHM_UpdateCameraV21 census (LocoYaw / LocoIFY / InFrameOff / CamEnv / CamRecTurnSign setters, > 1500 nodes, no LINKED LastHitBy),
SHM_UpdateRouting (SHM234_RevAgo / RevDir / GapT setters), BP_GR_Player: the 7 locomotion readers read GR234_LocoYaw and no control
rotation reaches them directly + the writer, ABP: SHM234_RevDB snapshot memory + the Update_MotionMatching entry keep. Prints VERIFY234."""
import builtins, json
E = dict(getattr(builtins, 'V234_EXP', {}))
builtins.V233_EXP = {'standback': True, 'camrec': True, 'sprintcalm': bool(E.get('sprintcalm'))}
g3 = {'__name__': 'v233'}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V233_20261027/verify233.py', encoding='utf8').read(), g3)
import unreal as u
from qa_graph import info as qinfo, src as qsrc
B = g3['B']; graph = g3['graph']; pn = g3['pn']; tid = g3['tid']
bad = [b for b in g3['bad'] if not (E.get('camfollow') and str(b).startswith('CamRecMinSpeed'))]
sda = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default')
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
abp = u.load_asset(AP); cdo = u.get_default_object(abp.generated_class())
da = {k: sda.get_editor_property(k) for k in ('LocoFrameEnabled', 'LocoExploreEnabled', 'LocoExploreMaxSpeed', 'CamRecEnabled', 'CamRecMinSpeed', 'CamRecWalkRate', 'CamRecFaceMax', 'CamRecTurnSide', 'CamEnvEnabled', 'RevGraceTime')}
want = {}
if E.get('loco'): want.update({'LocoFrameEnabled': True, 'LocoExploreEnabled': True, 'LocoExploreMaxSpeed': 380.0})
if E.get('camfollow'): want.update({'CamRecMinSpeed': 60.0, 'CamRecWalkRate': 45.0, 'CamRecFaceMax': 40.0, 'CamRecTurnSide': True, 'CamEnvEnabled': True})
if E.get('revkeep'): want.update({'RevGraceTime': 0.4})
for k, v in want.items():
    if (abs(float(da[k]) - v) > 1e-3) if isinstance(v, float) else (bool(da[k]) != v): bad.append('DA %s=%s want %s' % (k, da[k], v))
knob = float(cdo.get_editor_property('SHM234_RevKeepOn'))
if bool(E.get('revkeep')) != (knob >= 0.5): bad.append('SHM234_RevKeepOn %s' % knob)
comp = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent')
cam = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateCameraV21'))]
rt = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateRouting'))]
cen = {'cam_nodes': len(cam), 'route_nodes': len(rt)}
for k in ('LocoYaw', 'LocoIFY', 'InFrameOff', 'CamEnv', 'CamRecTurnSign'): cen[k] = sum(t.endswith('|Set' + k) for t in cam)
for k in ('SHM234_RevAgo', 'SHM234_RevDir', 'SHM234_GapT'): cen[k] = sum(t.endswith('|Set' + k) for t in rt)
cen['lhb_linked'] = sum(1 for n in B.find_nodes(graph(comp, 'SHM_UpdateCameraV21')) if tid(pn(n)).endswith('|GetLastHitBy') and any(o.connected_pins for o in qinfo(pn(n)).output_pins))
if cen['cam_nodes'] < 1500 or cen['route_nodes'] < 150 or cen['lhb_linked'] or any(cen[k] < 1 for k in ('LocoYaw', 'LocoIFY', 'InFrameOff', 'CamEnv', 'CamRecTurnSign', 'SHM234_RevAgo', 'SHM234_RevDir', 'SHM234_GapT')):
    bad.append('component census %s' % cen)
gp = u.load_asset('/Game/GraceRanger/BP_GR_Player'); rd = {}
for fn in ('CalculateMaxSpeed', 'CalculateMaxAcceleration', 'CalculateGroundFriction', 'GetDesiredGait', 'GR_Impl_CR_UpdateBackwardIntent', 'GR_Impl_CP_PhysicalRedirect', 'GR_UpdateIdleTurn'):
    ns = [pn(n) for n in B.find_nodes(graph(gp, fn))]
    loco = sum(tid(p).endswith('|GetGR234_LocoYaw') for p in ns)
    direct = 0
    for p in ns:
        for ip in qinfo(p).input_pins:
            for s_ in qsrc((p, ip.name)):
                if tid(s_[0]).endswith('GetControlRotation') and 'BreakRotator' not in tid(p): direct += 1
    rd[fn] = [loco, direct]
    if loco < 1 or direct: bad.append('reader %s %s' % (fn, rd[fn]))
sig = [tid(pn(n)) for n in B.find_nodes(graph(gp, 'GR_UpdateSHMSignals'))]
if not any(t.endswith('|SetGR234_LocoYaw') for t in sig) or not any(t.endswith('|SetGR234_LocoOn') for t in sig): bad.append('GR234 writer missing')
sn = [tid(pn(n)) for n in B.find_nodes(graph(abp, 'SHM_Snapshot'))]; mm = [tid(pn(n)) for n in B.find_nodes(graph(abp, 'Update_MotionMatching'))]
rk = {'snap_db': any(t.endswith('|SetSHM234_RevDB') for t in sn), 'snap_t': any(t.endswith('|SetSHM234_RevDBT') for t in sn), 'entry': sum(t.endswith('|GetSHM234_RevDB') for t in mm)}
if not (rk['snap_db'] and rk['snap_t'] and rk['entry'] >= 1): bad.append('revkeep graph %s' % rk)
print('VERIFY234 ' + json.dumps({'v233_bad': g3['bad'], 'da': {k: str(v) for k, v in da.items()}, 'revkeep_knob': knob, 'census': cen, 'readers': rd, 'revkeep': rk,
                                  'bad': bad, 'ALL_OK': not bad}, default=str))
