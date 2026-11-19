# vidc.py: vid.py recorder + camera framing fields per frame (row keys):
#  sc   normalized screen x,y of head / neck / chest / shoulders / hands / pelvis / feet and of the plan's aim target ('tgt')
#  occ  body parts (head, neck, chest, shoulders, far arm) that cover the camera ray to each hand / the target
#  wocc world hit distance on the camera ray to each hand / target (pawn ignored), None = free
#  cine (focus distance, aperture, focal length), vt view target name, st (look ignored, move ignored, carry, home, crouched, falling)
#  sc2  SphCamera component variables (builtins.VIDC_CAMVARS), VID_CAM = per-frame overrides on that component
import unreal as u, builtins
_src=open(u.Paths.project_dir()+'Tools/Day_20261107/vid.py',encoding='utf8').read()
_k="            st['rows'].append(row)"; assert _src.count(_k)==1
_src=_src.replace(_k,"            _vidc_extra(row,pw,pc,vis,w_,cm,seg,st)\n"+_k)
# The harness plays the PLAYER's look: while a station has the look locked (IsLookInputIgnored) it must not write the control
# rotation (the real player cannot either) - it follows the camera's own assisted look and continues from the seen angle;
# a segment's fixed pitch is approached at 120 deg/s instead of snapping.
_k2="            else: st['pitch']=pitch\n"; assert _src.count(_k2)==1
_src=_src.replace(_k2,"            else:\n                st['pitch']=st.get('pitch',pitch); st['pitch']+=max(-120.0/FPS,min(120.0/FPS,pitch-st['pitch'])); pitch=st['pitch']\n")
_k3="            pc.set_control_rotation(u.Rotator(pitch=pitch,yaw=st['yaw'],roll=0))\n"; assert _src.count(_k3)==1
_src=_src.replace(_k3,"            if pc.is_look_input_ignored() or (getattr(builtins,'VID_HANDSOFF',False) and st.get('locked')):\n                st['locked']=True; cr_=pc.get_control_rotation(); st['yaw']=cr_.yaw; st['pitch']=((cr_.pitch+180.0)%360.0)-180.0\n            else: pc.set_control_rotation(u.Rotator(pitch=pitch,yaw=st['yaw'],roll=0))\n")
exec(open(u.Paths.project_dir()+'Tools/Camera_20261112/vidc_goto.py',encoding='utf8').read())
exec(open(u.Paths.project_dir()+'Tools/Camera_20261112/vidc_neck.py',encoding='utf8').read())
_OR={'head':11.5,'neck_01':7.0,'spine_05':16.0,'spine_03':16.0,'clavicle_r':9.0,'clavicle_l':9.0,'upperarm_r':6.0,'upperarm_l':6.0}
def _vidc_extra(row,pw,pc,vis,w_,cm,seg,st):
    try:
        vs=u.WidgetLayoutLibrary.get_viewport_size(w_); cl=cm.get_camera_location(); S={}
        pts={b:vis.get_socket_location(b) for b in ('head','neck_01','spine_05','spine_03','clavicle_r','clavicle_l','upperarm_r','upperarm_l','hand_r','hand_l','pelvis','foot_r','foot_l')}
        if len(seg)>4 and seg[4]: pts['tgt']=u.Vector(*seg[4])
        sc_=[c for c in pw.get_components_by_class(u.ActorComponent) if c.get_name()=='SphCamera']
        if sc_:
            c_=sc_[0]
            at_=getattr(builtins,'VID_AT',None) or {}
            if st['f'] in at_:
                try:
                    if at_[st['f']]==1: c_.call_method('ResPulse',args=(1.0,2.5)); row['at']='ResPulse'
                except Exception as e: row['at']='ERR '+repr(e)[:80]
            for k_,v_ in (getattr(builtins,'VID_CAM',None) or {}).items():
                try:
                    if c_.get_editor_property(k_)!=v_: c_.set_editor_property(k_,v_,u.PropertyAccessChangeNotifyMode.NEVER)
                except Exception as e: row['camerr']=str(e)[:60]
            d_={}
            for k_ in getattr(builtins,'VIDC_CAMVARS',()):
                try:
                    v_=c_.get_editor_property(k_)
                    d_[k_]=[round(v_.x,1),round(v_.y,1),round(v_.z,1)] if isinstance(v_,u.Vector) else (round(v_,3) if isinstance(v_,float) else (v_ if isinstance(v_,(int,bool)) else str(v_)[:40]))
                except Exception: pass
            row['sc2']=d_
            try:
                if bool(c_.get_editor_property('CtxActive')): pts['ctx']=c_.get_editor_property('CtxTarget')
            except Exception: pass
        for k,p in pts.items():
            sp=pc.project_world_location_to_screen(p,False); S[k]=(round(sp.x/max(vs.x,1),3),round(sp.y/max(vs.y,1),3)) if sp is not None else None
        row['sc']=S; occ={}; wocc={}
        sa_=[c for c in pw.get_components_by_class(u.SpringArmComponent) if c.get_name()=='GR_SpringArm']
        if sa_: so_=sa_[0].get_editor_property('socket_offset'); to_=sa_[0].get_editor_property('target_offset'); row['arm']=(round(sa_[0].get_editor_property('target_arm_length'),1),round(so_.x,1),round(so_.y,1),round(so_.z,1),round(to_.x,1),round(to_.y,1),round(to_.z,1),bool(sa_[0].is_collision_fix_applied()))
        for k in ('hand_r','hand_l','tgt','ctx'):
            if k not in pts: continue
            b=pts[k]; ab=b-cl; L2=max(ab.x*ab.x+ab.y*ab.y+ab.z*ab.z,1e-6); hit=[]
            for bn,r in _OR.items():
                if k.startswith('hand') and bn[-1]==k[-1] and bn[:3] in ('upp','cla'): continue
                p=pts[bn]; ap=p-cl; t=max(0.0,min(1.0,(ap.x*ab.x+ap.y*ab.y+ap.z*ab.z)/L2)); q=cl+ab*t-p
                if (q.x*q.x+q.y*q.y+q.z*q.z)**0.5<r and t<0.96: hit.append(bn)
            occ[k]=hit
            try:
                h=u.SystemLibrary.line_trace_single(w_,cl,b,u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[pw],u.DrawDebugTrace.NONE,True)
                wocc[k]=round(float(h.to_tuple()[3]),1) if h else None
            except Exception as e: wocc[k]='E'+str(e)[:30]
        row['occ']=occ; row['wocc']=wocc
        # posture review: elbows, neck_02, eyes (head tilt / yaw / pitch from the eye line), body-ABP posture overrides
        try:
            row['ub2']={b:[round(v,1) for v in (lambda q:(q.x,q.y,q.z))(vis.get_socket_location(b))] for b in ('lowerarm_l','lowerarm_r','neck_02','calf_l','calf_r','spine_04')}
            fc=[c for c in pw.get_components_by_class(u.SkeletalMeshComponent) if c.get_name()=='Face']
            if getattr(builtins,'VID_NECK',False):
                fw_=pw.get_actor_forward_vector(); row['nk']={'fw':[round(fw_.x,4),round(fw_.y,4)],**{b_:[round(v_,2) for v_ in (lambda q:(q.x,q.y,q.z))(vis.get_socket_location(b_))] for b_ in ('spine_05','neck_01','neck_02','head','clavicle_l','clavicle_r')}}
            if fc: row['eyes']=[[round(v,2) for v in (lambda q:(q.x,q.y,q.z))(fc[0].get_socket_location(b))] for b in ('FACIAL_L_Eye','FACIAL_R_Eye')]
            va_=vis.get_anim_instance(); seq_=getattr(builtins,'VID_BODYSEQ',None) or {}
            if st['f'] in seq_: st['bodyov']=dict(st.get('bodyov') or {},**seq_[st['f']])
            ov_=dict(getattr(builtins,'VID_BODY',None) or {},**(st.get('bodyov') or {}))
            for k_,v_ in ov_.items():
                val_=(u.Vector(*v_) if (k_[:1]=='V' and k_[2:3]=='_') else u.Rotator(roll=v_[0],pitch=v_[1],yaw=v_[2])) if isinstance(v_,(tuple,list)) else v_
                va_.set_editor_property(k_,val_,u.PropertyAccessChangeNotifyMode.NEVER)
            if ov_: row['bodyov']={k_:v_ for k_,v_ in ov_.items()}
            try: row['bsig']=[round(float(va_.get_editor_property(k_)),3) for k_ in ('RunA','AccA','EffA','ArmW','HeadA','Fat','BreathAmt')]
            except Exception: pass
            try: rp_=va_.get_editor_property('RPt'); row['reach']=[round(float(va_.get_editor_property('RAR')),3),round(float(va_.get_editor_property('RAL')),3),round(rp_.x,1),round(rp_.y,1),round(rp_.z,1)]
            except Exception: pass
        except Exception as e: row['ub2err']=repr(e)[:100]
        try:
            rp_=getattr(builtins,'VID_REFPOSE',None)
            if rp_ and st['f']==rp_: vis.set_animation_mode(u.AnimationMode.ANIMATION_SINGLE_NODE); row['refpose']=1
            for k_,v_ in (getattr(builtins,'VID_PAWN',None) or {}).items():
                if pw.get_editor_property(k_)!=v_: pw.set_editor_property(k_,v_,u.PropertyAccessChangeNotifyMode.NEVER)
            cm_=pw.get_movement_component()
            row['gt']=[int(pw.get_editor_property('GR_Pace')),bool(pw.get_editor_property('GR_Tempo')),int(pw.get_editor_property('GR_GaitSel')),round(float(pw.get_editor_property('SphContextSpeedScale')),3),round(float(pw.get_editor_property('GR_JumpPend')),1),round(float(cm_.get_editor_property('max_walk_speed')),1),round(float(cm_.get_editor_property('jump_z_velocity')),1),bool(pw.get_editor_property('GR_Load2H'))]
        except Exception as e: row['gterr']=repr(e)[:100]
        try: row['g4']=[int(pw.get_editor_property('GR_RunBlock')),bool(pw.get_editor_property('GR_Back')),int(pw.get_editor_property('GR_Gait')),round(float(cm_.get_editor_property('rotation_rate').yaw),1),bool(cm_.get_editor_property('orient_rotation_to_movement'))]
        except Exception: pass
        try:
            ai2=pw.mesh.get_anim_instance(); d_=[]
            for k_ in ('RotationMode','MovementDirection','Direction','Gait','MovementState','Trj_FutureVelocity','MovementDirectionBias'):
                try:
                    v_=ai2.get_editor_property(k_); d_.append(round(float(v_),1) if isinstance(v_,float) else ([round(v_.x),round(v_.y)] if hasattr(v_,'x') else str(v_).split(':')[0][-16:]))
                except Exception as e_: d_.append('E:'+k_)
            row['g4d']=d_
        except Exception: pass
        cn=[c for c in pw.get_components_by_class(u.CineCameraComponent)]
        if cn: row['cine']=(round(cn[0].get_editor_property('current_focus_distance'),1),round(cn[0].get_editor_property('current_aperture'),2),round(cn[0].get_editor_property('current_focal_length'),2))
        try: row['vt']=pc.get_view_target().get_name()
        except Exception: pass
        cmv=pw.get_movement_component()
        try:
            if getattr(builtins,'_VHUBW',None)!=pw.get_world().get_path_name():
                builtins._VHUBW=pw.get_world().get_path_name()
                builtins._VHUB=[a_ for a_ in u.GameplayStatics.get_all_actors_of_class(pw.get_world(),u.Actor) if a_.get_class().get_name().startswith('BP_GR_DayHub')]
            h_=builtins._VHUB[0] if builtins._VHUB else None
            if h_: row['hub']=[int(h_.get_editor_property(k_)) if not isinstance(h_.get_editor_property(k_),bool) else bool(h_.get_editor_property(k_)) for k_ in ('GR_Wood','GR_Split','GR_Loose','GR_Fire','GR_Busy')]
            if h_ and st['f']%5==0:
                pp_=[]
                for a_ in (h_.get_editor_property('GR_Pieces') or []):
                    if a_ and a_.root_component and a_.root_component.is_visible(): l_=a_.get_actor_location(); pp_.append([round(l_.x),round(l_.y),round(l_.z),bool(a_.get_editor_property('GR_Settled')),bool(a_.is_actor_tick_enabled()),round(a_.get_actor_tick_interval(),2),round(a_.get_horizontal_distance_to(pw)),round(float(a_.get_editor_property('GR_AutoPickR')))])
                row['pcs']=pp_
        except Exception as e_: row['huberr']=str(e_)[:80]
        row['st']=(bool(pc.is_look_input_ignored()),bool(pc.is_move_input_ignored()),bool(pw.get_editor_property('GR_CarryActive')),round(float(pw.get_editor_property('GR_HomeContext')),2),bool(pw.get_editor_property('is_crouched')) if hasattr(pw,'is_crouched') else False,bool(cmv.is_falling()))
        try: row['pp']=(round(float(pw.get_editor_property('GR_CamOpen')),2),round(float(pw.get_editor_property('GR_CamFov')),1))
        except Exception: pass
    except Exception as e: row['scerr']=repr(e)[:120]
_k4="if not getattr(builtins,'VID_NODIL',False) and not getattr(builtins,'VID_NOSHOT',False): u.GameplayStatics.set_global_time_dilation"
assert _src.count(_k4)==1
# VID_DIL: keep the fixed-step time dilation without screenshots (frame-rate tests at 60 / 120 Hz game steps)
_src=_src.replace(_k4,"if not getattr(builtins,'VID_NODIL',False) and (getattr(builtins,'VID_DIL',False) or not getattr(builtins,'VID_NOSHOT',False)): u.GameplayStatics.set_global_time_dilation")
# 2026-11-18 measurement-reliability patch (exact plan yaw, flag reads, ground traces): Tools/UE59_20261118/vidm_patch.py
if not getattr(builtins,'VID_NOPATCH18',False): exec(open(u.Paths.project_dir()+'Tools/UE59_20261118/vidm_patch.py',encoding='utf8').read())
exec(_src)
