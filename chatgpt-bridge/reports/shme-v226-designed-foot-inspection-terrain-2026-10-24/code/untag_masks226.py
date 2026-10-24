"""untag_masks226.py (editor job): ROLLBACK of tag_masks226 - removes the actor tag GR_Inspect on the four R05
workshop masks (and nothing else). Checkpoint: Saved/Codex/SHME_V226_20261024/checkpoint/pre_v226/L_GR_SphirusHouse.umap.
Finds the actors by label in the loaded editor world (L_GR_SphirusHouse), adds the tag when missing, saves ONLY the level packages that
own those actors (never save_dirty_packages: other packages are not ours). Reads the tags back from the saved package. builtins.V226_TAG_SAVE
saves (default dry). Prints TAG226 {...}."""
import unreal as u, json, builtins
SAVE = bool(getattr(builtins, "V226_TAG_SAVE", False)); TAG = "GR_Inspect"; REMOVE = True
LABELS = ['R05_Workshop_Mask_Silent', 'R05_Workshop_Mask_Gilded', 'R05_Workshop_Mask_Cerulean', 'R05_Workshop_Mask_Cracked']
ELS = u.get_editor_subsystem(u.UnrealEditorSubsystem); w = ELS.get_editor_world(); out = {'world': w.get_name(), 'save': SAVE, 'actors': {}}
assert ELS.get_game_world() is None, 'PIE running'
acts = u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()
levels = set()
for a in acts:
    nm = a.get_actor_label()
    if nm in LABELS:
        tags = [str(t) for t in a.tags]
        if TAG in tags:   # ROLLBACK of tag_masks226: remove the tag
            a.modify(True); a.tags = [u.Name(t) for t in tags if t != TAG]
        lvl = a.get_outer()   # the level the actor lives in
        pkg = lvl.get_outermost(); levels.add(pkg.get_name())
        out['actors'][nm] = {'tags': [str(t) for t in a.tags], 'level': pkg.get_name(), 'class': a.get_class().get_name(), 'loc': [round(v) for v in (a.get_actor_location().x, a.get_actor_location().y, a.get_actor_location().z)]}
out['levels'] = sorted(levels); out['found'] = len(out['actors'])
if SAVE and out['found'] == 4:
    saved = []
    for pkgname in sorted(levels):
        ok = u.EditorLoadingAndSavingUtils.save_packages([u.load_package(pkgname)], False); saved.append([pkgname, bool(ok)])
    out['saved'] = saved
    out['dirty_after'] = [p.get_name() for p in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('TAG226 ' + json.dumps(out, default=str))
