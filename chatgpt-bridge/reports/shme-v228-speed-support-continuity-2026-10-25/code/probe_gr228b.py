"""probe_gr228b.py (editor job, READ-ONLY): BP_GR_Player graph structure for the clip-speed patch: for UpdateMovement_PreCMC,
CalculateGroundFriction, CalculateMaxAcceleration, GR_UpdateSHMSignals, GR_Impl_CP_PhysicalRedirect list every node (short name, type id,
input pins with their sources for exec/velocity-related nodes). Also every variable of BP_GR_Player whose name mentions SHM / Redirect /
Clip, and whether a BP_SHM component getter exists in any of those graphs. Prints PROBEGR228B; writes probe_gr228b.json. No save."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, src, pn, info, obj, op
import json, pathlib
PB = '/Game/GraceRanger/BP_GR_Player'
bp = u.load_asset(PB); out = {}
try: out['vars'] = [v for v in B.list_variables(bp) if any(k in str(v) for k in ('SHM', 'Redirect', 'Clip', 'Friction', 'Brake'))]
except Exception as e: out['vars'] = 'ERR ' + str(e)[:80]
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
for gname in ('UpdateMovement_PreCMC', 'CalculateGroundFriction', 'CalculateMaxAcceleration', 'GR_UpdateSHMSignals', 'GR_Impl_CP_PhysicalRedirect'):
    try:
        g = G(op(PB) + ':' + gname); nodes = [pn(n) for n in B.find_nodes(obj(g.path))]
        rows = []
        for p in nodes:
            t = tid(p); short = p.rsplit('.', 1)[-1]
            try:
                ins = [(q.name, [s[0].rsplit('.', 1)[-1] + ':' + s[1] for s in src((p, q.name))]) for q in info(p).input_pins]
                ins = [(a, b) for a, b in ins if b]
            except Exception: ins = []
            rows.append((short, t[-70:], ins[:6]))
        out[gname] = {'n': len(nodes), 'nodes': rows, 'shm_getter': [r[0] for r in rows if 'BP_SHM' in r[1] or 'GetComponentByClass' in r[1]]}
    except Exception as e: out[gname] = 'ERR ' + str(e)[:120]
pathlib.Path(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V228_20261025/probe_gr228b.json').write_text(json.dumps(out, indent=1, default=str), encoding='utf8')
print('PROBEGR228B ' + json.dumps({k: (v if isinstance(v, str) else {'n': v['n'], 'shm_getter': v['shm_getter'], 'types': sorted(set(r[1].rsplit('|', 1)[-1][-28:] for r in v['nodes']))[:40]}) for k, v in out.items()}, default=str)[:3000])
