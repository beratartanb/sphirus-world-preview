# GD30 — Burun tabanı: referansla doğrulamalı eşleştirme ve form yumuşatma

Tarih: 2026-10-11. Başlangıç ve geri dönüş noktası GD28 G28; GD28'e dokunulmadı.

Final aday **G30W** (sculpt adı W4). Durum: **PARTIAL**. Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED).

**Üretim karakterine uygulanmadı.** UE varlıkları `/Game/Sphirus/CharacterLab/GD30_IdentityMaster_20261011` altında, yalnız test amaçlı. Kaynaklar `SourceAssets/Characters/GD30_IdentityMaster_20261011` altında.

**GD29 reddedildi ve yayınlanmadı.** Kanat lobülünü her yönde şişirmek yapıyı bozdu (`process/05`). Bu tur GD28'den yeniden başladı.

## 1. İsteklerin

1. "Burun yapısı orijinale göre bozulmuş; önceki haline getirip referans üzerinden doğrulama ile benzet" (`process/00a`, `00b`).
2. "Burun ucu düşüklüğü ve deliğin üst kıvrımı tutarsız" (`process/00c`).
3. "Kıvrım, delik şekli ve burun ucu konumu hâlâ yanlış; uç düşük."
4. "Referansın geçişleri ve formu bizimkine uymuyor; kemik formu çok yanlış. Kırmızıyla çizdiğim ortalama formu daha yumuşak ve gerçekçi yap" (`process/00d`).

## 2. Doğrulama yöntemi (yeni)

Tahmine dayalı sculpt yerine her değişikliği referansla aynı kamerada ölçtüm:

- **Çizgi karşılaştırması** (`tools/gd30_valcmp.py`). Aynı koyu çizgi (oluk) dedektörü hem referans fotoğrafta hem modelin görüntüsünde çalışıyor. Referans kırmızı, model camgöbeği çiziliyor. Ölçüm hatları lobül altını, oluğu ve deliği milimetre olarak ölçüyor. Profilde panelin ölçek farkı uç ve subnazale hizalamasıyla kaldırılıyor (`process/01–04`).
- **Delik ağzı karşılaştırması** (`tools/gd30_cavity.py`, `tools/gd30_realopen.py`). Modelin her kamerada gerçekten görünen delik içi, referansın koyu delik ağzıyla örtüşmesine (IoU) göre ölçülüyor. Aynı bölütleme gerçek UE çekimine de uygulanıyor; bu fotoğrafla birebir karşılaştırma demek.
- **Form sertliği** (`gd30_relief.py`). Kanat bölgesindeki ince kabartı, yani keskin sırt ve köşeler ölçülüyor.

## 3. Teşhis (GD28)

- Lobül altı tüm görünümlerde referanstan 1–2 mm yukarıdaydı.
- Profilde referansın lobülü yuvarlak bir halka. GD28'de oluk deliğin arkasından çapraz kesiyordu; oluk ortası 4,5 mm öndeydi.
- Önden ve iki 3/4 kamera neredeyse yatay; üçü de kolumella tabanını ve uç altını referanstan 1–3 mm aşağıda gösterdi. Uç ve subnazaleye göre ölçen profil bunu görmüyordu.
- Referansta delik ağzı 3/4'te uzun, yüksek ve yaklaşık iki kat büyük. GD28'in gerçek görüntüsünde en koyu bölge delik değil, kanat oluğu ve kolumella gölgesiydi.
- U adayında lobülün yan-alt yüzünde ve arka kenarında yeni keskin sırtlar oluştu (rölyef en fazla 0,72 mm). Profilde gördüğün "Y" birleşimi ve dik arka kenar buradan geliyordu.

## 4. Müdahale (`tools/build_gd30.sh`, G28S'ten, 0,000000 mm farkla yeniden üretilir)

1. Lobül altını çan biçimli bir alanla indirme (önden lobül altları referansa).
2. Lobülün arka yüzünü geriye-yana itme, oluk dolgusu ve birleşim gevşetme.
3. Burnun alt bölümünü 2 mm kaldırma (uç lobülü, kolumella, subnazale).
4. Uç lobülünü 2 mm daha kaldırma ve delik kenarını kaldırma (ağız yukarı ve uzun).
5. **Form yumuşatma** (son isteğin): lobül sırtları, deliğin önündeki tepe ve "Y" birleşimi, lobülün arka kenarı konumsal olarak yumuşatıldı. Kenar kaldırması tek, geniş bir yaya çevrildi.

Adaylar: G (lobül), K (+ alt burun), U (+ uç ve delik), **W4 (+ yumuşatma, final)**. Elenenler `data/nose_base_measures.json` içinde.

## 5. Sonuçlar

Gerçek UE görüntüsünde delik ağzı örtüşmesi. Referans fotoğrafla aynı koyu bölge bölütlemesi kullanıldı, 1 = tam örtüşme (`process/35`, `data/real_opening_iou.txt`):

| Görünüm | GD28 | U | **W4** |
|---|---|---|---|
| 3/4 sol | 0,10 | 0,44 | **0,40** |
| 3/4 sağ | 0,25 | 0,36 | **0,35** |
| Önden (sol delik) | 0,00 | 0,14 | **0,15** |

