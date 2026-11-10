import unreal as u, re, json
D='/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/'
c=u.load_asset(D+'CHT_PoseSearchDatabases_Relaxed'); out={}
out['ctx']=[str(x.export_text()) for x in c.get_editor_property('context_data')]
out['cols']=[str(x.export_text()) for x in c.get_editor_property('columns_structs')]
abp=u.load_object(None,'/Game/Sphirus/Player/GASP/ABP_Sph_GASP.ABP_Sph_GASP_C'); cdo=u.get_default_object(abp)
names=sorted(set(re.findall(r'PropertyBindingChain=\(([^)]*)\)',' '.join(out['cols']))))
out['bind']={}
for n in names:
    f=n.split(',')[0].strip('"')
    try: out['bind'][n]=str(cdo.get_editor_property(f))[:80]
    except Exception: out['bind'][n]='MISSING'
import glob
out['dbs']={}
for a in u.EditorAssetLibrary.list_assets(D+'Databases',True,False):
    db=u.load_asset(a)
    if not db or db.get_class().get_name()!='PoseSearchDatabase': continue
    L=[]
    for i in range(db.get_num_animation_assets()):
        x=db.get_animation_asset(i); L.append(x.get_name() if x else None)
    out['dbs'][a.split('/')[-1].split('.')[0]]=L
json.dump(out,open(u.Paths.project_dir()+'Tools/GASP_20261109/rx_inventory.json','w'),indent=1); print('RXINV',len(out['dbs']))
