# SPHIRUS UE 5.9 — Tur 7: "The Guardian" ağırlık / toparlanma / düşme / dar alan (2026-11-22)

Durum: **teknik doğrulama yapıldı, kullanıcı kabulü YOK** (USER_ACCEPTED yazılmadı). Görsel ve oyun hissi kararı kullanıcınındır.

Kapsam: `BP_HybridA_Player` (GASP / Motion Matching), test haritası `L_Sph_MoveTest`, ev haritası `L_GR_SphirusHouse`. İkinci bir hareket sistemi eklenmedi; tüm değişiklikler mevcut sahiplerde (oyuncu Blueprint olayları, GASP AnimBP, görünür gövde AnimBP, `AC_Sph_Motion`).

Kanıt kuralı: aşağıdaki **"sonra"** sayıları, videolar ve ham veri **aynı sürümden**: varlıklar kaydedildi (`w_save7.py`, manifest `ue59_m27_r7save_142031`), editör kapatılıp yeniden açıldı, kaydedilen değerler geri okundu (`data/log.txt` başı, `RCHK`), sonra `scripts/final_r7.sh` bu açılmış durumda çalıştı (14:24–17:16). f7 / f8 görüntüleri bu turun kanıtı olarak kullanılmadı. Kullanıcı kaydı (`SFSaveSlot.sav`, sha `3d81ab9d…`) her ev akışından önce ve sonra aynı; test kaydı olarak kullanılmadı.

