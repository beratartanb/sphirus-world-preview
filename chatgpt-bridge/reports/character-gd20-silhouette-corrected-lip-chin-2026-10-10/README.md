# GD20 — Dış hat düzeltmesi: dudak–çene profili (uzman düzeltme turu)

Tarih: 2026-10-10. Başlangıç ve geri dönüş noktası GD19 G19; GD19'a dokunulmadı.

Final aday **G20**. Durum: **PARTIAL**. Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED).

**Üretim karakterine uygulanmadı.** UE varlıkları `/Game/Sphirus/CharacterLab/GD20_IdentityMaster_20261010` altında, yalnız test amaçlı. Kaynaklar `SourceAssets/Characters/GD20_IdentityMaster_20261010` altında.

## 1. Bulunan hata: ölçüm aracı dudaklarda ve olukta yanılıyordu

Senin "dış hat referansla eşleşsin" isteğini doğrulamak için profil silüetini iki yöntemle çıkardım:

- **Cilt-anahtarlı kontur** (GD13'ten beri kullanılan `contours_auto prof_front`): satır başına en soldaki *cilt sınıfındaki* piksel. Koyu vermilyon, ağız çizgisi ve gölgeli labiomental oluk cilt sınıfına girmediği için kontur bu satırlarda yüzün içine (5–15 px) atlıyor. `process/05` (sarı noktalar).
- **Arka plan anahtarlı silüet** (`tools/gd20_bgbands.py`): satır başına fondan farklı ilk piksel (≥ 6 px koşu), burun sırtı satırlarında kalibre edilmiş. Dudaklarda ve olukta doğru çalışıyor; profil overlay'lerinde turuncu çizgi.

Sonuç: cilt-anahtarlı kontur "model dudakları ve oluğu 3–11 px önde" diyordu; gerçek silüet tam tersini gösteriyor. **GD18'deki dudak geri alma (−3,2 / −2,2 mm) ve GD19'daki oluk derinleştirme (bant −3 mm, yastık üstü −3 mm) yanlış yöne gitmişti.** Bu raporda bunları düzelttim. GD19'un geçerli kalan kısımları: burun kaynaştırma, çene uzunluğu (ön görünümde referansla aynı satır), çene genişliği.

Kalibre edilmiş arka plan anahtarlı profil bantları (px; + = model önde; ~0,71 mm/px):

| Bant | GD17 | GD18 | GD19 | **GD20** |
|---|---|---|---|---|
| Infratip / kolumella | +1,6 | −1,9 | −1,4 | −0,5 |
| Üst dudak (filtrum) | +3,0 | −1,4 | −1,4 | +0,3 |
| Üst vermilyon | +3,0 | −1,4 | −1,4 | −0,1 |
| Alt dudak | +5,5 | +2,3 | +0,3 | +3,3 |
| Oluk / alt dudak gövdesi | −4,7 | −6,8 | −10,9 | −3,8 |
| Yastık üstü | +3,1 | +3,5 | −1,4 | −0,6 |
| Yastık ortası | +1,7 | +3,1 | +1,0 | +0,6 |

Alt dudak satırlarında ~+3 px kalıntı panelin dikey kaymasından (referansta ağız çizgisi 4 satır yukarıda) etkileniyor; özellik-özellik bakıldığında alt dudak projeksiyonu eşleşiyor.

## 2. Müdahale (tek, pürüzsüz alan)

Yığılmış yerel hareketler alt dudak altında dalgalanma ve iç mukoza katlanması üretti (adaylar A–H, hepsi elendi). Çözüm: `tools/gd20_profield.py` — z boyunca monoton kübik spline ile tanımlı tek bir ileri yer değiştirme alanı, yanal plato (±2,0 cm, 3,3'e yumuşak geçiş), dudak kalınlığının tamamı ve dişler birlikte (iç kayma yok).

1. **Alan I** (tam kalınlık): alt dudak gövdesi / oluk +4…+5 mm (z 154,0–154,4), üst vermilyon +2 mm, filtrum +0,4 mm.
2. **Infratip / kolumella** +1,3 mm öne (`ops/N20c.json`; GD18'in geri çekmesi aşırıydı).
3. **Alan L** (yalnız dış cilt, silüet-fit): oluk +2,8 mm tepe, alt dudak alt kenarı −0,8 mm. Kalıntılardan otomatik üretilen kontrol noktaları (`tools/gd20_silfit.py`), ters üçgen sıfırlanana kadar yumuşatıldı.

Denenen ve elenenler: burun deliği tabanını kaldırma (sill katlandı, 11 ters üçgen), kanat kenarı kalınlaştırma (ince kenar katlandı), alt dudak üst kenarını geri alma (dudak temas çizgisinde 29–74 ters üçgen), 7 mm tek dilim dolgu (yüzeyde raf/kırışık).

Burun: GD19'un kaynaştırılmış burnu korundu; burun delikleri GD17 boyutunda (kanat kenarını daha fazla sarkıtmak bu topolojide katlanıyor — açık madde).

## 3. Teknik testler

| Test | Sonuç |
|---|---|
| Fit (2 rezidüel geri besleme) → sculpt | **PASS** (ortalama 0,040 mm, p95 0,20, p99 0,47, en fazla 1,37 mm) |
| Otomatik rig, DNA, 858 morph | **PASS** (otomatik rig ok, DNA, 858 morph) |
| Rig sonrası mesh ↔ sculpt | **PASS** (ortalama 0,040 mm, en fazla 1,37 mm; GD19 → GD20 rig sonrası ortalama 0,34 mm, en fazla 7,7 mm oluk bölgesinde) |
| Ters üçgen | **PASS** (0) |
| Keskin kıvrım | **PARTIAL** (7 sınırda: GD17'den gelen doğal kenarlar + ağız içi mukozada 3 sınırda 125–138°; dış yüzeyde yeni yok) |
| Üçgen alan oranı min | 0,26 |
| Göz kapağı / göz küresi | **PASS** (değişmedi) |
| Kaş-kirpik bağlama, göz kırpma, RigLogic ifadeleri | **PASS** (19 RigLogic ifadesi × 2 görünüm; `F1`, `F2`) |
| LOD | **PARTIAL** (LOD0–3 yakalandı, `F3`; LOD4–7 NOT_TESTED) |
| PIE, animasyon, saç sim. | **NOT_TESTED** |
| Yeniden üretim | **PASS** (`tools/build_gd20.sh` G19S'ten G20S'i 0,000000 mm farkla üretir) |
| Üretim değişmedi | **PASS** (GD20 klasörleri dışında dosya değişmedi; qa_config geri yüklendi; editör kaydetmeden kapatıldı) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 4. Panolar

`O1–O3` teşhis (GD19 overlay'leri, profilde turuncu = gerçek silüet), `O4_*` sonuç overlay'leri (REF | aday | %50 | fark; GD19 / GD20 gerçek ve kil), `O5`–`O6` burun ve çene yakın plan overlay'leri, `A2` profil çizgileri (cilt-anahtarlı; dudak satırlarında güvenilmez — not düşüldü), `C2`–`C6` kil ve UE yakın planlar, `D1`–`D4` tam yüz, `E` deformasyon GD19 → GD20, `F1`–`F3` rig/ifade/LOD. `process/01–04` oluk satırlarının 6x zoom'u (REF | GD19 | adaylar), `process/05` kontur hatası, `process/06` burun 4x kil.

## 5. Açık kalanlar

- Oluk hâlâ ~2–3 mm geride, alt dudak alt kenarı ~2 mm önde: alt dudak alt kenarı ile gövdesi arasındaki işaret değişimi bu topolojide 6 mm içinde katlanıyor; daha fazlası için dudak çevresinde yerel yeniden örnekleme gerekir.
- Burun delikleri referanstan büyük (aynı neden).
- Burun ucu ~1,2 mm önde (GD18'den; kabul edilebilir).
