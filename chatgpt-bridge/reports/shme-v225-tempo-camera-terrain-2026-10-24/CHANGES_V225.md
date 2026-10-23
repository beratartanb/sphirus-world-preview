# SPHIRUS V2.25 — değişiklik listesi

Taban: V2.24 üretimi. Motor UE 5.8, yalnız Blueprint. Kontrol noktası: `Saved/Codex/SHME_V225_20261023/checkpoint/pre_v225/` (ikili varlıklar) ve `checkpoint/tools/` (DSL kaynakları, harness).

## Üretimde (kaydedildi, temiz yeniden açılışta `verify_prod225` ALL_OK)

| Değişiklik | Sahibi | Anahtar / kaynak | Geri alma |
|---|---|---|---|
| Durup inceleme kamerası + sınırlı baş/boyun/gövde bakışı | SHME `SHM_UpdateCameraV21` + ABP AnimGraph (3 × Look At) | `DA_SHM_Response_Default.CamInspectEnabled = true`; ayarlar `Inspect*` (MaxDist 450, Radius 22, DwellOn 0.35, MaxSpeed 60, Share 0.35, Boom 0.94, TauOn 0.35, TauOff 0.6, LookMaxYaw 75, Key1..4 "INS_/Mask/Door/Lamp") | `CamInspectEnabled = false` (bakış alfası 0 → Look At düğümleri kimlik) |
| İnceleme bırakma düzeltmesi (I2) | SHME DSL | bekleme sayacı `InspectDwellOn + 0.15` ile sınırlı; `InspectMaxSpeed` 170 → 60 | `v225_patch_inspect2.py` öncesi kaynak (kontrol noktası) |
| Yükselen zemin kaldırma kapısı: ayağın KENDİ zemini (T1) | SHME `SHM_UpdateBodyTargets` | iz: ayak altı + yol üzerinde 0.5/1.0/1.5× ileri; kapı `gL − guL` | V2.24 kaynağı (kontrol noktası) |
| Basılı ayağa kaldırma yok (T1b, titreme düzeltmesi) | SHME `SHM_UpdateBodyTargets` | `SwingAirTL/R`: kaldırma ancak ayak ≥ 0.10 s temassızsa | kontrol noktası kaynağı |
| Warping alfa çarpanları (davranış aynı) | ABP `AnimationBlendStackGraph_0` | `SHM225_SWAlpha`, `SHM225_OWAlpha` = 1.0 (mevcut alfa kaynakları × değişken) | değişkenler 1.0 kaldıkça etkisiz |
| Ölçüm araçları | `Tools/SHME_V225_20261023/` | `plant225.py` (yeni), `ter225.py` catch düzeltmesi, `ins225.py` | — |
| QA harness | `qa_pie.py` | `INS_*` kutularına etiket (`set_actor_label`); `pie_window` (yüzen PIE penceresi, tam kare çekim) | kontrol noktası |

## Üretimde DEĞİL (aday, kanıt ve nedenleriyle)

| Aday | Durum | Neden |
|---|---|---|
| Yazılı jog fren–destek–itiş klipleri `SHM225_JogRev_{B_F,F_B}_P0..7` + `PSD_SHM225_JogRevBwd/Fwd` | Üretime alınmadı | 20/30 FPS'te ortalama en kötü basılı ayak kayması 26.1 → 17.5 cm (13 senaryo); 60/120 FPS'te eşit ya da daha kötü (ör. 120 FPS ovl 35.2 → 39.1 cm). Kare hızına bağlı; sağlam değil. |
| Planlı adım hazırlığı (T2 / T2b / T2c, `StepPrepEnabled`) | Kapalı | V2.24'te leğen basamakta zaten sürekli; T2c, FootPlacement ile çift düzeltme yapıp basamak çıkışında leğeni 8 cm çökertti (pelvis 90 → 82). |
