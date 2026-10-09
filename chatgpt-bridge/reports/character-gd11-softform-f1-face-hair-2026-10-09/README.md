# GD11 F1: yüz formu (ww5bt1h), saç silüeti (h75a) ve ince teller (h75c)

Tarih: 2026-10-09. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi. Eski varlıkların hiçbiri silinmedi ya da değiştirilmedi.

| Aşama | Aday | Taban |
|---|---|---|
| 1. Yüz formu | **SKM_G11RR_Face_ww5bt1h (F1H)** | O1G (ww5bo1g) |
| 2. Saç silüeti ve kütle | **h75a** | h74b; son işlem, yeniden kurulum yok |
| 3. İnce teller ve son dağınıklık | **h75c** = h75a + ince teller | h75a |
| Korunanlar | cilt x19a, iris e3n, kaş M_SlightArch (m3), ağız onarımı | aynı |

Bütün çekimler taze editörde alındı. Editör bellek sınırına yaklaşınca saç kask LOD'una düşüyordu (O1 raporu); her zincirden önce editör yeniden başlatıldı.

## Aşama 1: yüz formu

### Neden kontur değil iç biçim?

O1'de ön ve 3/4 alt yüz konturu referansla zaten ±1–5 mm eşleşiyordu. Önde ve 3/4'te alt yüz silüeti referans kadar ya da biraz daha geniş; dışa genişlik eklemek referanstan uzaklaştırır.

"Kemikli / oyuk / sert" okumanın kaynağını geniş ölçekli kabartı haritası (σ 1,6 cm; kırmızı sırt, mavi oyuk) gösterdi:

| İmza | Görünüm |
|---|---|
| Çene hattı | Çeneden çene açısına keskin bir sırt |
| Elmacık–çene arası yan düzlem | Düz; 3/4'te elmacık altından çeneye inen koyu çapraz bant |
| Burun yanı / burun-dudak | Geniş oyuk |

### Ne yapıldı (yalnız yumuşak doku, yalnız dolgu)

| İşlem | Miktar | Yön |
|---|---|---|
| Alt yanak / yan düzlem | 2,7 mm | ağırlıkla **öne** (çan profili); ön silüet genişlemesin diye |
| Jowl / alt yanak | 1,3 mm | öne |
| Çene altı | 2,3 mm | aşağı + hafif öne; çene sırtı yuvarlansın, çene–boyun geçişi yumuşasın |
| Elmacık tümseğinin alt kenarı | 1,2 mm | yüzey normali; "elmacık altı çukuru" okumasını kırmak için |
| Çene sırtı bandı | σ 1,6 yalnız dolgu | sırtın iki yanı yükseldi, sırt kesilmedi |

Çene ucu, çene açısı, dudak, burun ve göz kapakları 0 mm. Tarif: `data/F1h.json`.

**Elenen ara sürümler:**

| Ara sürüm | Neden elendi |
|---|---|
| F1a | burun yan duvarı 4,4 mm doldu (burnu genişletirdi) |
| F1c, F1e | çan tepelerinde küçük çıkıntılar |
| F1d | düzleştirme dolguyu sildi |
| F1f | önde çene gövdesi bandı 3,5 mm genişledi |
| F1g | burun-dudak dolgusu ağız köşesinde 11 yeni form üretti, geniş ölçekte etkisi yoktu |

### Hangi çizgiler değişti? (O1G → F1H)

Kontur: mm, + = aday referansın dışında. Çene alt çizgisi: + = aday aşağıda.

| Çizgi | O1G → F1H | Okuma |
|---|---|---|
| Ön kontur: alt yanak (sol / sağ) | −1,2 / +4,9 → aynı | ön silüet korunuyor |
| Ön kontur: çene gövdesi (sol / sağ) | −1,2 / +3,0 → −0,6 / +3,3 | ±0,6 mm |
| Ön çene alt çizgisi: çene gövdesi | +0,6 / +2,1 → +1,8 / +3,0 | çene altı dolduğu için ~1 mm aşağı |
| Ön çene yanı / çene tabanı | değişmedi | çene korunuyor |
| Sağ 3/4 uzak kontur: alt yanak / ağız / çene | +2,6 / +3,5 / +1,9 → +3,2 / +3,9 / +2,6 | ~0,6 mm dışa |
| Sol 3/4 (ref aynalı): ağız / çene | −0,6 / −1,9 → 0,0 / −1,3 | referansa yaklaştı |
| Profiller | değişmedi | orta hat dokunulmadı |

