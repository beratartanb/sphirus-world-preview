# apply_dress.py: rear work-garden and entry dressing of this pass, idempotent (deletes its own R2G_ actors and recreates them).
# Every new actor is a duplicate of an actor that is already in the map (same mesh, material, collision, level); nothing imported.
# Rear: firewood lean-to at the kitchen side of the rear door, the loose log pile now sits under it; tool rack by the door;
# stepping stones along the wall from the door to the existing chopping yard (wood route door <-> yard). Entry: rug on the door axis.
import unreal as u, builtins, random
CFG={'shed_yaw':90.0,'shed_scale':0.70,'shed_x':1120.0,'shed_y':-62.0}; CFG.update(getattr(builtins,'R2G_DRESS',None) or {})
EAS=u.get_editor_subsystem(u.EditorActorSubsystem); w=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_editor_world()
acts={a.get_actor_label():a for a in EAS.get_all_level_actors()}
for lb,a in list(acts.items()):
    if lb.startswith('R2G_Rear_') or lb.startswith('R2G_Rug_'): EAS.destroy_actor(a)
def ground(x,y):
    # landscape height only: anything else that is hit (roof edge, props, ivy) is ignored and the trace repeated
    ign=[]
    for _ in range(12):
        h=u.SystemLibrary.line_trace_single(w,u.Vector(x,y,900),u.Vector(x,y,-400),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,ign,u.DrawDebugTrace.NONE,False)
        if not h: break
        t=h.to_tuple()
        if not t[0]: break
        if t[9] and 'Landscape' in t[9].get_class().get_name(): return t[4].z
        if t[9]: ign.append(t[9])
        else: break
    return 110.0
def dup(src,lb,loc,rot=None,scale=None,folder=None):
    a=EAS.duplicate_actor(acts[src]); a.set_actor_label(lb)
    a.set_actor_location(u.Vector(*loc),False,False)
    if rot is not None: a.set_actor_rotation(u.Rotator(pitch=rot[0],yaw=rot[1],roll=rot[2]),False)
    if scale is not None: a.set_actor_scale3d(u.Vector(*scale) if isinstance(scale,(tuple,list)) else u.Vector(scale,scale,scale))
    if folder: a.set_folder_path(folder)
    return a
F='EXTERIOR/HouseLife/R2G_RearGarden'
# shed: keep the bottom of the mesh on the ground at the new scale
s0=acts['GR_Life_WoodShed']; o,e=s0.get_actor_bounds(False); base_off=(s0.get_actor_location().z-(o.z-e.z))/s0.get_actor_scale3d().z
sx,sy=CFG['shed_x'],CFG['shed_y']; gz=min(ground(sx-70,sy-40),ground(sx+70,sy-40),ground(sx,sy))
sh=dup('GR_Life_WoodShed','R2G_Rear_LogStore',(sx,sy,gz+base_off*CFG['shed_scale']-2.0),(0,CFG['shed_yaw'],0),CFG['shed_scale'],F)
o2,e2=sh.get_actor_bounds(False); print('DRESS shed bounds',[round(v) for v in (o2.x,o2.y,o2.z)],[round(v) for v in (e2.x,e2.y,e2.z)],'ground',round(gz,1))
# firewood rows under the lean-to (duplicates of the veranda stack pieces), split ends facing out
random.seed(1123); src=['AD_Life2_Wood_0_0','AD_Life2_Wood_0_1','AD_Life2_Wood_0_2','AD_Life2_Wood_1_0','AD_Life2_Wood_1_1']
n=0
for row in range(4):
    x=sx-58.0+random.uniform(-3,3)
    while x<sx+60.0:
        s=random.choice(src); be=acts[s].get_actor_bounds(False)[1]
        dup(s,'R2G_Rear_Wood_%02d'%n,(x,sy+18.0+random.uniform(-3,3),gz+14.0+row*10.5),(random.uniform(-6,6),random.uniform(-6,6),random.uniform(-10,10)),None,F); n+=1
        x+=random.uniform(15.5,19.0)
print('DRESS wood pieces',n)
# tool rack by the door (kitchen side), stones along the wall to the chopping yard
t0=acts['AD_Life_WallTools']; tl=t0.get_actor_location()
dup('AD_Life_WallTools','R2G_Rear_DoorTools',(952.0,tl.y,ground(952,-40)+(tl.z-ground(tl.x,-40))),None,None,F); print('DRESS tools z',round(ground(952,-40)+(tl.z-ground(tl.x,-40)),1),'src z',tl.z)
ST=[(1012,-178,0.60),(1108,-212,0.66),(1212,-188,0.57),(1318,-214,0.63),(1424,-186,0.60),(1528,-206,0.66),(1610,-290,0.60),(1692,-372,0.62)]   # last two pass north of the existing log pile (axis (1612,-101)-(1688,-309), 72 cm wide)
for i,(x,y,sc) in enumerate(ST):
    print('DRESS stone',i,round(ground(x,y),1)); dup('AD_Life_Step1','R2G_Rear_Stone_%d'%i,(x,y,ground(x,y)+2.0),(0,random.uniform(-180,180),0),sc,F)
# entry rug on the door axis (duplicate of an upstairs rug so the pattern is not repeated next to the hall rug)
r=dup('R05_Rug_Reading','R2G_Rug_Entry',(800.0,858.0,151.1),(0,90.0,0),(1.03,0.60,1.0),'House/Textiles/Entry')   # runner 3.1 x 1.2 m between hall rug and door mat
print('DRESS done', sorted(a.get_actor_label() for a in EAS.get_all_level_actors() if a.get_actor_label().startswith('R2G_'))[:6], 'lvl', sh.get_outer().get_outermost().get_name().split('/')[-1], r.get_outer().get_outermost().get_name().split('/')[-1])
