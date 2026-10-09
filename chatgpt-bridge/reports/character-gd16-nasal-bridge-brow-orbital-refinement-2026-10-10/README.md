# SPHIRUS — GD16 | Burun Köprüsü, Kaş Kıvrımı ve Orbital Anatomi

Tarih 2026-10-10 · Başlangıç ve geri dönüş noktası **GD15 G15** · En iyi aday **GD16 G16** · Genel sonuç **PARTIAL**: burun ve kaş bölgesi belirgin biçimde referansa yaklaştı, ama yüzün genel kimliği henüz tam değil.

Üretim karakteri değiştirilmedi. GD15 G15, GD14 W9, eski karakter kaynakları, B2 gövde, kıyafetler, saç kaynakları, animasyon/locomotion, kamera ve haritalar korundu. Tüm yeni UE varlıkları yalnız `/Game/Sphirus/CharacterLab/GD16_IdentityMaster_20261010` içinde. Kullanıcı onayı için durduruldu.

---

## 0. Kısa özet

| Bölge | GD15 → GD16 | Kanıt |
|---|---|---|
| Burun kökü (radix) | Profil bandı +4.48 → +3.06 px. Ölçüm sağ radix kanadının merkez dışı tümseğini gösterdi; bu kanat 1.3 mm geri alındı. | A2 |
| Burun sırtı / kemer | "Kayak pisti" (içe kavisli) sırt düz-hafif dışbükey hatta döndü: üst sırt rms 2.37 → 1.50 px, alt sırt/supratip −2.29 → −0.52 px, sırt dışbükeyliği 0.0 → 1.2 (referans 0.81). | A2, A1, A4 |
| Burun ucu / kanatlar | Önden kanat genişliği +2.80 → +0.65 px. Lobül 1.5 mm yukarı; uç sivriltilmedi, küçültülmedi. Burun delikleri önden iki küçük oval olarak okunuyor. | A1, A3 |
| Kaş kemiği / glabella | Supraorbital sırt 1.6 mm geri (geniş yumuşak alan, oyma değil); korrugatör düğümleri ve dikey glabella izi yumuşatıldı. | B4, C |
| Kaş | Referanstan ölçülen eğriyle **özel kaş groom'u** üretildi. 16 istasyonda kıl sınırı hatası 6.70 → 3.34 px. | B1, B2, B5 |
| Teknik | Ters üçgen 1 → **0**. DNA, 858 morph, ifadeler ve göz kırpma çalışıyor. | F |

Değişim büyüklüğü (GD15 → GD16, riglenmiş): ortalama 0.04 mm, p99 1.3 mm, en çok 2.9 mm. Değişim yalnız burun, radix, glabella ve kaş kemiğinde. Yanak, çene, dudak, yüz genişliği ve kafatası 0.000 mm (ağız köşesi onarımı ≤ 0.6 mm). Göz kapakları ≤ 0.15 mm.

---

## 1. Başlangıç analizi

GD15 renderları yeniden ve eleştirel değerlendirildi. Raporun "burun en büyük kazanım" yargısı ön görünümde doğruydu, ama profil ölçümü yeni bir sorun gösterdi.

**Profil satır analizi** (sabit çözülmüş profil kamerası, model − referans):

| Bölge | GD15 kalıntısı | Okuma |
|---|---|---|
| Radix | +2..+4 px | Kök fazla önde |
| Orta-alt sırt | −1.5..−3.6 px | Sırt içe çökük |
| Lobül alt yüzü / kolumella | + | Aşağıda |

Kamera ölçeği ya da eğimi böyle S biçimli bir desen üretemez; bu gerçek şekil farkıdır. Referansta derin kök, düz-hafif dışbükey köprü ve sırt hattını aşmayan yuvarlak, hafif aşağı bakan bir uç var.

**Sunita preset'inin etkisi:**
- burun kanatlarını genişletti (W9 +0.3..+1.6 px → GD15 +2.1..+3.3 px);
- lobülü ağırlaştırdı.