### Biçim ölçümleri (O1G → F1H)

| Ölçüm | O1G | F1H |
|---|---|---|
| Kesit dolgunluğu, ort (z 153 / 151,5 / 150,5) | +5,9 / +3,9 / +4,2 mm | **+6,5 / +4,7 / +4,5 mm** |
| Geniş ölçekli kabartı: çene sırtı bandı p10 / p90 | −1,23 / +1,22 | **−0,83** / +1,11 |
| σ 0,8 kabartı: çene gövdesi sırtı p90 | 0,40 | **0,31** |
| σ 0,8 kabartı: elmacık altı ortalama | −0,31 | **−0,27** (daha az oyuk) |
| Yeni çukur / çıkıntı | | 0 / 0 |
| Keskin kıvrım | 43 | 43 |
| Çene ucu / dudak / burun / kapaklar | | 0 mm |
| Çene açısı | | en çok 0,15 mm |

Görsel olarak 3/4'te kulak önünden yanak ortasına inen koyu çapraz bant açıldı ve yumuşadı; yan düzlem artık ışığı tutuyor (`12_ASAMA1_FORM.jpg`). Önde değişim ince.

## Aşama 2: saç silüeti ve kütle (h75a)

- **Arka kütle inceltildi:** kafanın arkasındaki saç katmanı kafa derisine doğru %15 inceltildi; kökler sabit, telin ilk %25'i korundu.
- **Seyreltme:** arka kütleden %15 ana tel çıkarıldı (4576 tel); dış kabuk havadar olsun ve topuz ayrı form okunsun diye.
- **Topuz:** %12 küçültüldü ve 0,5 cm kafaya yaklaştırıldı.

| Silüet (mm; + = bizimki referansın dışında) | h74b | **h75a** | h75c |
|---|---|---|---|
| Sağ profil arka: kulak üstü | −31,7 | **−45,5** | −45,1 |
| Sağ profil arka: kulak | −32,5 | **−51,5** | −51,5 |
| Sol profil arka: kulak üstü | −19,6 | **−37,6** | −37,6 |
| Arka toplam genişlik: kulak | +1,8 | +1,8 | +4,8 |
| Arka toplam genişlik: ense | −3,0 | +1,2 | +9,1 (ense telleri) |
| 3D arka uç (tepe–ense) | | 0,5–1,4 cm geri | aynı |

**Okuma ve sınır:**
- Arka kütle kafayı daha az büyütüyor; profilde topuz kafaya yaklaştı.
- Referanstaki topuz ise çok geride ve büyük. Profil silüetimiz artık referansın 3–5 cm içinde: bu sizin "arka kütle kafayı büyütmesin" isteğinizle referans paneli arasındaki bilinçli bir tercih.
- Arka görünümde kütle hâlâ geniş ve katmanlı; topuz referanstaki kadar ayrı bir düğüm okunmuyor.

## Aşama 3: ince teller ve son dağınıklık (h75c)

Mevcut tellerin döndürülmüş, uzatılmış ya da kısaltılmış kopyaları gevşek saça eklendi:

| Bölge | Eklenen tel | Not |
|---|---|---|
| Saç çizgisi | 781 geriye uzayan + 480 öne-aşağı düşen | Düşen teller saç çizgisinin üstüne sarkıyor, kaşın üstünde (z ≥ 164,8) bitiyor |
| Şakak ve yüz çevresi | 3241 | |
| Topuz çevresi | 1450 | |
| Ense ve kulak arkası | 1379 | |

| Ön silüet, toplam (sol + sağ, mm) | h74b | h75a | **h75c** |
|---|---|---|---|
| Kulak | −12,7 | −12,1 | **−4,3** |
| Kulak altı | −25,5 | −24,5 | **−15,5** |
| Şakak / kulak üstü | −1,8 | −2,8 | **−0,6** |
| Üst yan | +4,9 | +4,9 | +4,9 |

