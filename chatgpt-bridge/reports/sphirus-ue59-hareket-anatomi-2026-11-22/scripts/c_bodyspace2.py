# c_bodyspace2.py (control job, in-memory; saved by a gated write job) on ABP_Sph_Body_GASP - 2026-11-22 round 5.
#  - lowerarm posture nodes (AnimGraphNode_ModifyBone_14/15) COMPONENT -> PARENT-BONE space (forearm valgus / humeral rotation of the
#    posture controller need a body-attached frame); V?_ForeL/R re-expressed with the bind axes (probe_fore.py).
#  - effort vectors of spine / head / clavicles (VE_*) zeroed: the posture controller owns the effort posture now (they produced a
#    sudden ~15 deg slump + rolled shoulders within 0.3 s when a run ended, cancelled only 1 s later).
#  - FatBreath 1.0 -> 0.45 (breath amplitude at full fatigue 0.75 instead of 1.6: shoulders pumped), HeadIdle/Walk/Run look-at
#    weights 0.2/0.35/0.65 -> 0.1/0.15/0.3 (the head was held on a fixed forward point).
import unreal as u, json
P='/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP'; a=u.load_asset(P); T=u.BlueprintToolset; pd=u.Paths.project_dir()
FA=json.load(open(pd+'Saved/UE59Work/r5/fore_axes.json'))
g=[x for x in T.list_graphs(a) if x.get_name()=='AnimGraph'][0]; N={n.get_name():n for n in T.find_nodes(g)}
want={'AnimGraphNode_ModifyBone_14':'lowerarm_l','AnimGraphNode_ModifyBone_15':'lowerarm_r'}
for nm,bn in want.items():
    nd=N[nm].get_editor_property('node'); assert str(nd.get_editor_property('bone_to_modify').get_editor_property('bone_name'))==bn,(nm,bn)
    assert nd.get_editor_property('rotation_space')==u.BoneControlSpace.BCS_COMPONENT_SPACE,'already converted'
d=u.get_default_object(a.generated_class()); old={}; vals={}
for pf in ('VI','VR','VA','VE','VC','VW','VD'):
    for k,sd in (('ForeL','l'),('ForeR','r')):
        n='%s_%s'%(pf,k)
        try: v=d.get_editor_property(n)
        except Exception: continue
        old[n]=[v.x,v.y,v.z]; c=FA[sd]['cols']; vals[n]=[round(v.x*c[0][i]+v.y*c[1][i]+v.z*c[2][i],3) for i in range(3)]
for n in ('VE_Spine3','VE_Spine5','VE_Head','VE_Neck1','VE_ClavL','VE_ClavR'):
    try: v=d.get_editor_property(n); old[n]=[v.x,v.y,v.z]; vals[n]=[0.0,0.0,0.0]
    except Exception: pass
S={'FatBreath':0.45,'HeadIdle':0.1,'HeadWalk':0.15,'HeadRun':0.3}
for k in S: old[k]=d.get_editor_property(k)
json.dump({'old':old,'new':vals,'scalars':S},open(pd+'Saved/UE59Work/r5/bodyspace2_values.json','w'),indent=0)
for nm in want:
    nd=N[nm].get_editor_property('node'); nd.set_editor_property('rotation_space',u.BoneControlSpace.BCS_PARENT_BONE_SPACE); N[nm].set_editor_property('node',nd)
u.BlueprintEditorLibrary.compile_blueprint(a)
d=u.get_default_object(u.load_asset(P).generated_class())
for n,nv in vals.items(): d.set_editor_property(n,u.Vector(*nv))
for k,v in S.items(): d.set_editor_property(k,v)
u.BlueprintEditorLibrary.compile_blueprint(a)
d=u.get_default_object(u.load_asset(P).generated_class())
print('BODYSPACE2',{k:old[k] for k in list(old)[:4]},'->',{k:vals[k] for k in list(vals)[:4]},'FatBreath',d.get_editor_property('FatBreath'),'HeadRun',d.get_editor_property('HeadRun'),'VE_Spine5',d.get_editor_property('VE_Spine5').z,str(u.load_asset(P).get_editor_property('status'))[-12:])
