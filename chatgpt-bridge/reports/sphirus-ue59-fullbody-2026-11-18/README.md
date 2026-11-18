# SPHIRUS UE 5.9 — yokuş, dönüş/duruş, iç mekân güneşi (2026-11-18)

Başlangıç referansı: `sphirus-ue59-fullbody-2026-11-17` (commit `bde3ce7`). Çalışma kopyası `Documents\Unreal Projects\sphirus_UE59` (UE 5.9.0, CL 60351404).
Orijinal 5.8.4 projesine ve kullanıcının asıl kayıt dosyasına dokunulmadı; test kaydı her koşudan sonra SHA1 `4823d83a…`.

Durum etiketleri: **UYGULANDI** (kalıcı yazıldı) / **TEKNİK TEST** (ölçüldü) / **GÖRSEL** (kareler ya da video incelendi) / **PERFORMANS** / **AÇIK**.
**Kullanıcı kabulü hiçbir madde için yok.** Videolar gerçek hızda (30 fps sabit oyun adımı) kaydedildi; ben yalnız kare dizilerini
inceleyebildim, akıcılığı ve oynanış hissini gerçek hızda izleyip onaylamadım.

## 0. Başlangıç durumu (çalışan projeden okundu)

| Alan | Değer | Kaynak |
|---|---|---|
| Harita / oyuncu | `L_GR_SphirusHouse` / `BP_HybridA_Player` | editör |
| Profil | C, ileri-yalnız eşleme (fwd=3, 34 veritabanı eşlemesi), PivotAroundBall | `data/state_after_w18.txt`, `profile_req.json` |
| Hızlar | yürüyüş 180/170/150, jog 415/350/300, sprint 585 | CDO |
| Kayıtlı ayar | `{"profile":"C","plant":"PivotAroundBall","fwd":3,"run_speed":415}` | değişmedi |

Korunanlar: ileri klip seçimi, yürüyüşte kol dengesi (kol salınımı 40/42 cm, karşı faz korunuyor), odun–şömine akışı (bkz. §7).
**Korunamayan bir kazanım bulundu:** önceki turdaki "jog 415'te koşu duruşu" bu derlemede yeniden üretilemiyor (§4.3).

Bu tura özgü engel: Windows Akıllı Uygulama Denetimi (Code Integrity 3077, hata 4551) bugün 5.9 kopyasındaki yerel derlenmiş
`UnrealEditor-Black_Eye_Editor_Bootstrap.dll`'i engelledi; editör açılmıyordu. Güvenlik ayarına dokunmadım ve engellenen DLL'i
yükletmeye çalışmadım. Bu modül yalnız Sequencer varsayılan iz ayarlarını bir ini dosyasına yazıp bir film formatı ön ayarı ekliyor; oynanışla
ilgisi yok. 5.9 kopyasındaki `Black_Eye.uplugin`'den yalnız bu modülü çıkardım (oyuncu kamerası Black_Eye runtime/editor modüllerini
kullanıyor, onlar engellenmiyor). Geri dönüş: `Saved/UE59Work/checkpoints/20261118_blackeye/Black_Eye.uplugin.orig`. Nwiro DLL'i bir açılışta
aralıklı engellendi, sonraki açılışta yüklendi.

## 1. Ölçüm güvenilirliği (önce düzeltildi)