- Yüzü çerçeveleyen teller ön silüeti referansa yaklaştırdı.
- Saç çizgisinde şakak köşelerinde alın kenarına düşen teller görünüyor. Ortadaki koyu saç çizgisi bandı hâlâ seçilebiliyor (`22_ASAMA3_INCE_TELLER.jpg`).
- Ara sürüm h75b'de saç çizgisi telleri geriye uzadığı için alına inmiyordu; h75c onun yerini aldı.

## Dürüst değerlendirme

| Hedef | Durum | Not |
|---|---|---|
| Dış kontur referansla eşleşsin | **BAŞARILI (korundu)** | Önde ±0,6 mm değişim; 3/4 ±0,6; profil aynı. Kontur zaten eşleşiyordu. |
| Daha az kemikli / oyuk / sert | **KISMEN** | 3/4'teki koyu çapraz bant ve düz yan düzlem yumuşadı; çene sırtı yuvarlandı. Önde değişim ince; burun-dudak oluğunun geniş ölçekli derinliği değişmedi (araç kilitli kenarlarda dolduramadı). |
| Alt yanak / çene yanı hafif etli, çene projeksiyonu korunsun | **BAŞARILI** | Kesitler +0,6…0,8 mm dolgun; çene ucu 0 mm. |
| Önde saç kafayı doğal sarsın; saç çizgisi sert/boş olmasın | **KISMEN** | Yüz çevresi ve şakak telleri arttı, ön silüet referansa yaklaştı. Ortadaki saç çizgisi bandı hâlâ belirgin. |
| Profilde arka kütle kafayı büyütmesin | **BAŞARILI** | Arka kütle 1–2 cm geri çekildi. Referans topuzundan daha küçük. |
| Arka / topuz blok-kask gibi olmasın | **KISMEN** | Seyreltme ve topuz çevresi telleriyle daha gevşek; topuz hâlâ ayrı düğüm okunmuyor. |
| Küçük ayrık ince teller | **BAŞARILI** | 7331 ince tel (saç çizgisi, yüz çevresi, topuz, ense). |

Teknik başarı referansa benzerlikle aynı şey değil.

## Teknik

| Kontrol | Sonuç |
|---|---|
| ww5bt1h | ww5bo1g kopyası + doğrudan fark; 858 morph ve DNA korundu |
| h75a / h75b / h75c | içe aktarma, simülasyon, kask ve LOD'lar tamam; ww5bt1h bağlamaları kaydedildi |
| Rig pozları (ww5bt1h + h75b) | 27, temiz |
| Hareket kareleri (h75c) | 27, temiz; saç hareket halinde tellerle render ediliyor |
| Korunan adaylar | 89/89 (üç zincirde) |
| Kilitli dosyalar | geri dönüş kaydıyla aynı (7/7) |
| LOD | TEST EDİLMEDİ |
| Disk | C: ~51 GB boş |

## Board'lar

| Dosya | İçerik |
|---|---|
| `10_ASAMA1_SACSIZ.jpg` | aşama 1: saçsız O1G / F1H / referans; 5 açı |
| `11_ASAMA1_OVERLAY.jpg` | aşama 1: kontur overlay'i; 5 açı (camgöbeği referans, pembe aday) |
| `12_ASAMA1_FORM.jpg` | aşama 1: geniş ölçekli kabartı (ön, 3/4) ve yakın planlar |
| `20_ASAMA2_3_SAC_OVERLAY.jpg` | saç silüeti overlay'i: h74b / h75a / h75c; ön, arka, 3/4, iki profil |
| `21_ASAMA2_3_SAC_GORUNUM.jpg` | saç: h74b / h75a / h75c / referans; 6 açı |
| `22_ASAMA3_INCE_TELLER.jpg` | saç çizgisi, şakak, topuz–ense yakın planı: önce / sonra |
| `08_TECH_*.jpg` | rig ve hareket kareleri |

- Sayılar: `data/face_lines_O1G_F1H.txt`, `data/hair_lines_h74b_h75a_h75c.txt`, `data/sections_O1G_F1H.txt`, `data/lsrel_O1G_F1H.txt`.
- Kaynaklar: `SourceAssets/Characters/GD11_SoftFormF1_20261009`.
- Saç tel verisi: `Saved/Codex/GD11_HairQ_20261006/hair/h75a`, `h75b`, `h75c`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
