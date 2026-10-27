# SHME V2.32 — değişiklik listesi (2026-10-27)

## Üretimde (promote232, verify232 ALL_OK temiz yeniden açılış)
| grup | varlık / değer | V2.31 değeri | geri alma |
|---|---|---|---|
| camera | DA_SHM_Response_Default: CamOrbitEnabled true, CamOrbitLagTau 0.3, CamOrbitFreq 5, CamOrbitMaxSprint 16, MaxJog 8, MaxWalk 2, TravelW 0.5 | Enabled false (alan yoktu) | promote232 rollback |
| camera | BP_GR_Player: değişken GR_SHM_CamOrbit; GR_UpdateSHMSignals setter (Select(gate, SHM.CamOrbitYaw, 0)); GR_UpdateRig MakeRotator_43.Yaw = eski kaynak + GR_SHM_CamOrbit | — | checkpoint pre_v232 |
| camera | BP_SHM_HumanMotionComponent SHM_UpdateCameraV21: yörünge bloğu + LastHitBy onarımı (GetLastHitBy → Pawn::GetController) | — | checkpoint pre_v232 / pre_lhb232 |
| bfexit | ABP_GR_MotionMatchingBase: SHM224_DB_JRBwd / JRBwdM → V232/PSD_SHM232_JogRevBwdX; SHM231_DB_JRBwdS → V232/PSD_SHM232_SlowRevBwdX | V226/PSD_SHM226_JogRevBwd, V231/PSD_SHM231S_SlowRevBwd | promote232 rollback |
| loadedbf | ABP: SHM230_DB_JRBwdL → V232/PSD_SHM232_LoadRevBwdX | V226/PSD_SHM226_JogRevBwd | promote232 rollback |
| loadedbf | V231/PSD_SHM231L_LoadRevFwd YERİNDE yeniden kuruldu: 30 yüklü F_B (P29 yeniden) + SHM226_JogRev_F_B_P21 / P30 geri düşüş | 32 yüklü F_B | checkpoint pre_v232 (editör kapalı) |
| floorguard | DA: SwingFloorGuard 1.5 (T7) | 0 | promote232 rollback |

## Yeni varlıklar
- /Game/GraceRanger/SHME/Animations/V232/PSD_SHM232_JogRevBwdX, PSD_SHM232_LoadRevBwdX, PSD_SHM232_SlowRevBwdX
- V231 loaded klasöründe yeniden üretilen F_B P29 klibi (gen232_loaded)
- Starts/Jog/SHM232_IS_* (9 kopya, NÖTR: orijinalin birebir eşi; başlangıç DB'lerinde)

## Kurulu ama kapalı
- DA SwingPelvisComp 0 (T6 reddedildi), ABP SHM232_StartBind 0 (sb reddedildi), DA IntentTickPrePhysics false (tick sırası reddedildi)
- Başlangıç kliplerinde SHM226_V/W + SHM232_SW eğrileri (StartBind 0 iken etkisiz)

## Geri alınan / değişmeyen
- 23 Stops klibi + 17 JogQ başlangıcı checkpoint'ten geri yüklendi (minclear / pinstart etkisiz veya gerilemeli).
- Checkpoint'siz kalan: A_CT_Ref_Walk_Stop_F_L/R + 4 A_CT_Sample_* (≤ 1.2 cm salınım kaldırma; rapor §1).

## Araçlar (metin)
- Tools/SHME_V232_20261027/: cam232, camcmp232, blip232, upper232, terrain232, tables232, promote232, verify232, fix_v232_lasthitby, installers, generators.
- Tools/SHME_V1_20260925/build_funcs.py: LastHitBy onarımı her yeniden kurulumda.
- shm_src.py / shm_profiles.py / shm_component_vars.py / qa_pie.py / v212_run.sh: V2.32 blokları (diff'ler code/ içinde).
