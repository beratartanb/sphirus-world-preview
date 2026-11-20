import builtins, unreal as u
def _hk(pw, ai, st, w_):
    o={}
    try:
        pc=pw.get_controller(); cm=pw.get_movement_component(); li=pw.get_last_movement_input_vector()
        o=dict(pawn=pw.get_class().get_name(), pc=pc.get_class().get_name() if pc else None, mode=str(cm.get_editor_property('movement_mode')), ign=bool(pc.is_move_input_ignored()) if pc else None,
               inp=[round(li.x,2),round(li.y,2)], maxsp=round(cm.get_max_speed(),1), mws=round(cm.get_editor_property('max_walk_speed'),1), ai=ai.get_class().get_name() if ai else None,
               tdil=round(pw.get_editor_property('custom_time_dilation'),2), acc=round(cm.get_editor_property('max_acceleration'),1), tick=bool(pw.is_actor_tick_enabled()), paused=bool(u.GameplayStatics.is_game_paused(w_)))
    except Exception as e: o={'err':repr(e)[:150]}
    return o
builtins.VID_TICKHOOK=_hk
