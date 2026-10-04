"""GD11 refinement E: head-pitch test clip for the hair (copy of an AAMS stand idle in GD11_HeadRefinementE/Anim; the source clip is untouched).
neck_01 / neck_02 / head get an extra rotation about their local Z (the nod axis of this skeleton) following a pitch curve:
0 -> 0.6 s to +P_UP, hold, 1.4 -> 2.2 s to -P_DN, hold, 3.0 -> 3.8 s back to 0 (shares 0.35 / 0.30 / 0.35)."""
import unreal as u, json, math
SRC = '/Game/CoreMotion_Retargeted/AAMS/Idle/am_Stand_Idle_03_LookAround'; DST = '/Game/Sphirus/CharacterLab/GD11_HeadRefinementE_20261004/Anim/AS_G11RE_HeadPitch'
EAL = u.EditorAssetLibrary; out = {}
a = EAL.load_asset(DST) if EAL.does_asset_exist(DST) else EAL.duplicate_asset(SRC, DST)
n = u.AnimationLibrary.get_num_frames(a); L = a.get_play_length(); fps = n/L; out['frames'] = n; out['len'] = L
P_UP, P_DN = 26.0, -30.0
def sst(t): t = max(0.0, min(1.0, t)); return t*t*(3-2*t)
def pitch(t): return P_UP*sst(t/0.6)*(1-sst((t-1.4)/0.8))+P_DN*sst((t-1.4)/0.8)*(1-sst((t-3.0)/0.8))
ctrl = a.get_editor_property('controller') if hasattr(a, 'get_editor_property') else None
try: ctrl = a.controller
except Exception: pass
out['ctrl'] = str(type(ctrl))
SH = {'neck_01': 0.35, 'neck_02': 0.30, 'head': 0.35}
ctrl.open_bracket(u.Text('head pitch'))
for b, sh in SH.items():
    pos, rot, scl = [], [], []
    for f in range(n+1):
        t = min(f/fps, L); tr = u.AnimationLibrary.get_bone_pose_for_frame(a, b, min(f, n-1), False)
        dq = u.Quat(); dq.set_from_euler(u.Vector(0.0, 0.0, pitch(t)*sh)) if hasattr(dq, 'set_from_euler') else None
        q = tr.rotation*u.Rotator(0.0, 0.0, pitch(t)*sh).quaternion() if False else u.MathLibrary.compose_rotators(u.Rotator(0.0, 0.0, pitch(t)*sh), tr.rotation.rotator()).quaternion()
        pos.append(tr.translation); rot.append(q); scl.append(tr.scale3d)
    ok = ctrl.set_bone_track_keys(b, pos, rot, scl); out[b] = ok
ctrl.close_bracket()
out['saved'] = EAL.save_loaded_asset(a, False)
out['pitch_samples'] = [round(pitch(t), 1) for t in (0, 0.6, 1.4, 1.8, 2.2, 3.0, 3.8)]
print('PITCH_ANIM', json.dumps(out))
