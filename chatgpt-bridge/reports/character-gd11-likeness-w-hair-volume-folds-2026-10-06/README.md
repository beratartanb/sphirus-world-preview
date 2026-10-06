# GD11 tur W: saç hacmi ve yaşanmışlık kıvrımları (u1 + h67a → w5 + h68e)

Tarih: 2026-10-06. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi. Önceki adaylar değiştirilmedi.

Kullanıcı tur V sonrasındaki öneriyi onayladı: önce saç hacmi, sonra yaşanmışlık kıvrımları. Ten (k13), kaş (M_SlightArch) ve göz (e3g) tur V'deki gibi kaldı.

## Aday

| Parça | Önce (tur V) | Sonra (tur W) |
|---|---|---|
| Yüz / DNA | `SKM_G11RR_Face_u1` / `MHC_G11RR_U1_Head` | **`GD11_FaceR_20261006/Face/SKM_G11RR_Face_w5` / `MHC_G11RR_W5_Head`** (yeni auto-rig) |
| Saç | `GR_LK_Hair_*_h67a` | **`GD11_HairQ_20261006/Hair/GR_LK_Hair_*_h68e`** (`GB_G11RR_Hair*_w5h68e`) |
| Ten / kaş / kirpik / göz | gqk13 / M_SlightArch / S_Thin / e3g | aynı |

Önce (`prov/g11rwP0.json`) ve sonra (`prov/g11rwP1.json`) aynı editör oturumunda, aynı ışıkla ve time=0 ile çekildi.

## 1. Saç hacmi

**Teşhis.** Kullanıcının 6 açılı referansında arka, kulak üstü seviyesinde en geniş olan yuvarlak bir kütle. Taç topuza doğru dolgun, her yerde ince kabarık teller var. Bizimki kafaya yakın ve arkadan ters üçgen gibi okunuyor.

Referans kamerasındaki silüet ölçümü (`data/hairsil_P0_P1.txt`; yeni araç `blender_g11rw_hairsil.py`, renk doygunluğuna göre maske):
- Önden saç referansla yaklaşık 1 cm içinde.
- 3/4 referans fotoğrafında taç referansta yaklaşık 4–5 cm daha yüksek, arka kütle 5–6 cm daha geride.

| Deneme | Değişiklik | Sonuç |
|---|---|---|
| h68a | rehber kalınlığı 1,25 → 1,45, taç-arka kalkışı +0,4–0,6 cm, yan bastırma azaltıldı, kabarıklık 1,4, 2000 uçuşan tel | küçük artış |
| h68b | daha güçlü (1,65, arka kilitlere 0,7 cm bombe) | arkadan tepe kare, mantar gibi |
| h68c | taç-arka kalkışı +1,5–2,4 cm | **reddedildi:** tepede ayrı kabarık sırt ve katmanlar arasında boşluk |
| h68d | h68c yönünde | derleme yarıda durduruldu (yanlış yön) |
| **h68e** | rehber 1,45 + arka kilit bombesi 1,5 cm, yanlar eski haliyle, taç-arka orta (+0,8–1,7 cm), kulak arkası/ense kütlesi 1,3 → 2,2, topuz halkaları 140 → 220, kabarıklık 1,7, 2800 uçuşan tel | **seçildi** |

h68e'de:
- profil tacı topuza tek ve sürekli bir kütleyle bağlanıyor;
- arka orta çizgide kafatası üstü yükseklik +1,0–1,5 cm;
- ön tepe +0,3–0,6 cm;
- arkadan daha yuvarlak ve daha kabarık okunuyor.

Ayrım çizgisi tepeleri yeniden çıkmadı; ayrım bölgesinin çarpanı ters orantıyla düşürüldü. Saç rengi h67a ile aynı (bakır-kestane). Teknik:
- `blender_g11rq_guides.py` içine `GP_HBULGE` (arka kilitler için dışa bombe) eklendi; varsayılan 0, eski çıktılar değişmez;
- tel sayısı ve kökler h67a ile aynı;
- yüz önüne düşen tel sayısı 312 → ~305.

