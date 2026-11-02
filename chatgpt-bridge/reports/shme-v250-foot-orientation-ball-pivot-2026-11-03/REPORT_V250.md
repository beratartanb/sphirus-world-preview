# SHME V2.50 — dönüşlü kalkışta ayak: batmanın kesin sahibi, ayak yönü onarımı, ilk adımda top pivotu (2026-11-03)

Taban: V2.49 üretimi. Ham puanlar `data/score_final.md`, değişiklikler `CHANGES_V250.md`.
Videolar (60 fps, gerçek hız; ikisinde de aynı kırpma seçildi): `vid/turn135_diag_realtime_part1.avi` ve `vid/turn135_gamecam_realtime_part1.avi` (solda V2.49, sağda V2.50). Ayrıca `vid/turn180_side_diag_realtime_part1.avi` (yalnız V2.50; klipler değiştiği için "önce" kaydı yok).
**Videoları oynatıp izleyemiyorum**; tek tek kareleri inceledim. Oyun hissi NOT_TESTED.

## 1. Kesin kök neden (kare kare, katman katman)
1. **Katman izolasyonu.** Görünen MetaHuman iskeleti (vb) ile mannequin pozu (mx) aynı: retarget sahip değil. Stride warping kapalıyken (135°) ve orientation warping kapalıyken (180°) batma birebir aynı. FootPlacement (V2.49), inertialization, aynalama (şemada mirror tablosu yok), kök eğimi ve sıkıştırma (ham = sıkıştırılmış) da elendi.
2. **Çevrimdışı kanıt** (`probe250_blendfk.py`). Idle örneğinden kırpmanın ilk karesine eklem rotasyonları tek tek harmanlandığında top −7,6 cm'e iniyor, ayak 74° bükülüyor (oyunda −9 cm / ~76°). Sebep, kırpmada ayak kemiğinin yerel rotasyonunun idle'dan 110–116° farklı olması; baldır ve uyluk yalnız 1–19° farklı.
3. **Bu farkın sahibi içerik** (`probe250_footaxes.py`). `CoreMotionAAMS/Candidate` jog kalkışları aynı Core Motion kliplerinin **bozuk bir retarget'ı**: ayak aşağı-geri bakıyor (bileşen uzayında −68/−101°, 83° eğim, top zeminin 8 cm altında). Aynı klipler `/Game/CoreMotion_Retargeted/AAMS/Walk/` altında, aynı iskelette ve kare kare aynı zamanlamada **doğru**: ayak ileri (74/110°), 24° eğim, top zeminde.
4. **V2.49 onarımı durumu kötüleştirmişti.** Neredeyse dik ayağı cross(bilek→top, Z) ekseni etrafında kaldırırken eksen belirsizdi; ayak geriye döndü. Kırpma boyunca görülen "sivri/bale ayak" buydu.

## 2. Üretime alınanlar (yeni klip üretilmedi; mevcut doğru kaynak kullanıldı)
- **Ayak yönü onarımı** (`fix250_footorient.py`): 6 dönüş kırpması ve Candidate'tan türeyen 16 üretim kopyası (düz/geri/sol/sağ kalkış, 45/90/135/180 dönüşlü kalkış). Her karede ayağın bileşen yönü doğru retarget'tan alındı ve kırpmanın kendi baldırına göre yeniden yazıldı. Bilek konumları değişmedi. Giriş karesinde ayak idle'a 12–14° yakın (önce 110–116°).
- **İlk adımda top pivotu (yeni fiziksel davranış)** (`fix250_ballpin.py`). Dönüşlü kalkışın ilk temas fazında, ayak kalkmadan önce topu zeminde 1,4–6,3 cm kayıyordu (kaynakta yazılı). Artık top ilk karedeki noktasında sabit; ayak kendi yönünü koruyor, topuk top etrafında dönüyor, sonra ayak temiz kalkıyor. Bacak diz menteşesi korunarak IK ile çözüldü, kalkıştan sonra 6 karede yumuşak çıkış var. Uygulanan ayaklar: 90° ve 135° sol (iki ayak), 180° sağ (sağ ayak). Diğer ayaklarda diz ekseni kare-kare sıçraması kaynağa göre 3°'den fazla arttığı için uygulanmadı.

