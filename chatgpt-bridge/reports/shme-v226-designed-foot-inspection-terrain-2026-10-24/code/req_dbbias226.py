"""dbbias226.py (editor job): the exit of the authored reversal - MM leaves the SHM226 clip at ~1.0 s of 1.97 s for the loop at another
foot phase (24 cm planted-foot jump). Sets continuing_pose_cost_bias on the two V2.26 databases only (builtins.V226_CPB; None = print only).
Prints DBBIAS226 {before, after, saved}."""
import unreal as u, json, builtins
V = '/Game/GraceRanger/SHME/Animations/V226/'; CPB = getattr(builtins, 'V226_CPB', None)
out = {'before': {}, 'after': {}, 'cpb': CPB}
for p in (V + 'PSD_SHM226_JogRevBwd', V + 'PSD_SHM226_JogRevFwd', '/Game/GraceRanger/Animations/CorePerformance/PSD_CP2_JogPivots', '/Game/GraceRanger/SHME/Animations/V224/PSD_SHM224_JogRevBwdO'):
    db = u.load_asset(p)
    if not db: out['before'][p.rsplit('/', 1)[-1]] = 'missing'; continue
    rec = {}
    for k in ('base_cost_bias', 'continuing_pose_cost_bias', 'looping_cost_bias'):
        try: rec[k] = db.get_editor_property(k)
        except Exception as e: rec[k] = 'ERR ' + str(e)[:60]
    out['before'][p.rsplit('/', 1)[-1]] = rec
    if CPB is not None and 'PSD_SHM226_' in p:
        db.set_editor_property('continuing_pose_cost_bias', float(CPB))
        out['after'][p.rsplit('/', 1)[-1]] = {'continuing_pose_cost_bias': db.get_editor_property('continuing_pose_cost_bias'), 'saved': bool(u.EditorAssetLibrary.save_asset(p, False))}
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('DBBIAS226 ' + json.dumps(out, default=str))
