# c_cam.py (control, in-memory only): AC_Sph_Camera class defaults from builtins.R2G_CAM (dict). Prints old -> new and the player templates.
import unreal as u, builtins
V = getattr(builtins, 'R2G_CAM', None) or {}
a = u.load_asset('/Game/Sphirus/Player/Camera/AC_Sph_Camera'); d = u.get_default_object(a.generated_class())
K = ('OutD','OutDTight','HomeD','HomeDTight','HeadX','HeadY','FovOut','FovHome','FovRun','SpeedArm','LagMax','LagSpeed','BackRaise','TightRaise','YKeep','HeadTopZ','HeadMargin')
print('CAM_OLD', {k: round(d.get_editor_property(k), 3) for k in K})
for k, v in V.items(): d.set_editor_property(k, v)
print('CAM_NEW', {k: round(d.get_editor_property(k), 3) for k in K})
for p in ('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player', '/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'):
    bp = u.load_asset(p); sub = u.get_engine_subsystem(u.SubobjectDataSubsystem)
    for h in sub.k2_gather_subobject_data_for_blueprint(bp):
        o = u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(h))
        if o and o.get_name().startswith('SphCamera'): print('TEMPLATE', p.split('/')[-1], {k: round(o.get_editor_property(k), 3) for k in ('OutD','HomeD','HeadX','HeadY')})
