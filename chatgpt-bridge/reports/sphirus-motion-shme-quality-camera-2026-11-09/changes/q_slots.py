# q_slots.py (measure): is the DefaultSlot output linked twice (UpperBody slot source + layered blend base)? A node with two
# consumers is updated twice per frame in an anim graph, which doubles sequence-player time (idle at 2x) and corrupts the
# pose-history trajectory. Also lists cached-pose node types and the slots the project montages use.
exec(open(__import__('unreal').Paths.project_dir()+'Tools/SF52_20261105/g_common.py',encoding='utf8').read())
d=u.load_asset('/Game/Sphirus/Player/Anim/ABP_Sph_Driver'); ag=[g for g in B.list_graphs(d) if g.get_name()=='AnimGraph'][0]
nodes=B.find_nodes(ag); handles={str(pn(n)):n for n in nodes}
def label(n):
    cn=n.get_class().get_name()
    if cn=='AnimGraphNode_Slot': return 'Slot:'+str(n.get_editor_property('node').get_editor_property('slot_name'))
    return cn
cons={}
for n in nodes:
    p=pn(n)
    for ip in info(p).input_pins:
        try: s=src((p,str(ip.name)))
        except Exception: s=[]
        for q in s: cons.setdefault(str(q[0]),[]).append(label(n)+'.'+str(ip.name))
for k,v in cons.items():
    n=handles.get(k); print('OUT',label(n) if n else k[-40:],'->',v,'| LINKS',len(v))
print('TYPES',[t for t in B.find_node_types(ag,'Cache')][:8],[t for t in B.find_node_types(ag,'nbellek')][:8],[t for t in B.find_node_types(ag,'Kayde')][:8])
AR=u.AssetRegistryHelpers.get_asset_registry()
for a in AR.get_assets_by_class(u.TopLevelAssetPath('/Script/Engine','AnimMontage'),True):
    p=str(a.package_name)
    if '/Sphirus/' in p or '/GraceRanger/' in p:
        m=u.load_asset(p)
        try: print('MONTAGE',p.split('/')[-1],[str(t.get_editor_property('slot_name')) for t in m.get_editor_property('slot_anim_tracks')])
        except Exception as e: print('MONTAGE',p.split('/')[-1],'ERR',str(e)[:60])
print('Q_DONE')
