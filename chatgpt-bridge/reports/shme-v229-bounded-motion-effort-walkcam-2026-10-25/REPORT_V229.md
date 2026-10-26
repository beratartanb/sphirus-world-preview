# SPHIRUS — SHME V2.29: ölçülü insan hareketi, efor ve destek sürekliliği, doğal yönlenme ve yürüyüş kamerası (2026-10-25)

Taban: V2.28 üretimi (bridge `510d32a`). Başlangıç durumu taze editörde doğrulandı (`verify_fin228` ALL_OK). Kontrol noktaları: `Saved/Codex/SHME_V229_20261025/checkpoint/pre_v229/` (iki ABP, BP_GR_Player, BP_PBI_Player, BP_GR_MotionProfile, bileşen, BP_SHM_ResponseProfile, üç DA, DSL kaynakları), `checkpoint/revturn/` (dört RevTurn klibinin düzeltme öncesi hali), `checkpoint/post_promo229/` (ilk terfiden sonraki ABP'ler + DA'lar, ikinci düzeltmeden önce). Her koşu etkin durum kaydıyla (`state/*_state.json`); "üretim" (`o`) = kaydedilmiş durum, bayraksız; aday = üretim + açık bayraklar. Sabit 30 FPS = gerçek hız (oyun saati), yavaş çekim yok.

## 0. Raporun başında istenen sorular

