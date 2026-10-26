exec(compile(open(r'C:/Users/berat/OneDrive/Documents/Unreal Projects/ActionAdventureMovementS/Tools/SHME_V1_20260925/shm_build.py', encoding='utf8').read(), 'shm_build.py', 'exec'))
bp = u.load_asset('/Game/GraceRanger/SHME/BP_SHM_HumanMotionComponent'); g = graph(bp, 'SHM_UpdateCameraV21')
for q in ('GetPathName', 'GetObjectName', 'GetDisplayName', 'EqualEqual_StrStr', 'Equal (String)'):
    try: print('NT', q, [getattr(x, 'type_id', x) for x in B.find_node_types(g, q)][:8])
    except Exception as e: print('NT', q, 'ERR', e)
print('NODES', len(B.find_nodes(g)))
