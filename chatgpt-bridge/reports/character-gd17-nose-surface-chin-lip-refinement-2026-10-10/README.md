# GD17 — Burun yüzeyi, çene yumuşak dokusu ve üst dudak uçları

Tarih: 2026-10-10. Başlangıç ve geri dönüş noktası GD16 G16; GD16'ya dokunulmadı.

Final aday **G17**. Durum: **PARTIAL**. Teknik testler geçti, ancak görsel benzerlik kabulü senin incelemene bağlı (NOT_TESTED). Bir de küçük bir regresyon var; aşağıda anlatılıyor.

**Üretim karakterine uygulanmadı.** Tüm UE varlıkları `/Game/Sphirus/CharacterLab/GD17_IdentityMaster_20261010` altında, yalnızca test amaçlı. Kaynaklar `SourceAssets/Characters/GD17_IdentityMaster_20261010` altında: `GD17_IdentityMaster.blend`, GLB/OBJ, sculpt verisi, op'lar ve araçlar.

## 1. Teşhis: sorun geometride mi, materyalde mi?

Kil ve gerçek materyal yakın planlarını aynı kamera ve ışıkta karşılaştırdım (`process/01–04`). Ayrıca yüzeyin yüksek frekans rölyefini bölge bölge ölçtüm (`tools/gd17_relief.py`).

| Bölge (rölyef HF, mm) | W9 | GD16 | **GD17** |
|---|---|---|---|
| Sırt / radix | 0.027 | 0.039 | **0.026** |
| Uç lobül | 0.051 | 0.087 | **0.067** |
| Yan duvarlar | 0.031 | 0.032 | 0.032 |
| Kanat + kanat oluğu | 0.039 | 0.045 | 0.045 |
| Burun deliği tabanı / kolumella | 0.100 | 0.112 | 0.108 |

- **Asıl kaynak geometri.** GD16'daki Grab/Draw darbeleri sırtta ve uç lobülde fırça izi bıraktı. Kilde görülen "bozuk" yüzey bu.
- **İkincil kaynak materyal.**
  - Cildin burun normal katmanı, yan duvarlarda çizgi çizgi bir doku yaratıyor. Bu doku W9'dan beri değişmemişti ve geometride karşılığı yok.
  - Base color'da kanat oluğunu saran kırmızı bir halka var.

## 2. Burun: düz Smooth yerine katmanlı düzeltme

Uygulanan adımlar:

1. **Zımparalama (NSb).** Rölyefin yalnız yüksek frekans bandı, normal yönünde ve 4 burun bölgesinde alındı. Doğal kıvrımlar korundu: kanat olukları, kolumella tabanı ve burun deliği tabanı. Değişim en fazla 0.59 mm, ortalama 0.06 mm. Büyük ve orta formlar (sırt çizgisi, lobül hacmi, kanat daralması) yerinde kaldı.
2. **Alçak geçiren (NLa).** Alt burun ve sırttaki yer değiştirme alanı plato maskeyle yumuşatıldı. Taban olarak GD15 G15S kullanıldı.
3. **Kanat daralması (NMa).** Alçak geçiren adım GD16'da kazanılan kanat daralmasını azaltmıştı. Bu yüzden tek parça, yumuşak bir plato hareketiyle yeniden uygulandı. Ön kalıntı 0.04 px.
4. **Materyal (s1t6n).**
   - Burun normal katmanı yumuşatıldı: Nose Strength 0.9, Intensity Nose 0.35.
   - Base color'daki kırmızı kanat halkasının doygunluğu düşürüldü: f6 dokusu, alar_desat 0.6.

Denenen ama elenen yollar:

- **AL\* (kanat oluğu relax):** etkisiz kaldı, çünkü çapalar yüzeyin dışında.
- **NLb (60 iterasyon):** profili gereğinden fazla düzleştirdi.
- **NMb:** kanadı fazla daralttı.

Panolar:

- `G1` (UE yakın plan; GD16 ve GD17, gerçek ve kil)
- `A1`, `A4`, `C1–C3`
- `process/05`, `process/09`

**Dürüst not (regresyon).** Profil çizgilerinde (`A2`) GD17 alt sırtta ve uçta referansın biraz daha gerisinde kalıyor:

| Bant | GD16 | GD17 |
|---|---|---|
| Alt sırt / supratip | −0.52 px | −1.56 px (≈ 0.7 mm daha geride) |
| Uç | −0.55 px | −0.97 px |
| Sırt konveksitesi | 1.2 | 0.61 (referans 0.81) |
| Üst sırt | +0.36 px | −0.12 px (daha iyi) |

Sebep alçak geçiren adım. Onaylarsan bir sonraki turda supratip ve uca ≈ 0.5–0.7 mm'lik yumuşak bir plato ilerletme ekleyerek bu kayıp geri alınabilir.

## 3. Çene: gerçekten uzun mu?

Referans ile GD16'yı aynı kameralarda karşılaştırdım (`process/06–08`). Uzunluk farkı küçük. Sivri ve uzun görünümün asıl nedeni şu: çene yastığı dar, yanlara doğru düşüşü dik. Referansta çene geniş ve yumuşak bir U.

