"""Hair motion evidence: real-time segments in the QA editor world (anim playing at rate 1, actor translated / turned), groom
simulation on the loose groom. A head-tracking rear-3/4 scene capture is sampled every SAMPLE s (exported 2 ticks later).
Segments: walk, jog, sprint -> sudden stop (pose frozen, capture the settle), head/body yaw swing, forward bend 0->90->0 (pose-lib
scrub), twist l/r (scrub), jump, crouch. Output: captures/hm_<seg>_<k>.png + hm_results.json (sim flags, timings)."""
import unreal, pathlib, json, time, math, builtins, traceback
R = pathlib.Path(unreal.Paths.project_dir()).resolve(); E = R/'Saved/Codex/CharacterRevision_20260930/captures'; Q = builtins.SPH_RV_QA
b = Q['components']['Body']; h = Q['components']['Head']; actor = b.get_owner(); cap = Q['capture']; cc = Q['cc']
PL = json.loads((E.parent/'rv_poselib.json').read_text()); PLA = PL['asset'].split('.')[0]; T = PL['times']
LOC = '/MetaHumanCharacter/Optional/Animation/UEFNAnimPreset/Locomotion/'; MO = '/Game/Sphirus/CharacterLab/NativeBody_20260928/Diagnostics/Motion/'
SEG = [dict(n='hold', anim=LOC+'AS_MH_Neutral_Stand_Idle_Loop', speed=0, dur=2.0, freeze=True), dict(n='walk', anim=LOC+'AS_MH_Neutral_Walk_Loop_F', speed=0, dur=2.4), dict(n='jog', anim=MO+'QA_jog', speed=0, dur=2.0),
       dict(n='sprint', anim=MO+'QA_sprint', speed=0, dur=2.4), dict(n='stop', anim=None, speed=0, dur=1.8, freeze=True),
       dict(n='yaw', anim=LOC+'AS_MH_Neutral_Stand_Idle_Loop', speed=0, dur=2.4, yaw=45), dict(n='bend', scrub=[T['neutral'], T['bend90'], T['neutral']], dur=3.0),
       dict(n='twist', scrub=[T['neutral'], T['twist_l'], T['neutral'], T['twist_r'], T['neutral']], dur=2.4, pl=True), dict(n='jump', anim=MO+'QA_jump', speed=0, dur=1.6),
       dict(n='crouch', anim=MO+'QA_crouch', speed=0, dur=1.6)]
SAMPLE = 0.2
for part, c in Q['components'].items():
    m = c.skeletal_mesh_asset
    for i in range(c.get_num_materials()): c.set_material(i, m.get_editor_property('materials')[i].get_editor_property('material_interface'))
    c.set_forced_lod(1); c.set_visibility(True, False)
for g, c in Q['garments'].items():
    c.set_visibility(True, False); c.set_forced_lod(1); m = c.skeletal_mesh_asset
    for i in range(c.get_num_materials()): c.set_material(i, m.get_editor_property('materials')[i].get_editor_property('material_interface'))
for g, gc in Q['grooms'].items(): gc.set_visibility(True, False)
cc.set_editor_property('fov_angle', 30.0)
LIGHTS = [(lc.get_owner(), lc.get_owner().get_actor_location()) for lc, _ in Q['lights'].values()]+[(Q['sky'].get_owner(), Q['sky'].get_owner().get_actor_location())]
def lights_follow(dy):
    for a_, l0 in LIGHTS: a_.set_actor_location(unreal.Vector(l0.x, l0.y+dy, l0.z), False, False)
info = {'loose_sim_flags': [p.get_editor_property('solver_settings').get_editor_property('enable_simulation') for p in Q['grooms']['HairLoose'].groom_asset.get_editor_property('hair_groups_physics')],
        'main_sim_flags': [p.get_editor_property('solver_settings').get_editor_property('enable_simulation') for p in Q['grooms']['HairMain'].groom_asset.get_editor_property('hair_groups_physics')], 'segments': [], 'frames': []}
