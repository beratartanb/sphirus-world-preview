# GD11 tur T: yaşanmışlık izleri, burun ucu düzeltmesi, kemik yapısı ve kafa formu (s3 → s5 + k13)

Tarih: 2026-10-06. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi. Önceki adaylar değiştirilmedi. r5 DNA dosyası için aşağıdaki teknik notta bir açıklama var.

## Aday

| Parça | Varlık |
|---|---|
| Yüz / DNA | `GD11_FaceR_20261006/Face/SKM_G11RR_Face_s5` / `MHC_G11RR_S5_Head` (yeni auto-rig) |
| Cilt | `GD11_FaceR_20261006/Skin/MI_LK_Face_*_VT_gqk13` (k10'un kopyası, k10 değişmedi) |
| Kaş / kirpik / saç | M_SlightArch, S_Thin, h66b (s5'e bağlı: `GB_G11RR_*_s5h48a`, `GB_G11RR_Hair*_s5h66b`) |

Ara adaylar: s4 (yüz, k10/k11/k12/k13 ile çekildi), k11, k12. Tümü `SourceAssets/Characters/GD11_FaceS_20261006`. Önce (s3 + k10) ve sonra (s5 + k13) aynı editör oturumunda, aynı ışık ve sıfırlanan simülasyonla çekildi (`prov/g11rsU.json`, `prov/g11rsW.json`).

## Burun ucu

s3'te uç 2,2 mm aşağı döndürülmüştü ve referansa göre düşük duruyordu. s4/s5'te bu dönüş geri alındı: uç r5'e göre yalnız 0,9 mm aşağıda, 0,5 mm önde. Böylece referanstaki gibi daha düz, ileri bakan bir uç kaldı. Kanat daraltma (2,3 mm), uç daraltma (1,2 mm) ve sırt daraltma (0,9 mm) korundu.

## Kemik yapısı ve yüz şekli (abartısız, `data/S4.json`)

| Bölge | Değişiklik |
|---|---|
| Elmacık kemeri | 1,0 mm yükselti; yanaktan kulağa giden kemik hattı belirginleşti |
| Elmacık altı | 0,5 mm yumuşak çökme; oyuk açılmadı |
| Çene kemiği alt kenarı | 0,6 mm belirginlik |
| Çene ucu | 1 mm uzama; önceki reddedilen 5–8 mm ile karşılaştırılamayacak kadar küçük |
| Göz altı torbası ve gözyaşı oluğu | 0,8 mm torba, 0,4 mm oluk; alt kapak kenarı hiç hareket etmedi |
| Gülme çizgisi | burun kanadından ağız köşesine doğru 0,4–0,45 mm'lik üç adımlı hafif kıvrım |

Dudaklar, üst dudak, kulaklar ve kapak kenarları bölge ölçümünde 0,00 mm.

## Kafa formu (s5 = s4 + `data/S5_cranium.json`)

- Tepe yanları 3,2 mm içe alındı: z 166–168'de kafatası yarı genişliği 7,53 → 7,34 ve 7,30 → 7,08 cm.
- Tepe 2 mm indirildi.
- Yüz, alın ve kulaklar 0,00 mm (yüz bölgesinde en fazla 0,04 mm).

Saçsız karşılaştırma board 01'in son iki satırında. Kafa referanstaki gibi daha dar ve daha az yüksek okunuyor; fark bilerek küçük tutuldu.

## Yaşanmışlık izleri (board 03)

Cilt malzemesinde, doku değiştirmeden, var olan ayarlar güçlendirildi:
- pişmiş normal haritası 1,0 → 2,0,
- mikro gözenek normali 1,0 → 2,2,
- normal düzleştirme 0,33 → 0,
- bölgesel mikro ayrıntı (alın, kaş arası, kapak, elmacık, çene, burun) 0,35–0,4 → 0,7–0,8,
- çukurlarda daha mat ve daha az parlak yüzey, sahte ortam gölgesi 1,0 → 1,5.

Sonuç: alın çizgileri, göz çevresi kırışıklıkları, gözenekler ve gülme çizgisi belirgin biçimde daha görünür, cilt daha "yaşanmış".

**Çalışmayan yol:** sabit kırışıklık haritası ağırlıkları (k12). Yüz animasyonu bunları çalışma anında sıfırlıyor; editörden okunan değer 0. Bu yüzden k13'e alınmadı.

## Teknik (board 04)

| Kontrol | Sonuç |
|---|---|
| s4 ve s5 auto-rig | taze editör, rig sonucu kontrolüyle; fit ort. 0,017 / maks 0,35 mm; 858 morph; DNA bağlı |
| 27 rig pozu + hareket (s5 + k13 + h66b) | temiz: göz kırpma tam kapanıyor, kaş, çene, gülümseme, konuşma biçimleri, burun deliği; saç başla gidiyor |
| Kilitli dosyalar | m2, M DNA, M_SlightArch ve bağlamaları, h51a geri dönüş kaydıyla aynı; korunan eski adaylar 89/89; r5 yüz mesh'i ve h65b özetleri bu tur öncesiyle aynı |
| **r5 DNA dosyası** | yeniden kaydedildi. Her rig dışa aktarımı aynı DNA klasöründeki tüm DNA varlıklarını yeniden yazıyor. r5 yeniden çekildi: nötr, göz kırpma, çene açma, gülümseme, kaş kaldırma ve burun deliği açma pozları önceki r5 çekimleriyle aynı, işlevsel değişiklik yok. |
| LOD | TEST EDİLMEDİ |

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| YAŞANMIŞLIK İZLERİ | KISMEN-İYİ (belirgin artış; referanstaki derin alın çizgileri ve renk lekeleri doku olmadan sınırlı) |
| BURUN UCU (düşmeyen, referans gibi) | BAŞARILI |
| KEMİK YAPISI / YÜZ ŞEKLİ | KISMEN (elmacık, çene hattı ve göz altı referans yönünde; abartıya kaçılmadı) |
| KAFA FORMU | KISMEN (daha dar, daha alçak tepe; küçük adım) |
| KİMLİK KORUNUMU | BAŞARILI |
| TEKNİK ÇALIŞIRLIK | BAŞARILI (LOD TEST EDİLMEDİ) |

## Board'lar

`boards/01_REF_BEFORE_AFTER_HEADFORM.jpg` referans | önce s3 + k10 | sonra s5 + k13 | saçsız kafa formu s3 ile s5 · `02_NOSE_BONES_CLAY.jpg` kil s3, s4, s5 + referans · `03_SKIN.jpg` cilt k10, k11 ve k13 · `04_TECH.jpg` rig pozları, hareket, r5 kontrolü.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
