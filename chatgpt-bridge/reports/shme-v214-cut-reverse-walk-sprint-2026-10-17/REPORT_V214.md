# SHME V2.14 — Kesiş→ters istek zinciri ve kısa yürüyüş→depar itişi (2026-10-17)

Kapsam: V2.13 üretimi üzerine iki somut hareket. (1) Depar sağ kesiş → itiş bitmeden sol istek → fren/destek → ikinci bir başlangıç
olmadan yeni yöne itiş. (2) Yürüyüş → daha kısa, ölçülü itiş → depar. Bileşen bölüm bitiş/yeniden-başlama kusuru kaynağında düzeltildi.
Tüm sayılar gerçek tuşlu PIE koşularından (qa_pie, 30 fps telemetri; `Saved/Codex/SHME_V1_20260925/Evidence/<etiket>.json`), ölçüm
betikleri `Tools/SHME_V213_20261017/dirchange213.py`, `Tools/SHME_V212_20261017/push212.py`, `pushpose212.py`,
`.agents/skills/sphirus-human-motion-engine/scripts/contactslip.py`. Kullanıcı kabulü verilmiş sayılmaz; teknik PASS ≠ görsel kabul.

## 0. Özet (hedef başına)

| Hedef | Sonuç | Kanıt |
|---|---|---|
| 1a Bileşen bölüm bitişi/yeniden başlaması (kaynak düzeltmesi) | **PASS** (teknik) | `cv_RedirectTime` ters istekte aynı tikte 0.00'a döner; `comp episodes 0.00-0.06 c1 0.06-0.65 c2` (önce: c1 bölüm MaxDwell'e kadar sürüyordu, `RedirectEnd 3` tek tik) |
| 1b Kesiş→ters zinciri tek bütün (destek → fren/pivot → itiş duruşu → depar döngüsü), jog döngüsü / ayakta koşu başlangıcı yok | **PASS** (r_cutrev_r / r_cutrev_l, 3 tekrar) / **PARTIAL** (r_cutrev_r2 geç ters istek: tam 180°, hız 60'a düşer → ayakta koşu başlangıcı 0.07 s'den girer) | §2 |
| 2 Yürüyüş→depar: giriş kayması, çıkış kayması, duruş | §3 (giriş kayması için 0.77 s giriş penceresi denemesi; sayılar §3) | §3 |
| TIP ters ayak kayması | §4 | |
| Koruma zinciri (kesiş→S, S→W, bırakma, ikinci yön, eğim, tek ayak, yeniden başlama) | §4 | |

## 1. Kaynak düzeltmesi: BP_SHM_HumanMotionComponent.SHM_UpdateRouting

Ölçülen kusur (V2.12 q1 / V2.13 f partileri): yanal bölüm içindeki ters istekte bileşen `RedirectEnd = 3` (yeni niyet) yazar ama bölüm
sürer (`RedirectTime` sayar, sınıf 1 kalır) ve MaxDwell'e kadar biter — ABP'de V2.13 telafisi (SHM213_RevVel, hız–girdi açısı > 110°)
bu yüzden eklenmişti.

Neden (graf yürütme sırası + saf düğüm yeniden değerlendirmesi): zincir `SetRedirectEnd(pick = END) → SetRedirectDirLatched(lerp alpha =
START) → SetRedirectSpeed0 / Class / Gait / Side / Phase / Time (pick = START) → SetRedirectActive(START or (active and not END))`.
END (`Operator_27`) ve START (`Operator_30`) **saf** ifadeler ve `RedirectDirLatched`'i okurlar; `SetRedirectDirLatched` yeni yönü
yazdığı anda sonraki her tüketici END/START'ı **yeni** yönle yeniden hesaplar → yeni-niyet testi 0° → END false → START false → süre /
sınıf / taraf eski bölümde kalır.

Düzeltme (`Tools/SHME_V214_20261017/install_v214_comp.py`, kaydedildi): END ve START `SetRedirectEnd`'den **önce** iki üyeye
(`SHM14_EpEnd`, `SHM14_EpStart`) kilitlenir; tüm tüketiciler (CallFunction_49/50/52/55/57/58/59/60.bPickA, Operator_28.B, Operator_33.A,
CallFunction_61.A) bu üyeleri okur. Bayrak yok: grafın amaçlanan mantığı. Doğrulama (v213c1, r_cutrev_r): `cv_RedirectEnd 3` ile aynı
tikte `RedirectTime 0.00`, sınıf 2 bölüm başlar.

