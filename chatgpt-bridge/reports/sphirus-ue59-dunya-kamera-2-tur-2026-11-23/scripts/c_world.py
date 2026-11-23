# c_world.py (control, in-memory only, nothing saved): apply candidate values to level actors of the editor world.
# builtins.R2G_W = { '<actor label>': { 'rot': (pitch,yaw,roll) | 'loc': (x,y,z) | 'scale': (x,y,z) | 'hidden': bool | '<component prop>': value | 'pp:<settings prop>': value } }
# Light / fog / sky components are found automatically; PostProcessVolume settings use the 'pp:' prefix. Prints old -> new. Dirties the open map.
import unreal as u, builtins
V=getattr(builtins,'R2G_W',None) or {}
acts={a.get_actor_label():a for a in u.get_editor_subsystem(u.EditorActorSubsystem).get_all_level_actors()}
def comp(a):
    for cls in (u.LightComponent,u.SkyLightComponent,u.ExponentialHeightFogComponent,u.LocalFogVolumeComponent,u.SkyAtmosphereComponent,u.StaticMeshComponent):
        c=a.get_component_by_class(cls)
        if c: return c
for lb,d in V.items():
    a=acts.get(lb)
    if not a: print('W_MISSING',lb); continue
    for k,v in d.items():
        try:
            if k=='rot': old=a.get_actor_rotation(); a.set_actor_rotation(u.Rotator(pitch=v[0],yaw=v[1],roll=v[2]),False); print('W',lb,k,(round(old.pitch,1),round(old.yaw,1)),'->',v)
            elif k=='loc': old=a.get_actor_location(); a.set_actor_location(u.Vector(*v),False,False); print('W',lb,k,(old.x,old.y,old.z),'->',v)
            elif k=='scale': old=a.get_actor_scale3d(); a.set_actor_scale3d(u.Vector(*v)); print('W',lb,k,(old.x,old.y,old.z),'->',v)
            elif k=='hidden': a.set_is_temporarily_hidden_in_editor(bool(v)); a.set_actor_hidden_in_game(bool(v)); print('W',lb,k,'->',v)
            elif k.startswith('pp:'):
                s=a.settings; kk=k[3:]; old=s.get_editor_property(kk)
                ov='override_'+kk
                try: s.set_editor_property(ov,True)
                except Exception: pass
                s.set_editor_property(kk,v); a.set_editor_property('settings',s); print('W',lb,k,old,'->',a.settings.get_editor_property(kk))
            else:
                c=comp(a); old=c.get_editor_property(k)
                if isinstance(old,u.LinearColor) and isinstance(v,(tuple,list)): v=u.LinearColor(*v)
                if isinstance(old,u.Color) and isinstance(v,(tuple,list)): v=u.Color(r=v[0],g=v[1],b=v[2],a=255)
                c.set_editor_property(k,v); print('W',lb,k,old,'->',c.get_editor_property(k))
        except Exception as e: print('W_ERR',lb,k,repr(e)[:200])
