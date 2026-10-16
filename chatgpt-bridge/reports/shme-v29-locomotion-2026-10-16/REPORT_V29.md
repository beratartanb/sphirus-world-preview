# SHME V2.9 — Dönüş bütünlüğü + ayak–diz–pelvis uyumu (2026-10-16)

**İstek:** önce mevcut bozuklukları düzelt (eğimde / tek ayak yüksekte bacak, ikinci çökme, burulmuş dizler, parçalı dönüş),
sonra destek adımlı ve ağırlık aktarımı görünen dönüşleri aynı görevde uygula; gerçek oyun zincirlerinde ölç, kaydet, yayımla.

**Sonuç (kısa):**
- **Geriye bükülen / burulan dizler — giderildi (kaynak: bizim klip bake'lerimiz).** 76 proje klibinde diz menteşesi
  bozuktu (eski IK bake'lerinin "diz ipucu" hatası). Ayak dönüşümü birebir korunarak onarıldı.
  - Yüzey koşularında geriye bükülen diz karesi: aşama başına 62'ye kadar → **0**.
  - Satıcı (AAMS) klipleri sağlam; dokunulmadı.
- **Engebeli zeminde duruştan sonra ikinci çökme / yere gömülen ayak — giderildi (kaynak: idle "duruş tutma" anlık görüntüsü).**
  - V1.2'den beri idle, duruşun SON pozunun (FootPlacement zemine uyarlamış hâli) anlık görüntüsünü tutuyor ve onu yeniden
    FeetIK'ten geçiriyordu. Zemin uyarlaması ikinci kez uygulanıyordu.
  - Örnekler: 10 cm basamakta zemindeki ayak 9 cm yere gömülüyordu, pelvis 19–22 cm iniyordu; 8° eğimde ayak açısı iki kat; çapraz eğimde alçak ayak 8 cm içeride.
  - Düz zeminde uyarlama sıfır olduğu için önceki düz zemin testleri bunu göstermiyordu.
  - Düzeltme: tutulan poz IK öncesi eşdeğerine geri çevriliyor; FootPlacement artık bir kez uyarlıyor.
  - Sonuç: ayak–zemin boşluğu her yüzeyde **≤ 1.8 cm**; 10 cm basamakta pelvis inişi **19.2 → 10.3 cm** (bu, tek uyarlamanın geometrik gereği).
- **Parçalı yerinde dönüş — giderildi (kaynak: çift telafi).**
  - Dönüş montajı kapsülü kendi kök hareketiyle döndürüyordu; SHME'nin eski kök sayacı bunu iptal edip 90°/sn ile geri sarıyordu.
  - Sonuç: kalçalar dönüşe ters 50–70° savruluyordu, basılı ayaklar 20–30 cm buruluyordu, yürüyüşe kalkınca kalan açı tek karede atlıyordu.
  - Düzeltmeden sonra kapsül–kalça ayrılması **64–224° → 25–71°** (klibin kendi gecikmesi); kalçanın dönüşün yarısına gelme süresi **0.5 s / hiç → 0.05–0.35 s**; dönüş pop'ları 7–12 → 1–5.
- **Dönerken burulan bacak (180° yerinde dönüş) — giderildi (kaynak: basma kilidi tipi).**
  - Ayakta duran ön ayar ayağın yönünü kilitliyor (LockRotation, 60° açılma). Klip topun üzerinde pivot yaparken ayak dönemiyordu; kalça ile basılı ayak arası 110–119°'ye çıkıyordu (klibin kendisinde 38–62°).
  - Dönüş montajı sırasında topun etrafında pivot ön ayarı kullanılıyor: **37–70°**, top kayması ≤ 2 cm.
- **Hareket hâlinde destek adımlı dönüşler — uygulandı, kısmen kabul edilebilir (görsel / his kabulü senin).**
  - Depar 90° kesişi artık satıcının destek adımlı depar dönüş kliplerinden oluşan yeni köprüyü kullanıyor: fren çökmesi ve dönüşe eğilme görünüyor.
  - Fare ile hızlı 180° (depar / tempolu) artık ters dönüş köprüsüne gidiyor; eskiden ters köprü hiç seçilmiyor, 4–6 veritabanı arasında (bazı koşularda depar başlangıçları dâhil) geçiş yapılıyordu.
  - Tempolu ileri↔geri dönüşte araya giren yürüyüş döngüsü kalktı; ikinci dönüşte ayak kayması **15.6 → 4.4 cm**.
  - Açık:
    - Depar kesişi klibi dönüşün ancak ilk yarısında kalıyor (kapsül 0.65 s'de dönüyor, klip 1.2 s istiyor).
    - İlk basan ayak her zaman dış ayak değil.
    - Tempolu fare dönüşü için koşu dönüş klipleri bağlanmadı (§5).
- **Teknik PASS / görsel inceleme / kullanıcı kabulü ayrı:**
  - Teknik ölçümler §3–§6.
  - Görsel inceleme §7: bel altı yan / çapraz kayıt ve oyun kamerası; gerçek video (AVI) + GIF.
  - **His / kontrol kabulü NOT_TESTED:** bkz. `USER_PLAYTEST_V29.md`.

## 1. Başlangıç durumu ve ölçüm yöntemi
- **Okunanlar:** AGENTS.md, CLAUDE.md, skill'ler (`sphirus-game-dev-director` → SHME / QA), V2.8 raporu ve oyun testi rehberi.
- **Başlangıç doğrulaması:**
  - UE 5.8; pawn zinciri BP_PBI_Player → BP_GR_Player → BP_Player_MM.
  - Sürücü: `ABP_GR_MotionMatching` (Mascot, gizli). Görünür: Manny/MetaHuman `ABP_MH_Ranger_Retarget_V2` + `ABP_LK_Body_PostProcess`.
  - V2.8 değerleri (`SHM28_StopMode 1`, `SHM28_StartMode 0`) canlıda doğrulandı.
  - Başlangıç adayı açılmadı: V2.8'de kısa basmalarda regresyon ölçülmüştü, durum değişmedi.
- **Yedek (git yok):**
  - Her varlık değişikliğinden önce `.uasset` kopyası + SHA256 (`Saved/Codex/SHME_V29_20261016/checkpoint/`).
  - Kopyalar: `baseline_v28`, `knee_repair_before` (76 klip), `before_v29_abp_save`, `before_sprintcut`, `before_v29b_save`, `before_tp_save`.
- **Karşılaştırılabilirlik:**
  - Her varyant aynı girişle (gerçek IA_Move / IA_Look yolu), aynı başlangıç pozu / zemin / ayarlarla koşuldu.
  - Tüm ABP bayrakları her koşuda açıkça verildi (harness bunları sıfırlamıyor).
  - Bellekte (kaydedilmeden) yapılan denemeler her koşudan sonra diskten geri yüklendi (`fp_restore.py`).
- **Test yüzeyleri** (yalnız PIE dünyasında geçici kutular): düz, sol ayak 10 cm yüksek, sağ ayak 10 cm yüksek, 8° eğim, 10° çapraz eğim, 18 cm basamak dizisi.
  - Her yüzeyde: yürüyüş / tempolu / depar duruşu → idle → 180° dönüş → geri yürüme.
- **Araçlar (`Tools/SHME_V29_20261016/`):**
  - `legs.py`: diz menteşesi, fleksiyon, top–zemin boşluğu, pelvis düşüşü (aşama başına, sürücü + görünür mesh).
  - `turns.py`: kapsül / kök / kalça / göğüs / ayak sapma açıları, ayrılma, gecikme, basılı ayak dönmesi.
  - `cuts.py`: hareket hâlinde yön değişimi; hız kaybı, hizalanma süresi, yanal g, destek adımları, fren çökmesi, seçilen veritabanı.
  - `pop_report.py` (V2.1).
- **Diz metriği:**
  - Menteşe = dot(diz düzleminin normali, baldır yerel Z).
  - +1 doğru, < 0 geriye bükülü, < 0.7 45°'den fazla burulmuş. Satıcı kliplerinde 0.98–1.0.
  - Görünür MetaHuman baldırında aynı değer ölçülüyor.
- **Toplam:** ~170 PIE koşusu.
  - 2 bellek yeniden başlatması, 1 editör yeniden başlatması (kendi hatam, §9).
  - Örtüşen iki toplu koşunun verisi atıldı ve temiz tekrarlandı.

## 2. Ayak–diz–pelvis: neden ve düzeltme
### 2.1 Diz menteşesi (klip kaynaklı)
- **Tarama:**
  - 1074 klip tarandı: bozuk olan 76 klibin hepsi proje klibi. Satıcı klibinde bozuk diz yok.
  - Bozuk diz, eski bake'lerin (`v137_animedit.solve_leg`, "diz ipucu" ile) diz düzlemini kaynaktan alıp kemikleri en kısa yay ile döndürmesinden geliyor.
  - Etkilenen bake'ler: V1.3.7 duruş, V2.6–V2.8 başlangıç / duruş, WDIAG, V2.8 üretici.
- **Onarım** (`v29_knee_repair.py`):
  - Kötü karelerde diz düzlemi ayağın menteşe eksenine çevriliyor; ±3 kare rampa.
  - Diz üçgenle yeniden kuruluyor. Ayak bileşen dönüşümü birebir korunuyor: hata 0.000 cm, fleksiyon değişimi 0.
  - 76 klip: menteşe min −0.37 … 0.70 → ≥ 0.90.
- **Oyunda:** 18 yüzey koşusunda geriye bükülen diz karesi 0. Duruş sonu "geriye bükük sağ diz" kalktı.
- **Not:** Manny ile görünür ayaklar örtüşüyor diye diz doğru demek değil. Görünür baldırda da ayrı ölçüldü.

### 2.2 Engebeli zeminde ikinci çökme (çalışma zamanı kaynaklı)
- **Ayrıştırma:**
  - Klip pozu ≠ sorun: CP duruşunun sonunda tek uyarlama doğruydu (ayak zeminde).
  - Bozulma tam idle'a geçiş karesinde başlıyor: 6 karede zemin ayağı 10 cm daha iniyor, pelvis de iniyor.
- **Elenen hipotezler (tek değişkenli A/B):** FootPlacement ayarları bu bozulmanın sahibi değil.
  - MaxGroundPenetration 20→2, pelvis MaxOffset 250→12, PelvisHeightMode AllLegs→AllPlantedFeet.
  - Üçünde de idle pelvis düşüşü 19.1–19.4 cm, değişmedi.
- **Kök neden:** V1.2 idle tutma `SavePoseSnapshot` son pozu alıyor. Bu poz FeetIK, PBI ve kök sayacı uygulanmış hâli.
  - Poz FeetIK'in önüne geri veriliyor.
  - FootPlacement zemin farkını, pelvis ofsetini ve eğim hizalamasını ikinci kez uyguluyor.
  - Kök sayacı da ikinci kez uygulanıyor.
- **Düzeltme** (`install_hold_deadapt.py`, kaydedildi):
  - FeetIK_Layer'a 28 BoneDrivenController (eğri) eklendi: FootPlacement öncesi ve LegIK sonrası pelvis T/R ve ik_foot TZ/R.
  - `SHM_HoldDeadapt` fonksiyonu (anlık görüntü karesinde) farkları hesaplıyor.
  - Tutma dalı kökü sıfırlıyor, pelvisi geri alıyor, ayakları TwoBoneIK ile IK öncesi hedefe taşıyor (kemik boyları korunuyor) ve ayak dönüşünü geri alıyor.
  - Sonuç: FootPlacement bir kez uyarlıyor, tüm sonraki karışımlar aynı türden pozları karıştırıyor.
  - IK kapatılmadı, pelvis kilitlenmedi, diz bükümü kaldırılmadı. Geri alma anahtarı: `SHM_HC_Off`.

| Yüzey (duruş sonrası idle, sürücü) | Ayak–zemin boşluğu L / R (önce → sonra, cm) | Ek |
|---|---|---|
| Sol ayak 10 cm yüksek | −11.4 / −9.3 → −1.7 / −0.6 | pelvis düşüşü 19.2 → 10.3; diz fleks 78/81° → 62/57° |
| Sağ ayak 10 cm yüksek | −11.3 / −9.8 → −1.7 / −0.6 | diz fleks 79/81° → 55/66° |
| 8° eğim | −5.2 / −3.6 → −1.6 / −0.4 | ayak eğimi duruş sonundaki değerde kalıyor (önce +8° fazla) |
| 10° çapraz eğim (yürüyüş / tempolu) | −10.2 / −8.1 → −1.8 / −0.7; −9.3 / −9.1 → −1.5 / −0.6 | diz fleks 56/58° → 45/42° |
| 18 cm basamak (tempolu) | sağ −17.6 → −2.5 | pelvis "düşüşü" 46.8 → 16.3; kalan sol −16 bir ölçüm artefaktı (aşağıda) |
| Depar, sol ayak yüksek | −4.3 / −8.1 → −1.5 / −0.6 | pelvis düşüşü 22.1 → 13.0 |
| Düz zemin | değişmedi | regresyon yok |

- **Basamak notu:** kapsül basamağın kenarına oturuyor, iki ayak da aradaki zeminde doğru duruyor. Kalan "−16 cm", parmak ucu basamak yüzüne değdiğinde tek çizgilik iz sürmenin basamak üstüne vurmasıdır.
- **Kalan (açık):**
  - FootPlacement pelvisi yalnız dikey taşıyor (yuvarlama / yana kaydırma yok). 10 cm basamakta ~10 cm iniş geometrik gerek; gerçek insan bunu kısmen pelvis eğmesiyle yapar.
  - Doğuş idle'ında sol dizde küçük yana bükülme (fleks ~11°, menteşe 0.47; LegIK neredeyse düz bacakta). Bu görevden önce de vardı; değişmedi, düşük öncelik.

## 3. Parçalı dönüş: neden ve düzeltme
- **Sahiplik:**
  - Ayakta fare dönüşü `BP_GR_Player.GR_UpdateIdleTurn` tarafından tam gövde DefaultSlot montajı olarak oynatılıyor.
  - ABP kök hareket modu "RootMotionFromMontagesOnly". Kapsül klibin kendi kök eğrisiyle dönüyor (180° klipte %98'i 0.43 s'de).
  - Yani kapsül sahibi montajın kök hareketi.
- **Çift telafi:**
  - SHME V1.3.2 kök sayacı her ayakta kapsül dönüşünü iptal ediyor, sonra 90°/sn ile geri sarıyordu (o dönemde dönüş montajı yoktu).
  - Kalça klipte kökten 40–68° geride kalıyor. Kök "tutulunca" kalça dönüşe ters 50–70° savruluyor gibi görünüyordu.
  - Basılı toplar kök tutulunca 20–30 cm kayıyordu; klip kökü uygulanınca yalnız 1–4 cm.
  - Montaj bitince ya da yürüyüş başlayınca kalan ~90° 0.15 s'de serbest bırakılıyordu (yürüyüş başlangıcında 72° / 2 kare atlama).
  - 1 karelik gecikme: kapsül dönüyor, sayaç bir kare sonra.
- **Düzeltme** (`install_idle_wait.py` içinde, kaydedildi):
  - DefaultSlot montajı varken kapsül sapması telafi edilmiyor.
  - Montaj yine "dönüş" sayılıyor (tutma / devralma serbest, sonda yeni duruş görüntüsü), ama yalnız 0.3 s karışma süresinden sonra.
  - İlk karede serbest bırakmak, ~0 ağırlıklı montajın altında kaynak pozu değiştirip eğimde 70–77 m/s² omuz pop'u yapıyordu. Bulundu ve düzeltildi: 77 → 34.
  - Geri alma anahtarı: `SHM29_TipOld`.

| Senaryo | Kapsül–kalça ayrılması | Kalça gecikmesi (%50) | Pop (>25 m/s²) |
|---|---|---|---|
| Yavaş fare 45–180° (yerinde) | 64–124° → 25–44° | 0.49–0.62 s / hiç → 0.13–0.35 s | 7 (52) → 1–2 (≤28) |
| Hızlı fare 90/180° | 110–224° → 34–71° | hiç → 0.05–0.28 s | 7–12 (96–110) → 2–5 (≤38) |
| Hızlı fare 180°: kalça – basılı ayak | 110–119° (klip 38–62°) | — | pivot ön ayarıyla 37–70°, top kayması ≤ 1.6 cm |
| Yürü → dur → 90° → yürü | 120° → 44° | 0.71 → 0.21 s | 2–3 (66–82) → 1 (28); yürüyüş başlangıcında atlama yok |
| 10 cm şerit + 180° | 213° → 70° | hiç → 0.17–0.22 s | 3 (130–172) → 1 (36–56) |
| Eğimde dur → sağ / sol 90° | 44° | 0.21 s | 1–2 (70–81) → 0–2 (≤ 34) |

- **Montaj ilk karesi:** dönüşü ilk karede "dönüş" saymak tutma pozunu ~0 ağırlıklı montajın altında değiştiriyordu (eğimde 70–81 m/s² omuz pop'u). Bulundu ve 0.3 s gecikmeyle giderildi.
- **180° dönüşte bacak burulması:** oyunda kalça–basılı ayak ayrılması 110–119°'ye çıkıyordu, klibin kendisinde 38–62° (`probe_tip180_feet.py`).
  - Sahip: ayakta duran basma ön ayarı (LockRotation, 60° açılma açısı) ayak yönünü kilitliyordu.
  - Düzeltme: dönüş montajında `PlantSettings_Stops` (PivotAroundBall). Topun kayması azaldı (2.3 → 1.6 cm), ayak klipteki gibi pivot yapıyor.
  - Şerit üstü 180°: 62.6 → 40.3°; eğimde 52 → 39°; yürü-dur-dön 65 → 37°.
  - Geri alma: `SHM29_TipOld` ile birlikte kapanıyor.

## 4. Hareket hâlinde dönüşler: envanter, kararlar, yeni davranış
- **Açılarak incelenen klipler** (isme göre değil; `probe_turnclips.py`):

| Aile | Giriş → min → çıkış (cm/s, klip hızı) | Dönüş süresi | Pelvis çökmesi | Durum |
|---|---|---|---|---|
| Depar dönüş 90° L/R × L/R ayak (AAMS) | 721 → 518 → 721 | %10→90: 0.8 s (proje hızında ~1.2 s) | 16–21 cm | canlı DB'de var, ama 90° kesişte hiç seçilmiyordu |
| Depar dönüş 180° | 721 → ~5 → 721 | 0.3–0.5 s | 23–33 cm | ters dönüş köprüsünde |
| Koşu dönüş 90/135/180° | 515 → 319/53/0 → 515 | 0.4–0.6 s | 26–33 cm | **hiçbir canlı DB'de yok** |
| Yürüyüş dönüş 90/180° | 206 → 164/8 → 206 | 0.4–0.5 s | 3–7 cm | DB'de yok (yürüyüşte döngüler yeterli, §5) |
| Koşu / tempolu pivot F→B | 515 / 245 → 0 → … | — | 13–21 cm | ters dönüş köprülerinde |

- Tüm adaylarda diz menteşesi 0.99.
- Koşu / depar dönüşlerinde basılı top klip hızında 13–50 cm/s yuvarlanıyor. Proje oynatma hızında FootPlacement'in 60 cm/s basma eşiğinin altında, yani kilitlenebiliyor.
- **Neden 90° kesişlerde destek adımı yoktu:**
  - V2.1 "yanal bölüm kapalı" kuralı 110°'nin altındaki her yönlendirme bölümünü yok sayıyor.
  - "Pivot" eşiği 115°. Depar 90° kesişi yalnız döngülerle yapılıyordu: 1.2 g yanal, ilk basan iç ayak, fren yok.
- **Neden fare ile 180° dağılıyordu:** bölümün sınıfı ilk karede sabitleniyor. Fare dönüşü hedef yönü ~0.25 s'de çevirdiği için ilk karede açı 52°. 180° yanal sanılıp atlanıyor, 4–6 veritabanlı dur-kalk zinciri oluşuyordu.
- **Uygulanan (kaydedildi, `SHM29_CutMode = 2`):**
  1. **Niyet açısıyla sınıflandırma:**
     - Bölümün ilk 0.3 s'sinde max(hız–hedef, başlangıç hızı–güncel hedef) zirvesi kullanılıyor.
     - İlk karede kararsız (niyet < 70°, yani fare dönüşü) bölümler zirve 120°'yi geçene ya da pencere bitene kadar bekliyor.
     - Geç aktivasyon / ters dönüşe yükseltme köprüyü yeniden seçtiriyor.
  2. **Depar kesiş köprüsü `PSD_SHM_SprintCut`:**
     - İçerik: satıcının 4 depar 90° destek adımlı dönüş klibinin proje kopyaları + `A_LB_Sprint_Fwd`.
     - Depar yanal bölümleri artık atlanmıyor. Tempolu yanal kesişler V2.1 kuralıyla döngülerde kalıyor.
  3. **Ters dönüş kuyruğu:** bölüm bittikten sonra hız < 150 cm/s ve giriş varken köprü 0.4 s daha tutuluyor. Araya yürüyüş döngüsü girmiyor.
  - Geri alma: `SHM29_CutMode 0` = V2.8, `1` = yalnız 1 ve 3.

| Zincir (c0 = V2.8 mantığı → c2 = üretim) | Önce | Sonra |
|---|---|---|
| Depar → 90° kesiş (çubuk) | yalnız döngü; pelvis çökmesi 4 cm; üst gövde ivmesi pencere max 17 m/s² | kesiş köprüsü; çökme 9.4 cm, öne / içe eğilme; pencere max 37–50 m/s²; ilk basan iç ayak (0.5 s) |
| Depar, fare 90° | döngü; dış ayak bazen 1.1 s sonra | köprünün kullanıldığı 3 olayın 2'sinde dış ayak ilk (0.10–0.37 s), birinde iç ayak; çökme 7–14 cm |
| Depar, fare 180° | ters köprü yok; 4–6 DB, bazı koşularda depar başlangıçları; çökme 7.6 cm | ters köprü (DirectionalSafe → SprintReversal → jog → depar), fren çökmesi 24–26 cm |
| Tempolu, fare 180° | 5 DB, jog pivot arada | 4 DB, ters köprü |
| Tempolu ileri↔geri | yürüyüş döngüsü araya giriyor; 2. dönüşte kayma 15.6 cm | yürüyüş döngüsü yok; kayma 4.4 cm |
| Tempolu A/D kesiş, W+A↔W+D | dış ayak ilk 0.03–0.25 s, 0.82–0.87 g, kayma 4–9 cm | aynı (değişmedi) |
| Yürüyüşte ±30° | %0–2 hız kaybı, 0.22 g, kayma 3.7–4.3 cm | aynı |
| Tempolu fare yavaş dönüş, depar geniş viraj | kapsül–kalça 7–19°, adım yok | aynı; depar virajında sapma adımı 2–5 → 0–1 |
| Dokun → bırak → tekrar → çapraz | start-transfer yönlendirmesi normal | aynı |

- **Görsel değerlendirme (benim, his kabulü değil):**
  - Depar kesişinde eski hâlde dik bir depar adımı dönerek ilerliyor.
  - Yenide 0.15–0.45 s boyunca dizler bükülüp gövde içe ve öne eğiliyor; kısa fren adımları var. Ağırlık aktarımı okunuyor, ama çökme belirgin; "fazla mı?" kararı senin.
  - Ters dönüşte belirgin fren, pivot ve yeniden hızlanma var.
- **Kalan / bilinçli bırakılan:**
  - Depar kesiş klibi dönüşün ilk yarısında kalıyor. GR dönüş sınırı (TurnLatAccelMax 1400) kapsülü 0.65 s'de döndürüyor, klip 1.2 s istiyor; köprü yarıda bırakılıyor.
    - Sınırı düşürmek (800 / 500) 0.74 g ve 0.72 s verdi, ama tempolu dönüşü de etkileyeceği için üretime alınmadı.
    - Önerilen: depar'a özel sınır (GR'de küçük bir parametre).
  - İlk basan ayak her kesişte dış ayak değil (çubuk 90°'de iç ayak 0.5 s).
  - Tempolu **fare** dönüşleri (yüz + hız birlikte dönüyor) için koşu dönüş klipleri bağlanmadı.
    - Neden: kapsül bakışa 300°/sn ile dönüyor, klip ~0.7 s istiyor. Önce kapsül dönüş hızının klibe bağlanması gerekiyor.
    - Bu, oyun hissini değiştiren bir karar; döngü tabanlı hâl tutarlı (§3 tablosu son satır).
  - Kontrollü savrulma + toparlama adımı: yalnız ters dönüş / kesiş klibinin içindeki fren-adım olarak var. Ayrı "momentum taşması + toparlama" davranışı eklenmedi → **NOT_TESTED / açık**.

## 5. Yeniden kullanılan / yeni / yeniden bağlanan klipler
- **Yeni (proje kopyası, satıcıya dokunulmadı):** `SHM_M_Neutral_Sprint_Turn_L_090_Lfoot`, `_L_090_Rfoot`, `_R_090_Rfoot` (`R_090_Lfoot` zaten vardı).
- **Yeni veritabanı:** `PSD_SHM_SprintCut` (5 giriş). `SHM_RedirectDB_SL` artık buna bakıyor.
  - Eski `PSD_SHM_Redirect_SprintLateral` duruyor, kullanılmıyor.
- **BranchIn izi eklenen:** `A_LB_Sprint_Fwd` ve 4 kesiş kopyası (yalnız yeni DB için).
- **Onarılan (diz):** 76 proje klibi (liste `Saved/Codex/SHME_V29_20261016/kr_apply.json`); aralarında 8 duran dönüş klibi.
- **Yeniden kullanılan:** V1.3.5 ters dönüş köprüleri (`JogReversal`, `SprintReversal_L/R`), V1.3.8 duran dönüş klipleri, V2.8 duruşları.
- **Bağlanmayan (kanıtla):** koşu dönüş klipleri (§4), yürüyüş dönüş klipleri (yürüyüş ±30°'de döngüler doğal; 0–2% kayıp).

## 6. Doğrulama zincirleri ve kare hızları
- Zincirler: §3 / §4 tabloları. Hepsi gerçek giriş yolu; eski / yeni mantık aynı koşullarda, aynı editör sürecinde.
- **Kare hızları** (konsol `t.MaxFPS`; elde edilen = telemetri hızı):
  - 30 (standart): 25–33 fps. 20: 19–20 fps ✓.
  - 60: yalnız 23–30 fps elde edildi (editör PIE + yakalama) → **60 fps NOT_TESTED** (ulaşılamayan hız geçti sayılmaz).
  - 20 fps'te sonuçlar korunuyor: şerit ayak boşluğu −1.8 / −0.6 cm; yürü-dur-dön kapsül–kalça 44° (eski mantık 118.6°); depar kesiş köprüsü seçiliyor.
- **Son doğrulama (kaydedilmiş üretim, harness bayrağı olmadan):**
  - Şerit / çapraz eğim boşluğu ≤ 1.8 cm (görünür MetaHuman dizi sürücüyle aynı).
  - Hızlı dönüş kapsül–kalça 34–71°, kalça–ayak 37–69°.
  - Depar kesiş + ters köprü; tempolu ileri↔geri kayma 2.0 / 0.6 cm.
  - Accessed None 0, PoseSearch indeks atlaması 0, editör günlüğünde Blueprint çalışma hatası 0.
- **Teknik doğrulama (diskten taze yükleme):**
  - 28 ölçüm düğümü, `SHM_HoldDeadapt`, 2 TwoBoneIK, basma ön ayarı seçimi.
  - Varsayılanlar `SHM29_CutMode 2`, `SHM29_TipOld false`, `SHM_HC_Off false`.
  - Pawn profilleri yerinde, kirli paket yok, derleme 0 hata (uyarılar önceden de vardı).

## 7. Görseller ve videolar (`img/`, `vid/`)
- **Kamera / ışık:**
  - Pawn'ı izleyen ama dünya yönü sabit yan ve ön-çapraz kamera; dönüşte kamera dönmüyor.
  - Pawn'a bağlı 3 dolgu ışığı. QA zemini. Gerçek zamanlı 30 fps yakalama (elde ~22 fps).
- **Kadraj — bel altı (kalça + diz + ayak aynı karede):**
  - Tam gövde ön görünümlerde kıyafette göğüs bölgesinde ten görünen bir delik / içinden geçme var (§9). Bu karelerin hiçbiri yayımlanmadı.
  - Gövde–kalça uyumu ölçümle verildi (§3).
- **Videolar:** `*_realtime.avi` (gerçek hız) ve `*_slow3x.avi` (1/3 hız) MJPEG; GitHub'da indirilip oynatılır. Ayrıca satır içi GIF.

| Dosya (eski → yeni) | Ne gösteriyor |
|---|---|
| `img/stripfeet_old.jpg` / `img/stripfeet_new.jpg` | 10 cm şerit, duruştan sonra ayaklar (yakın plan): eskide zemin ayağı bileğe kadar yere gömülü |
| `img/slopefeet_old.jpg` / `img/slopefeet_new.jpg` | 8° eğimde duruş: eskide iki ayak da parmaklara kadar yüzeyin içinde |
| `img/xslopefeet_old.jpg` / `img/xslopefeet_new.jpg` | 10° çapraz eğim: eskide alçak ayak gömülü |
| `vid/strip_oS.gif` / `vid/strip_nS.gif` (+ `*_realtime.avi`, `strip_nS_slow3x.avi`) | şerit: dur → bekle → 180° dön → geri yürü (yan) |
| `vid/slope_oS.gif` / `vid/slope_nS.gif` | 8° eğim, aynı zincir |
| `vid/xslope_oD.gif` / `vid/xslope_nD.gif` | çapraz eğim, ön-çapraz |
| `vid/walkturn_oS.gif` / `vid/walkturn_nS.gif` (+ AVI) | yürü → dur → fareyle 90° → yürü |
| `vid/tipfast_oD.gif` / `vid/tipfast_nD.gif` | hızlı fare 90/180° yerinde dönüşler (son üretim: pivot ön ayarı dâhil) |
| `vid/sprint_oS.gif` / `vid/sprint_nS.gif` (+ AVI) | depar → 90° kesiş → ters dön → yeniden hızlan |
| `vid/jogfb_oS.gif` / `vid/jogfb_nS.gif` | tempolu ileri → geri → ileri |
| `vid/jflick180_oD.gif` / `vid/jflick180_nD.gif` | tempolu, fareyle 180° |
| `vid/sflick_nD.gif`, `vid/jogcut_nD.gif`, `vid/wawd_nD.gif`, `vid/tapdiag_nD.gif`, `vid/slopeturn_nS.gif` | yalnız V2.9: depar fare dönüşleri, tempolu A/D, W+A↔W+D, dokun-bırak-çapraz, eğimde dönüş |
| `vid/sprint_nG.gif` | oyun kamerası (depar kesiş / ters dönüş). Karakterin yüzü kameraya döndüğü 18 kare (72–89) çıkarılıp bir ara kartla değiştirildi (göğüsteki kıyafet kusuru, §9) |

- **Kayıt zamanı:** `strip_nS`, `walkturn_nS`, `tipfast_nD` son üretimle (pivot ön ayarı dâhil) yeniden kaydedildi. Diğer yeni kayıtlar pivot düzeltmesinden önce alındı: yerinde dönüş anlarında (ör. `slope_nS`, `xslope_nD`, `slopeturn_nS`) basılı ayak burulması onlarda hâlâ görülebilir; hareketli dönüşleri etkilemiyor.
- Eski = aynı kaydedilmiş varlıklar, V2.8 mantığı geri alma anahtarlarıyla (`SHM_HC_Off`, `SHM29_TipOld`, `SHM29_CutMode 0`). Diz onarımı her ikisinde de var.
- Kendi incelemem (gerçek hız, sonra 1/3 hız):
  - Şerit / eğim / çapraz eğimde eski hâlde ayak yere gömülü ve dizler fazla bükük; yenide ayaklar yüzeyde.
  - Dönüşlerde eski hâlde kalça ters savruluyor, sonra yetişiyor; yenide gövde ayakla birlikte dönüyor.
  - Depar kesişinde yeni hâlde fren çökmesi belirgin (§4).
- **Kısıtlar:**
  - Yakalama sırasında oyun ~21–24 fps.
  - Oyun kamerası bacakları kırpıyor (V2.8 ile aynı).
  - AVI dosyaları Windows Media Player COM ile çözümlendi (süre doğru); başka oynatıcıda denenmedi.

## 8. Değişen dosyalar, ayarlar, geri alma
- **Varlıklar (kaydedildi):**
  - `ABP_GR_MotionMatchingBase` (+ child `ABP_GR_MotionMatching`).
  - 76 onarılmış klip.
  - `PSD_SHM_SprintCut` + 3 klip kopyası + 5 klibe BranchIn izi.
- **Araçlar:** `Tools/SHME_V1_20260925/install_idle_wait.py` (TIP / kesiş / kuyruk DSL), `qa_pie.py` (yüzeyler, ışık, dünya yönlü kamera, eğri ve nesne telemetrisi), `Tools/SHME_V29_20261016/*` (ölçüm: `legs.py`, `turns.py`, `cuts.py`, `turnslip.py`; kurulum: `install_hold_deadapt.py`, `install_turnplant.py`, `build_v29_sprintcut.py`; güvenli A/B: `ab_safe.sh`; medya: `mjpeg_avi.py`, `gif_anim.py`, `crop_frames.ps1`, `make_media.sh`).
- **Yeni ABP değişkenleri:** `SHM29_CutMode` (2), `SHM29_TipOld` (false), `SHM_HC_Off` (false), `SHM_HC_*`, `SHM_Rd*`, `SHM_MontT`, `SHM_TurnPlant`.
- **Grafik:** `Get_FootPlacementPlantSettings` içine bir Select (`install_turnplant.py`).
- **Geri alma:**
  - Hızlı: ABP sınıf varsayılanında `SHM29_CutMode 0`, `SHM29_TipOld true`, `SHM_HC_Off true` (V2.8 mantığı; diz onarımı ve yeni DB kalır).
  - Tam: `checkpoint/before_v29_abp_save/` (V2.8 ABP'leri, SHA256 doğrulamalı) ve `checkpoint/knee_repair_before/` (76 klibin onarım öncesi hâli), editör kapalıyken geri kopyalanır.
  - Ara noktalar: `before_v29b_save` (kesiş öncesi), `before_tp_save` (pivot ön ayarı öncesi), `before_sprintcut` (BranchIn izleri öncesi).
- **Skill eklemeleri** (yalnız doğrulanmış): `sphirus-human-motion-engine/references/architecture.md`, `validation.md`, `authoring.md`, "V2.9" bölümleri.
  - `sync_claude_skills.py`: 71 skill, 0 hata.

## 9. Açık sorunlar ve dürüst notlar
- Depar kesişi kısmi (kapsül sınırı); ilk basan ayak her zaman dış ayak değil; ayrı toparlama adımı davranışı yok.
- Tempolu fare dönüşü için koşu dönüş klipleri bağlanmadı (kapsül dönüş hızı kararı gerekiyor). İstenirse içerik brifi aşağıda.
- Depar ters dönüşünde üst gövde pop'u 57–99 m/s² (önceden de vardı).
- Depar basmalarında 5–8 cm kayma (önceden de vardı).
- FootPlacement pelvisi yalnız dikey; basamakta pelvis eğmesi yok.
- **Kıyafet:** tam gövde ön görünümde gömlekte göğüs bölgesinde ten görünüyor (içinden geçme / delik). Bu görevin kapsamı dışı (kıyafete dokunulmadı); ayrı bir iş.
- **Benim hatalarım:**
  - Aynı editöre iki toplu A/B koşusunu aynı anda gönderdim. Etkilenen veriler atıldı ve sıralı tekrarlandı; artık `ab_safe.sh` buna izin vermiyor.
  - Çalışan bir runner işinin dosyasını taşıyıp runner'ı kilitledim; editör yeniden başlatıldı.
  - Kaybolan kayıtlı iş yok.
- **İçerik brifi** (satın alma yapılmadı; ürün uygunluğu gerçek listelemeden):
  - İhtiyaç: tempolu ~3 m/s ve depar ~4.9 m/s hızında, dış ayakla basılan 60–90° kesişler (L/R, her iki destek ayağı), 0.5–0.8 g, 1–2 kısa fren adımı ve toparlama; kök hareketi ve UE5 Manny uyumu.
  - Fab "Mobility Pro" (MoCap Online) listelemesi tempolu ve koşu dönüşlerini 45/90/135/180° olarak beyan ediyor; kök hareketi + yerinde, UE4 iskeleti + Manny retargeter, FBX.
  - Klip bazında içerik (ayak varyantları, hız) Google Sheet'te ve oturum açmadan görülemedi → uygunluk **doğrulanmadı**. Fiyat lisans seçmeden görünmüyor.
