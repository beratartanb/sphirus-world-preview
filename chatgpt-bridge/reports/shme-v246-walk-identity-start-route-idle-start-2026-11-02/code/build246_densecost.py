"""build246_densecost.py (editor job): V2.46 walk identity, second step - the whole Dense (Ranger/Neutral) FORWARD walk-loop family competes
with the LB forward loop after every start (costing one clip only moved the first 1.45 s to its siblings F_L_20 / F_R_20). Adds a full-window
PoseSearchModifyCost (cost_addend, default 6.0) to every PSD_Dense_Stand_Walk_Loops entry whose name matches the forward family
(Walk_Loop_F, _FL, _FR, _F_L_20, _F_R_20; project-integrated copies under /Game/ActionAdventureMovementS/.../Integrated, not vendor).
'dry': True only lists the clip paths (for the write manifest). 'remove': True strips the track. Prints DCOST246 {...}."""
import unreal as u, json, builtins
L = u.AnimationLibrary; EAL = u.EditorAssetLibrary
c = dict(getattr(builtins, 'V246_DC', {})); DRY = bool(c.get('dry', True)); ADD = float(c.get('cost_addend', 6.0)); REMOVE = bool(c.get('remove', False)); tr = 'SHME_V246_Cost'
db = u.load_asset('/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/PSD_Dense_Stand_Walk_Loops'); assert db
pats = ('Walk_Loop_F', 'Walk_Loop_FL', 'Walk_Loop_FR', 'Walk_Loop_F_L_20', 'Walk_Loop_F_R_20')
clips = []
for i in range(db.get_num_animation_assets()):
    a = db.get_animation_asset(i); n = a.get_name()
    base = n.split('_Phase')[0]
    if any(base.endswith(p) for p in pats): clips.append(a.get_path_name().split('.')[0])
out = {'dry': DRY, 'cost_addend': ADD, 'clips': clips, 'done': []}
if not DRY:
    for p in clips:
        s = u.load_asset(p); names = [str(t) for t in L.get_animation_notify_track_names(s)]
        if tr in names: L.remove_animation_notify_events_by_track(s, tr); L.remove_animation_notify_track(s, tr)
        if not REMOVE:
            ln = float(s.get_play_length()); L.add_animation_notify_track(s, tr)
            mc = L.add_animation_notify_state_event(s, tr, 0.0, ln, u.AnimNotifyState_PoseSearchModifyCost); mc.set_editor_property('cost_addend', ADD)
        out['done'].append([p.split('/')[-1], EAL.save_asset(p, False)])
out['dirty'] = [q.get_name() for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]
print('DCOST246 ' + json.dumps(out, default=str))
json.dump(clips, open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V246_20261101/data/dense_fwd_clips.json', 'w'))
