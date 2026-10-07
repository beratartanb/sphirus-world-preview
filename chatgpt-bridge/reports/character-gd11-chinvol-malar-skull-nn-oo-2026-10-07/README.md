# GD11 turlar NN + OO: çene hacmi (M5 → N6), elmacık yanağa ve baş arkası (N6 → O4)

Tarih: 2026-10-07. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi.

## Kullanıcı istekleri

1. "Çene hacmi ve görüntüsü hâlâ büyük; formunu bozmadan referanstaki gibi hacmini küçült."
2. "Elmacık kemikleri referansta biraz daha yanakta, yani surat kafada güzel şekilde oturuyor ve baş arkası daha düzgün. N6'yı yaparken bunları da yap."

İşaretler: `data/user_markup_cheek.jpg`, `data/user_markup_skull.jpg`. Yeni kel profil referansı: kaynaklardaki `ref_bald_profile.png`.

**Taban:** M5 + k15 + M_SlightArch + e3g + S_Thin + h68e.

## N6: çene hacmi (`data/N6.json`)

**Teşhis:**
- Önden çene genişliği ve boyu referansla uyumluydu.
- Büyük okumanın kaynağı, tur CC'deki çene çıkıntısının öne taşan kütlesi.
- Bir de 3/4'te görünen yan çene kütlesi vardı: 3/4 referans kamerasında çenenin uzak konturu referansın 7–9 mm dışındaydı. Bu konturu x ≈ 3,5–3,9 cm'deki köşeler oluşturuyordu.

**Yapılan:**

| İşlem | Değer |
|---|---|
| Çene yastığı geri | 4,5 mm |
| Yan çene kütlesi geri | 4,5 + 2,7 mm |
| Çene yanları dar | 1,2 mm |

Çene boyu korundu (oran 0,736). Dudaklar ve ağız köşeleri 0,00 mm. Kısaltan bir deneme (N5) elendi.

## O4: elmacık ve baş arkası (`data/O4.json`)

**Elmacık:**
- Bizde elmacık kütlesi yukarıda ve yanda, kulağa yakın duruyordu; referansta öne ve aşağıya, yanağın üzerine oturuyor.
- Yan elmacık çıkıntısı 1,8 mm azaltıldı.
- Göz altı ile burun kanadı hizası arasında yanağın önüne 2,7 + 1,2 mm dolgu eklendi.
- Göz kapakları ve dudaklar 0,00 mm.

**Baş arkası:**
- Kel profil referansıyla yan silüet karşılaştırıldı (`blender_g11roo_baldprof.py`, tragus ve dış göz köşesine hizalı).
- İşaretli bölgedeki tepe-arka çıkıntısı, tur U'da kafa formu için eklenen 6 mm'lik radyal büyütmeden geliyordu.
- O4'te bu çıkıntı yuvarlak bir eğriyle geri alındı: tepe-arkada en çok 13 mm.
- Orta hat arka profili: z 168'de −5,52 → −4,34 cm, z 170'te −4,36 → −3,13 cm.
- Kafanın en arka noktası (z 164–166) yalnız 3–6 mm değişti; yüz ve kulak dokunulmadı (kulakta en çok 3 mm, sınır sönümü).
- Saç kökleri yeni yüzeye oturdu; profilde ve arkadan kopma ya da boşluk görülmedi (board 03).

## Gözlemlerim (karar kullanıcının)

- **N6:** çene daha küçük ve daha az çıkık; biçim korundu.
- **O4 elmacık:** 3/4'te yanak önü daha dolu, yan elmacık daha az çıkık.
- **O4 baş arkası:** profilde tepe-arka köşesi yok; kafa referanstaki gibi tek, düzgün bir kubbe olarak okunuyor.

## Teknik

| Kontrol | Sonuç |
|---|---|
| n6 ve o4 auto-rig | taze editör, rig kapısıyla; fit ort. 0,021 mm, maks 0,280 mm; göz 0,000; 858 morph; DNA bağlı |
| n6 ve o4 27 rig pozu / 27 hareket karesi | temiz |
| Kilitli dosyalar | geri dönüş kaydıyla aynı; korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ |

## Board'lar

- `01_FACE_COMPARE.jpg`: M5 / N6 / O4; ön, 3/4, çene.
- `02_HEAD_SHAPE.jpg`: kafa profili ve arka 3/4: N6 / O4 ile kel referans.
- `03_WITH_HAIR.jpg`: saçlı görünüm.
- `04_REF_CAMERA.jpg`: çözülmüş referans kameraları.
- `05_CLAY.jpg`: kil.
- `06_TECH_RIG_o4.jpg`, `07_TECH_MOTION_o4.jpg`: rig pozları ve hareket.

Kaynaklar: `SourceAssets/Characters/GD11_ChinVolMalarSkullNNOO_20261007`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
