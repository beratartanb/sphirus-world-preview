# fill_contracts.py : writes the reference-to-game case contracts for the Sphirus slice (schema of r2g 0.1.0, commit 6a00e49).
# Rerunnable. Observed / inferred / authored are labelled per entry. Does not touch references/.
import json, os, sys
C = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'Docs', 'ReferenceToGame', 'sphirus-slice-01')
def rd(n): return json.load(open(os.path.join(C, n), encoding='utf8'))
def wr(n, v): json.dump(v, open(os.path.join(C, n), 'w', encoding='utf8'), indent=2, ensure_ascii=False); open(os.path.join(C, n), 'a', encoding='utf8').write('\n')

# ---------------------------------------------------------------- case.json (authority per reference)
case = rd('case.json')
A = {
 'ref-001': dict(sphirus_id='R01', role='character direction sheet', authority=['style'],
   notes='Authority: hair mass (copper messy bob), relaxed standing posture, shoulder-arm relation, everyday clothing, fabric/leather/skin material approach. '
         'NOT authority: the face. The approved MetaHuman face (live asset SKM_MHC_Sph8_FaceMesh on BP_HybridA_Player) and the user edits stay; this sheet is not a new identity approval.'),
 'ref-002': dict(sphirus_id='R02', role='exterior world', authority=['style'],
   notes='Authority: sheltered world feeling, house-water-slope relation, depth layers, light, vegetation and material coherence. '
         'NOT authority: gameplay camera distance, metres / walking times / map size, roof or footprint of the existing house (no rebuild order).'),
 'ref-003': dict(sphirus_id='R03', role='house and workshop interior', authority=['style'],
   notes='Authority: lived-in feeling, care, interior/exterior material consistency, light, room for the player to move. NOT a floor plan; doors, floors and architecture of the existing house are not rebuilt from it.'),
 'ref-004': dict(sphirus_id='R04', role='main gameplay camera', authority=['style'],
   notes='Authority: size and position of the character in frame (close, behind the right shoulder, character on the left, travel space open), character and world read together. '
         'NOT authority: an exact FOV, arm length or follow spring constant.'),
 'ref-005': dict(sphirus_id='R05', role='natural movement poses', authority=['motion'],
   notes='Authority (limited): silhouette, trunk balance, head-neck-shoulder relation, visual intent of the movement. Still images: no timing, foot lock, acceleration, retarget or physics evidence. '
         'Generated-pose anatomy errors are not transferred (see analysis/observations.md).'),
 'ref-006': dict(sphirus_id='X01', role='supplementary: cottage service side (not one of the six named references)', authority=['historical'],
   notes='Supplied in the same message but outside the R01-R06 list. Lowest priority; read only as extra evidence for the R02 material/lived-in language (wood store, chopping block, tools). No layout authority.'),
 'ref-007': dict(sphirus_id='X02', role='supplementary: cottage front with porch above the water', authority=['historical'],
   notes='Outside the R01-R06 list. Extra evidence for the R02 house-water relation and porch use. Shows a different house shape than R02; neither is a rebuild order.'),
 'ref-008': dict(sphirus_id='X03', role='supplementary: open-plan interior', authority=['historical'],
   notes='Outside the R01-R06 list. Extra evidence for the R03 interior language. No floor-plan authority.'),
}
for r in case['references']:
    r.update(A[r['id']]); r['inspection'] = 'viewed in full by the agent (2026-11-23), metadata read with r2g inspect'
case['notes'] = [
 'R06 (resonance / hallucination state of the R04 place) was NOT supplied: eight images arrived, none shows an altered-perception state. No R06 decision is recorded as observed; the resonance section documents the existing project system only.',
 'Priority order: current explicit user instruction > approved identity and project assets > the per-reference authority above > agent proposals.',
 'Engine: the existing Unreal Engine 5.9 project (sphirus_UE59). r2g ships no Unreal generator; app/ holds only a hash manifest of the real Unreal source (see app/README.md).',
 'Reference ids are the tool ids (ref-00N); the brief ids R01-R05 / X01-X03 are in sphirus_id.']
wr('case.json', case)

# ---------------------------------------------------------------- style.json
pal = []
for f in ('palette-r02.json', 'palette-r01.json'):
    for s in json.load(open(os.path.join(C, 'analysis', f), encoding='utf8')):
        if 'backdrop' in s['role']: continue
        pal.append({'role': s['role'], 'hex': s['hex'], 'reference_id': s['reference_id'], 'origin': 'observed: r2g palette, median encoded RGB at uv %s (no ICC conversion)' % s['uv']})