| Sorun | Kök neden | Düzeltme | Durum |
|---|---|---|---|
| 45/90/135/180° yerine 48/96/144/192° | Test sürücüsü 0,25 s'yi 30 Hz'de 8 kareye yuvarlayıp kare başına hız×1/30 ekliyordu; karakter istenen 48°'yi uyguluyordu | Segment `round(süre×fps)` kare, toplam açı tam `hız×süre`; satıra istenen yaw (`yreq`) yazılıyor; analiz istenen / kapsül / hız yönü açısını ayrı veriyor | TEKNİK TEST: yeni kayıtlarda 45/90/135/180 = uygulanan = hız yönü |
| Durağan pozda kadans 60000 | İki iniş aynı karede → bölen 1e-3 s | <30 cm/s, <3 iniş ya da <0,5 s'de kadans **N/A** | TEKNİK TEST |
| Geri yürüyüşte 359,6° / 710,4° | Kalça çizgisi açısı ±180'de sarıyordu | Açılar dairesel ortalama etrafında açılıyor (geri yürüyüş: 359,6 → 13,7°, 710,4 → 27,9°) | TEKNİK TEST |
| Odun kayıtlarında `Failed to find property 'Idle'` | Kaydedici ABP'de olmayan `Idle` alanını okuyordu; oyun hatası değil | Bayraklar tek tek okunuyor, olmayan alan `None` | TEKNİK TEST |
| Ayak teması "yatay hız < 60" ile tanımlıydı (kayan ayak sayılmıyordu) | — | Temas = topun/bileğin **kendi altındaki izlenen zemine** yüksekliği + dikey hız; yatay hız sınırı yok; kayma ve "temasta >60 cm/s oranı" raporlanıyor | TEKNİK TEST: düz yürüyüşte çift destek artık 0,14 (eski kural 0,00 veriyordu, yürüyüşte imkânsız) |
| `turn_sev` en çok 0,21 | Sinyal yalnız girdi–hız açısı farkını ölçüyor; karakter hızla döndüğü için fark çok kısa sürüyor | Hedef = max(eski terim, hızla ölçeklenmiş yön değişim hızı `TurnW` 30–240°/s) | UYGULANDI, TEKNİK TEST: yürüyüş 0,30, jog/sprint 0,80 |
| Kalça yüksekliği tek referansla | — | Her karede zemin izleri (iki top, iki bilek, kapsül merkezi), kapsül yarı yüksekliği, çarpılan bileşen; kalça **zemine**, **alçaktaki ayağın zeminine** ve **kapsül tabanına** göre ayrı; oyuncu kamerasında baş/pelvis ekran konumu | TEKNİK TEST |

Kayıt satırlarına profil, gait, klip, veritabanı, hız, kamera ve görünüm sabit yazılıyor. Veri koşuları 60 Hz sabit oyun adımı (ekran görüntüsüz),
videolar 30 Hz. Araçlar: `changes/vidm_patch.py`, `an_bio2.py`, `an_slope2.py`, `an_hip2.py`, `an_stop.py`, `an_turnslide.py`.

## 2. Yokuş (birinci öncelik)

### Kök neden (katman katman, aynı kayıtta)
1. **Görünen zemin – çarpışma:** kapsül altındaki iz landscape heightfield (görünür zeminle aynı yüzey). Sorun değil.
2. **Kapsül tabanı:** `CharacterMovement.bUseFlatBaseForFloorChecks = True` (GASP örneğinden geliyor). Düz tabanlı kapsül eğimde yokuş yukarı
   kenarına (merkezden 30 cm) oturuyor: kapsül tabanı merkezdeki zeminin 9,5 cm (9°) – 17,7 cm (29°) üstünde, tam r·tanθ. Görünür gövdenin kökü
   kapsül tabanında; ayak yerleşimi pelvisi aşağı çekerek telafi ediyor. **Önceki raporun "85 → 63 cm" çöküşü bu havada kapsül tabanına göre ölçülmüştü.**
3. **Pelvis gerçekte:** zemine göre 85 cm (düzde 92–95); alçaktaki (arka) ayağa göre 90–91 cm, yani destek bacağı neredeyse tam boyda. Kalan alçalma
   geometrik: arka ayak merkezdeki zeminden ~14 cm aşağıda.
4. **Kaynak klip / hız:** düz zemin yürüyüşü aynı adım uzunluğu ve hızla yokuşa taşınıyor; ön ayak IK ile ~26 cm kaldırılınca ön diz 95–111°'ye katlanıyor.
5. **Gövde:** yokuşa hiç tepki yok (eğim +0,2…+2°).
6. **Foot Placement pelvis modu** (`AllLegs`, motorun düz zemin önerisi): eğim modu (`FrontPlantedFeetUphill_FrontFeetDownhill`) denendi → BAŞARISIZ (diz değişmedi, hafif eğimde pelvis çukuru 80 → 64 cm), bellekte geri alındı, kaydedilmedi.

