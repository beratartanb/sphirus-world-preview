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
            # the slate tick dt is clamped at 0.125 s, so the real frame time comes from the wall clock (0.3-1.5 s with window
            # screenshots in the house map); the dilation is then corrected in closed loop from the game delta actually seen
            import time as _tm
            gdt=u.GameplayStatics.get_world_delta_seconds(w_); tn=_tm.perf_counter(); rdt=max(0.004,min(4.0,tn-st.get('tlast',tn-1.0/FPS))); st['tlast']=tn
            st['rdt']=0.7*st['rdt']+0.3*rdt; dil=(1.0/FPS)/st['rdt']
            if st['f']>3 and gdt>0: dil*=max(0.5,min(2.0,(1.0/FPS)/(0.5*gdt+0.5*st.get('gprev',gdt))))
            st['gprev']=gdt
            if not getattr(builtins,'VID_NODIL',False) and not getattr(builtins,'VID_NOSHOT',False): u.GameplayStatics.set_global_time_dilation(w_,max(0.005,min(1.0,dil)))   # VID_NODIL: capture at the real game step (diagnostics)
            if st['yaw'] is None: st['yaw']=pc.get_control_rotation().yaw
            now=st['f']/FPS
            if st['seg']<0 or (st['f']-st['segf'])/FPS>=plan[st['seg']][1]:
                st['seg']+=1; st['segf']=st['f']
                if st['seg']>=len(plan): finish(); return
                setkeys(plan[st['seg']][0].split())
            seg=plan[st['seg']]; yr=seg[2]; pitch=seg[3] if len(seg)>3 else -12.0
            if yr: st['yaw']+=yr/FPS
            pc.set_control_rotation(u.Rotator(pitch=pitch,yaw=st['yaw'],roll=0))
            # VID_SIDE=(dist, angle_deg, height): body-review camera that tracks the pawn from the side / 3-4 (rack camera
            # GR_CamRack as view target; the player camera logic still runs, only the rendered view changes)
            sv=getattr(builtins,'VID_SIDE',None)
            if sv:
                if 'rack' not in st:
                    st['rack']=[a for a in u.GameplayStatics.get_all_actors_of_class(w_,u.CameraActor) if a.get_actor_label()=='GR_CamRack'][0]
                    cc=st['rack'].get_components_by_class(u.CameraComponent)[0]; cc.set_editor_property('field_of_view',40.0); cc.set_editor_property('constrain_aspect_ratio',False); cc.set_editor_property('post_process_blend_weight',0.0)
                    pc.set_view_target_with_blend(st['rack'],0.0); st['ryaw']=pw.get_actor_rotation().yaw
                pl=pw.get_actor_location(); st['ryaw']=st['ryaw']+0.15*(((pw.get_actor_rotation().yaw-st['ryaw'])+540)%360-180)
                a_=math.radians(st['ryaw']+sv[1]); cpos=u.Vector(pl.x+sv[0]*math.cos(a_),pl.y+sv[0]*math.sin(a_),pl.z+sv[2]); tgt=u.Vector(pl.x,pl.y,pl.z+10)
                st['rack'].set_actor_location_and_rotation(cpos,u.MathLibrary.find_look_at_rotation(cpos,tgt),False,True)
            k={c.get_name():c for c in pw.get_components_by_class(u.SkeletalMeshComponent)}; vis=k.get('Manny'); src=pw.mesh; ai=src.get_anim_instance()
            l=pw.get_actor_location(); v=pw.get_velocity(); r=pw.get_actor_rotation(); cm=u.GameplayStatics.get_player_camera_manager(w_,0); cl=cm.get_camera_location(); cr=cm.get_camera_rotation()
            row=dict(f=st['f'],t=round(now,3),gdt=round(gdt,4),rdt=round(dt,4),s=st['seg'],x=round(l.x,2),y=round(l.y,2),z=round(l.z,2),vx=round(v.x,1),vy=round(v.y,1),vz=round(v.z,1),yaw=round(r.yaw,1),cy=round(st['yaw'],1),
                cam=(round(cl.x,2),round(cl.y,2),round(cl.z,2),round(cr.pitch,2),round(cr.yaw,2)),fov=round(cm.get_fov_angle(),2),
                mont=(ai.get_current_active_montage().get_name() if ai.get_current_active_montage() else None))
            try: row['mm']=(str(ai.get_editor_property('MM_Asset')),round(float(ai.get_editor_property('MM_Time')),3),round(float(ai.get_editor_property('MM_Rate')),3))
            except Exception: pass
            try: row['cc']=(round(float(ai.get_curve_value('SphClip')),2),round(float(ai.get_curve_value('SphTime')),3))
            except Exception: pass
            try: row['db']=(str(ai.get_editor_property('LocoDB')).split('/')[-1].strip("'>"),int(ai.get_editor_property('GaitSel')),bool(ai.get_editor_property('ForceLegacy')),int(pw.get_editor_property('GR_GaitSel')))
            except Exception as e: row['db']=str(e)[:60]
            # GASP driver ABP selection state (ABP_Sph_GASP): selected anim / database / gait / movement state
            try:
                ca=ai.get_editor_property('CurrentSelectedAnim'); cdb=ai.get_editor_property('CurrentSelectedDatabase')
                row['gasp']=(ca.get_name() if ca else None, cdb.get_name() if cdb else None, str(ai.get_editor_property('Gait')).split('.')[-1].split(':')[0], str(ai.get_editor_property('MovementState')).split('.')[-1].split(':')[0])
            except Exception: pass
            # Sphirus motion-physics component state (AC_Sph_Motion 'SphMotion'), when present; VID_MOTION={prop: value}
            # is applied to it every frame (A/B switches such as EffortEnabled - a one-shot PIE prelude did not stick)
            try:
                mo=[c for c in pw.get_components_by_class(u.ActorComponent) if c.get_name()=='SphMotion']
                for k_,v_ in (getattr(builtins,'VID_MOTION',None) or {}).items():
                    if mo: mo[0].set_editor_property(k_,v_)
                if mo: m_=mo[0]; row['mo']=tuple(round(float(m_.get_editor_property(k)),3) for k in ('SpeedScale','AccScale','E','EUse','TurnSev','ReqLoad','Acc'))
            except Exception: pass
            try:
                va=vis.get_anim_instance(); row['br']=(round(float(va.get_editor_property('BreathAmt')),3),round(float(va.get_editor_property('BreathPhase')),1),round(float(va.get_editor_property('EUse')),3))
            except Exception: pass
            # visible-body upper-body chain: world position + yaw/pitch/roll (shoulder height, spine counter-rotation)
            try:
                ub={}
                for b in ('pelvis','spine_01','spine_03','spine_05','neck_01','head','clavicle_l','clavicle_r','upperarm_l','upperarm_r','thigh_l','thigh_r','ball_l','ball_r'):
                    tr=vis.get_socket_transform(b,u.RelativeTransformSpace.RTS_WORLD); p_=tr.translation; q_=tr.rotation.rotator()
                    ub[b]=(round(p_.x,1),round(p_.y,1),round(p_.z,1),round(q_.yaw,1),round(q_.pitch,1),round(q_.roll,1))
                row['ub']=ub
                ud={}
                for b in ('pelvis','spine_05','neck_01','clavicle_l','clavicle_r','upperarm_l','upperarm_r','thigh_l','thigh_r'):
                    tr=src.get_socket_transform(b,u.RelativeTransformSpace.RTS_WORLD); p_=tr.translation; ud[b]=(round(p_.x,1),round(p_.y,1),round(p_.z,1))
                row['ud']=ud
            except Exception: pass
            for b in bones:
                p=vis.get_socket_location(b); row['v_'+b]=(round(p.x,2),round(p.y,2),round(p.z,2))
            for b in ('foot_l','foot_r'):
                p=src.get_socket_location(b); row['s_'+b]=(round(p.x,2),round(p.y,2),round(p.z,2))
            rt=src.get_socket_transform('root',u.RelativeTransformSpace.RTS_WORLD); dr=[]
            for b in ('foot_l','foot_r','hand_l','hand_r','head','pelvis'):
                q=rt.inverse_transform_location(src.get_socket_location(b)); dr+=[round(q.x,1),round(q.y,1),round(q.z,1)]
            row['drv']=dr
            # screen framing: normalized head / pelvis screen X,Y (0-1), spring arm state, steady/idle flags
            try:
                vs=u.WidgetLayoutLibrary.get_viewport_size(w_); scr={}
                for b in ('head','pelvis'):
                    sp=pc.project_world_location_to_screen(vis.get_socket_location(b),False); scr[b]=(round(sp.x/max(vs.x,1),3),round(sp.y/max(vs.y,1),3))
                row['scr']=scr
                sa=[c for c in pw.get_components_by_class(u.SpringArmComponent)]; sa=[c for c in sa if c.get_name()=='GR_SpringArm'] or sa
                if sa: sa=sa[0]; so=sa.get_editor_property('socket_offset'); to=sa.get_editor_property('target_offset'); row['arm']=(round(sa.get_editor_property('target_arm_length'),1),round(so.x,1),round(so.y,1),round(so.z,1),round(to.x,1),round(to.y,1),round(to.z,1),bool(sa.is_collision_fix_applied()))
            except Exception as e: row['scr']='ERR '+str(e)[:60]
            try: row['flags']=(bool(pw.get_editor_property('GR_Steady')),bool(ai.get_editor_property('Idle')),round(float(ai.get_editor_property('StillTime')),2))
            except Exception as e: row['flags']=str(e)[:50]
            st['rows'].append(row)
            if not getattr(builtins,'VID_NOSHOT',False): _c('Shot showui')   # VID_NOSHOT: data only, no screenshots (real time, long tests)
            st['f']+=1
        except Exception as e:
            print('VIDERR',repr(e)[:200]); finish()
    builtins._vr=u.register_slate_post_tick_callback(tick); print('VIDREC',label,round(sum(p[1] for p in plan),1),'s')
