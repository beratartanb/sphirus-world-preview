# TABLES V2.47 (2026-11-02)

## 1. Dense DB yeniden kayıt doğrulaması
| | yedek (`v246_ddb`) | şimdi |
|---|---|---|
| .uasset boyutu | 13 341 B | 13 341 B |
| giriş adları (15) | af_Loco_Walk_Bwd{Left,Right,}_AAMS, M_Neutral_Walk_Loop_{F_L_20_Phase27Support, F_R_20_Phase275Support, BL, BR, FL, FR, LL, RL, F_R_20}, M_Ranger_Walk_Loop_F_PureForward_CWF, af_Loco_Walk_Fwd_NoRM, M_Neutral_Walk_Shuffle_LR_to_LL_Lfoot | aynı |
"18" V2.44 sondasının aynı adlı SATICI DB'yi (AAMS) saymasıydı; proje DB'si değişmedi.

## 2. Arama rotası kancası v1 (`SHM247_WalkOn`; Dense ileri döngü seçilince bir sonraki arama yalnız `PSD_LB_WalkLoops`)
| Senaryo (30 FPS) | üretim | wr |
|---|---|---|
| w42 klip sırası | kalkış → Ranger 1,45 s → SHM245 | kalkış → Ranger **1 kare** → SHM245 |
| w42 kayma / pop / karşı dönüş | 10,2 / 0 / 19,6 | 10,2 / 0 / 19,6 (2 koşu aynı) |
| taps | 17,3 / 0 | **16,7** / 0 (dokunuş kalkışları SHM245'e) |
| gait / wdiag / wstart / w43 | 6,8/0 · 18,1/0 · 21,0/0 · 6,3/0 | 6,8/0 · 18,1/0 · 21,0/0 · **5,6**/0 |
| devir penceresi 2,2–3,5 s: kalça / klavikula / karşı dönüş / pelvis z | 14,9 / 11,1 / 17,2 / 5,5 | 14,7 / 11,1 / 17,2 / 5,4 (metrikler aynı; fark klip ailesi) |
| **gerçek zaman** w42 r1 / r2 | 8,6–9,7 / 0 | **24,7** (30° kalkışında F_R_20@2.73 girişine tekme) / **28,3** (devirde SHM245@0.04'e tekme), pop 0/1 |
| gerçek zaman taps / wdiag / gait | 15,4 / 12,1 / 8,4 (2 pop) | 14,3 (2 pop) / 11,8 / 10,1 (**6 pop**, 39) |
Okuma: v1 kancası faz gözetmeden tekme atıyor (InvalidateContinuingPose): sabit adımda devir anında (faz ~0) sorunsuz, gerçek zamanda orta-adımda girilen Dense döngüsüne tekme → faz uyumsuz LB karesi → 25–28 cm sürüklenme ve gait popları. v2: tekme yalnız GİRİŞ penceresinde (`Phase27_SelectedTime` < 0,12 s).

## 3. Kanca v2 (giriş penceresi 0,12 s), 30 FPS
| | w42 klip sırası | w42 / taps / gait / wdiag / w43 / wstart |
|---|---|---|
| wr (v2) | kalkış → Ranger 2,07–3,53 → SHM245 (= üretim; kanca ateşlenmedi) | 10,2/0 · 17,3/0 · 6,8/0 · 18,1/0 · 6,5/0 · 21,0/0 (= üretim) |

## 4. Üretim
Terfi yok; üretim = V2.45 (`verify241 ALL_OK true` kurulum sonrası; kanca kapalı).
