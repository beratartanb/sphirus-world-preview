"""schema240_edb.py (editor job, write manifest = the 96 entry databases) - V2.40: the per-(source, target) entry databases search with
PSS_SHM239_Takeover (PSS_Default duplicate, trajectory weight 0.15). Measured (v240c120_j38_cc90_tk): request at cut time 0.79 (contact K3
ahead, its prefix frame identical to the playing cut) - MM entered K1 at 0.43 (after K1's divergence, a future that already turns back):
inside ONE source's database the trajectory channel (weight 1.0) still beat the exact pose. With same-source, identical-prefix content
the pose must decide. Prints SCH240 {...}."""
import unreal as u, json
EAL = u.EditorAssetLibrary
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
s = u.load_asset('/Game/GraceRanger/SHME/Animations/V239/PSS_SHM239_Takeover'); assert s
tw = float([x for x in s.get_editor_property('channels') if 'Trajectory' in x.get_class().get_name()][0].get_editor_property('weight'))
out = {'traj_w': tw, 'set': 0, 'errors': []}
for e in range(96):
    p = '/Game/GraceRanger/SHME/Animations/V240/PSD_SHM240_E%02d' % e
    try:
        d = u.load_asset(p); d.set_editor_property('schema', s); assert EAL.save_asset(p, False); out['set'] += 1
    except Exception as ex: out['errors'].append('%d %s' % (e, str(ex)[:100]))
out['ok'] = out['set'] == 96 and not out['errors']
print('SCH240 ' + json.dumps(out))