Sonuç: ABP telafisi üretimde **kapatıldı** (SHM213_RevVel 0, SHM212_RdRev 0; geri dönüş anahtarı olarak kaldı), SHM213_RestartOn 1
(bileşen yeniden başlatmayı artık gerçekten yaptığı için ABP cStart tespiti çalışır).

## 2. Kesiş → ters istek zinciri

### 2.1 İçerik ve yol (içerik yaklaşımı; montaj yeniden denenmedi)

V2.13 kök-hareket montajı başarısız olmuştu (GR aktör yaw'ını yazmayı sürdürüyor → kayma; satıcı klibi 55 cm pelvis; giriş hızı
sıçraması). Bu geçişte montaj **yeniden denenmedi**; neden: aynı entegrasyon hataları (GR yaw yazımı animasyon kapsülü sürerken)
için önce GR tarafında ayrı bir sahiplik değişikliği gerekir, bu da bu görevin kapsamı (iki hareket) dışındadır. İçerik yaklaşımı
yeterli oldu:

- Yeni veri tabanları `/Game/GraceRanger/SHME/Animations/V214/PSD_SHM214_Rev_L/_R` (`build_v214_revdb.py`): frenli pivot
  `A_LR_Run_Pivot_F_B_{L,R}foot` (PIV geçişinde pişirilmiş, pelvis ≥ 78 cm), sahipli kopya `SHM214_Run_Reface_{L,R}_180` (AAMS
  M_Neutral_Run_Reface_Start_F 180; ilk 0.9 s 1.4× uzatıldı; giriş 0–0.35 s) ve `A_LB_Sprint_Fwd`. V1.3.5 geri koşu döngüleri **yok**
  (geri pedal seçimine yol açıyordu).
- Yol (`install_v214_route.py`, SHM213_MontTick yeniden kuruldu): `SHM214_RevTurnMode > 0.5 ∧ RedirectActive ∧ girdi var ∧ kamera-ileri
  ∧ hız > 150 ∧ (bileşen sınıfı > 1.5 ∨ hız–girdi açısı > 100°)` → SHM212_RevTurn, sınıf 2, gait 1 → Update_MotionMatching köprüsü
  SHM212_RouteSRL/SRR = PSD_SHM214_Rev_L/R. Pivot +0.08–0.09 s'de seçilir.