**1. Depar tersinde bozulma/kaybolmanın gerçek nedeni neydi, nasıl giderildi?**
İki ayrı kusur vardı.
- *"Animasyon ters dönüyor / bozuluyor"* (deparda kamera 180° çevrilip W basılı tutulduğunda): göğüs (spine_03) ile pelvis yönü arasındaki fark 6–10 karede tam tur dönüyordu (kare başına 93–159°). Yalnız RevTurn yolunda (s29_cam, s29_cam2, b_cam180, chain_sprint, jog j24_m180w) vardı, klavye S geri dönüşlerinde hiç yoktu. Sahibi **içerik**: V2.22'de `rb222_revturn.py` ile pişirilen `SHM216_RevTurn_R_Lfoot` (kare 29–33, 94–97) ve `R_Rfoot` (31–39). Pişirme betiğindeki "korunan burulma" terimi yaw(spine_05) − yaw(pelvis) farkını **±180'de sarmadan** 0,5 ile çarpıyordu; klibin göğüs ve pelvis yönleri ±180'in iki yanına düştüğünde 360° hata 180° spine_01 dönüşüne dönüştü. Kanıt: eski hesap önbellekteki kaynak anahtarlardan yeniden koşturulunca kliplerdeki anahtarları birebir verdi (fark 0,0°); sarılmış hesap (`rb229_revturn.py`) bütün dönme karelerini kaldırdı (bacak/kök/pelvis okuması 0,0 cm değişti). Sonuç (üretim): SPIN 0, burulma sıçraması ≤ 18°/kare, pop'lar 290–324 → 33 m/s²; j23_m180 292 → 30, j24_m180w 305 → 46.
- *Ters yönde kontrol kilidi* (son üretim kanıtında bulundu, V2.28'den beri var): depar W→S→W→S→W'de son W'ye basılıyken karakter **2 s boyunca geriye koşmaya devam ediyordu** (469 cm, 256 cm/s). Son W geldiğinde F_B klibi itiş fazındaydı; V2.28 "niyete karşı" güvenliği tutuşu bir kare öldürdü, fakat bu kilit yalnız bileşen bölümü kapalıyken sürüyordu; yeni W yeni bölüm açtı → bir sonraki karede tutuş aynı F_B klibine **eski aile veritabanıyla** yeniden kuruldu, giriş işareti −1'e yeniden mandallandı, itiş fren gibi okundu ve klip-bağlı kapsül geriye sürdü. Düzeltme `SHM229_PushCancel`: V2.28'deki iptal yolu (karşı aile veritabanına tek kesen arama) artık itiş fazında da çalışıyor. Sonuç: karşı aile klibine (B_F_P3) aynı karede geçiş, 0,37 s'de dönüş, 45 cm doğal fren; A/B'de diğer 21 senaryo birebir aynı.
- *Kaybolma*: sabit 30'da **yeniden üretilemedi** (NOT_REPRODUCED): görünür pelvis kapsülden ≤ 28 cm, kamera başa hiç 188 cm'den yakın değil, göğüs her karede ekranda (`screen229`: ekran dışı kare 0), görünürlük bayrakları (vvis/vrr) her karede açık. Görünen kusur tam tur gövde dönmesiydi. Gerçek zaman ve 20/60/120 FPS koşularındaki durum §5'te.

**2. Karakterin aşırı çevikliği hangi davranışla azaltıldı?**
Kısa süreli efor (`EffortE`): yatay ivmenin eşik üstü kısmı × hız payı (+ küçük sürekli depar terimi) ile birikiyor, istek yokken `EffortTauRec` 5 s ile toparlanıyor. Efor gecikmeli kopyası (`EffortEUse`, 1,2 s) ve istek anında mandallanan destek yükü (`EffortReqLoad`), `BP_GR_Player` içinde iki gerçek davranışı ölçekliyor: CMC azami ivmesi (`EffortAccScale`, yeniden hızlanma daha çok adım alıyor) ve fiziksel yönlendirme sürtünmesi (`EffortTurnScale`, yük altında dönüş daha geniş yay). Giriş gecikmesi, sabit bekleme, ağır çekim, rastgele tökezleme yok; yükü tuş sayısı veya kamera yaw'ı değil, gövdenin gerçek ivmesi üretiyor.

**3. Önceki efor ve tamamlanmamış destek yeni isteğe nasıl taşınıyor?**
Efor klipten bağımsız bileşen durumunda; klip değişince sıfırlanmıyor. Yeni yön isteğinde o anki destek yükü `EffortReqLoad` olarak mandallanıyor ve 0,6 s'de sönüyor; birikmiş efor gecikmeli kopyayla etkiliyor (manevra kendi kendini yavaşlatmıyor). Klip-bağlı kapsül (V2.28) klip pozdayken yer değiştirmenin tek sahibi; efor o karelerde kapsül hızına dokunmuyor (çift sahiplik yok, işaret/eksen tutarsızlığı yok). Ölçüm (son üretim, sabit 30, aynı giriş; efor kapalı → açık): dinlenmiş tek sert sol t60 0,47 → 0,53 s, eski yönde taşıma 164 → 184 cm; zincirde ikinci istek (geri) t60 0,40 → 0,57 s, taşıma 53 → 72 cm, destek adımı 2 → 10 (istekten bağlanana kadar); son geri dönüşte giriş hızı 290 → 168 cm/s (yeniden hızlanma daha çok adım); hızlı S-kesme zincirinde üçüncü kesme t60 0,43 → 0,63 s; 4,7 s dinlenmeden sonra aynı sert sol 0,60 s (dinlenmiş 0,53: toparlanma tam değil, §6).

**4. Küçük toparlama/hata hangi gerçek koşulda oluşuyor?**
Rastgele değil. Yük yüksekken (EffortEUse > ~0,5) ve yeni istek eski hareketin tersine düştüğünde: daha uzun fren, daha çok destek adımı (zincirde 2 → 3–4), daha geniş dönüş yayı. Düz yürüyüşte, ev içinde ve bakınırken efor hiç birikmiyor (e29_house E = 0,00). Yükte daha sık görülen gerçek bir hata kalıyor (açık): geri koşu 40–135 cm/s'ye düşünce W isteği yetkili geri dönüş rotasının hız eşiğinin (120) altında kalıyor, MM satıcının depar pivot klibinin kuyruğundan WalkToSprint'e geçiyor → baş ivmesi 88–119 m/s² (bkz. §6, efor kapalıyken de swl12'de 109).

**5. Girdi gecikmesi veya ağır çekim eklemeden ağırlık hissi sağlandı mı?**
Teknik olarak evet: isteği anlama karesi aynı (istek karesinde yeni hedef; t_rev değişmeyen yerlerde 0,23–0,77 s), değişen fren mesafesi, adım sayısı ve yeniden hızlanma süresi. Hissin kabulü kullanıcıya ait (NOT_ACCEPTED_YET).

**6. Genel geçişlerin hangi aileleri gerçekten iyileştirildi?**
(a) Kamera-180 RevTurn ailesi (içerik düzeltmesi), (b) tempolu geri dönüşte bırak–yeniden bas (`SHM229_ResumeWin` 0,2: aynı klip itişe devam ediyor, Jog_Bwd_Start_AAMS'e düşmüyor; j24_rel 33,9 → 11,1 cm), (c) depar geri dönüşünde itiş fazındaki ikinci istek (PushCancel). Değişmeyenler (ölçüldü): j24 ph0/ph3/sw/dbl kaymaları V2.28 ile aynı, pivot ailesi ad_ph0 26,8 → 24,5. İyileşmeyen: düşük hızlı geri koşu → depar pivot kuyruğu (§6).

**7. Çapraz hareketin kaynağı neydi; 16 yön gerekti mi?**
Yön referansı doğru: istenen yön her 22,5°'de seyahat yönüyle ≤ 1° hatayla eşleşiyor, sürekli kamera dönüşünde basamaklanma yok, analog büyüklük korunuyor (0,35/0,7/1,0 → 46/88/126 cm/s), dijital W+D 126 < W 132. Yürüyüş bakış güdümlü strafe (aktör = kamera yaw'ı), 8 klip yönü + OrientationWarping. Kayma sektör sınırlarında: −112,5° 14,1 cm, 85/95° 6,7, 22,5° 4–5 (klip açılarında 2–3). Kaynak içerik + blend sınırı; 16 yönlü yeni klip seti bu turda **yapılmadı** (yeni içerik gerektirir; arka çaprazda kazanç en çok −112,5°'de). Basit sürekli eşleme ön/yan yönler için yeterli.

**8. Yürüyüşte kadraj neden yapaydı, hangi değişiklik bunu düzeltti?**
İki sahip üst üste biniyordu: V2.23 takip yumuşak bölgesi (12/10 cm, dünya x/y'de saklanıyor) ve V2.1 yarım omuz değişimi (60 cm/s'den itibaren). A/D yürüyüşünde kamera–kapsül yanal sapması 28 cm ve 13 geri tepme. Değişiklik: omuz değişimi yalnız 230 cm/s üstünde, yürüyüş bölgesi 3/4 cm (jog/sprint değişmedi). Sonuç: A/D sapma 28 → 4,8 cm (göğüs x aralığı 0,32 → 0,16), yürürken fare 25 → 7,5 (0,20 → 0,07), çapraz 23 → 6,6, kombine dizi 19 → 5,7; yerinde bakınma doğrudan kaldı; jog bakınma 25,5 / 25,6 (değişmedi, tasarım). 2×2'de beden ve kamera ayrışıyor: kamera değişikliği gövde metriklerini değiştirmiyor (cn = o), efor kamera metriklerini değiştirmiyor (bn = o).

**9. Üretimde açık olanlar, kapalı adaylar ve kalan eksikler neler?**
Üretimde: RevTurn içerik düzeltmesi, efor (Gain 1,6, TurnK 0,5, AccK 0,5, LoadK 0,6, TauRec 5, ölçek tabanı `EffortScaleMin` 0,7), yürüyüş kadrajı (230 / 3 / 4), bırak-bas devamı (0,2), itiş fazı iptali (1). Kapalı aday: `RedirectEpisodeMinSpeed` 70/40 (`ems`, tutarsız → terfi edilmedi), efor tabanı 0,8 (`sm80`, 0,7'den belirgin farkı yok), daha güçlü efor (ef3, dinlenmiş manevrayı yavaşlattı). Kalan eksikler §6.

## 1. Depar ters dönüşü (öncelik 1)

### 1.1 İlk kötü kare ve sahip
Senaryolar (sabit 30): `s29_ws` (depar + S, Shift basılı), `s29_ws_ph` (farklı ayak evresi), `s29_cam` / `s29_cam2` (depar + kamera 180, W basılı), `s29_sa` / `s29_dg` (karşı çapraz), `s29_dbl` (dönüş bitmeden ikinci istek), `s29_rel` (Shift bırak–bas + geri), `b_s2back`, `b_cam180`, `chain_sprint`, `d_sprint`; ek olarak itiş fazı taraması `s29_swl08…20` (S 0,8–2,0 s sonra W), jog taraması `j29_swl10/14/20`, yük zinciri `e29_load` (W>S>W>S>W>A).

İlk kötü karede ölçülenler (`rev229.py`): girdi, kapsül hızı, aktör/kapsül, mesh–kapsül uzaklığı, kök/pelvis, göğüs–pelvis burulması, seçili klip/zaman/ağırlık, kamera–baş uzaklığı, görünürlük bayrakları. ActorForward × işaretli klip hızı (V2.28 bağı) ters dönüşlerde tutarlı (|v − tasarım| ≤ 5 cm/s), çift dönüş yok, ±180 yolunda yaw sıçraması ≤ 13,6°/kare (kapsül), yanlış aile/aynalı poz yok — tek sahip RevTurn klip içeriği (§0.1). Görünürlük/culling'e dokunulmadı, sınırlar büyütülmedi, kamera taşınmadı.

| Senaryo (sabit 30) | Önce (V2.28 üretimi, t1): SPIN / burulma sıçraması / en kötü pop | **Sonra (son üretim)** |
|---|---|---|
| s29_cam | 4 / 93° / 290 | **0 / 10° / 33** |
| s29_cam2 | 3 / 159° / 313 | **0 / 9° / 33** |
| b_cam180 | 3 / 150° / 303 | **0 / 11° / 38** |
| chain_sprint | 4 / 91° / 324 | **0 / 16° / 59** |
| j23_m180 / j24_m180w (jog) | 292 / 305 (V2.28) | **30 / 46** |
| s29_ws / s29_dbl / s29_rel / b_s2back | 0 spin; pop 33 / 81 / 33 / 29 | 0 spin; 33 / 33 / 33 / 29 |

### 1.2 Kontrol kilidi (itiş fazındaki ikinci istek)
`lock229.py`: tutulan ters istekte gövdenin isteği izlemeye başlama süresi (t_rev), isteğe karşı yol ve 0,3 s sonrası isteğe karşı hız.

| | t_rev | isteğe karşı yol | 0,3 s sonra karşı hız | seçilen klip |
|---|---|---|---|---|
| e29_load son W, V2.28 üretimi | **izlemedi (2,0 s, tuş bırakıldı)** | 469 cm | 256 cm/s | F_B P20/P11 ct 1,3–1,66 döngü |
| aday `pc` (aynı editör) / son üretim | **0,37 s** | 45 cm | 7 cm/s | B_F_P3 ct 0,063 → fren → ileri itiş |

A/B (`v229v229pc_*`, 22 senaryo × 2): yalnız e29_load değişti; j24 ph0/ph3/sw/rel/dbl/ad, s29 dbl/ws/cam, e29_chain, chain_sscut birebir aynı (kayma, pop, kilit). Son üretimde 19 ters-istek senaryosunda kilit 0, en kötü t_rev 0,83 s (chain_sprint, 490 cm/s'den frenleme).

### 1.3 Kaybolma
NOT_REPRODUCED (sabit 30, 20/60/120 FPS ve gerçek zaman koşularında, §5): ekran dışı göğüs karesi 0, görünür mesh kapsülden ≤ 28 cm, kamera–baş ≥ 188 cm (duvar yanında 76 cm: kamera çarpışması, beden görünür). Kullanıcının gördüğü "kaybolma" tam tur gövde dönmesinin hızlı kareleri olabilir; ayrıca gerçek zaman soğuk ilk koşuda 0,4 s duraklama sonrası 81,7° gövde sıçraması görüldü (§5, §6.7). İkisi de kaybolmanın kanıtlanmış nedeni değil.

### 1.4 Klavye S deparı
Shift basılı S: fren yüzü ileri, sonra geri koşu 300 cm/s (≤ jog) — tasarım; geri koşu depar hızında değil.

## 2. Efor ve çeviklik (öncelik 2–4)

### 2.1 Model (DSL `SHM_UpdateState`, profil alanları V229)
- Anlık yük: yatay ivmenin `EffortA0` 250 cm/s² üstü kısmı / `EffortA1` 500 × hız payı (hız > `EffortMinSpeed` 300) + depar terimi (`EffortSprintGain` 0,02 × (v − 380)).
- Birikim: `EffortE += dt·Gain·talep`, talep ~0 iken `EffortTauRec` 5 s ile toparlanma (tuş sayısı, kamera yaw'ı, yerinde bakınma yük üretmez).
- Kullanılan değer `EffortEUse` = E'nin 1,2 s alçak geçirgeni (manevra kendini yavaşlatmaz); istek yönü değiştiği karede `EffortReqLoad` mandallanır (dönüş miktarı ×), 0,6 s'de söner.
- Ölçekler → `BP_GR_Player`: `CalculateMaxAcceleration × EffortAccScale`, PhysicalRedirect sürtünmesi × `EffortTurnScale`; taban `EffortScaleMin` 0,7. Klip-bağlı kapsül karelerine dokunmaz (tek yer değiştirme sahibi).
- Etki: hareket planı (yeniden itiş, ek destek adımı, daha geniş yay, hıza dönmek için daha çok adım). Girdi gecikmesi, sabit kilit, ağır çekim, sürekli salınım, rastgele tökezleme veya ragdoll yok.

### 2.2 Davranış karşılaştırması (aynı giriş, sabit 30; efor kapalı = aynı üretim + `EffortEnabled` false)
| Olay | ölçü | efor kapalı | **efor açık (üretim)** |
|---|---|---|---|
| e29_rest: dinlenmiş depar + tek sert sol | t60 / eski yönde taşıma / adım | 0,47 s / 164 cm / 3 | 0,53 / 184 / 3 |
| e29_chain 1: sert sol (depar 490) | t60 / taşıma | 0,47 / 200 | 0,53 / 229 |
| e29_chain 2: hemen sağ (ters, 300 cm/s) | t60 / taşıma / adım | 0,40 / 53 / 2 | 0,57 / 72 / 10 |
| e29_chain 4: geri → ileri | giriş hızı / t60 | 290 / 0,27 | 168 / 0,30 |
| chain_sscut 3. kesme | t60 / taşıma | 0,43 / 121 | 0,63 / 205 |
| e29_recov: 3 depar geri dönüşü + 4,7 s dinlenme + sert sol | t60 | 0,47 | 0,60 (dinlenmiş 0,53) |
| e29_house (ev içi yürüyüş) | E en çok | — | 0,00 |
| ter_hill8_jog / legs_slope_sprint (eğim) | E / ölçek en az | — | 0,12 / 0,96; 0,61 / 0,78 |

Tek kesmede eforun etkisi sınırlı (dinlenmiş), birikmiş yükte belirgin (ikinci/üçüncü istek). Yük değeri her klipte sıfırlanmıyor ve takılı kalmıyor (dinlenmede düşüyor), ama 4,7 s'de tamamen dönmüyor (§6).

### 2.3 Efor tabanı neden 0,7
Taban 0,4'te ölçek 0,55'e iniyordu; kapsül yazılmış dönüş kliplerinin (RevTurn, SHM226) tasarım zamanlamasının gerisinde kaldı, klip bitince MM depar pivot kuyruğuna (`PSD_Dense_Stand_Sprint_Pivots`, ct 1,1) ve WalkToSprint'e geçti: chain_sprint baş ivmesi 69 → 150, e29_chain 56 → 88. Taban 0,7: chain_sprint 59, e29_chain 55, chain_sscut 44, d_sprint 31; davranış etkisinin çoğu korundu (yukarıdaki tablo). 0,8 belirgin fark getirmedi.

## 3. Geçişler ve karakter (öncelik 5)
- Bırak → yeniden bas (V2.28 açığı): `SHM229_ResumeWin` 0,2. j24_rel: basılı ayak kayması 33,9 → 11,1 cm, aynı klip itişe devam ediyor (ct 0,44 → 1,64), Jog_Bwd_Start_AAMS yok, duran kalkış yok.
- Yürüyüş kalkış kolları (V2.22 kalkışları) değiştirilmedi.
- Jog geri dönüş kayması (`plant225`/`plant227`, sabit 30, son üretim; V2.28 → V2.29): ph0 13,0 → 13,2 (temas başı 13,0 → 10,8), ph3 12,1 / 7,7 aynı, sw_ph0 5,8 → 5,6, sw_ph2 9,2 aynı, rel 33,9 → 11,1, **dbl 16,7 → 23,1 (temas başı 11,0 → 23,1: efor tabanı terfisinden sonra kötüleşti, açık)**, pivot ad_ph0 26,8 → 24,5.
- Kısa takılmalar: `e29_hitch` (istek anlarında 0,12/0,08/0,15 s gerçek duraklama) kilit 0, en kötü pop 55 (takılmasız zincirle aynı); `j29_hitch` (125 ms kareler) kayma 13,2 / 10,8 (takılmasız ph0 ile aynı), pop 0.
- Duvar yanında fren (`s29_wall`, sağda 31 cm boşluklu duvar): t_rev 0,77 s (açık alanla aynı), pop 33; duvar yanında duruş (`s29_wstop`) pop 33. Kamera duvar çarpışmasıyla başa 76 cm'ye kadar yaklaşıyor (beden görünür). Görsel değerlendirme: NOT_TESTED (yakalama alınmadı).
- İnceleme sırasında yürümeye başlama (`ins_ws`, `ins_ws2`): bakış hatası ort. 6,0°, en kötü pop 40/42 (V2.28 43/42).

## 4. Yönler (öncelik 6)
`a29_ang` / `a29_angb` (0…±180, 22,5° adım), `a29_edge` (sektör sınırları), `a29_mag` (analog büyüklük), `a29_kdg` (dijital çapraz), `a29_csweep` (sürekli kamera dönüşü), `dir229.py`. a29_ang/angb son üretimde yeniden koşuldu (V2.28 ile aynı); edge/mag/kdg/csweep V2.28 üretiminde (t1) ölçüldü — V2.29 yürüyüş yön yolunu değiştirmedi (yürüyüşte efor 0, kamera değişikliği gövde metriklerini değiştirmiyor):

| Açı | seyahat − istek | hız | klip | kayma (cm) |
|---|---|---|---|---|
| 0 / 45 / 90 / 135 / 180 | ≤ 1° | 117–132 | Fwd / FwdRight / Right / RearRight / Rear | 2–3 |
| 22,5 / 67,5 | ≤ 1° | 125–130 | blend | 4–5 |
| 85 / 95 | ≤ 1° | | blend sınırı | 6,7 |
| −112,5 | ≤ 1° | 117 | RearLeft | **14,1** |

Sürekli kamera dönüşünde basamaklanma yok (yön sürekli). Analog 0,35/0,7/1,0 → 46/88/126 cm/s; dijital W+D 126 < W 132. Sonuç: eşleme doğru, kalan kayma sektör sınırı içerik/blend kaynaklı; 16 yön kanıtlanmış ihtiyaç değil ön/yan için, arka çapraz (−112,5) için içerik açığı (bu turda yeni klip yapılmadı).

## 5. Doğrulama, üretime alma, kanıt

**Üretime alma (üç adım, her biri taze editör, kayıt + temiz yeniden açılış doğrulaması):**
1. 17:52 `promote229` {camera, effort, resume} → `VERIFY229` ALL_OK (RevTurn burulma sıçraması ≤ 15°).
2. 20:44 {pushcancel} (son kanıtta bulunan kilit) → ALL_OK.
3. 22:56 {effort: `EffortScaleMin` 0,7} → ALL_OK (`verify_fin229`: V2.28 üretim grupları + V2.29 bütün beklentiler + 4 RevTurn klibi).
Geri alma: `promote229.py {'rollback': True}` (kamera 60/12/10, efor kapalı, ResumeWin 0, PushCancel 0); RevTurn için `checkpoint/revturn/` (editör kapalıyken).

**Üretim kanıtı (taze editör, bayraksız, 66 senaryo + efor kapalı 5, `state/`):** hiçbir koşu `INVALID_STATE` değil (kaydedilmiş ayarlar koşu sırasında değişmedi).

**Üretim kanıtı özet tablosu (sabit 30; en kötü üst gövde ivmesi m/s², pop sayısı; V2.28 üretimi t1 → V2.29 son üretim):** s29_cam 290 → 33, s29_cam2 313 → 33, b_cam180 303 → 38, chain_sprint 324 → 59, s29_dbl 81 → 33, e29_chain 294 → 55, chain_sscut 41 → 44, s29_sa 35 → 44, s29_dg 45 → 63, e29_rest 61 → 56, e29_recov 62 → **110** (açık §6.1), e29_load (V2.28 t4/t5 33) → **110** (§6.1), j23_m180 292 → 30, j24_m180w 305 → 46; j24 ph0/ph3/sw_ph0/sw_ph2 0; ins_ws 43 → 40; arazi/harita V2.28 ile aynı (ter_drop_walk 260, ter_drop_jog 251, ter_step2 190, map_r1 58, map_r2 58). Yürüyüş kadrajı ve yönler §0.8 ve §4 ile aynı.

**FPS (aynı girdi zamanı, sabit adım 20 / 30 / 60 / 120):**

| Senaryo | ölçü | 20 | 30 | 60 | 120 |
|---|---|---|---|---|---|
| s29_cam | SPIN / burulma sıçraması °/kare / mesh yaw sıçraması | 0 / 15 / 19,7 | 0 / 10 / 13,5 | 0 / 5 / 6,4 | 0 / 3 / 3,2 |
| e29_chain | kilit / en kötü t_rev | 0 / 0,45 | 0 / 0,43 | 0 / 0,48 | 0 / 0,50 |
| e29_load | kilit / t_rev | 0 / 0,70 | 0 / 0,77 | 0 / 0,82 | 0 / 0,83 |
| s29_swl14 | kilit / t_rev | 0 / 0,70 | 0 / 0,77 | 0 / 0,80 | 0 / 0,82 |
| j24_ph0 | basılı ayak kayması cm | 15,2 | 13,2 | 5,8 | 13,0 |
| j24_sw_ph2 | kayma | 7,4 | 9,2 | 11,7 | 15,0 |
| j24_rel | kayma | 14,1 | 11,1 | 5,8 | 13,0 |
| j24_dbl | kayma / kilit | 35,4 / 0 | 23,1 / 0 | 18,2 / 0 | 13,8 / 0 |
| c29_ad | kamera–kapsül yanal aralık cm | 6,5 | 4,8 | 4,7 | 5,9 |
| c29_combo | yanal aralık | 6,8 | 5,7 | 6,7 | 8,2 |
| düşük hızlı pivot kuyruğu (e29_load) | fazla yer değiştirme cm | 6,4 | 5,0 | 1,5 | 0,7 |

İvme tabanlı pop ölçüsü örnekleme sıklığıyla büyüyor (120 FPS ısınma yürüyüşünde bile 56), bu yüzden FPS'ler arası karşılaştırmada kayma, kilit, burulma ve "fazla yer değiştirme" kullanıldı. 20 FPS'te `vrr` (son karede çizildi) bayrağı koşu boyunca, dururken bile (t 0,45 s) rastgele düşüyor; `vvis` her karede açık, mesh kapsülden ≤ 26 cm, kamera–baş ≥ 191 cm → ölçüm yapaylığı, kaybolma değil. j24_dbl 20 FPS'te 35,4 cm (açık §6.2).

**Değişken kare süresi ve takılmalar:** `e29_hitch` / `j29_hitch` (sabit 30 + istek anlarında 0,08–0,15 s gerçek duraklama, 125 ms kareler) §3'te: kilit 0, kayma takılmasız koşuyla aynı.

**Gerçek zaman (sabit adım yok; soğuk ilk koşu `s29_cam`, sonra ısınmış):**

| Senaryo | kare/s | sonuç |
|---|---|---|
| s29_cam (soğuk) | 22 (dt 23–125 ms) | SPIN 0, burulma sıçraması 19°; **6,06–6,46 s arasında 0,4 s kayıt boşluğu (soğuk başlatma duraklaması): kapsül yaw'ı 81,7° ilerledi, RevTurn klip saati yalnız 0,06 s** → duraklamadan sonra görünür sıçrama (§6.7) |
| e29_chain | 32 | kilit 0, t_rev 0,47 |
| e29_load | 32 | kilit 0, t_rev 0,79, en kötü pop 130 (düşük hızlı pivot kuyruğu) |
| s29_swl14 | 29 | kilit 0, t_rev 0,77 |
| c29_wlook | 29 | yanal aralık 8,1 cm (sabit 30: 7,5) |
| j24_rel / j24_sw_ph2 | 28 / 25 | kayma 15,3 / 8,2 |
| map_r2 | 24 | en kötü pop 48 (sabit 30: 58) |

**Aynı girdi zamanı ile aynı fiziksel giriş durumu:** yukarıdaki FPS tablosu aynı girdi zamanını kullanır; FPS'e göre girdi gecikmesi değiştiği için giriş anındaki ayak evresi ve hız farklı olabilir (V2.28 bulgusu). Aynı fiziksel giriş durumu (aynı hız + ayak evresi) için `j24_ph0/ph3/sw_ph0/sw_ph2` evre senaryoları sabit 30'da ayrı tutuldu (§3); FPS başına evre eşleştirmeli deney bu turda yapılmadı (NOT_TESTED).

**Beden/kamera 2×2 (sabit 30, terfiden önce aynı editörde; `pre_*`):**

| | c29_combo yanal aralık (kamera) | e29_chain 2. istek t60 / taşıma (beden) |
|---|---|---|
| referans beden + referans kamera (o) | 19,3 cm | 0,40 s / 53 cm |
| yeni beden + referans kamera (bn) | 19,3 | 0,67 / 80 |
| referans beden + yeni kamera (cn) | 5,7 | 0,40 / 53 |
| son birleşim (fin) | 5,7 | 0,67 / 80 |

(2×2 efor tabanı 0,4 iken alındı; son üretimde (taban 0,7) beden değeri 0,57 s / 72 cm.) Efor açık/kapalı karşılaştırması §2.2'de. 2×2 telemetriyle verildi; görüntüde yalnız referans ve son birleşim var (ara iki kombinasyon için yakalama alınmadı: NOT_TESTED görsel).

**Yakalamalar (`vid/`, sabit 30 = gerçek hız, tam kare, kesintisiz, yavaş çekim yok):** referans (`ref` = V2.28 davranışı + RevTurn düzeltmesi, bayraklarla: efor kapalı, eski yürüyüş kamerası, ResumeWin/PushCancel 0) ve son üretim, aynı editörde (`cap4`):
- `sprint_WSWSW_ref_side` / `sprint_WSWSW_v229_side` / `_game`: depar W>S>W>S>W — referansta son W'de 2 s geri koşu (kilit, 382 cm), üretimde 0,37 s'de dönüş.
- `effort_chain_ref_side` / `effort_chain_v229_side` / `_game`: depar → sert sol → sağ → geri → ileri (efor yok / var).
- `effort_rest_ref_side` / `effort_rest_v229_side`: dinlenmiş tek sert sol.
- `walkcam_combo_ref_game` / `walkcam_combo_v229_game` / `_v229_side`: idle → ilk adım → ileri/çapraz → A/D → yalnız kamera dönüşü → dur.
- `jogrev_release_ref_side` / `jogrev_release_v229_side`: tempolu geri dönüşte bırak–bas.
- `sprint_cam180_v229_side` / `_game`, `sprint_cam180b_v229_game`: depar + kamera 180 (RevTurn düzeltmesi sonrası; düzeltme öncesi içerik bayrakla geri getirilemediği için "önce" görüntüsü yok — veri §1.1).
Her biri GIF (önizleme, 0,38 ölçek) + `_realtime.avi` (tam kare, 30 fps). Yakalama notu: ilk V2.29 yakalama turları editör penceresi ekranı kapladığı için boş çıktı (`SHM_MCAP refused`), `qa_pie.fit_window` düzeltildi ve hepsi yeniden alındı.


## 6. Açık liste
1. **Düşük hızlı geri koşu → W (depar basılı):** hız < `RedirectEpisodeMinSpeed` 120 iken yetkili rota devreye girmiyor; satıcı depar pivot kuyruğu → WalkToSprint, baş ivmesi 88–119 m/s² (e29_load/e29_recov 110, s29_swl12 119, swl14 110, swl16 90). Efor bu hız bandını sıklaştırıyor (e29_load efor kapalı 60), ama efor kapalıyken de var (swl12 109). Eşik 70/40 tutarlı çözmedi. Doğru çözüm: düşük hızlı B_F/F_B girişleri (içerik) veya bu bant için ayrı rota.
2. **j24_dbl** efor tabanı terfisinden sonra 16,1 → 23,1 cm (temas başı 10,9 → 23,1). Sahibi ölçülmedi.
3. Efor toparlanması 4,7 s'de tam değil (t60 0,60 vs 0,53); `EffortTauRec` ayarı açık.
4. Arka çapraz −112,5° kayma 14,1 cm (içerik).
5. Eğimde depar + kamera 180 (`legs_slope_sprint`) baş pop 175 — V2.29 öncesinde de 174 (mevcut).
6. Arazi düşüşleri (ter_drop_walk/jog 260/251, ter_step2 190) V2.28 ile aynı (mevcut).
7. Kaybolma sabit adımda yeniden üretilemedi. Gerçek zamanda soğuk başlatma duraklamasında (0,4 s) kapsül yaw'ı RevTurn klibinden 81,7° önde kaldı ve duraklama sonrası görünür sıçrama oluştu: kullanıcının gördüğü "kaybolma/bozulma" ile ilişkili olabilir, sahibi (anim tick'in duraklamada ilerlememesi mi, kayıt boşluğu mu) bu turda ayrılmadı.
8. Referans (Resident Evil Requiem, Grace): izlenen bölümlerde depar geri dönüşü/koşudan duruş yok (`reference_watch229.md`); hedefler stil olarak kullanıldı, sayı türetilmedi.
9. Görsel ve oyun hissi kabulü kullanıcıya ait (NOT_ACCEPTED_YET). Teknik geçiş ≠ his kabulü.

## 7. Etiketler
- WRONG_PATH: yok (her ölçülen senaryo amaçlanan rotayı tetikledi; e29_load son W V2.28'de WRONG_PATH idi — eski aile DB'si — düzeltildi).
- NOT_TRIGGERED: `s29_wstop` kilit denetimi (ters istek yok, olay 0 — "0 hata" sayılmadı); `c29_look` yerinde bakınmada çeviklik olayı yok.
- NOT_TESTED: duvar yanında fren görseli; gamepad girdisi (yalnız enjekte klavye/analog); paketlenmiş yapı; 16 yön içeriği.
- NOT_REPRODUCED: depar ters dönüşünde kaybolma.

## 8. Dosyalar
- `code/`: araçlar (`rev229`, `twist229`, `screen229`, `cam229`, `agil229`, `lock229`, `dir229`, `cmp229`, `rb229_revturn`, kurulumlar `install_v229_effort/resume/pushcancel`, `promote229`, `verify_fin229`, `media229.sh`), zincirler (`run229_*.sh`), varyantlar (`vars229*.sh`), DSL/harness farkları (`shm_src_v229.diff`, `shm_profiles_v229.diff`, `shm_component_vars_v229.diff`, `v212_run_v229.diff`, `qa_pie_v229.diff`).
- `data/`: `chain.out` (bütün koşuların özet satırları), terfi/doğrulama çıktıları, RevTurn pişirme kanıtları (`rb229_*.json`), tablolar.
- `state/`: her kanıt koşusunun etkin durum kaydı (DB'ler, efor, rota, kamera ayarları).
- `vid/`: tam kare, sabit 30 = gerçek hız, kesintisiz yakalamalar (yan + oyun kamerası). Ücretli ham animasyon ve özel dosya yok.

