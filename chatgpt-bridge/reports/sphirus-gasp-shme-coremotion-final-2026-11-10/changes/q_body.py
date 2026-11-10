# q_body.py (read-only): ABP_Sph_Body anim graph node list + retarget node settings; face ABP summary.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
for path in ['/Game/Sphirus/Player/Anim/ABP_Sph_Body']:
    bp=u.load_asset(path); print('==',path,'skel',bp.get_editor_property('target_skeleton').get_path_name())
    for g in B.list_graphs(bp):
        ns=B.find_nodes(g); print(' GRAPH',g.get_name(),len(ns))
        for n in ns:
            p=pn(n); i=info(p); t=str(i.type_id)
            print('   N',t[:90],'|',[ (str(x.name)) for x in i.input_pins][:8])
    for o in u.EditorAssetLibrary.load_asset(path).get_outer().get_outermost().get_name() and []: pass
# retarget node objects via graph object scan
import gc as _gc
bp=u.load_asset('/Game/Sphirus/Player/Anim/ABP_Sph_Body')
for g in B.list_graphs(bp):
    for n in B.find_nodes(g):
        try:
            nd=n.get_editor_property('node')
            print('NODE',type(n).__name__, {k:str(nd.get_editor_property(k))[:120] for k in ('ik_retargeter_asset','use_attached_parent','source_mesh_component_name','retarget_from','b_use_attached_parent') if hasattr(nd,k) or True for _ in [0] if (lambda kk: (nd.get_editor_property(kk) is not None))(k) } )
        except Exception as e: pass
