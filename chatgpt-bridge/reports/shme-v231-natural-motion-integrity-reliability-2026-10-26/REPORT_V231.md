# SPHIRUS — SHME V2.31: düşük hızlı dönüş içeriği, depar çıkışı, yük altında yakalama adımı, geçiş bütünlüğü, inceleme hedefi, basamak ve geliştirme güvenilirliği (2026-10-26)

Taban: V2.30 üretimi (bridge `37c3962`), temiz editörde `VERIFY230 ALL_OK`. UE 5.8, Blueprint-only. Sahipler: bileşen `BP_SHM_HumanMotionComponent` (DSL), ABP `ABP_GR_MotionMatchingBase`, DA `DA_SHM_Response_Default`, içerik `SHME/Animations/V231`. Yeni sistem/framework yok; her değişiklik mevcut sahibinde, ayrı düğme grubunda (`promote231.py`). Checkpoint `checkpoint/pre_v231` (101 varlık + araçlar). Temiz yeniden açılışta **`VERIFY231 ALL_OK`** (V2.29/V2.30 sözleşmeleri + yedi V2.31 grubu + inceleme çözücüsü + eğri oranları + DB'ler).

**Ölçüm notu.** V2.30'un “tüm klip kayması” (yalnız yükseklik) pivotu, alçak salınımı ve gerçek kaymayı karıştırıyordu. V2.31 `contact231` sınıflandırıcısı görünür toplar üzerinde: **SLIP** (durduktan sonra ≥ 5 cm), **DRAG** (yere değerken > 25 cm/s ile ≥ 5 cm sürüklenme), **PIVOT** (top sabit, ayak dönüyor = normal), **SKIM** (hiç durmayan alçak salınım = temas değil). Ayağın kalkıp yeniden basması (gerçek destek yer değiştirmesi) ayrı epizottur, kayma sayılmaz. “Pencere” = olayın kendisi (ör. swl12'de W anı +1,4 s, e29'da ikinci dönüş). LTP aynı kareyi bazen iki kez yazıyordu → sahte ivme sıçramaları; okuyucu artık tekrarları atıyor. Tüm tablolar `data/`.

## 0. Raporun başında istenen sorular

1. **49 cm/s düşük hız girişi artık güvenilir mi?** Sabit 30'da **evet (teknik)**. Üretimde 3 tekrar: 11,6 / 8,8 / 11,6 cm (V2.30: aynı koşul iki kipli, 20,3 cm DRAG / P6'da 46,5 cm net). Her iki giriş evresinde de yeni düşük hız ailesi (`SHM231S_SlowRev_*`) seçiliyor, satıcı kuyruğu / ters poz yok. 20 FPS 23 → 17, 120 FPS 12 → 12, gerçek zaman 26 → 10. **60 FPS'te PARTIAL**: kötü evrede 55 (üretim) → 21–44 cm; kalan sürüklenme, kaynak satıcı pivot → geri yürüyüş karışımının iniş anına denk gelmesi (§2.3).
2. **60/120 FPS eforlu dönüş kayması düzeldi mi?** **Büyük ölçüde.** Sahip, depardaki her yazılmış dönüş çıkışının V2.14 RevPush penceresine düşmesiydi (tüm FPS'lerde 12–42 cm; 60/120'de bir sonraki dönüş girişini bozuyordu). e29_load pencere: 60 FPS 36,9 → **0**, 120 FPS 29,4 → 19,7; e29_recov 60 FPS 36,9 → 0, 120 29,4 → 21,1; e29_chain 120 66,1 → 33,5. Aynı fiziksel giriş taraması (`e31_s2`) 120 FPS 4900: 29,3 → 6,5. Tek koşuda gerileme: e29_chain 60 FPS 14,3 → 26,1 (önceki sprint dönüşünde rota ayrışması, §3).
3. **Yeni destek/toparlanma animasyonları üretildi ve kullanılıyor mu?** **Evet.** Yük altında (`EffortEUse` ≥ 0,45) F_B dönüşü **yakalama adımlı** yeni koreografiye gidiyor: kısa fren ayağı → karşı ayak yakalama adımı → ilk geri adım → ölçülü itiş (`SHM231L_LoadRev_F_B_*`, 29/32 faz). e29_load'da üretimin satıcı pivotu (baş ~20 cm çömelik, 0,8 s) yerine dik gövde, 6 cm pelvis emilimi, iki destek adımı. Faz taramasında 6 evrenin 5'i eşit/iyi; **4750 evresinde gerileme** (30 FPS 0 → 23, 20 FPS 0 → 14; §4).
4. **Baş–kol performansı normal hızda karakterimize uygun mu?** Teknik: depar eğrileri artık 0,93–0,98 hızda oynuyor (0,82 idi; V2.30 döngüsünden yeniden pişirildi), eğri girişindeki 17,8 cm sürüklenme 0; V2.30'un `support_slide` 58–96 cm değerleri ölçüm hatası (gerçek 0–3,9 cm). Görsel uygunluk **kullanıcı kabulüne bağlı** (medya §11).
5. **Geçişlerde iskeletin ters/uygunsuz pozlara zorlanması giderildi mi?** **Kısmen.** Giderilen: düşük hızlı geri→ileri (satıcı pivot), depar çıkışı → itiş duruşu, eğimde TIP sonu satıcı dönüş kuyruğu (baş 176 → 37 m/s²), yük altındaki satıcı pivot çömelmesi. Açık: duruştan geri kalkış (AAMS start, 35–38 cm), yürüyüş/tempolu durma kapanış adımı (27–33 cm), yan yürüyüş yön değişimi (c29_combo 48,8), geri çapraz geçişi (33,5) — §5.
6. **Bırak–yeniden bas ve çift ters yön kaymaları düzeldi mi?** Fren evresine göre: erken bırakma (fren, destek yok) 53,8 → **12,2**; yeni itiş başlamışken 18,2 → 8,1 (aday koşusu; üretimde 24,5 kaldı — koşudan koşuya); orta evreler 0 (değişmedi); bırakmada hız 18 cm/s'ye inen durum (gerçek duruş) 35 (AAMS geri kalkış) → AÇIK. j24_dbl 11,3 (iki tekrar aynı). Ayrışma kaynağı §2.1.
7. **Basamakta askıda kalma ve eğimde depar geçişi düzeldi mi?** Yükseliş: önde giden ayak 17,3 → 10,2 cm, iniş 0,30 → 0,10 s (**PARTIAL**: arkadaki ayak 0,5 s ve tempolu değişmedi). İniş: sahip kapsülün kenarda kalması + FP pelvis hızı (**AÇIK**; perch denemesi WRONG_PATH). Eğimde depar: **düzeldi** (176 → 37 m/s², satıcı kuyruğu yok).
8. **Arka çapraz hareket doğal mı?** Sabit −112,5'te basılı ayak kayması yok (RearLeft + OW 22,5°). Kayma −90 → −112,5 **geçişinde** (33,5 cm; OW bükmesi ayak basılıyken değişiyor) → **AÇIK**; 16 yön içeriği gerekliliği kanıtlanmadı.
9. **İnceleme kamerası gerçek maskeleri doğru hedefliyor mu?** **Evet (teknik).** Kimlik `GR_Inspect` etiketi + nesne yolu, odak maskenin kendi mesh merkezi (x 33; V2.30'da sorgu küresi x 58, 25 cm önde), 29 cm aralıklı iki maske ayrı ve yumuşak geçişle, duvar arkası seçim yok, boş nesneye üye çağrısı yok.
10. **Unreal belleği, yeniden başlatmaları ve telemetri depolaması kontrol altında mı?** Bellek: koşu başı medyan **0,15 GB** (p90 0,26), uzun oturumda doğrusal (en yüksek 33,8 GB), bellek koruması yeniden başlatması **0**. Editör açılışı 15 (12 planlı, her biri gerekçeli + 3 motor çökmesi; V2.30: 22). Telemetri: eski sürüm LTP/Evidence **5,86 → 0,73 GB** sıkıştırıldı (doğrulamalı, silme yok), politika kodda. Kalan büyümenin olası sahibi editör günlüğü (koşu başı ~470 SHM telemetri satırı + ~330 komut satırı, ~0,8 MB) — ölçüldü, düzeltilmedi.

## 1. Başlangıç ve koruma
- Okunanlar: `AGENTS.md`, `CLAUDE.md`, V2.30 raporu/değişiklikleri/tabloları, director / human-motion / character-camera / editor-automation / source-control skill'leri, V2.25–V2.30 hafıza notları.
- Doğrulanan proje durumu: UE 5.8; zincir `BP_PBI_Player → BP_GR_Player → BP_Player_MM`; üretim değerleri temiz editörden (`verify_p0.out`). Temizlik sonrası bütünlük sağlam; silinmiş 95 GB yeniden üretilmedi; pre_reauthor kaynakları, aktif klipler, araçlar yerinde.
- Korunan V2.30 kazanımları (son doğrulamada): düşük hız sınıfı 30, RevTurn ±180, klip-bağlı kapsül, IdleGuard (tutuş içinde boşta girişi tüm koşularda 0), tempolu bırak–bas, V2.30 klipleri, yürüyüş kamerası, LTP yan dosyası, atomik iş kuyruğu, ZenServer bekçisi.

## 2. Öncelik 1 — 49 cm/s girişte dönüş (s29_swl12)
### 2.1 Gerçek giriş durumu
W anında −49…−63 cm/s, poz geri **yürüyüş** (`A_LB_Walk_Bwd`). Üretim ailesi 245 cm/s'lik tempolu geri koşudan tasarlanmış: P6'da fren ayağı yerde 2–4 m/s sürükleniyor, klip-bağlı kapsül tasarım hızına bir karede sıçrıyor (−18 → −86 cm/s). İki kipliliğin zinciri: aynı girdili koşular PIE'nin ilk karelerinden mikron düzeyinde ayrışıyor (FeetIK çıkış eğrileri aynı girdiyle iki değer alabiliyor; aynı başlangıçta bile hareket başında `PelvisOffset` 10 µm) → ilk depar pivotunda Rfoot/Lfoot satıcı klibi → geri yürüyüşün farklı evresi → P29 (6,6 cm) ya da P6 (46,5 cm). Elenen sahipler: pawn mesh tick seçenekleri (zaten AlwaysTickPoseAndRefreshBones + URO kapalı), gerçek zamana bağlı mantık (yalnız performans ölçümü). Kaynak bulunamadı → içerik her iki evrede de güvenli olmalı.
### 2.2 Değişiklik
- **İçerik `SHM231S_SlowRev_*`** (16 B_F + 16 F_B; üretim üretecinin üzerinde `gen231_slow.py`): giriş döngüsü yürüyüş, v0 55 cm/s, fren 600 cm/s² (~3 cm'de durur). Koreografi: **destek ayağı yerinde frenler ve iter**, salınımdaki ayak doğrudan yeni yöndeki ilk adım olur (jog tasarımındaki ayrı fren adımı bu hızda anlamsız: dry-run'da 7–14 cm sürüklenme, 35 cm diz uzaması). Kalite kapısı (kutu başına sürüklenme < 3 cm, IK < 8 cm) tüm kutularda geçti. r2 denemesi (destek ayağı inerken havada sabitlenmesin) B_F'yi değiştirmedi, F_B'yi bozdu (5–37 cm) → kapı tarafından **yazılmadı**, r1 üretimde.
- **Yönlendirme**: epizot 90 cm/s altında başlıyorsa yavaş aile. Tuzak: istek karesinde (V2.24 EarlyRev) bileşen epizodu yok, `RedirectSpeed0` önceki epizodu (424) veya 0'ı tutuyordu → ilk denemede yol hiç çalışmadı / ilk tempolu dönüşte yanlışlıkla yavaş aileyi seçti; düzeltme: epizot yokken o anki hız.
### 2.3 Sonuç (pencere / tüm koşu en kötü, cm)
| FPS | Üretim (V2.30 yolu) | V2.31 |
|---|---|---|
| 20 | 23,2 | 17,1 |
| 30 (3 tekrar) | 20,3 (P6) / 13,0 (P29) | 11,6 / 8,8 / 11,6 |
| 60 | 55,3 | 44,2 (F60) / 20,7 ×2 (S3b) |
| 120 | 12,2 | 12,0 |
| gerçek zaman | 25,8 | 10,2 |
60 FPS kötü evresi: kaynak satıcı pivot → geri yürüyüş karışımı, sağ ayağın iniş anına denk geliyor; yeni klibin destek ayağı başka yerde → 3 kare 4–6 m/s → **PARTIAL**.

## 3. Öncelik 2 — yüksek FPS'de eforlu dönüş kayması
- **Sahip**: depardaki her yazılmış B_F çıkışı V2.14 “dönüş sonrası itiş penceresine” (`PSD_SHM214_RevPush`: satıcı pivotu sonrası itiş duruşu kopyaları) düşüyordu; klip itişi zaten yapmış → ikinci itiş duruşu, başka ayak evresi (tüm FPS'lerde 12–42 cm). 60/120 FPS'te tutuş bir sonraki S'den bir kare önce bitti → MM 2 kare RevPush → yeni F_B girişi o pozdan (h60 e29_load 36,9). Kare hızının etkisi = tutuş bitişinin girdiye göre bir kare kayması.
- Yalnız pencereyi kapatmak (aday A1) `PSD_RR_Start`'ı (duruştan kalkış) adım ortasında açtı (57–71 cm) → yazılmış klipten sonra pencere tempolu→depar itişine (`PSD_SHM218_JogPush`, J2S) yönlendirildi (`exit`).
- İki deney: (1) aynı gerçek zamanlı girdi 20/30/60/120 + gerçek zaman; (2) aynı fiziksel giriş: `e31_s2_<ms>` ikinci S zamanını 50 ms adımla tarar.

| Senaryo (pencere cm) | 20 o→V2.31 | 30 o→V2.31 | 60 o→V2.31 | 120 o→V2.31 | gerçek z. o→V2.31 |
|---|---|---|---|---|---|
| e29_load | 11,6→11,6 | 6,3→0 | 36,9→0 | 29,4→19,7 | 11,2→0 |
| e29_recov | 20,0→11,6 | 7,1→0 | 36,9→0 | 29,4→21,1 | — |
| e29_chain | 17,8→5,1 | 26,9→25,4 | 14,3→**26,1** | 66,1→33,5 | — |
| e31_s2_4750 | 0→**13,6** | 0→0 | 0→0 | 0→0 | — |
| e31_s2_4900 | 8,1→9,0 | 17,6→11,7 | 18,9→13,6 | 29,3→6,5 | — |
- FootPlacement'a müdahale edilmedi; bu sürümün kaymaları seçim/çıkış zincirinden geliyor (FP kör kapatılmadı).

## 4. Eforun bedensel karşılığı
- V2.30 yük ailesi: aynı koreografinin zamanda gerilmesi → görünür fark yok; yöntem çoğaltılmadı.
- **Yakalama adımlı yük dönüşü** (`gen231_loaded.py`): (1) fren ayağı durma noktasının 22 cm gerisine iner, beden üzerinden geçer (540 cm/s²); (2) karşı ayak durma noktasının 6 cm ötesine **yakalama adımı**, pelvis 4 cm emer, karşı eğim 6°; (3) ilk geri adım fren ayağıyla; (4) ölçülü itiş 150 cm/s² (üretim 198). Önce tek temsilî dönüş (e29_load ikinci dönüş, F_B 290 cm/s, P12) doğru tamamlandı; sonra 32 faz: r1 17/32 kapıdan geçti, r2 (destek ayağı bacak boyu dolunca kalkar; döngüde inen ayak indiği yerde sabitlenir) 29/32.
- Oyunda (sabit 30, e29_load): üretim → V2.14 RevPush + satıcı koşu pivotu (baş 128–131 cm, 0,8 s çömelik); V2.31 → fren 0,55 s, fren ayağı 7,00 s, yakalama 7,33 s, ilk geri adım 7,80 s, pelvis ~6 cm, baş 144–152 (dik), 0,85 s'de −121 cm/s.
- Rastgelelik yok: tetik yalnız `EffortEUse` ≥ 0,45 + F_B dönüş. Normal yürüyüş / tek dönüş / dinlenmiş manevra etkilenmiyor (e29_rest 13,1 = 13,1).
- Kalan: 4750 evresi (fren ayağı karışım sırasında tasarımdan erken iniyor) 20/30 FPS'te 14–23 cm; 3 faz kutusu (P21/P29/P30) hâlâ kapı dışında.

## 5. Geçişlerin fiziksel sürekliliği
`trans231.py` (her klip değişiminde 0,35 s: basılı ayak sürüklenmesi, gövde burulma hızı, baş ivmesi). Liste: idle→yürüyüş 6,5 cm; yürüyüş→tempolu/tempolu→depar 5,9; depar→duruş 0; duruş→yürüyüş 0; fren→yeniden itiş 16,7 → 15,0; sert dönüş→sert dönüş 8–27. Ters/uygunsuz poz düzeltilenler §0-5. Açık kalanlar ve sahipleri:
- Duruştan geri kalkış (`SHM_JogQ_af_Loco_Jog_Bwd_Start_AAMS`): ilk karelerde kapsül CMC ile ivmelenirken klip ayakları basılı tutuyor, iki ayak birlikte 80–145 cm/s ve zeminin 5 cm altında → 35–38 cm (j30_slow, j30_rel_3200/3400/3450).
- Erken bırakmada yazılmış frenden yürüyüş-durma klibine geçiş fren ayağını sürüklüyor (20 FPS / gerçek zamanda 40–53 cm; 30'da 12).
- Yürüyüş/tempolu durma kapanış adımı zemine sürtünüyor (27–33 cm); yan yürüyüş yön değişimi (c29_combo 48,8); duruştan yürüyüş kalkışında iki ayak birlikte sürükleniyor (e29_recov sonu 30,6).
Yalnız karışım süresi uzatılmadı; çözülenler kaynak sahibinde (içerik / seçim / çıkış rotası) düzeltildi.

## 6. Depar, baş, omuz, kol
- **Eğriler**: V1.3.9'da eski uzun adımlı döngüden “MM oranı 0,813” varsayımıyla pişirilmiş, `rate_scale` 0,813 ayarlanmıştı; V2.30 döngüyü düzeltti ama eğriler eski kaldı. V2.31: V2.30 döngüsünden RATE 1,0 ile yeniden pişirildi (ayak hatası 0), `rate_scale` 1,0; oyunda oynatma 0,82 → 0,93–0,98; eğri girişi sürüklenmesi 17,8 → 0 (d_sprint). Üst gövde izleri (V2.30 salınım azaltması) korundu.
- **`support_slide` denetimi**: V2.30 ölçüsü 58–96 cm; temas-tabanlı gerçek kayma aynı kliplerde 0–3,9 cm → **ölçüm hatası** (depar uçuş evresi %71; “alçak ayak” salınım ayağını sayıyor).
- Baş/omuz/kol genliği V2.30 değerlerinde; son görsel kalite kullanıcı kabulüne bağlı.

## 7. Bırak–yeniden bas ve çift ters yön
| Bırakma evresi (görünür ayaklar) | bırakma s | Üretim V2.30 | V2.31 |
|---|---|---|---|
| fren, destek yok | 3,10 | 53,8 (duruş → AAMS kalkış) | **12,2** (duruş → yavaş F_B) |
| fren, destek yok | 3,20 | 35,0 | 35,0 (yeniden basışta 18 cm/s: gerçek duruş → AAMS kalkış, §5) |
| fren, destek yok / fren ayağı basılı | 3,25 / 3,30 | 0 / 0 | 0 / 0 |
| hız sıfıra yakın | 3,35 / 3,40 | 0 / 29,2 | 0 / 29,2 |
| yeni itiş başlamış | 3,45 | 24,5 | 24,5 (aday koşusunda 8,1) |
Değişiklik `fwdrev` + `slow`: tempolu kipte ileri giderken de düşük hız dönüş sınıfı → epizot + klip-bağlı kapsül + tutuş + yavaş F_B. Zaman penceresine tolerans eklenmedi. j24_dbl iki tekrar 11,3 / 11,3.

## 8. Kamera inceleme sistemi
- V2.30 gerilemesi doğrulandı: kimlik = görünen addaki `INS_`/`Mask`, odak = sorgu küresinin sınır merkezi (maskenin 25 cm önü).
- V2.31 (`inspect`): kamera fonksiyonu yalnız isabet bileşenini saklar; `SHM231_InspectResolve` (IsValid dallı yürütme grafı, `SHM_Tick`'te kameradan hemen sonra): `GR_Inspect` (bileşen veya aktör) → kimlik = sahibin nesne yolu, odak = sahibin kök mesh sınır merkezi. Kamera bunu bir kare sonra, yalnız aynı nesne için (yol eşitliği) kullanır; sorgu küresi merkezi ile görsel odak ayrı.
- Gerçek R05 maskeleri (üretim): odak x 33 (mask), y 315 / 344 iki maske ayrı; kısa bakış kaymasında odak maskede kalıyor; maskeden maskeye geçiş yumuşak (344 → 338 → 334 → 330 → 327); QA feneri aynı; mandal zamanı aynı (tanıma 1 kare geç).
- Doğrulayıcı: V2.26 (`ActorHasTag`) ve V2.28 (`InspectFocusMode` 1) kalemleri yeni sözleşmeyle süperseded, açıkça gerekçeli filtrelendi; V2.31 kalemi çözücü + IsValid + tick çağrısı + kamera okuması + DSL'de üye çağrısı yok'u denetler.

## 9. Arazi, eğim, arka çapraz
- **30 cm yükseliş**: CMC kapsülü 0,13 s'de 28–30 cm yükseltiyor; kapsül-göreli salınım kaldırması yalnız tau 0,12 ile sönüyordu → önde giden ayak basamağın 17 cm üstüne çıkıp 0,30 s asılı. `steplift` (kaldırma o karedeki kapsül yükselişi kadar düşer): 17,3 → 10,2 cm, iniş 0,30 → 0,10 s. Arkadaki ayak 17–18 cm / 0,5 s, tempolu 20–25 cm → **PARTIAL**.
- **İniş**: kapsül kenarın 37 cm ötesine kadar üstte kalıp tek karede düşüyor; öndeki ayak ancak FP pelvisi indirdiği hızla iniyor (38 → 2 cm, 0,5 s). Baş inişi 33–35 cm ≈ geometrik düşüş 30 cm + ~3–5 cm animasyon; ivme 21–27 m/s² (çoğu geometrik). CMC perch (22 / 40) zamanlamayı değiştirmedi → WRONG_PATH. **AÇIK**.
- **Eğimde depar**: TIP montaj sonu karesinde hız 0, ABP ailesi bir kare geride → orijinal seçici satıcı depar-dönüş kuyruğunu 1 kare oynatıyordu (baş 29 / 18 / 16 cm). `tipend`: 176 → 37 m/s² (iki tekrar), satıcı kuyruğu yok; s29_cam değişmedi.
- **Arka çapraz −112,5**: sabit durumda kayma yok; sürüklenmeler (33,5) geçişte (OW bükmesi ayak basılıyken değişiyor + Left→RearLeft) → **AÇIK**, 16 yön içeriğine ihtiyaç kanıtlanmadı.
- Gerçek ev–orman rotası (`map_r1`): oynatıldı ve yakalandı; sınıflandırıcı değişken zeminde geçersiz (zemin yüksekliği rota boyunca değişiyor) → ölçü değil görüntü.

## 10. Unreal bellek, otomasyon, telemetri
- **Bellek**: 300 örnek; koşu başı medyan 0,15 GB, p90 0,26; uzun oturum doğrusal (en yüksek 33,8 GB, koruma eşiğinin altında); bellek koruması yeniden başlatması 0. V2.30 onarımları (LTP yan dosyası, güvenli sonda) korunuyor. Kalan büyümenin olası sahibi editör Output Log metni: koşu başı ~470 SHM telemetri satırı (`LogBlueprintUserMessages`, evidence.py bunları günlükten okuyor) + ~330 `Cmd:` satırı (~0,8 MB). Ölçüldü; taşınması bileşen telemetri değişikliği gerektiriyor → bu sürümde yapılmadı.
- **Editör açılışları (15)**: s1 (başlangıç doğrulaması), a2b (çökme sonrası yanlış kip → geçersiz koşuların tekrarı), b1a (DA alanı + bileşen değişkenleri), b1b (fonksiyon derlemesi ayrı editörde — profiller+fonksiyonlar tek editörde OOM kuralı), f60 / f120 / f20 / frt (FPS bir açılış argümanı), s3 / s3b (yavaş aile kontrolü 30 / 60), fin (terfi), finv (temiz yeniden açılış doğrulaması) + **3 motor çökmesi** (`Assertion failed: GameViewport.IsUnique()`, SLevelViewport.cpp:5196, PIE sonu; ~1/120 koşu). Hazır olma medyanı 128 s, toplam ~32 dk.
- **Otomasyon arızaları ve kalıcı onarımları**: (a) çökme sonrası otomatik yeniden açılış sabit adımsız açıyordu → bir A/B tamamen değişken adımda koştu (yakalandı, tekrarlandı); kip artık korunuyor (`RELAUNCH_ARGS`), her koşuda `FPSCHECK` (sonraki 2 çökmede kip korundu, kayıp koşu tekrarlandı). (b) İstek düzeyi anahtarlar (`live_cm`) `abp_flags` içine düştü → qa_pie PIE'ye başlamadan düştü, harness 900 s bekledi → `qa.sh` hızlı çıkış (`QA_JOB_FAILED`). (c) Yürütme pini yeniden bağlarken `disconnect` tüm kaynakları siliyordu (2 kez üretim yolu etkilendi: V2.14 pencere dalı, PerfLapCam ELSE) → yakalandı, onarıldı, kural: her bağlama öncesi/sonrası exec kaynakları yazdırılır. (d) `build_funcs` hatası fonksiyonu bellekte boş bırakıyor → kaydetmeden aynı editörde yalnız o fonksiyon yeniden derlendi.
- **Telemetri depolama**: `retention231.py` (sürüm sınıfı FINAL / CURRENT / TEMP; eski sürümler gzip, arşiv geri okunarak doğrulanır, FINAL asla silinmez, TEMP sıkıştırılmış 30 gün sonra silinebilir, boyut tavanı). Uygulandı: 6 735 kayıt, 5,86 → 0,73 GB, silme 0. V2.31'in kendi ham kayıtları (~4 GB) şimdilik açık (raporun tabloları onlardan); bir sonraki sürümde politika V2.30'u sıkıştırır.
- **Kademeli test**: hızlı (tek senaryo + karşı örnek, aynı editör), aday (A1–A3, B1–B2: ilgili aile + varyantlar), son (FPS 20/60/120 + gerçek zaman, üretim kanıtı, medya). Kayıtlı 355 PIE koşusu (medyan 32 s, toplam 14 443 s ≈ 4 sa), 14 planlı editör açılışı + 3 çökme sonrası yeniden açılış (hazır olma medyanı 128 s), bellek nedenli yeniden başlatma 0; zincir 14:19 → 20:50 (editör 20:52 kapatıldı, `revert_quit`: kirli paket yok).

## 11. Nihai testler ve medya
- Üretim kanıtı (temiz editör, sabit 30, 43 koşu): `data/tables231_fin.txt`; V2.30 üretimiyle karşılaştırma `data/tables231_before_after.md`; FPS özeti `data/tables231_fps_summary.md`. Zorunlu 10 akışın hepsi koşuldu ve yakalandı (`vid/`: 22 GIF + gerçek zamanlı AVI çifti — sakin akış yan/oyun, düşük hız geri→ileri önce/sonra/oyun, depar zinciri yan/oyun, yüklü dönüş önce/yakalama adımı, dinlenmiş dönüş, erken bırak-bas önce/sonra, eğim deparı önce/sonra, depar+kamera 180, depar eğrileri, geri çapraz yürüyüş, 30 cm basamak önce/sonra, inceleme maskeleri önce/sonra, gerçek ev rotası).
- Aynı girdi zamanı (20/30/60/120/gerçek zaman) ve aynı fiziksel giriş (`e31_s2` taraması) ayrı tutuldu.
- Tetiklenmeyenler: CMC perch adayı basamakta etkisiz → WRONG_PATH; belirlenimcilik adayı (`live_anim`) zaten aynı ayarlar → NOT_TRIGGERED. Hiçbir “0 hata” tetiklenmemiş bir davranıştan yazılmadı.

## 12. Teslim: üretimde / aday / açık
| Başlık | Üretimde ve doğrulandı | Aday, kabulü geçmedi | Açık ve neden |
|---|---|---|---|
| Düşük hız girişi | `slow` (30 FPS her iki evre ≤ 11,6; gerçek z. 10) | slow r2 içerik (kapı: F_B bozuldu) | 60 FPS kötü evre 21–44 (kaynak karışımının iniş anı) |
| FPS eforlu kayma | `exit` (60 FPS 36,9 → 0, 120 66 → 34) | A1 (yalnız pencere kapatma: kalkış klibi) | e29_chain 60 tek koşu 26; 120'de 20–21 cm kalan |
| Efor | `loaded` (yakalama adımı, 29/32 faz) | r1 aile (17/32) | 4750 evresi 14–23 cm; P21/P29/P30 kapı dışı |
| Geçişler | düşük hız / depar çıkışı / TIP sonu / yük pivotu | — | AAMS geri kalkış, durma kapanış adımı, yan yön değişimi, duruştan kalkış |
| Depar | eğriler RATE 1,0 (0,93–0,98) | — | görsel kabul |
| Bırak–bas | `fwdrev` (erken bırakma 53,8 → 12,2) | — | gerçek duruşta AAMS kalkış; erken bırakmada duruş klibi sürüklemesi (20 FPS / gerçek z.) |
| İnceleme | `inspect` (mask odağı, etiket kimliği) | — | — |
| Basamak | `steplift` (öndeki ayak 17 → 10 cm, 0,3 → 0,1 s) | CMC perch (WRONG_PATH) | iniş askıda kalma, arkadaki ayak |
| Eğim | `tipend` (176 → 37) | — | — |
| Arka çapraz | — | — | geçiş sürüklenmesi 33,5 |
| Bellek/otomasyon | kip koruma, FPSCHECK, qa hızlı çıkış, retention | — | günlük metni büyümesi (0,15 GB/koşu) |

Teknik kabul satırları yukarıdaki gibidir. **Görsel / oyun hissi kabulü: NOT_ACCEPTED_YET (kullanıcıya ait).** Kayma azaldı diye arcade tavrı kabul edilmiş sayılmadı.

Kayıt ve doğrulama: terfi taze editörde (`promo_fin.out`: yedi grup, kirli paket yok), temiz yeniden açılışta `verify_fin2.out` **VERIFY231 ALL_OK**. Geri alma: `promote231.py {'rollback': True}` + editör kapalıyken `checkpoint/pre_v231` (eğri klipleri dahil).
