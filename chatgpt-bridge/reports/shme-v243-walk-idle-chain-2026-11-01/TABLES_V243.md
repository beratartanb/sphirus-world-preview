# TABLES V2.43 (2026-11-01)

## 1. Idle sahipliği deneyleri (w42_id, 30 FPS; idle penceresi 6,9–7,95 s = duruştan 1 s sonra)

| Aday | IdleHold | Görünen klip | pelvis p2p x/y/z (cm) | göğüs z | baş z | ayak kayması (bütün koşu) | kalkış pop >25 m/s² |
|---|---|---|---|---|---|---|---|
| o (üretim) | True | af_Stand_Idle (üst) + anlık görüntü (alt) | 0,09 / 0,03 / 0,06 | 0,23 | 0,21 | 10,4 (yürüyüş döngüsü) | 0 |
| idl (V2.42 MM kancası) | True | SHM242_Idle_Weighted (MM, görünmez) | 0,02 / 0,10 / 0,05 | 0,19 | 0,16 | — | 0 |
| idlh (+IdleStanceTolerance 30) | True | aynı | 0,02 / 0,10 / 0,05 | 0,19 | 0,16 | — | 0 |
| idp (sekans oynatıcı değişimi, nefes 0,5°) | True | — | 0,09 / 0,03 / 0,06 | 0,14 | 0,13 | — | 0 |
| idp (nefes 1,2°) | True | — | — | 0,10 | 0,09 | — | 0 |
| **idlg (kapı kapalı + MM idle)** | **False** | **SHM242_Idle_Weighted, zaman ilerliyor** | **0,79 / 0,88 / 0,33** | 0,36 | 0,36 | **0,0** | **0** |
| og (kapı kapalı, satıcı idle) | False | af_Stand_Idle (MM) | 4,93 / 1,18 / 0,10 | 0,11 | 0,12 | 7,7 (30° kalkış) | 0 |

## 2. Dönüş kuralı (latgl = yanal aile + yerleşme kapısı + bakış kuralı), 30 FPS

| Senaryo | o | latg (V2.42) | latgl |
|---|---|---|---|
| j41_rl_p04: en kötü kayma / montaj | 39,2 SLIP / hemen | 8,1 DRAG / +0,43 s | 8,1 DRAG / **montaj yok**, beden −80° (bakış −74°) |
| j41_rl_p10 | 38,3 / hemen | 32,5 (Bl_P21) / +0,6 s | 32,5 (Bl_P21 kapanış adımı: FootPlacement kilit → bırakma sıçraması, montaj yok) |
| j42_lr_p10 (sağ) | 12,5 (kalkış) | 0,0 | 14,6 (idle devralmada sol ayak, 13,1 s) / montaj yok |

## 3. Yürüyüş izolasyonu (w42_id, mv_walk_0_0)

| | o | oSCR | oPBI | oRAW |
|---|---|---|---|---|
| adım / kadans | 72,9 / 1,67–1,9 | aynı | aynı | 72,5 / 1,9 |
| pelvis yanal / dikey | 3,7 / 5,5 | 3,7 / 5,5 | 3,1 / 5,5 | 3,7 / 5,5 |
| karşı dönüş p2p | 23,0° | 23,0° | 23,1° | 23,0° |
| kol salınımı l/r | 28,7 / 34,6 | aynı | aynı | aynı |
| MM oynatma | 1,24 | 1,24 | 1,24 | 1,24 |

## 4. Uzun idle (w43_idle: yürü 3 s → 8 s bekle → yürü; 30 FPS; pencere = hız < 3 cm/s, 5,6–12,9 s)

| | o | idlg |
|---|---|---|
| IdleHold | True (duruştan sonra) | False |
| görünen klip | af_Stand_Idle (202 kare) | SHM242_Idle_Weighted (201 kare, zaman ilerliyor) |
| pelvis p2p x/y/z | 0,12 / 1,79 / 2,75 | 1,07 / 5,07 / 3,43 |
| pelvis ayaklar arası ekseni (sağa +) | −6,6 … −1,0 (duruş yerleşmesi) | −1,1 … **+4,8** (ağırlık sağ ayağa) |
| göğüs z / baş x,y,z p2p | 2,97 / 7,3 6,9 3,1 | 3,5 / 9,1 8,7 3,6 |
| ayak kayması (bütün koşu) | 6,5 (yürüyüş döngüsü) | **0,0** |
| pop > 25 m/s² | 0 | 0 |
| kalkış pelvis hız rampası (13,0 s) | 32→131 cm/s | 39→132 cm/s |

