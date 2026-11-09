# Sphirus: SHME yönteminde Core Motion hareket sistemi ve yakın omuz kamerası (2026-11-09)

Tarih: 2026-11-09 05:00–09:30. Motor UE 5.8.4; harita `/Game/GraceRanger/Maps/L_GR_SphirusHouse`; oyuncu `BP_HybridA_Player`; sürücü `ABP_Sph_Driver` (gizli SKM_MCPaul); görünür gövde `ABP_Sph_Body` + `RTG_Sph_Core_to_MH2`. Geri alma noktası: `C:\Users\berat\SphirusCheckpoints\MotionShme_20261109_0500` (oyuncu, sürücü, MM, istasyonlar, haritalar, test haritası, Input, Config, kayıtlar; 124 MB) ve iş başına manifest yedekleri (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/day_*.json`). Değişen varlıklar: `BP_HybridA_Player` (GR_LagPivot, GR_TurnScale/GR_HeadErr, GR_SteadyEnable, TargetOffset yazıcı, yay kolu gecikmesi kapalı), `ABP_Sph_Driver` (Save/Use Cached Pose `LocoCache`). Satıcı dosyaları, Story Framework, haritalar değişmedi.

## 0. Sonuç özeti

Çalışma yöntemi SHME V2.5x'teki gibi: her olgu gerçek Pawn + görünür MetaHuman üzerinde gerçek zamanlı telemetriyle yeniden üretildi, kök neden ölçüldü, tek değişiklik uygulandı, aynı testle yeniden ölçüldü; bozan değişiklikler (bir tane oldu) ölçümle yakalanıp geri alındı/onarıldı.

| Kullanıcı şikâyeti | Ölçülen kök neden | Durum |
|---|---|---|
| Boşta aynı ağırlık aktarımı hızlı hızlı tekrar ediyor | Sürücü anim grafiğinde çift tüketicili düğüm → boşta klibi 2× hızda (11,47 s klip 5,8 s'de) | **PASS (ölçüm)**: 1×, baş hızı p95 14 → 8 cm/s; görsel REVIEW_REQUIRED (`I_idle_shme.mp4`) |
| Yürüyüş titriyor, kısa klipler hızlandırılmış | Aynı çift değerlendirme (tüm zincir 2× güncelleniyordu) + tam veritabanında başlangıç penceresi tercihi | **PARTIAL**: çift değerlendirme giderildi; döngü veritabanları sabit hızda `Walk_Fwd/Jog_Fwd/Run_Fwd` oynatıyor (1×); tam veritabanının kendi tercihi çözülmedi (AÇIK) |
| Farklı walk/jog/run yok | Gait veritabanları + döngü veritabanları (önceki tur), bu turda ölçümle doğrulandı | PASS (ölçüm): 180/300/500 cm/s'de ayrı klip aileleri |
| Dönüşler yapay, frenlemiyor | Kapsül dönüşte hız kaybetmiyordu (180/500 sabit) | **PARTIAL**: yön hatasına bağlı fren (W→S: 0,5 s'de 167 → 115 cm/s); fare süpürmelerinde fren yok (tasarım); pivot klibi seçimi yok |
| Sola giderken karakter kadrajdan çıkıyor | Yay kolu yanal konum gecikmesi (45 cm = ekranın %25'i) | **PASS (ölçüm + video)**: baş X A'da −0,06…0,05 → 0,20…0,29; tüm yönlerde 0,20–0,44 bandı |
| Kamera donuk | Derinlik gecikmesi korunuyor (143 → 159 cm hızlanmada), yanal sıfır | PARTIAL/REVIEW_REQUIRED: kütle hissi için ivme tepkisi eklenmedi |

Dokunulmayan: Core Motion satıcı dosyaları, Story Framework, AAMS (geri gelmedi), ev sahnesi, kullanıcı kaydı (bayt bayt korunuyor). Yapılmayan: Inertialization, stride warping, ayak IK yeniden etkinleştirme, efor/nefes katmanı, cook/paket, menüden save-load.
## 1. Önceki raporun hatalı/eksik PASS'ları ve bu turda ölçülen kök nedenler

### 1.1 Bulunan asıl kök neden: sürücü anim grafiğinde çift değerlendirme
`ABP_Sph_Driver` AnimGraph'ında `DefaultSlot` düğümünün çıkışı **iki tüketiciye** bağlıydı (`UpperBody` slotunun kaynağı ve `LayeredBoneBlend` taban pozu; `q_slots.py`: `Slot:DefaultSlot -> ['Slot:UpperBody.Source','LayeredBoneBlend.BasePose'] LINKS 2`). Unreal anim grafiğinde iki tüketicisi olan bir düğüm ve onun üstündeki her şey her karede **iki kez güncellenir**: poz geçmişi toplayıcısı, boşta kapısı, boşta SequencePlayer ve Motion Matching düğümü.

Ölçülen etkileri:
- **Boşta klibi 2× hızda** (SequencePlayer çift delta alıyor): 11,47 s'lik `af_Stand_Idle_01` 5,8 s periyotla tekrarlıyordu (r = 0,99), poz kütüphanesinde klip zamanı 2,06× eğimle ilerliyordu → kullanıcının "aynı ağırlık aktarımı hızlı hızlı tekrar ediyor" gözlemi.
- **Yörünge geçmişi bozuk**: toplayıcı her karede iki örnek yazıyor; sorgunun geçmiş/hız özellikleri yarıya iniyor → arama her hızda yavaş pozları (başlangıç kliplerinin ivmelenme penceresi) seçiyordu. Önceki raporda "kanıtlanamadı" denen seçim hatasının mekanizması budur; şema/geçmiş derinliği/yörünge pini değişikliklerinin etkisiz kalması da bununla tutarlıdır.
- Motion Matching düğümü kendi güncelleme sayacıyla çift ilerlemeye karşı korunduğu için yürüyüş döngüsü ~1,08× hızda kaldı; ama çift arama/karışım kareleri titreme ve kısa kesilmeler üretir.
- Montaj slotlarındaki çift güncelleme: montaj oynarken kolların/gövdenin 2× ilerlemesi (yatak/kesme/maske montajları) — doğrulanacak.

Düzeltme (`cm_cache1.py`): `DefaultSlot` → **Save Cached Pose `LocoCache`**, iki **Use Cached Pose** okuyucu (UpperBody slot kaynağı, layered blend tabanı). Önceki raporun "teknik PASS" dediği gait seçimi/klip kırpma/döngü veritabanı adımları bu hata altında ölçülmüştü; sonuçlar §4'te yeniden ölçülüyor.
## 2. Baseline ölçümleri (gerçek zamanlı, telemetri)

Araç: `Tools/Day_20261107/lab.sh` — ekran görüntüsü almadan, zaman ölçeği değiştirmeden (gerçek oyun adımı 17–42 ms), her karede kapsül/hız/yaw, kamera transformu/FOV, görünür gövde ve gizli sürücü kemikleri, MM veritabanı, `GR_Steady`/`Idle`/`StillTime`, baş–pelvis normalize ekran koordinatı ve yay kolu durumu (`vid.py`); analiz `an_lab.py`. Gövdenin oynattığı klip ve klip zamanı 45 kliplik poz kütüphanesine en yakın komşuyla bulunur; oynatma hızı, klibin kendi hareket periyodu ile oyundaki periyodun oranından ölçülür (NN zaman eğimi 57 fps'te kuantalanıyor, güvenilmez).

| Senaryo (06:36–06:40) | Ölçüm | Sonuç |
|---|---|---|
| 45 s boşta (`I_idle.json`, 1350 kare, adım 0,033) | sürücü sağ el x / baş z otokorelasyon | **5,8 s'lik güçlü periyot (r = 0,99)**; `af_Stand_Idle_01` klibi 11,47 s ve kendi içinde bu periyoda sahip değil (klip otokorelasyonu 4,5 s'de r ≈ 0). Gövde poz kütüphanesinde Idle_01'e eşleniyor ama klip zamanı 2 s'de ~4 s ilerliyor (eğim 2,06). Yani boşta görünen hareket tek klip değil, iki faz kopyasının üst üste binmesi gibi davranıyor → kullanıcının "aynı ağırlık aktarımı hızlı tekrar ediyor" şikâyeti ölçüldü. Kök neden §1'de. |
| 15 s yürüyüş (`G_gaits.json` SEG 1, 7,7 s kayıt, 174 cm/s) | foot_l z periyodu klip 0,933 s → oyunda 0,86 s | döngü **1,08×** hızda oynuyor (2× değil); gövde 450 karenin 267'si `Walk_Fwd`, WalkLoop veritabanı 408 kare. Basılı ayak hızı p20 sürücü 92 / görünür 105 cm/s (yüksek; 57 fps'te salınım fazı dahil, ham metrik). |
| 15 s koşu (SEG 2, 460 cm/s) | RunLoop 393 kare, gövde Run_Fwd / Jog_Fwd_Start karışık (NN belirsizliği) | koşu döngüsü oynuyor; hız 500'e 1,5 s'de çıkıyor (Shift ile önce jog). |
| Kamera sabit A/D/W+A/W+D/W/S (`CL_cam.json`) | kapsül 170 cm/s, yaw 0→−90 (A), →90 (D), S'de 180° dönüş | ekran koordinatı alanı ilk kayıtta hata verdi (Vector2D), tekrar kaydedilecek; kamera–baş mesafesi A'da 153, D'de 140, W+A 168, W+D 161 cm (sol/sağ asimetrisi var). |
## 3. Klip envanteri ve gait/idle/start/stop/turn yapısı

Kurulu Core Motion içeriği (proje kopyaları `/Game/Sphirus/Player/Anim/Core/`, satıcı orijinalleri `/Game/MC_Core_Motion/Animations/` dokunulmadan; kök hız/yaw profilleri `q_trim.py`, `data/trim_plan.json`):

| Aile | Klipler (uzunluk, kök hızı) | Kullanım |
|---|---|---|
| Boşta | `af_Stand_Idle_01` 11,47 s (kapı klibi), `af_Stand_Idle_02_WeightShift` 6,33 s (MM veritabanlarında) | Duruştan 0,35 s sonra Idle_01 döngüsü; MM boşta pozu WeightShift |
| Boşta dönüş | `af_Stand_Idle_Turn{L,R}{045,090,135,180}` 2,7–3,3 s (yaw 24–84°/s) | Walk veritabanı, yerinde dönüş |
| Yürüyüş | `Walk_Fwd` 1,9 s **197 cm/s** (döngü), `Walk_FwdLeft/Right` 197, `Walk_Fwd_Start` 2,5 s (0→212), `Walk_Fwd_Stop` 4,27 s (207→0), `Walk_Fwd_Pivot` 3,1 s, `Walk_Start_Turn{L,R}{045..180}` 2,4–3,0 s | PSD_Sph_Walk (23) / WalkLoop (3) |
| Jog | `Jog_Fwd` 1,5 s **294**, `Jog_FwdLeft/Right`, `Jog_Fwd_Start` 1,93 s (0→329), `Jog_Fwd_Stop` 2,37 s, `Jog_Fwd_Pivot`, `Jog_Start_Turn*` ×8 | PSD_Sph_Jog (15) / JogLoop (3) |
| Koşu | `Run_Fwd` 0,63 s **532**, `Run_Fwd_Start` 2,0 s (0→489), `Run_Fwd_Stop` 3,0 s, `Run_Start_Turn{L,R}{090,180}` | PSD_Sph_Run (8) / RunLoop (1) |
| Yok | strafe döngüleri dışında yan/geri yürüyüş, koşu 45/135 dönüşleri, vault/mantle, çömelme döngüleri (ayrı `PSD_Sph_Crouch`) | geri yürüyüş yok → S kamera-göreli 180° dönüşe çözülüyor |

Kapsül hızları yürüyüş 180 (ev içi 150) / jog 300 / koşu 500; MM oynatma hızı 0,7–1,25 (yürüyüşte ölçülen 1,08×). Şema `PSS_Sph_Loco`: yörünge 7 örnek (−0,6…+1,0 s, ağırlık 1,3), ayak konumu/hızları, pelvis yönü; veritabanı seçimi gait'e göre; `ForceLegacy` (tek eski veritabanı) ve `GR_SteadyEnable` (yalnız döngü veritabanları) A/B anahtarları.
## 4. Hareket düzeltmeleri (önce/sonra)

### 4.1 Çift değerlendirme düzeltmesi — aynı testler, önce/sonra (gerçek zaman, veri kaydı)

| Ölçüm | Önce (`I_idle2`, `G_gaits2`, `CL_cam2`) | Sonra (`I_idle3`, `G_gaits3`, `CL_cam3`) |
|---|---|---|
| Boşta klip zamanı ilerlemesi (2 s'de) | +3,9 s (2× hız; 5,8 s periyot) | **+2,0 s (1×; 11,47 s döngü)** |
| Boşta baş hızı p50 / p95 (cm/s) | 5 / 14 | **2 / 8** |
| Boşta yeniden başlama / s | 0,1 | 0,0 |
| Yürüyüş döngüsü (174 cm/s), WalkLoop veritabanı | 408/450 kare | 408/450 kare |
| Koşu (460 cm/s), RunLoop veritabanı | 393/450 | 393/450 |

Kamera testi kameranın kendi düzeltmesiyle birlikte ölçüldü (§5.2). Montajlar (kesme, yatak, maske) önceden 2× hızda oynuyordu; istasyon zamanlamaları §6'da yeniden test edilir.

### 4.2 Tam gait veritabanı tek başına — düzeltilmiş okuma
İlk okuma yanlıştı: `G_full.json` kaydında test ön-ayarı (`GR_SteadyEnable=false`) etkili olmamış, kayıt yine WalkLoop veritabanıyla alınmıştı (`db` alanı: WalkLoop 222 / Walk 18). Döngü veritabanı gerçekten kapalıyken (`G_gaits5.json`, Walk veritabanı 300/300 kare) gövde **yine** `Walk_Fwd_Start` 0,7–1,2 s penceresinde (186 kare) + 45° dönüş-başlangıçları (70), `Walk_Fwd` döngüsü 0; sıfırdan arama sondası Start@0,6 (93). Yani çift değerlendirme düzeltmesi boşta klibini ve yörünge geçmişini onardı ama tam veritabanındaki "ivmelenme penceresi" tercihini **değiştirmedi**; bu tercih veritabanı/şema tarafında (başlangıç kliplerinin özellik uzayı) duruyor ve bu turda çözülmedi (AÇIK). Üretim mekanizması olarak **sabit hızda döngü veritabanları açık kalır** (`GR_SteadyEnable=true`, `cm_steady3.py`); ölçülen davranış: yürüyüşte 0,35 s sonra WalkLoop, gövde `Walk_Fwd` döngüsünde (G_gaits3: 234/450 kare, 1× hız).

### 4.3 Dönüşlerde fren (SHME V2.55 yön doğruluğu davranışının bağımsız yeniden kurulumu)
Ölçüm (`T_walk.json`, `T_jog.json`): kamera 360°/s dönerken kapsül hızı yürüyüşte 180, koşuda 489–500'de **sabit** kaldı; gövde 40 cm yarıçaplı yayda strafe/dönüş-başlangıç klipleriyle kayıyordu. Düzeltme (`cm_turn1.py`): yön hatası = hareket girdisi ile yüz yönü arasındaki açı; `GR_TurnScale = clamp(1 − max(0, hata−25°)/110°, 0,3, 1)` 8/s yumuşatılmış, azami hız çarpanı. Keskin dönüşte yürüyüş 180 → ~55, koşu 500 → ~150'ye frenler; MM yörüngesi freni görüp duruş/dönüş-başlangıç kliplerini seçer; yön oturunca normal ivmeyle (450) toparlar.

İlk uygulama (`cm_turn1.py`) **regresyon** üretti ve geri alındı: çarpan, azami hızı yumuşatan `FInterpTo(Current=MaxWalkSpeed)` düğümünün *çıkışına* uygulanmıştı → geri besleme, her karede ×0,3 → kapsül 8–15 cm/s'ye düştü (`R_rev_after.json`, `G_gaits4.json`); ayrıca ölçek formülü yön hatası 0 iken 0,3 veriyordu. Onarım (`cm_turn2.py`): çarpan `FInterpTo`'nun *hedefine*, formül tek `MapRangeClamped(hata, 25→135°, 1,0→0,3)` düğümü. Önce/sonra `R_rev_before` ↔ `R_rev3` (kamera sabit, klavye ile W→S, A↔D, koşuda W→S), `T_walk` ↔ `T_walk3`, `T_jog` ↔ `T_jog3`.

| Geri dönüş (kamera sabit) | Önce | Sonra (`R_rev3`) |
|---|---|---|
| Yürüyüş W→S: hız 0,25 / 0,5 / 0,75 / 1,0 s (yüz yönü −54° / −119° / 180° / 180°) | 54 / **167** / 180 / 180 → karakter 0,5 s'de henüz dönmemişken 167 cm/s ile geri gidiyor (V2.55'teki "geri koşma") | 54 / 115 / 134 / 157; %90 hıza 0,5 → 1,08 s |
| A↔D 180° | 54 / 167 / 180 | 54 / 115 / 134 / 157 |
| Koşu W→S (500) | 35 / 147 / 260 / 372; %90'a 1,21 s | 35 / 148 / 246 / 344; %90'a 1,33 s |
| Fare ile 90°/180° süpürme (360°/s) | yürüyüş 180, koşu 489–500 sabit | değişmedi (girdi yönü yavaş döndüğü için yön hatası 25–60° kalıyor; yay yürüyüşü) |

Sıkılaştırma (`cm_turn3.py`: taban 0,3 → 0,15, tepki 8 → 12/s; `R_rev4.json`): yürüyüş W→S 0,5 / 0,75 / 1,0 s → 98 / 129 / 157 cm/s (önce 167 / 180 / 180); koşu 147 / 238 / 329 (önce 147 / 260 / 372).

Kapsül CMC frenlemesiyle zaten 0,13 s'de 5 cm/s'e düşüyor; fark **yeni yöne hızlanmanın** yüz dönene kadar bastırılmasında. Dönüş hızı 260°/s olduğu için 180°'lik dönüş 0,7 s sürüyor; 0,25–0,75 s arasında karakter hâlâ kısmen yan/geri hareket ediyor (PARTIAL). Gerçek pivot klibi seçimi ve dönüş sırasında daha sert kısıt (taban 0,3 → 0,15, tepki 8 → 12/s) sonraki adım; fare süpürmelerinde fren istemiyoruz (oyuncu yay çiziyor).
## 5. Kamera: sola giderken kadraj, takip hissi, aksiyon kadrajı (önce/sonra)

### 5.1 Sola giderken kadrajdan çıkma — ölçülen kök neden
Protokol: kamera yaw sabit (fare yok), açık alan (çarpışma yok), yürüyüş hızı: boşta 1 s → A 4 s → boşta → D 4 s → boşta → W+A → boşta → W+D → boşta → W 3 s → S 3 s (`CL_cam2.json`, 915 kare, gerçek zaman). Her karede baş ve pelvisin normalize ekran X'i (`ProjectWorldLocationToScreen` / görünüm boyutu), yay kolu uzunluğu, çarpışma düzeltmesi, kamera–baş mesafesi.

| Durum | Baş X (min / ort / maks) | Pelvis X ort | Kamera–baş |
|---|---|---|---|
| boşta | 0,28 / 0,30 / 0,30 | 0,31 | 143 |
| **A (sola)** | **−0,06 / 0,05 / 0,31** | 0,14 | 153 |
| D (sağa) | 0,28 / 0,54 / 0,58 | 0,49 | 140 |
| W+A | 0,14 / 0,19 / 0,30 | 0,23 | 168 |
| W+D | 0,30 / 0,48 / 0,50 | 0,45 | 161 |
| W | 0,31 / 0,34 / 0,35 | 0,35 | 171 |
| S (180° dönüp yürüyüş) | 0,18 / 0,23 / 0,34 | 0,28 | 120 |

Kullanıcının gözlemi birebir ölçüldü: sola giderken baş ekranın sol kenarına ve dışına çıkıyor (X < 0), sağa giderken merkezin sağına kayıyor; sol/sağ asimetrik çünkü kompozisyon zaten sol üçte bir (0,30). Yay kolunda çarpışma düzeltmesi hiç devreye girmedi (0/915 kare), kol 140 cm sabit → sebep çarpışma değil.

Kök neden: yay kolunun yerleşik **konum gecikmesi** (7/s, en fazla 45 cm): karakter kameraya göre yanal hareket edince kamera pivotu geride kalıyor; 140 cm kol ve 66° FOV'da 45 cm yanal kayma ekran genişliğinin ~0,25'i. Bu gecikme omuz kompozisyonuna ekleniyor: 0,30 − 0,25 ≈ 0,05 (sol), 0,30 + 0,25 ≈ 0,55 (sağ) — ölçülen değerlerle uyuşuyor.

Düzeltme (`cm_camlag1.py`): yerleşik konum gecikmesi kapatıldı; proje sahipli gecikme pivotu `GR_LagPivot` (VInterpTo 7/s) ile kameranın **yalnız bakış ekseni** boyunca gecikmesi (derinlik, ±45 cm) ve küçük dikey bileşen (±15 cm) yay kolu `TargetOffset`'ine (dünya uzayı) yazılıyor; yanal gecikme sıfır. Ağırlık hissi (hızlanmada kısa uzaklaşma, frenlemede yaklaşma) korunur, kadraj korunur. Dönüş gecikmesi (14/s) değişmedi. Sonra ölçümü §5.2'de.

### 5.2 Aynı protokol, düzeltme sonrası (`CL_cam3.json`)

| Durum | Baş X önce (min/ort/maks) | **Baş X sonra** | Pelvis X sonra | Kamera–baş sonra |
|---|---|---|---|---|
| boşta | 0,28 / 0,30 / 0,30 | 0,30 / 0,30 / 0,31 | 0,32 | 143 |
| A (sola) | −0,06 / 0,05 / 0,31 | **0,21 / 0,24 / 0,30** | 0,31 | 143 |
| D (sağa) | 0,28 / 0,54 / 0,58 | **0,27 / 0,36 / 0,39** | 0,33 | 143 |
| W+A | 0,14 / 0,19 / 0,30 | 0,26 / 0,28 / 0,32 | 0,33 | 154 |
| W+D | 0,30 / 0,48 / 0,50 | 0,30 / 0,37 / 0,44 | 0,34 | 155 |
| W | 0,31 / 0,34 / 0,35 | 0,25 / 0,33 / 0,34 | 0,33 | 159 |
| S (180° dönüp yürüyüş) | 0,18 / 0,23 / 0,34 | 0,23 / 0,26 / 0,34 | 0,30 | 129 |

Baş artık bütün yönlerde 0,21–0,44 bandında; sola yürürken ekran dışına çıkma yok. Sol/sağ farkı 0,05 ↔ 0,54'ten 0,24 ↔ 0,36'ya indi (kalan fark omuz kompozisyonunun kendisi). Derinlik gecikmesi korunduğu için ileri yürüyüşte kamera–baş mesafesi 143 → 159 cm'e açılıp durunca geri geliyor (hızlanma/fren hissi). Çarpışma düzeltmesi bu açık alanda 0 kare. Görsel kabul: gerçek hızda video §7.
## 6. Regresyon ve dayanıklılık

| Test | Sonuç | Kanıt |
|---|---|---|
| Yeni oyun uyanma akışı (`v45c.sh reg_wake`, canlı kayıt kenara alınıp geri kondu) | PASS (teknik): 0,6 s'de yatak hub'ına yerleşme (1229,767,580, yaw 90), 5,2 s'de kalkış, 6,8 s'de yatak yanında ayakta (1309,767), meşgul bayrağı düşüyor | `data/reg_wake_t.txt` |
| Kesme istasyonu (E → balta bekle → tıkla), aksiyon kamerası | PASS (teknik): kamera–baş 143 → 126 → aksiyon; video D | `videos/D_chop_shme.mp4`, `data/D_chop_shme.json` |
| Ev içi koridor, hız sınırı 150, kamera çarpışması | PASS (teknik): 135–150 cm/s, çarpışma düzeltmesi 12/75 kare, baş X 0,29–0,39 | `videos/H_hall_shme.mp4` |
| Çömelme / zıplama (`CJ_test.json`, bahçe) | PASS (teknik): C ile kapsül 264 → 216 (Crouch veritabanı, çömelik yürüyüş 104 cm/s), C ile ayağa (Walk veritabanı); yürürken ve yerinde zıplama vz 388 / 398, iniş sonrası yürüyüş döngüsü devam | `data/CJ_test.json` |
| Kullanıcı kaydı | PASS: her testten sonra bayt bayt aynı (`SAVE_OK`) | `lab*/reg*_progress.txt` |
| Temiz yeniden açılış | PASS: her yazma işinden sonra editör kapatılıp açıldı (emb_399–421), derleme hatası 0 | gate günlüğü |
| Maske / odun taşıma (UpperBody slot) | NOT_TESTED bu turda (yapısal olarak cached pose üzerinden aynı montaj yolu) | |
| AAMS | PASS: çalışma zamanı referansı yok (oyuncu Character türevi, sürücü ABP_Sph_Driver) | |
| Cook / paket, menüden save-load, 60 FPS | NOT_TESTED | |
## 7. Videolar

Hepsi gerçek oyun (PIE, `L_GR_SphirusHouse`), kesintisiz, 30 kare/s, **gerçek zamanlı** (her karede oyun adımı 0,033 s; `data/*_shme.json` `gdt`); kare verileri aynı JSON'larda. Çözünürlük 1510×922 (editör penceresinin oyun bölgesi). Önceki yapının videoları karşılaştırma için önceki raporda (`sphirus-core-motion-camera-feel-rebuild-2026-11-08`).

| Video | İçerik | Telemetri (aynı kayıt) |
|---|---|---|
| `videos/CL_strafe_shme.mp4` (18 s) | **Kamera sabit (fare yok):** A 2,5 s, D 2,5 s, W+A, W+D, W, S | Baş X: A 0,20–0,29 (önce −0,06…0,31), D 0,27–0,39 (önce 0,54), W+A 0,25–0,31, W+D 0,30–0,44, S 0,23–0,33; kareler `evidence/CL_strafe_A_left_f060.png`, `CL_strafe_D_right_f150.png` |
| `videos/I_idle_shme.mp4` (20 s) | Boşta, fare yok | Baş hızı p50 2 / p95 8 cm/s; tek `Idle_01` döngüsü 1× (yeniden başlama 0); `evidence/I_idle_f300.png` |
| `videos/A_loco_shme.mp4` (11 s) | Yürüyüş → jog → koşuya 180° → koşu → yürüyüş → duruş → yürüyüş → duruş | Gait veritabanları Walk/WalkLoop → JogLoop → Run/RunLoop → WalkLoop; baş X 0,23–0,43 |
| `videos/B_turns_shme.mp4` (15 s) | 180° ×2, 45° zikzak, duruş, yerinde dönüş, jog/koşu dönüşü | 180° sonrası hız 179 → 77 (fren) → 180 (toparlama); baş X 0,24–0,39; `evidence/B_turns_f090.png` |
| `videos/H_hall_shme.mp4` (10 s) | Ev alt kat koridoru: yürüyüş, jog, duruş, 180°, geri | Ev içi 135–150 cm/s; kamera–baş 93–117 cm; çarpışma düzeltmesi 12/75 karede devrede, baş X 0,29–0,39; `evidence/H_hall_f090.png` |
| `videos/D_chop_shme.mp4` (11 s) | Kesme istasyonu: yaklaş, E, bekle, vur | Aksiyon kamerası ve istasyon akışı (regresyon, §6); `evidence/D_chop_f240.png` |
## 8. Kalan engeller

1. **Tam gait veritabanı başlangıç penceresi tercihi** (§4.2): döngü veritabanı geçersiz kılması kapatılınca gövde yine `Walk_Fwd_Start` 0,7–1,2 s'de dönüyor. Yörünge üretimi doğru ölçüldü (`trajprobe.py`), çift değerlendirme giderildi; kalan aday: şema özellik bayrakları (PSS_Default'tan türetilmiş hız/yön bayrakları) ve başlangıç kliplerinin özellik uzayında döngüyle çakışması. Oyunda etkisi: döngü veritabanları sayesinde sabit hızda görünmez; başlangıç→sabit geçişinde (0,35 s) bir veritabanı anahtarlaması var.
2. **Dönüş fiziği**: 180° klavye dönüşünde 0,25–0,75 s arasında karakter yüzü dönmeden 54–134 cm/s hareket ediyor (pivot klibi seçilmiyor, dönüş hızı 260°/s). Gerçek pivot/plant için `Walk_Fwd_Pivot` seçimini zorlayan durum veya dönüş sırasında dönüş hızı artışı gerekiyor.
3. **Kamera kütle hissi**: yalnız derinlik gecikmesi var; hızlanma/frenleme için ivmeye bağlı küçük sönümlü tepki (SHME V2.53 tarzı) eklenmedi.
4. **Ayak IK / zemin teması** kapalı; eğim/basamak teması test edilmedi (ev koridoru düz).
5. Efor/nefes katmanı koşu sonrası yok; weighted idle yok (bilinçli: önceki SHME gerilemeleri).
6. Cook/paket, menüden save-load, 60 FPS gerçek oyun performansı NOT_TESTED.
7. Ayrı test haritası (`L_Sph_MoveTest`) PIE'de siyah render ediyor; veri kayıtları için kullanılıyor, görüntü için ev haritası.
