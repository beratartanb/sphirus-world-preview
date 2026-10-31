"""abp_dump.py : read-only dump of the two SHME AnimBlueprints for a disk-vs-memory comparison.
Run (a) as a measure job in the running editor -> the IN-MEMORY state, and (b) in a separate headless commandlet
(UnrealEditor-Cmd -run=pythonscript) -> the ON-DISK state. Same code, tag from builtins/argv/env ABP_DUMP_TAG.
Writes, per ABP: <OUT>/<tag>/<name>.t3d (ObjectExporterT3D text export of the Blueprint: graphs, nodes, pin links, variable
descriptions) and <name>.cdo.t3d (T3D of the generated-class default object = every variable default).
Nothing is saved, compiled, reverted or reloaded.
"""
import unreal as u, json, os, sys

OUT = r'C:\Users\berat\AppData\Local\Temp\claude\C--Users-berat-OneDrive-Documents-Unreal-Projects-ActionAdventureMovementS\5f49a232-b001-47ad-8881-1eb04d9cb1c5\scratchpad\abpdiff'
TAG = os.environ.get('ABP_DUMP_TAG') or (sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in ('mem', 'disk') else 'mem')
ABPS = ['/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatching',
        '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase']
D = os.path.join(OUT, TAG)
os.makedirs(D, exist_ok=True)


def txt(v):
    if hasattr(v, 'get_path_name') and not isinstance(v, str):
        return v.get_path_name()
    if isinstance(v, float):
        return repr(round(v, 6))
    try:
        return str(v.export_text()) if hasattr(v, 'export_text') else str(v)
    except Exception:
        return str(v)


summary = {'tag': TAG, 'abps': {}}
for path in ABPS:
    name = path.rsplit('/', 1)[-1]
    bp = u.load_asset(path)
    cdo = u.get_default_object(bp.generated_class())
    rows = {}
    t = u.AssetExportTask()
    t.set_editor_property('object', bp)
    t.set_editor_property('filename', os.path.join(D, name + '.t3d'))
    t.set_editor_property('exporter', u.ObjectExporterT3D())
    t.set_editor_property('automated', True)
    t.set_editor_property('prompt', False)
    t.set_editor_property('replace_identical', True)
    ok = u.Exporter.run_asset_export_task(t)
    f = os.path.join(D, name + '.t3d')
    # the generated-class CDO (all variable defaults) as its own T3D text
    t2 = u.AssetExportTask()
    t2.set_editor_property('object', cdo)
    t2.set_editor_property('filename', os.path.join(D, name + '.cdo.t3d'))
    t2.set_editor_property('exporter', u.ObjectExporterT3D())
    t2.set_editor_property('automated', True)
    t2.set_editor_property('prompt', False)
    t2.set_editor_property('replace_identical', True)
    ok2 = u.Exporter.run_asset_export_task(t2)
    f2 = os.path.join(D, name + '.cdo.t3d')
    summary['abps'][name] = {'t3d_ok': bool(ok), 't3d_bytes': os.path.getsize(f) if os.path.exists(f) else 0,
                             'cdo_t3d_ok': bool(ok2), 'cdo_t3d_bytes': os.path.getsize(f2) if os.path.exists(f2) else 0,
                             'generated_class': bp.generated_class().get_path_name()}
dirty = sorted(p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages())
summary['dirty_content_packages_after'] = dirty
json.dump(summary, open(os.path.join(D, 'summary.json'), 'w'), indent=1)
print('ABP_DUMP', json.dumps(summary))
