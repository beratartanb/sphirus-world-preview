"""probe3_pfr.py (measure job, read-only): target-layer settings struct, PFP landscape master expression collection (grass output / RVT /
layer blend names), FoliageType factory availability. Writes recon/probe3.json."""
import unreal as u, json, pathlib, time
D = pathlib.Path(u.Paths.project_dir()) / 'Saved/Codex/PineForestRedesign_20261104/recon'
A = u.get_editor_subsystem(u.EditorActorSubsystem); land = next(a for a in A.get_all_level_actors() if isinstance(a, u.Landscape))
out = {'started': time.strftime('%H:%M:%S')}
for nm in ('LandscapeTargetLayerSettings', 'LandscapeLayerInfoObject', 'FoliageType_InstancedStaticMeshFactory', 'FoliageTypeFactory', 'MaterialInstanceConstantFactoryNew', 'MaterialEditorOnlyData', 'MaterialExpressionCollection', 'LandscapeGrassType', 'MaterialExpressionLandscapeGrassOutput', 'MaterialExpressionRuntimeVirtualTextureOutput', 'MaterialExpressionRuntimeVirtualTextureSample', 'MaterialExpressionLandscapeLayerBlend', 'MaterialExpressionLandscapeLayerSwitch', 'MaterialExpressionLandscapeLayerSample', 'MaterialExpressionLandscapeLayerWeight'):
    out['has_' + nm] = hasattr(u, nm)
try:
    tl = land.get_editor_property('target_layers'); out['target_layers_type'] = str(type(tl)); first = None
    for k, v in tl.items():
        first = (str(k), str(type(v)), [p for p in dir(v) if not p.startswith('_')][:40]); break
    out['target_layer_entry'] = first
    try:
        s = u.LandscapeTargetLayerSettings(); out['tls_props'] = [p for p in dir(s) if not p.startswith('_')][:40]
        for p in ('layer_info_obj', 'layer_info', 'layer_info_object'):
            try:
                out['tls_' + p] = str(s.get_editor_property(p))
            except Exception as ex:
                out['tls_' + p] = 'NO'
    except Exception as ex:
        out['tls_err'] = repr(ex)[:200]
    # current layer infos
    cur = {}
    for k, v in tl.items():
        try:
            cur[str(k)] = str(v.get_editor_property('layer_info_obj'))[:120]
        except Exception as ex:
            cur[str(k)] = 'NO ' + repr(ex)[:80]
    out['current_layer_infos'] = cur
except Exception as ex:
    out['target_layers_err'] = repr(ex)[:300]
# PFP master expressions via editor-only data
ML = u.MaterialEditingLibrary
def collection(mat):
    try:
        eod = mat.get_editor_property('editor_only_data'); col = eod.get_editor_property('expression_collection')
        ex = col.get_editor_property('expressions'); return list(ex)
    except Exception as e:
        return 'NO ' + repr(e)[:200]
res = {}
for p in ('/Game/PineForestPack/Materials/Landscape/Masters/M_Landscape_PineForest', '/Game/GraceRanger/Environment/Exterior20260921/Materials/M_EX_Integration_Floor'):
    m = u.load_asset(p); ex = collection(m)
    if isinstance(ex, str):
        res[p.split('/')[-1]] = ex; continue
    info = {'n': len(ex), 'classes': {}}
    for e in ex:
        c = e.get_class().get_name(); info['classes'][c] = info['classes'].get(c, 0) + 1
        if 'LayerBlend' in c:
            try:
                info.setdefault('layer_blend', []).append([{'name': str(l.get_editor_property('layer_name')), 'blend': str(l.get_editor_property('blend_type')).split('.')[-1]} for l in e.get_editor_property('layers')])
            except Exception as er:
                info.setdefault('layer_blend_err', []).append(repr(er)[:100])
        if 'Grass' in c:
            try:
                info.setdefault('grass', []).append([{'name': str(g.get_editor_property('name')), 'type': (g.get_editor_property('grass_type').get_path_name() if g.get_editor_property('grass_type') else None)} for g in e.get_editor_property('grass_types')])
            except Exception as er:
                info.setdefault('grass_err', []).append(repr(er)[:100])
        if 'LayerSwitch' in c or 'LayerSample' in c or 'LayerWeight' in c:
            try:
                info.setdefault('layer_nodes', []).append(c + ':' + str(e.get_editor_property('parameter_name')))
            except Exception:
                info.setdefault('layer_nodes', []).append(c)
        if 'VirtualTexture' in c:
            info.setdefault('rvt', []).append(c)
        if c == 'MaterialExpressionStaticSwitchParameter' or c == 'MaterialExpressionStaticBoolParameter':
            try: info.setdefault('static_switches', []).append(str(e.get_editor_property('parameter_name')) + '=' + str(e.get_editor_property('default_value')))
            except Exception: pass
    try:
        info['use_material_attributes'] = m.get_editor_property('use_material_attributes')
    except Exception:
        pass
    res[p.split('/')[-1]] = info
out['materials'] = res
# PFP MI static switch overrides (the instance may enable RVT/grass switches)
try:
    mi = u.load_asset('/Game/PineForestPack/Materials/Landscape/Instances/MI_LandscapePineForest')
    sp = mi.get_editor_property('static_parameters') if False else None
    out['pfp_mi_static'] = {str(n): ML.get_material_instance_static_switch_parameter_value(mi, n) for n in ML.get_static_switch_parameter_names(mi)}
except Exception as ex:
    out['pfp_mi_static'] = 'NO ' + repr(ex)[:160]
# factory check for foliage types
try:
    f = u.FoliageType_InstancedStaticMeshFactory(); out['ft_factory'] = str(f)
except Exception as ex:
    out['ft_factory'] = 'NO ' + repr(ex)[:120]
out['finished'] = time.strftime('%H:%M:%S')
(D / 'probe3.json').write_text(json.dumps(out, indent=1, default=str))
print('PROBE3', json.dumps(out, default=str)[:2500])