Kayıt sayıları (bu paket, son durum): **8 kayma kaydı** (genel `planU_A`/`planU_B` × 60 / 30 / değişken Hz = 6, ters yön planı × 60 / 30 Hz = 2) + 7 arazi kaydı, toplam 764 ölçülen ayak teması; **33 çarpışma / temas kaydı** (16'sında gerçek çarpma veya takılma; 3'ü 30 Hz; 2'si farklı ayak fazı için kaydırılmış başlangıç); 21 hareket videosu + 4 ev videosu; 3 ev akış testi (rota + odun + ateş, parça toplama, kayıt yükleme + ateş).

Test edilmeyenler (yapılmış sayılmadı): **fiziksel gamepad / analog girdi**, **standalone oyunda hareket**, paketleme. Tüm girdiler editör içinde enjekte edilen klavye tuşlarıdır.

---

## 1. Şikâyet → katman → kök neden → değişiklik

Katmanlar: kaynak klip / sürücü (kapsül) / retarget / IK / duruş-fizik katmanı / kamera. Pelvis ölçümleri **kütle merkezi değildir**; pelvis yalnızca görünür gövdenin bir göstergesi olarak raporlanıyor.

### 1.1 Zıplama / sallanma (bounce, sway)
- Katman ayrımı (`an_bob7.py`): kapsül z düz zeminde 0 (sürücü zıplamıyor); sürücü pelvis = görünür pelvis = dünya pelvis (retarget ve duruş katmanı eklemiyor). **Kaynak: klip** (`probe_loops7.py`, `data/loops7.txt`).
- Değişiklik: `ABP_Sph_GASP` içinde FootPlacement'tan **önce** pelvis için toplamalı `ModifyBone` (`SphBob`), değeri `GR_Bob` olayı yazar: klibin pelvis yüksekliği kendi yavaş ortalamasına göre yürüyüşte ×0,55, sprintte ×0,25 sönümlenir, yanal ×0,4; yalnız **sabit yürüyüşte** (hız değişimi < 200 cm/s²) açık; başlangıç, duruş, geçiş klibe dokunulmadan oynar; koşunun uçuş fazı korunur, pelvis kilitlenmez. Göğüs yuvarlanması (roll) için ayrı sönümleyici (`m_posture7_mcp.py`, PS_RK 0,6).
- Sonuç: sabit koşu (s4) pelvis tepe-tepe **7,8 → 5,9 cm**; yürüyüş **4,6 → 4,6 cm** (değişmedi); yürüyüş→koşu geçiş segmenti (s2) 7,8 → 8,1 (geçişte sönümleme kasıtlı kapalı). Yürüyüşte baş yanal 6,2 → 5,3 cm.

### 1.2 Başlangıç, hız kademeleri, momentum
- Yürüyüş başlangıçları başlangıç veritabanını kullanmıyordu: ilk karede hız IsMoving eşiğinin altında kalıyordu ve StBoost her klibi takip ediyordu. → `StSoftK 1,0` + StBoost yalnız klibin hızı **yükselirken** (`StBoostRise 250`). Yürüyüş başlangıcı artık `N_Walk_Start_F_*` (0→180 cm/s %90'a 0,32 s).
- Koşu→yürüyüş: kapsül frenlemesi üst sınırı `DmMax 650` (koşu döngüsü yavaşlarken kapsülün klipten hızlı kalması 0,00 s).

### 1.3 İleri koşarken geri (S)
- Kök neden (önce, `r7f_R` s2): fren tutma (GR_BrakeHold) sırasında MM 0,5 s boyunca **ileri koşu döngüsüne** düşüyordu; yeni yöne geçiş 0,83 s.
- Değişiklik: ters yön freninin erken tabanı `RcMin 750` (frenin ilk karesinden itibaren pivot/fren klibi ile tutarlı yavaşlama).
- Sonuç: yeni yön **0,83 → 0,25 s** (30 Hz: 0,27 s); hâlâ ileri giderken geri döngü oynama süresi 0,00 s; fren klibi `Run_Pivot_F_B` → geri koşu.

### 1.4 Görünür sendeleme / toparlanma
- Önce: kafa kafaya çarpmada senaryolu bir geri sekme hızı vardı, adım görünmüyordu.
- Değişiklik: Core Motion `ReactBumpLight` 6 klibi (Front / FrontLeft / FrontRight / Back / BackLeft / BackRight) sürücü iskeletine retarget edildi (`/Game/Sphirus/Player/Anim/React/SphR_*`, kök hareketi açık, ayak temas eğrileri klibin kendi ayaklarından üretildi). Seviye 2 çarpmada çarpma yönüne göre klip oynar; kapsülü klibin adımları taşır (ayak kaymaz). Önde engel takılması: **destek ayağına göre** `Land_Stumble_Lfoot / Rfoot` (CT_Sup seçimi gerçekten etkiliyor). Kilit bittikten sonra hareket girdisi tepkiyi güvenli fazda keser.
- Kademeler: hafif (blok) / sendeleme (adımlı) / denge kaybı (diz) / düşme. Yorgunluk, yük ve hız şiddete girer.

### 1.5 Düşme / kalkma
- Önce: göbeğe tutunan `InjuredBelly_DropToFloor` klibi; yerdeyken ve kalkarken ayak kütüğün içindeydi (f8: yatma 26 kare ≤ 5,5 cm, kalkma 14 kare ≤ 6,0 cm).
- Değişiklik: ileri düşme = `Stand_Trans_ProneCrawl` (eller yere uzanıyor, diz, yüzüstü), kalkma = `ProneCrawl_Trans_Stand`; düşme yolu **mesafeyle** (185 cm: ayaklar engelin ötesine taşınır); kalkma yalnız baş üstünde yer varsa.
- Sonuç (60 Hz, son durum): düşme 1 kare 0,7 cm; **yatma 0 kare, kalkma 0 kare**. 30 Hz (3 tekrar): düşme 3 kare ≤ 3,8 cm, kalkma 2 kare ≤ 2,6 cm.
- Yan / geri **düşme** klibi projede yok; yan ve geri **toparlanma** (adımlı) var. Ragdoll kullanılmadı: kalkma seçimi poz + zemin + baş üstü boşluğuna göre klip ile yapılıyor, ragdoll'un bu kuralları bozacağı (yer kontrolü, kamera) için gerekli görülmedi.

### 1.6 Diz yüksekliği engel, alçak engelden geçme
- Öngörülü çarpma: salınan ayak engele girmeden (mesafe < 6 + hız × 0,025) çarpma tetiklenir → diz önce: koşu 8,9 cm → **yok**.
- Ayak açıklığı IK (`ABP_Sph_Body_GASP` iki TwoBoneIK, olay `GR_Foot`): salınan ayak (sürücü temas eğrisi "serbest") altındaki yüzey zeminden 8–40 cm yüksekse bilek/top/parmak ucundan 3 noktada yükseltilir. 40 cm üstü (diz bloğu) temas sisteminin işi (aşağıda 1.8).
- Kütük (25 cm) üstünden **yürüyerek ve tempoda gerçekten geçiyor** (yavaşlayıp durmuyor): yürüyüş top 1 kare 4,2 cm, tempo 1 kare 0,8 cm.

### 1.7 Duvar sıyırma, tek el taşıma
- Sıyırmada duvar tarafı kol içeri alınıyordu ama duruş katmanının −14° tabanı bunu geri alıyordu → taban sıyırma miktarına bağlandı: dirsek **4,9 cm / 19 kare → 1,3 cm / 4 kare**.
- Tek el taşıma: bir elde eşya varken (GR_Prop / GR_PropL görünür) artık eller kapanmıyor; kafa kafaya duvarda **boştaki el** duvara uzanır (sağ elde eşya: sol el, örtüşme yok). Uzanma 70 cm'de başlar (önce 55; rampa sırasında salınan el duvarın içinden geçiyordu: 6,2 cm → yok).
- İki el yük (odun): diz bloğuna 28 cm daha erken durulur (ayak öne en uzak uzuv): ayak 9,1 cm → **yok**.

### 1.8 Dar alan
- Yeni test şeridi (test haritası): 96 cm genişliğinde koridor (yan duvarlar kapsülden 14 cm uzakta), içinde diz bloğu ve uç duvar. **Gerçek çarpma**: tempo → sendeleme (destek sağ ayak), koşu / sprint → denge kaybı → diz → kalkma; hiçbir uzuv yan duvarlara veya bloğa girmiyor; kamera her karede koridorun içinde (göğüse 101–153 cm).
- Bulunan hata: baş yüksekliği sondası göğüs sondasından 20 cm uzun olduğu için her tam boy duvar önce "baş hizasında kiriş" sanılıyordu → **kendiliğinden çömelme**, dizler duvara (14 cm). Alçak geçit artık aynı uzunlukta bir göğüs sondasının boş olmasını da istiyor; kiriş şeridinde çömelerek geçme korunuyor.

### 1.9 Geriye giderken çarpma
- Önce: geri giderken de önündeki gibi "görüp" duruyor, hatta arkaya elini uzatıyordu.
- Şimdi: 200 cm/s üstü geri harekette öngörme kapalı (yavaş, dikkatli geri adımda açık), arkadan görülmeyen çarpma ×1,4 şiddet → `ReactBumpLight_Back` (öne iki toparlanma adımı, ~1,1 m). Örtüşme yok.

### 1.10 Yorgunluk
- Yorgunlukta koşu kapanıyor (hız yürüyüşte), yürüyüş pelvis salınımı dinç ile aynı (5,0–5,8 / 4,6–5,6 cm): **kalıcı çökme yok**. Ritim, nefes ve kademeli toparlanma değişimi **yapılmadı** (aşağıda açık).

### 1.11 Kamera
- Koridor / duvar / sıyırma: kamera duvarın içine girmiyor, eller dünya tarafından örtülmüyor, FOV 66–69°.
- Maske inceleme yakınlığı: tezgâhın kamera geçersiz kılması 18 cm kol (kamera neredeyse başta) → saç/omuz kadrajın yarısı. 45 ve 60 cm kol denendi: kamera başın tam arkasına geçip **maskeyi tamamen gizledi** (`evidence/04_…`), değerler eski haline (18/24/33/0,9) döndürüldü, kaydedilmedi. **Çözülmedi.**

---

## 2. Önce → sonra (aynı analiz araçları)

`data/before.txt` (önce: tur 6 son durum f8 + tur 7 ilk kayıtları), `data/*.txt` (sonra, kaydedilmiş + yeniden açılmış).

| Ölçüm | Önce | Sonra |
|---|---|---|
| İleri koşu → S: yeni yöne geçiş | 0,83 s | **0,25 s** (30 Hz 0,27) |
| Fren sırasında ileri koşu döngüsü | ~0,5 s | 0,00 s |
| Sabit koşu pelvis tepe-tepe (s4) | 7,8 cm | **5,9 cm** |
| Yürüyüş pelvis tepe-tepe | 4,6 cm | 4,6 cm |
| Kütük sprint: yatma / kalkma örtüşmesi | 26 kare ≤ 5,5 / 14 kare ≤ 6,0 cm | **0 / 0** (30 Hz kalkma 2 kare ≤ 2,6) |
| Diz bloğu koşu: top | 8,9 cm | yok |
| Duvar sıyırma dirsek | 4,9 cm, 19 kare | 1,3 cm, 4 kare |
| İki el yük, diz bloğu: ayak | 9,1 cm | yok |
| Dar koridor yürüyüş (yalancı çömelme) | diz 14,4 cm | yok |
| Hızlı A/D (koşu, 0,4 s) en kötü kayma | 39,7 cm | **39,6 cm (değişmedi)** |
| Ayakta koşu başlangıcı: ilk 1,2 s baş düşüşü | 15,1–15,5 cm | **19,4–19,5 cm (KÖTÜLEŞTİ)** |
| 90° dönüşlü koşu başlangıcı: baş düşüşü | 17,5–19,8 cm | **19,9–22,5 cm (KÖTÜLEŞTİ)** |

Kayma özeti (son durum, `data/slide.txt`): 6 genel kayıtta ≥ 10 cm kayma yalnız 1 (30 Hz koşu durması 16,5 cm; önceki ölçümlerde 16–26 cm). Pop karesi (60 Hz) A 38 / B 75, üst gövde 10 / 11; en büyük üst gövde adımı 5,4–8,4 cm. "Pop" sayısı dar bir ölçüttür; 30 fps videoda görülen pop sayısı ayrıca sayılmadı.

Çarpışma tablosu tam hâli, faz bazında (uzuv, kare sayısı, en kötü cm): `data/contact.txt`. Kalan örtüşmeler: 30 cm basamakta koşu takılmasında baldır 12 kare ≤ 5,4 cm, top 7,1 cm (1 kare); sağ elde eşya ile duvar tarafı sıyırmada el 4 kare 5,8 cm; kütük yürüyüşte top 1 kare 4,2 cm.

Arazi (`data/terrain.txt`): merdiven çıkış / iniş (yürüyüş, koşu), rampa, zıplama — ≥ 10 cm ayak kayması yok. Merdivenlerde raporlanan uzun "hava" fazı analiz sondasının hatası: kapsülün zemin vuruşu her karede basamak üstü (z 72 / 90); gerçek hava süresi yalnız zıplamada (3 × 0,6 s).

Duruş (`data/posture.txt`): beklemede kol aralığı 10–13°/taraf, baş eğimi sabit; koşu/sprintte kol açıklığı ortalama 15–25°, kollar gövdeye yapışmıyor.

Performans (`data/perf7.txt`, test haritası, kayıt aracının 41,7 ms kare sınırı): p50 41,7 ms (değişmedi), **p95 42,3 → 44,4 ms, p99 42,6 → 45,8 ms** — kuyrukta ~2 ms artış (bu turun ek izleri: 6 ayak izi, 1 sonda, salınım olayı; bileşen bazında ayrıştırılmadı). Ev haritası eşleştirilmiş rota ölçümü bu tur **yapılmadı** (ölçüm betiği kullanıcı kaydını geçici olarak taşıyor; izin alınmadan yapılmadı).

Ev akışları (`data/house.txt`, ev haritası): yatak, maske ("Görev tamamlandı"), dolap (uzanma + giyinme), çay (alma + eve dönüş), rota + kapılar + odun + 2 parça + ateş yakma **PASS**, kayıt yükleme → ocak → ateş **PASS**. Durma (stand-off) kuralları istasyon erişimini kesmedi. Kullanıcı kaydı değişmedi.

---

## 3. Değişen varlıklar (hepsi manifest + doğrulanmış yedek ile, `data/manifests.txt`)

| Varlık | Değişiklik |
|---|---|
| `BP_HybridA_Player` | olaylar `GR_Bob` (yeni), `GR_Foot` (yeni), `GR_Contact` (m_contact7: tepki klipleri, destek ayağı, düşme/kalkma, öngörülü çarpma, diz ek mesafesi, tek el, geri çarpma, yalancı çömelme düzeltmesi), `GR_Posture` (göğüs roll sönümü, kol tabanı); yeni değişkenler + varsayılanlar |
| `ABP_Sph_GASP` | FootPlacement öncesi pelvis `ModifyBone` (`SphBob`) |
| `ABP_Sph_Body_GASP` | ayak açıklığı için iki `TwoBoneIK` (FootTR/TL, FootAR/AL) |
| `AC_Sph_Motion` + `BP_Sph_GASPCharacter` (SphMotion) | StBoost yükselme koşulu; `StSoftK 1,0`, `StBoostRise 250`, `DmMax 650`, `RcMin 750` |
| `/Game/Sphirus/Player/Anim/React/SphR_am_Stand_ReactBumpLight_*` (6 yeni) | Core Motion kopyalarından retarget; kök hareketi, temas eğrileri (orijinaller değişmedi) |
| `L_Sph_MoveTest` | dar koridor şeridi (zemin, iki yan duvar, uç duvar, diz bloğu) |

Ev haritası, ev sahnesi ve satıcı orijinalleri **değişmedi** (maske kadraj denemesi yalnız bellekte, geri alındı, kaydedilmedi).

## 4. Videolar (`videos/`, gerçek hız, omuz kamerası veya sabit yan kamera, aynı son sürüm)
01–02 yürüyüş / koşu / sprint merdiveni (omuz, yan) · 03 başlangıç / duruş (yan) · 04–05 ters yön, 90° dönüşlü başlangıçlar, hızlı A/D (omuz, yan) · 06 diz bloğu tempo sendeleme · 07–08 diz bloğu koşu denge kaybı (yan, omuz) · 09–10 kütük sprint düşme–yatma–kalkma (yan, omuz) · 11 kütük yürüyerek geçme · 12–13 dar koridor koşu / tempo · 14 geri koşu duvara çarpma · 15 duvar sıyırma (arka) · 16 tek el eşya + duvar · 17 iki el yük + diz bloğu · 18–19 merdiven çıkış / iniş · 20 zıplama + çömelme · 21 yorgun yürüyüş · 22–25 ev: yatak, maske, dolap, çay. Kare şeritleri: `evidence/01–03`.

## 5. Yapılmayanlar ve açık kalanlar
1. **Hızlı A/D (koşu, 0,4 s dokunuşlar): bir ayak 22–40 cm kayıyor.** Kök neden ölçüldü: 180° dönüş klibinin koşuya devam eden giriş fazında ayak klipte yerde ama kök 375 cm/s ilerliyor, kapsül ise zaten frenliyor (kapsül ~7 cm, ayak bileşen uzayında 82 cm). MM karışım süresi 0,5 → 0,25 denendi, iz neredeyse aynı kaldı, geri alındı. Çözüm yeni bir hızlı yanal ters yön klip ailesi gerektiriyor.
2. **Gerileme:** ayakta koşu başlangıcında baş düşüşü 15,3 → 19,4 cm, 90° dönüşlü koşu başlangıcında 17,5–19,8 → 19,9–22,5 cm arttı. Olası sahipler bu turun başlangıç değişiklikleri (yürüyüş başlangıcı → yürüyüş-koşu geçiş klibi zinciri, StSoftK / StBoostRise); ayrıştırılmadı. 45 / 135 / 180° dönüşlü başlangıç bu planda ölçülmedi.
3. Kafa kafaya tepki kliplerinde destek ayağı seçimi yok (klipler çarpma yönüne göre; ayak sırası sabit). Takılmada destek ayağı var.
4. `ReactBumpLight_BackLeft / BackRight` bağlandı ama testlerde tetiklenmedi (25° geri çarpma hafif blok kaldı). Doğrulanmadı.
5. Sağ elde eşya ile o taraftaki duvarı sıyırma: el 5,8 cm. Kök: eşyalı kol boş kol gibi sallanıyor (tek el taşıma kol pozu yok).
6. 30 cm basamakta koşu takılması: baldır 12 kare ≤ 5,4 cm.
7. Yorgunluk: ritim / nefes / kademeli toparlanma değişimi yok; yalnız hız sınırı.
8. Kamera: Shift basılı ama hız yürüyüşte iken (yorgun / yumuşak başlangıç) omuz kamerası dikeyde 8,5–12,8 cm oynuyor (baş ~7 cm, düz yürüyüşte kamera 1,2–1,4 cm) → kamera bu durumda salınımı **büyütüyor**. Dar koridorda sendelemede kamera saça çok yaklaşıyor (`evidence/03`). Maske inceleme kadrajı çözülmedi.
9. Performans kuyruğu +2 ms (p95/p99), ayrıştırılmadı; ev rotası ölçümü yapılmadı.
10. Analog / gamepad, standalone hareket, fiziksel cihaz: **test edilmedi**.

## 6. Yeniden üretim
`scripts/final_r7.sh` (bütün son doğrulama), analizler `an_bob7.py`, `an_rev7.py`, `an_trans7.py`, `an_ct7.py` (faz bazında örtüşme), `an_slide3.py` / `an_terr6.py` / `an_post6.py` (önceki turlardan, değişmedi). Temas betiği `mk_contact7.py` ile tur 6 betiğinden doğrulanmış metin değişiklikleriyle üretilir (`m_contact7_mcp.py`, `c_contact7_defaults.py`). Ham kayıtlar `raw/*.json.xz`.
