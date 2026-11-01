import unreal as u, json
ct = u.load_asset('/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/CHT_PBI_PlayerDense'); out = {'cls': ct.get_class().get_name(), 'props': {}}
for pr in ('results_structs', 'columns_structs', 'output_object_type', 'result_type', 'fallback_result', 'results', 'columns'):
    try: v = ct.get_editor_property(pr); out['props'][pr] = str(v)[:1500]
    except Exception as ex: out['props'][pr] = 'ERR ' + str(ex)[:50]
try: out['export'] = u.SystemLibrary.get_display_name(ct)
except Exception: pass
try:
    txt = u.EditorAssetLibrary.get_path_name_for_loaded_asset(ct); out['path'] = txt
except Exception: pass
try:
    from unreal import ChooserFunctionLibrary as CF; out['cflib'] = [x for x in dir(CF) if not x.startswith('_')][:40]
except Exception as ex: out['cflib_err'] = str(ex)[:80]
out['dir'] = [x for x in dir(ct) if not x.startswith('_') and ('result' in x.lower() or 'column' in x.lower() or 'row' in x.lower())][:40]
print('CHT245 ' + json.dumps(out, default=str))
