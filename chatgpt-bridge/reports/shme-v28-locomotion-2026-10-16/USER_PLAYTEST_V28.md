# SHME V2.8 — Oyun testi rehberi

Teknik ölçümler QA zemininde enjekte girişle yapıldı. His / kontrol kabulü senin oyun testine bağlı.
- V2.8 kayıtlı varsayılan: yeni yürüyüş duruşu açık, yeni başlangıç kapalı.
- Her madde için "doğal / hâlâ X / fazla Y" notu yeterli.

## 1. Yürüyüş duruşu (asıl değişiklik)
- **Nasıl:** W ile yürü, bırak. 10–15 kez, farklı anlarda bırak (adımın başında, ortasında, sonunda). Yandan ve arkadan bak.
- **Beklenen:**
  - Basan ayak yerinde kalıyor, geriye / öne kaymıyor.
  - Son adım kısa; arkadaki ayak bir kapanış adımıyla yanına geliyor.
  - Sonra ikinci bir "çökme" veya büyük kol / gövde salınımı yok.
  - Son fren adımında hafif diz bükümü normal.
- **Not et:**
  - "Kapanış adımı fazla çabuk / fazla yavaş."
  - "Bazı fazlarda ayak yine kayıyor" (hangi adımda bıraktığını yaz).
  - "Duruş fazla sert."

## 2. Duruştan hemen sonra
- **Nasıl:** dur, hemen tekrar W'ye bas. Bir de dur → 1 sn bekle → kısa bir dokunma (0.2 sn).
- **Beklenen:** V2.7 ile aynı ya da daha iyi; duruştan sonra ayaklar kendi kendine kaymıyor.

## 3. Yürüyüş başlangıcı ve kısa basmalar (değişmedi — kontrol)
- Başlangıç hâlâ V2.7'deki gibi. Yeni başlangıç adayı hazır, ama çok kısa basmalarda kötüleştirdiği için kapalı.
- **İstersen dene:**
  - `ABP_GR_MotionMatchingBase` sınıf varsayılanında `SHM28_StartMode = 1`.
  - Ölçülen fark:
    - Normal başlangıç ve yeniden kalkışta ayak kayması büyük ölçüde azalıyor, ilk adım daha küçük.
    - İlk görünür adım ~0.3 sn sonra (önce ağırlık aktarımı). Kapsül hızı aynı, yani kontrol gecikmesi eklenmedi.
    - Kısa basma / iptalde ayaklar daha fazla kayıyor.
  - Görüşün sıradaki işi belirler: başlangıç bu yönde mi gitsin, ilk adım daha erken mi gelsin?
- **Geri almak için:** `SHM28_StartMode = 0`.

## 4. Değişmemesi gerekenler (kısa regresyon)
- Tempolu ve deparda duruş, depar A/D kesişi, hızlı fare dönüşü, W↔W+D, geri dönüş.
  - Bu yollar V2.8'de değişmedi; V2.7'deki gibi olmalı.
  - Tempolu / depar duruşundaki çökme bilinen açık madde.

## Geri alma
- V2.8 duruşunu kapatmak için `ABP_GR_MotionMatchingBase` sınıf varsayılanında `SHM28_StopMode = 0`.
- Tam geri dönüş: `Saved/Codex/SHME_V28_20261015/checkpoint/baseline_v27/`.