st = {'s': -1, 't0': 0.0, 'y': 0.0, 'last': 0.0, 'pend': [], 'k': 0, 'ticks': 0, 'prev_t': time.time()}
def start(i):
    s = SEG[i]; st.update(s=i, t0=time.time(), last=-1.0, k=0)
    if s.get('freeze'):
        if s.get('anim'): b.play_animation(unreal.load_asset(s['anim']), False); b.set_position(0.0, False)
        b.set_play_rate(0.0); return
    if s.get('scrub'): b.play_animation(unreal.load_asset(PLA), False); b.set_play_rate(0.0); b.set_position(s['scrub'][0], False); return
    b.play_animation(unreal.load_asset(s['anim']), True); b.set_play_rate(1.0)
    if s['n'] in ('walk', 'jog', 'sprint') and i == 0: st['y'] = 0.0
def cam_follow():
    hp = h.get_socket_location('head'); yaw = actor.get_actor_rotation().yaw
    # rear 3/4 relative to the actor facing (+Y at yaw 0): offset rotated with the actor
    a = math.radians(yaw); ox, oy = 62.0, -60.0; x = ox*math.cos(a)-oy*math.sin(a); y = ox*math.sin(a)+oy*math.cos(a)
    cap.set_actor_location(unreal.Vector(hp.x+x, hp.y+y, hp.z+9), False, False)
    cap.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(cap.get_actor_location(), unreal.Vector(hp.x-3*math.sin(a), hp.y-3*math.cos(a), hp.z+5)), False)
def tick(dt):
    try:
        now = time.time(); rdt = now-st['prev_t']; st['prev_t'] = now; st['ticks'] += 1
        # pending exports (2 ticks after the capture)
        keep = []
        for (img, n) in st['pend']:
            if st['ticks'] >= n: unreal.RenderingLibrary.export_render_target(Q['world'], Q['rt'], str(E), img)
            else: keep.append((img, n))
        st['pend'] = keep
        if keep: return   # do not issue a new capture before the previous one is exported
        if st['s'] < 0: start(0)
        s = SEG[st['s']]; t = now-st['t0']
        if t > s['dur']:
            info['segments'].append({'n': s['n'], 'dur': s['dur'], 'frames': st['k']})
            if st['s']+1 == len(SEG):
                unreal.unregister_slate_post_tick_callback(handle); lights_follow(0.0); actor.set_actor_location(unreal.Vector(0, 0, 0), False, False); actor.set_actor_rotation(unreal.Rotator(0, 0, 0), False)
                (E/'hm_results.json').write_text(json.dumps(info, indent=1)); return
            start(st['s']+1); s = SEG[st['s']]; t = 0.0
        if s.get('speed'): st['y'] += s['speed']*min(rdt, 0.1); actor.set_actor_location(unreal.Vector(0, st['y'], 0), False, False); lights_follow(st['y'])
        if s.get('yaw'): actor.set_actor_rotation(unreal.Rotator(yaw=s['yaw']*math.sin(2*math.pi*t/1.2), pitch=0, roll=0), False)
        elif s['n'] == 'bend': actor.set_actor_rotation(unreal.Rotator(0, 0, 0), False)
        if s.get('scrub'):
            ks = s['scrub']; u = min(t/s['dur'], 0.9999)*(len(ks)-1); j = int(u); f = u-j; f = f*f*(3-2*f); b.set_position(ks[j]+(ks[j+1]-ks[j])*f, False)
        cam_follow()
        if t-st['last'] >= SAMPLE:
            st['last'] = t; cc.capture_scene(); img = f"hm_{s['n']}_{st['k']:02d}.png"; st['pend'].append((img, st['ticks']+2)); st['k'] += 1
            info['frames'].append({'img': img, 'seg': s['n'], 't': round(t, 3), 'fps_est': round(1.0/max(rdt, 1e-3), 1)})
    except Exception:
        unreal.unregister_slate_post_tick_callback(handle); (E/'hm_error.txt').write_text(traceback.format_exc())
handle = unreal.register_slate_post_tick_callback(tick); print('HM_STARTED', info['loose_sim_flags'], info['main_sim_flags'])
