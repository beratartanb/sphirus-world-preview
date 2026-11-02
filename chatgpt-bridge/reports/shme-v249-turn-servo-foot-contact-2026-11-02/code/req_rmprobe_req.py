"""rmprobe (measure): why RootMotionFromEverything yields zero root motion. Lists every anim-graph node (all graphs of the ABP base and child,
incl. linked layers) whose class or title mentions MotionMatching / BlendStack / Root / Offset / Linked / Inertial / Snapshot, with the
properties that govern root motion; the mesh / character settings that gate root motion consumption."""
import unreal as u, json
from editor_toolset.toolsets.blueprint import BlueprintTools as B
out = {}
for ap in ('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase', '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching'):
    bp = u.load_asset(ap); rows = []
    for g in B.list_graphs(bp):
        for n in B.find_nodes(g):
            cn = n.get_class().get_name()
            if any(k in cn for k in ('MotionMatching', 'BlendStack', 'Root', 'Offset', 'Linked', 'Inertial', 'Snapshot', 'Sequence', 'Mirror', 'Warping', 'FootPlacement')) and cn.startswith('AnimGraphNode'):
                d = {'g': g.get_name(), 'cls': cn}
                try:
                    nd = n.get_editor_property('node')
                    for k in ('root_motion', 'b_root_motion', 'use_root_motion', 'root_motion_mode', 'b_teleport_to_explicit_time', 'translation_mode', 'rotation_mode', 'b_use_root_motion', 'evaluation_mode', 'mode'):
                        try: d[k] = str(nd.get_editor_property(k))[:60]
                        except Exception: pass
                except Exception as e: d['err'] = str(e)[:60]
                rows.append(d)
    out[ap.split('/')[-1]] = rows
    cdo = u.get_default_object(bp.generated_class())
    for k in ('root_motion_mode', 'b_use_multi_threaded_animation_update', 'use_multi_threaded_animation_update'):
        try: out[ap.split('/')[-1] + '_' + k] = str(cdo.get_editor_property(k))
        except Exception: pass
pb = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/BP_PBI_Player'); cdo = u.get_default_object(pb.generated_class())
try:
    m = cdo.get_editor_property('mesh')
    for k in ('anim_class', 'visibility_based_anim_tick_option', 'enable_update_rate_optimizations', 'b_enable_update_rate_optimizations'):
        try: out['mesh_' + k] = str(m.get_editor_property(k))[:90]
        except Exception: pass
    cm = cdo.get_editor_property('character_movement')
    for k in ('allow_physics_rotation_during_anim_root_motion', 'b_allow_physics_rotation_during_anim_root_motion'):
        try: out['cmc_' + k] = str(cm.get_editor_property(k))
        except Exception: pass
except Exception as e: out['pawn_err'] = str(e)[:100]
print('RMPROBE249 ' + json.dumps(out, default=str))
