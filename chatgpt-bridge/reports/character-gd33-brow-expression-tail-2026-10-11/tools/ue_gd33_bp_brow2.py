"""GD33: switch the Eyebrows component template (2nd revision: c7u2 = tail lifted from the user-marked reference region, replaces the rejected hooked c6t2) of the GD33 evaluation Blueprint (own GD33 asset, unpublished) from brow c5hl1 to the
tail-extended c7u2 (same medial / body build, temple tail continued down along the orbital rim, l1 colour) with its binding
(set_binding_asset on the template, see the GD32 binding trap); compile + save; read back."""
import unreal as u, json
G = '/Game/Sphirus/CharacterLab/GD33_IdentityMaster_20261011'; bp = u.load_asset(G+'/Assembly/BP_GD33_Character_G31')
sds = u.get_engine_subsystem(u.SubobjectDataSubsystem); BFL = u.SubobjectDataBlueprintFunctionLibrary; out = {}
for h in sds.k2_gather_subobject_data_for_blueprint(bp):
    t = BFL.get_object(BFL.get_data(h))
    if isinstance(t, u.GroomComponent) and t.get_name().startswith('Eyebrows'):
        t.modify(); t.set_editor_property('groom_asset', u.load_asset(G+'/Grooms/GR_GD33_BrowCustom_c7u2')); t.set_binding_asset(u.load_asset(G+'/Face/Bindings/GB_GD33_EyebrowsCustom_c7u2_g31'))
        out['eyebrows'] = [t.groom_asset.get_name(), t.binding_asset.get_name() if t.binding_asset else None]
assert out.get('eyebrows') and out['eyebrows'][1], out
u.BlueprintEditorLibrary.compile_blueprint(bp); out['saved'] = u.EditorAssetLibrary.save_loaded_asset(bp, False); print('GD33_BPBROW', json.dumps(out))
