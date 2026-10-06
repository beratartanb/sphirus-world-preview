# GD11 tur V: benzerlik turu (göz, alt kapak, dudak, burun, saç rengi ve formu)

Tarih: 2026-10-06. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi. Önceki adaylar değiştirilmedi.

Kullanıcı isteği: "Gördüğün eksikler doğrultusunda karakteri daha fazla benzetme üzerine profesyonelce çalış". Tur U sonunda listelenen eksiklerden kilitli olmayanlar ele alındı.

## Aday

| Parça | Önce (tur U) | Sonra (tur V) |
|---|---|---|
| Yüz / DNA | `SKM_G11RR_Face_t6` / `MHC_G11RR_T6_Head` | **`GD11_FaceR_20261006/Face/SKM_G11RR_Face_u1` / `MHC_G11RR_U1_Head`** (yeni auto-rig) |
| Göz | `MI_GD3_Eye*_e2` (baked iris, koyu kahve) | **`GD11_FaceR_20261006/Skin/MI_G11RV_Eye{L,R}_e3g`** (procedural iris, açık ela-kehribar) |
| Saç | `GR_LK_Hair_*_h66b` | **`GD11_HairQ_20261006/Hair/GR_LK_Hair_*_h67a`** (`GB_G11RR_Hair*_u1h67a`) |
| Ten / kaş / kirpik | gqk13 / M_SlightArch / S_Thin | **aynı** (kullanıcı kararıyla geri alındı, aşağıda) |

Önce (`prov/g11rvP0.json`), yalnız geometri (`g11rvPg.json`) ve sonra (`g11rvP3.json`) aynı editör oturumunda, aynı ışıkla ve time=0 ile çekildi. Kompozisyon editörden okundu.

## Yüz: u1 = t6 + `data/U1.json` (en çok 1,24 mm)

| İşlem | Değer | Amaç |
|---|---|---|
| Alt kapak yükseltme (`lidrot`, göz küresi merkezi etrafında −2,2°) | 0,4–0,5 mm | Referanstaki daha dar göz açıklığı ve daha az görünen göz akı |
| Alt kapak dolgunluğu | 0,4 mm | Referanstaki dolu, hafif gergin alt kapak |
| Alt dudak inceltme / üst dudak inceltme | 1,24 / 0,7 mm | Referanstaki ince dudaklar |
| Burun kanadı ve sırt daraltma | 0,8 / 0,4 mm | Burnun önden geniş okunmasını azaltmak |

Bölge ölçümü (`data/heat_U1_vs_t6.txt`):
- ağız köşeleri, yanaklar, kulaklar ve kafatası 0,00 mm;
- çene en çok 0,29 mm (dudak işleminin kenar sönümü).

Ağız köşesi indirilmedi, çene uzatılmadı, ağız sertleştirilmedi.

## Göz (board 04)

Göz malzemesinde `Use Baked Material` açıktı. İris rengi pişmiş dokudan geliyordu ve renk ayarları neredeyse etkisizdi; e3a–e3d denemelerinde bu görüldü. Anahtar kapatılınca procedural iris çalıştı. Dört değer denendi: e3e (zeytin-ela), e3g, e3h, e3f (fazla sarı).

