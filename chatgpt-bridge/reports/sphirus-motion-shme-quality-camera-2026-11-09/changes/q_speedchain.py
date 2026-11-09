# q_speedchain.py (measure): print the node chain feeding SetMaxWalkSpeed (3 levels) with pin literals, to find why the
# max speed became 7.5 after cm_turn1 (GR_TurnScale 0.3 with heading error 0 -> a literal pin did not take).
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
PP='/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player'
bp=u.load_asset(PP); g=B.get_graph(bp,'EventGraph'); N=[pn(x) for x in B.find_nodes(g)]; tp=lambda p:str(info(p).type_id)
def pv(p,k):
    try: return str(B.get_pin_value([x for x in info(p).input_pins if str(x.name)==k][0].pin_id))
    except Exception: return None
def show(p,depth,seen):
    if depth<0 or str(p) in seen: return
    seen.add(str(p)); i=info(p); d={}
    for ip in i.input_pins:
        n=str(ip.name)
        if n in ('execute',): continue
        try: s=src((p,n))
        except Exception: s=[]
        d[n]=('<-'+tp(s[0][0])[-40:]+'.'+str(s[0][1])) if s else pv(p,n)
    print('  '*(3-depth)+'NODE',tp(p)[-50:],d)
    for ip in i.input_pins:
        try: s=src((p,str(ip.name)))
        except Exception: s=[]
        for q in s: show(q[0],depth-1,seen)
for p in N:
    if tp(p).endswith('SetGR_TurnScale') or tp(p).endswith('SetGR_HeadErr'): show(p,4,set())
for p in N:
    t=tp(p)
    if 'GR_TurnScale' in t or 'GR_HeadErr' in t:
        i=info(p); print('VARNODE',t[-40:],{str(x.name):pv(p,str(x.name)) for x in i.input_pins if str(x.name)!='execute'})
print('Q_DONE')
