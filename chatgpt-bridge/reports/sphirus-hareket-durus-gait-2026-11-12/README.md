# Sphirus: hareket, duruş, gait ve zıplama düzeltmesi (2026-11-12)

Bu rapor "HAREKET, POSTURE, GAIT VE ETKİLEŞİM KAMERASI DÜZELTME GÖREVİ"nin gerçek projedeki uygulamasını, önce/sonra ölçümlerini ve oyundan alınmış gerçek hızda videoları içerir. Görevin etkileşim kamerası ve genel oyun kamerası bölümleri (6 ve 7) bir önceki kamera görevinde yapıldı (`chatgpt-bridge/reports/sphirus-kamera-oynanis-atmosfer-2026-11-12`); burada yeniden yapılmadı, yalnız durumları özetlendi. **Kullanıcı kabulü yok** — her satırda teknik sonuç, benim görsel incelemem ve kullanıcı kabulü ayrı yazıldı.

Amaç yeni animasyon paketi denemek değildi: hiçbir klip, Motion Matching veritabanı, retarget varlığı ya da satıcı dosyası değişmedi; reddedilen Core Motion C profili kapalı. Değişiklikler mevcut etkin oyuncunun (`BP_HybridA_Player`) tek sahipli katmanlarında: girdi + gait seçimi (oyuncu), hareket fiziği durumu (`AC_Sph_Motion`), görünen beden (`ABP_Sph_Body_GASP`, retarget sonrası).

## 0. Başlangıç ve korunanlar

- Motor 5.8.4, harita `L_GR_SphirusHouse`; düz test haritası `L_Sph_MoveTest` beden incelemesi için.
- Hareket tabanı: GASP Relaxed (erkek mocap `M_Relaxed_*`) → UEFN manken → `RTG_Sph_UEFN_to_MH` → MetaHuman beden. Hızlar 165 / 375 / 585 cm/sn.
- Senin kaydın `SFSaveSlot.sav` (SHA1 `66556281…`) her testte kenara alınıp bayt bayt geri kondu; iş sonunda SHA1 aynı.
- Geri dönüş noktası: `C:\Users\berat\SphirusCheckpoints\Motion_Pre_20261112_1200` + her yazma işinin manifest yedeği (ayrıntı `changes/changes.md`).

Ölçüm yöntemi: her senaryo editörde gerçek oyun (PIE) olarak 30 kare/sn sabit adımla oynatıldı; her karede görünen bedenin kemik konumları, göz konumları, hız, gait durumu ve katman sinyalleri kaydedildi (`Saved/Codex/Grip_20261106/rec/*.json`). "Önce" = A kayıtları (bu görevden önceki durum), "sonra" = D kayıtları (değerler kalıcı varsayılan olarak kaydedildikten sonra, hiçbir çalışma zamanı müdahalesi olmadan).

## 1. Sonuç özeti

