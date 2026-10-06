# GD11 tur DD: burun–dudak arası normalleştirildi, burun kökü yumuşatıldı, yanaklar geri alındı (D1)

Tarih: 2026-10-06. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi.

## Kullanıcı geri bildirimi (C2b üzerine)

1. Burun–dudak arası burun düzenlemesinden sonra çok açılmıştı, C2b'de daha da açıldı. Normalleştirilsin.
2. Yan görünüşte C2b iyi. Ama yanaklar yüzün önüne doğru bastırılmış gibi; bu yüzden dudak gömük duruyor.
3. Burnun üst kısmı, iki göz arasında ikinci bir kemik gibi görünen yer yumuşasın; C2b'de daha da kalınlaşmıştı.

## D1: taban y1'den yeniden kuruldu (`data/D1.json`)

| Alan | C2b | **D1** |
|---|---|---|
| Burun tabanı (burun altı) | 6 mm yukarı | **2 mm yukarı** |
| Burun ucu (toplam) | ~7,5 mm yukarı | **~5,5 mm yukarı** |
| Burun sırtı öne | 0,8 mm, burun köküne kadar | 0,5 mm, yalnız alt yarıda |
| Burun–yanak geçişi dolgusu | 1,6 mm | **yok** (burun kökünü önden kalın gösteriyordu) |
| Burun kökü (gözler arası) | — | **0,6 mm daraltma; kaş arası kabarıklık 0,5 mm geri; yumuşatma** |
| Yanak ön kütlesi | — | **1,5 mm geri** (ağız köşesinin dışında; dudaklar ve köşeler sabit) |
| Çene | 3 mm öne, alt kenar 2 mm aşağı | aynı |

Gözlere göre oranlar (`data/prop_y1_c2b_d1.txt`):

| | y1 | C2b | **D1** | Referans |
|---|---|---|---|---|
| burun ucu | 0,631 | 0,503 | **0,538** | 0,525 |
| burun altı | 0,809 | 0,702 | **0,756** | 0,685 |
| ağız | 1,10 | 1,10 | 1,10 | 1,13 |
| burun–dudak arası (fark) | 0,29 | 0,40 | **0,34** | 0,45 |

Not: referans fotoğraftaki ölçüye göre burun–dudak arası referansta daha da uzun (0,45). Bu turda kullanıcının görsel değerlendirmesi esas alındı ve ara tabana yakın tutuldu.

**Bölge ölçümü (y1'e göre):**
- göz kapakları en çok 0,48 mm;
- yanak en çok 1,56 mm;
- dudak bölgesi ortalama 0,16 mm (dudak altı oluğu sınırında en çok 3 mm, çene işleminden);
- burun ucu en çok 5,5 mm.

**Çene konturu, referansa göre:** ön çene ucu −0,50, 3/4 çene altı −0,71 cm. C2b ile aynı.

## Gözlemlerim (karar kullanıcının)

- **Burun–dudak arası:** önden C2b'deki uzun boşluk kapandı, tabana yakın.
- **Burun ucu:** yukarıda kaldı.
- **Burun kökü:** yakın planda (board 01, alt sıra) gözler arası daha dar ve yumuşak; C2b'deki kalınlık gitti.
- **Yanak:** profil ve 3/4'te yanak ön kütlesi hafif geride. Dudakların gömüklüğü azaldı; etkisi orta düzeyde.

## Teknik

| Kontrol | Sonuç |
|---|---|
| d1 auto-rig | taze editör, rig kapısıyla; fit ort. 0,019 / maks 0,352 mm; göz 0,000; 858 morph; DNA bağlı |
| d1 27 rig pozu (board 04) / 27 hareket karesi (board 05) | temiz |
| Kilitli dosyalar | geri dönüş kaydıyla aynı; korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ |

## Board'lar

- `01_NOHAIR_COMPARE.jpg`: saçsız, yumuşak ışık: referans / y1 / C2b / D1; profil, 3/4, ön ve yakın burun kökü.
- `02_WITH_HAIR_REFCAM.jpg`: saçlı görünüm ve çözülmüş referans kamerası.
- `03_CLAY.jpg`: kil.
- `04_TECH_RIG_d1.jpg`, `05_TECH_MOTION_d1.jpg`: rig pozları ve hareket.

Kaynaklar: `SourceAssets/Characters/GD11_NormalizeDD_20261006`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