style = {
 'status': 'draft',
 'anchors': [
  {'reference_id': 'ref-002', 'notes': 'R02 governs exterior mood: enclosed bowl of forest, dark calm water with a readable far bank, house above the water, one path to the shore and one up behind.'},
  {'reference_id': 'ref-003', 'notes': 'R03 governs interior mood: warm, worked-in, maintained; mask bench, hearth and kitchen read by function.'},
  {'reference_id': 'ref-004', 'notes': 'R04 governs gameplay framing: head-to-hip figure on the left third, travel space to the right.'},
  {'reference_id': 'ref-001', 'notes': 'R01 governs hair mass, relaxed posture and clothing materials; not the face.'},
  {'reference_id': 'ref-005', 'notes': 'R05 governs pose intent only.'}],
 'palette': pal,
 'identity': [
  'observed (R01): adult woman, copper messy bob to the jaw, long-sleeve henley with rolled sleeves, slate jeans, brown belt, worn ankle boots; arms hang close to the body, shoulders level and relaxed.',
  'observed (live project): BP_HybridA_Player uses groom /Game/Grooms/001_Messy_Bob (matches the R01 hair mass), body SKM_MHC_Sph8_BodyMesh, face SKM_MHC_Sph8_FaceMesh, garments SKM_Sph_RetroTop + SKM_Sph_Pants70 + belt. MHC_HazelM is not the mesh on the active pawn.',
  'authored: the fresh-start look (sleeveless top, shorts) is the at-home state; R01 clothing is the going-out look and belongs to the wardrobe stations (GR_Day_WardDoor, GR_Day_Set0-4), not to a forced default swap.',
  'not decided from references: face details (protected), any later costume stage (shoulder cape / late equipment stays out of the start).'],
 'materials': [
  'observed (R02/R03/X01): rough plaster with patched areas, dark weathered timber, mossy shingle roof, field stone, woven wool and linen, hammered copper, worn leather.',
  'observed (live project): plaster + dark timber veranda house, weathered boards, copper wheelbarrow, firewood; interior plaster walls, wood floor, leather sofa, stone hearth. Same family as the references; the references are rougher and more hand-built.',
  'authored: no rebuild of the house shell from R02/X01/X02/R03; material work stays on project-owned overrides.'],
 'lighting': 'observed (R02): soft, overcast-like forest light with no hard sun patches, dark reflective water, warm small window accents. '
             'observed (live project, 2026-11-23): low hard sun (pitch -24) with strong shafts; the pond clips to white when the view faces the sun (A00/A02), while the west-shore view (W01) already reads dark and calm. '
             'inferred: the mismatch is the key-view direction relative to the sun, not the water material (four single-variable tests ruled out roughness, sun volumetric scattering, sun specular scale and murkiness).',
 'camera': 'observed (R04): figure from head to hip, on the left third (head centre about x 0.28, y 0.25 of the frame), right two thirds open for the path and the house. '
           'authored (this pass): AC_Sph_Camera defaults OutD 165, OutDTight 135, HomeD 118, HomeDTight 98, HeadX 0.30, HeadY 0.24 chosen by matching figure scale in player-camera captures, not by deriving FOV/arm from R04. FOV values unchanged (66 out / 62 home, +3 at run).',
 'ui': 'not in scope of this pass; no reference shows UI. The existing Story Framework prompts stay.',
 'motion': 'observed (R05): balanced stance, walking stride with opposite arm swing, a turn with the trunk leading and a recovery/settle pose. '
           'authority limit: silhouettes only. Timing, weight transfer and camera behaviour come from the project motion work (reports sphirus-ue59-*-2026-11-2x) and real gameplay recordings.',
 'nonnegotiables': [
  'Enclosed Woodland Refuge: depth from far bank, rising slope and tree layers; no open horizon (AGENTS.md).',
  'Approved MetaHuman face and user edits stay untouched.',
  'One camera owner (AC_Sph_Camera), one locomotion owner (GASP / Motion Matching on BP_HybridA_Player).',
  'Close right-shoulder camera, character on the left, mouse look has priority, S back-pedals without turning.',
  'Animation faults are never hidden with DOF, blur, vignette or shake.'],
 'avoid': [
  'Browser game / Three.js prototype / architecture copied from the r2g example games.',
  'Rebuilding the house, pond or routes from a single perspective image.',
  'Raising saturation, fog or bloom as a stand-in for lighting and material work.',
  'Catwalk hip sway, posed-model stance, fatigue shown as dropped shoulders.',
  'Temple / village / castle dressing in the start area.'],
 'deliberate_changes': [
  'Gameplay camera moved from the previous tighter bust framing (OutD 124, head at x 0.34 / y 0.33) to the R04 head-to-hip framing. Rollback: manifest backup of AC_Sph_Camera (see STATUS.txt).',
  'No atmosphere or water value was changed: every tested candidate was reverted because the captures showed no improvement.']}
