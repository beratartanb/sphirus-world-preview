"""sway230.py label [label ...] [--vmin=300]: lateral sway audit per selected clip (V2.30). For frames with speed > vmin: lateral axis =
perpendicular to the capsule velocity. Per clip run (Phase27_SelectedObject): peak-to-peak lateral excursion of the head relative to the
pelvis, the pelvis relative to the capsule, the left hand relative to the pelvis, and the shoulder-line roll (deg) - on the MM output
mesh (mh_head / mx_pelvis / mx_hand_l / mx_clavicle) and on the visible body (vb_head / vb_pelvis / vx_hand_l / vb_sh) - so the source
chain (clip -> MM/blend -> retarget/PBI) shows where the sway grows. Prints SWAY230 rows."""
import json, sys, math, pathlib, collections
E = pathlib.Path(__file__).resolve().parents[2] / 'Saved/Codex/SHME_V1_20260925/Evidence'
opt = {a.split('=')[0]: a.split('=')[1] for a in sys.argv[1:] if a.startswith('--') and '=' in a}; VMIN = float(opt.get('--vmin', 300))
def f(x):
    try: return float(x)
    except Exception: return 0.0
for lab in [a for a in sys.argv[1:] if not a.startswith('--')]:
    R = [r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and isinstance(r.get('ax'), list)]; R.sort(key=lambda r: f(r['t']))
    seg = collections.OrderedDict()
    for r in R:
        vx, vy = f(r.get('avx')), f(r.get('avy')); s = math.hypot(vx, vy)
        if s < VMIN: continue
        n = (-vy / s, vx / s)
        def lat(a, b):
            A, Bv = r.get(a), r.get(b)
            if not (isinstance(A, list) and isinstance(Bv, list)): return None
            return (A[0] - Bv[0]) * n[0] + (A[1] - Bv[1]) * n[1]
        def roll(a, b):
            A, Bv = r.get(a), r.get(b)
            if not (isinstance(A, list) and isinstance(Bv, list)): return None
            d = math.hypot(A[0] - Bv[0], A[1] - Bv[1]); return math.degrees(math.atan2(A[2] - Bv[2], max(d, 1e-3)))
        k = str(r.get('av_Phase27_SelectedObject'))[-34:]
        g = seg.setdefault(k, collections.defaultdict(list)); g['t'].append(f(r['t']))
        for name, val in (('hw_vb', lat('vb_head', 'ax')), ('hd_mx', lat('mh_head', 'mx_pelvis')), ('hd_vb', lat('vb_head', 'vb_pelvis')), ('pv_mx', lat('mx_pelvis', 'ax')), ('pv_vb', lat('vb_pelvis', 'ax')),
                          ('hn_mx', lat('mx_hand_l', 'mx_pelvis')), ('hn_vb', lat('vx_hand_l', 'vb_pelvis')), ('sh_mx', roll('mx_clavicle_l', 'mx_clavicle_r')), ('sh_vb', roll('vb_sh_l', 'vb_sh_r'))):
            if val is not None: g[name].append(val)
    for k, g in seg.items():
        if len(g['t']) < 6: continue
        pp = lambda v: round(max(v) - min(v), 1) if v else None
        print('SWAY230 %s %-34s n%3d t%.2f-%.2f headW %s head %s/%s pelvis %s/%s hand %s/%s shoulder-roll %s/%s' % (lab[-30:], k, len(g['t']), g['t'][0], g['t'][-1], pp(g['hw_vb']), pp(g['hd_mx']), pp(g['hd_vb']), pp(g['pv_mx']), pp(g['pv_vb']), pp(g['hn_mx']), pp(g['hn_vb']), pp(g['sh_mx']), pp(g['sh_vb'])))