## 3. Sonuç
Ölçüm `contact250.py`, görünen iskelet üzerinde, her ayak için ayrı: PEN = zemine batma, PLANT = basılı noktanın ötelemesi (topuk/top pivotu kayma sayılmaz), BALL = topun zeminde kayması.

| 135° kalkış girişi (60 FPS) | V2.49 | V2.50 |
|---|---|---|
| zemine batma (sol/sağ) | 6,3 / 5,8 cm | yok / 1,7 cm |
| basılı nokta ötelemesi | 3,0 / 3,5 cm | 2,4 / 4,2 cm |
| top kayması | 6,3 / 6,4 cm | 3,1 / 4,2 cm |
| contact231 (V2.48/49 raporlarındaki ölçüm) | 17,5–29,3 cm | 11,0 cm |

| 180° kalkış girişi | V2.49 | V2.50 |
|---|---|---|
| batma, 20/60/120 FPS | 4,7–6,7 cm | yok |
| top kayması, 60 FPS | 12,2 / 12,7 cm | 0 / 4,1 cm |
| contact231, 60 / 120 FPS | 23,8 / 21,7 cm | 0 / 0 cm |

- **Gerçek zaman (5 koşu).** 135° ve 180° seçilen koşularda batma yok. Basılı nokta 0,3–5,9 cm, top 1,0–6,1 cm. Üç koşuda bakış açısı yüzünden yanal kalkış seçildi (beklenen davranış; batma 0,6–1,3 cm).
- **20 FPS.** 135°'de batma ≤1,8 cm, top 3,2/6,0 cm.
- **Aynı klip ailesindeki yan kazanç.** jstart (30 FPS) basılı nokta 31/29 → 8,5/7,6 cm, top 50 → 15 cm, contact231 63,8 → 34,3 cm (45° ve geri kalkış kopyaları).
- **Görsel kontrol (kareler).** V2.49'da girişte sol ayak ucu zemine dikiliyor ve dönüş boyunca iki ayak sivri. V2.50'de iki ayak düz basıyor ve doğal adım duruşunda.
- **Regresyonlar.** j42_lr_p10'da (30 FPS) MM artık başka bir yanal klip seçiyor: contact231 12,5 → 17,3 cm, batma aynı. Diğer senaryolar (gait, taps, wstart, w42, w43, j40, j41, j45_sl) V2.49 ile aynı aralıkta.

## 4. Açık kalanlar
- **60 FPS sıçraması.** 180° kırpma bitmeden dönüş tamamlanınca normal kalkışa geçişte bir kare omuz 77 m/s² (1,6 cm fazla yer değiştirme). Ayak onarımıyla ilgili değil; V2.49'da 69'du. Çözülmedi.
- **Kalan batmalar başka klip ailelerinde.** 45° kalkış girişi 4,3 cm, LS yanal kalkış 4–5 cm, RevTurn 6 cm. V2.49'da da vardı.
- **Kapsül izleme hatası.** Dönüş ortasında ≤3,5 cm; 180°'de sabitlenen sağ ayakta oyunda 4 cm olarak görünüyor.

## 5. Ağırlıklı idle — üretime alınmadı
Ayak onarımı sonrası yeniden test edildi (30/60 FPS).
- **İyileşenler.** wstart (30 FPS) 21,0 → 16,7 cm, taps (60 FPS) 18,8 → 13,1 cm.
- **Kötüleşenler.** w42_id 10,2 → 19,7 cm ve gait 6,8 → 14,7 cm. wstart 60 FPS'de 23,5 → 27,7 cm.
- **Sahipler.** w42'de ağırlıklı idle sırasında gövde ayakta 85° dönüyor ve basılı sol ayak 2,4 s boyunca 11,7 cm kayıyor; ayakta dönüş ağırlıklı idle ile uyumlu değil. gait'te ağırlıklı idle pozundan yürüyüş kalkışında sağ ayak 9,5 cm kayıyor.

Kural gereği regresyon yaratan sistem üretime alınmadı.

## 6. Disk saklama
`Tools/Retention/retention.py` korunuyor (varsayılan kuru çalıştırma). Bu tur eklenen koruma: medya geçici klasörleri ancak 6 saatten eskiyse budanıyor (çalışan video üretimini silmemek için). Son durum kapanışta ölçüldü (CHANGES).
