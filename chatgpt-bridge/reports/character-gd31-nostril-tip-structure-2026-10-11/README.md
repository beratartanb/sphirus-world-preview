# GD31 — Burun delikleri, delik içi ve uç yapısı: referansla gerçek görüntü doğrulaması

Tarih: 2026-10-11. Başlangıç noktası GD30'un finali W4 (`MHC_GD30_G30W`); GD30'a dokunulmadı.

Final aday **G31** (sculpt adı Z1, doku n3). Durum: **PARTIAL**. Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED).

**Üretim karakterine uygulanmadı.** UE varlıkları `/Game/Sphirus/CharacterLab/GD31_IdentityMaster_20261011` altında, yalnız test amaçlı. Kaynaklar `SourceAssets/Characters/GD31_IdentityMaster_20261011` altında.

## 1. İsteğin

"Burun delikleri ve burun ucu, kemiği. Referans ile aynı hale getir."

## 2. Teşhis (W4)

1. **Işık** (`process/01`). UE'deki "front" çekim ışığı kanat oluklarını ve yan duvarı çok koyu ve sert gösteriyor. Referans fotoğraflar yumuşak ışıkta çekilmiş. Aynı W4 burnu mevcut stüdyo ışığı çekiminde yumuşak görünüyor ve referansa yakın. Yani "kemik gibi" görünümün büyük kısmı geometri değil çekim ışığıydı. Adil karşılaştırma stüdyo ışığı.
2. **Doku** (`process/02`). Pişmiş renk dokusu (GD17) yalnız deliğin en derin ortasını siyaha boyuyor. Noktalar: modelin kanat oluğu ve delik köşeleri UV'de (sarı E, camgöbeği GD28, kırmızı W4). Dokudaki oluk, geometrinin oluğuyla uyumlu; sertliğin kaynağı doku değil.
3. **Delik içi.** Kil geometride görünen delik içi zaten referanstaki ağız kadar uzun. Gerçek görüntüde ise deliğin arka kısmında ışık alan, ten rengi iç duvar görünüyor. Delik arkada sığ ve doku orayı koyu boyamıyor; bu yüzden delik fotoğraftakinden küçük ve kısa görünüyordu.
4. **Ağız yönü** (`data/aperture_projected.txt`, yalnız geometri). Burun tabanının arka kısmını indirmek delik ağzını kameraya çeviriyor. Ağız, fotoğraftaki gibi arkaya doğru aşağı eğimli hale geliyor.

## 3. Müdahale

