# TABLES V2.45 (2026-11-01)

## 1. Bırakma-fazı taraması (j45_rl_r0..5 sol / j45_lr_r0..5 sağ; ikinci yanal segmentin bırakması `A_CT_Jog_Left/Right` döngüsünün 6 penceresine kilitli, zaman aşımı 1,5 s; üretim = PSD_SHM244_LatStop)
| Koşu (30 FPS) | bırakma anındaki döngü | seçilen duruş | duruş episodu | okuma |
|---|---|---|---|---|
| rl_r0 | `A_CT_Jog_Left`@0,03 (döngü girişi) | `SHM237_JogStop_Bl_P04` (İLERİ aile) | 13,6 (ayak 143°) | aile sınırı yönlendirmesi |
| rl_r1..r5, lr_r0, r1, r4, r5 | `A_CT_Jog_Fwd` (strafe keşifle düz jog'a döndü, pencere yakalanamadı) | ileri JogStop | — | harness/keşif sınırı; yanal aile girmedi |
| lr_r2 | `A_CT_Jog_Right`@0,42 | `SHM244_LatStop_R_Bl_P20` | duruş temiz; idle devralma 9,0 | yanal aile PASS |
| lr_r3 | `A_CT_Jog_Right`@0,62 | `SHM_M_Neutral_Walk_Stop_F_Rfoot` (satıcı YÜRÜYÜŞ duruşu) | 13,5 | aile sınırı yönlendirmesi |
| gerçek zaman: rl_r3 | `A_CT_Jog_Left`@0,64 | ileri JogStop_Bl_P04 + satıcı walk stop | 13,4 | yönlendirme |
| gerçek zaman: lr_r2 | `A_CT_Jog_Right`@0,44 | `SHM244_LatStop_R_Bl_P20` | temiz; devralma 9,2 | PASS (tekrarlanabilir) |
| gerçek zaman: rl_r1, r5, lr_r4 | `A_CT_Jog_Fwd` | ileri JogStop | ≤ 7,5 | keşif |
Daha önce ölçülen yanal faz girişleri: p04 (döngü 1,1–1,2 → Br_P23, 8,1), p10 (0,47–0,55 → Bl_P11, 5,4; V2.42 ailesinde P21 32,5).

## 2. Duruştan sonra yanal istek (`j45_sl`: 2,7 s sağ strafe → tam duruş → bakışa göre SOL)
| Koşu | duruştaki beden / bakış | seçilen kalkış | kalkış episodu | not |
|---|---|---|---|---|
| 30 FPS r1, r2 | beden 0°, bakış ~60° | `A_LS_Jog_Left_Start` | 5,5 DRAG | aynı (deterministik) |
| gerçek zaman r1 | −90 / 0 | `A_LS_Jog_Left_Start` | 8,5 | |
| gerçek zaman r2 | −56 / 0 | `A_LS_Jog_Left_Start` | 7,5 (+ duruş sonu 12,9, R_Bl_P10@0.94 dyaw 70) | |
| gerçek zaman r3 | ~180 / 0 | **`af_Loco_Jog_Bwd_Start` (geriye kalkış)** | **23,0 + 38,6** (ayak 134–177° dönüyor) | V2.44'teki 23–48 cm sınıfı |

Sahip: V2.34 keşif çerçevesi strafe sırasında bedeni seyre çeviriyor; gerçek zamanda duruş anındaki beden/bakış farkı koşudan koşuya değişiyor (−56…180°); kalkış ailesi (JogQ DB: dönüşlü kalkışlar + LS strafe kalkışları) bu farkı kalkış içinde ayakta döndürüyor; duruş ile yeniden basış arasındaki 0,3–0,4 s'de ayakta dönüş (needs-look kuralı) henüz ateşlenmiyor. Fark ≤ 90° → LS kalkışı 7–9 cm; fark ~180° → geriye kalkış 23–39 cm.

## 3. Idle–kalkış (jstart 135° dönüşlü kalkış, 20,0 s)
| | hold AÇIK (üretim) | kapı KAPALI (og / idl4) |
|---|---|---|
| kalkış anında MM klibi | `SHM_M_Neutral_Walk_Stop_BR` @2,36 (donmuş) | @2,93 (oynamaya devam) |
| sağ omuz (pelvise göre x/y) | −5,1 / 15,5 | −9,8 / 18,0 |
| 0,13 s sonra (`A_LS_Jog_Left_Start`@0.05) | +4,4 / 15,7 (8,6 cm) | +2,2 / 16,4 (12,7 cm) |
| `SHM_IdleUpperW` | 0,86→0,57 | 0,93→0,60 (aynı katman) |
| pop | yok | 26 / 32 m/s² |

## 4. Yürüyüş — metrik sahibi
| | klip (A_LB_Walk_Fwd) | oyun (gait242) |
|---|---|---|
| pelvis Z-burgusu p2p / kalça çizgisi p2p | 12,1 / 12,06 | — / 11,6 |
| klavikula çizgisi p2p | 15,63 | 14,8 |
| karşı dönüş | 23,9 | 23,0 |
| V2.44 adayı (burgu ×0,65, göğüs ×0,55): kalça çizgisi / klavikula / karşı | ~10,9 / ~12 / — | 10,5 / 12,5 / 19,1 |
| V2.45 adayı (kalça çizgisi ×0,65, klavikula ×0,55): | **7,84 / 8,60 / 14,04** (ayak hatası 0,007, baş 0) | (bölüm 5) |

## 5. Yürüyüş adayı oyun içi (proje klibi `SHM245_Walk_Fwd` → `PSD_LB_WalkLoops` BranchIn + ModifyCost −1; AYNI oturum önce/sonra, 30 FPS)
| w42_id düz yürüyüş | önce (A_LB_Walk_Fwd) | sonra (SHM245_Walk_Fwd seçiliyor, 186/186 kare) |
|---|---|---|
| karşı dönüş p2p | 23,0° | **19,6°** (r1 = r2) |
| kalça çizgisi yaw p2p (gait242 / pencere 2,6–5,4) | 14,0 / 11,6 | 13,8 / 10,5 |
| klavikula çizgisi yaw p2p (pencere) | 14,8 | — (karşı dönüşten ≈ 12) |
| kol salınımı l/r | 28,7 / 34,6 | 27,3 / 33,6 |
| kadans / adım | 1,9 / 72,9 | aynı |
| ayak kayması (koşu en kötüsü) / pop | 10,3 / 0 | 10,2 / 0 |
| gait (yürü→jog→sprint) | 8,3 / 0 | 6,8 / 0 (jog→sprint itişi aynı bin) |
| taps | 17,3 / 0 | 17,3 / 0 |

Okuma: klipte kalça çizgisi 12,1→7,8 düşmesine rağmen oyunda 11,6→10,5: MM çıkışındaki pelvis yaw'ı (`SHM_HCi_pelvis_RZ` eğrisi, IK öncesi) zaten 11,6→10,4 → kliple oyun arasına giren katman MM sonrası, IK/FootPlacement öncesi (OrientationWarping / StrideWarping / blend stack adayları; bölüm 6 izolasyonu). Göğüs tarafı klipteki gibi düştü.

## 6. Pelvis yaw sahibi izolasyonu (w42_id düz yürüyüş penceresi 2,6–5,4 s, aday üretimde)
| varyant | kalça çizgisi | klavikula | karşı dönüş | MM çıkışı pelvis RZ eğrisi | seçilen klipler |
|---|---|---|---|---|---|
| o | 10,5 | 12,4 | 19,6 | 10,4 | SHM245_Walk_Fwd 57 kare + **M_Ranger_Walk_Loop_F_PureForward_CWF 28 kare** |
| oow (OrientationWarping 0) / osw (StrideWarping 0) / ofp (FootPlacement+LegIK 0) / oRAW / oSCR / oPBI | 10,5 / 12,4 / 19,6 (hepsi bit-özdeş) | | | 10,4 | aynı |

Okuma: (1) izolasyon anahtarları bu harness yolunda etkisiz görünüyor (altı varyant bit-özdeş) → bu koşular negatif kanıt sayılmadı. (2) Asıl bulgu klip listesinde: düz yürüyüşün ~1/3'ü (28/85 kare) `PSD_Dense_Stand_Walk_Loops`'tan **`M_Ranger_Walk_Loop_F_PureForward_CWF`** (206 cm/s'lik döngü 0,64× oynuyor) ile oynuyor; MM iki DB arasında gidip geliyor. Adayın pelvis genliği klipte 7,8 iken oyunda 10,5 olmasının sahibi bu karışım: kalan pelvis yaw'ı Ranger döngüsünden geliyor (göğüs tarafında da aynı). Kalıcı yürüyüş kimliği için Ranger yürüyüş döngüsünün yürüme DB kümesinden çıkarılması veya maliyetlendirilmesi gerekiyor (chooser/DB kararı, bu turda yapılmadı).

## 7. Üretim (temiz oturum, yeniden başlatma sonrası, `verify241 ALL_OK true`, 30 FPS) — V2.44 → V2.45
| Senaryo | V2.44 üretim | V2.45 üretim |
|---|---|---|
| w42_id karşı dönüş / kayma / pop | 23,0° / 10,3 / 0 | **19,6°** / 10,2 / 0 |
| gait | 8,3 / 0 | 6,8 / 0 |
| taps | 17,3 / 0 | 17,3 / 0 |
| j41_rl_p10 duruş | 5,4 (Bl_P11) / 2 (28) | 5,4 / 2 (28) |
| j42_lr_p10 | 12,5 (strafe kalkışı) / 0 | 12,5 / 0 |
| w43_idle | 6,5 / 0 | 6,5 / 0 |
| jstart | 57,4 / 4 | 57,4 / 4 |
| wdiag | 18,1 / 1 | 18,1 / 0 |
| gerçek zaman w42_id | — | 19,2°, 6,6 cm, pop 0 |
