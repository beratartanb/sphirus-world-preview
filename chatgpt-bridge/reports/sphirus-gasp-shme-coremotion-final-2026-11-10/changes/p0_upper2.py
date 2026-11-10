# p0_upper2.py (write, phase 2 of 2) on ABP_Sph_GASP: UpperBody montage layer with a single evaluation of the GASP base.
#   GaspBase(cached) -> Use#1 -> LayeredBoneBlend.BasePose
#   GaspBase(cached) -> Use#2 -> Slot 'UpperBody' -> LayeredBoneBlend.BlendPoses_0  (branch spine_01, mesh-space rotation)
#   LayeredBoneBlend -> DefaultSlot.Source  (DefaultSlot full-body montages stay on top)
# The pose that fed DefaultSlot now has exactly one consumer (the Save Cached Pose).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
d=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); ag=[g for g in B.list_graphs(d) if g.get_name()=='AnimGraph'][0]; nodes=B.find_nodes(ag)
ds=[n for n in nodes if n.get_class().get_name()=='AnimGraphNode_Slot' and str(n.get_editor_property('node').get_editor_property('slot_name'))=='DefaultSlot']; assert len(ds)==1; pds=pn(ds[0])
sv=[n for n in nodes if n.get_class().get_name()=='AnimGraphNode_SaveCachedPose' and str(n.get_editor_property('cache_name'))=='GaspBase']; assert len(sv)==1
S=src((pn(sv[0]),'Pose')); assert len(S)==1; print('BASE src',S)
cur=src((pds,'Source')); print('DefaultSlot src now',cur); assert cur==S, 'already rewired?'
ut=[t for t in B.find_node_types(ag,'GaspBase')]; print('USE types',ut); assert ut
lt=[t for t in B.find_node_types(ag,'Animation|Blends|')]; print('BLEND types',lt)
st=[t for t in B.find_node_types(ag,"Slot'")]; print('SLOT types',st[:6])
u1=pn(B.create_node(ag,ut[0],u.IntPoint(-300,700))); u2=pn(B.create_node(ag,ut[0],u.IntPoint(-300,900)))
lbt=[t for t in lt if ('katman' in t.lower() or 'layered' in t.lower())]; print('LBB pick',lbt[:3]); assert lbt; lb=B.create_node(ag,lbt[0],u.IntPoint(0,800)); plb=pn(lb)
sl=B.create_node(ag,st[0],u.IntPoint(-150,950)); psl=pn(sl)
nd=sl.get_editor_property('node'); nd.set_editor_property('slot_name','UpperBody'); sl.set_editor_property('node',nd); print('SLOT name',sl.get_editor_property('node').get_editor_property('slot_name'))
ln=lb.get_editor_property('node'); ls=ln.get_editor_property('layer_setup')
bf=u.BranchFilter(); bf.set_editor_property('bone_name','spine_01'); bf.set_editor_property('blend_depth',0)
ib=u.InputBlendPose(); ib.set_editor_property('branch_filters',[bf]); ln.set_editor_property('layer_setup',[ib])
ln.set_editor_property('mesh_space_rotation_blend',True); lb.set_editor_property('node',ln)
print('LBB layer',[str(x.get_editor_property('branch_filters')[0].get_editor_property('bone_name')) for x in lb.get_editor_property('node').get_editor_property('layer_setup')])
print('pins LBB in',[str(x.name) for x in info(plb).input_pins],'out',[str(x.name) for x in info(plb).output_pins],'SLOT in',[str(x.name) for x in info(psl).input_pins])
disconnect((pds,'Source'))
connect((u1,'Pose'),(plb,'BasePose')); connect((u2,'Pose'),(psl,'Source')); connect((psl,'Pose'),(plb,'BlendPoses_0')); connect((plb,'Pose'),(pds,'Source'))
L.compile_blueprint(d); e=errs(d); print('ERR',e); assert not e; assert EA.save_loaded_asset(d,False); print('PHASE2 DONE')
