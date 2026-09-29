"""J0: checkpoint before any outfit asset creation. The destination folder must not exist; the shared isolated skeleton
(referenced by the new garment meshes) is file-copied so any accidental modification can be reverted."""
import unreal as u, pathlib, json, shutil, hashlib, datetime
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/OutfitHome_20260929'; CK = O/'checkpoint_pre_assets'; CK.mkdir(parents=True, exist_ok=True)
DEST = '/Game/Sphirus/CharacterLab/Outfit_Home_20260929'
assert not u.EditorAssetLibrary.does_directory_exist(DEST) or not u.EditorAssetLibrary.list_assets(DEST), 'destination not empty'
files = {'skeleton': R/'Content/Sphirus/CharacterLab/ShoulderFix_20260928/Common/Female/Medium/NormalWeight/Body/metahuman_base_skel.uasset',
         'body_mesh': R/'Content/Sphirus/CharacterLab/BodyRealism_20260929/SKM_BR_BodyMesh.uasset',
         'face_mesh': R/'Content/Sphirus/CharacterLab/BodyRealism_20260929/SKM_BR_FaceMesh.uasset',
         'production_body': R/'Content/MetaHumans/MH_MainCharacter/Body/SKM_MH_MainCharacter_BodyMesh.uasset',
         'production_outfits': R/'Content/MetaHumans/MH_MainCharacter/Clothing/MH_MainCharacter_Outfits.uasset',
         'accepted_b2': R/'Content/Sphirus/CharacterLab/NativeBody_20260928/MH_B2_PendingNativeWorkflow.uasset'}
rec = {'time': datetime.datetime.now().isoformat(), 'dest': DEST, 'files': {}}
for k, p in files.items():
    assert p.exists(), p
    shutil.copy2(p, CK/p.name); rec['files'][k] = {'path': str(p), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest(), 'size': p.stat().st_size}
rec['dirty'] = [p.get_path_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
(CK/'checkpoint.json').write_text(json.dumps(rec, indent=1)); print(json.dumps(rec, indent=1))
