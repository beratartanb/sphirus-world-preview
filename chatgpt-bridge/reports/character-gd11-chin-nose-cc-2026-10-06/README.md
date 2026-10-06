# GD11 tur CC: çene çıkıntısı, burun altı / burun–dudak mesafesi, burnun göz altı hizası

Tarih: 2026-10-06. Durum: **KULLANICI SEÇİMİ İÇİN DURDURULDU.** Üretime geçirilmedi.

Kullanıcı işaretli görsellerle üç şey istedi (`data/user_markup_*`):
1. Çene referans gibi değil; ezik ve altı yok gibi duruyor, referanstaki gibi bir çıkıntı yapılsın.
2. Burun altı ve burun–dudak mesafesi farklı; taban ile B4 arasındaki yön.
3. Burnun göz altı hizası referans gibi değil.

**Taban:** y1 + k15 + M_SlightArch + e3g + S_Thin + h68e. Kaş, göz, ağız ve kulak bu turda sabit.

## Adaylar

| Aday | İçerik | Varlık |
|---|---|---|
| **B4** (tur BB) | Burun tabanı 6 mm yukarı, uç ve sırt; burun–dudak arası uzun | `SKM_G11RR_Face_b4` |
| **C2b** | B4 + burun–yanak geçişi + **çene 3 mm öne, alt kenar 2 mm aşağı** | `SKM_G11RR_Face_c2` / `MHC_G11RR_C2_Head` |
| **C3** | B4 + burun–yanak geçişi + **çene 5 mm öne, alt kenar 2,5 mm aşağı** | `SKM_G11RR_Face_c3` / `MHC_G11RR_C3_Head` |

**Burnun göz altı hizası** (C2b ve C3'te aynı):
- Bizde burun yan duvarı ile yanak arasında göz altından burun kanadına inen derin, koyu bir oluk vardı; ölçümde burnun yanında 3 mm'de 1,5 cm'lik derinlik düşüşü.
- Referansta burun orada dar ve yanağa yumuşak geçiyor.
- Yapılan: yanağın burna bitişik iç kısmı 1,6 mm doldurularak öne alındı; burun yan duvarı 0,7 mm içe alındı. Alt göz kapağının altında sönümleniyor.

**Çene:**
- Çene yumuşak dokusu (dudak altı oluğunun altından çene ucuna) öne alındı.
- Çene alt kenarı hafifçe aşağı indirildi, böylece "altı var" okunuyor.
- Dudaklar 154,4 cm'nin üstünde 0,00 mm. Dudak altı oluğu sınırında en çok 0,5 mm; çene ucunda en çok 5,6 mm (C3).

## Ölçüm: referans çene konturu (`data/chin_contours.txt`, cm; − = bizimki referansın içinde)

| Nokta | B4 | C2b | C3 |
|---|---|---|---|
| ön: çene sol / sağ | −0,73 / −0,60 | −0,57 / −0,33 | −0,43 / −0,20 |
| ön: çene ucu alt noktası | −0,77 | −0,50 | −0,43 |
| 3/4: çene ön-alt | −0,08 | +0,21 | +0,34 |
| 3/4: çene altı | −1,13 | −0,71 | −0,71 |
| 3/4: çene ucu alt noktası | −1,26 | −0,96 | −0,92 |

C3 her noktada referansa en yakın olanı. Çene altı hâlâ referansın 7–9 mm içinde. Bunu kapatmak için çeneyi daha fazla aşağı indirmek, yani uzatmak gerekir. Bu adımı (K5 ve X turlarında reddedilmişti) yapmadım; istenirse ayrı aday olarak hazırlanabilir.

## Gözlemlerim (karar kullanıcının)

- **C3:** profilde çene referanstaki gibi belirgin bir çıkıntı yapıyor, alt dudak ile çene arasında oluk var, çene altı okunuyor. Önden alt yüz daha toplu.
- **C2b:** aynı yönde, daha hafif.
- **Burun–yanak geçişi:** 3/4'te burnun yanındaki koyu oluk azaldı. Etkisi orta düzeyde.

## Teknik

| Kontrol | Sonuç |
|---|---|
| c2 ve c3 auto-rig | taze editör, rig kapısıyla; fit ort. 0,020 / 0,021 mm, maks 0,352 mm; göz 0,000; 858 morph; DNA bağlı |
| c2 / c3 27 rig pozu (board 05) | temiz; çene açma, sağa/sola çene, konuşma biçimleri, gülümseme, göz kırpma sorunsuz |
| c3 hareket 27 kare (board 06) | saç başla gidiyor, kesişme yok |
| Kilitli dosyalar | geri dönüş kaydıyla aynı; korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ |

## Board'lar

- `01_NOHAIR_COMPARE.jpg`: saçsız, yumuşak ışık: referans / taban / B4 / C2b / C3 (profil, 3/4, ön).
- `02_REF_CAMERA.jpg`: çözülmüş referans kamerası.
- `03_WITH_HAIR.jpg`: saçlı görünüm.
- `04_CLAY.jpg`: kil.
- `05_TECH_RIG_c2.jpg`, `05_TECH_RIG_c3.jpg`: 27'şer rig pozu.
- `06_TECH_MOTION_c3.jpg`: 27 hareket karesi.

Kaynaklar: `SourceAssets/Characters/GD11_ChinNoseCC_20261006`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI SEÇİMİ İÇİN DUR.**
