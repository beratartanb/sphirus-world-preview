# SHME V2.55 raporu: yön doğruluğu ve dönüş ailesi

Tarih: 2026-11-04. Taban: V2.54 üretimi.

## Sonuç

**V2.55 üretime alındı, ama görsel olarak kabul edilmiş değil.** Üretimdeki V2.54 değerlerinde kanıtlanmış bir ters yön hatası vardı ve bunu ancak oyunda deneyebilirsin. Terfi ederken hiçbir FPS'te oynanışı bozan bir sonuç görmedim.

Temiz yeniden açılıştan sonra üretim yapısı 10 senaryonun hepsinde adayla birebir aynı sonucu verdi. "Terfi ve geri alma" bölümünde beğenmediğin davranışı tek başına kapatmanın yolu var.

**Son kabul sorusuna cevabım: henüz evet diyemem.** Karakter artık sprint ve koşuda istediğin yöne güvenilir gidiyor ve bunu ölçtüm. Bacakların doğal görünüp görünmediğini ise sen oynayarak karar vereceksin. Yürüyüşte S hâlâ geri yürüyüş, sprint 180 pivotunda bacaklar geniş ve alçak açılıyor. Bu ikisi yüzünden iş tamamlanmış değil.

| konu | durum |
|---|---|
| Yanlış yön (engelleyici) | Teknik PASS, sprint ve koşuda: yön matrisi 144 olay 0 hata (üretim 21 hata) |
| Bacak ve anatomi | PARTIAL. Geri koşu ve kıyma adım gitti, sprint 180 pivotu hâlâ şüpheli |
| Momentum | PARTIAL. 90° ve 180° artık ayrı davranıyor, yürüyüş küçük düzeltme adımı yok |
| Aynı karakter, her hız | PARTIAL. Sprint ve koşu aynı aile, yürüyüş teslim edilmedi |
| Kamera ve üst gövde | PARTIAL. Omuz burulması düzeldi, omuz ofseti ve çapraz açı değişmedi |
| Görsel kabul | Senin kararın. Ben yalnızca gerçek zaman damgalı kare dizilerine baktım |

## Yanlış yön: kanıtlanan nedenler

Önerdiğin altı aday ayrı ayrı sınandı.

| aday | karar | kanıt |
|---|---|---|
| Girdi yanlış çerçevede veya iki kez dönüştürülmüş | Kanıtlandı, ama çift dönüşüm olarak değil | V2.34 çerçeve el değiştirme uygulanan yönle besleniyordu ve 60° üstünde salınıyordu. Hareket eden fare de koşu çerçevesini bitiriyordu. FRAME .80→.05 s |
| Sağ/sol işareti ve ±180 | Kanıtlandı | V2.54'teki işaret düzeltmem 120° üstü her isteği klip tarafına zorluyordu: sağ klipte −135, +135 oluyordu. Bu hatayı ben eklemiştim |
| Yeni komuta rağmen eski hedefin tutulması | Kanıtlandı | Hedef kilitliydi ve iptal 75° eşiğine bağlıydı. Hedef hatası 170°'ye çıkıyordu, iptalden sonra eski klip oynamaya devam ediyordu |
| Klip, kapsül ve gövde sahiplerinin çakışması | Kanıtlandı | V2.28 kapsülü `ActorForward × ClipSpeed` yazıyordu: hareket gövde eksenine kilitliydi, çaprazda 45°'ye kadar sapıyordu |
| Otomatik kameranın girdi referansını değiştirmesi | Kanıtlandı | Otomatik toparlama açık/kapalı karşılaştırması: FRAME 3.90→1.09 s, STALL 3.08→1.98 s |
| Geri yürüme ile dönüp koşmanın karışması | Koşuda kanıtlandı ve düzeldi, yürüyüşte duruyor | Koşuda S hep geri koşuydu: 2.50 s→0. Yürüyüş 2.32 s, değişmedi |

