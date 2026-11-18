# w_profile.py (write, gated runner + manifest): persistent locomotion profile + plant lock on the active player chain.
# Request: Saved/UE59Work/profile_req.json {"profile": "A"|"B"|"C", "plant": "LockRotation"|"PivotAroundBall"}
#  A = GASP Relaxed (SphRelaxed True, SphCM False, 165/375/585)      -- 2026-11-15 production
#  B = GASP Normal  (SphRelaxed False, SphCM False, 200,180,150 / 500,350,300 / 700)
#  C = Sphirus curated (SphRelaxed True, SphCM True, CM map Relaxed walk+run -> Dense walk+run, 180,170,150 / 430,350,300 / 585)
# Writes ABP_Sph_GASP, BP_Sph_GASPCharacter, BP_HybridA_Player (CDO values only, no graph edits). Previous values -> Saved/UE59Work/profile_prev_*.json
import unreal as u
L = u.BlueprintEditorLibrary; EA = u.EditorAssetLibrary
def errs(bp):   # 5.9: editor_toolset BlueprintTools is gone; use the blueprint status after compile (UpToDate / UpToDateWithWarnings)
    try: st = str(bp.get_editor_property('status'))
    except Exception as e: return []   # status not exposed: rely on the post-reopen check
    return [] if ('UP_TO_DATE' in st.upper() or 'UPTODATE' in st.upper()) else [st]
import json, time, builtins
PD = u.Paths.project_dir(); req = json.load(open(PD + 'Saved/UE59Work/profile_req.json'))
PR = req['profile']; PL = req.get('plant', 'LockRotation')
SPD = {'A': ((165,165,165),(375,375,375),(585,585,585)), 'B': ((200,180,150),(500,350,300),(700,700,700)), 'C': ((180,170,150),(430,350,300),(585,585,585))}[PR]
if req.get('run_speed'): SPD = (SPD[0], (int(req['run_speed']), SPD[1][1], SPD[1][2]), SPD[2])   # 2026-11-17: jog top speed override (415 keeps the run-stop database)
a = u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); cdo = u.get_default_object(a.generated_class())
g = u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); gcd = u.get_default_object(g.generated_class())
P_ = '/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'; bp = u.load_asset(P_); pc = u.get_default_object(bp.generated_class())
prev = {'SphRelaxed': cdo.get_editor_property('SphRelaxed'), 'SphCM': cdo.get_editor_property('SphCM'),
        'CM_Keys': [x.get_path_name() if x else None for x in cdo.get_editor_property('CM_Keys')], 'CM_Vals': [x.get_path_name() if x else None for x in cdo.get_editor_property('CM_Vals')],
        'PlantSettings_Default': cdo.get_editor_property('PlantSettings_Default').export_text(),
        'speeds_player': [str(pc.get_editor_property(k)) for k in ('WalkSpeeds','RunSpeeds','SprintSpeeds')], 'speeds_gasp': [str(gcd.get_editor_property(k)) for k in ('WalkSpeeds','RunSpeeds','SprintSpeeds')]}
json.dump(prev, open(PD + 'Saved/UE59Work/profile_prev_%s.json' % time.strftime('%Y%m%d_%H%M%S'), 'w'), indent=1)
cdo.set_editor_property('SphRelaxed', PR != 'B')
if PR == 'C':
    builtins.C_GAITS = ('Walk', 'Run'); builtins.C_FWD = int(req.get('fwd', 0)); exec(open(PD + 'Tools/UE59_20261116/cmap.py', encoding='utf8').read())
    ks = [u.load_asset(k) for k in builtins.SPH_MAP]; vs = [u.load_asset(v) for v in builtins.SPH_MAP.values()]; assert all(ks) and all(vs)
    cdo.set_editor_property('CM_Keys', ks); cdo.set_editor_property('CM_Vals', vs); cdo.set_editor_property('SphCM', True)
else:
    cdo.set_editor_property('SphCM', False)
ps = cdo.get_editor_property('PlantSettings_Default')
ps.set_editor_property('lock_type', u.FootPlacementLockType.LOCK_ROTATION if PL == 'LockRotation' else u.FootPlacementLockType.PIVOT_AROUND_BALL)
try: cdo.set_editor_property('PlantSettings_Default', ps)
except Exception as e: print('PLANT direct set refused, relying on struct reference:', str(e)[:120])
rb = cdo.get_editor_property('PlantSettings_Default').export_text(); print('PLANT readback', rb[:200]); assert ('LockType=%s' % PL) in rb
L.compile_blueprint(a); assert not errs(a)
rb2 = u.get_default_object(a.generated_class()).get_editor_property('PlantSettings_Default').export_text(); print('PLANT after compile', rb2[:120]); assert ('LockType=%s' % PL) in rb2
assert EA.save_loaded_asset(a, False)
for o, B_ in ((gcd, g), (pc, bp)):
    for k, v in zip(('WalkSpeeds','RunSpeeds','SprintSpeeds'), SPD): o.set_editor_property(k, u.Vector(*v))
    L.compile_blueprint(B_); e = errs(B_); print('ERR', B_.get_name(), e); assert not e; assert EA.save_loaded_asset(B_, False)
c2 = u.get_default_object(a.generated_class())
print('RESULT profile', PR, 'SphRelaxed', c2.get_editor_property('SphRelaxed'), 'SphCM', c2.get_editor_property('SphCM'), 'map', len(c2.get_editor_property('CM_Keys')),
      'speeds', [str(u.get_default_object(bp.generated_class()).get_editor_property(k)) for k in ('WalkSpeeds','RunSpeeds')])
print('DONE')
