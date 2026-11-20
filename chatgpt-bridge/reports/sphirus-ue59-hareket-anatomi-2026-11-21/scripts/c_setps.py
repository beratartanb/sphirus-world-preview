# c_setps.py (control, in-memory): set player CDO vars from builtins.PSV
import unreal as u, builtins
d=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
for k,v in (getattr(builtins,'PSV',None) or {}).items(): d.set_editor_property(k,v); print('SETPS',k,d.get_editor_property(k))
