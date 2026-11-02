"""set249_t2bias.py (editor job, write manifest = PSD_SHM248_JogStartT2_L / _R): keep Motion Matching on the turning-start clip it chose.
Measured (v249l60 jstart, -180 request): with the turn 6 deg from complete MM switched mid-clip from the TurnR180 crop to a later frame of
the TurnR135 crop and then to the CP2 start (pose jump, shoulder 69 m/s2). continuing_pose_cost_bias of both T2 databases := BIAS
(negative = prefer the continuing pose; the source V2.37 start databases' value is reported). builtins.V249_BIAS (default -0.5).
Prints T2BIAS249 {...}."""
import unreal as u, json, builtins
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
B_ = float(getattr(builtins, 'V249_BIAS', -0.5)); out = {'bias': B_}
for s in ('L', 'R'):
    p = '/Game/GraceRanger/SHME/Animations/V248/PSD_SHM248_JogStartT2_' + s; db = u.load_asset(p)
    before = db.get_editor_property('continuing_pose_cost_bias'); db.set_editor_property('continuing_pose_cost_bias', B_)
    assert u.EditorAssetLibrary.save_asset(p, False); out[s] = [before, db.get_editor_property('continuing_pose_cost_bias')]
out['dirty'] = [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('T2BIAS249 ' + json.dumps(out, default=str))