**e3g** seçildi:
- birincil değer 1,2, ikincil 0,45, doygunluk 0,95, gölge detayı 0,55;
- renk çarpanı [1,2, 0,98, 0,62];
- göz akı çarpanı [0,9, 0,85, 0,82] (e2'de daha koyu ve kırmızımsıydı).

## Saç h67a (board 08)

- **Ayrım çizgisindeki iki "boynuz" tepe:** q5 rehberleri (`GP_TOP` 0,72 → 0,48, `GP_RISE` 0,45 → 0,25). Ön üst silüet kafatasından en çok 3,8 → 2,7 cm.
- **Sarkan tutamlar:** uçta daha az sivri toplanma (0,6 → 0,3), daha fazla ayrılan tel (%12 → %30), tutam içinde daha fazla kabarma. Amaç "dreadlock" görünümünü azaltmak. Sayı ve yerleşim h66b ile aynı.
- **Renk:** önce daha koyu denendi (melanin 0,62). Referanstan koyu kaldığı için bakır-kestaneye çekildi: ana 0,56 / kırmızılık 0,56, gevşek 0,60, highlight 0. Sarı uçlar belirgin biçimde azaldı. Arkadan ışıkta gevşek tel uçları hâlâ biraz açık okunuyor.
- h67b (üst örtü kaldırma 0,5) silüet ölçümünde h67a ile aynı çıktı. İçe aktarılmadı.

## Kullanıcı tarafından reddedilen denemeler (board 05)

Bu turda iki deneme de yapıldı, kullanıcı ikisini de beğenmedi ("Yeni kaşları ve ten rengini beğenmedim"):
- kaş v1–v3: M_SlightArch'ın daha ince ve saç renginde kopyaları;
- ten k14a–k14d: daha sıcak ve bronz ten.

Son aday M_SlightArch + gqk13 ile kuruldu. Denemelerin varlıkları silinmedi, yalnızca kayıt olarak `GD11_FaceR_20261006/Grooms` ve `/Skin` altında duruyor.

## Teknik (board 06, 07)

| Kontrol | Sonuç |
|---|---|
| u1 auto-rig | taze editör, rig kapısıyla; fit ort. 0,018 / p95 0,072 / maks 0,352 mm; göz 0,000; 858 morph; DNA bağlı |
| 27 rig pozu (son kompozisyon) | temiz. Göz kırpma yükseltilmiş alt kapakla tam kapanıyor. Tek göz kırpma, bakış, kaş, çene, gülümseme, konuşma biçimleri, burun deliği sorunsuz. |
| Hareket 27 kare | saç başla gidiyor, kök kopması ve kesişme yok |
| Kilitli dosyalar | m2, M DNA, M_SlightArch, M bağlamaları, h51a geri dönüş kaydıyla aynı (`data/hashes_passV.json`; iki "DIFFERS" satırı önceki turlarla bit-bit aynı); korunan eski adaylar 89/89 |
| DNA klasörü | u1 rig dışa aktarımı aynı DNA klasöründeki DNA varlıklarını yeniden kaydeder (bilinen davranış, tur T notu) |
| LOD | TEST EDİLMEDİ |

Not: kaş varyantında Python'dan LOD0 eğri seyreltme denendi; kayıtta 1'e dönüyor, kullanılmadı.

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| GÖZ RENGİ (açık ela-kehribar) | BAŞARILI (referans yönünde belirgin) |
| GÖZ AÇIKLIĞI / ALT KAPAK | KISMEN (yakın planda daha dolu alt kapak; uzak çekimde fark küçük) |
| DUDAK İNCELİĞİ | KISMEN (alt dudak inceldi; referans hâlâ daha ince) |
| BURUN | KISMEN (küçük daralma; referans hâlâ biraz daha uzun ve ince) |
| SAÇ ÜST FORMU (boynuz tepeler) | KISMEN-İYİ (belirgin alçaldı) |
| SAÇ RENGİ / SARI UÇLAR | KISMEN-İYİ (bakır-kestane; arkadan ışıkta uçlar hâlâ hafif açık) |
| KAŞ VE TEN | DEĞİŞTİRİLMEDİ (denendi, kullanıcı reddetti) |
| ÇENE BOYU | TEST EDİLMEDİ: kilitli, kullanıcı kararı gerekiyor |
| KİMLİK KORUNUMU | BAŞARILI |
| TEKNİK ÇALIŞIRLIK | BAŞARILI (LOD TEST EDİLMEDİ) |

## Board'lar

- `01_REF_BEFORE_AFTER.jpg`: referans kameralarında önce/sonra.
- `02_FINAL_VIEWS.jpg`: beş açı.
- `03_FACE_EYES_LIGHT.jpg`: yakın plan, yumuşak ön ışık, saçsız.
- `04_EYE_IRIS.jpg`: iris denemeleri.
- `05_REJECTED_BROW_SKIN.jpg`: reddedilen kaş/ten denemeleri.
- `06_TECH_RIG.jpg`: 27 rig pozu.
- `07_TECH_MOTION.jpg`: 27 hareket karesi.
- `08_HAIR.jpg`: h66b ile h67a karşılaştırması.

Kaynaklar: `SourceAssets/Characters/GD11_LikenessV_20261006`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
