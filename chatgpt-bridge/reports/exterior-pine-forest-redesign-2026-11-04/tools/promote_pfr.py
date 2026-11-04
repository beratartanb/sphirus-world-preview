"""promote_pfr.py (WRITE job under the pfr_world manifest): SAVE the applied Pine Forest redesign - the map package, every new owned
FoliageType / material instance / texture copy the design created and the edited owned MIs (all listed in the manifest).
Dirty packages OUTSIDE the manifest (vendor assets that got flagged in memory, e.g. MI_FallenNeedle after load) are never saved: they are
reloaded from disk so the editor is clean afterwards, and reported. Unused owned trial assets (blocked landscape route) are deleted after the
save when nothing references them. Refuses when PIE runs or when the map is not dirty. builtins.PFR_PROMOTE_DRY = True -> report only.
Output: Saved/Codex/PineForestRedesign_20261104/design/<v>/promote.json"""
import unreal as u, json, pathlib, time, builtins, hashlib

PJ = pathlib.Path(u.Paths.project_dir()); ROOTD = PJ / 'Saved/Codex/PineForestRedesign_20261104'; VAR = getattr(builtins, 'PFR_VARIANT', 'p3'); D = ROOTD / 'design' / VAR
DRY = bool(getattr(builtins, 'PFR_PROMOTE_DRY', False))
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None, 'PIE running'
S = u.EditorLoadingAndSavingUtils
MAN = json.loads((PJ / 'Saved/Codex/SHME_V233_20261027/checkpoint/manifests/pfr_world.json').read_text()); ALLOW = {a['package'] for a in MAN['assets']}
MAP = '/Game/GraceRanger/Maps/L_GR_SphirusHouse'; f = PJ / 'Content/GraceRanger/Maps/L_GR_SphirusHouse.umap'
OWNED = '/Game/GraceRanger/Environment/Exterior20260921/'
UNUSED = ['/Game/GraceRanger/Environment/Exterior20260921/Materials/MI_EX_PF_Landscape']   # created by the blocked landscape-layer trial
res = {'variant': VAR, 'dry': DRY, 'started': time.strftime('%H:%M:%S'), 'problems': []}
dc = list(S.get_dirty_content_packages()); dm = list(S.get_dirty_map_packages())
names_c = [p.get_name() for p in dc]; names_m = [p.get_name() for p in dm]
res['dirty_content'] = names_c; res['dirty_maps'] = names_m
if MAP not in names_m:
    res['problems'].append('map not dirty')
# unused owned trial assets first (never saved to disk: remove the in-memory object so no dirty package remains)
for path in UNUSED:
    obj = u.load_asset(path) if u.EditorAssetLibrary.does_asset_exist(path) else u.find_asset(path) if hasattr(u, 'find_asset') else None
    if obj is None:
        try: obj = u.load_object(None, path + '.' + path.split('/')[-1])
        except Exception: obj = None
    if obj is None: continue
    refs = list(u.EditorAssetLibrary.find_package_referencers_for_asset(path, False)) if u.EditorAssetLibrary.does_asset_exist(path) else []
    if refs: res.setdefault('unused_kept', []).append([path, refs[:5]]); continue
    if DRY: res.setdefault('unused_would_delete', []).append(path); continue
    try:
        ok = u.EditorAssetLibrary.delete_asset(path) if u.EditorAssetLibrary.does_asset_exist(path) else u.EditorAssetLibrary.delete_loaded_asset(obj)
        res.setdefault('unused_deleted', []).append([path, bool(ok)])
    except Exception as ex: res['problems'].append('delete unused %s: %s' % (path.split('/')[-1], repr(ex)[:80]))
dc = list(S.get_dirty_content_packages()); dm = list(S.get_dirty_map_packages())
save_pkgs = [p for p in dm if p.get_name() == MAP] + [p for p in dc if p.get_name() in ALLOW and p.get_name().startswith(OWNED) and p.get_name() not in UNUSED]
outside = [p for p in dc + dm if p not in save_pkgs and p.get_name() not in UNUSED]
res['save_planned'] = [p.get_name() for p in save_pkgs]; res['outside_not_saved'] = [p.get_name() for p in outside]
res['map_sha1_before'] = hashlib.sha1(f.read_bytes()).hexdigest()
if not res['problems'] and not DRY:
    ok = S.save_packages(save_pkgs, False); res['save_ok'] = bool(ok)
    res['map_sha1_after'] = hashlib.sha1(f.read_bytes()).hexdigest(); res['map_mtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(f.stat().st_mtime))
    res['saved'] = [p.get_name() for p in save_pkgs]
    # vendor / foreign packages flagged dirty in memory: back to their disk state, never saved
    if outside:
        try:
            r = S.reload_packages(outside, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); res['outside_reloaded'] = str(r)
        except Exception as ex:
            res['problems'].append('reload outside: ' + repr(ex)[:100])
            for p in outside:
                try: p.set_dirty_flag(False); res.setdefault('outside_undirtied', []).append(p.get_name())
                except Exception as ex2: res['problems'].append('undirty %s: %s' % (p.get_name(), repr(ex2)[:60]))
    res['dirty_after'] = sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
res['finished'] = time.strftime('%H:%M:%S')
(D / 'promote.json').write_text(json.dumps(res, indent=1, default=str))
print('PFR_PROMOTE', 'DRY' if DRY else 'SAVED', res.get('save_ok'), 'problems', res['problems'][:4], 'saved', len(res.get('saved', [])), 'outside', res['outside_not_saved'], 'dirty_after', res.get('dirty_after'))
