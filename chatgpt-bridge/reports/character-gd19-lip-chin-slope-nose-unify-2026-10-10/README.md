# GD19 — Dudak–çene profil eğimi ve bütünleşik burun yüzeyi

Tarih: 2026-10-10. Başlangıç ve geri dönüş noktası GD18 G18 (E adayı); GD18'e dokunulmadı.

Final aday **G19**. Durum: **PARTIAL**. Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED).

**Üretim karakterine uygulanmadı.** UE varlıkları `/Game/Sphirus/CharacterLab/GD19_IdentityMaster_20261010` altında, yalnız test amaçlı. Kaynaklar `SourceAssets/Characters/GD19_IdentityMaster_20261010` altında (blend, GLB/OBJ, sculpt verisi, op'lar, araçlar). GD14–GD18 kaynakları ve GD17 görünüm varlıkları yalnız okunarak kullanıldı.

## 1. Senin iki notun ve teşhis

**a) Profilde çenenin dudağa doğru eğimi doğal değil; alt dudağa doğru olan eğim de.**

GD18'in profil satır kalıntıları (sabit çözülmüş profil kamerası, + = model önde) şunu gösterdi: alt dudak 1–3 px önde; dudak altındaki yanal doku (x ±1,6 cm, "raf") 3–6 px önde; orta hatta oluk kısa ve keskin bir çentik; yastığın üst yarısı 1–2 px önde; yastığın en dolgun noktası yüksek (z ≈ 152,6). Referansta alt dudaktan çeneye geçiş uzun, sığ bir S: dudak yumuşakça geri döner, oluk uzundur, yastığın dolgunluğu aşağıdadır. `process/04`.

Çene uzunluğunu da tek bir yöntemle (orta hat sütunlarında parlaklık düşüşü, fotoğraf ve renderlarda aynı) yeniden ölçtüm: referans çene alt kenarı satır 761, GD17 761–764, GD18 754–758. Yani **GD17'de çene uzun değildi**; GD18'deki 2 mm kısaltma kırmızı/cyan farkın yanlış okunmasından kaynaklandı ve çeneyi referanstan 2,3 mm kısa yaptı. "Uzun" okunması yastık formundandı. `process/03`.

**b) Önden burun iki ayrı parça gibi; delik üstü bölge yapay.**

4x kil karşılaştırması (`process/01`): GD18'de uç lobülü ayrı bir top, kanatlar yanlarda ayrı yastıklar; aralarında oluklar ve deliklerin üstünde yatay bir kırışık. Sebep: GD18'in lobül şişirme + kanat şişirme + lobül sıkıştırma op'larının birleşim yerlerinde kaynaşmaması.

## 2. Müdahaleler

**Burun** (`ops/N19.json`, `gd19_sand.py`, `ops/N19b.json`; relax tabanı GD17 G17S):
- GD18'in alt burun yer değiştirmesi relax ile kaynaştırıldı (ayrı tümsekler tek yumuşak hacme), uç–kanat birleşimine 0,3–0,4 mm dolgu, alt buruna 0,3 mm bütünleşik yuvarlatma, lobül+kanat yüzeyinde yüksek frekans zımparalama (doğal kıvrımlar hariç).
- GD18'in kazanımları korundu: pronasale z 159,06 → 159,05, burun deliği çatısı z 158,54 → 158,51, kolumella yeri.

**Çene** (`ops/C19.json`, `C19c.json`, `C19d.json`):
- Çene altı 2,0 mm aşağı: GD18'in kısaltması geri alındı (çene alt kenarı satırı 762 ≈ referans 761).
- Mentolabial bant toplam −3,0 mm geri, yanal raf −1,8 mm, yastık üstü toplam −3,0 mm geri, alt yastık −1,2 mm, oluk +0,9 mm (S genliği yumuşatma).
- Sonuç: alt dudaktan çeneye uzun, yumuşak bir S; yastığın dolgunluğu aşağıda; gonial, masseter, çene sınırı, yanaklar 0,000 mm.

## 3. Adaylar

| Aday | İçerik | Karar |
|---|---|---|
| A | Burun kaynaştırma + bant −1,5 / yastık üstü −0,7 | Reddedildi: raf hâlâ 2–3 mm önde; yastık üstü önde |
| B | A + birleşim relax + raf −1,8 + yastık üstü −1,0 + alt "top" +1,2 | Burun seçildi; çene reddedildi: alt yastık aşırı öne (+2,4 px) |
| C | B'nin burnu + çene altı geri (−2,0) + bant/raf/yastık üstü | Yakın; oluk 1–2 mm fazla derin, alt yastık +2 px |
| **D = G19** | C + S genliği yumuşatma (oluk +0,9, yastık üstü −0,9, alt yastık −1,2) | Seçildi |

