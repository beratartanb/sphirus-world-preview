# SPHIRUS — SHME V2.30: düşük hızlı geri dönüş yolu, depar/ivmelenme salınımı, oynatma hızı, geçiş sürekliliği ve geliştirme verimliliği (2026-10-26)

Taban: V2.29 üretimi (bridge `f971e94`). Temizlikten sonra başlangıç durumu taze editörde doğrulandı (`verify_fin229` ALL_OK; 6 607 paket tarandı, 46 eksik referans = kurulu olmayan satıcı demo içeriği, önceden de vardı). Kontrol noktaları: `Saved/Codex/SHME_V230_20261026/checkpoint/pre_v230/` (iki ABP, BP_GR_Player ×2, BP_PBI_Player, DA_PBI_Prototype, BP_GR_MotionProfile, DA_GR_LocomotionBehavior, bileşen, yanıt profili, DA_SHM, V2.26 + V2.16 animasyon klasörleri, araç kaynakları), `checkpoint/pre_reauthor/` (yeniden yazılan 22 klibin özgün hali), `checkpoint/pre_loadedDB/` (4 arka döngü). Ölçüm: sabit 30 FPS adım (aynı girdi zamanı) + gerçek zaman ve 20/60/120 FPS; tüm sayılar `pub/data` altındaki tablolardan.

Sınıflar: **PASS** (kaynak → üretim → görünür doğrulama), **PARTIAL** (ölçülü iyileşme, kalan kusur açık yazılı), **OPEN** (sahip bulundu, çözülmedi), **NOT_REPRODUCED**, **NOT_TRIGGERED**, **WRONG_PATH**. Görsel/oyun hissi kabulü kullanıcıya ait: hiçbir madde "kullanıcı kabulü" sayılmadı.

## 0. Raporun başında istenen sorular

**1. Hangi eski hatalar düzeldi?**
- **Düşük hızlı geri koşudan ileri isteği → satıcı depar pivot kuyruğu + WalkToSprint baş pop'u** (V2.29 §6.1 açık): sahibi bulundu ve üretimde giderildi (§2). Aynı içerikte yol kapalı/açık karşılaştırması: s29_swl14 **112 → 34**, j30_slow **28 → 0** m/s² (yakalama koşuları); üretim kanıtında s29_swl12/14/16 **119/110/90 → 32/32/32**, e29_load **110 → 61**, e29_recov **110 → 54**.
- **Ağır çekim aileleri** (V2.29 E): yürüyüş arka/arka çapraz 0,72–0,75 → **0,98–1,00**, tempolu yan 0,82 → **1,00**, depar döngüsü 0,82 → **0,98**, depar eğri R25 0,64 → 0,82 oynatma hızı (§3.2).
- **j24_dbl V2.29 gerilemesi** (16,7 → 23,1 cm): V2.30'un dört ayrı oturumunda (üretim dahil) **16,1 cm**; V2.29'daki 23,1 oturuma bağlı seçim eşitliğiydi, kalıcı gerileme değil (§6 A).
- **Bırak–yeniden bas (iptal) akışında boşta girişi yarışı** (V2.29 bırak-devam düzeltmesini bazı koşularda boşa çıkarıyordu): tutulan geri dönüş içinde boşta girişi engellendi; yarışın tetiklendiği bırakmalarda aile kayması 28–33 → 13,2 cm (§2.5).
- **Soğuk başlatma "81,7° kapsül önde" bulgusu**: ölçüm hatası çıktı (kayıt bir kare geç), §5.

**2. Hangi hareketler yeniden tasarlandı veya üretildi?**
Klip içeriği yerinde yeniden yazıldı (iskelet oranı, anatomi değişmedi): depar döngüsü `A_LB_Sprint_Fwd`, 6 depar eğrisi, 4 tempoludan depara (`SHM217_J2S_*`), 4 yürüyüşten depara (`SHM218_W2S_*`) geçişi, 3 yürüyüş arka/arka çapraz döngüsü, 2 tempolu yan döngü. Yöntem: aynı kadansta adım uzunluğu ölçekleme (oynatma hızı ≈ 1), pelvis / göğüs / baş / kol yanal salınımının zayıflatılması, bacakların yeniden çözülmesi (`solve_leg` + leg_guard), IK ayak eşlemesi (§3). Ayrıca **yük altında geri dönüş ailesi** (53 faz klibi, `SHM230L_JogRev_*`) üretildi; kapalı aday kaldı (§4).

