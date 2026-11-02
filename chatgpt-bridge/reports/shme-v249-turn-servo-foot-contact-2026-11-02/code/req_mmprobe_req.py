"""mmprobe (measure): the Motion Matching anim node's play-rate / blend settings and which of its pins are exposed or bound, plus the
script-callable MotionMatchingAnimNodeLibrary functions (looking for a per-frame play-rate control)."""
import unreal as u, json
from editor_toolset.toolsets.blueprint import BlueprintTools as B
out = {'lib': [m for m in dir(u.MotionMatchingAnimNodeLibrary) if not m.startswith('_')] if hasattr(u, 'MotionMatchingAnimNodeLibrary') else 'n/a'}
bp = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase')
for g in B.list_graphs(bp):
    if g.get_name() != 'AnimGraph': continue
    for n in B.find_nodes(g):
        if n.get_class().get_name() != 'AnimGraphNode_MotionMatching': continue
        nd = n.get_editor_property('node'); d = {}
        for k in dir(nd):
            if k.startswith('_') or callable(getattr(nd, k, None)): continue
        for k in ('play_rate', 'blend_time', 'b_use_inertial_blend', 'search_throttle_time', 'b_reset_on_becoming_relevant', 'b_should_filter_notifies', 'blend_parameters', 'max_active_blends', 'database', 'b_use_pose_history_root_bone_override'):
            try: d[k] = str(nd.get_editor_property(k))[:120]
            except Exception as e: d[k] = 'n/a'
        try: d['props'] = [p for p in dir(nd) if not p.startswith('_')][:80]
        except Exception: pass
        try: d['shown_pins'] = [str(x.get_editor_property('property_name')) + ':' + str(x.get_editor_property('b_show_pin')) for x in n.get_editor_property('show_pin_for_properties')]
        except Exception as e: d['shown_pins'] = 'err ' + str(e)[:60]
        out.setdefault('mm_nodes', []).append(d)
print('MMPROBE249 ' + json.dumps(out, default=str))