`process/06_*` aday profil overlay'leri.

## 4. Ölçümler

Profil satır kalıntıları, dudak–çene (px; + = model önde):

| Bölge (z) | GD18 | **GD19 (sculpt)** |
|---|---|---|
| Alt dudak (155,3–154,9) | +2,2 … +3,1 | +2,2 … −0,6 |
| Oluk / raf (154,7–154,2) | +0,4 … +2,9 | −2,4 … +0,9 |
| Yastık üstü (154,1–153,5) | +3,2 … +6,3 | +0,3 … +1,8 |
| Yastık ortası (153,4–152,8) | +0,5 … +2,3 | −2,1 … +0,4 |
| Alt yastık (152,6–151,9) | +0,2 … +2,4 | +0,4 … +1,7 |
| Çene altı satırı (ön, 2x) | 754–758 (ref 761) | 762 sculpt / 764 rig sonrası gerçek |

S genliği ±3–6 px'ten ±2 px'e (≈1,4 mm) indi; profil panelinin güvenilirlik sınırı bu civarda (panel %9 küçük, boyun duruşu farklı).

Burun: pronasale, delik çatısı ve kolumella yüksekliği GD18 ile aynı; `process/02` ve `boards/C4` kil/gerçek yakın planlar.

Rölyef (yüksek frekans pürüz, mm, rig sonrası): uç lobülü 0,085 → 0,075, kanatlar 0,063 → 0,058, çene yastığı 0,040 → 0,039 (burun yüzeyi GD18'den daha pürüzsüz).

Rig sonrası profil bantları ve bölge değişimleri: `data/gd19_summary.json`, `data/G19S_region_changes.json`.

## 5. Teknik testler

| Test | Sonuç |
|---|---|
| Fit (2 rezidüel geri besleme) → sculpt | **PASS** (ortalama 0,037 mm, p95 0,20, p99 0,43, en fazla 1,17 mm) |
| Otomatik rig, DNA, 858 morph | **PASS** (otomatik rig ok, DNA, 858 morph) |
| Rig sonrası mesh ↔ sculpt | **PASS** (ortalama 0,037 mm, en fazla 1,17 mm; GD18 → GD19 rig sonrası ortalama 0,12 mm, en fazla 5,4 mm çene altında) |
| Ters üçgen | **PASS** (0) |
| Keskin kıvrım | **PARTIAL** (7 sınırda; GD17/GD18'dekiler + ağız içi mukozada 2 sınırda 130–137°; dış yüzeyde yeni yok) |
| Üçgen alan oranı min | 0,28 |
| Göz kapağı / göz küresi | **PASS** (değişmedi) |
| Kaş-kirpik bağlama, göz kırpma, RigLogic ifadeleri | **PASS** (19 RigLogic ifadesi × 2 görünüm; `F1`, `F2`) |
| LOD | **PARTIAL** (LOD0–3 yakalandı, `F3`; LOD4–7 NOT_TESTED) |
| PIE, animasyon, saç sim. | **NOT_TESTED** (C: 2–3 GB boş) |
| Yeniden üretim | **PASS** (`tools/build_gd19.sh` G18S'ten G19S'i 0,000000 mm farkla üretir) |
| Üretim değişmedi | **PASS** (GD19 klasörleri dışında dosya değişmedi; qa_config geri yüklendi; editör kaydetmeden kapatıldı) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 6. Panolar

`O4_*` sonuç overlay'leri (REF | aday | %50 | fark; satırlar GD18 gerçek / GD19 gerçek / GD18 kil / GD19 kil), `O5`–`O6` burun ve çene yakın plan overlay'leri, `A2` profil çizgileri, `C2`–`C6` kil ve UE yakın planlar, `D1`–`D4` tam yüz, `E` deformasyon GD18 → GD19, `F1`–`F3` rig/ifade/LOD. Tüm görseller gerçek render; GD18 ve GD19 aynı görünüm, ışık ve kameralarla.

## 7. Açık kalanlar

- Oluk orta hatta referanstan 1–2 mm derin kalmış olabilir (profil paneli belirsizliği içinde).
- Üst dudak profilde hâlâ ~2 mm önde (GD18'den kalan).
- Burun delikleri GD17 boyutunda; referansın daha küçük delikleri için kanat kenarının sarkması mevcut topolojide katlanıyor (GD18 raporu).
