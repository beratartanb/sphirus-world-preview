# SHME V2.53: frenleme sonrası yerleşme, yürüyüş kalkışında destek ayağı ve 180° sıçraması (2026-11-03)

**Taban:** V2.52 üretimi. Sayılar `TABLES_V253.md`, değişiklikler `CHANGES_V253.md` dosyasında.

**Ölçüm koşulları:**
- Önce/sonra karşılaştırmaları aynı oturumda ve aynı sabit adımlı karelerde yapıldı. "Önce" = V2.52 üretim değerleri (`pre` varyantı).
- Ardından 20 / 30 / 120 FPS ve gerçek zaman koşuları yapıldı.

**Görsel kabul:**
- Videoları oynatıp izleyemiyorum. Görsel kabul ve oyun hissi **NOT_TESTED**; görsel PASS verilmedi.
- Yalnızca tek kareleri kontrol ettim. Örneğin duruşta V2.53'te pelvis daha aşağıda ve dizler daha bükülü görünüyor.

**Videolar** (`vid/`, gerçek hız, 60 fps; solda V2.52, sağda V2.53, aynı oturum):
- `stop_settle_side` / `_diag` / `_gamecam`: koşudan duruş.
- `walkstart_side` / `_diag`: ileri-sağ yürüyüş kalkışı (destek ayağı).
- `turn180_diag`: 180° kalkış. Crop onarımı içerik olduğu için aynı oturumda kapatılamıyor; bu yüzden sol taraf V2.52 oturumunun kaydı.

## 1. Ağırlık aktarımı: doğrulama ve destek ayağı

### 1.1 Destek ayağının 10–24 cm'lik hareketi
Her kalkışta destek ayağının topu, topuğu, dönüşü ve havada geçen kareleri ayrı ölçüldü (`stance253.py`).

**İleri / yan kalkışlar (FR, LL, RL): kayma.**
- Destek ayağı hiç yerden kalkmıyor.
- İlk 0,2 s'de düz basarken ileri-geri 9–11 cm yüzüyor.
- Net yer değiştirme 4–5 cm, yol uzunluğu 25 cm.
- V2.51 içeriğinde de aynısı var; APA'dan kaynaklanmıyor.

**Geri kalkış (B): gerçek adım.**
- 12 cm'in büyük kısmı topuk pivotu (−30°) ve gerçek bir adım (30 cm havada).

**Sahibi: istek karesindeki vendor örneği.**
- İstek karesinde yürüyüş başlangıç rotası bir kare geç kalıyor.
- MM bu karede bir vendor veritabanında arama yapıyor (Dense_Stand_Walk_Loops / CR_Backward_Stand).
- Seçilen tek kare blend stack'te kalıyor ve kendi giriş ağırlığı bir sonraki klibin altında büyümeye devam ediyor: +0,2 s'de ~%25.
- FootPlacement kilidi kopuyor (ContactL false) ve ayak sürükleniyor.
- Kanıt: aşağıdaki düzeltmeyle topun kaydığı mesafe ~0'a iniyor ve FootPlacement kilidi kopmuyor (ContactL tüm kalkış boyunca true).

**Düzeltme (üretimde): `SHM253_WalkHold`.**
- Yalnızca hareketin ilk karesinde (zemin hızı < 5 cm/s), MM o anki veritabanında `DoNotInterrupt` ile arıyor.
- Duran poz bir kare devam ediyor; hatalı örnek blend stack'e girmiyor.
- Sonraki kare normal rota karar veriyor.

| Kalkış (destek ayağı topunun kayma mesafesi) | V2.52 | V2.53 |
|---|---|---|
| FR 30 / 60 / 120 / gerçek zaman | 25,0 / 23,7 / 21,8 / 25–26 cm | 2,6 / 2,6 / 2,5 / 2,3–2,7 cm |
| LL 30 / 60 / 120 | 13,3 / 15,8 / 13,0 | 0,2 / 0,2 / 0,2 |
| RL 60 / 120 | 11,1 / 13,0 | 3,2 / 2,6 |
| taps en kötü sıçrama (60) | 62 m/s² | 47 m/s² |
| wstart contact231 (60) | 30,7 | 20,6 |

**Kalan topuk hareketi (yalnızca 2–10 cm):**
- Topun etrafında topuğun dönmesi: 45° kalkışta −20°, RL'de +31°. Doğal pivot.

