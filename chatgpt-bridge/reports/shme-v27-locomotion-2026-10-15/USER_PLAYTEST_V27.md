# SHME V2.7 — Oyun testi rehberi

Teknik ölçümler QA zemininde enjekte girişle yapıldı; his / görsel kabul senin oyun testine bağlı. V2.7 değerleri kayıtlı varsayılan.
Her madde için "doğal / hâlâ X / fazla Y" notu yeterli.

## 1. Yürüyüş başlangıcı
- **Nasıl:** Dur, 2 sn bekle, W ile yürü. Bir de durduktan hemen sonra tekrar yürü.
- **Beklenen:** ilk adımda gövde artık öne kapanmıyor (eğim ~21° → ~10°), baş öne fırlamıyor.
- **Not:** Beklerken karakter ağırlığını bir kalçasına veriyor; yürümeye başlarken ortaya gelmesi normal.

## 2. Yürüyüş
- **Nasıl:** 15–20 sn düz yürü, yandan ve arkadan bak.
- **Beklenen:** her iki adımda birebir aynı hareket artık yok. Kol salınımı adımdan adıma biraz değişiyor, gövde hafif oynuyor,
  arada baş hafifçe sağa / sola bakıyor; tekrar ~7 sn'de bir.
- **Not et:** "hâlâ tekrarlı" / "fazla oynak" / "baş bakışları tuhaf".

## 3. Duruşlar (yürüme, tempolu, depar)
- **Nasıl:** Her gait'te koş, bırak; birkaç kez, farklı adımlarda.
- **Beklenen:**
  - Yürüyüşte duruş sonundaki büyük sallanma ve çökme azaldı.
  - Tempolu ve deparda fren hamlesinin derinliği ~%25–30 azaldı; arka ayak frenlerken erken kalkıyor.
- **Not et:** tempolu / depar duruşundaki çökme hâlâ fazla mı? Fazlaysa sıradaki iş daha kısa son adımlı yeni bir koşu duruş animasyonu.

## 4. Hızlı dönüşler (tempolu ve depar)
- **Nasıl:** Depardayken A / D ile 90° kes; fareyi hızlı çevir; W+A ↔ W+D geç.
- **Beklenen:**
  - Depar animasyonu dönüşte tempoluya düşmüyor.
  - Hız eskisi kadar düşmüyor (90° kesmede ~2 m/s yerine ~3 m/s).
  - Gövde yeni yöne yolun biraz önünde dönüyor (hafif savrulma), sonra düz deparla devam.
  - Yalnızca 180° tam geri dönüşte durup yeniden hızlanıyor.
- **Not:** Artık A / D ile yana doğru depar atılabiliyor (karakter o yöne dönüp koşuyor). İstenmezse eski kural geri açılır.

## Geri alma
- **`DA_GR_LocomotionBehavior`:** `TurnSpeedLoss` 0.6, `TurnSpeedLossMin` 0.5, `SprintSideRunDot` 0.4226.
- **`ABP_GR_MotionMatchingBase` → Class Defaults:** `SHM_SprintDBMinSpeed` 380, `SHM_SprintDBDirMin` −65, `SHM_SprintDBDirMax` 65.
- **Klipler:** `Saved/Codex/SHME_V27_20261015/checkpoint/` (editör kapalıyken geri kopyala).
