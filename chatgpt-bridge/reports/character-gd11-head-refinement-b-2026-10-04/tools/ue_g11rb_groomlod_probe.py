"""GD11 refinement B: groom LOD probe (read-only). Reports the LOD table of the given grooms (geometry type per LOD: strands / cards / meshes,
screen size, curve / vertex decimation) and, on the QA-scene groom components, forces each LOD and reads back what the component reports.
builtins.G11RB_GL = {'grooms': [paths], 'out': abs json}"""
import unreal as u, json, builtins
C = builtins.G11RB_GL; out = {'assets': {}, 'components': {}}
def props(o, names):
    d = {}
    for n in names:
        try:
            v = o.get_editor_property(n); d[n] = str(v)[:120] if not isinstance(v, (int, float, bool)) else v
        except Exception: pass
    return d
for p in C['grooms']:
    g = u.load_asset(p); a = {'lod_mode': str(g.get_editor_property('lod_mode'))}
    try:
        groups = g.get_editor_property('hair_groups_lod'); a['groups'] = []
        for gi, grp in enumerate(groups):
            lods = grp.get_editor_property('lods'); a['groups'].append([props(l, ('geometry_type', 'screen_size', 'curve_decimation', 'vertex_decimation', 'angular_threshold', 'visible', 'bind_type', 'simulation')) for l in lods])
    except Exception as e: a['groups_err'] = str(e)[:200]
    for k in ('hair_groups_cards', 'hair_groups_meshes'):
        try: a[k] = len(g.get_editor_property(k))
        except Exception as e: a[k] = str(e)[:80]
    out['assets'][p.split('/')[-1]] = a
world = u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
comps = []
for act in u.GameplayStatics.get_all_actors_of_class(world, u.Actor):
    for gc in act.get_components_by_class(u.GroomComponent): comps.append(gc)
for gc in comps:
    nm = gc.get_name(); r = {'groom': gc.get_editor_property('groom_asset').get_name() if gc.get_editor_property('groom_asset') else None,
                             'binding': gc.get_editor_property('binding_asset').get_name() if gc.get_editor_property('binding_asset') else None}
    tried = {}
    for L in (-1, 0, 1, 2, 3):
        try:
            gc.set_forced_lod(L); rb = {}
            for f in ('get_forced_lod', 'get_desired_sync_lod', 'get_num_lods', 'get_lod_count'):
                if hasattr(gc, f):
                    try: rb[f] = getattr(gc, f)()
                    except Exception as e: rb[f] = 'ERR ' + str(e)[:60]
            tried[str(L)] = rb or 'set ok (no readback API)'
        except Exception as e: tried[str(L)] = 'ERR ' + str(e)[:100]
    r['forced_lod_test'] = tried; r['api'] = [x for x in dir(gc) if 'lod' in x.lower() or 'force' in x.lower()]; r['props'] = props(gc, ('forced_lod', 'lod_bias', 'use_cards', 'simulation_settings', 'enable_simulation'))
    out['components'][nm] = r
open(C['out'], 'w').write(json.dumps(out, indent=1)); print('G11RB_GL', json.dumps(out)[:3000])
# console variables that control groom LOD in this engine build
cv = {}
for n in ('r.HairStrands.LODMode', 'r.HairStrands.ForceLOD', 'r.HairStrands.LOD.Force', 'r.HairStrands.Enable', 'r.HairStrands.Cards', 'r.HairStrands.Meshes', 'r.HairStrands.Strands'):
    try: cv[n] = u.SystemLibrary.get_console_variable_int_value(n)
    except Exception as e: cv[n] = 'n/a'
out['cvars'] = cv; open(C['out'], 'w').write(json.dumps(out, indent=1)); print('G11RB_GL2', json.dumps(cv))
