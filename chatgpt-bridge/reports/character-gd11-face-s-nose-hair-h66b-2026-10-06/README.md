# GD11 tur S: yüz kasları ve baş formu, burun, sarkan saç tutamları (r5 + h65b → s3 + h66b)

Tarih: 2026-10-06. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi. Önceki adaylar (m2, r5, h64a, h65b) değiştirilmedi.

## Adaylar

| Durum | Yüz / DNA | Kaş / kirpik | Saç |
|---|---|---|---|
| Önce | `SKM_G11RR_Face_r5` / `MHC_G11RR_R5_Head` | M_SlightArch / S_Thin | `GR_LK_Hair_*_h65b` |
| Yalnız saç | r5 | aynı | **h66b** (`GD11_HairQ_20261006/Hair/GR_LK_Hair_*_h66b`) |
| **Birleşik** | **`GD11_FaceR_20261006/Face/SKM_G11RR_Face_s3` / `MHC_G11RR_S3_Head`** (yeni auto-rig) | M_SlightArch / S_Thin, s3'e bağlı (`GB_G11RR_*_s3h48a`) | h66b (`GB_G11RR_Hair*_s3h66b`) |

Üç durum aynı editör oturumunda, aynı ışıkla ve sıfırlanan simülasyonla (time=0) çekildi. Kompozisyon editörden okundu (`prov/g11rsE.json`, `g11rsH.json`, `g11rsK.json`).

## Burun ve yüz (board 02)

s3 = r5 üzerine (`data/S3.json`, en çok 2,45 mm):

| İşlem | Değer | Amaç |
|---|---|---|
| Uç aşağı dönüş | 2,2 mm aşağı, 0,6 mm öne | Referanstaki gibi önden delikler daha az görünür, burun daha uzun okunur |
| Kolumella | 0,9 mm uçla birlikte | |
| Kanatlar içe | 2,3 mm | Delik duvarlarıyla birlikte bütün olarak, delik içi ezilmedi (kil alttan görünüm) |
| Kanat kıvrımı | 0,5 mm içe | |
| Uç daraltma | 1,2 mm | |
| Üst sırt daraltma | 0,9 mm | |
| Yan yanak / baş formu | 2,5 mm içe | Üst-orta yanak referanstan genişti; yüz daha dar ve uzun okunur |
| Gülme çizgisi üstü yanak dolgunluğu | 1,4 mm | Referanstaki yanak kası hacmi |

Ara aday s2 aynı işlemlerin yaklaşık üçte ikisiydi (rig'lendi). s1'de yanak işlemi kulağa ve kanat işlemi dudağa taşıyordu, reddedildi.

**Korunan:** gözler ve kapaklar (r5 kapağı aynen), kaş, burun kökü (en çok 0,14 mm), üst dudak ve filtrum (bölge ölçümünde 0,00 mm), çene ucu, çene köşesi, kulak. Çene boyu ve dudaklar önceki ret kararları nedeniyle değiştirilmedi.

## Sarkan tutamlar (board 03)

h66a/h66b'de ana groom h65b ile bit-bit aynı. Sarkan teller yeniden kuruldu:
- **Toplu kilitler:** her tutam 40–70 telli, 3–5 alt tutamlı, ortası dolgun, ucu yumuşak toplanan, hafif yassı kesitli; tellerin %12'si uçta ayrılıyor.
- **Ana saça bağlılık:** kökten çıktıktan sonra ana kütlenin içinde yaklaşık 1,8 kat daha uzun ilerleyip oradan ayrılıyor.
- **Sayı:** daha az ama daha kalın tutam (yüz yanı 10/taraf, kulak arkası 8/taraf, ense 18, topuzdan dökülen 14).
- **Kalınlık:** h66b aynı tellerin daha kalın gevşek tel genişliğiyle (0,006 → 0,0085) içe aktarılması, bu yüzden tutamlar daha opak ve koyu okunuyor.

## Teknik (board 04)

| Kontrol | Sonuç |
|---|---|
| s3 auto-rig | taze editör, rig sonucu kontrolüyle; fit ort. 0,017 / maks 0,35 mm; 858 morph; DNA bağlı |
| 27 rig pozu (ön) | temiz: göz kırpma, bakış, kaş, çene, ağız, konuşma, burun deliği sıkma/açma (yeni kanatlarla) |
| Hareket 27 + eğim 5 | saç başla gidiyor, kök kopması ve kesişme yok |
| Kilitli dosyalar | m2, M DNA, M_SlightArch ve bağlamaları, h51a geri dönüş kaydıyla aynı; korunan adaylar 89/89; r5 ve h65b dosyalarına yazılmadı (önceden özet alınmamıştı, bu yalnız iş kaydıyla doğrulandı) |
| LOD | TEST EDİLMEDİ |

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| BURUN REFERANSA BENZERLİK | KISMEN, belirgin ilerleme (uç ve kanatlar referans yönünde; burun hâlâ biraz daha geniş ve kısa) |
| YÜZ KASLARI / BAŞ FORMU | KISMEN (yanak daraldı, yanak kası belirginleşti; çene boyu ve dudak farkı duruyor) |
| SARKAN TUTAMLARIN HACMİ VE BAĞLILIĞI | KISMEN-İYİ (arkada ve yanlarda toplu, kalın, dalgalı; önde yüz yanındaki tutamlar referanstan hâlâ biraz daha ince) |
| KİMLİK KORUNUMU | BAŞARILI |
| TEKNİK ÇALIŞIRLIK | BAŞARILI (LOD TEST EDİLMEDİ) |

## Board'lar

`boards/01_REF_BEFORE_AFTER.jpg` referans | önce (r5 + h65b) | sonra (s3 + h66b) · `02_FACE_NOSE.jpg` yüz ve burun + kil + ısı haritası · `03_HANGING_LOCKS.jpg` sarkan tutamlar h65b ile h66b · `04_TECH.jpg` rig pozları + hareket.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
