# GD11 tur AA: kaş geri alındı, kaş dışı tekli iyileştirme adayları

Tarih: 2026-10-06. Durum: **KULLANICI SEÇİMİ İÇİN DURDURULDU.** Üretime geçirilmedi.

Kullanıcı kararı: "Önceki kaşa geri dön, bu kontrolden geçmedi. Kaş dışında diğer iyileştirmeler ile devam et." M_Natural kaş ve kaş başı ekleri (z1–z3) adaydan çıkarıldı. Varlıkları yalnızca kayıt olarak duruyor.

**Yeni taban** (board 00): y1 yüz (azaltılmış kapak örtüsü) + k15 ten + **M_SlightArch** kaş + e3g iris + S_Thin kirpik + h68e saç.

Her adayda **yalnızca bir değişiklik** var. Her biri tabanla aynı editör oturumunda, aynı ışıkla ve time=0 ile çekildi (`prov/`).

| Aday | Tek değişiklik | Ölçüm (y1'e göre) | Varlık | Board |
|---|---|---|---|---|
| **A1 burun** | uç inceltme 1 mm, uç 0,8 mm yukarı, sırt inceltme 0,9 mm, kanat daraltma 1,8 mm | burun en çok 1,45 mm; dudak kenarında 0,68 mm sönüm; göz, yanak ve çene 0,00 mm | `SKM_G11RR_Face_a1` / `MHC_G11RR_A1_Head` | `01_A1_NOSE.jpg` |
| **A2 ağız** | Cupid yayı ve dudak kenarı tanımı, alt dudak çıkıklığı 0,75 mm azaltıldı, üst dudak 0,6 mm inceltildi. Ağız genişletilmedi, köşeler değişmedi. | dudak en çok 0,73 mm; göz, yanak ve çene 0,00 mm | `SKM_G11RR_Face_a2` / `MHC_G11RR_A2_Head` | `02_A2_MOUTH.jpg` |
| **A4 saç** | yüzü çerçeveleyen daha çok ve daha dalgalı teller | ana saç h68e ile aynı | `GR_LK_Hair_*_h69a` (`GB_G11RR_Hair*_y1h69a`) | `03_A4_HAIR.jpg` |

**A3 (kaş arası çizgileri kaldırma) sunulmadı.** Tur W'deki çizgi geometride yalnızca 6 noktada en çok 0,4 mm'lik bir iz bırakmış. Dokulu görüntüde ayırt edilemeyeceği için rig'lenmedi. Kaş arasında görülen çizgiler ten dokusundan geliyor, geometriden değil.

## Gözlemlerim (karar kullanıcının)

| Aday | Görsel etki |
|---|---|
| A1 | Burun önden belirgin biçimde daha ince ve daha rafine; uç daha az yumru, kanatlar daha dar. Kimlik korunuyor. |
| A2 | Hafif: dudak kenarı daha net, alt dudak daha az çıkık. Etkisi küçük. |
| A4 | Yüz kenarında daha çok dalgalı tel. Referanstaki çerçeveye bir adım; önden yüzü biraz daraltıyor. |

## Teknik

| Kontrol | Sonuç |
|---|---|
| a1 ve a2 auto-rig | taze editör, rig kapısıyla; fit ort. 0,018 / maks 0,352 mm; göz 0,000; 858 morph; DNA bağlı |
| a1 / a2 27 rig pozu (board 05) | temiz; göz kırpma, konuşma biçimleri, burun deliği sıkma/açma ve gülümseme sorunsuz |
| Kilitli dosyalar | geri dönüş kaydıyla aynı; korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ |

Kaynaklar: `SourceAssets/Characters/GD11_SingleAA_20261006`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI SEÇİMİ İÇİN DUR.** Seçilen adaylar bir sonraki adımda tek kompozisyonda birleştirilir; geometri birleşimi yeni bir rig gerektirir.
