# Değişen / eklenen varlıklar (2026-11-10/11)

Hepsi gated runner ile, yazma manifesti + doğrulanmış yedekle (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/day_cm_*`) yazıldı. Tam geri dönüş: `C:\Users\berat\SphirusCheckpoints\WomanMotion_Pre_20261110_2255` (Content/Sphirus/Player, Hazel Playable, Config, uproject, kayıt kopyası; SHA1 listesi `WomanMotion_Pre_20261110_2255_sha1.txt`).

## Yeni (proje sahipli)
| Varlık | Ne |
|---|---|
| `/Game/Sphirus/Player/GASP/CM/Rig/RTG_Sph_CM_to_UEFN` | Core Motion (MCPaul) → GASP UEFN retarget |
| `/Game/Sphirus/Player/GASP/CM/Anim/CM_af_*` (82) | kadın klip kopyaları: kök hareketi, IK kemikleri, `loop`, `contact_l/r` + `movedata_speed` eğrileri, BranchIn arama pencereleri |
| `/Game/Sphirus/Player/GASP/CM/DB/PSD_CM_*` (32 kullanımda; ilk denemenin 8 yönsüz veritabanı — `PSD_CM_Walk/Jog_Loops/Starts/Pivots`, `PSD_CM_Run_Loops/Starts` — boş ve referanssız duruyor) | yöne göre bölünmüş Motion Matching veritabanları (Relaxed şemaları + PSN_Relaxed_All, Relaxed maliyet ayarları) |

## Değişen
| Varlık | Değişiklik | Önce → sonra |
|---|---|---|
| `ABP_Sph_GASP` | `SphCM` (bool, varsayılan **True**), `CM_Keys/CM_Vals/CM_Out`; gece: `MovementDirection_Recent` (E_MovementDirection) + `MovementDirection_Time` ve 0,1 s kuralı (`w13_mdr.py`); `Update_MotionMatching` içinde ValidDatabases eşlemesi; MM düğümü `PlayRate` | PlayRate 0,85–1,15 → 0,80–1,05 |
| `BP_Sph_GASPCharacter` | `CalculateMaxAcceleration` sabitleri; hız CDO | ivme 800/800/800→300 → 350/420/450→350; hız 165/375/585 → 160/290/500 |
| `BP_HybridA_Player` | hız CDO; ev içi `SphContextSpeedScale` sabiti; `SphMotion` şablonu | 150/165 → 150/160 (=0,9375) |
| `AC_Sph_Motion` (CDO + iki şablon) | `BrakeDecelLow/High`; bekleme kırılmaları | 380/780 → 260/520; Relaxed v01..v07 → CM af_Stand_Idle 03/04/06/02/05 |

## Dokunulmayan
Vendor `MC_Core_Motion`, GASP/Relaxed klipleri, şemaları, seçim tabloları; `ABP_Sph_Body_GASP`, `RTG_Sph_UEFN_to_MH` (köprücük −5° korunuyor), MetaHuman baş/beden/saç/kıyafet, Story Framework, kapılar, envanter, kamera bileşenleri, harita. Ham animasyon veya `.uasset` yayımlanmadı.

## Araçlar
`Tools/WomanMotion_20261110/`: `w1_rtg.py` (retarget), `w2_dbs.py`/`w9_dbdir.py` (veritabanları), `w3_abp.py`/`w10_abpmap.py` (sürücü eşlemesi), `w4_rm.py` (kök hareketi), `w5_ikbones.py` (IK kemikleri), `w6_mmrate.py`, `w7_accel.py`, `w8_dbbias.py`, `w11_curves.py`, `w12_loop.py`, `p_cm_promote.py` (terfi), `cm_cfg.py` (aday ayarları), `vids_cm.sh`/`cmrun.sh` (kayıt, meşgul koruması), `an_cm.py`/`an_summary.py` (analiz), `mksheet.sh`/`sheet.py` (karşılaştırma tabloları), `reg_save_C.sh` (kayıt/yükleme + tek piyon). Kaydedici `Tools/Day_20261107/vid.py`: aday anahtarı (`VID_ABP`), aranan veritabanları, IK hedefleri, Story Framework etkileşim hedefi ve fareyle nişan segmenti eklendi (yedek `vid.py.bak_20261110b`).

## Gece devamı
Kontrol noktası `C:\Users\berat\SphirusCheckpoints\WomanMotion_Night_20261111_0906`. Kalıcı değişiklik yalnız `ABP_Sph_GASP` (`w13_mdr.py`). Denenip geri alınan: `w14_turnbias.py` (CM dönüş/kalkış veritabanlarında devam önceliği; `w14_restore.py` ile eski değerler geri yazıldı).
