# V2.21 değişiklik özeti (kod / graf / araç)

Tüm ikili varlık değişiklikleri editör üzerinden yapıldı. Değişiklik öncesi kopyalar `Saved/Codex/SHME_V221_20261021/checkpoint/` altında:
- `baseline_v220/`: V2.20 üretim varlıkları.
- `pre_promo/`: terfi öncesi durum.
- `tools_v1/*.v221a`: DSL kaynakları.

## Üretimde olanlar

### ABP_GR_MotionMatchingBase
- **`SHM213_MontTick` hata akışı.** `fix_v221_lasthitby.py` uygulandı. DSL çevirisinin ürettiği `LastHitBy` okuması `Pawn.GetController` ile değiştirildi. MontTick DSL'den yeniden kurulursa bu düzeltme tekrar uygulanmalı.
- **Toparlama tutma: `SearchThrottleTime`.** `install_v221_recthrottle.py` ile AnimGraph'taki MM düğümünün `SearchThrottleTime` girişi `FMax(eski, Select(NOT SHM220_Search, SHM221_RecThrottle, 0))` oldu. Yeni değişken `SHM221_RecThrottle` (1.0).
- **Toparlama çıkış koruması.** `install_v221_recexit.py` ile `Set SHM220_Search` girişi `OR(önceki, NOT SHM217_RecOn)` oldu.
- **Kesiş → S pivot tutma.** `install_v221_pivothold.py` kuruldu: `SHM221_PivHold` / `PivHoldT` / `PivSub` / `PivWin`. Düğme **0 (kapalı)**.
- **Terfi.** `SHM220_RecHold` 0 → **1**.

### BP_GR_Player / BP_PBI_Player / BP_GR_MotionProfile
- **Küçük adım.** `install_v221_tapstep.py` ile `GR_Impl_CP_PhysicalRedirect` içine eklendi: `GR221_*` değişkenleri ve profil düğmeleri. `GR221_TapStepCm` **0 (kapalı)**, aday reddedildi.
- **Kendi yol açtığım gerileme ve onarımı.** Profil sınıfı yeniden derlenince `BP_PBI_Player.GR_Profile` açık bir `None` geçersiz kılmasına düştü. Kaydedildiğinde tüm girdi kesildi. `req/fix_profile_ref.py` ile onarıldı. `verify_prod221.py` artık bunu denetliyor.

### BP_SHM_HumanMotionComponent (DSL → graf)
Değişen fonksiyonlar `SHM_UpdateBodyTargets` ve `SHM_UpdateCameraV21`. `SHM_UpdateRouting` yeniden kurulmadı. Fark dosyaları:
- `diff_shm_src.py.txt`
- `diff_shm_profiles.py.txt`
- `diff_shm_component_vars.py.txt`

**Duruş yerleşmesi**
- Bayrak: `SettleBodyEnabled`.
- Bir hareket bölümü bittiğinde gövdeye tek bir öne-sonra-hafif-geri darbe: exp(−t/τ)·cos(2πt/T). İleri bölümünde diz verir.
- Genlik giriş hızına göre ölçeklenir (SpeedPeak/300). Yeni girdi geldiğinde 0.08 s'de söner.

**Arazi bedeni**
- Bayrak: `TerrainBodyEnabled`.
- Gerçek çarpışmaya üç Visibility çizgi izi: kapsül altı, hızla orantılı ileri nokta ve 30 cm sağ.
- Bunlardan eğim, yan eğim ve ani zemin düşmesi hesaplanır ve gövdeye yansır:
  - süzülmüş eğim → `LeanFwdTarget`;
  - yan eğim → `LeanLatTarget`, yokuş yukarı tarafa;
  - iniş eğimi → diz düşüşü;
  - ani düşme → pelvis karşılaması.
- Eğim tepkisi yürüyüş hızıyla açılır (20 → 80 cm/s).

**Yaşayan kamera**
- Bayrak: `CamV221Enabled`.
- Doğrulanmış topuk temasına bağlı analitik adım darbesi. Tetik `CamStepFire` ile bir kez kilitlenir; çift tetik koruması var.
- Hızla büyüyen ileri bakış, yalnız pivot ofsetinde.
- Hız FOV'u kodda duruyor ama 0'da, çünkü mevcut sistem zaten hızla FOV veriyor.
- `CamComfortScale` konfor ölçeği ve ışınlanmada süzgeçlerin sıfırlanması.

**DSL yazım kuralı.** Her `set`, bağlı saf ifadeleri yeniden değerlendirir. Bu yüzden bellekler en sonda yazıldı ve tek seferlik tetikler değişkene kilitlendi.

### Terfi edilen değerler (DA_SHM_Response_Default)
- `SettleBodyEnabled` 1, `SettleBodyDeg` 6, `SettleBodyDipCm` 2, `SettleBodyMinSpeed` 60.
- `TerrainBodyEnabled` 1, `TerrainLeanUpGain` 0.15, `TerrainLeanUpMax` 2.5, `TerrainLeanDownGain` 0.1, `TerrainLeanDownMax` 1.2.
- `CamV221Enabled` 1, `CamFOVSpeedMax` 0, `CamStepGain` yürüyüş / tempo / depar 0.35 / 0.6 / 0.9 cm, `CamComfortScale` 1.

## Araçlar (Tools/SHME_V221_20261021/)

**Ölçüm**
- `contact221.py`: kalibrasyonu yalnız pencereden önceki satırlardan yapar.
- `cmp221.py`: varyant karşılaştırması.
- `rewind221.py`: klip zamanı geri sarmaları.
- `terrain221.py`, `terseg221.py`: segment başına gövde eğimi ve eğim sinyali.
- `settle221.py`: duruş yerleşmesi.
- `smallstep221.py`: dokunuş adımları.
- `cam221.py`: FOV pompalama, kamera sıçrama ve sarsıntısı, yuvarlanma, çerçeve açısı, kamera adımları.
- `camcol221.py`: koridorda duvara girme.

**Kurulum ve doğrulama**
- `install_v221_*`, `fix_v221_lasthitby.py`.
- `promote221.py`: SHME DA dahil.
- `verify_prod221.py`.
- `v221_patch.py`, `v221_build.sh`, `only_v221.py`.

**Harness (Tools/SHME_V212_20261017/v212_run.sh, atomik düzenleme)**
- `mvb()`: kutu argümanını taşıyan yardımcı. Eski `mv()` ikinci argümanı düşürüyordu.
- Senaryolar:
  - `ter_*` arazi parkurları;
  - `ss_*` dokunuşlar;
  - `pilot` rotası;
  - `map_r1..3`: gerçek harita çizgileri, `req/probe_route.py` ile bulundu;
  - `cam_corr`: kamera çarpışma koridoru.
- `cvars` listesine V2.21 sinyalleri eklendi.