### Uygulanan (mevcut sahiplerin içinde, paralel sistem yok)
- `BP_HybridA_Player`: `bUseFlatBaseForFloorChecks = False` (yalnız oyuncu; GASP üst sınıfı değişmedi).
- `AC_Sph_Motion` (Graph DSL ile, 5.9'un desteklenen yolu; Python grafik yardımcıları bu derlemede yok):
  - `SlopeDeg`: kapsülün hareket yönündeki eğimi (yerde, >40 cm/s, yumuşatılmış).
  - Mevcut `EffLean` (görünür gövdede omurga eğimi, %40 spine_03 / %60 spine_05) hedefine eğim terimi: yokuş yukarı 0,55°/°, en çok 12°; aşağı 0,15°/°, en çok −3°;
    hızla ölçekli (durunca %35).
  - Mevcut `SpeedScale` hedefine eğim yavaşlaması: 6°'den itibaren, 25°'de yukarı %25, aşağı %12. Düzde hız değişmiyor.
  - `SlopeOn` ve katsayılar örnekte ayarlanabilir.

### Eşlenmiş önce/sonra (aynı rota, girdi, kamera; "önce" = aynı derlemede çalışma anında düz taban + eğim kapalı)

| Eğim bandı (hareket hâlinde) | Hız | Pelvis zemine (ort / en düşük) | Pelvis alçak ayağa | Yukarıdaki diz | Baş/gövde öne eğimi | Kapsül boşluğu |
|---|---|---|---|---|---|---|
| Dik yukarı 15–40°, önce | 180 | 85,0 / 69,8 | 90,6 | 111° | +1,3° | 15,7 |
| Dik yukarı 15–40°, sonra | 154–165 | 87,1 / 75,8 | 91,1 | 116° | +5,9° | 5,7 |
| Hafif yukarı 6–15°, önce → sonra | 162 → 170 | 90,8 / 79,8 → 91,4 / 83,0 | 93,4 → 93,1 | 138 → 140° | +2,1 → +2,8° | 5,7 → 2,2 |
| Dik aşağı (jog), önce → sonra | 398 → 369 | 91,9 / 79,4 → 90,7 / 81,1 | 92,6 → 91,9 | 117 → 119° | ≈ aynı | 15,0 → 4,8 |

Kamera (oyuncu kamerası): düz yürüyüşte en büyük dikey ivme 3391 → 381 cm/s² (kapsül basamak sıçramaları kalktı), dik yokuş yukarıda kamera–baş yüksekliği
oynaması 20,3 → 13,1 cm, başın ekran konumu oynaması 0,19 → 0,13. Dik yokuş aşağı jog'da değişmedi (33 → 36 cm).
Veri: `data/slope_before_after.txt`, `data/slope_candidates.txt`, `data/slope_S*.txt`, `data/floor.txt`, `data/fp_node.txt`.

Durum: UYGULANDI, TEKNİK TEST. GÖRSEL: video kareleri incelendi (bkz. §8). **AÇIK:** dik yokuş yukarı ön diz hâlâ ~116° (adım uzunluğu kaynak klipten geliyor;
yokuşa özgü klip ya da adım ölçekleme bu turda yok); yokuş aşağı gövde tepkisi küçük (−3° sınırı).

## 3. Evdeki beyaz kırpılma (üçüncü öncelik, ama uygulandı)

### Teşhis (dünkü teşhis düzeltildi ve kesinleşti)
- Dünkü "yerel pozlama vurgu kontrastı işe yaramıyor" sonucu **geçersizdi**: ayar görüntüyü etkilemeyen hacme (`PostProcessVolume_18`, ağırlık 0) uygulanmıştı.
- Görüntünün sahipleri: `PostProcessVolume_0` (sınırsız, otomatik pozlama histogram, EV −1…10, ton eşleme XR5 ayarları), **`PostProcessVolume_15` "EX_Look_PPV_House"** (evin içi, öncelik 2, pozlama ofseti −0,30 — iç mekânda genel hacmin ofsetini eziyor), kameralarda pozlama geçersiz kılması yok; güneş `DirectionalLight_0` 1250, yumuşak açı 8°. (`data/light_owner_indoor.txt`, `data/ppv_full.txt`)
- Güneş 1 ya da 0,01 → leke yok; 100 → hâlâ neredeyse beyaz. Düz gri motor küresinin güneşli yüzü de kırpılıyor (`evidence/light_05_neutral_sphere_check.jpg`).
  Yansıma, saç, temas gölgesi, mesafe alanı gölgesi, donanım ışın izleme, VSM, yerel pozlama kapatılınca leke kalıyor (`light_03`, `light_04`).
- **Sonuç:** iç mekân lambaları düşük; otomatik pozlama iç mekânı alt sınıra yakın açıyor; pencereden giren doğrudan güneş oda orta grisinin ~10 kademe üstünde.
  Ton eşleme / yerel pozlama 1–2 kademe kurtarabiliyor (`light_01`, `light_02`, `light_06`): leke küçülüyor ama renksiz beyaz kalıyor, oda kararıyor.
  Gürültülü kenar, güneşin 8°'lik yumuşak açısının sanal gölge haritası yarı gölgesi.

### Uygulanan
- Yeni ışık fonksiyonu malzemesi `/Game/Sphirus/Lighting/Day_20261118/M_Sph_SunInterior_LF`: güneş çarpanı = 1, evin iç kutusunda (x 50–1472, y 40–1100, z 120–1000;
  duvar düzlemlerinin içinde, 15 cm yumuşak kenar) `InsideK = 0,02`. Dış cepheler, saçak ve dış dünya kutunun dışında: çarpan 1.
- `DirectionalLight_0`'a atandı; `L_GR_SphirusHouse` kaydedildi. Güneş şiddeti, yönü, gökyüzü, pozlama hacimleri ve XR5 ton ayarları **değişmedi**.

| Aday | Kırpılan piksel (omuz/kol bölgesi) | Oda ortalaması | Karar |
|---|---|---|---|
| Mevcut | %2,52 | 0,377 | — |
| Vurgu kontrastı 0,4 / eşik / bulanık karışım (genel hacim) | %0 (ölçüt) ama gözle hâlâ beyaz | 0,32–0,35 (oda kararıyor) | Reddedildi |
| İç hacimde yerel pozlama + ofset −0,9 | gözle küçük ama beyaz | 0,26–0,29 | Reddedildi |
| Güneş 800 / 600 (genel) | lekede fark yok | ≈ aynı | Reddedildi (dışarıyı değiştirir) |
| İç mekân pozlama alt sınırı 1,5 / 3,5 | — | 0,18 / 0,10 | Reddedildi |
| İç güneş ×0,25 / ×0,12 / ×0,06 | %0,01 / %0 / %0, gözle hâlâ parlak beyaz | 0,374–0,376 | Yetersiz |
| **İç güneş ×0,03 / ×0,015** | ten rengi ve biçim okunuyor, güneş hâlâ belirgin | 0,377 | **0,02 seçildi** |

Kanıt: `evidence/light_07…`, `light_08…` (omuz yakın kırpım), `light_09_room_before_after_k015.jpg` (oda ve pencere dışı korunuyor).
Hareketli kontrol: §8'deki `videos/light_patch_*` (lekeye girip çıkma) ve `videos/light_exit_*` (mutfak arka kapısından dışarı).
Durum: UYGULANDI, TEKNİK TEST, GÖRSEL (kare). **AÇIK:** yarı gölge gürültüsü (güneş yumuşak açısı 8°) dış görünümü etkilediği için değiştirilmedi.

## 4. Keskin dönüşler ve duruşlar (ikinci öncelik)

Tam açılı testler (düz harita, yan kamera, kaydedilmiş durum). `data/turns_exact_angle.txt`, `data/turns_walk_foot_slide.txt`, `data/stops.txt`.

### 4.1 Yürüyüş sola 180°
- Önceki 12,4 cm yanal sapmanın bir kısmı 192°'lik ölçüm hatasıydı; tam 180°'de 5,8 cm (düz ±3,3).
- Kayma gerçek: iki ayak temasta ~35'er cm (anlık 240–270 cm/s); sağa 180°'de 3 + 17 cm. Zincir `Walk_Turn_L_090_Lfoot → (0,07 s sonra) Walk_Turn_L_180_Lfoot`:
  MM 90° klibine girip hemen 180° klibine atlıyor.
- Denenen (çalışma anı): Relaxed dönüş klipleri (toplam kayma 224 → 296 cm, kötü), ayak kilidi açılma açısı 60 → 90° (212 cm), bilek burulma azaltımı 0,75 → 0,4 (214 cm). Hiçbiri anlamlı değil; uygulanmadı.
- **AÇIK.** Sonraki somut adım: `PSD_Sph_N_Walk_F_Turns` (Sphirus kopyası) için devam eden poz maliyet yanlılığı ya da 90→180 geçişini engelleyen seçim kuralı; birden çok adım fazında ölçmek.

### 4.2 Jog 90/135/180°
- 90°: yanal 12–13,5 cm, çökme 7,6 cm, yerleşme ~0,5 s. 135/180°: yanal 13–16 cm, çökme 15–21 cm, yerleşme 0,7–1,4 s, hız 415 → 150–290.
- Aday: jog dönüş/pivotları Neutral kliplere (çalışma anı) → yanal 15–20 cm, daha kötü; uygulanmadı. Relaxed pivot klipleri korunuyor. **AÇIK.**

### 4.3 Duruşlar
- Yürüyüş duruşu 7 cm, toparlanma 0,7 s; kısa tuş dokunuşları (0,15/0,3/0,6 s) 4–8 cm. Değişmedi.
- **Jog (415) duruşu:** bu derlemede 30, 36 ve 60 Hz adımda, 8 farklı bırakma fazında ve bu turun değişiklikleri çalışma anında geri alınmışken bile
  her seferinde `M_Relaxed_Sprint_Stop` seçiliyor, pelvis 29–32 cm çöküyor. Önceki turun (v5) "Run_Stop" sonucu yeniden üretilemedi; yavaşlama eğrisi v5 ile aynı (415→0, 0,75 s, ~155 cm).
  Kök neden: Chooser'ın durma satırı (`CHT_Sph_PoseSearchDatabases_Relaxed`, satır 0) gait'ten bağımsız bütün duruş veritabanlarını birlikte açıyor; 415'ten durma eğrisine sprint duruşu daha iyi uyuyor. 415 hız ayarı eşikteydi.
- Aday: sprint duruşlarını Dense (Neutral) veritabanına eşlemek. Jog duruşunda çöküş ~26 → ~19 cm, toparlanma kısaldı, **ama temasta ayak kayması ~39 → ~89 cm**.
  Takas olduğu için kalıcı yazıldıktan sonra **geri alındı** (`changes/w_cm18.py`, `w_cm18_revert.py`).
- Sprint duruşu 31 cm çöküş: iki ailenin sprint duruş kliplerinde de var. **AÇIK.**
- Hız değiştirilmedi (kullanıcı uyarısı: seçimi hızla kaçırmak yerine seçim kuralını düzeltmek). Sonraki adım: sprint duruşu veritabanını önceki gait'e göre kapılayan Chooser sütunu ya da Sphirus kopyasına maliyet yanlılığı.

## 5. Beden dili ve hızlar
Değişmeyen: yürüyüş 180 (kadans/adım ve kol salınımı korunuyor), jog 415, sprint 585, tempolu yürüyüş seçenekleri. Yeni: yalnız yokuşta yavaşlama
(6° altında 0, 25°'de %25/%12) ve yokuşta gövde eğimi. Toplu oynatma hızı yavaşlatması yok. Jog'un beden dili (gövde +21°, kol 45/50 cm) değişmedi.

## 6. Kamera
Yakın omuz kadrajı korunuyor: yürüyüşte ve jog'da ayaklar hiç kadraja girmiyor (alt ayak ekran y 1,8–2,1); jog'da kol 117 → 127 cm, FOV 66 → 68°.
Yokuşta baş yüksekliği daha kararlı (§2). Duvar yakını ve etkileşim kadrajı: §7 akış kaydı.

## 7. Etkileşim akışı
Rota (gerçek girdi, ışınlama yok): mutfak → arka kapıdan çıkış → bahçe patikasında yürüyüş ve **jog (415)** → odun al (E) → taşı → kütükte kes (E + tık)
→ iki parçayı topla → arka kapıdan gir → şömine: E (yerleştir), E (yak). Ardından kayıt yükleme ve odunsuz şömine. `data/flow_counters.txt`, `data/flow_counters_C.txt`, video `videos/flow_player_cam.mp4`.

| Adım | Sonuç | Durum |
|---|---|---|
| Evden çıkış, patikada yürüyüş/jog | jog 415'e çıkıyor, GOTO ile yön değişimleri | TEKNİK TEST |
| Odun al → taşı → kes | sayaç odun 1 → gevşek parça 2; Pick / CarryArms / Chop montajları sırayla | TEKNİK TEST |
| İki parçayı topla | 4 koşunun 2'sinde iki parça; 2'sinde biri kaldı (bölünmüş 1, gevşek 1). Kalan parça kütükten ~80 cm uzağa düşmüş; sabit test rotasının en yakın geçişi 79–81 cm, otomatik toplama yarıçapı 70 cm → test rotası, oyun hatası değil. Ateş tek parçayla da yakıldı | KISMİ |
| Şömineye yerleştir, yak | ateş 0 → 1 → 2 | TEKNİK TEST |
| Kayıt yükle → parçalar geri geldi → yak | yüklemeden sonra bölünmüş 2; E, E → ateş 2 | TEKNİK TEST, GEÇTİ |
| Odunsuz şömine | reddetme hareketi, durum değişmedi | TEKNİK TEST, GEÇTİ |
| İstemlerin kapanması | bakış/hareket kilidi her montaj bitince 0,2–0,3 s içinde açılıyor | TEKNİK TEST |
| El–nesne teması, kapıdan geçiş | odun göğüs önünde, eller kütüklerin üstünde; kapı kasasında geçme görülmedi (kare düzeyi, `evidence/flow_frames.jpg`) | GÖRSEL (kare) |
| Maske tezgâhı, veranda kapısı | test planı E anında hedefi yakalayamadı (tezgâh hedefi 17. saniyede seçildi; kapı açılmadı, karakter kapının 40 cm önünde durdu). Bu turda etkileşim kodu değişmedi ama **doğrulanmadı** | TEST EDİLEMEDİ |
| Çay, yatak | haritada ayrı etkileşim aktörü bulunamadı (`data/interact.txt`) | TEST EDİLEMEDİ |

Kamera: dar geçişte (koltuk–duvar arası) kamera başın arkasına çok yaklaşıyor, saç kadrajın ~üçte birini kaplıyor (`evidence/flow_frames.jpg`, 70. s). **AÇIK** (kamera çarpışma davranışı; bu turda değiştirilmedi).
Kayıtçı düzeltmesi: gün merkezi (`BP_GR_DayHub`) önbelleği her PIE oturumunda aynı dünya yolu yüzünden ölü nesneyi tutuyordu; sayaçlar artık her kayıtta okunuyor.

## 8. Kayıtlar
Bütün videolar 30 Hz sabit oyun adımında, her karede bir ekran görüntüsüyle kaydedildi ve gerçek hızda (30 fps) kodlandı. "Önce" = aynı derlemede
çalışma anında geri alınmış durum (yokuş: düz taban + eğim kapalı; ışık: güneşte ışık fonksiyonu yok). Rota, girdi, kamera, başlangıç noktası eşleşik.

| Video | Kamera | İçerik |
|---|---|---|
| `videos/slope_pc_before_left_after_right.mp4` | oyuncu kamerası | ev–orman yokuş rotası: yürüyüş, dik yokuşta 45°/s dönüş, jog, ters yönde dönüş, duruş (28 s) |
| `videos/slopediag2_before_left_after_right.mp4` | teşhis (yan, 420 cm) | aynı rota; ormanda kamera bitkilerin arkasında kaldığı için **yalnız bu teşhis kaydında** bitki örnekleri görüntüden gizlendi (`ShowFlag`), çarpışma/oynanış değişmedi |
| `videos/lightpatch_before_left_after_right.mp4` | oyuncu kamerası | atölyede pencere güneşi lekesine girip çıkma |
| `videos/lightexit_before_left_after_right.mp4` | oyuncu kamerası | mutfaktan arka kapıdan dışarı çıkış (parlaklık eğrisi önce/sonra aynı: kare ortalaması 0,20 → 0,30 → 0,35 → 0,32) |
| `videos/turns_diag_after_walk180_jog135_180.mp4` | teşhis (yan, düz harita) | yürüyüş ±180°, jog +135° / −180° (yalnız sonra; dönüş için kalıcı değişiklik yok) |
| `videos/stops_diag_after_jog_sprint_walk.mp4` | teşhis | jog, sprint ve yürüyüş duruşları (yalnız sonra; duruş için kalıcı değişiklik yok) |
| `videos/flow_player_cam.mp4` | oyuncu kamerası | §7 akışı |

Görsel inceleme yöntemi: her videodan saniyede bir kare, kritik anlarda yakın kırpım (`evidence/*`). **Videoları gerçek hızda izleyerek akıcılık ya da his
değerlendirmesi yapmadım**; o değerlendirme kullanıcıda.

Bu turda geçersiz sayılan kayıtlar (rapora konmadı): ilk teşhis kamerası (260 cm, baş ve ayaklar kesik), ikinci teşhis kamerası (520 cm, ormanda bitkilerin arkasında),
bitki bayrakları editör görünümüne sızdığı sırada alınan akış videosu, performans ölçümü ve iki Bridge dışa aktarımı (bkz. §12).

## 9. Performans
Ortam: RTX 4060 Laptop GPU, i7-13650HX, 32 GB, prizde, Windows "Turbo" güç planı; **editör PIE** (paketlenmiş oyun değil), PIE görünümü 1507×918,
ölçeklenebilirlik Epic (sg.* = 3), TSR (ekran yüzdesi otomatik, TSR geçmişi %200), Lumen GI/yansıma donanım ışın izleme, VSM, Nanite, MegaLights kapalı,
VSync yok, kare sınırı yok. Rota: perf_cam.sh yokuş patikası (bekle 3 s → yürü 6 s → sprint 4 s → dur 3 s), motor CSV profilleyici. `data/perfenv.txt`.

| Koşu (aynı oturum, sırayla) | fps | Kare p50 / p95 / p99 (ms) | Oyun iş parçacığı p50 | Render iş parçacığı p50 | GPU p50 / p99 | >50 ms kare |
|---|---|---|---|---|---|---|
| Sonra 1 | 19,8 | 50,0 / 58,9 / 60,6 | 15,2 | 50,0 | 48,7 / 59,0 | 190 / 371 |
| Önce 1 | 19,9 | 49,8 / 58,3 / 62,4 | 15,1 | 49,8 | 48,4 / 59,7 | 170 / 351 |
| Sonra 2 | 20,2 | 49,8 / 56,4 / 58,5 | 15,1 | 49,8 | 48,5 / 56,7 | 160 / 338 |
| Önce 2 | 20,3 | 49,3 / 57,3 / 62,2 | 15,1 | 49,3 | 47,8 / 60,9 | 161 / 378 |

**Sonuç:** ışık fonksiyonu, yuvarlak taban ve eğim katmanının ölçülebilir maliyeti yok (fark ölçüm gürültüsü içinde). GPU sınırlı (GPU ≈ kare süresi).
Mutlak değer 17 Kasım'daki 36,1 fps ölçümünden çok düşük; ölçüm sırasında GPU 85 °C ve %98 kullanımdaydı. Koşullar (ısıl durum, editör durumu) aynı
değilken bu farkı bu turun değişikliklerine bağlamıyorum; 5.9'un 5.8.4'e göre hızlı ya da yavaş olduğu sonucunu da yazmıyorum (aynı koşulda 5.8.4 ölçülmedi).
İlk ölçüm (49 fps) bitki örnekleri görüntüden gizliyken alındığı için geçersiz sayıldı.
Saç ve kıyafet hareketi bütçesi: GPU zaten kare süresinin tamamı; ek simülasyon için önce GPU maliyetinin (Lumen/VSM/TSR ayarları) ayrıca profillenmesi gerekiyor. Uygulanmadı.

## 10. 5.9 araçları ve kapsam
| Araç | Durum | Kullanım |
|---|---|---|
| Epic MCP (yerel istemci) + **BlueprintDslToolset** | Çalışıyor (düz Blueprint) | `AC_Sph_Motion` grafik düzenlemeleri bununla yapıldı; AnimBlueprint DSL'de desteklenmiyor |
| BlueprintToolset (grafik/düğüm) | Çalışıyor | Okuma, değişken ekleme, derleme |
| Python Blueprint grafik yardımcıları (5.8) | Yok | — |
| Foot Placement pelvis modları | Çalışıyor | Eğim modu denendi, reddedildi |
| Işık fonksiyonu malzemesi (dünya konumu) | Çalışıyor | İç güneş zayıflatması |
| **AnimGen** | Motorda deneysel eklenti olarak kurulu (`Experimental/Animation/AnimGen`, `AnimGenOffline`, `UAFAnimGen`); projede **etkin değil**, hiç yüklenmemiş, üretimde **kullanılmamış** | İçeriği PyTorch ile otokodlayıcı/denetleyici eğitme betikleri; eğitim verisi ve hattı yok → bu turda somut katkı yok |
| ML Deformer, Chaos Flesh | Motorda var, projede kapalı | Uygulanmadı |
| Saç/kumaş hareketi | Uygulanmadı | Bütçe: §9; önce hareket ve ışık kusurları |

Doğrulanan kapsam: editör PIE'de oynanış (hareket, yokuş, dönüş, duruş, etkileşim akışı, kayıt yükleme). **Paketlenmiş oyun, bütün eklentiler, cook doğrulanmadı.**

## 11. Değişen varlıklar ve geri dönüş
| Varlık | Değişiklik | Yedek (manifest) |
|---|---|---|
| `/Game/Sphirus/Player/Motion/AC_Sph_Motion` | eğim değişkenleri ve grafik, `turn_sev` terimi, örnek düzenlenebilir bayrakları | `ue59_m18_char`, `ue59_m18_char_w` (ilk sürüm) |
| `/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player` | CMC düz taban kapalı | `ue59_m18_char_w` |
| `/Game/Sphirus/Lighting/Day_20261118/M_Sph_SunInterior_LF` | yeni | `ue59_m18_lf` (yeni) |
| `/Game/GraceRanger/Maps/L_GR_SphirusHouse` | `DirectionalLight_0` ışık fonksiyonu | `ue59_m18_light`, `ue59_m18_light2` |
| `/Game/Sphirus/Player/GASP/ABP_Sph_GASP` | sprint duruşu eşlemesi eklendi, sonra **geri alındı** (34 satır, başlangıçla aynı) | `ue59_m18_char`, `ue59_m18_cm`, `ue59_m18_cm_rev` |
| `Plugins/Marketplace/Black_Eye/Black_Eye.uplugin` (5.9 kopyası) | Bootstrap modülü çıkarıldı | `Saved/UE59Work/checkpoints/20261118_blackeye/` |
| `Tools/SHME_V233_20261027/manifest233.py` | `.umap` desteği | `Tools/UE59_20261118/manifest233.py.orig_20261118` |
| `Tools/Camera_20261112/vidc.py`, `Tools/UE59_20261116/cmap.py`, `w_profile.py` | ölçüm yaması kancası; sprint duruşu seçeneği | `Tools/UE59_20261118/*.orig_20261118` |

Yedekler `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/<ad>/` altında; geri dönüş = dosyayı editör kapalıyken geri kopyalamak.
Çalışma anında geri dönüş anahtarları: `SphMotion.SlopeOn = False`, CMC `use_flat_base_for_floor_checks = True`, güneşte ışık fonksiyonu `None`.

## 12. Güvenlik
- Orijinal 5.8.4 projesi: 1149/1149 dosya taban SHA1 listesiyle aynı; oradaki asıl kayıt `SFSaveSlot.sav` SHA1 `4823d83a…` (değişmedi).
- 5.9 kopyasındaki test kaydı her koşudan sonra `4823d83a…` (≈40 koşu). Yarıda kesilen iki koşuda oyunun yazdığı kayıt kenara alındı, özgün kopya geri kondu.
- Bütün varlık yazımları manifest + doğrulanmış yedek + tek kilit sahibiyle (`lock233`, `emb`) yapıldı; kilit bırakıldı, editörde dirty paket yok.
- Harita yazımı için `manifest233.py` `.umap` destekleyecek şekilde genişletildi (yedek doğrulaması aynı); kapı yazımı `save_packages` üzerinden geçti.
- Editörde yan etki (düzeltildi): teşhis videoları için verilen bitki gösterim bayrakları (`ShowFlag.*`) editör görünümüne sızdı. Bu sırada alınan akış videosu,
  performans ölçümü ve iki Bridge dışa aktarımı **geçersiz** sayıldı, bayraklar varsayılana (2) döndürüldü, hepsi yeniden alındı (`INVALID.txt` işaretli koşular yayınlanmadı).
- Windows güvenlik ayarlarına dokunulmadı; engellenen DLL yükletilmedi (§0).
- Git yalnız yayın deposunda (`sphirus-world-preview`) kullanıldı; proje git'siz.

## Yayın
- Bu rapor: `chatgpt-bridge/reports/sphirus-ue59-fullbody-2026-11-18/`.
- Dünya önizlemesi: 5.9 kopyasından standart Bridge dışa aktarımı, **son yayınlanan çalıştırmanın (2026-11-12, 5.8.4) 18 kamera pozuyla birebir**,
  run `2026-11-18_102752_814812_8c909a`, motor `5.9.0-60351404`, 18/18 görüntü, 0 hata, koruma doğrulaması geçti. `chatgpt-bridge/latest/LATEST.json` bu çalıştırmayı gösterir.
  5.9'da Bridge'in kullandığı `CaptureViewport` aracı kaldırıldığı için 5.9 kopyasındaki modülde bu çağrının "araç yok" hatası ölümcül olmaktan çıkarıldı (`changes/` notu).

## Özet durum
| Konu | UYGULANDI | TEKNİK TEST | GÖRSEL | PERFORMANS | AÇIK |
|---|---|---|---|---|---|
| Ölçüm güvenilirliği | ✓ | ✓ | — | — | yürüyüş kadansı çift destekle hâlâ fazla sayıyor olabilir (adım×kadans > hız) |
| Yokuş (taban, eğilme, yavaşlama) | ✓ | ✓ | ✓ kare | ✓ | dik yokuşta ön diz; yokuş aşağı tepki küçük |
| Evdeki beyaz kırpılma | ✓ | ✓ | ✓ kare | ✓ | yarı gölge gürültüsü |
| Yürüyüş sola 180° kayma | — | ✓ | ✓ kare | — | ✓ |
| Jog 135/180° çökme | — | ✓ | ✓ kare | — | ✓ |
| Jog/sprint duruşu | denendi, geri alındı | ✓ | ✓ kare | — | ✓ (Chooser durma satırı) |
| `turn_sev` | ✓ | ✓ | — | — | — |
| Kamera | — | ✓ | ✓ kare | — | dar alanda saç kadrajı |
| Etkileşim akışı + kayıt | — | ✓ | ✓ kare | — | maske/kapı kontrolü yapılamadı; çay/yatak aktörü yok |
| Saç/kıyafet hareketi, ML Deformer, AnimGen | — | — | — | — | ✓ (gerekçe §9–10) |

Kullanıcı kabulü: **yok**. Videoları gerçek hızda izleyip onaylamadım.
