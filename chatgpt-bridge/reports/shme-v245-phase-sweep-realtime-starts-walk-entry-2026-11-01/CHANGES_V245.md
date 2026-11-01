# CHANGES V2.45 (2026-11-01)

## Üretim
| Asset | Değişiklik | Etki |
|---|---|---|
| `/Game/GraceRanger/SHME/Animations/V245/SHM245_Walk_Fwd` (YENİ proje klibi) | `A_LB_Walk_Fwd` kopyası + kalça çizgisi ×0,65, klavikula çizgisi ×0,55, bacaklar orijinal temaslara; BranchIn iz `SHME_V245_Walk` → `PSD_LB_WalkLoops`; `PoseSearchModifyCost` −1,0 tam pencere; loop true | düz yürüyüşte MM bu klibi seçiyor (186/186; gerçek zaman 211); karşı dönüş 23,0 → 19,6° |
| `/Game/GraceRanger/Animations/LocomotionBehavior/PSD_LB_WalkLoops` (proje DB) | BranchIn kaydı sonrası kaydedildi (içerik/şema değişmedi; 9. giriş) | manifest `v245_walk` yedeği var |
Değişmeyen: `PSD_SHM244_LatStop`, dönüş kuralları, idle anahtarları (kapalı), satıcı klipler (sha1 doğrulandı).

## İçerik / araçlar
| Ne | Dosya | Not |
|---|---|---|
| Kalça/klavikula-çizgisi tabanlı yürüyüş adayı üreteci | `Tools/SHME_V245_20261101/gen245_walk.py` | hip_scale 0,65 / chest_scale 0,55; bacaklar orijinal temaslara; `out` modu proje kopyası |
| Proje walk-DB girişi (satıcıya dokunmadan) | `build245_walkentry.py` | BranchIn iz `SHME_V245_Walk` + `PoseSearchModifyCost` −1,0 (tam pencere); rollback = iz kaldır + klibi sil + yeniden başlat |
| (hazır, kullanılmadı) proje walk-DB kopyası | `build245_walkdb.py` | 8 satıcı döngü kopyası + aday; chooser satırı Python'dan değiştirilemediği için beklemede |
| Senaryolar | `v212_run.sh`: `j45_rl_r0..5`, `j45_lr_r0..5` (yanal bırakma fazı taraması, `A_CT_Jog_*` 0,45–1,17 s pencereleri), `j45_sl` (duruştan sonra yanal istek) | |
| Analiz | `sweep245.py` | bırakma fazı, seçilen bin, duruş episodu, pop |
| Harness | `lib245.sh`, `vars245*.sh`, `media245.sh`, zincirler `run245_a..e.sh` | |

Satıcı asset değiştirilmedi. Manifestler: `v245_walk` (A_LB_Walk_Fwd + PSD_LB_WalkLoops yedek, SHM245_Walk_Fwd yeni).
