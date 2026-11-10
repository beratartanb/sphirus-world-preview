# Sphirus: GASP Relaxed + SHME tam beden fiziği + seçici Core Motion (2026-11-10 akşam)

Başlangıç: `sphirus-gasp-shme-coremotion-final-2026-11-10` raporu (GASP Normal üretimde). Bu tur yeni bir framework kurmadı; aynı oyuncu, aynı AnimBP zinciri ve aynı hareket bileşeni geliştirildi. Bütün sayılar gerçek PIE kayıtlarından (30 kare/s sabit oyun adımı, gerçek zaman, `data/*.json`), aynı MetaHuman (yüz/saç/kıyafet değişmedi), ev haritası ya da düz test sahnesi. Etiketler: **TECH_PASS** (ölçüm geçti), **VISUAL_REVIEW_REQUIRED** (görsel/his kararı kullanıcıda), **PARTIAL**, **FAIL**, **NOT_TESTED**. Kullanıcı bu sürümü henüz oynamadı; hiçbir madde "doğal bulundu" anlamına gelmez.

## 0. Özet

| Konu | Sonuç | Bölüm |
|---|---|---|
| GASP Relaxed ailesi gerçekten çalışıyor (seçilen klipler `M_Relaxed_*`, Sphirus chooser kopyası, bağlam `ABP_Sph_GASP_C`) ve aktif oyuncuda | **TECH_PASS**; görünüm VISUAL_REVIEW_REQUIRED | §1, §2 |
| Hız–kadans sözleşmesi: yürüme 165 / koşu 375 / sprint 585 cm/s = Relaxed kliplerin kendi kök hızları | **TECH_PASS** | §3 |
| Duruş artık klibin fren süresinde: sprint 0,33 → 0,83 s; yürüme 0,13 → 0,47 s | **TECH_PASS** | §4 |
| "Omuzlar düşük": kök neden retarget (köprücük her hızda ~4,3° aşağı); retarget pozunda düzeltildi, görünür = sürücü ±1,4° | **TECH_PASS**; görünüm VISUAL_REVIEW_REQUIRED | §5 |
| SHME beden katmanı: fren sonrası sönümlü yerleşme, dönüşte göğüs ön hazırlığı, efor duruşu | **PARTIAL** (çalışıyor, genlik küçük ve görsel kabul bekliyor) | §6 |
| Efor açık/kapalı (aynı girdi) | **TECH_PASS** (hız/fren/toparlanma farkı); görünür beden farkı küçük → VISUAL_REVIEW_REQUIRED | §7 |
| Klavye 45/90/135/180 | **TECH_PASS** yürüme 45/135, sprint 45/180; **PARTIAL** sprint 135 (1,5 s içinde 4–5 klip değişimi) | §8 |
| Fareyle hızlı dönüş: Relaxed tablosu yerdeyken zıplama klibi seçebiliyordu | Gerçek olay: yürürken küçük basamaktan 0,1 s düşüş → "boşluğa basma + hafif iniş" klibi (0,9 s); Normal set aynı yerde iniş seçmiyordu → VISUAL_REVIEW_REQUIRED. Yerdeyken zıplama-başlangıç veritabanları ayrıca filtrelendi (gerçek zıplama çalışıyor) | §8 |
| Core Motion (C) | Ölçüldü, **eklenmedi** (ayak kayması 5–20 kat) | §2.3 |
| Ev içi 150 cm/s, Shift koşmuyor | **TECH_PASS** | §9 |
| İş istasyonunda bekleme kırılması çıkmıyor | **TECH_PASS** (kilit mekanizması: hareket girdisi kilitliyken 32 s'de 0 kırılma; serbest beklemede 55 s'de 2). Gerçek istasyonun içinde: **NOT_TESTED** (bu protokolde E istasyonu açmadı, dün de açmamıştı) | §9 |
| Kayıt/yükleme | **TECH_PASS** (oyun içi `LoadGame(IgnorePlayerLocation=False)` konum/yön birebir, sonra yürüyüş 165); menü üzerinden: NOT_TESTED | §9 |
| 60 FPS | **TECH_PASS** (sabit 30 ve 60 kare/s adımda aynı klip dizisi ve duruş süreleri); gerçek kare süresi/GPU maliyeti ölçülmedi | §10 |
| Kök ofseti fareyle sert dönüşte 20–29 cm | **PARTIAL / açık** | §8 |
| Cook/paket, eğim/merdiven, kapıdan dışarı geçiş | **NOT_TESTED** | §11 |

