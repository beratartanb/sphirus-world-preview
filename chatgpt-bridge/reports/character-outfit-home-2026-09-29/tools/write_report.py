"""Assemble REPORT.md + public_report/ for the home outfit candidate from the pipeline's JSON evidence and boards."""
import json, gzip, pathlib, shutil, hashlib, subprocess
R = pathlib.Path(__file__).resolve().parents[2]; O = R/'Saved/Codex/OutfitHome_20260929'; C = O/'captures'; B = O/'boards'; P = O/'public_report'
def J(p, default=None):
    try: return json.loads(open(p).read())
    except Exception: return default
j4 = J(O/'j4_meshes.json', {}); j5 = J(O/'j5_lods.json', {}); bq = J(O/'build_final/outfit_build_qa.json', {})
ev = {k: J(C/f'eval_{k}.json') for k in ('of_deform', 'of_gameplay', 'of_lods', 'of_neutral')}
def lodrow(name):
    a = (j5.get(name) or {}).get('after') or []
    return ' / '.join(f"LOD{x['lod']} {x['tris']} tris, {x['verts']} verts" for x in a if 'tris' in x)
def pen(row, g): return row.get(g, {})
lines = []
lines.append('# SPHIRUS first production outfit candidate: home / everyday (2026-09-29)\n')
lines.append('Candidate: `/Game/Sphirus/CharacterLab/Outfit_Home_20260929/` (`SKM_Home_Henley`, `SKM_Home_Trousers`, `Materials/M_SPH_Textile` + 6 instances, `Textures/`). Not promoted; the production character `MH_MainCharacter` and its outfit asset are untouched.\n')
lines.append('Reference: the supplied clothing image (ivory Henley, charcoal drawstring trousers, barefoot) used for garment language only.\n')
# ---- garment construction
lines.append('## Garment construction (Blender 5.2, `Tools/OutfitHome_20260929/blender_outfit_build.py`)')
lines.append('Pattern logic, not body inflation: the Henley is a front/back body shell (rings about the torso sections + ease) closed over a shared shoulder seam, with a round neck opening, centre-front placket slit and set-in sleeve tubes; the trousers are a waistband + hip shell joined to two leg tubes along a sagittal crotch seam. Ease: chest +10, waist +14, hem +20 (over the trousers), sleeve +12.5 -> cuff +3 cm; trousers waistband +7 (soft, drawstring), hip +12, thigh +13, hem 47 cm straight leg.')
lines.append('Drape: Blender cloth (trousers mass 0.10 / tension 60 / bend 2.5; Henley mass 0.3 / tension 30 / bend 1.5), body collision against the exact current BR neutral body (BR_Neutral applied), trousers as a second collider for the shirt, pinned neckline / shoulder seam (0.3) / knit cuffs / tucked centre front / waistband; 90 frames; post-sim Laplacian relax; then construction details built on the settled cloth (neck binding, placket strips, 5 buttons with holes, cuffs, hems, waistband double layer with gathers, eyelets, drawstring with knot and two hanging ends, side-seam pocket welts).')
fa = bq.get('facts', {})
lines.append(f"Body facts used: crotch z {fa.get('z_crotch', 0):.1f} cm, armpit z {fa.get('z_armpit', 0):.1f} cm, shoulder joint {fa.get('shoulder_joint_l')}.")
for g in ('henley', 'trousers'):
    q = bq.get('garments', {}).get(g+'_after_fix', {}); e = bq.get('garments', {}).get(g+'_export', {})
    lines.append(f"- {g}: {e.get('verts')} verts / {e.get('tris')} tris exported (LOD0); rest clearance to the body min {q.get('min_signed_cm', 0):.2f} cm, p5 {q.get('clearance_p5_cm', 0):.2f}, median {q.get('clearance_median_cm', 0):.2f}, penetrating verts {q.get('penetrating_verts')}.")
lines.append('Thickness: main panels single layer (two-sided material); binding, placket, cuffs, hems, waistband boxed 0.16-0.22 cm; buttons 0.22 cm; cord radius 0.3 cm.\n')
# ---- UE assets
lines.append('## Unreal assets')
for g in ('henley', 'trousers'):
    d = j4.get(g, {})
    lines.append(f"- `{d.get('asset', '')}`: LOD0 {d.get('lod0')} (verts, tris), LOD1 (Blender decimate 50 %) {d.get('lod1')}, engine LOD2; {lodrow('SKM_Home_'+g.capitalize())}; bones {d.get('bones_in_mesh')}, unweighted verts {d.get('unweighted_final')} (LOD1 {d.get('lod1_unweighted_final')}); slots {d.get('materials')}; rejected non-manifold triangles {d.get('rejected_triangles')}.")
