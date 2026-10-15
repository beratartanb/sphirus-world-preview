# SHME V2.7 — Daha küçük başlangıç / duruş, uzun ve değişken yürüyüş döngüsü, duruşta çökme, hızlı dönüşte koşu animasyonunun korunması (2026-10-15)

**İstek:** yürüyüş başlangıcı ve bitişi hâlâ büyük ve doğal olmayan animasyonlar; yürüyüş animasyonu çok kısa ve tekrarlı; yürüme / koşu /
depar her durumda dururken karakter doğal durmuyor ve duruş pozuna geçerken bir tık aşağı iniyor; koşuda hızlı dönüşte hız düşüyor ve
animasyon tempoluya geçiyor — bunun yerine o anki hızla, hafif savrulma ile, o anki koşu şekline özel bir dönüş olmalı.
(Önceki talimat: gerekirse yeni animasyon üret.)

**Sonuç:**
- Teknik **PASS**: taze editörde diskten `verify_v27_final.py` **ALL_OK**, override'sız üretim duman koşusu adayla aynı, hata 0.
- His / görsel kabul **NOT_TESTED**: oyun testi senin, bkz. `USER_PLAYTEST_V27.md`.
- Duruştaki çökme: yürüyüşte iyi, tempolu / deparda **PARTIAL** (yarıdan fazlası kaldı, §6).

## 1. Nasıl ölçüldü
- **Ortam:** QA zemini, gerçek giriş yolu (IA_Look, gait tuşları), üretim bayrakları.
- **Final:** V2.6 üretim bayrakları ↔ V2.7 adayı, 23 senaryo × 2 tekrar, dönüşümlü (92 koşu, 2 bellek yeniden başlatması, çökme yok).
  - Klip değişiklikleri diskte olduğu için iki tarafta da var.
  - Klip etkisi, sabah alınan bake öncesi koşularla (`v27d_*`) karşılaştırıldı.
- **Yeni araçlar** (`Tools/SHME_V27_20261015/`):
  - `stopdip.py`: dururken pelvisin yürüyüş / koşu yüksekliğinin ne kadar altına indiği, en alt noktada diz bükümü, ayak açıklığı.
  - `startsize.py`: başlangıçta baş yana / öne kayması, gövde eğimi, pelvis inişi.
  - `turngait.py`: dönüşlerde hangi animasyon ailesinin oynadığı (depar / tempolu / yürüme veritabanı payı) ve en düşük hız.
  - `walkrep.py`: yürüyüşte döngüden döngüye eller / baş / omuz yatışı farkı, yani tekrarlılık.
