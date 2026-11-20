# an_seg.py <label> <planfile>: per plan segment: keys, speed at 80 %, gait state from the hk_gait hook, Gait enum, clip
import json,math,ast,sys
plan=ast.literal_eval(open(sys.argv[2]).read())
R=json.load(open('Saved/Codex/Grip_20261106/rec/%s.json'%sys.argv[1])); R=R['rows'] if isinstance(R,dict) else R
seg={}
for r in R: seg.setdefault(r['s'],[]).append(r)
for s in sorted(seg):
    if s>=len(plan): continue
    rows=seg[s]; m=rows[int(len(rows)*0.8)]; h=m.get('hook') or {}; g=m.get('gasp') or [None]*4
    print('s%-2d %-22s speed %4.0f | TempoOn %-5s Act %-5s Back %-5s Hold %-5s Sel %s scale %s | %-6s %s'%(s,plan[s][0][:22],math.hypot(m['vx'],m['vy']),h.get('GR_TempoOn'),h.get('GR_TempoAct'),h.get('GR_Back'),h.get('GR_BrakeHold'),h.get('GR_GaitSel'),h.get('SphContextSpeedScale'),str(g[2])[-6:],str(g[0])[-30:]))