lines.append('Skin weights: authored offline (closest point on the BR body -> barycentric blend of the body\'s own weights, 2 smoothing passes, 8 influences) and written per vertex; skeleton = the isolated ShoulderFix `metahuman_base_skel` copy, bind pose = the body mesh bind (`use_mesh_bone_proportions`). The garments follow the body through leader-pose (no own animation, no PostProcess ABP); the SHCB helper bones are inherited through `upperarm_out` weights. Chaos Cloth: not used (skinned garments; see the deformation section).')
lines.append('Materials: `M_SPH_Textile` (Cloth shading model, two-sided, MaterialAttributes): unique 2048 BaseColor / Normal / Roughness-AO per garment + tiling weave detail normal (jersey knit for the Henley, twill for the trousers, angle-corrected blend), tint, roughness multiplier, fuzz colour, cloth amount. Instances: MI_Home_Henley, _Henley_Trim, _Trousers, _Trousers_Trim, _Drawstring, _Buttons. Textures 8 (6 x 2048 unique, 2 x 512 tiles).')
lines.append('UVs: rectangular islands per panel (front/back torso, sleeves, binding, placket, cuffs, hem, buttons; hip front/back, legs, band, welts, hems, cord, crotch), 0.7 mm/px at 2048; seam stitch rows drawn along island borders in the unique maps.\n')
# ---- QA
lines.append('## Body clearance / deformation (captured UE geometry: real skinning + BR morph + SHCB, garment vs body+head BVH)')
for lab, title in (('of_deform', 'Deformation poses'), ('of_gameplay', 'Gameplay poses'), ('of_lods', 'LOD1 / LOD2'), ('of_neutral', 'Neutral')):
    e = ev.get(lab)
    if not e: lines.append(f'### {title}: NOT_TESTED (no evaluation file)'); continue
    lines.append(f'### {title}')
    lines.append('| pose | Henley pen. verts (max cm) | Henley clearance p5 / median | stretch p99 | Trousers pen. verts (max cm) | Trousers clearance p5 / median | stretch p99 | shirt inside trousers |')
    lines.append('|---|---|---|---|---|---|---|---|')
    for nm, row in e['poses'].items():
        if not isinstance(row, dict): lines.append(f'| {nm} | missing |||||||'); continue
        h = row.get('henley', {}); t = row.get('trousers', {})
        lines.append(f"| {nm.replace('of_dfm_', '').replace('of_gp_', '').replace('of_', '')} | {h.get('penetrating')} ({h.get('max_penetration_cm')}) | {h.get('clearance_p5_cm')} / {h.get('clearance_median_cm')} | {h.get('stretch_p99', '-')} | {t.get('penetrating')} ({t.get('max_penetration_cm')}) | {t.get('clearance_p5_cm')} / {t.get('clearance_median_cm')} | {t.get('stretch_p99', '-')} | {row.get('shirt_inside_trousers_verts', '-')} ({row.get('shirt_inside_trousers_max_cm', '-')}) |")
    lines.append('')

