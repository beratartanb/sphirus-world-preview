"""fz255.py <name> <gait walk|jog|sprint> <seed> <seconds> [mouse 0|1] : V2.55 seeded input fuzz on the REAL key path (W/A/S/D + Shift through
Enhanced Input). Writes Saved/Codex/SHME_V255_20261104/req/<name>.move (+ .yaw when mouse = 1). Direction changes are drawn from all 8 directions
with every class of change (45/90/135/180), hold times from a short tap to a long hold, instant swap / small gap / small overlap of the keys and
full releases, so entries land on every loop phase and support foot; mouse = an open-loop look (sine sweeps + wandering drift) like a hand on a
mouse. The point is coverage of what a player really does, not one scripted case: dir255.py then judges every frame."""
import json, random, sys
name, gait, seed, secs = sys.argv[1], sys.argv[2], int(sys.argv[3]), float(sys.argv[4]); mouse = len(sys.argv) > 5 and sys.argv[5] == '1'
R = random.Random(seed); DIRS = ['W', 'WD', 'D', 'SD', 'S', 'SA', 'A', 'WA']
ev = []
if gait == 'jog': ev += [[0.0, 'LeftShift', 1], [0.12, 'LeftShift', 0]]
if gait == 'sprint': ev += [[0.0, 'LeftShift', 1]]
t = 0.3; cur = 'W'
def press(t, ks):
    for k in ks: ev.append([round(t, 3), k, 1])
def rel(t, ks):
    for k in ks: ev.append([round(t, 3), k, 0])
press(t, cur); t += 2.6
n = 0
while t < secs:
    n += 1; i = DIRS.index(cur)
    step = R.choices([4, 3, -3, 2, -2, 1, -1], [30, 12, 12, 14, 14, 9, 9])[0]
    nxt = DIRS[(i + step) % 8]
    style = R.choices(['swap', 'gap', 'over', 'release'], [62, 14, 12, 12])[0]
    if style == 'release':
        rel(t, cur); t += R.choice([0.2, 0.4, 0.7, 1.1]); press(t, nxt)
    else:
        lose = [k for k in cur if k not in nxt]; gain = [k for k in nxt if k not in cur]
        if style == 'swap': rel(t, lose); press(t, gain)
        elif style == 'gap': rel(t, lose); press(t + 0.05, gain); t += 0.05
        else: press(t, gain); rel(t + 0.05, lose); t += 0.05
    cur = nxt
    t += R.choices([0.15, 0.3, 0.6, 1.0, 1.6, 2.4], [10, 16, 22, 24, 18, 10])[0]
rel(t, cur)
if gait == 'sprint': ev.append([round(t + 0.1, 3), 'LeftShift', 0])
ev.sort(key=lambda e: e[0])
mv = {'start': 2.0, 'gait': 'walk', 'keys': ev, 'stop': 2.0}
D = 'Saved/Codex/SHME_V255_20261104/req/'
open(D + name + '.move', 'w').write(json.dumps(mv, separators=(',', ':')))
y = {'start': 2.5, 'hold': 2.0, 'steps': [], 'osc': {'seconds': secs + 3.0, 'period': 2.3, 'amps': [10, 22, 34, 6], 'drift': [[4.0, 24.0], [3.0, -36.0], [5.0, 14.0], [3.0, -8.0]]}} if mouse else None
if y: open(D + name + '.yaw', 'w').write(json.dumps(y, separators=(',', ':')))
print(name, 'events', n, 'end', round(t, 1), 'mouse', mouse)
