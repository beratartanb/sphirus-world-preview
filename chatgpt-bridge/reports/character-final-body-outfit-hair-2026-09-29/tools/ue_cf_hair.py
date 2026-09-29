"""CF hair candidate: copy the closest MetaHuman-library groom into the isolated candidate folder, auburn material
instances (MetaHuman hair shader: melanin / redness / roughness), and a GroomBindingAsset that fits the groom (authored on
the MetaHuman groom head) to the candidate face mesh. Alternates get bindings only (QA comparison, engine assets untouched).
Config via builtins.CF_HAIR = {'style': 'Hair_S_Updo', 'face': '/Game/.../SKM_CF_FaceMesh', 'alternates': [...]}"""
import unreal as u, pathlib, json, builtins, time
P = pathlib.Path(u.Paths.project_dir()).resolve(); S = P/'Saved/Codex/CharacterFinal_20260929'
CFG = getattr(builtins, 'CF_HAIR', {}); STYLE = CFG.get('style', 'Hair_S_Updo'); FACE = CFG.get('face', '/Game/Sphirus/CharacterLab/BodyRealism_20260929/SKM_BR_FaceMesh'); ALT = CFG.get('alternates', [])
LIB = '/MetaHumanCharacter/Optional/Grooms'; DST = '/Game/Sphirus/CharacterLab/CharacterFinal_20260929/Hair'
EAL = u.EditorAssetLibrary; ME = u.MaterialEditingLibrary; AT = u.AssetToolsHelpers.get_asset_tools(); out = {'style': STYLE, 'face': FACE}
# auburn / copper-red, slightly dry lived-in: MetaHuman M_hair_v4 parameters
AUBURN = {'hairMelanin': 0.72, 'hairRedness': 0.8, 'RedVariation': 0.15, 'MelaninVariationFine': 0.75, 'MelaninVariationRough': 0.45, 'Desat': 0.1, 'RoughnessOverall': 0.62, 'HairRoughness': 0.46, 'Roughness': 0.68, 'Scraggle': 0.22, 'Spec0': 0.35, 'Spec1': 0.55, 'LightAmount': 0.3}   # dark auburn / copper: melanin high, red high, restrained specular
def auburn_mi(name, parent_path):
    path = DST+'/'+name
    mi = u.load_asset(path) if EAL.does_asset_exist(path) else AT.create_asset(name, DST, u.MaterialInstanceConstant, u.MaterialInstanceConstantFactoryNew())
    ME.set_material_instance_parent(mi, u.load_asset(parent_path))
    for k, v in AUBURN.items(): ME.set_material_instance_scalar_parameter_value(mi, k, v)
    EAL.save_loaded_asset(mi, False); return mi
src = LIB+f'/GroomAssets/Hair/{STYLE}/{STYLE}'; gpath = DST+f'/{STYLE}_CF'
if not EAL.does_asset_exist(gpath): assert EAL.duplicate_asset(src, gpath), src
g = u.load_asset(gpath)
mats = g.get_editor_property('hair_groups_materials'); new = []; slots = []
for m in mats:
    pm = m.get_editor_property('material'); pn = pm.get_name() if pm else 'MI_Hair'
    mi = auburn_mi(f'MI_CF_Auburn_{pn}', pm.get_path_name() if pm else LIB.replace('/Optional/Grooms', '')+'/Materials/MI_Hair')
    m.set_editor_property('material', mi); new.append(m); slots.append((str(m.get_editor_property('slot_name')), mi.get_path_name()))
g.set_editor_property('hair_groups_materials', new); out['materials'] = slots; EAL.save_loaded_asset(g, False)
def bind(groom_path, name):
    bpath = DST+'/'+name
    if EAL.does_asset_exist(bpath): EAL.delete_asset(bpath)
    groom = u.load_asset(groom_path); face = u.load_asset(FACE)
    lib_b = u.load_asset(LIB+f'/Bindings/Hair/{groom_path.split("/")[-1].replace("_CF", "")}_Binding'); srcmesh = lib_b.get_editor_property('source_skeletal_mesh') if lib_b else None
    t0 = time.time(); b = u.GroomLibrary.create_new_groom_binding_asset_with_path(bpath, groom, face, 100, srcmesh, 0)
    assert b, 'binding creation failed '+name
    info = {'path': b.get_path_name(), 'source': srcmesh.get_path_name() if srcmesh else None, 'target': b.get_editor_property('target_skeletal_mesh').get_path_name(), 'sec': round(time.time()-t0, 1)}
    try: info['valid'] = b.is_valid() if hasattr(b, 'is_valid') else None
    except Exception as e: info['valid'] = str(e)[:80]
    info['saved'] = EAL.save_loaded_asset(b, False); return info
out['binding'] = bind(gpath, f'{STYLE}_CF_Binding')
out['alternates'] = {}
for a in ALT:
    try: out['alternates'][a] = bind(LIB+f'/GroomAssets/Hair/{a}/{a}', f'QA_{a}_Binding')
    except Exception as e: out['alternates'][a] = 'ERR '+str(e)[:120]
out['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(S/'cf_hair.json').write_text(json.dumps(out, indent=1, default=str)); print(json.dumps(out, indent=1, default=str))
