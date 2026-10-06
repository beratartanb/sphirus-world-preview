# GD11 tur FF: alt yüzü önden inceltme, daha az geniş ve erkeksi çene (E1 → F1 / F2)

Tarih: 2026-10-07. Durum: **KULLANICI SEÇİMİ İÇİN DURDURULDU.** Üretime geçirilmedi.

Kullanıcı isteği: "Suratı biraz daha oturtabiliriz gibi ve böylelikle çene önden geniş ve erkeksi durmayabilir."

**Taban:** E1 (tur EE) + k15 + M_SlightArch + e3g + S_Thin + h68e. Göz, burun, dudak, ağız hizaları, kulak ve çenenin öne çıkıntısı ile uzunluğu bu turda sabit.

## Yapılan (yalnız alt yüz genişliği)

| İşlem | F1 | F2 |
|---|---|---|
| Çene yanları içe (çene ucu daha dar) | 1,5 mm | 2,6 mm |
| Çene köşeleri geriye (köşeli değil yuvarlak çene) | 1,0 mm | 1,7 mm |
| Çene açısı (gonion) içe | 2,5 mm | 4,3 mm |
| Ağız dışı alt yanak içe | 1,5 mm | 2,6 mm |

Bölge ölçümü E1'e göre:
- F1: çene/alt yüz en çok 1,8 mm, yanak en çok 1,8 mm;
- F2: çene en çok 3,1 mm, yanak en çok 3,1 mm, çene açısı arkasında en çok 3,7 mm;
- her ikisinde: burun, göz ve kulak 0,00 mm; dudaklar ortalama 0,02–0,03 mm.

Çene altından 4,5 cm yukarıda, ön yarıdaki alt yüz genişliği (`data/jaw_widths.txt`):

| | E1 | F1 | F2 |
|---|---|---|---|
| genişlik | 9,68 cm | 9,41 cm | 9,21 cm |

## Gözlemlerim (karar kullanıcının)

- **F2:** önden alt yüz belirgin biçimde daha dar ve çeneye doğru V biçiminde daralıyor. Çene açısı yumuşadı, erkeksi kare görünüm azaldı.
- **F1:** aynı yönde, daha hafif.
- **Profil:** E1 ile aynı; çene çıkıntısı korundu.

## Teknik

| Kontrol | Sonuç |
|---|---|
| f1 ve f2 auto-rig | taze editör, rig kapısıyla; fit ort. 0,019 / 0,020 mm, maks 0,349 mm; göz 0,000; 858 morph; DNA bağlı |
| f1 / f2 27 rig pozu (board 05) | temiz; çene açma, sağa/sola çene, konuşma, gülümseme |
| f2 hareket 27 kare (board 06) | temiz |
| Kilitli dosyalar | geri dönüş kaydıyla aynı; korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ |

## Board'lar

- `01_NOHAIR_FRONT.jpg`: saçsız, yumuşak ışık: referans / E1 / F1 / F2 (ön, 3/4, profil).
- `02_REF_CAMERA.jpg`: çözülmüş referans kamerası.
- `03_WITH_HAIR.jpg`: saçlı görünüm.
- `04_CLAY.jpg`: kil.
- `05_TECH_RIG_f1.jpg`, `05_TECH_RIG_f2.jpg`: 27'şer rig pozu.
- `06_TECH_MOTION_f2.jpg`: 27 hareket karesi.

Kaynaklar: `SourceAssets/Characters/GD11_ChinWidthFF_20261007`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI SEÇİMİ İÇİN DUR.**
