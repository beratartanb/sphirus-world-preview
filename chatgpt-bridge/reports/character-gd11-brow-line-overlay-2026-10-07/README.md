# GD11 kaş çizgisi: referansla üst üste (SS4 + M_SlightArch, yüz değişmeden)

Tarih: 2026-10-07. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi.

Kullanıcı: "Referanstaki kaşı da üst üste koyarak aynı çizgide yapabilir misin?"

**Taban:** SS4 + k15 + e3g + S_Thin + h68e. Kaş tipi **M_SlightArch korundu**; yalnız kaşın yüzdeki konumu değişti.

## Ölçüm (referans ön kamerası, 5 piksellik ızgara, `boards/03_REF_CAMERA_GRID.jpg`)

Referans fotoğrafı ve bizim render aynı çözülmüş kamerada üst üste kondu. Göz bebekleri aynı satırda (y ≈ 411).

| | Kaş orta çizgisi (satır) | Göz bebeğine göre fark |
|---|---|---|
| Referans | ≈ 367 | — |
| SS4 (şimdiki kaş) | ≈ 355 | 12 piksel ≈ 4 mm **yukarıda** |
| −2,5 mm bağlama | ≈ 362–363 | yaklaşık 1,5 mm yukarıda |
| −3,7 mm bağlama | ≈ 367 | **referansla aynı çizgide** (≤ 1 piksel) |

Kavisin biçimi (kaş başı, tepe, kuyruk) iki kaşta benzer. Fark neredeyse tamamen yükseklikte.

## Yöntem: yüz değişmeden kaşı indirmek

- Kütüphane kaşı, MetaHuman şablon kafası (`SKM_Groom_Head_Legacy01`) kaynak alınarak yüze aktarılıyor. Şablon kafa ile yüzümüzün topolojisi aynı (33.845 köşe), bu yüzden aktarım üçgen eşleşmesiyle yapılıyor.
- Şablon kafanın bir kopyasında kaş bölgesi 2,5 / 3,7 mm yukarı kaydırıldı. Bu kopya kaynak alınınca kaş kökleri bizim yüzde aynı miktarda aşağıya oturuyor.
- **Yüz mesh'i, rig ve deri hiç değişmedi.** Kapak ve alın da aynı. Kaş ifadelerde deriyle birlikte hareket ediyor (`04_TECH_RIG_brow37.jpg`).
- Kütüphane varlıklarına dokunulmadı. Yeni varlıklar:
  - kaynak kafa kopyaları `GD11_FaceR_20261006/Grooms/BrowSrc/SKM_G11BB_BrowSrc_d25|d37`;
  - kaş kopyaları `Grooms/GR_G11BB_Eyebrows_d25|d37`;
  - bağlamalar `Face/Bindings/GB_G11RR_EyebrowsCustom_d25|d37_ss4h48a`.
- Bağlamalar ss4 yüzü için kuruldu. Başka bir aday seçilirse aynı yöntemle o yüze yeniden kurulur.

## Gözlemlerim (karar senin)

- **−3,7 mm:** kaş referansla aynı çizgide. Bakış daha ağır, kaş göze yakın; referansa benzer.
- Aşağı inen kaş, aynı groom olduğu halde **daha koyu ve dolgun görünüyor**. Kökler kapak kıvrımına yaklaşınca tüyler deriye daha yatık oturuyor ve gölge artıyor.
  - Bu referansın koyu, dolgun kaşına yakın.
  - Stüdyo ışığında ve saçlı ön görünümde bakışı sertleştiriyor (`02_WITH_HAIR.jpg`, alt sıra).
- **−2,5 mm:** daha yumuşak bir ara seçenek.
- Kaş rengi ve kalınlığı değiştirilmedi; daha önce reddedilmişti.

## Teknik

| Kontrol | Sonuç |
|---|---|
| Yüz ve rig | değişmedi (ss4) |
| Kaş ifade pozları (9) | kaş deride, kopma veya yüzme yok |
| Kilitli dosyalar | geri dönüş kaydıyla aynı (7); korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ |

## Board'lar

| Dosya | İçerik |
|---|---|
| `01_BROW_LINE.jpg` | kaş yakın plan, ön ve 3/4: SS4 / −2,5 / −3,7 / referans |
| `02_WITH_HAIR.jpg` | saçlı görünüm |
| `03_REF_CAMERA_GRID.jpg` | referans kamerasında 5 piksellik ızgara ve %50 bindirme |
| `04_TECH_RIG_brow37.jpg` | −3,7 mm ile kaş ifadeleri |

Kaynaklar: `SourceAssets/Characters/GD11_BrowLineBB2_20261007`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
