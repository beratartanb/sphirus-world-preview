# c_steerpin5.py (control, in-memory): Steering nodes under the Motion Matching node of ABP_Sph_GASP: exposed pin defaults
# (builtins.STEERPIN = {pin: value text}); prints the pin values of every Steering node. The exposed pin, not the node struct, is used.
import unreal as u, builtins, re
T=u.BlueprintToolset; a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); S=getattr(builtins,'STEERPIN',None) or {}; o=[]
if getattr(builtins,'STEERPIN_DOC',False): print('DOC', (T.set_pin_value.__doc__ or '')[:600])
for g in T.list_graphs(a):
    for n in T.find_nodes(g):
        if n.get_class().get_name()!='AnimGraphNode_Steering': continue
        pth=n.get_path_name(); mm='MotionMatching_0' in pth
        def pins():
            inf=T.get_node_infos([n])[0]; return {str(p_.get_editor_property('name')):p_ for p_ in inf.get_editor_property('input_pins')}
        P=pins()
        if mm:
            for k,v in S.items():
                try: T.set_pin_value(P[k].get_editor_property('pin_id'),str(v))
                except Exception as e: print('SETERR',k,str(e)[:300])
        P=pins(); o.append('%s %s %s'%('MM' if mm else 'BS',n.get_name()[-10:],{k:str(P[k].get_editor_property('value')) for k in P if k not in ('ComponentPose','TargetOrientation')}))
u.BlueprintEditorLibrary.compile_blueprint(a); print('STEERPIN status',a.get_editor_property('status')); print('STEERPIN\n'+'\n'.join(o))