Ek bulgular: efor modeli ivmeyi %30 kesiyordu. Yaklaşma hızının altında girilen plan kapsülü hızlandırıyordu, yani oyuncu tersini isterken karakter eski yönde hızlanıyordu.

## Dönüş karnesi

60 FPS, üretim→aday, saniye.

| senaryo | ilk tepki | yüz | yön | yeniden hız | en düşük v | tepe g | geri koşu |
|---|---|---|---|---|---|---|---|
| sprint 180 sağ | .18→0 | 1.55→.98 | 1.23→.93 | 2.72→1.72 | 1→6 | .71→1.00 | .07→0 |
| sprint 180 sol | .18→0 | 1.52→.98 | 1.20→.90 | 2.68→1.93 | 1→9 | .70→1.04 | .07→0 |
| sprint 135 | .18→0 | 1.52→1.05 | 1.52→.98 | yok→2.02 | 2→7 | .68→1.06 | .07→0 |
| sprint 90 sağ | 0→0 | .77→.58 | .77→.63 | 1.88→1.35 | 170→209 | 1.06→1.09 | 0 |
| sprint 90 sol | 0→0 | 1.10→.83 | 1.10→.85 | 1.98→1.83 | 141→211 | .64→1.00 | 0 |
| koşu 180 | 0→0 | yok→1.00 | .50→.92 | 1.53→1.33 | 0→5 | .89→1.04 | 2.50→0 |
| koşu 135 | .03→0 | yok→.95 | 1.67→.92 | 1.65→1.33 | 1→5 | .89→1.08 | 1.98→0 |
| koşu 90 sağ | .18→.25 | .72→.47 | .72→.50 | 1.05→.82 | 175→143 | .56→.89 | 0 |
| koşu 90 sol | .42→.37 | .92→.62 | .92→.67 | 1.33→1.15 | 162→142 | .58→.86 | 0 |
| yürüyüş 180 | 0 | yok | .68 | 1.12 | 0 | .62 | 2.32, değişmedi |

Koşu 180'de yön süresi .50→.92 uzadı. Bu kötüleşme değil: üretim .50 s'de geriye koşarak o yöne gidiyordu, gövde hiç dönmüyordu. Şimdi önce frenleyip dönüyor. Koşu 90'da ilk tepki .18→.25 biraz geç kaldı, ama yön ve itiş daha erken.

Dönüş ortası komutlar: sprintte kısa dokunuşta bedava hız yok (tepe 490). 180 sırasında W'ye dönmek v 209'dan 473'e çıkıyor, donma yok. Hızlı sağ-sol spam'de en düşük hız 139→218, son tuşa tepki .48→0.

Bütün tablolar `TABLES_V255.md` içinde.

## FPS taraması

Dönüşler 20, 30, 60, 120 FPS ve gerçek zamanda tetikleniyor. Üretimdeki ters yön ve geri koşu her FPS'te aynı biçimde düzeliyor.

| FPS | sprint 180 yüz | sprint 180 yeniden hız | koşu 180 yüz | koşu 180 geri koşu | sprint fare WRONG | koşu fare WRONG |
|---|---|---|---|---|---|---|
| 20 | 1.60→.90 | 2.80→2.20 | yok→.60 | 2.45→.10 | .90→.10 | .20→.35 |
| 30 | 1.57→.87 | 2.77→2.10 | yok→1.07 | 2.47→0 | .83→.07 | .20→.43 |
| 60 | 1.55→.98 | 2.72→1.72 | yok→1.00 | 2.50→0 | 1.03→.42 | .53→.65 |
| 120 | 1.51→.93 | 2.62→1.65 | yok→.97 | 2.53→0 | .79→.33 | .62→.26 |
| gerçek zaman | 1.59→1.01 | 2.82→1.78 | yok→1.02 | 2.46→0 | 1.52→.03 | .37→.27 |

Kötüleşenler:

