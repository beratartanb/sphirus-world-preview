# Değişen varlıklar (2026-11-11, hareket geri alma)

Hepsi editör üzerinden, kapılı runner + yazma manifesti ve doğrulanmış yedekle (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/day_mr_*`). Tam geri dönüş noktası: `C:\Users\berat\SphirusCheckpoints\MotionRestore_Pre_20261111_1353`.

| Varlık | Değişiklik | Araç | Durum |
|---|---|---|---|
| `ABP_Sph_GASP` | `SphCM` True → False; MM PlayRate 0,80–1,05 → 0,85–1,15 (`MovementDirection_Recent` korunuyor) | `r1_profile.py` ('R') | üretim |
| `AC_Sph_Motion` (CDO + `BP_Sph_GASPCharacter` / `BP_HybridA_Player` şablonları) | fren 260/520 → 380/780; bekleme CM → Relaxed Idle_Break v01/02/03/05/07 | `r1_profile.py` | üretim |
| `BP_Sph_GASPCharacter` | `CalculateMaxAcceleration` 350/420/450→350 → 800/800/800→300; hız 160/290/500 → 165/375/585 | `r1_profile.py` | üretim |
| `BP_HybridA_Player` | hız 165/375/585; ev içi ölçek 0,9375 → 0,9091 (=150) | `r1_profile.py` | üretim |
| `BP_HybridA_Player` EventGraph | **sprint kilidi**: `GR_GaitSel=2` şartı `ShiftT>0,9 AND (hız>250 OR önceki GR_GaitSel==2)` | `g1_sprintlatch.py` | üretim |
| `AC_Sph_Motion` + `BP_Sph_GASPCharacter` (`CalculateBrakingDeceleration`, `CalculateGroundFriction`) | `RevOn` geri dönüş freni adayı (`Rev`, `RevLatch`, `RevDecel`, `RevFricMul`) | `m1_rev.py`, `m2_rev.py` | bayrak KAPALI (etkisiz), terfi etmedi |
| `AC_Sph_Motion` + `BP_Sph_GASPCharacter` (`CalculateMaxSpeed`) | `TurnCapOn` dönüş hızı sınırı adayı (`TurnW`, `TurnCap`) | `m3_turncap.py` | bayrak KAPALI (etkisiz), terfi etmedi |
| eski rapor README | başına REJECTED_REGRESSION notu | — | — |

Dokunulmayan: GASP/Relaxed vendor klipleri, veritabanları, seçim tabloları; Core Motion varlıkları (diskte, kullanılmıyor); `ABP_Sph_Body_GASP`, retarget, MetaHuman, kıyafet, saç, kamera bileşenleri, Story Framework, harita. Ham animasyon veya `.uasset` yayımlanmadı.

## Araçlar (`Tools/MotionRestore_20261111/`)
`r1_profile.py` (R/C profil anahtarı), `g1_sprintlatch.py`, `m1_rev.py`/`m2_rev.py`/`m3_turncap.py` (adaylar), `an_react.py` (beden tepki ölçüleri), `an_layers.py` (sürücü ve görünen), `an_clips.py` (klip dizisi), `an_contacts.py` (temas başına kayma + klip), `cmp_acr.py` (A/C/R tabloları), `q_turnroot.py` (dönüş kliplerinin kök eğrileri), `q_brakegraphs.py`/`q_gait.py`/`q_sprint.py` (sahip bulma, salt okuma), `q_final2.py` (temiz açılış denetimi), `vframes.py` (videodan kare), `pub_mr.py` (yayın).
