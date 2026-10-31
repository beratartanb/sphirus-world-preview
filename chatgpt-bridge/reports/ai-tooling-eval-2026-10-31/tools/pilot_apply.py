"""pilot_apply.py (WRITE job under a manifest; NEVER saves): apply or restore P1 instance moves in the editor world, in memory only.

builtins.PILOT_GROUPS = ['G1_nearfield', ...]; builtins.PILOT_MODE = 'apply' | 'restore'.
Native foliage path used by the earlier environment passes (PostRain/RefugeArtDirection): the FoliageType of a component is the one with the
same mesh AND the same cull distance (several types share a mesh); all transforms of that type are read, the moved ones replaced, then
InstancedFoliageActor.remove_all_instances + add_instances, so the foliage type data and the component agree. Instances are found by
location (+-2 cm of the plan's original position for 'apply', of the target for 'restore'), not by index (indices change on rebuild).
After the change: every moved instance is re-found at its new location and the per-type instance count is checked unchanged.
Output: <PILOT>/apply_<mode>_<groups>.json
"""
import unreal as u, json, os, builtins, math

PILOT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\pilot'
GROUPS = list(getattr(builtins, 'PILOT_GROUPS', []))
MODE = getattr(builtins, 'PILOT_MODE', 'apply')
assert GROUPS and MODE in ('apply', 'restore'), (GROUPS, MODE)
assert 'G4_lookback_window' not in GROUPS, 'G4 is not part of this test'
plan = json.load(open(os.path.join(PILOT, 'plan_p1_resolved.json')))
moves = [m for m in plan['moves'] if m['group'] in GROUPS]
E = u.get_editor_subsystem(u.UnrealEditorSubsystem)
assert E.get_game_world() is None, 'PIE running'
w = E.get_editor_world(); assert w.get_path_name().startswith('/Game/GraceRanger/Maps/L_GR_SphirusHouse.')
actors = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
ifas = [a for a in actors if a.get_class().get_name() == 'InstancedFoliageActor']
reg = u.AssetRegistryHelpers.get_asset_registry()
FT_DIR = '/Game/GraceRanger/Environment/Exterior20260921/Foliage'
fts = [ad.get_asset() for ad in reg.get_assets_by_path(FT_DIR, True)]
fts = [t for t in fts if isinstance(t, u.FoliageType_InstancedStaticMesh)]


def comps():
    return [c for a in ifas for c in a.get_components_by_class(u.FoliageInstancedStaticMeshComponent)]


def ft_of(c):
    found = [t for t in fts if t.get_editor_property('mesh') == c.static_mesh and t.get_editor_property('cull_distance').min == c.get_editor_property('instance_start_cull_distance')
             and t.get_editor_property('cull_distance').max == c.get_editor_property('instance_end_cull_distance')]
    return found


def tf(d):
    return u.Transform(location=u.Vector(*d['loc']), rotation=u.Rotator(pitch=d['rot_pyr'][0], yaw=d['rot_pyr'][1], roll=d['rot_pyr'][2]), scale=u.Vector(*d['scale']))


def near(t, loc, tol=2.0):
    L = t.translation; return abs(L.x - loc[0]) < tol and abs(L.y - loc[1]) < tol and abs(L.z - loc[2]) < tol


S = u.EditorLoadingAndSavingUtils
res = {'mode': MODE, 'groups': GROUPS, 'n_moves': len(moves), 'per_type': {}, 'moves': [], 'problems': [],
       'dirty_before': sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])}
by_comp = {}
for m in moves:
    # the component is always located by mesh + the instance at the source location (a remove_all/add_instances rebuild renames components,
    # so the plan's component path can point at a different component afterwards)
    src_loc = (m['original'] if MODE == 'apply' else m['target'])['loc']
    c = next((x for x in comps() if x.static_mesh and x.static_mesh.get_name() == m['mesh'] and any(near(x.get_instance_transform(i, True), src_loc)
                                                                                             for i in range(x.get_instance_count()))), None)
    if c is None:
        res['problems'].append('component not found %s' % m['comp']); continue
    by_comp.setdefault(c.get_path_name(), (c, []))[1].append(m)
todo = []
for cp, (c, ms) in by_comp.items():
    f = ft_of(c)
    if len(f) != 1:
        res['problems'].append('foliage type not unique for %s: %s' % (cp, [t.get_path_name() for t in f])); continue
    ft = f[0]
    ts = [c.get_instance_transform(i, True) for i in range(c.get_instance_count())]
    n0 = len(ts)
    for m in ms:
        src, dst = (m['original'], m['target']) if MODE == 'apply' else (m['target'], m['original'])
        hit = [i for i, t in enumerate(ts) if near(t, src['loc'])]
        if len(hit) != 1:
            res['problems'].append('instance not found uniquely %s %s at %s (%d hits)' % (m['mesh'], m['group'], src['loc'], len(hit))); continue
        ts[hit[0]] = tf(dst)
        res['moves'].append({'group': m['group'], 'mesh': m['mesh'], 'foliage_type': ft.get_path_name(), 'from': src, 'to': dst})
    todo.append((ft, ts, n0, c.static_mesh.get_name()))
if res['problems']:
    raise RuntimeError('REFUSED before any change: %s' % res['problems'])
with u.ScopedEditorTransaction('P1 pilot %s %s (unsaved test)' % (MODE, '+'.join(GROUPS))):
    for ft, ts, n0, mesh in todo:
        u.InstancedFoliageActor.remove_all_instances(w, ft)
        u.InstancedFoliageActor.add_instances(w, ft, ts)
# verify
for ft, ts, n0, mesh in todo:
    cs = [c for c in comps() if ft_of(c) == [ft]]
    n1 = sum(c.get_instance_count() for c in cs)
    res['per_type'][ft.get_path_name()] = {'mesh': mesh, 'count_before': n0, 'count_after': n1, 'equal': n0 == n1}
for mv in res['moves']:
    cs = [c for c in comps() if c.static_mesh and c.static_mesh.get_name() == mv['mesh']]
    mv['found_at_new_location'] = any(near(c.get_instance_transform(i, True), mv['to']['loc']) for c in cs for i in range(c.get_instance_count()))
res['all_found'] = all(m['found_at_new_location'] for m in res['moves'])
res['counts_equal'] = all(v['equal'] for v in res['per_type'].values())
res['dirty_after'] = sorted([p.get_name() for p in S.get_dirty_content_packages()] + [p.get_name() for p in S.get_dirty_map_packages()])
json.dump(res, open(os.path.join(PILOT, 'apply_%s_%s.json' % (MODE, '+'.join(g.split('_')[0] for g in GROUPS))), 'w'), indent=1, default=str)
print('PILOT_%s groups %s moves %d all_found %s counts_equal %s dirty %s' % (MODE.upper(), GROUPS, len(res['moves']), res['all_found'], res['counts_equal'], res['dirty_after']))
