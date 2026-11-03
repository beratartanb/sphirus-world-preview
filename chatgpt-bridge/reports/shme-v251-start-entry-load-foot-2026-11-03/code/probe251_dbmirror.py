"""probe251_dbmirror.py (measure job, read-only): per PoseSearch database used by the jog starts / lateral starts / stops: schema, its mirror
data table, normalization set, and every entry's animation + mirror option (export text of DatabaseAnimationAssets). Prints DBMIRROR251 {...}."""
import unreal as u, json, re
DBS = ['/Game/GraceRanger/SHME/Animations/V237/PSD_SHM237_JogStartS_L', '/Game/GraceRanger/SHME/Animations/V237/PSD_SHM237_JogStartS_R',
       '/Game/GraceRanger/SHME/Animations/V248/PSD_SHM248_JogStartT2_L', '/Game/GraceRanger/SHME/Animations/V248/PSD_SHM248_JogStartT2_R']
ar = u.AssetRegistryHelpers.get_asset_registry(); out = {}
allp = {str(a.asset_name): str(a.package_name) for a in ar.get_assets_by_class(u.TopLevelAssetPath('/Script/PoseSearch', 'PoseSearchDatabase'), True)}
for n in ('PSD_SHM237_JogStartS_L', 'PSD_SHM237_JogStartS_R', 'PSD_SHM248_JogStartT2_L', 'PSD_SHM248_JogStartT2_R', 'PSD_LS_CoreLateralStart', 'PSD_SHM216_RevTurn', 'PSD_SHM237_JogResume', 'PSD_CT_JogSteady'):
    p = allp.get(n)
    if not p:
        cand = [k for k in allp if n.lower() in k.lower()]; out[n] = {'missing': cand[:5]}; continue
    db = u.load_asset(p); r = {'path': p}
    try:
        sch = db.get_editor_property('schema'); r['schema'] = sch.get_path_name()
        t = sch.export_text() if hasattr(sch, 'export_text') else ''
    except Exception as e: r['schema_err'] = str(e)[:100]
    try: r['norm'] = str(db.get_editor_property('normalization_set').get_path_name()) if db.get_editor_property('normalization_set') else None
    except Exception as e: r['norm_err'] = str(e)[:80]
    try:
        from editor_toolset.toolsets.object import ObjectTools as O
        sp = json.loads(O.get_properties(sch, ['Skeletons'])); r['mirror_table'] = [s.get('mirrorDataTable') for s in sp.get('Skeletons', [])]
        ents = json.loads(O.get_properties(db, ['DatabaseAnimationAssets'])).get('DatabaseAnimationAssets', [])
        r['entries'] = [[str(e)[:220]] for e in ents][:60]
    except Exception as e: r['entries_err'] = str(e)[:200]
    r['n'] = db.get_num_animation_assets()
    r['names'] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
    out[n] = r
print('DBMIRROR251 ' + json.dumps(out, default=str))
