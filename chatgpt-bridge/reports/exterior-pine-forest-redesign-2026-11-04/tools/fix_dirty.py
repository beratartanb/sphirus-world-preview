"""fix_dirty.py (control job): in a freshly opened editor nothing should be dirty; packages that come back dirty straight after load
(vendor material instances such as MI_FallenNeedle) are reloaded from disk (never saved) so the Bridge export's clean-state assertion holds.
Refuses to touch the map package or anything under the owned Exterior20260921 folder (those would be real edits).
Output: Saved/Codex/PineForestRedesign_20261104/design/fix_dirty.json"""
import unreal as u, json, pathlib
PJ = pathlib.Path(u.Paths.project_dir()); OUT = PJ / 'Saved/Codex/PineForestRedesign_20261104/design/fix_dirty.json'
S = u.EditorLoadingAndSavingUtils
dm = [p.get_name() for p in S.get_dirty_map_packages()]; dc = list(S.get_dirty_content_packages())
res = {'dirty_maps_before': dm, 'dirty_content_before': [p.get_name() for p in dc], 'reloaded': [], 'kept': [], 'problems': []}
todo = [p for p in dc if not p.get_name().startswith('/Game/GraceRanger/Environment/Exterior20260921/')]
res['kept'] = [p.get_name() for p in dc if p not in todo]
if todo:
    try:
        r = S.reload_packages(todo, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE); res['reloaded'] = [p.get_name() for p in todo]; res['reload_result'] = str(r)
    except Exception as ex: res['problems'].append(repr(ex)[:120])
res['dirty_maps_after'] = [p.get_name() for p in S.get_dirty_map_packages()]; res['dirty_content_after'] = [p.get_name() for p in S.get_dirty_content_packages()]
OUT.write_text(json.dumps(res, indent=1)); print('FIX_DIRTY', res)
