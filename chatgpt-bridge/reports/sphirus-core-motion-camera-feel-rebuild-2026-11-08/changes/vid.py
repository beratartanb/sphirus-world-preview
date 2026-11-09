# vid.py: vidrec(label, plan): gameplay video capture at a 30 fps game step. Each editor frame writes one window screenshot;
# the global time dilation is set every frame to (1/30) / last real frame time so the game advances ~1/30 s per frame
# (t.FixedFrameRate is not honoured in PIE). The real game delta of every frame is recorded (gdt) for verification. plan = [(keys, seconds, yawRate, pitch)]; keys are injected console presses.
# Per-frame data (capsule, velocity, yaw, camera, feet, montage, MM pick when available) goes to rec/<label>.json.
import json,builtins,math,os
RD=u.Paths.project_dir()+'Saved/Codex/Grip_20261106/rec/'; os.makedirs(RD,exist_ok=True)
def _w(): return u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
def _c(c):
    w_=_w(); u.SystemLibrary.execute_console_command(w_,c,u.GameplayStatics.get_player_controller(w_,0))
def vidrec(label,plan,bones=('foot_l','foot_r','pelvis','head','hand_r','hand_l')):
    st=dict(seg=-1,f=0,segf=0,rows=[],down=[],yaw=None,done=False)
    FPS=30.0
    _c('DisableAllScreenMessages'); st['rdt']=1.0/FPS
    def setkeys(ks):
        for x in st['down']:
            if x not in ks: _c('Input.-key '+x)
        for x in ks:
            if x not in st['down']: _c('Input.+key '+x+' true')
        st['down']=list(ks)
    def finish():
        st['done']=True; setkeys([])
        try: u.GameplayStatics.set_global_time_dilation(_w(),1.0)
        except Exception: pass
        try: u.unregister_slate_post_tick_callback(builtins._vr)
        except Exception: pass
        open(RD+label+'.json','w').write(json.dumps(dict(label=label,plan=plan,fps=FPS,rows=st['rows']))); print('VIDDONE',label,len(st['rows']))
    def tick(dt):
        try:
            if st['done']: return
            w_=_w(); pc=u.GameplayStatics.get_player_controller(w_,0) if w_ else None
            if pc is None or pc.get_controlled_pawn() is None: return
            pw=pc.get_controlled_pawn()
            # real frame time with window screenshots is 0.3-1.5 s in the house map, so the dilation must go down to ~0.02
            gdt=u.GameplayStatics.get_world_delta_seconds(w_); rdt=max(0.004,min(4.0,dt)); st['rdt']=0.7*st['rdt']+0.3*rdt
            u.GameplayStatics.set_global_time_dilation(w_,max(0.005,min(1.0,(1.0/FPS)/st['rdt'])))
            if st['yaw'] is None: st['yaw']=pc.get_control_rotation().yaw
            now=st['f']/FPS
            if st['seg']<0 or (st['f']-st['segf'])/FPS>=plan[st['seg']][1]:
                st['seg']+=1; st['segf']=st['f']
                if st['seg']>=len(plan): finish(); return
                setkeys(plan[st['seg']][0].split())
            seg=plan[st['seg']]; yr=seg[2]; pitch=seg[3] if len(seg)>3 else -12.0
            if yr: st['yaw']+=yr/FPS
            pc.set_control_rotation(u.Rotator(pitch=pitch,yaw=st['yaw'],roll=0))
            k={c.get_name():c for c in pw.get_components_by_class(u.SkeletalMeshComponent)}; vis=k.get('Manny'); src=pw.mesh; ai=src.get_anim_instance()
            l=pw.get_actor_location(); v=pw.get_velocity(); r=pw.get_actor_rotation(); cm=u.GameplayStatics.get_player_camera_manager(w_,0); cl=cm.get_camera_location(); cr=cm.get_camera_rotation()
            row=dict(f=st['f'],t=round(now,3),gdt=round(gdt,4),rdt=round(dt,4),s=st['seg'],x=round(l.x,2),y=round(l.y,2),z=round(l.z,2),vx=round(v.x,1),vy=round(v.y,1),vz=round(v.z,1),yaw=round(r.yaw,1),cy=round(st['yaw'],1),
                cam=(round(cl.x,2),round(cl.y,2),round(cl.z,2),round(cr.pitch,2),round(cr.yaw,2)),fov=round(cm.get_fov_angle(),2),
                mont=(ai.get_current_active_montage().get_name() if ai.get_current_active_montage() else None))
            try: row['mm']=(str(ai.get_editor_property('MM_Asset')),round(float(ai.get_editor_property('MM_Time')),3),round(float(ai.get_editor_property('MM_Rate')),3))
            except Exception: pass
            for b in bones:
                p=vis.get_socket_location(b); row['v_'+b]=(round(p.x,2),round(p.y,2),round(p.z,2))
            for b in ('foot_l','foot_r'):
                p=src.get_socket_location(b); row['s_'+b]=(round(p.x,2),round(p.y,2),round(p.z,2))
            rt=src.get_socket_transform('root',u.RelativeTransformSpace.RTS_WORLD); dr=[]
            for b in ('foot_l','foot_r','hand_l','hand_r','head','pelvis'):
                q=rt.inverse_transform_location(src.get_socket_location(b)); dr+=[round(q.x,1),round(q.y,1),round(q.z,1)]
            row['drv']=dr
            st['rows'].append(row)
            _c('Shot showui'); st['f']+=1
        except Exception as e:
            print('VIDERR',repr(e)[:200]); finish()
    builtins._vr=u.register_slate_post_tick_callback(tick); print('VIDREC',label,round(sum(p[1] for p in plan),1),'s')
