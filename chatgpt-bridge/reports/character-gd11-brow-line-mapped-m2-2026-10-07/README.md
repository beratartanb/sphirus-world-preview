# GD11 kaş çizgisi m2: referansa noktadan noktaya eşleme (SS4 + M_SlightArch, yüz değişmeden)

Tarih: 2026-10-07. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi.

Kullanıcı (−3,7 mm sürümü için): "Tutarsız bir incelme kalınlaşması var, ayrıca kıvrım pozisyonları aynı değil."

## Teşhis

Önceki −3,7 mm sürümü iki sorun içeriyordu.

1. **Tek parça kaydırma.** Ölçünce gereken kaydırmanın kaş boyunca değiştiği görüldü:

   | Bölge | Gereken kaydırma |
   |---|---|
   | Kaş başı | yaklaşık 1,6 mm |
   | Orta ve dış kavis | 3,0–3,7 mm |
   | Kuyruk | yaklaşık 1 mm |

   Referansın kavis tepesi bizimkinden daha dışarıda. Tek parça 3,7 mm, kaş başını fazla indirdi ve kavisin yerini taşıdı.
2. **Kenar geçişi kaşın içinden geçiyordu.** Kaydırma alanının sınırı kuyruk ve kaş başından geçtiği için bu bölgeler ortadan farklı miktarda kaydı. Ölçülen kalınlık (sapma, piksel):

   | | Kuyruk | Orta |
   |---|---|---|
   | SS4 orijinal | 6,5 | 7–8 |
   | −3,7 mm | **4,7** | — |
   | m2 | 6,7 | 7,5 |

## Yöntem

- **Bizim kaş:** referans kamerasında kaşlı ve kaşsız iki çekimin farkından kesin tüy maskesi çıkarıldı.
- **Referans:** her sütunda kaşın koyuluk ağırlıklı orta çizgisi ve kalınlığı ölçüldü (`tools/blender_g11bb_browfit.py`). Kaş arası gölge ve kırışıklıklar ile kuyruktaki saç telleri dışarıda bırakıldı.
- **Eşleme:** kaş boyunca her noktada referans ile bizim aramızdaki yükseklik farkı tabloya alındı; sağ ve sol ortalanarak simetrik tutuldu.
  - Bu tablo, kaşın bağlandığı şablon kafa kopyasına uygulandı. Kaydırma alanı artık kaşın tamamını rahatça kapsıyor; hiçbir kök geçiş bölgesinde değil.
  - İlk turda (m1) dış kavis fazla kaydı, çünkü kaynak kafa orada yanlara doğru eğimli. Ölçülen tepkiye göre tablo düzeltildi (m2).
- **Yüz, rig, deri ve kaş tipi değişmedi.**

## Sonuç (referans ön kamerası; referans ile bizim orta çizgi farkı)

| | Sol kaş (ort. mutlak fark) | Sağ kaş |
|---|---|---|
| SS4 orijinal | 7,5 px ≈ 2,5 mm (bizimki yukarıda) | 9 px ≈ 3 mm |
| m1 | 4,2 px (dış kavis fazla aşağıda) | 1,8 px |
| **m2** | **1,9 px ≈ 0,6 mm** | **1,0 px ≈ 0,3 mm** |

- Sol kuyruktaki kalan küçük fark (−4,5 px) referansın kendi asimetrisinden geliyor; kaşlar simetrik tutuldu.
- `06_BROW_FIT_LINES.jpg`: m2'nin orta çizgisi ve kalınlık sınırları, referans fotoğrafının üzerinde.

## Kalanlar (dürüst durum)

- **Kaş başı kalınlığı:** referansta kaş başı daha kalın görünüyor (10–12 px; bizde 7–8). Ölçüme göz çukuru gölgesi de karışıyor. Kalınlık, tüy yoğunluğuna bağlı bir groom özelliği; kökleri yayarak kalınlaştırmak kaşı seyreltir. Bu turda değiştirilmedi.
- **Kuyruk:** referansta kuyruğun ucu saçın altında kalıyor. Bizim kuyruğumuzun uzunluğu ve biçimi korundu.
- **Renk:** değiştirilmedi.

## Teknik

| Kontrol | Sonuç |
|---|---|
| Yüz ve rig | değişmedi (ss4) |
| Kaş ifade pozları (9) | kaş deride, kopma veya yüzme yok |
| Kilitli dosyalar | geri dönüş kaydıyla aynı (7); korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ |

Yeni varlıklar (kütüphane dokunulmadı):
- `GD11_FaceR_20261006/Grooms/BrowSrc/SKM_G11BB_BrowSrc_m1|m2`
- `Grooms/GR_G11BB_Eyebrows_m1|m2`
- `Face/Bindings/GB_G11RR_EyebrowsCustom_m1|m2_ss4h48a`

## Board'lar

| Dosya | İçerik |
|---|---|
| `05_BROW_MAPPED_m2.jpg` | SS4 kaşı / −3,7 mm tek parça / m2 / referans: yakın plan, ön, 3/4 ve saçlı |
| `06_BROW_FIT_LINES.jpg` | orta çizgi ±1 sapma; turkuaz bizim, mor referans |
| `07_TECH_RIG_m2.jpg` | kaş ifadeleri |

Kaynaklar: `SourceAssets/Characters/GD11_BrowLineBB2_20261007`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
