# GD25 — Üst dudak sınırı, alt dudak çıkıntısı, kolumella kavisi ve çene dönüşü

Tarih: 2026-10-11. Başlangıç ve geri dönüş noktası GD24 G24; GD24'e dokunulmadı.

Final aday **G25** (sculpt adı F). Durum: **PARTIAL**. Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED).

**Üretim karakterine uygulanmadı.** UE varlıkları `/Game/Sphirus/CharacterLab/GD25_IdentityMaster_20261011` altında, yalnız test amaçlı. Kaynaklar `SourceAssets/Characters/GD25_IdentityMaster_20261011` altında (sculpt verisi, op'lar, araçlar, blend/GLB/OBJ).

## 1. Notların ve ölçüm yöntemi

İşaretli görselin (`process/00`): (1) üst dudağın küçük ucu dışarı çıkmıyor, kıvrılarak yukarı devam ediyor; (2) alt dudakta küçük garip bir çıkıntı var; (3) burun deliklerinin ortasındaki kemik (kolumella) referanstaki gibi kavisli inmiyor; (4) çenede hâlâ kavisli dönüş yok.

Bu turda göz kararı yerine **profil silüetinin şekil analizini** kullandım (`tools/gd25_contour_shape.py`, `tools/gd25_anchored.py`):

- Referans fotoğrafın ve modelin silüeti sınır takibiyle çıkarıldı; landmark'lar otomatik bulundu: burun ucu → subnazal → labrale superius (üst dudağın en ön noktası) → stomion → labrale inferius → oluk → pogonion → gnathion → menton.
- Her segmentin **eğrilik profili** (kordona göre sarkma / kord uzunluğu, t = 0,1…0,9) ölçekten bağımsız karşılaştırıldı.
- Ayrıca model konturu iki landmark'a göre referansa yerel olarak hizalandı. Her noktadaki fark model mm'si olarak hesaplandı ve kamera projeksiyonuyla o silüeti oluşturan 3B köşeye bağlandı. Bu sayede alanlar doğrudan bu farklardan tasarlandı.
- Profil kamerası tam yan değil (17° önden). Silüet burun altında orta hattan (kolumella), dudak ve çenede ise orta hattın 0,3–0,9 cm yanından geliyor. Alanların yanal genişlikleri buna göre seçildi.

GD24'te (rig sonrası) ölçülen hatalar:

| Bölge | Referans | GD24 | Anlamı |
|---|---|---|---|
| Kolumella (uç→subnazal) sarkma, t=0,4 / 0,5 | +0,118 / +0,090 | +0,014 / −0,013 | Alt kenar kavisli değil, ortası 2,3–2,6 mm fazla yukarıda |
| Filtrum alt kısmı (subnazal→ls) sarkma, t=0,7 / 0,8 | −0,036 / −0,010 | +0,034 / +0,035 | Dudak filtruma dışbükey akıyor ("kıvrılarak yukarı") |
| Üst dudağın en ön noktası (ls) | — | 2,5 mm fazla aşağıda | Alt vermilyon 1,3–2,0 mm fazla önde |
| Vermilyon eğimi (ls→stomion) | 29° | 43° | |
| Alt dudak rölyefi | tek dışbükey | iki sırt (z 155,3 ve 154,8) + arada düz bant | Önden "çift dudak", yandan "küçük çıkıntı" |
| Çene alt yayı (pg→gn) sarkma / pg→me kord | 0,115 / 24,8 px | 0,092 / 14,6 px | Dönüş kısa ve sıkı; yastık üstü 1,0–1,4 mm geride, alt ön 0,6 mm önde |

## 2. Müdahale (`tools/build_gd25.sh`, G24S'ten, 0,000000 mm farkla yeniden üretilir)

1. **Üst/alt dudak** (tek dış-cilt alanı, temas çizgisinde 0, dişler sabit): üst dudağın alt vermilyonu en fazla 2,45 mm geri, alt dudak 0,1–0,5 mm öne. En ön nokta vermilyon sınırına çıktı; vermilyon referanstaki gibi ağız çizgisine doğru eğimli.
2. **Alt dudak** ön yüzü (z 154,45–155,45) konumsal yumuşatma: iki sırt ve aradaki bant tek dışbükey hacme birleşti (rölyef +0,07…+0,11, kesintisiz).
3. **Kolumella / infratip lobülü** (yeni araç `tools/gd25_undershell.py`): burnun yalnız **alt kabuğu**, y'ye bağlı bir profille aşağı-öne indirildi (en fazla 3,2 mm, lobül altı; subnazale doğru yumuşak geçiş). Burun deliği çatısı yerinde kaldı; çatı birleşiminde lokal gevşetme yapıldı.
4. **Çene**: yastık üstü/ortası +0,8…1,3 mm, alt yastık +0,2…0,9 mm (tam kalınlık). Oluk tabanı +0,4 mm (dış cilt). Alt ön köşe, ön-alt yüzlerde yalnız **öne** 1,7 mm itilerek yuvarlatıldı (aşağı bileşen yok); ardından çene yumuşatma. Çene altı ve önden çene alt kenarı GD24 ile aynı (satır 762), yani çene uzatılmadı.
5. Hafif burun zımparası.

Sonuç (sculpt F, aynı ölçüm):

| Segment | Referans | GD24 | **GD25** |
|---|---|---|---|
| Kolumella sarkma t=0,3 / 0,4 / 0,5 / 0,6 | +0,123 / +0,118 / +0,090 / +0,048 | +0,056 / +0,014 / −0,013 / −0,025 | **+0,129 / +0,116 / +0,084 / +0,063** |
| Filtrum sarkma t=0,5 / 0,7 / 0,8 | −0,083 / −0,036 / −0,010 | −0,023 / +0,034 / +0,035 | **−0,077 / −0,048 / −0,013** |
| ls konum hatası | 0 | 2,5 mm aşağıda | **0,0 mm** |
| Vermilyon (ls→sto) sarkma / açı | 0,128 / 29° | 0,176 / 43° | **0,110 / 26°** |
| Alt dudak (sto→li) sarkma | 0,087 | 0,108 | **0,091** |
| Çene alt yayı pg→gn sarkma | 0,115 | 0,092 | **0,091** |
| Çene pg→me sarkma / kord | 0,173 / 24,8 px | 0,191 / 14,6 px | **0,205 / 17,2 px** (daha dolgun, yuvarlak top) |

Yerel hizalı farklar (model mm): kolumella ±0,45 içinde (GD24: 2,6 mm). Kolumella tabanında tek bir nokta −0,67; burada silüet kolumella ile kanat eşiği arasında gidip geliyor. Üst vermilyon −0,3…−0,6 (GD24: −2,0). Çene, oluktan gnathiona kadar ±0,4 içinde (GD24: +1,4 / −0,65).

Adaylar (`process/`, `G1`):
- **A:** ilk geçiş; dudak açısı tuttu, kolumella yalnız uçta kavisli.
- **B:** dudak ve filtrum referansla eşleşti; kolumella ortası 1 mm yüksek, çene alt yayı düz.
- **C:** kolumella eşleşti, ama burun deliği çatısı birleşiminde üçgen alan oranı 0,125 (ezilme) ve kolumella tabanında dirsek.
- **D:** daha kalın geçiş kabuğu + birleşim gevşetme; alan oranı 0,20.
- **E:** subnazale daha yumuşak geçiş, daha dolgun alt çene yastığı. UE zincirinden geçti ama **reddedildi**: köşe itmesinin aşağı bileşeni çene altını 1,2 mm indirdi, önden çene alt kenarı 764 → 768 satır (referans 761). Bu "çene uzatma" demek.
- **F (final):** E ile aynı, ama köşe yalnız öne yuvarlandı. Önden çene alt kenarı 762 (GD24 ile aynı).

## 3. Teknik testler

| Test | Sonuç |
|---|---|
| Fit (2 rezidüel geri besleme) → sculpt | **PASS** (ortalama 0,040 mm, p95 0,20, p99 0,52, en fazla 1,26 mm) |
| Otomatik rig, DNA, 858 morph | **PASS** (otomatik rig ok, DNA bağlı, 858 morph, blendshape'li DNA; varlık `MHC_GD25_G25F`, yüz `SKM_GD25_Face_g25f`) |
| Rig sonrası mesh ↔ sculpt | **PASS** (ortalama 0,040 mm, en fazla 1,26 mm; GD24 → GD25 rig sonrası ortalama 0,05 mm, p99 1,2, en fazla 2,7 mm burun altı) |
| Ters üçgen (sculpt ve rig sonrası) | **PASS** (0 / 0) |
| Keskin kıvrım | **PARTIAL** (42; E'ye göre 9 sınırda, GD24'tekilerle aynı yerler) |
| Üçgen alan oranı min / max | 0,22 / 3,99 (max: kolumella iç duvarı, alçaltmadan gerilen üçgenler; GD24 3,70) |
| Göz kapağı / göz küresi | **PASS** (değişmedi) |
| Çene alt kenarı satırı (ön, 2x) | **PASS** (rig sonrası 764 = GD24, referans 761; E adayı 768 idi → reddedildi) |
| Rölyef rig sonrası (mm): uç lobülü / kanat / çene yastığı / üst dudak köşeleri | 0,034 → 0,042 / 0,033 → 0,032 / 0,038 → 0,038 / 0,032 → 0,032 |
| Profil şekil (rig sonrası, `H1`) | kolumella t=0,3–0,6: +0,124 / +0,108 / +0,079 / +0,055 (ref +0,123 / +0,118 / +0,090 / +0,048); filtrum ve vermilyon ±0,02; ls konum hatası 2,5 → 0,1 mm; pg→gn 0,103 (ref 0,115); pg→me 0,223 (ref 0,173; daha dolgun) |
| Kaş-kirpik bağlama, göz kırpma, RigLogic ifadeleri | **PASS** (19 RigLogic ifadesi × 2 görünüm; `F1`, `F2`) |
| LOD | **PARTIAL** (LOD0–3 yakalandı, `F3`; LOD4–7 NOT_TESTED) |
| PIE, animasyon, saç sim. | **NOT_TESTED** (C: ~2,2 GB boş) |
| Yeniden üretim | **PASS** (`tools/build_gd25.sh` G24S'ten G25S'i 0,000000 mm farkla üretir) |
| Üretim değişmedi | **PASS** (GD25 klasörleri dışında proje dosyası değişmedi; tek istisna lookdev araçlarının `Saved/Codex/CharacterFaceMatch_20260930/` altına yazdığı dört GD25 bağlama kaydı (E ve F). Content / SourceAssets / Config temiz; qa_config geri yüklendi; editör kaydetmeden kapatıldı. Reddedilen E'nin UE varlıkları (`MHC_GD25_G25`, `SKM_GD25_Face_g25`) GD25 test klasöründe kaldı) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

Not: Satır tabanlı bant tablosunda "infratip/kolumella" bandı +2,2 → +5,6 px görünüyor. Kolumella neredeyse yatay bir kenar; indikçe bu satırlarda silüet öne taşıyor. Bu bant yatay kenarda anlamlı değil; doğru ölçü yukarıdaki şekil analizi.

## 4. Panolar

- `H1`: profil şekil analizi (REF turuncu, GD24 cyan, GD25 magenta; landmark'lar kare).
- `O1–O3`: teşhis (GD24 gerçek/kil overlay'leri).
- `O4_*`: sonuç overlay'leri (REF | aday | %50 | fark; GD24 / GD25 gerçek ve kil).
- `O5`–`O6`: burun ve çene yakın plan overlay'leri.
- `C2`–`C6`: kil ve UE yakın planlar (C4 burun, C5 dudak, C6 çene).
- `D1`–`D4`: tam yüz.
- `E`: deformasyon GD24 → GD25.
- `F1`–`F3`: rig/ifade/LOD.
- `G1`: adaylar (GD24 / B / F kil overlay).
- `process/00`: senin işaretin; `01–08`: teşhis ve sonuç zoom'ları, şeritler.
- `A2`: eski cilt-anahtarlı burun profil çizgileri. Dudakta ve burun deliği gölgesinde güvenilmez (GD20'den beri bilinen sınır); karar için `H1` ve bant tabloları esas.

## 5. Açık kalanlar

- Profil ölçümünde mutlak konum ±2 px belirsiz (kamera yaw'ı, panel ölçeği).
- Referansın çene altı, hizalanmış profilde modelden 1–1,8 mm daha aşağıda. Önden çene alt satırı zaten eşleştiği için "çene uzatma yok" kuralıyla bunu uygulamadım. Dönüşün kavisi yastık ve köşe şekliyle verildi.
- Labiomental kıvrım (li→oluk) referanstan daha yumuşak/sığ kaldı. Daha önce bu kıvrımın şiddetini düşürmemi istemiştin; bilinçli bırakıldı.
- Burun delikleri önden referanstan büyük/düzensiz (GD18'den beri); kolumella indikçe yandan burun deliği görünürlüğü arttı (referansta da var).
