# Sphirus World v6: P1 aşamalı test. ABP geri dönüşü, temiz BEFORE, G1 ve G1+G2+G3 (2026-10-31)

**Kalıcı kayıt yapılmadı.**
- Harita yalnız bellekte değişti ve test sonunda özgün transformlara geri alındı.
- Diskteki `L_GR_SphirusHouse.umap` hiç değişmedi: SHA1 `70dd481a…`, manifestteki değerle aynı.
- G4 uygulanmadı.

Bütün kanıtlar `v6/` altında. Videolar ve kâğıtlarda üç sürüm aynı oyun zamanında **yan yana**: BEFORE | G1 | G1+G2+G3.

---

## 0. Yan eğim aralığı neden farklıydı? (DOĞRULANDI)

- v5 raporundaki "±5°" yanlıştı. Aralığı yalnız her ikinci örnekten (s = 0, 1, 2 … m) özetlemiştim; 0.5 m adımlı tüm 34 örnekte gerçek aralık **−9.0 … +6.1°** (env_probe işaret kuralıyla).
- **Bitişteki −9°:** ayrıntılı ölçümde (`data/crossslope_fine.json`, 15.0–17.5 m, 25 cm adım) patika merkezi **her iki kenardan da alçakta**:
  - ±0.75 m'de sağ (yokuş) kenar +14 → +31 cm, sol kenar +2 … +16 cm yüksek.
  - Yürüme yüzeyi oyulmuş bir **oluk**; 24 Eylül yapısal geçişindeki "asimetrik kenar dudakları" ile uyumlu.
  - −9°, iki dudak arasındaki yükseklik farkı; 16.5 m'de yokuş tarafı dudağı soldan ~24 cm yüksek. Yürünen yüzeyin 9° yana yatık olduğu anlamına gelmiyor.
  - Bu fark 15–17.5 m'de 0°'den ~10°'ye çıkıyor; yokuş şevi burada başlıyor.
- **s = 0.5 m'deki +6.1°:** bu kez sol dudak 22 cm yüksek.
- Patika boyuna eğimi doğru raporlanmıştı: 2 m pencerede 1.8–8.8°, 1 m pencerede 1.4–10.9°.

## 1. Dirty ABP'ler: korundu, üretime döndürüldü (DOĞRULANDI)

| Adım | Sonuç |
|---|---|
| Disk sürümü korundu | İki `.uasset` → `Saved/Codex/AIToolingEval_20261031/abp_protect/disk_v240_production/`. SHA1'ler V2.40 manifestiyle aynı (`abp/SHA1SUMS.txt`) |
| Bellek sürümü korundu | 00:40 otomatik kayıt kopyaları → `abp_protect/memory_candidate/`. Bellekteki T3D şimdi yeniden alındı ve 03:53'teki ile **byte düzeyinde aynı** (o zamandan beri değişmemiş) |
| Geri yükleme | Projenin mevcut aracı `SHME_V21/revert_noquit.py` (kaydetmez, beklenmeyen dirty paket görürse reddeder): iki paket diskten yeniden yüklendi, `dirty after reload []` |
| Doğrulama | verify240 **ALL_OK**. Düğmeler üretimde: `SHM239_Own` 0, `HeadOn` 0, `BlkSpd` 60 |
| Tam karşılaştırma (bellek ↔ disk) | `abp/t3d_compare.json`, sıradan bağımsız, nesne bazlı. Grafiklerde 14633 + 5 nesne birebir aynı. **Tek gerçek fark iki ABP'de de 3 CDO değeri:** `SHM239_Own` 1→0, `SHM240_HeadOn` 1→0, `SHM240_BlkSpd` −1→60 |

**Karşılaştırmada maskelenen gürültü:** yeniden yüklemede yeniden üretilen PinId / GraphGuid / LinkedTo GUID'leri, `NSLOCTEXT(...)` ile düz metin biçim farkı, `K2Node_PropertyAccess_N` numaralandırması. Maskelemeden önce bu gürültü 773 "farklı" nesne gösteriyordu.

## 2. Test yöntemi

- **Temiz BEFORE:** ABP'ler üretimdeyken; dirty paket yok.
- **Uygulama:** her aşamada **aynı** yetkili patika yürüyüşü:
  - 12.8 s, 385 kare;
  - 13 istasyon karesi;
  - sıkışma (8 m) ve açılma (14 m) istasyonlarında kayıtlı sağ-sol kamera dönüşü (−100° → +100°, 6 s);
  - CSV performans profili;
  - kaplanma ölçüsü;
  - bitkilerin alındığı ve konduğu yerlerden editör inceleme kareleri.
