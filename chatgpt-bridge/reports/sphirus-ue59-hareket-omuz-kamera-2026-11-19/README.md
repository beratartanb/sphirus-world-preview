# SPHIRUS UE 5.9 — omuz–kol, duruş/dönüş, yokuş, dar alan kamerası, ışık ve performans (2026-11-19)

Başlangıç referansı: `75e55ac` commit'indeki iki rapor (`sphirus-ue59-fullbody-2026-11-18`, `sphirus-ue59-jogstop-2026-11-18`). O günden sonra projede yerel varlık değişikliği yoktu (yalnız kaydedici betiği). 5.9 kopyasındaki `SFSaveSlot.sav` 18 Kasım 14:53'te değişmişti (kullanıcının oyunu); kullanıcı verisi gibi korundu. Gerçek 5.8.4 kaydı `4823d83a…` değişmedi, 5.8.4 projesine dokunulmadı.

Durum etiketleri ayrı tutuldu: **UYGULANDI** (kalıcı, kayıtlı), **TEKNİK TEST** (ölçüm), **GÖRSEL İNCELEME** (kare kare baktım), **PERF ÖLÇÜLDÜ**, **KULLANICI KABULÜ** (verilmedi — hiçbir madde kabul edilmiş sayılmadı). Videoları gerçek hızda oynatarak izleme imkânım yok; görsel inceleme kare panoları ve tek karelerle yapıldı, akıcılık / his değerlendirmesi kullanıcıya kalır.

## 0. Ortam ve korunan kazanımlar

- Editör bugün Windows Akıllı Uygulama Denetimi yüzünden açılmadı: projedeki yerel derlenmiş dört eklentinin (Black_Eye, Nwiro, PBL_Database, GravityScatterTool) DLL'leri her açılışta engellendi (Code Integrity 3077/3033). Güvenlik ayarına dokunulmadı; ev haritası ve alt seviyeleri bu eklentilere referans vermiyor; editör yalnız bu oturum için `-DisablePlugins=…` komut satırı argümanıyla açıldı (proje dosyası değişmedi). **Paketlenmiş oyun ve bu eklentilerin özellikleri bu turda test edilmedi.**
- Çalışan projeden doğrulandı (`data/` + `changes/`): seçici bantları 200/440, Relaxed koşu/yürüyüş duruş eşlemeleri kaldırılmış (eşleme 32 → bu turda 33, §3), kapsül yuvarlak taban, yokuş eğimi/hız ölçeği açık (SlopeOn), iç mekân güneş ışık fonksiyonu takılı, kayıt/etkileşim akışı çalışıyor (§9).
- 5.9'da Python `BlueprintTools` API'si kalktı; grafik betikleri için `unreal.BlueprintToolset` üstüne ince uyum katmanı yazıldı (`changes/b59.py`). Animasyon Blueprint'leri DSL ile düzenlenemiyor (MCP ve Python), o yüzden düğüm düzeyi API kullanıldı.

## 1. Ölçüm ve video zamanlaması (8. madde)