**Kaş:**
- GD15'in kaş yüksekliği eşleşmişti, ama M_FlatThick kütüphane groom'unun biçimi referansla uyuşmuyordu: seyrek medial baş, fazla kavisli ve dağınık lateral, aşağı düşen kuyruk.
- Kil, belirgin bir kaş kemiği "rafı" ve medial korrugatör düğümleri ("kaş çatma" okuması) gösterdi.

**Referans kaşı ×10 yakın inceleme:**
- **Kalınlık:** gövde ~6–7 mm, baş ~4 mm, kuyruk ~2.5 mm.
- **Medial baş:** gövdeyle aynı yükseklikte; hafif kabarık, yukarı kıllı.
- **Gövde:** üst sınır yavaşça yükselir; tepe uzunluğun ~%70–75'inde, yumuşak-hafif açılı.
- **Kuyruk:** aşağı-dışa iner, incelir.
- **Alt sınır:** neredeyse düz.
- **Asimetri:** iki taraf ayrı ölçüldü. Panelde sol kaş ~2 mm aşağıda görünüyor, ama 3B'de bunun çoğu kamera dönüklüğü; doğal asimetri korundu.

**Belirsizlikler:**
- Profil paneli ~%9 küçük ve boyun pozu farklı. Dudak ve subnazal bantları şekil hedefi olarak kullanılmadı.
- Fotoğrafta alt kaş sınırı orbital gölgeyle birleşiyor. Otomatik sınır gölgeye sızdı; alt sınır görsel okumayla belirlendi (`process/12`).

---

## 2. Burun (Aşama N)

Gerçek Blender fırçalarıyla (GUI, yön kalibrasyonu doğrulanmış) çalışıldı. Adaylar gerçek UE renderları ve profil çizgileriyle karşılaştırıldı.

**N1b — köprü ve kök:**
- Radix: profil görünümünde Grab ile 2.3 mm geri.
- Burun kemiği → rhinion: Draw ADD ile köprü inşası (+1.3 mm öne, sırt normali boyunca +1.1).
- Alt sırt / supratip: +0.5 mm.
- Ön görünüm Grab'ları silüet kenarında boşa düştü (öne çekme yapılamadı). Bu yüzden köprü Draw ile kuruldu.

**N2:** infratip ve kolumella küçük kaldırma.

**N3 / N4 — kanatlar:** ön görünümde tüm alar lobül, burun deliği duvarıyla birlikte, rijit olarak içe alındı (iki geçiş, ~1.7 mm/taraf). Kanat şişkinliği hafif azaltıldı.

**N5 elendi:** kolumella bandını değiştirmedi. Ölçüm, bu bandın lobül değil subnazal/üst dudak geçişi (poz etkisi) olduğunu gösterdi.

**N6 (seçilen):**
- Bütün lobül (uç, infratip, kolumella, alar kenarlar) burunla maskeli düz bir alanla 1.5 mm yukarı alındı.
- Üst dudak 0.000 mm. Uç sivriltilmedi, küçültülmedi.
- Profilde lobül referansa yaklaştı; önden burun delikleri iki küçük oval.

**Sonuç:** köprü hattı nasiondan uca kadar referansla örtüşüyor (A2). Kalanlar:
- radix bandı hâlâ +3 px;
- lobül alt yüzü referanstan biraz aşağıda;
- kanat oluğu (alar crease) gölgesi referanstan derin.

---

## 3. Kaş ve orbita (Aşama B)

### 3.1 Kaş kemiği / glabella

**B1 — elendi:** Draw SUBTRACT vuruşlarıyla sırt azaltıldı, ama kil topak/çukur bir yüzey gösterdi (`process/08`).

**B2:** supraorbital sırt geniş, düz çekirdekli, yumuşak kenarlı bir alanla 1.6 mm geri alındı; sağ radix kanadı 1.3 mm geri. Ardından korrugatör ve glabella üzerinde geniş yumuşak Smooth uygulandı.

