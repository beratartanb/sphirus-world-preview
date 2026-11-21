# c_pelvis5.py (control, in-memory): FootPlacement PelvisSettings.LinearStiffness of ABP_Sph_GASP (builtins.PELVIS_K, default 600; was 100).
# The pelvis offset spring (critically damped, w = sqrt(k)) trailed the capsule on stairs by 2 v / w: capsule rising 108 cm/s at a walk
# -> 22 cm, 249 cm/s at a run -> 50 cm, on top of the one-step drop the node adds for the rear foot (a_stair_walk pelvis 46 cm low,
# a_stair_run 66 cm low = the body sank into the stairs).
import unreal as u, builtins, re
T=u.BlueprintToolset; a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); k=float(getattr(builtins,'PELVIS_K',None) or 600.0); done=0
for g in T.list_graphs(a):
    for n in T.find_nodes(g):
        if n.get_class().get_name()=='AnimGraphNode_FootPlacement':
            nd=n.get_editor_property('node'); t=nd.export_text(); m=re.search(r'PelvisSettings=\(MaxOffset=[-0-9.]+,LinearStiffness=([0-9.]+)',t); assert m
            new=m.group(0)[:m.group(0).rindex('=')+1]+'%.6f'%k
            nd.import_text(t.replace(m.group(0),new)); n.modify(); n.set_editor_property('node',nd); done+=1
            print('PELVIS5',m.group(0)[-28:],'->',re.search(r'LinearStiffness=([0-9.]+)',n.get_editor_property('node').export_text()).group(0))
assert done==1
u.BlueprintEditorLibrary.compile_blueprint(a); print('PELVIS5 status',a.get_editor_property('status'))
