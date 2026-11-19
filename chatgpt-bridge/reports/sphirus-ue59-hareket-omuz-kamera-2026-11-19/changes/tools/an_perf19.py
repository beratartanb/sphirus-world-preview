# an_perf19.py <label> [label ...]: frame/GPU percentiles + the top GPU passes (GPU/* columns, mean ms) from the engine CSV, and the
# GPU clock / power / temperature summary from the matching nvidia-smi log (P19_*.smi.txt).
import sys, csv, statistics as st, os
D = 'Saved/Codex/Camera_20261112/perf/'
def pct(v, p):
    v = sorted(v); return v[min(len(v) - 1, int(len(v) * p))] if v else float('nan')
for lab in sys.argv[1:]:
    rows = list(csv.reader(open(D + lab + '.csv', encoding='utf8', errors='ignore')))
    hi = next(i for i, r in enumerate(rows) if 'FrameTime' in r); hdr = rows[hi]; fi = hdr.index('FrameTime'); data = [r for r in rows[hi + 1:] if len(r) >= len(hdr) - 1 and r[fi].replace('.', '', 1).isdigit()]
    col = lambda n: [float(r[hdr.index(n)]) for r in data if r[hdr.index(n)] not in ('', None)]
    ft = col('FrameTime'); gt = col('GPUTime') if 'GPUTime' in hdr else []
    print('== %s  frames %d  FrameTime p50 %.1f p95 %.1f | GPUTime p50 %.1f p95 %.1f | avg fps %.1f' % (lab, len(ft), pct(ft, .5), pct(ft, .95), pct(gt, .5), pct(gt, .95), 1000.0 / st.mean(ft)))
    gp = [(st.mean(col(h)), h) for h in hdr if h.startswith('GPU/') and col(h)]
    for m, h in sorted(gp, reverse=True)[:14]: print('     %6.2f ms  %s' % (m, h))
    s = D + lab + '.smi.txt'
    if os.path.exists(s):
        L = [l.split(', ') for l in open(s) if l.count(',') >= 6]
        try:
            clk = [float(x[1].split()[0]) for x in L]; pw = [float(x[3].split()[0]) for x in L]; lim = L[0][4]; tp = [float(x[5]) for x in L]; thr = sorted(set(x[7].strip() for x in L))
            print('     GPU clock p50 %.0f MHz (min %.0f) | power p50 %.1f W / limit %s | temp p50 %.0f C (max %.0f) | throttle reasons %s' % (pct(clk, .5), min(clk), pct(pw, .5), lim, pct(tp, .5), max(tp), thr))
        except Exception as e: print('     smi parse', e)
