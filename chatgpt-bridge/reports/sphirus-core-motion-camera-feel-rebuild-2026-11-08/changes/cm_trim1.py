# cm_trim1.py (write): apply trim_plan.json (from q_trim.py) to the gait-database BranchIn notify states so that start
# clips only offer their acceleration, stop clips only their deceleration and idle turns only the turning part. The
# motion-matching search then has to use the loops for steady travel instead of flipping between start/stop clips
# (probe: 5-8 clip switches per second while walking straight, Walk_Fwd loop almost never chosen). PSD_Sph_Loco2
# (legacy comparison) keeps its own full-range BranchIn track and is not touched.
import unreal as u, json
EA=u.EditorAssetLibrary; AL=u.AnimationLibrary; C='/Game/Sphirus/Player/Anim/Core/'; D='/Game/Sphirus/Player/MM/'
plan=json.load(open(u.Paths.project_dir()+'Saved/Codex/Day_20261107/trim_plan.json'))
def dbof(n):
    if 'Jog' in n: return 'Jog'
    if 'Run' in n: return 'Run'
    return 'Walk'
n_ok=0
for n,p in plan.items():
    if not p.get('range'): continue
    s,e=p['range']; a=u.load_asset(C+n); assert a,n; g=dbof(n); tr='SphDB_'+g; db=u.load_asset(D+'PSD_Sph_'+g); assert db
    if tr in [str(t) for t in AL.get_animation_notify_track_names(a)]: AL.remove_animation_notify_track(a,tr)
    AL.add_animation_notify_track(a,tr); st=AL.add_animation_notify_state_event(a,tr,float(s),float(e-s),u.AnimNotifyState_PoseSearchBranchIn); st.set_editor_property('database',db)
    assert EA.save_loaded_asset(a,False); n_ok+=1; print('TRIM',n,g,s,e,'of',p['len'])
for g in ('Walk','Jog','Run'):
    db=u.load_asset(D+'PSD_Sph_'+g); print('DB',g,db.get_num_animation_assets())
print('DONE',n_ok)
