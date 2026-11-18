# cmp_slope.py <label>...: slope support comparison by grade band (walking/jogging windows, v > 100) from an_slope2 outputs
import json, sys, statistics as st
L = sys.argv[1:]; D = {l: json.load(open('Saved/UE59Work/rec_slope_%s.json' % l)) for l in L}
def agg(X, lo, hi, sg):
    S = [x for x in X if lo <= abs(x['grade']) < hi and x['v'] > 100 and x['grade'] * sg > 0]
    return (len(S), st.mean(x['v'] for x in S), st.mean(x['pelG'] for x in S), min(x['pelG_rg'][0] for x in S), st.mean(x['pelLo'] for x in S), st.mean(x['knee_up'] for x in S), st.mean(x['knee_lo'] for x in S), st.mean(x['trunk'] for x in S)) if S else None
for nm, (lo, hi, sg) in (('flat 0-4', (0, 4, 1)), ('up 6-15', (6, 15, 1)), ('up 15-40', (15, 40, 1)), ('down 6-15', (6, 15, -1)), ('down 15-40', (15, 40, -1))):
    for l in L:
        a = agg(D[l], lo, hi, sg)
        if a: print('%-11s %-24s n %2d v %4.0f pelG %5.1f (min %5.1f) pelLo %5.1f kneeUp %4.0f kneeLo %4.0f trunk %+5.1f' % ((nm, l) + a))