## 1. Aktif zincir (canlı projeden doğrulandı)
- Pawn: `BP_HybridA_Player` → `/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter` (GASP CMC kopyası). Tek piyon; AAMS bağımlılığı yok.
- Sürücü: `ABP_Sph_GASP` (UEFN iskeleti). `SphRelaxed = true` (varsayılan) → `Choosers/CHT_Sph_PoseSearchDatabases_Relaxed`; `false` → `Choosers/CHT_Sph_PoseSearchDatabases_Dense` (GASP Normal). İkisi de satıcı tablolarının Sphirus kopyası, bağlamları `ABP_Sph_GASP_C` (InstancedStruct `import_text`). Satıcı varlıklarına dokunulmadı.
- Görünür beden: `ABP_Sph_Body_GASP` (retarget `Rig/RTG_Sph_UEFN_to_MH` → nefes katmanı → SHME omurga katmanı).
- Fizik/efor sahibi: `/Game/Sphirus/Player/Motion/AC_Sph_Motion` (`SphMotion`). Tek sahip: hız/ivme çarpanları, fren (`BrakeDecel` → GASP `CalculateBrakingDeceleration`), efor, beden sürücüleri, bekleme kırılmaları. GASP'ın CMC/Offset Root Bone/Foot Placement zinciri değişmedi; SHME aynı kemiğe yazan ikinci bir denetleyici kurmadı (omurga katmanı retarget'tan sonra, görünür bedende additive).
- Kamera: GraceRanger SpringArm + Cine zinciri değişmedi; GASP kameraları kapalı.

## 2. GASP Normal (A) / Relaxed (B) / Core Motion (C)
### 2.1 Relaxed kurulu sürümden doğrulanan kapsama (`data/rx_inventory.json`)
511 klip, 60+ veritabanı: yürüme/koşu/sprint döngüleri (F, B, LL, RL, LR, RR), F/B/LL/RL başlangıçları, 90/180 "reface" başlangıçları, duruşlar (F, B, LL, RL, 90/180 reface), 90/180 dönüşler (yürüme, koşu, sprint), pivot/box/spin aileleri, yerinde 45/90/135/180 dönüş, gait geçişleri (walk↔run↔sprint), iniş/zıplama, eğilme (Neutral eğilme klipleri), traversal çıkışları. Sprint yalnız ileri (geri/yan sprint yok). Bekleme döngüsü tek (`M_Relaxed_Stand_Idle_Loop`) + 8 idle break (veritabanında değil; `SphMotion` montaj olarak oynatıyor).
Chooser sütunları `MovementMode / Stance / MovementState / Gait`; dört özellik de `ABP_Sph_GASP`'ta var ve aynı enum'lar.

### 2.2 Klip kök hızları (`data/rx_speeds*.json`, kaynak klip ölçümü)
| | Normal | Relaxed |
|---|---|---|
| Yürüme döngüsü | 200 (yan 180, geri 150) | 165 (her yön) |
| Koşu döngüsü | 500 (yan 350, geri 300) | 375 (her yön) |
| Sprint döngüsü | 700 | 585 |
| Yürüme duruşu | 200→0 ≈0,25 s | 165→0 ≈0,45 s |
| Koşu duruşu | 500→0 ≈0,35 s | 375→0 ≈0,65 s |
| Sprint duruşu | 700→0 ≈0,45 s | 585→0 ≈0,80 s |
| Koşu 180 dönüş | 500→71→500 | 375→87→375 |

Brifin bandı (yürüme 165–190, jog 280–330, hızlı koşu 500–550) ile karşılaştırınca Relaxed çok daha yakın. Koşu 375 bandın üstünde; 330'a indirmek klibin adım uzunluğunu bozacağı (ayak kayması) için bilerek yapılmadı.

