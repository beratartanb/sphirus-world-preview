# Hareket ve kamera testleri (ölçüm; düzeltme yapılmadı)

## Yöntem
- **Girdi:** Enhanced Input `Input.+action` konsol enjeksiyonu kullanıldı: `IA_Move`, `IA_Look`, `IA_Jump`, `IA_Ranger_GaitShift`. Fare dönüşü, açık döngü IA_Look ile verildi (kazanç 0.5 °/birim). Gait davranışı README_TR'ye göre: kısa basış koşu açar/kapar, basılı tutmak sprint yapar.
- **Diziler:** `Tools/HardwareQualityBaseline_20261013/motion_suite.py` dosyasında. Her test aynı başlangıç noktasından ve yönden başlar, 2.5 s oturma süresi vardır.
- **Ortamlar ve gerçekleşen kare hızı** (tick dt ile ölçüldü; FPS sınırı ile karıştırılmadı):

| Etiket | Ortam | Gerçekleşen FPS | Not |
|---|---|---|---|
| `lab_D_native` | Hafif ortam (L_GR_MovementLab) | 58.3–60.0 | PIE dünyası max tick rate 60 |
| `lab_D_fps30` | Hafif ortam + t.MaxFPS 30 | 29.9–30.0 | Gerçekten 30 FPS (dt ort. 33.3 ms) |
| `house_motion_A` | Ev arka bahçesi (1150,-520), A | 47.1–53.6 | Yük altında |
| `house_motion_C` | Aynı nokta, C | 27.2–32.9 | Ağır yük; dt p99 37–51 ms |

- **Telemetri:** Her tick'te konum, hız, aktör/kontrol yaw'u ve kamera kaydedildi. Ayrıca gizli AAMS sürücü iskeletinin (`CharacterMesh0`) ve görünen MetaHuman gövdesinin (`Manny`) soketleri alındı.
- Görünen gövde ölçümleri `*_v2` oturumlarındadır. Ayak kayması değerleri iki iskelette ±%10 içinde benzer.
- Ham veriler `raw/pie_*.json`, özet tablolar `raw/motion_table.json` ve `raw/motion_analysis.json` dosyalarında.

## Bulgular (her biri: tetikleyici · ortam · kanıt · sınıf)

