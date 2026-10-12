"""GD43: markdown comparison table of the anthropometric JSONs (gd43_anthro.py) for several candidates against the norm bands.
usage: python gd43_anthro_table.py <out.md> label=path.json ..."""
import sys, json
out = sys.argv[1]; cols = [a.split('=', 1) for a in sys.argv[2:]]; D = {l: json.load(open(p)) for l, p in cols}
H = 173.27
NORM = {'bust_circ': (86, 92), 'underbust_circ': (73, 78), 'waist_circ': (66, 73), 'navel_circ': (70, 78), 'hip_circ': (93, 99), 'thigh_upper_circ': (54, 59), 'thigh_mid_circ': (47, 52), 'knee_circ': (35, 38.5), 'calf_circ': (34, 37.5), 'ankle_circ': (20.5, 23),
        'upper_arm_circ': (25.5, 28.5), 'forearm_circ': (22.5, 25), 'wrist_circ': (14.8, 16.2), 'shoulder_w_at_acromion': (40, 45), 'bust_point_distance': (18, 21.5), 'waist_w': (23.5, 26.5), 'waist_d': (18, 21), 'waist_wd_ratio': (1.18, 1.42), 'hip_w': (33, 36.5), 'hip_d': (22, 26), 'hip_wd_ratio': (1.3, 1.6),
        'crotch_z': (0.46*H, 0.485*H), 'knee_joint_z': (0.27*H, 0.295*H), 'acromion_z_est': (0.80*H, 0.83*H), 'upper_arm_len': (0.16*H, 0.178*H), 'forearm_len': (0.138*H, 0.156*H), 'thigh_len': (0.235*H, 0.26*H), 'shank_len': (0.23*H, 0.255*H)}
TR = {'bust_circ': 'göğüs çevresi (meme ucu seviyesi)', 'underbust_circ': 'göğüs altı çevresi', 'waist_circ': 'bel çevresi (en dar)', 'navel_circ': 'göbek çevresi', 'hip_circ': 'kalça çevresi (en geniş)', 'thigh_upper_circ': 'üst uyluk çevresi', 'thigh_mid_circ': 'orta uyluk çevresi', 'knee_circ': 'diz çevresi', 'calf_circ': 'baldır çevresi', 'ankle_circ': 'bilek çevresi (ayak)',
      'upper_arm_circ': 'üst kol çevresi', 'forearm_circ': 'ön kol çevresi', 'wrist_circ': 'el bileği çevresi', 'shoulder_w_at_acromion': 'omuz genişliği (akromion seviyesi)', 'bust_point_distance': 'meme ucu arası', 'waist_w': 'bel genişliği', 'waist_d': 'bel derinliği', 'waist_wd_ratio': 'bel genişlik/derinlik', 'hip_w': 'kalça genişliği', 'hip_d': 'kalça derinliği', 'hip_wd_ratio': 'kalça genişlik/derinlik',
      'crotch_z': 'kasık yüksekliği', 'knee_joint_z': 'diz eklemi yüksekliği', 'acromion_z_est': 'akromion yüksekliği (tahmin)', 'upper_arm_len': 'üst kol (eklem-eklem)', 'forearm_len': 'ön kol (eklem-eklem)', 'thigh_len': 'uyluk (eklem-eklem)', 'shank_len': 'bacak alt (eklem-eklem)'}
def st(v, lo, hi):
    if v is None: return '—'
    return 'OK' if lo <= v <= hi else ('%.0f%% düşük' % (100*(lo-v)/lo) if v < lo else '%.0f%% yüksek' % (100*(v-hi)/hi))
labs = [l for l, _ in cols]; lines = ['| ölçü | ' + ' | '.join(labs) + ' | norm (cm) | durum (' + labs[-1] + ') |', '|---|' + '---|'*(len(labs)+2)]
nok = 0; ntot = 0
for k, (lo, hi) in NORM.items():
    vals = [D[l].get(k) for l in labs]
    if all(v is None for v in vals): continue
    s_ = st(vals[-1], lo, hi); ntot += 1; nok += (s_ == 'OK')
    lines.append('| %s | %s | %.1f–%.1f | %s |' % (TR.get(k, k), ' | '.join('—' if v is None else ('%.2f' % v if 'ratio' in k else '%.1f' % v) for v in vals), lo, hi, s_))
lines.append(''); lines.append('%s: %d / %d ölçü norm bandında (bantlar yaklaşık; ANSUR-II kadın ortalamaları boya ölçeklenmiş + atletik/zayıf düzeltme).' % (labs[-1], nok, ntot))
open(out, 'w', encoding='utf-8').write('\n'.join(lines)+'\n'); print('TABLE_OK', nok, ntot)