### 2.3 Core Motion (C) — ölçüldü, eklenmedi
Aynı MetaHuman, aynı ölçütler (dünkü Core Motion oyuncu kayıtları `A_loco_gaspA`, `TS_side_A_t2`):
| Ölçüt | Core Motion | GASP Normal | GASP Relaxed (üretim) |
|---|---|---|---|
| Basan ayak yatay kayması, yürüyüş (medyan) | 53–86 cm/s | 9 cm/s | 4,9 cm/s |
| El–uyluk yatay boşluğu, yürüyüş | 12 cm | 16 cm | 16 cm |
| Köprücük açısı görünür, yürüyüş | −6° | −7,6° | −1,9° (§5 sonrası) |
Core Motion kadın yürüyüşü yan görüntüde yumuşak, ama bu kurulumda ayak kayması ve seçim karmaşası (dün: saniyede 12–21 blend kimliği) belirgin. "Daha doğal" olduğu doğrulanamadı → aktif sete eklenmedi. Görsel karşılaştırma: `videos/TS_side_A_t2` (Core Motion) ↔ `videos/TS_side_pr1` (Relaxed üretim).

## 3. Hız–kadans sözleşmesi
Hızlar = klip kök hızları (her yön): yürüme 165, koşu 375, sprint 585 cm/s; ev içi `SphContextSpeedScale = 150/165`. Aynı klip hızlandırılmadı, play-rate oynanmadı. Yürüyüş başlangıç klibi (`Walk_Start_F`, 3,5 s) kendi içinde düz yürüyüşe dönüyor; MM ancak maliyet artınca döngü klibine geçiyor (30 s yürüyüş: 1 başlangıç klibi 3,2 s + 26,8 s tek `M_Relaxed_Walk_Loop_F`, başa dönme 0; basan ayak kayması medyan 6,5 / p75 16,8 cm/s (Normal: 9,1 / 55,5)).

## 4. Fren ve duruş (SHME fren planı, GASP'a uyarlanmış)
`SphMotion.PhysBrake`: tuş bırakıldığında son hıza göre sabit yavaşlama (165 cm/s → 380 cm/s², 585 cm/s → 780 cm/s²; efor ile en fazla %15 daha zayıf fren). GASP'ın kendi değeri 2000 cm/s² idi (her duruş ~0,1–0,4 s). Yeni değerler Relaxed duruş kliplerinin kendi süreleriyle eşleşiyor; MM duruş klibini tam boyunda oynayabiliyor (1–3 fren adımı).
| Duruş (aynı girdi) | GASP Normal, önce | Relaxed + fren, üretim |
|---|---|---|
| Sprintten bırak | 0,40 s / 156 cm | 0,83 s / 260 cm |
| Yürümeden bırak | 0,13 s / 20 cm | 0,47 s / 46 cm |
Kontrol gecikmesi yok: bırakınca fren hemen başlar; yeni girdi freni anında keser (CMC giriş yönünde ivmelenir).

## 5. Omuz / köprücük / omurga (kaynak → sürücü → görünür)
`an_shoulder.py`: köprücük açısı = köprücük kökü → üst kol ekleminin yataya göre yükselişi; aynı karelerde GASP sürücüsü (UEFN) ve görünür MetaHuman.
| Hız bandı | Sürücü | Görünür, önce | Görünür, sonra |
|---|---|---|---|
| Bekleme | −8,7° | −12,6° (−4,3) | −8,2° (+0,5) |
| Yürüme | −2,3° | −6,3° (−4,0) | −1,9° (+0,4) |
| Koşu | −1,8° | −8,2° (−4,3) | −1,8° (0,0) |
| Sprint | +1,7° | −3,0° (−4,4) | +2,2° (+0,5) |
Kök neden animasyon değil retarget'tı: UEFN→MH retarget köprücüğü her hızda ~4,3° aşağı indiriyordu (eski Core Motion retarget'ında +1°). Köprücük zinciri `OneToOne` → hedef retarget pozundaki köprücük yönü doğrudan çıktıya geçiyor. Düzeltme: `RTG_Sph_UEFN_to_MH` hedef pozunda `clavicle_l/r` dönüş ofseti yerel Y −5° (`changes/r5_rtg_clav.py`; +5° önce ters yönde denendi, ölçümle geri alındı). Sürekli sinüs ya da kemik ofseti eklenmedi; omuz düşüklüğü/genişlik oranı beklemede 0,31 → 0,27.
Omurga: göğüs–pelvis karşı dönüşü (twist p95−p5) yürüyüşte 33°, sprintte 58–62° (kaynak klipte olduğu gibi korunuyor). Bu sayılar beden oranına bağlı göreli ölçümlerdir; "kilitli omurga" şikâyetini sayıyla geçersiz saymıyoruz → yan/3-4/ön videolarla VISUAL_REVIEW_REQUIRED.

