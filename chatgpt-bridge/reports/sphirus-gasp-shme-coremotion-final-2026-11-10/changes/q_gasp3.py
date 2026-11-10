# q_gasp3.py (read-only): how the GASP ABP reads the pawn; GASP character graphs/variables.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
import collections
for path in ['/Game/Blueprints/SandboxCharacter_CMC_ABP','/Game/Blueprints/SandboxCharacter_CMC']:
    bp=u.load_asset(path); gs=B.list_graphs(bp); print('==',path,'graphs',len(gs))
    print('  GRAPHS',[g.get_name() for g in gs][:80])
    cnt=collections.Counter(); hits=[]
    for g in gs:
        try: ns=B.find_nodes(g)
        except Exception as e: continue
        for n in ns:
            p=pn(n); t=str(info(p).type_id)
            if any(k in t for k in ('Cast','BPI_','Interface','Message','GetOwningActor','TryGetPawnOwner','GetCharacterMovement','PropertyAccess')):
                cnt[t]+=1
    for t,c in cnt.most_common(40): print('  NODE',c,t[:160])
    try: print('  VARS',[str(v) for v in B.list_variables(bp)][:120])
    except Exception as e: print('  VARS ERR',str(e)[:80])
