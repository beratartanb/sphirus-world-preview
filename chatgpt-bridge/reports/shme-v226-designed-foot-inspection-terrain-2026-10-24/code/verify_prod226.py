"""verify_prod226.py (read-only editor job): V2.26 production state (V2.25 checks + V2.26 via builtins.V226_EXP: Reversal226 (32-bin DBs), StepEdgeOn, InspectZoomOn, InspectTag, Snapshot SHM226_ShiftL, 2 world-space shift ModifyBones, SwingShift in BodyTargets, tag + bounds contract and hit telemetry in CameraV21, V226 DBs 32+4 without pivots, footspeed curves on the clips, no SHM226 leak, mask tags + probes). Base: V2.25 production state (V2.24 checks + V2.25) after a fresh editor start. Prints VERIFY225 {...} and ALL_OK.
V2.25 expectations from builtins.V225_EXP: Reversal (ABP JR databases = PSD_SHM225_JogRev*), StepPrepEnabled, CamInspectEnabled; the look-at chain
(AnimGraph Look At on head / Snapshot writes SHM225_LookAlpha), the component functions (SetStepPrepZ in BodyTargets, SetInspectOn in CameraV21),
the V2.25 databases (8 phase clips + 4 rear loops each, BranchIn entry windows) and no SHM225 clip in any production database.
V2.24 expectations come from builtins.V224_EXP (defaults = the V2.24 production decision): ABP SHM224_JRMode, SHM224_DB_JR* set, MontTick has the
request-identity nodes, EventGraph writes SHM_RedirectDB_JR, FeetIK lift nodes present, SHM_Snapshot writes SHM224_LiftL; SHME DA RedirectSpeedDecay,
SwingLiftEnabled; the V2.24 pivots / databases: no SHM224 asset in a production DB except through the JR route.
V2.23: ABP SHM223_RevRearGate 1 / JrHold 0 / SHM_RedirectDB_JR = PSD_SHM_Redirect_JogReversalQ; MontTick has the backRev / jrNow nodes;
GR: GR223_RevPushAccel 0 (candidate off), GR223_PivotXY (expected value builtins.V223_EXP_PXY, default 1); GR_CameraSafeOrigin returns the
unrotated XY offset (LessLess_VectorRotator present); SHME DA camera values (CamFollowEnabled etc. per builtins.V223_EXP_CAM, default on);
the V2.23 authored pivots are in NO production database (only PSD_SHM223_JogReversal).
Checks: no dirty packages / PIE; ABP CDO knobs (SHM220_RecHold 1, SHM221_RecThrottle 1, SHM221_PivHold 0 + V2.20 knobs unchanged);
graph wiring (MM SearchThrottleTime FMax with SHM221_RecThrottle, Set SHM220_Search fed by OR(.., NOT SHM217_RecOn), SHM221_PivWin set,
SHM213_MontTick has no LastHitBy variable read); pawn chain GR_Profile resolves to DA_GR_LocomotionBehavior on BP_GR_Player AND
BP_PBI_Player (the V2.21 tap-install regression); behaviour DA (GR221_TapStepCm 0, V2.20 values); SHME response DA V2.21 values;
component functions present (SHM_UpdateBodyTargets / SHM_UpdateCameraV21 contain the V2.21 traces / CamStepFire)."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import src, pn, info, obj
import json
LS = u.EditorLoadingAndSavingUtils
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
PB = '/Game/GraceRanger/BP_GR_Player'; CH = '/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'
DA = '/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior'; SDA = '/Game/GraceRanger/SHME/DA_SHM_Response_Default'
out = {'pie': u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is not None, 'dirty': [p.get_name() for p in LS.get_dirty_content_packages()]}
bad = []
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
abp = u.load_asset(AP); ac = u.get_default_object(abp.generated_class())
EXP_ABP = {'SHM28_StartMode': 1.0, 'SHM222_TapGate': 0.0, 'SHM220_RecHold': 1.0, 'SHM221_RecThrottle': 1.0, 'SHM221_PivHold': 0.0, 'SHM220_PivotOn': 1.0, 'SHM220_PivotT0': 0.0, 'SHM220_PivotNoRd': 0.0, 'SHM_SprintDBMinSpeed': 230.0}
out['abp'] = {}
for k, v in EXP_ABP.items():
    x = float(ac.get_editor_property(k)); out['abp'][k] = x
    if abs(x - v) > 1e-4: bad.append('abp.' + k)
ag = graph(abp, 'AnimGraph'); mm = [pn(n) for n in B.find_nodes(ag) if n.get_class().get_name() == 'AnimGraphNode_MotionMatching']
thr = src((mm[0], 'SearchThrottleTime')); out['throttle'] = [tid(x[0])[-30:] for x in thr]
if not (len(thr) == 1 and tid(thr[0][0]).endswith('Max(Float)')): bad.append('throttle_wiring')
eg = graph(abp, 'EventGraph'); en = [pn(n) for n in B.find_nodes(eg)]
ss = [p for p in en if 'SetSHM220_Search' in tid(p)]; sx = src((ss[0], 'SHM220_Search')) if len(ss) == 1 else []
out['search_src'] = [tid(x[0])[-30:] for x in sx]
if not (sx and ('BooleanOR' in tid(sx[0][0]) or 'ORBoolean' in tid(sx[0][0]))): bad.append('recexit_wiring')
if not any('SetSHM221_PivWin' in tid(p) for p in en): bad.append('pivwin_missing')
mt = graph(abp, 'SHM213_MontTick'); lhb = [pn(n) for n in B.find_nodes(mt) if 'LastHitBy' in tid(pn(n))]
def linked(p):
    try: return any(len(q.connected_pins) for q in info(p).output_pins)
    except Exception: return True
out['monttick_lasthitby_nodes'] = [(x.rsplit('.', 1)[-1], tid(x)[-40:], linked(x)) for x in lhb]
if any(linked(x) for x in lhb): bad.append('lasthitby_linked')
out['profile'] = {}
for ap in (PB, CH):
    v = u.get_default_object(u.load_asset(ap).generated_class()).get_editor_property('GR_Profile')
    out['profile'][ap.rsplit('/', 1)[-1]] = v.get_path_name() if v else 'None'
    if not v or not v.get_path_name().endswith('DA_GR_LocomotionBehavior'): bad.append('profile.' + ap.rsplit('/', 1)[-1])
da = u.load_asset(DA)
EXP_DA = {'GR221_TapStepCm': 0.0, 'GR220_StopFaceHold': 1.0, 'GR220_StopFaceHoldMinErr': 45.0, 'GR220_GaitDownDecel': 250.0, 'GR215_RevBrakeAccel': 0.0, 'GR215_RevBrakeDecel': 0.0}
out['da'] = {}
for k, v in EXP_DA.items():
    x = float(da.get_editor_property(k)); out['da'][k] = x
    if abs(x - v) > 1e-4: bad.append('da.' + k)
sda = u.load_asset(SDA)
EXP_SHM = {'SettleBodyEnabled': True, 'SettleBodyDeg': 6.0, 'SettleBodyDipCm': 2.0, 'SettleBodyMinSpeed': 60.0, 'TerrainBodyEnabled': True,
           'TerrainLeanUpGain': 0.15, 'TerrainLeanUpMax': 2.5, 'TerrainLeanDownGain': 0.1, 'TerrainLeanDownMax': 1.2, 'CamV221Enabled': True,
           'CamFOVSpeedMax': 0.0, 'CamStepGainWalk': 0.35, 'CamStepGainJog': 0.6, 'CamStepGainSprint': 0.9, 'CamComfortScale': 1.0,
           'CurveLeanDirectEnabled': True, 'CamRollGain': 0.1, 'CamBodyFreq': 3.5, 'CamCloseEnabled': True, 'CamCloseWalk': 0.88, 'CamCloseJog': 0.92, 'CamCloseSprint': 0.97, 'CamCloseStand': 0.9}
out['shm'] = {}
for k, v in EXP_SHM.items():
    x = sda.get_editor_property(k); out['shm'][k] = x
    if (bool(x) != v) if isinstance(v, bool) else abs(float(x) - v) > 1e-4: bad.append('shm.' + k)
comp = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent')
for fnm, key in (('SHM_UpdateBodyTargets', 'LineTraceByChannel'), ('SHM_UpdateCameraV21', 'SetCamStepFire')):
    try:
        ns = [tid(pn(n)) for n in B.find_nodes(graph(comp, fnm))]; ok = any(key in t for t in ns)
    except Exception as e: ok = False
    out['fn.' + fnm] = ok
    if not ok: bad.append('fn.' + fnm)

# ---- V2.22: start clips, re-acceleration content (baked != checkpoint original), re-keyed databases
for k, nm in (('SHM28_StartL', 'A_SHM222_WalkStart_L'), ('SHM28_StartR', 'A_SHM222_WalkStart_R')):
    v = ac.get_editor_property(k); out['abp'][k] = v.get_path_name() if v else 'None'
    if not v or not v.get_path_name().endswith(nm): bad.append('abp.' + k)
import hashlib, pathlib as _pl
_P = _pl.Path(u.Paths.project_dir()).resolve(); out['revturn'] = {}
for s_ in ('L_Lfoot', 'L_Rfoot', 'R_Lfoot', 'R_Rfoot'):
    a_ = _P / ('Content/GraceRanger/SHME/Animations/V216/SHM216_RevTurn_%s.uasset' % s_); b_ = _P / ('Saved/Codex/SHME_V222_20261022/checkpoint/revturn/SHM216_RevTurn_%s.uasset' % s_)
    same = b_.exists() and hashlib.md5(a_.read_bytes()).hexdigest() == hashlib.md5(b_.read_bytes()).hexdigest()
    out['revturn'][s_] = 'ORIGINAL' if same else 'baked'
    if same: bad.append('revturn.' + s_)
for dbp in ('/Game/GraceRanger/SHME/Animations/V214/PSD_SHM214_RevPush', '/Game/GraceRanger/SHME/Animations/V215/PSD_SHM215_RevPushLow', '/Game/GraceRanger/SHME/Animations/V215/PSD_SHM215_Rev_L', '/Game/GraceRanger/SHME/Animations/V215/PSD_SHM215_Rev_R'):
    tg = [str(t) for t in (u.load_asset(dbp).get_editor_property('tags') or [])]
    if 'SHME_V222_RB3' not in tg: bad.append('dbtag.' + dbp.rsplit('/', 1)[-1])
for p_ in ('/Game/GraceRanger/SHME/Animations/V222/A_SHM222_WalkStart_L', '/Game/GraceRanger/SHME/Animations/V222/A_SHM222_WalkStart_R'):
    if not u.EditorAssetLibrary.does_asset_exist(p_): bad.append('missing.' + p_.rsplit('/', 1)[-1])

# ---- V2.23
import builtins as _b
EXP_PXY = float(getattr(_b, 'V223_EXP_PXY', 1.0)); EXP_CAM = bool(getattr(_b, 'V223_EXP_CAM', True))
for k, v in (('SHM223_RevRearGate', 1.0), ('SHM223_JrHold', 0.0)):
    x = float(ac.get_editor_property(k)); out['abp'][k] = x
    if abs(x - v) > 1e-4: bad.append('abp.' + k)
jr = ac.get_editor_property('SHM_RedirectDB_JR'); out['abp']['JR'] = jr.get_path_name() if jr else 'None'
if not jr or not jr.get_path_name().endswith('PSD_SHM_Redirect_JogReversalQ'): bad.append('abp.JR')
mtn = [tid(pn(n)) for n in B.find_nodes(graph(abp, 'SHM213_MontTick'))]
if not any('GetActorForwardVector' in t for t in mtn): bad.append('monttick.backRev')
if not any('SetSHM223_JrOn' in t for t in mtn): bad.append('monttick.jrHold')
for k, v in (('GR223_RevPushAccel', 0.0), ('GR223_PivotXY', EXP_PXY)):
    x = float(da.get_editor_property(k)); out['da'][k] = x
    if abs(x - v) > 1e-4: bad.append('da.' + k)
so = [tid(pn(n)) for n in B.find_nodes(graph(u.load_asset(PB), 'GR_CameraSafeOrigin'))]
if not any('LessLess_VectorRotator' in t or 'UnrotateVector' in t for t in so): bad.append('safeorigin.xy')
pr = [tid(pn(n)) for n in B.find_nodes(graph(u.load_asset(PB), 'GR_Impl_CP_PhysicalRedirect'))]
if not any('SetGR223_RevAgainstT' in t for t in pr): bad.append('physredirect.revpush')
for k, v in (('CamFollowEnabled', EXP_CAM), ('CamBrakeCarry', 0.0 if EXP_CAM else 6.0), ('CamAccelCarry', 0.0 if EXP_CAM else 8.0)):
    x = sda.get_editor_property(k); out['shm'][k] = x
    if (bool(x) != v) if isinstance(v, bool) else abs(float(x) - v) > 1e-4: bad.append('shm.' + k)
for dbn in ('/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogPivots', '/Game/GraceRanger/SHME/Animations/Redirect/PSD_SHM_Redirect_JogReversal', '/Game/GraceRanger/SHME/Animations/Redirect/PSD_SHM_Redirect_JogReversalQ'):
    d_ = u.load_asset(dbn); ents = [d_.get_animation_asset(i).get_name() for i in range(d_.get_num_animation_assets())]
    if any(e.startswith('SHM223_') for e in ents): bad.append('db_leak.' + dbn.rsplit('/', 1)[-1])
    out.setdefault('db', {})[dbn.rsplit('/', 1)[-1]] = len(ents)

# ---- V2.24
EXP = dict({'SHM224_JRMode': 3.0, 'RedirectSpeedDecay': 600.0, 'SwingLiftEnabled': True, 'CamFolYawFade': 90.0}, **getattr(_b, 'V224_EXP', {}))
x = float(ac.get_editor_property('SHM224_JRMode')); out['abp']['SHM224_JRMode'] = x
if abs(x - EXP['SHM224_JRMode']) > 1e-4: bad.append('abp.SHM224_JRMode')
for m, nm in (('SHM224_DB_JRFwd', 'PSD_SHM224_JogRevFwdO'), ('SHM224_DB_JRBwd', 'PSD_SHM224_JogRevBwdO'), ('SHM224_DB_JRLat', 'PSD_SHM224_JogRevLat'), ('SHM224_DB_JRFwdM', 'PSD_SHM224_JogRevFwdM'), ('SHM224_DB_JRBwdM', 'PSD_SHM224_JogRevBwdM')):
    v = ac.get_editor_property(m); out['abp'][m] = v.get_name() if v else None
    if not v or v.get_name() != nm: bad.append('abp.' + m)
fol = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateCameraV21'))]
if not any('SetCamFolYawK' in t for t in fol): bad.append('comp.folyaw')
for nm_ in ('SetSHM224_RevIntent', 'SetSHM224_EarlyRev', 'SetSHM224_RevMir'):
    if not any(nm_ in t for t in mtn): bad.append('monttick.' + nm_)
umm = [tid(pn(n)) for n in B.find_nodes(graph(abp, 'Update_MotionMatching'))]
if not any(t.endswith('|GetSHM224_EarlyRev') for t in umm): bad.append('bridge.earlyrev')
egn = [tid(pn(n)) for n in B.find_nodes(graph(abp, 'EventGraph'))]
if not any('SetSHM_RedirectDB_JR' in t for t in egn): bad.append('eventgraph.jrdb')
snn = [tid(pn(n)) for n in B.find_nodes(graph(abp, 'SHM_Snapshot'))]
if not any('SetSHM224_LiftL' in t for t in snn): bad.append('snapshot.lift')
fik = [n for n in B.find_nodes(graph(abp, 'FeetIK_Layer')) if n.get_class().get_name() == 'AnimGraphNode_ModifyBone' and 'ik_foot_l' in n.get_editor_property('node').export_text()]
if not fik: bad.append('feetik.lift')
for k in ('RedirectSpeedDecay', 'SwingLiftEnabled', 'CamFolYawFade'):
    xv = sda.get_editor_property(k); out['shm'][k] = xv
    if (bool(xv) != EXP[k]) if isinstance(EXP[k], bool) else abs(float(xv) - EXP[k]) > 1e-4: bad.append('shm.' + k)
comp_fn = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateBodyTargets'))]
if not any('SetSwingLiftL' in t for t in comp_fn): bad.append('comp.swinglift')
comp_rt = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateRouting'))]
if not any('SetSpeedOnset' in t for t in comp_rt): bad.append('comp.speedonset')
V4 = '/Game/GraceRanger/SHME/Animations/V224/'
for dbn, want in ((V4 + 'PSD_SHM224_JogRevFwdO', {'A_CP2_Jog_Fwd_Pivot'}), (V4 + 'PSD_SHM224_JogRevBwdO', {'SHM_DPP_Jog_Bwd_Pivot'}), (V4 + 'PSD_SHM224_JogRevLat', {'A_CP2_Jog_Left_Pivot', 'A_CP2_Jog_Right_Pivot'}), (V4 + 'PSD_SHM224_JogRevFwdM', {'SHM224_Jog_Fwd_Pivot_M'}), (V4 + 'PSD_SHM224_JogRevBwdM', {'SHM224_Jog_Bwd_Pivot_M'})):
    d_ = u.load_asset(dbn)
    if not d_: bad.append('missing.' + dbn.rsplit('/', 1)[-1]); continue
    ents = set(d_.get_animation_asset(i).get_name() for i in range(d_.get_num_animation_assets()))
    piv = [e for e in ents if 'Pivot' in e]
    if not want <= ents or (not dbn.endswith('Lat') and len(piv) != 1): bad.append('db.' + dbn.rsplit('/', 1)[-1])
    out.setdefault('db224', {})[dbn.rsplit('/', 1)[-1]] = ents
# no V2.24 clip may leak into a production database
for dbn in ('/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogPivots', '/Game/GraceRanger/SHME/Animations/Redirect/PSD_SHM_Redirect_JogReversalQ', '/Game/GraceRanger/SHME/Animations/Redirect/PSD_SHM_Redirect_JogReversal', '/Game/GraceRanger/SHME/Animations/Redirect/PSD_SHM_Redirect_JogLateral', '/Game/GraceRanger/Animations/LocomotionBehavior/RearRevision/PSD_RB_Jog_Rear'):
    d_ = u.load_asset(dbn)
    if not d_: continue
    ents = [d_.get_animation_asset(i).get_name() for i in range(d_.get_num_animation_assets())]
    if any(e.startswith('SHM224_') for e in ents): bad.append('db_leak224.' + dbn.rsplit('/', 1)[-1])

# ---- V2.25
EXP5 = dict({'Reversal': True, 'StepPrepEnabled': True, 'CamInspectEnabled': True}, **getattr(_b, 'V225_EXP', {}))
want_bwd = 'PSD_SHM225_JogRevBwd' if EXP5['Reversal'] else 'PSD_SHM224_JogRevBwdO'; want_fwd = 'PSD_SHM225_JogRevFwd' if EXP5['Reversal'] else 'PSD_SHM224_JogRevFwdO'
for m, nm in (('SHM224_DB_JRBwd', want_bwd), ('SHM224_DB_JRBwdM', want_bwd if EXP5['Reversal'] else 'PSD_SHM224_JogRevBwdM'), ('SHM224_DB_JRFwd', want_fwd), ('SHM224_DB_JRFwdM', want_fwd if EXP5['Reversal'] else 'PSD_SHM224_JogRevFwdM')):
    v = ac.get_editor_property(m); out['abp'][m + '_225'] = v.get_name() if v else None
    if not v or v.get_name() != nm: bad.append('abp225.' + m)
for k in ('StepPrepEnabled', 'CamInspectEnabled'):
    xv = sda.get_editor_property(k); out['shm'][k] = xv
    if bool(xv) != EXP5[k]: bad.append('shm.' + k)
snn5 = [tid(pn(n)) for n in B.find_nodes(graph(abp, 'SHM_Snapshot'))]
if not any('SetSHM225_LookAlpha' in t for t in snn5): bad.append('snapshot.lookalpha')
ag5 = [n for n in B.find_nodes(graph(abp, 'AnimGraph')) if n.get_class().get_name() == 'AnimGraphNode_LookAt']
out['abp']['lookat_nodes'] = len(ag5)
if len(ag5) != 3: bad.append('animgraph.lookat')
bt5 = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateBodyTargets'))]
if not any('SetStepPrepZ' in t for t in bt5): bad.append('comp.stepprep')
if not any('SetSwingPathMaxL' in t for t in bt5): bad.append('comp.swingpath')
cv5 = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateCameraV21'))]
if not any('SetInspectOn' in t for t in cv5): bad.append('comp.inspect')
V5 = '/Game/GraceRanger/SHME/Animations/V225/'
for dbn, fam in ((V5 + 'PSD_SHM225_JogRevBwd', 'B_F'), (V5 + 'PSD_SHM225_JogRevFwd', 'F_B')):
    d_ = u.load_asset(dbn)
    if not d_: bad.append('missing.' + dbn.rsplit('/', 1)[-1]); continue
    ents = [d_.get_animation_asset(i).get_name() for i in range(d_.get_num_animation_assets())]
    piv = [e for e in ents if 'JogRev_' + fam in e]
    if len(piv) != 8 or any('Pivot' in e for e in ents) or 'A_RB_Jog_Rear' not in ents: bad.append('db225.' + dbn.rsplit('/', 1)[-1])
    out.setdefault('db225', {})[dbn.rsplit('/', 1)[-1]] = len(ents)
for dbn in ('/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogPivots', '/Game/GraceRanger/SHME/Animations/Redirect/PSD_SHM_Redirect_JogReversalQ', '/Game/GraceRanger/Animations/LocomotionBehavior/RearRevision/PSD_RB_Jog_Rear', '/Game/GraceRanger/Animations/Continuity/PSD_CT_Jog', '/Game/GraceRanger/SHME/Animations/V224/PSD_SHM224_JogRevBwdO', '/Game/GraceRanger/SHME/Animations/V224/PSD_SHM224_JogRevFwdO'):
    d_ = u.load_asset(dbn)
    if not d_: continue
    ents = [d_.get_animation_asset(i).get_name() for i in range(d_.get_num_animation_assets())]
    if any(e.startswith('SHM225_') for e in ents): bad.append('db_leak225.' + dbn.rsplit('/', 1)[-1])
# ---- V2.26
EXP6 = dict({'Reversal226': False, 'StepEdgeOn': False, 'InspectZoomOn': False, 'Probes': True}, **getattr(_b, 'V226_EXP', {}))
want6b = 'PSD_SHM226_JogRevBwd' if EXP6['Reversal226'] else want_bwd; want6f = 'PSD_SHM226_JogRevFwd' if EXP6['Reversal226'] else want_fwd
for m, nm in (('SHM224_DB_JRBwd', want6b), ('SHM224_DB_JRFwd', want6f)):
    v = ac.get_editor_property(m); out['abp'][m + '_226'] = v.get_name() if v else None
    if not v or v.get_name() != nm: bad.append('abp226.' + m)
for k in ('StepEdgeOn', 'InspectZoomOn'):
    try: xv = sda.get_editor_property(k); out['shm'][k] = xv
    except Exception: xv = None; bad.append('shm226.missing.' + k)
    if xv is not None and bool(xv) != EXP6[k]: bad.append('shm226.' + k)
try: out['shm']['InspectTag'] = str(sda.get_editor_property('InspectTag')); out['shm']['InspectJump'] = sda.get_editor_property('InspectJump')
except Exception: bad.append('shm226.inspecttag')
if out['shm'].get('InspectTag') != 'GR_Inspect': bad.append('shm226.inspecttag.value')
out['shm']['SwingLiftMargin'] = sda.get_editor_property('SwingLiftMargin')
if 'SwingLiftMargin' in EXP6 and abs(float(out['shm']['SwingLiftMargin']) - float(EXP6['SwingLiftMargin'])) > 1e-4: bad.append('shm226.swingliftmargin')
snn6 = [tid(pn(n)) for n in B.find_nodes(graph(abp, 'SHM_Snapshot'))]
if not any('SetSHM226_ShiftL' in t for t in snn6): bad.append('snapshot.shift')
fk6 = [n for n in B.find_nodes(graph(abp, 'FeetIK_Layer')) if n.get_class().get_name() == 'AnimGraphNode_ModifyBone' and 'BCS_WorldSpace' in n.get_editor_property('node').export_text()]
out['abp']['shift_nodes'] = len(fk6)
if len(fk6) != 2: bad.append('feetik.shift')
bt6 = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateBodyTargets'))]
if not any('SetSwingShiftL' in t for t in bt6): bad.append('comp.swingshift')
cv6 = [tid(pn(n)) for n in B.find_nodes(graph(comp, 'SHM_UpdateCameraV21'))]
if not any('ActorHasTag' in t for t in cv6) or not any('GetActorBounds' in t for t in cv6): bad.append('comp.inspect.contract')
if not any('SetInspectHitName' in t for t in cv6): bad.append('comp.inspect.telemetry')
V6 = '/Game/GraceRanger/SHME/Animations/V226/'
for dbn, fam in ((V6 + 'PSD_SHM226_JogRevBwd', 'B_F'), (V6 + 'PSD_SHM226_JogRevFwd', 'F_B')):
    d_ = u.load_asset(dbn)
    if not d_: bad.append('missing.' + dbn.rsplit('/', 1)[-1]); continue
    ents = [d_.get_animation_asset(i).get_name() for i in range(d_.get_num_animation_assets())]
    piv = [e for e in ents if 'JogRev_' + fam in e]
    if len(piv) != 32 or any('Pivot' in e for e in ents) or 'A_RB_Jog_Rear' not in ents: bad.append('db226.' + dbn.rsplit('/', 1)[-1])
    out.setdefault('db226', {})[dbn.rsplit('/', 1)[-1]] = len(ents)
    s0 = u.load_asset(V6 + 'SHM226_JogRev_%s_P0' % fam)
    cur = [str(c) for c in u.AnimationLibrary.get_animation_curve_names(s0, u.RawCurveTrackTypes.RCT_FLOAT)] if s0 else []
    out.setdefault('curves226', {})[fam] = cur
    if 'footspeed_l' not in cur or 'footspeed_r' not in cur: bad.append('curves226.' + fam)
for dbn in ('/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogPivots', '/Game/GraceRanger/SHME/Animations/Redirect/PSD_SHM_Redirect_JogReversalQ', '/Game/GraceRanger/SHME/Animations/V224/PSD_SHM224_JogRevBwdO', '/Game/GraceRanger/SHME/Animations/V225/PSD_SHM225_JogRevBwd'):
    d_ = u.load_asset(dbn)
    if not d_: continue
    ents = [d_.get_animation_asset(i).get_name() for i in range(d_.get_num_animation_assets())]
    if any(e.startswith('SHM226_') for e in ents): bad.append('db_leak226.' + dbn.rsplit('/', 1)[-1])
try:   # house targets: tag + query probe on the four R05 masks (editor world)
    acts = {a.get_actor_label(): a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()}
    masks = {}
    for nm in ('R05_Workshop_Mask_Silent', 'R05_Workshop_Mask_Gilded', 'R05_Workshop_Mask_Cerulean', 'R05_Workshop_Mask_Cracked'):
        a = acts.get(nm)
        if not a: masks[nm] = 'missing'; bad.append('mask.missing.' + nm); continue
        probes = [c for c in a.get_components_by_class(u.SphereComponent) if 'GR_Inspect' in [str(t) for t in c.component_tags]]
        masks[nm] = {'tag': 'GR_Inspect' in [str(t) for t in a.tags], 'probes': len(probes)}
        if not masks[nm]['tag']: bad.append('mask.tag.' + nm)
        if EXP6['Probes'] and len(probes) != 1: bad.append('mask.probe.' + nm)
    out['masks'] = masks
except Exception as e: out['masks'] = 'ERR ' + str(e)[:100]
if out['pie'] or out['dirty']: bad.append('pie_or_dirty')
out['bad'] = bad
print('VERIFY226 ' + json.dumps(out, default=str))
print('ALL_OK' if not bad else 'NOT_OK ' + ','.join(bad))
