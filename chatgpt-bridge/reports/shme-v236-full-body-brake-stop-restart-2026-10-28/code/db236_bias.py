"""db236_bias.py (editor job): set continuing_pose_cost_bias on a V2.36 candidate database (builtins.V236_BIAS = {'db': path, 'bias': x}).
Prints BIAS236 {...}."""
import unreal as u, json, builtins
c = builtins.V236_BIAS; db = u.load_asset(c['db']); old = db.get_editor_property('continuing_pose_cost_bias')
db.set_editor_property('continuing_pose_cost_bias', float(c['bias'])); ok = u.EditorAssetLibrary.save_asset(c['db'], False)
print('BIAS236 ' + json.dumps({'db': c['db'], 'old': old, 'new': db.get_editor_property('continuing_pose_cost_bias'), 'saved': ok}))
