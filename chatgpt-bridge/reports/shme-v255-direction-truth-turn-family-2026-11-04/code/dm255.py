"""dm255.py : V2.55 direction matrix inputs. For gait x camera yaw: W>S, S>W, A>D, D>A, WA>SD, SD>WA, WD>SA, SA>WD, each twice with hold times half a stride apart (both support feet).
Writes Saved/Codex/SHME_V255_20261104/req/fz_dm_<gait>_<cam>.move/.yaw so the fz_* harness hook runs them. Print the expected event list to data/dm_events.json."""
import json
D = 'Saved/Codex/SHME_V255_20261104/req/'
PAIRS = [('W', 'S'), ('S', 'W'), ('A', 'D'), ('D', 'A'), ('WA', 'SD'), ('SD', 'WA'), ('WD', 'SA'), ('SA', 'WD')]
names = []
for gait in ('walk', 'jog', 'sprint'):
    for cam in (0, 60, -120):
        ev = []
        if gait == 'jog': ev += [[0.0, 'LeftShift', 1], [0.12, 'LeftShift', 0]]
        if gait == 'sprint': ev += [[0.0, 'LeftShift', 1]]
        t = 1.5
        for rep, delta in enumerate((0.0, 0.14)):
            for a, b in PAIRS[rep * 4:(rep + 1) * 4] + PAIRS[((rep + 1) % 2) * 4:((rep + 1) % 2) * 4 + 4]:
                for k in a: ev.append([round(t, 3), k, 1])
                t += 2.3 + delta
                for k in a:
                    if k not in b: ev.append([round(t, 3), k, 0])
                for k in b:
                    if k not in a: ev.append([round(t, 3), k, 1])
                t += 1.9
                for k in b: ev.append([round(t, 3), k, 0])
                t += 0.9
        if gait == 'sprint': ev.append([round(t, 3), 'LeftShift', 0])
        ev.sort(key=lambda e: e[0])
        name = 'fz_dm_%s_%s' % (gait, str(cam).replace('-', 'm'))
        open(D + name + '.move', 'w').write(json.dumps({'start': 2.0, 'gait': 'walk', 'keys': ev, 'stop': 1.5}, separators=(',', ':')))
        open(D + name + '.yaw', 'w').write(json.dumps({'start': 0.6, 'hold': 200.0, 'steps': [cam], 'ramp': 240}, separators=(',', ':')))
        names.append(name)
print(' '.join(names), 'end', round(t, 1))
