# GD22 — Alt dudağın doğal formunun geri getirilmesi

Tarih: 2026-10-10. Sculpt GD19 G19'un doğal dudağından yeniden kuruldu; motor tabanı GD21 (GD21'e dokunulmadı).

Final aday **G22**. Durum: **PARTIAL**. Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED).

**Üretim karakterine uygulanmadı.** UE varlıkları `/Game/Sphirus/CharacterLab/GD22_IdentityMaster_20261010` altında, yalnız test amaçlı. Kaynaklar `SourceAssets/Characters/GD22_IdentityMaster_20261010` altında.

## 1. Hata ve nedeni

GD21'de alt dudak gaga gibi sivrilmiş, altında çentik ve önden yatay bir "çift dudak" kırışığı oluşmuştu (`process/01–02`). Orta hat profili (y, cm): GD19'da vermilyon 13,50 → alt kenar 13,18 → gövde 12,93 → oluk 12,28; GD21'de vermilyon 13,43 ama altındaki gövde 13,79 — yani **dolgu dudağın 2–3 mm önüne geçmişti** (GD20 L ve GD21 B alanları dudak alt kenarını geri çekerken gövdeyi öne itmişti).

## 2. Düzeltme

GD19'un doğal dudağından başlayıp tek bir tam-kalınlık profil alanı (`tools/gd22_profield.py`): alt dudak şekli bozulmadan rijit +1,5 mm, altındaki gövde ve oluk +3…+6 mm (dudak her zaman en önde kalacak biçimde), üst vermilyon +2 mm, filtrum +0,4 mm; infratip +1,3 mm (`ops/N20c.json`); ardından dudak altı kıvrımında hedefli konumsal yuvarlama (`tools/gd22_crease_smooth.py`, yalnız dış cilt, 8 × 0,5).

Sonuç orta hat (y, cm): 155,2: 13,65 → 155,0: 13,44 → 154,8: 13,33 → 154,6: 13,03 → 154,4: 12,82 → 154,0: 12,77 → 153,6: 12,53 — dudak önde, altı tek yönlü yumuşak eğim (`process/05–06`).

Adaylar: A (hafif dolgu: dudak doğal ama oluk GD19 kadar derin), B (hedef türevli alan: orta hat mükemmel ama iç mukozada 126 ters üçgen ve dalgalanma), C/C2 (y-ağırlıklı dış cilt: dolgu kayboldu), E (normal-ağırlıklı: dudak köşesi içinde katlanma), **F** (rijit dudak + yuvarlama: 0 ters üçgen) — seçildi.

Arka plan anahtarlı profil bantları (px; + = model önde):

| Bant | GD19 | GD21 | **GD22** |
|---|---|---|---|
| Alt dudak | +0,3 | +3,6 | +2,1 |
| Oluk / alt dudak gövdesi | −10,9 | −1,2 | −5,5 |
| Yastık üstü | −1,4 | −1,1 | −0,8 |
| Üst vermilyon | −1,4 | −0,9 | +0,5 |

Oluk GD21'e göre daha derin (dudak formu önceliklendirildi) ama GD19'un yarısı; alt dudak projeksiyonu doğal.

## 3. Teknik testler

| Test | Sonuç |
|---|---|
| Fit (2 rezidüel geri besleme) → sculpt | **PASS** (ortalama 0,038 mm, p95 0,20, p99 0,44, en fazla 1,16 mm) |
| Otomatik rig, DNA, 858 morph | **PASS** (otomatik rig ok, DNA, 858 morph) |
| Rig sonrası mesh ↔ sculpt | **PASS** (ortalama 0,038 mm, en fazla 1,16 mm; GD21 → GD22 rig sonrası ortalama 0,18 mm, en fazla 5,9 mm dudak altında) |
| Ters üçgen | **PASS** (0) |
| Keskin kıvrım | **PARTIAL** (sınırda olanlar önceki turlarla aynı; dış yüzeyde yeni yok) |
| Üçgen alan oranı min | 0,22 |
| Göz kapağı / göz küresi | **PASS** (değişmedi) |
| Kaş-kirpik bağlama, göz kırpma, RigLogic ifadeleri | **PASS** (19 RigLogic ifadesi × 2 görünüm; `F1`, `F2`) |
| LOD | **PARTIAL** (LOD0–3 yakalandı, `F3`; LOD4–7 NOT_TESTED) |
| PIE, animasyon, saç sim. | **NOT_TESTED** |
| Yeniden üretim | **PASS** (`tools/build_gd22.sh` G19S'ten G22S'i 0,000000 mm farkla üretir) |
| Üretim değişmedi | **PASS** (GD22 klasörleri dışında dosya değişmedi; qa_config geri yüklendi; editör kaydetmeden kapatıldı) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 4. Panolar

`O1–O3` teşhis (GD21 overlay'leri; profilde turuncu = gerçek silüet), `O4_*` sonuç overlay'leri (GD21 / GD22 gerçek ve kil), `O5`–`O6` burun ve çene yakın plan overlay'leri, `C2`–`C6` kil ve UE yakın planlar (C5 dudak), `D1`–`D4` tam yüz, `E` deformasyon GD21 → GD22, `F1`–`F3` rig/ifade/LOD.

## 5. Açık kalanlar

- Oluk referanstan ~4 mm derin (GD21'de 1 mm'ydi ama dudak bozuktu): dudak formunu bozmadan daha fazla dolgu bu topolojide dudak altı dikişinde katlanıyor; yerel yeniden örnekleme gerekir.
- Burun delikleri referanstan büyük (GD18'den beri).
