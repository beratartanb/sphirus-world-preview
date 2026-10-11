# GD27 — Burun ucu ve çenenin hafif geri alınması, çene altının kavisli dönüşü

Tarih: 2026-10-11. Başlangıç ve geri dönüş noktası GD26 G26; GD26'ya dokunulmadı.

Final aday **G27** (sculpt adı B). Durum: **PARTIAL**. Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED).

**Üretim karakterine uygulanmadı.** UE varlıkları `/Game/Sphirus/CharacterLab/GD27_IdentityMaster_20261011` altında, yalnız test amaçlı. Kaynaklar `SourceAssets/Characters/GD27_IdentityMaster_20261011` altında.

## 1. İsteklerin ve teşhis

1. GD26'da kalan burun ucu ve çene fazlalıklarını hafifçe geri almak. Subnazale göre: burun ucu +0,9 mm; pogonion / gnathion / menton +0,6 / +1,5 / +1,3 mm.
2. "Çene altı hâlâ düz gidiyor; referanstaki gibi biraz daha aşağı kavisli ve yumuşak dönebilir."

Çene altını global profil hizasında ölçtüm (`tools/gd27_chinbottom.py`). Model konturu tüm landmark'larla referansa hizalandı, pogonion'dan çene altına ve boyna doğru her noktanın farkı mm ve 3B kaynak köşeyle hesaplandı. 6x zoom (`process/01`) ve sayılar aynı şeyi söylüyor. Referansta çene alt kısmı yuvarlak bir top: en alçak nokta çenede, arkasındaki çene altı hattı boyna doğru **yükseliyor**. GD26'da köşeden sonra düz bir çizgi var. Orta hat kesitinde çene altı y 12 → 9 boyunca z ≈ 151,4'te düz kalıyor; global hizada bu hat referansın 1–5 mm altında okunuyor. Yastığın alt-önü 0,4–0,9 mm fazla önde.

## 2. Müdahale (`tools/build_gd27.sh`, G26S'ten, 0,000000 mm farkla yeniden üretilir)

