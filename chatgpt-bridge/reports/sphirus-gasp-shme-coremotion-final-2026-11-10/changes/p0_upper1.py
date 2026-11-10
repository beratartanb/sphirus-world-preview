# p0_upper1.py (write, phase 1 of 2):
#  a) SK_UEFN_Mannequin.compatible_skeletons += SK_MCPaul_Skeleton - the 18 Sphirus interaction montages (MCPaul skeleton,
#     same UE5 bone names) can play on the GASP driver. Metadata only, reversible (manifest backup); documented exception
#     to "vendor assets untouched".
#  b) ABP_Sph_GASP: Save Cached Pose 'GaspBase' fed by the pose that enters DefaultSlot (consumers untouched; phase 2
#     after an editor restart adds the UpperBody slot + layered blend through two Use Cached Pose readers).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
sk=u.load_asset('/Game/Characters/UEFN_Mannequin/Meshes/SK_UEFN_Mannequin'); mc=u.load_asset('/Game/MC_Core_Motion/Demo/Characters/MCPaul/Meshes/SK_MCPaul_Skeleton')
cs=list(sk.get_editor_property('compatible_skeletons'))
if mc not in cs: cs.append(mc); sk.set_editor_property('compatible_skeletons',cs)
print('COMPAT',[x.get_name() for x in sk.get_editor_property('compatible_skeletons')]); assert EA.save_loaded_asset(sk,False)
d=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); ag=[g for g in B.list_graphs(d) if g.get_name()=='AnimGraph'][0]; nodes=B.find_nodes(ag)
ds=[n for n in nodes if n.get_class().get_name()=='AnimGraphNode_Slot' and str(n.get_editor_property('node').get_editor_property('slot_name'))=='DefaultSlot']; assert len(ds)==1
pds=pn(ds[0]); S=src((pds,'Source')); print('DefaultSlot source',S); assert len(S)==1
saves=[n for n in nodes if n.get_class().get_name()=='AnimGraphNode_SaveCachedPose' and str(n.get_editor_property('cache_name'))=='GaspBase']
if not saves:
    print('SAVE types',[t for t in B.find_node_types(ag,'nbelleğealınmışpoz')][:6])
    sn=B.create_node(ag,'Animation|CachedPoses|YeniÖnbelleğealınmışpozukaydet...',u.IntPoint(-600,600)); assert sn
    sn.set_editor_property('cache_name','GaspBase'); connect(S[0],(pn(sn),'Pose'))
L.compile_blueprint(d); print('ERR',errs(d)); assert not errs(d); assert EA.save_loaded_asset(d,False); print('PHASE1 DONE')
