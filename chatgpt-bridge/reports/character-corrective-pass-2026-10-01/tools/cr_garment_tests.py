"""CORRECTIVE pass garment behaviour capture request: static poses with a cloth settling window + animation-in-flight clips.
usage: python cr_garment_tests.py <prefix> [set: shorts|henley|both] -> captures/capture_request.json"""
import json, sys, pathlib
R = pathlib.Path(__file__).resolve().parents[2]; O = R/'Saved/Codex/CharacterLookdev_20260930/captures'; P = sys.argv[1]; SET = sys.argv[2] if len(sys.argv) > 2 else 'both'
PL = '/Game/Sphirus/CharacterLab/CharacterRevision_20260930/Anim/AN_RV_PoseLib2'; ROM = '/MetaHumanCharacter/Optional/Animation/TemplateAnimations/Technical_Loops/BodyROM/mhc_body_rom_body'
WALK = '/MetaHumanCharacter/Optional/Animation/UEFNAnimPreset/Locomotion/AS_MH_Neutral_Walk_Loop_F'; M = '/Game/Sphirus/CharacterLab/NativeBody_20260928/Diagnostics/Motion/'
STOP = '/MetaHumanCharacter/Optional/Animation/UEFNAnimPreset/Locomotion/AS_MH_Neutral_Run_Stop_F_Lfoot'; TURN = '/Game/CoreMotion_Retargeted/AAMS/Idle/af_Stand_Idle_TurnL090_NoRM'
STATIC = {'neutral': (None, 0), 'stride': (PL, 0.3), 'highknee_l': (PL, 0.26667), 'bend45': (PL, 0.1), 'twist_l': (PL, 0.2)}
DYN = {'walk': (WALK, 0.15, 0.85), 'jog': (M+'QA_jog', 0.0, 0.45), 'sprint': (M+'QA_sprint', 0.0, 0.5), 'crouch': (M+'QA_crouch', 0.2, 1.0),
       'squat': (ROM, 18.5, 20.0), 'hipflex': (ROM, 13.5, 15.0), 'stop': (STOP, 0.0, 0.6), 'turn': (TURN, 0.0, 0.6)}
CAMS = {'shorts': {'front': ([0, 150, 88, -90, 0], 22), '3q': ([-106, 106, 88, -45, 0], 22), 'side': ([150, 3, 88, 180, 0], 22), 'rear3q': ([106, -106, 88, 135, 0], 22)},
        'henley': {'front': ([0, 170, 108, -90, 0], 24), '3q': ([-120, 120, 108, -45, 0], 24), 'side': ([170, 3, 108, 180, 0], 24), 'rear3q': ([120, -120, 108, 135, 0], 24)}}
cams = CAMS['shorts'] if SET == 'shorts' else CAMS['henley']
S = []
if SET == 'neck':   # neckline / placket progression at 0/20/30/45/60/90 deg forward bend (PoseLib2 frames, 30 fps)
    for k, t in (('b00', 0.0), ('b20', 1/30), ('b30', 2/30), ('b45', 3/30), ('b60', 4/30), ('b90', 5/30)):
        for v, c in (('front', [0, 120, 142, -90, -12]), ('3q', [-85, 85, 142, -45, -12])): S.append(dict(name=f'{P}_nk_{k}_{v}', view='custom', cam=c, fov=22, garments=True, materials='real', light='studio', animation=PL, time=t, light_target_z=125, min_seconds=2.0, min_frames=60, cam_follow=False))