1. **Çene altı dalgası** (`gd27_undershell.py`, yalnız alt kabuk, +z): çene altı hattı boyna doğru en fazla 2,9 mm yükseltildi (y 6,5–11,9, yanlarda 2,6–4,2 cm'ye kadar azalarak). Çene topunun altı yerinde, köşe yuvarlatıldı. Sonuç: orta hatta z 151,48 (y 12) → 151,67 (y 9), yani hat artık boyna doğru yükseliyor.
2. **Çene alt-önü** en fazla 0,6 mm geri (z 151,4–153,2, tam kalınlık). Alt yay dışbükey kalacak kadar hafif tutuldu.
3. **Burun ucu** 0,7 mm geri (uç bölgesi bütün halinde).

Adaylar:
- **A:** dar çene altı alanı (yanlarda 1,5–3,0) ve daha fazla alt-ön geri alma. Çene alt yayı düzleşti (pg→gn sarkma 0,065), köşe referansın 0,5–0,9 mm dışında kaldı → elendi.
- **B (final):** geniş alan, hafif geri alma ve köşe yuvarlatma.

Sonuç (sculpt B):

| Ölçü | GD26 | **GD27** | Referans |
|---|---|---|---|
| Burun ucu fazlalığı (subnazale göre) | 0,9 mm | **0,2 mm** | 0 |
| Kolumella kord açısı | 42,5° | **40,6°** | 40,5° |
| pg / gn / me fazlalığı | 0,6 / 1,5 / 1,3 mm | **0,3 / 0,9 / 0,3 mm** | 0 |
| E-çizgisi farkı sn / ls / sto / li / oluk | 0,7 / 0,8 / 0,5 / 1,0 / 0,3 mm | **0,15 / 0,17 / −0,08 / 0,41 / 0,21 mm** | 0 |
| Çene köşesi (global hiza) | +0,1…+0,5 | **±0,3** | 0 |
| Çene altı orta hat eğimi (y 12 → 9) | düz (151,47 → 151,39) | **yükseliyor (151,48 → 151,67)** | yükseliyor |
| Önden çene alt kenarı satırı | 762 | **760** | 761 |

## 3. Teknik testler

| Test | Sonuç |
|---|---|
| Fit (2 rezidüel geri besleme) → sculpt | **PASS** (ortalama 0,043 mm, p95 0,22, p99 0,59, en fazla 1,60 mm) |
| Otomatik rig, DNA, 858 morph | **PASS** (otomatik rig ok, DNA bağlı, 858 morph; `MHC_GD27_G27`, `SKM_GD27_Face_g27`) |
| Rig sonrası mesh ↔ sculpt | **PASS** (ortalama 0,043 mm, en fazla 1,60 mm; GD26 → GD27 rig sonrası ortalama 0,04 mm, en fazla 2,7 mm çene altı) |
| Ters üçgen (sculpt ve rig sonrası) | **PASS** (0 / 0) |
| Keskin kıvrım | **PARTIAL** (42; E'ye göre 9 sınırda, GD26 ile aynı yerler) |
| Üçgen alan oranı min / max | 0,22 / 4,29 (GD26 ile aynı) |
| Göz kapağı / göz küresi | **PASS** (değişmedi) |
| Çene alt kenarı satırı (ön, 2x, rig sonrası gerçek) | **PASS** (763; GD26 764, referans 761, yani uzama yok) |
| Çene altı orta hat (rig sonrası) | y 12 → 9: 151,50 → 151,67 (boyna doğru yükseliyor; GD26 151,48 → 151,40 düz) |
| Profil oranları (rig sonrası) | Subnazale göre fazlalık: burun ucu **0,19**, pg **0,34**, gn **0,85**, me **0,59 mm** (GD26: 0,87 / 0,62 / 1,54 / 1,27). E-çizgisi farkı sn / ls / sto / li / oluk: 0,25 / 0,24 / −0,01 / 0,46 / −0,17 mm |
| Kolumella (rig sonrası) | kord açısı 41,2° (ref 40,5°); sarkma t=0,3 / 0,5: +0,109 / +0,081 (ref +0,123 / +0,090) |
| Çene yayı (rig sonrası) | pg→gn 0,087 (ref 0,115); pg→me 0,195 (ref 0,173) |
| Rölyef rig sonrası (mm): uç lobülü / kanat | 0,037 → 0,039 / 0,033 → 0,033 |
| Kaş-kirpik bağlama, göz kırpma, RigLogic ifadeleri | **PASS** (19 RigLogic ifadesi × 2 görünüm; `F1`, `F2`) |
| LOD | **PARTIAL** (LOD0–3 yakalandı, `F3`; LOD4–7 NOT_TESTED) |
| PIE, animasyon, saç sim. | **NOT_TESTED** (C: ~2,5 GB boş) |
| Yeniden üretim | **PASS** (`tools/build_gd27.sh` G26S'ten G27S'i 0,000000 mm farkla üretir) |
| Üretim değişmedi | **PASS** (GD27 klasörleri dışında yalnız lookdev araçlarının `Saved/Codex/CharacterFaceMatch_20260930/` altına yazdığı iki GD27 bağlama kaydı değişti; Content / SourceAssets / Config temiz; qa_config geri yüklendi; editör kaydetmeden kapatıldı) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 4. Panolar

- `H1`: profil şekil analizi (REF turuncu, GD26 cyan, GD27 magenta).
- `O1–O3`: teşhis (GD26).
- `O4_*`: sonuç overlay'leri.
- `O5`–`O6`: burun ve çene yakın plan overlay'leri.
- `C2`–`C6`: kil ve UE yakın planlar (C6 çene).
- `D1`–`D4`: tam yüz.
- `E`: deformasyon GD26 → GD27.
- `F1`–`F3`: rig/ifade/LOD.
- `G1`: adaylar (GD26 / A / B).
- `process/01–05`: çene altı teşhis ve sonuç zoom'ları, kontur, elenen A.

Not: Referans profil paneli modelden ~%13 büyük olduğu için aynı kameradaki %50 overlay'lerde alt yüz konumları 1–3 mm kayık görünür. Karar için ölçekten bağımsız `H1` ve oran ölçüleri esas.

## 5. Açık kalanlar

- Çene altının arka kısmı (boyna yakın, y 8–9) referansta hâlâ 4–8 mm daha yüksek. Bu fark referans fotoğraftaki boyun duruşu ve çene–boyun açısından geliyor. Tam eşleşme boynun gövdeye bağlandığı bölgeyi değiştirmeyi gerektirir; "biraz" dediğin için ve gövde bağlantısını bozmamak için yarı ölçüde bıraktım.
- Çene alt yayının dışbükeyliği (pg→gn) referanstan biraz az (0,083 / 0,115).
- Çene kenarına (prejowl / jawborder) etki en fazla 0,3 mm.
