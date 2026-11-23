# unreal_source_manifest.py [case dir] : hash record of the real Unreal source behind a reference-to-game case.
# r2g freeze only fingerprints the case contracts and app/; this file is written into app/ so the fingerprint follows the Unreal files.
# It records sha256 / size / mtime. It is NOT an art-quality check, a build or a playtest. The project has no git: there is no commit id.
import hashlib, json, os, sys, time
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
CASE = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'Docs', 'ReferenceToGame', 'sphirus-slice-01')
GROUPS = {
 'changed_in_this_pass': ['Content/Sphirus/Player/Camera/AC_Sph_Camera.uasset'],
 'verified_owners_unchanged': [
  'Content/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player.uasset',
  'Content/Sphirus/Player/GASP/BP_Sph_GASPCharacter.uasset',
  'Content/Sphirus/Player/GASP/ABP_Sph_GASP.uasset',
  'Content/Sphirus/Player/GASP/ABP_Sph_Body_GASP.uasset',
  'Content/Sphirus/Player/GASP/Rig/RTG_Sph_UEFN_to_MH.uasset',
  'Content/Sphirus/Player/Motion/AC_Sph_Motion.uasset',
  'Content/Sphirus/Player/Camera/M_Sph_Resonance.uasset',
  'Content/Sphirus/Player/Camera/MPC_Sph_Perception.uasset',
  'Content/GraceRanger/BP_GM_GR_GraceRanger.uasset',
  'Content/GraceRanger/Maps/L_GR_SphirusHouse.umap',
  'Content/GraceRanger/Maps/L_GR_CurrentHouseContent.umap',
  'Content/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_Pond.uasset',
  'Content/Grooms/001_Messy_Bob/001_Messy_Bob/001_Messy_Bob.uasset'],
 'project_settings': ['sphirus.uproject', 'Config/DefaultEngine.ini', 'Config/DefaultGame.ini', 'Config/DefaultInput.ini', '.claude/settings.json'],
 'pass_tools': ['Tools/R2G_20261123/' + n for n in ('w_cam_r2g.py', 'c_cam.py', 'c_atm.py', 'c_water.py', 'tour2_r2g.sh', 'rec_r2g.sh', 'views_slice.txt', 'views_cam.txt', 'fill_contracts.py', 'unreal_source_manifest.py')],
 'user_save_not_written': ['Saved/SaveGames/SFSaveSlot.sav'],
}
def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
out = {'what_this_is': 'sha256 / size / mtime of the Unreal files this case refers to. Hash record only; no judgement of art quality, no build, no playtest.',
       'project_root': ROOT, 'source_control': 'none (no git in this project); rollback is the manifest233 backup named in STATUS.txt',
       'engine': 'UE 5.9.0-60738873 (read live from the editor, 2026-11-23)', 'written': time.strftime('%Y-%m-%d %H:%M:%S'), 'files': {}}
for g, fs in GROUPS.items():
    out['files'][g] = {}
    for rel in fs:
        p = os.path.join(ROOT, rel)
        out['files'][g][rel] = {'sha256': sha(p), 'bytes': os.path.getsize(p), 'mtime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(p)))} if os.path.isfile(p) else {'missing': True}
os.makedirs(os.path.join(CASE, 'app'), exist_ok=True)
json.dump(out, open(os.path.join(CASE, 'app', 'UNREAL_SOURCE_MANIFEST.json'), 'w', encoding='utf8'), indent=2)
print('MANIFEST', sum(len(v) for v in out['files'].values()), 'files', 'missing', [r for v in out['files'].values() for r, e in v.items() if e.get('missing')])
