# w_idle.py (write, gated): calm idle-break set. Measured (probe_idle/probe_idle2): v03/v05/v07 = wrist 21-33 deg, elbow 54-88 deg,
# hands lifted to chest height (reads as loosening wrists / getting ready); v01/v02/v04/v06 keep hands low (wrist <= 13, elbow <= 13).
import unreal as u
A='/Game/Characters/UEFN_Mannequin/Animations/Idle/'
ar=u.AssetRegistryHelpers.get_asset_registry(); path={str(a.asset_name):str(a.package_name) for a in ar.get_assets_by_path('/Game/Characters/UEFN_Mannequin/Animations',recursive=True) if 'Stand_Idle_Break' in str(a.asset_name)}
S=[u.load_asset(path['M_Relaxed_Stand_Idle_Break_'+v]) for v in ('v01','v02','v04','v06','v02')]; assert all(S)
c=u.get_default_object(u.load_asset('/Game/Sphirus/Player/Motion/AC_Sph_Motion').generated_class())
objs=[c]
g=u.load_asset('/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'); sds=u.get_engine_subsystem(u.SubobjectDataSubsystem)
for h in sds.k2_gather_subobject_data_for_blueprint(g):
    o=u.SubobjectDataBlueprintFunctionLibrary.get_object(u.SubobjectDataBlueprintFunctionLibrary.get_data(h))
    if o and 'SphMotion' in o.get_name(): objs.append(o)
for o in objs:
    old=[o.get_editor_property('Idle%d'%i).get_name()[-3:] for i in range(5)]
    for i,s in enumerate(S): o.set_editor_property('Idle%d'%i,s)
    print('IDLE',o.get_name(),old,'->',[o.get_editor_property('Idle%d'%i).get_name()[-3:] for i in range(5)])
for p in ('/Game/Sphirus/Player/Motion/AC_Sph_Motion','/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter'):
    print('SAVE',p.split('/')[-1],u.EditorAssetLibrary.save_loaded_asset(u.load_asset(p),False))
print('DIRTY',[x.get_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
