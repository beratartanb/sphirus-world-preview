# GD11 tur BB: yüz oranı: burun kısaltma, uç ve sırt yükseltme (y1 → b3 / b4)

Tarih: 2026-10-06. Durum: **KULLANICI SEÇİMİ İÇİN DURDURULDU.** Üretime geçirilmedi.

Kullanıcı gözlemi: "Surat hâlâ uzun duruyor, göz-burun-ağız geniş bir alana yayılmış gibi; burun ucu bizde çok düşük, referansta oldukça yüksekte; burun sırtı da aynı şekilde."

**Taban:** y1 + k15 + M_SlightArch + e3g + S_Thin + h68e. Bu turda yalnız burun değişti; kaş, göz, ağız ve çene sabit.

## Teşhis: ölçüm

Yüz noktaları çözülmüş ön referans kamerasında ölçüldü. Dikey mesafeler göz merkezleri arası uzaklığa bölündü (`data/prop_*.txt`, yeni araç `blender_g11rbb_prop.py`; referans için göz kapağı ve dudak izleri `g11rbb_propref.py`).

| Mesafe (göz hizasından) | Referans | Taban y1 | **B3** | **B4** |
|---|---|---|---|---|
| burun ucu | 0,525 | 0,631 | 0,554 | **0,503** |
| burun altı (subnasale) | 0,685 | 0,809 | 0,820* | **0,702** |
| ağız (stomion) | 1,13 | 1,10 | 1,10 | 1,10 |

\* B3'te burun altı nokta tespiti kararsız; ara değer olarak okunmalı.

Tur U'daki baş eğimi taraması ayrıca kontrol edildi (−6° ile +8° arası): burun altı her eğimde referanstan 7–11 mm aşağıda. Yani fark poz değil, biçim.

**Sonuç:** gözler ve ağız referansla aynı yerde. Yüzü "uzun ve yayılmış" gösteren şey burnun uzun ve sarkık olması: burun tabanı yaklaşık 7–9 mm, uç 3–6 mm aşağıda. Buna karşılık burun ile ağız arası (filtrum) kısa kalmış. Profilde bizim burun ucu aşağı dönük ve sırt hafif çukur; referansta sırt düz ve uç yukarıda.

## Yapılan (yalnız burun)

| İşlem | B3 (yarım) | B4 (tam) |
|---|---|---|
| Burun tabanı (kolumella, delikler, kanatlar, uç) yukarı; dudağın üst kenarı sabit, aradaki filtrum uzar | 3,5 mm | 6 mm |
| Uç ek yukarı dönüş | 1 mm | 1,5 mm |
| Burun sırtı öne (düz profil) | 0,5 mm | 0,8 mm |

Bölge ölçümü B4 (`data/heat_B4_vs_y1.txt`):
- burun en çok 7,5 mm;
- dudak bölgesi ortalama 0,18 mm, en çok 4,6 mm (filtrumun dudakla birleştiği kenar);
- ağız açıklığı, köşeler ve çene 0,00 mm;
- göz kapakları ortalama 0,004 mm (iç köşeye yakın tek noktada 1,4 mm);
- yanak ortalama 0,03 mm.

İlk deneme (B1/B2) gözün altına ve dudağa taşıyordu (kapak 4 mm, ağız yukarı kayıyordu). Reddedildi, maskeli alanla yeniden yapıldı.

## Gözlemlerim (karar kullanıcının)

- **B4:** profilde burun belirgin biçimde kısaldı, uç yukarıda, sırt düz. Referans profiline en yakın olan bu. Önden yüz daha kısa okunuyor. Bedeli: önden burun delikleri biraz daha görünür ve burun-dudak arası daha uzun; referansta da öyle.
- **B3:** aynı yönde, daha az.

## Teknik

| Kontrol | Sonuç |
|---|---|
| b3 ve b4 auto-rig | taze editör, rig kapısıyla; fit ort. 0,019 / 0,020 mm, maks 0,352 mm; göz 0,000; 858 morph; DNA bağlı |
| b3 / b4 27 rig pozu (board 05) | temiz; burun deliği sıkma/açma, ağız, konuşma biçimleri, gülümseme ve göz kırpma sorunsuz |
| Kilitli dosyalar | geri dönüş kaydıyla aynı; korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ |

## Board'lar

- `01_PROFILE_NOHAIR.jpg`: saçsız, yumuşak ışık: referans / taban / B3 / B4 (profil, 3/4, ön).
- `02_REF_CAMERA.jpg`: çözülmüş referans kamerasında aynı karşılaştırma.
- `03_WITH_HAIR.jpg`: saçlı görünüm.
- `04_CLAY.jpg`: kil y1 / B3 / B4 ve referans.
- `05_TECH_RIG_b3.jpg`, `05_TECH_RIG_b4.jpg`: 27'şer rig pozu.

Kaynaklar: `SourceAssets/Characters/GD11_ProportionBB_20261006`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI SEÇİMİ İÇİN DUR.**
