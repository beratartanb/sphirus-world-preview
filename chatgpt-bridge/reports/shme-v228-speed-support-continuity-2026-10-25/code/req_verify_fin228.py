"""verify_fin228.py: V2.26 production verify with the V2.28 expectation. builtins.V228_EXP = dict(motion, cancel, terrain, stepedge, inspect) booleans.
Checks the ABP knobs, the GR profile DA knob, the SHME DA knobs, the 64 clips' three curves (Rev / V / W) and the V2.26 verify. Prints VERIFY228 {... ALL_OK}."""
import builtins, json
X = dict(getattr(builtins, 'V228_EXP', {}))
builtins.V225_EXP = {'Reversal': False, 'StepPrepEnabled': False, 'CamInspectEnabled': True}
builtins.V226_EXP = {'Reversal226': bool(X.get('motion')), 'StepEdgeOn': bool(X.get('stepedge')), 'InspectZoomOn': False, 'Probes': True, 'SwingLiftMargin': 6.0}
g = {'__name__': 'v226'}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/verify_prod226.py', encoding='utf8').read(), g)
import unreal as u
bp = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'); cdo = u.get_default_object(bp.generated_class())
names = ('SHM227_RevHold', 'SHM227_FPOff', 'SHM227_HoldExit', 'SHM227_FlatMax', 'SHM227_ThrottleT', 'SHM228_ClipSpeed', 'SHM228_LeadFrames', 'SHM228_RelHold', 'SHM228_CancelOn')
kn = {k: float(cdo.get_editor_property(k)) for k in names}
want = {'SHM227_RevHold': 1.0 if X.get('motion') else 0.0, 'SHM227_FPOff': 0.0, 'SHM227_HoldExit': 0.25, 'SHM227_FlatMax': 6.0, 'SHM227_ThrottleT': 2.5,
        'SHM228_ClipSpeed': 1.0 if X.get('motion') else 0.0, 'SHM228_LeadFrames': 1.0, 'SHM228_RelHold': 1.0 if X.get('cancel') else 0.0, 'SHM228_CancelOn': 1.0 if X.get('cancel') else 0.0}
bad = [k for k, v in want.items() if abs(kn[k] - v) > 1e-6]
da = u.load_asset('/Game/GraceRanger/Profiles/DA_GR_LocomotionBehavior'); gr = float(da.get_editor_property('GR228_ClipSpeed'))
if abs(gr - (1.0 if X.get('motion') else 0.0)) > 1e-6: bad.append('GR228_ClipSpeed=%s' % gr)
sda = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default')
sd = {k: sda.get_editor_property(k) for k in ('SwingLiftMax', 'StepEdgeOn', 'StepEdgeShift', 'InspectIdOn', 'InspectFocusMode', 'InspectJump', 'InspectRadius', 'InspectZoomOn', 'StepEdgeShort', 'InspectSwitchOn')}
if abs(float(sd['SwingLiftMax']) - (36.0 if X.get('terrain') else 25.0)) > 1e-6: bad.append('SwingLiftMax=%s' % sd['SwingLiftMax'])
if abs(float(sd['InspectIdOn']) - (1.0 if X.get('inspect') else 0.0)) > 1e-6: bad.append('InspectIdOn=%s' % sd['InspectIdOn'])
if abs(float(sd['InspectFocusMode']) - (1.0 if X.get('inspect') else 0.0)) > 1e-6: bad.append('InspectFocusMode=%s' % sd['InspectFocusMode'])
if X.get('stepedge') and abs(float(sd['StepEdgeShift']) - 18.0) > 1e-6: bad.append('StepEdgeShift=%s' % sd['StepEdgeShift'])
AL = u.AnimationLibrary; miss = []
for f in ('B_F', 'F_B'):
    for k in range(32):
        s = u.load_asset('/Game/GraceRanger/SHME/Animations/V226/SHM226_JogRev_%s_P%d' % (f, k))
        for c in ('SHM226_Rev', 'SHM226_V', 'SHM226_W'):
            if not s or not AL.does_curve_exist(s, c, u.RawCurveTrackTypes.RCT_FLOAT): miss.append('%s_P%d:%s' % (f, k, c))
# the V2.26 verify has no expectation for the 32-bin databases in production (its 'abp' / 'abp225' DB-ref checks assume the V2.24 pivot
# or V2.25 clips): with the motion group promoted those eight keys are checked HERE instead (the four ABP DB refs must be the PSD_SHM226 pair)
v226_bad = list(g['out'].get('bad', [])) if isinstance(g.get('out'), dict) else ['n/a']
DBKEYS = {'abp.SHM224_DB_JRFwd', 'abp.SHM224_DB_JRBwd', 'abp.SHM224_DB_JRFwdM', 'abp.SHM224_DB_JRBwdM', 'abp225.SHM224_DB_JRBwd', 'abp225.SHM224_DB_JRBwdM', 'abp225.SHM224_DB_JRFwd', 'abp225.SHM224_DB_JRFwdM'}
if X.get('motion'):
    v226_rest = [b for b in v226_bad if b not in DBKEYS]
    dbs = {k: cdo.get_editor_property(k).get_name() for k in ('SHM224_DB_JRBwd', 'SHM224_DB_JRBwdM', 'SHM224_DB_JRFwd', 'SHM224_DB_JRFwdM')}
    for k, v in dbs.items():
        want_db = 'PSD_SHM226_JogRevBwd' if 'Bwd' in k else 'PSD_SHM226_JogRevFwd'
        if v != want_db: bad.append('%s=%s' % (k, v))
else:
    v226_rest = v226_bad; dbs = {}
print('VERIFY228 ' + json.dumps({'abp': kn, 'gr228': gr, 'shm': {k: str(v) for k, v in sd.items()}, 'dbs': dbs, 'bad': bad, 'curve_missing': miss[:5], 'v226_bad_rest': v226_rest, 'ALL_OK': (not bad and not miss and isinstance(g.get('out'), dict) and not v226_rest)}, default=str))
