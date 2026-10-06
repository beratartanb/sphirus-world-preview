# GD11 tur JJ: alt yüzü kafaya yayma, çene ve çene kemiği (H6 → J5 / J6)

Tarih: 2026-10-07. Durum: **KULLANICI SEÇİMİ İÇİN DURDURULDU.** Üretime geçirilmedi.

Kullanıcı: "H6 iyi gibi ancak surat hâlâ sivri, ince, uzun okunuyor. Referansla tekrar eşleştirip suratı kafaya daha iyi yayalım; çene ve çene kemiği üzerinde üst seviye çalışalım."

**Taban:** H6 (F2 + G2 göz altı + H6 yanak) + k15 + M_SlightArch + e3g + S_Thin + h68e.

## Teşhis

Çözülmüş referans kameralarında karşılaştırma (`blender_g11rt_measure.py`, ön ve 3/4 maske bindirmesi) ve çene alt kenarının yükseklik profili:
- Elmacık ve orta yanak genişliği referansla örtüşüyor; üst yanakta bizimki 2–6 px daha geniş.
- Bizim çene alt kenarı çene ucundan (z ≈ 151,0) yanlara doğru hızla yükseliyor: x 3 cm'de ≈ 152,4, x 4 cm'de ≈ 153,0, x 5 cm'de ≈ 154,0. Alt yüz **V** biçiminde sivriliyor.
- Referansta çene hattı çene ucu hizasına kadar geniş ve yataya yakın: ön görünümde çene hattı noktası çene ucundan yalnızca ≈ 0,5 cm yukarıda, yarım genişlik ≈ 3,5 cm. Alt yüz **U** biçiminde.
- F2'deki çene ve çene açısı inceltmesi bu sivriliği artırmıştı.

**Araç notu:** ölçüm aracı, çene altını ayırmak için 153 cm altında ve y < 9 cm'deki her şeyi kesiyor. Bu yüzden yanal çene noktaları ("jaw", "jawbot") bu kesim düzlemine denk geliyor ve sayısal değerleri güvenilir değil. Karar görsel bindirme ve çene alt kenarı profiliyle verildi.

## J5 / J6 = H6 + `data/J5.json` / `J6.json`

| İşlem | J5 | J6 |
|---|---|---|
| Çene yanları dışa (geniş çene ucu) | 3 mm | 5 mm |
| Çene açısı dışa | 3 mm | 5 mm |
| Çene hattının alt kısmı dışa | 3 mm | 5 mm |
| Ağız dışı alt yanak dışa (F2 inceltmesinin geri alınması) | 1,5 mm | 2,6 mm |
| Çene yastığı geniş ve aşağı | 2 mm | 2 mm |

Önden yarım genişlik (y > 3 cm, ön kısım):

| | H6 | J5 | J6 |
|---|---|---|---|
| çene ucundan ~1,5 cm yukarıda | 4,07 cm | 4,36 cm | 4,62 cm |
| ~3 cm yukarıda | 4,96 cm | 5,28 cm | 5,53 cm |

Bölge ölçümü (H6'ya göre): göz, burun ve kulak 0,00 mm; dudak ortalama 0,05–0,09 mm. Değişim çene ve alt yanakta: J5'te en çok 6,2 mm, J6'da en çok 11,7 mm (çene yanı, iki genişletmenin çakıştığı nokta).

## Gözlemlerim (karar kullanıcının)

- **J6:** önden alt yüz U biçiminde, referans gibi geniş bir çene hattı ve çene. Sivri/ince/uzun okuma belirgin biçimde azaldı. Çene köşeleri hafif belirgin.
- **J5:** aynı yönde, ara değer.
- **Profil:** H6 ile neredeyse aynı.

## Teknik

| Kontrol | Sonuç |
|---|---|
| j5 ve j6 auto-rig | taze editör, rig kapısıyla; fit ort. 0,021 / 0,022 mm, maks 0,345 / 0,392 mm; göz 0,000; 858 morph; DNA bağlı |
| j5 / j6 27 rig pozu (board 06) | temiz; çene açma, sağa/sola çene, konuşma, gülümseme |
| j6 hareket 27 kare (board 07) | temiz |
| Kilitli dosyalar | geri dönüş kaydıyla aynı; korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ |

## Board'lar

- `01_NOHAIR_COMPARE.jpg`: saçsız, yumuşak ışık: referans / H6 / J5 / J6.
- `02_REF_CAMERA.jpg`: çözülmüş referans kameraları.
- `03_FRONT_BLEND.jpg`: ön referans kamerasında %50 bindirme.
- `04_WITH_HAIR.jpg`: saçlı görünüm.
- `05_CLAY.jpg`: kil.
- `06_TECH_RIG_j5/j6.jpg`, `07_TECH_MOTION_j6.jpg`: rig pozları ve hareket.

Kaynaklar: `SourceAssets/Characters/GD11_JawJJ_20261007`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI SEÇİMİ İÇİN DUR.**
