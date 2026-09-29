"""Assemble REPORT.md + public_report/ for the CharacterFinal candidate (body v6 + home outfit V2 + hair) from the
pipeline's JSON evidence and boards. Verdicts live in verdicts.json (edited after the visual review)."""
import json, pathlib, shutil
R = pathlib.Path(__file__).resolve().parents[2]; O = R/'Saved/Codex/CharacterFinal_20260929'; C = O/'captures'; B = O/'boards'; P = O/'public_report'
def J(p, default=None):
    try: return json.loads(open(p, encoding='utf-8').read())
    except Exception: return default
V = J(O/'verdicts.json', {}); st = J(O/'br_stats_v6.json', {}); prop = J(O/'proportions_v6.json', {}); j4 = J(O/'j4_outfit_meshes.json', {}); hair = J(O/'cf_hair.json', {}); bq = J(O/'outfit_v2_build_c/outfit_build_qa.json', {})
ev = {k: J(C/f'eval_{k}.json') for k in ('cf_neutral', 'cf_deform', 'cf_gameplay', 'cf_lods')}
L = []
L.append('# SPHIRUS final character pass: body v6 + home outfit V2 + hair (2026-09-29)\n')
L.append('Isolated candidate: `/Game/Sphirus/CharacterLab/CharacterFinal_20260929/` (`Body/SKM_CF_BodyMesh`, `Body/SKM_CF_FaceMesh`, `Body/ABP_CF_*_PostProcess`, `Outfit/SKM_Home2_Henley`, `Outfit/SKM_Home2_Shorts`, `Outfit/Materials`, `Outfit/Textures`, `Hair/Hair_S_Updo_CF` + `_Binding` + `MI_CF_Auburn_*`). Not promoted. Production `MH_MainCharacter`, the accepted B2 body, the accepted SHCB set, the BR v5 candidate and the user-created face are untouched.\n')
L.append('Reference: the attached concept board (THE GUARDIAN: oatmeal Henley with open placket, charcoal drawstring shorts, barefoot, auburn messy low bun) used for outfit, hair and mood only; the face is the user\'s MetaHuman.\n')
L.append('## Method and honesty')
L.append('- BODY: procedural neutral morph `BR_Neutral` v6 (the v5 feature set + audit-driven secondary corrections + a foot/ankle vector pass), baked as a morph target on copies of the BR candidate meshes; SHCB correctives rebased on v6 and re-baked; all LODs re-projected. **PROCEDURAL, ARTIST-GRADE = NO.** Manual brush sculpting was not available in this session; the artist round-trip package (`Saved/Codex/BodyRealismArtist_20260929/`) remains the path to artist-grade soft tissue.')
L.append('- OUTFIT: pattern-logic garments built and cloth-draped in Blender 5.2 against the v6 body (no body inflation), skinned offline, imported as skeletal meshes with three Blender-authored LODs. Chaos Cloth not used (skinned garments).')
L.append('- HAIR: closest MetaHuman-library groom (`Hair_S_Updo`: messy bun with face-framing strands) duplicated into the candidate, auburn material instances, GroomBinding built against the candidate face (source = MetaHuman groom head). Custom groom authoring (Alembic importer) is not enabled in this project.\n')
L.append('## Body v6 (procedural)')
L.append(f"Displacement (all moved body vertices, n={st.get('moved_verts')}): mean {st.get('mean_mm', 0):.2f} mm, p95 {st.get('p95_mm', 0):.2f} mm, max {st.get('max_mm', 0):.2f} mm; feet/hands vector pass {st.get('feet_hands_verts')} verts, max {st.get('feet_hands_max_mm', 0):.2f} mm (medial arch lift, malleoli, Achilles hollows, heel pad; exempt from the low-pass so the arch is a real silhouette change).")
L.append('New v6 forms over v5: lateral breast root softening + axillary tail (attachment, not size), inframammary fold softening + lower-pole fullness, upper-pole relax, sternal plane, flank pad, lower-abdomen softness, glute-ham weight, lateral fold fade, medial lower glute, lateral glute soft hollow, inner-thigh softness, knuckle/thenar hints. Feature amplitudes: ' + ', '.join(f"{k} {v:.2f} mm" for k, v in (st.get('feature_max_mm') or {}).items() if k in ('lateral_root_soften', 'axillary_tail', 'imf_soften', 'upper_pole_relax', 'sternal_plane', 'flank_pad', 'lower_abdomen_soft', 'glute_ham_weight', 'fold_lateral_fade', 'lower_glute_medial', 'inner_thigh_soft')) + '.')
if prop: L.append('Proportion preservation (convex-hull circumference, accepted B2 -> v6): ' + ' · '.join(f"{k} {a:.2f}->{b:.2f} cm ({d:+.2f} mm)" for k, (a, b, d) in prop.items()) + '. Height 173.272 cm unchanged; face above the collar 0.0 mm.')
L.append('SHCB: helper nodes and driver unchanged (+2.0/+3.0/+3.5 cm at 150/165/180); SHC_150/165/180 l/r recomputed on the v6 neutral and baked (base positions unchanged, 0.0 cm); far-LOD helper effect re-projected (70/70 LOD morph bakes OK).\n')
L.append('## Outfit V2 (Blender construction + drape)')
L.append('Henley: front/back torso shell (ease chest +7.5, waist +8.5, hip +9.5, hem +9 cm), shared shoulder seam, rounded scoop neckline (centre front z 132.5, neck base ~135.5), narrow placket slit to z 121.5 with 4 buttons (top 2 open), set-in sleeves (ease 7.5 -> 8 -> 4.5 cm at the wrist), armhole dropped 2.4 cm below the armpit with +8 cm underarm ease (fabric reserve for 165-180 deg elevation), high-hip hem (side z 97.5, back 96, slightly irregular), neck binding / placket / cuffs / hem built on the settled cloth. Cloth: mass 0.3, tension 30, bend 1.5, shear 15, 90 frames, shorts as extra collider.')
L.append('Shorts: soft waistband (top z 104.5, 3.5 cm, +6.5 cm ease, pinned) + hip shell (+8..+10 cm) + two short leg tubes joined on a shallow sagittal crotch seam (crotch 3.4 cm below the body crotch), hem mid 64.5 cm with a curved hem (sides +2.6 cm), slight A-line (+10 -> +11.5 cm), side-entry pocket welts, eyelets, thin drawstring with knot and two uneven tails, hems. Cloth: mass 0.10, tension 60, bend 2.5.')
for g in ('henley', 'trousers'):
    q = (bq.get('garments') or {}).get(g+'_after_fix', {}); e = (bq.get('garments') or {}).get(g+'_export', {}); e1 = (bq.get('garments') or {}).get(g+'_lod1_export', {}); e2 = (bq.get('garments') or {}).get(g+'_lod2_export', {})
    L.append(f"- {'henley' if g == 'henley' else 'shorts'}: LOD0 {e.get('verts')} verts / {e.get('tris')} tris, LOD1 {e1.get('tris')} tris, LOD2 {e2.get('tris')} tris (Blender decimate 50 % / 22 % cloth + 45 % details); rest clearance min {q.get('min_signed_cm', 0):.2f} cm, p5 {q.get('clearance_p5_cm', 0):.2f}, median {q.get('clearance_median_cm', 0):.2f}, penetrating verts {q.get('penetrating_verts')}.")
