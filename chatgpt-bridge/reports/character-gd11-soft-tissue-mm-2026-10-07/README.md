# GD11 tur MM: yumuşak doku (etlenme) ve çok küçük çene küçültme (L3 → M5)

Tarih: 2026-10-07. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi.

Kullanıcı: "Çeneyi ve çene ucunu biraz daha yumuşat ve küçült ama çok küçük müdahale. Ayrıca surat birazcık kemikli ve zayıf duruyor; referanstaki gibi uygun etlenmeyi yapalım."

**Taban:** L3 + k15 + M_SlightArch + e3g + S_Thin + h68e.

## Teşhis

Yanak bölgesine son turlarda üst üste birçok küçük düzenleme uygulanmıştı: H6 kütle geri, J5 genişletme, L3 yan dolgu. Bunlar yanakta santimetre ölçeğinde küçük tümsek ve çukurlar bıraktı (kil görünümü, board 05). Kemikli ve zayıf okumanın asıl kaynağı bu ve elmacık altındaki derinlik.

Yerel çukurluk ölçümünde (1,2 cm yarıçap) elmacık ve elmacık altında en düşük değerler −1,6 / −1,9 mm. u1'de bunlar −0,3 / −0,2 mm'ydi.

## M5 (`data/M5_recipe.txt`)

1. **Yanak birleştirme (yeni araç `blender_g11rmm_lowpass.py`):** u1'den L3'e kadar birikmiş düzenleme farkı, yanak maskesi içinde yüzey üzerinde Gauss (σ 0,9 cm) ile süzüldü. Düzenlemelerin genel biçimi (yanak geri, yan dolgu, alt yüz genişliği) korunurken aradaki tümsek ve çukurlar tek bir pürüzsüz kütleye yayıldı.
2. **Çok küçük çene küçültme:** çene ucu 1 mm geri, 0,7 mm dar; yumuşatma.
3. **Yumuşak doku (etlenme):**

| Bölge | Değer |
|---|---|
| Elmacık altı | 2,2 mm |
| Alt yanak | 1,4 mm |
| Elmacık | 0,8 mm |
| Şakak | 0,8 mm |
| Çene açısı kenarı | yumuşatma |

**Bölge ölçümü (L3'e göre):**
- yanak en çok 3,6 mm;
- çene en çok 2,3 mm;
- alt göz kapağı bandı en çok 1,8 mm (ortalama 0,1);
- ağız köşesi en çok 2,3 mm (ortalama 0,2);
- dudak ortası 0,06 mm;
- göz kapağının üstü 0,00 mm.

**Elenen:** M7, kapak ve ağız köşesi tamamen korunarak birleştirme yaptı ama yanak tümsekleri geri geldi. M6 (daha güçlü etlenme) M5 ile neredeyse aynı.

## Gözlemlerim (karar kullanıcının)

Yanaklar daha dolu ve pürüzsüz, yüz daha az kemikli ve zayıf okunuyor. Çene çok az daha küçük ve yumuşak. Referans konturuyla kontur farkları değişmedi (orta yanak +1–2 mm, alt yanak +1–2 mm); değişiklik yüzey kalitesinde.

## Teknik

| Kontrol | Sonuç |
|---|---|
| m5 auto-rig | taze editör, rig kapısıyla; fit ort. 0,020 / maks 0,280 mm; göz 0,000; 858 morph; DNA bağlı |
| m5 27 rig pozu / 27 hareket karesi | temiz; gülümseme ve yanak sıkmada yanak doğal |
| Kilitli dosyalar | geri dönüş kaydıyla aynı; korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ |

## Board'lar

- `01_COMPARE.jpg`: referans / L3 / M5; ön, 3/4 ve çene; yumuşak ve stüdyo ışığı.
- `02_REF_CAMERA.jpg`, `03_FRONT_BLEND.jpg`: referans kameraları ve bindirme.
- `04_WITH_HAIR.jpg`: saçlı görünüm.
- `05_CLAY.jpg`: kil denemeleri.
- `06_TECH_RIG_m5.jpg`, `07_TECH_MOTION_m5.jpg`: rig pozları ve hareket.

Kaynaklar: `SourceAssets/Characters/GD11_SoftTissueMM_20261007`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