GD28'in önden görüntüsünde en koyu bölge delik değil, kolumella gölgesiydi. Yani delik önden hiç görünmüyordu. W4'te delikler önden ve 3/4'ten açık görünüyor (`process/34`).

| Ölçü | GD28 | **W4** | Referans |
|---|---|---|---|
| Kanat rölyefi, rig sonrası (ortalama / en fazla, mm) | 0,028 / 0,33 | **0,032 / 0,30** | — |
| Kanat rölyefi, U'da (yumuşatma öncesi) | — | 0,045 / 0,72 | — |
| Uç yüksekliği, subnazaleye göre (+ = aşağıda) | −0,13 mm | **−1,98 mm** | 0 |
| Uç–subnazale kord açısı | 40,4° | **36,5°** | 40,5° |
| Uç–subnazale sarkma (en fazla) | 0,117 | **0,101** | 0,125 |
| Profil oluk ortası (uç+sn hizalı) | −4,5 mm | **−2,8 mm** | 0 |
| 3/4 uç altı (sol / sağ, + = aşağıda) | +2,8 / +0,9 mm | **+1,9 / +0,8 mm** | 0 |

Uç, son üç geri bildirimine göre bilinçli olarak profilde referansın yaklaşık 2 mm üstüne alındı. Profil silüeti tek başına ucu yerinde gösteriyordu.

## 6. Teknik testler

| Test | Sonuç |
|---|---|
| Fit (2 rezidüel geri besleme) → sculpt | **PASS** (ortalama 0,045 mm, p95 0,22, p99 0,61, en fazla 1,60 mm) |
| Otomatik rig, DNA, 858 morph | **PASS** (`MHC_GD30_G30W`, `SKM_GD30_Face_g30w`) |
| Rig sonrası mesh ↔ sculpt | **PASS** (ortalama 0,045 mm, en fazla 1,60 mm; GD28 → GD30 rig sonrası ortalama 0,10 mm, en fazla 3,6 mm uç altında, yani uç kaldırma) |
| Ters üçgen (sculpt ve rig sonrası) | **PASS** (0 / 0) |
| Keskin kıvrım | **PARTIAL** (43; E'ye göre 10 sınırda; GD28'de 42 / 9) |
| Üçgen alan oranı min / max | 0,216 / 3,86 (GD28 0,185 / 4,22) |
| Çene alt kenarı satırı (ön, rig sonrası) | **PASS** (763; GD28 763, referans 761, çene uzamadı) |
| Kaş-kirpik bağlama, göz kırpma, RigLogic ifadeleri | **PASS** (`F1`, `F2`) |
| LOD | **PARTIAL** (LOD0–3, `F3`; LOD4–7 NOT_TESTED) |
| PIE, animasyon, saç sim. | **NOT_TESTED** |
| Yeniden üretim | **PASS** (`tools/build_gd30.sh` G28S'ten G30S'i 0,000000 mm farkla üretir) |
| Üretim değişmedi | **PASS** (Content / SourceAssets / Config / Plugins temiz; GD29/GD30 dışında yalnız lookdev kayıtları değişti, `data/outside_change_scan.txt`; qa_config geri yüklendi; editör kaydetmeden kapatıldı) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

Ara adaylar G ve K'nın zincirleri yarıda durduruldu (bekleyen işler karantinaya alındı). Varlıkları GD30 CharacterLab klasöründe test kaydı olarak duruyor.

## 7. Panolar

- `process/34`, `process/35`: gerçek UE karşılaştırması (REF | GD28 | W4) ve gerçek delik ağzı örtüşmesi (REF | GD28 | U | W4). `process/29`: U'nun gerçek görüntüsü.
- `process/31`, `process/32`: W4 yumuşatma; yan ışıkta kil ve profil çizgi haritası (U üstte, W4 altta).
- `C4`: burun yakın plan, gerçek ve kil (GD28 | GD30).
- `H1`: profil şekil analizi.
- `O1–O3`: GD28 teşhis overlay'leri. `O4–O6`: sonuç overlay'leri.
- `G1`: adaylar (GD28 / G / W4).
- `D`, `E`, `F`: tam yüz, deformasyon, rig/ifade/LOD.

## 8. Açık kalanlar

- **Profil:** Uç artık referansın yaklaşık 2 mm üstünde. Uç–subnazale çizgisi referanstan biraz daha düz ve kalkık (kord 36,5° / 40,5°). Profil fazla kalkık görünürse 4. adımdaki 2 mm'lik uç kaldırma yarıya indirilebilir.
- **Delik ağzı:** 3/4 açılarda referansın ağzı hâlâ daha büyük (alan 86/109 px², W4'te 43/56).
- **Yumuşatmanın bedeli:** Profilde oluk ortası yeniden öne geldi (U'da +0,2, W4'te −2,8 mm). Önden lobül altları 1–2 mm yüksek kaldı.
- **Işık:** Profildeki gerçek görüntüde kanadın arkasındaki koyu bölgenin önemli kısmı ön ışıktan geliyor. Referans fotoğraf yandan aydınlatılmış. Geometrik sertlik (rölyef) GD28 seviyesine indirildi; gerçek görüntüdeki fark ince.
