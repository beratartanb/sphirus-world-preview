# probe_orb.py (read-only): OffsetRootBone node settings + property bindings, stop / start database contents.
import unreal as u
T=u.BlueprintToolset; a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); o=[]
for g in T.list_graphs(a):
    for n in T.find_nodes(g):
        cn=n.get_class().get_name()
        if cn in ('AnimGraphNode_OffsetRootBone',):
            nd=n.get_editor_property('node'); o.append('ORB node in '+g.get_name()); o.append(nd.export_text()[:3000])
            try: o.append('BINDINGS '+n.export_text()[:100])
            except Exception as e: o.append('nb '+str(e)[:80])
            try:
                b=n.get_editor_property('binding'); o.append('binding obj '+str(b)); o.append(b.export_text()[:3000] if hasattr(b,'export_text') else str(b.get_editor_property('property_bindings'))[:3000])
            except Exception as e: o.append('bind err '+str(e)[:200])
AR=u.AssetRegistryHelpers.get_asset_registry()
f=u.ARFilter(class_paths=[u.TopLevelAssetPath('/Script/PoseSearch','PoseSearchDatabase')],package_paths=['/Game'],recursive_paths=True)
for ad in AR.get_assets(f):
    n=str(ad.asset_name)
    if 'Stop' in n or 'Start' in n:
        d=u.load_asset(str(ad.package_name)); names=[]
        try:
            for i in range(d.get_num_animation_assets()):
                x=d.get_animation_asset(i); names.append(x.get_name() if x else 'None')
        except Exception as e: names=['ERR '+str(e)[:80]]
        o.append('DB %s (%s): %d: %s'%(n,ad.package_name,len(names),' '.join(names)))
open(u.Paths.project_dir()+'Saved/UE59Work/r5/orb.txt','w',encoding='utf8').write('\n'.join(o)); print('ORB',len(o))
