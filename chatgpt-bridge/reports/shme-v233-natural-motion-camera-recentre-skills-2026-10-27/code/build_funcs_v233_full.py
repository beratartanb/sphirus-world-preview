exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py',encoding='utf8').read(),'shm_build.py','exec'))
import builtins, shm_component_vars as CV, shm_src; importlib.reload(CV); importlib.reload(shm_src)
bp=u.load_asset(D+'/BP_SHM_HumanMotionComponent')
members={n:c for n,t,c in CV.VARS}
members.update({'Response':'SHM|Config','Anthro':'SHM|Config','OwnerChar':'SHM|Refs','Mesh':'SHM|Refs','MoveComp':'SHM|Refs','Capsule':'SHM|Refs'})
only=getattr(builtins,'SHM_ONLY',None)
# the toolset caches node types per graph, fingerprinted on THIS blueprint's structure only: a field added to the
# profile Blueprint (another class) stays invisible ('...Al does not exist') until the cache is dropped
try:
    from editor_toolset.toolsets.blueprint import _BlueprintCache; _BlueprintCache._graph_node_types.clear()
except Exception as _e: print('cache clear failed', _e)
names=[f[0] for f in shm_src.FUNCS]
res={}
for name,params,returns,src in shm_src.FUNCS:
    if only and name not in only: continue
    ids=own_function_ids(bp,[n for n in names if n!=name])
    tr=shm_dsl.Translator(members,ids,{'R':('BPSHMResponseProfile','Response'),'A':('BPSHMAnthropometryProfile','Anthro')})
    try: res[name]=rebuild_function(bp,name,params,returns,src,tr)
    except Exception as e: res[name]='FAIL '+str(e)[:2500]; break
# V2.32: the translator bridges (Piyon|GetControlRotation :self OwnerChar) through Pawn.LastHitBy (always None -> control yaw 0, 3 errors
# per frame); re-apply the V2.21 repair (LastHitBy -> Pawn::GetController) to every rebuilt function, idempotent
_lhb={'__name__':'lhb_lib'}; exec(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V221_20261021/fix_v221_lasthitby.py',encoding='utf8').read(),_lhb)
res['_lasthitby_patched']=_lhb['patch'](bp,[n for n in res if not str(res[n]).startswith('FAIL')])
st,errs=compile_ok(bp)
print(json.dumps(res,indent=1,ensure_ascii=False));print(st,[e[:600] for e in errs[:4]])
# V2.33 early-failure gate: a failed function build leaves that graph EMPTY in memory (2026-10-27 SHM_UpdateCameraV21 was saved empty by
# the next save job) -> the job itself fails, the chain stops before any save; revert / relaunch discards the emptied graph
_fails=[k for k,v in res.items() if str(v).startswith('FAIL')]
if _fails: raise RuntimeError('BUILD_FUNCS_FAILED %s' % _fails)
