# vidm_patch.py (2026-11-18): measurement-reliability fixes applied to the vid.py source (inside vidc.py, before exec).
# 1 exact plan yaw: a segment lasts round(dur*FPS) frames and turns exactly yawRate*dur in total. Before, a 0.25 s flick lasted
#   ceil(7.5)=8 frames at 30 Hz and turned 8*rate/30, i.e. 48/96/144/192 deg for the requested 45/90/135/180.
#   row['yreq'] = cumulative requested yaw of the plan (deg, unwrapped), so analysers can separate requested and applied turn.
# 2 flags: each flag read on its own; a property that does not exist on the current ABP is recorded as None (it was the
#   string "ABP_Sph_GASP_C: Failed to find property 'Idle'...", an observer error, not a game error).
# 3 ground truth under the body: line traces (visibility channel, pawn ignored) under the visible balls and ankles and under
#   the capsule; capsule half height; hit component; mesh component heights. row['gnd'] = dict(f=[[z, nz] x4], cap=[hh, z, nz, actor, comp], mz=[vis z, drv z])
_a = "(st['f']-st['segf'])/FPS>=plan[st['seg']][1]"   # also present after vidc_goto's ' or goto_done' extension
assert _src.count(_a) == 1
_src = _src.replace(_a, "(st['f']-st['segf'])>=max(1,int(round(plan[st['seg']][1]*FPS)))")
_b = "            if yr: st['yaw']+=yr/FPS\n"
assert _src.count(_b) == 1
_src = _src.replace(_b, "            if yr:\n                _dy=yr*seg[1]/max(1,int(round(seg[1]*FPS))); st['yaw']+=_dy; st['yreq']=st.get('yreq',0.0)+_dy\n")
_c = "            try: row['flags']=(bool(pw.get_editor_property('GR_Steady')),bool(ai.get_editor_property('Idle')),round(float(ai.get_editor_property('StillTime')),2))\n            except Exception as e: row['flags']=str(e)[:50]\n"
assert _src.count(_c) == 1
_src = _src.replace(_c, """            def _fg(o_,k_):
                try: return o_.get_editor_property(k_)
                except Exception: return None
            _f1=_fg(pw,'GR_Steady'); _f2=_fg(ai,'Idle'); _f3=_fg(ai,'StillTime')
            row['flags']=(None if _f1 is None else bool(_f1), None if _f2 is None else bool(_f2), None if _f3 is None else round(float(_f3),2))
            row['yreq']=round(st.get('yreq',0.0),2)
            try:
                def _tr(p_,d_):
                    h_=u.SystemLibrary.line_trace_single(w_,u.Vector(p_.x,p_.y,p_.z+80),u.Vector(p_.x,p_.y,p_.z-d_),u.TraceTypeQuery.TRACE_TYPE_QUERY1,False,[pw],u.DrawDebugTrace.NONE,True)
                    if not h_: return None
                    t_=h_.to_tuple()
                    if not t_[0]: return None
                    return [round(t_[5].z,1),round(t_[7].z,3),(t_[9].get_name() if t_[9] else None),(t_[10].get_name() if t_[10] else None)]
                _gf=[]
                for _bn in ('ball_l','ball_r','foot_l','foot_r'):
                    r_=_tr(vis.get_socket_location(_bn),250); _gf.append(r_[:2] if r_ else None)
                _cc=[c_ for c_ in pw.get_components_by_class(u.CapsuleComponent)][0]; _hh=_cc.get_scaled_capsule_half_height()
                _gc=_tr(pw.get_actor_location(),_hh+250)
                row['gnd']=dict(f=_gf,cap=[round(_hh,1)]+(_gc or [None,None,None,None]),mz=[round(vis.get_world_location().z,1),round(src.get_world_location().z,1)])
            except Exception as e_: row['gnd']='ERR '+str(e_)[:80]
            try:
                _m=[c_ for c_ in pw.get_components_by_class(u.ActorComponent) if c_.get_name()=='SphMotion'][0]
                row['slope']=[round(float(_m.get_editor_property(k_)),3) if not isinstance(_m.get_editor_property(k_),bool) else _m.get_editor_property(k_) for k_ in ('SlopeDeg','SlopeLean','EffLean','SpeedScale','TurnSev','TurnW','SlopeOn')]
            except Exception as e_: row['slope']=None
""")

# 4 GOTOJ plan step: as GOTO (vidc_goto) but jogging (W + LeftShift held)
_g1 = "setkeys(['W'] if plan[st['seg']][0]=='GOTO' else plan[st['seg']][0].split())"
if _src.count(_g1) == 1:
    _src = _src.replace(_g1, "setkeys(['W'] if plan[st['seg']][0]=='GOTO' else (['W','LeftShift'] if plan[st['seg']][0]=='GOTOJ' else plan[st['seg']][0].split()))")
    _src = _src.replace("            if seg[0]=='GOTO':\n", "            if seg[0] in ('GOTO','GOTOJ'):\n")

# 5 reset the DayHub actor cache at every recording start (the PIE world path is the same in every session, so the cached hub was a dead object)
import builtins as _b18; _b18._VHUBW = None

