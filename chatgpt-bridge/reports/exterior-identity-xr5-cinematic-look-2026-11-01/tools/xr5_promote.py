"""xr5_promote.py (write job, manifest xr5_map): promote the approved XR5 FINAL v2 look to the map (user approval 2026-11-01).
1. applies FINAL exactly as the trial did (xr5_final.py builtins + xr5_look.py, from xr5_backup.json), 2. renames the five XR5_* region
volumes to EX_Look_* (folder EX_PostRain_Look) so trial restores never destroy them, 3. adds EX_Look_Resonance: an unbound PPV,
priority 3, blend weight 0 (no effect until game logic raises it) holding the resonance delta as absolute values on top of FINAL,
4. saves ONLY the map package (the 9 project MIs stay dirty with original content: do not save them), 5. writes design/xr5_promote.json.
builtins.XR5_PROMOTE_DRY = True -> everything except the save."""
import unreal as u, json, os, builtins, pathlib, hashlib, time

PJ = pathlib.Path(u.Paths.project_dir()); D = PJ / 'Saved/Codex/ExteriorIdentity_XR3_20261031/design'; T = PJ / 'Tools/ExteriorIdentity_XR3_20261031'
DRY = bool(getattr(builtins, 'XR5_PROMOTE_DRY', False))
E = u.get_editor_subsystem(u.UnrealEditorSubsystem); assert E.get_game_world() is None, 'PIE running'
A = u.get_editor_subsystem(u.EditorActorSubsystem)
res = {'dry': DRY, 'started': time.strftime('%H:%M:%S'), 'problems': []}

# 0. a previous (dry) run leaves EX_Look_* volumes behind: remove them so the FINAL apply spawns exactly one set
res['prev_removed'] = 0
for a in A.get_all_level_actors():
    if a.get_actor_label().startswith('EX_Look_'): A.destroy_actor(a); res['prev_removed'] += 1

# 1. FINAL v2 (same code path as the trial)
builtins.XR5_LOOK = 'FINAL'; builtins.XR5_BASE = 'L1'
exec(open(T / 'xr5_final.py', encoding='utf-8').read())
exec(compile(open(T / 'xr5_look.py', encoding='utf-8').read(), 'xr5_look.py', 'exec'), {'__name__': '__job__'})
fin = json.loads((D / 'xr5_FINAL.json').read_text())
res['final'] = {'problems': fin['problems'], 'regions': len(fin['regions']), 'sun_rot': fin['sun_rot']}
assert not fin['problems'] and len(fin['regions']) == 5, 'FINAL apply incomplete'

# 2. rename region volumes -> permanent owners
ren = {}
for a in A.get_all_level_actors():
    lab = a.get_actor_label()
    if lab.startswith('XR5_'):
        new = 'EX_Look_' + lab[len('XR5_'):]; a.set_actor_label(new); a.set_folder_path('EX_PostRain_Look'); ren[lab] = new
res['renamed'] = ren; assert len(ren) == 5, ren

# 3. resonance PPV (absolute values = FINAL pp + delta), blend weight 0
ACT = {a.get_actor_label(): a for a in A.get_all_level_actors()}
pp_a = ACT['EX_PostRain_NeutralExposure']; base = pp_a.get_editor_property('settings')
V4 = lambda v: u.Vector4(v[0], v[1], v[2], v[3] if len(v) > 3 else 1.0)
sat0 = base.get_editor_property('color_saturation'); wt0 = base.get_editor_property('white_temp')
gr0 = base.get_editor_property('film_grain_intensity'); vg0 = base.get_editor_property('vignette_intensity')
RES = {'white_temp': wt0 - 300.0, 'color_saturation': V4([sat0.x * 0.94, sat0.y * 0.94, sat0.z * 0.94, 1.0]), 'film_grain_intensity': gr0 + 0.08,
       'vignette_intensity': vg0 + 0.1, 'scene_fringe_intensity': 0.35, 'color_gain_shadows': V4([0.98, 0.96, 1.04, 1.0])}
if 'EX_Look_Resonance' in ACT: A.destroy_actor(ACT['EX_Look_Resonance'])
r = A.spawn_actor_from_class(u.PostProcessVolume, u.Vector(0, 0, 0), u.Rotator(0, 0, 0))
r.set_editor_property('unbound', True); r.set_editor_property('priority', 3.0); r.set_editor_property('blend_weight', 0.0)
s = r.get_editor_property('settings')
for k, v in RES.items():
    s.set_editor_property(k, v); s.set_editor_property('override_' + k, True)
r.set_editor_property('settings', s); r.set_actor_label('EX_Look_Resonance'); r.set_folder_path('EX_PostRain_Look')
res['resonance'] = {'white_temp': RES['white_temp'], 'saturation': sat0.x * 0.94, 'grain': RES['film_grain_intensity'], 'vignette': RES['vignette_intensity'], 'blend_weight': 0.0}

# 4. save only the map
S = u.EditorLoadingAndSavingUtils
dirty_before = sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
res['dirty_before_save'] = dirty_before
MAP = '/Game/GraceRanger/Maps/L_GR_SphirusHouse'; f = PJ / 'Content/GraceRanger/Maps/L_GR_SphirusHouse.umap'
res['map_sha1_before'] = hashlib.sha1(f.read_bytes()).hexdigest()
if not DRY:
    pkgs = [p for p in S.get_dirty_map_packages() if p.get_name() == MAP]
    assert len(pkgs) == 1, ('map package not dirty/found', [p.get_name() for p in S.get_dirty_map_packages()])
    ok = S.save_packages(pkgs, False)
    res['save_ok'] = bool(ok)
    res['map_sha1_after'] = hashlib.sha1(f.read_bytes()).hexdigest(); res['map_mtime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(f.stat().st_mtime))
    res['dirty_after_save'] = sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
    # the trial backup is now stale (production = FINAL): keep it under a dated name so the next look5 run takes a fresh backup
    bk = D / 'xr5_backup.json'
    if bk.exists(): bk.rename(D / 'xr5_backup_preXR5_production.json'); res['backup_renamed'] = True
res['finished'] = time.strftime('%H:%M:%S')
(D / 'xr5_promote.json').write_text(json.dumps(res, indent=1, default=str))
print('XR5_PROMOTE', 'DRY' if DRY else 'SAVED', res.get('save_ok'), 'regions', len(ren), 'dirty_after', len(res.get('dirty_after_save', dirty_before)))
