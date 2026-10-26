# SHME V2.31 — değişiklik listesi (2026-10-26)

Taban V2.30 (`37c3962`). Geri alma: editör kapalıyken `Saved/Codex/SHME_V231_20261026/checkpoint/pre_v231/` (README; 101 varlık + araçlar); düğmeler için `promote231.py {'rollback': True}`.

## Üretime alınan (düğme grupları, `promote231.py`)

| Grup | Sahip | Değişiklik | Üretim değeri |
|---|---|---|---|
| `slow` | ABP EventGraph JR seçimi (`install_v231_slowroute.py` + `_b.py`) + yeni içerik | Epizot 90 cm/s altında başlamışsa (epizot yokken o anki hız, varken başlangıçta mandallanan hız) yazılmış geri dönüş araması **düşük hızlı aileye** gider: `PSD_SHM231S_SlowRevBwd/Fwd` (16 + 16 faz klibi `SHM231S_SlowRev_*`: yürüyüş giriş döngüsü, destek ayağı yerinde frenler ve iter, salınım ayağı yeni yöndeki ilk adım) | `SHM231_SlowOn` 1, `SHM231_SlowV` 90 |
| `exit` | ABP EventGraph V2.14 itiş penceresi (`install_v231_exitpush.py` + `_b` + `fix_..._c`) | Yazılmış klipten depar çıkışı V2.14 `PSD_SHM214_RevPush` (satıcı pivotu sonrası itiş duruşu) yerine tempolu→depar itişine (`PSD_SHM218_JogPush`, J2S) gider | `SHM231_ExitAuth` 1 |
| `fwdrev` | Bileşen `SHM_UpdateRouting` (DSL) + DA alanı | Düşük hız geri dönüş sınıfı, tempolu kip isteğinde (`MaxSpeedNow` < 330) **ileri giderken** de açılır: frende bırak–yeniden basta epizot + klip-bağlı kapsül + tutuş | `RedirectLowRevFwdMax` 330 |
| `inspect` | Bileşen `SHM_UpdateCameraV21` (DSL) + yeni `SHM231_InspectResolve` (IsValid dallı yürütme grafı, `SHM_Tick`'te kamera fonksiyonundan hemen sonra) | Hedef kimliği: `GR_Inspect` etiketi (bileşen veya aktör), nesne yolu eşitliği; odak: maskenin kendi mesh sınırlarının merkezi (sorgu küresi değil); hiçbir üye çağrısı boş nesneye gitmez | `InspectFocusMode` 2 |
| `steplift` | Bileşen `SHM_UpdateBodyTargets` (DSL) + DA alanı | Kapsülün basamak yükselişi (CMC step-up) salınım kaldırmasından o karedeki yükseliş kadar düşülür | `SwingLiftBaseComp` 1 |
| `tipend` | ABP `Update_MotionMatching` girişi (`install_v231_tipend.py`) | Yerinde dönüş bitiş karesinde hız sıfırken MM bir kare TIP veritabanında kalır (satıcı depar-dönüş kuyruğu yok) | `SHM231_TipEndHold` 1 |
| `loaded` | ABP V2.30 yük rotası (`SHM230_LoadedOn`) + yeni içerik | Yük altında (`EffortEUse` ≥ 0,45) F_B dönüşü **yakalama adımlı** aileye gider: `PSD_SHM231L_LoadRevFwd` (29 faz klibi `SHM231L_LoadRev_F_B_*`: kısa fren ayağı → karşı ayak yakalama adımı → ilk geri adım → ölçülü itiş); B_F üretim ailesi | `SHM230_LoadedOn` 1 — üretimde (30 FPS ve gerçek zaman pencere kayması 0; 60 FPS e29_load 36.9→0; 120 FPS 29.4→19.7 kısmi; 20 FPS e29_load_4750 fazı 0→13.6 gerileme açık; 60 FPS e29_chain 14.3→26.1 gerileme açık) |

## İçerik (yerinde)

| Varlık | Değişiklik |
|---|---|
| `A_SHM_Sprint_Curve_L/R 12/25/40` | V1.3.9 eğri pişiricisiyle V2.30 depar döngüsünden (adım 0,82) yeniden pişirildi, `RATE` 1,0; varlık `rate_scale` 0,813 → 1,0 (üst gövde izleri — V2.30 salınım düzeltmesi — korunur) |

## Araç / otomasyon

| Dosya | Değişiklik |
|---|---|
| `qa_pie.py` | `cm.<prop>` aday anahtarları (CharacterMovement şablonu), `live_cm` / `live_anim` (yalnız PIE'de doğan piyon), pawn mesh tick ayarlarının günlüğü |
| `qa.sh` | PIE'ye başlamadan düşen qa_pie işi için hızlı çıkış (`QA_JOB_FAILED`; önce 900 s bekliyordu) |
| `lib231.sh`, `v231_ab.sh` | Çökme sonrası yeniden açılış kipi korur (`-UseFixedTimeStep -FPS=N`), `RELAUNCH_ARGS` kaydı, her koşuda `FPSCHECK` (sabit adım ≥ %98 kare) |
| `v212_run.sh` | `e31_s2_<ms>` senaryo ailesi (ikinci dönüş isteği zaman taraması: aynı fiziksel giriş) |
| `build_tick.py`, `shm_component_vars.py`, `shm_profiles.py`, `shm_src.py` | yukarıdaki DSL / değişken / DA alanı değişiklikleri |
| `ltp231.py`, `contact231.py`, `entry231.py`, `exits231.py`, `relphase231.py`, `step231.py`, `trans231.py`, `tables231.py`, `diverge231.py`, `slide231.py`, `fpscheck231.py` | ölçüm araçları |
| `retention231.py` | eski sürüm LTP / Evidence gzip (doğrulamalı, silme yok) |

## Kayıtlı, kapalı / etkisiz bulunan

| Aday | Sonuç |
|---|---|
| CMC perch (`PerchRadiusThreshold` 22, `PerchAdditionalHeight` 40; `live_cm`) | Basamak inişinde zamanlama değişmedi → WRONG_PATH |
| `live_anim always_tick` (belirlenimcilik) | Piyon meshleri zaten AlwaysTickPoseAndRefreshBones + URO kapalı → etkisiz |

## Değişmeyen (bilinçli)
V2.30 düşük hız sınıfı (`RedirectLowRevSpeed` 30), RevTurn ±180 düzeltmesi, klip-bağlı kapsül, IdleGuard, ResumeWin / PushCancel, V2.30 yeniden yazılmış klipler, yürüyüş kamerası, bellek/telemetri ve iş kuyruğu onarımları. Anatomi, iskelet oranları, yüz, kıyafet, harita değişmedi.
