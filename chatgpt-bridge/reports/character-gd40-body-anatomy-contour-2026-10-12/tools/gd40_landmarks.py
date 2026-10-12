"""GD40: anatomical landmark widths from silhouette profiles (gd40_refsil.py json) of a FRONT (or back) and a SIDE view, so a reference
figure and the SPHIRUS body can be compared by shape RATIOS (independent of image scale and of vertical proportions).
Front: the torso run per row (arms excluded once they separate). Landmarks (rows as height fraction f, 0 = top of head):
  shoulder = max width over f 0.15..0.26 (deltoids, arms attached);  armpit = first row below the shoulder where the run narrows by > 25 %
  ribcage = width 2 % of height below the armpit;  waist = min width between armpit+4 % and the hip;  hip = max width between waist and crotch
  crotch = first row below the hip where the axis falls outside the run (legs split);  then per leg (the run nearest the axis side):
  upper thigh = width 2 % below the crotch;  mid thigh, knee (min over f 0.66..0.76), calf (max 0.76..0.86), ankle (min 0.88..0.96).
Side: depth (front-back extent of the run containing the body axis): bust (max over armpit..armpit+8 %), waist depth (min near the front-view
  waist row +-3 %), glute (max over hip-4 %..crotch), thigh depth 4 % below the crotch, calf depth max.
usage: python gd40_landmarks.py <front.json> <front_name> <side.json> <side_name> [label]"""
import sys, json, numpy as np
fj, fn, sj, sn = sys.argv[1:5]; lab = sys.argv[5] if len(sys.argv) > 5 else fn
F = json.load(open(fj))[fn]; S = json.load(open(sj))[sn]
def widths(V):
    r = V['rows']; return np.array([np.nan if x is None else x[1]-x[0] for x in r], float), V['height_px']
wf, hf = widths(F); ws, hs = widths(S)
def at(w, h, f): i = int(f*h); return i
def rng(w, h, f0, f1): i0, i1 = int(f0*h), int(f1*h); return i0, i1
o = {}
i0, i1 = rng(wf, hf, 0.15, 0.26); sh_i = i0+int(np.nanargmax(wf[i0:i1])); o['shoulder'] = wf[sh_i]
ap = None
for i in range(sh_i, int(0.40*hf)):
    if wf[i] < 0.75*wf[i-3]: ap = i; break
ap = ap or int(0.28*hf); o['armpit_f'] = ap/hf; rc = ap+int(0.02*hf); o['ribcage'] = wf[rc]
cr = None; hip_lo = int(0.62*hf)
axis = F['axis_x']
for i in range(ap+int(0.10*hf), hip_lo):
    r = F['rows'][i]
    if r and not (r[0] < axis-2 < r[1] and r[0] < axis+2 < r[1]): cr = i; break
    if r and (r[1]-r[0]) > 0 and False: pass
# crotch: first row where the run containing the axis is gone or the run is clearly one leg (width drops > 35 % vs the row above)
if cr is None:
    for i in range(ap+int(0.15*hf), hip_lo):
        if wf[i] < 0.65*wf[i-2]: cr = i; break
o['crotch_f'] = (cr or hip_lo)/hf; cr = cr or hip_lo
wa_i = ap+int(0.04*hf)+int(np.nanargmin(wf[ap+int(0.04*hf):cr-int(0.08*hf)])); o['waist'] = wf[wa_i]; o['waist_f'] = wa_i/hf
hp_i = wa_i+int(np.nanargmax(wf[wa_i:cr])); o['hip'] = wf[hp_i]; o['hip_f'] = hp_i/hf
o['thigh_upper'] = wf[cr+int(0.02*hf)]; o['thigh_mid'] = wf[cr+int(0.08*hf)]
k0, k1 = rng(wf, hf, 0.66, 0.76); kn_i = k0+int(np.nanargmin(wf[k0:k1])); o['knee'] = wf[kn_i]; o['knee_f'] = kn_i/hf
c0, c1 = kn_i+int(0.03*hf), int(0.88*hf); ca_i = c0+int(np.nanargmax(wf[c0:c1])); o['calf'] = wf[ca_i]; o['calf_f'] = ca_i/hf
a0, a1 = rng(wf, hf, 0.88, 0.96); o['ankle'] = np.nanmin(wf[a0:a1])
# side depths at the same height fractions (side figure scaled by its own height)
def sat(f): return int(f*hs)
b0, b1 = sat(o['armpit_f']), sat(o['armpit_f']+0.08); o['bust_depth'] = np.nanmax(ws[b0:b1])
wd0 = sat(o['waist_f']-0.03); wd1 = sat(o['waist_f']+0.03); o['waist_depth'] = np.nanmin(ws[wd0:wd1])
g0, g1 = sat(o['hip_f']-0.04), sat(o['crotch_f']); o['glute_depth'] = np.nanmax(ws[g0:g1])
o['thigh_depth'] = ws[sat(o['crotch_f']+0.04)]; o['calf_depth'] = np.nanmax(ws[sat(o['calf_f']-0.03):sat(o['calf_f']+0.03)])
hip = o['hip']; R = {k: round(float(v)/hip, 3) for k, v in o.items() if not k.endswith('_f')}
F_ = {k: round(float(v), 3) for k, v in o.items() if k.endswith('_f')}
print('LANDMARKS %-6s ratios/hip: %s | rows (f): %s' % (lab, ' '.join('%s %.3f' % (k, v) for k, v in R.items()), ' '.join('%s %.3f' % (k, v) for k, v in F_.items())))
json.dump({'label': lab, 'ratios_to_hip': R, 'rows_f': F_, 'px': {k: float(v) for k, v in o.items()}}, open(fj.replace('.json', f'_landmarks_{lab}.json'), 'w'), indent=1)
