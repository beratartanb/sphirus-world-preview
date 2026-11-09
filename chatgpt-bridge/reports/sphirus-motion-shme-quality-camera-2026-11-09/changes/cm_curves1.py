# cm_curves1.py (write): true "played clip" telemetry. Neither the fresh-search probe nor the pose-library nearest
# neighbour tells which clip the Motion Matching blend stack really plays (steady poses match many clips), and the node's
# OnUpdate binding is not reachable from Python. Classic solution: every project clip copy gets two float curves,
#   SphClip = constant clip id (Saved/Codex/Day_20261107/clipids.json), SphTime = clip time (key every 0.1 s, linear),
# so the driver anim instance's GetCurveValue gives the played clip + time per frame (non-integer SphClip = blend).
# Vendor originals untouched; only /Game/Sphirus/Player/Anim/Core/ copies change. Curves are not schema features.
import unreal as u, json
AL=u.AnimationLibrary; EA=u.EditorAssetLibrary; C='/Game/Sphirus/Player/Anim/Core/'
ids=json.load(open(u.Paths.project_dir()+'Saved/Codex/Day_20261107/clipids.json')); n=0; miss=[]
for name,cid in ids.items():
    a=u.load_asset(C+name)
    if not a: miss.append(name); continue
    L=float(a.get_play_length())
    for cn in ('SphClip','SphTime'):
        if AL.does_curve_exist(a,cn,u.RawCurveTrackTypes.RCT_FLOAT): AL.remove_curve(a,cn,False)
        AL.add_curve(a,cn,u.RawCurveTrackTypes.RCT_FLOAT,False)
    AL.add_float_curve_keys(a,'SphClip',[0.0,L],[float(cid),float(cid)])
    ts=[round(i*0.1,3) for i in range(int(L/0.1)+1)]+[L]; AL.add_float_curve_keys(a,'SphTime',ts,ts)
    assert EA.save_loaded_asset(a,False); n+=1
print('CURVED',n,'MISSING',miss); print('DONE')
