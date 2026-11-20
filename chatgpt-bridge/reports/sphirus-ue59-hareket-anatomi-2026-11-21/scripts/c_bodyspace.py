# c_bodyspace.py (control job, in-memory; saved later by a gated write job) on ABP_Sph_Body_GASP - 2026-11-21 round 4.
# The posture nodes of spine_03, spine_05, neck_01, neck_02, head, clavicles and upper arms (AnimGraphNode_ModifyBone_5..13) worked
# in COMPONENT space. The capsule snaps to the input direction (GASP: rotation rate -1) and the body follows through the root
# offset, so during every turn / reface start the body is yawed against the component and those offsets acted about the wrong
# axes (sagittal -16 deg became a side bend): upper-body step of 14-23 cm in one frame at each sharp direction change.
# Now PARENT-BONE space (body-attached). All V?_ vectors of these bones are re-expressed with the bind axes (probe_axes.py), the
# constant carriage terms the posture controller (BP_HybridA_Player.GR_Posture) replaces are zeroed, head level integrator off
# (the controller owns head roll).
import unreal as u, json
P='/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'; a=u.load_asset(P); T=u.BlueprintToolset; pd=u.Paths.project_dir()
AX=json.load(open(pd+'Saved/UE59Work/r4/axes.json'))
g=[x for x in T.list_graphs(a) if x.get_name()=='AnimGraph'][0]
want=['AnimGraphNode_ModifyBone_%d'%i for i in range(5,14)]; exp=['spine_03','spine_05','neck_01','neck_02','head','clavicle_l','clavicle_r','upperarm_l','upperarm_r']
N={n.get_name():n for n in T.find_nodes(g)}; chk=[]
for nm,bn in zip(want,exp):
    nd=N[nm].get_editor_property('node'); b=str(nd.get_editor_property('bone_to_modify').get_editor_property('bone_name')); sp=nd.get_editor_property('rotation_space')
    assert b==bn,(nm,b,bn); assert sp==u.BoneControlSpace.BCS_COMPONENT_SPACE,('already converted?',nm,sp)
d=u.get_default_object(a.generated_class()); old={}
KEY={'Spine3':'spine_03','Spine5':'spine_05','Neck1':'neck_01','Neck2':'neck_02','Head':'head','ClavL':'clavicle_l','ClavR':'clavicle_r','ArmL':'upperarm_l','ArmR':'upperarm_r'}
ZERO=['VW_ArmL','VW_ArmR','VW_ClavL','VW_ClavR','VW_Spine5','VW_Neck1','VW_Head','VD_ClavL','VD_ClavR','VD_ArmL','VD_ArmR','VD_Spine5','VR_Spine3','VR_Spine5','VA_Spine3','VA_Spine5','VR_ArmL','VR_ArmR']
vals={}
for pf in ('VI','VR','VA','VE','VC','VW','VD'):
    for k,b in KEY.items():
        n='%s_%s'%(pf,k)
        try: v=d.get_editor_property(n)
        except Exception: continue
        old[n]=[v.x,v.y,v.z]; c=AX[b]['cols']
        nv=[0.0,0.0,0.0] if n in ZERO else [round(v.x*c[0][i]+v.y*c[1][i]+v.z*c[2][i],3) for i in range(3)]
        vals[n]=nv
old['HLevelK']=d.get_editor_property('HLevelK')
json.dump({'old':old,'new':vals},open(pd+'Saved/UE59Work/r4/bodyspace_values.json','w'),indent=0)
for nm in want:
    nd=N[nm].get_editor_property('node'); nd.set_editor_property('rotation_space',u.BoneControlSpace.BCS_PARENT_BONE_SPACE); N[nm].set_editor_property('node',nd)
u.BlueprintEditorLibrary.compile_blueprint(a)
d=u.get_default_object(u.load_asset(P).generated_class())
for n,nv in vals.items(): d.set_editor_property(n,u.Vector(*nv))
d.set_editor_property('HLevelK',0.0)
u.BlueprintEditorLibrary.compile_blueprint(a)
d=u.get_default_object(u.load_asset(P).generated_class()); g=[x for x in T.list_graphs(u.load_asset(P)) if x.get_name()=='AnimGraph'][0]
N={n.get_name():n for n in T.find_nodes(g)}
print('BODYSPACE spaces',[str(N[nm].get_editor_property('node').get_editor_property('rotation_space')).split('.')[-1][:12] for nm in want][:3],'VI_Spine5',d.get_editor_property('VI_Spine5'),'VC_Spine3',d.get_editor_property('VC_Spine3'),'VW_ClavL',d.get_editor_property('VW_ClavL'),'HLevelK',d.get_editor_property('HLevelK'),'n',len(vals))