| Konu (senin geri bildirimin) | Önce (A) | Sonra | Teknik | Görsel incelemem | Kullanıcı kabulü |
|---|---|---|---|---|---|
| Gait yapısı: iç mekân yürüyüş + tempolu; dışarıda yürüyüş, tempolu, jog, koşu | 3 hız; Shift 0,9 sn = sprint; içeride tek hız | Ctrl = yürüme/koşu modu, Shift = bir kademe hızlı; içeride 150/195, dışarıda 165/214/375/585 | IMPLEMENTED, TECH_TESTED: PASS (düz harita, koridor, kapı, bahçe, patika, kayıt/yükleme sonrası) | VISUALLY_INSPECTED | yok |
| Yürüyüşten koşuya ani fırlama | yürüyüş → jog 0,13–0,23 sn (796 cm/sn²) | 0,33 sn; jog → koşu 0,57 sn (467 cm/sn²) | TECH_TESTED: PASS | — | yok |
| Kollar açılıyor / erkeksi yürüyüş | eller omuz hattının 10–12 cm (koşuda 34–41) dışında | 7–9 cm (koşuda en çok 17–21) | IMPLEMENTED, TECH_TESTED | VISUALLY_INSPECTED: kollar gövdeye yakın, yapışık değil | yok — kalça/adım hâlâ erkek klipten (PARTIAL) |
| Boyun önde ve yamuk | baş göğsün 4,8–5,1 cm önünde, üst hat 12–13°; baş eğikliği −0,7..−3,9° | 1,5–1,8 cm, 4°; eğiklik +0,4..+1,7° (baş düzleme) | IMPLEMENTED, TECH_TESTED: PASS | VISUALLY_INSPECTED: baş omuzların üstünde | yok |
| Koşu fiziksel değil / sprinter dalışı | gövde 33°, baş yere bakıyor, baş ±21–26° sallanıyor | gövde 23°, bakış yolda, baş −1..+4° | TECH_TESTED | VISUALLY_INSPECTED | yok |
| İleri zıplama düz hoplama | her hızda 127 cm / 1,0 sn; havada iki diz toplu; inişte 72° katlanma | 59–65 cm / 0,60–0,63 sn; mesafe 161 / 265 / 366 cm (yürüyüş/jog/koşu); havada adım açılımı; inişte en çok 49° | IMPLEMENTED, TECH_TESTED | VISUALLY_INSPECTED: yürüyüş/jog iyi; koşu zıplamasının tepesi hâlâ dik (PARTIAL) | yok |
| Uzun koşu sonrası yorgunluk | görünür değil (efor 5 sn'de sıfırlanıyor) | yavaş yorgunluk: 20 sn koşudan sonra nefes ~40/dk, omuzlar 2,5 cm inip kalkıyor, hafif öne düşüş; ~13 sn'de sakinleşiyor | IMPLEMENTED, TECH_TESTED | PARTIAL: göğüs az kalkıyor; dinlenme pozu yok | yok |
| İç mekânda yavaş tempo, koşu yok | — | koridor/kapı: 150 / 194; Ctrl reddediliyor | TECH_TESTED: PASS | — | yok |
| İki elle odun taşırken koşu | (kamera görevinde koşu/zıplama kapatılmıştı) | yürüyüş 148, tempolu 172, koşu modu ve zıplama yok | TECH_TESTED: PASS | VISUALLY_INSPECTED: demet iki elde | yok |
| Nesneyle zıplayınca tutuş tek ele düşüyor | maske taşırken zıplama serbestti (iki el arası zıplamada değişmedi: 23,6–25 cm) | maske de iki elli yük: zıplama ve koşu kapalı, tempolu var | TECH_TESTED: PASS | PARTIAL: maske önden görüntüde seçilemedi (kamera saça girdi, §12) | yok |
| Kamera (görev 6–7) | — | kamera görevinde teslim; bu görevde yalnız havada dikey izleme | TECH_TESTED: zıplamada kadraj dışı kare 15 → 0 | — | yok |
| Kayıt / yükleme sonrası hareket | — | kayıt, oturum içi yükleme ve açılışta yükleme sonrası gait merdiveni aynı | TECH_TESTED: PASS | — | yok |
| Temiz açılış | — | 9 Blueprint güncel ve hatasız, kirli paket yok, oyunda çalışma zamanı hatası 0 | PASS | — | — |
| Performans | — | ölçülmedi (yeni katman 21 kemik düğümü + 1 LookAt, beden ABP'sinde) | NOT_TESTED | — | — |

Durum etiketleri: IMPLEMENTED = projede kayıtlı; TECH_TESTED = gerçek oyunda ölçüldü; VISUALLY_INSPECTED = saniyede bir kare ve zıplama/inişte kare kare çıkarılmış görüntüleri inceledim; USER_ACCEPTED = yok.

## 2. Gait yapısı ve tempolu yürüyüş

Önce: üç hız vardı ama denetim kabaydı — Shift'i 0,9 sn basılı tutmak sprinti seçiyordu, arada "jog" tutmanın yolu yoktu; ev içinde tek hız (150).

Sonra (tek sahip: `BP_HybridA_Player` gait zinciri, okuyucuları değişmedi):

| Gait | Nasıl | Hız (dış / iç) | Klip ailesi |
|---|---|---|---|
| Yürüyüş | varsayılan | 165 / 150 | Relaxed Walk |
| Tempolu yürüyüş | yürüme modunda **Shift basılı** | 214 / 195 | Relaxed Walk, Motion Matching oynatma hızı ~1,3 (adım süresi 0,53 → 0,40 sn) |
| Jog | **Sol Ctrl** (gamepad sol omuz) koşu moduna geçirir | 375 / — | Relaxed Run |
| Koşu | koşu modunda **Shift basılı** | 585 / — | Relaxed Sprint |

- Ctrl bir anahtar: koşu modu ↔ yürüme modu. Shift her modda "bir kademe hızlı". Koşu, joglarken (hız > 250) ya da zaten koşarken seçilir: duruştan önce jog'a çıkar, sonra koşuya geçer.
- **Ev içinde** (`GR_HomeContext`) koşu modu kapanır ve açılamaz: yalnız yürüyüş (150) ve tempolu (195).
- İki elli yükte (odun demeti ya da maske) koşu modu kapanır: yürüyüş 148, tempolu 172 (ayrıntı §8).
- Geçişler: ölçülen (düz harita, `M_gaits_D`) yürüyüş 165 → tempolu 214 → yürüyüş → (Ctrl) jog 375 → (Shift) koşu 585 → jog → (Ctrl) yürüyüş. Tüm adımlarda gait durumu ve hız beklenen değerde; tempoluda ayak kayması yürüyüşle aynı düzeyde (1–9 cm, yürüyüş 2–7 cm).
- Ani fırlama: yürüyüşten joga 0,23 sn'de (721 cm/sn²) çıkıyordu. Düz giderken üst gait'e geçişte ivme 0,55 ile ölçeklendi (`AC_Sph_Motion.GaitUpAcc`; duruştan kalkış, dönüş, ters dönüş ve fren değişmedi). Ölçü (`M_gaits_D` → `M_gaits_E`, %10–90 süresi): yürüyüş → jog 0,13 → 0,33 sn, jog → koşu 0,33 → 0,57 sn; en yüksek ivme 796 → 467 cm/sn². Ayak kayması değişmedi (tempolu 1–6 cm, jog 2–13 cm, koşu 1–10 cm).

## 3. Kadın beden dili (kollar, omuzlar, pelvis–göğüs)

Kök neden: hareket klipleri erkek mocap (`M_Relaxed_*`), UEFN mankenden MetaHuman bedene aktarılıyor. Bu bedenin kendi referans pozuna göre ölçtüğüm sapmalar: eller omuz ekleminin 10–12 cm dışında asılı (yürüyüş salınımında 15–19, sprintte 34–41 cm), baş göğüs ekleminin 4,8–5,1 cm önünde (referans pozda 0,4), sprintte gövde 27–33° (kalkışta 40–45°) öne yatık, baş sağa-sola ±21–26° sallanıyor.

Çözüm: görünen bedende retarget'tan sonra çalışan bir **duruş katmanı** (`ABP_Sph_Body_GASP`; 13 kemik, bileşen uzayında toplamsal döndürme). Her kemik için `sabit + koşu payı × RunA + ivme payı × AccA + yorgunluk payı × EffA`; kollar etkileşim montajlarında otomatik sönüyor (`ArmW`), yani odun/maske/kapı pozları kendi elleriyle kalıyor. Bütün hızları yavaşlatmak ya da gövdeyi dondurmak yok: klipten gelen salınım, pelvis–göğüs karşı dönüşü ve adım ritmi aynen duruyor (ölçü, yürüyüş: el salınımı 48,5/35,2 → 48,2/34,1 cm, pelvis yanal salınımı 8,3 → 8,3 cm, inip kalkma 10,2 → 10,3 cm).

| Ölçü (görünen beden) | Önce (A) | Sonra (D) |
|---|---|---|
| Durma: el, omuz ekleminin dışında (sol / sağ) | 11,2 / 11,1 cm | 6,9 / 8,4 cm |
| Durma: dirsek dışarıda | 8,4 / 6,8 cm | 6,3 / 5,4 cm |
| Yürüyüş: el dışarıda, ortalama (en çok) | 10,1 (14,8) / 12,2 (17,8) cm | 7,5 (13,1) / 9,3 (15,8) cm |
| Yürüyüş: dirsek dışarıda | 8,0 / 8,2 cm | 6,5 / 6,7 cm |
| Koşu: el dışarıda, ortalama (en çok) | 9,9 (40,6) / 10,4 (34,3) cm | 4,1 (17,0) / 5,3 (21,4) cm |
| Koşu: dirsek dışarıda | 14,0 / 14,0 cm | 9,9 / 11,3 cm |
| Koşu: gövde öne eğimi (pelvis → göğüs) | 32,6° | 22,9° |

Görsel incelemem (VISUALLY_INSPECTED, `evidence/durus_*_once_sonra.png`): yürüyüşte kollar gövdeye daha yakın ama yapışık değil, dirsek doğal kırık; koşuda kollar gövdenin önünde, eller göğüs hizasının altında, omuzlar düşük. Klipler hâlâ erkek mocap: adım genişliği, kalça hareketi ve ağırlık aktarımı kaynak klipten geliyor — bunlar duruş katmanıyla değil ancak kadın kaynaklı kliplerle ya da adım/kalça için ayrı bir bacak katmanıyla değişir (bu görevde yapılmadı, §10).

## 4. Boyun, baş, omuz kuşağı ve üst omurga (P0)

| Ölçü | Referans poz (bedenin kendi bind pozu) | Önce (A) | Sonra (D) |
|---|---|---|---|
| Durma: baş, göğüs ekleminin (spine_05) önünde | 0,4 cm | 4,8 cm | 1,6 cm |
| Durma: boyun tabanı göğüs ekleminin önünde | −1,8 cm | 1,7 cm | 0,3 cm |
| Durma: üst hat eğimi (göğüs → baş) | ~1° | 12,4° | 4,2° |
| Durma: göz hattı yatıklığı (baş eğikliği) | +1° | −3,9° / −0,7° (iki kayıt)* | +1,7° / +0,4° (baş düzleme ile; düzlemesiz son kayıtta −0,9° / −2,2°) |
| Yürüyüş: göz hattı yatıklığı, ortalama (aralık) | — | −1,3° (−5,8..+3,0) | +0,3° (−4,2..+4,3) |
| Yürüyüş: baş göğsün önünde | 0,4 cm | 5,1 cm | 1,5 cm |
| Yürüyüş: üst hat eğimi | — | 13,3° | 4,0° |
| Koşu: baş göğsün önünde / üst hat eğimi | — | 15,0 cm / 45,6° | 7,2 cm / 19,2° |
| Koşu: bakış (yüz eğimi; + = ileri) | — | 7° (yere bakıyor) | 29° (yola bakıyor) |
| Koşu: baş sallanması (sağ-sol, en küçük..en büyük) | — | −21..+26° | −1..+4° |
| Omuz eklemi genişliği | 24,6 cm | 24,5 cm | 24,5 cm |

\* Bekleme klibi beş varyant arasında dönüyor; baş eğikliği varyanta göre −0,7° ile −3,9° arasında değişiyor. Bu yüzden ayrı bir **baş düzleme** eklendi (önceki kareden başın yan ekseninin yataydan sapmasını ölçen, ±8° sınırlı, ~2 sn'lik yavaş integratör: kalıcı eğikliği alır, yürüyüşün doğal salınımını bırakır; montajlarda kapalı).

Ne yapıldı: göğüs (spine_05) −9° geriye açıldı ve baş +8° düzeltildi (çene geri, boyun dik), kollar göğsün açılmasını telafi edip dikey asılacak şekilde öne alındı; koşuda ve ivmelenmede spine_03/05 dikleştirildi; başa ileriye bakan hafif bir LookAt (durma 0,2 / yürüyüş 0,35 / koşu 0,65 ağırlık, 40° sınır). Retarget pozuna dokunulmadı (bacak IK hedefleri retarget'ta; kalça/omurga ofseti ayak temasını bozardı).

Omuz kuşağı: omuz eklemleri arası oyunda 24,5 cm, bedenin kendi bind pozunda 24,6 cm — genişlik ve yükseklik bind ile uyumlu, bu yüzden klavikulalara sabit bir düzeltme verilmedi (yalnız yorgunlukta ±7° öne yuvarlanma). Omuz kuşağı oturuşu (kıyafetle birlikte) için ayrı bir görsel karşılaştırmayı senin bakışına bırakıyorum: ölçü uyumlu, görünüş kabulü yok.

## 5. İleri / hareketli zıplama

Önce: her hızda aynı 500 cm/sn dikey itiş: 127 cm apeks, 1,0 sn havada; GASP zıplama klipleri havada dik gövde + iki diz birden toplu ("yerinde hoplama"), iniş klipleri bu büyük düşüşe göre gövdeyi 49–72° katlayıp başı yere indiriyor.

Sonra:
- Fizik (oyuncu): yerçekimi ölçeği 1,25; kalkış hızı duruş 400 / yürüyüş 385 / jog 400 / koşu 380 → apeks 59–65 cm, havada 0,60–0,63 sn. Hareket girdisiyle kalkışta ileri taşıma: yürüyüşte en az 255 cm/sn, jog +45, koşu +25.
- Havada adım (görünen beden, yeni katman): kalkışta hangi ayak öndeyse o bacak öne uzanıp diz açılıyor, arkadaki bacak geride diz kırık; göğüs hızla birlikte 5° öne. Ağırlık hızla ölçekli (duruş zıplamasında yok, koşuda tam).
- İniş: iniş anında göğüs yayına hızla orantılı bir tekme (ağırlık hissi) ve **eğim sınırlayıcı**: inişten sonraki 0,9 sn'de gövde katlanması 30°'yi aşarsa fazlası alt omurgada geri alınıyor (en çok 40°), dizler yükü emmeye devam ediyor. Aynı sınırlayıcı her zaman 40° üstünü de kesiyor (sprint/jog duruş kliplerinin dize kadar katlanması).

| Zıplama | Önce: apeks / hava / mesafe | Sonra: apeks / hava / mesafe | İniş: en büyük eğim, baş en alçak (önce → sonra) |
|---|---|---|---|
| Duruş | 128 cm / 1,00 sn / 0 | 65 cm / 0,63 sn / 0 | 49° → 40°, 5 → 18 cm |
| Yürüyüş (165) | 128 / 1,00 / 166 cm | 60 / 0,63 / 161 cm | 28° → 27°, 26 → 29 cm |
| Tempolu (214) | — | 60 / 0,63 / 162 cm | 27°, 29 cm |
| Jog (375) | — | 65 / 0,63 / 265 cm | 49°, 16 cm |
| Koşu (585) | 127 / 1,00 / 586 cm | 59 / 0,60 / 366 cm | 72° → 49°, −5 → 19 cm |

(Baş yüksekliği aktörün merkezine göre; ayakta ~70 cm.)

Görsel incelemem (`evidence/ziplama_*`): yürüyüş ve jog zıplamasında havada adım açılımı okunuyor, inişte gövde dik kalıp dizler kırılıyor; koşu zıplamasında tepe anında poz hâlâ fazla dik (klibin kendisi) — PARTIAL. Yürüyüş/jog/koşu zıplamaları artık mesafe, hız ve iniş klibiyle ayrışıyor.

Oyun kamerası: zıplama tepesinde baş 4–5 kare kadraj üstünden çıkıyordu (kamera pivotu havada 5/sn ile geride kalıyordu); havadayken dikey izleme hızlandırıldı (§7).

## 6. Efor ve yorgunluk

Önce: hızlı efor (`E`) her sprintte 3 sn'de doluyor, durunca 5 sn'de bitiyordu: uzun koşu ile kısa koşu aynı görünüyordu; görünür tek iz hafif nefes.

Sonra (`AC_Sph_Motion.Fat`, yavaş yorgunluk): yalnız efor yüksekken birikir (koşuda ~17 sn'de dolar, jogda ~50 sn; sakin yürüyüşte hiç), dururken ~13 sn'de, hızlı hareket ederken daha yavaş boşalır. Görünen beden: nefes genliği ve hızı yorgunlukla artar, durunca göğüs ve omuzlar hafif öne düşer, baş hafif iner (`VE_*`). Yeniden hızlanma ivmesi ×(1 − 0,15·Fat). Kontrol gecikmesi, hız sınırı, sendeleme yok.

| 20 sn jog+koşu, sonra 10 sn durma (`M_effort_D`) | 0–3 sn | 3–6 sn | 6–10 sn | sonra yürüyüş |
|---|---|---|---|---|
| Yorgunluk (Fat) | 1,00 | 0,97 | 0,73 | 0,46 |
| Omuz inip kalkması (tepe–tepe) | (duruş adımı) | 2,5 cm | 2,1 cm | 2,9 cm |
| Nefes / dk | — | ~40 | ~30 | — |
| Gövde öne eğimi | — | 3,8° | 1,8° | 6,1° |

Sakin durmada (yorgunluk 0) nefes 13/dk ve omuz hareketi belirsiz düzeyde — sürekli soluma yok. PARTIAL: göğüs kafesinin kendisi az kalkıyor (0,5 cm); yorgunluğu esas omuz/klavikula hareketi ve hafif öne düşüş gösteriyor. "Eller dizde/belde" gibi bir dinlenme pozu yok (klip gerektirir).

## 7. Etkileşim ve oyun kamerası (görev 6–7)

Senin notun üzerine bu bölümler yeniden yapılmadı; kamera görevinde teslim edildi (tek sahip `AC_Sph_Camera`, istasyon bağlam sözleşmesi, iş kadrajları). Bu görevde kameraya tek ek dokunuş: **havada dikey izleme**. Zıplama tepesinde baş 4–5 kare kadrajın üstünden çıkıyordu (pivot yükseklik süzgeci 5/sn ve 20 cm sınırla, baş yüksekliği süzgeci 2,5/sn ile geride kalıyordu). Karakter havadayken bu iki süzgeç 25/sn ve 8/sn çalışıyor; yerde hiçbir şey değişmedi. Sonuç: oyun kamerasıyla zıplamada kadraj dışı kare 15 → 0, baş havada ekranın 0,17–0,51 aralığında (`sonra_ziplama_oyun_kamerasi`).

## 8. Taşıma kuralları

| Durum | Yürüyüş / tempolu | Jog / koşu | Zıplama | Kaynak |
|---|---|---|---|---|
| Elde bir şey yok | 165 / 214 (ev içi 150 / 195) | 375 / 585 (ev içinde yok) | var (gait'e göre) | §2, §5 |
| İki elli yük (odun kucakta, `AM_GR_Day_CarryArms`) | 148 / 172 | yok (koşu modu kapanır) | yok | `GR_Load2H` |
| Maske taşıma (`AM_GR_Mask_Carry`, UpperBody; iki el önde, 24 cm arayla) | 148 / 172 (ev içinde 150 / 175) | yok | yok | `GR_CarryActive` → `GR_Load2H` |

- Kural: iki elle taşınan her şey (odun demeti, maske) aynı tek bayrağı (`GR_Load2H`) açar: koşu modu kapanır, zıplama reddedilir, yürüyüş ve tempolu kalır, kamera taşıma kadrajına geçer. Projede şu an tek elle taşınan bir taşıma durumu yok (bitki/parça alma anlık eylemler); tek el kuralı için bağlantı noktası hazır (`GR_KCarryJog` 0,9 — şu an kullanılmıyor).
- Ölçüm (gerçek harita, `F_carry_F`): odun kucakta yürüyüş 148, Shift ile 172; Ctrl + Shift ile koşu açılmadı (Pace 0); Space ile zıplama olmadı; kol duruş katmanı montaj süresince sıfır (ArmW 0) — kolları ve elleri montaj taşıyor, gövde/boyun düzeltmesi açık kalıyor. Görüntüde demet iki elde, kamera görevindeki taşıma kaydıyla aynı tutuş (`evidence/odun_alma_tasima_kesme.png`).
- Maske (`K_mask_F`, kural öncesi): yerinde bir zıplamada iki el arası 23,6–25 cm'de kaldı (tutuş iki elde). Kural sonrası (`K_mask_G`): zıplama yok, iki el arası 24–27 cm, koşu modu kapalı.
- El/nesne/omurga/kamera birlikte: odun taşımada hepsi görünür; maske taşımada karakter tezgâh önünde kameraya doğru geri yürüdüğünde kamera saça girdi ve maske görünmedi — kamera kusuru (§12).

## 9. Gerçek haritada ve kayıt/yüklemede doğrulama

| Akış | Ölçülen | Sonuç |
|---|---|---|
| Ev içi koridor (`F_hall_F`) | yürüyüş 150, Shift 194; Ctrl + Shift: koşu modu açılmadı, tempolu kaldı | TECH_TESTED: PASS (rota 4,5 sn sonra duvara ulaştı; sonrası duran karakter) |
| Kapıdan çıkış (`F_exit_F`) | içeride tempolu 194 → eşikte ev bağlamı kalkınca 214; kapı açılırken ~3 sn bekleme (kapı) | TECH_TESTED: PASS |
| Bahçe (`F_out_F`) | 165 → 214 → (Ctrl) jog 375 → (Shift) koşu; koşu 2 sn sonra bahçe sınırına çarptı; yürürken zıplama 255 cm/sn ile | TECH_TESTED: PASS (koşu kısa) |
| Patika (`F_trail_G`) | 165 → 214 → jog 375 → koşu 585 → jog → duruş | TECH_TESTED: PASS |
| Patikada zıplamalar (`F_trailj_G`) | yürüyüş 0,67 sn / 170 cm, jog 0,60 sn / 251 cm, koşu (yokuşta erken temas); baş havada ekranın 0,11–0,47'sinde | TECH_TESTED: PASS |
| Odun alma → taşıma → kesme (`F_chop2_F`) | alma montajı, kucakta yürüme 150, kütüğe varış, kesme montajı; çalışma zamanı hatası yok | TECH_TESTED: PASS |
| Odunla hareket (`F_carry_F`) | §8 | TECH_TESTED: PASS |
| Maske tezgâhı, bakma (`F_bench_F`) | inceleme montajı, sağ el hiç örtülmedi, kol katmanı montajda kapalı | TECH_TESTED: PASS |
| Maske taşıma (`K_mask_G`) | §8 | TECH_TESTED: PASS; görsel PARTIAL |
| Kayıt / yükleme (`data/kayit_yukleme_hareket.txt`) | yeni oyun → merdiven → kayıt → 7 m ışınla → oturum içi yükleme → merdiven → editörü kapatıp aç (açılışta yükleme) → merdiven: üçünde de 165 / 214 / 375 / koşu durumu aynı; kullanıcı kaydı bayt bayt geri | TECH_TESTED: PASS. Not: test yardımcısı `LoadGame(IgnorePlayerLocation=True)` çağırdığı için konum geri gelmiyor (Story Framework bilerek; 10 Kasım raporunda açıklandı). Yükleme sonrası zıplama bu probla ölçülemedi (komut gecikmesi) — NOT_TESTED |
| Gamepad | sol omuz = Ctrl eşlendi | NOT_TESTED |

## 10. Nasıl terfi edildi (promotion)

Yeni bir anahtar ya da paralel sistem yok: değişiklikler doğrudan etkin oyuncunun mevcut sahiplerine yazıldı ve sınıf varsayılanı oldu. Sıra: ölçüm (A) → katmanlar nötr değerlerle kuruldu → değerler çalışma zamanında aday dosyalarıyla denendi (C1 duruş, C2 havada adım + baş bakışı, C3 yorgunluk duruşu + iniş) → C3 sınıf varsayılanına yazıldı ve geri okunarak doğrulandı (`p2_values.py`, VERIFY bad []) → hiçbir müdahale olmadan son kayıtlar (D, E, F) → temiz açılış denetimi. Her yazma: kapılı çalıştırıcı, manifest yedeği, tek kilit sahibi; bir iş, editör yeniden başlarken kuyrukta kaldığı için kapı tarafından "eski iş" olarak reddedildi ve yeniden çalıştırıldı (hiçbir şey yarım yazılmadı).

Temiz açılış (`data/temiz_acilis_denetimi.txt`): editör kapatılıp açıldıktan sonra `BP_HybridA_Player`, `ABP_Sph_Body_GASP`, `AC_Sph_Motion`, `AC_Sph_Camera`, `BP_Sph_GASPCharacter`, `ABP_Sph_GASP`, `BP_GR_DayStation`, `BP_GR_DayHub`, `BP_GR_MaskBench` güncel ve hatasız; kayıtlı varsayılanlar beklenen değerlerde; kirli paket yok; `ABP_Sph_GASP.SphCM = False` (reddedilen Core Motion profili kapalı), GASP hızları 165 / 375 / 585. Akış kayıtlarının editör günlüklerinde Blueprint çalışma zamanı hatası 0.

## 11. Videolar (gerçek hız, 30 kare/sn)

Hepsi oyundan, 30 kare/sn sabit adımla alınıp 30 kare/sn kodlandı (gerçek hız). `once_A_*` = bu görevden önce, `sonra_*` = son durum, `ara_*` = arada.

| Video | Ne gösteriyor |
|---|---|
| `once_A_yandan_durma_yuruyus_kosu` / `sonra_yandan_durma_yuruyus_kosu` | yandan: durma, yürüyüş, duruş, koşuya kalkış, koşu, geri yürüme |
| `once_A_onden_*` / `sonra_onden_*` | aynı akış önden |
| `once_A_arkadan_*` / `sonra_arkadan_*` | aynı akış arkadan |
| `sonra_gait_merdiveni_yandan` | yürüyüş → tempolu → yürüyüş → jog → koşu → jog → yürüyüş |
| `sonra_gait_merdiveni_oyun_kamerasi` | aynı merdiven, oyun kamerası (yumuşak gait geçişinden önceki kayıt) |
| `sonra_patika_gait_merdiveni` | gerçek haritada patikada merdiven |
| `once_A_ziplama_yandan` / `sonra_ziplama_yandan` | durma, yürüyüş, (sonra: tempolu, jog), koşu zıplamaları |
| `ara_ziplama_oyun_kamerasi_kamera_yamasi_oncesi` / `sonra_ziplama_oyun_kamerasi` | oyun kamerasından zıplama; kamera yamasından önce baş tepede kadraj dışı |
| `sonra_patika_ziplamalar` | patikada yürüyüş/jog/koşu zıplamaları |
| `sonra_efor_uzun_kosu_yandan` / `sonra_efor_uzun_kosu_oyun_kamerasi` | 20 sn jog + koşu, duruş, 10 sn soluklanma, yeniden yürüme |
| `sonra_ev_ici_koridor_yuruyus_tempolu`, `sonra_kapidan_cikis_tempolu` | ev içi yürüyüş/tempolu, kapıdan çıkış |
| `sonra_bahce_gait_ziplama` | bahçede merdiven ve yürürken zıplama |
| `sonra_odun_alma_tasima_kesme`, `sonra_odun_tasima_kurallar` | odun alma, kucakta taşıma, kesme; taşırken tempolu, reddedilen koşu ve zıplama |
| `sonra_maske_tezgah_bakis` | maskeye bakma |
| `sonra_maske_tasima_iki_el_kurali` | maske bağlama, alma, taşıma; reddedilen zıplama |

## 12. Açık kalanlar ve dürüst sınırlar

- **Kullanıcı kabulü yok.** Görsel incelemem saniyede bir kare ve zıplama/iniş için kare kare çıkarılmış görüntülere dayanıyor; videoları gerçek hızda izleyemiyorum.
- Klipler erkek mocap: adım genişliği, kalça hareketi, ağırlık aktarımı kaynak klipten geliyor. Kollar, omuzlar, boyun, baş, gövde eğimi düzeltildi; "erkeksi yürüyüş" hissinin kalçadan/adımdan gelen kısmı bu katmanla değişmez. Bunun için kadın kaynaklı yürüyüş klipleri gerekir — "toplu animasyon değişimi yapma" kuralı nedeniyle bu görevde yapılmadı.
- Koşu zıplamasının tepe anı hâlâ dik (klipten). Havada adım ağırlığı ve iniş sınırlayıcı iyileştiriyor ama "koşarak sıçrama" klibinin yerini tutmuyor.
- Yorgunlukta "eller belde / dizde" dinlenme pozu yok; yorgunluk nefes, omuz ve hafif öne düşüşle okunuyor.
- Jog'dan koşuya geçerken bir geçiş klibi (`Transition_Run_to_Sprint_Lfoot`) başı ~1 sn boyunca ±10–15° sallıyor; klibin kendisi.
- Ev içi/dış ayrımı mevcut `GR_HomeContext` hacimlerine bağlı; eşikte geçiş anlık.
- Gamepad: Ctrl karşılığı sol omuz eşlendi, gamepad ile sınanmadı (NOT_TESTED).
- Performans bu görevde ölçülmedi (NOT_TESTED). Ek maliyet: görünen beden ABP'sinde 21 kemik değiştirme düğümü + 1 LookAt ve olay grafiğinde birkaç soket okuması.
- **Bulunan kamera kusuru:** maske taşırken tezgâhın önünde kameraya doğru geri yürüyünce kamera karakterin saçının içine girdi (`sonra_maske_tasima_iki_el_kurali`, 22.–27. sn). Kamera bileşeninin dar alan davranışı; kamera kalanlarıyla birlikte ele alınacak.
- Sprint/jog duruş klibi dizleri derin kırıyor; eğim sınırlayıcı gövdeyi 40°'de tutuyor ama çömelme klipten.
- Bekleme klibi varyantları arasında baş eğikliği değişiyor; baş düzleme ~2 sn'de oturuyor, bir varyant değiştiğinde kısa bir an eğik kalabilir.