# 6 (2026-11-19) shoulder/arm layer data: row['sh'] = dict(d=driver (UEFN source mesh) world xyz of clavicle/upperarm/lowerarm/hand L/R,
#   spine_05, neck_01, pelvis; v=visible body hand_l/r + lowerarm already in ub/ub2; a=body ABP posture weights (None if absent);
#   g=driver ABP gait/state strings)
_s6 = "            try:\n                _m=[c_ for c_ in pw.get_components_by_class(u.ActorComponent) if c_.get_name()=='SphMotion'][0]\n"
assert _src.count(_s6) == 1
_src = _src.replace(_s6, """            try:
                _sd={}
                for _bn in ('clavicle_l','clavicle_r','upperarm_l','upperarm_r','lowerarm_l','lowerarm_r','hand_l','hand_r','spine_05','neck_01','pelvis','head','neck_02','spine_03'):
                    _p=src.get_socket_location(_bn); _sd[_bn]=[round(_p.x,2),round(_p.y,2),round(_p.z,2)]
                _va={}
                _bai=vis.get_anim_instance()
                for _k in ('RunA','AccA','EffA','ArmW','HeadA','Fat','MoveA','RelA','AirA'):
                    try: _vv=_bai.get_editor_property(_k); _va[_k]=round(float(_vv),3)
                    except Exception: pass
                try: _va['mFat']=round(float([c_ for c_ in pw.get_components_by_class(u.ActorComponent) if c_.get_name()=='SphMotion'][0].get_editor_property('Fat')),3)
                except Exception: pass
                row['sh']=dict(d=_sd,a=_va)
            except Exception as e_: row['sh']='ERR '+str(e_)[:80]
""" + _s6)

# 7 (2026-11-19) GOTO toward a live actor: ('GOTO', max_s, 0, pitch, 'BP_GR_SplitPiece') walks to the nearest actor whose class name
#   contains that text at this moment (re-resolved every frame); if none exists the step ends at once (e.g. the piece was picked up).
def _vtarget(spec_, pw_, w_):
    if not isinstance(spec_, str): return spec_
    best_ = None
    for a_ in u.GameplayStatics.get_all_actors_of_class(w_, u.Actor):
        if spec_ in a_.get_class().get_name() and not bool(a_.get_editor_property('hidden')) and a_.get_attach_parent_actor() is None:
            l_ = a_.get_actor_location(); p_ = pw_.get_actor_location(); d_ = ((l_.x - p_.x) ** 2 + (l_.y - p_.y) ** 2) ** 0.5
            try: sett_ = bool(a_.get_editor_property('GR_Settled'))
            except Exception: sett_ = True
            key_ = (0 if sett_ else 1, d_)
            if best_ is None or key_ < best_[0]: best_ = (key_, (l_.x, l_.y, l_.z))
    return best_[1] if best_ else None
_b18._VTARGET = _vtarget
_g7 = "                p_=pw.get_actor_location(); dx_=seg[4][0]-p_.x; dy2_=seg[4][1]-p_.y\n"
if _src.count(_g7) == 1:
    _src = _src.replace(_g7, "                p_=pw.get_actor_location(); tg_=__import__('builtins')._VTARGET(seg[4],pw,w_)\n"
                             "                if tg_ is None: tg_=(p_.x,p_.y,p_.z)\n"
                             "                dx_=tg_[0]-p_.x; dy2_=tg_[1]-p_.y\n")
else: print('VIDM7_ANCHOR_MISSING')
# 8 (2026-11-19 evening) TIME BASE. Before: row['t'] = frame/FPS and the dilation was clamped to <= 1.0. In data-only mode
#   (no screenshots) the editor runs ~60 fps, so a "30 Hz" run could not slow to 1/30 per frame: the game advanced 1/60 per
#   frame while t claimed 1/30 (Z_SP_30: t 30.7 s, sum of game deltas 16.9 s). Now:
#   - dilation may go up to VID_DILMAX (default 4) so the game step really reaches 1/FPS when the editor is faster;
#   - row['t'] = simulated game time (sum of world deltas since the first row), row['tf'] = frame/FPS (old label),
#     row['tw'] = wall clock since the first row, row['dil'] = global time dilation in effect, row['tstep'] = target step;
#   - VID_VARDT=(lo_hz,hi_hz): each frame targets a random step between 1/hi and 1/lo (seeded, variable frame time test);
#     plan segments then advance on simulated time and the plan yaw rate is applied per target step.
_k8a = "st['rdt']=0.7*st['rdt']+0.3*rdt; dil=(1.0/FPS)/st['rdt']"
assert _src.count(_k8a) == 1
_src = _src.replace(_k8a, """st['rdt']=0.7*st['rdt']+0.3*rdt
            _vd=getattr(builtins,'VID_VARDT',None)
            if _vd:
                import random as _rnd
                if 'rng' not in st: st['rng']=_rnd.Random(1234)
                st['tstep_prev']=st.get('tstep',1.0/FPS); st['tstep']=1.0/st['rng'].uniform(_vd[0],_vd[1])
            else: st['tstep']=1.0/FPS
            dil=st['tstep']/rdt if _vd else st['tstep']/st['rdt']""")
