"""GD26 lip prominence (scale- and alignment-free): signed perpendicular distance of labrale superius (ls), stomion (sto), labrale inferius (li),
subnasale (sn) and sulcus (sm) to two reference lines of the same profile - the E-line (nose tip -> pogonion) and the sn-pg line - divided by
the line length; + = in FRONT of the line (toward the background). Also the model mm needed to match the reference ratio (ratio difference x
the candidate's line length in panel px x 10/14.78 mm). Contours: background-key reference photo / candidate alpha renders (gd26_contour_lib).
usage: -- <ref panel png> label=alpha.png [...]"""
import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD13_Identity_20261009/tools')); sys.path.insert(0, os.path.join(os.getcwd(), 'Saved/Codex/GD26_Identity_20261011/tools'))
import gd13_img as gi
from gd26_contour_lib import ref_mask, alpha_mask, analyse, MMPX
a = sys.argv[sys.argv.index('--')+1:]; TIPR = (225, 255)
def prom(Q, L):
    out = {}
    for ln, (A, B) in (('E', ('tip', 'pg')), ('snpg', ('sn', 'pg'))):
        PA, PB = Q[L[A]], Q[L[B]]; d = PB-PA; Ln = np.linalg.norm(d); n = np.array([d[1], -d[0]])/Ln   # rotate so that + points toward -x (front)
        if n[0] > 0: n = -n
        for k in ('sn', 'ls', 'sto', 'li', 'sm'):
            if k in L and k not in (A, B): out[(ln, k)] = (float((Q[L[k]]-PA)@n/Ln), Ln)
    return out
RQ, RL, _ = analyse(ref_mask(gi.load(a[0])), 1.0, TIPR); R = prom(RQ, RL)
C = {}
for s in a[1:]:
    lab, p = s.split('=', 1); Q, L, _ = analyse(alpha_mask(gi.load(p)), 2.0, TIPR); C[lab] = prom(Q, L)
print('line  pt    REF ratio | ' + ' | '.join('%s ratio  need_mm' % l for l in C))
for key in R:
    r = R[key][0]; row = '%-5s %-4s %+7.4f   | ' % (key[0], key[1], r)
    for lab, d in C.items():
        if key in d: v, Ln = d[key]; row += '%+7.4f  %+5.2f | ' % (v, (r-v)*Ln*MMPX)
    print(row)
print('(+ ratio = in front of the line; need_mm > 0 = the point must move FORWARD by that much, model mm)')
