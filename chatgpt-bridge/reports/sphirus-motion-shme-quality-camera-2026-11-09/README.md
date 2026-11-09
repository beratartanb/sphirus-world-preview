# Sphirus: SHME yönteminde Core Motion hareket sistemi ve yakın omuz kamerası (2026-11-09)

Tarih: 2026-11-09 05:00–09:30 (1. tur, §1–8) ve 12:30–23:00 (2. tur, §9). Motor UE 5.8.4; harita `/Game/GraceRanger/Maps/L_GR_SphirusHouse`; oyuncu `BP_HybridA_Player`; sürücü `ABP_Sph_Driver` (gizli SKM_MCPaul); görünür gövde `ABP_Sph_Body` + `RTG_Sph_Core_to_MH2`. Geri alma noktası: `C:\Users\berat\SphirusCheckpoints\MotionShme_20261109_0500` (oyuncu, sürücü, MM, istasyonlar, haritalar, test haritası, Input, Config, kayıtlar; 124 MB) ve iş başına manifest yedekleri (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/day_*.json`). Değişen varlıklar: `BP_HybridA_Player` (GR_LagPivot, GR_TurnScale/GR_HeadErr, GR_SteadyEnable, TargetOffset yazıcı, yay kolu gecikmesi kapalı), `ABP_Sph_Driver` (Save/Use Cached Pose `LocoCache`). Satıcı dosyaları, Story Framework, haritalar değişmedi.

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

**2. tur güncellemesi (§9, aynı gün öğleden sonra–gece):** gövdenin gerçekten oynattığı klip artık klip eğrileriyle ölçülüyor (§9.1; sabahki NN okuması yanlıştı). Kapsül fizik sözleşmesi yeniden kuruldu (§9.2–9.3): sürtünme 8→3, fren/ivme gait'e göre, gait kilidi, dönüş freni anında. Sonuç (§9.4): yürüyüş/koşu duruşları kaynak kliplerin süresinde ve gövde gerçekten `*_Fwd_Stop` oynatıyor; başlangıçlar 1× ve kesintisiz; "hızlandırılmış klip" izi kalmadı. Tersleme hâlâ PARTIAL (blend zinciri; pivot klipleri kök yaw içermiyor, tersleme veritabanı seti denendi ve ölçümle geri alındı). Kamera: ivmeye bağlı kütle tepkisi eklendi (§9.5) ve yanal **baş** izleme ile sol/sağ kadraj farkı 0,25 → 0,03 (§9.6b). Ayrıca sabahki videoların kodlayıcı hatasıyla sol ~200 px'inin eksik olduğu bulundu; kodlayıcı düzeltildi ve tüm videolar yeniden çekildi (§9.8, §9.9/8) — bu rapordaki `*_shme.mp4` kadraj yargıları için kullanılmamalı, `*_shme4.mp4` geçerli.
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

Hepsi gerçek oyun (PIE, `L_GR_SphirusHouse`), kesintisiz, 30 kare/s, **gerçek zamanlı** (her karede oyun adımı 0,033 s; `data/*_shme.json` `gdt`); kare verileri aynı JSON'larda. Çözünürlük 1510×922 (editör penceresinin oyun bölgesi).

> **Düzeltme (2. tur, §9.9/8):** bu bölümdeki `*_shme.mp4` dosyaları kodlayıcı hatası yüzünden oyun görüntüsünün sol ~200 px / üst ~60 px'i eksik kodlanmıştı (karakter sol kenarda kesik görünür; gerçek kadraj değil). Dosyalar rapordan kaldırıldı; aşağıdaki telemetri sütunları geçerli, görüntü için §9.8'deki `*_shme4.mp4` setine bakın. Buradaki `evidence/*_f*.png` kareleri de hatalı videodan alınmıştı; ham ekran görüntüsünden kırpılmış kareler `evidence/*_raw_f*.png`. Önceki yapının videoları karşılaştırma için önceki raporda (`sphirus-core-motion-camera-feel-rebuild-2026-11-08`).

| Video | İçerik | Telemetri (aynı kayıt) |
|---|---|---|
| `videos/CL_strafe_shme.mp4` (18 s) | **Kamera sabit (fare yok):** A 2,5 s, D 2,5 s, W+A, W+D, W, S | Baş X: A 0,20–0,29 (önce −0,06…0,31), D 0,27–0,39 (önce 0,54), W+A 0,25–0,31, W+D 0,30–0,44, S 0,23–0,33; kareler `evidence/CL_strafe_shme_raw_f60.png`, `CL_strafe_shme_raw_f150.png` |
| `videos/I_idle_shme.mp4` (20 s) | Boşta, fare yok | Baş hızı p50 2 / p95 8 cm/s; tek `Idle_01` döngüsü 1× (yeniden başlama 0); `evidence/I_idle_shme_raw_f300.png` |
| `videos/A_loco_shme.mp4` (11 s) | Yürüyüş → jog → koşuya 180° → koşu → yürüyüş → duruş → yürüyüş → duruş | Gait veritabanları Walk/WalkLoop → JogLoop → Run/RunLoop → WalkLoop; baş X 0,23–0,43 |
| `videos/B_turns_shme.mp4` (15 s) | 180° ×2, 45° zikzak, duruş, yerinde dönüş, jog/koşu dönüşü | 180° sonrası hız 179 → 77 (fren) → 180 (toparlama); baş X 0,24–0,39; `evidence/B_turns_shme_raw_f90.png` |
| `videos/H_hall_shme.mp4` (10 s) | Ev alt kat koridoru: yürüyüş, jog, duruş, 180°, geri | Ev içi 135–150 cm/s; kamera–baş 93–117 cm; çarpışma düzeltmesi 12/75 karede devrede, baş X 0,29–0,39; `evidence/H_hall_shme_raw_f90.png` |
| `videos/D_chop_shme.mp4` (11 s) | Kesme istasyonu: yaklaş, E, bekle, vur | Aksiyon kamerası ve istasyon akışı (regresyon, §6); `evidence/D_chop_shme_raw_f240.png` |
## 8. Kalan engeller (1. tur sonu; güncel liste §9.9)

1. **Tam gait veritabanı başlangıç penceresi tercihi** (§4.2): döngü veritabanı geçersiz kılması kapatılınca gövde yine `Walk_Fwd_Start` 0,7–1,2 s'de dönüyor. Yörünge üretimi doğru ölçüldü (`trajprobe.py`), çift değerlendirme giderildi; kalan aday: şema özellik bayrakları (PSS_Default'tan türetilmiş hız/yön bayrakları) ve başlangıç kliplerinin özellik uzayında döngüyle çakışması. Oyunda etkisi: döngü veritabanları sayesinde sabit hızda görünmez; başlangıç→sabit geçişinde (0,35 s) bir veritabanı anahtarlaması var.
2. **Dönüş fiziği**: 180° klavye dönüşünde 0,25–0,75 s arasında karakter yüzü dönmeden 54–134 cm/s hareket ediyor (pivot klibi seçilmiyor, dönüş hızı 260°/s). Gerçek pivot/plant için `Walk_Fwd_Pivot` seçimini zorlayan durum veya dönüş sırasında dönüş hızı artışı gerekiyor.
3. **Kamera kütle hissi**: yalnız derinlik gecikmesi var; hızlanma/frenleme için ivmeye bağlı küçük sönümlü tepki (SHME V2.53 tarzı) eklenmedi.
4. **Ayak IK / zemin teması** kapalı; eğim/basamak teması test edilmedi (ev koridoru düz).
5. Efor/nefes katmanı koşu sonrası yok; weighted idle yok (bilinçli: önceki SHME gerilemeleri).
6. Cook/paket, menüden save-load, 60 FPS gerçek oyun performansı NOT_TESTED.
7. Ayrı test haritası (`L_Sph_MoveTest`) PIE'de siyah render ediyor; veri kayıtları için kullanılıyor, görüntü için ev haritası.

## 9. İkinci tur (2026-11-09 öğleden sonra): kapsül fizik sözleşmesi, gerçek klip telemetrisi, kamera kütlesi

Sabah turunun açık maddeleri (§8) üzerinde aynı yöntemle devam edildi: aynı protokol, tek değişiklik, aynı ölçüm. Protokol `P_phys` (test koridoru, kamera sabit, klavye): boşta 1 s → W 2,5 s → bırak 1,5 s → W 1,5 s → **S 1,5 s (yürüyüşte 180° tersleme)** → bırak 1,2 s → W+Shift 2,5 s → bırak 2 s → W+Shift 2 s → **S+Shift 1,5 s (koşuda tersleme)** → bırak 1,5 s. Kayıtlar `data/P_phys_*.json` (before, a…i), analizler `an_turn.py`, `an_cmp.py`, `an_cc.py`.

### 9.1 Ölçüm aracı düzeltmesi: gövdenin gerçekten oynattığı klip
Sabahki rapor gövde klibini poz kütüphanesinden en yakın komşu ile okuyordu; sabit yürüyüş pozları birçok klipte aynı olduğu için bu okuma durakta "1,3 s'de 7–15 klip değişimi" gibi **yanlış** sonuçlar verdi (§9.3'teki "önce" sütunlarında NN okuması bu nedenle ayrıca işaretlendi). Motion Matching düğümünün gerçek seçimi için düğüm referansı (OnUpdate bağlama) Python'dan erişilemedi; `GetInstanceAssetPlayerTime` de dışa açık değil. Çözüm: 45 proje klip kopyasına iki float eğri yazıldı (`cm_curves1.py`, satıcı orijinalleri dokunulmadı): `SphClip` = sabit klip kimliği (`data/clipids.json`), `SphTime` = klip zamanı (0,1 s'de bir anahtar, doğrusal). Sürücü anim örneğinden `GetCurveValue` ile her karede oynatılan klip + zaman okunuyor; kimlik tam sayı değilse 0,3 s'lik blend sürüyor demektir. Bu, raporun "seçilen klip + zaman + yeniden seçim + oynatma hızı" gereksinimini karşılayan ilk gerçek kanıt kaynağıdır (`an_cc.py`: koşu uzunlukları, blend aralıkları, yeniden başlama sayısı, klip zamanı eğimi = oynatma hızı).

### 9.2 Ölçülen kök nedenler (kapsül tarafı)
1. **Zemin sürtünmesi 8 (× fren çarpanı 2)**: tuş bırakılınca kapsül her gait'te 0,11–0,17 s'de duruyordu (yürüyüş 180→0: 9 cm; koşu 500→0: 21 cm); W→S'de hız 0,13 s'de sıfırdan geçiyordu. Core Motion duruş klipleri 0,6–1,6 s'de yavaşlar; bu kadar hızlı duran bir kapsülün yörüngesine hiçbir duruş klibi uymaz → arama ayakta duran poza (klip sonu) atlıyor, gövde "pop" yapıyordu. (SHME V2.53 fren/yerleşme davranışının yeni sisteme taşınması.)
2. **Gait seçicisi hız düşerken anında Walk'a düşüyordu**: koşuda tuş bırakılınca 0,18 s sonra sürücü Walk veritabanına geçiyordu; `Run_Fwd_Stop` yalnız Run veritabanında olduğundan koşu duruşu hiç seçilemiyordu.
3. **Dönüş freni gait yumuşatmasının hedefine bağlıydı**: `MaxWalkSpeed` 3/s ile yumuşatıldığı için 180° terslemede hız sınırı geç düşüyor, karakter yüzü dönmeden 99 cm/s'ye çıkıyordu.
4. **Kapsül ivmesi 450 cm/s²** kaynak başlangıç kliplerinin 2,6 katıydı (Walk_Fwd_Start 180 cm/s'ye 1,05 s'de, kapsül 0,41 s'de): gövde başlangıç klibini doğru fazda oynatırken (gerçek klip: Walk_Fwd_Start 0,20→0,97 s kesintisiz) ayaklar 0,5 s boyunca zeminden yavaştı (kayma).
5. **Pivot klipleri (Walk/Jog_Fwd_Pivot) kök yaw içermiyor** (`q_prof.py`: yaw hızı tüm klipte 0; hız 207→154→0→163): gövde dönüyor, kök dönmüyor. Hareket yönüne dönen (OrientRotationToMovement) bir kapsülün yörüngesi bu klibe hiçbir zaman benzemez; bu yüzden sabah "pivot seçilmiyor" sonucu çıkmıştı. Terslemeler `*_Start_Turn*180` klipleriyle (0,7 s'de 180°, 26→157 cm/s hızlanırken) karşılanıyor; bu, kapsülün 260°/s dönüş hızına birebir uyuyor.

### 9.3 Uygulanan sözleşme (hepsi `BP_HybridA_Player`, satıcı/anim dosyaları değişmedi)
| Adım | Değişiklik | Betik |
|---|---|---|
| a | Fren sürtünmesi ayrı ve 0, zemin sürtünmesi 8→3 (yön değişimi ~0,4 s'de, duruş yalnız fren ivmesiyle) | `cm_phys1.py` |
| b | `GR_GaitSel` kilidi: girdi yokken ve kapsül >30 cm/s iken gait tutulur ("duruş, içinde olduğun gait'e aittir") | `cm_gait2.py` |
| c | Gait'e göre fren ivmesi 300 / 500 / 420 (yürüyüş 0,6 s–58 cm, koşu 1,25 s–3,1 m; kaynak kliplere göre) | `cm_brake1.py` |
| d | `GR_SpeedBase` (gait yumuşatması) ayrı değişken; `MaxWalkSpeed = GR_SpeedBase × GR_TurnScale` anında | `cm_turn4.py` |
| e | Klip eğrileri (telemetri) | `cm_curves1.py` |
| f | Dönüş freni tabanı 0,15→0,5 (dönerken ≤90 cm/s; kaynak start-turn kliplerinin hız bandı) | `cm_turn5.py` |
| g | Gait'e göre ivme 220 / 300 / 330 (yürüyüş 0,8 s, jog 1,0 s, koşu 1,5 s) | `cm_accel1.py` |
| h/i | Kamera kütle tepkisi (§9.5) | `cm_camkick1/2.py` |

### 9.4 Önce/sonra (aynı protokol)
Aynı `P_phys` protokolü, aynı test koridoru, kamera sabit. **Önce** = sabah turunun son hâli (`data/P_phys_before.json`, kapsül sözleşmesinden önce); **sonra** = bu turun son hâli (`data/P_phys_m.json`, §9.3 a–g + tersleme setinin geri alınması, §9.9/3). Kapsül sütunları `an_cmp.py` (duruş süresi/yolu, 0,25/0,5/0,75/1 s'deki hız, yüz açısı); gerçek klip dizisi `an_cc.py` (SphClip eğrisi; `~` = 0,3 s blend; parantez: klip değişimi, yeniden başlama, blend toplamı, oynatma hızı = klip zamanı eğimi). "Önce" kaydında klip eğrisi henüz yoktu; o sütun yalnız kapsül ölçümüdür.

| Segment | Önce: kapsül | Sonra: kapsül | Sonra: gerçek klip dizisi (SphClip) |
|---|---|---|---|
| Yürüyüş başlangıcı (W) | hız 0,25/0,5/0,75/1 s: 107/180/180/180; yüz: 0/0/0/0 | hız 0,25/0,5/0,75/1 s: 46/101/156/180; yüz: 0/0/0/0 | ?0.0 → ~ → Walk Fwd Start → ~ → Walk Fwd (3 switches 2 restarts 0 blend 0.38s rate [0.9, 0.11]) |
| Yürüyüş duruşu (bırak) | duruş 0.11 s / 9 cm; hız 0,25/0,5/0,75/1 s: 0/0/0/0; yüz: 0/0/0/0 | duruş 0.63 s / 58 cm; hız 0,25/0,5/0,75/1 s: 118/42/0/0; yüz: 0/0/0/0 | Walk Fwd → ~ → Walk Fwd Stop → ~ → ?0.0 (3 switches 2 restarts 0 blend 0.50s rate [1.03, 0.0]) |
| Yürüyüşte 180° tersleme (S) | duruş 0.14 s / 9 cm; hız 0,25/0,5/0,75/1 s: 52/99/129/132; yüz: -61/-125/180/180 | duruş 0.29 s / 21 cm; hız 0,25/0,5/0,75/1 s: 15/44/99/169; yüz: -54/-119/180/180 | Walk Fwd → ~ → Walk Start TurnL180 Lfoot → ~ → Walk Start TurnL045 Lfoot → ~ → Walk FwdLeft → ~ → Walk Fwd (5 switches 4 restarts 0 blend 0.83s rate [0.91]) |
| Koşu başlangıcı (W+Shift) | hız 0,25/0,5/0,75/1 s: 102/136/202/259; yüz: -121/-54/0/0 | hız 0,25/0,5/0,75/1 s: 59/134/209/284; yüz: -126/-61/0/0 | ?0.0 → ~ → Jog Start TurnR090 Rfoot → ~ → Run Fwd Start → ~ → Run Fwd (4 switches 3 restarts 0 blend 0.83s rate [0.93, 0.91, 0.02]) |
| Koşu duruşu (bırak) | duruş 0.16 s / 21 cm; hız 0,25/0,5/0,75/1 s: 0/0/0/0; yüz: 0/0/0/0 | duruş 1.25 s / 308 cm; hız 0,25/0,5/0,75/1 s: 412/307/202/97; yüz: 0/0/0/0 | Run Fwd → ~ → Run Fwd Stop → ~ → Walk Fwd → ~ → Walk Fwd Stop → ~ → Walk Start TurnR045 Rfoot → ~ → Walk Start TurnR180 Rfoot → ~ → ?0.0 (7 switches 6 restarts 0 blend 0.63s rate [0.01, 1.0, 0.0]) |
| Koşuda tersleme (S+Shift) | hız 0,25/0,5/0,75/1 s: 35/146/223/226; yüz: -61/-125/180/180 | hız 0,25/0,5/0,75/1 s: 79/34/109/184; yüz: -54/-119/180/180 | Run Fwd → ~ → Jog Start TurnL090 Lfoot → ~ → Jog Start TurnL045 Lfoot → ~ → Jog Fwd Start (4 switches 3 restarts 0 blend 0.50s rate [0.91, 0.92]) |

Okuma: yürüyüş ve koşu duruşları artık kaynak kliplerin yavaşlama süresinde (0,63 s / 58 cm; 1,25 s / 3,1 m) ve gövde gerçekten `Walk_Fwd_Stop` / `Run_Fwd_Stop` oynatıyor (önce 0,11–0,16 s'de duran kapsüle hiçbir duruş klibi uymuyordu). Başlangıçlar 1×'e yakın oynatma hızıyla (`Walk_Fwd_Start` 0,9; `Run_Fwd_Start` 0,91–0,93) kesintisiz; "hızlandırılmış klip" izi kalmadı (rate ≤ 1,03). Terslemeler: kapsül 0,29 s / 21 cm'de fren yapıp 180° dönüyor; gövde `Start_TurnL180` → `Start_TurnL045` → `Walk_Fwd` zinciriyle 0,8 s blend içinde (PARTIAL, §9.9/1,3). Koşu duruşunun son 0,6 s'inde kapsül 97 → 0 cm/s inerken arama kısa süreli Walk kliplerine düşüyor (tek karelik seçimler, 1,25–1,58 s) — gözle görülür sorun değil ama temiz değil (§9.9/2).

### 9.5 Kamera kütle tepkisi
Kol uzunluğu `FInterpTo(2,2/s)` ile yalnız hıza bağlı tek yönlü bir yumuşatmaydı; ivme içeriği yoktu ("donuk"). SHME V2.53'teki sönümlü sinyal yaklaşımı bağımsız olarak yeniden kuruldu (`cm_camkick1/2.py`): `GR_Accel` = yumuşatılmış ileri ivme (8/s), `GR_CamKick` sızıntılı integratör (`dKick = (0,05·a − 3·Kick)·dt`), kol = `GR_ArmBase` (eski 2,2/s yumuşatma, artık kendi değişkeninde) + clamp(Kick, ±8 cm). İlk sürümde `GR_PrevSpeed` ivmeden önce yazıldığı için (Blueprint pinleri çalıştığı anda değerlenir) ivme hep 0 çıktı; canlı sondayla yakalanıp sıra düzeltildi (`cm_camkick2.py`). Ölçüm (`P_phys_i.json`, kol uzunluğu 0,2 s'de bir):

| Durum | Kol izi (cm) | Okuma |
|---|---|---|
| Yürüyüş başlangıcı (0→180, 0,8 s) | 140 → 141,2 → 142,3 → 140,9 → 140,5 → 140,1 | +2,3 cm kısa açılma, 1 s'de yerleşme |
| Yürüyüş duruşu (180→0, 0,9 s) | 140 → 138,7 → 137,0 → 136,0 → 137,1 → 138,2 → 139,6 | −4 cm yaklaşma, 1,2 s'de geri |
| Koşu başlangıcı | 139,7 → 143 → 148 → 153 (hız tabanı +12) → 152,2 | hız açılması + küçük aşım |
| Koşu duruşu (500→0, 1,25 s) | 152 → 146 → 139 → **135,3** → 138 → 139,9 | tabanın 5 cm altına inip yerleşme |
| Koşuda tersleme | 152 → 137 → 141 → 147 → 153 | fren yaklaşması, itişle açılma |

Boşta kol sabit (kick 0); sabit hızda kick 0,7 s içinde sönüyor. Ritmik baş sallanması kola kopyalanmıyor (ivme kapsül hızından türetiliyor).

### 9.6 Kamera simetri ve fare testleri (koşu, fare süpürmeleri)
`CS_mouse_kick.json` (bahçe, gerçek çevre): yürüyüşte 90° / −90° fare süpürmeleri ve 0,5 s'de 360°, koşuda 90° / −90°: baş X 0,27–0,42 bandında kaldı (yürüyüş süpürme 0,34–0,36, 360° 0,28–0,37, koşu süpürme 0,34–0,42); çarpışma düzeltmesi 0 kare. Kamera yaw'ı fare sürerken karakter omuz-arkası kompozisyonda sabit kaldı; yön değişimi kapsülü yaydan geçirdi (fren istenmiyor).

`CS_run_kick.json` (bahçe, kamera sabit, Shift): A (sol koşu) baş X 0,20–0,25, D (sağ koşu) 0,45–0,49, W+A 0,21–0,31, W+D 0,40–0,45 (hedef bant 0,28–0,43). A segmentinde 1,17 s'de ölçülen 0,09 bir kamera hatası değil: karakter (1700,−700)'den +y yönüne koşarken **kesme istasyonuna çarpıp durdu** (hız 252→0), gövde engele yaslandı. Simetri nedeni ölçüldü: kapsül kompozisyonu ~0,33'te; gövde hareket yönüne doğru genişliğin ~0,1'i kadar eğiliyor/öteleniyor (pelvis X sola 0,30, sağa 0,36; baş daha fazla). Derinlik-only gecikme bunu göremez → yanal gövde kütlesi izleme eklendi (§9.6b).

**9.6b Yanal gövde kütlesi izleme** (`cm_camlat1/2.py`): görünür gövdenin **baş** soketinin kapsülden yanal (kamera sağ ekseni) sapması 4/s yumuşatılıp ±30 cm ile sınırlanarak yay kolu `TargetOffset`'ine ekleniyor (derinlik gecikmesinin yanına). İlk sürüm pelvisi izledi: pelvis ortalandı (A 0,33 / D 0,34) ama baş 0,21 / 0,46'da kaldı — koşuda gövde hareket yönüne genişliğin ~0,13'ü kadar eğiliyor ve oyuncunun gördüğü "karakter" baştır. Baş izleme ile (koridor, kamera sabit, `CS_run_head.json`; önce = `CS_run_lat.json` pelvis izleme / `CS_run_kick.json` izleme yok):

| Durum (kamera sabit) | Baş X önce (izleme yok) | Baş X sonra (baş izleme) | Bant dışı süre (ilk 0,4 s hariç) |
|---|---|---|---|
| A + Shift (sola koşu, 4 s) | 0,20–0,25 (koridor: 0,13–0,31, ort. 0,21) | **0,23–0,35, ort. 0,31** | 0,49 s (başlangıç dönüşü) |
| D + Shift (sağa koşu) | 0,45–0,49 (koridor 0,28–0,54, ort. 0,46) | **0,29–0,41, ort. 0,34** | 0,00 s |
| W+A koşu | 0,21–0,31 | 0,24–0,39, ort. 0,34 | 0,19 s |
| W+D koşu | 0,40–0,45 | 0,34–0,42, ort. 0,37 | 0,00 s |
| A yürüyüş | 0,16–0,39, ort. 0,24 | 0,23–0,36, ort. 0,29 | 1,04 s (0,23–0,28 arası) |
| D yürüyüş | 0,27–0,38 | 0,29–0,36, ort. 0,31 | 0,00 s |
| Boşta | 0,30 | 0,30 | 0 |

Sol/sağ farkı 0,25 → 0,03'e indi. Fare süpürmeleri (`CS_mouse_head.json`): yürüyüşte 0,30–0,36, koşuda 0,35–0,43, 360°'de 0,34–0,38; bant dışı 0 s. Yürüyüşteki baş salınımı kamerada görünür sallanma yaratmadı (4/s yumuşatma; boşta kol ve ofset sabit).

### 9.7 Regresyon (2. tur)
| Test | Sonuç | Kanıt |
|---|---|---|
| Kayıt / yükleme (`reg_save.sh`, canlı kullanıcı kaydı kenara alınıp bayt bayt geri kondu) | **PARTIAL**: oyun içi `SaveGame (StoryFramework)` çağrısı slotu yazdı (5764 B); aynı oturumda `LoadGame(True)` çağrısı pawn'ı kaydedilen noktaya (1280,−695) **taşımadı** (1300,−700'de kaldı; seviye yeniden yüklenmedi); test slotu ile **temiz başlangıçta** oyun kaydı yükledi ve oyuncu (832,−220)'de ayakta başladı (yeni oyunun yatak uyanışı değil), yürüyüş ve kamera normal (2 s'de 4,3 m). Story Framework'ün oyuncu konumunu nereden geri yüklediği (checkpoint alanı mı, pawn transformu mu) doğrulanmadı. | `data/reg_save2_t.txt` |
| Kullanıcı kaydı bütünlüğü | PASS: her lab/video sonrası kenara alınan kopya geri yazıldı; `cmp` eşit | lab/video betikleri |
| Temiz yeniden açılış | PASS: her yazma işinden sonra editör kapatılıp açıldı (emb_422–452); derleme hatası 0 (`ERR []`). İki kez (emb_4231, emb_4361) yazma/okuma işinden hemen sonra yeniden açmadan PIE başlatınca editör çöktü (python311 erişim ihlali) → kural: grafiğe dokunan her işten sonra PIE'den önce yeniden açılış | `data/phys_*_progress.txt`, günlükler |
| Çömelme / zıplama / ev içi hız / kesme istasyonu / uyanma | videolar §9.8 (H_hall, D_chop, A_loco) ile yeniden çekildi; kapsül fiziği değiştiği için yeniden izlenmeli | `videos/*_shme2.mp4` |
| Taşıma montajları, cook, 60 FPS | NOT_TESTED (değişmedi) | |

### 9.8 Videolar (2. tur)
Yedi video, hepsi bu turun **son** yapısıyla (§9.3 a–i + tersleme seti kapalı) ve düzeltilmiş kodlayıcıyla (§9.9/8) 2026-11-09 21:35–22:30 arasında gerçek oyunda (PIE, `L_GR_SphirusHouse`) çekildi: 30 kare/s, kesintisiz, gerçek zamanlı (her karede oyun adımı; `data/<video>.json` `gdt`), 1510×922 oyun bölgesi (editör penceresi ham ekran görüntüsünden kırpıldı). Kamera **sabit** (fare yok) — kadraj yargısı için en sert koşul; fare profili §9.6. Telemetri aynı kayıttan (`an_vidtab.py`); baş X hedef bandı 0,28–0,43 (segmentin ilk 0,4 s'si hariç). Kanıt kareleri her 30. ham kareden kırpıldı (`evidence/<video>_raw_f<kare>.png`).

| Video | Protokol (klavye) | Bakılacak yer |
|---|---|---|
| `PH_phys_shme4.mp4` | boşta → W+Shift 1,7 s → bırak 1,8 s (koşu duruşu) → **S 2 s (kameraya doğru 180° tersleme)** → bırak → W → S → bırak | koşu duruşu 1,25 s / 3 m, gövde `Run_Fwd_Stop`; tersleme fren → dönüş → yürüyüş; kamera kütle tepkisi (duruşta yaklaşma, kalkışta açılma) |
| `CL_strafe_shme4.mp4` | A 2,5 s, D 2,5 s, W+A, W+D, W, S | **sola yürürken** kadraj (şikâyet): baş sol/sağ simetrisi, ilk saniyedeki eğilme |
| `A_loco_shme4.mp4` | yürüyüş → jog → koşu (150° fare dönüşüyle) → koşu → yürüyüş → duruş → yürüyüş → duruş | gait geçişleri, kol uzunluğu hızla açılma, duruşlarda yerleşme |
| `B_turns_shme4.mp4` | 360° fare dönüşleri, 150° zikzak, duruş, yerinde 180°, Shift dönüşleri | dönüş freni (`GR_TurnScale`), dönüşte klip zinciri, kadraj |
| `H_hall_shme4.mp4` | ev alt kat koridoru: W, Shift, duruş, 300° dönüş, W | ev içi hız 150, kamera çarpışma düzeltmesi, dar alanda kadraj |
| `D_chop_shme4.mp4` | kesme istasyonu: yaklaş, E, bekle, sol tık, bekle | regresyon: etkileşim, aksiyon kamerası, montaj |
| `I_idle_shme4.mp4` | 20 s boşta | boşta klibi 1× ve tekrar yok; kamera tamamen sabit |

| Video | Süre / kare | Gerçek zaman (oyun adımı ort / maks) | Baş X segmentlere göre (min–ort–maks; bant dışı s) |
|---|---|---|---|
| `videos/PH_phys_shme4.mp4` | 12.5 s / 369 | 0.0338 / 0.2415 | bırak 0.30–0.30–0.30; W Shift 0.30–0.35–0.38; bırak 0.30–0.35–0.39; S 0.23–0.27–0.32 (dışarıda 1.4 s); bırak 0.24–0.28–0.32 (dışarıda 0.2 s); W 0.29–0.32–0.35; S 0.23–0.28–0.35 (dışarıda 0.9 s); bırak 0.21–0.28–0.34 (dışarıda 0.1 s) |
| `videos/CL_strafe_shme4.mp4` | 18.1 s / 543 | 0.0334 / 0.0613 | bırak 0.27–0.27–0.28 (dışarıda 0.4 s); A 0.22–0.29–0.37 (dışarıda 0.9 s); bırak 0.29–0.32–0.35; D 0.29–0.31–0.34; bırak 0.24–0.27–0.29 (dışarıda 0.3 s); W A 0.28–0.31–0.35; bırak 0.28–0.33–0.36; W D 0.29–0.33–0.37; bırak 0.30–0.32–0.33; W 0.28–0.33–0.36; S 0.20–0.26–0.35 (dışarıda 1.4 s); bırak 0.23–0.28–0.34 (dışarıda 0.2 s) |
| `videos/A_loco_shme4.mp4` | 10.9 s / 330 | 0.0330 / 0.0921 | bırak 0.28–0.28–0.28; W 0.28–0.34–0.36; W Shift 0.34–0.35–0.37; W Shift 0.37–0.39–0.41; W Shift 0.38–0.39–0.40; W 0.33–0.36–0.38; bırak 0.28–0.31–0.33 (dışarıda 0.1 s); W 0.30–0.34–0.36; bırak 0.30–0.32–0.36 |
| `videos/B_turns_shme4.mp4` | 15.3 s / 459 | 0.0332 / 0.0615 | bırak 0.28–0.29–0.30; W 0.28–0.34–0.36; W 0.30–0.35–0.37; W 0.30–0.33–0.35; W 0.30–0.30–0.32; W 0.30–0.32–0.33; W 0.34–0.37–0.38; W 0.32–0.33–0.38; W 0.31–0.32–0.33; W 0.31–0.34–0.35; bırak 0.26–0.31–0.34 (dışarıda 0.1 s); bırak 0.26–0.29–0.31; W 0.27–0.28–0.31; bırak 0.29–0.30–0.31; W Shift 0.30–0.33–0.37; W Shift 0.32–0.36–0.39; W Shift 0.32–0.37–0.39; bırak 0.28–0.34–0.39 |
| `videos/H_hall_shme4.mp4` | 9.9 s / 297 | 0.0332 / 0.0554 | bırak: ölçüm yok; W: ölçüm yok; W Shift 0.33–0.33–0.35; bırak 0.25–0.29–0.34 (dışarıda 0.4 s); bırak 0.26–0.28–0.32; W 0.21–0.32–0.35; bırak 0.24–0.30–0.33 (dışarıda 0.1 s) |
| `videos/D_chop_shme4.mp4` | 11.2 s / 339 | 0.0330 / 0.1536 | bırak 0.28–0.28–0.29; W 0.28–0.33–0.36; bırak 0.30–0.34–0.36; E 0.29–0.30–0.30; bırak 0.24–0.29–0.30 (dışarıda 0.4 s); LMB 0.29–0.29–0.29; bırak 0.28–0.29–0.29; bırak 0.28–0.29–0.30 |
| `videos/I_idle_shme4.mp4` | 20.0 s / 600 | 0.0334 / 0.0658 | bırak 0.27–0.29–0.30 (dışarıda 1.9 s) |

Okuma (telemetri aynı kayıttan; `an_cc.py` gerçek klip dizisi):

- **Gerçek zaman**: yedi videoda da oyun adımı ortalaması 0,033 s (30 kare/s = 1×). Tek karelik takılmalar: `PH_phys` 0,24 s (1 kare), `D_chop` 0,15 s (1 kare), `A_loco` 0,09 s — seviye/varlık yükleme; diğer tüm kareler ≤ 0,07 s. Hızlandırılmış görüntü yok. İlk `CL_strafe_shme4` kaydı telemetri JSON'u yazmadan bitti (bilinen aralıklı kusur); video aynı protokolle yeniden çekildi, tablo o kayda ait.
- **Sola yürürken kadraj (şikâyet)**: kamera sabit, A 2,5 s: baş X 0,22–0,37, ort. 0,29; D: 0,29–0,34, ort. 0,31 — sol/sağ farkı 0,02 (sabah 0,25). A'nın ilk ~0,9 s'inde baş 0,22–0,27 (gövde sola eğilirken baş izleme 4/s ile yetişiyor), sonra bantta; kadrajdan çıkma yok (`evidence/CL_strafe_shme4_raw_f60.png` 2 s, `_f90.png` 3 s, `_f150.png` D 5 s). W+A 0,31 / W+D 0,33. **PASS (ölçüm + ham kare)**; görsel kabul oyuncuya ait.
- **Kameraya doğru tersleme (S, kamera sabit)**: `PH_phys` ve `CL_strafe` S segmentlerinde baş X 0,20–0,26 (~1,4 s bant altı) ve karakter kameraya ~1 m'ye kadar yaklaşıyor (derinlik gecikme pivotu −20 cm kameraya doğru kayıyor); yüz kadrajın sol-alt çeyreğini dolduruyor (`evidence/PH_phys_shme4_raw_f150/180.png`). Kadrajdan çıkmıyor ama bu kompozisyon istenen "omuz arkası" değil; sabit kamerayla kameraya yürümenin çözümü otomatik yeniden ortalama/dönüş (tasarım kararı, §9.9/4) — **PARTIAL / REVIEW_REQUIRED**.
- **Boşta** (`I_idle`, 20 s): baş X 0,27–0,30, kamera tamamen sabit (kol 118 sabit, kick 0); 0,27 bandın hemen altı (nefes/ağırlık salınımı), kayma yok. Boşta klibi MM dışı tek SequencePlayer (klip eğrisi yok; 1× doğrulaması §1/§9.1'deki baş hızı ölçümüyle).
- **Hareket (videolarda görünen gerçek klipler)**: `PH_phys` koşu başlangıcı `Walk_Fwd_Start` 0,18→1,47 s kesintisiz (hız 0,97) → koşu; koşu duruşu 1,25 s / 3 m boyunca `Run_Fwd_Stop` 1,58→1,86 s, sonra 0,4 s düşük hızlı blend (§9.9/2); tersleme 0,7 s blend → `Walk_Start_TurnR090` → `Walk_Fwd` (§9.9/1,3). `A_loco` sabit gait segmentlerinde tek klip, değişim 0 (Walk_Fwd / Run_Fwd döngüleri), oynatma hızı 0,89–0,94 — kapsül hızı (180/500) kaynak klip kök hızının (196/512) biraz altında olduğu için; 1,0'a çekmek için yürüyüş hızı 195 yapılabilir (açık, küçük). Duruş segmentlerinde 5–6 klip değişimi (yavaşlama fazı blend çorbası, §9.9/2) — gözle "yerleşme" olarak okunuyor, temiz değil.
- **Regresyon**: `H_hall` ev içi 150 cm/s, kamera çarpışma düzeltmesi dar koridorda devrede, baş 0,29–0,35; `D_chop` E → aksiyon kamerası (kol 107) → sol tık → montaj; etkileşim ve istasyon akışı bozulmadı (**PASS**). Kullanıcı kaydı her videodan sonra bayt bayt geri yazıldı (`cmp` eşit).
- **Kabul durumu**: teknik (gerçek zaman, kodlama, telemetri eşleşmesi) PASS; kadraj A/D/W/boşta PASS, kameraya doğru tersleme PARTIAL; hareket başlangıç/duruş PASS (kaynak klip süresinde, gövde doğru klibi oynatıyor), tersleme PARTIAL. Görsel/his kabulü oyuncunun izlemesini bekliyor (REVIEW_REQUIRED).

### 9.9 Kalan engeller (güncel)
1. **Gerçek pivot yok**: paketin `Walk/Jog_Fwd_Pivot` kliplerinde kök yaw 0 (gövde dönüyor, kök dönmüyor); hareket yönüne dönen kapsülle eşleşemez. Python'dan kemik izi yeniden yazımı mümkün değil (`AnimSequence.get_controller/get_data_model` yok, `q_pivotapi.py`); çözüm için klibin DCC'de (Blender) kök yaw'ı eklenerek proje kopyası olarak yeniden dışa aktarılması gerekir — bu turda yapılmadı. Terslemeler `*_Start_Turn*180` kliplerinden karşılanıyor (fren → dönüş başlangıcı → itiş); yüksek hızda "yüklü ayakla pivot" hissi hâlâ yok (PARTIAL).
2. **Yürüyüş duruşu**: kapsül 0,62 s / 58 cm'de duruyor; gövde `Walk_Fwd_Stop` klibinin yalnız son 0,5 s'ini (2,9→3,4 s, ayakta yerleşme) oynatıyor; klibin yavaşlama adımı (1,3–2,9 s, ~140 cm/s²) oyuna giremiyor. Fren 300→200 denemesi (`cm_brake2.py`) pin eşleştirmesi başarısız olduğu için uygulanamadı (iki deneme, `CHANGED 0`); açık. Koşu duruşu: `Run_Fwd_Stop` 1,1→1,85 s (son yavaşlama + yerleşme) oynuyor, kapsül 1,25 s'de duruyor; son ~0,3 s'de ayak kayması olası.
3. **Tersleme blend süresi** (denendi, geri alındı): 180° klavye terslemesinde gövde 0,75–0,85 s blend içinde (tek karelik seçimler). Durum sürümlü bir **tersleme veritabanı seti** denendi (`cm_rev1.py`: gait'in `Start_Turn{L,R}180` + `Fwd_Stop` klipleri, pawn `GR_Reverse` histerezisli yön hatası bayrağı, sürücüde Steady dalından önce kontrol): aynı protokolde blend süresi **0,75 → 1,21 s'ye çıktı** (`data/P_phys_l.json` seg 4) — üçüncü bir veritabanı kademesi (Loop → Rev → Full → Loop) bir arama/blend daha ekliyor ve 180° klipleri yine tutunamıyor. SHME yöntemi gereği geri alındı (`cm_rev2.py`: eşikler 9999, bayrak kapalı; `data/P_phys_m.json` ≈ geri alma öncesi j2 kaydı, 0,83 s). Veritabanı varlıkları (`PSD_Sph_*Rev`) projede duruyor ama hiçbir dalda seçilmiyor. Kalıcı çözüm kök yaw'lı pivot klibi (madde 1).
4. **Kamera yanal kadraj**: ölçüldü ve kapatıldı (§9.6b): baş izleme ile sol/sağ farkı 0,25 → 0,03; koşuda A 0,23–0,35, D 0,29–0,41. Kalan: sabit kamerayla A'ya ilk basışta ~1 s baş 0,22–0,27 (gövde sola eğilirken izleme 4/s ile yetişiyor) ve 180° terslemede kameraya doğru yürürken baş 0,24–0,27 (bandın hemen altı, kadrajda). Her iki durum da videolarda (§9.8) görülüyor; kadrajdan çıkış yok.
5. **Save/load**: oyun içi `LoadGame` çağrısı pawn'ı taşımadı; önyükleme ile yükleme (832,−220)'ye koydu — Story Framework'ün konum geri yükleme sözleşmesi doğrulanmadı.
6. Tam gait veritabanının başlangıç penceresi tercihi (§8.1), ayak IK/eğim, efor/nefes katmanı, taşıma montajları, cook, 60 FPS: değişmedi (NOT_TESTED / açık).
7. Test haritası siyah render ediyor (veri kayıtları için kullanıldı); fare süpürme ve koşu simetri testleri bahçede (gerçek çevre) ve koridorda (engelsiz) ayrı ayrı yapıldı.
8. **Video kodlayıcı hatası (bulundu, düzeltildi)**: `mkvid.py` Blender 5.2'de kırpma dikdörtgenini yeniden ortalamıyordu; sabah (`*_shme.mp4`) ve öğleden sonra (`*_shme2/3.mp4`) videolarının **sol ~200 px / üst ~60 px'i eksikti** ve siyah bantla doluyordu — bu videolarda karakter sol kenarda kesik görünüyor, gerçek kadraj değil. Ham editör ekran görüntüsü (`frames/<video>/ScreenShot*.png`, her 30. kare) ile karşılaştırılarak bulundu: boşta baş X ham karede 0,29 = telemetri 0,29; hatalı videoda 0,19. Kodlayıcı düzeltildi (crop merkez ofseti), yedi video düzeltilmiş kodlayıcıyla yeniden çekildi (`*_shme4.mp4`, §9.8); kanıt kareleri (`evidence/*_raw_f*.png`) artık ham ekran görüntüsünden kırpılıyor. Hatalı videolar rapordan kaldırıldı. Telemetri (ProjectWorldLocationToScreen / viewport) doğru çıktı; kamera ölçümleri geçerli.
