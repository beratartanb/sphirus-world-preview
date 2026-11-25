#!/bin/bash
# perf_ab.sh: SAME editor session, alternating: layered house materials (A) / source parents (B) / A / B. Six fixed views, 4 s average each.
cd "<PROJECT>"; source Tools/VF2B_20261125/lib.sh; O=Saved/UE59Work/vf2c/ev/perf_house_AB_same_session.txt; : > $O
for r in A1 B1 A2 B2; do
  case $r in A*) RUN Tools/VF2C_20261125/_h2_on.py vf2c_on control 200 | grep -E "VF2H2 done|rror" | cut -c1-40;; B*) RUN Tools/VF2C_20261125/_h2_rev.py vf2c_rev control 200 | grep -E "reverted|rror" | cut -c1-40;; esac
  W 25
  bash Tools/VF2_20261124/vf2_world_tour.sh ab_$r Tools/VF2C_20261125/views_ab.txt 2>&1 | grep -E "fps" | cut -c1-34 | sed "s/^/$r /" >> $O
done
"/c/Program Files/Epic Games/UE_5.9/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" - <<'PY' | tee -a Saved/UE59Work/vf2c/ev/perf_house_AB_same_session.txt
import collections
d = collections.defaultdict(dict)
for l in open('Saved/UE59Work/vf2c/ev/perf_house_AB_same_session.txt'):
    p = l.split()
    if len(p) >= 4 and p[2] == 'fps': d[p[1]][p[0]] = float(p[3])
print('view              A1    B1    A2    B2   | mean A  mean B  A-B (layered - source)')
ta = tb = 0; n = 0
for v, r in d.items():
    if len(r) == 4:
        a = (r['A1'] + r['A2']) / 2; b = (r['B1'] + r['B2']) / 2; ta += a; tb += b; n += 1
        print('%-16s %5.1f %5.1f %5.1f %5.1f | %5.1f   %5.1f   %+.1f' % (v, r['A1'], r['B1'], r['A2'], r['B2'], a, b, a - b))
if n: print('MEAN over %d views: layered %.1f fps, source %.1f fps, difference %+.1f fps' % (n, ta / n, tb / n, (ta - tb) / n))
PY
