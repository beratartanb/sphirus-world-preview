# Karakter, çevre ve oynanış — nitel değerlendirme

Bu belge **gözlem** içerir; nihai sanat/his onayı kullanıcıya aittir. Hiçbir yüz, vücut, kıyafet veya sahne öğesi değiştirilmedi.

## 1. Karakter (mevcut vücut)

**Görüntüler:** `images/charshots_lab_char_front.jpg`, `_side_left`, `_back`, `_threequarter`, `_gameplay_cam`.
- Çekim yeri: hafif ortam (L_GR_MovementLab), tek directional ışık ve gökyüzü.
- Kamera: 520 cm uzaklık, 92 cm yükseklik, FOV 40; oyun kamerası ayrıca alındı.
- Perspektif: FOV 40 / 5.2 m; ayaklar ve baş merkezden uzak olduğu için yaklaşık %2–3 perspektif büyümesi olabilir. Ortografik değildir.

**İskelet ölçüleri** (görünen MetaHuman gövdesi `SKM_MH_MainCharacter_BodyMesh`; boşta duruş, kemik merkezleri, cm, zemin z≈0):

| Ölçü | Değer |
|---|---|
| pelvis z | 95.0 |
| kalça eklemleri (thigh_l/r) z | 88.9 / 89.8 |
| diz (calf_l) z | 49.3 |
| ayak bileği (foot_l) z | 10.7 |
| neck_01 z / head z / FacialRoot z | 144.9 / 156.1 / 159.9 |
| clavicle z | 138.7 |
| Omuz eklemleri arası (upperarm_l ↔ upperarm_r) | 33.0 |
| Kalça eklemleri arası | 17.8 |
| Uyluk (thigh→calf) / baldır (calf→foot) dikey | 39.6 / 38.6 |
| Gövde (pelvis→neck_01) | 49.9 |

- Kafatası tepesi ölçülmedi: bounds API'si bu sürümde Python'a açık değil. Bu yüzden **boy ve baş/vücut oranı sayısal olarak verilmiyor**. Görüntüden tahmini oran uydurulmadı.
- **Sürücü/görünen iskelet farkı:** animasyonu süren gizli AAMS "Mascot" iskeletinde değerler farklı:

| Ölçü | Mascot | MetaHuman |
|---|---|---|
| Omuz eklemleri arası | 41.5 cm | 33.0 cm |
| head z | 161.4 | 156.1 |
| hand_l z | 92.1 | 87.2 |

  Görünen gövde retarget ile sürülüyor. El/ayak temas ve IK işleri bu oran farkını hesaba katmalı (gözlem).

**Görsel gözlemler** (nötr ışık; hüküm değil):
- **Önden:** duruş dik, kollar gövdeden hafif açık, ağırlık iki ayakta eşit. Omuz–bel–kalça geçişi yumuşak. Göğüs/bel/kalça hacimleri ölçülü.
- **Yandan:** pelvis hafif öne yatık. Sırt eğrisi doğal, baş gövdenin üzerinde. Diz hafif kilitli görünüyor.
- **Arkadan:** omuz hattı kalçadan dar değil. Belde hafif içe dönüş var. Bacaklar düz.
- **Oyun kamerası:** karakter ekranın alt-sol çeyreğinde; ölçek ve okunabilirlik iyi. Hafif ortam zemininde görüntünün ortasında dikey bir **doku/mip geçiş sınırı** görülüyor: sol taraf yüksek frekanslı, sağ taraf bulanık. Bu yalnız test haritasında; üretim haritasında gözlenmedi.
- **Temel pozlarda deformasyon:** yalnız boşta ve hareket kliplerinde gözlendi. Omuz/kalça sıkışması klip çözünürlüğünde seçilmedi. Yakın ve ayrıntılı deformasyon incelemesi **NOT_TESTED**.

**Referans:** Bu görev kapsamında "onaylanmış" olarak işaretli bir vücut referansı bulunamadı; önceki GD39–GD44 raporları referans karşılaştırması içerir ama onay durumu doğrulanamadı. **Benzerlik puanı verilmedi.**

## 2. Çevre: A ↔ C eşleşmesi ve donanımdan bağımsız eksikler

Görüntüler: `images/P{1..5}_*_{A,C}_r1.jpg`; fark haritaları `images/diff/`.

