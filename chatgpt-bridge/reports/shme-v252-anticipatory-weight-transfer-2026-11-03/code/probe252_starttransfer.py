"""probe252_starttransfer.py (measure job, read-only): weight transfer inside the walk start-transfer clips (SHM_StartTransfer_*).
Per clip (component space with the animated root): swing foot = the one named in the clip (_Lfoot / _Rfoot steps), stance = the other;
per frame the pelvis / spine_05 position projected on the stance->swing foot axis (0 = over the stance foot centre, 1 = over the swing
foot centre), swing heel-off (ankle +1.5 cm over frame 0) and toe-off (ball +1.5 cm) times, pelvis height, and the clip's notify tracks.
Also the two start-transfer databases: entries and their notify tracks. Prints STPROBE252 {...}."""
import unreal as u, json, sys, importlib
sys.path.insert(0, r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925')
import v137_animedit as ae; importlib.reload(ae)
L = u.AnimationLibrary
F = '/Game/GraceRanger/SHME/Animations/StartTransfer/'
ar = u.AssetRegistryHelpers.get_asset_registry()
names = sorted(str(a.asset_name) for a in ar.get_assets_by_path(F[:-1], False) if str(a.asset_class_path.asset_name) == 'AnimSequence')
out = {'clips': {}, 'dbs': {}}
def proj(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; dd = dx * dx + dy * dy or 1.0
    return ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / dd
for n in names:
    seq = u.load_asset(F + n); sw = 'l' if n.endswith('_Lfoot') else 'r'; st = 'r' if sw == 'l' else 'l'
    c = ae.Clip(seq, ['foot_l', 'foot_r', 'ball_l', 'ball_r', 'pelvis', 'spine_05']); nf = c.nf; Ln = seq.get_play_length(); dt = Ln / max(1, nf - 1)
    a0 = c.comp('foot_' + sw, 0)[0][2]; b0 = c.comp('ball_' + sw, 0)[0][2]; heel = toe = None; rows = []
    for f in range(nf):
        fa = c.comp('foot_' + sw, f)[0]; ba = c.comp('ball_' + sw, f)[0]
        if heel is None and fa[2] > a0 + 1.5: heel = f
        if toe is None and ba[2] > b0 + 1.5: toe = f
        sc = [(c.comp('foot_' + st, f)[0][i] + c.comp('ball_' + st, f)[0][i]) / 2 for i in range(2)]
        wc = [(fa[i] + ba[i]) / 2 for i in range(2)]
        pe = c.comp('pelvis', f)[0]; ch = c.comp('spine_05', f)[0]
        rows.append([round(f * dt, 3), round(proj(pe, sc, wc), 2), round(proj(ch, sc, wc), 2), round(pe[2], 1)])
    tracks = [str(t) for t in L.get_animation_notify_track_names(seq)]
    out['clips'][n] = {'nf': nf, 'len': round(Ln, 3), 'swing': sw, 'heel_off': round(heel * dt, 3) if heel is not None else None, 'toe_off': round(toe * dt, 3) if toe is not None else None,
                       'pelvis_t_f0': rows[0][1], 'pelvis_t_heel': rows[heel][1] if heel is not None else None, 'pelvis_t_toe': rows[toe][1] if toe is not None else None,
                       'pelvis_t_min_before_toe': min(r[1] for r in rows[:(toe or nf)]), 'rows': rows[:min(nf, 24)], 'tracks': tracks,
                       'width_f0': round(((c.comp('foot_l', 0)[0][0] - c.comp('foot_r', 0)[0][0]) ** 2 + (c.comp('foot_l', 0)[0][1] - c.comp('foot_r', 0)[0][1]) ** 2) ** 0.5, 1)}
for s in 'LR':
    db = u.load_asset(F + 'PSD_SHM_StartTransfer_' + s)
    out['dbs'][s] = [db.get_animation_asset(i).get_name() for i in range(db.get_num_animation_assets())]
print('STPROBE252 ' + json.dumps(out))
