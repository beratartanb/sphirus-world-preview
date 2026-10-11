"""GD32 fix: set the groom bindings on the BP_GD32_Character_G31 component TEMPLATES with set_binding_asset() (set_editor_property on the template
dropped the three bindings that have a source mesh: HairMain, HairLoose, Eyelashes). Reads back; compiles and saves the Blueprint only if all
four templates hold their binding. GD32 asset only."""
import unreal as u, json, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD32_Identity_20261011/data'; G31 = '/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011'
BP_PATH = '/Game/Sphirus/CharacterLab/GD32_IdentityMaster_20261011/Assembly/BP_GD32_Character_G31'
B = {'HairMain': G31+'/Face/Bindings/GB_GD31_HairMain_g31cbh75c', 'HairLoose': G31+'/Face/Bindings/GB_GD31_HairLoose_g31cbh75c', 'Eyelashes': G31+'/Face/Bindings/GB_GD31_EyelashesS_Thin_g31cb', 'Eyebrows': G31+'/Face/Bindings/GB_GD31_EyebrowsCustom_c4_g31'}
bp = u.load_asset(BP_PATH); sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); BFL = u.SubobjectDataBlueprintFunctionLibrary; res = {}
def pn(o): return o.get_path_name() if o is not None else None
for hdl in sds.k2_gather_subobject_data_for_blueprint(bp):
    t = BFL.get_object(BFL.get_data(hdl))
    if isinstance(t, u.GroomComponent):
        n = t.get_name().replace('_GEN_VARIABLE', ''); before = pn(t.binding_asset)
        if before is None:
            t.modify(); t.set_binding_asset(u.load_asset(B[n]))
            if t.binding_asset is None:   # second route: plain property write without the edit-change validation
                t.set_editor_property('binding_asset', u.load_asset(B[n]), u.PropertyAccessChangeNotifyMode.NEVER)
        res[n] = {'before': before, 'after': pn(t.binding_asset)}
ok = len(res) == 4 and all(v['after'] and v['after'].split('.')[0] == B[k] for k, v in res.items())
if ok: u.BlueprintEditorLibrary.compile_blueprint(bp); assert u.EditorAssetLibrary.save_loaded_asset(bp, False)
# compiled class defaults (what a spawned / loaded instance gets)
cdo = {}
for hdl in sds.k2_gather_subobject_data_for_blueprint(bp):
    t = BFL.get_object(BFL.get_data(hdl))
    if isinstance(t, u.GroomComponent): cdo[t.get_name()] = pn(t.binding_asset)
out = {'templates': res, 'saved': ok, 'after_compile': cdo}; (O/'bindfix.json').write_text(json.dumps(out, indent=1)); print('GD32_BINDFIX', json.dumps(out))
