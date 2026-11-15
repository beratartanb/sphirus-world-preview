# Değişiklik manifesti — tam beden biyomekaniği, 1. tur (2026-11-15)

Tüm yazmalar kapılı çalıştırıcıdan (doğrulanmış yedek + tek kilit sahibi, PIE kapalıyken). Vendor kaynakları, yüz / beden
mesh'leri, saç, kıyafet, malzemeler, harita, `ABP_Sph_Body_GASP` ve `AC_Sph_Motion` değişmedi.

## Yazma 1 — manifest `day_bio_apply1_103307` (`Tools/Bio_20261115/b_apply1.py`)

| Varlık | Alan | Önce | Sonra |
|---|---|---|---|
| `/Game/Sphirus/Player/GASP/Rig/RTG_Sph_UEFN_to_MH` | Pelvis Motion → TranslationOffsetGlobal Z | 1.0 | 2.4 |
| `/Game/Sphirus/Player/GASP/ABP_Sph_GASP` | FootPlacement → LockType / UnplantAngle | PivotAroundBall / 60 | LockRotation / 35 (**yazma 2 ile geri alındı**) |
| `/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter` | CalculateMaxAcceleration, yürüme sabiti | 800 | 500 |
| `/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter` | CrouchSpeeds | (225, 200, 180) | (165, 150, 140) |
| `/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player` | CrouchSpeeds (üst sınıftan geliyor) | (225, 200, 180) | (165, 150, 140) |

Not: derleme sırasında `BP_Sph_GASP_B` bellekte kirlendi (manifest dışı); kaydedilmedi, editör yeniden başlatılınca atıldı.

## Yazma 2 — manifest `day_bio_revert2_111014` (`Tools/Bio_20261115/b_revert2.py`)

`ABP_Sph_GASP` FootPlacement: LockRotation / 35 → PivotAroundBall / 60 (ölçülebilir etkisi olmadığı için eski değer).

## Son durum (SHA1 ilk 12)

| Varlık | Bu işten önce | Şimdi |
|---|---|---|
| RTG_Sph_UEFN_to_MH | 0e79f980d424 | 98c21e995aff |
| ABP_Sph_GASP | 6f5d95659743 | e3e593a08428 (değerler eski; yeniden kaydedildi) |
| BP_Sph_GASPCharacter | 3d7dc17661f1 | 09fe0bdd07f1 |
| BP_HybridA_Player | aafc4cef872b | add514416170 |

## Geri alma

- Editör kapalıyken manifest yedeklerini ya da `%USERPROFILE%\SphirusCheckpoints\Bio_Pre_20261115\` kopyalarını geri koyun.
- Değer düzeyinde: pelvis ofseti 1.0; yürüme ivmesi 800; CrouchSpeeds (225, 200, 180).

## Test araçları (oyuna girmez)

`Tools/Bio_20261115/`: an_bio.py, an_events.py, an_leg.py, q_prop.py, q_rtg.py, q_owners.py, q_crclips.py, pp_probe.py,
probe_drv.py, probe_crouch.py, bio1–bio3.sh, chain1–3.sh. Çıktılar `Saved/Codex/Bio_20261115/`.
