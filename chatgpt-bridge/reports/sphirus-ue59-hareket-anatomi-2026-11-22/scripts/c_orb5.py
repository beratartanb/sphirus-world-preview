# c_orb5.py (control, in-memory): OffsetRootBone RotationHalfLife (builtins.ORB_RHL, default 0.05; shipped 0.1) on ABP_Sph_GASP + compile.
# With 0.1 the visible body lagged the capsule facing by ~0.29 s x yaw rate (33 deg at a 90 deg/s camera turn while walking: the body
# pointed 22 deg outside its own travel direction and a stop / start then began from that offset).
import unreal as u, builtins, re
T=u.BlueprintToolset; a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); hl=float(getattr(builtins,'ORB_RHL',None) or 0.1); done=0
for g in T.list_graphs(a):
    for n in T.find_nodes(g):
        if n.get_class().get_name()=='AnimGraphNode_OffsetRootBone':
            nd=n.get_editor_property('node'); t=nd.export_text(); m=re.search(r'RotationHalfLife=([0-9.]+)',t); assert m
            nd.import_text(t.replace(m.group(0),'RotationHalfLife=%.6f'%hl)); n.modify(); n.set_editor_property('node',nd); done+=1
            print('ORB5',m.group(0),'->',re.search(r'RotationHalfLife=([0-9.]+)',n.get_editor_property('node').export_text()).group(0))
assert done==1
u.BlueprintEditorLibrary.compile_blueprint(a); print('ORB5 status',a.get_editor_property('status'))
