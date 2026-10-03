# Asset manifest — GD11 head refinement (2026-10-04)

## A. GD11_BASELINE_READONLY (verified, untouched)

Verification:
- The composition was printed by the capture setup as `COMP4 e g11k9 h23`, with bindings `*_e11`.
- A fresh capture matches the GD11 report frames (board 01).
- All 40 GD11 files are byte-identical to the checkpoint.

| Part | Asset |
|---|---|
| Face | `/Game/Sphirus/CharacterLab/CharacterGuardian11_20261002/Face/SKM_GD11_Face_e`. DNA user data `MHC/DNA/MHC_GD11_E_Head`, 858 morphs, 8 LODs, `Face_Archetype_Skeleton`, `ABP_Face_PostProcess`. |
| MetaHuman character | `.../CharacterGuardian11_20261002/MHC/MHC_GD11_E` |
| Neutral sculpt | `Saved/Codex/CharacterGuardian11_20261002/head_pE.npy`. Auto-rig target `target_e.json`; post-rig `E_postrig.npy` differs by 0.14 mm on average. |
| Skin | `.../CharacterGuardian11_20261002/Skin/MI_LK_Face_{LOD0,LOD1,LOD2,LOD3,LOD4,LOD5to7}_VT_g11k9` and `MI_GD11_Body_k9`. Textures `Skin/Textures/T_LK_Head_{BC,N,SRMF}_k9b`. |
| Eyes | `/Game/Sphirus/CharacterLab/CharacterGuardian3_20261001/Skin/MI_GD3_EyeL_e2` and `MI_GD3_EyeR_e2` (head slots 3/4). Eyeballs, eye shell, lashes, eye edge and cartilage come from the GD11 DNA. Teeth, eye-shell and lacrimal materials come from the P face slots. |
| Hair h23 | `/Game/Sphirus/CharacterLab/CharacterGuardian8_20261002/Hair/GR_LK_Hair_{Main,Loose}_h23` and `MI_GD_Hair_h23` / `MI_GD_HairLoose_h23`. Source: `Saved/Codex/CharacterGuardian8_20261002/hair/h23` (builder `blender_gd8_hair.py` + `build_env.txt`). |
| Brows | `/Game/Sphirus/CharacterLab/CharacterGuardian_20261001/Grooms/GR_GD_Eyebrows_M_SlightArch` |
| Lashes | `.../CharacterGuardian_20261001/Grooms/GR_GD_Eyelashes_S_Thin` |
| Bindings | `.../CharacterGuardian11_20261002/Face/Bindings/GB_GD11_{HairMain,HairLoose,EyebrowsM_SlightArch,EyelashesS_Thin}_e11` |
| Body / garments (unchanged) | B2 body and correctives; Henley `.../CharacterGuardian_20261001/Outfit/SKM_LK_Henley_g17e`; shorts `.../CharacterCorrective_20261001/Outfit/SKM_LK_Shorts_g16c` with Chaos `Cloth/CA_CR_Shorts_m1` |

**Contamination check:**
- None of these are present in the baseline: K5 / GD14 nose, N1 / N2 eye set, later mouth or lower-face shifts, k11 / k12 skin or lip map, h24–h29 hair, later cranium or cheek edits.
- The face is the GD11 E DNA and the skin is g11k9.
- The hair is h23, built for GD8 C8 and bound to E as in GD11.

## B. GD11_HEAD_REFINEMENT (new candidate, not promoted)

Folder: `/Game/Sphirus/CharacterLab/GD11_HeadRefinement_20261003/`. Source data is in `Saved/Codex/GD11_HeadRefinement_20261003/`.

| Part | Asset |
|---|---|
| Face (final) | `Face/SKM_G11R_Face_r3`. DNA user data `MHC/DNA/MHC_G11R_R3_Head`, 858 morphs, 8 LODs, same skeleton and post-process ABP. One fresh auto-rig of `head_R3.npy`; rig fit 0.015 mm mean. |
| MetaHuman character | `MHC/MHC_G11R_R3` |
| Hair (final) | `Hair/GR_LK_Hair_{Main,Loose}_h32` and `Hair/MI_GD_Hair_h32` / `MI_GD_HairLoose_h32` (final colour). Strands and parameters: `hair/h32/`. |
| Bindings (final) | `Face/Bindings/GB_G11R_{HairMain,HairLoose,EyebrowsM_SlightArch,EyelashesS_Thin}_r3h32` |
| Skin, eyes, brows, lashes | GD11 assets used **by reference, unchanged** (not copied, because they were not edited). |
| Rig-test animation | `Face/Diagnostics/AS_G11R_FacialRig`: 27 cases, including sneer, upper-lip raise and nostril dilate/compress. |

**Diagnostic assets, not part of the final candidate:**
- `MHC/MHC_G11R_Work` and `MHC/MHC_G11R_Model`: GD11 own-model readout.
- Hair `h30`, `h31`.
- Bindings `*_r3`, `*_r3b`, `*_r3nat` (M_Natural brow test), `*_r3h30`, `*_r3h31`, `*_test_e`.
- `Studio/MI_LK_Backdrop`, `Studio/MI_LK_Floor2`.

## Geometry chain (`Saved/Codex/GD11_HeadRefinement_20261003`)

1. `head_E_base.npy` is a copy of GD11 `head_pE.npy`.
2. `head_R1.npy`: right-cheek crease removal (`gd11r_face_ops.py`, HF mirror of the clean left cheek).
3. `head_R2.npy`: nose-base transfer from GD11's own model (`blender_gd14_nosebase.py`, high frequency only, k=120).
4. `head_R3.npy`: R2 with the tip lobule restored from R1 (tip position identical to GD11).
