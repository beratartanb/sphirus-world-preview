# GD37 — Profilde dudak, üst dudak büyüklüğü ve burun

Tarih: 2026-10-11. Başlangıç: GD36 yüzü K36 (GD35 görünümü: kaş ds7n4, ten n3, göz h6, sakin göz pozu).

Durum: **PARTIAL.** Teknik testler geçti. Görsel kabul senin incelemene bağlı (NOT_TESTED). Üretim karakterine uygulanmadı. Yeni varlıklar yalnız `/Game/Sphirus/CharacterLab/GD37_IdentityMaster_20261011` altında.

## 1. İsteğin

"Yan profilde işaretlediğim yerde dudak garip duruyor. Üst dudak referanstan farklı ve büyük gibi duruyor. Aynı şekilde burun da modelde biraz daha büyük gibi." İşaretli görsel: `process/00_KULLANICI_ISARETI.jpg`.

## 2. Teşhis (GD36, referansla aynı çözülmüş kameralar)

### Profil siluet
Ölçüm, 9 nokta benzerlik hizasıyla yapıldı (`tools/gd37_contour_shape.py`). Değerler model mm'sidir; "aşağıda" referansa göre demek.

| Nokta | GD36 sapması | Anlamı |
|---|---|---|
| Burun ucu | 1,3 mm yukarıda | Burun ucu ile subnazale arası referanstan **%7 uzun** (hizalı 38,0 / ref 35,4). Profilde burun büyük okunuyor. |
| Stomion | 1,2 mm aşağıda | Ağız çizgisi aşağıda. |
| Alt dudak en önde noktası (li) | 0,7 mm yukarıda | Alt dudak profilde kısa ve topak (stomion–li 10,1 / ref 13,2). |

### Kil yakın plan (`process/01`, `boards/L1` alt satır)
Asıl "garip" görüntünün kaynağı siluet değil, yüzey biçimi:
- Üst dudağın vermilion sınırı keskin bir sırt yapıyor ve hemen üstünde bir oluk var. Profilde ve 3/4'te bu, dudağı **sivri, gaga gibi** gösteriyor.
- Referansta üst dudak derisi düz-içbükey iniyor ve vermilion yuvarlak.

### 3/4 görünüm
Üst dudak köşeye doğru incelmiyor, kalın bir rulo gibi devam ediyor.

### Ön görünüm (kil, aynı kamera)
Burun kanat genişliği referanstan yaklaşık **%9–10 fazla**.

## 3. Yöntem

### Hedef `N2` (`tools/gd37_edit3.py`)
Ağız ve burun bölgesinde, iki yanda simetrik, yumuşak alanlar kullanıldı.
- Vermilion, yüz dokusunun kırmızılığından sınıflandırıldı (`process/03`).
- Yalnız dış deri değiştirildi: önden ışın testi uygulandı, ağız içi ve burun deliği içi sabit kaldı.

| Alan | Değer | Amaç |
|---|---|---|
| Vermilion sınır sırtını köreltme | 0,6 mm geri (yanlarda +%30) | Gaga görüntüsü yuvarlanıyor |
| Üst dudağın yan kısmını dikey inceltme | Ortada 0, yanlarda %20 | Üst dudak köşeye doğru inceliyor |
| Ağız çizgisi | +0,8 mm yukarı | İki dudak temas çizgisinde birlikte hareket ediyor; alt dudağın alt sınırı sabit, bu yüzden alt dudak uzuyor |
| Üst dudak derisi | Ortada 0,35 mm içe | Subnazale–dudak arası daha içbükey |
| Burun kanatları | %6,5 daraltma (burun ucu kubbeleri %4) | Kanat genişliği düşüyor |
| Burnun alt kısmı (uç, kolumella, kanatlar) | Burun tabanı merkezli %3,5 küçültme | Burun boyutu küçülüyor |

### Adaylar
Tümü `process/01` panosunda.

| Aday | İçerik | Sonuç |
|---|---|---|
| M1 | Yalnız sırt + burun kanadı | Ara aday |
| M2 | Güçlü sürüm | 3 ters üçgen; **reddedildi** |
| N1 | M1 + ağız çizgisi + burun ölçeği | Kanatlar referanstan %3 dar kaldı |
| **N2** | N1, kanat daraltma azaltılmış, üst dudak derisi içbükeyliği eklenmiş | **Seçildi** |

### Motor zinciri (`tools/gd37_finalN.sh`)
1. GD36 MHC'sinin kopyası alındı.
2. 4 aşamalı geri beslemeli fit yapıldı.
3. Otomatik rig üretildi (858 morph, DNA).
4. GD35 kaşı yeni deri üzerinde yeniden üretildi.
5. Saç ve kirpik yeni yüze bağlandı.
6. Çekimler alındı.
7. Değerlendirme Blueprint'i ve haritası kuruldu, PIE çalıştırıldı.

## 4. Sonuç (rig sonrası yüz, aynı ölçüm)

