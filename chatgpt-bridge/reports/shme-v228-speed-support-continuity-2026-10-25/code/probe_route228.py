"""probe_route228.py (editor job, READ-ONLY): the reversal database route and the bridge in ABP_GR_MotionMatchingBase.Update_MotionMatching:
nodes whose type mentions SHM224_DB_JR, SHM224_RevIntent, SHM224_RevMir, SHM224_EarlyRev, SetDatabaseToSearch, SHM_HoldDB, SHM_HoldValid,
SHM_RedirectFrames, SHM227_Restart, or the named Select_311 / Select_312 / AND_172 / OR_182 / OR_206, each with its input pin sources (one
level) and literal defaults; plus the SHM_Snapshot nodes that set SHM224_RevIntent / SHM224_RevMir (their value sources, two levels).
Prints ROUTE228 and writes probe_route228.json. No save."""
exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, src, pn, info, obj
import json, pathlib
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP); out = {}
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
def pins(p, depth=1):
    d = {}
    for q in info(p).input_pins:
        sv = src((p, q.name))
        if sv:
            d[q.name] = [s[0].rsplit('.', 1)[-1] + ':' + s[1] + ' <' + tid(s[0])[-40:] + '>' + ((' ' + json.dumps(pins(s[0], depth - 1))) if depth > 1 else '') for s in sv]
        else:
            dv = None
            for a in ('default_value', 'default', 'value'):
                if hasattr(q, a): dv = str(getattr(q, a))[:40]; break
            if dv not in (None, '', 'None'): d[q.name] = dv
    return d
KEYS = ('SHM224_DB_JR', 'SHM224_RevIntent', 'SHM224_RevMir', 'SHM224_EarlyRev', 'SetDatabaseToSearch', 'SHM_HoldDB', 'SHM_HoldValid', 'SHM227_Restart', 'SHM_RedirectFrames', 'SHM227_Hold', 'SHM227_Dead', 'SHM227_IntentEnd')
NAMES = ('K2Node_CallFunction_311', 'K2Node_CallFunction_312', 'K2Node_CommutativeAssociativeBinaryOperator_172', 'K2Node_CommutativeAssociativeBinaryOperator_182', 'K2Node_CommutativeAssociativeBinaryOperator_206')
for gname in ('Update_MotionMatching', 'SHM_Snapshot'):
    gp = pn(graph(bp, gname)); nodes = [pn(n) for n in B.find_nodes(obj(gp))]
    rows = []
    for p in nodes:
        t = tid(p); short = p.rsplit('.', 1)[-1]
        if any(k in t for k in KEYS) or short in NAMES:
            rows.append({'node': short, 'type': t[-60:], 'pins': pins(p, 2 if gname == 'SHM_Snapshot' and 'SetSHM224_Rev' in t else 1)})
    out[gname] = rows
pathlib.Path(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Saved/Codex/SHME_V228_20261025/probe_route228.json').write_text(json.dumps(out, indent=1, default=str), encoding='utf8')
print('ROUTE228 ' + json.dumps({k: len(v) for k, v in out.items()}))