- "Kuyruk" (bölüm bittikten sonra Rev DB'yi tutma, SHM214_TailSpeed) **işe yaramadı**: Reface klibi hiç seçilmedi (GR düşük hızda
  aktörü hızlı döndürür, MM depar ileri / jog'u tercih eder) → üretimde TailSpeed 0 (kapalı).
- İtiş duruşundan giriş (`build_v214_revpush.py` + `install_v214_revpush.py`): pivot sonrası itiş `PSD_SHM212_GaitPush`'tan 1.03 s'de
  (yürüyüş adımı, "ikinci başlangıç" görüntüsü) giriyordu. Yeni DB `PSD_SHM214_RevPush` = yeniden adımlanmış yürüyüş→depar kliplerinin
  kopyaları `SHM214_RevPush_{L,R}foot`, giriş penceresi **1.45–1.65 s** (itiş duruşu, 145→300 cm/s). ABP: `SHM214_RevEndT` (ileri-ters
  kilidinin düştüğü an), `SHM214_PushRevOn` = RevTurnMode ∧ (now − RevEndT < SHM214_PushRevWin 0.8 ∨ itiş sürüyor) → EventGraph
  `SHM211_DB_Push` = DB_RevPush, aksi hâlde DB_GaitPush'a geri. Tuzak: ilk kurulumda `(bind revEnd …)` kilit güncellemesinden sonra
  okunduğu için hiç ateşlemedi — bind saf ifadedir, kullanım yerinde yeniden değerlenir (bileşen hatasının aynısı); `RevEndT` kilit
  güncellemesinden **önce** yazılır.
- `SHM211_PushRdCool` 0.35 → **0.0**: 0.1 s'de bile pivot ile itiş arasında 2–3 kare jog döngüsü kalıyordu.
- Yakalama aşamasında bulunan delik (`install_v214_revpush3.py`): V2.12 itiş yolu, itiş yürüyüş hızının üstünde başladığında
  (`SHM212_PushWalk` false) `SHM211_DB_Push` yerine `SHM212_DB_PushStand`'ı (PSD_RR_Start, ayakta koşu başlangıcı) okur; yan kamera
  yakalaması `v214z_r_cutrev_r_nS_r1`'de pivot → 214 cm/s'de itiş → `A_RR_M_Relaxed_Run_Start_F 0.07` (ayakta poz) görüldü. Düzeltme:
  takas dalı PushRevOn iken `SHM212_DB_PushStand`'ı da RevPush'a çevirir, PushRestore'da yeni üye `SHM214_DB_PushStand0` (PSD_RR_Start)
  ile geri alır. Tuzak: `qa_graph.disconnect()` bir **girdi** pininin tüm bağlarını koparır (ortak birleşim düğümünde diğer dalları da
  kopardı; bellekteki ABP editör yeniden başlatılarak atıldı, kaydedilen varlık etkilenmedi); tek bağ için `B.break_pins`.

### 2.2 Zaman çizelgesi (r_cutrev_r: depar, 3.0 s D, 3.35 s A; `dirchange213.py --tl`, ikinci olay = ters istek)

| Durum | +0.00 | pivot | ara | itiş | depar döngüsü | vmin | pelvis düşüşü (itiş) |
|---|---|---|---|---|---|---|---|
| V2.13 üretim (q0) | Sprint_Turn_R_090 | +0.06 Pivot_F_B (SprintReversal) → +0.34 Pivot_B_F | +0.48 A_CT_Jog_Fwd 0.34 s | +0.82 Walk_to_Sprint **1.03** | +1.81 | 147 | — |
| V2.14 rt2 (c7; kuyruk kapalı, RdCool 0.1) | aynı | +0.08 Pivot_F_B (PSD_SHM214_Rev) | +0.66 Jog 0.09 s + None | +0.81 Walk_to_Sprint **1.03** | +1.85 | 136 | 10–13 cm |
| V2.14 rt3 (d2; RevPush) | aynı | +0.09 Pivot_F_B | +0.67 Jog 0.08 s | +0.81 RevPush **1.47** | +1.82 | 144 | −1.2 / −0.4 (düşüş yok) |
| **V2.14 rt4 (d3; üretim: RdCool 0)** | aynı | +0.09 Pivot_F_B (0.59 s) | **yok** | **+0.68 RevPush 1.47** | +1.83 | 142 | — |
| rt4 ayna (r_cutrev_l) | Sprint_Turn_L_090 | +0.09 Pivot_F_B_Rfoot | yok | +0.68 RevPush_Rfoot 1.47 | +1.80 | 144 | — |

Bileşen sınıfı: ters istek anındaki hız–istek açısı 100–120° arasında kaldığında bileşen bölümü **yanal (c1)** olarak yeniden başlatır
(ReversalClassAngle 120; e1 r1: `comp 0.00-0.64 c1`), 120° üzerinde ters (c2; e1 r2: `0.06-0.64 c2`). ABP yolu bu yüzden bileşen
sınıfını **veya** kendi hız–girdi açısını (> 100°) kullanır; her iki durumda pivot +0.09, itiş duruşu +0.67.

Girdi gecikmesi (A basımı → MM pivot): 0.08–0.09 s. Fiziksel tamamlanma (A basımı → depar döngüsü 416 cm/s): 1.80–1.83 s;
yön 90° dönüşü (`heading90`) 0.80–0.82 s; `re90` 1.11–1.15 s. |a|max 1400–1450 cm/s² (kesiş kapasitesi 450 yanal + fren).

Geç ters istek (r_cutrev_r2, 3.6 s'de A; o anda gövde ~90° dönmüş, istek gerçek 180°): V2.13 pivot → jog pivot → jog 0.3 s (75–95
cm/s) → yürüyüş-itişi 1.03; V2.14 (e1, PushStand takası öncesi) pivot (0.57 s, vmin 60) → `A_RR_M_Relaxed_Run_Start_F_Rfoot` **0.07**
(ayakta koşu başlangıcı) → +1.78 depar — itiş yolu, itiş yürüyüş hızının üstünde/altında başladığına göre PushStand DB'sine gidiyordu.
`install_v214_revpush3.py` (PushStand takası) sonrası son yakalama `v214z_r_cutrev_r2_nD_r1`: pivot (0.64 s, vmin 87) → **RevPush 1.47
+0.74 (133 cm/s)** → +1.76 depar: ayakta başlangıç yok. Kalan görsel risk: 133 cm/s'de 250 cm/s'lik itiş pozu (stride warping telafi
eder; kabul sende).

Erken ters istek (r_cutrev_r0, 3.15 s): §4 koruma partisinde.

### 2.3 Kesiş→S geri pedal korunur (k_cut_back)
§4.

## 3. Yürüyüş → depar itişi (p_w2s: 2.0 s'de yürüyüş, 5.0 s'de Shift)

### 3.1 Yeniden adımlama (içerik)
`v212_push_posture.py` `restep` (yeni, V2.14): kök yolu / ayaklar / pelvis XY ölçeklenir ve bacaklar yeniden çözülür. Uygulanan S1b:
`[[0,0.70],[1.45,0.70],[1.75,0.80],[2.3,0.90],[2.8,1.0]]`, pelvis tabanı 92 / dip_keep 0.1, baz eğim 12 / keep 0.15, arm_damp 0.6 →
`SHM212_Walk_to_Sprint_{L,R}foot` (kontrol noktası `checkpoint/pre_restep/`). Klip: yürüyüş 145 cm/s, 1.45 s'den 2.0 s'ye 145→502;
dizler v137 leg_guard. Sonuç (c7, q0 ile): çıkış→döngü kayması 23–27 → **2.7–3.8 cm**; gövde eğimi tepe 30°; pelvis düşüşü 6–8 cm;
kollar 56 / 42 cm. Giriş kayması 9.4–12.3 → 7.1–10.3 cm (5 tekrar; **yetersiz**, tekrarlar arası varyans ±1.5 cm).

### 3.2 Giriş kaymasının nedeni (kare analizi, c7 r2 5.17–5.62 s)
Shift anında yürüyüş döngüsü: sol ayak topu pelvisin altında (+1.9 cm ileri, temasta), sağ ayak sallanmada (+23 cm). Klip 1.03 s'de
ise sol top **−39 cm / 9 cm yukarıda** (parmak kalkışı bitmiş), sağ top +33 cm basmış (topuk vuruşu). Geçiş harmanı sol ayağı temasta
iken +1.9 → −10 cm sürükler (dünya hızı 38–117 cm/s) = kayma. Klibin yürüyüş pozuyla eşleşen anı **0.767 s** (`probe_entry.py`: sol top
−0.1 cm / z 0.9, sağ +31 cm / z 4.6). V2.13'ün 1.13 s denemesinin kaymayı artırması bununla tutarlı (daha geç = daha büyük uyumsuzluk).

### 3.3 Erken giriş penceresi denemeleri (başarısız; üretim 1.01–1.65'te kaldı)
Engel 1: V2.12 kurucusu klibin ilk 1.01 s'sini **veri tabanından dışlamıştı** (`AnimNotifyState_PoseSearchExcludeFromDatabase 0–1.01`),
BlockTransition penceresi 0.77'ye çekilse bile (d4) giriş 1.03'te kaldı. `push_exclude214.py` dışlamayı 0–0.77'ye çekti.
Engel 2: MM pozu değil yörüngeyi tercih eder — **izin verilen en geç pozu** seçer:

| Pencere (giriş / dışlama) | Giriş zamanı (klip) | Giriş kayması (cm) | Not |
|---|---|---|---|
| 1.01–1.65 / 0–1.01 (V2.13 = üretim) | 1.03 | 7.1, 9.1, 10.2, 10.3, 4.1 (p_w2s ×5); erken (sağ ayak) 9.2, 8.1 | — |
| 0.77–1.65 / 0–0.77 (d5) | 0.97–1.03 | 3.9, 7.7, 8.2; erken 9.8 | aynı poz, aynı kayma |
| 0.77–0.90 / 0–0.77 (d6) | 0.87 | 4.9, 9.6; erken **17.5** | geç duruş pozu, sağ-ayak durumunda çok kötü |
| 0.77–0.80 / 0–0.77 (d7) | — | 6.3, 13.4; erken 8.9 | MM yürüyüş kliplerini bırakıp **Run_to_Sprint 0.57**'ye atlar (eğim 20°) |

Sonuç: giriş kayması yürüyüş fazı ile tek giriş pozu arasındaki faz farkıdır (tekrarlar arası 4–10 cm, aynı bayraklarla); pencere
kaydırma çözmez. Çözüm adayı (bu geçişte yok): faz başına birden çok giriş pozu (şema yörünge ağırlığı / sürekli-poz yanlılığı ile
birlikte) veya giriş anında ayak kilidi. Üretim pencereye geri döndü (`req/pw_revert.py`: 1.01–1.65, dışlama 0–1.01; kontrol noktaları
`checkpoint/pre_window077/`, `pre_exclude077/`).

### 3.4 Sayılar (üretim durumu: yeniden adımlanmış klipler + 1.01–1.65; p_w2s 5.0 s'de Shift)
- Girdi gecikmesi: Shift → itiş klibi girişi **0.33–0.37 s** (`SHM211_Push` ivme tespiti); hız 200 cm/s 0.53–0.54 s, 300 0.86 s, 416
  1.24–1.28 s, 480 1.44–1.49 s (kapsül ivmesi 300 cm/s², hareket modeli M1 — değişmedi).
- Fiziksel tamamlanma: depar döngüsüne giriş Shift + **1.47–1.51 s** (klip 1.93–2.05 s'de; önce 1.51).
- Giriş kayması (±0.1 s, temasta): **4–10 cm** (n = 7; V2.13 9.4–12.3) → **PARTIAL** (kabul engeli eşiği 10–12 cm'nin altında ama
  giderilmedi). Sağ-ayak destekli giriş (p_w2s_early): 8.1–9.8 cm (V2.13 10.9).
- Çıkış kayması (klip → depar döngüsü): **1.8–3.8 cm** (V2.13 23–27 cm; "contact air" durumlarında 0) → PASS.
- Gövde eğimi tepe 28.9–30.0° (V2.13 30.5–30.8); pelvis düşüşü 5.8–7.8 cm (V2.13 ~8); kollar el ileri 53–57 / 38–44 cm (V2.13 56–59).
- Pelvis/gövde ayaklardan: re-step'te bacaklar yeni ayak yerlerine yeniden çözülür (leg_guard), pelvis tabanı 92 cm (klipte min 80.5–81).
- Kök/kapsül: klip 1.45 s'ye kadar 144 cm/s (yürüyüş), kapsül Shift'ten 0.86 s sonra 300 → klip pozu kapsülden geri kalır (stride
  warping telafi eder; görsel kabul sende).

## 4. Koruma ve tekrarlar (e1 partisi, kayıtlı V2.14 üretimi = `v214_ab.sh` base; karşılaştırma V2.13 q0)

| Senaryo | V2.13 (q0) | V2.14 (e1) | Durum |
|---|---|---|---|
| r_cutrev_r ×2 / r_cutrev_l | pivot → jog 0.34 s → yürüyüş itişi 1.03 → döngü +1.81 | pivot +0.09 → **RevPush 1.47 +0.67/0.68** → döngü +1.81/1.85/1.88; vmin 127–142; \|a\|max 889–1406 | PASS (tekrarlar tutarlı) |
| r_cutrev_r0 (0.15 s sonra ters) | — | gövde henüz dönmemiş → istek 90° yanal (ters değil): kavis klibi, 0.09 s jog pozu, +0.79 depar; vmin 228; yanlış pivot yok | PASS (yanlış tetik yok) |
| r_cutrev_r2 (0.6 s sonra, gerçek 180°) | pivot → jog pivot → jog 0.3 s → yürüyüş itişi | e1 (takas öncesi): pivot → `A_RR_M_Relaxed_Run_Start_F` 0.07; **son yakalama (takas sonrası)**: pivot (0.64 s, vmin 87) → RevPush 1.47 +0.74 → +1.76 depar | PASS (ayakta başlangıç yok; düşük hızda itiş pozu görsel risk) |
| k_cut_back (kesiş → S) | jog pivot → geri koşu | +0.09 A_CP2_Jog_Fwd_Pivot (pişirilmiş) → +0.81 A_RB_Run_Rear; vmin 105; geri ≤ tempolu | PASS (değişmedi) |
| k_ws_clean / k_ws_ovl40 / p_revpush (geri tuşlar) | — | ters dönüş +0.75–0.77 s; geri hız ≤ 300; geri giderken ileri koşu klibi **yok**; p_revpush S→W pivot → RR_Start | PASS (değişmedi) |
| chain_scutrel (kesişte tuş bırakma) | kesiş → duruş (vmin 0, +1.07) | aynı (+1.06 / +1.08) | PASS (değişmedi) |
| chain_sscut (ikinci yön değişimi) | 4 olay; 3. olayda pelvis 84.7→68 (DirectionalSafe WalkToSprint 1.03 + kesiş) | aynı (86.3→69); zaman çizelgesi aynı | PASS (değişmedi) — derin çömelme **önceden var**, açık |
| t_tiprev (yerinde dönüş → ters) | montaj 0.34 s kesilir, ters 1.83 s | 0.34 / 1.81 s (aynı) | PASS (değişmedi) |
| **TIP ters ayak kayması** (t_tiprev2: 90 → 180) | — | kesilen dönüşte basılı sağ ayak **16.8 cm orta-duruş kayması + 11.8 cm kalkış** (0.61 s, `yaw_90_1+mv_stop`); t_tiprev'de sağ ayak 13.8 cm / 3.1 s sürüklenme | **FAIL (ele alınmadı)** — bu geçişte içerik/entegrasyon değişikliği yapılmadı; neden: montaj 0.12 s'de durdurulurken aktör yaw'ı dönmeye devam eder ve idle'a harman ayak kilidi olmadan gider. Öneri: montaj durdurma anında FootPlacement kilidi / duruş fazına kadar bekleme |

| p_w2s ×2, p_w2s_early (üretim) | giriş 9.4–12.3 / çıkış 23–27 | giriş **6.4 / 9.0 / 8.3 (sağ ayak)**, çıkış **2.1 / 3.1 / 4.5**; eğim 29.8; pelvis düşüşü 7.4 | PARTIAL (giriş), PASS (çıkış) |
| p_tapretrig (dururken Shift+W) | RR_Start 0.38 | RR_Start 0.33, eğim 26.9→30.6, çıkış 3.95 s | PASS (değişmedi) |
| p_j2s (tempolu → Shift) | itişsiz, hız 480'e +4.1 s | aynı (0 itiş bölümü; tasarım gereği) | PASS (değişmedi) |
| a_restart ×2 (idle → yürü → dur → yürü) | Dl max 13.7 / p99 7.2, n>30 0 | Dl max 18.7 / 14.2, p99 7.3 / 7.8, **n>30 0**; pop 0 | PASS (tekrar varyansı, eşik aşımı yok) |
| chain_slope_r ×2 (eğimde dur → dön → başla) | Dl max 6.7 / p99 6.5 | Dl max 8.0 / 10.6, p99 6.8 / 9.4, n>30 0; pop 0 / 1 (26) | PASS |
| legs_lfoot_walk (tek ayak yükseltide) | Dl max 8.8 | Dl max 8.6, p99 7.2, n>30 0 | PASS (değişmedi) |
| r_curve / r_wcurve / chain_wawd / wdiag (yanlış tetik) | — | `SHM212_RevTurn` 0 kare, `SHM214_PushRevOn` 0 kare, V2.14 DB'si hiç seçilmedi; kavis/köşe zaman çizelgeleri V2.13 ile aynı | PASS (yanlış tetik yok) |
| Pop sayacı (>25 m/s², 27 koşu) | — | 0–8 / koşu, en kötü 54 (k_cut_back, klip içi); p_revpush 195 (V2.13'te de var: S → W pivot ilk karesi) | değişmedi |
| Uyuyan aday taraması (`scan_dormant214.py v214e1_`) | — | 27/27 OK: istek bayrakları = üretim, montaj/kuyruk 0 kare, emekli DB yok | PASS |

## 5. Üretim değerleri, değişen dosyalar, geri dönüş (`verify_prod214.txt`, `req/promote214.py`)

ABP_GR_MotionMatchingBase (kayıtlı sınıf varsayılanları): SHM214_RevTurnMode **1**, SHM214_PushRevWin **0.8**, SHM214_TailSpeed **0**
(kuyruk kapalı), SHM214_TailMax 1.4, SHM211_PushRdCool **0.0** (önce 0.35), SHM213_RestartOn **1** (önce 0), SHM213_RevVel **0** (önce 1),
SHM212_RdRev **0** (önce 1), SHM213_RevMont 0, SHM212_RevTurnMode 0, SHM212_RdBreak 0; SHM211_DB_Push PSD_SHM212_GaitPush (değişmedi),
SHM212_DB_CutRevL/R → PSD_SHM214_Rev_L/R, SHM214_DB_RevPush PSD_SHM214_RevPush, SHM214_DB_GaitPush PSD_SHM212_GaitPush,
SHM214_DB_PushStand0 PSD_RR_Start (SHM212_DB_PushStand değişmedi). Uyuyan adaylar
denetimi (`dormant_off`): RevVel ✓ RdRev ✓ RevMont ✓ Tail ✓ RevTurnMode(V2.12) ✓. DA_GR_LocomotionBehavior: V2.13 M1 değerleri
**değişmedi** (dosya özeti `same`). DA_SHM_Response_Default değişmedi. BP_GR_Player / BP_GR_MotionProfile / BP_PBI_Player değişmedi.

Değişen ikili dosyalar (hepsi editör üzerinden):
- `Content/GraceRanger/SHME/BP_SHM_HumanMotionComponent.uasset` — SHM_UpdateRouting END/START kilidi (SHM14_EpEnd/EpStart).
- `…/ABP_GR_MotionMatchingBase.uasset` + child `ABP_GR_MotionMatching.uasset` — SHM213_MontTick yeniden kuruldu (yol + kuyruk + itiş
  duruşu girişi), EventGraph DB_Push dalı, yeni üyeler SHM214_*, varsayılanlar.
- `Content/GraceRanger/SHME/Animations/V214/` (yeni): PSD_SHM214_Rev_L/R, PSD_SHM214_RevPush, SHM214_Run_Reface_L/R_180,
  SHM214_RevPush_L/Rfoot.
- `…/V212/SHM212_Walk_to_Sprint_L/Rfoot.uasset` — yeniden adımlama (S1b) + pencere 1.01–1.65 (giriş sonu 1.45 → 1.65).
- `…/Reversal/A_LR_Run_Pivot_F_B_L/Rfoot.uasset`, `…/LocomotionBehavior/A_LB_Sprint_Fwd.uasset` — ek BranchIn izi (SHME214_Rev_L/_R)
  → yeni veri tabanlarına katılım (içerik değişmedi).

Geri dönüş: `Saved/Codex/SHME_V214_20261017/checkpoint/baseline_v213/` (ABP'ler, bileşen, pawn, profil, DA'lar, klipler),
`pre_revdb/` (pivot + Sprint_Fwd izler öncesi), `pre_restep/` (yürüyüş→depar klipleri), `pre_window077/`, `pre_exclude077/`. Bayrak
geri dönüşü (içerik kalır): RevTurnMode 0, PushRevWin 0, RdRev 1, RevVel 1, RestartOn 0, PushRdCool 0.35 (`vars_v214.sh` `rb`).
Veri tabanı denetimi: hiçbir aktif DB'de `/Rollbacks/` veya None girdi yok (yeniden açma + yeniden indeksleme sonrası
`verify_prod214.txt`).

## 6. Yakalamalar ve medya (`cap_v214.sh z` → `v214z_*`, `media214.sh`, `pub/`)
Kayıtlı **son üretim** üzerinde gerçek zamanlı 30 fps mcap (QA kil test görünümü, yalnız PIE; kare kesilmedi/düzenlenmedi). Kameralar:
yan (S), ön-sağ çapraz (D), oyun kamerası (G). ÖNCE = V2.13 son yakalamaları (`v213z_*`), SONRA = `v214z_*`. Ters istek ve itiş
sahneleri gerçek hız + 1/3 hız AVI. Otomatik denetim: `scan_dormant214.py v214z_` (istek bayrakları = `verify_prod214.txt`, montaj/kuyruk
0 kare, emekli DB yok) — sonucu §6.1. Yeniden açılan editörde (bellek koruması yeniden başlatması sonrası) `verify_prod214.py`
yeniden koşuldu: aktif DB'lerde `/Rollbacks/` veya None girdi yok (§6.1).

### 6.1 Denetim çıktıları
- `scan_dormant_v214z.txt`: **28/28 OK, SCAN_OK** (her yakalamanın istek bayrakları = üretim; `av_SHM213_MontOn` / `av_SHM214_TailOn` 0
  kare; emekli DB yok; V2.14 DB'leri yalnız kesiş→ters sahnelerinde).
- `verify_prod214.txt` (PushStand takası kurulumu + yeniden açılmış editörde): tüm aktif DB'lerde `/Rollbacks/` 0, None 0; dormant_off
  hepsi ✓; dosya özetleri V2.13 taban noktasına göre: bileşen / ABP'ler `changed`, pawn / profil / DA'lar `same`.
- Kesiş→ters son yakalamaları (`dirchange213.py --tl`): oyun kamerası pivot +0.10 → RevPush 1.47 +0.67 → döngü +1.83; yan kamera (girdi
  dünya −175°, gerçek 180°) pivot +0.11 → 2–3 kare Sprint_Fwd/jog → RevPush +0.84 → döngü +1.73; çapraz kamera (girdi 135°) kavis +0.20 →
  RevPush +0.67 → +1.81; geç ters (r2) pivot → RevPush +0.74 → +1.76. Not: sabit yan/çapraz kameralarda tuş yönü dünyaya farklı eşlenir
  (A/B oyun kamerası senaryosundan farklı açılar); oyun kamerası yakalaması A/B zinciriyle aynıdır.
- İlk yakalama partisi bellek koruması yeniden başlatmasından sonra telemetriyi kaybetti (`cap_run_notelemetry.out`, rows 0); yakalama
  betiği grup başına canlı günlüğü seçer hâle getirildi ve tüm set yeniden alındı (rows > 0, 28/28).

### 6.2 Kontak sayfaları (`pub/img`)
- `cut_reverse_before_after.jpg` — r_cutrev_r yan kamera: A basımı +0.1 / +0.4 / +0.7 / +1.0 / +1.4 / +1.8 s (V2.13 üstte, V2.14 altta).
- `push_before_after.jpg` — p_w2s yan kamera: Shift +0.3 / +0.5 / +0.7 / +0.9 / +1.2 / +1.5 s.
- `cutrev_late_before_after.jpg` — r_cutrev_r2 çapraz: geç ters istek (PARTIAL durumu).

## 7. Beceri / bellek güncellemeleri
- `.agents/skills/sphirus-human-motion-engine/references/architecture.md` — "V2.14 cut -> reverse chain + walk -> sprint stepping"
  bölümü (bileşen saf-yeniden-değerlendirme düzeltmesi ve DSL `bind` tuzağı, Rev/RevPush veri tabanları ve yol, kuyruk başarısızlığı,
  re-step, giriş kayması sahibi, ExcludeFromDatabase tuzağı, MM'in en geç pozu seçmesi).
- `.agents/skills/sphirus-human-motion-engine/references/validation.md` — V2.14 araçları (`verify_prod214.py`, `push_exclude214.py`,
  `build_v214_*`, `probe_entry.py`, `scan_dormant214.py`), uyarılı derleme / var olmayan DSL değişkeni tuzağı.
- `Tools/SkillSystem/sync_claude_skills.py` çalıştırıldı (uyarı yok).
- Bellek: `shme-v214-cut-reverse-walk-sprint.md` (yalnız doğrulanmış yöntemler ve tuzaklar).
- Yalnız doğrulanmış yöntemler yazıldı; denenip reddedilenler (kuyruk, erken giriş pencereleri, montaj) "başarısız" olarak işaretli.
