# GD11 tur LL: çene ucu körletme, yan alt yüz konturu, burun yanı göz altı bandı (K5 → L3)

Tarih: 2026-10-07. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi.

## Kullanıcı isteği

"Çene ucunu referanstaki gibi biraz daha körelt; ayrıca çene kenarını ve burunda işaretlediğim yerleri de referansa yaklaştır. Göz altı–burundaki yeri ayarlamıştık, ne oldu?" İşaretler `data/user_markup.jpg` dosyasında.

**Göz altı–burun dolgusu ne oldu?** G2 dolgusu (en çok 2–3 mm) zincirde duruyor: F2 → G2 → H6 → J5 → K5 → L3. Etkisi küçük kaldı. Bu turda ölçünce burnun hemen yanında (x 0,9 → 1,5 cm, z 160,8–161,6) yaklaşık 1 cm'lik ani bir derinlik basamağı çıktı; G2 dolgusu bu basamağın dışında kalmıştı. Koyu bandın bir kısmı da cilt dokusundaki gölge renginden geliyor (yakın planda iki adayda da görünür). Bu kısım geometriyle tamamen kaybolmaz.

**Taban:** K5 + k15 + M_SlightArch + e3g + S_Thin + h68e.

## L3 = K5 + `data/L3.json`

| Alan | İşlem | Değer |
|---|---|---|
| Çene ucu | köşeler daha yuvarlak, uç noktası yumuşak, çene yastığı hafif geniş | 0,7–1 mm; çene boyu oranı 0,758 (referans 0,769) |
| Yan alt yüz konturu (işaretli) | elmacık altından çene köşesine dolgu; kontur daha düz iner | 3,5 mm |
| Burun yanı göz altı bandı (işaretli) | burun–yanak basamağı doldurma ve yumuşatma | 1,5 mm; burun kökü 0,00 mm |

Ön referans konturuna göre:

| | K5 | L3 |
|---|---|---|
| alt yanak | −0,30 / −0,27 cm | +0,17 / +0,30 cm |
| orta yanak | +0,07 / +0,13 cm | +0,13 / +0,23 cm |

Daha güçlü denemeler (L1/L2) orta yanağı +4–7 mm taşırdığı için kullanılmadı (board 05).

**Bölge ölçümü (K5'e göre):** dudak en çok 1 mm, göz kapağı en çok 1,6 mm, yanak/çene en çok 3,5 mm, burun kökü 0,00 mm.

## Gözlemlerim (karar kullanıcının)

- **Çene ucu:** biraz daha yuvarlak ve kör.
- **Yan kontur:** önden alt yüz yanları daha dolu, elmacıktan çeneye daha düz bir hat.
- **Burun yanı:** basamak yumuşadı. Ancak yakın planda koyu renk bandı büyük ölçüde duruyor; bu cilt dokusundan geliyor. Bir sonraki adım olarak ten malzemesinde bu bölgeye yerel aydınlatma önerilebilir.

## Teknik

| Kontrol | Sonuç |
|---|---|
| l3 auto-rig | taze editör, rig kapısıyla; fit ort. 0,021 / maks 0,358 mm; göz 0,000; 858 morph; DNA bağlı |
| l3 27 rig pozu / 27 hareket karesi | temiz |
| Kilitli dosyalar | geri dönüş kaydıyla aynı; korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ |

## Board'lar

- `01_COMPARE.jpg`: işaretler / K5 / L3; ön, stüdyo, burun ve çene yakın planı, 3/4.
- `02_REF_CAMERA.jpg`: çözülmüş referans kameraları.
- `03_FRONT_BLEND.jpg`: %50 bindirme.
- `04_WITH_HAIR.jpg`: saçlı görünüm.
- `05_CLAY.jpg`: kil.
- `06_TECH_RIG_l3.jpg`, `07_TECH_MOTION_l3.jpg`: rig pozları ve hareket.

Kaynaklar: `SourceAssets/Characters/GD11_ChinCheekLL_20261007`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
