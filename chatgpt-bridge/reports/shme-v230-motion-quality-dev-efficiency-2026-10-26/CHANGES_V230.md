# SHME V2.30 — değişiklik listesi (2026-10-26)

Taban V2.29 (`f971e94`). Geri alma: editör kapalıyken `Saved/Codex/SHME_V230_20261026/checkpoint/pre_v230/` (README) ve `checkpoint/pre_reauthor/`; bayraklar için `promote230.py {'rollback': True}`.

## Üretime alınan

| Alan | Değişiklik | Varsayılan / üretim değeri |
|---|---|---|
| Bileşen `SHM_UpdateRouting` (DSL `shm_src.py`) | Düşük hızlı geri dönüş sınıfı `lowRev`: geri koşu (hız ile bakış ters, dot < −0,7) + istenen yürüyüş tempolu/depar (`MaxSpeedNow` > `RedirectLowRevPeak`) + dönüş açısı sınıf açısının üstünde → epizot alt sınırı `min(RedirectLowRevSpeed, RedirectEpisodeMinSpeed)`, sınıf `SpeedOnset` koşulu olmadan açılır | `RedirectLowRevSpeed` 0 (DA'da **30**), `RedirectLowRevPeak` 145 |
| `shm_profiles.py` / DA_SHM | yeni alanlar `RedirectLowRevSpeed`, `RedirectLowRevPeak` | 30 / 145 |
| ABP `SHM213_MontTick` | EarlyRev alt hız sınırı: `SHM230_EarlyRevMin` (150 yerine) yalnız `MaxSpeedNow` > `SHM230_EarlyRevPeak` iken (yürüyüş hiç girmez) | `SHM230_EarlyRevMin` **30**, `SHM230_EarlyRevPeak` 145 |
| Bileşen `SHM_UpdateCameraV21` (inceleme sondası) | `ActorHasTag` / `ComponentHasTag` / `GetActorBounds` (boş aktörde her kare "Accessed None") yerine bileşen adı anahtarı (`INS_`, `Mask`) + `GetComponentBounds`; davranış aynı | `InspectKey1` "INS_", `InspectKey2` "Mask" |
| Animasyon içeriği (yerinde, 22 klip) | aynı kadansta adım ölçekleme + yanal salınım zayıflatma + bacak yeniden çözümü: `A_LB_Sprint_Fwd` (adım 0,82; pelvis 0,6 / göğüs 0,5 / baş 0,45 / kol 0,75), `A_SHM_Sprint_Curve_L/R 12/25/40` (adım 1,0; aynı salınım), `SHM217_J2S_*` (0,92/0,92/1,0/0,92), `SHM218_W2S_*` (1,0), `A_CT_Walk_Rear/RearLeft/RearRight` (0,74/0,72/0,72; 0,8/0,8/0,7/0,85), `A_CT_Jog_Right` 0,82, `A_CT_Jog_Left` 1,0 | — |
| ABP `SHM_Snapshot` (`install_v230_idleguard.py`) | `idleNow` → `idleNow AND NOT(SHM230_IdleGuard AND SHM227_Hold AND (SHM228_Brake OR PostT < SHM229_ResumeWin))` (IdleEntry ve IdlePrev birlikte) | `SHM230_IdleGuard` **1** |
| `qa_pie.py` / `evidence.py` | LTP telemetri satırları editör günlüğü yerine `Saved/Codex/SHME_V1_20260925/LTP/<etiket>.ltp` (kanıt önce onu okur); ekranı büyütülmüş pencere düzeltmesi korunuyor | — |
| `v212_run.sh` senaryo ailesi `j30_rel_<ms>` | bırakma anı taraması | — |
| `run.sh` (SHME iş kuyruğu) | iş dosyası geçici adla yazılıp yeniden adlandırılıyor (yarım yazılmış işin çalışması yarışı) | — |
| `editor_launch230.sh` | ZenServer bekçisi (önceki zen kapanana kadar ≤ 20 s bekle; "Waiting for ZenServer" 90 s ilerlemezse erken bırak, sınırlı yeniden deneme) | — |
| `lib230.sh` | RUNNER_NOT_READY nedeni kaydı + en çok 2 yeniden deneme | — |
| `v212_run.sh` | yeni senaryolar: `s29_camh`, `s29_camh2`, `s29_camh3` (gerçek duraklamalar), `w30_rev`, `w30_postsprint`, `j30_slow`, `c30_calm` | — |

## Kayıtlı, varsayılan kapalı (kapalı aday)

| Aday | Ne yapıyor | Neden üretimde değil |
|---|---|---|
| `SHM230_FamGate` (ABP) | yazılmış klip tutulurken toparlanma ailesine geçişi kapatır | j24_dbl'deki seçim eşitliğini kanıtlanabilir biçimde çözmedi (oturuma bağlı) |
| `SHM230_LoadedOn` + `PSD_SHM230L_JogRevBwd/Fwd` (53 klip) | yük altında (EffortEUse ≥ 0,45) ayrı geri dönüş ailesi | yükte seçildi, görünür fayda ölçülemedi, giriş boşluğu açtı |
| StepPrep (`StepPrepEnabled`, sp1/sp2) | basamak öncesi adım hazırlığı | 28 cm basamakta havada kalma 0,43/0,50 s → 0,37–0,53 s, pop'lar aynı: etkisiz |
| `lr70` (taban 70) | düşük hız sınıfını ≥ 70 cm/s ile sınırlar | s29_swl12'de yalnız V2.29 yolunu geri getirdi (pop 109–111, kayma 33,6–68,6) |

## Değişmeyen (bilinçli)
Yürüyüş kadrajı (230 / 3 / 4), efor (V2.29 değerleri), RevTurn içerik düzeltmesi, PushCancel, ResumeWin 0,2, inceleme maskeleri, kamera. Anatomi, iskelet oranları, yüz, kıyafet, harita değişmedi.
