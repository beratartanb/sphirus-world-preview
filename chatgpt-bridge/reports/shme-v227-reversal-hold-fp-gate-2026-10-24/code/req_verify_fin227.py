"""verify_fin227.py: V2.26 production verify with the V2.27 expectation (Reversal226 = builtins.V227_EXP_REV, default True) + the ABP knobs."""
import builtins, json
REV = bool(getattr(builtins, 'V227_EXP_REV', True))
builtins.V225_EXP = {'Reversal': False, 'StepPrepEnabled': False, 'CamInspectEnabled': True}
builtins.V226_EXP = {'Reversal226': REV, 'StepEdgeOn': False, 'InspectZoomOn': False, 'Probes': True, 'SwingLiftMargin': 6.0}
g = {'__name__': 'v226'}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V226_20261024/verify_prod226.py', encoding='utf8').read(), g)
import unreal as u
bp = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'); cdo = u.get_default_object(bp.generated_class())
kn = {k: float(cdo.get_editor_property(k)) for k in ('SHM227_RevHold', 'SHM227_FPOff', 'SHM227_HoldExit', 'SHM227_FlatMax', 'SHM227_ThrottleT')}
want = {'SHM227_RevHold': 1.0 if REV else 0.0, 'SHM227_FPOff': 1.0 if REV else 0.0, 'SHM227_HoldExit': 0.25, 'SHM227_FlatMax': 6.0, 'SHM227_ThrottleT': 2.5}
bad = [k for k, v in want.items() if abs(kn[k] - v) > 1e-6]
# clip curves: every SHM226 clip carries SHM226_Rev
AL = u.AnimationLibrary; miss = []
for f in ('B_F', 'F_B'):
    for k in range(32):
        s = u.load_asset('/Game/GraceRanger/SHME/Animations/V226/SHM226_JogRev_%s_P%d' % (f, k))
        if not s or not AL.does_curve_exist(s, 'SHM226_Rev', u.RawCurveTrackTypes.RCT_FLOAT): miss.append('%s_P%d' % (f, k))
print('VERIFY227 ' + json.dumps({'knobs': kn, 'knobs_bad': bad, 'curve_missing': miss, 'v226_bad': g['out'].get('bad') if isinstance(g.get('out'), dict) else 'n/a', 'ALL_OK': (not bad and not miss and isinstance(g.get('out'), dict) and not g['out'].get('bad'))}))
