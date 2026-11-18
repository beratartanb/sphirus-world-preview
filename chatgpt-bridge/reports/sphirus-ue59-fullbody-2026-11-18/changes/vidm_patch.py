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