## 6. SHME beden katmanı (görünür bedende, retarget sonrası)
- Fren sonrası yerleşme (V2.53 karşılığı): `SetX` sönümlü yay (ω 9, ζ 0,45), giriş = boyuna yavaşlama; göğüs frenin sonunda öne taşınıp küçük aşımla yerleşiyor (spine_03 %40, spine_05 %60). Eksen PIE'de ölçülerek çevrildi (ilk denemede göğüs geriye gidiyordu: −1,5°).
- Dönüşte göğüs ön hazırlığı: giriş–hız açısının %12'si, ±9° ile sınırlı, hız > 80 cm/s.
- Efor duruşu: 250 cm/s üstünde EUse × 2° öne eğilme; nefes katmanı (önceki tur) korunuyor.
Genlikler bilerek küçük (aşırı sallanma/kamera sarsıntısı yok). Ölçülen gövde eğimi farkı frende +1,1–1,3°. **PARTIAL**: mekanik çalışıyor; bunun gözle okunup okunmadığı kullanıcı kararı.
Destek ayağı / ağırlık aktarımı: Relaxed başlangıç, duruş, 90/180 dönüş ve pivot klipleri sol/sağ ayak varyantlı; MM basan ayağa göre seçiyor (ör. `Walk_Turn_180_R_Lfoot`). Önceki SHME'deki proje-sahipli fren/itiş klip üretimi bu turda yeniden kurulmadı; Relaxed set bu açıları kendi klipleriyle kapsıyor.

## 7. Efor açık/kapalı (gerçek oyuncu, düz sahne, aynı girdi; `TE_on_pr1` / `TE_off_pr1`)
Plan: rested sprint → 3 ardışık sert tersleme → 2 s dur → tersleme → 5 s dinlen → sprint/tersleme. Tam tablo `data/effort_ab_pr1.md`; videolar `videos/B_final_effort_on.mp4`, `B_final_effort_off.mp4`.

| Ölçüt | Efor kapalı | Efor açık |
|---|---|---|
| 1. sert terslemeden sonra ulaşılan hız | 571 | 570 (ilk manevra kendini yavaşlatmıyor) |
| 3. ardışık terslemeden sonra ulaşılan hız | 528 | 500 |
| Bu noktada bırakma anındaki hız | 505 | 395 |
| Yorgunken sprint duruşu | 0,80 s / 248 cm | 0,90 s / 277 cm (fren gücü eforla −%15) |
| En düşük ivme çarpanı (AccScale) | 1,00 | 0,78 |
| 5 s dinlenmeden sonraki sprint | 585 | 578 (E 0,96 → 0,39) |
| Pelvis düşüşü / omuz sallanması (görünür) | 12–26 cm / 5–16 cm | benzer (fark < %10) |

Okuma: efor hız, ivme, fren süresi ve toparlanmada ölçülüyor; komut gecikmesi yok. Görünür bedende fark küçük (nefes + 2° efor eğimi): **görsel tarafı PARTIAL / VISUAL_REVIEW_REQUIRED**.

## 8. Dönüşler
**Klavye (kamera sabit, düz sahne, `KT_turnsT_pr2`, `KT_turnsS_pr2` yan):**
| Dönüş | Giriş → en düşük → çıkış (cm/s) | Yeni yöne ulaşma | Seçilen klipler |
|---|---|---|---|
| Yürüme 45° | 165 → 165 → 165 | 0,13 s | döngü devam (MM yön) |
| Yürüme 135° | 165 → 81 → 165 | 0,23 s | `Walk_Turn_180_R_Lfoot` |
| Sprint 45° | 585 → 576 → 585 | 0,27 s | `Transition_Run_to_Sprint` → `Sprint_Loop_F` |
| Sprint 135° | 585 → 169 → 571 | 0,67 s | `Sprint_Turn_180` → `Run_Turn_180` → `Transition_Walk_to_Sprint` → `Sprint_Reface_090` (**PARTIAL**: değişim fazla) |
| Sprint 180° | 573 → 3 → 550 | 0,53 s | `Sprint_Turn_180_R_Rfoot` → `Run_Turn_L_180` → `Transition_Walk_to_Sprint` |
180°'de eski yön enerjisi söndürülüp (573 → 3) yeni yöne itiş geliyor; basan ayağa göre sol/sağ varyant seçiliyor. Bahçe rotasındaki ilk klavye kaydında sprint 90°'de hız 0,1 s'de 575 → 28'e düştü: bu bir engele çarpmaydı (yön tersine sekti), düz sahnede tekrarında yok.

