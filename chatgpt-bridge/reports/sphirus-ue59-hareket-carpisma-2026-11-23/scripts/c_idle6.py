# c_idle6.py (control, in-memory): idle-break slot 4 back to v02. v09 was tried and rejected: its head looks 67 deg down (idle_neck.txt, p6_I_60 t 144-150).
# duplicated v02 - four different calm breaks + one weight shift, drawn at random every 14-26 s.
import unreal as u
ar=u.AssetRegistryHelpers.get_asset_registry(); path={str(a.asset_name):str(a.package_name) for a in ar.get_assets_by_path('/Game/Characters/UEFN_Mannequin/Animations',recursive=True) if 'Stand_Idle_Break' in str(a.asset_name)}
s=u.load_asset(path['M_Relaxed_Stand_Idle_Break_v02']); objs=[u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class())]
g=u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem)
for h in sds.k2_gather_subobject_data_for_blueprint(g):
    o=u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(h))
    if o and 'SphMotion' in o.get_name(): objs.append(o)
for o in objs:
    o.set_editor_property('Idle4',s); print('IDLE6',o.get_name(),[o.get_editor_property('Idle%d'%i).get_name()[-3:] for i in range(5)])