| Aday | Değişiklik | Sonuç |
|---|---|---|
| **F (CH1)** | Hafif | Yetersiz |
| **E (CH2)** | Orta | Daha iyi ama hâlâ dar |
| **G (CH3)** | Seçilen | Aşağıda |

G'de yapılanlar:

- Yan çene yastığına plato şişirme: 1.25 mm.
- Çene-çene açısı köşesine plato şişirme: 1.05 mm.
- Çene altı 1.0 mm yukarı. Ölçülen menton yükselmesi 0.7 mm.

Sonuç: ön yarıda z = 152 cm seviyesinde çene genişliği 5.13 → 5.22 cm. Gonial bölge, masseter, çene alt sınırı ve yanaklar 0.000 mm değişti. Çene **uzatılmadı ve sivriltilmedi.**

Panolar: `G3`, `G4` (adaylar), `process/07–08`.

## 4. Üst dudak uçları

Üst vermilyonun yan üçte biri, dudak temas çizgisine doğru dikeyde sıkıştırıldı (`gd17_lipthin.py`, K 0.2, en fazla 0.86 mm). Ortadaki Cupid yayı, temas çizgisi ve ağız köşeleri **hareket etmedi**, yani üzgün ve aşağı dönük bir ağız oluşmadı.

Panolar: `G2`, `process/07`, `process/09`.

## 5. Korunanlar

`data/G17S_region_changes.json` (G16S → G17S):

| Bölge | En fazla değişim |
|---|---|
| Alın, kaş kemiği, üst ve alt kapak, yanak (malar, orta, alt), çene açısı, kafatası, boyun, kulaklar | 0.000 mm |
| Burun | ≤ 1.5 mm |
| Dudaklar | ≤ 0.86 mm |
| Çene | ≤ 2.29 mm |

Kaş GD16'daki c4 groom'unun aynısı; yalnızca GD17 yüzüne yeniden bağlandı. Göz, iris, kirpik ve saç değişmedi.

## 6. Teknik testler

| Test | Sonuç |
|---|---|
| Fit (2 rezidüel geri besleme) → sculpt | **PASS** (ortalama 0.024 mm, p99 0.26, en fazla 1.15 mm; GD16 ile aynı glabella noktaları) |
| Otomatik rig, DNA, 858 morph, ABP_Face_PostProcess | **PASS** |
| Ters üçgen | **PASS** (0) |
| Keskin kıvrım | **PARTIAL** (7 sınırda: GD16'nın 6 doğal kıvrımı + sağ üst dudak sınırında 1 yeni, 127°) |
| Göz kapağı ve göz küresi | **PASS** (değişmedi) |
| Kaş ve kirpik bağlama, göz kırpma, 19 RigLogic ifadesi | **PASS** (`F1`, `F2`) |
| LOD | **PARTIAL** (LOD0–3 yakalandı, `F3`; LOD4–7 NOT_TESTED) |
| PIE, gövde animasyonu, saç simülasyonu | **NOT_TESTED** (C: sürücüsünde 2.2–2.8 GB boş) |
| Yeniden üretim | **PASS** (`tools/build_gd17.sh` G16S'ten G17S'i 0.000000 mm farkla üretir) |
| Üretim değişmedi | **PASS** (GD17 klasörleri dışında dosya değişmedi; qa_config geri yüklendi) |
| Görsel benzerlik kabulü | **NOT_TESTED** (senin incelemen) |

## 7. Panolar

| Pano | İçerik |
|---|---|
| `A1–A4` | Burun: referans yakın plan, profil çizgileri, ortak kamera, kil |
| `B1–B5` | Kaş ve orbita (değişmediğinin kontrolü) |
| `C1–C3` | Anatomik kil (UE ve Blender) |
| `D1–D4` | Tam yüz (REF / GD16 / GD17; aynı ışık, kamera ve görünüm) |
| `E` | Deformasyon haritası GD16 → GD17 |
| `F1–F3` | Rig, ifade ve LOD |
| `G1–G4` | Burun, dudak ve çene yakın planları (gerçek ve kil) ve aday karşılaştırması |
| `process/` | Teşhis ve aday ara adımları |

Tüm görseller gerçek render; üzerine boyama yapılmadı.

GD16 ile GD17 aynı oturumda yakalandı. GD16 kendi görünümünde (s1t5), GD17 ise s1t6n ile; ikisi de aynı ön ışık ve aynı kameralarda.

## 8. Disk

C: sürücüsünde 2.2–2.8 GB boş alanla çalışıldı. Kaynak dosyalar ve önceki sürümler (GD14 W9, GD15, GD16) korundu.

Yalnızca iki tür geçici dosya silindi, manifest ile:
- Ham referans yakalamalarının dönüştürülmüş kopyaları.
- Birebir aynı olan çift kopyalar.

Motor DDC ve eski capture klasörü büyük yer kaplıyor; temizlenip temizlenmeyeceği senin kararın.

## 9. Önerilen sonraki adım

Onaylarsan:

1. Supratip ve uç profilindeki ≈ 0.7 mm'lik kaybı yumuşak bir plato ilerletme ile geri al.
2. Ardından üretime aktarma planına geç.