_k8b = "if st['f']>3 and gdt>0: dil*=max(0.5,min(2.0,(1.0/FPS)/(0.5*gdt+0.5*st.get('gprev',gdt))))"
assert _src.count(_k8b) == 1
_src = _src.replace(_k8b, "if st['f']>3 and gdt>0 and not _vd: dil*=max(0.5,min(2.0,(1.0/FPS)/(0.5*gdt+0.5*st.get('gprev',gdt))))")
_k8c = "u.GameplayStatics.set_global_time_dilation(w_,max(0.005,min(1.0,dil)))"
assert _src.count(_k8c) == 1
_src = _src.replace(_k8c, "u.GameplayStatics.set_global_time_dilation(w_,max(0.005,min(float(getattr(builtins,'VID_DILMAX',4.0)),dil)))")
_k8d = "            now=st['f']/FPS\n"
assert _src.count(_k8d) == 1
_src = _src.replace(_k8d, """            now=st['f']/FPS
            if st['f']==0: st['tg']=0.0; st['tw0']=tn; st['segtg']=0.0
            else: st['tg']=st.get('tg',0.0)+gdt
""")
_k8e = "(st['f']-st['segf'])>=max(1,int(round(plan[st['seg']][1]*FPS)))"
assert _src.count(_k8e) == 1
_src = _src.replace(_k8e, "((st['tg']-st['segtg'])>=plan[st['seg']][1]-0.5*st.get('tstep',1.0/FPS) if (getattr(builtins,'VID_VARDT',None) or getattr(builtins,'VID_NODIL',False)) else (st['f']-st['segf'])>=max(1,int(round(plan[st['seg']][1]*FPS))))")
_k8f = "                st['seg']+=1; st['segf']=st['f']\n"
assert _src.count(_k8f) == 1
_src = _src.replace(_k8f, "                st['seg']+=1; st['segf']=st['f']; st['segtg']=st['tg']\n")
_k8g = "                _dy=yr*seg[1]/max(1,int(round(seg[1]*FPS))); st['yaw']+=_dy"
assert _src.count(_k8g) == 1
_src = _src.replace(_k8g, "                _dy=(yr*st.get('tstep',1.0/FPS) if (getattr(builtins,'VID_VARDT',None) or getattr(builtins,'VID_NODIL',False)) else yr*seg[1]/max(1,int(round(seg[1]*FPS)))); st['yaw']+=_dy")
_k8h = "            row=dict(f=st['f'],t=round(now,3),"
assert _src.count(_k8h) == 1
_src = _src.replace(_k8h, "            row=dict(f=st['f'],t=round(st['tg'],4),tf=round(now,3),tw=round(tn-st['tw0'],4),dil=round(float(u.GameplayStatics.get_global_time_dilation(w_)),4),tstep=round(st.get('tstep',1.0/FPS),4),")
# 9 (2026-11-19 evening) per-frame experiment hook: builtins.VID_TICKHOOK(pw, ai, st, w_) runs every recorded frame before the
#   row is built (in-memory runtime experiments only; returns an optional dict stored as row['hook']).
_k9 = "            l=pw.get_actor_location(); v=pw.get_velocity(); r=pw.get_actor_rotation();"
assert _src.count(_k9) == 1
_src = _src.replace(_k9, """            _hk=getattr(builtins,'VID_TICKHOOK',None); _hko=None
            if _hk:
                try: _hko=_hk(pw,ai,st,w_)
                except Exception as e_: _hko={'err':repr(e_)[:100]}
            l=pw.get_actor_location(); v=pw.get_velocity(); r=pw.get_actor_rotation();""")
_k9b = "            try: row['mm']=(str(ai.get_editor_property('MM_Asset'))"
assert _src.count(_k9b) == 1
_src = _src.replace(_k9b, "            if _hko is not None: row['hook']=_hko\n"+_k9b)
# 10 (2026-11-19 evening) ONE RECORDER AT A TIME. finish() unregistered builtins._vr, i.e. the most recently registered callback,
#   not its own: a recording whose PIE was stopped early stayed registered (tick returns while no pawn) and came back in the next
#   PIE with its old plan (keys, time dilation) - two recorders fought and the newest was then killed by the zombie's finish().
#   Now each recording unregisters its own handle, and a new recording first unregisters and closes every earlier one.
_k10a = "        try: u.unregister_slate_post_tick_callback(builtins._vr)"
assert _src.count(_k10a) == 1
_src = _src.replace(_k10a, "        try: u.unregister_slate_post_tick_callback(st['h'])")
_k10b = "    builtins._vr=u.register_slate_post_tick_callback(tick);"
assert _src.count(_k10b) == 1
_src = _src.replace(_k10b, """    for _o in list(getattr(builtins,'_vr_all',[])):
        try: _o[1]['done']=True; u.unregister_slate_post_tick_callback(_o[0])
        except Exception: pass
    builtins._vr_all=[]
    st['h']=builtins._vr=u.register_slate_post_tick_callback(tick); builtins._vr_all.append((st['h'],st));""")
