"""schema239.py (editor job, write manifest: new PSS_SHM239_Takeover + the takeover databases) - V2.39: the takeover databases search with
their OWN schema = PSS_Default (AAMS, unchanged) duplicated, trajectory channel weight SHM239 traj_w (0.15; pose group unchanged).
Measured (v239f_j39_rl_tk / rw_tk): on the takeover touchdown MM entered SHM239_Tk_R_P21_K3_Opp at 1.07 s / K1_Back 0.20 -> K3_Back 0.57
instead of the frame 0 of the takeover that starts AT this touchdown: features are root-relative, so a mid-run frame late in another
takeover clip (already heading to the new side) matches the running pose and the CMC-predicted turn better than the exact braking frame 0
(its future brakes first). Short BranchIn windows cannot constrain the entry (V2.25 entry-window trap) - the weight can.
builtins.V239_PSS = {'dry': bool, 'traj_w': 0.15, 'dbs': [...]}. Prints PSS239 {...}."""
import unreal as u, json, builtins
EAL = u.EditorAssetLibrary
c = dict(getattr(builtins, 'V239_PSS', {})); DRY = bool(c.get('dry', True)); W = float(c.get('traj_w', 0.15))
SRC = '/Game/AAMS/AAMS/Animations/Locomotion/MotionMatchingData/Schemas/PSS_Default'; DST = '/Game/GraceRanger/SHME/Animations/V239/PSS_SHM239_Takeover'
out = {'dry': DRY}
if not DRY:
    s = u.load_asset(DST) if EAL.does_asset_exist(DST) else EAL.duplicate_asset(SRC, DST); assert s
    ch = [x for x in s.get_editor_property('channels') if 'Trajectory' in x.get_class().get_name()]; assert len(ch) == 1
    ch[0].set_editor_property('weight', W); assert EAL.save_asset(DST, False)
    for d in c.get('dbs', []):
        db = u.load_asset(d); db.set_editor_property('schema', s); assert EAL.save_asset(d, False), d
    out['schema_traj_w'] = float([x for x in u.load_asset(DST).get_editor_property('channels') if 'Trajectory' in x.get_class().get_name()][0].get_editor_property('weight'))
    out['db_schemas'] = {d.rsplit('/', 1)[-1]: u.load_asset(d).get_editor_property('schema').get_name() for d in c.get('dbs', [])}
    out['src_traj_w'] = float([x for x in u.load_asset(SRC).get_editor_property('channels') if 'Trajectory' in x.get_class().get_name()][0].get_editor_property('weight'))
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('PSS239 ' + json.dumps(out, default=str))
