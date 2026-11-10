# cal_breath.py (exec'd in a PIE job after h.py): axis calibration of the ABP_Sph_Body_GASP breathing layer.
# For each config (one bone group active, exaggerated 20 deg, one axis) it samples 2.5 s every frame and regresses
# against s = sin(BreathPhase) * BreathAmt: shoulder elevation (upperarm-clavicle z, L and R), neck height over pelvis,
# neck forward offset (capsule frame). Writes Saved/Codex/Day_20261107/cal_breath.json and prints CAL lines.
import builtins, json, math
def calrun():
    pw=PW; k={c.get_name():c for c in pw.get_components_by_class(u.SkeletalMeshComponent)}; vis=k['Manny']; ai=vis.get_anim_instance()
    cfgs=[]
    for ax,v in (('X',u.Vector(1,0,0)),('Y',u.Vector(0,1,0)),('Z',u.Vector(0,0,1))):
        cfgs.append(('clav',ax,v)); cfgs.append(('chest',ax,v))
    st=dict(i=-1,t=0.0,rows=[],res=[])
    def setcfg(c):
        z=u.Vector(0,0,0)
        if c[0]=='clav': ai.set_editor_property('ChestDeg',0.0); ai.set_editor_property('ClavDeg',20.0); ai.set_editor_property('ClavAxisL',c[2]); ai.set_editor_property('ClavAxisR',c[2])
        else: ai.set_editor_property('ClavDeg',0.0); ai.set_editor_property('ChestDeg',20.0); ai.set_editor_property('ChestAxis',c[2])
    def slope(xs,ys):
        mx=sum(xs)/len(xs); my=sum(ys)/len(ys); sxx=sum((x-mx)**2 for x in xs) or 1e-9; return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sxx
    def tick(dt):
        try:
            w_=u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
            if st['i']<0 or st['t']>2.5:
                if st['i']>=0 and st['rows']:
                    R=st['rows']; s=[r[0] for r in R]
                    res=dict(cfg=cfgs[st['i']][0]+cfgs[st['i']][1],n=len(R),srange=round(max(s)-min(s),3))
                    for j,nm in ((1,'shL'),(2,'shR'),(3,'neckZ'),(4,'neckFwd'),(5,'chestFwd')): res[nm]=round(slope(s,[r[j] for r in R]),2)
                    st['res'].append(res); print('CAL',res)
                st['i']+=1; st['t']=0.0; st['rows']=[]
                if st['i']>=len(cfgs):
                    u.unregister_slate_post_tick_callback(builtins._calcb); ai.set_editor_property('ChestDeg',2.0); ai.set_editor_property('ClavDeg',2.5)
                    open(u.Paths.project_dir()+'Saved/Codex/Day_20261107/cal_breath.json','w').write(json.dumps(st['res'])); print('CALDONE'); return
                setcfg(cfgs[st['i']]); return
            st['t']+=u.GameplayStatics.get_world_delta_seconds(w_)
            if st['t']<0.4: return
            s=math.sin(math.radians(ai.get_editor_property('BreathPhase')))*ai.get_editor_property('BreathAmt')
            g=lambda b: vis.get_socket_location(b)
            yw=math.radians(pw.get_actor_rotation().yaw); fx,fy=math.cos(yw),math.sin(yw)
            ul,cl,ur,cr,nk,pv,sp=g('upperarm_l'),g('clavicle_l'),g('upperarm_r'),g('clavicle_r'),g('neck_01'),g('pelvis'),g('spine_05')
            st['rows'].append((s,ul.z-cl.z,ur.z-cr.z,nk.z-pv.z,(nk.x-pv.x)*fx+(nk.y-pv.y)*fy,(sp.x-pv.x)*fx+(sp.y-pv.y)*fy))
        except Exception as e:
            print('CALERR',str(e)[:200]); u.unregister_slate_post_tick_callback(builtins._calcb)
    builtins._calcb=u.register_slate_post_tick_callback(tick); print('CAL started',len(cfgs))
