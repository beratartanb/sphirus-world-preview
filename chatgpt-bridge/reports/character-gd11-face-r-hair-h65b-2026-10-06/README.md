# GD11 tur R: topuz altına doğallık ve bolluk (h65b) + yüz karakterini referansa yaklaştırma (r5)

Tarih: 2026-10-06. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi. m2, M DNA, M_SlightArch ve h64a dahil önceki her şey değişmeden duruyor.

## Adaylar

| Durum | Yüz / DNA | Kaş / kirpik | Saç | Bağlamalar |
|---|---|---|---|---|
| Önce | `SKM_G11RM_Face_m2` / `MHC_G11RM_M2_Head` | M_SlightArch / S_Thin (M) | `GD11_HairQ_20261006/Hair/GR_LK_Hair_*_h64a` | `GB_G11RQ_*_m2h64a` |
| Yalnız saç | m2 | aynı | **h65b** (`GD11_HairQ_20261006/Hair/GR_LK_Hair_*_h65b`) | `GB_G11RQ_*_m2h65b` |
| **Birleşik** | **`GD11_FaceR_20261006/Face/SKM_G11RR_Face_r5` / `MHC_G11RR_R5_Head`** (yeni auto-rig) | M_SlightArch / S_Thin, r5'e bağlı | h65b | `GB_G11RR_*_r5h65b`, `GB_G11RR_EyebrowsM_SlightArch_r5h48a` |

Ten / göz k10 / e2. Üç durum aynı editör oturumunda, aynı ışıkla ve kurulumda sıfırlanan simülasyonla (time=0) çekildi. Kompozisyon editörden okundu (`prov/g11rrA.json`, `g11rrB.json`, `g11rrD.json`).

## Topuz altı (board 02)

h65b'de ana groom h64a ile bit-bit aynı; yalnız gevşek katman değişti:
- **Sarkık halkalar** (`mess_loop`, 34 küme): enseden topuz altına giden, boyundan 1–2,6 cm ayrılıp sarkan yumuşak halkalar.
- **Topuzdan dökülen teller** (`mess_fall`, 22 küme): topuzun alt yüzeyinden boyna yakın, dalgalı dökülüyor.
- **Ense sarkan teller** 26 → 38 küme, topuz halkaları 110 → 140.

Topuz altındaki boyun arkasından geçen gevşek tel sayısı 2.058 → 3.865. İlk deneme h65a'da dökülen teller 4–7 cm geriye savruluyordu, yandan bakınca tek düz bir çubuk gibi okunuyordu. h65b'de boyna yakın sarkıyorlar.

## Yüz (board 03)

**Ölçüm.** Referans çerçevesindeki kontur ölçümüne göre m2'nin çenesi ve çene ucu referansın içinde kalıyor: çene köşesi 1,1–1,5 cm, çene ucu 0,9 cm daha yukarıda. Referansın daha uzun okunmasının ana sebebi bu. Çene uzatma ve sertleştirme daha önce reddedildiği için yüz boyuna dokunulmadı.

**Yapılan (r5, m2'ye göre en çok 2,85 mm):**
- **Üst kapak:** kapak kenarı göz küresi merkezi etrafında 3° döndürüldü. Kapak küre yüzeyinde kaldı, 0,4–0,6 mm indi, alt kapak hiç hareket etmedi. Kapak çizgisinin üstüne 2,4 mm, dış köşeye 1,5 mm yumuşak örtü eklendi. Referanstaki irisin üstünü hafif örten, dinlenmiş ve ağır bakış buradan geliyor.
- **Elmacık:** yüksek ve dışta 1,5 mm dolgunluk.
- **Alt yanak:** ağız köşesinin dışında 2 mm yumuşak ovalleştirme. Yanak oyuğu açılmadı, çene ucu ve çene köşesi değişmedi.

**Dokunulmayan:** burun, dudak, ağız köşeleri, çene ucu, kaş ve kulak (`data/heat_R5_vs_m2.txt`: dudak, çene, kulak ve kafatası 0,00 mm). Burun kökü bandında hareket eden noktalar iç göz köşesine yakın üst kapak noktaları.

**Sonuç.** Önden ve 3/4'te bakış referansa belirgin biçimde yaklaştı, alt yüz çok hafif ovalleşti. Yüz biçimindeki büyük farklar ise kasıtlı olarak bırakıldı: referansın daha uzun çenesi, daha ince dudakları, daha ince ve uzun burnu, elmacık altı gölgesi. Bunlar önceki turlarda reddedilen ya da kilitlenen bölgeler.

Ara denemeler: r1/r2 (0,75 mm, görünmez), r3 (1,7 mm, rig'lendi, dokulu görselde m2'den ayırt edilemedi), r4 (örtü burun köküne taşıyordu). Hepsi `SourceAssets/Characters/GD11_FaceR_20261006/face`.

## Teknik (board 04)

| Kontrol | Sonuç |
|---|---|
| r5 auto-rig | taze editör, rig sonucu kontrolüyle; fit ort. 0,017 / maks 0,35 mm; 858 morph; DNA bağlı |
| 54 rig pozu | temiz: göz kırpma tam kapanıyor (yeni kapakla), tek göz kırpma, bakış, kaş, çene, ağız, konuşma biçimleri, burun deliği |
| Hareket 27 + eğim 5 (r5 + h65a) | saç başla birlikte; kök kopması, kulak/boyun kesişmesi yok |
| Kilitli dosyalar | m2, M DNA, M_SlightArch ve M bağlamaları, h51a özetleri geri dönüş kaydıyla aynı; korunan eski adaylar 89/89 |
| LOD | TEST EDİLMEDİ |

**Yol üstündeki iki hata, düzeltildi:**
- Rig betiklerinin R kopyası oluşturulurken iki O betiği (`gd11ro_face_run.sh`, `gd11ro_frames.sh`) yanlışlıkla sıfırlandı. Biri korunan kopyadan, diğeri türetildiği N betiğinden geri yüklendi; içerik hata öncesiyle aynı.
- İlk üç kompozisyonda Git Bash saç bağlama yollarını bozdu. O çekimler silinip yeniden yapıldı.

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| TOPUZ ALTI DOĞALLIK VE BOLLUK | BAŞARILI (ana yapı + gevşek katman; referanstan hâlâ biraz daha düzenli) |
| YÜZ KARAKTERİ (bakış / kapak) | KISMEN-İYİ (referans yönünde belirgin) |
| YÜZ BİÇİMİ / YAPISI | KISMEN (alt yanak hafif; çene boyu, burun ve dudak bilerek değiştirilmedi) |
| KİMLİK KORUNUMU | BAŞARILI (aynı kişi) |
| TEKNİK ÇALIŞIRLIK | BAŞARILI (LOD TEST EDİLMEDİ) |

## Board'lar

`boards/01_REF_BEFORE_AFTER.jpg` referans | önce | sonra · `02_BELOW_BUN.jpg` topuz altı h64a ile h65b karşılaştırması · `03_FACE.jpg` referans, m2, r5 + kil + ısı haritası · `04_TECH.jpg` rig pozları + hareket.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