- **Katman ayrıştırma:** FootPlacement, fren postürü, PBI, SHME gövde hedefleri tek tek kapatıldı. Duruştaki çökme ve büyük
  başlangıç **hiçbir katmandan değil, kliplerden** geliyor (her katman 1–2 cm'den az).

## 2. Kök nedenler
| Şikâyet | Kök neden |
|---|---|
| Yürüyüş başlangıcı büyük | CP başlangıç klipleri (`A_LS_M_Relaxed_Walk_Start_F_L/R`, "Relaxed" stil) yavaş ve geniş hareketler taşıyor. Klipte pelvis 8.5 cm iniyor, baş 10 cm yana / 20 cm öne gidiyor, gövde 20° öne eğiliyor. Oyunda hızlı yeniden kalkışta gövde +21°, baş +20 cm öne. Not: ilk kalkıştaki 9 cm yana kayma, rahat bekleme pozunun (ağırlık bir kalçada) ortaya gelmesi; bu doğal. |
| Yürüyüş bitişi büyük, duruşta aşağı inme | **Yürüme:** CP duruş klipleri (Relaxed / CT_Ref) adım başına 8–9 cm zıplıyor (bizim yürüyüş döngüsü 4.5 cm). Mesafe eşleşmesi duruşa tam son çift destek çukurunda giriyor: pelvis yürüme yüksekliğinin 3.6 cm altına iniyor, iki diz 45–50°. **Tempolu:** `SHM_A_CP2_Jog_Fwd_Stop` derin bir fren hamlesi; pelvis 12 cm iniyor, ön diz 90°. **Depar:** `SHM_A_RR_M_Relaxed_Run_Stop_F_L/R` 13 cm iniyor. Projedeki diğer tüm koşu duruşları da aynı (AAMS run stop 22 cm). |
| Yürüyüş kısa ve tekrarlı | Düz yürüyüşün tek klibi `A_LB_Walk_Fwd`: tek döngü, 1.37 s (2 adım), her döngü birebir aynı tekrarlanıyor. |
| Hızlı dönüşte animasyon tempoluya geçiyor | İki kapı vardı. (1) ABP `Update_MotionMatching`: depar veritabanı yalnız hız ≥ 380 cm/s **ve** yön ±65° iken veriliyor. Ayrıca tempolu yolu (daha önce test ediliyor) hız < 380 olan deparı da alıyor. V2.5 dönüş hız kaybı (deparda 290–360'a iniyor) ve dönüşteki gövde-hız açısı ikisini de bozuyordu. (2) Pawn `GetDesiredGait`: girdi kamera önünden 65–110° iken gait'i zorla Run yapıyor; deparda A/D ile kesmek tempoluya düşürüyordu. Önce: depar A/D testinde zamanın %49'u tempolu animasyon, gait %41 Run. |

## 3. Yapılanlar

### 3.1 Yeni / yeniden üretilmiş animasyonlar
Hepsi editör içi bake: kök hareketi korundu, ayaklar IK ile orijinal yerlerinde (basan ayak kayması 0, ayak hatası 0). Orijinaller
`checkpoint/clips_lb`, `walkloop`; ilk bake sürümü `v27_bake1`.

| Klipler | Ne yapıldı | Klipte sonuç |
|---|---|---|
| Rahat yürüme başlangıçları L/R (`v27_lowband_bake.py`) | Yavaş (0.4 s üstü) büyük sapmalar bastırıldı, adım ritmi korundu. Kapsam: pelvis yer değiştirmesi, pelvis + omurga + boyun + baş dönüşleri. Pelvisi yükseltmek için arka ayak gerektiğinde topunun üstünde yuvarlanıyor (topuk kalkıyor, top yerinde). | Pelvis inişi 8.5 → 4.4 cm, baş yana 10 → 5.5 cm, öne 20 → 11.5 cm, eğim 20 → 12° |
| 4 CP yürüme duruşu (Relaxed + CT_Ref, L/R) | Aynı bake + zıplama çukurlarının yükseltilmesi. | Baş yana 13 → 6 cm, öne 10.6 → 5 cm, gövde salınımı yarıya. Pelvis yükseltme bacak boyuyla sınırlı (~1.7 cm). |
| `SHM_A_CP2_Jog_Fwd_Stop` + 2 `SHM_A_RR_M_Relaxed_Run_Stop` | Aynı bake + erken parmak-kalkışı: gergin arka ayak, topuk kalkışı yetmezse yerden **dikey** biraz erken kalkıyor (kayma yok, gerçek koşucu frenindeki gibi). | Tempolu pelvis inişi 12.1 → 7.4 cm, depar 12.3 → 7.6 cm, depar baş yana 22 → 10 cm |
| `A_LB_Walk_Fwd` → **6.83 s uzun döngü** (`v27_walkvar_bake.py`) | 5 döngü. Bacak / ayak / kök birebir aynı (adım, hız, temas değişmedi). Üst gövdede tüm döngü boyunca periyodik (dikişsiz) doğal değişkenlik: gövde / boyun sallanması ~1°, kol salınım genliği adımdan adıma ±%18, kollarda küçük farklar, iki yavaş baş bakışı (+6° / −4°). PoseSearchBranchIn 0..uzunluk yeniden yazıldı (döngüsel kalıyor; audit ok). | Tekrar periyodu 1.37 → 6.83 s |

Veritabanları yeniden anahtarlandı: `PSD_CP2_JogStop`, `PSD_RR_Stop` (V27L2), `PSD_LB_WalkLoops` (V27W2).

### 3.2 Dönüş mantığı (`install_v27_turn.py`)
| Konu | Değişiklik | Üretim |
|---|---|---|
| Depar veritabanı kapısı | ABP literal'leri değişken oldu: `SHM_SprintDBMinSpeed` (380), `SHM_SprintDBDirMin/Max` (±65). Tempolu yolunun deparı kapma eşiği de aynı değişkene bağlandı. | 230 cm/s, ±110° |
| Yana depar kuralı | Pawn `GetDesiredGait` 65–110° → Run kuralı profil alanı oldu: `SprintSideRunDot` (0.4226 = eski). | −0.36 (kural kapalı) |
| Hızla dönüş, hafif savrulma | GR `TurnSpeedLoss` 0.6 → 0.35, `TurnSpeedLossMin` 0.5 → 0.7. Dönüşte hız daha çok korunuyor, gövde yolu ~15° önden götürüyor (momentum). Deparın kendi viraj klipleri (`A_SHM_Sprint_Curve_*`) seçilmeye devam ediyor. | — |

## 4. Final sonuçlar (tam tablo `FINAL_SUMMARY_V27.md`)

### Dönüşte depar animasyonu payı (depar veritabanı)
| Test | Önce | Sonra |
|---|---|---|
| A/D kesme | %45 | %91 |
| Fare dönüşü | %90 | %99 |
| Hızlı fare flick | %70 | %91 |

- A/D'de gait %59 → %100 Sprint.
- Kalan tempolu anlar yalnız 180°'lik flick'te, hız ~70 cm/s'ye düştüğünde (neredeyse durma; doğru).
- 90° depar kesmede en düşük hız 202 → ~310 cm/s.
- Dönüş zamanı / yolu: cut 90 %0.80 → 0.88 s, en küçük yarıçap ~1.0–1.15 m (bisiklet yayı geri gelmedi).

### Pop (>25 m/s²)
- Toplam 63 → 57.
- Hızlı depar flick'i 16 → 5.5 / koşu (en kötü 202 → 98).

### Yürüyüş başlangıcı (oyunda, hızlı yeniden kalkış)
- Gövde eğimi tepe **20.9° → 10.5°**.
- Baş öne **20 → 14 cm**.
- Başlangıç süresi aynı.

### Duruşta aşağı inme (pelvis yürüme / koşu yüksekliğinin altına)
| Gait | Önce | Sonra |
|---|---|---|
| Yürüme | 3.6 cm | **2.9 cm** |
| Tempolu | 12.2 cm | **9.2 cm** |
| Depar | 12.9 cm | **9.7 cm** |

- Baş inişi: yürüme 8.6 → 7.7, tempolu 14.8 → 12.3, depar 19.3 → 15.0 cm.
- Duruş mesafesi / süresi değişmedi.

### Yürüyüş tekrarlılığı
- Döngü 1.37 → 6.83 s.
- Döngüden döngüye ellerde fark 1.0 → 2.0 cm, omuz yatışında +%40–70 (eskiden aynı döngü birebir tekrarlıyordu).

### Diğer
- **Kayma:** p90 yürüyüş senaryolarında 2.5–3.7 cm (önceki sürümle aynı aralık), basan ayak bake'lerde 0.
- **Hata / seçim:** hata 0, index skip 0, P2 duruş seçimi 14/18 (aynı), BranchIn audit: 130 döngü tam kapsama.

## 5. Üretim değerleri ve geri alma
| Nerede | Alan | V2.7 | Geri almak için |
|---|---|---|---|
| `DA_GR_LocomotionBehavior` | TurnSpeedLoss / TurnSpeedLossMin | 0.35 / 0.7 | 0.6 / 0.5 |
|  | SprintSideRunDot | −0.36 | 0.4226 |
| `ABP_GR_MotionMatchingBase` CDO | SHM_SprintDBMinSpeed / DirMin / DirMax | 230 / −110 / 110 | 380 / −65 / 65 |
| Klipler + veritabanları | başlangıç / duruş bake'leri, uzun yürüyüş döngüsü | — | `Saved/Codex/SHME_V27_20261015/checkpoint/clips_lb` ve `walkloop` (editör kapalıyken geri kopyala) |
| Blueprint kurulumu öncesi | ABP / pawn / profil | — | `checkpoint/assets` |

V2.6 değerleri (kamera, lens, rahat yürüyüş, gait mantığı) aynen duruyor.

## 6. Açık kalanlar
1. **Tempolu / depar duruşunda hâlâ ~9 cm iniş.** Mevcut tüm koşu duruş klipleri derin fren hamlesi içeriyor. Bake, bacak boyu ve
   erken parmak kalkışıyla yapılabilecek en fazlasını aldı (−%25..30). Tam çözüm için son fren adımının **daha kısa** olduğu yeni bir
   koşu duruşu gerekiyor (ayak basma yerlerinin değişmesi). Bu bir sonraki adım olarak önerilir.
2. **Yürüyüş duruşu kalan 2.9 cm.** Son adımın uzunluğu yüzünden; aynı sınır.
3. **Görsel kabul yok.** Yürüyüş değişkenliğinin (baş bakışları, kol salınımı) fark edilir ama abartısız olup olmadığı oyunda
   görülmeli; fazla / az ise genlikler `v27_walkvar_bake.py` ile değiştirilir.
4. **Yana depar.** A/D ile artık yana depar atılabiliyor (gövde koşu yönüne dönüyor). Bu tasarım değişikliği; istenmezse
   `SprintSideRunDot` 0.4226.

## 7. Dosyalar
- **Ölçüm:** `FINAL_SUMMARY_V27.md`, `Reports/`, `ab_*.log`, `smoke_*.log`, `verify_final.out`, `promote.out`.
- **Araçlar** (`Tools/SHME_V27_20261015/`):
  - Koşu: `v27_ab.sh`, `v27_run.sh`, `v27_summary.py`
  - Ölçüm: `stopdip.py`, `startsize.py`, `turngait.py`, `walkrep.py`
  - Bake ve kurulum: `v27_lowband_bake.py`, `v27_walkvar_bake.py`, `install_v27_turn.py`
  - Terfi / doğrulama: `promote_v27.py`, `verify_v27_final.py`