**Açık kalan.** 3/4 referans fotoğrafındaki çok büyük taç-arka kütlesi kapanmadı; silüet farkı hâlâ yaklaşık 4–5 cm. h68c'nin gösterdiği gibi, saç kabuğunu bu kadar kaldırmak alttaki katmanlar takip etmediği için boşluk açıyor. Bunu kapatmak için saç oluşturucusunun iç dolgu katmanlarını yeniden kurmak gerekir. Bu daha büyük bir iş ve ayrı bir tur ister.

## 2. Yaşanmışlık kıvrımları (w5 = u1 + `data/W5.json`)

| İşlem | Değer |
|---|---|
| Gülme çizgisi (burun kanadından ağız köşesinin ~1 cm dışına, 11 noktalı sürekli oluk) | nokta başına en çok 0,65 mm |
| Oluğun üstünde yanak taşması (9 nokta) | nokta başına en çok 1,0 mm; toplam en çok 1,19 mm |
| Taubin yumuşatma (3 tur) | sürekli kıvrım |
| Kaş arası dikey çizgiler | 0,6 mm |

- Bölge ölçümü (`data/heat_W5_vs_u1.txt`): yanak en çok 1,19 mm; dudak/ağız 0,49 mm (oluğun kenar sönümü); göz, kulak ve kafatası 0,00 mm.
- Ağız köşeleri aşağı çekilmedi, yanak oyulmadı, çene değişmedi.
- Elenen ara adaylar:
  - W1/W2: aralıklı noktalar boncuk gibi tırtıklı çıktı (board 05);
  - W3/W4: daha yumuşak, w4 rig'lendi ve dokulu görüntüde zor seçiliyordu.
- **Sonuç.** w5'te kıvrım saçsız önden ve yumuşak ön ışıkta okunuyor. Saçlı uzak çekimde etkisi küçük; milimetre düzeyindeki geometrinin bilinen sınırı bu.
- Alın çizgileri ve boyun çizgileri mesh çözünürlüğüyle yapılamaz; doku ya da normal haritası işi gerektirir. TEST EDİLMEDİ.

## Teknik (board 07, 08)

| Kontrol | Sonuç |
|---|---|
| w4 ve w5 auto-rig | taze editör, rig kapısıyla; fit ort. 0,018 / maks 0,352 mm; göz 0,000; 858 morph; DNA bağlı |
| 27 rig pozu (w5 + h68e) | temiz: göz kırpma tam kapanıyor, gülümseme ve konuşma biçimleri yeni kıvrımla doğal |
| Hareket 27 kare | saç başla gidiyor, kök kopması ve kesişme yok |
| Kilitli dosyalar | m2, M DNA, M_SlightArch, M bağlamaları, h51a geri dönüş kaydıyla aynı; özetler tur V ile bit-bit aynı; korunan eski adaylar 89/89 |
| DNA klasörü | rig dışa aktarımı aynı klasördeki DNA varlıklarını yeniden kaydeder (bilinen davranış) |
| LOD | TEST EDİLMEDİ |

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| SAÇ HACMİ (taç-arka, topuz, kabarıklık) | KISMEN (doğru yönde, belirgin değil; 3/4 referanstaki büyük kütle açık) |
| SAÇ ARKA YUVARLAKLIĞI | KISMEN |
| GÜLME ÇİZGİSİ | KISMEN-İYİ (yakın plan ve saçsız görünümde okunuyor) |
| KAŞ ARASI ÇİZGİLER | KISMEN (hafif) |
| ALIN / BOYUN ÇİZGİLERİ | TEST EDİLMEDİ (doku işi) |
| KİMLİK KORUNUMU | BAŞARILI |
| TEKNİK ÇALIŞIRLIK | BAŞARILI (LOD TEST EDİLMEDİ) |

## Board'lar

- `01_REF_BEFORE_AFTER.jpg`: referans kameraları.
- `02_HAIR_VS_6VIEW.jpg`: 6 açılı referansla saç karşılaştırması.
- `03_HAIR_TRIALS.jpg`: saç denemeleri.
- `04_FACE_FOLDS.jpg`: u1 / w4 / w5.
- `05_CLAY_FOLDS.jpg`: kil karşılaştırması.
- `06_FINAL_VIEWS.jpg`: aynı oturumda önce/sonra.
- `07_TECH_RIG.jpg`: 27 rig pozu.
- `08_TECH_MOTION.jpg`: 27 hareket karesi.

Kaynaklar: `SourceAssets/Characters/GD11_LikenessW_20261006`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
