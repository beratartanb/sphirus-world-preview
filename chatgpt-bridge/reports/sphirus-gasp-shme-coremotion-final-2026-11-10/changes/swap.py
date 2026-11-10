# swap.py (exec'd in a PIE job after h.py): replace the player pawn with another pawn class at the same spot.
# Spawn through the running GameMode's SpawnDefaultPawnAtTransform (DefaultPawnClass set to the new class), then possess.
def swap(cls_path):
    global PW
    C=u.load_object(None,cls_path); assert C,cls_path; old=PW; l=old.get_actor_location(); r=old.get_actor_rotation(); cr=PC.get_control_rotation()
    gm=u.GameplayStatics.get_game_mode(W); gm.set_editor_property('default_pawn_class',C)
    t=u.Transform(location=u.Vector(l.x,l.y,l.z+300),rotation=r,scale=u.Vector(1,1,1))
    old.set_actor_enable_collision(False); old.set_actor_location(u.Vector(l.x,l.y,l.z-5000),False,True)
    n=gm.spawn_default_pawn_at_transform(PC,t); print('SPAWNED',n.get_class().get_name() if n else None)
    assert n and n.get_class()==C,(n,C)
    PC.possess(n); n.set_actor_location(l,False,True); PC.set_control_rotation(cr); old.destroy_actor(); PW=n
    print('SWAP',PC.get_controlled_pawn().get_class().get_name(),[round(x) for x in (l.x,l.y,l.z)])
