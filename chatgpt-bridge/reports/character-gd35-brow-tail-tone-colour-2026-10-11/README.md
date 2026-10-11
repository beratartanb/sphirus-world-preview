# GD35 — Kaşta açık kalanlar: kuyruk tonu, kaş rengi, sol-sağ farkı

Tarih: 2026-10-11. Başlangıç: GD34 ds6n. Yüz mesh'i (GD31 G31), sakin göz pozu (`AS_GD33_Rest_lid60`) ve kaş biçimi (GD34'te yumuşatılan yol) değişmedi.

Durum: **PARTIAL.** Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED). Üretim karakterine uygulanmadı. Yeni varlıklar yalnız `/Game/Sphirus/CharacterLab/GD35_IdentityMaster_20261011` altında.

## 1. İsteğin

"Hâlâ açık olanları da düzelt." GD34'ün açık listesinde üç madde vardı:

1. Kuyruk gövdeden biraz koyu.
2. Kaş rengi referanstan sıcak. GD34'te bunu turuncu tene bağlamıştım.
3. Sağ kaş soldan koyu ölçülüyor.

## 2. Ölçümler ve bulgular

**Ten (ölçüldü, değiştirilmedi).** Önden aynı kamerada medyan ten rengi ölçüldü (`process/01`, `data/skin_base.json`):

| Bölge (R/G, B/G) | Referans | GD34 |
|---|---|---|
| Alın | 1,35 / 0,82 | 1,36 / 0,79 |
| Sol göz altı | 1,46 / 0,78 | 1,45 / 0,78 |
| Sağ göz altı (stüdyo ışığının gölge tarafı) | 1,39 / 0,80 | 1,71 / 0,65 |
| Burun | 1,54 / 0,78 | 1,64 / 0,69 |

Işık alan tarafta ten referansla aynı. Sıcaklık yalnız gölge tarafında; deri altı saçılması gölgede tonu ısıtıyor. Bu yüzden GD34'teki "ten turuncu" açıklamam yanlıştı: kaşın sıcak görünmesinin sebebi ten değil, kılların kendi rengiydi. Teni değiştirmedim; global bir değişiklik alnı referanstan soğuk yapardı.

**Sol-sağ farkı ışıktan geliyor** (`L1`). Kaş gövdesi koyuluğu, sol / sağ:

- Stüdyo ışığında 0,53 / 0,65.
- Simetrik ön ışıkta 0,55 / 0,61.
- Referansın kendisinde 0,42 / 0,47.

Simetrik ışıkta kalan 0,05'lik fark referanstaki kadar. Kaş modeli dengeli; değişiklik gerekmiyor.

## 3. Yapılanlar

1. **Kuyruk tonu (ds7).**
   - Kuyruk bölgesi kaşın son %50'sinde başlıyor.
   - Yoğunluk ortada 0,35'e, uçta 0,04'e iniyor; uçtaki kıl uzunluğu ×0,30.
   - Tel sayısı 4368'den 4093'e indi. Kaş yolu ve kalınlık GD34 ile aynı.
2. **Kaş rengi (n4).** `MI_GD35_BrowS_n4`: melanin 0,65 aynı, kızıllık 0,30'dan 0,05'e, doygunluk azaltma (Desat) 0,10'dan 0,55'e. Ara adımlar: n2 (kızıllık 0,15), n3 (kızıllık 0,15, Desat 0,35) (`process/02`, `process/03`).

| Önden, saç gizli | GD34 ds6n | **GD35 ds7n4** | Referans |
|---|---|---|---|
| Kuyruk − gövde koyuluğu (sol, stüdyo ışığı) | +0,13 | **+0,02** | +0,01 |
| Gövde R/G, stüdyo ışığı (sol / sağ) | 1,75 / 2,20 | **1,69 / 1,98** | 1,59 / 1,58 |
| Gövde R/G, simetrik ışık (sol / sağ) | 2,00 / 2,04 | **1,79 / 1,86** | 1,59 / 1,58 |
| Gövde B/G, stüdyo ışığı (sol / sağ) | 0,65 / 0,53 | **0,67 / 0,58** | 0,71 / 0,71 |

Kaş rengi belirgin biçimde nötrleşti. Daha ileri gitmedim, çünkü kaş gri ve küllü görünmeye başlayabilir. Ölçümde kalan fark, kılların arasından görünen tenden ve ışıktan geliyor.

## 4. Editörde değerlendirme

1. Şu haritayı aç: `/Game/Sphirus/CharacterLab/GD35_IdentityMaster_20261011/Maps/L_GD35_Eval_G31`. Kameralar ve ışık önceki geçişlerle aynı.
2. Sakin göz pozu yalnız **Simulate (Alt+S) veya PIE** sırasında görünür.

## 5. Panolar

- `T1`: kuyruk tonu ve kaş rengi, saç gizli (REF | GD34 | GD35).
- `F2`: kaş yakın plan, saçlı (REF | GD34 | GD35). `F1`: genel sonuç.
- `L1`: sol-sağ farkın ışıktan geldiğinin kanıtı (stüdyo ışığı / simetrik ön ışık).
- `C1`: baş-omuz dönüşü (kayıtlı Blueprint).
- `process/01`: ten ölçüm bölgeleri. `process/02`, `03`: renk adayları ds6n / n3 / n4, saçlı.

## 6. Teknik testler

| Test | Sonuç |
|---|---|
| Blueprint: 4 groom bağlaması; PIE'de ds7n4 bağlı, `eyeUpperLidUp` 0,6 | **PASS** |
| Kayıtlı Blueprint ile çekim düzeninin birebirliği | **PASS** (yüz bölgesinde ortalama fark 0,013–0,016, yalnız gürültü) |
| Yüz mesh'i, kaş yolu ve ten MI'ları değişmedi | **PASS** |
| Üretim değişmedi | **PASS** (`data/outside_change_scan.txt`; qa_config geri yüklendi; editör kaydetmeden kapatıldı) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 7. Kalanlar

- **Burun kızıllığı.** Burun referanstan biraz kızıl (R/G 1,64'e karşı 1,54). Bu pişmiş dokudan geliyor; istersen ayrı bir doku geçişinde düzeltilebilir.
- **Işık seçimi.** Stüdyo ışığının asimetrisi değerlendirme düzeninin bir özelliği. Referansa daha benzer, yumuşak ve simetrik bir ışık istenirse değerlendirme haritasına ayrı bir ışık önayarı eklenebilir.
- **GD33'ten kalanlar.** Kirpik yoğunluğu, kaş altı gölge, saç rengi ve topuz konumu bu turun konusu değildi.
