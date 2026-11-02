# TABLES V2.48 (2026-11-02)

Senaryo `j45_sl` / `j45_sl2` (2,7 s sağ koşu-yanal → tam duruş → bakışa göre SOL istek; sl2 = istek 4,4 s tutulur). "istek" sütunu = istek anında beden-göreli açı (bakış yaw'ı gerçek zamanda 0–63° arasında değişir, bu yüzden açı koşudan koşuya değişir). Kayma = `contact231` en kötü SLIP/DRAG (cm). **Ölçüm notu:** §2–3'teki ilk sayılar 9,5–14,5 s penceresiyle alındı; bu pencere duruştan (9,0 s) önce başlayan basılı-ayak temasını DIŞARIDA bırakıyordu. Pivot fazının gerçek sürüklenmesi §6'da (8,5–13 s penceresi, duruştan itibaren) — karar o tabloya göre verildi. Pop = >25 m/s² sayısı.

## 1. Üretim (V2.45) — gerçek zaman, istek beden-göreli −138…−170°
| koşu | istek | ilk klip | kayma | not |
|---|---|---|---|---|
| v246lrreal o r2 | −170 | SHM233_StandBack2 → af_Loco_Jog_Bwd_Start | 22 + 55 | geriye koşarak kalkış (yanlış) |
| v248tsreal o r2 (V2.47 durumu) | −146 | af_Loco_Jog_Bwd_Start → A_LS_Jog_Left | 0,0 | geriye kalkış 0,45 s, sonra yan adım |
| v248tmreal o r2 | −139 | af_Loco_Jog_Bwd_Start | 0,0 | geriye kalkış |
| v248th60/tm60 o (60 FPS) | −137 | af_Loco_Jog_Bwd_Start → A_LS_Jog_Left | 9,4 | geriye kalkış + yan adım karışımı |
| istek −118…−124 (o, 6 koşu) | | A_LS_Jog_Left_Start | 5,8–11,7 | doğru (yanal kalkış), referans aralığı |

## 2. Aday aşamaları (ts = `SHM248_On` 1), istek −136…−162
| aşama | 30/60 FPS | gerçek zaman | sorun |
|---|---|---|---|
| A rota (dönüş DB, sözleşme yok) | 60: TurnL135, 25 cm (pivot sırasında) | 31,5 / 39,0 (TurnL180/135 @0,47) | klip yerinde dönerken kapsül CMC ivmesiyle ilerliyor; LS yanal rotası dönüşü 0,63 s'de kesiyor |
| C bağlama (hız/yön sözleşmesi V2.28/V2.38 + tutma) | 60: 25,2 | 19,8 / 22,5 | pivot sürüklenmesi yarıya; dönüş tamamlanıyor (−138/−140 tam); tutma döngüsel → 2,2 s kalkış DB'si |
| D tutma-bırakma (T≥89) | 60: 25,2 | — | bırakma sonrası kapsül yine sözleşmede (redirect episodu) |
| H her iki yön DB + işaretli dönüş + yanal hız | 60: ilk 0,5 s'de sürüklenme yok; 20–31 (klip koşu adımları 1,2–1,9 s) | 30,3 / 47,2 / 15,8 (klip sonu devri 11,8–12,0) | 2,3 s klibin koşu-adımları + devirde başka bir kalkış klibi |
| I sözleşme sahipliği (orta-klip bırakma) | 60: 59,8, pop 72, yaw −47/+23/−30 | — | ABP redirect episodu yaw'ı devralıyor → GERİ ALINDI |
| K/L kırpılmış dönüş klipleri (0,93–1,0 s, T2 DB) | 60: 29,8 | — | dönüş sonu gövde bakışa geri dönüyor (loco çerçevesi hâlâ bakış) |
| **M + loco çerçeve takibi (SON)** | **60: 5,7** (üretim 9,4) | **5,8 / 17,2** (−136/−137); −117…−121 istekler LS 6,0–8,7 | — |

## 3. Son aday (M) gerçek zaman ×8 ve regresyonlar
| koşu | istek | ilk klip | kayma | pop |
|---|---|---|---|---|
| tmreal ts r1 | −137 | TurnL135_crop → CP2 kalkış devri | 17,2 (10,57 CP2_Jog_Fwd_Start@0,52) | 1 |
| tmreal ts r4 | −136 | TurnL135_crop | 5,8 | 2 |
| tmreal ts r2 | −117 | StartTransfer (yürüyüş gait) | 6,1 | 0 |
| tmreal ts r3 | −120 | A_LS_Jog_Left_Start | 8,7 | 2 |
| tmreal j45_sl ts r1/r2 | −121/−118 | A_LS_Jog_Left_Start | 6,0 / 5,7 | 2 / 5 |
| tmreal o r1/r2 | −122/−139 | LS / **Bwd** | 5,9 / 0,0 | 2 / 3 |
| tm60 ts / o | −138/−137 | TurnL135_crop / Bwd | 5,7 / 9,4 | 22 / 21 |
| gerçek zaman jstart / taps / wstart (ts) | | | 42,6 / 19,3 / 22,3 | 7 / 1 / 1 |
| 30 FPS (th30, aşama H) taps / wstart / gait / w42 / jstart / j41_rl_p10 | | | 17,3 / 21,0 / 6,8 / 10,2 / 26,0 / 14,3 | 0/0/0/0/5/4 |
30 FPS taps / wstart / gait / w42 üretimle aynı (17,3 / 21,0 / 6,8 / 10,2). jstart ve j41_rl_p10 üretim çiftleri: §5.

## 4. Klip içi yazılan ayak hareketi (authdrift248, TurnL135 kopyası)
Basılı sağ ayak ilk 0,43 s'de 0,0–0,4 cm (yazılı pivot yok); oyunda A aşamasında 39 cm, C'de 20–25 cm, H+ (yanal hız) ile 0 → kayma kapsül yolundan geliyordu, içerikten değil.

## 5. Üretim doğrulaması (terfi sonrası, temiz oturum, `SHM248_On` 1, `verify241 ALL_OK`)
| | 30 FPS | gerçek zaman | 60 FPS |
|---|---|---|---|
| j45_sl2 | −119 → LS 10,2 | r1 −122 → TurnL135 30,3; r2 −180 → TurnR180 49,1; r3 −121 → LS 15,5 | −137 → TurnL135 26,8 (pivot) / 5,7 (devir) |
| j45_sl | −119 LS 10,2 | −113 LS 8,5; −119 LS 14,2 | −137 TurnL135 26,8 |
| taps / wstart / w42 / gait / w43 | 17,3 / 21,0 / 10,2 / 6,8 / 6,5 (= V2.45) | 15,2 / **53,1** (SHM245_Walk_Fwd@2,79; aday turunda 22,3 — atfedilemedi, tekrar gerek) / 9,5 / — | — |
| jstart / j41_rl_p10 / j42_lr_p10 | 33,9 (önce 57,4) / 14,1 (önce 9,1) / 12,5 | 33,9 | 42,8, pop 74 (90° segment devri; önce 47) |

## 6. Pivot fazı sürüklenmesi, duruştan itibaren (8,5–13 s penceresi) — karar tablosu
| koşu | istek | klip | en kötü ayak (cm) |
|---|---|---|---|
| tmreal ts r1 / r4 | −137 / −136 | TurnL135_crop | 25,4 / 22,6 |
| prodreal o r1 | −122 | TurnL135_crop | 30,3 → eşik 130° ile LS'e bırakıldı (§7) |
| prodreal o r2 | −180 (bakış yaw 0) | TurnR180_crop | 49,1 |
| **üretim V2.45 aynı istekler** | −139 / −146 / −170 | af_Loco_Jog_Bwd_Start (geriye koşarak) | **36,8 / 40,9 / 55,3** |
| klipte yazılı (authdrift) | | TurnL135 basılı ayak ilk 0,43 s | 0,4 |
Dönüşlü kalkış: davranış doğru + aynı isteklerde geriye kalkıştan 10–25 cm daha az sürüklenme; ama yazılı 0,4 cm'e karşı 22–30 cm hâlâ açık (kapsül klip kök yolunu pivotta tam izlemiyor: devreye giriş gecikmesi 0,12 s + yön hızı/Delta ölçekleme).

## 7. Eşik 130° doğrulaması (`SHM248_BackCos` −0,64, temiz oturum, gerçek zaman ×5 + wstart)
| koşu | istek | klip | kayma (8,5–13 s) |
|---|---|---|---|
| prod2real r1 / r3 | −137 / −137 | TurnL135_crop | 25,8 / 26,2 |
| prod2real r2 / r4 / j45_sl r1 | −123 / −121 / −119 | A_LS_Jog_Left_Start (eşik altı → LS) | 5,2 / 12,0 / 7,6 |
| prod2real wstart | | | 26,9 (önceki 53,1 gerçek-zaman varyansıydı; 30 FPS 21,0) |
