# c_pelvis6.py (control, in-memory): FootPlacement PelvisSettings of ABP_Sph_GASP: PelvisHeightMode / MaxOffset (builtins.PELVIS6 = {'mode':..,'max':..}).
# Round-5 state: AllLegs + MaxOffset 250: on stairs the pelvis is lowered until the REAR foot (one or two steps below) still reaches the
# ground -> visible pelvis 42 cm (walk) / 30 cm (run) above its foot level instead of ~90 (deep knee bend, user review).
import unreal as u, builtins, re
T=u.BlueprintToolset; a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); P=dict(mode='FrontPlantedFeetUphill_FrontFeetDownhill',max=None); P.update(getattr(builtins,'PELVIS6',None) or {}); done=0
for g in T.list_graphs(a):
    for n in T.find_nodes(g):
        if n.get_class().get_name()=='AnimGraphNode_FootPlacement':
            nd=n.get_editor_property('node'); t=nd.export_text(); t0=t
            m=re.search(r'PelvisHeightMode=([A-Za-z_]+)',t); assert m,t[:400]
            if P['mode']: t=t.replace(m.group(0),'PelvisHeightMode='+P['mode'])
            if P['max'] is not None:
                m2=re.search(r'PelvisSettings=\(MaxOffset=[-0-9.]+',t); t=t.replace(m2.group(0),'PelvisSettings=(MaxOffset=%.6f'%P['max'])
            nd.import_text(t); n.modify(); n.set_editor_property('node',nd); done+=1
            print('PELVIS6',m.group(0),'->',re.search(r'PelvisSettings=\(MaxOffset=[-0-9.]+',n.get_editor_property('node').export_text()).group(0),re.search(r'PelvisHeightMode=([A-Za-z_]+)',n.get_editor_property('node').export_text()).group(0))
assert done==1
u.BlueprintEditorLibrary.compile_blueprint(a); print('PELVIS6 status',a.get_editor_property('status'))