- **Önceki ana video yarı hızdaydı — doğrulandı ve düzeltildi.** `sbs.py` yan yana videoları sabit 30 fps kodluyordu; 60 Hz yakalanmış 1.098 kare 36,6 s oldu (simülasyon 18,3 s → 2× yavaş). Araç artık kaynak FPS'i kullanıyor; her video `vtime.py` ile denetleniyor (simülasyon süresi/adımı, yakalanan kare, kodlanan FPS, son süre → REAL_SPEED / SLOW). `data/video_timing_previous_round.txt`, `data/video_timing_this_round.txt`.
- Bu turun bütün videoları **30 Hz sabit oyun adımı, 30 fps kodlama = gerçek hız**. Ağır çekim üretilmedi.
- Yeni ölçüm araçları (`changes/tools/`): `an_stop2.py`, `an_turn2.py`, `an_shoulder.py`, `an_stride.py`, `an_camtight.py`, `an_perf19.py`.
  - Pencereler saniye cinsinden; giriş hızı **anlık** (`v_in`) ve **0,5 s ortalama** (`v_win`) ayrı.
  - Ayak teması: top kemiği izlenen zeminin < 5 cm üstünde **ve** dikey hız < 20 cm/s. Yatay hız kullanılmıyor, yani kayan basılı ayak temas sayılıyor; havadaki ayak sayılmıyor.
  - Kayma her ayak için ayrı (`slide L/R`) ve toplam (`sum`) — iki ayağın temas sırasındaki yatay yol uzunluğu toplamı; ayrıca `drift L/R` = bir temas boyunca ayağın temas başladığı noktadan en çok uzaklaşması. cm/s değil.
  - Kalça çöküşü: bırakıştan önceki 0,5 s ortalamasına göre; dönüşlerde adım salınımı sayılmasın diye 0,4 s kayan ortalama. Yerleşme/toparlanma: değerin **0,3 s boyunca** 1,5 cm içinde kaldığı ilk an (tek karelik yaklaşma sayılmaz).
  - Ölçüm tanımı değiştiği için önceki turun kayıtları da yeni yöntemle yeniden ölçüldü (aynı tablolar "önce" sütunu).
- Kaydedici: omuz–kol katmanı alanları (`sh`: sürücü iskelet konumları + beden katmanı ağırlıkları), canlı nesneye yürüme adımı (`GOTO` hedefi bir sınıf adı olabilir — ikinci odun parçası için, §9).

## 2. Omuz–kol gerginliği (AYRI KABUL MADDESİ)

**Gözlenen kusur:** yürürken ve özellikle koşudan yürüyüşe geçerken omuzlar kalkık / geride, üst kollar gövdeden açık.

**Kök neden (ölçümle ayrıldı, `data/shoulder_*`):**

| Ölçü (görünen beden) | Ayakta | Düz yürüyüş | Koşu→yürüyüş +0,5–1,0 s | Jog |
|---|---|---|---|---|
| Üst kol açısı (dikeyden dışa, °) | 11,9 | 16,2 | 28,3 | 28,8 |
| Omuz eklemi göğüs eklemine göre yükseklik (cm) | 5,0 | 6,0 | 6,3 | 7,6 |
| Omuz eklemi göğüse göre önde/geride (cm, − = geride) | −0,3 | −1,5 | −3,2 | +1,6 |

- Geçişteki geniş kol taşıma **kaynak klipten** geliyor: `M_Neutral_Transition_Run_to_Walk` ~3,8 s sürüyor ve ilk ~1 s'de sürücü iskeleti de 28–29° taşıyor (retarget değil).
- Düz yürüyüşteki açıklık da sürücüde var (17°, erkek mocap); görünen bedende duruş katmanının "göğüs yukarı" ayarı (spine_05 −12°) omuzları ~1,3 cm geride tutuyordu.
- Efor/yorgunluk duruşu (köprücüklere ±7°) bu testlerde hiç devreye girmedi (EffA = 0), neden değil. Köprücük retarget ayarı (−5°) değiştirilmedi.
- Duruş katmanında yalnız yürüyüşe ya da yalnız yavaşlamaya ağırlık verebilen bir kanal yoktu.

