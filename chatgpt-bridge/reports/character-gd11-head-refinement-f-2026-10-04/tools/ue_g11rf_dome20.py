"""refinement F: enlarge the transient QA studio dome (LKQA_Backdrop sphere, radius ~20 m) to ~35 m so a 20 m groom-LOD shot is taken from INSIDE
the studio. The dome is respawned by ue_lk_qa_setup.py on every setup; the level is not saved."""
import unreal as u, json
out = {}
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    if a.get_actor_label() in ('LKQA_Backdrop', 'LKQA_Floor'):
        s = 70.0 if a.get_actor_label() == 'LKQA_Backdrop' else 80.0; sc = a.get_actor_scale3d(); a.set_actor_scale3d(u.Vector(s, s, sc.z if a.get_actor_label() == 'LKQA_Floor' else s)); out[a.get_actor_label()] = str(a.get_actor_scale3d())
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('DOME20', json.dumps(out))