- **Tekrarlanabilirlik:** sabit adımlı kayıt deterministik; aynı durumda iki BEFORE koşusu GPU ortalamasında 40.63 / 40.62 ms verdi.
- **Uygulama yolu:**
  - manifest + doğrulanmış yedek: `manifest_map.py`, manifest233 ile aynı şema; `.umap` desteği eklendi;
  - kapılı `write` işi; projenin önceki geçişlerindeki yerel foliage yolu: FoliageType = mesh + cull mesafesi, `remove_all_instances` + `add_instances`;
  - **hiç kayıt yok** (runner günlüğü: `written=[]`).
- **Geri alma:** 10 örnek özgün konumlarında yeniden bulundu (z farkı 0, aynı indeksler); örnek sayıları eşit.
  - İlk geri alma denemesi **hiçbir şeyi değiştirmeden reddetti**, çünkü yeniden kurulan bileşenlerin adları değişmişti. Bileşen artık konumla bulunuyor; ikinci denemede başarılı.
  - Harita paketi bellekte "dirty" işaretli kaldı, içeriği ise özgün haline döndü. Editör kapatılırken "Kaydetme" seçilmeli ya da paket diskten yeniden yüklenmeli.

## 3. Sonuçlar

### 3.1 Ölçülenler (DOĞRULANDI)

| | BEFORE | G1 | G1+G2+G3 |
|---|---|---|---|
| Kameranın yakın bitkiye sürtündüğü kare (taç kutusu yaklaşığı, yürüyüş) | **24** (~0.8 s, s≈8–10 m) | **0** | **0** |
| GPU ort. / p95 | 40.62 / 43.08 ms | **38.74 / 40.71 ms** | 39.64 / 41.72 ms |
| Kare süresi ort. | 42.09 ms | 40.20 ms | 41.14 ms |
| Oyun thread'i | 15.25 ms | 15.24 ms | 15.23 ms |
| Taşınan örnek / toplam | 0 | 1 | 10 (sayı aynı) |

GPU'daki iyileşme, kameranın hemen önündeki masked genç çamın ekranı doldurmaması (aşırı çizimin azalması) ile tutarlı. G2+G3, G1'e göre +0.9 ms geri getiriyor; toplamda yine BEFORE'dan 1 ms iyi.

### 3.2 Görsel değerlendirme

Kaynak: STILL_IMAGES_VIEWED ve saniyede bir kare kâğıtları. Videolar gerçek zamanlı izlenmedi.

| Konu | G1 | G2 | G3 |
|---|---|---|---|
| Kamera kaplanması | **Çözüldü.** 7–8.7 s arasında genç çamın dalları artık kadrajın sağ üçte birini kaplamıyor; yalnız 7.0–7.3 s'de kenarda bir parça | — | — |
| Patika okunurluğu | **İyileşti.** Sıkışma ileri bakışında patika ve önde devrik gövde/kaya yönlendirmesi açıkça görünüyor (`compare/station_compression_forward.png`) | — | **Görünür etki yok denecek kadar az.** 6 eğrelti 0.9–1.4 m'ye kondu, ama açılma bölümü hâlâ açık bir yosun yamacı gibi okunuyor |
| Büyük kütle hiyerarşisi | Sağdaki genç çam kütlesi 0.5 m geride; sıkışma hissi hâlâ var ama biraz azaldı | Ölü gövde yalnız sağa dönünce görünüyor: **açık renkli, temiz, "yerleştirilmiş"** duruyor. Hedefinde bir `SM_Bush_02` ile iç içe (5.6 cm; **yapay örtüşme**). Bir ucu 5.7 cm havada. 2 genç ladin patikadan pratikte algılanmıyor (şevin 3.2–4.3 m içinde, mevcut çalıların arkasında) | — |
| Orta plan | Sıkışmada orta plan açıldı: kaya, devrik gövde, gövde sırası okunuyor | Belirgin katkı yok | Belirgin katkı yok |
| Işığın yönlendirmesi | Değişmedi (ışığa dokunulmadı). Patikadaki benekli güneş daha görünür hale geldi | — | — |
| Sinematik kompozisyon | **Sıkışma kareleri daha iyi kuruluyor:** sol yumuşak kütle → patika → sağ şev; arka planda dikey gövdeler | Sağa dönüşte yatay bir öğe ekliyor, ama sahte görünüyor | Açılma kareleri pratikte aynı |
| Ormanın kapalı karakteri | Korunuyor (koridor açılmadı) | Korunuyor | Korunuyor |

