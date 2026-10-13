"""GD45: destroy the stray transient BP_PBI_Player actor left in the editor world by a crashed audit job (at z -100000); report map dirty state (the map is NOT saved by this job)."""
import unreal as u, json
gen = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player').generated_class(); out = {'destroyed': [], 'kept': []}
for act in u.EditorLevelLibrary.get_all_level_actors():
    if act.get_class() == gen:
        loc = act.get_actor_location()
        if loc.z < -50000: act.destroy_actor(); out['destroyed'].append(act.get_name())
        else: out['kept'].append([act.get_name(), round(loc.z, 1)])
w = u.EditorLevelLibrary.get_editor_world(); out['world'] = w.get_path_name()
try: out['map_dirty'] = w.get_outermost().is_dirty()
except Exception as e: out['map_dirty'] = 'ERR ' + str(e)[:60]
out['dirty_packages'] = [str(p.get_path_name()) for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()][:10]
try: out['dirty_maps'] = [str(p.get_path_name()) for p in u.EditorLoadingAndSavingUtils.get_dirty_map_packages()][:10]
except Exception as e: out['dirty_maps'] = 'ERR ' + str(e)[:60]
print('GD45_CLEANUP', json.dumps(out), flush=True)
