# SPHIRUS UE 5.9 — Tur 6: ayak kayması kök nedeni, çarpışma v2, düşme/kalkma, yumuşak başlangıç (2026-11-23)

**Durum: ARA RAPOR.** Bütün değişiklikler Unreal projesine kaydedildi ve editör iki kez yeniden açıldı. Bu rapor yazılırken son doğrulama zinciri (`scripts/final7.sh`) hâlâ çalışıyordu; son durumun tam matrisi, videoları ve ham kayıtları bu klasöre ayrı bir commit ile eklenecek. Aşağıda her sayının hangi durumda ölçüldüğü yazıyor:

| Etiket | Anlamı |
|---|---|
| **A** | Tur 6a kaydedildi + editör yeniden açıldı (`f6_*` kayıtları, 60 / 30 / değişken Hz tam kayma regresyonu + temas alt kümesi) |
| **B** | Tur 6b değişiklikleri, kaydetmeden önce bellekte, tekil ölçüm (`x6b_`, `s6a_`, `t6b_`, `d6b_`, `pv6a_` kayıtları) |
| **C** | Tur 6b kaydedildi + yeniden açıldı: değerlerin diskten okunması doğrulandı (`data/saved6.txt`); oynanış matrisi sürüyor |

Görsel / oynanış kabulü kullanıcıya aittir; bu raporda **USER_ACCEPTED yoktur**. Başlangıç: commit `9765db9` (tur 5). Proje: `C:\Users\berat\Documents\Unreal Projects\sphirus_UE59`, oyuncu `BP_HybridA_Player`, test haritası `L_Sph_MoveTest`.

Test ortamı (bu oturumda okundu): Intel i7-13650HX, 32 GB RAM, NVIDIA RTX 4060 Laptop 8 GB (sürücü 616.56), 1920×1200, editör içi PIE. Girdi simüle klavye planlarıdır; gerçek gamepad (DualSense bağlı) **test edilmedi** — fiziksel çubuk girdisi bir insan gerektirir.

---

## 1. Şikâyet → kök neden → değişiklik

### 1.1 Ayak kayması (tur 5'te büyüyen planU_B, ters yön, fren, çömelme duruşu)

Katman teşhisi (`scripts/an_dump6.py`, `probe_rawfoot.py`, `probe_rootmd6.py`): ham kliplerde basan ayak sabit (1–5 cm) ve `movedata_speed` eğrisi klibin gerçek kök hızına eşit. Kayma oyunda üç ayrı yerde üretiliyordu:

