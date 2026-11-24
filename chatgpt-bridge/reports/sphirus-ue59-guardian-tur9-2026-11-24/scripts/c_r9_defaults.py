# c_r9_defaults.py (control, in-memory; re-appliable): round-9 class defaults. builtins.R9V may override single values for an A/B.
import unreal as u, builtins
M9={'RcOpen':1500.0,'RcKMax':1.3,'DmMin':150.0,'DmOpen':280.0,'DmRate':280.0,'DmRateK':0.75,'DmWalkV':300.0}
M9.update(getattr(builtins,'R9V',None) or {})
m=u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class())
for k,v in M9.items(): m.set_editor_property(k,v)
c=u.get_default_object(u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP').generated_class())
d=c.get_editor_property('PlantSettings_Default'); d.set_editor_property('unplant_radius',45.0); c.set_editor_property('PlantSettings_Default',d)
t=u.FootPlacementPlantSettings(); t.import_text(c.get_editor_property('PlantSettings_Default').export_text()); t.set_editor_property('unplant_radius',float(getattr(builtins,'R9TURNRAD',85.0))); c.set_editor_property('PlantSettings_Turns',t)
d=c.get_editor_property('PlantSettings_Default'); d.set_editor_property('unplant_radius',45.0); c.set_editor_property('PlantSettings_Default',d)
assert abs(c.get_editor_property('PlantSettings_Default').get_editor_property('unplant_radius')-45.0)<0.01 and abs(c.get_editor_property('PlantSettings_Turns').get_editor_property('unplant_radius')-float(getattr(builtins,'R9TURNRAD',85.0)))<0.01
P9={'BOB_DipK':0.8,'BOB_DipFree':3.0,'BOB_DipMax':12.0,'PS_FW':1.0}
pc=u.get_default_object(u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player').generated_class())
for k,v in P9.items(): pc.set_editor_property(k,v)
print('R9DEF player',{k:pc.get_editor_property(k) for k in P9})
print('R9DEF motion',{k:m.get_editor_property(k) for k in M9},'plant default/turns',c.get_editor_property('PlantSettings_Default').get_editor_property('unplant_radius'),c.get_editor_property('PlantSettings_Turns').get_editor_property('unplant_radius'))