for g, key in (('henley', 'henley'), ('trousers', 'trousers')):
    d = j4.get(key, {})
    if d: L.append(f"- `{d.get('asset')}`: LOD0 {d.get('lod0')}, LOD1 {d.get('lod1')}, LOD2 {d.get('lod2')} (verts, tris); bones {d.get('bones_in_mesh')}, unweighted 0/{d.get('lod1_unweighted_final')}/{d.get('lod2_unweighted_final')}; slots {d.get('materials')}; rejected non-manifold triangles {d.get('rejected_triangles')}.")
L.append('Skin weights: offline (closest point on the v6 body -> barycentric blend of the body weights, 14 Laplacian passes, 8 influences); skeleton = isolated ShoulderFix `metahuman_base_skel`, bind = body mesh bind. Garments follow the body by leader-pose; SHCB helper bones inherited through `upperarm_out` weights.')
L.append('Materials: `M_SPH_Textile` (Cloth shading, two-sided) + 6 instances (Henley oatmeal tint 0.97/0.93/0.86, jersey knit detail; shorts warm charcoal tint 1.25/1.2/1.15 on the charcoal map, twill detail; trims, drawstring, buttons); unique 2048 BC/N/RA per garment + 512 detail tiles, stitch rows along the UV island borders, faint tonal motif on the shorts.\n')
L.append('## Hair')
L.append(f"Style `{hair.get('style')}` from the MetaHuman Creator library (on disk); the concept\'s low messy bun has no library equivalent on disk (`Hair_M_UpdoBun_Messy` thumbnail only). Materials: {', '.join(m[1].split('/')[-1] for m in hair.get('materials', []))} (melanin 0.46, redness 0.92, red variation 0.18, roughness overall 0.6, scraggle 0.22). Binding: `{(hair.get('binding') or {}).get('path')}` (source {(hair.get('binding') or {}).get('source', '').split('/')[-1]}). Alternates bound for the QA comparison only: {', '.join(hair.get('alternates', {}).keys())}.\n")
# ---- evaluation tables
L.append('## Body clearance / deformation (captured UE geometry: real skinning + BR v6 + SHCB, garment vs body BVH)')
for lab, title in (('cf_neutral', 'Neutral'), ('cf_deform', 'Deformation poses'), ('cf_gameplay', 'Gameplay poses'), ('cf_lods', 'LOD1 / LOD2')):
    e = ev.get(lab)
    if not e: L.append(f'### {title}: NOT_TESTED (no evaluation file)'); continue
    L.append(f'### {title}')
    L.append('| pose | Henley pen. verts (max cm) | Henley clearance p5 / median | stretch p99 | Shorts pen. verts (max cm) | Shorts clearance p5 / median | stretch p99 | shirt inside shorts |')
    L.append('|---|---|---|---|---|---|---|---|')
    for nm, row in e['poses'].items():
        if not isinstance(row, dict): L.append(f'| {nm} | missing |||||||'); continue
        h = row.get('henley', {}); t = row.get('shorts', {})
        L.append(f"| {nm.replace('cf_dfm_', '').replace('cf_gp_', '').replace('cf_', '')} | {h.get('penetrating')} ({h.get('max_penetration_cm')}) | {h.get('clearance_p5_cm')} / {h.get('clearance_median_cm')} | {h.get('stretch_p99', '-')} | {t.get('penetrating')} ({t.get('max_penetration_cm')}) | {t.get('clearance_p5_cm')} / {t.get('clearance_median_cm')} | {t.get('stretch_p99', '-')} | {row.get('shirt_inside_shorts_verts', '-')} ({row.get('shirt_inside_shorts_max_cm', '-')}) |")
    L.append('')
