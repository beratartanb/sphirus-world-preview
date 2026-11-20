# probe_bedmesh.py (read-only): top surface of the bed mesh (max vertex z on a grid, world space) + mesh / collision facts
import unreal as u
o=[]
a=[x for x in u.EditorLevelLibrary.get_all_level_actors() if x.get_actor_label()=='Furniture_R3_PatchworkBed'][0]
c=a.get_component_by_class(u.StaticMeshComponent); m=c.get_editor_property('static_mesh'); tr=a.get_actor_transform()
o.append('mesh %s sections %d loc %s rot %s scale %s'%(m.get_path_name(),m.get_num_sections(0),a.get_actor_location(),a.get_actor_rotation(),a.get_actor_scale3d()))
grid={}
for s in range(m.get_num_sections(0)):
    try:
        r=u.ProceduralMeshLibrary.get_section_from_static_mesh(m,0,s); V=r[0]
    except Exception as e: o.append('sec %d err %s'%(s,str(e)[:80])); continue
    mat=c.get_material(s); zs=[]
    for v in V:
        w=u.MathLibrary.transform_location(tr,v); k=(int((w.x-1090)//23),int((w.y-660)//27)); grid[k]=max(grid.get(k,-1e9),w.z); zs.append(w.z)
    o.append('sec %d verts %d z %.0f..%.0f mat %s'%(s,len(V),min(zs) if zs else 0,max(zs) if zs else 0,mat.get_name() if mat else None))
for j in range(8,-1,-1):
    o.append('y%3d: '%(660+j*27)+' '.join('%4.0f'%grid.get((i,j),0) for i in range(9)))
o.append('cols x: '+' '.join('%4d'%(1090+i*23) for i in range(9)))
st=[x for x in u.EditorLevelLibrary.get_all_level_actors() if x.get_actor_label()=='GR_Day_Bed'][0]
for cc in st.get_components_by_class(u.PrimitiveComponent):
    o.append('station comp %s %s col %s vis-resp %s ext %s'%(cc.get_name(),cc.get_class().get_name(),cc.get_collision_enabled(),cc.get_collision_response_to_channel(u.CollisionChannel.ECC_VISIBILITY),str(cc.get_editor_property('box_extent')) if hasattr(cc,'box_extent') or cc.get_class().get_name()=='BoxComponent' else ''))
open(u.Paths.project_dir()+'Saved/UE59Work/r4/bedmesh.txt','w',encoding='utf8').write('\n'.join(o)); print('BEDMESH',len(o))