**Fare (yürürken 360°/s ve 150° süpürme, sprintte 360°/s; `videos/B_final_mouseturns.mp4`):** yürürken Relaxed "spin" klipleri (gövde dönerken adım akışı), dururken yerinde 90/135 dönüş, sprintte `Sprint_Turn_090`. Kamera yaw'ı tek başına fren üretmiyor (efor/fren girdi–hız açısına bakıyor). Görünür pelvis–kapsül ofseti p95 23,7 / en çok 29,4 cm (GASP Offset Root Bone sınırı 30); hızlı fare dönüşünde basan ayak kayması medyan 22 cm/s (düz yürüyüşte 5–7) → **PARTIAL / açık** (ayak kilidi çıkış yolu bu turda düzeltilmedi).

## 9. Oyun regresyonu
| Test (gerçek oyuncu) | Sonuç | Kanıt |
|---|---|---|
| Ev içi koridor, Shift | En fazla 150 cm/s, koşu yok → TECH_PASS | `B_final_hall150` |
| Evden dışarı geçiş | NOT_TESTED (test rotası 5,6 s'de duvara çarptı; kapı rotası bulunamadı) | `data/HO_out_pr1.json` |
| Hareket kilitliyken bekleme kırılması | 32 s'de 0 → TECH_PASS | `data/IG_gate_pr2.json` |
| 55 s bekleme | 2 Relaxed kırılma (11,3 s ve 39,3 s), kapsül kayması 0 → TECH_PASS, görünüm VISUAL_REVIEW_REQUIRED | `B_final_idle55` |
| Gerçek zıplama (yürürken, sprintte) | Zıplama montajı + Relaxed havada/iniş klipleri → TECH_PASS | `B_final_jump` |
| Kayıt / yükleme (oyun içi) | Konum ve yön birebir; yükleme sonrası yürüyüş 165 → TECH_PASS | `data/reg_save_pos_pr2.txt` |
| Sola/sağa yürüme kadrajı | Görünür pelvis–kapsül p95 8,2 cm; kamera zinciri değişmedi | `B_final_strafe` |
| Kıyafet / yüz / saç | Değişmedi (aynı MetaHuman) | tüm videolar |
| Derleme | Oyuncu + 9 başvuran BP + iki AnimBP + bileşen: hatasız | `q_compile` |
| Kullanıcı kaydı | SHA1 `8622025b…` korundu (bkz. §13) | — |
| 18 iş montajı (yatak, dolap, maske, kesme, şömine, çay) gerçek girdiyle | NOT_TESTED bu turda (montaj katmanına dokunulmadı; dünkü teknik test geçerli) | — |

## 10. FPS / performans
Sabit adımlı kayıtlar: 30 kare/s (adım ort. 0,0345 s) ve 60 kare/s (0,0167 s) aynı girdiyle aynı klip dizisi; duruş süreleri 0,47/0,43 s (yürüme), 0,83/0,83 s (sprint). Değişen tek şey bazı geçişlerde sol/sağ ayak varyantı (faza bağlı). Gerçek zamanlı kare süresi, GPU/CPU maliyeti ve düzensiz kare (20/120) testleri yapılmadı → **NOT_TESTED**. Editör bellek kullanımı 17–22 GB (değişmedi).

## 11. Açık kalanlar
1. Kullanıcı oynayarak kabul etmedi: Relaxed duruşu, omuz/kol görünümü, frenin ağırlığı ve sprint duruşundaki öne katlanma görsel karar bekliyor.
2. Sprint 135° dönüşlerinde klip değişimi fazla (PARTIAL).
3. Fareyle sert dönüşte kök ofseti 20–29 cm ve basan ayak kayması (PARTIAL).
4. Küçük basamaktan inişte 0,9 s'lik iniş klibi (ağır görünebilir).
5. SHME beden katmanının genliği küçük; görünür efor farkı sınırlı.
6. Önceki SHME'nin proje-sahipli fren/itiş klip üretimi ve ilk adım öncesi ağırlık aktarımı (V2.52) bu GASP mimarisinde yeniden kurulmadı; Relaxed klipleri bu rolü üstleniyor.
7. Cook/paket, gerçek FPS/performans, eğim/merdiven, kapıdan dışarı geçiş, gerçek istasyon akışı, menüden kayıt/yükleme, 18 iş montajının gerçek girdiyle testi: NOT_TESTED.
8. GASP traversal / çarpışma kanalları: dokunulmadı.
9. Koşu hızı 375 cm/s, brif bandının (280–330) üstünde (klip adım uzunluğu korunmak için).

## 12. Videolar (gerçek zaman, düzeltilmiş kırpma)
Hepsi PIE, sabit oyun adımı, gerçek hızda kodlandı, oyun görüş alanı kırpması düzeltilmiş kodlayıcıyla (kare 5,168 → 1515,1090; sol 200 px hatası yok — `frames/` örnekleriyle aynı kadraj).
| Video | İçerik |
|---|---|
| `A_normal_*` (loco, phys, mouseturns, side, q34) | GASP Normal (bu turdan önceki üretim) |
| `C_coremotion_side`, `C_coremotion_loco` | Core Motion oyuncusu (karşılaştırma) |
| `B0_relaxed_before_clavfix_loco` | Relaxed, köprücük düzeltmesinden önce |
| `B_final_loco`, `B_final_phys` | yürüme→koşu→sprint→duruş; sprint-bırak-S-W-S (fren/tersleme) |
| `B_final_keyturns_flat`, `B_final_keyturns_side` | klavye 45/135/180, yürüme ve sprint (arka / yan kamera) |
| `B_final_mouseturns`, `B_final_strafe` | fare dönüşleri; kamera sabit A/D/W+A/W+D |
| `B_final_side`, `B_final_q34`, `B_final_front` | yakın yan / 3-4 arka / 3-4 ön beden görünümü |
| `B_final_walk30`, `B_final_sprint18`, `B_final_idle55` | uzun yürüyüş, uzun sprint, bekleme |
| `B_final_effort_on`, `B_final_effort_off` | efor A/B, aynı girdi |
| `B_final_hall150`, `B_final_jump`, `B_final_fps60` | ev içi kural, zıplama, 60 kare/s |

## 13. Geri alma ve değişen varlıklar
- Checkpoint (SHA1 listeli): `C:\Users\berat\SphirusCheckpoints\GASP_Relaxed_Pre_20261110_1504` (Player klasörü, oyuncu BP, Config, kayıtlar). Her yazma işinin manifest yedeği: `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/day_*`.
- Değişen: `ABP_Sph_GASP` (Relaxed yolu + zıplama filtresi), `ABP_Sph_Body_GASP` (omurga katmanı), `AC_Sph_Motion` (fren, beden sürücüleri, idle kilidi), `BP_Sph_GASPCharacter` (fren bağlantısı, hızlar), `BP_HybridA_Player` (hızlar, ev içi oran), `RTG_Sph_UEFN_to_MH` (köprücük ofseti). Yeni: `Choosers/CHT_Sph_PoseSearchDatabases_Relaxed`.
- Normal'e dönüş tek anahtar: `ABP_Sph_GASP.SphRelaxed=false` + hızlar 200/500/700 + `PhysBrake=false` (ya da checkpoint).
- Geri alınan denemeler: köprücük +5° (yanlış yön), omurga ekseni −Z (yanlış yön), `1−k·EUse` ve `2·ζ` düğümlerinde silinen sabitler (fren hiç çalışmıyordu; düzeltildi), aday ön ayar dizisinin yarıda kesilmesi (geçersiz kayıtlar rapordan çıkarıldı).
- Kullanıcı kaydı: test sırasında bir kayıt dosyası test yazımıyla yer değiştirdi; testin kenara aldığı kopyadan geri yazıldı (SHA1 `8622025b…`, 5566 B, 8 Kasım 20:03 — checkpoint ile aynı). Test dosyası silinmedi (`Saved/Codex/Day_20261107/slot_test_artifact_20261110/`). Kaydedicilere iki koruma eklendi (test yazdığı kaydı kenara taşır; dizi her testten sonra SHA kontrol eder).