| # | Konu | Ölçüm | Ortamlar | Sınıf |
|---|---|---|---|---|
| H1 | **Yerinde fare dönüşü → üst gövde öne bükülmesi** | M1, IA_Look 90°/s (4 s), -180°/s (2 s), 360°/s (1 s). Gövde kamerayı hemen izlemiyor; kamera ~130–170° sapınca yerinde dönüş montajı (`AnimMontage_*`) aktör yaw'unu toplu döndürüyor. Bu sırada üst omurga (spine_03→spine_05) öne bükülmesi -9…-12°'den +8.4…+8.7°'ye çıkıyor (≈17–20° öne). Baş, pelvise göre 1.6 cm alçalıyor. Ayaklar 40–45 cm yer değiştiriyor | Hafif 60 FPS, hafif 30 FPS, ev A, ev C: **dört ortamda aynı aralık** | **Hafif ortamda da mevcut** (yük veya kare hızına bağlı değil). Sanatsal hissi kullanıcı değerlendirir. Klip `clips/house_A_M1_idle_mouse_turn.gif`, `clips/lab_M1_idle_mouse_turn.gif` |
| H2 | Kısa yürüyüşün ilk/son adımı | M2, 0.6 s ve 1.5 s basış. İlk hareket 0.05–0.07 s'de başlıyor, tepe hız 132 cm/s. Bırakınca 0.43–0.47 s'de duruyor. Yol 72–75 cm / 193–195 cm | 4 ortamda ±0.04 s | Yükten bağımsız. Hissel değerlendirme klipte; PASS/FAIL hükmü kullanıcıda |
| H3 | Walk / tempo / sprint ayrımı | M3: walk 132, tempo (kısa basış) 245, sprint (basılı) 490 cm/s; ev C'de sprint ortalaması 463 (eğim/engel) | 4 ortam | **Ayrım ölçülebilir ve tutarlı** (teknik PASS) |
| H4 | 45°/90°/180° dönüşte frenleme | M4 (tempo): 45°'de hız 300 → 287; 90°'de 287 → 212–219; 180°'de hız ~0'a iniyor (1–5 cm/s). Gövde yan eğimi (roll) 45/90°'de -2.8…+3.8°; 180°'de 30 FPS'te -13.8°, evde C'de -13.5° görüldü (60 FPS'te -4.2°) | 4 ortam | 180°'deki roll farkı **kare hızına duyarlı olabilir** (30 FPS ve C'de büyük); tek örnek, **kanıt yetersiz** |
| H5 | İleri–geri zıt yön | M5: her terste hız 0–5 cm/s'ye iniyor; 0.29–0.40 s'de dip, sonra 245/300 | 4 ortam ±0.02 s | Yükten bağımsız |
| H6 | **Sprintte W + art arda sağ–sol → donma** | M6: ±45° girişler 0.3 s arayla 10 kez. Hafif ortamda hız 422–490 arası, düşük hız bölümü yok (donma **yok**). Evde 3.49 s'de hız 490 → 0 düşüyor ve 1.2 s geriye itilme montajı oynuyor. Kapsül izi `AD_Life_GatePostN` aktörüne (bahçe kapı direği) çarpma olduğunu gösteriyor | Hafif ortamda yok; ev A ve C'de var | **Girdi donması değil; çarpışma + tepki montajı.** Rota/çarpışma tasarımı konusu. Klip `clips/house_A_M6_sprint_zigzag.gif` (kamera bu sırada çalıyı da delip geçiyor), `clips/lab_M6_sprint_zigzag.gif` |
| H7 | Sürekli çapraz harekette ikinci launch / yanlış eğilme | M7 (walk 45°) ve M8 (tempo -45°): ilk 2.5 s'de **yeniden fırlama (dipten sonra yeniden hızlanma) = 0**. Sabit hız 126 / 287. Ortalama roll -0.3…0.0°, aralık ±3.6° | 4 ortam | **Bu testte gözlenmedi.** Kullanıcının bildirdiği durum farklı bir giriş zamanlaması gerektiriyor olabilir: **kanıt yetersiz** |
| H8 | Ayak kayması (yerde sayılan ayağın yatay hızı) | Düz zeminde walk 11–16 cm/s; tempo/dönüş 29–51; sprint zikzak 86–110. Evde eğim ve engel varken bazı testlerde 150–225 cm/s, ama "yerde" sayılan süre çok kısa (0.14–0.8 s) | Hafif ortamda da mevcut | Ölçüt yaklaşıktır (ayak topu z ≤ yerel min + 2 cm). Evdeki yüksek değerler eğim ve çarpışma etkisi olabilir; görsel doğrulama klipte |
| H9 | Yerinde zıplama vs ileri atlayış | M9: yerinde havada 0.56–0.60 s, pelvis +67…+76 cm; ileri (yürürken) havada 0.53–0.55 s, pelvis +62…+66 cm, toplam yatay 233–236 cm | 4 ortam | Yükten bağımsız. Yerinde zıplamanın pelvis yükselişi ileri atlayıştan büyük; hissel değerlendirme kullanıcıda |

## Kamera
| Ölçüm | Değer | Not |
|---|---|---|
| Spring arm hedef boyu | 300 cm, iç ve dış aynı | Bu, telemetrideki `arm_len` değeri |
| Gerçek kamera–pelvis mesafesi, ev içi (R1 0.5–3 s) | 86–155 cm | Çarpışma ile kısalıyor |
| Kapı/veranda geçişi (R1 3–7.5 s) | 85 → 195 cm, en hızlı değişim 182 cm/s | Yumuşak açılma, tek karede sıçrama yok |
| İniş ve kıyı (R1 7.5–32 s) | 197–236 cm, en hızlı değişim 90 cm/s | Kararlı |
| Ev yanı → arka bahçe → yokuş (R2) | 104–237 cm, en hızlı değişim 847 cm/s | Ağaç ve dar geçişlerde kısa ani yaklaşmalar |
| Hafif ortam koridoru (160 cm genişlik) | 236 → 157 cm, en hızlı değişim 165–173 cm/s | Yumuşak |
| Duvara yürüme (L1b) | 164 → 82 cm, en hızlı değişim 518 cm/s | Duvara yaklaşırken hızlı ama sürekli |
| Duvar önünde sağa/sola bakış (L1c) | 100–160 cm, en hızlı değişim 240 cm/s | |
| Merdiven çıkışı (16 cm basamak) | Sıçrama yok; kamera–pelvis yükseklik farkı 68–122 cm | Merdiven sonundaki 1.6 m düşüşte inişte tek karede 175 → 103 cm (arkadaki blok) |
| Rampa (tempo) | Rampa sonundaki düşüşte tek karede 218 → 157 cm | Test geometrisine özgü düşüş |
| Karakter görünürlüğü | Kamera→baş görüş izi engellenme oranı 0.0 | **Ölçüt yetersiz:** çarpışmasız bitki izi engellemiyor. M6 klibinde kamera çalı içinden geçiyor ve karakter yapraklarla örtülüyor (`images` / `clips/house_A_M6_sprint_zigzag.gif`) |

**Ev içi merdiven, alçak tavan ve tavan arası merdiveni test edilmedi (NOT_TESTED):** yalnız hafif ortamın merdiveni ölçüldü.

## Kare hızı karşılaştırması (sonuç)
- H1–H3, H5, H7 ve H9 sonuçları 30, 47–54 ve 60 FPS'te aynı (±0.04 s, ±1 cm/s). Bu sorunlar **donanımdan bağımsız**: yeni bilgisayarda aynı davranış beklenir, ancak orada yeniden ölçülmelidir.
- H4'teki 180° roll farkı ve H8'deki kayma değerleri düşük kare hızında farklılaşabilir; **kanıt yetersiz**. Daha fazla tekrar gerekir.
- **Ağır çekim kullanılmadı.** Klipler gerçek zamanlı ve 30 FPS sınırlı; performans ölçümünden ayrı bir geçişte alındı.
