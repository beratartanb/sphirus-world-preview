"""exposure_table.py <stats.json> [<stats2.json> ...] : markdown table (per station + per place + overall) of the exposure_stats.ps1 output.
Columns = the capture sets (dir names); cells = mean luminance / white% / black% / saturation."""
import json, sys, collections
sets = collections.OrderedDict()
for f in sys.argv[1:]:
    for k, v in json.load(open(f, encoding='utf-8-sig')).items(): sets[k] = v
names = list(sets); stations = sorted(set().union(*[set(v) for v in sets.values()]))
print('| station | ' + ' | '.join(names) + ' |'); print('|---|' + '---|' * len(names))
def cell(d): return '%.0f / %.2f / %.2f / %.3f' % (d['mean'], d['white_pct'], d['black_pct'], d['sat']) if d else '-'
for s in stations: print('| %s | %s |' % (s, ' | '.join(cell(sets[n].get(s)) for n in names)))
print('| **mean** | ' + ' | '.join(cell({k: sum(d[k] for d in sets[n].values()) / len(sets[n]) for k in ('mean', 'white_pct', 'black_pct', 'sat')}) for n in names) + ' |')
for place in ('P0', 'P1', 'P2', 'P3'):
    row = []
    for n in names:
        ds = [d for s, d in sets[n].items() if s.startswith(place)]
        row.append(cell({k: sum(d[k] for d in ds) / len(ds) for k in ('mean', 'white_pct', 'black_pct', 'sat')}) if ds else '-')
    print('| *%s mean* | %s |' % (place, ' | '.join(row)))