**Denenip üretime alınmayan alternatif: `SHM253_WalkEntry`.**
- V2.51'in koşu yöntemi: istek karesinde başlangıç veritabanında arama.
- Kaymayı da gideriyordu, ama bileşenin kısa dokunuş (tap) kararını atladı. Taps'ta başta 62 → 88 m/s² sıçrama oluştu.
- Kurulu ama kapalı.

**Bilinen sınırlar:**
- 20 FPS'te ilk karedeki hız zaten 6,6 cm/s olduğu için tutma devreye girmiyor. 20 FPS, V2.52 ile aynı kaldı (24–26 cm).
- Bedeli: 30/60 FPS'te kalkış 1 kare (17 ms) geç başlıyor.

### 1.2 APA telafisi farklı giriş fazlarında
**Ölçülenler:**
- Pelvis aktarımı doğru yönde.
- Gövde pelvisi izliyor; göğüs–pelvis yanal ofseti değişmiyor.
- Ayaklar yerinde.

**Yapay hareket sorunu:**
- Kısa ayak kalkışlı kalkışlarda (BL, RL, LL: 0,13–0,20 s) pelvisin yanal ivme tepesi 8–22'den 13–27 m/s²'ye çıkıyordu.

**Denenen çözüm: APA v3 (`gen253_apa.py`).**
- Minimum-jerk profil ve görünür ivme sınırı 3 m/s².
- 14 klip ve 2 veritabanı üretildi, test edildi.
- Sonuç: ivme ancak 0–2 m/s² düştü, aktarım azaldı (t 0,29–0,36 → 0,34–0,43).

**Karar:** WalkHold ile V2.52 APA'nın yanal ivmesi V2.52 seviyesinde ya da altında kaldı (wstart 8,5–22,2 m/s²). Aktarım korundu (t 0,29–0,36). APA v3 üretime alınmadı.

