"""GD11 refinement B: retune the groom LOD table (fresh editor, before any QA scene holds the groom). Same structure as ue_lk_hair_lods.py
(Main: strands LOD0-2 + helmet mesh LOD3; Loose: strands LOD0-2, LOD3 hidden), denser LOD1/LOD2 and an earlier LOD3 so distant hair does not
break into a speckled thin cap. builtins.G11RD_LOD = {'grooms': {'Main': path, 'Loose': path}}"""
import unreal as u, json, builtins
C = builtins.G11RD_LOD; EAL = u.EditorAssetLibrary; out = {}
def lod_text(levels):
    TS = C.get('thickness', [1.0, 1.0, 1.0, 1.0])
    parts = ['(CurveDecimation=%f,VertexDecimation=%f,AngularThreshold=1.000000,LengthThreshold=0.000000,ThicknessScale=%f,ScreenSize=%f,bVisible=%s,GeometryType=%s)' % (cd, vd, TS[i], ss, 'True' if vis else 'False', geo) for i, (cd, vd, ss, geo, vis) in enumerate(levels)]
    return '(AutoLODBias=0.000000,LODs=(%s))' % ','.join(parts)
LV = {'Main': [(1.0, 1.0, 1.0, 'Strands', True), (0.65, 0.8, 0.5, 'Strands', True), (0.4, 0.6, 0.25, 'Strands', True), (0.1, 0.5, 0.12, 'Meshes', True)],
      'Loose': [(1.0, 1.0, 1.0, 'Strands', True), (0.65, 0.8, 0.5, 'Strands', True), (0.4, 0.6, 0.25, 'Strands', True), (0.1, 0.5, 0.12, 'Strands', False)]}
for part, p in C['grooms'].items():
    g = u.load_asset(p); lods = g.get_editor_property('hair_groups_lod'); nl = []
    for q in lods: q.import_text(lod_text(LV[part])); nl.append(q)
    g.set_editor_property('hair_groups_lod', nl); g.modify(); out[part] = {'saved': EAL.save_loaded_asset(g, False)}
    rb = g.get_editor_property('hair_groups_lod')[0].get_editor_property('lods'); out[part]['readback'] = [[round(l.get_editor_property('curve_decimation'), 2), round(l.get_editor_property('screen_size'), 2), str(l.get_editor_property('geometry_type')).split('.')[-1][:8], (round(l.get_editor_property('thickness_scale'), 2) if 'thickness_scale' in dir(l) or True else None)] for l in rb]
out['dirty'] = [x.get_path_name() for x in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]; print('G11RD_LOD', json.dumps(out))