1. **Ayak kilidi eşiği ve yarıçapı (en büyük pay).** `ABP_Sph_GASP` sınıf varsayılanları `PlantSettings_Default / _Stops`: `SpeedThreshold = 1` (0–100 aralıklı temas eğrisinde). Klipler arası karışımda eğri 2–25 arasında gezindiği için kilit çözülüyor; tutsa bile `UnplantRadius = 20` cm'de bırakıyordu. Kaymaların zamanı eğrinin 1'i aştığı karelerle birebir örtüşüyor. Düğümün pin değeri değil, `Get_FootPlacementPlantSettings` fonksiyonunun döndürdüğü bu değişkenler çalışıyor. → eşik 25, yarıçap 45 / 50, açı 90 (`c_plant6.py`). Eşik 40 denendi; 30 Hz'de ayağı karışım sırasında erken kilitleyip 38,7 cm'lik yeni bir aykırı örnek üretti, 25'e indirildi.
2. **Kapsül hızı ≠ klip hızı.** Kapsül, geçiş klibinin hızını girişte ölçülen bir K oranıyla izliyordu; ayak basarken (K−1) × yol kadar kayıyordu (koşu duruşu K 1,18 → 17,7 cm). Ters dönüşte K, ilk CMC karesi hızı düşürdükten *sonra* ölçülüyordu (584/572 = 1,02 olması gerekirken 0,80). Ters dönüş sonrası yeniden itişte kapsül 300, klip 730 cm/s² ile hızlanıyordu. → `m_gov6_mcp.py`, `m_gov6b_mcp.py` (`AC_Sph_Motion`: K, hiçbir ayak basmıyorken 1'e yaklaşır; giriş hızı = max(hız, önceki kare hızı); taban fren yalnız süre aşımında; kalkışta ve yeniden itişte ivme klibe yetişir).
3. **Sprint 180° dönüşü, 30 Hz / değişken Hz.** `UpdateMovement_PreCMC`, hareket bileşeni o karenin girdisini işlemeden *önce* çalışıyor; ters komutun geldiği ilk karede sürtünme hâlâ tamdı (tek 45 ms'lik karede 584 → 413 cm/s). Motion Matching dönüş klibine basıştan 0,23 s önce, klibin pozundan ~50 cm geride bir pozdan giriyordu. → `m_gov6c_mcp.py`, `m_gov6d_mcp.py` (`BP_Sph_GASPCharacter.CalculateGroundFriction`, o karenin bekleyen girdisini kullanır; ters dönüş etkinken 500 cm/s² taban fren uygulanmaz). Karışım süresinin neden olmadığı ayrıca denendi (0,5 → 0,2 s: fark yok).

Not: `M_Relaxed_Sprint_Turn_180_R_Lfoot` ham klibinin kendisinde 16–22 cm kayarak basış var (`data/raw180.txt`); `M_Relaxed_Run_Stop_B_*` kliplerinde temas bayrağı ayak 11 cm havadayken açılıyor (tabloda "eğri" değeri yüksek, "zemin" değeri düşük görünen satırlar).

### 1.2 Çarpışma (diz engelin içine giriyor; her ağır temas aynı diz çökme)

`m_contact6_mcp.py`, `BP_HybridA_Player` içindeki `GR_Contact` olayını tümüyle değiştirir:

- **Tek temas = tek sorgu.** Nokta, normal, mesafe ve nesne adı en yakın isabetten alınır. Aynı nesne, gövde 25 cm ayrılmadan veya 2,5 s geçmeden yeniden tetiklenmez.
- **Momentum.** Çarpma sonrası hız = teğetsel bileşen × 0,7 + normal boyunca geri tepme (eskiden hız tümüyle sabit geri hızla değiştiriliyordu); geri tepme arkadaki boş alana göre kısalır.
- **Önce geri adım, sonra diz.** Denge kaybında 0,38 s'de 44 cm'lik (arkadaki alana göre kısalan) geri adım atılır; diz çökme yalnız kapsül yüzeyden ≥ 30 cm uzaktaysa başlar. Yer yoksa diz çökmez, ayakta el desteğiyle kalır.
- **Takılma (yeni sınıf).** Baldır hizasında, tek başına duran alçak engel (arkasındaki 1,5 m'de diz hizasında başka isabet yok → merdiven ve rampa sayılmaz) koşu hızında: sendeleme; sprintte veya yorgun koşuda, ilerideki zemin dört sondayla düz ve boşsa **öne düşme → yerde yatma → kalkma**. Taşırken yere düşülmez.
- **Düşme / kalkma klipleri.** `MC_Sample` klipleri (`SKM_MCUE5v2` iskeleti) mevcut Core Motion → UEFN retarget'ı ile sürücü iskelete aktarıldı: `/Game/Sphirus/Player/Anim/Fall/SphF_*` (`w_fallclips6.py`, `w_fallroot6.py`). Kullanılan çift: `InjuredBelly_DropToFloor` + `_GetUp` (ProneCrawl çifti havada "uçan" bir poz verdiği için bırakıldı).
- **Kontrol.** Yerde yatma ve diz üstünde bekleme, 0,5 s sonra hareket girdisiyle kısaltılabilir; kalkış kesilemez.
- **Duvar.** Yaklaşma yüzeyden 20 cm önce durur (öncesinde yürürken öndeki ayak duvara 7–17 cm, el 5–12 cm giriyordu). Yürüme hızında diz hizasındaki engel de önceden görülür.
- **Avuç hizalama.** `ABP_Sph_Body_GASP` içinde erişim IK'sından sonra iki `ModifyBone` düğümü (hand_r / hand_l, dünya uzayında döndürme) eklendi (`c_palm6.py`); oyuncu her karede yüzey normalinden avuç yönünü yazar.
- **Alçak geçit.** Yalnız baş hizasındaki engelde (göğüs ve bel sondaları boş) karakter kendiliğinden çömelir, üç düşey sonda temizken doğrulur.
- **Sıyırma.** Duvar tarafındaki kol gövdeye çekilir.

### 1.3 Duruş, başlangıç, merdiven

- **Koşu hızında kaynak omurga katkısı.** Artık sıfırlanmıyor: koruma katsayısı `Lerp(1, 0,4, koşu oranı)` (`m_posture6_mcp.py`).
- **Atletik başlangıç.** Projedeki bütün koşu / sprint başlangıç klipleri (Neutral ve Relaxed) atletik hamle: gövde 41–61°, kalça 15–22 cm alçalıyor (`data/starts6.txt`); oyunda baş 0,45 s içinde 33 cm alçalıyordu. → **yumuşak başlangıç** (`m_softstart6_mcp.py`): duruştan çıkışın ilk 0,42 s'si / 150 cm/s'ye kadar yürüyüş adımıdır, sonra istenen hız yürüyüş→koşu geçiş klipleriyle devralınır; sprint 250 cm/s'den sonra devreye girer. Ek olarak gövde eğimi sınırlayıcı (`PS_Lu`).
- **Merdiven.** 65 cm'lik yürüyüş adımı iki basamağı (2 × 30 cm) kaplıyor, ayaklar iki basamak arayla basıyordu; kalça, arkadaki bacağın erişiminden yükseğe çıkamıyordu. → dik çıkışta hız basamak ritmine iner (yürüyüş 80, koşu 170 cm/s). `PelvisHeightMode` değişikliği denendi, etkisi olmadı, geri alındı.
- **Montaj sırasında "eski sabitlere dönüş".** Ölçüldü (`c6a_knee_run`): sabitler (C3 −4, C5 −12, boyun +12, baş −2), denetleyicinin ayakta beklemede vardığı değerlerle 1–3° içinde aynı; giriş ve çıkış 0,33 s'lik yumuşatmayla sürekli. Değiştirilmedi.
- **Bekleme hareketleri.** Değiştirilmedi; ölçüme göre (`data/idle6.txt`, `data/idle_neck.txt`) mevcut dört hareket setin en sakinleri (bilek ≤ 9°, eller kalçanın altında, el hızı ≤ 46 cm/s). Eklenmesi denenen v09, başı 67° aşağı eğdiği için geri alındı.

---

## 2. Önce → sonra

### 2.1 Ayak kayması — durum A, aynı planlar, aynı ölçüm (`an_slide3.py`, değiştirilmedi)

Sütunlar: ortalama / p90 / en kötü (≥10 cm sayısı, ≥20 cm sayısı). "Zeminde en kötü" = ayak gerçekten yerdeyken ölçülen kayma. Tur 5 değerleri tur 5 raporunun `final5_slide.txt` dosyasından.

| Plan | Hz | Tur 5 | Tur 6 (A) | Tur 6 zeminde en kötü |
|---|---|---|---|---|
| planU_A | 60 | 2.0 / 2.1 / 16.4 (4, 0) | 0.8 / 1.4 / **2.0** (0, 0) | 2.0 |
| planU_B | 60 | 2.2 / 3.4 / 29.8 (2, 2) | 0.9 / 1.7 / **2.8** (0, 0) | 2.8 |
| planSt2 | 60 | 2.0 / 4.0 / 11.3 (2, 0) | 0.9 / 1.9 / **3.3** (0, 0) | 3.3 |
| planQt | 60 | 1.5 / 2.4 / 9.9 (0, 0) | 1.2 / 2.2 / **5.9** (0, 0) | 3.3 |
| planK1 | 60 | 1.3 / 1.6 / 24.2 (1, 1) | 0.8 / 1.3 / **3.5** (0, 0) | 3.5 |
| planT1 | 60 | 2.0 / 2.7 / 16.7 (3, 0) | 1.1 / 1.6 / **10.6** (1, 0) | 1.9 |
| planC1 | 60 | 1.8 / 3.4 / 20.4 (2, 2) | 0.9 / 1.9 / **3.5** (0, 0) | 3.1 |
| planC2 | 60 | 3.4 / 9.5 / 19.0 (5, 0) | 1.3 / 2.2 / **7.8** (0, 0) | 7.8 |
| planDm | 60 | 2.0 / 3.1 / 16.8 (4, 0) | 1.2 / 1.8 / **14.8** (2, 0) | 2.2 |
| planSp | 60 | 1.1 / 1.7 / 3.3 (0, 0) | 0.7 / 1.3 / **1.8** (0, 0) | 1.8 |
| planR1 | 60 | 2.9 / 6.2 / 22.6 (4, 2) | 1.0 / 1.6 / **5.3** (0, 0) | 1.9 |
| planCv (çömelme) | 60 | tur 5'te 22.3 (ayrı plan) | 1.2 / 2.1 / **2.5** (0, 0) | 2.5 |
| planU_A | 30 | 1.5 / 2.5 / 21.3 (1, 1) | 0.8 / 1.5 / **2.8** (0, 0) | 2.5 |
| planU_B | 30 | 2.9 / 4.7 / 44.9 (4, 2) | 1.4 / 1.8 / **28.2** (1, 1) | 28.2 |
| planSt2 | 30 | 1.6 / 2.7 / 10.0 (1, 0) | 0.8 / 1.7 / **2.6** (0, 0) | 2.6 |
| planK1 | 30 | 0.9 / 1.7 / 4.4 (0, 0) | 1.3 / 1.6 / **27.1** (2, 0) | 27.1 |
| planC1 | 30 | 2.3 / 6.1 / 26.4 (2, 1) | 0.7 / 1.5 / **3.2** (0, 0) | 3.2 |
| planC2 | 30 | 2.9 / 8.3 / 18.5 (6, 0) | 1.0 / 1.7 / **3.7** (0, 0) | 3.7 |
| planCv | 30 | ölçülmedi | 1.0 / 1.9 / **2.5** (0, 0) | 2.5 |
| planU_A | değişken | 1.3 / 2.0 / 13.3 (1, 0) | 0.9 / 1.6 / **5.1** (0, 0) | 2.4 |
| planU_B | değişken | ölçülmedi | 1.9 / 1.7 / **76.4** (1, 1) | 76.4 |
| planK1 | değişken | ölçülmedi | 0.8 / 1.6 / **3.5** (0, 0) | 3.1 |
| planC1 | değişken | 2.1 / 3.3 / 32.6 (2, 2) | 0.9 / 1.6 / **4.2** (0, 0) | 1.8 |
| planC2 | değişken | 3.0 / 6.9 / 17.2 (4, 0) | 1.1 / 2.2 / **3.6** (0, 0) | 3.6 |

Durum A'da kalan üç aykırı örnek ve tur 6b sonrası (durum **B**, tekil ölçüm, `data/slide_x6b.txt`):

| Örnek | Durum A | Tur 6b sonrası (B) |
|---|---|---|
| planU_B değişken Hz — sprint 180° | 76.4 | **2.3** |
| planU_B 30 Hz — sprint 180° | 28.2 | **5.0** |
| planK1 30 Hz — kısa geri → ileri (yürüyüş→koşu geçişi) | 27.1 | tur 6b sonrası 30 Hz'de yeniden ölçülmedi (değişken Hz: 3.5) |

Gerileme notu: planK1 30 Hz, tur 5'te 4,4 cm iken durum A'da 27,1 cm tek temas içeriyor. Son zincir bunu yeniden ölçüyor; sonuç güncellemede yazılacak.

Yan etki denetimi: yerdeki ayağın kilit bırakılırken çekilmesi (`an_snap6.py`) bütün kayıtlarda 0; bacak uzaması ve kalça yüksekliği değişmedi. Süreklilik denetiminin işaretlediği kare sayısı bazı planlarda arttı (planK1 değişken: 9 → 31, yalnız bacak); bunlar görüntüyle eşleştirilmedi (açık madde).

Dönüş ağırlığı (durum A, `planT1`): koşuda 45° → hızın %90'ı, 90° → %68–71, 135° → %27; tur 5 ile aynı.

### 2.2 Çarpışma — durum A (60 Hz, `data/final6_contact_f6_reopen1.txt`; tam 25 senaryoluk matris: `data/ct_c6.txt`)

Gövde–engel çakışması yeni bir ölçümdür (`an_ct6.py`): görünür bedenin diz, baldır (3 nokta), uyluk, ayak, ayak ucu, kalça, el, dirsek ve baş noktaları, uzuv yarıçapı düşülerek engel kutusuna karşı sınanır. Tur 5 kayıtlarında bu ölçüm yoktu; tur 5 için tek kanıt videodur (09b, 4–5. saniye).

| Senaryo | Sonuç | Çakışma |
|---|---|---|
| Diz engeli, koşu 415 (zorunlu kabul testi) | denge kaybı → 37 cm geri adım → diz çökme → kalkma | yalnız çarpma anında ayak ucu 4,3 cm; çökme ve kalkma boyunca **yok** (30 Hz: aynı, 4,8 cm) |
| Diz engeli, tempo 278 | sendeleme | ayak ucu 5,0, diz 3,6 cm |
| Diz engeli, yürüyüş 180 | engelin önünde durur (60 ve 30 Hz) | yok |
| Diz engeli, yorgun (0,9) tempo | sendeleme (dinç yürüyüşte tepki yok) | yok |
| Diz engeli, taşırken (gerçek taşıma bayrağı, hız 187) | sendeleme, el desteği yok | yok |
| Duvar: yürüyüş / koşu / sprint | 20 cm önce durur, el yüzeyde | yok |
| Kütük (25 cm), sprint 585 | takılma → öne düşme → yatma → kalkma (30 Hz: aynı) | düşerken arkadaki ayak ucu 8 cm |
| Kütük, dinç koşu 415 | takılma → sendeleme | ayak ucu 8,4 cm |
| Basamak (30 cm × 60 cm), sprint | sendeleme (ilerisi düz değil → düşme yok) | baldır 5,8 cm |
| Dar alan (arkada 40 cm, zorlanmış eşikler) | geri adım kısalır → diz çökmez, ayakta destek | yok |
| Merdiven sprint, merdiven koşu, rampa koşu | tepki yok (yanlış takılma yok) | — |
| Yan duvar sıyırma | hız düşer, kol çekilir | dirsek 7,6 → **5,1** cm (B), el 6,3 cm |
| Alçak kiriş (alt yüz 150 cm) | durum A: önünde duruyordu; **B**: çömelip geçer, baş en fazla 113 cm | yok |

Avuç hizalama (durum B, `an_palm6.py`, `pv6a_wall`): destek elinin avuç yönü ile yüzeye dik yön arasındaki açı ortalama **86° → 4°**, parmak yükselişi 84°. Bu sayısal ölçümdür; görüntü doğrulaması son zincirin videosunda.

### 2.3 Başlangıç ve merdiven — durum B (tekil ölçüm)

| Ölçüm | Önce (durum A) | Sonra (B) |
|---|---|---|
| Koşu başlangıcı: baş alçalması / gövde eğimi en fazla | 32,3 cm / 26° | **12,7 cm** / 14,8° |
| Tempo başlangıcı: baş alçalması | 32,9 cm | 19,6 cm |
| Sprint başlangıcı: baş alçalması | 28,5 cm | 20,1 cm |
| Koşuda hızın %90'ına ulaşma | 0,67 s | 0,43 s |
| Başlangıç planlarında en kötü kayma (planSp, planStart6) | 1,8 cm | 1,6 / 2,0 cm |
| Merdiven yürüyüş: diz açısı en düşük / %5 | 45° / 54° | **60° / 71°** |
| Merdiven yürüyüş: kalça, öndeki ayağın üstünde (ortalama) | 52 cm | 62 cm |
| Merdiven yürüyüş: en kötü kayma | 2,1 cm | 2,1 cm |

Yorgunluk (durum A, `data/final6_posture_reopen1.txt`): 14 s sprintte 0 → 0,63'e kademeli artış, duruşta 0,82 tepe, ~12 s'de sönüm; gövde eğimi dinç duruştan ≤ 1° farklı. Geçiş anları artık ayrı raporlanıyor (`an_post6.py`: her bölümün ilk 1,2 s'si ve kararlı kısmı, tepe değerler ve 0,1 s'deki en büyük değişim).

---

## 3. Değişen varlıklar

| Varlık | Değişiklik |
|---|---|
| `Sphirus/Player/GASP/ABP_Sph_GASP` | `PlantSettings_Default / _Stops` (eşik, yarıçap, açı) |
| `Sphirus/Player/Motion/AC_Sph_Motion` | K gevşetme, ters dönüş giriş hızı ve taban fren, başlangıç / yeniden itiş ivmesi (`KRelax`, `StBoost*`) |
| `Sphirus/Player/GASP/BP_Sph_GASPCharacter` | `CalculateMaxAcceleration`, `CalculateBrakingDeceleration`, `CalculateGroundFriction` |
| `Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player` | `GR_Contact` (v2), duruş olayı (omurga koruma, hamle sınırlayıcı), yumuşak başlangıç satırı, `CT_*` / `GR_SoftStart*` değişkenleri |
| `Sphirus/Player/GASP/ABP_Sph_Body_GASP` | avuç için iki `ModifyBone` düğümü + `PalmR/L`, `PalmAR/AL` |
| `Sphirus/Player/Anim/Fall/SphF_*` (4 yeni klip) | retarget edilmiş düşme / kalkma klipleri |
| `Sphirus/Test/L_Sph_MoveTest` | yeni test şeritleri: kütük, dar alan, alçak kiriş, itilebilir kutu |

Geri dönüş: `Saved/UE59Work/checkpoints/20261122_round6_start` (134 varlık + ayarlar + kullanıcı kaydı) ve her yazma işi için doğrulanmış yedek (`data/manifests.txt`, `ue59_m26_*`).

Kaydetme ve yeniden açma: değerler yeniden açılan editörde diskten okundu (`data/saved6.txt`). Kullanıcı kaydı `SFSaveSlot.sav` SHA1 `3d81ab9d…` (tur başıyla aynı). Bu turda arka planda kalan bir doğrulama zinciri dosyayı iki kez kayıt aracının park klasöründe bıraktı; ikisinde de kullanıcı onayıyla yerine kopyalandı, içerik değişmedi.

---

## 4. Videolar (bu ara raporda)

| Dosya | İçerik | Durum |
|---|---|---|
| `videos/01_omuz_…` | gerçek omuz kamerası: bekleme → yürüyüş → tempo → koşu | A (yumuşak başlangıçtan önce) |
| `videos/02_yan_…` | aynı plan, tam beden yan görünüm | A (yumuşak başlangıçtan önce) |
| `videos/03_yan_diz_engeli_…` | koşarak diz engeli: geri adım → diz çökme → kalkma | kaydetmeden önce, mantık aynı |
| `videos/04_yan_kutuk_sprint_…` | kütüğe sprint: takılma → düşme → yatma → kalkma | kaydetmeden önce; düşüş mesafesi sonradan 198 → 154 cm'e kısaltıldı |
| `evidence/01`, `02` | düşme ve kalkma kare şeritleri | aynı kayıt |

Yorgunluk, bekleme, dönüş, duvar / avuç, dar alan, taşıma, alçak kiriş, merdiven videoları ve ev akışları (yatak, maske, odun → şömine) son zincirde üretiliyor; bu commit'te **yoktur**.

---

## 5. Yapılmayanlar ve açık kalanlar

1. **Son durumun tam oynanış doğrulaması sürüyor** (durum C): kayma (24 kayıt), temas, duruş, arazi, videolar, ev akışları. Tur 6b sayıları şu an tekil ölçümdür.
2. **Performans ölçülmedi.** Yeni temas olayı karede 16 çizgi sorgusu yapıyor; maliyeti ve kare süresi sıçramaları henüz ölçülmedi.
3. **Standalone / paket çalıştırma yapılmadı.**
4. **Ev akışları yeni sistemle henüz çalıştırılmadı** (yatak, maske, çay, gardırop, odun → şömine, kayıt / yükleme). Duvar önünde 20 cm durma kuralının ev içi etkileşimlere etkisi bilinmiyor.
5. **Gamepad test edilmedi** (yukarıda).
6. **Merdiven**: diz açısı 60–71°; doğal değer ~95°. Merdiven inişi ölçülmedi (test şeridinde iniş planı yok).
7. **Engelin üstünden yürüme**: yürürken ve tempoda ayak ucu kütüğe 10–13 cm giriyor. Yavaşlatma denendi, işe yaramadı, geri alındı; savrulan ayağı engele göre kaldıran bir katman yok.
8. **Sıyırmada dirsek** 5 cm, el 6 cm duvarın içinde (kapsül duvara 6 cm mesafede).
9. **Tempo / sprint başlangıcı**: baş alçalması 20 cm; koşudaki kadar düşmedi.
10. **Taşırken yere düşme** oyunda oluşamıyor (taşırken hız 187, takılma eşiği 330 cm/s); taşırken sendeleme doğrulandı. Tek elle taşımada boştaki elin desteği uygulanmadı.
11. **Destek ayağına göre tepki**: çarpma anındaki destek ayağı kaydediliyor ve raporlanıyor, ama tepkinin yönünü değiştirmiyor.
12. **Süreklilik işaretleri** görüntüyle eşleştirilmedi; ayak kilidi bırakılırken bacakta kısa hareket artışı olabilir.
13. **Ham kayıtlar** (kayıt başına 12–22 MB JSON) bu commit'te yok; son zincirden sonra sıkıştırılmış olarak eklenecek.
14. Şömine yanındaki parlak nokta, çay / gardırop / görev sırası, hareketli ve itilebilir nesnelerle ayrıntılı test (itilebilir kutu yalnız "takılma → sendeleme" verdi), başka karakterle temas: bu turda ele alınmadı.

---

## 6. Yeniden üretim

Betikler `scripts/` altında, önceki turlardan kullanılan parçalar dahil (`an_slide3.py`, `an_popsum.py`, `an_contw.py`, `an_carry5.py`, `an_fat5.py`, `an_turn5.py`, `hk_pose3.py`, `seqP.sh`, `run2.sh`, `vc59.sh`, `vidm_patch.py`, `vid.py`, `loadmap.py`), girdi planları `scripts/plans/` altında.

- Doğrulama zinciri: `final7.sh` (aşamalar: `final6.sh slide|posture|contact|terrain <etiket>`), temas matrisi `ctall6.sh`, tek senaryo `ct6.sh`.
- Çözümleyiciler: `an_ct6.py` (olaylar + gövde–engel çakışması), `an_post6.py` (geçiş / kararlı duruş), `an_terr6.py` (arazi; tur 5'teki `nan / n 0` ve havada kalma hatası düzeltildi), `an_palm6.py`, `an_snap6.py`, `an_dump6.py`.
- Uygulama betikleri (yeniden uygulanabilir): `m_gov6*_mcp.py`, `m_contact6_mcp.py`, `m_posture6_mcp.py`, `m_softstart6_mcp.py`, `c_plant6.py`, `c_palm6.py`, varsayılanlar `c_*6_defaults.py`.
