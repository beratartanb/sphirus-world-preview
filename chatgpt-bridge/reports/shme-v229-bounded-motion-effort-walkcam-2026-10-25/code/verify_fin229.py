"""verify_fin229.py (fresh editor, read-only): V2.28 production verify (all five groups) + V2.29 expectations (builtins.V229_EXP groups
camera / effort / resume) + the RevTurn content check (no chest-vs-pelvis twist jump > 30 deg/frame in the four SHM216_RevTurn clips).
Prints VERIFY229 {... ALL_OK}."""
import builtins, json, math, sys, pathlib
X = dict(getattr(builtins, 'V229_EXP', {}))
builtins.V228_EXP = {'motion': True, 'cancel': True, 'terrain': True, 'stepedge': True, 'inspect': True}
g = {'__name__': 'v228'}
exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V228_20261025/req/verify_fin228.py', encoding='utf8').read(), g)
import unreal as u
bad = list(g['bad']) + ['curve:' + m for m in g['miss']] + ['v226:' + b for b in g['v226_rest']]
sda = u.load_asset('/Game/GraceRanger/SHME/DA_SHM_Response_Default')
cam = {k: float(sda.get_editor_property(k)) for k in ('CamSwapMinSpeed', 'CamFolDZLatWalk', 'CamFolDZFwdWalk')}
want = (230.0, 3.0, 4.0) if X.get('camera') else (60.0, 12.0, 10.0)
for (k, v), w in zip(cam.items(), want):
    if abs(v - w) > 1e-4: bad.append('%s=%s' % (k, v))
ef = bool(sda.get_editor_property('EffortEnabled'))
if ef != bool(X.get('effort')): bad.append('EffortEnabled=%s' % ef)
esm = float(sda.get_editor_property('EffortScaleMin'))
if 'effort_min' in X and abs(esm - float(X['effort_min'])) > 1e-4: bad.append('EffortScaleMin=%s' % esm)
bp = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'); cdo = u.get_default_object(bp.generated_class())
rw = float(cdo.get_editor_property('SHM229_ResumeWin'))
if abs(rw - (0.2 if X.get('resume') else 0.0)) > 1e-6: bad.append('SHM229_ResumeWin=%s' % rw)
pc = float(cdo.get_editor_property('SHM229_PushCancel'))
if abs(pc - (1.0 if X.get('pushcancel') else 0.0)) > 1e-6: bad.append('SHM229_PushCancel=%s' % pc)
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae
spin = {}
for c in ('L_Lfoot', 'L_Rfoot', 'R_Lfoot', 'R_Rfoot'):
    seq = u.load_asset('/Game/GraceRanger/SHME/Animations/V216/SHM216_RevTurn_' + c); n = ae.num_frames(seq); clip = ae.Clip(seq, ['root', 'pelvis', 'spine_05'])
    def yaw(q): f = ae.qrot(q, (0.0, 1.0, 0.0)); return math.degrees(math.atan2(f[1], f[0]))
    tw = [(yaw(clip.comp('spine_05', f)[1]) - yaw(clip.comp('pelvis', f)[1]) + 180.0) % 360.0 - 180.0 for f in range(n)]
    j = max(abs((tw[k] - tw[k - 1] + 180.0) % 360.0 - 180.0) for k in range(1, n)); spin[c] = round(j, 1)
    if j > 30: bad.append('spin %s %.0f' % (c, j))
print('VERIFY229 ' + json.dumps({'cam': cam, 'effort': ef, 'effort_min': esm, 'resume': rw, 'pushcancel': pc, 'revturn_max_twist_jump': spin, 'bad': bad, 'ALL_OK': not bad}))