| Profil ölçüsü | GD36 | **GD37** | Referans |
|---|---|---|---|
| 9 nokta toplam sapma (RMS) | 1,05 mm | **0,84 mm** | 0 |
| Burun ucu – subnazale (hizalı) | 38,0 | **36,2** | 35,4 |
| Burun ucu yüksekliği | 1,32 mm yukarı | **0,95** | 0 |
| Stomion | 1,23 mm aşağı | **0,65** | 0 |
| Alt dudak en önde noktası | 0,72 mm yukarı | **0,41** | 0 |
| Stomion – alt dudak (hizalı) | 10,1 | **11,3** | 13,2 |
| Alt dudak kavisi (sto–li) | 0,102 | **0,080** | 0,087 |
| Üst dudak derisi içbükeyliği (sn–ls) | −0,056 | **−0,059** | −0,083 |
| Üst dudağın en önde noktası (ls) | 1,06 mm aşağı | **1,53 mm aşağı** (kötüleşti) | 0 |

Diğer ölçümler:
- **Burun kanadı (mesh, en geniş bant):** 34,0 → **30,7 mm** (−%10). Kil ön görünümde referans genişliğine eşit (okuma hassasiyeti ±%3).
- **Ön görünüm, üst vermilion yüksekliği orta hatta:** GD36 ~9,9 mm → **GD37 ~9,0 mm**; referans ~7,5–8 mm. Ölçüm, ızgaralı yakın planda elle okundu, hassasiyet ±0,6 mm.

## 5. Panolar

- `L1`: profil dudak ve burun. Satırlar: saçlı stüdyo, saç gizli, kil. Değişim en net kil satırında görünüyor.
- `L2`: sağa bakış (3/4) dudak ve burun. Satırlar: saçlı, ön ışık, kil.
- `L3`: önden burun ve dudak. Satırlar: stüdyo, ön ışık, kil.
- `F1`: REF | GD36 | GD37, saçlı, sakin göz, dört açı. `F2`: aynısı saç gizli.
- `process/02`: profil kontur bindirmesi (turuncu REF).

## 6. Editörde değerlendirme

1. Şu haritayı aç: `/Game/Sphirus/CharacterLab/GD37_IdentityMaster_20261011/Maps/L_GD37_Eval_N37`. Blueprint: `BP_GD37_Character_N37`.
2. Sakin göz pozu yalnız **Simulate (Alt+S) veya PIE** sırasında görünür.

## 7. Teknik testler

| Test | Sonuç |
|---|---|
| Hedef N2: ters üçgen 0, kat 41 (GD36: 40). En küçük alan oranı 0,16, ağız köşesinin içindeki çok küçük üçgenlerde (görünmeyen bölge). | **PASS** |
| Fit (4 aşama) → hedef: ortalama 0,057 / p95 0,28 / p99 0,75 mm. En fazla 3,8 mm, ense–boyunda; GD36 ile aynı. Düzenleme bölgesinde değişikliğin %100'ü korundu. | **PASS** |
| Otomatik rig, DNA, 858 morph (`MHC_GD37_N37`, `SKM_GD37_Face_n37`) | **PASS** |
| Rig sonrası: ters üçgen 0, kat 41, alan oranı 0,53–3,1 | **PASS** |
| Dudak/burun dışındaki yüz, kafa, göz ve dişler GD36 rig sonrasıyla aynı (en fazla 0,017 mm) | **PASS** |
| Kaş (ds7n4, yeni deri), saç h75c ve kirpik yeni yüze bağlı. PIE'de 4 groom görünür, `eyeUpperLidUp` 0,6. | **PASS** |
| Kayıtlı Blueprint ile çekim düzeninin birebirliği: yüzde ortalama fark 0,011–0,016, yalnız gürültü (GD36: 0,012–0,017) | **PASS** |
| İfadeler (RigLogic), LOD1–7 | **NOT_TESTED** |
| Üretim değişmedi (`data/outside_change_scan.txt`). qa_config geri yüklendi, editör kaydetmeden kapatıldı. | **PASS** |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 8. Açık kalanlar

- **Değişimin büyüklüğü.** Ortalama 0,74 mm, en fazla ~2 mm. Dokulu ve saçlı görüntüde ince kalıyor; en net `L1` / `L2` kil satırlarında görülüyor.
- **Üst vermilion hâlâ ~1 mm uzun (önden).** Daha fazla kısaltmanın iki geometrik yolu da kısıtlı:
  - Sınırı aşağı almak filtrumu uzatır. Filtrum önden zaten referanstan biraz uzun görünüyor.
  - Ağız çizgisini daha yukarı almak çeneyi uzatır (yasak).
  - Kalan seçenekler:
    - vermilion'un alt yarısını içe-aşağı döndürmek ("içe kıvrık" dudak; referanstaki gibi ışığı daha az alır);
    - doku tarafında vermilion sınırını inceltmek.
  - Hangisini istersen sonraki geçişte yapabilirim.
- **Üst dudağın en önde noktası (ls) 1,5 mm aşağıda.** Bu, sivri sırtın köreltilmesinin yan etkisi. Referansın sınırında da hafif bir uç var. İstenirse köreltme azaltılabilir.
- **Alt dudak önden referanstan ~%25 uzun.** GD23'te bilinçli olarak doldurulmuştu; bu turda dokunulmadı.
- **Disk.** C: 3,2 GB'a düşmüştü. Otomatik rigden önce motorun 3 günden eski DDC önbelleği (6,5 GB, yeniden üretilebilir) temizlendi. Şu an ~5 GB boş.
