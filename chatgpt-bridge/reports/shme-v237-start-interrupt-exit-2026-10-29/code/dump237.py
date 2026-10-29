"""dump237.py <label> <t0> <t1> [foot l|r] : per-frame visible body around an event (same frames): input, capsule speed, family, DB, clip+time
(+ clip rate), planted ball world pos + mesh-relative (mx) in the MOVEMENT frame (along / lateral to the capsule velocity), ball z, pelvis z."""
import sys, os, math; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'SHME_V231_20261026'))
from ltp231 import load, short
lab, t0, t1 = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]); s = sys.argv[4] if len(sys.argv) > 4 else 'r'
R = load(lab); prev = None
for r in R:
    if not (t0 <= r['t'] <= t1): prev = r; continue
    b = r['vb_ball_' + s]; o = r['vb_ball_' + ('l' if s == 'r' else 'r')]; rt = r.get('mx_root') or (0, 0, 0)
    rate = (r['av_Phase27_SelectedTime'] - prev['av_Phase27_SelectedTime']) / max(r['t'] - prev['t'], 1e-3) if prev else 0
    print('%.2f in(%.1f,%.1f) v%4.0f fam %-3s %-14s %-30s %5.2f r%4.2f ball%s(%.1f,%.1f,%.1f) other(%.1f,%.1f,%.1f) rel(%.1f,%.1f) pelz %.1f' % (
        r['t'], r['lix'], r['liy'], r['Speed2D'], str(r.get('cv_Family'))[:3], short(r['av_CurrentSelectedDatabase'])[-14:], short(r['av_Phase27_SelectedObject'])[:30],
        r['av_Phase27_SelectedTime'], rate, s, *b, *o, b[0] - rt[0], b[1] - rt[1], r['vb_pelvis'][2] - rt[2]))
    prev = r
