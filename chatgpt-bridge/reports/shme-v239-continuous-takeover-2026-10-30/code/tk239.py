"""tk239.py <label> [t_from] [t_to] : V2.39 consecutive-request read of ONE run (LTP side file, same frames).
Prints (1) the owner timeline (clip, clip time, database, SHM238_W / SHM239 step, target, request, takeover pulse, episode class);
(2) control stages per input change after t_from: request frame -> first visible body reaction (head or chest yaw moves >= 5 deg toward
the new intent) -> first support after the request (planned touchdown clock step, else ball contact) -> velocity transfer (velocity
component along the new intent rises 30 cm/s above its value at the request) -> stable new heading (within 10 deg of the intent and
speed >= 0.8 of its final value); (3) worst planted-ball slide (contact231) with owner clip and the actor-yaw rate peak (deg/s)."""
import sys, os, math, json
H = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [H + '/../SHME_V231_20261026', H + '/../SHME_V238_20261030']
from ltp231 import load, short
from contact231 import classify
def yaw_of(v): return math.degrees(math.atan2(v[1], v[0]))
def wrap(a): return (a + 180.0) % 360.0 - 180.0
def axyaw(r, k):
    v = r.get(k)
    if isinstance(v, (list, tuple)) and len(v) >= 2: return yaw_of(v)
    return None
def main(lab, t0=2.5, t1=1e9):
    R = load(lab); rows = [r for r in R if t0 <= r['t'] <= t1]
    print('== %s  rows %d' % (lab, len(rows)))
    prev = None
    for r in rows:
        k = (short(r.get('av_Phase27_SelectedObject'))[:26], str(r.get('av_CurrentSelectedDatabase'))[:22], round(float(r.get('ac_SHM238_W') or 0), 1),
             round(float(r.get('ac_SHM239_Step') or 0)), round(float(r.get('ac_SHM239_Tgt') or 0)), r.get('av_SHM239_OwnOn'), r.get('av_SHM239_TkReq'),
             r.get('av_SHM239_TkGo'), round(float(r.get('cv_RedirectClass') or 0)))
        if k != prev:
            vy = yaw_of((r['avx'], r['avy'])) if math.hypot(r['avx'], r['avy']) > 5 else float('nan')
            print('%6.2f sp%4.0f vhd%5.0f my%5.0f in(%4.1f,%4.1f) ct%.2f | %s' % (r['t'], r['Speed2D'], vy, r['my'] + 90, r['lix'], r['liy'], r.get('av_Phase27_SelectedTime') or 0, ' | '.join(str(x) for x in k)))
            prev = k
    # control stages per input change
    print('-- control stages')
    def inyaw(r): return yaw_of((r['lix'], r['liy'])) if math.hypot(r['lix'], r['liy']) > 0.3 else None
    ev = []
    for i in range(1, len(rows)):
        a, b = inyaw(rows[i - 1]), inyaw(rows[i])
        if b is not None and (a is None or abs(wrap(b - a)) > 30): ev.append(i)
    for i in ev:
        r0 = rows[i]; iy = inyaw(r0); ux, uy = math.cos(math.radians(iy)), math.sin(math.radians(iy))
        v0 = r0['avx'] * ux + r0['avy'] * uy
        def bodyyaw(r, k):
            y = axyaw(r, k); return y
        hb = {k: bodyyaw(r0, k) for k in ('vaz_head', 'vaz_spine_05')}
        st = {'req': r0['t']}
        for r in rows[i:]:
            if 'body' not in st:
                for k in ('vaz_head', 'vaz_spine_05'):
                    y = bodyyaw(r, k)
                    if y is not None and hb[k] is not None and abs(wrap(iy - y)) <= abs(wrap(iy - hb[k])) - 5: st['body'] = (r['t'], k[4:]); break
            if 'support' not in st and float(r.get('ac_SHM239_Step') or 0) > float(r0.get('ac_SHM239_Step') or 0) + 0.5: st['support'] = r['t']
            if 'transfer' not in st and r['avx'] * ux + r['avy'] * uy > v0 + 30: st['transfer'] = r['t']
            if inyaw(r) is None or abs(wrap(inyaw(r) - iy)) > 30: break
        vf = None
        seg = [r for r in rows[i:] if inyaw(r) is not None and abs(wrap(inyaw(r) - iy)) <= 30]
        if seg: vf = max(r['Speed2D'] for r in seg)
        for r in seg:
            vh = yaw_of((r['avx'], r['avy'])) if r['Speed2D'] > 5 else None
            if vh is not None and abs(wrap(vh - iy)) <= 10 and vf and r['Speed2D'] >= 0.8 * vf: st['stable'] = r['t']; break
        rel = {k: (round(v - r0['t'], 2) if isinstance(v, float) else (round(v[0] - r0['t'], 2), v[1])) for k, v in st.items() if k != 'req'}
        print('  input %4.0f deg at %.2f s (speed %3.0f, heading %4.0f): %s' % (iy, r0['t'], r0['Speed2D'], yaw_of((r0['avx'], r0['avy'])), json.dumps(rel)))
    eps = [e for e in classify(R, max(t0, 2.5), t1) if e['cls'] in ('SLIP', 'DRAG')]
    w = max(eps, key=lambda e: e['drift']) if eps else None
    yr = 0.0
    for a, b in zip(rows, rows[1:]):
        if b['t'] > a['t']: yr = max(yr, abs(wrap(b['my'] - a['my'])) / (b['t'] - a['t']))
    print('-- worst slide %s | actor yaw rate peak %.0f deg/s' % (('%.1f cm %s at %.2f' % (w['drift'], short(w['clip'])[:28], w['t'])) if w else '0', yr))
if __name__ == '__main__':
    a = sys.argv[1:]; main(a[0], float(a[1]) if len(a) > 1 else 2.5, float(a[2]) if len(a) > 2 else 1e9)
