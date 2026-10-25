# V2.28 çalışma notları (rapora işlenecek sayılar, 2026-10-25 02:xx)

## Hareket (rhC = tutma + klip-bağlı kapsül, FP açık)
- Sabit 30 (yükseklik|temas): ph0 13,0|13,0 (üretim 49,7); ph3 12,1|7,7 (16,6); sw_ph0 5,8 (16,7|10,9); sw_ph2 9,2 (26,1–31,2); rel 36,6|37,7 (30,4); dbl 26,9|26,5 (35,5|5,2).
- FP: rhCF (FP klipte kapalı) ph3 21,9 / ph0 18,0 → FP açık daha iyi; rhC0 (ileri bakış yok) ph3 16,5 → bir kare ileri bakış işe yarıyor.
- 60 FPS: ph0 5,8 (32,4); ph3 18,5 (15,4); sw_ph2 11,7 (21,6); ovl120 8,8 (23,4); dbl 32,0|32,4 (31,2|27,8); rel 28,5|1,6.
- 120 FPS: ph0 13,0|12,2 (30,5); ph3 13,3 (26,7|17,7); sw_ph2 30,7 (51,6) [B_F P6 kutusu, içerik]; ovl120 14,5|14,3 (35,2|24,7); rel 33,1|32,4.
- 20 FPS: ph0 15,0 (49,6); ph3 18,5|20,1 (16,8|13,3); sw_ph2 7,4 (25,3); ovl120 7,6 (65,4|24,4); dbl 22,2 (32,5|7,2); rel 34,8|37,6.
- Gerçek zaman: ph0 soğuk GEÇERSİZ (Shift tap kaçtı → yürüyüş; v228rt ph0 0.0); sw_ph2 34,7 (üretim rt 17,6; P6 kutusu); dbl 23,8 (15,3); ph3 13,5|14,1.
- clipspeed228: |v_act − desV| ≤ 5 cm/s sonraki karelerde, integral ~1 cm (30, 60 FPS; 120'de −0,1 cm); ilk telafi karesi 24–64 cm/s.
- Çıkış (exit227, rhC 30): ph0 1,8/2,7; ph3 1,9 (F_B) ve 1,8 (B_F P29, FP açık); sw_ph0 2,7/1,6; sw_ph2 1,8/2,0; klipler 1,43–1,60 s (bitime 0,29–0,30 s).
- Kol/baş/gövde (arms228): el devir sıçraması 11 cm (üretim pivot 14–17), baş 1–2 cm, göğüs–leğen karşı dönüş −9…+13 korunuyor, ikinci hazırlık yok.
- İptal yolları (rhCR, 1. sürüm): dbl 10,8|9,9 AMA kontrol kilidi (W basılıyken 3 s geri koşu: reroute arama kısıtına takıldı) → 2. sürüm (ThrOK, güçlü interrupt, niyete karşı güvenlik 0,08 s) GEN2 zincirinde test edilecek. rel 33,9 (RelHold ile fren sonuna tutma: dur → Start_AAMS).
- İçerik: 10 kutu (B_F P6 P14, F_B P2 P6 P10 P13 P18 P26 P29 P30) fren ayağı tau0'da zaten zeminde ve 24–46 cm zeminde yeniden konumlanıyor → FP sürüklemesi 30 cm (P6 @120/rt). gen228 kuralı ile yeniden üretim GEN2'de.

## Arazi (T5)
- ter_drop_jog 28 cm: üretim L ilk basış 3,5 cm içeri, topuk −12,5 boşlukta, z −6,3 (yüzeye girme), kaldırma 24,8 (tavan 25); tl36: z −1,7 (giderildi), topuk aynı; te4 (gerçek-kenar kaydırma 12): 9,3 cm içeri, topuk −6,7, z −1,7.
- ter_drop_walk 28: tl36 R 11,1 içeri topuk −4,9; te4 13,4 içeri topuk −2,6; askı 0,37–0,47 s (R, basıştan önce yüzeyin 4 cm üstünde bekleme).
- Yanlış tetikleme: map_r1 te4 7 kare (max 8 cm) [V2.26 te6x: 278 kare]; hill8_jog 0; bump_jog 27 (gerçek 13 cm kutu kenarı); step2 70 (gerçek basamaklar).
- Kaldırma tavanı 36 ile map_r1 lift max 36 (eskiden 25'te doyuyordu) — rota üstü etkisi kontrol edilecek (pop 10/57).

## İnceleme (T5)
- ins5 (kimlik + aktör konumu odak): ins_ws2 iki yakın maske — Silent 3 kare → Cerulean: dwell kimlikle sıfırlandı, mandal 4,07 (üretim 3,93: mesafe kuralı 29 cm komşuyu aynı saydı); 5,63'te Silent'a dönüş: 0,27 s dwell sonrası yumuşak geçiş, mandal düşmedi. Odak x 33 (maske merkezi) vs üretim 47,7–48,6 (sonda küre bounds'u 15 cm odaya kaydırıyor).
- Bakış ölçümü (gaze228): ins_ws2 ort. hata 5,8–6,1°, baş–gövde yaw −8…+10°, 10° içine 0,57–0,63 s; ins_ws ort. 10,7–11,2 (yürüyüş dönüşü geçişi), min 1°.
- Kusur: mandal yokken yeni hedefte InspectPoint eski noktadan (0,0,0) süzüldü → snap düzeltmesi (CameraV21 yeniden derleme BUILD228b).
- LookAt ekseni zaten +Y (ilk "aşağı eğiliyor" okuması yanlıştı; düğüm değiştirilmedi).

## Harness olayları
- rt soğuk ph0: Shift tap kaçtı → yürüyüş (geçersiz).
- GR kurulumunda ivme sıfırlama niyeti öldürdü (1. parti 58 cm); sınıf pini nesne yerine yol dizesi; profil sınıf paketi reload → PBI GR_Profile None (kurucu yakaladı, editör yeniden açıldı); GetWorldDeltaSeconds NATIVE'de yok; InRange tip adı yerelleşmiş; W eşiği 0,3 → 0,1 (3 kare gecikme).
- Cancel 1: SelectObject tipli DB pinine bağlanamadı → exec dalları; Cancel 2: AnimGraph NOT/AND bağlantısı reddedildi → ThrOK bayrağı snapshot'ta.
- LookAt enum: u.Axis = FAxis struct (Vector axis) — gereksiz kurulum iptal edildi.

## T6 (snap fix derlemesi sonrası)
- te4b (StepEdgeShift 18 + tavan 36): koşu 28 cm L ilk basış 16,0 cm içeri, topuk +0,0 (kenarda, boşlukta değil), z −1,1; yürüyüş R 15,6 içeri, topuk −0,4; ikinci adım 116 / 85 cm (değişmedi). map_r1 kaydırma 6 kare (üretim 0; eski aday 278), pop 10/57 üretimle aynı; tavan 36 ile map_r1 t≈20 s dik yokuş sprintinde (kapsül z 120→255/1 s, zemin önde 35–40 cm yükseliyor) kaldırma 33–36 (eskiden 25'te doyuyordu) — pop yok.
- ins5 (snap düzeltmesi): ilk adayda nokta doğrudan odağa (33, 315) → sonra Cerulean (33, 344); bakış ort. 6,0° (ins_ws2), 10,6° (ins_ws, yürüyüş dönüşü).
