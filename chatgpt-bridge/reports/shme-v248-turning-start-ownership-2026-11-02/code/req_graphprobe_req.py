exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import G, src, pn, info, obj
import json
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
sg = pn(graph(bp, 'SHM_Snapshot')); sn = [pn(n) for n in B.find_nodes(obj(sg))]
out = {'vars': [v for v in [str(x) for x in B.list_variables(bp)] if 'SHM248' in v], 'dirty': [q.get_name().split('/')[-1] for q in u.EditorLoadingAndSavingUtils.get_dirty_content_packages()]}
def tree(ep, depth):
    s_ = src(ep)
    if not s_ or depth > 4: return str(s_)
    n, pin = s_[0]; t = tid(n).rsplit('|', 1)[-1][-40:]
    kids = {q.name: tree((n, q.name), depth + 1) for q in info(n).input_pins if q.name not in ('execute', 'self') and src((n, q.name))}
    return {t or n.rsplit('.', 1)[-1]: kids} if kids else (t or n.rsplit('.', 1)[-1])
st = [p for p in sn if tid(p).endswith('|SetSHM248_TurnStart')]
out['turnstart_src'] = tree((st[0], 'SHM248_TurnStart'), 0) if st else 'no set node'
so = [p for p in sn if tid(p).endswith('|SetSHM228_On')]
out['on_src'] = tree((so[0], 'SHM228_On'), 0) if so else 'no set node'
print('GRAPHPROBE248 ' + json.dumps(out, default=str))
