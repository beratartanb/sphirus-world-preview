# TABLES V2.46 (2026-11-01)

## 1. Yürüyüş kalkışından sonra klip sırası (V2.45 üretimi, w42_id)
| aralık | klip | DB | okuma |
|---|---|---|---|
| 0,07–2,07 | af_Stand_Idle (CP kalkış sahip) | Stand_Idles | kalkış |
| 2,07–3,53 | **M_Ranger_Walk_Loop_F_PureForward_CWF** | Dense_Stand_Walk_Loops | 206 cm/s döngü 0,64× |
| 3,53–5,67 | SHM245_Walk_Fwd | LB_WalkLoops | aday döngü |
| 5,67–6,80 | SHM_M_Neutral_Walk_Stop_F_Lfoot | Dense_Stand_Walk_Stops | duruş |
| 8,07–9,53 / 9,53–11,67 | Ranger / SHM245 (ikinci kalkış aynı sıra) | | |
| 14,10–14,73 / 14,73– | StartTransfer_FR → SHM245 (30° kalkış) | | |

## 2. Ranger ileri döngüsüne ModifyCost (aynı oturum / yeniden başlatma)
| durum | kalkış sonrası ilk 1,45 s | w42 karşı dönüş / kayma / pop | taps | not |
|---|---|---|---|---|
| V2.45 üretimi | M_Ranger_Walk_Loop_F_PureForward | 19,6 / 10,2 / 0 | 17,3 / 0 | |
| PureForward +2, aynı oturum | **M_Neutral_Walk_Loop_F_R_20 / F_L_20** (kardeş) | 19,6 / 10,2 / 0 | **23,1** (tap-2 kalkışı F_L_20 → StartTransfer_B) | karışım yer değiştirdi |
| + Dense ileri aile +6, aynı oturum | F_R_20 (hâlâ) | 19,6 / 10,2 / 0 | 23,1 | maliyet yetersiz/etkisiz |
| yeniden başlatma (DB yeniden kayıtlı) | **PureForward geri** | 19,6 / 10,2 / 0 | 17,3 / 0 (son temiz koşu §5) | maliyetler DDC indeksinde yok |

## 3. CP kalkış devri (BlendListByBool_3) — geçiş tipi üretimde zaten Inertialization (PRE 'before' = INERTIALIZATION)
| | idl4 (canlı idle) | inrt (canlı idle + PRE) | inrto (yalnız PRE) | üretim |
|---|---|---|---|---|
| taps | 19,0 / 2 (26) | 19,0 / 2 | 17,3 / 0 | 17,3 / 0 |
| jstart | 60,2 / 6 | 60,2 / 6 | 57,4 / 4 | 57,4 / 4 |
| j40_rlw | 21,3 / 3 | 21,3 / 3 | — | 17,2 / 3 |
| w43_idle | 6,4 / 0 | 6,4 / 0 | — | 6,3 / 0 |

## 4. Bakışa göre yanal kalkış rotası (`SHM246_LookRoute`, j45_sl)
| koşu | beden / bakış | kalkış | episod |
|---|---|---|---|
| 30 FPS lr = o | 0 / 61 | A_LS_Jog_Left_Start | 10,2 (kesme), kalkış temiz |
| gerçek zaman lr r1/r2/r3 | 0 / 35, 42, 42 | **af_Loco_Jog_Bwd_Start** ×3 | 24+41, 22+36, 26+36 |
| gerçek zaman o r1 | 0 / 57 | A_LS_Jog_Left_Start | 5,1 + 13,2 |
| gerçek zaman o r2 | 0 / 10 | SHM233_StandBack2_Jog_Bwd → af_Loco_Jog_Bwd_Start | 22+55 |
Okuma: ABP'deki `PreviousDesiredControllerYaw` kontrol yaw'ı değil (aday bakış-göreli yönü yanlış hesaplayıp LS rotasını düşürdü); üretimdeki geriye kalkış standback rotasından da geliyor. Aday kapalı.

## 5. Üretim (temiz oturum, yeniden başlatma sonrası, `verify241 ALL_OK true`, dirty paket yok) V2.45 → V2.46
| Senaryo | V2.45 | V2.46 (30 FPS) | V2.46 gerçek zaman |
|---|---|---|---|
| w42_id karşı dönüş / kayma / pop | 19,6 / 10,2 / 0 | 19,6 / 10,2 / 0 (2 koşu) | 8,1–9,7 / 0 (4 koşu) |
| yürüyüş klip sırası | kalkış → Ranger 1,45 s → SHM245 | aynı | aynı |
| taps | 17,3 / 0 | 17,3 / 0 | 15,4 / 3 (36; gerçek-zaman taps tabanı yok) |
| gait | 6,8 / 0 | 6,8 / 0 (dc partisi; dc2 koşusu disk doluyken kaybedildi) | 8,4 / 2 (32) |
| wdiag | 18,1 / 0 | 18,1 / 0 | 12,1 / 0 |
| w43_idle | 6,3 / 0 | 6,5 / 0 | — |
| inrt gerçek zaman (aday, üretim dışı) | — | taps 12,8 / 1 (36); jstart 46,5 / 4 (40) | |
Not: `v246dc2_taps` ve `v246dc2_gait` koşuları disk dolu (0 B) anında kesildi (LTP 30 satır / yok); taps temiz oturumda yeniden koşuldu (`v246fin_taps`).
