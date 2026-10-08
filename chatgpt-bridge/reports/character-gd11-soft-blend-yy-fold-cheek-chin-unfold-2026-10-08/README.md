# GD11 tur YY: burun-dudak kıvrımı yanağa açıldı, göz-burun ucu, yüz katlanmaları onarıldı, çene çıkıntısı (yy9)

Tarih: 2026-10-08. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi.

## Kullanıcı istekleri (xx10 üzerine)

1. Göz altından buruna "uç" hâlâ garip; daha yumuşak olsun, kenarları yumuşasın.
2. Dudak kenarlarından yukarı uzanan kas yanaklara doğru genişlesin ve yumuşasın. xx10'da tersine dudağa yaklaşmış ve hâlâ keskin.
3. İşaretli yerler: yanak çukuru ve ağız köşesi altı (önden ve 3/4'ten).
4. Çene ucunun yan profilde referanstaki gibi yumuşak bir çıkıntısı yok.

| | Yüz | Cilt | Saç |
|---|---|---|---|
| Önce | xx10 | x19a | h72d |
| Sonra | **yy9** | x19a | h72d |

İris e3n ve kaş M_SlightArch (m3 tablosu) değişmedi. Önceki varlıklar değiştirilmedi.

## Bulgu: yüzeyde katlanmalar

Bütün adaylarda keskin kıvrım taraması yaptım (iki komşu üçgen arasında 120 dereceden fazla açı). Temel kafada doğal olarak yaklaşık 45 tane var: dudak köşesi içi, burun delikleri.

| Sürüm | Ön yüzde keskin kıvrım | Nerede |
|---|---|---|
| vv2 | 42 | doğal düzey |
| ww12 | 113 | ağız ve dudak çevresi (WW'deki üst dudak ve çene profil işlemleri) |
| xx10 | 138 | ek olarak göz-burun birleşimi ve kulak önü |
| **yy9** | **43** | vv2 düzeyine döndü |

Bu katlanmalar render'da küçük koyu çentik ve kırışık olarak görünür. Gördüğün ağız köşesi kırışıklığı ve göz-burun "ucu"nun bir kısmı bunlardan geliyordu.

**Onarım (`blender_g11yy_unfold.py`):** Katlanan üçgenler vv2'ye göre bulunur. Yalnız o şeritte değişim miktarı yumuşatılır, düzenlemelerin geri kalanı yerinde kalır. Katlanmış üçgen sayısı 1156'dan 32'ye indi; değişim katlanma şeritlerinde en çok 3,5 mm.

## Yapılanlar

| # | İstek | İşlem | Ölçüm |
|---|---|---|---|
| 2 | Kıvrım yanağa açılsın | Sırtın tepesi alçaltıldı. Dış tarafa ve ağız köşesi altına geniş, yumuşak dolgunluk eklendi; sonra gevşetme. | Sırt ortalama 1,8 mm (en çok 3 mm) alçaldı. Dış dolgu en çok 2,4 mm. Ağız köşesi altı oluğu −3,5'ten −2,2 mm'ye, yanak çukuru ortalaması −0,47'den −0,27 mm'ye. |
| 1 | Göz-burun ucu | Burun yanına yalnız doldurma rampası (en çok 2,8 mm). Burun sırtı koruması daraltıldı. Konumların gevşetilmesi ve katlanma onarımı. | Birleşim köşesi yaklaşık 2 mm dolduruldu. |
| 4 | Çene çıkıntısı | Çene ucuna yumuşak, yuvarlak öne çıkıntı (+2,6 mm). Dudak altı kıvrımı korundu. | Çene ucu dudak altı kıvrımından 2,1 mm yerine 4,5 mm önde; kavis yuvarlak. |

**Çene orta hat profili (y, cm):**

| z | 151,75 | 152,0 | 152,25 | 152,5 (çene ucu) | 152,75 | 153,25 (dudak altı kıvrımı) |
|---|---|---|---|---|---|---|
| xx10 | 12,06 | 12,58 | 12,73 | 12,82 | 12,80 | 12,61 |
| yy9 | 12,15 | 12,74 | 12,97 | **13,06** | 12,97 | 12,61 |

## Elenen ara sürümler

| Sürüm | Sorun |
|---|---|
| YY1 | Göz-burun dolgusu, burun sırtı korumasının kenarında katlanma yaptı (54 ters üçgen). |
| YY2, YY3 | Normal yönünde dolgu V şeklindeki köşede üçgenleri katlıyordu; onarım dolguyu da geri alıyordu. |
| YY4 | Yalnız gevşetme, köşede yetersiz. |
| YY5 | Temiz ama kıvrımın yanağa açılması zayıftı. UE'de denendi; ara varlık `SKM_G11RR_Face_yy5`. |
| YY6–YY8 | Kıvrım tepesini alçaltmak tek başına zirveyi dudağa doğru kaydırıyordu (tam şikâyet ettiğin şey). Dış dolgu eklenene kadar yetersiz. |

## Dürüst değerlendirme

| İstek | Durum | Not |
|---|---|---|
| Kıvrım yanağa açılsın, yumuşasın | **KISMEN** | UE'de ağız çevresi ve yanak geçişi daha dolgun ve yumuşak; ağız köşeleri daha az sıkışık. Kıvrımın dudağa yakın sırtı hâlâ belirgin (yerel kabartı yaklaşık 3 mm). Dolgunluk biraz daha artırılabilir, ama alt yüz genişlemeye başlar. |
| Göz-burun ucu | **KISMEN** | Katlanma ve kırışık giderildi, köşe yumuşadı. Burun yan duvarı ile yanak arasındaki doğal köşe hâlâ var; yerel kabartı ölçüsü değişmedi (2,47). |
| İşaretli yanak çukuru ve ağız köşesi altı | **KISMEN** | İkisi de doldu, ağız köşesi altı daha belirgin biçimde. |
| Çene çıkıntısı | **BAŞARILI (biçim)** | Yandan yumuşak, yuvarlak bir çıkıntı var; kel referanstaki kavise yakın. Çene boyu değiştirilmedi. |
| Katlanma onarımı | **BAŞARILI** | Ön yüzde keskin kıvrım 138'den 43'e indi. Ağız çizgisi ve köşeleri temiz. |

## Teknik

| Kontrol | Sonuç |
|---|---|
| yy9 | vv2 kopyası + doğrudan fark (YY9 − VV2), 9873 köşe, en çok 6,1 mm. Normaller ve teğetler yeniden; 858 morph ve DNA korundu. |
| Rig pozları ve hareket kareleri | 27 + 27, temiz |
| Kilitli dosyalar | geri dönüş kaydıyla aynı (7); korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ |

**Yeni araç:** `blender_g11yy_unfold.py` (katlanma onarımı). `blender_g11xx_soften6.py` dosyasına burun sırtı koruma genişlikleri eklendi (`CORE_AX_UP`, `NOSE_AX_UP`); varsayılan değerler xx10'u değiştirmez.

**Ara varlık:** `SKM_G11RR_Face_yy5` (silinmedi).

## Board'lar

| Dosya | İçerik |
|---|---|
| `00_BEFORE_AFTER.jpg` | önce (xx10) / sonra (yy9) / referans |
| `01_FACE_NOHAIR.jpg` | saçsız yüz |
| `02_FORMS.jpg` | kabartı haritası, dokusuz yüz, çene orta hattı kel referans üstünde |
| `04_REF_CAMERA.jpg` | referans kameraları, %50 bindirme |
| `05_TECH_Rig_yy9.jpg`, `05_TECH_Mot_yy9.jpg` | rig pozları ve hareket kareleri |

Board'lar `boards/`, ölçümler `data/`, araçlar `tools/` klasöründe. Kaynaklar: `SourceAssets/Characters/GD11_SoftBlendYY_20261008`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
