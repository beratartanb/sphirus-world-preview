"""GD11 refinement N: probe which groom-LOD related properties / functions are readable from Python on the live LKQA groom components, and read them.
Also reads the skeletal mesh components' forced / predicted LOD. Writes Saved/Codex/GD11_HeadRefinementN_20261005/data/lodprobe_<n>.json"""
import unreal as u, json, pathlib, datetime
R = pathlib.Path(u.Paths.project_dir()).resolve(); out = {'read_at': datetime.datetime.now().isoformat(timespec='seconds'), 'components': {}}
for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors():
    lab = a.get_actor_label()
    if not lab.startswith('LKQA_'): continue
    gc = a.get_component_by_class(u.GroomComponent); sk = a.get_component_by_class(u.SkeletalMeshComponent); rec = {}
    if gc:
        names = [n for n in dir(gc) if 'lod' in n.lower()]; rec['lod_attrs'] = names
        for n in names:
            try:
                v = getattr(gc, n); rec[n] = str(v() if callable(v) else v)[:200]
            except Exception as e: rec[n] = 'ERR %s' % str(e)[:120]
        g = gc.get_editor_property('groom_asset')
        if g:
            try: rec['asset_lod_count'] = len(g.get_editor_property('hair_groups_lod')[0].get_editor_property('lods'))
            except Exception as e: rec['asset_lod_count'] = 'ERR %s' % e
        try: rec['bounds_sphere_radius'] = float(gc.bounds.sphere_radius)
        except Exception: pass
    if sk:
        for n in ('forced_lod_model', 'predicted_lod_level', 'min_lod_model'):
            try: rec[n] = sk.get_editor_property(n)
            except Exception as e: rec[n] = 'ERR %s' % str(e)[:80]
        try: rec['get_num_lods'] = sk.get_num_lods()
        except Exception: pass
    if rec: out['components'][lab] = rec
n = len(list((R/'Saved/Codex/GD11_HeadRefinementN_20261005/data').glob('lodprobe_*.json')))+1
(R/'Saved/Codex/GD11_HeadRefinementN_20261005/data'/('lodprobe_%d.json' % n)).write_text(json.dumps(out, indent=1)); print('G11RN_LODPROBE', json.dumps(out)[:1500])
