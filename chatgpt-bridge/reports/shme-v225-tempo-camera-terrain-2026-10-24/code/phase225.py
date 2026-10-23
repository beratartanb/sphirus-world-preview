"""phase224.py: per run - pivot entry clip/time, the INCOMING loop clip/time on the frame before, the left/right ball heights then,
and the worst planted-foot net slip (win223) in the reversal window. Usage: phase224.py label:t0:t1 ..."""
import json, sys, subprocess, re, pathlib
R0 = pathlib.Path(__file__).resolve().parents[2]; E = R0 / 'Saved/Codex/SHME_V1_20260925/Evidence'
for a in sys.argv[1:]:
    lab, t0, t1 = a.split(':'); t0 = float(t0); t1 = float(t1)
    R = sorted([r for r in json.load(open(E / (lab + '.json'))) if isinstance(r, dict) and r.get('t') is not None and t0 <= float(r['t']) <= t1], key=lambda r: float(r['t']))
    ent = None
    for i, r in enumerate(R):
        o = str(r.get('av_Phase27_SelectedObject')).split('.')[-1]
        if ('Pivot' in o or 'JogRev' in o) and 'Right_Pivot' not in o and 'Left_Pivot' not in o:
            p = R[i - 1]; q = [x for x in R[:i] if 'Rear' in str(x.get('av_Phase27_SelectedObject')) or 'Jog_Fwd' in str(x.get('av_Phase27_SelectedObject')).split('.')[-1] and 'Pivot' not in str(x.get('av_Phase27_SelectedObject'))]
            inc = q[-1] if q else p
            ent = (o, float(r.get('av_Phase27_SelectedTime') or 0), str(inc.get('av_Phase27_SelectedObject')).split('.')[-1], float(inc.get('av_Phase27_SelectedTime') or 0), inc.get('vb_ball_l', [0, 0, 0])[2], inc.get('vb_ball_r', [0, 0, 0])[2]); break
    w = subprocess.run([sys.executable, str(R0 / 'Tools/SHME_V223_20261022/win223.py'), lab, str(t0), str(t1)], capture_output=True, text=True).stdout.strip().splitlines()[-1]
    nl, nr = [float(x) for x in re.findall(r'net\s+([\d.]+)', w)[:2]]
    if ent: print('PH224 %-28s entry %-24s@%.2f <- %-14s@%.2f ballL %5.1f ballR %5.1f | netL %5.1f netR %5.1f worst %5.1f' % (lab[:28], ent[0][-24:], ent[1], ent[2][-14:], ent[3], ent[4], ent[5], nl, nr, max(nl, nr)))
    else: print('PH224 %-28s no entry' % lab)
