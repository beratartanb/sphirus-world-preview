"""probe241_sub.py (measure): data-input tree (depth N) of given nodes in a BP function graph. builtins.V241_SUB = {'bp':..,'graph':..,'nodes':[..],'depth':5}.
Prints SUB241 lines."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import pn, info, src
import builtins, json
c = builtins.V241_SUB; bp = u.load_asset(c['bp']); g = graph(bp, c['graph']); base = pn(g)
seen = set()
def walk(p, d, ind):
    try: i = info(p)
    except Exception as e: print('SUB241 ' + ind + p.split('.')[-1] + ' ?' + str(e)[:60]); return
    t = str(i.type_id)[-55:]
    vals = []
    for q in i.input_pins:
        s = src((p, q.name))
        if not s:
            try: v = str(q.value)
            except Exception: v = ''
            if v and q.name not in ('self',): vals.append('%s=%s' % (q.name, v[:20]))
    print('SUB241 %s%s [%s] %s' % (ind, p.split('.')[-1], t, ' '.join(vals)[:150]))
    if d == 0 or p in seen: return
    seen.add(p)
    for q in i.input_pins:
        if q.name in ('execute',): continue
        for s_ in src((p, q.name)):
            print('SUB241 %s  <%s> from %s:%s' % (ind, q.name, s_[0].split('.')[-1], s_[1])); walk(s_[0], d - 1, ind + '    ')
for n in c['nodes']: walk(base + '.' + n, int(c.get('depth', 5)), '')
