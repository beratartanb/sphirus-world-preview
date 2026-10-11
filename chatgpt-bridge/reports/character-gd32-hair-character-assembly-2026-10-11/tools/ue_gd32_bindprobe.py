"""GD32 probe (no saves): why the HairMain / HairLoose / Eyelashes binding assets did not stick on the Blueprint groom templates. Prints each
binding's groom / source / target mesh and group count, then tries set_binding_asset() on the placed instance's components and reads back."""
import unreal as u, json, pathlib
R = pathlib.Path(u.Paths.project_dir()).resolve(); O = R/'Saved/Codex/GD32_Identity_20261011/data'; G31 = '/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011'
B = {'HairMain': G31+'/Face/Bindings/GB_GD31_HairMain_g31cbh75c', 'HairLoose': G31+'/Face/Bindings/GB_GD31_HairLoose_g31cbh75c', 'Eyelashes': G31+'/Face/Bindings/GB_GD31_EyelashesS_Thin_g31cb', 'Eyebrows': G31+'/Face/Bindings/GB_GD31_EyebrowsCustom_c4_g31'}
out = {}
def pn(o): return o.get_path_name() if o is not None else None
def gp(o, k):
    try: v = o.get_editor_property(k); return pn(v) if isinstance(v, u.Object) else str(v)[:120]
    except Exception as e: return 'ERR '+repr(e)[:80]
for n, p in B.items():
    b = u.load_asset(p); out[n] = {k: gp(b, k) for k in ('groom', 'target_skeletal_mesh', 'source_skeletal_mesh', 'target_binding_attribute', 'num_interpolation_points', 'group_infos')}
    try: out[n]['binding_type'] = gp(b, 'groom_binding_type')
    except Exception: pass
eas = u.get_editor_subsystem(u.EditorActorSubsystem)
ch = [a for a in eas.get_all_level_actors() if a.get_actor_label() == 'GD32_Character_G31'][0]
for g in ch.get_components_by_class(u.GroomComponent):
    n = g.get_name(); before = pn(g.binding_asset)
    try: g.set_binding_asset(u.load_asset(B[n])); r = 'called'
    except Exception as e: r = repr(e)[:120]
    out[n]['instance'] = {'groom': pn(g.groom_asset), 'before': before, 'set': r, 'after': pn(g.binding_asset), 'parent_mesh': pn(g.get_attach_parent().skeletal_mesh_asset) if isinstance(g.get_attach_parent(), u.SkeletalMeshComponent) else None}
(O/'bindprobe.json').write_text(json.dumps(out, indent=1)); print('GD32_BINDPROBE', json.dumps({k: (v['instance']['after'] is not None) for k, v in out.items()}))
