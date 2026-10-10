# GD26 — Dudakların genel profil hattına göre yeniden hizalanması

Tarih: 2026-10-11. Başlangıç ve geri dönüş noktası GD25 G25 (sculpt F); GD25'e dokunulmadı.

Final aday **G26** (sculpt adı B). Durum: **PARTIAL**. Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED).

**Üretim karakterine uygulanmadı.** UE varlıkları `/Game/Sphirus/CharacterLab/GD26_IdentityMaster_20261011` altında, yalnız test amaçlı. Kaynaklar `SourceAssets/Characters/GD26_IdentityMaster_20261011` altında.

## 1. Notun ve teşhis

Not: "Dudaklar biraz içeride kalmış gibi; orijinal referans üzerinden genel hattı tekrar hizala."

GD25'teki yerel hizalamalar (subnazal–oluk gibi iki landmark'a göre) dudakların **şeklini** referansla eşleştirmişti. Ama dudakların bütün profil hattı içindeki **yeri** ayrıca ölçülmemişti. Bu turda bunu ölçekten ve hizalamadan bağımsız iki ölçüyle ölçtüm (`tools/gd26_lip_prominence.py`, `tools/_horiz_profile.py`):

- **E-çizgisi** (burun ucu → pogonion) ve **sn–pg çizgisi**ne dik uzaklık / çizgi uzunluğu (subnazal, labrale superius, stomion, labrale inferius, oluk).
- Landmark'ların subnazale göre yatay konumu / sn–menton yüksekliği.

GD25 (rig sonrası) sonuçları, referans oranını tutturmak için gereken ileri hareket (model mm):

| Nokta | E-çizgisine göre | sn–pg çizgisine göre | Subnazale göre yatay fark |
|---|---|---|---|
| Subnazal | +3,0 | — | — |
| Üst dudak (ls) | +3,0 | +0,5 | +0,2 (doğru) |
| Stomion | +2,6 | +0,7 | +0,3 |
| Alt dudak (li) | +3,0 | +1,2 | +0,5 |
| Oluk | +2,1 | +0,6 | +1,4 fazla önde |
| Burun ucu | — | — | **+3,6 fazla önde** |
| Pogonion / gnathion / menton | — | — | **+2,7 / +4,1 / +3,8 fazla önde** |

Yani dudakların kendi şekli ve subnazale göre yeri doğru; ama **tüm ağız bloğu (subnazal + dudaklar + oluk) burun ucu ve çeneye göre ~3 mm geride**. Bu yüzden dudaklar "içeride" görünüyor. Burnu ve çeneyi geri çekmek son turlarda istediğin hacmi bozacağı için, referans oranlarını tutturan çözüm olarak ağız bloğunu öne aldım.

## 2. Müdahale (`tools/build_gd26.sh`, G25S'ten, 0,000000 mm farkla yeniden üretilir)

Yeni araç `tools/gd26_perioral.py`, tek bir ileri alan:

- **Ağız bloğu +2,8 mm öne**: deri + dişler/dil/diş etleri + tükürük birlikte. Subnazalden alt dudağa kadar düz, böylece dudak şekilleri aynen korunur. Oluk ve çene yastığı üzerinde azalarak z 151,8'de 0'a iner; çene altı sabit, önden çene alt kenarı 762 = GD25.
- **Burun tabanı**: subnazalde tam, burun ucunda 0 olan bir y-rampası. Kolumella şeklini koruyarak ucun etrafında yatayda kısalır. Burun ucu ve sırtı değişmez.

Adaylar:
- **A:** burun tabanı geçişi z'ye bağlı. Kolumella şişkinleşti (sarkma t=0,6'da +0,115, ref +0,048) ve subnazal 1,7 mm yukarı kaydı → elendi.
- **B (final):** y-rampası. Kolumella şekli korundu, açısı referansa yaklaştı.

Sonuç (sculpt B, aynı ölçüler):

| Ölçü | GD25 | **GD26** |
|---|---|---|
| E-çizgisi farkı: sn / ls / sto / li / oluk (mm) | 3,0 / 3,0 / 2,6 / 3,0 / 2,1 | **0,6 / 0,7 / 0,4 / 1,0 / 0,7** |
| sn–pg çizgisi farkı: ls / sto / li / oluk (mm) | 0,5 / 0,7 / 1,2 / 0,6 | **0,2 / 0,0 / 0,3 / 0,3** |
| Subnazale göre fazlalık: burun ucu / pg / gn / me (mm) | 3,6 / 2,7 / 4,1 / 3,8 | **0,95 / 0,6 / 1,6 / 2,2** |
| Kolumella (uç→sn) kord açısı | 47,3° | **41,9°** (ref 40,5°) |
| Kolumella sarkma t=0,3 / 0,5 / 0,7 | +0,124 / +0,079 / +0,014 | **+0,118 / +0,077 / +0,017** (ref +0,123 / +0,090 / −0,002) |
| Global hizada landmark hataları | sn +1,3, ls +1,1, pg −1,7 | **sn +0,3, ls +0,3, sto 0,0, sm 0,0, pg −0,4** |

## 3. Teknik testler

