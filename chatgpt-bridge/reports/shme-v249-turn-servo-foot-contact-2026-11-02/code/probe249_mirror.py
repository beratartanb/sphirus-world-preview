"""probe249_mirror.py (measure job, read-only): mirror option of every entry of the V2.48/V2.49 turning-start databases + the schema's
mirror data table (the in-game TurnL135 entry bends the feet ~110 deg while the clip, raw and compressed, keeps 35 deg). Prints MIRROR249 {...}."""
import unreal as u, json
from editor_toolset.toolsets.object import ObjectTools as O
out = {}
for s in ('L', 'R'):
    db = u.load_asset('/Game/GraceRanger/SHME/Animations/V248/PSD_SHM248_JogStartT2_' + s); r = {}
    try: r['props'] = json.loads(O.get_properties(db, ['DatabaseAnimationAssets']))
    except Exception as e: r['err'] = str(e)[:300]
    try:
        sch = db.get_editor_property('schema'); r['schema'] = sch.get_path_name()
        r['schema_props'] = json.loads(O.get_properties(sch, ['MirrorDataTable', 'Skeletons']))
    except Exception as e: r['schema_err'] = str(e)[:300]
    out[s] = r
print('MIRROR249 ' + json.dumps(out, default=str)[:20000])