**B3 (seçilen):** B2 artı yalnız hareket yer değiştirmesinin Laplace gevşetmesi. B2'deki alan kenarı oluğu kalktı, sırt daha yumuşak ve doğal okunuyor (`process/10`, B4).

**Kalan:** yan ışıkta medial korrugatör bölgesinde hafif bir dolgunluk. Oyma yapılmadı.

### 3.2 Özel kaş groom'u (c4)

**Yöntem:**
1. Referans ön panelinde her kaş için 8 istasyon ölçüldü: medial baş, ilk üçte bir, gövde, tepe, kuyruk; üst ve alt kıl sınırları.
2. Çözülmüş ön kamerayla 3B deriye yansıtıldı.
3. `gd16_brow.py` ile kıllar üretildi; kıl akış alanı:
   - medial baş yukarı;
   - gövdede alt kıllar yukarı-dışa, üst kıllar aşağı-dışa (merkez hatta birleşir);
   - tepe ve kuyrukta dışa-aşağı;
   - uzunluk, yoğunluk ve kalınlık uca doğru incelir.

**Tanı süreci:**
- **c1:** UE'de ince ve yüksek göründü. İşaretçi groom'u, groom ile yüz uzayının aynı olduğunu kanıtladı (dönüşüm hatası yok).
- **Asıl nedenler:**
  - Kılların yukarı akışı görünen bandı köklerin üstüne taşıyordu.
  - Uzak görüşte çok ince (0.0045) kıllar düşüyordu. Kütüphane kaşları gibi **stable rasterization** ve 0.009–0.011 kıl genişliği gerekti.
- **c2:** referans bandının yalnız üst kısmını kapladı. İstasyon alt sınırı +2.5 satır düzeltildi.
- **c3:** kahve-siyah, düz gövdeli kaş.
- **c4 (seçilen):** kökler ölçülen bandın biraz dışına taştı; ~2000 kıl/kaş, genişlik 0.0095.

**Sonuç (B1 istasyon panosu):** GD16 kaşı referans istasyonlarını medial başta, tepede ve kuyrukta dolduruyor; kalınlık da uyuşuyor.

| Kaş | Kıl sınırı ortalama hatası |
|---|---|
| GD15 kütüphane kaşı | 6.70 px |
| GD16 | 3.34 px |

**Kalanlar:**
- GD16 kaşının kenarları referanstan daha keskin; daha az tüylü.
- Rengi referanstan biraz koyu.
- Ölçüm, alt sınırı hâlâ ~1.5–2.4 mm aşağıda veriyor (kısmen kaş altı gölgesi).

### 3.3 Kaş – kapak

- GD15'in sakin bakışı korundu. Kapak verteksleri ≤ 0.15 mm değişti; kapak-göz küresi sayımı aynı (360/300).
- Düz ve ağır kaş yüzü sert yapmadı. Ön ve 3/4'te ifade nötr-ciddi; referansla aynı karakter.
- İfade testinde (F2) özel kaş yüzü izliyor: kaş kaldırma/indirme, kaş çatma, gülümseme ve göz kırpmada kopma yok.

---

## 4. Birleştirme ve teknik onarım (Aşama C)

- **Burun-kaş ilişkisi:** N6 burun ve B3 kaş kemiği aynı kafada. Alından → kaş kemiğine → nasiona → dorsuma → supratip ve uca geçiş profilde ve 3/4'te kesintisiz (A2, A4, B4). Yeni çıkıntı veya çöküntü yok.
- **Ağız köşesi:** GD15'teki tek ters üçgen sağ ağız köşesindeydi. Blend yer değiştirmesi W9'a göre küçük kürelerde rijit yapıldı (en çok 0.6 mm). Sonuç: **0 ters üçgen**.
- **Bilerek bırakılan kıvrımlar:** ağız köşesi 150°, burun deliği eşiği ×4 (123–128°) ve sağ dış kantus (121°). Bunlar doğal anatomik kenarlar ve eşiğe çok yakın.
  - Konum gevşetme kıvrımları çökertti (5–16 ters üçgen); reddedildi.
  - W9'a rijit eşleme burun eşiğinde anatomik uyumsuzluk yaratırdı (GD16 burnu daha dar).
  - Talimata uygun olarak, yalnız metrik için anatomi bozulmadı.