### 1.3 V2.52 "regresyonları"
- **gait batma 2,2 → 2,8:** ölçüm hatası. Topun mutlak minimum yüksekliği koşularda birebir aynı (−4,62 / −3,64 cm). Yalnızca ilk saniyedeki ayakta durma zemin tahmini farklıydı. Gerçek batma yok.
- **wstart 23,5 → 30,7:** APA değil. Kalkıştan sonraki SHM245_Walk_Fwd döngüsünün itişi (ayak topu itişte −1,9 cm iniyor, sonra hızla kalkıyor) iki kare farklı fazda yakalandı. contact231 bu hızlı alçak salınımı kayma sayıyor. V2.53'te 60 FPS'te 20,6.
- **Gerçek zamanda aynı olay 47–51 cm ölçüldü (V2.52'de 19,8–22,4):** gerçek zamanda RL kalkışı sol ayakla seçildi ve döngüye farklı fazda girildi. contact250 PLANT ise iyileşti (15,6 → 11,5–13,1). Döngünün itişindeki ayak ucu alçaklığı açık.

## 2. 180° geçişindeki omuz sıçraması: çözüldü (60 FPS)
**Katman kapatma testleri:**
- Steering, StrideWarping, OffsetRootBone, Inertialization ve DeadBlending tek tek kapatıldı (V2.52'de OW ve FP de kapatılmıştı). Sıçrama hiçbirinde değişmedi.
- Sıradaki klip farklı olsa bile değişmedi: F_Lfoot 79, CP2 72.

**Gerçek sahip: içerik.**
- `SHM248_Jog_Start_TurnR180_crop`'un 0,900 s anahtar karesi, dönüşün yaw'ının bittiği kare.
- Bu karede üst gövdenin bütün segmentlerinin hızı aynı anda değişiyor (kök çerçevesinde):

| Segment | 0,900 s karesi | Komşu kareler |
|---|---|---|
| omuz–köprücük | 34 cm/s | 2–14 cm/s |
| gövde–pelvis | 32 cm/s | 2–14 cm/s |
| baş | 18 cm/s | 2–14 cm/s |

- Oyunda crop 1,12x hızla oynuyor ve bu kareye tam 15,033'te ulaşıyor.
- Servo bırakması aynı karede, çünkü dönüş orada bitiyor. Bırakma sahip değil, sadece eş zamanlı.
- R135 crop'unda da aynı kırılma var.

**Düzeltme (içerik, manifest yedekli, `fix253_cropkink.py`):**
- k−1..k+1 karelerinde pelvis ve üst gövde yerel dönüşleri, k−2 ile k+2 arasında C1 Hermite ile yeniden anahtarlandı.
- Bacaklar her karede ayağın orijinal yerine yeniden çözüldü (ayak hatası 0).
- Sonuç: omuz–köprücük 34 → 6, gövde–pelvis 32 → 14, baş 18 → 7 cm/s.

| 15,02 sıçraması | V2.52 | V2.53 |
|---|---|---|
| 60 FPS | 79 m/s² (omuz 1,54 cm) | 39 m/s² (omuz 0,42 cm) |
| 120 FPS | 103 | 79 |
| gerçek zaman | 46 | 26 |
| 30 FPS | 26 | eşik altı |

**Not:** 120 FPS'te 79 hâlâ yüksek. 30 fps anahtarlar 120'de doğrusal enterpolasyonla oynatıldığı için her anahtar kırılması 4 kat görünüyor; kalan değer bu sınıftan.

### 2.1 120 FPS koşu döngüsünde ayak ucu: incelendi, açık
**Ne oluyor:**
- Ayak ucu sürtünmüyor. Jog_Left_Start → A_CT_Jog_FwdLeft geçişinde sağ ayağın topu, salınımın ortasında 7–11 m/s hızla zemine değiyor (−2 cm), yeniden kalkıyor (+3,8 cm) ve 0,15 s sonra iniyor.
- 60 FPS'te de aynı; mannequin pozunda da var.

**Elenenler:**
- FootPlacement: kapalıyken −1,5 cm, hâlâ zemin altında.
- StrideWarping: kapalıyken birebir aynı.
- FPS: 60 ve 120'de aynı.

**Klip verisi:** döngünün kendi salınım açıklığı ~3 cm. Salınım-çukuru onarımı (`fix253_swingdip.py`) yalnızca 0,3–0,5 cm kaldıracaktı; yazılmadı.

**Kalan sahip:** oyundaki salınım her iki klipten 2–5 cm daha alçak geçiyor, yani geçişteki blend-stack bileşimi. Bu turda düzeltilmedi.

## 3. Yeni davranış: frenleme sonrası denge yerleşmesi (üretimde)
**Ölçülen eksik:**
- 24 kutuluk koşu duruşu ailesinde ayaklar yere bastığı anda pelvis tamamen durmuş (sonrasında ileri hareket 0, yüklenme 0–1,2 cm).
- Göğüs, baş ve omuz da onunla birlikte duruyordu; beden makine gibi varıyordu.

**Yeni içerik:** `SHM253_JogStop_*` (24 klip) ve `PSD_SHM253_JogStop`.
- Kaynak klipler ve veritabanı değiştirilmedi.
- Her klibin kendi kök frenleme ivmesiyle sürülen ikinci derece sönümlü tepkiler eklendi.
- Sürücü u = −a/410 cm/s². Tepki hızla değil ivmeyle ölçekleniyor; hafif duruşta küçük, sert duruşta büyük.

| Segment | Tepki | Parametreler |
|---|---|---|
| Kalça/diz yüklenmesi | pelvis 2,8 cm iner, son basışta küçük bir emilim | T 0,5 s, ζ 0,62 |
| Pelvis | frenlemede ~1,9 cm geride, durunca küçük bir ileri dönüş | — |
| Gövde | 5,8° öne fleksiyon; üst omurga 0,04 s gecikmeli | T 0,7 s |
| Baş | 0,08 s gecikmeyle karşı yönde toparlanır (bakış seviyelenir) | — |
| Kollar | ileri salınım, 0,08 s gecikmeli | — |

- Ayaklar kaynağın yerinde (hata 0; diz menteşe çözücüsü).
- Bacak koruması (leg guard) temiz.
- Tepki, klibin idle devralma anında (SHM_StopSettle düştüğünde) tam sıfıra iniyor. Böylece idle devralırken alınan alt gövde anlık görüntüsü yerleşmiş duruşu yakalıyor.

**İlk deneme (klibi 0,9 s uzatmak) geri alındı:**
- Uzun statik kuyruklar yeni veritabanının kendi normalizasyonunu değiştirdi.
- MM girişte üç kutu atladı ve bir ayakta 10,9 cm kayma oluştu.
- v2'de klip uzunluğu korundu.

**Düzeltme adımı gerekmedi:**
- Son basışta tahmini kütle merkezi (XCoM) her kutuda destek alanı içinde: topuk tarafı 5–9 cm, top tarafı 14–16 cm pay.
- Gerekli kapanış adımı ailenin içinde zaten var.

**Oyunda sonuç** (60 FPS, aynı kareler, V2.53 eksi V2.52, 9 duruş):

| | Fark | Zaman |
|---|---|---|
| Pelvis yüksekliği (diz/kalça yüklenmesi) | 2,5–2,6 cm daha aşağı | +0,22–0,30 s |
| Omuzlar pelvise göre | 2,5–3,0 cm daha önde | +0,33–0,47 s |
| Baş pelvise göre | 3,6–4,4 cm daha önde | +0,35–0,47 s |

- Sıralama: önce pelvis, sonra omuzlar, en son baş. Segmentler aynı karede durmuyor.
- Hepsi ~0,9–1,0 s'de V2.52 duruşuna geri yakınsıyor; sürekli sallanma yok.
- Temas: j36_stop BALL 4,1/4,8 aynı, contact231 6,7 → 6,8. j36_stopb'de bir ayakta top 7,7 → 8,4 cm, contact231 6,7 → 8,0 (küçük artış).
- Sıçrama sayıları aynı.
- 20/30/120 FPS ve gerçek zamanda seçim doğru (SHM253 klipleri). Bu FPS'lerde eşli fark yalnızca 60'ta ölçüldü.

**Kapsam:** yalnızca koşu duruşu ailesi.
- Yürüyüş duruşları (CP evaluator'ın oynattığı walk stop'lar) bu turda değiştirilmedi.
- Bu yüzden "hafif duruşta küçük yerleşme" oyunda henüz görünmüyor; model ivmeye göre ölçekli ama yalnızca 3 m/s'lik koşu duruşunda uygulandı.

## 4. Ağırlıklı idle: kapalı kaldı
WalkHold (veya WalkEntry) ile birlikte denendi, sonuçlar:

| Senaryo | V2.53 üretim | Ağırlıklı idle ile |
|---|---|---|
| w43_idle sıçrama | 39 | 26 (iyi) |
| wstart contact231 | — | 37,2 (kötü) |
| w42 PLANT | 5,9 | 12,8 cm (kötü) |
| gait sıçrama | 52 | 70 m/s² (kötü) |

Kural gereği açılmadı.

## 5. Görev dağılımı (yeni paralel sistem yok)
- **MM:** klip seçimi. WalkHold yalnızca istek karesinde mevcut veritabanında arama yaptırıyor.
- **SHME:** destek tarafı ve aile rotası; değişmedi.
- **Animasyon içeriği:** duruş tepkisi (24 klip) ve crop onarımı.
- **IK/FootPlacement:** temas. Yerleşme sırasında pelvis zaten klipteydi (V2.37 SHM237_FPPelvisOff).

## 6. Disk
- Saklama listesi doğrulandı:
  - Tutulan turlar 250–253, koruma listesi, checkpoint/data, .md ve .uasset dosyaları listede yok.
  - V250/V251 yayın kopyaları hariç tutuldu.
- 4047 öğe (13,39 GB) Geri Dönüşüm Kutusu'na taşındı (0 hata). Kayıt: `Saved/Codex/Retention/recycle253_log.txt`.
- Kalıcı silme yapılmadı. Alan, Geri Dönüşüm Kutusu boşaltılınca açılır.

## 7. Açık kalanlar
- Koşu döngüsü geçişindeki salınım ayağının zemine değmesi (§2.1).
- SHM245_Walk_Fwd itişindeki alçak ayak ucu; gerçek zamanda wstart contact231 47–51 (§1.3).
- 20 FPS'te WalkHold devreye girmiyor.
- Yürüyüş duruşlarına yerleşme.
- Ağırlıklı idle.
- Lateral (LR) kalkışta gerçek zamanda destek ayağının 29–30 cm hareketi. V2.52'de 35 cm idi; sabit adımda bu kalkış seçilmiyor.
