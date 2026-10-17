# SHME V2.13 — yeni yön isteğinin karşılanması + ölçülü insan hareketi

Tarih: 2026-10-17. Motor: UE 5.8.1. Başlangıç: V2.12 üretimi + fren pivotu bake'i (2026-10-17 sabahı). Kanıt: `Saved/Codex/SHME_V213_20261017/`. Araçlar: `Tools/SHME_V213_20261017/`.

**Kabul ayrımı:** teknik = benim ölçümlerim; görsel = yakalama karelerine benim bakışım; kullanıcı kabulü = senin oyun testin. Hiçbir maddede kullanıcı kabulünü verilmiş saymadım.

## 0. Özet durum

| Hedef | Teknik | Görsel (benim) | Kullanıcı | Üretimde |
|---|---|---|---|---|
| 2 Yeni yön isteği: kesiş → S / kesiş → ters kesiş | PARTIAL: eski kesiş itişi 0.26–0.33 s → 0.06 s'de fren pivotuna geçiyor; sonrası hâlâ tempolu döngü + koşu başlangıcı ("ikinci başlangıç") | PARTIAL | bekliyor | evet (`SHM212_RdRev` 1 + `SHM213_RevVel` 1) |
| 2 Yerinde dönüş → ters dönüş | PASS: ters dönüş 1.9 s → 0.5–0.8 s'de başlıyor | PARTIAL (kesilen dönüşte 0.2–0.4 s yerinde kayma) | bekliyor | evet (`GR213_TipRev` 1) |
| 3 Atiklik (hareket modeli) | PASS ölçüm: depar kesiş 0.96 → 0.69 g, tempolu 0.86 → 0.71 g, depar ivmesi 360 → 300, geri fren ilk kare 1281 → 931 cm/s²; yürüyüş aynı | PARTIAL | bekliyor | evet (`DA_GR_LocomotionBehavior` M1) |
| 4 Depara atılma | PARTIAL: yürüyüşten itiş eğilme 35.6 → 32°, pelvis 12.4 → 8 cm, kol hamlesi 68 → 57 cm; duruştan 36.9 → 30.4°, 17 → 12 cm; giriş kayması 10–12 cm kaldı | PARTIAL | bekliyor | evet (klip bake'leri) |
| 5 Fren–destek–yeniden itiş adayı | FAIL (iki yaklaşım denendi, ikisi de kaliteyi karşılamıyor; §5) | — | — | hayır (uyuyor) |
| 6 Geri + rahat dönüş | PASS sınırlar; ilk kare kesiğinin sahibi bulundu (§6) | PARTIAL | bekliyor | korundu |

## 1. "Normal insan" hedefi — mevcut üretimden okunanlar (V2.12 + pivot bake'i, `v212q0_*`, 30 fps)
- **Rahat yürüyüş:** 132 cm/s, kol salınımı 19–31 cm; küçük yön düzeltmeleri (45°) 0.29 g, 90° yön değişimi 0.60 g. Hedefe uygun; dokunulmadı.
- **Yürüyüşten depara:** gövde 35.6° öne, pelvis 12.4 cm iniyor, el ileri-geri hamlesi 67–70 cm (depar döngüsü 44–57 cm) → **döngüden %40 büyük kol hamlesi, blok çıkışı izi.**
- **Duruştan depara (Shift+W):** 36.9°, pelvis 17 cm iniyor.
- **Depar kesişi (W+D):** 0.89–0.96 g yanal, 490 → 101–139 cm/s (%72–79 hız kaybı), gövde 59° öne (kesiş klibi içeriği); kesiş bitince tempolu döngü → koşu başlangıcı.
- **Kesiş → ters istek:** ters tuştan sonra eski kesiş klibi 0.26–0.33 s daha oynuyor, sonra aynalı kesiş klibi 0.77'den; hız 100'e düşüyor; "ikinci başlangıç".
- **Yerinde dönüş → ters dönüş:** ikinci dönüş ilk montaj bitene kadar bekliyor (1.9 s).
- **Deparda S:** fren pivotu (bake'li) 10.4 cm pelvis inişi; S'nin ilk karesinde 1281 cm/s² hız kesiği.
- Gerçek hareket referansı olarak yalnız V2.4'te kaydedilmiş insan ölçüleri (rahat kesiş 0.3–0.5 g, 45–90° kesiş 1–2 adımda) kullanıldı; video incelemedim.

## 2. Yeni yön isteği — eski harekete takılma
### 2.1 Zaman çizelgesi (sahibi, ölçülerek; `dirchange213.py`, `v212q0/q1_*`)
Depar W+D kesişi, 0.35 s sonra A (`r_cutrev_r`):
- +0.00 A basılı: bileşen `RedirectionAngle` 44° → 135°, `RedirectEnd` = 3 ("yeni niyet") bir kare yanıyor; **ama bileşen bölümü bitmiyor:** `RedirectTime` artmaya devam ediyor, sınıf 1 (yanal) kalıyor, bölüm ancak azami süreyle (0.7 s) bitiyor. Bu, `BP_SHM_HumanMotionComponent.SHM_UpdateRouting`'in gerçek davranışı; grafikteki bitiş mantığı bunu yapmamalıydı, telemetriyle kanıtlandı (`cv_RedirectEnd`, `cv_RedirectTime`).
- ABP bu yüzden eski bölümde kalıyor: `SHM_RedirectFrames` sayıyor, veritabanı tutması (`SHM_HoldDB`) eski kesiş veritabanında, `SHM210_CutTail` 0.8 s'ye kadar uzatıyor.
- MM: eski kesiş klibi +0.26–0.33 s daha (itiş evresi), sonra aynalı kesiş klibi 0.77'den (yeni itiş = ikinci başlangıç), hız 100.
- Kapsül: `RedirectFriction` 4.6 ile ~1950 cm/s² frenliyor; yani **kapsül sola yönlenirken animasyon sağa itişi sürdürüyor** (kullanıcının gözlemi).

Denenen ama etkisiz: `SHM213_RestartOn` (bileşen `RedirectTime` sıfırlanınca ABP bölümünü yeniden başlatma) — bileşen yeniden başlamadığı için hiç tetiklenmedi; kuruldu, kapalı (0).

### 2.2 Değişiklik (ABP `SHM212_Guard`, `install_v213_guard3.py`)
- **Hız–niyet açısı tetiği (`SHM213_RevVel` 1, açı 110°):** yanal bölüm sürerken girdi, hızla 110°'den fazla açı yapıyorsa (hız > 150) ABP bölümü ters dönüş olarak yeniden sınıflıyor (sınıf 2, köprü karesi, yan = hız × niyet). V2.12'nin ters dönüş yolu (`SHM212_RdRev` 1) bunun üstünde çalışıyor; `RevTurnMode` 0 (CutRev veritabanları yok).
- Niyet, bileşenin yumuşatılmış istek yönü değil, o karenin CMC girdi ivmesi (bileşen yönü tuşu ~0.2 s geç izliyor).
- Sonuç: eski kesiş klibi yerine 0.06 s'de fren pivotu (`A_LR_Run_Pivot_F_B`, bake'li) geliyor; sonra geri/aynalı tempolu döngü ve koşu başlangıcı.

### 2.3 Önce / sonra (30 fps; önce `v212q0`, sonra `v212q2/q3` rv ve son üretim `v213f`)

| Olay | MM'in yeni içeriğe geçişi | İlk içerik | Pelvis inişi (olay penceresi) |
|---|---|---|---|
| Sağ kesiş → A | 0.33 s → 0.06 s | aynalı kesiş itişi 0.77 → fren pivotu 0.63–0.67 | 10.7 → 5.3–11.8 cm |
| Sol kesiş → D | 0.32 → 0.05 s | aynı | 12.0 → 11.5 |
| Erken (0.15 s) | 0.25 → 0.05 s | aynı | 16.7 → — |
| Geç (0.6 s) | 0.15 → 0.06 s | aynı | 8.0 → — |
| Kesiş → S | 0.25–0.26 → 0.06 s | aynalı kesiş → fren pivotu, sonra geri koşu | 4.9 → 2.0–6.3 |

(Son üretim sayıları §7'de.)

### 2.4 Kalanlar
- Pivot bitince tempolu döngü → koşu başlangıcı ("ikinci başlangıç") duruyor; bağlantılı itiş yok (madde 5).
- Tetik düz depar → S'de de bir kez yanıyor (sınıf zaten 2 olduğu için görünür bir değişiklik yok; ölçüldü).
- Bileşenin bölüm bitiş kusuru (`RedirectEnd` 3 ama bölüm sürüyor) bileşen tarafında düzeltilmedi; ABP bunu telafi ediyor.

### 2.5 Yerinde dönüşte ters istek (`BP_GR_Player.GR_UpdateIdleTurn`, `install_v213_tipint*.py`)
- **Sebep:** yeni dönüş montajı yalnız hiç montaj oynamıyorken başlıyordu.
- **Değişiklik (`GR213_TipRev` 1, profil alanı):** montaj 0.35 s'den eskiyse, kontrol–aktör açısı ≥ 42° ve işareti montaj başlarken kilitlenen açının tersiyse montaj durduruluyor (0.12 s harman); normal seçim ters dönüşü bir sonraki karede başlatıyor.
- **Önce / sonra:** ters dönüş başlangıcı kamera isteğinden 1.9 s sonra → 0.53–0.77 s sonra (`t_tiprev`, `t_tiprev2`).
- **Kalan:** kesilen montajın basılı ayağı yerinde kayıyor (18–23 cm orta basış kayması, önce 13–21); montaj yarıda kesilince kapsül kısmi dönmüş kalıyor, ikinci montaj kalan açıyı tamamlıyor.

## 3. Atiklik — hareket modeli (`DA_GR_LocomotionBehavior`)
### 3.1 Sahip
Kapsül tepkisi GR piyonunun fizik yeniden yönlendirmesi (`GR_Impl_CP_PhysicalRedirect`): kesiş sürtünme tavanı `CutLatAccelMax`, dönüşte hız kaybı `TurnSpeedLoss*` (150–490 cm/s arasında devreye giriyor, yürüyüş etkilenmiyor), gait ivmeleri. Üç varyant ölçüldü (temel / M1 / M2; `v212q2_*`).

### 3.2 Seçilen (M1, üretimde)

| Alan | Önce | Sonra |
|---|---|---|
| `SprintAcceleration` | 360 | 300 |
| `RunAcceleration` | 300 | 270 |
| `CutLatAccelMax` | 650 | 450 |
| `TurnSpeedLoss` / `Min` | 0.35 / 0.7 | 0.5 / 0.6 |
| Değişmeyen | yürüme ivmesi 200, hızlar 132/300/490, frenler, `TurnLatAccelMax` 1400, bakış hızları, kamera | |

### 3.3 Önce / sonra (`turn_shape.py`, 30 fps)

| Senaryo | Önce | M1 | M2 (alınmadı) |
|---|---|---|---|
| Depar W+D/W+A geniş viraj, yanal g | 0.96–0.97 | 0.69 | 0.59–0.84 |
| Depar fare 45° viraj, yanal g | 0.62–0.63 | 0.59 | 0.51 |
| Tempolu W+A↔W+D, yanal g / dönüş yarıçapı | 0.85–0.86 g / 60 cm | 0.71 g / 73 cm | 0.63 g / 88 cm |
| Yürüyüş 45° / 90° düzeltme, yanal g | 0.29 / 0.60 | 0.28 / 0.55 | 0.28 / 0.51 |
| Deparda S, ilk karedeki hız kesiği | 1281 cm/s² | 931 | 811 |
| Depar kesişi → ters: ilk kesişte hız kaybı | %79 (101 cm/s) | %70 (147) | %69 (153) |

- M2 alınmadı: geniş viraj hız kaybı %14 ve depar virajında `TurnLatAccelMax` 1100 ile yön tamamlanma 1.27 s (M1 1.2, önce 1.04); fazla yavaş.
- Girdi alınma süresi değişmedi (MM geçişleri 0.05–0.06 s); fiziksel yön tamamlanma süresi uzadı (depar 90 % yön: 1.10 → 1.23 s). Bekletme yok.

## 4. Depara atılma
### 4.1 İnceleme
- Yürüyüşten itiş (V2.12 `GaitPush`, satıcı yürüme→depar): oyunda 35.6°, pelvis 12.4 cm, kol hamlesi 67–70 cm (döngü 44–57): **kol hamlesi döngüden %40 büyük** (`armswing213.py`).
- Duruştan (Shift+W, `RR_Start`): 36.9°, 17 cm.
- Tempolu → depar: itiş içeriği yok (V2.12 F3b reddi sürüyor); hızlanma 300 → 490'da yalnız döngü hızlanıyor. **Değişmedi.**
- Giriş kayması: yürüme döngüsünden klibe geçiş karesinde basılı ayak 10–12 cm.

### 4.2 Değişiklik (klip bake'leri; `v212_push_posture.py` + kol sönümü)
- **Yürüme/koşu → depar kopyaları (4 klip, satıcı kaynağından tek geçiş):** 12°'yi aşan öne eğilmenin %85'i geri; pelvis 93 cm tabanı; bacaklar aynı ayak konumlarına; **kol hamlesi**: kol kemiklerinin yerel dönüşü ±0.47 s'lik koşan ortalamaya doğru %40 çekildi (itiş penceresi 0.33–0.62). Baş bakışı korundu. `leg_guard` geçti.
- **Duruştan koşu başlangıcı (`A_RR_M_Relaxed_Run_Start_F_L/R`, mevcut klipten yerinde):** 16°'yi aşan eğilmenin %75'i geri, pelvis 90 tabanı. Kollar dokunulmadı (zaten küçük).
- **Giriş penceresi denemesi:** son yürüme adımının basış ortasına (1.13 s) kaydırılınca giriş kayması 12.5–16.7 cm'ye çıktı → geri alındı (1.01). Kalıntı.

### 4.3 Önce / sonra (30 fps)

| Ölçü | Önce | Sonra |
|---|---|---|
| Yürü → Shift: gövde tepe | 35.6° | 30.2–32.3° |
| Yürü → Shift: pelvis inişi | 12.4 cm | 5.8–8.8 cm |
| Yürü → Shift: el hamlesi (itiş / döngü) | 67–70 / 44–57 cm | 56–59 / 36–57 cm |
| Yürü → Shift: giriş kayması | 9.9–11.5 cm | 9.6–11.8 cm (aynı) |
| Depar döngüsüne çıkış kayması | 0.3–1.1 cm | 0.4–2.3 cm |
| Dururken Shift+W: gövde tepe / pelvis | 36.9° / 17.0 cm | 30.4° / 11.6–12.2 cm |
| Ters dönüş → W (koşu başlangıcının ortasından giriş) | 1 itiş | 1 itiş (aynı giriş noktası) |

## 5. Fren–destek–yeniden itiş adayı (depar → sağ kesiş → itiş bitmeden sol)
İki yaklaşım kuruldu ve gerçek koşuda ölçüldü.

**A. Mevcut hareket modeline uygun içerik (köprü = V2.12 ters dönüş veritabanı, bake'li fren pivotu):** §2'deki üretim yolu. Fren pivotu 0.06 s'de geliyor, ayak kayması pivot bake'iyle sınırlı; **ama** pivot bitince MM tempolu döngü/koşu başlangıcına gidiyor: yeni yöne bağlantılı itiş yok. Üretimde (madde 2 çözümü olarak), "toparlanma adayı" olarak değil.

**B. Yerel kök hareketi (`SHM213_RevMont`, `install_v213_revmont.py`, `SHM213_MontTick`):** ters istek anında projeye ait 180° depar dönüşü kopyası `DefaultSlot`'ta kök hareketli dinamik montaj olarak oynatılıyor (0.75 s'den, 0.65 s, harman 0.1/0.15). Kapsül klibin kökünü izlediği için basışlar kaymıyor. Ölçüm (`v212q4_r_cutrev_r_mont_r2`):
- montaj A'dan 0.03 s sonra başlıyor; kapsül klibin kökünü izliyor: 262 → 432 cm/s'ye sıçrama (giriş hızı eşleşmiyor), 0.24 s'de 0'a fren, 0.25 s sonra 237'ye yeniden hızlanma; çıkışta `SHM_Rec_*` toparlanma klipleri devreye giriyor;
- **pelvis 55 cm'ye iniyor** (satıcı 180° dönüşünün çömelmesi; V2.12 itişinden de derin): "normal insan" hedefiyle çelişiyor;
- **aktör yönü kök hareketiyle dönmüyor** (GR piyonu her kare yönü kendisi yazıyor): kapsül yolu −136°'ye dönerken gövde +44°'de kalıyor, yani 0.5 s "moonwalk"; yön ancak montaj bitince GR'ın dönüş hızıyla tamamlanıyor.
- **Sonuç: FAIL; kapalı (0).** Çalışır hale gelmesi için gerekenler: (1) montaj boyunca GR yön yazımının kök hareketine bırakılması, (2) 180° klibinin pelvis/duruş bake'i (fren pivotu gibi) veya oyun hızında kaydedilmiş sakin bir dönüş, (3) giriş zamanının kapsül hızına göre seçilmesi.

**Eksik kaynak hareket:** 300–490 cm/s'de, ~800–2000 cm/s² ile frenleyen, bir dengeleme adımıyla 130–180° dönen ve yeni yöne tek adımda iten, pelvisi 80 cm'nin altına indirmeyen bir yön değişimi. Projede ve önizlediğim satıcı paketlerinde yok (180° depar dönüşleri 727 cm/s, pelvis 54–58 cm; 90° kesişler 59° öne eğilme).

## 6. Geri hareket ve rahat dönüş
- Shift+S: fren pivotu → geri tempolu (≤300), ileri klip geriye taşınmıyor, kamera 180+W ayrı (önceki ölçüm aynı).
- **İlk S karesindeki sert hız düşüşünün sahibi:** CMC'nin sürtünme terimi; GR yeniden yönlendirmede `GroundFriction` = `RedirectFriction` (4.6) → 4.6 × 447 ≈ 2050 cm/s² + ivme 360 → ~2400 cm/s² ilk kare. Bir hız sınırı kesmesi değil. `CutLatAccelMax` tavanı (M1 450) bunu 931 cm/s²'ye indiriyor.
- Geri geçişteki çömelme: fren pivotu bake'i (sabah) 17–21 → 5–11 cm; M1 ile 8.2–10.2 cm.
- Yerinde dönüş kolları V2.11 gibi (abd medyan −5..+6°, idle 12–18); gövde yana savrulması 6–9° (klip içeriği, değişmedi).
- Veritabanları: `/Rollbacks/` kopyası 0; yeniden açılış + indeksleme sonrasında aynı (`verify_prod213.txt`).

## 7. Son üretim ölçümleri (kayıtlı V2.13, `v213f_*`, 30 fps; önce = `v212q0_*` aynı gün)

| Zincir | Ölçü | Önce (V2.12) | Sonra (V2.13) |
|---|---|---|---|
| Depar kesişi → ters kesiş (sağ / sol) | yeni istekten fren pivotuna | 0.33 / 0.32 s (önce aynalı kesiş itişi) | 0.06 / 0.06 s |
| | istek anındaki hızdan en düşük hıza | 312 → 101 / 313 → 110 | 300 → 142 / 303 → 146 |
| | fren mesafesi | 64 / 63 cm | 91 / 94 cm |
| | yeniden hızlanma (vmin → %90) | 1.05 / 1.04 s | 1.11 / 1.09 s |
| | en büyük \|a\| | 1607 / 1630 cm/s² | 920 / 877 cm/s² |
| Erken (0.15 s) / geç (0.6 s) ters istek | pivota geçiş | 0.25 / 0.15 s | 0.06 / 0.06 s |
| Depar kesişi → S | pivota geçiş; pelvis | 0.25 s; 4.9 cm | 0.06 s; 14.3 cm (pivot F_B içeriği, fren) |
| Depar S → W (fren bitmeden) | ilk içerik | pivot F_B 0.09 s | aynı, 0.09 s |
| Yerinde dönüş → ters (90/90, 90/180) | ters dönüşün başlaması | 1.9 s (ilk montaj bitince) | 0.52 s / 0.68 s (ilk montaj 0.33 / 0.46 s'de kesiliyor) |
| Yürü → Shift | gövde tepe / pelvis / el hamlesi / giriş kayması | 35.6° / 12.4 cm / 67–70 cm / 11.5 cm | 31.1–31.3° / 7.7–8.0 cm / 56–59 cm / 10.2–12.3 cm |
| | depar döngüsüne giriş hızı | 488 cm/s, 0.95 s | 488 cm/s, 1.13 s (ivme 300) |
| Dururken Shift+W | gövde tepe / pelvis | 36.9° / 16.6 cm | 31.5° / 11.8 cm |
| Tempolu → Shift | itiş | yok | yok (değişmedi) |
| Depar W+D / W+A geniş viraj | yanal g / hız kaybı | 0.96 g / %7–9 | 0.66–0.71 g / %5–12 |
| Depar fare 45° viraj | yanal g / yön tamamlama | 0.63 g / 0.87–1.04 s | 0.56 g / 0.91–1.20 s |
| Tempolu W+A↔W+D | yanal g / yarıçap | 0.86 g / 60 cm | 0.69–0.71 g / 72 cm |
| Yürüyüş 45° / 90° düzeltme | yanal g | 0.29 / 0.60 g | 0.28 / 0.56 g |
| Deparda W bırak → S | ilk kare kesiği / pelvis / geri azami | 1281 cm/s² / 10.4 cm / 300 | 938 cm/s² / 8.4 cm / 300 |
| S+A | pelvis / geri azami | 18.0 cm (bake öncesi) | 4.2 cm / 300 |
| W basılıyken S (40 ms) | ilk kare / geri azami | 2597 cm/s² / 300 | 2076 cm/s² / 300 |
| Idle → yürü → dur → yürü | basış kayması toplam en çok | 12.3 cm | 16.1 cm (orta basış 6.1 → 11.8; tek koşu) |
| Eğimde dur → dön → başla | toplam en çok | 33.6 cm (rampaya ilk adım 24.6) | 54.0 cm (rampaya ilk adım 39.2; tek koşu, yürüme modeli değişmedi) |
| Tek ayak yükseltide | toplam en çok | — | 19.4 cm |
| Düz yürüyüş 16 s | orta basış p90 | — | 1.2 cm |
| Diz ekseni >30° sıçrama | 23 koşu | — | 0 |

Notlar: fren mesafesi ve yeniden hızlanma bilerek uzadı (hareket modeli); girdi alınma süresi (MM geçişi) 0.03–0.09 s. Rampa ve yeniden başlama kaymaları tek koşu; önce/sonra farkı yürüme modeli değişmediği için koşu değişkenliği olarak işaretlendi, doğrulanmadı.

## 8. Görsel inceleme (yakalama kareleri; kabul değil)
- **Kesiş → ters istek** (`img/cut_reverse_before_after.jpg`, çapraz):
  - Önce (V2.12): A'dan sonra derin, öne kapanmış sağ kesiş hamlesi sürüyor, sonra aynalı hamle; iki "atılma" üst üste.
  - Sonra (V2.13): A'dan hemen sonra bacaklar açık, daha dik bir fren duruşu (fren pivotu), sonra sola dönüp koşu. Daha az çömelme; ama pivottan koşuya geçiş hâlâ bir "yeniden kalkış" gibi okunuyor (tempolu döngü → koşu başlangıcı).
  - Kesiş → S: fren pivotu, sonra geri koşu; öne kapanma yok.
- **Depara atılma** (`img/push_before_after.jpg`, yan): önce gövde belirgin öne, kollar büyük hamleyle; sonra daha dik gövde, daha küçük kol hamlesi, daha yüksek pelvis; adım hâlâ bir koşu adımı (adım uzunluğu değiştirilmedi). Duruştan Shift+W: dik, kademeli bir koşu başlangıcı.
- **Yerinde dönüş → ters** (`img/tip_reverse_before_after.jpg`): önce ilk dönüş bitene kadar (60 kare+) karakter sağa dönük kalıyor; sonra ~30. kareden itibaren geri dönmeye başlıyor. Kesilen montajda ayak yerinde kayıyor (ölçüldü).
- **Virajlar / küçük düzeltmeler / geri:** oyun kamerası videoları `vid/` altında; önce/sonra farkı videoda hız ve yarıçap olarak görünüyor, kare tablosuyla anlamlı değil.
- Test görünümü yalnız test dünyasında (gövdede opak kil); hiçbir kare kesilmedi.

## 9. Değişen dosyalar, etkin ayarlar, geri alma
**ABP `ABP_GR_MotionMatchingBase` (+ alt derleme):**
- `SHM_Snapshot`: `SHM213_RestartOn` dalı (0, etkisiz, kaldı).
- `SHM212_Guard`: `SHM213_RevVel` / `SHM213_RevVelAngle` tetiği.
- `SHM213_MontTick` + EventGraph montaj dalı (`SHM213_RevMont` 0 = kapalı; `SHM213_RevClipL/R`, `MontStart` 0.75, `MontLen` 0.65).
- Varsayılanlar: `SHM212_RdRev` 1, `SHM213_RevVel` 1, `SHM213_RevVelAngle` 110; diğer modlar değişmedi (`verify_prod213.txt`).

**`BP_GR_Player.GR_UpdateIdleTurn`:** ters dönüş kesme dalı + `GR213_TurnDelta0` kilidi. **`BP_GR_MotionProfile`:** `GR213_TipRev` alanı. **`DA_GR_LocomotionBehavior`:** M1 + `GR213_TipRev` 1.

**Klipler (yerinde bake, checkpoint'leri `checkpoint/pre_push`, `pre_rrstart`, `pre_window`):** `SHM212_Walk_to_Sprint_{L,R}foot`, `SHM212_Run_to_Sprint_{L,R}foot`, `A_RR_M_Relaxed_Run_Start_F_{L,R}foot`. Veritabanı girişleri değişmedi.

**Değişmeyenler:** `BP_PBI_Player`, `BP_SHM_HumanMotionComponent`, `DA_SHM_Response_Default`, anatomi/iskelet/kıyafet/harita/kamera, diz üreticisi ve `leg_guard`, V2.11 kolları, V2.12 itiş tetikleri/veritabanı temizliği.

**Geri alma:**
- Hızlı: `SHM213_RevVel` 0 + `SHM212_RdRev` 0 (madde 2); `GR213_TipRev` 0 (yerinde dönüş); DA M1 alanlarını önceki değerlere (360/300/650/0.35/0.7).
- Tam: `checkpoint/baseline_v212piv/` (ABP'ler, piyon, profil, DA'lar, bileşen, klipler) editör kapalıyken.

**Araçlar:** `install_v213_cstart.py`, `install_v213_tipint.py` + `tipint2.py`, `install_v213_guard3.py` (kaynak `install_guard3_src.lisp`), `install_v213_revmont.py` (`install_revmont_src.lisp`), `push_window213.py`, `verify_prod213.py`, `v213_ab.sh` / `ab_safe213.sh` / `cap_v213.sh`; ölçüm: `dirchange213.py`, `armswing213.py`; `v212_push_posture.py` (kol sönümü eklendi), `pivdrop.py`; harness `v212_run.sh` yeni cvars/avars.
