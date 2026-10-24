import json, bisect, sys
C=json.load(open('Saved/Codex/SHME_V226_20261024/clipfoot226.json'))
def clip_at(name,t):
    rows=C[name]['rows']; ts=[r[0] for r in rows]; i=min(bisect.bisect_left(ts,t),len(rows)-1); return rows[i]
for lab in sys.argv[1:]:
    R=sorted([r for r in json.load(open('Saved/Codex/SHME_V1_20260925/Evidence/%s.json'%lab)) if isinstance(r,dict) and r.get('t') is not None and isinstance(r.get('ax'),list)],key=lambda r:float(r['t']))
    print(lab); first=None
    for r in R:
        t=float(r['t']); so=str(r.get('av_Phase27_SelectedObject'))
        if 'JogRev' not in so: 
            if first is not None: break
            continue
        name=so.rsplit('.',1)[-1].rsplit('/',1)[-1]; ct=float(r.get('av_Phase27_SelectedTime') or 0)
        if name not in C: print('no clip', name); break
        if first is None: first=t
        c=clip_at(name,ct)
        gp=r['vb_pelvis'][0]-r['ax'][0]; gl=r['vb_ball_l'][0]-r['ax'][0]; gr=r['vb_ball_r'][0]-r['ax'][0]
        if int(round((t-first)*30))%2==0 and t-first<=1.3:
            print('  +%.2f ct %.3f %s | d pelvis %6.1f | d L %6.1f (z g %5.1f c %5.1f) | d R %6.1f (z g %5.1f c %5.1f) | cap v %5.0f'%(t-first,ct,name[-7:],gp-c[2][0],gl-c[5][0],r['vb_ball_l'][2],c[5][2],gr-c[6][0],r['vb_ball_r'][2],c[6][2],float(r.get('cv_Speed') or 0)))
