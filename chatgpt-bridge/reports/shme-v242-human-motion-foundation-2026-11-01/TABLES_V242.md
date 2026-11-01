# TABLES V2.42 (2026-11-01)

Kayma = `contact231.py` (görünür ayak topu; SLIP = basılıyken ≥ 5 cm yatay sürüklenme, DRAG = düşük ayak kaydırma). Pencere = fren girişi → duruş sonrası ilk dönüş. Sabit adım 30 FPS, aksi yazılmadıkça.

## 1. Yanal fren/duruş (A1) — en kötü kayma, fren penceresi

| Senaryo (faz) | o (üretim, satıcı A_LS_Jog_*_Stop) | lat (SHM242_LatStop) | latg (lat + dönüş kapısı) | Not |
|---|---|---|---|---|
| j41_rl_p10 (sol, tur 1) | 38,3 SLIP @1.79 | 6,2 DRAG (Br_P23 @0.12) | — | lat1 |
| j41_rl_p10 (tur 2, r2) | — | 9,1 (kalkış klibi, duruş 0) | — | |
| j41_rl_p10 (latg) | — | — | 32,5 SLIP (Bl_P21) = duruş SONRASI dönüş montajı basılı ayağı sürüklüyor (kapı montajı 0,6 s erteledi, kayma montajda) | |
| j41_rl_p16 | — | 9,2 (kalkış klibi, duruş 0) | — | |
| j41_rl_p04 (tur 1) | — | 32,2 SLIP dyaw 101° (Bl_P21: dönüş montajı klip oynarken) | — | |
| j41_rl_p04 (tur 4) | 39,2 SLIP (+17,5 r) | 8,1 DRAG (Br_P23) | 8,1 DRAG; montaj 12,00 → 12,43 s (yerleşme sonrası) | |
| j41_rl_p10 kayıtlar | oS 36,6 | latS 6,8 | — | kamera türevleri |
| j42_lr_p10 (sağ, ayna) | 12,5 (kalkış), duruş: satıcı A_LS_Jog_Right_Stop | 0,0 (PIVOT 41° dönüşte) ×2 | — | |

Klip içi (jeneratör kontrolü, dünya): L 15 bin planted_drift ≤ 2,2 cm, foot_err ≤ 8,5; R 20 bin, 3'ü (P16–18, 13–31 cm) DB dışı. Diz-ekseni koruması: L 9 / R 4 bin atlandı (çapraz adım, 60–94°).

## 2. Duruş sonrası yeniden yönelme (A2)

| Koşu | Kapsül 0 (s) | Dönüş montajı (s) | Gecikme | Montajda ayak sürüklenmesi |
|---|---|---|---|---|
| p04 lat | 12,00 | 12,00 | 0 | klip oynarken, 32 cm (tur 1) |
| p04 latg | 12,00 | 12,43 | 0,43 | 8,1 (ayak salınımda) |
| p10 latg | 12,27 | 12,87 | 0,60 | 32,5 (Bl_P21: basılı ayak, montaj root motion) |

## 3. Yürüyüş identity tabanı (w42_id, üretim, `gait242.py`)

| Metrik | Yürüyüş 0° (×2) | 30° | İnsan referansı (173 cm, 1,32 m/s) |
|---|---|---|---|
| hız (cm/s) | 125,6 | 121,7 | 132 |
| adım (cm) / sd | 72,9 / 0,6 | 79,8 / 22 | ~70 |
| kadans (adım/s) | 1,67–1,69 | 2,57* | ~1,9 |
| çift destek oranı | 0,02** | 0 | 0,20 |
| pelvis yanal / dikey p2p (cm) | 3,7 / 5,5 | 7,2 / 7,8 | 4–6 / 4–5 |
| baş dikey p2p (cm) | 5,6 | 8,1 | ~4 |
| pelvis–göğüs karşı dönüş p2p (°) | 23 | 23 | 8–12 |
| kol salınımı p2p l/r (cm) | 29 / 35 | 45 / 38 | 25–35 |
| MM oynatma hızı | 1,24 (A_LB_Walk_Fwd 106 → 132) | 1,16 | 1,0 |
| duruş: kapsül / ayaklar / pelvis (s), mesafe | 0,53 / 0,80 / 0,90, 33,7 cm | | |
| kalkış: ilk kaldırma / %90 hız (s), ilk adım | 0,33 / 0,73, 72 cm | 0,17 / 0,73, 108 cm | |
| idle: pelvis / göğüs / baş p2p (cm) | 0,09 / 0,2 / 1,7 | | pelvis 1–3, göğüs 0,5–1 (nefes) |

\* 3 adımlık kısa pencere, kalkış dâhil. \*\* 'düşük' bandı (p10 + 3,5 cm) topuk kalkışını kaçırıyor; göreli karşılaştırma için.

## 4. FPS matrisi (A8) — yanal duruş, en kötü kayma (fren penceresi) / dönüş montajı gecikmesi

| FPS | j41_rl_p04 o | j41_rl_p04 latg | j42_lr_p10 latg (sağ ayna) |
|---|---|---|---|
| 30 | 39,2 SLIP (A_LS_Jog_Left_Stop @1.80) | 8,1 DRAG (Br_P23), montaj +0,43 s | 0,0 (P19), ×2 (lat) |
| 60 | 59,3 SLIP (@1.85, dyaw 81°), montaj +0,0 s | 9,0 DRAG (Br_P23), montaj +0,37 s | 9,0 (kalkış klibi A_CT_Jog_Right; duruş R_Bl_P19 temiz), montaj +0,25 s |
| 120 | 39,0 SLIP (@1.49, dyaw 84°), montaj +0,0 s | 6,2 DRAG (kalkış klibi; duruş Br_P13 temiz), montaj +0,17 s | — |
| gerçek zaman | üretim bu koşuda farklı rotaya girdi: yeniden kalkışta `TurnL045` (jstart sorunu), 91,7 cm DRAG, yanal duruşa hiç girmedi | 22,4 DRAG (Bl_P21 @0.32, dyaw 25°), montaj +0,59 s | — |

Okuma: sabit adımda (30/60/120) yanal duruş klibi temiz (6–9 cm, hepsi DRAG/kalkış klibinde); gerçek zamanda fren ayağı 22 cm sürükleniyor (değişken kare süresinde klip kökü ile CMC fren profili ayrışıyor — V2.28 klip-bağlı kapsül bu klip ailesine henüz uygulanmadı). Üretimin gerçek zaman koşusu karşılaştırılamaz (farklı kalkış rotası).
