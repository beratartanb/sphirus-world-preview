# probe_chooser2.py (read-only): export the Relaxed chooser table as text (rows/results) to Saved/UE59Work/probe/chooser_export.txt
import unreal as u
c = u.load_asset('/Game/Sphirus/Player/GASP/Choosers/CHT_Sph_PoseSearchDatabases_Relaxed')
t = u.AssetExportTask(); t.object = c; t.filename = u.Paths.project_dir() + 'Saved/UE59Work/probe/chooser_export.copy'; t.automated = True; t.prompt = False; t.replace_identical = True
ok = u.Exporter.run_asset_export_task(t); print('EXPORT', ok, [str(e) for e in t.errors][:3])
