# probe_body.py (read-only): animgraph node list + all variable defaults of ABP_Sph_Body_GASP, and mesh component / anim setup of BP_HybridA_Player
import unreal as u
exec(open(u.Paths.project_dir()+'Tools/UE59_20261119/b59.py',encoding='utf8').read())
B = u.BlueprintToolset; o = []
for P in ('/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP',):
    a = u.load_asset(P); d = u.get_default_object(a.generated_class())
    o.append('#### ' + P + ' parent ' + str(a.generated_class().get_super_class().get_name() if hasattr(a.generated_class(),'get_super_class') else ''))
    for g in B.list_graphs(a):
        ns = B.find_nodes(g); o.append('== graph %s nodes %d' % (g.get_name(), len(ns)))
        for n in ns:
            cn = n.get_class().get_name()
            if not cn.startswith('AnimGraphNode_'): continue
            line = cn
            try:
                nd = n.get_editor_property('node'); ex = []
                for p in ('bone_to_modify','rotation_mode','rotation_space','translation_mode','alpha','source_mesh_component','b_use_attached_parent','ik_retargeter_asset','retarget_from','lod_threshold','control_rig_class','post_process','layer','interface','tag','blend_weights','alpha_input_type','b_alpha_bool_enabled','alpha_curve_name','curve_name','effector_location_space','ik_bone'):
                    try:
                        v = nd.get_editor_property(p); s = str(v)
                        if hasattr(v,'bone_name'): s = str(v.bone_name)
                        ex.append('%s=%s' % (p, s[:90]))
                    except Exception: pass
                line += ' | ' + ' '.join(ex)
            except Exception as e: line += ' | ERR ' + str(e)[:50]
            try:
                for pn in n.get_editor_property('show_pin_for_properties') if False else []: pass
            except Exception: pass
            o.append('  ' + line)
    try:
        vs = u.BlueprintEditorLibrary.list_member_variables(a) if hasattr(u.BlueprintEditorLibrary,'list_member_variables') else []
    except Exception: vs = []
    names = []
    try:
        for pr in dir(d):
            pass
    except Exception: pass
import json
open(u.Paths.project_dir() + 'Saved/UE59Work/r4/body_graph.txt', 'w', encoding='utf8').write('\n'.join(o)); print('PB', len(o))