# ---- verdict sections
for sec in ('body_review', 'outfit_review', 'hair_review', 'skin', 'performance', 'preservation'):
    if V.get(sec): L.append(f"## {V[sec]['title']}"); L.extend(V[sec]['lines']); L.append('')
for tname, key in (('BODY', 'body'), ('OUTFIT', 'outfit'), ('HAIR', 'hair'), ('FINAL CHARACTER', 'final')):
    if V.get(key):
        L.append(f'## FINAL STATUS: {tname}'); L.append('| item | status |'); L.append('|---|---|')
        for k, v in V[key]: L.append(f'| {k} | {v} |')
        L.append('')
if V.get('not_tested'): L.append('## NOT_TESTED'); L.extend('- '+x for x in V['not_tested']); L.append('')
L.append('## Boards'); L.extend(f'![{b.stem}](boards/{b.name})' for b in sorted(B.glob('*.jpg'))); L.append('')
L.append('## Reference'); L.append('![concept](reference/concept_guardian_home.png)'); L.append('')
(O/'REPORT.md').write_text('\n'.join(L), encoding='utf-8')
if P.exists(): shutil.rmtree(P)
for d in ('boards', 'blender_preview', 'tools', 'reference', 'hair_thumbs'): (P/d).mkdir(parents=True)
for b in B.glob('*.jpg'): shutil.copy2(b, P/'boards'/b.name)
for f in ('sheet.jpg',):
    src = O/'outfit_v2_build_c/render'/f
    if src.exists(): shutil.copy2(src, P/'blender_preview'/('outfit_v2_'+f))
shutil.copy2(O/'reference/concept_guardian_home.png', P/'reference/concept_guardian_home.png')
if (O/'hair_thumbs/sheet.jpg').exists(): shutil.copy2(O/'hair_thumbs/sheet.jpg', P/'hair_thumbs/library_sheet.jpg')
for f in ('j4_outfit_meshes.json', 'cf_body_setup.json', 'cf_hair.json', 'br_stats_v6.json', 'proportions_v6.json', 'j2_br_morph_v6.json', 'j2_morph_data_br_shcb.json', 'j2_br_lods.json', 'verdicts.json', 'preservation_hashes.json'):
    if (O/f).exists(): shutil.copy2(O/f, P/f)
for k in ev:
    if (C/f'eval_{k}.json').exists(): shutil.copy2(C/f'eval_{k}.json', P/f'eval_{k}.json')
if (O/'outfit_v2_build_c/outfit_build_qa.json').exists(): shutil.copy2(O/'outfit_v2_build/outfit_build_qa.json', P/'outfit_build_qa.json')
for t in (R/'Tools/CharacterFinal_20260929').glob('*'):
    if t.suffix in ('.py', '.sh', '.ps1') and not t.name.startswith('_'): shutil.copy2(t, P/'tools'/t.name)
shutil.copy2(O/'REPORT.md', P/'README.md')
print('report written', O/'REPORT.md', 'public files', len(list(P.rglob('*'))))
