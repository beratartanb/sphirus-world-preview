# trajprobe.py (PIE, via J after gx.py): generates the motion-matching trajectory with the same engine function the pose
# history node uses (PoseSearchTrajectoryLibrary.pose_search_generate_trajectory) every frame while W is held, and
# writes the final trajectory samples (time offset, position relative to the actor, facing) to rec/trajprobe.json.
import json,builtins
RD=u.Paths.project_dir()+'Saved/Codex/Grip_20261106/rec/'
def _w(): return u.get_editor_subsystem(u.UnrealEditorSubsystem).get_game_world()
def _c(c):
    w_=_w(); u.SystemLibrary.execute_console_command(w_,c,u.GameplayStatics.get_player_controller(w_,0))
st=dict(f=0,traj=u.TransformTrajectory(),yaw=0.0,out=[],done=False)
td=u.PoseSearchTrajectoryData()   # defaults (RotateTowardsMovementSpeed 10, MaxControllerYawRate 70) - not editable on instances
def dump(tag,traj,pw):
    try:
        samples=traj.get_editor_property('samples'); base=pw.get_actor_transform(); rows=[]
        for s in samples:
            t=float(s.get_editor_property('time_in_seconds')); pos=s.get_editor_property('position'); loc=base.inverse_transform_location(pos)
            rows.append((round(t,2),round(loc.x,1),round(loc.y,1)))
        st['out'].append((tag,st['f'],rows))
    except Exception as e: st['out'].append((tag,st['f'],'ERR '+str(e)[:160]))
def tick(dt):
    try:
        if st['done']: return
        w_=_w(); pc=u.GameplayStatics.get_player_controller(w_,0) if w_ else None
        if pc is None or pc.get_controlled_pawn() is None: return
        pw=pc.get_controlled_pawn(); ai=pw.mesh.get_anim_instance()
        if st['f']==0: _c('Input.+key W true')
        r=u.PoseSearchTrajectoryLibrary.pose_search_generate_trajectory(ai,td,u.GameplayStatics.get_world_delta_seconds(w_),st['traj'],st['yaw'],0.04,26,0.25,6)
        try: st['traj']=r[0]; st['yaw']=float(r[1]); out_traj=r[2]
        except Exception: out_traj=r
        if st['f'] in (5,30,60,89): dump('F%d'%st['f'],out_traj,pw); v=pw.get_velocity(); st['out'].append(('VEL',st['f'],(round(v.x),round(v.y)),round(pw.get_actor_rotation().yaw),round(pw.mesh.get_world_rotation().yaw)))
        st['f']+=1
        if st['f']>=90:
            st['done']=True; _c('Input.-key W')
            try: u.unregister_slate_post_tick_callback(builtins._tp)
            except Exception: pass
            open(RD+'trajprobe.json','w').write(json.dumps(st['out'])); print('TRAJPROBE_DONE')
    except Exception as e:
        st['out'].append(('TICK_ERR',st['f'],str(e)[:200])); st['done']=True
        try: u.unregister_slate_post_tick_callback(builtins._tp)
        except Exception: pass
        open(RD+'trajprobe.json','w').write(json.dumps(st['out'])); print('TRAJPROBE_ERR',str(e)[:200])
builtins._tp=u.register_slate_post_tick_callback(tick); print('TRAJPROBE_START')
