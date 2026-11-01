"""pre242_idle.py / post242_idle.py (per-run PRE/POST, in memory, never saved): A/B hook for the V2.42 weighted idle without touching
production assets on disk. PRE replaces the production idle sequence (af_Stand_Idle_NaturalBaseline_Phase275) inside the live idle
database PSD_Dense_Stand_Idles (the Integrated copy the chooser / ABP reference) with SHM242_Idle_Weighted; the database re-indexes at
PIE start. POST (builtins.V242_IDLE_POST = True) reloads the database package from disk. Prints PREIDLE / POSTIDLE {...}.
builtins.V242_IDLE_DB overrides the database path, builtins.V242_IDLE_CLIP the replacement clip."""
import unreal as u, json, builtins
DB = getattr(builtins, 'V242_IDLE_DB', '/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/PSD_Dense_Stand_Idles')
CLIP = getattr(builtins, 'V242_IDLE_CLIP', '/Game/GraceRanger/SHME/Animations/V242/SHM242_Idle_Weighted')
POST = bool(getattr(builtins, 'V242_IDLE_POST', False))
assert u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world() is None, 'PIE running'
db = u.load_asset(DB); assert db, DB
S = u.EditorLoadingAndSavingUtils
if POST:
    pk = [p for p in S.get_dirty_content_packages() if p.get_name() == DB]
    ok = S.reload_packages(pk, u.ReloadPackagesInteractionMode.ASSUME_POSITIVE) if pk else None
    db = u.load_asset(DB); names = [str(x.get_editor_property('sequence').get_name()) if x.get_editor_property('sequence') else None for x in db.get_editor_property('animation_assets') if isinstance(x, u.PoseSearchDatabaseSequence)]
    print('POSTIDLE ' + json.dumps({'reloaded': bool(pk), 'ok': str(ok), 'has_weighted': any(n and 'SHM242_Idle' in n for n in names), 'dirty': [p.get_name() for p in S.get_dirty_content_packages()]}))
else:
    new = u.load_asset(CLIP); assert new, CLIP
    arr = list(db.get_editor_property('animation_assets')); hit = []
    for i, e in enumerate(arr):
        if isinstance(e, u.PoseSearchDatabaseSequence):
            sq = e.get_editor_property('sequence')
            if sq and 'NaturalBaseline_Phase275' in sq.get_name():
                e.set_editor_property('sequence', new); arr[i] = e; hit.append(i)
    db.set_editor_property('animation_assets', arr); db.modify()
    print('PREIDLE ' + json.dumps({'db': DB, 'replaced_entries': hit, 'n': len(arr), 'dirty': [p.get_name().split('/')[-1] for p in S.get_dirty_content_packages()]}))