wr('style.json', style)

# ---------------------------------------------------------------- game.json
game = {
 'status': 'draft',
 'premise': 'First representative slice of Sphirus World in the existing Unreal project: leave the lived-in house, cross the yard, go down to the pond, start up the rear forest trail.',
 'actions': ['walk (W/A/S/D)', 'jog (hold Shift)', 'sprint (Shift+Ctrl)', 'back-pedal (S) without turning', 'look (mouse)', 'interact (E) at day stations'],
 'loop': {'goal': 'observed (project): day stations - bed, wardrobe, tea, mask bench, wood, hearth - are the existing loop; this pass adds no mechanic.',
          'success': 'authored for this pass: the slice route is walkable with the saved player and reads as one identity from the gameplay camera.',
          'failure_or_pressure': 'none in this slice (exploration); fatigue only lowers pace.',
          'restart': 'PIE restart / Story Framework save-load; the user slot is never written by tests (sha1 checked per run).'},
 'mechanics': [
  {'name': 'gait ladder', 'origin': 'observed in project', 'detail': 'Shift = jog, Shift+Ctrl = sprint, S = back-pedal. Unchanged.'},
  {'name': 'resonance', 'origin': 'observed in project', 'detail': 'AC_Sph_Camera Res/ResTarget drive MPC_Sph_Perception (Resonance, ResonanceGrade) and PPV EX_Look_Resonance. No new rule, collision, route or puzzle is derived from any image; R06 was not supplied.'}],
 'invariants': ['Collision and layout of the slice are unchanged by this pass.', 'User save sha1 identical before and after every run.', 'No second camera or movement system.'],
 'levels': ['/Game/GraceRanger/Maps/L_GR_SphirusHouse (+ L_GR_CurrentHouseContent, L_SphirusHouse_ASSET_YARD)'],
 'assumptions': ['Stills taken after a teleport prove framing and look at that point only.', 'Recorded sessions use injected key events and harness-written look rotation at a fixed 30 Hz game step; they are not a human-played or gamepad session.']}
wr('game.json', game)

# ---------------------------------------------------------------- assets.json (existing project assets judged against the references; nothing generated)
assets = {'items': [
 {'id': 'camera-ac-sph-camera', 'references': ['ref-004'], 'representation': 'existing Blueprint component /Game/Sphirus/Player/Camera/AC_Sph_Camera (class defaults)', 'status': 'accepted', 'runtime_path': 'app/UNREAL_SOURCE_MANIFEST.json',
  'notes': 'Changed in this pass (framing defaults). The runtime_path points at the hash manifest because the .uasset lives in the Unreal Content tree, outside this case.'},
 {'id': 'hair-messy-bob', 'references': ['ref-001'], 'representation': 'existing groom /Game/Grooms/001_Messy_Bob + binding GB_Sph_Hair_81', 'status': 'accepted', 'runtime_path': 'app/UNREAL_SOURCE_MANIFEST.json',
  'notes': 'Already in the project and on the active pawn; matches the R01 hair mass. Not changed.'},
 {'id': 'outfit-going-out', 'references': ['ref-001'], 'representation': 'needed: long-sleeve henley, slate jeans, ankle boots fitted to SKM_MHC_Sph8_BodyMesh', 'status': 'deferred',
  'notes': 'Not verified in this pass whether a fitted henley/jeans/boots set exists among the wardrobe sets. The active start look is RetroTop + Pants70. No purchase, generation or external upload was made.'},
 {'id': 'pond-water-key-view', 'references': ['ref-002'], 'representation': 'existing EX_Pond_CalmSurface with MI_EX_Pond; sun EX_PostRain_Sun', 'status': 'deferred',
  'notes': 'White clipping toward the sun remains. Roughness, sun volumetric scattering, sun specular scale and murkiness were each tested alone and reverted. Next step is a sun-direction / canopy decision, which changes the approved look and needs the user.'},
 {'id': 'house-shell', 'references': ['ref-002', 'ref-003'], 'representation': 'existing house (L_GR_CurrentHouseContent)', 'status': 'accepted', 'runtime_path': 'app/UNREAL_SOURCE_MANIFEST.json',
  'notes': 'Kept as is: the references are not a rebuild order.'},
 {'id': 'resonance-look', 'references': [], 'representation': 'existing M_Sph_Resonance, MPC_Sph_Perception, PPV EX_Look_Resonance', 'status': 'deferred',
  'notes': 'R06 not supplied; nothing changed.'}]}
wr('assets.json', assets)
print('CONTRACTS_WRITTEN')
