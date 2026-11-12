# Değişiklik listesi — kamera kalanları (2026-11-12/13)

| Varlık | Değişiklik | Betik (`Tools/Motion_20261112/`) |
|---|---|---|
| `/Game/Sphirus/Player/Camera/AC_Sph_Camera` | havada dikey izleme (`JumpPivK` 25, `JumpHeadK` 8); arkada-engel yükseltmesi değişkene (`BackRaise` 10) ve ×SafeFrac³; merdiven ileri beslemesi (`VzF`, `ZLead` 0,2); çay iş kadrajı (tür 5: arka 1, yan 100) | `k9_jumpcam.py`, `k10_backraise.py`, `k11_backraise_safe.py`, `k14_backraise10.py`, `k13_stairlead.py`, `k12_teaprofile.py` |
| `/Game/Sphirus/Player/Motion/AC_Sph_Motion` | kapı uzanma sinyali (`ReachPt/ReachA/ReachR`, zarf 0,28 / 0,6 / 1,0 sn, menzil 120 cm) | `m3_reach.py` |
| `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP` | iki iki-kemik IK (hand_r, hand_l), dünya uzayı hedef, dirsek kendi bükümünde | `p6_reach.py` |
| `BP_HybridA_Player` | konfor paneli sahibi (`GR_ComfortToggle`, `GR_ComfortW`), açılışta konfor kaydı yükleme | `c4_comfort_pawn.py`, `c5_createwidget.py`, `c7_saveexec.py` |
| `/Game/Sphirus/Player/Camera/WBP_Sph_Comfort` (yeni) | konfor paneli | `c2_comfort_widget.py`, `c3_comfort_logic.py`, `c6_layout.py` |
| `/Game/Sphirus/Player/Camera/SG_Sph_Comfort` (yeni) | konfor kaydı sınıfı (slot `SphComfort`) | `c1_comfort_assets.py` |
| `/Game/Sphirus/Player/Input/IA_Sph_Comfort` (yeni) + `IMC_GR_SFGameplay` | F10, gamepad View (boştu); duraklatılmışken de çalışır | `c1_comfort_assets.py` |
| `.../Exterior20260921/Materials/M_EX_WindFoliage_NearFade` (yeni) | satıcı `M_Object_Wind_Foliage` kopyası + yakın-kamera titreşimli solma | `f1_nearfade.py` |
| `.../MI_EX_Plant_Level02_FO_NearFade` + `MI_EX_{Bush01,BushCollectionSet02,BushSalixElag01,SonoSapling01}_FO_NearFade` (yeni) | satıcı ara/yaprak örneklerinin proje kopyaları | `f1_nearfade.py` |
| `MI_PR_Fern01_FO`, `MI_PR_FernLong01`, `MI_PR_FernWild01`, `MI_PR_Fern_03_S_FO`, `MI_EX_Refuge_Pine_Juvenile_FO`, `MI_PR_PineTree03_FO`, `MI_PR_PineTree01_FO`, `MI_PR_PineTree05_FO`, `MI_GL_Bush01_FO`, `MI_GL_BushCollectionSet02_FO`, `MI_GL_BushSalixElag01_FO`, `MI_GL_SonoSapling01_FO` | yalnız ebeveyn değişti (kendi doku/sayı değerleri aynı) | `f1_nearfade.py` |

Dokunulmayanlar: satıcı dosyaları (PineForestPack, Story Framework kapı/menü), harita, ışık, istasyonlar, klipler.

Geri alma: ilgili `day_mot_*` manifestinin yedeği editör kapalıyken geri kopyalanır; yaprak solması için 12 örneğin ebeveyni eski satıcı örneğe döndürülebilir (yeni 6 malzeme silinebilir); konfor paneli için `IA_Sph_Comfort` eşlemesi kaldırılırsa panel açılmaz.

Test araçları: `vteafire.sh` (çay/şömine, hub kodu), `vflow2/3/4.sh` (merdiven, köşe, kapı, gamepad, 30/60/120 Hz), `probe_pause.sh`, `probe_comfort.sh`, `probe_hub.sh`, `an_fps.py`, `q_final3.py`.
