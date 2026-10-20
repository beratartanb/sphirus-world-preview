# SHME V2.19: kare hızından bağımsızlık, regresyonlar, toparlama gerçekçiliği (2026-10-20)

**Taban:** V2.18 üretimi (commit `053fcd0`).

**Karşılaştırmalar:**
- **Gerçek zaman:** "Önce" = V2.18 final üretim partisi `v218f`. "Sonra" = tek, kaydedilmiş V2.19 üretim partisi `v219f`. 107 koşu, en düşük 21 satır/s.
- **FPS:** Sabit zaman adımında 20 ve 120 FPS. V2.18 (`q20`/`q120`) ile V2.19 (`x20`/`x120`) aynı girdilerle koşturuldu.
  - Bu koşular deterministik: aynı ayarla aynı santim çıkıyor.
  - Bu yüzden FPS sütunlarındaki farklar doğrudan değişiklikten geliyor; tekrar gürültüsü yok.
- **Doğrulama:** Editör yeniden açıldıktan sonra yapıldı (`verify_prod219_f0.txt`): PASS, sızıntı yok, kirli paket yok. Tek bayrak farkı `TelemetryEnabled` (yalnızca test kaydı).

**Ölçüm araçları:**
- Ayak başına net kayma / sürükleme yolu (`contact216`). İki ayak hiçbir zaman toplanmadı.
- Gerçek zemin evresi (`rec218`).
- Diz: `knee217` ve ayak-ucu düzlemi.
- Klip sınıfı dizisi (`fps219_cmp.py`).

Görsel kontroller teknik değerlendirmedir; **kullanıcı kabulü verilmiş sayılmaz**.

## Kare hızı (öncelik 2): ne bulundu, ne yapıldı

**Yöntem:**
- Editör `-UseFixedTimeStep -FPS=N` ile başlatıldı: her kare tam 1/N s.
- 20, 30, 60 ve 120 FPS'de aynı girdiler koşturuldu.
- Ayrıca değişken FPS (`t.MaxFPS`) ve kontrollü takılmalar denendi: 0.15 s'lik tek takılma (ters tuştan önce, tuşta, fren duruşunda) ve dört takılmalı bir dizi.
- Veritabanının ilk kullanımı her editör açılışında ayrı ölçüldü.

**Zaman zinciri:**
- Ham tuştan girdi vektörüne 2 kare, klip seçimine 1 kare daha geçiyor. Kesiş, tuştan 0.15 s (20 FPS) ile 0.025 s (120 FPS) arasında bir sürede başlıyor.
- Sonuç olarak, sonraki ters tuşa gelindiğinde kesişin **evresi** FPS'ye göre değişiyor. Gizli FPS bağımlılıklarının çoğu buradan doğdu.

**Bulunan ve düzeltilen FPS sınıf hatası:**
- V2.18'deki "hareketli itiş" tespiti, itişin ilk karesindeki hız 220 cm/s'nin altındaysa kilitleniyordu.
- 20 FPS'de bu kare toparlama adımının sonuna denk geliyordu. Karakter 303 cm/s'de ayakta-başlangıç türü itişe (`PushLow`) düşüyor, ayak **125 cm** kayıyordu.
- **Düzeltme:** ters yön kilidi (toparlama dahil) açıkken başlayan itiş artık hareketli itiş sayılmıyor.
- **Sonuç:** 20 FPS'de **7 cm**. Hareket 30–120 FPS ile aynı sınıfa giriyor (RevPush @1.50).

**Toparlama tetiği:**
- 20, 30, 60 ve 120 FPS'de, değişken FPS'de ve dört takılma senaryosunun hepsinde girdi.
- V2.18'deki kayıt koşusu kaçağının nedeni FPS değildi. Kesişten hemen önceki 0.13 s'lik takılma sağ tuşu tek kareye indirdi ve sistem hareketi "sola kesiş" olarak doğru sınıflandırdı. Bu, girdinin takılma sırasında gecikmesi; mantıktaki bir FPS bağımlılığı değil.