| Alan | Ayarlarla değişen (C) | Ayardan bağımsız; yeni donanımda da aynı kalacak gözlem |
|---|---|---|
| **P1 ev içi** | Çok küçük ışık tonu farkı (ortalama luma 88.2 → 89.9) | Sıcak, yaşanmış iç mekân okunuyor (halı, lamba, mobilya). Arka kapıdan orman görünüyor. Değerlendirme kullanıcıda |
| **P2 evden göle** | Su yansıması, sis huzmesi keskinliği | Gölet geniş, düz bir su yüzeyi olarak okunuyor. Kıyı çizgisinde sert/düz bir çamur düzlemi var. **Su yüzeyinde dikdörtgen/şerit yansıma deseni** var. Sis yoğun ve süt beyazı; arka orman katmanları birbirine karışıyor (AGENTS: "aşırı sis yok" ile karşılaştırılmalı) |
| **P3 göl kıyısı** | Yansıma şeritleri C'de belirginleşiyor | Kıyıda yakın bitki zengin; su–kıyı geçişi keskin. Şerit deseni burada da var |
| **P4 arka yokuş / orman yolu** | Gölge yumuşaklığı ve bitki içi GI tonu | Yoğun alt bitki ve kapalı orman hissi güçlü; patika bu kadrajda okunmuyor. Fark rüzgâr gürültüsünün az üstünde |
| **P5 yokuştan eve bakış** | Üst bant (taç/sis) ton farkı | Ev ağaçların arasından "sığınak" olarak görünüyor (AGENTS'taki geri bakış hedefiyle uyumlu). Sol taraftaki patika, keskin kenarlı **kahverengi bir oluk** gibi okunuyor (AGENTS "temiz kahverengi şerit yok" maddesiyle karşılaştırılmalı) |

**Sonuç:**
- C açıkken de görüntünün kimliği (kot ilişkisi, ormanın sarması, patika doğallığı, bahçe geçişleri, kompozisyon, malzeme uyumu) **değişmiyor**. C yalnız ışık/yansıma kalitesini oynatıyor.
- Sahne, rota ve malzeme eksikleri yeni donanımda kendiliğinden düzelmez: su yansıma deseni, sis yoğunluğu ve katman ayrımı, oluk gibi okunan yol, sert kıyı düzlemi, rotalardaki çarpışma engelleri.
- Rota boyunca tek tek kareler incelenmedi; yalnız 5 nokta ve R1 klibi incelendi. **Güzel bir ekran görüntüsü, rotanın tamamının başarılı olduğu anlamına gelmez.** R1/R2'nin tüm rota görsel değerlendirmesi **PARTIAL**.

## 3. Oynanış (yalnız mevcut olan)

| Konu | Durum | Kanıt |
|---|---|---|
| Ev → gölet rotası (R1) | Teknik **PASS**: içeriden açık veranda kapısından çıkıldı, veranda inildi, kıyıya varıldı. 20 PIE tekrarının hepsinde varış (ARRIVED), hiç STALL yok | `raw/pie_perf_*.json`, `clips/house_A_R1_house_to_pond.gif` |
| Ev yanı → arka yokuş (R2) | Teknik **PASS**: 15 tekrarın hepsinde varış | `raw/pie_perf_*.json` |
| Başlangıç | PIE oyuncusu `ReviewOnly_PlayerStart` (892, -220, 183) noktasında, evin arkasında doğuyor. Oyuncu başlangıcının adı "ReviewOnly"; gerçek oyun başlangıcı olarak niyet edilip edilmediği belirsiz | `inventory/editor_state.json`, probe |
| Yeniden başlatma | **NOT_TESTED** | — |
| Kayıt/yükleme | **NOT_IMPLEMENTED**: proje SaveGame sınıfı yok; yalnız AAMS demo `BP_SaveGame`; `Saved/SaveGames/Reset.sav` dışında kayıt dosyası yok | Dosya araması |
| Kapı/kol kapı/tavan arası merdiveni/vent/sandık etkileşimleri | **NOT_TESTED**: bu görevde etkileşim girişi denenmedi. Haritada aktörler mevcut (`BP_SphirusHinged_C` ×8, `BP_GR_LeverDoor_C`, `BP_GR_AtticLadder_C`, `BP_SphirusVentPull_C`). Kapıların çoğu haritada açık durumda (`R4_IsOpen=True`), `FamilyChestLid` kapalı | `raw` probe çıktısı |
| Maske/algı/görev fikirleri | **NOT_IMPLEMENTED** (bozuk değil, henüz yok); AI/görev/narrative bayrak sistemi yok (systems-inventory) | — |
| PIE başlangıç hataları | PIE her başladığında `MI_Fabric_White_Solid_01` ve `MI_Ground_MossyNeedles_01` için "requires virtual texture" materyal hataları loglanıyor (mevcut durum, düzeltilmedi) | `raw/pie_*.json → log_lines` |