- **Yan etki ölçümü** (G15S → G16S): yanak 0, çene/çene hattı 0, yüz genişliği 0, kafatası 0, alın ≤ 0.13 mm, üst kapak ≤ 0.15 mm, dudak ≤ 0.6 mm (yalnız köşe onarımı).

---

## 5. Aktarım ve rig

- **MetaHuman aktarımı:** GD15 G15 durumu GD16 klasörüne kopyalandı (GD15'e dokunulmadı). Ardından 2 artık geri beslemeli fit; sculpt'a ortalama 0.020 mm, p99 0.21 mm, en çok 1.15 mm. En büyük sapma glabella orta hattındaki 19 verteksteydi; MHC orada biraz daha dolgun kaldı.
- **Auto-rig:** ok. DNA blendshape'li, **858 morph**, `ABP_Face_PostProcess`, kalıcı DNA bağı.
- Rig sonrası mesh = fit (0.001 mm).
- **Boyun bağlantısı:** sınırdaki 92 verteks 0.0000 mm. Gözler ve dişler değişmedi.

---

## 6. Panolar (hepsi gerçek UE yakalaması veya Blender render; boyama yok)

**A — Burun:** REF / GD15 / GD16

![A1](boards/A1_BURUN_YAKIN_REF_GD15_GD16.jpg)
![A2](boards/A2_BURUN_PROFIL_CIZGILERI.jpg)

A2 renkleri: sarı = referans, eflatun = GD15, camgöbeği = GD16. Beyaz çizgiler referans eğrisi üzerinde bulunan nasion, rhinion/sırt, supratip, uç (pronasale) ve subnazaldir. Panel ölçeği ~14 px/cm; kamera ve poz belirsizliği §1'de.

![A3](boards/A3_BURUN_ORTAK_KAMERA_SAG_PROFIL.jpg)

A3: sağ profil referansta yok; yalnız anatomik kontrol.

![A4](boards/A4_BURUN_KIL_YUMUSAK_ve_YAN_ISIK.jpg)

**B — Kaş ve orbita**

![B1](boards/B1_KAS_ISTASYONLARI_REF_GD15_GD16.jpg)

B1 renkleri: yeşil = medial başlangıç, sarı = tepe, eflatun = kuyruk, camgöbeği = diğer istasyonlar. Çizgiler referanstan ölçülen üst ve alt kıl sınırlarıdır; üç karede aynı çerçevede.

![B2](boards/B2_KAS_ON_ve_3_4_REF_GD15_GD16.jpg)
![B3](boards/B3_KAS_KAPAK_YAKIN_UE.jpg)
![B4](boards/B4_KAS_KEMIGI_ORBITA_KIL.jpg)
![B5](boards/B5_KAS_GROOMLU_SACLI_GERCEK.jpg)

**C — Anatomik kil** (aynı kamera ve ışık; yumuşak ışık ve güçlü yan ışık)

![C1](boards/C1_ANATOMIK_KIL_UE_5ACI_2ISIK.jpg)
![C2](boards/C2_KIL_BLENDER_YUMUSAK_ISIK.jpg)
![C3](boards/C3_KIL_BLENDER_YAN_ISIK.jpg)

**D — Tam yüz kimlik kontrolü** (aynı cilt, iris, saç, ışık ve kamera)

![D1](boards/D1_TAM_YUZ_ONISIK_SACSIZ.jpg)
![D2](boards/D2_TAM_YUZ_ONISIK_SACLI.jpg)
![D3](boards/D3_TAM_YUZ_STUDYO.jpg)
![D4](boards/D4_ORTAK_KAMERA.jpg)

**E — 3B deformasyon GD15 → GD16**

![E](boards/E_DEFORMASYON_GD15_GD16.jpg)

Değişim burun, radix, glabella ve kaş kemiğinde. İstenmeyen değişim ölçümü §4'te.

**F — Teknik doğrulama**

![F1](boards/F1_RIG_IFADE_TESTI.jpg)
![F2](boards/F2_KAS_KAPAK_IFADE_YAKIN.jpg)
![F3](boards/F3_LOD_0_3.jpg)

Süreç ve elenen adaylar `process/` klasöründe: profil evrimi, N2/N4/N6, B1 (reddedildi)/B2/B3, kaş c1–c4 tanı adımları.

---

## 7. "Aynı koşullarda GD15'ten daha mı benzer?"

| Açı | Cevap | Gerekçe |
|---|---|---|
| Ön | **Evet** | Kaş mimarisi (düz-ağır gövde, yumuşak tepe), daha dar alt burun, iki küçük burun deliği |
| Sağ 3/4 | **Evet** | Düz köprü, yumuşak kaş kemiği, kaş biçimi |
| Sol 3/4 | **Evet** | Köprü ve kaş; lobül daha hafif |
| Profil | **Evet (kısmen)** | Derin kök ve düz köprü referansla örtüşüyor; lobül alt yüzü hâlâ biraz aşağıda |

---

## 8. Kabul kriterleri

| # | Kriter | Sonuç |
|---|---|---|
| 1 | Burun kökü ve kemeri referansa anatomik olarak yaklaştı | **PARTIAL** — köprü hattı PASS; radix bandı hâlâ +3 px (~2 mm) önde |
| 2 | Sırt, supratip ve uç bağlantısı doğal | **PASS** |
| 3 | Ön, 3/4 ve profilde aynı burun kimliği | **PASS** |
| 4 | Kaşın gerçek eğrisi ve kıl dağılımı | **PARTIAL** — eğri, konum ve kalınlık istasyonlarla uyumlu; kenarlar keskin, renk koyu, kıl akışı sadeleştirilmiş |
| 5 | Kaş kemiği ve üst orbita doğal | **PARTIAL** — sırt yumuşadı; hafif medial korrugatör dolgunluğu kaldı |
| 6 | Gözlerde istenmeyen yeni ifade yok | **PASS** |
| 7 | GD15 kazanımları korundu | **PASS** (bölge ölçümü 0) |
| 8 | Referansla görsel benzerlik belirgin arttı | **PASS** burun-kaş bölgesinde; yüzün genel kimliği **PARTIAL** (olgunluk, yumuşaklık, saç) |
| 9 | Mesh ve rig güvenliği | **PASS** test edilenlerde; PIE ve animasyon NOT_TESTED |
| 10 | Gerçek UE renderlarında iyileşme açıkça görülüyor | **PASS** |

---

## 9. Teknik testler

| Test | Sonuç |
|---|---|
| DNA ve 858 morph | PASS |
| Mesh bütünlüğü, normal/winding (33 845 v, DNA sırası) | PASS |
| Ters üçgen | PASS (0; GD15'te 1) |
| Keskin kıvrımlar | PARTIAL (6 doğal kenar, eşikte; bilerek bırakıldı, §4) |
| Göz küresi – kapak | PASS |
| Kaş ve kirpik bağlantıları | PASS (özel kaş ifadelerle hareket ediyor) |
| Göz kırpma | PASS |
| Mimik testleri (19 durum × 2 açı, statik) | PASS |
| LOD 0–3 | PASS (görsel); LOD 4–7 **NOT_TESTED** |
| Gövde animasyonu + saç simülasyonu | **NOT_TESTED** |
| PIE (ayrı test karakteri) | **NOT_TESTED** — C: boş alanı iş boyunca 2.1–3.8 GB idi; editör/rig için risk alınmadı |
| Yeniden üretim (`build_gd16.sh --blender-stage`) | PASS (N6, B3, G16S 0.000 mm; kaş kılları birebir) |
| Üretim karakteri değişmedi | PASS |

---

## 10. Disk alanı

**Başlangıç:** 3.7 GB boş.

**Silinenler** (manifest: `data/disk_cleanup_manifest.json`):
- 568 ham yakalama (2.25 GB): GD14/GD15 iş klasörlerinde SHA-1 ile birebir kopyası olanlar.
- 308 ham referans-kamera yakalaması (1.07 GB): bükülmüş panel görüntüsü GD15/GD16 klasöründe duranlar. Ara çıktılardır; raporlar bükülmüş görüntüleri kullanır.
- GD16 boyunca birebir kopyalar otomatik temizlendi.

Kaynak, geri dönüş noktası veya başka geçişin dosyası silinmedi.

**Şimdi:** ~2.1 GB boş. Bir sonraki rig, PIE veya yakalama işinden önce yer açılmalı.

**Güvenli seçenekler** (kullanıcı kararı; hiçbiri silinmedi):

| Seçenek | Boyut | Not |
|---|---|---|
| Motor yerel DDC (`%LOCALAPPDATA%/UnrealEngine/Common/DerivedDataCache`) | ~14 GB | Yeniden üretilebilir önbellek; silinirse shader'lar uzun süre yeniden derlenir |
| Proje `DerivedDataCache` | 1.8 GB | |
| `Intermediate` | 0.6 GB | |
| `Saved/Logs` | 0.45 GB | |
| Ortak yakalama klasörü (`Saved/Codex/CharacterLookdev_20260930/captures`) | ~58 GB | Eski geçişlerin ham yakalamaları; kullanıcı onayı gerekir |

---

## 11. Dosyalar

- **Blender Identity Master:** `SourceAssets/Characters/GD16_IdentityMaster_20261010/GD16_IdentityMaster.blend`
  - düzenlenebilir `GD16_Head`;
  - salt-okunur karşılaştırma kafaları: GD15 G15, GD16 riglenmiş, GD14 W9;
  - referans panelli çözülmüş kameralar;
  - op programları.
- **Export:** `export/GD16_Head.glb` / `.obj`
- **Kaş kaynağı:** `brow/c4/brow_main.abc`, `strands.npz` ve istasyonlar (`data/brow_stations_v2.json`, `brow3d_v2_B3.json`)
- **UE varlıkları** (`/Game/Sphirus/CharacterLab/GD16_IdentityMaster_20261010`):
  - `MHC/MHC_GD16_G16` (düzenlenebilir MetaHuman)
  - `MHC/MHC_GD16_G16_Rig`
  - `Face/SKM_GD16_Face_g16`
  - `MHC/DNA/MHC_GD16_G16_Rig_Head`
  - `Grooms/GR_GD16_BrowCustom_c4`
  - `Face/Bindings/GB_GD16_EyebrowsCustom_c4_g16`
  - Ara adaylar silinmedi.
- **Yeniden üretim:** `tools/build_gd16.sh` (Blender aşaması çalıştırılabilir) ve `tools/gd16_final16.sh` (fit → rig → kaş → yakalamalar)
- **Sayısal özet:** `data/gd16_summary.json`, `data/profline_final.json`, `data/brow_shape_metric.json`, `data/G16S_region_changes.json`, `data/checks_g16_postrig.json`

---

## 12. Açık kalanlar ve dürüst notlar

**Burun:**
- Radix hâlâ +3 px önde.
- Lobül alt yüzü ve kolumella biraz aşağıda.
- Alar oluk gölgesi derin.
- Burun yan duvarındaki koyu gölge materyal/ışık kaynaklı (GD15'te de aynı).

**Kaş:**
- Daha yumuşak, tüylü kenarlar ve kahve tonunda bir renk varyantı gerekebilir.
- Kıl akışı prosedürel; elle tarama ile daha doğal yapılabilir.

**Genel kimlik:**
- Referansın olgun, yumuşak yüz okuması (alın, şakak, alt yüz) bu görevin kapsamı dışında kaldı.
- h75c saç tutamları alnı ve kaşları örtüyor (saç kaynakları korunuyor).

**Durum:** kullanıcı onayı bekleniyor. Üretime aktarım yapılmadı.