**Uygulanan (UYGULANDI, `ABP_Sph_Body_GASP`):** duruş katmanının sonuna iki ağırlıklı terim:
- `MoveA` (hızla 0→1, ayakta 0): köprücükler 3° aşağı + 3° öne, üst kollar 3° içe, üst göğüs kaldırması 4° az.
- `RelA` (hareket hâlinde yavaşlarken hızla yükselir, ~1 s'de söner): köprücükler 3° aşağı + 2° öne, üst kollar 5° içe — koşu→yürüyüş geçişini hedefliyor.
- Hepsi `ArmW` ile çarpılı: montaj (odun alma, taşıma, kesme, şömine) sırasında 0. Akışta ölçüldü: taşıma/kesme sırasında ArmW 0,000–0,002 (`data/flow_*`), el–nesne teması bu terimlerden etkilenmiyor.
- Sabit omuz düşürme ya da bütün animasyonlara kol kapatma yok; ayakta durma değişmedi (11,9 → 11,0–12,1°).

**Önce/sonra (kayıtlı durum, aynı plan, 60 Hz veri):**

| Ölçü | Önce | Sonra |
|---|---|---|
| Düz yürüyüş üst kol açısı | 16,2° | 8,6° |
| Düz yürüyüş omuzların geride tutulması | −1,5 cm | −0,6 cm |
| Geçiş +0,5–1,0 s üst kol açısı (sürücü aynı anda 28,5°) | 28,3° | 16,1° |
| Geçiş +1,0–1,5 s | 21,3° | 9,9° |
| Geçiş omuz yüksekliği | 6,3 cm | 5,4 cm |

- Değer taraması (R0–R3) ve elenen aday: R3 geçişte kolu gövdeye yapıştırıyordu (7,6°). `data/shoulder_screening_R0-R3.txt`.
- GÖRSEL İNCELEME: `evidence/shoulder_before.jpg` / `shoulder_after.jpg` (önden 3/4, yan, arkadan 3/4; yürüyüş, jog sonu, geçiş +0,5/+1,0/+2,0 s, geç yürüyüş). Düz yürüyüşte kollar gövdenin yanında, omuzlar daha aşağıda ve önde; kamburlaşma ya da omuz çökmesi görülmedi. **Geçiş +0,5 s'de el hâlâ göğüs hizasına kadar salınıyor** (klibin salınım genliği; ek rotasyon bunu küçültmez) — AÇIK.
- Videolar: `videos/shoulder_a35|a90|a150_before_left_after_right.mp4`. Oyuncu kamerasında: `videos/flow_full_player_camera.mp4`.

## 3. Duruşlarda kayma ve sprint freni

**Kök neden:** karakterin fren eğrisi (PhysBrake 380 → 780 cm/s², 165 → 585 cm/s) klip frenlerinden yavaştı: Relaxed jog duruşu ~900, Neutral koşu duruşu ~1650 cm/s² ile duruyor (`data/stop_clip_root_speed.txt`). Kapsül, klibin beklediğinden uzun süre ilerliyor, basılı ayak sürükleniyordu (önceki raporun 48–62 cm'lik geçiş/dönüş duruş kaymasının neredeyse tamamı sağ ayak, `M_Relaxed_Run_Stop_F_Rfoot`). Sprint duruşundaki 31 cm çöküş Relaxed sprint duruş klibinin içeriği.

**Uygulanan (UYGULANDI):** fren üst değeri 780 → **1100** (alt 380 korunuyor: yürüyüş ~406, jog ~808, sprint 1100 cm/s²) — `AC_Sph_Motion` + `BP_Sph_GASPCharacter` bileşen şablonu; sprint bırakışı için eşleme `Relaxed_Stand_Sprint_Stops → Dense_Stand_Run_Stops` (Neutral koşu duruşu). 200/440 bantları ve Relaxed duruşlar korunuyor.

**Elenen adaylar:** alt değer 500 (60 Hz'de iyi, ama 30 Hz'de yürüyüş duruşunu 1 → 36 cm kaydırdı — kare adımına bağlı klip fazı); sprint 1400 (jog duruşunu 94 cm'ye kısaltıyordu); Neutral sprint duruşu (kayma iyi, çöküş 24–31 cm kalıyor). `data/stops_*`.

**Önce/sonra (kayıtlı durum, aynı plan):**

| Duruş | Önce kayma (toplam) / çöküş | Sonra 60 Hz | Sonra 30 Hz |
|---|---|---|---|
| Jog 415 (bırakış fazları) | 4,8–52,4 cm / 12–13 cm | 1,6–8,4 cm / 12–13 cm | 0–7,8 cm (bir fazda 43 cm) |
| Yürüyüş→jog→duruş | 48,4 cm | 2,3–5,7 cm | 6,9–7,2 cm |
| 90° dönüp durma | 45,8 cm | 25,5 cm | 27,1 cm |
| 360° dönüp durma | — | 32 cm | 35 cm |
| Jog fren (iki deneme) | 47 / 7 cm | 4,2 / 2,3 cm | — |
| Yürüyüş duruşları | 15,7 cm | 2,7–4,7 cm | 0,8–1,1 cm |
| Sprint 585 | 62–73 cm / 31 cm | 20–27 cm / 11–12 cm | 31 cm / 10 cm |

- Durma mesafeleri: jog 155 → ~116 cm, sprint 253 → ~180 cm, yürüyüş değişmedi (~42 cm).
- **Kanıt videosu kipinde (30 Hz, ekran görüntülü; `data/stops_video30_before_after.txt`)** sonuç karışık: jog duruşu 3,1 → 3,0, yürüyüş→jog→duruş 27,3 → 3,8, sprint çöküşü 27 → 11 cm (kayma 35 → 38); ama **yürüyüş duruşu 1,4 → 44,7 cm** ve **360° dönüp durma 21 → 42 cm** kötüleşti. Yürüyüşte iki durumun freni neredeyse aynı (394 / 406 cm/s²): yürüyüş duruşu ayak fazına aşırı duyarlı — aynı hızda bir kayıtta sol, diğerinde sağ ayaklı `Relaxed_Walk_Stop_F` seçiliyor ve sağ ayaklı varyant bu fazda ayağı 35–45 cm sürüklüyor. Aynı plan 30 Hz veri kipinde 1,1 cm, 60 Hz'de 2,7–4,7 cm. Bu, değişiklikten bağımsız, faza bağlı açık bir kusur olarak kaydedildi.
- TEKNİK TEST: PARTIAL. Kalça çöküşü azalırken toplam kayma da azaldı; ama **dönerek durma 25–35 cm ve bazı fazlarda jog/sprint 27–43 cm** hâlâ yüksek, kare adımına (30/60 Hz) duyarlı. Düz harita 30/60 Hz başarısı yokuşta ve değişken kare süresinde doğrulanmış sayılmadı.
- Video: `videos/stops_fullbody_before_left_after_right.mp4` (tüm beden ve ayaklar, yan kamera 450 cm).

## 4. Keskin dönüşler

- **Yürüyüş sola 180°:** yeniden doğrulandı — `Walk_Loop → Turn_L_090_Lfoot → (dönüşün ortasında) Turn_L_180_Lfoot`; sağ ayak 26 cm sürükleniyor (toplam 42–47 cm). Kök neden: dönüş isteği 0,25 s'de geldikçe önce 90° klibi seçiliyor, istek 180°'ye ulaşınca orta-klipte 180°'ye geçiliyor. Yürüyüş dönüş veritabanının "devam eden pozu sürdürme" eğilimi −0,01 (jog'da −0,35): −0,35 ve −0,15 denendi — sol 180° 42 → 22–27 cm iyileşti ama sağ 90° 5 → 18, sağ 135° 17 → 39–41 cm bozuldu; **alınmadı** (yalnız bellekte denendi, kaydedilmedi). **AÇIK** — sıradaki doğru adım: dönüş klip kopyalarına orta-klip geçişini engelleyen işaret (BlockTransition) koymak.
- **Jog 135/180° kalça alçalması 12–19 cm:** kaynak klip içeriği — Relaxed jog dönüş klipleri kendileri 11–20 cm iniyor; Neutral dönüş klipleri daha derin (25–33 cm) (`data/turn_clip_pelvis_drop.txt`). Kalçayı yukarı iten ofsetle gizlenmedi. **AÇIK** (klip düzeyi çözüm gerekiyor).
- Diğer dönüşler (±45/90) yürüyüşte 3–8 cm, jog'da 5–8 cm kayma. `data/turns_final.txt`.

## 5. Yokuş

- Ölçümler gerçek zemine, kapsül tabanına ve her ayağın kendi zeminine göre ayrı (önceki "85 → 63 cm" kullanılmadı).
- **Kök neden (ölçüldü, `data/slope_step_length.txt`):** yokuş yukarı adım uzunluğu kısalmıyor (düz 101,6 cm, dik yokuş 98,6 cm), yalnız tempo düşüyor (112 → 102 adım/dk). Hız düşürülünce Motion Matching oynatma hızı 0,85'e iniyor (aralık 0,85–1,15), adım boyu sabit kalıyor; bu yüzden ön ayak eğimde uzağa uzanıyor ve diz katlanıyor (~116°).
- Doğru sahibi: sürücü animasyonunda adım boyunu kapsül hızına göre kısaltan Stride Warping ("Adım Bükülmesi" düğümü 5.9'da mevcut). Düğüm bellekte kuruldu ve ayarları okundu; doğru ölçek için oynatılan klibin kök hızı gerekiyor ve Graph modunun hız pini açık değil. Oynatma hızını sabitlemek jog kliplerinde kaymaya yol açacağı için **bu turda uygulanmadı — AÇIK**.
- Eğim katmanı kısa testleri (TEKNİK TEST, ev haritası yokuşu): ters yöne dönünce eğim değeri 0,5 s içinde yeni yöne göre güncelleniyor; zıplamada sıçrama yok; dik eğimde dururken ~3° öne eğilme kalıyor (doğal). Rotanın son bölümünde test girdisi bir kaya/engele yöneldi (ayak izi 80 cm yukarıda bir yüzeye çarpıyor) — oyun kusuru sayılmadı.

## 6. Dar alan kamerası

**Kök neden:** `AC_Sph_Camera` kol engele çarpınca güvenlik oranı (SafeFrac 0,3–1) arka uzaklık, yan kayma **ve yüksekliği** birlikte küçültüyordu: kamera baş hizasında, başın arkasına dümdüz yaklaşıyordu.

**Uygulanan (UYGULANDI):** sıkışınca yüksekliği küçültmek yerine kontrollü yükseltme — `TightRaise` 45 cm × MapRange(SafeFrac 1→0,4), tavan probuyla sınırlı (DUp − 40), 5/s yumuşatılmış; engel kalkınca SafeFrac'ın mevcut 1,6/s dönüşüyle normal kadraja döner. Yakın omuz kamerası mesafesi değişmedi.

| Kapı geçişi (2,5 s) | Önce | Sonra |
|---|---|---|
| Kamera–baş mesafesi | 78,5 cm | 78,9 cm |
| Kamera başın üstünde | 6,5 cm | 30,5 cm |
| 12 cm'yi aşan kamera sıçrama karesi | 37 | 37 |

GÖRSEL İNCELEME: önce saç kadrajın üst-ortasını kapatıyordu; sonra baş kadrajın altına iniyor, pencere/mutfak/geçiş görünüyor (`evidence/camera_tight_tr0_top_tr45_bottom.jpg`, `videos/camera_tight_tr0_left_tr45_right.mp4`). Etkileşim başlangıç/bitişinde kadraj: akış videosunda incelendi (§9), ayrı sayısal test yapılmadı.

## 7. Işık ve performans

**Işık (korundu, TEKNİK TEST):** kapıdan çıkış ve atölye penceresi rotalarında kare parlaklığı önceki turun "sonra" kayıtlarıyla 0,01 içinde aynı; beyaz kırpılan piksel oranı %0,06. Kapı geçişinde parlaklık 1 s'de yumuşakça 0,13 → 0,30 çıkıyor, 3 karedeki en büyük adım 0,03 — ışık bölgesi sınırında sıçrama yok. `videos/light_exit_final.mp4`, `light_workshop_window_final.mp4`.

**Performans (PERF ÖLÇÜLDÜ, editör PIE, RTX 4060 Laptop):**
- Ortam: PIE görünümü 1509×920, TSR (render ölçeği otomatik, `r.ScreenPercentage` 0 — gerçek iç çözünürlük okunmadı), Epic ölçeklenebilirlik, Lumen GI + yansımalar, donanım ışın izleme, sanal gölgeler, Nanite, VSync kapalı, kare sınırı yok (`data/perfenv.txt`). Bitki ve saç açık.
- GPU geçiş dökümü (`r.GPUCsvStatsEnabled`): kare 45–50 ms, bunun **24–26,5 ms'si sanal gölge çizimi (ShadowDepths)**; diğer geçişlerin her biri < 3 ms (Nanite 2,8, gölge yansıtma 2,5, TSR 1,8, saç görünürlüğü 1,6, Lumen 0,9).
- Isı/saat: GPU 2310–2520 MHz, 80–95 W, 82–89 °C; kısıtlama bayrakları arasında ısıl yavaşlama (0x20) var. Aynı saat hızında farklı ayarlar tutarlı fark verdi — sıcaklık tek başına neden değil.
- **Uygulanan (UYGULANDI, `Config/DefaultScalability.ini`, Epic gölge kalitesi):** durağan güneş gölgesi çözünürlük bias'ı −1,5 → 0 (motorun "High" kademesi). Hareketli nesneler (karakter) −1,5'te kaldı — karakter gölgesi aynı. Projedeki sanat ayarı (SMRT ışın 12/örnek 8) korundu.

| | Önce (−1,5) | −0,5 | Sonra (0) |
|---|---|---|---|
| Gölge çizimi | 24–26,5 ms | 11,2 ms | 7,2–7,8 ms |
| Kare süresi medyan | 46–50 ms | 34,6 ms | 28,5 ms |
| Ortalama FPS | 20,1–21,9 | 28,9 | 35,0–35,2 |

- Elenen aday: bitki WPO önbellek geçersizleştirme mesafesi (etki yok).
- GÖRSEL İNCELEME: dışarıda üç bias arasında oyuncu kamerasında fark seçilmedi (`evidence/shadow_bias_stills.jpg`); iç mekân kareleri kamera kıpırdadığı için birebir karşılaştırılamadı.
- **Bağımsız/paketlenmiş oyun ölçülmedi**; sonuç başka donanıma genellenmedi.

## 8. Oyun akışı (son kayıtlı durum, gerçek girdiler)

Ev → mutfakta yürüyüş → kısa jog → ileri giderken koşudan yürüyüşe → arka kapıdan çıkış → patikada yürüyüş + jog (yokuş aşağı) → duruş → 180° dönüş ve geri → odun al → taşı → kütüğe koy, kes → **iki parçayı topla** → eve dön → şömineye yerleştir → yak.

- **PASS** (`data/flow_counters.txt`, `videos/flow_full_player_camera.mp4`, 92,7 s): Wood 1 → Split 2 → Fire 1 (yerleştirildi) → Fire 2 (yandı).
- Önceki testin ikinci parçayı kaçırma nedeni test planıydı: parça her koşuda farklı yere düşüyor (bu koşularda 1,5 m'ye kadar) ve sabit rota ona varmıyordu; ayrıca kütüğün kuzeyindeki odun rafı/el arabası düz yolu kesiyordu. Plan artık parçanın o anki konumuna yürüyor ve kütüğü güneyden dolaşıyor.
- Kayıt yükleme: akışın yazdığı test kaydı şömine başında yüklendi → iki parça envanterde → yerleştir + yak **PASS**. Odunsuz şömine reddediyor **PASS**.
- Yan not: toplanan parçalar sayaçta toplanmış görünürken parça listesinde ilk konumlarında "görünür" kayıtlı kalıyor; videoda kontrol edilecek bir görsel kalıntı olabilir — doğrulanmadı.
- **Maske, çay, yatak, kapı:** kurulumlar bulundu (önceki turdaki "yok" sonucu yanlıştı): `GR_Day_Tea` (tür 5), `GR_Day_Bed` (tür 9), `GR_MaskBench` + `GR_MaskHook`, `GR_Day_WardDoor`/`Set0–4`, altı `GenericDoor_BP`. Kısa E testleri tetiklenmedi — kayıtta kamera yönü hedefe hiç dönmedi, yani test girdisi nişan almadan basıldı. **Doğrulanmadı** (oyunda çalışmadığı sonucu çıkarılmadı).

## 9. Değişen varlıklar ve geri dönüş

| Varlık | Değişiklik | Geri dönüş (ilk yedek) |
|---|---|---|
| `ABP_Sph_Body_GASP` | MoveA/RelA terimleri ve değerleri | manifest `ue59_m20_relax` (SHA1 önce `d7305875…`) |
| `AC_Sph_Motion` | BrakeDecelHigh 780 → 1100 | `ue59_m20_round` |
| `BP_Sph_GASPCharacter` | SphMotion şablonu aynı fren | `ue59_m20_round` |
| `ABP_Sph_GASP` | sprint duruşu eşlemesi (32 → 33 satır) | `ue59_m20_round` |
| `AC_Sph_Camera` | TightRaise / TRaiseA | `ue59_m20_cam_122721` |
| `Config/DefaultScalability.ini` | durağan güneş gölgesi bias 0 | `Saved/UE59Work/checkpoints/20261119_config/` |

Yedekler `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/<manifest>/` altında, SHA1'leri `changes/manifests/*.json`. Kirli paket kalmadı. Ara manifestler (`ue59_m20_relax2`, `ue59_m20_cam2`, `ue59_m20_brake2`) aynı varlıkların ara durumlarını tutuyor.

## 10. Özet durum

| Madde | Uygulandı | Teknik test | Görsel inceleme | Perf | Kullanıcı kabulü | Açık |
|---|---|---|---|---|---|---|
| Omuz–kol (ayrı madde) | ✓ | ✓ | ✓ kare | etkisiz | — | geçişte el salınımı yüksek |
| Duruş kaymaları | ✓ | PARTIAL | ✓ kare | — | — | dönüp durma 25–42 cm; yürüyüş duruşu faza bağlı (1–45 cm) |
| Sprint freni | ✓ | PARTIAL | ✓ kare | — | — | kayma 20–31 cm |
| Yürüyüş sol 180° | — (aday elendi) | ✓ | — | — | — | orta-klip geçişi |
| Jog dönüş alçalması | — | ✓ (klip kaynağı) | — | — | — | klip düzeyi |
| Yokuş adım/diz | — | ✓ kök neden | — | — | — | Stride Warping |
| Dar alan kamerası | ✓ | ✓ | ✓ kare | — | — | etkileşim kadrajı sayısal test yok |
| Işık kazanımı | korundu | ✓ | ✓ | — | — | — |
| Performans | ✓ | — | ✓ dış | ✓ 20 → 35 fps | — | bağımsız/paketli ölçüm yok |
| Tam akış + kayıt yükleme | — | ✓ PASS | ✓ kare | — | — | maske/çay/yatak/kapı doğrulanmadı |

AnimGen, saç/kumaş hareketi: bu turda dokunulmadı. Paketlenmiş oyun: test edilmedi.

## 11. Kanıt sürümü ve dünya önizlemesi

- Bütün son kanıtlar (videolar, `data/*final*`, `data/flow_counters.txt`, `evidence/shoulder_after.jpg`) son kayıtlı yapılandırmada alındı (fren 380/1100, gevşetme terimleri, sprint → Neutral koşu duruşu, TightRaise 45, durağan güneş gölgesi bias 0). Ara aday kayıtları yalnız `data/*screening*` ve `*variants*` dosyalarında.
- Bir kayıt zincirinde ekran görüntüsü alınamadı (22–25 / 435–923 kare; büyük olasılıkla ekran kilidi ya da editör penceresi arka planda). O videolar ve veri dosyaları `Saved/UE59Work/invalid_20261119/` altına ayrıldı, hepsi yeniden kaydedildi; rapora girmedi.
- Bütün videolar `vtime.py` ile denetlendi: REAL_SPEED (`data/video_timing_this_round.txt`).
- Dünya önizlemesi: gölge yapılandırması değiştiği için son durumdan yeni Bridge dışa aktarımı alındı — run `2026-11-19_174051_964355_346de9`, 18 görünüm, son yayınla aynı kamera pozları, 0 hata (8 standart kapsam uyarısı).
