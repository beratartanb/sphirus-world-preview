# GD11 tur UU: yumuşak dolgunluk, göz altı → burun geçişi, kestane saç, açık iris, alçak kaş başı (uu31c)

Tarih: 2026-10-07. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi.

## Kullanıcı istekleri

1. Saçta iki yandan ayrı kütle halinde sarkaç gibi inen teller olmasın.
2. Saç rengi kızıl değil, referanstaki gibi kestane olsun.
3. Yüz oyun içinde fazla köşeli ve kaslı; yanaklarda referanstaki etlenme yok.
4. Kaş başları burun üstünde biraz fazla yukarıda.
5. Göz altından burna doğru yükselti eksik; önden ve yandan oyuk duruyor.
6. Yüz hattı dikey okunuyor; daha yatay olmalı, çene kenarı yumuşamalı.
7. Gözler fazla koyu.

Geri bildirimle netleşen tarifler:
- **5'in tarifi:** "dikey yüksek bir parça değil, göz altından burun üst kemerine bir rampa ya da düzlük"; daha sonra "elmacık kemiğinden burun üstüne uzanan kusursuz ve yumuşak bir yükselti".
- **Ara sürüm uu11b için:** "burna koyduğun kas garip ve dışarıda; kaslı görünüm artmış".

| | Yüz | Cilt | İris | Saç | Kaş |
|---|---|---|---|---|---|
| Önce | ss4j | k17 | e3m | h70c | m2j |
| Sonra | **uu31c** | **k18** | **e3n** | **h71b** | m3 (kaş başı aşağıda) |

Önceki varlıklar değiştirilmedi.

## Ne yapıldı

| # | Sonuç |
|---|---|
| 1 | **h71b:** yapışık sarkan tutamlar kapalı; yanlarda ince, dağınık teller. En uzun yan çerçeve telleri çıkarıldı. Şakak üstü teller kaldı. |
| 2 | Renk melanin 0,55 / kırmızılık 0,40. h71a (0,62/0,38) fazla koyuydu. |
| 3 | Yanak ve orta yüz hacmi koruyan bir yumuşatmayla düzeltildi (kaslı dalgalanma azaldı). Yerel kabarıklıklar yerine çok geniş, düşük bir dolgunluk eklendi. |
| 4 | Kaş başları yaklaşık 0,7–1 mm aşağı (eşleme tablosu m3). Kaş tipi aynı. |
| 5 | Göz altından burun sırtına geniş (yarıçap 2 cm'nin üstünde) ve yaklaşık 2 mm'lik yumuşak bir yükselti. Kenar, sırt ya da oluk yok. |
| 6 | Yanlarda yatay genişlik +1,6 mm, çene açısı yumuşatma, çene kenarı yumuşatma. Ölçümle ön konturlar zaten referansa yakındı; "dikey" okumanın büyük kısmı gölgeli oluklardan geliyordu. |
| 7 | İris e3n: e3g ile e3m arası açık kahve. |

Cilt k18: k15 tonu ve detayı, yalnız mat (k16/k17'deki ek bölgesel detay kaldırıldı; kaslı gölgeye katkı yapıyordu).

## Yanlış giden denemeler (hepsi elendi)

- **UU4 dikey kabarıklık:** reddedildi ("dikey yüksek parça").
- **UU5–9 rampa:** düz ama basamaklı ya da yamalı bir geçiş verdi.
- **UU10/11 dar bant:** ışıkta sırt ve oluk olarak okundu.
- **UU20/21 çukur doldurma:** burun ve kapak kenarında buruşuk çentikler bıraktı.
- **Rig sonrası geri yazma — üç hata bulundu ve düzeltildi:**
  1. Taşınan bölgenin normalleri güncellenmiyordu. Normaller ve teğetler yeniden hesaplanarak düzeltildi.
  2. Göz çevresinin kısmen korunması koruma bölgesinin sınırında eğim kırığı yarattı (koyu çizgiler). Koruma kaldırılarak düzeltildi.
  3. Ham fark köşe köşe yazılınca, rig'in yumuşattığı birikmiş milimetre altı işlem pürüzleri geri geldi; kaslı ve yumrulu görünümün asıl nedeni buydu. Kalan fark yüzeyde alçak geçiren süzgeçten geçirilerek düzeltildi.
- Gördüğün uu11b bu üç hatayı taşıyordu. uu31c üçü de düzeltilmiş haldir.

## Teknik

| Kontrol | Sonuç |
|---|---|
| uu11 auto-rig | taze editör, rig kapısıyla; fit ort. 0,023 cm; göz 0; 858 morph |
| uu31c | uu11 kopyası + alçak geçirilmiş kalan fark (en çok 1,6 mm), normaller ve teğetler yeniden; 858 morph ve DNA korundu |
| Rig pozları ve hareket kareleri | 27 + 27, temiz |
| Kilitli dosyalar | geri dönüş kaydıyla aynı (7); korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ (yalnız LOD0 güncellendi) |
| Disk | **C: 2,2 GB boş.** Yeni rig turlarından önce yer açılması gerekiyor. |

**Ara varlıklar:** `SKM_G11RR_Face_uu4`, `uu11`, `uu11b`, `uu11c`, `uu31`, `uu31b` (elenen ara sürümler; silinmedi).

**Yeni araçlar:** `blender_g11uu_ramp.py`, `blender_g11uu_band.py`, `blender_g11uu_smoothfill.py`, `blender_g11uu_residual3.py`, `ue_g11uu_apply2.py`, `ue_g11uu_dump_dm.py`.

## Board'lar

| Dosya | İçerik |
|---|---|
| `00_BEFORE_AFTER.jpg` | önce / sonra / sonra + dinlenik ifade / referans |
| `01_FACE_NOHAIR.jpg` | saçsız yüz |
| `02_HAIR.jpg` | saç |
| `03_REF_CAMERA.jpg` | referans kameraları |
| `04_NORMALS_FIX.jpg`, `06_UU31B.jpg`, `08_LOWPASS_uu31c.jpg` | geri yazma hatalarının teşhisi ve düzeltmesi |
| `05_SOFT_FILL_uu31.jpg` | yumuşak dolgu |
| `09_TECH_Rig_uu31c.jpg`, `09_TECH_Mot_uu31c.jpg` | rig pozları ve hareket kareleri |

Kaynaklar: `SourceAssets/Characters/GD11_SoftHorizUU_20261007`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
