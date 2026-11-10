# p1_reparent.py (write, PRODUCTION): same as b2_reparent.py on BP_HybridA_Player (SpringArm -> GR_SpringArm, parent -> BP_Sph_GASPCharacter).
# SandboxCharacter_CMC). The only SCS name collision is SpringArm (both classes add one); the Sphirus one is renamed
# GR_SpringArm first so its graph references follow the rename. Reports compile errors and the merged component list.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
D='/Game/Sphirus/Player/GASP/'
b=u.load_asset('/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'); P=u.load_object(None,D+'BP_Sph_GASPCharacter.BP_Sph_GASPCharacter_C'); assert P
scs=u.get_engine_subsystem(u.SubobjectDataSubsystem); SD=u.SubobjectDataBlueprintFunctionLibrary
def handles(bp):
    out={}
    for h in scs.k2_gather_subobject_data_for_blueprint(bp):
        d=SD.get_data(h); o=SD.get_object(d)
        if o: out[str(SD.get_variable_name(d))]=h
    return out
hs=handles(b); print('CHILD VARS',sorted(hs))
if 'SpringArm' in hs:
    ok=scs.rename_subobject_member_variable(b,hs['SpringArm'],'GR_SpringArm'); print('RENAME SpringArm->GR_SpringArm',ok)
L.compile_blueprint(b); print('ERR after rename',errs(b))
r=L.reparent_blueprint(b,P); print('REPARENT',r)
L.compile_blueprint(b); e=errs(b); print('ERR after reparent',e)
print('MERGED VARS',sorted(handles(b)))
assert EA.save_loaded_asset(b,False); print('SAVED')
