# SPHIRUS UE 5.9 — hareket, anatomi ve süreklilik turu (2026-11-21)

Proje: `Documents/Unreal Projects/sphirus_UE59` · harita `/Game/GraceRanger/Maps/L_GR_SphirusHouse` · oyuncu `BP_HybridA_Player` (GASP).
Başlangıç: 148b4916 raporundaki kayıtlı durum. Geri dönüş: `Saved/UE59Work/checkpoints/20261121_round4_start` (dosya kopyası + sha1) ve
her yazma işi için `ue59_m24_r4a..r4d` manifest yedekleri. Kullanıcı kaydı (`SFSaveSlot.sav`) her testte kenara alınıp geri kondu (SLOT_OK).

**Hiçbir madde USER_ACCEPTED değildir.** Aşağıdaki "geçti" ifadeleri teknik ölçüm ve kendi görsel incelememdir; son karar oynayışındır.

## 1. Bozulmanın üretildiği katman (ham klip → yalnız retarget → son poz)

Aynı girdilerle üç aşama ölçüldü (`data/katman_*.txt`, `evidence/01..07`):

| Aşama | Yürüyüş üst kol açıklığı | Yürüyüşte el bileği – kalça hattı | Tempo omurga eğimi (bel / göğüs / üst sırt / boyun, bind'e göre) |
|---|---|---|---|
| Ham klip (sürücü iskelet) | 17,3° | 27,8 cm (erkek manken) | 15 / 14 / 12 / 6° (düzgün) |
| Yalnız retarget (MetaHuman) | 18,9° | 22,7 cm | 17 / 14 / 14 / 7° (düzgün) |
| Önceki son hal | 11,1° | 15,8 cm (en az 11,2) | 17 / 8 / −3 / −4° (**belden kırık**) |
| Yeni son hal | 17,5° | 22,0 cm (en az 18,9) | 17 / 12 / 9 / 6° (düzgün) |

Sonuç: kol daralması ve omurga kırığı **klipten ya da retarget'ten değil, benim eklediğim beden duruş katmanından** geliyordu
(`ABP_Sph_Body_GASP` içindeki sabit `VI_/VW_/VD_/VR_/VA_` ofsetleri). Bu sabitler Relaxed bekleme pozuna göre ayarlanmıştı ve farklı
doğal duruşu olan klip ailelerine (Neutral yürüyüş/koşu, Core Motion tempo, Relaxed sprint) aynen uygulanıyordu:
- yürüyüşte bütün kol omuzdan 8° içeri dönüyor, kol-kareleri'nin 284/574'ünde el bileği kalça bölgesinin içine giriyordu (yalnız retarget'te 0);
- tempoda eller orta hattı 4 cm geçiyor, bel 17° öne eğikken üst sırt dik kalıyordu (kırık);
- koşuda baş gövdeye göre geri çekiliyordu.

## 2. Yaygın animasyon atlamalarının bulunan nedenleri

`an_contw.py` / `an_popsum.py`: görünür bedenin 25 kemiği için kare kare hız sıçraması (dünya yönelimli, kapsül ötelemesi çıkarılmış).

1. **Duruş katmanı bileşen uzayında çalışıyordu.** GASP, kapsülü girdi yönüne tek karede çevirir (rotation rate −1) ve bedeni kök
   ofsetiyle arkadan getirir. O süre boyunca beden bileşene göre 90–180° dönük kaldığı için "öne/arkaya" ofsetler yanlış eksende
   uygulanıyordu (−16° sırt düzeltmesi yana bükülme oluyordu). Her keskin yön değişiminde ve her "dönerek başlama"da üst beden **tek karede
   14–47 cm** sıçrıyordu. Düzeltme: omurga/boyun/baş/köprücük/üst kol düğümleri ebeveyn-kemik uzayına alındı (`c_bodyspace.py`).
2. **Bir kare gecikmeli durum.** GASP'in `AC_PreCMCTick` bileşeni pawn tick'inden önce çalışıyor, pawn'ın o karede yazdığı strafe/gait
   durumu hareket bileşenine bir kare geç ulaşıyordu: koşuda W→S'de kapsül **bir kare 180° dönüp geri geliyor**, Motion Matching o kare
   `Run_Turn_180` seçiyordu. Düzeltme: tick sırası (pawn → PreCMC → hareket bileşeni); motorun varsayılan ters bağımlılığı açıkça kaldırıldı.
3. Kalan bacak "sıçramaları" 30 fps kliplerin 60 Hz'de doğrusal ara değerlenmesidir (hız iki karede bir sabit); durum hatası değildir, düzeltilmedi.

| Plan (60 Hz, düzeltmeden hemen sonraki ölçüm; yeniden açılmış durum için 4.2) | Üst beden sıçrama karesi önce → sonra | En büyük üst beden adımı | Tek karelik klip ziyareti |
|---|---|---|---|
| Koşu yön değişimleri (A) | 22 → 0 | 47 cm → 0 | 7 → 1 |
| Sprint + yürüyüş (B) | 18 → 8 | 46 cm → 2,9 cm | 7 → 1 |
| Başlangıçlar (S) | 20 → 8 | 23,5 cm → 2,6 cm | 3 → 0 |
| Tempo (Q) | 21 → 2 | 22,7 cm → 2,4 cm | 4 → 0 |
| Düz yürüyüş/tempo/koşu/sprint (L) | 6 → 4 | 20,7 cm → 2,6 cm | 3 → 0 |

## 3. Uygulanan değişiklikler (gerçek projede, kaydedildi)

| Varlık | Değişiklik |
|---|---|
| `BP_HybridA_Player` | **Duruş denetleyicisi** `GR_Posture` (her tick): sabit ofsetler yerine görünür bedende ölçülen yavaş integral düzeltmeler. Kalça hattı çerçevesinde ölçer (kapsül değil). Omurga: göğüs/üst sırt/boyun, bel eğimini azalan oranla izler (0,70 / 0,55 / 0,30) → her klip ailesinde aynı düzgün taşıma; klibin hızlı hareketi geçer (zaman sabiti ≈ 0,4 sn). Baş: eğim ve yana yatma düzlenir. Omuzlar: simetrik öne yuvarlanma/yükselme düzeltmesi (adım salınımı korunur). Kollar: düzeltilen göğsün altında kolun sarkma açısı korunur (sarkan kolda 0,85, bükülü kolda 0,45); **kalça açıklığı**: el bileği kalça yanında 21 cm, bel yanında 17 cm, önde 3 cm'den içeri giremez (gerektiği kadar omuz açılır, yavaşça bırakılır). Montajda (etkileşim, taşıma) eski sabitlere yumuşak döner; havada tutar. Tick sırası düzeltmesi. |
| `ABP_Sph_Body_GASP` | 9 duruş düğümü bileşen uzayından ebeveyn-kemik uzayına; ilgili 47 vektör bind eksenleriyle yeniden ifade edildi; denetleyicinin devraldığı sabitler sıfırlandı; baş düzleme integratörü kapatıldı (tek sahip denetleyici). |
| `AC_Sph_Motion` + `BP_Sph_GASPCharacter.CalculateMaxAcceleration` | **Klibe bağlı ters dönüş** (250 cm/s üstü giriş: tempo/koşu/sprint): 180° yön değişiminde kapsül, Motion Matching'in oynattığı dönüş klibinin kendi hız eğrisini (fren → basış → yeniden itiş) izler; sürtünme hızı artık anında öldürmez. Düşük hız sınırı (150 cm/s altı) artık gerçekten etki ediyor (`MinAnalogWalkSpeed` sınırı izliyor). |
| `ABP_Sph_GASP` + `A_Sph_Bed` | Yatış: ayak yerleştirme (FootPlacement) düğümüne kendi devre dışı eğrileri tanımlandı; yatış klibi bu eğriyi taşıyor. |
| `BP_GR_DayHub`, `BP_GR_DayStation` | Yatak kamerası (`GR_BedCam`); görev sırası (ateş/çay bitmişse görev yeniden eklenmez). |
| `BP_GR_MaskBench` | Maske incelemesinde kamera maskeyi hedefler, ayrı kadraj. |
| `L_GR_SphirusHouse` | Yatak/uyanış kamerası hedefi; maske kadraj değerleri; şömine ışığı (60 → 9 cd, yumuşak kaynak, alevlerin önünde). |

Betikler: `scripts/` (uygulama `m_*_mcp.py`, `c_*.py`, kayıt `w_r4_save.py`; ölçüm `an_*.py`, `hk_pose2.py`).

## 4. Sonuçlar

Tüm sayılar **kaydedilip editör yeniden açıldıktan sonra** alınmıştır (`data/final4.txt`, betik `scripts/final4.sh`); girdiler gerçek tuşlardır (X ile tempo dahil).

### 4.1 Kol ve omurga taşıması (60 Hz, `data/durus_once_sonra_60hz.txt`)

| Yürüyüş tipi | El bileği – kalça hattı (kalça yanında) önce → sonra | Kalça bölgesine giren kol-karesi önce → sonra | Omurga eğimi bel/göğüs/üst sırt/boyun önce → sonra |
|---|---|---|---|
| Bekleme | 18,8 → 23,7 cm | 102/102 → 0/100 | −0,4 / −2,1 / 2,9 / 0,4 → −0,2 / −0,7 / −0,9 / 0,8 |
| Yürüyüş 180 | 17,6 → 22,1 cm (en az 11,3 → 18,9) | 284/574 → 0/576 | 1,4 / 4,4 / 3,8 / 4,8 → 1,4 / 1,2 / 0,9 / 1,0 |
| Tempo 278 | 15,8 → 23,1 cm (orta hat −4,2 → −0,3) | 185/576 → 21/574 | 16,9 / 7,6 / −2,7 / −3,7 → 16,9 / 11,5 / 9,4 / 5,6 |
| Koşu 415 | 22,1 → 21,6 cm (en az 0,0 → 5,3) | 23/576 → 18/576 | 21,6 / 19,4 / 17,9 / 14,4 → 21,6 / 14,7 / 11,9 / 7,1 |
| Sprint 585 | 24,8 → 23,9 cm (en az −0,7 → 10,4) | 9/456 → 16/454 | 21,4 / 20,0 / 17,6 / 15,2 → 21,3 / 14,6 / 11,4 / 6,5 |

Kalça hattı = leğen orta düzlemi; bu bedende kalça yarı genişliği ≈ 17,5 cm, yani 21–23 cm el bileğinin kalçanın 3–5 cm dışından geçmesi demek.
Tempoda eller önde hâlâ orta hatta buluşuyor (−0,3 cm; önce 4 cm geçiyordu). Koşu ve sprintte kol açıklığı klipteki değerde; kalça bölgesi sayımı düşük ama sıfır değil.
Görsel: `evidence/01–06` (aynı kareler, önce/sonra; yan, ön, arka), videolar `videos/04–05` ve `00_once_*`.

### 4.2 Süreklilik (üst beden sıçraması, yeniden açılmış durum)

| Plan (60 Hz) | Üst beden sıçrama karesi | En büyük üst beden adımı (tek kare) | Tek karelik klip ziyareti |
|---|---|---|---|
| Koşu yön değişimleri | 2 (önce 22) | 2,5 cm (önce 47) | 2 (önce 7) |
| Sprint + yürüyüş | 7 (önce 18) | 2,8 cm (önce 46) | 2 (önce 7) |
| Başlangıçlar | 5 (önce 20) | 2,7 cm (önce 23,5) | 0 (önce 3) |
| Tempo | 2 (önce 21) | 2,3 cm (önce 22,7) | 0 (önce 4) |
| Düz yürüyüş/tempo/koşu/sprint | 4 (önce 6) | 2,3 cm (önce 20,7) | 0 (önce 3) |
| Geri tempo zinciri (yeni plan) | 2 | 2,5 cm | 6 |

Ölçüt değişmedi: aynı betik, aynı eşik (hız adımı > 120 cm/s ve yerel ortancanın 6 katı). Geri tempo planındaki 6 tek-karelik klip ziyareti (`Jog_Bwd_Pivot` → `Run_Pivot_F_B`) hâlâ duruyor: görünür sıçrama üretmiyor ama yanlış klibin bir kare seçilmesi sürüyor.

### 4.3 Ters yön dönüşleri (ağırlık)

| Durum | Sıfır geçişi önce → sonra | Tepe yavaşlama önce → sonra |
|---|---|---|
| Koşu A↔D | 0,22 → 0,35 sn | 2840 → 1500 cm/s² |
| Koşu W→S (Shift basılı) | 0,27 → 0,33 sn | 1910 → 1410 cm/s² |
| Sprint D→A | 0,52 → 0,43 sn | 1250 → 1660 cm/s² |
| Sprint W→S | 0,50 → 0,50 sn | 1830 → 1480 cm/s² |

Koşudan sürekli geri tempoya geçiş (S+Shift 4 sn tutuldu): koşu döngüsü → `Run_Pivot_F_B` (fren, basış, dönüş) → 2,7. saniyede sürekli `CM_af_Loco_Jog_Bwd` döngüsü, hız 234 cm/s, bu segmentte en kötü temas 3 cm. S+A / S+D: `Run_Diamond_F_BL/BR` → `Jog_BwdLeft/Right`, 1–2 cm. Sprintte: 0,42 sn fren tutuşu → `Run_Stop_F` → `Run_Start_B` → geri döngü. Fren sırasında karar değiştirme (S'ye 0,3 sn dokunup D'ye geçiş) çalışıyor. Video: `videos/03_omuz_geri_tempo_zinciri.mp4`.

### 4.4 Ayak kayması (klip temas eğrisine göre; ortalama / %90 / en kötü cm, parantezde ≥10 cm temas sayısı)

| Plan | 60 Hz | 30 Hz | değişken 22–60 Hz |
|---|---|---|---|
| Koşu yön değişimleri | 1,4 / 2,1 / 17,6 (1) | 1,7 / 2,7 / 22,2 (1) | 1,8 / 2,5 / 18,1 (2) |
| Sprint + yürüyüş | 1,8 / 3,0 / 17,6 (1) | 1,9 / 3,6 / 13,9 (1) | 1,7 / 3,1 / 19,7 (1) |
| Başlangıçlar | 1,7 / 2,8 / 15,1 (1) | 1,4 / 2,7 / 17,6 (1) | 1,6 / 2,5 / 16,3 (1) |
| Tempo (gerçek X) | 1,6 / 2,7 / 12,9 (1) | 1,6 / 2,7 / 14,2 (2) | 1,7 / 2,8 / 15,2 (2) |
| 12 fazlı ters dönüş | 2,4 / 3,2 / 37,6 (2) | 2,2 / 4,9 / 17,4 (3) | 2,0 / 3,7 / 22,7 (2) |
| Geri tempo zinciri + karar değiştirme | 1,9 / 2,4 / 33,3 (2) | 1,8 / 3,8 / 23,1 (1) | 2,0 / 2,9 / 38,1 (2) |

Ölçüm yöntemi önceki turla aynıdır (sürücü klibin `contact_l/r` eğrisi). Ortalama ve %90 değerleri korunuyor; **en kötü tekil örnekler düzelmedi** (bkz. bölüm 5). Bir kısmında (geri tempo duruşu 13–16 cm) eğri "temas" derken görünür ayak yerden 11 cm yukarıdadır; bunu ayrıca sınıflandırmadım, tabloda olduğu gibi sayılıyor.

### 4.5 Ev akışları

| Akış | Sonuç (yeniden açılmış durum, gerçek tuşlar) | Kanıt |
|---|---|---|
| Yatak: yatış → bekleme → kalkış → gün geçişi → uyanış | Beden şiltenin üstünde (leğen z 566; şilte üstü ≈ 560; önce 646 = havada). Yatış boyunca baş ucu kamerası; uyanıştan sonra görüş ve kontrol oyuncuya dönüyor. | `videos/06`, `evidence/08–09` |
| Maske: alma → inceleme → bırakma | Maske inceleme boyunca kadrajda ve yüzü görünür (sol omuz üstü, yukarıdan); bırakma sonrası kontrol geri geliyor. Kavrama pozu değişmedi (el maskenin kenarında). | `videos/07`, `evidence/10–11` |
| Odun: toplama → taşıma → yarma → iki parçayı alma → şömine → yakma | `CHECK wood picked True, split pieces 4 (need 2) PASS, fire state 2 PASS` | `videos/08` (akışın son 30 sn'si, %70 çözünürlük; bu videodaki ateş ışığı ara değer 24 cd; tam 93 sn'lik kayıt yerelde `Saved/Codex/Day_20261107/videos/F19_flow_R4.mp4`) |
| Şömine görünümü | Işık 60 → 9 cd, yumuşak kaynak, alevlerin önünde/üstünde: taş ve kütük ayrıntıları okunuyor, beyaza patlama yok. Test kaydı yüklenince ateş yanık geliyor (kayıt/yükleme ateş durumunu koruyor). | `videos/09`, `evidence/12–13` |
| Görev sırası | `GR_Dressed`: ateş/çay bitmişse görev yeniden eklenmiyor. **Kod değişti, oyun içinde çay → gardırop sırasıyla ayrıca oynatılıp doğrulanmadı.** | `scripts/m_task_mcp.py` |
| Çay, gardırop, kapılar, tam kayıt/yükleme, gün geçişi sonrası yeniden yükleme | Bu turda yeniden koşturulmadı (önceki turun sonuçları geçerli sayılmıştır; bu turdaki tick sırası ve duruş değişikliklerinden sonra ayrıca doğrulanmadı). | — |

Kullanıcı kaydı `SFSaveSlot.sav` tur başındaki sha1 ile aynı (3d81ab9d…). Testler ayrı yuvalar kullandı.



## 5. Açık kalanlar ve yapılmayanlar (dürüst liste)

Düzeltilmeyen veya yalnız kısmen düzelen maddeler:

**Ayak teması (bilinen kötü örnekler)**
- **30 Hz koşudan duruş 22 cm (düzelmedi).** İz: 30 Hz'de Motion Matching `M_Relaxed_Run_Stop_F_Rfoot` klibine frenin ortasından giriyor; kapsül klibin hız eğrisini tutuyor, sağ ayak klibin kendi yerleşme adımında yerde 20–38 cm ilerliyor (temas eğrisi bu adımı "basılı" sayıyor). Değişken Hz'de 18 cm, sprintten S'ye frende bir kez 38 cm aynı klipte görüldü. Çözüm klip varyantı / seçim penceresi işidir; bu turda yapılmadı.
- **Koşu ters dönüşleri:** çoğu ≤ 9 cm (önce 9–14), ama seyrek aykırı örnekler sürüyor: 17–23 cm (ayak kilidi tutmadığında) ve bir kez 37,6 cm (klip içinde zaman atlaması). Yeni mantık tipik durumu iyileştirdi, en kötü durumu iyileştirmedi.
- Yürüyüş S→W pivotu 12–18 cm (pivot klibinden başlangıç klibine geçişte basılı ayağın yer değiştirmesi), yürüyüş geri başlama bazı fazlarda 15–18 cm, geri tempo duruşu 13–16 cm (bu örnekte ayak yerden 11 cm yukarıda: eğri temas diyor, görünür temas yok), koşuda S'ye 0,3 sn dokunup W'ye dönüş 23–33 cm.
- Eski "A→D→bırak ≈ 51 cm" ve "yürüyüş + kamera 90° + duruş" zincirleri bu turda ayrıca yeniden üretilmedi.

**Ağırlık / arcade hissi**
- Yapılan: 180° dönüşlerde fren artık klibin kendi profili (tepe yavaşlama 2840 → ~1500 cm/s², sıfır geçişi 0,22 → 0,35 sn). Yapılmayan: ilk adım öncesi ağırlık aktarımı (APA), 90° yanal dönüşlerde beden tepkisi, duruş sonrası yerleşme çeşitliliği. Bu başlıklar açık.
- Koşu döngüsünün kendi öne eğimi (bel ~21°) klipten geliyor; göğüs artık onu düzgün izliyor ama eğim miktarı değiştirilmedi.

**Bu turda dokunulmayan veya yeniden ölçülmeyenler**
- Bekleme hareket seti (bilek/yumruk izlenimi) yeniden incelenmedi; yalnız kolların bekleme taşıması değişti (eller artık kalçanın yanında).
- İleri/duruştan zıplama ayrımı, eğim/merdiven, iki elle taşıma duruşu (taşımada denetleyici eski sabitlere döner; görsel olarak yeniden doğrulanmadı), çömelme.
- Kamera: dar oda, alçak tavan, merdiven, bitki örtüsü, çarpışma dönüşü yeniden ölçülmedi. Maske incelemesi **sol** omuz üstünden kadrajlanıyor (sağdan bakınca el maskeyi kapatıyor); yatışta omuz kamerası yerine baş ucu kamerası kullanılıyor.
- Yorgunluk duruşu (çökme) terimi fiilen etkisiz: denetleyici onu ortalama duruş olarak geri alıyor (hedefe bağlanmadı).
- Şömine: ışık yumuşatıldı; sağdaki parlak leke ateş ışığı değil (ışık kapalıyken de var; güneş sızıntısı) — giderilmedi.
- Yatarken "Yatak — Uzan/Kalk" istemi ekranda kalıyor.
- Gamepad akışı, standalone/paketli çalıştırma, performans ölçümü (iç render çözünürlüğü dahil) bu turda **yapılmadı**. Denetleyicinin maliyeti (tick başına ~14 soket okuması) ölçülmedi.
- 4 eklentinin (PBL_Database, Black_Eye, Nwiro, GravityScatterTool) 5.9 sürümleri hâlâ senin Fab/Launcher kurulumunu bekliyor.

