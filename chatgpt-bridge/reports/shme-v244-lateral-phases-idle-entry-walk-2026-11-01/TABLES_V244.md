# TABLES V2.44 (2026-11-01)

## 1. Bl_P21 teşhisi (V2.43 üretim, j41_rl_p10, LTP 30 FPS)
| Zaman | Olay |
|---|---|
| 11,77 | bırakma; sol ayak döngüde havada, 0,11 s sonra iniş noktasında |
| 11,80 | `SHM242_LatStop_L_Bl_P21` girişi; plan: fren ayağı (sol) 38,3 cm ileride, t_land 0,11 s, final değil |
| 11,83–11,87 | ayak yaw'ı +10° → −88° (0,07 s'de ≈ 100°): final olmayan plantta klip ayak yönünü idle yönüne (QFIN) çeviriyordu (`cur_q = QFIN` koşulsuz) |
| 11,90–11,97 | döngü inişi (karışım) yerde 3 kare; sonra ayak yeniden kalkıp 31 cm ileriye (klibin plant noktası) kayıyor; 12,17 ikinci iniş |
| 11,77–12,40 | contact231 bunu tek "basılı" episod sayıyor: 32,5 cm, dyaw 86° (beden yaw'ı sabit −167°: dönen beden değil, AYAK) |

Riskli binler (fren ayağı havada, iniş < 0,2 s, ileri istek > 15 cm): L Bl_P09–P11, Bl_P20–P22; R Br_P02–P04, Br_P14–P15.

## 2. Düzeltme (gen244_latstop.py) ve aile
(a) ulaşılabilir ilk iniş: `lim = doğal döngü inişi + 60 cm/s × t_land` (Bl_P21: 38,3 → 12,8 cm); (b) final olmayan plant yön sürekliliği: `q1 = slerp(döngü q, QFIN, 0,45)`, tam dönüş yalnız final plant'a giden salınımda. Yan etki: V2.42'de leg-guard'a takılan 9 (L) + 4 (R) binin 13'ü geçti (diz-ekseni sıçramasının sahibi yön sıçramasıydı); yeni aile 42/48 klip (`PSD_SHM244_LatStop`), reddedilen: L Br_P17 (drift 20), R Br_P02/Bl_P08 (guard), R Bl_P16–18 (drift 13–31, V2.42'de de aynı).

## 3. Aday C1 (30 FPS, aynı editör, üretim = V2.43)
| Senaryo | üretim (V2.43) | lat4 (yeni yanal aile) | idl4 (nötr-girişli idle, kapı kapalı) | all4 |
|---|---|---|---|---|
| j41_rl_p04 duruş episodu | 8,1 DRAG Br_P23 | **0** (pencerede episod yok; koşu en kötüsü 9,0 jog kalkışı) / pop 1 (28, önceki gibi) | — | — |
| j41_rl_p10 | 32,5 SLIP Bl_P21 (3 koşu) | **5,4** (Bl_P11@0.30, dyaw 18°) / pop 2 (28) | — | — |
| j42_lr_p10 idle devralma | 14,6 (af_Stand_Idle@79.17, ayak 51°) | **6,1 + 9,3** (af_Stand_Idle@58.13) / pop 0 | — | pencerede episod yok (en kötü 12,5 = strafe kalkışı, üretimle aynı) |
| w43_idle 8 s | hold True, donuk | — | hold False, `SHM244_Idle_Weighted` 206/206, giriş @1.20 s (nötr), eksen −5,9…+4,8, kayma 0 beklemede, kalkış sonrası 6,4 (üretim 6,5) / pop 0 | — |
| w42_id | 10,3 (yürüyüş döngüsü) / 0 | — | 21,8 (A_LB_Walk_FwdRight@1.03, 30° viraj) / 0 — üretim aynı pencerede 10,3 (A_LB_Walk_Fwd@0.35, dyaw 54°); viraj döngü seçimi farkı | — |
| taps | 17,3 / 0 | — | 19,0 (@1.03 nötr giriş; idlg3: 22,7 @11.0) / 2 (26, bırakma duruşları) | 19,0 / 2 |
| jstart | 57,4 / 4 | — | 60,2 / 6 (+26 @17,2, +32 @20,2: 135° satıcı dönüşlü kalkış, omuz; kapı-kapalı üst beden) | — |
| j40_rlw | 11,2–17,2 / 3 | — | 21,3 (A_CP2_Jog_Fwd_Start@0.45) / 3 | — |
| gait | 8,3 / 0 | — | 14,6 / 4 (26–30, jog→sprint itiş bini farkı) | — |

## 4. Kare hızı / gerçek zaman matrisi (lat4 = yeni yanal aile; duruş penceresi episodları; "—" = pencerede episod yok)
| FPS | j41_rl_p04 üretim → lat4 | j41_rl_p10 üretim → lat4 | j42_lr_p10 (sağ) üretim → lat4 |
|---|---|---|---|
| 20 | — → — | 5,4 (Br_P23) → — | — |
| 30 | 8,1 → **0** | 32,5 (Bl_P21) → **5,4** (Bl_P11) | 14,6 (idle devralma) → 6,1 + 9,3 |
| 60 | 7,6 → 7,6 (Br_P23) | — → — | 5,6 (devralma) |
| 120 | — | — → — (pop profili özdeş 10×, en kötü 93 klip içi, üretimle aynı) | — |
| gerçek zaman (29–35 Hz) | duruş —; **kalkış** 23,5/47,9/10,5 (satıcı TurnL045 + A_LS_Jog_Left_Start, V2.42'den beri bilinen gerçek-zaman kalkış varyansı) | r1 —, r2 6,9 (Br_P23) | 11,0 (R_Bl_P07 girişi; üretim gerçek zaman: 17,5 devralma) |

Idle (idl4) gerçek zaman w43_idle: klip 265 kare oynuyor, giriş @1,23 s, eksen −5,8…+4,9, bekleme kayması 0, kalkış sonrası 5,9 (üretim 6,5), pop 0.

## 5. Yürüyüş adayı (w42_id mv_walk_0_0, 30 FPS)
| | üretim (A_LB_Walk_Fwd) | walk4 (bellek içi: pelvis yaw ×0,65, göğüs ×0,55) |
|---|---|---|
| klip içi pelvis / göğüs / karşı dönüş p2p | 12,1 / 16,3 / 26,2° | 7,9 / 8,9 / 15,4° |
| oyun içi karşı dönüş p2p | 23,0° | **19,1°** |
| oyun içi pelvis yaw p2p | 14,0° | 13,8° |
| kol salınımı l/r | 28,7 / 34,6° | 27,3 / 33,7° |
| pelvis yanal / dikey, baş dikey | 3,7 / 5,5 / 5,6 | aynı |
| kadans / adım / çift destek | 1,9 / 72,9 / 0,021 | aynı |
| ayak kayması (koşu en kötüsü) / pop | 10,3 / 0 | 10,3 / 0 |

## 6. Üretim (terfi SONRASI, temiz oturum, bayraksız `o`, 30 FPS)
| Senaryo | V2.43 üretim | V2.44 üretim | pop |
|---|---|---|---|
| j41_rl_p04 duruş | 8,1 (Br_P23) | 8,1 (SHM244 Br_P23; bin (a)/(b) değişikliğinden etkilenmiyor) | 1 (28) aynı |
| j41_rl_p10 duruş | 32,5 (Bl_P21) | **5,4** (Bl_P11) | 2 (28) aynı |
| j42_lr_p10 idle devralma | 14,6 (af_Stand_Idle@79) | **6,1 + 9,3** (af_Stand_Idle@58.1) | 0 aynı |
| taps / gait / w42_id / w43_idle | 17,3/0 · 8,3/0 · 10,3/0 · 6,5/0 | aynı | aynı |
| jstart / wdiag / j40_rlw | 57,4/4 · 18,1/1 · 17,2/3 | aynı | aynı |
