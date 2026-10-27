"""expr233.py <graph dump txt> <node> [depth] : readable expression tree of one node from a graph_dump.py text (offline)."""
import sys, re
lines = open(sys.argv[1], encoding='utf8').read().splitlines(); root = sys.argv[2]; DEP = int(sys.argv[3]) if len(sys.argv) > 3 else 30
N = {}
for l in lines:
    m = re.match(r'(\S+) \[([^\]]*)\] ?(.*)$', l)
    if not m: continue
    name, typ, rest = m.groups(); pins = {}
    for part in [p for p in rest.split('; ') if p]:
        if '<-' in part: k, v = part.split('<-', 1); pins[k] = ('L', v.split(','))
        elif '=' in part: k, v = part.split('=', 1); pins[k] = ('V', v)
    N[name] = (typ.rsplit('|', 1)[-1], pins)
seen = {}
def ex(n, d=0):
    if n not in N: return n
    t, pins = N[n]
    if d > DEP: return t + '(...)'
    if n in seen and seen[n] < d: return '<' + t + ' ' + n + '>'
    seen[n] = d
    args = []
    for k, (kind, v) in pins.items():
        if k in ('execute', 'then', 'self'): continue
        if kind == 'V': args.append('%s=%s' % (k, v))
        else: args.append('%s=%s' % (k, ' | '.join(ex(x.rsplit('.', 1)[0], d + 1) for x in v)))
    short = t.replace('Get', '').replace('BreakRotator', 'BR').replace('MakeRotator', 'MR')
    return '%s(%s)' % (short, ', '.join(args)) if args else short
print(ex(root))