**Açık kalan FPS/takılma kusuru:**
- Fren duruşunun içinde 0.18 s takılma olursa MM aynı toparlama klibinde zamanda geri sıçrıyor (1.13 → 1.00) ve fren ayağı **~33 cm** kayıyor.
- Bunu düzeltmedim. Aynı durumda iki tekrarın birinde 35 cm, diğerinde 0 cm görüldü.

**Etkisiz çıkan, geri alınanlar:**
- MM düğümünün `BlendTime` ayarı. Grafikte açık bir pin; ne düğüm özelliği ne de pin değeri sonucu değiştirdi. V2.3'teki "harmanlama etkisiz" deneyi de bu yüzden geçersizdi.
- Toparlama çıkış kapısı.
- Ters dönüş veritabanında "devam eden klibi tercih et" ağırlığı (−0.5).
- Döngü sonuna giriş yasağı: karışık sonuç verdi (bir senaryoda 40 → 5, başka birinde 5 → 15 cm).

## ONARIMLAR

| Hedef | Doğrulanan neden | Gerçek değişiklik | Önce → sonra (cm, en kötü) | FPS güvenilirliği (20 / 120 FPS, V2.18 → V2.19) | Üretimde | Kalan eksik | Geri alma |
|---|---|---|---|---|---|---|---|
| Normal sağ kesiş → ters (2.4 → 26.1 gerilemesi) | Ters dönüş klibi serbest sağ ayağı dönüş boyunca yerden 8–9 cm yüksekte ve 300–770 cm/s hızla taşıyor. Kesişten geçiş bu ayağı yere indiriyor ve süpürme oluşuyor. Kesiş evresi FPS ile kaydığı için 20 FPS'de 3.5, 120 FPS'de 28 cm. Yeni bir hata değil: V2.17'de ayak 6–8 cm yukarıda kaldığı için ölçülmemişti | `swingclear219.py`: `RevTurn_L_Rfoot` 0.55–0.98 s'de hızlı salınan ayak ≥ 14 cm'de tutuluyor, bacak menteşe olarak yeniden çözülüyor (5.2 cm kaldırma) | Giriş R 26 → 5 (koşular 2/3/26 → 5/2/1) | 20 FPS: 3.5 → 3.5. 120 FPS: **27.8 → 13.7** | EVET | Ters dönüş klibinden depar döngüsüne çıkışta 9–14 cm. Sol tarafta 120 FPS'de R 22.6 (değişmedi) | `checkpoint/pre_swing` |
| Çok erken ters dönüş (sağ/sol) ve +0.25 s | (V2.18'de çözüldü) | Toparlama v8 içeriği (aşağıda) | Sağ R 17 → 5, sol L 8 → 4 | 20 FPS: L 7.4 → 7.4. 120 FPS: değişmedi | EVET | — | `checkpoint/pre_e1` |
| +0.25 s erken ters, 20 FPS | Hareketli itiş FPS sınıf hatası (yukarıda) | `install_v219_lowstand4.py` | Gerçek zamanda 7–8 (değişmedi) | **20 FPS: 125.2 → 7.0** | EVET | — | `checkpoint/pre_e3` (ABP + lisp) |
| Ardışık ters dönüş (`r_kb2`) | Pivottan sonraki hareketli itiş klibi (`PushLow`) hiç kapsüle göre yerleştirilmemiş bir kopyaydı. Klibin kök hızı ölçülen hızdan farklıydı (101 → 345 → 490 cm/s; tüm FPS'lerde aynı) | `pushlow219_jobs.py`: ayaklar ölçülen kapsül hızına yeniden yerleştirildi; duruş algılama 5 cm | L 24 → 13. R'de bir tekrar 32 cm (diğerleri 4/6) | 20 FPS: L 28.4 → 17.2, R 17.7 → 8.6. 120 FPS: L 33.7 → 10.4, R 28.2 → 7.4 | EVET | Girişte sol ayak ucu sürtmesi (17 cm). Önceki klibin ayak noktasına hizalama denendi, 76 cm'ye çıktığı için reddedildi | `checkpoint/pre_pushlow` |
| Kesiş → S geri koşu girişi (V2.18'de 124.5 sürüklenme) | Bağlantı klibinden geri koşu döngüsüne geçişte tek karelik poz sıçraması. 60 FPS'de ise AAMS tempolu pivot klibi (`A_CP2_Jog_Fwd_Pivot`) mesafe eşlemesiyle 1.7–2.7 kat hızlı oynuyor ve ayak ucu kayıyor | Doğrudan değişiklik yok | Kesiş evresi R 16 → 10. Geri koşu evresi R 32 → 11, ama L 19 → 26 (tek tekrar) | 20 / 120 FPS: değişmedi | — | AAMS pivot klibinin ayak ucu kayması **çözülmedi** | — |
| Kesiş sırasında tuş bırakma | Bırakma sonrası durma klibinde (RR_Stop) ayak ucu pivot kayması | Değişiklik yok | L 33 → 10, R 28 → 42 (her biri 2 tekrar) | — | — | Durma klibi kayması **çözülmedi** | — |
| Yürüyüş → depar, geç basış | 20 FPS'de bağlantıdan depar döngüsüne @0.17 çıkışta ayak ucu kayması; 60 FPS'de yürüyüş duruşundan bağlantıya girişte sürüklenme | Değişiklik yok | Geç R 27 → 15. Orta R 14 → 13 | 20 FPS: R 16.2 → 16.2 | — | Çıkış ve giriş evre farkı **açık** (14–16 cm) | — |
| Tempolu → depar, iptal ve kısa dokunuş | Bağlantı bölümü itiş bitmeden bitiyordu; MM itişin ortasında ayakta-başlangıç klibine (`RR_Start` @0.43) düşüyordu | `SHM217_JogLink` 470 → 490 (= itiş tavanı) | Kısa dokunuş L 40 → 30, bırak-yeniden-bas L 21 → 15, rel L 9 → 15 (tek tekrar) | 120 FPS `p_j2s`: **L 20.8 → 4.9**. 30 FPS dokunuş: L 18.8 → 9.4. Hiçbir senaryoda kötüleşme yok | EVET | Kısa dokunuş / yeniden basmada depar döngüsüne @2.13'ten girişte 24–34 cm. 20 FPS'de `J2S_Rfoot_a` seçilince L 18.7 | `SHM217_JogLink 470` |
| Geç ters dönüşte diz | Klibin kendi diz bükülme düzlemi saniyede 455° dönüyor, oyunda 1190–1210°. Fazlası çalışma anındaki IK katmanından geliyor. Bu koşularda dönüş ortasında klip değişimi yok; veritabanı ağırlığı etkisiz | Klip içi diz düzlemi yeniden çözme denendi: klip 455 → 798 °/s, kötüleşti, uygulanmadı | Düzlem hızı 1200 °/s (değişmedi). Ayak-ucu düzlemi ≤ 10 cm | Tüm FPS'de aynı | HAYIR | **ÇÖZÜLMEDİ**. Sahibi çalışma anı IK / FootPlacement | — |
| Yerinde ters dönüş (TIP) devri | V2.18 analizi geçerli: başlatma açı kutuları ve dönmeye devam eden ilk montaj, devri ilk montajın sonuna erteliyor | Değişiklik yok | t_tiprev R 15–17 (tüm FPS'de aynı) | — | HAYIR | **ÇÖZÜLMEDİ** | — |

## GELİŞTİRİLEN DAVRANIŞLAR

| Davranış | Gerçek uygulama | Önce → sonra | Görsel değerlendirmem | FPS güvenilirliği | Üretimde | Kalan eksik | Geri alma |
|---|---|---|---|---|---|---|---|
| Yere basan toparlama (v8) | Kalça tabanı 82 (`floor_keep 0`). V2.18 kaynaktaki çökmenin %30'unu bırakıyordu; gerçek sınırlayıcı buydu. Fren ve yeniden yerleşme adımları gövdeye doğru en fazla 12 cm çekildi (yeni `stance_pull`). Kol açıklığı 30 cm (önce 45–48) | Final: 15/15 girdi, hedef dışı 86 koşuda 0 tetik. Fren ayağı 0.16–0.31 s basıyor, ikinci ayak 0.05–0.12 s. Pencerede en kötü 7.7 cm. Kalça en düşük 74.7–77.7 → **76.4–79.6** | Kollar daha toplu. Dizler biraz daha açık, gövde daha dik. Yine de belirgin atletik bir fren pozu kalıyor (kalça koşudan ~10 cm aşağıda, sol tarafta geniş adım) | 20–120 FPS, değişken FPS ve takılmalarda girdi. Fren duruşundaki 0.18 s takılma kusuru açık | EVET | Atletik görünüm tamamen gitmedi. Yeni yön (`r0_w`) çıkışında bir tekrarda R 46 cm (kavis klibinde) | `checkpoint/pre_e1` |
| Doğal frenleme ve ağırlık aktarımı | Toparlama v8 ve yeniden yerleştirilmiş hareketli itiş | Yukarıdaki satırlar | Fren ayağı yükü taşıyor, gövde desteği takip ediyor (kayıtlar) | — | EVET | — | — |
| Kısa itiş / tek ek destek adımı | Toparlamanın tek yeniden yerleşme adımı. İkinci adım eklenmedi | — | Tek ek adım; ardından koşu | — | EVET | — | — |
| Ortam kontrolleri | Eğimde tempolu, basamakta yürüyüş, yürü-dur-yürü, eğimde kavis, kamera dönüşü (`k_ws_cam`), tempoluda kesiş-bırakma, çapraz koşu | Basamak L 24 → 5. Yürü-dur-yürü 35 → 32. Eğimde tempolu 34 → **59** | Bu koşularda V2.19 mekanizması devrede değil. Kayma AAMS duruş/başlangıç ve yerinde dönüş kliplerinde; hangi klibin seçildiği koşudan koşuya değişiyor | — | (değişiklik yok) | Eğimde başlangıç/durma kayması **açık**. Yeni bir ortam tepkisi eklenmedi | — |

## Kayıtlar

- **İçerik:** Gerçek hız, kil test görünümü, kareler düzenlenmedi. `vid/` klasöründe GIF ile gerçek zamanlı ve 1/3 hızlı AVI'ler, `img/` klasöründe kare tabloları var.
- **Kameralar:** Toparlama sağ ve sol, yandan, oyun kamerasından ve çaprazdan. Ayrıca çift ters, kesiş→S, tempolu itiş, yürüyüş→depar, geç ters dönüş (diz), normal ters dönüş, eğim, basamak ve yürü-dur-yürü.
- **Kare hızı:** Kayıt koşuları kodlama yükü nedeniyle ~20–25 FPS'de. Takılmalı kayıtlar kesin kanıt olarak kullanılmadı.

## Dosyalar ve geri alma

- **Araçlar:** `Tools/SHME_V219_20261020/`: `swingclear219`, `kneeplane219` (reddedildi), `tailblock219` (reddedildi), `db_bias219`, `install_v219_lowstand4`, `fps219_cmp`, `runfps`, `final219`, `verify_prod219`.
- **Kanıt:** `Saved/Codex/SHME_V219_20261020/`
  - `fps219_cmp.txt` ve `fps219_final_cmp.txt` (kare hızı karşılaştırmaları);
  - `final219_table.md`, `final219.json`, `rec219_final.txt`.
- **Paylaşılan araç değişiklikleri:**
  - `remap217.py`: `stance_pull` ve `stance_height` seçenekleri;
  - `qa_pie.py`: `hitches` (takılma enjeksiyonu);
  - `v2_editor_launch.sh`: `V219_EDARGS` (sabit adım argümanları).
- **Kontrol noktaları:** `checkpoint/baseline_v218`, `pre_e1`, `pre_e3`, `pre_swing`, `pre_pushlow`, `pre_tailblock`, `pre_dbbias`, `pre_promote`.
