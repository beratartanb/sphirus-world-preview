exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
from qa_graph import src, pn, info, obj
AP = '/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase'
bp = u.load_asset(AP)
def tid(p):
    try: return str(info(p).type_id)
    except Exception: return ''
for gn in ('Enable_AO', 'Get_AOValue'):
    g = graph(bp, gn)
    if not g: print('NOGRAPH', gn); continue
    for n in B.find_nodes(obj(pn(g))):
        p = pn(n); print('N', gn, p.rsplit('.', 1)[-1], tid(p)[-60:], [(q.name, [s[0].rsplit('.', 1)[-1] + ':' + s[1] for s in src((p, q.name))][:2], str(q.value)[:20]) for q in info(p).input_pins][:4])
ag = pn(graph(bp, 'AnimGraph'))
for n in B.find_nodes(obj(ag)):
    c = n.get_class().get_name()
    if any(k in c for k in ('Aim', 'LookAt', 'Layer', 'Linked')): print('AG', c, pn(n).rsplit('.', 1)[-1])
# V2.40: input pins (source + literal) of every aim / look-at node, and the graphs whose name mentions AO / Look / Aim
for n in B.find_nodes(obj(ag)):
    c = n.get_class().get_name()
    if any(k in c for k in ('Aim', 'LookAt', 'BlendSpace', 'Layer', 'Linked')):
        p = pn(n)
        for q in info(p).input_pins:
            print('AGPIN', c, p.rsplit('.', 1)[-1], q.name, [s[0].rsplit('.', 1)[-1] + ':' + s[1] + ':' + tid(s[0])[-40:] for s in src((p, q.name))][:3], str(q.value)[:60])
        for prop in ('blend_space', 'BlendSpace', 'node'):
            try: print('AGPROP', p.rsplit('.', 1)[-1], prop, str(n.get_editor_property(prop))[:300])
            except Exception: pass
print('GRAPHS', [x.get_name() for x in B.list_graphs(bp) if any(k in x.get_name() for k in ('AO', 'Look', 'Aim', 'Head', 'Gaze'))])
for gn in ('Get_AOValue', 'Enable_AO'):
    g = graph(bp, gn)
    if not g: continue
    for n in B.find_nodes(obj(pn(g))):
        p = pn(n)
        for q in info(p).input_pins:
            ss = src((p, q.name))
            if ss: print('LINK', gn, p.rsplit('.', 1)[-1], tid(p)[-50:], q.name, '<-', [s[0].rsplit('.', 1)[-1] + ':' + s[1] for s in ss])
