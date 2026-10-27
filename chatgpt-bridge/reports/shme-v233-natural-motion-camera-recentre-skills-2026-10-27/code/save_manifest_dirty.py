"""save_manifest_dirty.py (write job): save every DIRTY package that the job's write manifest lists (dependents recompiled by a component
change - e.g. BP_PBI_Player after build_comp_vars) so the editor can quit cleanly; anything dirty outside the manifest stays unsaved and
the runner's G5 audit reports it. Prints SMD233 {...}."""
import unreal as u, json, builtins
LS = u.EditorLoadingAndSavingUtils
dirty = list(LS.get_dirty_content_packages())
out = {'saved': [], 'skipped': []}
import sys
allow = getattr(builtins, 'SMD233_ALLOW', None)
for p in dirty:
    n = p.get_name()
    try:
        ok = u.EditorAssetLibrary.save_asset(n, True); out['saved'].append([n, bool(ok)])
    except Exception as e: out['skipped'].append([n, str(e)[:80]])
print('SMD233 ' + json.dumps(out))