**Eski yerlerde boşluk:** inceleme karelerinde doğu yamaçta birkaç eğreltinin eksildiği fark ediliyor; belirgin bir boşluk yok. Batıdaki 3 eğrelti farkı görünmüyor (`inspect/inspect_before_vs_after.png`). Sıkışma şevi inceleme karesinin kamerası bir çamın içine düştüğü için orada yorum sınırlı.

**Taç örtüşmesi** (bütçe tahmini, `plan_p1_resolved.json`):
- G1 çamı bir eğrelti ve bir kayayla örtüşüyor; doğal, sorun görünmüyor.
- G2 gövdesi bir çalının içinde (0.98); **düzeltilmeli.**
- G3'te bir eğrelti, iki komşu eğreltiyle %41–53 örtüşüyor.

**Zemin teması** (`data/contact_check.json`):
- Bitkilerin pivot–zemin farkı özgün haliyle aynı (−2.7 … −8 cm).
- Gövde özgün yerinde boyunca 21–28 cm gömülüydü. Hedefte şevin eğimine uymuyor: bir uç +5.7 cm havada, diğer uç −32 cm gömülü.

## 4. İki sürüm: karar için

| | **Sürüm A = G1** | **Sürüm B = G1+G2+G3** |
|---|---|---|
| Değişen örnek | 1 (genç çam, 51 cm) | 10 |
| Kamera kaplanması | Çözüldü | Çözüldü |
| Okunurluk / kompozisyon | Sıkışmada belirgin iyileşme; açılma değişmedi | A ile aynı + sağa dönüşte yapay görünen bir gövde; açılma pratikte değişmedi |
| Riskler | Düşük | Gövde–çalı iç içe, gövdenin bir ucu havada, bir eğrelti çift; 9 örneğin eski yerinde küçük eksilmeler |
| GPU | −1.9 ms | −1.0 ms |
| **Önerim** | **Kabul edilebilir aday** (kayıt ayrı onayla) | **Bu haliyle önerilmez** |

**Açılma bölümünün (11–16.5 m) kök nedeni bitki yerleşimi değil.**
- Patika tabanında zemin malzemesi ayrışmıyor: aşınmış toprak ve yaprak döküntüsü yok, her yer aynı yosun.
- Sağ ileride kaya levhası dışında bölümü çerçeveleyen bir kütle yok.
- G3 bu yüzden etkisiz kaldı. Bu bölüm için arazi boyası / döküntü ve bir çerçeveleme kütlesi gerekiyor. Arazi değişikliği ayrı onay ister.

## 5. Önerilen sonraki adımlar (hiçbiri yapılmadı)

1. **Sürüm A'nın kalıcı hale getirilmesi:**
   - G1 yeniden uygulanır, yalnız `L_GR_SphirusHouse` kaydedilir (manifest ve yedek hazır).
   - AGENTS gereği Bridge dışa aktarımı yapılır.
   - **Ayrı onay** gerekiyor.
2. **G2'nin düzeltilmiş hali (G2b):** gövdeyi şev eğimine yatırmak (pitch) ve çalının dışına almak, tabanına döküntü ve eğrelti koymak; ya da yerine, doğal olarak gömülü duran bir kök/kaya grubu. Aynı aşamalı testle.
3. **Açılma bölümü:** taban okunurluğu için arazi boya katmanı veya decal ile aşınmış toprak/döküntü; çerçeveleme için var olan bir kütle (kök plakası/kaya). Arazi ve malzeme değişikliği ayrı onay.
4. **Kamera tarafı (ayrı iş):** masked bitkiler için proje sahipli yakın-kamera dither'ı.
5. **G4:** yalnız istenirse.

## 6. Eksikler

- Videolar gerçek zamanlı izlenmedi; değerlendirme durağan kare ve kare kâğıtlarına dayanıyor.
- Taç ve kaplanma ölçüleri, sınır kutusuna dayalı yaklaşık hesaplar.
- Standalone performans ölçülmedi; tüm ölçümler editör PIE'de.
- Harita paketi bellekte "dirty" kaldı (içerik özgün); editör kapatılırken kaydedilmemeli.
