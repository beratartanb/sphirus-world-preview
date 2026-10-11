# GD28 — Burun ucunun dış hattı, burun deliği kavisi ve uç yüksekliği

Tarih: 2026-10-11. Başlangıç ve geri dönüş noktası GD27 G27; GD27'ye dokunulmadı.

Final aday **G28** (sculpt adı F). Durum: **PARTIAL**. Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED).

**Üretim karakterine uygulanmadı.** UE varlıkları `/Game/Sphirus/CharacterLab/GD28_IdentityMaster_20261011` altında, yalnız test amaçlı. Kaynaklar `SourceAssets/Characters/GD28_IdentityMaster_20261011` altında.

## 1. İsteklerin ve teşhis

Kırmızı ile işaretlediğin üç nokta (`process/00`):

1. Burun ucunun dış hattı referanstaki gibi tek, yuvarlak bir "C" olsun.
2. Burun deliğinin üst kenarı (kanat kenarı) referansta "∩" gibi kemer; bizde "⌐" gibi önden arkaya düz inen bir kanca.
3. Burun ucunun yüksekliği referanstaki gibi olsun; bizimki yine biraz aşağıdaydı.

GD27 rig sonrası ölçümler (`process/01`, `process/02`):

- **Uç yüksekliği:** Ucun en önde duran bölgesinin ortası, subnazale–menton yüksekliğine göre referanstan **0,35 mm aşağıda**. Eski ölçü tek piksele bakıyordu ve bunu göstermiyordu. Yeni araç `tools/_tipheight.py` bölgenin ortasını alıyor.
- **Uç konturu:** Kemerden uca inen hat, ucun hemen üstünde referanstan erken dönüyor. Bu yüzden "C" üstte yassı okunuyor. Kemerden bir nokta ve subnazale ile hizalanınca uç 1,6 mm geride kalıyor (`tools/gd28_nosecontour.py`).
- **Delik kavisi:** Kameraya bakan kanadın alt kenarı ucun arkasında z 157,8–158,1'de sarkıyor. Yandan bakınca kenar kolumellanın üstüne iniyor ve görünen delik ortada 1,5–3,4 piksele kadar daralıyor. Kenar referanstaki gibi yukarı kemer yapmıyor (`tools/gd28_rimproj.py`).

## 2. Müdahale (`tools/build_gd28.sh`, G27S'ten, 0,000000 mm farkla yeniden üretilir)

1. **Kanat kenarı kemeri** (`gd28_undershell.py`, yalnız kanadın alt kabuğu, +z). Kolumella ve delik tabanı orta hattan 0,85–1,05 cm içeride hariç tutuldu. Kaldırma y 13,8'de en fazla 2,5 mm; y 12,8 ve 14,75'te sıfıra iniyor. Kenar kalınlığı 0,6.
2. **Uç rotasyonu**, üç yumuşak plato hareketiyle: supratip 0,5 mm geri, üst lobül 0,4 mm ileri ve 0,2 mm yukarı, uç bloğu 0,2 mm geri ve 0,1 mm yukarı.
3. **Kanat tabanı köşe yuvarlatma** ve hafif zımpara.

Adaylar (`boards/G1`, `process/05`, `process/07`):

- **A:** Uç altı (infratip) kaldırma, eşleşmiş kolumella eğrisini düzleştirdi. Uç 0,5 mm önde kaldı. Elendi.
- **B:** Güçlü kanat kaldırma (3,0 mm), uçta yalnız supratip ve üst lobül hareketi. Uç hâlâ 0,12 mm aşağıda ve 0,5 mm öndeydi. Elendi.
- **C / D:** Uç fazla kalktı (referanstan 0,70 / 0,53 mm yukarı). Elendi.
- **E:** Uç doğru, ama 3,0 mm'lik kanat kaldırma önden raf gibi keskin kenar verdi. Elendi.
- **F (final):** E'nin ucu, daha yumuşak kanat kaldırma (2,5 mm), daha kalın kabuk ve köşe yuvarlatma.

Sonuç (rig sonrası, gerçek mesh):

| Ölçü | GD27 | **GD28** | Referans |
|---|---|---|---|
| Uç yüksekliği (+ = aşağıda) | +0,35 mm | **−0,13 mm** | 0 |
| Uç–subnazale sarkma, t = 0,1…0,5 | +0,071 +0,103 +0,109 +0,105 +0,081 | **+0,068 +0,107 +0,115 +0,112 +0,088** | +0,068 +0,108 +0,123 +0,118 +0,090 |
| Kolumella kord açısı | 41,2° | **40,4°** | 40,5° |
| Uç üstü teğet açısı, f = −0,4 / −0,3 | −36° / −30° | **−48° / −35°** | −49° / −39° |
| Kemer + subnazale hizasında uç geride | 1,57 mm | **1,16 mm** | 0 |
| Kanat kenarı yüksekliği, y 13,6–14,0 (yan bant) | z 157,86–158,06 | **z 158,12–158,34** (2,3–2,8 mm yukarı) | kemer |
| Kolumella alt hattı | z 157,54–157,75 | **aynı** | — |
| Yandan görünen delik, orta kısım (izdüşüm, px) | 1,5–4,0 | **4,1–7,0** | daha açık |
| Gerçek UE görüntüsünde koyu delik genişlik / yükseklik (× uç–sn) | 0,34 / 0,20 | **0,44 / 0,23** | daha uzun oval |
| Önden çene alt kenarı satırı | 763 | **763** | 761 |

