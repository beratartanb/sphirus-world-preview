# c_bob7_defaults.py (control, in-memory): bob damping defaults on the BP_HybridA_Player CDO (builtins.BOBV overrides)
import unreal as u, builtins
V={'BOB_On':True,'BOB_LP':2.5,'BOB_KzWalk':0.55,'BOB_KzSpr':0.25,'BOB_Kx':0.4,'BOB_AccMax':200.0}; V.update(getattr(builtins,'BOBV',None) or {})
c=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
for k,v in V.items(): c.set_editor_property(k,v)
print('BOBDEF',{k:c.get_editor_property(k) for k in V})