| Test | Sonuç |
|---|---|
| Fit (2 rezidüel geri besleme) → sculpt | **PASS** (ortalama 0,042 mm, p95 0,21, p99 0,56, en fazla 1,24 mm) |
| Otomatik rig, DNA, 858 morph | **PASS** (otomatik rig ok, DNA bağlı, 858 morph; `MHC_GD26_G26`, `SKM_GD26_Face_g26`) |
| Rig sonrası mesh ↔ sculpt | **PASS** (deri ortalama 0,042 mm, en fazla 1,24 mm; dişler 0,000 mm. GD25 → GD26 rig sonrası ortalama 0,68 mm, en fazla 2,96 mm ağız bloğu) |
| Ters üçgen (sculpt ve rig sonrası) | **PASS** (0 / 0) |
| Keskin kıvrım | **PARTIAL** (42; E'ye göre 9 sınırda, GD25'tekilerle aynı yerler) |
| Üçgen alan oranı min / max | 0,22 / 4,30 (max: kolumella iç duvarı, yatay kısalma; GD25 3,99) |
| Göz kapağı / göz küresi | **PASS** (değişmedi) |
| Çene alt kenarı satırı (ön, 2x) | **PASS** (rig sonrası 764 = GD25, referans 761) |
| Rölyef rig sonrası (mm): uç lobülü / kanat / çene yastığı | 0,039 → 0,038 / 0,032 → 0,033 / 0,039 → 0,039 |
| Profil oranları (rig sonrası) | E-çizgisi farkı sn / ls / sto / li / oluk: **0,7 / 0,8 / 0,5 / 1,0 / 0,3 mm** (GD25: 3,0 / 3,0 / 2,6 / 3,0 / 2,1). sn–pg: 0,2 / 0,0 / 0,3 / −0,2. Subnazale göre fazlalık: burun ucu 0,9, pg 0,6, gn 1,5, me 1,3 mm (GD25: 3,6 / 2,7 / 4,1 / 3,8) |
| Kolumella şekli (rig sonrası) | sarkma t=0,3 / 0,5 / 0,7: +0,112 / +0,074 / +0,009 (ref +0,123 / +0,090 / −0,002); kord açısı 42,5° (ref 40,5°, GD25 47,3°) |
| Kaş-kirpik bağlama, göz kırpma, RigLogic ifadeleri | **PASS** (19 RigLogic ifadesi × 2 görünüm; `F1`, `F2`) |
| LOD | **PARTIAL** (LOD0–3 yakalandı, `F3`; LOD4–7 NOT_TESTED) |
| PIE, animasyon, saç sim. | **NOT_TESTED** (C: ~3 GB boş) |
| Yeniden üretim | **PASS** (`tools/build_gd26.sh` G25S'ten G26S'i 0,000000 mm farkla üretir) |
| Üretim değişmedi | **PASS** (GD26 klasörleri dışında yalnız lookdev araçlarının `Saved/Codex/CharacterFaceMatch_20260930/` altına yazdığı iki GD26 bağlama kaydı değişti; Content / SourceAssets / Config temiz; qa_config geri yüklendi; editör kaydetmeden kapatıldı) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

Not, mutlak kamera çerçevesi: Referans profil paneli modele göre ~%12 büyük (global hizalama ölçeği 1,128). Bu yüzden aynı kameradaki %50 overlay'lerde (`O4`) ve satır bantlarında modelin alt yüzü ağız bloğu ilerledikten sonra referans silüetinin 1–3 mm önünde okunuyor. Bu fark panelin ölçeğinden geliyor, oranlardan değil. Karar için ölçekten bağımsız `H1` ve yukarıdaki oran ölçüleri esas.

## 4. GD25 raporunda düzeltme

GD25 raporundaki **Blender kil** görselleri yanlışlıkla elenen aday E'nin sculpt'ından üretilmişti: O4/O5/O6 kil satırları, C2/C3 ve G1'deki "F" sütunu. F dondurulduktan sonra Blender render'larını yenilemeyi atlamıştım. E ile F arasındaki tek fark çene alt köşesi (E'de çene altı 1,2 mm aşağıdaydı). GD25'in UE gerçek ve UE kil yakalamaları, H1 şekil analizi, bant ölçümleri ve test sonuçları F'ye aitti ve doğruydu. Bu raporda GD25 karşılaştırmaları doğru F render'larıyla (`G25FM`) yapıldı. Fark `process/06`'da: GD25 raporundaki kil (E) ile doğru F karşılaştırması.

## 5. Panolar

- `H1`: profil şekil analizi (REF turuncu, GD25 cyan, GD26 magenta).
- `O1–O3`: teşhis (GD25 gerçek ve doğru F kil).
- `O4_*`: sonuç overlay'leri (REF | aday | %50 | fark; GD25 / GD26 gerçek ve kil).
- `O5`–`O6`: burun ve çene yakın plan overlay'leri.
- `C2`–`C6`: kil ve UE yakın planlar.
- `D1`–`D4`: tam yüz.
- `E`: deformasyon GD25 → GD26.
- `F1`–`F3`: rig/ifade/LOD.
- `G1`: adaylar (GD25 / A / B).
- `process/`: teşhis ve sonuç kontur/zoom görselleri ile GD25 düzeltme görseli.

## 6. Açık kalanlar

- Burun ucu subnazale göre hâlâ ~1 mm, çene altı (gn/me) 1,6–2,2 mm referans oranından önde. Çene hacmi ve uç şekli senin önceki isteklerin olduğu için dokunmadım; istersen ayrı bir turda küçük bir geri alma yapılabilir.
- Ağız bloğu 2,8 mm öne geldiği için ¾ görünümde ağız çevresi biraz daha çıkık görünür; bu referans oranının gereği.
- Labiomental kıvrım referanstan sığ (bilinçli, GD21 isteğin).
