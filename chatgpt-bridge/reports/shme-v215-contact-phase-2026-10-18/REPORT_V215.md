# SHME V2.15 — Geçişlerde ayak teması ve hız uyumu (2026-10-18)

Kapsam: V2.14 üretimi üzerine üç uygulama hedefi — (1) yürüyüş→depar girişinde yanlış destek evresinden gelen ayak kayması,
(2) düşük hız / geç ters istekte fren→itiş bağlantısı (ikinci kalkış ve araya giren pozlar olmadan), (3) yerinde dönüş tersine
çevrildiğinde basılı ayağın sürüklenmesi; ayrıca derin çömelme analizi, test kamerasının kontrol yönünü değiştirmemesi ve ölçüm
tutarlılığı. Motor UE 5.8.1 (Blueprint-only), üretim haritası/anatomi/kıyafet/kadraj değişmedi.

Tüm sayılar gerçek tuşlu PIE koşularından (qa_pie, ~30 fps telemetri; `Saved/Codex/SHME_V1_20260925/Evidence/<etiket>.json`).
**Teknik sonuç ≠ görsel kabul; kullanıcı kabulü verilmiş sayılmadı.**

## 0. Özet

| Hedef | Sonuç | Üretimde |
|---|---|---|
| 1 Yürüyüş→depar girişi destek evresine göre | **PARTIAL** — seçim artık destek ayağı/evresine göre (sol ayak basılıyken sol klibin geç duruşu, sağ ayak basılıyken sağ duruşun başı); giriş sürüklenmesi ort. 8.7 → 7.2 cm (en kötü 14.7 → 9.2), sol ayak orta-duruş girişi hâlâ geç duruş pozuna giriyor | açık |
| 2 Fren→itiş bağlantısı, düşük hız/geç ters | **PARTIAL** — araya giren tempolu/ileri depar pozu ve ayakta kalkış kalktı (9/9 koşu: pivot → itiş duruşu → döngü); erken ters istekte yüksek hızda itiş duruşuna giriş engellendi; **pivot girişindeki ayak süpürmesi (22–138 cm, V2.14: 3–123) çözülmedi** | açık (bağlantı) / kapalı (adaylar) |
| 3 Yerinde ters dönüşte ayak sürüklenmesi | **PARTIAL** — dönüş penceresinde basılı ayak kayması ≈0 (V2.14 4.4 → 0.1–3.4 cm); 180° ters dönüşte zemine sürtünen adım (top 1.5–4 cm'de hareket) 43 → 9–30 cm; 90° tersinde 44 → 39 cm (az değişti); montaj başlangıcında tek karelik süpürme duruyor | açık |
| 4 Derin çömelme (ardışık yön değişimi) | **FAIL (neden ayrıldı, düzeltilemedi)** — kaynak: depar kesiş klibinin kendisi (SHM210_Sprint_Turn_*_090, pelvis 87 → 66–71 cm); iki bake yöntemi (pelvis tabanı; ön ayak kısaltma + taban) pelvisi kaldıramadı | değişmedi |
| 5 Test kamerası kontrol yönünü değiştirmesin | **Açıklandı** — kamera yönü değiştirmiyordu; V2.14'teki fark etiket hatası + seçim değişkenliği; araç düzeltildi (§5) | — |
| 6 Ölçüm çelişkisi | **Açıklandı** — iki farklı tanım (§6) | — |

## 1. Yürüyüş → depar girişi (Hedef 1)

### 1.1 Doğrulanan neden
Yeni temas aracı `Tools/SHME_V215_20261017/contact215.py` (tanım §6): Shift anında yürüyüş döngüsünde sol ayak basılı **orta**
(fwd −4…+2 cm) veya **geç** duruşta (−8…−22), sağ ayak önde salınımda. V2.14'te MM her zaman `SHM212_Walk_to_Sprint_Lfoot` 1.03 s'ye
giriyordu = klibin **sağ topuk vuruşu**, sol ayak 39 cm geride ve havada. Harman, yerdeki sol ayağı 2–3 karede 5–15 cm sürüklüyordu.
Sağ ayak basılıyken de aynı karede (1.00) giriyordu. Sağ/sol etiketi değil, evre uyuşmuyordu.

Seçim neden geç kareye gidiyordu: (a) V2.12 kurucusu 0–1.01 s'yi veri tabanından dışlamıştı; (b) aynı veri tabanında
`Run_to_Sprint` klipleri vardı (dar pencerede MM oraya kaçtı, V2.14 d7); (c) yörünge maliyeti (klip 1.45 s'den sonra hızlanır, kapsül
Shift anında) MM'i izin verilen **en geç** kareye çekiyordu.

### 1.2 Uygulama (`build_v215_walkpush.py`)
- **Bu geçişe özel seçim düzeni:** `PSS_SHM215_WalkPush` = PSS_Default kopyası, yörünge kanalı ağırlığı 1.0 → **0.35** (poz kanalları
  aynı). Bütün MM şeması değişmedi; yalnız yürüyüş itişi bu şemayı kullanır.
- `PSD_SHM215_WalkPush`: yalnız iki yürüyüş→depar klibi (BranchIn yeniden hedeflendi; `Run_to_Sprint` GaitPush'ta kaldı).
- Giriş penceresi **0.70–1.25 s** (Lfoot klibi: sol duruşun ortası → sağ duruşun ortası; Rfoot aynası), dışlama 0–0.70.
- ABP: `SHM211_DB_Push` ve ters-itiş takasının geri dönüş hedefi `SHM214_DB_GaitPush` → `PSD_SHM215_WalkPush`.
- Yörünge ağırlığı 0.12 denendi: daha iyi değil (ort. 5.7 cm) → 0.35'te kaldı.

### 1.3 Önce / sonra (aynı tanım: giriş karesi ±0.1/0.25 s, basılı top; "drag" = yerde ama >60 cm/s)

| Durum | Koşular | Seçilen kare | Basılı ayak sürüklenmesi (cm) |
|---|---|---|---|
| V2.13/V2.14 (q0, c7, d3, e1) | 9 | hep 1.00–1.03 | 4.8, 14.7, 7.3, 5.0, 13.3, 8.7, 8.2, 8.4, 8.0 (ort. 8.7) |
| V2.15 üretim (e2) | 6 | sol-orta/geç → **0.93** (sol geç duruş); sağ-erken → **1.10** (sağ erken duruş) | 7.5, 4.8, 7.5, 6.6, 7.3, 9.2 (ort. 7.2) |
| V2.15 aday g1 (aynı içerik) | 5 | 0.93–1.10 | 2.2, 4.5, 8.0, 4.4, 4.6 |

- Girdi algılama → itiş klibi: **0.33–0.36 s** (V2.14 0.34–0.45); hız 200 / 300 / 416 / 480 cm/s: 0.52–0.54 / 0.85–0.92 / 1.25–1.27 /
  1.46–1.48 s (V2.14 ile aynı; kapsül ivmesi M1, değişmedi).
- Depar döngüsüne çıkış (ilk depar basışının iniş kayması, contactslip): 1.5–4.3 cm (V2.14 2.1–3.5).
- Gövde eğimi tepe 29.4–29.5°, pelvis düşüşü 7.3–8.7 cm (V2.14 ile aynı).
- **Kalan kusur:** sol ayak **orta** duruştayken MM klibin orta-duruş karelerini (0.77–0.88) yine seçmiyor; 0.93 (geç duruş) seçiyor →
  bu durumda 7.5 cm sürüklenme. Klip yürüme hızında (144) 0.5 s daha adım atarken kapsül hızlanıyor (stride warping telafi ediyor; görsel
  kabul sende). Çözüm adayı (yapılmadı): giriş anından itibaren hızlanan, faz başına kısa bir bağlantı içeriği.

## 2. Fren → itiş bağlantısı (Hedef 2)

### 2.1 Doğrulanan nedenler (son-poz zinciri, `dirchange213.py --tl`)
1. **Araya giren ileri depar pozu:** V2.14 tersine-dönüş veri tabanında `A_LB_Sprint_Fwd` vardı; pivottan sonra 0.28 s boyunca
   139 cm/s'de depar döngüsü seçiliyordu (v215f2 base). → `dbremove215.py` ile çıkarıldı.
2. **2–3 kare tempolu poz:** bölüm bittiğinde itiş tespitçisi (V2.11, ivme eşiği) 2–3 tik sonra tetikleniyordu, MM arada tempolu döngüye
   düşüyordu. → `SHM215_LinkOn`: bölüm bitişi tikinde itiş başlar (`install_v215_pushlink.py`).
3. **Geç ters istekte ayakta kalkış:** V2.14 son düzeltmesiyle (PushStand takası) zaten RevPush'a giriyordu; 100–133 cm/s'de 145 cm/s'lik
   itiş duruşu hız olarak uyumlu. `PSD_SHM215_RevPushLow` (koşu başlangıcı 0.17–0.27 s) yalnız gerçekten durmuşken (<60 cm/s) devreye girer.
4. **Erken ters istekte yüksek hızda itiş duruşu:** bağlantı 294 cm/s'de tetiklenip 145 cm/s'lik pozu seçti (e2 r0) → bağlantı yalnız
   **<230 cm/s** (`SHM215_LinkMaxSpeed`).
5. **Pivot girişinde ayak süpürmesi (çözülmedi):** pivot klibinin kök yönü sabit (geri koşuya geçiyor), GR aktörü yeni yöne döndürüyor;
   ve kesiş klibinin pozundan pivot pozuna harman, basılı ayağı zeminde 50–100 cm/s üstünde taşıyor (bir koşuda ayak 8 cm zeminin altından
   68 cm kaydı). Denenen ve **üretime alınmayan** adaylar: hız çizgisinde fren (`GR215_RevBrakeDecel`: vmin 135 → 77–81 ama sürüklenme
   aynı), yön tutma (`GR215_RevYawHold`), destek ayağına göre pivot seçimi (`SHM215_PivFoot`: bileşenin temas sinyali depar uçuş
   evresinde iki ayak için de false, seçim güvenilmez).
6. **Açı eşikleri:** bileşen >120°'yi ters (`ReversalClassAngle`), ABP ileri-ters içerik yolu hız–niyet açısı >100°'yi ters sayar.
   100–120° arası bileşen için yanal, ABP için ters: hareket (GR) bileşen sınıfına bağlı değil, içerik yolu ABP'den karar verir; bu
   aralıkta çelişkili hız tepkisi ölçülmedi (r_cutrev: 125° isteklerin hepsi pivot→itiş). Ortaklaştırma (bileşen eşiğini 100°'ye çekmek)
   tüm ters dönüşleri etkileyeceği için bu geçişte yapılmadı — açık madde.

### 2.2 Son zincir (üretim, e2; A basımından itibaren)
| Senaryo | Zincir | vmin | itiş girişi | döngü |
|---|---|---|---|---|
| r_cutrev_r ×3 | kesiş → pivot 0.80 (+0.08–0.10) → RevPush 1.47 | 140–146 | +0.66–0.68 | +1.82–1.83 |
| r_cutrev_l ×3 | aynı (ayna) | 130–145 | +0.68–0.69 | +1.78–1.86 |
| r_cutrev_r2 ×2 (geç, gerçek 180°) | pivot → RevPush 1.47 @100–105 cm/s | 69–76 | +0.68–0.70 | +1.71–1.73 |
| r_cutrev_r0 (erken) | (e2'de bağlantı hız sınırı öncesi) RevPush @294 — §2.1/4 ile sınırlandı | 223 | +0.08 | +1.50 |

Araya giren tempolu/ileri depar karesi: **0/9** (V2.14: 2–3 kare tempolu veya 0.28 s depar). Ayakta kalkış: 0/9.

### 2.3 Pivot girişi süpürmesi (aynı tanım, giriş ±0.05/0.6 s, iki ayak toplam "drag")
V2.14 e1: 123, 68, 6, 3 cm · V2.15 e2: 125, 138, 48, 68, 28, 22, 58, 70 cm → **iyileşme yok**, tekrarlar arası çok değişken.

## 3. Yerinde ters dönüş (Hedef 3)

### 3.1 Doğrulanan neden (t_tiprev2: 90° sola, 0.7 s sonra 180° sağa)
- Kesilen montaj 0.12 s'de söner, 0.17–0.2 s idle, sonra 180° montaj başlar; aktör kök hareketiyle **ilk 0.04 s'de 28°** döner, harman
  ağırlığı düşükken idle pozu aktörle birlikte döner → basılı sağ top 6.6 cm süpürülür (ayak kilidi o anda 0.75–0.80'e düşmüştü).
- Dönüş kliplerinin (PSD_SHM_TurnInPlace, proje sahipli) basan ayağı **zemine sürterek** gidiyor: 180_R sağ ayak 111 cm, top en fazla
  5.7 cm yukarıda → çalışma zamanında "sürüklenen ayak" gibi okunuyor.
- Kalan dönüşü iki kez uygulama yok: aktör yaw'ını montaj kök hareketi yazıyor, GR montaj süresince yazmıyor (ölçüm: aktör −90 → +90
  tam 180°, taşma yok).

### 3.2 Uygulama
- `tip_clearance215.py`: 8 dönüş klibinde her ayak için yol parçaları ayrıldı — **pivot** (topuk veya top etrafında dönüş, bir uç <8 cm
  yol: dokunulmadı) / **adım** (iki uç da yol alıyor): ayak yumuşak bir tümsekle (sin^1.5) en az 3, en fazla 8 cm yükseltildi (klibin
  kendi kaldırması düşüldü), bacaklar yeniden çözüldü (leg_guard). XY hatası 0.
- `SHM215_TipLock` (`install_v215_tiplock.py`): dururken (|v|<30) ve beden dönerken (>20°/s) ayak kilidi ilk dönüş karesinde 1 —
  sönmüş kilidin yükselme gecikmesi kalktı.

### 3.3 Önce / sonra (dönüş penceresi 3.3–5.2 s; slip = yerde ve yavaş, drag = yerde ve hızlı, roll = 1.5–4 cm'de ve hızlı)
| Senaryo | V2.14 (e1) | V2.15 üretim (e2 ×3) |
|---|---|---|
| t_tiprev2 sol slip / sağ roll | 4.4 / 42.8 | 0.1, 3.4, 0.1 / 30.4, 24.7, 8.8 |
| t_tiprev (90 → geri) sağ roll | 43.9 | 39.4, 39.2, 40.1 |
| basılı ayak drag (iki senaryo) | 0 | 0 |

t_tip180_early (yürürken dur + 180) e2'de sol 29 / sağ 14 cm drag (durma evresinde) — bu senaryo yürüyüş durmasıyla karışık, açık.
Kalan: montaj başlangıcında tek karelik süpürme (~15 cm, 0.05 s), 90° tersinde alçak adım.

## 4. Derin çömelme (Madde 4)
- chain_sscut ve r_cutrev'deki pelvis 66–71 cm: seçilen klip `SHM210_Sprint_Turn_{L,R}_090_{L,R}foot` (V2.10 sahipli depar kesişi),
  klip zamanı 0.70–0.93, klibin **kendi** pelvisi 87 → 66.2–70.8 cm; doğru aileden, doğru pencereden giriliyor; çalışma zamanı pelvisi
  klibi 2 cm içinde izliyor (üst üste düzeltme yok).
- Denenen: (a) pelvis tabanı 80 (`v212_push_posture.py`): min 66.8 → 68.4 cm (bacak erişim sınırı); (b) frenleyen ön ayağı 12 cm kısaltma
  + taban 77 (`cut_crouch215.py`, PIV yöntemi): değişmedi (66.2 → 66.2), ayak hatası 0.7–7.8 cm → **yazılmadı**. Kesişteki yanal
  açılım (ayaklar yana 50 cm) ileri-geri kısaltmayla çözülmüyor. Sonuç: FAIL, içerik yeniden yazımı gerekiyor (yan adım genişliği).

## 5. Test kamerası
**Doğrulanan neden: V2.14 raporundaki "yan kamera tuşların yönünü değiştirdi" yorumu bir ölçüm etiketi hatasıydı.** `dirchange213.py`
istek yönünü (`world`) **görüntülenen** kameranın yaw'ına göre hesaplıyordu; gözlemci (yan/çapraz) çekimde bu gözlemcinin yaw'ı
(−85 / −135) olduğu için "world −175 / +134" yazdı. Oysa tuşlar kontrol rotasyonuna göre uygulanıyor (`CalculateMaxAcceleration`,
`GetControlRotation`). Aynı V2.14 çekimlerinin kök yolu ve aktör yönü üç kamerada da −90°'ye gidiyor:

| Çekim | +0.35 s | +0.6 s | +0.95 s | +1.4 s (kök, cm / aktör yaw) |
|---|---|---|---|---|
| v214z r_cutrev_r yan | (1110, 15) 21° | (1175, 36) −12° | (1202, 31) −54° | (1267, −212) −90° |
| v214z çapraz | (1064, 14) 21° | (1129, 32) −29° | (1171, 5) −86° | (1203, −236) −90° |
| v214z oyun kamerası | (1096, 28) 32° | (1146, 51) 0° | (1186, 34) −75° | (1217, −185) −90° |
| v215z yan / çapraz / oyun | 34° / 40° / 34° | 9° / −4° / 1° | −73° / −85° / −76° | −90° / −90° / −90° |

V2.14'te kameralar arasında görülen farklı zincirler (ör. yan çekimde koşu başlangıcı) aynı girdiyle **MM seçim değişkenliği** idi
(ve V2.14'teki PushStand deliği). Uygulama: `dirchange213.py` artık kontrol yaw'ını (`cy`) kullanıyor — üç kamera için de "world −90".
Tanı için eklenen `GR215_CamYawFromControl` profil alanı (kamera yörüngesinin `TW_CameraWorldYaw` girdisi) hareket girdisini
etkilemiyor; gerek yok, oyunda ve üretimde kapalı (kaldırılabilir). Gözlemci kamerası yalnız gözlemci; ölçüm araçları kontrol çerçevesini
kullanıyor. Aynı hareketin farklı açılardan incelenmesi için aynı koşunun kaydı tek kamerayla alınabiliyor; farklı koşular farklı
senaryo gibi etiketlenmeli (seçim değişkenliği: r_cutrev_r yan/çapraz pivot +0.11/0.12, oyun kamerası önce kesiş klibi +0.07).

## 6. Ölçümler ve eski–yeni tutarlılığı
### 6.1 Tanımlar (`contact215.py`)
- Nokta: ball_l / ball_r (dünya, cm). Zemin: koşunun o ayak için %10'luk top yüksekliği. Temas: zemine ≤1.5 cm **ve** <60 cm/s.
  **drag** = zemine ≤1.5 cm ama ≥60 cm/s (yerde kayan ayak). **roll** = 1.5–4 cm ve ≥60 cm/s (zemine sürtünen adım / doğal yuvarlanma,
  kayma sayılmaz). Evre: topun pelvise göre ileri konumu (> +8 erken, −8…+8 orta, < −8 geç). Pencere ve kare hızı her satırda yazılı.
### 6.2 "Çıkış kayması" çelişkisi
- V2.13 raporu "0.4–2.3 cm": `push212.py` EXIT satırı = geçiş karesinin ±0.1 s'sindeki temas (çoğu koşuda ayak havada → küçük/yok).
- V2.14 raporu "V2.13: 23–27 cm": `contactslip.py` geçişten sonraki **ilk depar basışının iniş** evresi (v213q0 p_w2s r1/r2: 27.1 / 21.7 cm).
- V2.14 "sonra" değeri (2.1–3.8) ise yine push212 penceresiydi → V2.14 karşılaştırması iki farklı tanımı karıştırmıştı.
- Aynı tanımla (ilk depar basışı inişi, contactslip): V2.13 21.7, 27.1, 1.5 · V2.14 2.1, 3.1, 3.5 · V2.15 1.5–4.3 cm. İyileşme V2.14'te
  gerçek; V2.13 raporundaki küçük değer başka ölçüydü.

## 7. Koruma (e2, kayıtlı üretim; 46 koşu, 17'si telemetri kaybı nedeniyle doğru günlükle yeniden koşuldu)
| Zincir | Sonuç |
|---|---|
| kesiş → S (k_cut_back) | +0.09 A_CP2_Jog_Fwd_Pivot → geri koşu; değişmedi |
| itişte tuş bırakma (chain_scutrel) | duruş vmin 0, değişmedi |
| ikinci yön değişimi (chain_sscut ×2) | zaman çizelgesi V2.14 ile aynı; pelvis 70 cm (§4) |
| geri tuşları (k_ws_clean, k_ws_ovl40, k_ws_shift, p_revpush) | ters dönüş +0.75–0.82 s, geri ≤300, geri giderken ileri klip yok |
| tempolu → depar (p_j2s) | itişsiz (tasarım), değişmedi — eksik olarak açık |
| dururken Shift+W (p_tapretrig) | RR_Start 0.36, değişmedi |
| idle→yürü→dur→yürü ×2, eğim ×2, tek ayak, 180 yürüyüş dönüşü | diz/baldır p99 4.9–8.3, n>30 = 0 |
| yanlış tetik (wdiag, chain_wawd, r_curve, r_wcurve, a_tap) | RevTurn / PushRevOn / LowOn 0 kare, V2.14/15 DB'si seçilmedi |

## 8. Üretim değerleri, dosyalar, geri dönüş
(verify_prod215.txt; LinkMaxSpeed kurulum çıktısında) ABP: SHM215_LinkOn 1, LinkMaxSpeed 230, LowSpeed 60, TipLock 1, PivFoot 0; SHM211_DB_Push / SHM214_DB_GaitPush =
PSD_SHM215_WalkPush; SHM212_DB_CutRevL/R = PSD_SHM215_Rev_L/R; V2.14 değerleri korunuyor. DA_GR_LocomotionBehavior: M1 değerleri değişmedi;
yeni alanlar GR215_RevBrakeAccel/Decel/YawHold = 0, CamYawFromControl false (uyuyan adaylar denetimi ✓).
Değişen ikili dosyalar (editörden): ABP_GR_MotionMatchingBase/MotionMatching (MontTick: bağlantı, düşük hız, fren ayağı, dönüş kilidi;
EventGraph dalları), BP_GR_Player (+BP_PBI_Player yeniden derleme; PhysicalRedirect / CalculateMaxAcceleration / CalculateGroundFriction /
GR_UpdateRig knob'ları, varsayılan kapalı), BP_GR_MotionProfile (alanlar), 8 dönüş klibi (adım yüksekliği), iki yürüyüş→depar klibi
(pencere/dışlama), yeni V215 varlıkları (PSD_SHM215_Rev_L/R, RevPushLow, WalkPush, PSS_SHM215_WalkPush, SHM215_Pivot_F_B_*, PushLow_*),
A_LB_Sprint_Fwd (ters DB izinden çıkarıldı).
Geri dönüş: `Saved/Codex/SHME_V215_20261017/checkpoint/baseline_v214/` (ABP'ler, pawn, profil, DA'lar, bileşen, V212/V214/Turns/RelaxedRun
klipleri), `pre_walkpush/`, `pre_tip_clearance/`; bayraklar: LinkOn 0, LowSpeed 0, TipLock 0, DB_Push = PSD_SHM212_GaitPush,
CutRevL/R = PSD_SHM214_Rev_L/R (V2.14 kopyaları checkpoint'te).

## 9. Yakalamalar ve medya
Kayıtlı son üretim, gerçek zamanlı 30 fps mcap (QA kil test görünümü, yalnız PIE), kare kesilmedi. 34 çekim (`v215z_*`), telemetri
34/34 (rows > 0). Otomatik denetim `scan_dormant_v215z.txt`: **SCAN_OK** (istek bayrakları = verify_prod215, montaj/kuyruk 0 kare,
pawn adayları RevBrake*/YawHold 0, emekli DB yok). Yeniden açılan editörde `verify_prod215.txt`: aktif DB'lerde `/Rollbacks/` ve None 0.
Kontak sayfaları (`pub/img`, üst V2.14 / alt V2.15): `cut_reverse_before_after.jpg` (oyun kamerası + çapraz), `cutrev_late_before_after.jpg`,
`push_before_after.jpg`, `tip_reverse_before_after.jpg` (ters 180 dönüşte basan ayağın yerden kalkışı f35). Videolar `pub/vid`
(gerçek hız GIF/AVI, ters dönüş ve itiş için 1/3 hız AVI).

## 10. Beceri / bellek
`.agents/skills/sphirus-human-motion-engine/references/validation.md` ve `architecture.md`'ye V2.15 bölümü (temas/evre tanımı,
DB'den klip çıkarma yöntemi, PF dizi adı çakışması, eski LR_LOG tuzağı, kontrol-yaw etiketi, doğrulanmış/başarısız adaylar);
bellek `shme-v215-contact-phase.md`.

## 11. Teknik / görsel / kabul ayrımı
Teknik: §0 tablosu. Görsel değerlendirme (benim gözümle, kontak sayfaları): ters 180 dönüşte basan ayak artık zeminden kalkıyor; itiş
zinciri tek parça; pivot girişinde ayak süpürmesi ve kesişteki derin çömelme çekimlerde görülebilir. Kullanıcı kabulü: bekleniyor.
