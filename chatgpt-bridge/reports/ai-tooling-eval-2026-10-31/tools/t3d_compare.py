"""t3d_compare.py <dir with mem/ and disk/> : order-insensitive comparison of two ABP exports (memory snapshot vs reloaded-from-disk).

Blueprint .t3d (UTF-16 or UTF-8): split into 'Begin Object ... End Object' blocks keyed by the object's full nesting path of Name=
values; compare the set of block keys and, for common keys, the sorted set of property lines (export order is not stable between an
in-memory and a freshly reloaded Blueprint). NodePosX/Y-only differences are reported separately. 32-hex GUIDs (PinId, LinkedTo targets, GraphGuid, NodeGuid) are masked because
hidden pins and compiler-generated intermediate graphs get new GUIDs on every reload; links are still compared by node name + pin.
Also normalised: NSLOCTEXT("ns", "key", "text") -> "text" (display-name text form) and K2Node_PropertyAccess_<n> numbering.
CDO .cdo.t3d: plain 'Key=Value' lines; K2Node_PropertyAccess_N names are regenerated per compile (numbering shifts), so they are
compared as a multiset of values; every other key is compared by name.
Output: <dir>/t3d_compare.json and a printed summary."""
import sys, os, re, json, collections

D = sys.argv[1]


def read(p):
    raw = open(p, 'rb').read()
    for enc in ('utf-16', 'utf-8'):
        try:
            t = raw.decode(enc)
            if 'Begin' in t or '=' in t:
                return t
        except Exception:
            pass
    return raw.decode('utf-8', 'replace')


def blocks(text):
    stack, out = [], collections.OrderedDict()
    for line in text.splitlines():
        s = line.strip()
        if s.startswith('Begin Object'):
            m = re.search(r'Name="?([^"\s]+)"?', s); stack.append([(m.group(1) if m else '?'), []])
        elif s.startswith('End Object'):
            if stack:
                name, lines = stack.pop(); key = '/'.join([n for n, _ in stack] + [name])
                out[key] = sorted(lines)
        elif stack and s:
            stack[-1][1].append(norm(s))
    return out


GUID = re.compile(r'[0-9A-F]{32}')
LOC = re.compile(r'NSLOCTEXT\("[^"]*", "[^"]*", ("[^"]*")\)')   # localized-text form (memory) vs plain string (reloaded): same text
GEN = re.compile(r'K2Node_PropertyAccess_\d+')                       # compile-generated property names, renumbered per compile


def norm(s):
    return GEN.sub('K2Node_PropertyAccess_N', LOC.sub(lambda m: m.group(1), GUID.sub('<GUID>', s)))
   # PinId / LinkedTo / GraphGuid / NodeGuid regenerate on reload or for compiler-generated graphs
res = {}
for f in sorted(os.listdir(os.path.join(D, 'mem'))):
    a, b = read(os.path.join(D, 'mem', f)), read(os.path.join(D, 'disk', f))
    if f.endswith('.cdo.t3d'):
        kv = lambda t: [l.strip().split('=', 1) for l in t.splitlines() if '=' in l and not l.strip().startswith(('Begin', 'End'))]
        A, B = kv(a), kv(b)
        pa = collections.Counter(v for k, v in A if k.startswith('K2Node_PropertyAccess_')); pb = collections.Counter(v for k, v in B if k.startswith('K2Node_PropertyAccess_'))
        da = {k: v for k, v in A if not k.startswith('K2Node_PropertyAccess_')}; db = {k: v for k, v in B if not k.startswith('K2Node_PropertyAccess_')}
        diff = {k: {'memory': da.get(k), 'disk': db.get(k)} for k in sorted(set(da) | set(db)) if da.get(k) != db.get(k)}
        res[f] = {'kind': 'cdo', 'keys_memory': len(da), 'keys_disk': len(db), 'differing_keys': diff,
                  'property_access_values_equal_as_multiset': pa == pb, 'property_access_count': [sum(pa.values()), sum(pb.values())]}
    else:
        A, B = blocks(a), blocks(b)
        only_a, only_b = sorted(set(A) - set(B)), sorted(set(B) - set(A))
        changed, pos_only = [], []
        for k in set(A) & set(B):
            if A[k] != B[k]:
                ra = [l for l in A[k] if not l.startswith(('NodePosX', 'NodePosY'))]; rb = [l for l in B[k] if not l.startswith(('NodePosX', 'NodePosY'))]
                if ra == rb:
                    pos_only.append(k)
                else:
                    sa, sb = set(A[k]), set(B[k])
                    changed.append({'object': k, 'memory_only': sorted(sa - sb)[:8], 'disk_only': sorted(sb - sa)[:8]})
        res[f] = {'kind': 'blueprint', 'objects_memory': len(A), 'objects_disk': len(B), 'only_in_memory': only_a[:20], 'only_on_disk': only_b[:20],
                  'n_only_in_memory': len(only_a), 'n_only_on_disk': len(only_b), 'changed_objects': changed[:40], 'n_changed': len(changed),
                  'n_position_only': len(pos_only)}
    print(f, json.dumps({k: v for k, v in res[f].items() if k not in ('changed_objects',)}, default=str)[:900])
    for c in res[f].get('changed_objects', [])[:6]:
        print('   CHANGED', c['object'][:120], '| MEM', c['memory_only'][:2], '| DISK', c['disk_only'][:2])
json.dump(res, open(os.path.join(D, 't3d_compare.json'), 'w'), indent=1)
