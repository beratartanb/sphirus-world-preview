import unreal as u
a=u.load_asset('/Game/Sphirus/Player/GASP/ABP_Sph_GASP'); cdo=u.get_default_object(a.generated_class()); o=[]
for n in ('PlantSettings_Default','PlantSettings_Stops','FootPlacement_PlantSettings','InterpolationSettings_Default','InterpolationSettings_Stops','OffsetRootBoneEnabled','OffsetRootTranslationHalfLife','OffsetRootTranslationRadius'):
    try: val=cdo.get_editor_property(n); o.append('%s = %s'%(n,val.export_text() if hasattr(val,'export_text') else val))
    except Exception as e: o.append('%s ERR %s'%(n,repr(e)[:80]))
for g in u.BlueprintToolset.list_graphs(a):
    gn=g.get_name()
    if 'lant' in gn or 'Offset' in gn or 'Steer' in gn or 'Foot' in gn: o.append('GRAPH '+gn)
open(u.Paths.project_dir()+'Saved/UE59Work/r6/plant6.txt','w',encoding='utf8').write('\n'.join(o)); print('PLANT6',len(o))
