# GD21 — Çenedeki içe kıvrımın yumuşatılması (çene ucu ve dudak tarafından)

Tarih: 2026-10-10. Başlangıç ve geri dönüş noktası GD20 G20; GD20'ye dokunulmadı.

Final aday **G21**. Durum: **PARTIAL**. Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED).

**Üretim karakterine uygulanmadı.** UE varlıkları `/Game/Sphirus/CharacterLab/GD21_IdentityMaster_20261010` altında, yalnız test amaçlı. Kaynaklar `SourceAssets/Characters/GD21_IdentityMaster_20261010` altında.

## 1. İstek ve ölçüm

İstek: labiomental içe kıvrımın şiddetini hem çene ucu tarafından hem dudak tarafından düşürmek.

Kıvrımı oluşturan iki duvar, arka plan anahtarlı gerçek silüetle (profil, kalibre, px; + = model önde): dudak tarafı = alt dudağın alt kenar çıkıntısı (GD20'de +3,3), oluk tabanı (GD20'de −3,8), çene tarafı = yastık üstünün öne atlaması (GD20'de −0,6 ama oluğa göre 3 px'lik basamak). Kıvrım genliği GD19'da 14 px, GD20'de 7 px idi.

## 2. Müdahale

Tek bir dış-cilt profil alanı (`tools/gd21_profield.py`, y ≥ 12,6; dudak temas çizgisi ve iç mukoza sabit): yastık üstü −0,8 mm, oluk tabanı +2,3…+2,8 mm, alt dudak alt kenarı −1,3 mm; ardından dudak kenarı basamağında yer değiştirme relax'ı (`ops/R21.json`). İşaret değişimi 8 mm'ye yayıldığı için katlanma yok.

| Bant | GD19 | GD20 | **GD21** |
|---|---|---|---|
| Alt dudak | +0,3 | +3,3 | +3,6 |
| Oluk / alt dudak gövdesi | −10,9 | −3,8 | −1,2 |
| Yastık üstü | −1,4 | −0,6 | −1,1 |
| Yastık ortası | +1,0 | +0,6 | +0,6 |
| Üst vermilyon | −1,4 | −0,1 | −0,9 |

Kıvrım genliği (alt dudak → oluk → yastık, tepe-tepe): ~7 px → ~4,5 px. Adaylar: A (hafif: oluk −1,8) ve B (seçilen: oluk −1,2); B2 = B + relax (final). `process/01–03`.

Değişmeyenler: burun, çene uzunluğu (alt kenar satırı 764 rig sonrası ≈ referans 761), çene genişliği, yanaklar, gözler, kaş (bölge değişimleri `data/G21S_region_changes.json`).

## 3. Teknik testler

| Test | Sonuç |
|---|---|
| Fit (2 rezidüel geri besleme) → sculpt | **PASS** (ortalama 0,041 mm, p95 0,21, p99 0,49, en fazla 1,5 mm) |
| Otomatik rig, DNA, 858 morph | **PASS** (otomatik rig ok, DNA, 858 morph) |
| Rig sonrası mesh ↔ sculpt | **PASS** (ortalama 0,042 mm, en fazla 1,5 mm; GD20 → GD21 rig sonrası ortalama 0,09 mm, en fazla 2,8 mm) |
| Ters üçgen | **PASS** (0) |
| Keskin kıvrım | **PARTIAL** (sınırda olanlar GD17–GD20 ile aynı; dış yüzeyde yeni yok) |
| Üçgen alan oranı min | 0,26 |
| Göz kapağı / göz küresi | **PASS** (değişmedi) |
| Kaş-kirpik bağlama, göz kırpma, RigLogic ifadeleri | **PASS** (19 RigLogic ifadesi × 2 görünüm; `F1`, `F2`) |
| LOD | **PARTIAL** (LOD0–3 yakalandı, `F3`; LOD4–7 NOT_TESTED) |
| PIE, animasyon, saç sim. | **NOT_TESTED** |
| Yeniden üretim | **PASS** (`tools/build_gd21.sh` G20S'ten G21S'i 0,000000 mm farkla üretir) |
| Üretim değişmedi | **PASS** (GD21 klasörleri dışında dosya değişmedi; qa_config geri yüklendi; editör kaydetmeden kapatıldı) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 4. Panolar

`O1–O3` teşhis (GD20 overlay'leri; profilde turuncu = gerçek silüet), `O4_*` sonuç overlay'leri (GD20 / GD21 gerçek ve kil), `O5`–`O6` burun ve çene yakın plan overlay'leri, `C2`–`C6` kil ve UE yakın planlar, `D1`–`D4` tam yüz, `E` deformasyon GD20 → GD21, `F1`–`F3` rig/ifade/LOD.

## 5. Açık kalanlar

- Alt dudağın alt kenarı hâlâ hafif çıkıntılı (topoloji sınırı: 6 mm içinde işaret değişimi katlanıyor); kıvrımı tamamen düzleştirmek için dudak çevresinde yerel yeniden örnekleme gerekir.
- Burun delikleri referanstan büyük (GD18 raporundaki neden).
