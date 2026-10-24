"""capterm.py label...: per frame while a SHM226 clip is selected: capsule-clock term = game capsule x - (capsule x at entry + D_table(ct) - D_table(ct_entry)),
pose term = visible ball (capsule frame, forward) - clip ball (clip y), for both feet; the designed world foot error = capsule term + pose term."""
import json, bisect, sys
C=json.load(open('Saved/Codex/SHME_V226_20261024/clipfoot226.json')); T=json.load(open('Saved/Codex/SHME_V225_20261023/capsule_rev_table.json'))
def clip_at(name,t):
    rows=C[name]['rows']; ts=[r[0] for r in rows]; i=min(bisect.bisect_left(ts,t),len(rows)-1); return rows[i]
def D(fam,t):   # designed capsule displacement along the OLD travel direction... table v is signed along +forward? use sign from the clip name: F_B travels +x at start
    tab=T[fam]['v']; dt=T[fam]['dt']; s=0.0; k=0
    while (k+1)*dt<=t and k+1<len(tab): s+=0.5*(tab[k]+tab[k+1])*dt; k+=1
    if k+1<len(tab): s+=tab[k]*(t-k*dt)
    return s
for lab in sys.argv[1:]:
    R=sorted([r for r in json.load(open('Saved/Codex/SHME_V1_20260925/Evidence/%s.json'%lab)) if isinstance(r,dict) and r.get('t') is not None and isinstance(r.get('ax'),list)],key=lambda r:float(r['t']))
    print(lab); first=None
    for r in R:
        t=float(r['t']); so=str(r.get('av_Phase27_SelectedObject'))
        if 'JogRev' not in so:
            if first is not None: break
            continue
        name=so.rsplit('.',1)[-1].rsplit('/',1)[-1]; fam='F_B' if '_F_B_' in name else 'B_F'; ct=float(r.get('av_Phase27_SelectedTime') or 0)
        sign = 1.0 if fam=='F_B' else -1.0   # the table is signed along the old travel; F_B old travel = +x (forward run), B_F old travel = -x (backpedal)... check table sign below
        if first is None: first=t; x0=r['ax'][0]; ct0=ct; print('  table v[0..3] %s'%[round(v) for v in T[fam]['v'][:4]], 'game v at entry', round((R[R.index(r)]['ax'][0]-R[R.index(r)-1]['ax'][0])*30))
        c=clip_at(name,ct); capterm = r['ax'][0] - (x0 + sign*(D(fam,ct)-D(fam,ct0)))
        gl=r['vb_ball_l'][0]-r['ax'][0]; gr=r['vb_ball_r'][0]-r['ax'][0]
        if int(round((t-first)*30))%2==0 and t-first<=1.0:
            print('  +%.2f ct %.3f | cap term %6.1f | pose L %6.1f R %6.1f | zL g %5.1f c %5.1f | zR g %5.1f c %5.1f'%(t-first,ct,capterm,gl-c[5][1],gr-c[6][1],r['vb_ball_l'][2],c[5][2],r['vb_ball_r'][2],c[6][2]))