## 5. FPS matrisi

| FPS | j41_rl_p04 o | j41_rl_p04 latgl | w42_id idlg (idle 1. s) | w42_id o |
|---|---|---|---|---|
| 30 | 39,2 SLIP | 8,1 DRAG, montaj yok | hold False, pelvis p2p 0,8/0,9/0,3, slip 0,0, pop 0 | hold True, 0,09/0,03/0,06 |
| 60 | 59,5 SLIP | 9,0 DRAG | hold False, 0,76/0,90/0,28, klip oynuyor; pop 2 (33, yürüyüş döngüsünde; üretimle aynı) | hold True, 0,1/0,02/0,06; pop 2 (33) |
| gerçek zaman (32–34 Hz) | (V2.42: karşılaştırılamaz, TurnL045 kalkışı) | **0,0** (SKIM 1, OK 3; V2.42'nin 22,4 cm'i bu koşuda tekrarlanmadı — tek koşu, kapanış adımı yeniden yazımı sonrası), montaj yok; pop 3 (26, klip içi) | hold False, 0,79/0,83/0,32, klip oynuyor, pop 0 | — |

## 7. Regresyon (30 FPS): o vs `all` (= yanal aile + yerleşme kapısı + bakış kuralı + stance kapısı kapalı + ağırlıklı MM idle)