# ---- verdict sections (visual review of the boards + evaluator numbers)
lines.append('## SHCB compatibility (ShoulderFix helper bones inherited through body weights; SHCB itself untouched)')
lines.append('150 deg elevation: clean, the shoulder seam rides up with the SHCB clavicle/upperarm_out motion, no inside-out cloth. 165 / 180 deg: the underarm of the skinned Henley opens (visible body through the armpit gap, small inside-out patches at the sleeve root, evaluator max penetration 5.3-6.8 cm on 1-3 vertices at the neck-seam edge = boundary false positives, real underarm gap is the visible defect). Verdict: PARTIAL (150 PASS, 165-180 visible underarm artefacts). Fix path: Chaos Cloth on the sleeve root panel or an extra upperarm_out-driven corrective; not a body/SHCB change.')
lines.append('')
lines.append('## Chaos / cloth simulation')
lines.append('Chaos Cloth is NOT used in the candidate: garments are fully skinned (offline weights), drape baked from the Blender cloth simulation. Reason: deterministic, cheap, no PIE/cloth asset required for review; the trade-off is the underarm opening at 165-180 deg and stiff hem/drawstring ends in motion. A Chaos Cloth pass (Henley hem + sleeves, drawstring ends, trouser legs below the knee) is the recommended next step after the silhouette is approved.')
lines.append('')
lines.append('## UV / materials')
lines.append('UVs: non-overlapping rectangular islands per panel, 0.7 mm/px at 2048. Materials: one master `M_SPH_Textile` (Cloth shading, two-sided) + 6 instances; unique BaseColor/Normal/Roughness-AO per garment, tiling knit/twill detail normal, ivory tint / charcoal tint. Textures verified in-viewport after the row-order fix (no mirroring, stitch rows along seams, faint motif on the trousers). Verdict: PASS for review quality; the knit detail tile is slightly too regular at close range (visible in the neckline / chest close-ups).')
lines.append('')
lines.append('## LOD')
lines.append('LOD0 Henley 16151 tris / Trousers 19876 tris; LOD1 (Blender 50 % decimate, own weights) 8075 / 9937 tris: silhouette and drape hold in neutral, walk, squat, 180. LOD2 (engine `regenerate_lod`, 12.5 %) 1820 / 2483 tris: sleeves and trouser legs break (spikes, open hems) -> LOD2 must be re-authored in Blender like LOD1. Verdict: PARTIAL (LOD0/LOD1 PASS, LOD2 FAIL).')
lines.append('')
lines.append('## Performance')
lines.append('Total outfit LOD0 36027 tris / 2 skeletal meshes / 6 material instances / 8 textures (6 x 2048, 2 x 512). No cloth sim cost, no extra bones, no PostProcess ABP. Within a normal third-person hero budget; not profiled in a real level (NOT_TESTED for frame cost).')
lines.append('')
lines.append('## Preservation')
lines.append('Package hashes before/after: B2 pending body 59d604a404ba, production body cc17c8b434d9, production outfit d4d07c6e4d50, skeleton 7c70d7a26da0, BR body e204fa5299d0: unchanged. Checkpoint of the candidate folder before asset mutation: `Saved/Codex/OutfitHome_20260929/checkpoint_pre_assets/`.')
lines.append('')
lines.append('## FINAL STATUS')
lines.append('| item | status |')
lines.append('|---|---|')
lines.append('| HENLEY | PASS (visual, neutral + gameplay); underarm at 165-180 see SHCB |')
lines.append('| TROUSERS | PASS |')
lines.append('| FIT | PASS (0 penetrations neutral; 0.7 cm p5 clearance; shirt hem over the waistband, no tuck-through) |')
lines.append('| CLOTH DEFORMATION | PARTIAL (skinned drape holds through 150 deg, crouch/squat/hipflex; trousers max 2.2 cm at hipflex on 130 verts; Henley elbow 1.3 cm; no Chaos Cloth) |')
lines.append('| SHCB COMPATIBILITY | PARTIAL (150 PASS; 165 / 180 underarm opening) |')
lines.append('| MATERIAL QUALITY | PASS for review (knit tile regularity noted) |')
lines.append('| LOD | PARTIAL (LOD0 / LOD1 PASS, engine LOD2 FAIL) |')
lines.append('| READY FOR USER APPROVAL | YES, for review of the silhouette / garment language; not for promotion |')
lines.append('| PRODUCTION CHARACTER MODIFIED | NO |')
lines.append('')
lines.append('## Boards')
for b in sorted(B.glob('*.jpg')): lines.append(f'![{b.stem}](boards/{b.name})')
lines.append('')
(O/'REPORT.md').write_text('\n'.join(lines), encoding='utf-8')
# public report
if P.exists(): shutil.rmtree(P)
(P/'boards').mkdir(parents=True); (P/'blender_preview').mkdir(parents=True); (P/'tools').mkdir(parents=True)
for b in B.glob('*.jpg'): shutil.copy2(b, P/'boards'/b.name)
for f in ('sheet_views.jpg', 'sheet_closeups.jpg'):
    src = O/'build_final/render'/f
    if src.exists(): shutil.copy2(src, P/'blender_preview'/f)
for f in ('j4_meshes.json', 'j5_lods.json'): (O/f).exists() and shutil.copy2(O/f, P/f)
for k in ev:
    if (C/f'eval_{k}.json').exists(): shutil.copy2(C/f'eval_{k}.json', P/f'eval_{k}.json')
(O/'build_final/outfit_build_qa.json').exists() and shutil.copy2(O/'build_final/outfit_build_qa.json', P/'outfit_build_qa.json')
for t in (R/'Tools/OutfitHome_20260929').glob('*.py'): shutil.copy2(t, P/'tools'/t.name)
for t in (R/'Tools/OutfitHome_20260929').glob('*.sh'): shutil.copy2(t, P/'tools'/t.name)
for t in (R/'Tools/OutfitHome_20260929').glob('*.ps1'): shutil.copy2(t, P/'tools'/t.name)
shutil.copy2(O/'REPORT.md', P/'README.md')
print('report written', O/'REPORT.md', 'public files', len(list(P.rglob('*'))))