Not: Referansın koyu delik alanı aşağıdaki gölgeyle dudağa kadar taşıyor, bu yüzden onun genişlik/yükseklik sayısı şişkin. Delik şeklini `process/08` ve `process/09`'daki görüntülerle değerlendir.

## 3. Teknik testler

| Test | Sonuç |
|---|---|
| Fit (2 rezidüel geri besleme) → sculpt | **PASS** (ortalama 0,044 mm, p95 0,22, p99 0,58, en fazla 1,60 mm) |
| Otomatik rig, DNA, 858 morph | **PASS** (otomatik rig ok, DNA bağlı, 858 morph; `MHC_GD28_G28`, `SKM_GD28_Face_g28`) |
| Rig sonrası mesh ↔ sculpt | **PASS** (ortalama 0,044 mm, en fazla 1,60 mm; GD27 → GD28 rig sonrası ortalama 0,03 mm, en fazla 2,7 mm kanat kenarında) |
| Ters üçgen (sculpt ve rig sonrası) | **PASS** (0 / 0) |
| Keskin kıvrım | **PARTIAL** (42; E'ye göre 9 sınırda, GD27 ile aynı yerler) |
| Üçgen alan oranı min / max | 0,185 / 4,22 (GD27 0,22 / 4,29). En küçük oran delik iç duvarında, GD27'deki en küçük üçgenle aynı yerde; eşik ~0,15'in üstünde |
| Göz kapağı / göz küresi | **PASS** (değişmedi) |
| Çene alt kenarı satırı (ön, 2x, rig sonrası gerçek) | **PASS** (763; GD27 763, referans 761, yani uzama yok) |
| Rölyef rig sonrası (mm): uç lobülü / kanat | 0,039 → 0,035 / 0,033 → 0,028 (daha pürüzsüz) |
| Kaş-kirpik bağlama, göz kırpma, RigLogic ifadeleri | **PASS** (19 RigLogic ifadesi × 2 görünüm; `F1`, `F2`) |
| LOD | **PARTIAL** (LOD0–3 yakalandı, `F3`; LOD4–7 NOT_TESTED) |
| PIE, animasyon, saç sim. | **NOT_TESTED** (C: ~3 GB boş) |
| Yeniden üretim | **PASS** (`tools/build_gd28.sh` G27S'ten G28S'i 0,000000 mm farkla üretir) |
| Üretim değişmedi | **PASS** (Content / SourceAssets / Config / Plugins temiz. GD28 klasörleri dışında yalnız lookdev araçlarının ortak kayıtları değişti: iki GD28 bağlama kaydı ve çekim meta verileri. qa_config geri yüklendi; editör kaydetmeden kapatıldı. Ayrıntı `data/outside_change_scan.txt`) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 4. Panolar

- `C4`: burun yakın plan, gerçek ve kil, önden ve yandan (GD27 | GD28).
- `H1`: profil şekil analizi (REF turuncu, GD27 cyan, GD28 magenta).
- `O1–O3`: teşhis (GD27).
- `O4_*`: sonuç overlay'leri.
- `O5`–`O6`: burun ve çene yakın plan overlay'leri.
- `A2`: burun profil çizgileri.
- `C2`, `C3`, `C5`, `C6`: kil ve UE yakın planlar.
- `D1`–`D4`: tam yüz.
- `E`: deformasyon GD27 → GD28.
- `F1`–`F3`: rig, ifade ve LOD.
- `G1`: adaylar (GD27 / B / F).
- `process/00`: senin işaretin.
- `process/01–02`: GD27 teşhisi.
- `process/03–04`: kil sonuç zoom'ları (profil, önden 8x).
- `process/05–07`: ara ve elenen adaylar.
- `process/08–09`: gerçek UE profil zoom'u ve delik segmentasyonu (REF | GD27 | GD28).

Not: Referans profil paneli modelden ~%13 büyük. Bu yüzden aynı kameradaki %50 overlay'lerde alt yüz konumları 1–3 mm kayık görünür. Karar için ölçekten bağımsız `H1` ve oran ölçüleri esas.

## 5. Açık kalanlar

- **Delik hâlâ referanstan kısa.** Yandan görünen koyu açıklık GD27'ye göre %30 uzadı ve kemerlendi. Referanstaki uzun oval açıklığa ulaşmadı. Daha fazla kaldırma (E, 3,0 mm) önden kanat kenarını raf gibi keskinleştirdi. Bir sonraki adım, kenarı daha da kaldırmak yerine delik içini (vestibül) derinleştirmek olabilir.
- **Ucun hemen üstü** (f = −0,2) hâlâ referanstan yumuşak dönüyor (−25° / referans −42°). "C" üst kısmı biraz geniş yarıçaplı. Bunu sıkılaştırmak supratipte çukur riski taşıyor, bu yüzden bu turda bıraktım.
- **Çene yayı** (pg→gn) bu turda değişmedi; GD27'deki 0,08 / 0,115 farkı sürüyor.