| Senaryo | o: en kötü kayma / pop>25 | all: en kötü kayma / pop>25 | Okuma |
|---|---|---|---|
| wdiag | 18,1 (idle devralma) / 1 | 8,7 / 0 | iyileşme |
| wstart | 21,0 (idle devralma) / 0 | 20,0 (yürüyüş döngüsü) / 0 | nötr |
| jstart | 57,4 (TurnL045 satıcı) / 4 | 59,6 / 6 | pop +2 — idle tarafı (ayrıştırılacak) |
| gait | 8,3 / 0 | 14,6 (A_LB_Walk_Fwd) / 4 (30) | **regresyon** |
| taps | 17,3 / 0 | 20,1 (SHM242_Idle_Weighted @1.07: tap sonrası ağırlık kayması başlamışken kalkış) / 3 (28) | **regresyon** |
| j38_c90r | 10,3 / 1 | 10,4 / 1 | aynı |
| j40_rlw | 11,2 / 3 | 21,3 (A_CP2_Jog_Fwd_Start @0.45: idle'dan yeniden kalkış) / 3 | kayma +10 |
| j41_rl_p04 | 39,2 | 8,1 / 1 | iyileşme |
| j42_lr_p10 | 12,5 (kalkış) | 12,5, devralma kayması yok / 0 | iyileşme (14,6 kapı açıkken) |
| w42_id | 10,4 / 0 | 0,0 / 0 | iyileşme |

Karar: `all` üretime ALINMADI. Kısa dokunuş/erken kalkışlarda ağırlık kayması başlamış pelvisten kalkış (0,8 s'de başlıyor) kayma/pop üretiyor → idle kayması 2,5 s'ye alındı (`SHM243_Idle_Weighted2`, `idlg2`); yanal parça (`latgl`) ve kapı-kapalı (`og`) ayrı ayrı regresyona alındı (bölüm 8).

## 8. Ayrıştırma (30 FPS; `all` regresyonunun hangi parçadan geldiği)

| Senaryo | o (üretim) | latgl (yanal aile + kapı + bakış kuralı) | og (yalnız stance kapısı kapalı) | Okuma |
|---|---|---|---|---|
| taps: en kötü kayma / pop | 17,3 (yürüyüş döngüsü) / 0 | 17,3 / 0 | 17,3 / 0 | ikisi de temiz → `all`'daki 20,1 / 3 pop **erken başlangıçlı idle klibinden** (0,8 s'de ağırlık kayması başlıyor, tap kalkışı bunun üstüne biniyor) |
| gait | 8,3 / 0 | 8,3 / 0 | 8,3 / 0 | temiz → `all`'daki 14,6 / 4 pop idle klibinden |
| j40_rlw | 11,2 **veya** 17,2 (r1/r3 11,2; r2 17,2) / 3 | 17,2 / 11,2 / 17,2 (r1/r3/r2) / 3 | 11,2 / 3 | 10,87 s'deki A_CP2_Jog_Fwd_Start→A_CT_Jog_Fwd geçişi üretimde de iki modlu (11,2 ↔ 17,2, bir kare uzun kayma) → **varyans**, regresyon değil; `all`'daki 21,3 (0,45 s'lik kalkış) idle klibinden |
| jstart | 4 pop (42) ×2 koşu | — | (bölüm 9) | idlg2 koşularında 6 pop (26, 32; 135° dönüşlü kalkışların ilk 0,2 s'si, omuz) |

**idlg2 geçersiz (hook adı tuzağı):** `PSD_SHM243_Idle` ile koşulan idlg2'de görünen klip 206 kare `af_Stand_Idle` idi (hold False, IdleOn 1). Neden: V2.42 kancası (`install242_idledb2.py`) override'ı yalnız seçili DB adı `'Stand_Idles'` **veya `'SHM242_Idle'`** içerirken sürdürür; `PSD_SHM243_Idle` adı ikisini de içermiyor → PostSelection yeni DB'yi yazar yazmaz koşul düşüyor, chooser'ın `PSD_Dense_Stand_Idles`'ı geri geliyor (her karede arama ping-pongu). Düzeltme: aynı klip (`SHM243_Idle_Weighted2`, 2,5 s geç başlangıç) `PSD_SHM242_IdleB` adıyla yeniden kuruldu, `PSD_SHM243_Idle` silindi (yedek: manifest `v243_idle2`), aday `idlg3` (bölüm 9).

## 9. idlg3 (geç başlangıçlı idle `SHM243_Idle_Weighted2` + `PSD_SHM242_IdleB`, stance kapısı kapalı), 30 FPS

| Senaryo | o (üretim) | idlg3 | Okuma |
|---|---|---|---|
| w43_idle (8 s bekleme) | hold True, af_Stand_Idle, pelvis ayaklar arası −6,6…−1,0, kayma 6,5 (yürüyüş döngüsü), pop 0 | hold False, **SHM243_Idle_Weighted2 206/206 kare**, pelvis ekseni −4,3…**+4,8**, göğüs z 4,6, **kayma 0,0, pop 0** | bekleme PASS (idlg ile aynı) |
| w42_id | 10,4 (yürüyüş döngüsü) / 0 | 10,4 / 0; idle 38 kare görünür, hold False | PASS |
| taps | 17,3 (8. dokunuş kalkışı, yürüyüş döngüsü) / 0 | **22,7** (8. dokunuş kalkışı; idle klibine 11,0 s'de girilmiş = ağırlık tek ayakta) / 2 (25, 26; bırakma duruşları) | **FAIL** (kalkış kayması +5, kalkış popu) |
| gait | 8,3 / 0 | 14,6 (A_LB_Walk_Fwd) / 4 (26–30, 7,4–8,2 s jog→sprint itişi) | dolaylı: idle'dan farklı fazla kalkış → jog→sprint itişinde `SHM217_J2S_Lfoot_b` (o: `_Rfoot_a`) seçiliyor; pop itiş klibi içeriği |
| j40_rlw | 11,2/17,2 (varyans) / 3 | **21,3** (A_CP2_Jog_Fwd_Start@0.45, idle'dan jog kalkışı) / 3 | **FAIL** (kalkış kayması +4…+10) |
| jstart | 4 pop (42) | 6 pop (42; +26 @17,17 s mv_jog_135, +32 @20,20 s mv_jog_−135, omuz, kalkışın ilk 0,2 s'si) | +2 pop **kapı-kapalıdan** (og da 6): satıcı 135° dönüşlü kalkış MM idle duruşundan karışıyor |

**Mekanizma (LTP):** MM idle klibine herhangi bir zamandan giriyor (taps 8,2 s: @11,03; w42_id: @10,53; klip sonu 12,9 s = ağırlık tek ayakta). Kalkış (`CP_StartOwned` True, `A_SHM222_WalkStart` / `A_CP2_Jog_Fwd_Start`) bu kaymış pelvisten karışıyor → kalkış ayağı +4…+10 cm kayıyor. Bekleme boyunca kayma 0 — sorun **giriş fazı**, bekleme değil. (Kalkış sırasında LTP'nin MM alanları — DB/klip/zaman — donuk görünür: CP evaluator sahipken MM aranmıyor; bu "kanca takıldı" değil.)

**Karar:** idle zinciri (kapı kapalı + ağırlıklı idle) **üretime ALINMADI** — bekleme PASS, ama kullanıcının "yeniden kalkışta ayak kayması/pop olmasın" şartını kısa dokunuş ve idle'dan jog kalkışında bozuyor. Sonraki adım: klip girişini nötr ağırlığa bağlamak (giriş DB'si = ilk 2,5 s'lik nötr duruş, ağırlık kayması ancak IdleWait sonrasında devam DB'siyle) veya kalkış kliplerinin pelvis girişini idle pelvisine yeniden hedeflemek; ayrıca 135° dönüşlü kalkışların MM idle duruşuyla uyumu.

## 6. Yeniden yazılmış kapanış adımı (close_apex 8), 30 FPS latgl
j41_rl_p10 11,5 DRAG (Br_P23 fren ayağı iniş kayması), j41_rl_p04 8,1 DRAG, j42_lr_p10 14,6 (idle devralma, dyaw 51°, kapı AÇIK aday) — `all` adayında regresyonla tekrar.

## 10. Üretim (terfi SONRASI, kaydedilmiş varsayılanlar, bayraksız `o`), editör yeniden başlatıldıktan sonra

Terfi editör içinde yapıldı (`PROMOTE243` ok, `verify241 ALL_OK true`), ama aynı editördeki ilk 30 FPS `o` partisi hâlâ satıcı `A_LS_Jog_Left_Stop` + montaj popu (39,2 / 36,6 / 33,9) gösterdi: oyun sınıfları çocuk BP'ler (`ABP_GR_MotionMatching`, `BP_PBI_Player`) ve bellekteki CDO'ları eski değeri koruyor. Yeniden başlatma sonrası sonda (`PROBE243`): taban ve çocuk ABP `SHM242_DB_LatStop = PSD_SHM242_LatStop`, taban ve çocuk pawn `GR242_TurnSettleGate`/`GR243_TurnNeedsLook` true, idle kapalı, DA `StanceIdleGateEnabled` true. Aşağıdaki sayılar yeniden başlatma sonrası.

| Senaryo | V2.42 üretim (terfi öncesi) | V2.43 üretim 30 FPS | 60 FPS | gerçek zaman (33–37 Hz) |
|---|---|---|---|---|
| j41_rl_p04 (sol strafe duruşu) | 39,2 SLIP A_LS stop + **90° montaj** (pop 69) | **8,1 DRAG** `SHM242_LatStop_L_Br_P23`, montaj yok, pop 1 (28, klip içi, öncekiyle aynı) | **7,6** `Br_P23` (V2.42: 59,5 A_LS + montaj); 7,95 s'deki 34/39 cm 90° jog kesme episodu eski üretimde de birebir var | **11,9 / 9,2** (iki koşu; en kötü episod jog-sol döngüsü, duruş değil), montaj yok |
| j41_rl_p10 | 36,6 A_LS stop + montaj (pop 65) | **32,5** `SHM242_LatStop_L_Bl_P21`@0.36 (sol fren ayağı 86° dönerek 0,63 s kayıyor; beden yaw'ı sabit −167°), montaj yok, pop 2 (28) — t2 adayı Br_P23 ile 11,5 vermişti → üretimde 3 koşuda da 32,5 / Bl_P21 (kararlı); t2'nin Br_P23 seçimi üretimde tekrarlanmadı | — | — |
| j42_lr_p10 (sağ ayna) | 33,9 A_LS_Jog_Right_Stop + montaj (pop 59) | **14,6** idle devralmasında (af_Stand_Idle, sol ayak 51° dönerek 1,6 s; beden yaw'ı sabit −6,8°), montaj yok, pop 0 (2 koşu aynı) | — | 17,5 (idle devralma), pop 4 (38) |
| taps / gait / w42_id / w43_idle | 17,3/0 · 8,3/0 · 10,3/0 · 6,5/0 | 17,3/0 · 8,3/0 · 10,3/0 · 6,5/0 (aynı) | taps 18,9 (StartTransfer, 60 FPS tabanı yok) · w42_id 12,5 (V2.42 60 FPS ile aynı) | w42_id 11,8 / 0 |
| jstart / wdiag / wstart / j40_rlw | 57,4/4 · 18,1/1 · 21,0/0 · 11,2–17,2/3 | 57,4/4 · 18,1/1 · 21,0/0 · 17,2/3 (aynı) | — | — |

Okuma: duruş sonrası 90° montaj üç senaryoda ve üç kare hızında yok; sol p04 duruşu 39→8 cm. Kalan: p10'da `Bl_P21` bininin fren ayağı (32,5 cm, ayak 86° dönüyor — kapanış adımı tepe yeniden yazımı bu bini değiştirmedi: sayı yeniden yazım öncesiyle aynı), sağ aynada idle devralmasında ayak yeniden yönelmesi (51°, 14,6 cm): yanal duruş bitiş ayak yönü ile `af_Stand_Idle` ayak yönü uyuşmuyor; MM duruştan sonra P19→P22→P07 binleri arasında dolaşıp idle'a geçiyor.