**3. Eforun yeni bedensel karşılığı ne?**
Üretimde değişmedi: V2.29 eforu (fren mesafesi, ek destek adımı, ölçülü yeniden itiş) olduğu gibi çalışıyor; klip değişince sıfırlanmıyor (bileşen durumu). Bu sürümde efora **bedensel** karşılık olarak yük altında ayrı geri dönüş ailesi denendi (EffortEUse ≥ 0,45'te `PSD_SHM230L_*`): yükte seçildi, fakat görünür fayda ölçülemedi ve yeni bir geçiş boşluğu açtı → **üretime alınmadı** (`SHM230_LoadedOn` 0). Dinlenme sonrası toparlanma (`EffortTauRec` 5 s) değişmedi; e29_rest V2.29 56 → 54.

**4. Baş/kol/gövde neden arcade görünüyordu?**
Kaynak zinciri katman katman ayrıldı (klip → MM → retarget → harmanlama → efor/beden → son poz). Çalışma zamanı katmanlarının hiçbiri sorumlu değil: PBI kapalı, omurga karşı dönüşü kapalı, eğri eğilimi kapalı, yönelim bükmesi kapalı, ham poz (FootPlacement/LegIK/Stride/Orientation kapalı), settle/terrain kapalı → baş–pelvis yanal salınım farkı ≤ 1 cm. **Sahip içerikti**: depar ve geçiş kliplerinde baş dünya düzleminde 32 cm yanal savruluyor, omuz hattı 36° yuvarlanıyordu; üstüne satıcı döngüleri büyük adımlarını 0,72–0,82 hızla oynatıyordu (ağır çekim ritmi). İkisi birlikte "sarsak + yavaş" arcade okuması verdi. Düzeltme içerikte (§3).

**5. Ters/uyumsuz poz zorlaması kaldırıldı mı?**
Kısmen. Düşük hızda satıcı depar pivot kuyruğu (ters yöne bakan duruştan WalkToSprint'e zorlama) kaldırıldı. RevTurn ±180 sarma düzeltmesi korunuyor (`verify` RevTurn burulma sıçraması ≤ 30°/kare, SPIN 0). Bırak–bas penceresinde boşta girişinin tutulan klibi koparıp fren duruşundan AAMS geri kalkışını zorlaması giderildi (§2.5). Kalan: 49 cm/s'lik en düşük girişte faz kutusu seçimine bağlı ayak kayması (s29_swl12, iki kipli 6,6 / 46,5 cm, §2.4).

**6. Düşük hızlı yanlış AAMS/pivot yolu kaldırıldı mı?**
Evet, üretimde (§2). Sahip: EarlyRev yolu hız > 150 istiyordu, bileşen sınıfı başlangıç hızı > 200 istiyordu; 40–135 cm/s geri koşuda ikisi de kapalı kalıyor, tutuş mandalı o anki satıcı depar pivot DB'sini tutuyordu. Yeni sınıf yalnız **istenen yürüyüş tempolu/depar** (CMC MaxSpeed > 145) ve **geri koşu** (hız ile bakış ters, dot < −0,7) iken açılıyor; yürüyüşte hiç tetiklenmiyor (w30_rev pop 0, yürüyüş pivotu değişmedi).

**7. Soğuk başlatmada depar dönüşü kopması düzeldi mi?**
Kopma "anim saati kapsülün gerisinde" değildi: V2.29'un 81,7° bulgusu kayıt sırasından doğan **bir kare geç okuma** (anim güncellemesi N karesini N+1'de yazıyor). Kontrollü 0,4 s duraklamada kapsül 116,8° döndü, klip aynı karenin devamında 0,400 s ilerledi; iki saat eşit. Duraklama sırasında görünen sıçrama oyun zamanının kendisi (0,4 s tek karede geçiyor), sonrasında senkron kaybı yok. Soğuk ilk koşudaki ayrı 47 cm pelvis gecikmesi aynı anda kontrollü duraklamayla **üretilemedi** (PBI/settle/SCR açık-kapalı: 25–28 cm) → NOT_REPRODUCED (§5).

**8. Hangi gerilemeler kaldı?**
PARTIAL: s29_swl12'de 49 cm/s girişte faz kutusuna bağlı 46,5 cm ayak kayması (iki kipli, §2.4); tempolu geri dönüş ailesinde 60/120 FPS'te kayma artışı (e29_load 31–37 cm, §7); koşudan koşuya değişkenlik (ilk adımda ayrışma, §8). §6 tablosu: C eğimde depar (175, TIP montaj sonu → satıcı pivot kuyruğu 1 kare; eğime özgü değil) OPEN; D arka çapraz −112,5 (OW bükme 14 cm, ara içerik gerekiyor) OPEN; F zemin zinciri (yürüyüş 28 cm basamakta 0,43–0,50 s havada kalma; StepPrep etkisiz) OPEN; depar döngüsünde 25–28 m/s² eşik geçişleri (gerçek kadans, §3.3) ve RevTurn R_Rfoot varyantının 42'lik girişi bilgi notu.

**9. Unreal neden yeniden başladı, hangileri önlendi?**
22 editör açılışı: 1 bellek tükenmesi (profiller + fonksiyon derlemesi tek editörde; artık ayrık), 3 bellek koruması (bellek sahibi düzeltilmeden önce), 1 ZenServer takılması (17 dk bekleme; artık 90 s bekçi), geri kalanı bilinçli taze editör (derleme öncesi, içerik düzenlemesi sonrası indeks, gerçek zaman/FPS modu, temiz yeniden açılış doğrulaması). Bellek sahibi düzeltildikten sonra **bellek kaynaklı yeniden başlatma 0** (V2.29: 49). §8.

**10. Neler üretimde, neler kapalı aday?**
Üretim: düşük hızlı geri dönüş sınıfı (`RedirectLowRevSpeed` 30 + `SHM230_EarlyRevMin` 30, istenen yürüyüş tipi geçidi), boşta girişi koruması (`SHM230_IdleGuard` 1), yeniden yazılan 22 klip, güvenli inceleme sondası, telemetri yan dosyası, harness/araç düzeltmeleri (iş dosyası yarışı, ZenServer bekçisi). Kapalı aday: `SHM230_FamGate`, yük ailesi (`SHM230_LoadedOn`), StepPrep (sp1/sp2), düşük hız tabanı 70 (`lr70`: yalnız V2.29 davranışını geri getirdi). Hiçbir üretim özelliği sessizce kapatılmadı.

## 1. Başlangıç ve temizlik sonrası güvenlik
- Temizlik (95,1 GB; ham video/kare, eski günlükler, V2.28 öncesi checkpoint kopyaları ve ham Evidence JSON) sonrası: `verify_fin229` ALL_OK, `integrity230.py` 6 607 paket / 46 eksik referans (kurulu olmayan AAMS demo Mannequin + EnviroSense; temizlikten önce de vardı). Aktif klipler, kaynak animasyonlar, derleme araçları, V2.28/V2.29 kanıtı ve checkpoint'ler yerinde. Temizlik bittikten sonra V2.30 başladı; ikisi eş zamanlı yürümedi.
- Üretim durumu her koşuda kaydedildi (`state_mode` production/candidate, `_state.json`); INVALID_STATE 0.
- Motor/mimari: UE 5.8, Blueprint-only; sahipler: bileşen `BP_SHM_HumanMotionComponent` (DSL), ABP `ABP_GR_MotionMatchingBase`, DA_SHM. Yeni sistem/framework yok; her değişiklik mevcut sahibinde.

## 2. Düşük hızlı geri koşudan ileri isteği (öncelik 1)

### 2.1 Giriş durumları ve sahip
Senaryolar: `s29_swl08…20` (depar W → S 0,8–2,0 s → W), `j30_slow` (tempolu geri, bırak, yavaşlarken W), `e29_load` / `e29_recov` / `e29_chain` (efor altında tekrar eden dönüşler). W anındaki giriş durumları: **frenleme sürüyor** (geriye 80–145 cm/s), **sıfıra yakın, destek tamamlanmamış** (30–80), **gerçekten durmuş** (< 30: sınıf açılmaz, normal kalkış), **zaten yeni yöne itiyor** (hız ileri: sınıf açılmaz). V2.29'da ilk iki durumun yolu: EarlyRev (hız > 150) kapalı, bileşen sınıfı (başlangıç hızı > 200) kapalı → tutuş mandalı o an seçili satıcı `PSD_Dense_Stand_Sprint_Pivots`'u tuttu → depar 180 pivot kuyruğu (çömelik geniş duruş) → `WalkToSprint` → baş pop'u 88–119 m/s².

### 2.2 Değişiklik (eşik düşürme değil, sınıf)
`lowRev` = geri koşu (dot(hız, bakış) < −0,7) **ve** istenen yürüyüş tempolu/depar (`MaxSpeedNow` > 145; yürüyüş isteği hiç girmez) **ve** dönüş açısı sınıf açısının üstünde. Bu sınıfta epizot alt sınırı 30 cm/s ve sınıf, başlangıç hızı koşulu olmadan açılıyor; ABP EarlyRev aynı geçitle 30 cm/s'den başlıyor. Sonuç: yazılmış tempolu geri dönüş ailesi (V2.26/V2.28 klip-bağlı kapsül) giriyor; AAMS/satıcı depar pivotu bu durumlarda seçilmiyor. İlk denenen "yakın zamanda koşuyordu" geçidi (SpeedPeak/efor) yürüyüşe de sızabilirdi; istenen yürüyüş tipine bağlandı.

### 2.3 Sonuç (aynı içerik, aynı oturum; sabit 30)

| Senaryo | Yol kapalı (`nolr`, V2.29 yolu): pop / tüm-klip kayma | **Üretim**: pop / kayma | Not |
|---|---|---|---|
| s29_swl14 | 109 / 40,2 | **34 / 40,2** (aile 1,9) | yakalama: 112 → 34 |
| s29_swl16 | 88 / 40,2 | **32 / 43,5** (aile 14,1) | |
| e29_load | 110 / 30,2 | **61 / 22,7** (aile 8,2) | |
| e29_recov | 110 / 35,5 | **54 / 21,0** (aile 9,4) | |
| j30_slow | 28 (yakalama) | **0** / aile 9,2 | |
| s29_swl12 | 109–111 / 33,6–68,6 | **32–33 / 6,6–46,5** | faz kutusu iki kipli (§2.4) |

Yürüyüş güvenliği: `w30_rev` (yürüyüş W→S→W) pop 0, yürüyüş pivot yolu değişmedi. `w30_postsprint` aslında Shift bırakınca RUN (245–300 cm/s): orada seçilen tempolu aile V2.26 yolu, düşük hız sınıfı değil (T10 ve T12 seçimleri birebir aynı).

### 2.4 Kalan: 49 cm/s girişte faz kutusu (PARTIAL)
s29_swl12'de W anında hız 49 cm/s; araya 2 karelik `A_LB_Walk_Bwd` giriyor. Aile girişi o döngünün evresine göre ya P29'u (sağ ayak salınımda, 6,6 cm) ya da P6'yı seçiyor: P6'da sağ top yerde (z −3,6) 2,2–4,0 m/s sürükleniyor = **46,5 cm kayma**. Aynı oturumda bile iki kipli (T15 r1 6,6 / r2 46,5). Kapsül hızı bu girişte 49 → 30 → 93 → 48 (245 cm/s için tasarlanmış klip hız eğrisi). Taban 70 adayı (`lr70`) yalnız V2.29 davranışını geri getirdi (pop 109–111, kayma 33,6–68,6) → kapalı. Gerçek çözüm: düşük giriş hızına uygun evre seçimi (basılı ayak eşleşmeli kutu) veya bu hız bandı için kısa yürüyüş-pivot bağlantı içeriği. Açık iş.

### 2.5 Bırak–yeniden bas penceresinde boşta girişi
**Bulgu** (v230fin j24_rel ile v230t1 j24_rel, aynı girdi): S, tutulan yazılmış geri dönüşün içinde 0,15 s bırakıldı (`SHM227_Hold`, kapsül tasarlanmış sıfır geçişinde ~0 cm/s). Bir koşuda sol topuk bir kare erken yere bastı (poz farkı 2–3 mm), `SHM_IdleWait` (ayaklar hareketli/yerleşiyor) düştü, `idleNow` doğru oldu → 5,40 s'de `SHM_IdleEntry`/`IdleHold` → S 5,47 s'de yeniden basılmış olmasına rağmen tutuş 5,50 s'de bitti → MM fren duruşundan `Jog_Bwd_Start_AAMS` oynattı (sağ ayak 33,8 cm kayma). V2.29'un bırak-devam penceresi (`SHM229_ResumeWin`) hiç devreye giremedi: boşta girişi ayrı bir yol.

**Değişiklik** (`SHM_Snapshot`, grafik düzeyi, `install_v230_idleguard.py`): `idleNow` → `idleNow AND NOT(düğme AND SHM227_Hold AND (SHM228_Brake OR PostT < SHM229_ResumeWin))`; `idleNow`'u okuyan iki tüketici (IdleEntry, IdlePrev) birlikte yeniden bağlandı, pencere bitince boşta girişi normal çalışıyor. Düğme `SHM230_IdleGuard`.

**Doğrulama** (aynı editör, bırakma anı taraması `j30_rel_<ms>`: S 3,10–3,45 s'de bırakılıp 0,15 s sonra yeniden basılıyor):

| Bırakma (s) | 3,10 | 3,15 | 3,20 | 3,25 | 3,30 | 3,35 | 3,40 | 3,45 |
|---|---|---|---|---|---|---|---|---|
| Üretim (koruma yok): tutuş içinde boşta girişi | 0 | 0 | 0 | **1** | **1** | **1** | 0 | **1** |
| Üretim: aile kayması cm | 53,8 | 19,5 | 12,0 | 32,7 | 28,0 | 31,7 | 28,5 | 20,8 |
| Koruma açık: aile kayması cm | 53,8 | 19,5 | 12,0 | **13,2** | **13,2** | **13,2** | 28,5 | 20,8 |

Yarışın tetiklendiği 4 bırakmanın 3'ünde koruma devralmayı engelledi (28–33 → 13,2 cm); 3,45'te sonuç aynı (pop 78 ikisinde de). 3,40'ta korumalı koşu toparlanma ailesine sapıp 93'lük pop verdi: o çiftte boşta/tutuş durumları kare kare aynı ve iki koşu daha **t = 2,77 s'de (ilk adım, `cv_CamStepCount` 0/1) ayrışıyor** → koruma etkisi değil, koşudan koşuya değişkenlik (§8). Sakin/yürüyüş/tempolu akışlar (c30_calm, c29_combo, w30_rev, j24_ph0, j24_dbl, j30_slow) koruma açık/kapalı birebir aynı. 3,10'daki 53,8 cm kayma her iki durumda var (bırakma frenin erken evresinde; ayrı, açık iş). **Üretime alındı** (FIN3, §9).

**Üretimde (FIN3, temiz yeniden açılış sonrası, sabit 30)**: hiçbir koşuda tutuş içinde boşta girişi yok; bırakma 3,25 / 3,30 / 3,35 → 13,2 / 13,2 / 13,2 cm; j24_rel 11,1; j24_dbl 16,1; sakin akışlar, yürüyüş ve düşük hız sonuçları FIN2 üretimiyle aynı (`tables230_fin3.txt`). Yakalamalar korumadan önce alındı; yakalanan akışlarda yarış tetiklenmedi (j24_rel 11,1 cm her iki durumda), görüntü aynı.

## 3. Depar/ivmelenmede baş–kol–omuz salınımı (öncelik 2)

### 3.1 Kaynak zinciri
Aynı girdide katmanlar tek tek kapatıldı (`oPBI`, `oSCR`, `oCLD`, `oOW`, `oRAW`, `oSET`): baş–pelvis yanal salınımında değişim ≤ 1 cm → çalışma zamanı katmanları sahip değil. MM çıktı ağı ile görünür beden aynı genlikte → retarget/harmanlama da değil. Sahip klip içeriği: `SHM217_J2S` başında baş dünya düzleminde 32,5 cm, omuz hattı 36° yuvarlanma; `SHM218_W2S` 16,6 cm / 27°; depar döngüsü 11,4 cm / 15°. Satıcı döngüleri ayrıca 0,72–0,82 hızla oynuyordu (ağır çekim ritmi, §3.2).

### 3.2 Yeniden yazım ve oynatma hızı
Aynı kadansta adım ölçekleme + segment başına yanal salınım zayıflatma (pelvis / göğüs / baş / kol; depar 0,6/0,5/0,45/0,75, yürüyüş-arka ve yan 0,8/0,8/0,7/0,85) + `solve_leg` bacak yeniden çözümü (leg_guard: diz sıçraması ≤ 24,6°; eğri kliplerinde büyük adım küçültme diz eşiğini aştı → adım 1,0, yalnız salınım) + IK ayak eşlemesi; otomatik yan eksen ve yuvarlanma işareti denetimi (ilk denemede yan eksen yanlıştı, düzeltildi).

| Klip (oyunda) | baş–pelvis yanal / pelvis / omuz yuvarlanma | V2.29 | **V2.30** |
|---|---|---|---|
| W2S_Lfoot_a (s29_ws) | cm / cm / ° | 16,8 / 5,2 / 24,0 | **6,4 / 3,6 / 8,4** |
| Depar döngüsü (s29_ws, düz) | | 12,9 / 7,6 / 13,7 | **11,3 / 4,9 / 7,4** |
| J2S_Lfoot_b (d_sprint) | | 24,9 / 14,1 / 32,6 | **11,2 / 8,8 / 10,7** |
| Depar eğri R25 | | 8,4 / 3,9 / 19,8 | **9,2 / 2,0 / 4,5** |

Oynatma hızı (tüm üretim koşuları, `rate230`): depar döngüsü 0,82 → **0,98**, yürüyüş arka 0,75 → **0,98**, arka sağ/sol 0,72 → **1,00**, tempolu sağ 0,82 → **1,00** (T-koşuları), eğri R25 0,64 → **0,82** (eğriler adım 1,0'da kaldı: kısmen).

### 3.3 Bilgi notu: ivme sayısı arttı (gerçek kadans)
d_sprint pop sayısı 7 → 15 (en kötü 31 → 36). Sahip: döngü artık gerçek hızında; ivme hız² ile ölçeklenir (1/0,82² = 1,49), genlik düşüşü bunu kısmen dengeliyor. Düz depar omuz ivmesi medyan 9,4 → 13,0, p95 21,5 → 23,8, **en yüksek 28,9 → 28,4 m/s²**. Eşik (25) geçişleri adım çevrimi başına bir kez (~0,6 s, ≈ 3,3 adım/s, hızlı koşu kadansı). s29_cam en kötü 33 → 42: depar evresi değiştiği için RevTurn **R_Rfoot** varyantı seçiliyor (V2.22 içeriği, girişi R_Lfoot'tan ~10 m/s² güçlü); yeni mekanizma değil.
Kamera kadrajı değişmedi (`screen229` d_sprint/s29_ws: ekran dışı kare 0, göğüs x/y aralığı V2.29 ile aynı). Önce sabit yan/çapraz kamera, sonra oyun kamerası yakalandı (§9).

## 4. Eforun bedensel karşılığı
Üretim V2.29 eforu: fren desteği ve ek yerleşme adımı yük arttıkça uzuyor (e29_chain 2 → 3–4 destek adımı), ölçülü yeniden itiş (`EffortScaleMin` 0,7), dinlenmeden sonra toparlanma (`EffortTauRec` 5 s; e29_rest 4,7 s'de değerlendirildi: pop 54, aile kayması 0). Efor klip değişince sıfırlanmıyor (bileşen durumu; `cv_EffortEUse` zaman serileri kanıtta). V2.30 adayı **yük ailesi** (`SHM230L_JogRev_*`, 53 faz klibi; ölçülmüş kapsül tablosuyla tempo gerilmesi; 11 kutu ayak hatası > 7,5 cm / sürüklenme > 3 cm nedeniyle dışarıda): yükte seçildi (e29_chain/load/recov), görünür yarar ölçülemedi, bir geçiş boşluğu açtı → kapalı aday. Rastgele tökezleme veya ağır çekim eklenmedi.

## 5. Geçiş sürekliliği ve soğuk başlatma
- RevTurn ±180 sarma düzeltmesi korunuyor: `verify` RevTurn burulma sıçraması ≤ 30°/kare; tüm üretim koşularında SPIN 0 (T14'teki tek SPIN, 0,4 s duraklama karesinin kendisi: 0,4 s'lik dönüş tek karede).
- Soğuk başlatma (gerçek zaman; `s29_cam` ilk koşu + `s29_camh/camh2/camh3` kontrollü 0,4 s duraklamalar): kayıtlı klip zamanı bir kare geç; duraklama karesinde kapsül 116,8° döndü, sonraki satırda klip 0,400 s ilerledi → saatler eşit. Duraklama sonrası mesh–kapsül ≤ 28 cm (sabit adım 24–27). Soğuk ilk koşuda 8,4 s'de 47 cm pelvis gerisi görüldü; aynı anda kontrollü duraklamayla üretilemedi (üretim, PBI kapalı, settle kapalı, SCR kapalı: 25–28 cm) → NOT_REPRODUCED. Kök kapsülle aynı; fark pozda.
- Değişken kare süresi: 20/60/120 FPS tablosu §7.

## 6. V2.29 gerilemeleri

| | Durum | Kanıt |
|---|---|---|
| A j24_dbl 16,7 → 23,1 | **çözüldü / yeniden üretilemedi**: V2.30'un 4 oturumunda (üretim dahil) 16,1 cm; 20/60/120 FPS 35,4/18,2/13,8 (V2.29 ile aynı) | `tables230_slip*.txt` |
| B soğuk başlatma kopması | **PARTIAL**: 81,7° bulgusu ölçüm hatası; duraklama sonrası senkron kaybı yok; soğuk ilk koşudaki 47 cm pelvis gerisi NOT_REPRODUCED | §5 |
| C legs_slope_sprint baş pop'u (175) | **OPEN**: TIP montaj sonu → satıcı pivot kuyruğu 1 kare → kapsül hâlâ 90° dönerken koşu kalkışı; eğime özgü değil | üretim 175 (V2.29 175) |
| D arka çapraz −112,5 (14 cm) | **OPEN**: RearLeft 22,5°'lik OW bükmesi 14,1 cm (sağ 7,6); ara yön içeriği gerekiyor | T-koşuları |
| E ağır çekim aileleri | **PASS (teknik)**: yürüyüş arka, tempolu yan, depar döngüsü ~1,0; depar eğrileri **PARTIAL** (0,82) | §3.2 |
| F zemin zinciri | **OPEN**: yürüyüş 28 cm yükselişte sağ ayak 0,43 s havada, inişte sol 0,50 s; StepPrep (sp1/sp2) etkisiz (0,37–0,53 s, pop'lar aynı 260/251/190); basamak inişindeki 260 = kapsülün 28 cm düşüşü (baş 27,8 cm). Tam bir yükseliş/iniş zinciri tamamlanamadı | T11, üretim |

## 7. FPS ve kare süresi (üretim; en kötü pop m/s² / aile kayması cm)

| Senaryo | 20 | 30 | 60 | 120 | V2.29 (20/30/60/120) |
|---|---|---|---|---|---|
| s29_swl14 | — (koşu kaybı, §8) | 32 / 16,4 | 66 / 1,1 | 145 / 22,8 | pop 82 / 110 / 131 / 162 |
| e29_load | 48 / 20,7 | 61 / 8,2 | 79 / 31,3 | 145 / 36,5 | pop 83 / 110 / 109 / 162; kayma 29,4 / 24,6 / 18,3 / 7,5 |
| e29_chain | 56 / 13,6 | 55 / 9,3 | 66 / 12,9 | 145 / 15,0 | pop 56 / 55 / 67 / 147; kayma 13,6 / 9,3 / 4,6 / 3,9 |
| s29_cam | 36 / 0 | 42 / 0 | 66 / 0 | 145 / 0 | burulma sıçraması 16 / 11 / 5 / 2° (V2.30) |
| j30_slow | 0 / 4,3 | 0 / 9,2 | 40 / 10,2 | 93 / 14,7 | — |
| j24_dbl | 0 / 35,4 | 0 / 16,1 | 48 / 18,2 | 82 / 13,8 | kayma 35,4 / 23,1 / 18,2 / 13,8 |

İvme pop ölçüsü örnekleme sıklığıyla büyür (120'de 145 = koşu başında 0,95 cm'lik baş titreşimi). Pop'lar her FPS'te V2.29'dan düşük. **Kayma 60/120 FPS'te e29_load ve e29_chain'de arttı**: tempolu geri dönüş ailesi seçimi FPS'e bağlı (V2.25'ten bilinen) → PARTIAL.

## 8. Unreal geliştirme süresi ve bellek
**Bellek sahibi** (yeni framework yok: süreç belleği + UObject sayımı, `-LLM -LLMCSV`): aynı 31 s'lik PIE koşusu başına özel bellek +1,73 GB; UObject/World/Actor sayıları sabit, GC hiçbir şey geri almıyor; LLM `UI/UI Slate/OnPaint` 6 koşuda +5 GB. Sahipler: (1) inceleme sondası her karede boş aktöre `ActorHasTag/GetActorBounds` → 6 koşuda 36 720 PIE "Accessed None" (mesaj günlüğü); (2) qa_pie her kare ~12 KB LTP satırını editör günlüğüne yazıyordu (Output Log hepsini tutup çiziyor). Düzeltme: güvenli sonda + LTP yan dosyası. Sonuç: **0,12–0,24 GB/koşu** (medyan 0,18; t2'den sonraki tüm oturumlar). Bellek koruması yeniden başlatması V2.29'da 49; V2.30'da düzeltmeden önce 3, sonra **0**.

**Derleme aşamaları**: profiller (yeni DA alanı) + `build_funcs` tek editörde < 60 s'de 19 → 78 GB commit, OOM çöküşü (1 kez) → V2.29 ayrımı gerçek. Fonksiyon derlemesi tek başına + ABP grafik yamaları + anim yazımı + PIE testleri aynı editörde sorunsuz (fonksiyon derlemesinden sonra yeniden başlatma gerekmedi; T12'de derleme 3 dk).

**Editör açılışları (21 satır, 20 hazır)**: p0 (temizlik sonrası doğrulama), m2 (LLM ölçümü), bA (derleme → OOM), bB (ayrık derleme), t1 (testler; geriye dönük bakışla bB editöründe yapılabilirdi), t2/t3/t6/t9/t10 (içerik/graf yazımı sonrası temiz durum; t2 bellek düzeltmesini doğrulamak için zorunluydu, diğerleri bellek düzeltmesi sonrasında artık gereksiz), t12 (DSL fonksiyon derlemesi), t13/t14 (gerçek zaman modu), fin (terfi), finv (temiz yeniden açılış doğrulaması: zorunlu), finv tekrar (ZenServer takılması), cap (sabit 30'a dönüş), h20/h60/h120 (FPS bir açılış argümanı), t15 (graf yaması + A/B). Açılış hazır olma medyanı 113 s, toplam 39 dk.

**Otomasyon arızaları ve kök nedenleri**: (a) RUNNER_NOT_READY 2 kez = ZenServer "Waiting for ZenServer to be ready" (önceki editörün zen'i kapanırken yeni editör ikinci zen başlatıp asılı kaldı; 17 dk). Düzeltme: `editor_launch230.sh` (eski zen'i ≤ 20 s bekle, 90 s ilerleme yoksa bırak) + sınırlı yeniden deneme (2); yeniden deneme 2 dk'da hazırdı. (b) İş dosyası yarışı: `run.sh` işi doğrudan `jobs/*.py`'ye kopyalıyordu; disk yükünde runner yarım yazılmış qa_pie işini 1 ms'de çalıştırdı, PIE hiç istenmedi, harness 13 dk bekledi (20 FPS swl14 koşusu kayıp). Düzeltme: geçici adla yaz + yeniden adlandır. (c) Bash heredoc'ta `\n` gerçek satır sonuna dönüştü (3 dosya) → `chr(10)`. (d) Bir ölçüm işinin `builtins` bayrağı sonraki yazma işine sızdı → tek kullanımlık bayraklar. (e) DB içeriği değiştikten sonra ilk PIE kullanımında indeks yeniden kuruluyor (seçim None) → ısınma + BuildIndex sessizliği beklemesi.

**Koşudan koşuya değişkenlik**: sabit adımlı editörde aynı girdiyle iki koşu ilk adımda (t = 2,77 s) `cv_CamStepCount` (0/1) ile ayrışıyor ve küçük poz farkları sonradan seçim eşitliklerini (j24_dbl, swl12 faz kutusu, toparlanma sapması) değiştiriyor. Bu yüzden tek koşuluk A/B farkları ancak adayın etkidiği karelerde (ör. tutuş içinde boşta girişi sayısı) değerlendirildi; sahibi bu sürümde bulunmadı (açık iş).

**Kademeli test**: hızlı (tek senaryo, aday), aday (A/B, 6–14 senaryo), son (üretim, 24 senaryo + FPS + gerçek zaman); her içerik düzenlemesinden sonra ısınma; yakalamadan önce 2 s'lik test yakalaması (60 kare doğrulandı).

**Zaman dökümü (zincir 04:58 → 12:41, 7 sa 43 dk; `timing230.out`)**

| Kalem | Süre | Not |
|---|---|---|
| Editör açılışı → runner hazır | 43 dk (22 açılış, medyan 113 s) | + 1 ZenServer takılması 17 dk (hazır olmadı) |
| PIE koşuları (ısınma + bellek örneği dahil) | 3 sa 50 dk (394 koşu, medyan 32 s) | test, aday, üretim, FPS, gerçek zaman |
| Derleme | bA 8 dk (OOM çöküşü), bB ~10 dk, T12 fonksiyon derlemesi 3 dk | |
| Anim yazımı / DB kurulumu | ~35 dk (yeniden yazım ölçüm + yazım, yük ailesi üretimi ve DB) | |
| Yakalama | 15 dk (16 yakalama + 2 s test) | medya kodlama ~12 dk (çevrimdışı) |
| Arıza / bekleme kaybı | ZenServer 17 dk, iş dosyası yarışı 13 dk, OOM 8 dk | üçünün nedeni bulundu ve düzeltildi |
| Bellek yeniden başlatması | 3 (hepsi bellek düzeltmesinden önce, 05:58–06:21) | V2.29: 49 |

Ölçülen kazanç: koşu başı bellek artışı 1,73 → 0,18 GB (aynı senaryo, ölçüm), bellek koruması yeniden başlatması düzeltmeden sonra 0. Tahmin (ölçüm değil): eski artışla bu sürümün 394 koşusu ~10 koşuda bir yeniden başlatma, yani ~39 × ~2,5 dk ≈ 1,6 sa olurdu. Ayarlar her koşuda kaydedildi (`state/*_state.json`: DA_SHM alanları, ABP DB referansları ve düğmeler, cvar'lar; INVALID_STATE 0). Etiketler: StepPrep **WRONG_PATH** (havada kalmanın sahibi değil), `IdleGuard` T15'te **NOT_TRIGGERED** (yarış o oturumda oluşmadı → bırakma taramasıyla tetiklendi), yük ailesi yükte tetiklendi ama yararı ölçülemedi.

**Editör açılışları (devamı)**: t15 (graf yaması + A/B), fin3 (ikinci terfi), fin3v (temiz yeniden açılış doğrulaması).

## 9. Kabul ve teslim
Sabit 30 (gerçek hız), tam kare, düzenlenmemiş. Yan (S), ön-sağ çapraz (D), oyun kamerası (G); dosyalar `vid/`.
- Sakin: `calm_idle_walk_stop_restart_v230_side/_game` (idle → ilk adım → yürüyüş → çapraz → dur → yeniden başla).
- Normal efor: `sprint_brake_repush_routeoff_side` (ÖNCE: düşük hız yolu kapalı) / `sprint_brake_repush_v230_side/_game`.
- Birikmiş efor: `effort_chain_v230_side/_game` (önce: V2.29 `effort_chain_v229_*`).
- İptal: `jogrev_release_v230_side` (önce: V2.29 `jogrev_release_v229_side`).
- Düşük hız: `slow_backjog_forward_routeoff_side` (ÖNCE) / `slow_backjog_forward_v230_side/_game`.
- Teknik: `sprint_cam180_v230_side/_game` (önce: V2.29 `sprint_cam180_v229_*`), `slope_sprint_turn_v230_side`.
- Salınım: `sprint_straight_sway_v230_side/_diag` (önce: V2.29 `sprint_WSWSW_v229_side` ve `effort_chain_v229_side` içindeki depar bölümleri; içerik yerinde değiştiği için aynı editörde "önce" yakalanamaz).
Aynı karede (s29_swl14, W anı): yol kapalıyken satıcı depar pivotunun geniş çömelik duruşu ve eller dizde; üretimde dik, ileri itişe geçen adım.

Teknik kabul: düşük hız yolu PASS (A/B), salınım/oynatma hızı PASS (teknik), j24_dbl çözüldü, swl12 faz kutusu PARTIAL, FPS'e bağlı kayma PARTIAL, C/D/F OPEN. **Görsel/oyun hissi kabulü: NOT_ACCEPTED_YET (kullanıcıya ait).**

Kayıt ve doğrulama: iki terfi taze editörde kaydedildi (`promo_fin.out`: düşük hız sınıfı; `promo_fin3.out`: boşta girişi koruması), temiz yeniden açılışta `verify_fin2.out` ve ikinci terfiden sonra `verify_fin3.out` **ALL_OK** (V2.29 grupları + RevTurn burulması + V2.30 düğmeleri + adaylar kapalı + güvenli inceleme sondası + yük ailesi varlıkları mevcut ama rotada değil). V2.26'nın eski inceleme sözleşmesi maddesi (`ActorHasTag`/`GetActorBounds` arıyordu) bilinçli olarak V2.30 denetimiyle değiştirildi.