**Sculpt Z1** (`tools/build_gd31.sh`, W4'ten, 0,000000 mm farkla yeniden üretilir):

1. **Arka burun tabanını indirme**, en fazla 2,0 mm (`ops_postdown_Z1.json`). Etkilenen bölgeler: delik eşiği, deliğin arka kenarı, kanat tabanı. Kolumella, uç ve dudak yerinde kaldı.
2. **Arka delik içini derinleştirme**, 1,8 mm (`tools/gd31_cavdeep.py`). Delik iç duvarı burun dokusuna doğru itildi; dış kanat derisine dokunulmadı.

**Lookdev n3** (yalnız GD31'de yeni isimlerle):

- `T_GD31_Head_BC_n3`: GD17 pişmiş renk dokusu, delik iç duvarı ağızdan itibaren derinliğe göre koyulaştırıldı (`tools/gd31_texnostril.py`). Dış deri değişmedi (`process/03`).
- `MI_GD31_Face_{lod}_s1t6n_n3`: salt okunur GD17 MI'larının alt örnekleri; yalnız renk dokusu değişti.

Elenen adaylar: öteleme (14–57 ters üçgen), en yakın nokta eşleştirme (37 ters üçgen), yana itme (burnu genişletti), X1 2,5 mm (alan oranı 0,07). `G1` panosunda X1 ve Z1 karşılaştırması var.

## 4. Sonuçlar

Gerçek UE görüntüsünde delik ağzı örtüşmesi (IoU). Referans fotoğrafla aynı koyu bölge bölütlemesi kullanıldı, 1 = tam örtüşme (`process/05`, `data/real_opening_iou.txt`):

| Görünüm | GD28 | W4 (GD30) | **GD31** |
|---|---|---|---|
| 3/4 sol, ön ışık | 0,10 | 0,40 | **0,48** |
| 3/4 sağ, ön ışık | 0,25 | 0,35 | **0,41** |
| Önden (sol delik), ön ışık | 0,00 | 0,15 | **0,20** |
| 3/4 sol, stüdyo ışığı | — | 0,32 | **0,37** |

| Ölçü | W4 | **GD31** | Referans |
|---|---|---|---|
| Önden delik ağzı alanı, gerçek görüntü (px²) | 25 | **47** | 51 |
| 3/4 sol / sağ delik ağzı alanı, gerçek görüntü (px²) | 43 / 56 | **52 / 71** | 86 / 109 |
| Önden yansıtılan ağız alanı, geometri (px²) | 112–116 | **125–132** | — |
| Ağız uzun ekseni eğimi (°) | +23–25 | **+20–21** | — |
| Kanat rölyefi (ortalama / en fazla, mm) | 0,032 / 0,30 | **0,037 / 0,33** | — |
| Uç–subnazale kord açısı (profil) | 36,5° | **35,6°** | 40,5° |

3/4 sağda stüdyo ışığında bölütleme deliği değil uç altı gölgesini buluyor (IoU 0); bu ölçüm geçersiz, tabloya alınmadı.

## 5. Teknik testler

| Test | Sonuç |
|---|---|
| Fit (2 rezidüel geri besleme) → sculpt | **PASS** (ortalama 0,045 mm, p95 0,23, p99 0,61, en fazla 1,60 mm) |
| Otomatik rig, DNA, 858 morph | **PASS** (`MHC_GD31_G31`, `SKM_GD31_Face_g31`) |
| Rig sonrası GD30 → GD31 | ortalama 0,03 mm, en fazla 1,81 mm (değişiklik burun tabanında yoğunlaşıyor, `E`) |
| Ters üçgen (rig sonrası) | **PASS** (0) |
| Keskin kıvrım | **PARTIAL** (41; GD30'da 43) |
| Üçgen alan oranı min / max | 0,217 / 4,30 (GD30 0,216 / 3,86) |
| Çene alt kenarı satırı (ön, rig sonrası) | **PASS** (763; GD30 763, referans 761, çene uzamadı) |
| Doku içe aktarma (4096², VT) ve MI | **PASS**. Not: `set_material_instance_texture_parameter_value` değeri atasa da False döndürüyor; atama gerçek görüntüde gözle doğrulandı (`process/04`). |
| Kaş-kirpik bağlama, göz kırpma, RigLogic ifadeleri | **PASS** (`F1`, `F2`) |
| LOD | **PARTIAL** (LOD0–3, `F3`; LOD4–7 NOT_TESTED) |
| PIE, animasyon, saç sim. | **NOT_TESTED** |
| Yeniden üretim | **PASS** (`tools/build_gd31.sh` W4'ten G31S'i 0,000000 mm farkla üretir) |
| Üretim değişmedi | **PASS** (Content / Config / Plugins / SourceAssets temiz; GD31 dışında yalnız lookdev kayıtları, `data/outside_change_scan.txt`; qa_config geri yüklendi; editör kaydetmeden kapatıldı) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 6. Panolar

- `process/04`: gerçek UE karşılaştırması. Sütunlar: REF, W4 ön ışık, GD31 ön ışık, W4 stüdyo, GD31 stüdyo. Satırlar: iki 3/4 açı, önden, profil.
- `process/05`: gerçek delik ağzı örtüşmesi (3/4 sol, 3/4 sağ, önden).
- `process/01`: ışık teşhisi (REF, W4 ön ışık, W4 stüdyo). `process/02`: doku teşhisi. `process/03`: doku n3 öncesi ve sonrası.
- `C4`: burun yakın plan, gerçek ve kil (GD30 | GD31). `H1`: profil şekil analizi.
- `O1–O3`: GD30 teşhis overlay'leri. `O4–O6`: sonuç overlay'leri. `G1`: adaylar X1 / Z1.
- `D`, `E`, `F`: tam yüz, deformasyon, rig/ifade/LOD.

## 7. Açık kalanlar

- **3/4 delik ağzı hâlâ küçük:** gerçek görüntüde 52 / 71 px², referansta 86 / 109. Daha fazla açmak için kanat kenarını yükseltmek gerekiyor; bu da GD29'daki gibi yapıyı bozma riski taşıyor.
- **Uç yüksekliği:** GD30'dan bu yana uç, subnazaleye göre referansın yaklaşık 2 mm üstünde. Kord açısı 35,6°, referansta 40,5°. Bu turda uca dokunulmadı.
- **Işık:** ön ışık oluğu ve yan duvarı sertleştiriyor. Fotoğrafla karşılaştırma için stüdyo ışığı daha adil. Üretimde kullanılacak ışık kararı ayrıca verilmeli.
- **Lookdev n3 yalnız GD31'de.** Beğenirsen ileride üretime taşınabilir; şu an hiçbir yerde kullanılmıyor.