if SET == 'waist':  # hem / waistband interaction close-ups
    WC = {'3q': [-80, 80, 101, -45, 0], 'side': [113, 3, 101, 180, 0], 'rear3q': [80, -80, 101, 135, 0], 'lside': [-113, 3, 101, 0, 0]}
    for k, (a, t) in (('neutral', (None, 0)), ('bend45', (PL, 0.1)), ('twist_l', (PL, 0.2)), ('stride', (PL, 0.3))):
        for v, c in WC.items(): S.append(dict(name=f'{P}_wb_{k}_{v}', view='custom', cam=c, fov=18, garments=True, materials='real', light='studio', animation=a, time=t, light_target_z=95, min_seconds=3.0, min_frames=120))
    for k in ('walk', 'crouch', 'turn'):
        a, t0, t1 = DYN[k]
        for v, c in WC.items(): S.append(dict(name=f'{P}_wb_{k}_{v}', view='custom', cam=c, fov=18, garments=True, materials='real', light='studio', animation=a, play=t0, time=t1, light_target_z=95, cam_follow=True))
if SET == 'full':   # full character, studio + gameplay light
    FC = {'front': [0, 330, 92, -90, 0], '3q': [-235, 235, 92, -45, 0], 'side': [330, 3, 92, 180, 0], 'back': [0, -330, 92, 90, 0]}
    for li in ('studio', 'gameplay'):
        for v, c in FC.items(): S.append(dict(name=f'{P}_fl_{li}_{v}', view='custom', cam=c, fov=34, garments=True, materials='real', light=li, animation=None, time=0, light_target_z=95, min_seconds=3.0, min_frames=120))
    for k in ('walk', 'jog'):
        a, t0, t1 = DYN[k]
        for v in ('3q', 'side'): S.append(dict(name=f'{P}_fl_{k}_{v}', view='custom', cam=FC[v], fov=34, garments=True, materials='real', light='studio', animation=a, play=t0, time=t1, light_target_z=95, cam_follow=True))
if SET == 'seam':   # head / body seam, garments hidden, 4 lights (same cams as the identity pass skH / skN)
    for li in ('studio', 'grazing', 'interior', 'gameplay'):
        for v, c in (('3q', [-70, 76, 151, -47, 0]), ('front', [0, 105, 151, -90, 0])): S.append(dict(name=f'{P}_{li}_{v}', view='custom', cam=c, fov=22, garments=False, materials='real', light=li, animation=None, time=0, light_target_z=150))
if SET == 'seamclay':
    for li in ('studio', 'grazing'):
        for v, c in (('3q', [-70, 76, 151, -47, 0]), ('front', [0, 105, 151, -90, 0])): S.append(dict(name=f'{P}_{li}_{v}', view='custom', cam=c, fov=22, garments=False, materials='clay', hair=False, light=li, animation=None, time=0, light_target_z=150))
if SET == 'lod':
    for L in range(4): S.append(dict(name=f'{P}_lod{L}_front', view='custom', cam=[0, 125, 159, -90, 0], fov=15, garments=True, materials='real', light='studio', lod=L, animation=None, time=0, light_target_z=150))
    for L in range(3): S.append(dict(name=f'{P}_glod{L}_3q', view='custom', cam=[-235, 235, 92, -45, 0], fov=34, garments=True, materials='real', light='studio', lod=L, animation=None, time=0, light_target_z=95, min_seconds=2.0, min_frames=60))
if SET in ('neck', 'waist', 'full', 'seam', 'lod', 'seamclay'):
    json.dump({'label': f'{P}_gt', 'cases': S}, open(O/'capture_request.json', 'w'), indent=1); print('cases', len(S)); raise SystemExit
for k, (a, t) in STATIC.items():
    for v, (c, f) in cams.items(): S.append(dict(name=f'{P}_st_{k}_{v}', view='custom', cam=c, fov=f, garments=True, materials='real', light='studio', animation=a, time=t, light_target_z=95, min_seconds=3.0, min_frames=120))
for k, (a, t0, t1) in DYN.items():
    for v, (c, f) in cams.items(): S.append(dict(name=f'{P}_dy_{k}_{v}', view='custom', cam=c, fov=f, garments=True, materials='real', light='studio', animation=a, play=t0, time=t1, light_target_z=95, cam_follow=True))
json.dump({'label': f'{P}_gt', 'cases': S}, open(O/'capture_request.json', 'w'), indent=1); print('cases', len(S))