- Koşu faresinde WRONG 20, 30 ve 60 FPS'te biraz arttı ve 20 ile 30 FPS'te .15 s'den uzun bir yanlış çalışma ortaya çıktı. Üretim bu senaryolarda çoğu zaman yanlış değil, durmuş (STALL) görünüyordu: STALL 3.00→1.85 ve 4.20→2.04.
- 20 FPS'te dönüş sonu pop'u: sprint 180 0→3.62 cm, koşu 180 0→3.06 cm. Fuzz'da sprint 4.96→9.15 cm. 20 FPS'te bir kare üç kat uzun olduğu için bu rakamlar 60 FPS'e taşınmaz, ama üretimden kötü.
- 30 FPS'te dönüş pop sayısı 1→4 ve 0→4, yine de en kötü 1.58 ve 1.77 cm. Fuzz'da ise iyileşti: 6.22→3.46 ve 6.67→3.00.
- 120 FPS fuzz'da baş pop'u: tepe 180→375 ve 195→367 m/s², exc 1.14→1.72 ve 1.24→2.48 cm. Kafa katmanı kapalıyken de aynı değerler çıktı (364 ve 367 m/s², koşuda 2.48 cm), yani kaynak kafa katmanı değil, plan girişindeki klip geçişi. Kafa katmanını bu yüzden açık bıraktım.

## Eski sorunlar

| konu | durum | not |
|---|---|---|
| Ağırlıklı idle, durarak dönüş, başlangıç uyumu | değişmedi | Bu turda dokunulmadı. Regresyon pop'ları aynı |
| Yürüyüş duruşunda doğal oturma | değişmedi | Aynı |
| Ayak kayması ve batması | kısmen düzeldi | Salınım tabanı −5.2→+2.4 cm, koşu 90 17.4→8.7 cm, sprint 180 sol 8.1→13.3 cm kötü (sprint döngüsünde) |
| Koşu geçişinde alçak salınan ayak | düzeldi | Üretilen kliplerde ölçüldü. 90° klipleri yeniden üretildikten sonra ölçüm tekrarlanmadı |
| Düşük FPS başlangıç sorunu | değişmedi | 20 ve 30 FPS `wstart`: exc 3.36→3.40, 0→0. Görsel bakılmadı |
| Yüksek FPS pop'ları | karışık | Dönüş senaryolarında aynı veya daha iyi (155→126), fuzz'da baş pop'u kötüleşti |
| Sprint S geri koşusu | düzeldi | Sprint ve koşuda geri koşu 0 |
| Yürüyüş W→S | değişmedi | Geri yürüyüş sürüyor. `PSD_CR_Backward_Stand` aynı karede `Walk_Pivot` seçiyor. Teslim edilmedi |
| Eğimde dönüş | düzeldi | Gerçek rampa, üretimden iyi: 90° rampada exc 7.39→1.19 cm. Ayak teması eğimde ölçülemedi |
| Küçük yükseklik farkı | değişmedi | Dönüşten önceki basamak çıkışı pop'u iki yapıda da aynı (exc 11.5 ve 19.8 cm) |
| Merdiven | test edilmedi | Gerçek merdiven senaryosu yok |
| Duvar yakını | düzeldi | Üretim duvara karşı .8 s koşuyordu. Aday duruyor ve çıkıyor. `j40_wall` exc .64→1.54 cm, v≈1'de biraz kötü |
| Eğimde ve duvar yakınında kamera | test edilmedi | Yalnızca yan kamerayla bakıldı |
| Kamera iç mekânda | test edilmedi | `CamOpenness` ile kapanıyor, görsel doğrulanmadı |
| Omuzların eski kamera yönüne burulması | düzeldi | Sprintte −23.5°→+.8°, koşuda −5.7° (döngü −5.8°) |
| Koşuda bacakların kadrajda kalması | kısmen düzeldi | Dönüşe kadar tam gövde. Sonra kameraya doğru koşarken ayaklar alt kenara iniyor, kamera toparlanınca düzeliyor |
| Omuz ofseti ve çapraz açı | değişmedi | Dokunulmadı |

