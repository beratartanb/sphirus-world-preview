exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
import json
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); out = {}
for g in B.list_graphs(bp):
    for n in B.find_nodes(g):
        if 'EvaluateChooser' in n.get_class().get_name():
            e = {'graph': g.get_name(), 'node': n.get_name(), 'props': {}}
            for pr in ('chooser', 'chooser_table', 'table', 'chooser_asset', 'result_type', 'mode'):
                try: e['props'][pr] = str(n.get_editor_property(pr))[:160]
                except Exception as ex: e['props'][pr] = 'ERR ' + str(ex)[:40]
            try: e['export'] = u.EditorAssetLibrary.get_metadata_tag(n, 'x') or ''
            except Exception: pass
            try:
                txt = str(n.export_text()) if hasattr(n, 'export_text') else ''
                e['export_text'] = txt[:400]
            except Exception as ex: e['export_err'] = str(ex)[:60]
            out[n.get_name()] = e
ar = u.AssetRegistryHelpers.get_asset_registry()
ch = [str(a.package_name) for a in ar.get_assets_by_path('/Game', True) if 'Chooser' in str(a.asset_class_path.asset_name) or 'Chooser' in str(a.asset_name)]
out['chooser_assets'] = ch[:20]
print('CHOOSER245 ' + json.dumps(out, default=str))
