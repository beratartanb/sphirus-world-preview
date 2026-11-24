# VF2B read-only: can this engine export / read groom strands? Lists groom-related Python classes and tries an Alembic export to Saved/.
import unreal as u, os
names = [n for n in dir(u) if any(k in n.lower() for k in ('groom', 'hairstrand', 'haircard'))]
print('PG classes', names)
g = u.load_asset('/Game/Sphirus/CharacterLab/VF2_20261124/Hair/GR_Sph_MessyBob_VF2')
print('PG groom methods', [n for n in dir(g) if not n.startswith('_') and n not in dir(u.Object)])
for cn in ('GroomEditorLibrary', 'GroomBlueprintLibrary', 'GroomAssetUtils', 'GroomExportLibrary', 'GroomBindingBuilderLibrary'):
    c = getattr(u, cn, None)
    if c: print('PG', cn, [n for n in dir(c) if not n.startswith('_') and n not in dir(u.Object)])
out = u.Paths.convert_relative_path_to_full(u.Paths.project_saved_dir()) + 'UE59Work/vf2b/groom/'; os.makedirs(out, exist_ok=True)
for ext in ('abc', 'usd', 'usda'):
    t = u.AssetExportTask(); t.object = g; t.filename = out + 'messybob.' + ext; t.automated = True; t.replace_identical = True; t.prompt = False
    try:
        ok = u.Exporter.run_asset_export_task(t); print('PG export', ext, ok, os.path.getsize(t.filename) if os.path.exists(t.filename) else None)
    except Exception as e: print('PG export', ext, 'EXC', str(e)[:160])
aid = g.get_editor_property('asset_import_data') if hasattr(g, 'get_editor_property') else None
try: print('PG source file', aid.get_first_filename() if aid else None)
except Exception as e: print('PG src', e)
for p in ('hair_groups_info', 'hair_groups_interpolation', 'hair_groups_lod'):
    try: print('PG', p, g.get_editor_property(p)[0].export_text()[:500])
    except Exception as e: print('PG', p, 'ERR', str(e)[:100])
print('PG dirty', [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()])