## Görsel inceleme

Videoları izleyemiyorum. Gerçek zaman damgalı kare dizilerine baktım, görsel PASS vermiyorum.

- **Üretim sprint 180:** kıyma adımlar ve bacak çaprazlaması. Koşu 180: geri koşu. Şikâyetin haklıydı.
- **Aday fren:** inandırıcı.
- **Aday 90° dönüşler:** sprint ve koşu iyi okunuyor.
- **Aday sprint 180 pivotu (5.80–6.00 s):** geniş, alçak duruş ve dışa açık dizler. Rampada da aynı. Yakalama kaynağı da bunu yapıyor, ama kaynak duran başlangıçtan geliyor, yani koşan bir dönüş için fazla alçak olabilir. **En büyük reddedilme riski bu.**
- **Aday koşu 180:** 5.90–6.10 s arasında geniş duruş, biraz tereddütlü.
- **Kollar:** 6.2–6.5 s'de öne uzanması sprint döngüsünün kol taşıması.

Aday hâlâ fuzz'da düşük hızda sprint stand pivotuna giriyor (v 30–75, pelvis 69→88 cm yükseliyor). Bu sınıf üretimde de var.

## Düzeltme

**V2.54 raporundaki videolar gerçek hızda değildi.** 60 fps yakalamaları 30 fps ile kodlanmıştı, yani yarı hızda oynuyorlardı ve ben onlara gerçek hız demiştim. Bu turun altı videosu 60 fps, gerçek hız. Karşılaştırma için önceki yorumlarımı bu hatayla birlikte oku.

## Açık kusurlar

1. Yürüyüşte W→S geri yürüyüş. Sonraki turun ilk işi.
2. Sprint 180 pivotunda geniş ve alçak duruş.
3. Düşük hızda tuş bırakma ve fare süpürmesi birlikte gelirse `A_CT_Jog_BwdLeft → Walk_Stop_BL` geçişi.
4. Yeni klip girişlerindeki pop'lar üretimden biraz yüksek, 60 FPS'te 1.5 cm altında.
5. Koşu faresinde kısa yanlış çalışma: t 23.20, v 53, en çok .18 s.
6. Kamera toparlanması beklerken ayaklar kadraj altına iniyor.
7. Editör: `GameViewport.IsUnique()` çökmesi bu turda bir kez oldu (30 FPS, PIE kapanışı). Yaklaşık 16–19 PIE'de bir görülen bilinen motor sorunu, V2.55 ile ilgisi yok. Zincir kaldığı yerden devam etti.

## Terfi ve geri alma

Terfi 2026-11-04 18:24'te manifest `v255_prom` ile yapıldı. Yedek sha1 ile doğrulandı. ABP, çocuk ABP, `BP_GR_Player` ve `BP_PBI_Player` derlendi. ABP'de durum `UP_TO_DATE_WITH_WARNINGS`: bu, önceden var olan `IsValid` iş parçacığı uyarısı. Kirli paket yok.

| geri alınacak şey | yol | durum |
|---|---|---|
| Tamamı | `req/rollback_req.py`, `data/promote255_before.json` değerlerini geri yazar | Hazır, denenmedi |
| Tamamı, ikili düzeyde | `checkpoint/manifests/v255_prom/` yedeği | Yedek doğrulandı |
| Yalnızca hız çerçevesi | `GR255_FrameOn` 0 | Düğme mevcut |
| Yalnızca kafa ve omuz katmanı | `SHM240_HeadOn` 0 | Düğme mevcut |
| Yalnızca dönüş ailesi | `SHM255_Ctl` 0 ve eski veritabanları | Ayak, başlangıç ve duruş kazanımlarına dokunmaz |

## Dosyalar

- `TABLES_V255.md`: bütün ölçüm tabloları
- `CHANGES_V255.md`: değişiklik listesi
- `vid/`: 6 önce/sonra video, 60 fps gerçek hız
- `sheets/`: kare dizileri
